#!/usr/bin/env python3
"""Check the plan prices in data/plans.yaml against the provider pages.

The script fetches every page a plan record cites under a `pricing` or `plans`
link, extracts the text, and reports two signals. The first signal is price
presence: does the page still state the amount the record claims? The script
extracts only currency-marked prices, so a bare number never counts as a match.
The second signal is a snapshot diff against the previous run.

The script never edits any file under data/. It writes only under .plan-drift/.
"""

from __future__ import annotations

import argparse
import difflib
import html
import json
import re
import sys
import urllib.error
import urllib.request
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path
from typing import Final

REPO_ROOT: Final = Path(__file__).resolve().parents[4]
PLANS_PATH: Final = REPO_ROOT / "data" / "plans.yaml"
SNAPSHOT_DIR: Final = REPO_ROOT / ".plan-drift"
SKILLS_DIR: Final = REPO_ROOT / ".claude" / "skills"

PRICE_LABELS: Final[frozenset[str]] = frozenset({"pricing", "plans"})
MIN_TEXT_LENGTH: Final = 400
DEFAULT_TIMEOUT: Final = 30
USER_AGENT: Final = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
BLOCKED_HTTP_CODES: Final[frozenset[int]] = frozenset({401, 403})
CHALLENGE_MARKERS: Final[tuple[str, ...]] = ("cdn-cgi", "enable javascript")

STATUS_OK: Final = "OK"
STATUS_NO_PRICES: Final = "NO PRICES FOUND"
STATUS_BLOCKED: Final = "BLOCKED"
STATUS_UNREADABLE: Final = "UNREADABLE"
STATUS_ERROR: Final = "ERROR"

EXIT_CLEAN: Final = 0
EXIT_ATTENTION: Final = 1
EXIT_FAILURE: Final = 2

PROVIDER_POINTERS: Final[dict[str, str]] = {
    "Alibaba (Qwen)": ".claude/skills/provider-alibaba/scripts/read_tables.py",
    "BytePlus": ".claude/skills/provider-byteplus/scripts/query_price.py",
    "Cursor": ".claude/skills/provider-cursor/scripts/read_yearly_prices.py",
    "Devin": ".claude/skills/provider-devin/scripts/model_rates.py",
    "Moonshot (Kimi)": ".claude/skills/provider-moonshot/scripts/read_plans.py",
    "Novita": ".claude/skills/provider-novita/scripts/read_coding_plan.py",
    "Zhipu (GLM)": ".claude/skills/provider-zai/scripts/read_subscribe.py",
}

SCRIPT_BLOCK_RE: Final = re.compile(
    r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL
)
TAG_RE: Final = re.compile(r"<[^>]+>")
WHITESPACE_RE: Final = re.compile(r"\s+")
SLUG_UNSAFE_RE: Final = re.compile(r"[^a-z0-9]+")

MIN_PRICE_TOKENS: Final = 2
AMOUNT_TOLERANCE: Final = 0.005
PERIOD_DIVISORS: Final[dict[str, int]] = {"quarter": 3, "year": 12}

_NUMBER: Final = r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?"
_SYMBOL: Final = r"(?:US\$|CA\$|A\$|NZ\$|S\$|HK\$|RMB|\$|¥|€|£|₹)"
_CODE: Final = r"(?:USD|CNY|EUR|GBP|JPY|RMB|INR|AUD|CAD|SGD|HKD)"
_UNIT: Final = r"(?:user|users|seat|seats|member|members|editor|editors|person)"
_PERIOD: Final = (
    r"(?:mo\b|mo\.|month|months|monthly|yr\b|yr\.|year|years|yearly|annually|"
    r"annum|quarter|quarterly|" + _UNIT + r")"
)
_SEPARATOR: Final = r"(?:/|\bper\b|\ba\b|\beach\b)"

PRICE_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    # $20, US$20, ¥199, €30, £25
    re.compile(rf"{_SYMBOL}\s?({_NUMBER})", re.IGNORECASE),
    # 20 USD, 199 CNY
    re.compile(rf"({_NUMBER})\s?{_CODE}\b", re.IGNORECASE),
    # USD 20, CNY 199
    re.compile(rf"\b{_CODE}\s?({_NUMBER})", re.IGNORECASE),
    # 20 / mo, 20/month, 20 per month, 20 / user / mo, 20 per seat per month
    re.compile(
        rf"({_NUMBER})\s*{_SEPARATOR}\s*(?:{_UNIT}\s*{_SEPARATOR}\s*)?{_PERIOD}",
        re.IGNORECASE,
    ),
)


class PlanDriftError(Exception):
    """The script cannot continue."""


@dataclass(frozen=True)
class PageResult:
    """One fetched URL and how it turned out."""

    url: str
    status: str
    text: str = ""
    variant: str = "plain"
    detail: str = ""
    prices: frozenset[float] = frozenset()

    @property
    def is_readable(self) -> bool:
        """Report whether the page yielded prices the script can compare."""
        return self.status == STATUS_OK

    @property
    def has_text(self) -> bool:
        """Report whether the page yielded text worth snapshotting."""
        return self.status in (STATUS_OK, STATUS_NO_PRICES)


@dataclass(frozen=True)
class PriceCheck:
    """One amount from one record, looked for on one page."""

    record_id: str
    provider: str
    plan: str
    period: str
    amount: float
    currency: str
    url: str
    found: bool
    match_note: str = ""


@dataclass(frozen=True)
class SnapshotDiff:
    """How far one page moved since the last run."""

    url: str
    changed_lines: int
    is_new_baseline: bool


@dataclass
class Report:
    """Everything one run learned."""

    checked_records: int = 0
    checked_urls: int = 0
    price_checks: list[PriceCheck] = field(default_factory=list)
    pages: list[PageResult] = field(default_factory=list)
    diffs: list[SnapshotDiff] = field(default_factory=list)
    unreadable_pointers: list[dict[str, str]] = field(default_factory=list)

    @property
    def missing(self) -> list[PriceCheck]:
        return [check for check in self.price_checks if not check.found]

    @property
    def changed_diffs(self) -> list[SnapshotDiff]:
        return [d for d in self.diffs if d.changed_lines > 0 and not d.is_new_baseline]

    @property
    def needs_attention(self) -> bool:
        return bool(self.missing) or bool(self.changed_diffs)


def load_plans(path: Path) -> list[dict[str, object]]:
    """Read data/plans.yaml and return its records."""
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment problem
        raise PlanDriftError("PyYAML is missing. Run pip install -r requirements.txt.") from exc
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PlanDriftError(f"{path} does not exist.") from exc
    except yaml.YAMLError as exc:
        raise PlanDriftError(f"{path} is not valid YAML: {exc}") from exc
    if not isinstance(raw, list):
        raise PlanDriftError(f"{path} must parse to a list of records.")
    return raw


def select_records(
    records: Sequence[dict[str, object]], provider: str | None
) -> list[dict[str, object]]:
    """Keep the records for one provider, or all records.

    An exact name wins. When no name matches exactly, fall back to a substring,
    so `Zhipu` still selects `Zhipu (GLM)`.
    """
    if provider is None:
        return list(records)
    wanted = provider.strip().casefold()
    exact = [r for r in records if str(r.get("provider", "")).casefold() == wanted]
    if exact:
        return exact
    return [r for r in records if wanted in str(r.get("provider", "")).casefold()]


def price_urls(record: dict[str, object]) -> list[str]:
    """Return the URLs of a record that state a price."""
    links = record.get("links") or []
    if not isinstance(links, list):
        return []
    urls: list[str] = []
    for link in links:
        if not isinstance(link, dict):
            continue
        if str(link.get("label", "")) in PRICE_LABELS:
            url = str(link.get("url", ""))
            if url:
                urls.append(url)
    return urls


def unique_urls(records: Iterable[dict[str, object]]) -> list[str]:
    """Collect every price URL once, in first-seen order."""
    seen: dict[str, None] = {}
    for record in records:
        for url in price_urls(record):
            seen.setdefault(url, None)
    return list(seen)


def html_to_text(body: str) -> str:
    """Turn an HTML body into plain text without a third-party parser."""
    without_blocks = SCRIPT_BLOCK_RE.sub(" ", body)
    without_tags = TAG_RE.sub(" ", without_blocks)
    return WHITESPACE_RE.sub(" ", html.unescape(without_tags)).strip()


def looks_challenged(body: str) -> bool:
    """Report whether the body carries a bot-challenge marker."""
    lowered = body.casefold()
    return any(marker in lowered for marker in CHALLENGE_MARKERS)


def fetch_once(url: str, timeout: int) -> tuple[str, str]:
    """Fetch one URL. Return the status and the body or the error text."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        if exc.code in BLOCKED_HTTP_CODES:
            return STATUS_BLOCKED, f"HTTP {exc.code}"
        return STATUS_ERROR, f"HTTP {exc.code} {exc.reason}"
    except urllib.error.URLError as exc:
        return STATUS_ERROR, f"{type(exc).__name__}: {exc.reason}"
    except (TimeoutError, OSError, ValueError) as exc:
        return STATUS_ERROR, f"{type(exc).__name__}: {exc}"
    return STATUS_OK, raw.decode("utf-8", errors="replace")


def markdown_twin(url: str) -> str:
    """Return the `.md` twin of a URL."""
    base, _, query = url.partition("?")
    twin = f"{base.rstrip('/')}.md"
    return f"{twin}?{query}" if query else twin


def classify(url: str, timeout: int) -> PageResult:
    """Fetch one URL and give it exactly one status."""
    status, body = fetch_once(url, timeout)
    if status == STATUS_BLOCKED:
        return PageResult(url, STATUS_BLOCKED, detail=body)
    if status == STATUS_OK and looks_challenged(body):
        return PageResult(url, STATUS_BLOCKED, detail="challenge marker in body")
    if status == STATUS_OK:
        text = html_to_text(body)
        if len(text) >= MIN_TEXT_LENGTH:
            return apply_price_gate(PageResult(url, STATUS_OK, text=text))
    return retry_markdown(url, timeout, first_status=status, first_detail=body)


def apply_price_gate(page: PageResult) -> PageResult:
    """Downgrade a readable page that states too few prices to compare.

    Such a page renders its prices client-side. One honest line beats one
    MISSING row per amount.
    """
    prices = extract_prices(page.text)
    if len(prices) >= MIN_PRICE_TOKENS:
        return replace(page, prices=prices)
    return replace(
        page,
        status=STATUS_NO_PRICES,
        prices=prices,
        detail=f"price tokens extracted from the page text: {len(prices)}",
    )


def retry_markdown(
    url: str, timeout: int, *, first_status: str, first_detail: str
) -> PageResult:
    """Retry a failed or thin fetch against the `.md` twin."""
    twin = markdown_twin(url)
    status, body = fetch_once(twin, timeout)
    if status == STATUS_OK and not looks_challenged(body):
        text = html_to_text(body)
        if len(text) >= MIN_TEXT_LENGTH:
            return apply_price_gate(
                PageResult(url, STATUS_OK, text=text, variant="markdown twin")
            )
    if first_status == STATUS_ERROR:
        return PageResult(url, STATUS_ERROR, detail=first_detail)
    return PageResult(
        url, STATUS_UNREADABLE, detail="text under 400 characters after both attempts"
    )


def normalize_number(raw: str) -> float | None:
    """Turn a captured price string into a float, or None when it will not parse.

    Handles both `1,234.56` and `1.234,56`. A single separator followed by
    exactly three digits is a thousands separator, not a decimal point.
    """
    text = raw.strip()
    if not text:
        return None
    has_comma, has_dot = "," in text, "." in text
    if has_comma and has_dot:
        decimal_sep = "," if text.rindex(",") > text.rindex(".") else "."
        thousands_sep = "." if decimal_sep == "," else ","
        text = text.replace(thousands_sep, "").replace(decimal_sep, ".")
    elif has_comma or has_dot:
        separator = "," if has_comma else "."
        head, _, tail = text.rpartition(separator)
        # `1,200` is twelve hundred, but `0.031` is a fraction, not `31`.
        is_thousands = len(tail) == 3 and head != "" and not head.startswith("0")
        text = text.replace(separator, "") if is_thousands else text.replace(separator, ".")
    try:
        return float(text)
    except ValueError:
        return None


def extract_prices(text: str) -> frozenset[float]:
    """Collect every number on the page that carries a currency or period marker.

    A bare number is never a price. `18` inside a token count and `20` inside
    `2026` must not match a plan amount, so only marked numbers get through.
    """
    found: set[float] = set()
    for pattern in PRICE_PATTERNS:
        for match in pattern.finditer(text):
            value = normalize_number(match.group(1))
            if value is not None:
                found.add(value)
    return frozenset(found)


def same_amount(left: float, right: float) -> bool:
    """Compare two amounts within the tolerance."""
    return abs(left - right) < AMOUNT_TOLERANCE


def match_amount(amount: float, period: str, prices: frozenset[float]) -> str | None:
    """Return a note describing how the amount matched, or None when it did not.

    A quarter or year `amount` is a term total that the repository derives.
    A provider often prints only the monthly rate, so accept that equivalent too.
    """
    if any(same_amount(amount, price) for price in prices):
        return "matched as term total"
    divisor = PERIOD_DIVISORS.get(period)
    if divisor is None:
        return None
    equivalent = round(amount / divisor, 2)
    if any(same_amount(equivalent, price) for price in prices):
        return f"matched as monthly equivalent {equivalent:g}"
    return None


def check_prices(record: dict[str, object], page: PageResult) -> Iterator[PriceCheck]:
    """Compare every amount of one record against the prices on one page."""
    prices = record.get("prices") or []
    if not isinstance(prices, list):
        return
    for entry in prices:
        if not isinstance(entry, dict):
            continue
        amount = entry.get("amount")
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            continue
        period = str(entry.get("period", ""))
        note = match_amount(float(amount), period, page.prices)
        yield PriceCheck(
            record_id=str(record.get("id", "")),
            provider=str(record.get("provider", "")),
            plan=str(record.get("plan", "")),
            period=period,
            amount=amount,
            currency=str(record.get("price_currency", "")),
            url=page.url,
            found=note is not None,
            match_note=note or "",
        )


def url_slug(url: str) -> str:
    """Derive a stable file name from a URL."""
    stripped = re.sub(r"^https?://", "", url).casefold()
    slug = SLUG_UNSAFE_RE.sub("-", stripped).strip("-")
    return slug[:120] or "page"


def diff_snapshot(page: PageResult, *, write_only: bool) -> SnapshotDiff | None:
    """Compare a page against its snapshot, then write the fresh text."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{url_slug(page.url)}.txt"
    fresh = page.text
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    path.write_text(fresh, encoding="utf-8")
    if write_only:
        return None
    if previous is None:
        return SnapshotDiff(page.url, changed_lines=0, is_new_baseline=True)
    changed = sum(
        1
        for line in difflib.unified_diff(
            previous.splitlines(), fresh.splitlines(), lineterm=""
        )
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
    )
    return SnapshotDiff(page.url, changed_lines=changed, is_new_baseline=False)


def provider_slug(provider: str) -> str:
    """Derive a skill directory slug from a provider name."""
    base = provider.split("(")[0]
    return base.casefold().replace(" ", "").replace(".", "")


def pointer_for(provider: str) -> str:
    """Return the skill path that already knows how to read this provider."""
    mapped = PROVIDER_POINTERS.get(provider)
    if mapped is not None:
        return mapped if (REPO_ROOT / mapped).exists() else missing_pointer(provider)
    derived = f".claude/skills/provider-{provider_slug(provider)}/SKILL.md"
    return derived if (REPO_ROOT / derived).exists() else missing_pointer(provider)


def missing_pointer(provider: str) -> str:
    """Describe where to look when no skill file exists."""
    return f"no skill file on disk — look under .claude/skills/ for {provider}"


def run_check(*, provider: str | None, timeout: int, update_snapshots: bool) -> Report:
    """Fetch every cited page once and build the report."""
    records = select_records(load_plans(PLANS_PATH), provider)
    report = Report(checked_records=len(records))
    pages: dict[str, PageResult] = {}
    for url in unique_urls(records):
        pages[url] = classify(url, timeout)
    report.checked_urls = len(pages)
    report.pages = list(pages.values())

    for page in report.pages:
        if not page.has_text:
            continue
        diff = diff_snapshot(page, write_only=update_snapshots)
        if diff is not None:
            report.diffs.append(diff)

    seen_pointers: set[tuple[str, str]] = set()
    for record in records:
        for url in price_urls(record):
            page = pages[url]
            if page.is_readable:
                report.price_checks.extend(check_prices(record, page))
                continue
            key = (str(record.get("provider", "")), url)
            if key in seen_pointers:
                continue
            seen_pointers.add(key)
            report.unreadable_pointers.append(
                {
                    "provider": key[0],
                    "url": url,
                    "status": page.status,
                    "detail": page.detail,
                    "pointer": pointer_for(key[0]),
                }
            )
    return report


FOOTER: Final = (
    "This script never edits any file under data/. It writes only under .plan-drift/."
)


def render_attention(report: Report, lines: list[str]) -> None:
    """Write the rows that need a human."""
    missing = report.missing
    lines.append(f"MISSING PRICE ({len(missing)})")
    if not missing:
        lines.append("  none")
    for check in missing:
        lines.append(
            f"  {check.record_id} | {check.plan} | {check.period} "
            f"{check.currency} {check.amount:g} | {check.url}"
        )
    if missing:
        lines.append(
            "  MISSING is a hint, not proof of a price change. Open the page and read it."
        )
    lines.append("")

    equivalents = [
        c for c in report.price_checks if c.found and "equivalent" in c.match_note
    ]
    if equivalents:
        lines.append(f"MATCHED AS MONTHLY EQUIVALENT ({len(equivalents)})")
        for check in equivalents:
            lines.append(
                f"  {check.record_id} | {check.plan} | {check.period} "
                f"{check.currency} {check.amount:g} | {check.match_note}"
            )
        lines.append("  The page states the monthly rate, not the term total.")
        lines.append("")

    changed = report.changed_diffs
    lines.append(f"CHANGED SNAPSHOT ({len(changed)})")
    if not changed:
        lines.append("  none")
    for diff in changed:
        lines.append(f"  {diff.changed_lines} changed lines | {diff.url}")
    lines.append("")


def render_unreadable(report: Report, lines: list[str]) -> None:
    """Write the pages the script could not read a price from."""
    for status in (STATUS_NO_PRICES, STATUS_BLOCKED, STATUS_UNREADABLE, STATUS_ERROR):
        rows = [p for p in report.unreadable_pointers if p["status"] == status]
        lines.append(f"{status} ({len(rows)})")
        if not rows:
            lines.append("  none")
        for row in rows:
            lines.append(f"  {row['provider']} | {row['url']}")
            if row["detail"]:
                lines.append(f"    detail: {row['detail']}")
            lines.append(f"    read it with: {row['pointer']}")
        lines.append("")


def render_summary(report: Report, lines: list[str]) -> None:
    """Write the counts for everything that looks unchanged."""
    found = len(report.price_checks) - len(report.missing)
    baselines = sum(1 for d in report.diffs if d.is_new_baseline)
    steady = len(report.diffs) - baselines - len(report.changed_diffs)
    ok_pages = sum(1 for p in report.pages if p.is_readable)
    lines.append("UNCHANGED")
    lines.append(f"  price amounts still stated on their page: {found}")
    lines.append(f"  pages identical to their snapshot: {steady}")
    lines.append(f"  pages recorded as NEW BASELINE: {baselines}")
    lines.append(f"  pages that stated prices: {ok_pages} of {report.checked_urls}")
    lines.append("")


def render_text(report: Report) -> str:
    """Build the whole text report."""
    lines = [
        f"Plan drift report — {date.today().isoformat()}",
        f"{report.checked_records} plan records, {report.checked_urls} unique pages",
        "",
    ]
    render_attention(report, lines)
    render_unreadable(report, lines)
    render_summary(report, lines)
    lines.append(FOOTER)
    return "\n".join(lines)


def render_json(report: Report) -> str:
    """Build the whole report as JSON."""
    payload = {
        "date": date.today().isoformat(),
        "checked_records": report.checked_records,
        "checked_urls": report.checked_urls,
        "footer": FOOTER,
        "pages": [
            {
                "url": p.url,
                "status": p.status,
                "variant": p.variant,
                "detail": p.detail,
                "text_length": len(p.text),
                "prices_extracted": sorted(p.prices),
            }
            for p in report.pages
        ],
        "price_checks": [
            {
                "id": c.record_id,
                "provider": c.provider,
                "plan": c.plan,
                "period": c.period,
                "amount": c.amount,
                "currency": c.currency,
                "url": c.url,
                "result": "FOUND" if c.found else "MISSING",
                "match_note": c.match_note,
            }
            for c in report.price_checks
        ],
        "snapshots": [
            {
                "url": d.url,
                "result": "NEW BASELINE" if d.is_new_baseline else "DIFF",
                "changed_lines": d.changed_lines,
            }
            for d in report.diffs
        ],
        "unreadable": report.unreadable_pointers,
        "needs_attention": report.needs_attention,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Read the command line."""
    parser = argparse.ArgumentParser(
        prog="check_plan_drift.py",
        description=(
            "Check the plan prices in data/plans.yaml against the pages they cite. "
            "The script writes only under .plan-drift/ and never edits data/."
        ),
    )
    parser.add_argument("--provider", help="Check one provider only. Case-insensitive.")
    parser.add_argument(
        "--json", action="store_true", help="Emit the report as JSON on stdout."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Fetch timeout in seconds. Default {DEFAULT_TIMEOUT}.",
    )
    parser.add_argument(
        "--update-snapshots",
        action="store_true",
        help="Write snapshots and skip the diff section. Use it for a first baseline.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run one check and print the report."""
    args = parse_args(argv)
    if args.timeout <= 0:
        print("--timeout must be a positive number of seconds.", file=sys.stderr)
        return EXIT_FAILURE
    try:
        report = run_check(
            provider=args.provider,
            timeout=args.timeout,
            update_snapshots=args.update_snapshots,
        )
    except PlanDriftError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_FAILURE
    print(render_json(report) if args.json else render_text(report))
    return EXIT_ATTENTION if report.needs_attention else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
