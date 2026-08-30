#!/usr/bin/env python3
"""Detect drift between data/plans.yaml and the price a provider states online.

For every plan record the script fetches the pages the record cites, finds the
tier name on the page, reads the price stated next to that name, and compares it
against the stored amount. Every stored amount lands in exactly one verdict:
MATCH, DRIFT, or CANNOT COMPARE.

CANNOT COMPARE is a first-class result. An amount the script cannot read online
must never look like a MATCH.

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
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path
from typing import Final

REPO_ROOT: Final = Path(__file__).resolve().parents[4]
PLANS_PATH: Final = REPO_ROOT / "data" / "plans.yaml"
SNAPSHOT_DIR: Final = REPO_ROOT / ".plan-drift"

PRICE_LABELS: Final[frozenset[str]] = frozenset({"pricing", "plans"})
MIN_TEXT_LENGTH: Final = 400
MIN_PRICE_TOKENS: Final = 2
WINDOW_RADIUS: Final = 200
MAX_PAIR_DISTANCE: Final = 120
MAX_PLAUSIBLE_FACTOR: Final = 10
PERIOD_LOOKAHEAD: Final = 24
AMOUNT_TOLERANCE: Final = 0.005
PERIOD_DIVISORS: Final[dict[str, int]] = {"quarter": 3, "year": 12}
DEFAULT_TIMEOUT: Final = 30

USER_AGENT: Final = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
BLOCKED_HTTP_CODES: Final[frozenset[int]] = frozenset({401, 403})
CHALLENGE_MARKERS: Final[tuple[str, ...]] = ("cdn-cgi", "enable javascript")

STATUS_OK: Final = "OK"
STATUS_NO_PRICES: Final = "NO PRICES"
STATUS_BLOCKED: Final = "BLOCKED"
STATUS_UNREADABLE: Final = "UNREADABLE"
STATUS_ERROR: Final = "ERROR"

VERDICT_MATCH: Final = "MATCH"
VERDICT_DRIFT: Final = "DRIFT"
VERDICT_CANNOT: Final = "CANNOT COMPARE"

REASON_BLOCKED: Final = "page blocked"
REASON_CLIENT_SIDE: Final = "page renders client-side"
REASON_NO_PRICES: Final = "page states no prices"
REASON_NO_TIER: Final = "tier name not found on page"
REASON_NO_NEARBY: Final = "no price near the tier name"
REASON_CURRENCY: Final = "page states prices in another currency"
REASON_FETCH: Final = "fetch failed"
REASON_TOO_FAR: Final = "tier name and price are too far apart"
REASON_IMPLAUSIBLE: Final = "candidate prices are implausible for this tier"
REASON_FREE: Final = "free tier prints no price"
REASON_MONTHLY_ONLY: Final = "page states only the monthly rate for this tier"

# A higher rank carries more information, so it wins when pages disagree.
REASON_RANK: Final[dict[str, int]] = {
    REASON_FETCH: 1,
    REASON_BLOCKED: 2,
    REASON_CLIENT_SIDE: 3,
    REASON_NO_PRICES: 4,
    REASON_NO_TIER: 5,
    REASON_NO_NEARBY: 6,
    REASON_TOO_FAR: 7,
    REASON_CURRENCY: 8,
}
# These reasons describe the page, not the row, so they earn a skill pointer.
PAGE_LEVEL_REASONS: Final[frozenset[str]] = frozenset(
    {REASON_BLOCKED, REASON_CLIENT_SIDE, REASON_NO_PRICES, REASON_FETCH}
)

EXIT_CLEAN: Final = 0
EXIT_DRIFT: Final = 1
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

SYMBOL_CURRENCY: Final[dict[str, str]] = {
    "us$": "USD",
    "ca$": "CAD",
    "a$": "AUD",
    "nz$": "NZD",
    "s$": "SGD",
    "hk$": "HKD",
    "rmb": "CNY",
    "$": "USD",
    "¥": "CNY",
    "€": "EUR",
    "£": "GBP",
    "₹": "INR",
}

_NUMBER: Final = r"\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?"
_SYMBOL: Final = r"US\$|CA\$|A\$|NZ\$|S\$|HK\$|RMB|\$|¥|€|£|₹"
_CODE: Final = r"USD|CNY|EUR|GBP|JPY|RMB|INR|AUD|CAD|SGD|HKD"
_UNIT: Final = r"(?:users?|seats?|members?|editors?|person|people)"
_PERIOD: Final = (
    r"(?:mo\b|mo\.|months?|monthly|yr\b|yr\.|years?|yearly|annually|annum|"
    r"quarters?|quarterly|" + _UNIT + r")"
)
_SEPARATOR: Final = r"(?:/|\bper\b|\ba\b|\beach\b)"

SYMBOL_PRICE_RE: Final = re.compile(
    rf"(?P<cur>{_SYMBOL})\s?(?P<num>{_NUMBER})", re.IGNORECASE
)
NUMBER_CODE_RE: Final = re.compile(
    rf"(?P<num>{_NUMBER})\s?(?P<cur>{_CODE})\b", re.IGNORECASE
)
CODE_NUMBER_RE: Final = re.compile(
    rf"\b(?P<cur>{_CODE})\s?(?P<num>{_NUMBER})", re.IGNORECASE
)
PERIOD_PRICE_RE: Final = re.compile(
    rf"(?P<num>{_NUMBER})\s*{_SEPARATOR}\s*(?:{_UNIT}\s*{_SEPARATOR}\s*)?{_PERIOD}",
    re.IGNORECASE,
)
PERIOD_SUFFIX_RE: Final = re.compile(
    rf"^\s*{_SEPARATOR}\s*(?:{_UNIT}\s*{_SEPARATOR}\s*)?{_PERIOD}", re.IGNORECASE
)


class PlanDriftError(Exception):
    """The script cannot continue."""


@dataclass(frozen=True)
class PriceToken:
    """One currency-marked number found on a page, and where it sits."""

    value: float
    currency: str | None
    period_marked: bool
    position: int


@dataclass(frozen=True)
class PageResult:
    """One fetched URL and how it turned out."""

    url: str
    status: str
    text: str = ""
    variant: str = "plain"
    detail: str = ""
    tokens: tuple[PriceToken, ...] = ()

    @property
    def is_parsed(self) -> bool:
        """Report whether the page yielded prices worth comparing."""
        return self.status == STATUS_OK

    @property
    def has_text(self) -> bool:
        """Report whether the page yielded text worth snapshotting."""
        return self.status in (STATUS_OK, STATUS_NO_PRICES)

    def page_reason(self) -> str:
        """Translate a non-comparable page status into a CANNOT COMPARE reason."""
        if self.status == STATUS_BLOCKED:
            return REASON_BLOCKED
        if self.status == STATUS_UNREADABLE:
            return REASON_CLIENT_SIDE
        if self.status == STATUS_NO_PRICES:
            return REASON_NO_PRICES
        return f"{REASON_FETCH}: {self.detail}"


@dataclass(frozen=True)
class PlanRow:
    """One stored amount and its verdict against the online page."""

    record_id: str
    provider: str
    plan: str
    period: str
    stored: float
    currency: str
    verdict: str
    online: float | None = None
    online_form: str = ""
    candidates: tuple[float, ...] = ()
    reason: str = ""
    url: str = ""
    urls: tuple[str, ...] = ()

    @property
    def base_reason(self) -> str:
        """Return the reason without a fetch detail, for grouping."""
        return REASON_FETCH if self.reason.startswith(REASON_FETCH) else self.reason


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
    rows: list[PlanRow] = field(default_factory=list)
    pages: list[PageResult] = field(default_factory=list)
    diffs: list[SnapshotDiff] = field(default_factory=list)

    def by_verdict(self, verdict: str) -> list[PlanRow]:
        return [row for row in self.rows if row.verdict == verdict]

    @property
    def drift(self) -> list[PlanRow]:
        return self.by_verdict(VERDICT_DRIFT)

    @property
    def uncomparable(self) -> list[PlanRow]:
        return self.by_verdict(VERDICT_CANNOT)

    @property
    def matched(self) -> list[PlanRow]:
        return self.by_verdict(VERDICT_MATCH)

    @property
    def changed_diffs(self) -> list[SnapshotDiff]:
        return [d for d in self.diffs if d.changed_lines > 0 and not d.is_new_baseline]


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


def load_plans(path: Path) -> list[dict[str, object]]:
    """Read data/plans.yaml and return its records."""
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment problem
        raise PlanDriftError(
            "PyYAML is missing. Run pip install -r requirements.txt."
        ) from exc
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
        if isinstance(link, dict) and str(link.get("label", "")) in PRICE_LABELS:
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


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------


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


def apply_price_gate(page: PageResult) -> PageResult:
    """Downgrade a readable page that states too few prices to compare."""
    tokens = tuple(extract_price_tokens(page.text))
    if len({token.value for token in tokens}) >= MIN_PRICE_TOKENS:
        return replace(page, tokens=tokens)
    return replace(
        page,
        status=STATUS_NO_PRICES,
        tokens=tokens,
        detail=f"currency-marked prices on the page: {len(tokens)}",
    )


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


def retry_markdown(
    url: str, timeout: int, *, first_status: str, first_detail: str
) -> PageResult:
    """Retry a failed or thin fetch against the `.md` twin."""
    status, body = fetch_once(markdown_twin(url), timeout)
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


# --------------------------------------------------------------------------
# Price extraction
# --------------------------------------------------------------------------


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
        text = text.replace(separator, "") if is_thousands else text.replace(
            separator, "."
        )
    try:
        return float(text)
    except ValueError:
        return None


def currency_of(marker: str) -> str | None:
    """Map a currency symbol or code onto a currency code."""
    key = marker.strip().casefold()
    if key in SYMBOL_CURRENCY:
        return SYMBOL_CURRENCY[key]
    upper = key.upper()
    return "CNY" if upper == "RMB" else (upper or None)


def has_period_suffix(text: str, end: int) -> bool:
    """Report whether a per-period phrase follows the number at `end`."""
    return bool(PERIOD_SUFFIX_RE.match(text[end : end + PERIOD_LOOKAHEAD]))


def extract_price_tokens(text: str) -> list[PriceToken]:
    """Collect every number carrying a currency marker or a per-period marker.

    A bare number is never a price. `18` inside a token count and `20` inside
    `2026` must not become a candidate.
    """
    found: dict[tuple[int, int], PriceToken] = {}

    def record(span: tuple[int, int], raw: str, currency: str | None, marked: bool):
        value = normalize_number(raw)
        if value is None:
            return
        previous = found.get(span)
        if previous is None:
            found[span] = PriceToken(value, currency, marked, span[0])
            return
        found[span] = PriceToken(
            value,
            previous.currency or currency,
            previous.period_marked or marked,
            span[0],
        )

    for pattern in (SYMBOL_PRICE_RE, NUMBER_CODE_RE, CODE_NUMBER_RE):
        for match in pattern.finditer(text):
            span = match.span("num")
            record(
                span,
                match.group("num"),
                currency_of(match.group("cur")),
                has_period_suffix(text, span[1]),
            )
    for match in PERIOD_PRICE_RE.finditer(text):
        span = match.span("num")
        record(span, match.group("num"), None, True)
    return [found[span] for span in sorted(found)]


# --------------------------------------------------------------------------
# Tier pairing
# --------------------------------------------------------------------------


def tier_positions(text: str, plan: str, longer_names: Sequence[str]) -> list[int]:
    """Find every position where the tier name stands on its own.

    `Pro` must not match inside `Pro+`, `Pro Plus`, or `Product`. When a longer
    tier name also matches at the same position, that longer name owns it.
    """
    lowered = text.casefold()
    needle = plan.casefold().strip()
    if not needle:
        return []
    longer = [
        name.casefold()
        for name in longer_names
        if len(name) > len(plan) and name.casefold().startswith(needle)
    ]
    positions: list[int] = []
    start = 0
    while True:
        index = lowered.find(needle, start)
        if index == -1:
            return positions
        start = index + 1
        end = index + len(needle)
        if index > 0 and (lowered[index - 1].isalnum() or lowered[index - 1] == "+"):
            continue
        tail = lowered[end : end + 8]
        if not needle.endswith("+") and tail.startswith("+"):
            continue
        if re.match(r"\s*plus\b", tail):
            continue
        if end < len(lowered) and lowered[end].isalnum():
            continue
        if any(lowered.startswith(name, index) for name in longer):
            continue
        positions.append(index)


def longer_than(plan: str, tier_names: Sequence[str]) -> list[str]:
    """Return the tier names that extend `plan`, such as `Pro+` for `Pro`."""
    needle = plan.casefold()
    return [
        name
        for name in tier_names
        if len(name) > len(plan) and name.casefold().startswith(needle)
    ]


def all_tier_marks(text: str, tier_names: Sequence[str]) -> list[tuple[int, str]]:
    """Return every position where any tier name of this provider stands."""
    marks: list[tuple[int, str]] = []
    for name in set(tier_names):
        for index in tier_positions(text, name, longer_than(name, tier_names)):
            marks.append((index, name))
    return sorted(marks)


def following_mark(position: int, marks: Sequence[tuple[int, str]]) -> int | None:
    """Return the start of the first tier name after this price."""
    for start, _ in marks:
        if start > position:
            return start
    return None


def owning_mark(position: int, marks: Sequence[tuple[int, str]]) -> int | None:
    """Return the start of the nearest tier name before this price.

    A pricing page names the tier and then prints its price. So a price belongs
    to the closest tier name above it, not to every name within 200 characters.
    This is what stops `Pro = 20` matching the `$20` that belongs to `Starter`.
    """
    owner: int | None = None
    for start, _ in marks:
        if start > position:
            break
        owner = start
    return owner


def distance_to_name(position: int, own: Sequence[int], length: int) -> int:
    """Return the character gap between a price and the nearest tier name."""
    gaps = []
    for index in own:
        if position < index:
            gaps.append(index - position)
        elif position >= index + length:
            gaps.append(position - (index + length))
        else:
            gaps.append(0)
    return min(gaps) if gaps else sys.maxsize


@dataclass(frozen=True)
class TierReading:
    """What one page shows around one tier name."""

    name_found: bool
    in_window: tuple[PriceToken, ...]
    near: tuple[PriceToken, ...]


def read_tier(page: PageResult, plan: str, tier_names: Sequence[str]) -> TierReading:
    """Find the prices the page states for one tier.

    Keep a price when the tier owns it and it sits inside the window. When the
    tier owns nothing, fall back to the whole window, because some layouts print
    the price above the name. Prefer tokens carrying a per-period marker.

    `near` narrows that set to the prices close enough to the tier name to be
    that tier's own price. A pricing card puts the two together; prose does not.
    """
    own = tier_positions(page.text, plan, longer_than(plan, tier_names))
    if not own:
        return TierReading(False, (), ())
    windows = [
        (max(0, index - WINDOW_RADIUS), index + len(plan) + WINDOW_RADIUS)
        for index in own
    ]
    in_window = [
        token
        for token in page.tokens
        if any(low <= token.position < high for low, high in windows)
    ]
    marks = all_tier_marks(page.text, tier_names)
    owned = set(own)
    assigned: list[PriceToken] = []
    unowned: list[PriceToken] = []
    for token in in_window:
        owner = owning_mark(token.position, marks)
        if owner in owned:
            assigned.append(token)
        elif owner is None and following_mark(token.position, marks) in owned:
            # No tier name precedes it, so read it as a card that prints the
            # price above the name. Only the very next tier name may claim it.
            unowned.append(token)
    # A price another tier owns is never ours, so it never becomes a fallback.
    inside = assigned or unowned
    marked = [token for token in inside if token.period_marked]
    chosen = marked or inside
    near = [
        token
        for token in chosen
        if distance_to_name(token.position, own, len(plan)) <= MAX_PAIR_DISTANCE
    ]
    return TierReading(True, tuple(chosen), tuple(near))


# --------------------------------------------------------------------------
# Comparison
# --------------------------------------------------------------------------


def same_amount(left: float, right: float) -> bool:
    """Compare two amounts within the tolerance."""
    return abs(left - right) < AMOUNT_TOLERANCE


def compare_amount(
    stored: float, period: str, candidates: Sequence[float]
) -> tuple[float, str] | None:
    """Match a stored amount against the online candidates.

    A quarter or year `amount` is a term total that the repository derives, so
    also accept the monthly equivalent the provider prints instead.
    """
    for candidate in sorted(candidates):
        if same_amount(stored, candidate):
            return candidate, f"per {period}"
    divisor = PERIOD_DIVISORS.get(period)
    if divisor is None:
        return None
    equivalent = round(stored / divisor, 2)
    for candidate in sorted(candidates):
        if same_amount(equivalent, candidate):
            return candidate, "per month"
    return None


def usable_candidates(
    tokens: Sequence[PriceToken], currency: str
) -> tuple[list[float], bool]:
    """Drop tokens whose currency contradicts the record.

    Return the usable values and whether a currency mismatch removed them all.
    A token with no detectable currency stays in the set.
    """
    kept = [t.value for t in tokens if t.currency is None or t.currency == currency]
    dropped_all = bool(tokens) and not kept
    return kept, dropped_all


def stored_prices(record: dict[str, object]) -> list[tuple[str, float]]:
    """Return the (period, amount) pairs a record stores."""
    prices = record.get("prices") or []
    if not isinstance(prices, list):
        return []
    pairs: list[tuple[str, float]] = []
    for entry in prices:
        if not isinstance(entry, dict):
            continue
        amount = entry.get("amount")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            continue
        pairs.append((str(entry.get("period", "")), float(amount)))
    return pairs


@dataclass(frozen=True)
class PageVerdict:
    """What one page could say about one tier."""

    url: str
    candidates: tuple[float, ...]
    reason: str


def read_tier_from_page(
    page: PageResult, plan: str, currency: str, tier_names: Sequence[str]
) -> PageVerdict:
    """Read the online prices one page states for one tier."""
    if not page.is_parsed:
        return PageVerdict(page.url, (), page.page_reason())
    reading = read_tier(page, plan, tier_names)
    if not reading.name_found:
        return PageVerdict(page.url, (), REASON_NO_TIER)
    if not reading.in_window:
        return PageVerdict(page.url, (), REASON_NO_NEARBY)
    # Guard 4: a price far from the tier name is prose, not that tier's price.
    if not reading.near:
        return PageVerdict(page.url, (), REASON_TOO_FAR)
    kept, dropped_all = usable_candidates(reading.near, currency)
    if dropped_all:
        return PageVerdict(page.url, (), REASON_CURRENCY)
    return PageVerdict(page.url, tuple(sorted(set(kept))), "")


def best_reason(verdicts: Sequence[PageVerdict]) -> tuple[str, str]:
    """Pick the most informative reason across the pages of one record."""
    ranked = sorted(
        verdicts,
        key=lambda v: REASON_RANK.get(
            REASON_FETCH if v.reason.startswith(REASON_FETCH) else v.reason, 0
        ),
    )
    chosen = ranked[-1]
    return chosen.reason, chosen.url


def build_rows(
    record: dict[str, object], pages: dict[str, PageResult], tier_names: Sequence[str]
) -> list[PlanRow]:
    """Give every stored amount of one record exactly one verdict."""
    plan = str(record.get("plan", ""))
    currency = str(record.get("price_currency", ""))
    urls = price_urls(record)
    verdicts = [
        read_tier_from_page(pages[url], plan, currency, tier_names) for url in urls
    ]
    readable = [v for v in verdicts if v.candidates]

    pairs = stored_prices(record)
    # Decide the month rows first: guard 3 needs the set a month row matched.
    order = sorted(range(len(pairs)), key=lambda i: 0 if pairs[i][0] == "month" else 1)
    month_matched: set[float] = set()
    decided: dict[int, PlanRow] = {}

    for index in order:
        period, stored = pairs[index]
        base = PlanRow(
            record_id=str(record.get("id", "")),
            provider=str(record.get("provider", "")),
            plan=plan,
            period=period,
            stored=stored,
            currency=currency,
            verdict=VERDICT_CANNOT,
            urls=tuple(urls),
        )
        if not readable:
            reason, url = best_reason(verdicts) if verdicts else (REASON_NO_TIER, "")
            decided[index] = replace(base, reason=reason, url=url)
            continue
        row = decide(base, readable, period, stored, frozenset(month_matched))
        if period == "month" and row.verdict == VERDICT_MATCH:
            month_matched.update(row.candidates)
        decided[index] = row
    return [decided[index] for index in range(len(pairs))]


def is_implausible(candidate: float, stored: float) -> bool:
    """Report whether a candidate is the wrong kind of number for this tier.

    A seat price and a per-token rate differ by orders of magnitude. A real
    price move is a fraction of the old price, not hundreds of times it.
    """
    if candidate <= 0 or stored <= 0:
        return not same_amount(candidate, stored)
    high, low = max(candidate, stored), min(candidate, stored)
    return high / low > MAX_PLAUSIBLE_FACTOR


def cannot_compare(
    base: PlanRow, reason: str, verdict: PageVerdict
) -> PlanRow:
    """Turn one unconfident reading into a CANNOT COMPARE row."""
    return replace(
        base,
        verdict=VERDICT_CANNOT,
        reason=reason,
        candidates=verdict.candidates,
        url=verdict.url,
    )


def decide(
    base: PlanRow,
    readable: Sequence[PageVerdict],
    period: str,
    stored: float,
    month_matched: frozenset[float],
) -> PlanRow:
    """Choose MATCH, DRIFT, or CANNOT COMPARE for one stored amount.

    Report DRIFT only when the script is confident it read this tier's own
    price. Where it is not confident, saying nothing beats saying something
    wrong, so the row degrades to CANNOT COMPARE.
    """
    for verdict in readable:
        hit = compare_amount(stored, period, verdict.candidates)
        if hit is not None:
            online, form = hit
            return replace(
                base,
                verdict=VERDICT_MATCH,
                online=online,
                online_form=form,
                candidates=verdict.candidates,
                url=verdict.url,
            )
    first = readable[0]
    candidates = first.candidates
    # Guard 2: a free tier prints "Free", never "$0", so it inherits a neighbour.
    if same_amount(stored, 0) and not any(same_amount(c, 0) for c in candidates):
        return cannot_compare(base, REASON_FREE, first)
    # Guard 3: the page shows the monthly rate only, so a term total cannot match.
    if (
        period in PERIOD_DIVISORS
        and month_matched
        and set(candidates) <= month_matched
    ):
        return cannot_compare(base, REASON_MONTHLY_ONLY, first)
    # Guard 1: every candidate is the wrong order of magnitude for this tier.
    if candidates and all(is_implausible(c, stored) for c in candidates):
        return cannot_compare(base, REASON_IMPLAUSIBLE, first)
    return replace(
        base,
        verdict=VERDICT_DRIFT,
        candidates=candidates,
        online=candidates[0] if candidates else None,
        url=first.url,
    )


# --------------------------------------------------------------------------
# Snapshots
# --------------------------------------------------------------------------


def url_slug(url: str) -> str:
    """Derive a stable file name from a URL."""
    stripped = re.sub(r"^https?://", "", url).casefold()
    return SLUG_UNSAFE_RE.sub("-", stripped).strip("-")[:120] or "page"


def diff_snapshot(page: PageResult, *, write_only: bool) -> SnapshotDiff | None:
    """Compare a page against its snapshot, then write the fresh text."""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{url_slug(page.url)}.txt"
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    path.write_text(page.text, encoding="utf-8")
    if write_only:
        return None
    if previous is None:
        return SnapshotDiff(page.url, changed_lines=0, is_new_baseline=True)
    changed = sum(
        1
        for line in difflib.unified_diff(
            previous.splitlines(), page.text.splitlines(), lineterm=""
        )
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
    )
    return SnapshotDiff(page.url, changed_lines=changed, is_new_baseline=False)


# --------------------------------------------------------------------------
# Provider pointers
# --------------------------------------------------------------------------


def provider_slug(provider: str) -> str:
    """Derive a skill directory slug from a provider name."""
    return provider.split("(")[0].casefold().replace(" ", "").replace(".", "")


def missing_pointer(provider: str) -> str:
    """Describe where to look when no skill file exists."""
    return f"no skill file on disk — look under .claude/skills/ for {provider}"


def pointer_for(provider: str) -> str:
    """Return the skill path that already knows how to read this provider."""
    mapped = PROVIDER_POINTERS.get(provider)
    if mapped is not None:
        return mapped if (REPO_ROOT / mapped).exists() else missing_pointer(provider)
    derived = f".claude/skills/provider-{provider_slug(provider)}/SKILL.md"
    return derived if (REPO_ROOT / derived).exists() else missing_pointer(provider)


# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------


def run_check(*, provider: str | None, timeout: int, update_snapshots: bool) -> Report:
    """Fetch every cited page once and give every stored amount a verdict."""
    everything = load_plans(PLANS_PATH)
    records = select_records(everything, provider)
    report = Report(checked_records=len(records))

    pages = {url: classify(url, timeout) for url in unique_urls(records)}
    report.checked_urls = len(pages)
    report.pages = list(pages.values())

    names_by_provider: dict[str, list[str]] = {}
    for item in everything:
        key = str(item.get("provider", ""))
        names_by_provider.setdefault(key, []).append(str(item.get("plan", "")))

    for record in records:
        names = names_by_provider.get(str(record.get("provider", "")), [])
        report.rows.extend(build_rows(record, pages, names))

    # A page earns a snapshot diff only when it left a row uncomparable.
    unresolved = {url for row in report.uncomparable for url in row.urls}
    for page in report.pages:
        if page.has_text and page.url in unresolved:
            diff = diff_snapshot(page, write_only=update_snapshots)
            if diff is not None:
                report.diffs.append(diff)
    return report


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


FOOTER: Final = (
    "This script never edits any file under data/. It writes only under .plan-drift/."
)


def format_candidates(values: Sequence[float]) -> str:
    """Render the online candidate list."""
    return ", ".join(f"{value:g}" for value in values) or "none"


def render_drift(report: Report, lines: list[str]) -> None:
    """Write every row whose stored amount disagrees with the page."""
    drift = report.drift
    lines.append(f"DRIFT ({len(drift)})")
    if not drift:
        lines.append("  none")
    for row in drift:
        lines.append(f"  {row.record_id} | {row.plan} | {row.period}")
        lines.append(
            f"    stored {row.stored:g} {row.currency} per {row.period} | "
            f"online near the tier name: {format_candidates(row.candidates)}"
        )
        lines.append(f"    {row.url}")
    lines.append("")


def render_uncomparable(report: Report, lines: list[str]) -> None:
    """Write every row the script could not compare, grouped by reason."""
    rows = report.uncomparable
    lines.append(f"CANNOT COMPARE ({len(rows)})")
    if not rows:
        lines.append("  none")
        lines.append("")
        return
    grouped: dict[str, list[PlanRow]] = {}
    for row in rows:
        grouped.setdefault(row.base_reason, []).append(row)
    for reason in sorted(grouped, key=lambda r: -len(grouped[r])):
        group = grouped[reason]
        lines.append(f"  {reason} ({len(group)})")
        for row in group:
            lines.append(
                f"    {row.record_id} | {row.plan} | {row.period} "
                f"| stored {row.stored:g} {row.currency}"
            )
            if row.candidates:
                lines.append(
                    f"      rejected candidates: {format_candidates(row.candidates)}"
                )
            if row.reason != reason:
                lines.append(f"      detail: {row.reason}")
        if reason in PAGE_LEVEL_REASONS:
            for provider in sorted({row.provider for row in group}):
                lines.append(f"      read it with: {pointer_for(provider)}")
    lines.append("")


def render_matches(report: Report, lines: list[str]) -> None:
    """Write the confirmed rows, one compact line each."""
    matched = report.matched
    lines.append(f"MATCH ({len(matched)})")
    for row in matched:
        lines.append(
            f"  {row.record_id} | {row.plan} | stored {row.stored:g} "
            f"{row.currency} per {row.period} | online {row.online:g} {row.online_form}"
        )
    lines.append("")


def render_diffs(report: Report, lines: list[str]) -> None:
    """Write the snapshot movement for pages the script could not compare."""
    changed = report.changed_diffs
    lines.append(f"CHANGED SNAPSHOT, UNCOMPARABLE PAGES ONLY ({len(changed)})")
    if not changed:
        lines.append("  none")
    for diff in changed:
        lines.append(f"  {diff.changed_lines} changed lines | {diff.url}")
    lines.append("")


def render_text(report: Report, *, only_uncomparable: bool) -> str:
    """Build the whole text report."""
    lines = [
        f"Plan drift report — {date.today().isoformat()}",
        f"{report.checked_records} plan records, {report.checked_urls} unique pages",
        f"{len(report.rows)} stored amounts: {len(report.drift)} DRIFT, "
        f"{len(report.matched)} MATCH, {len(report.uncomparable)} CANNOT COMPARE",
        "",
    ]
    if only_uncomparable:
        render_uncomparable(report, lines)
        lines.append(FOOTER)
        return "\n".join(lines)
    render_drift(report, lines)
    render_uncomparable(report, lines)
    render_matches(report, lines)
    render_diffs(report, lines)
    lines.append(FOOTER)
    return "\n".join(lines)


def render_json(report: Report) -> str:
    """Build the whole report as JSON."""
    payload = {
        "date": date.today().isoformat(),
        "checked_records": report.checked_records,
        "checked_urls": report.checked_urls,
        "counts": {
            "drift": len(report.drift),
            "match": len(report.matched),
            "cannot_compare": len(report.uncomparable),
        },
        "footer": FOOTER,
        "pages": [
            {
                "url": p.url,
                "status": p.status,
                "variant": p.variant,
                "detail": p.detail,
                "text_length": len(p.text),
                "price_tokens": len(p.tokens),
            }
            for p in report.pages
        ],
        "rows": [
            {
                "id": r.record_id,
                "provider": r.provider,
                "plan": r.plan,
                "period": r.period,
                "stored": r.stored,
                "currency": r.currency,
                "verdict": r.verdict,
                "online": r.online,
                "online_form": r.online_form,
                "candidates": list(r.candidates),
                "reason": r.reason,
                "url": r.url,
            }
            for r in report.rows
        ],
        "snapshots": [
            {
                "url": d.url,
                "result": "NEW BASELINE" if d.is_new_baseline else "DIFF",
                "changed_lines": d.changed_lines,
            }
            for d in report.diffs
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """Read the command line."""
    parser = argparse.ArgumentParser(
        prog="check_plan_drift.py",
        description=(
            "Compare every price in data/plans.yaml against the price the "
            "provider states online. The script writes only under .plan-drift/ "
            "and never edits data/."
        ),
    )
    parser.add_argument("--provider", help="Check one provider only. Case-insensitive.")
    parser.add_argument(
        "--json", action="store_true", help="Emit the report as JSON on stdout."
    )
    parser.add_argument(
        "--only-uncomparable",
        action="store_true",
        help="Print only the CANNOT COMPARE section.",
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
        help="Write snapshots and skip the diff section.",
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
    if args.json:
        print(render_json(report))
    else:
        print(render_text(report, only_uncomparable=args.only_uncomparable))
    return EXIT_DRIFT if report.drift else EXIT_CLEAN


if __name__ == "__main__":
    sys.exit(main())
