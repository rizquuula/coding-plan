#!/usr/bin/env python3
"""Validate the YAML data and render the static coding-plan tracker site."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"
ASSET_DIR = ROOT / "assets"
OUT_DIR = ROOT / "site"
__version__ = "0.1.0"

# Public base URL of the deployed site. Social meta tags need absolute URLs.
SITE_URL = "https://rizquuula.github.io/coding-plan/"

# Labels a link may carry. Any other label is a validation error.
LINK_LABELS = {"pricing", "rate limit", "plans", "model card", "docs", "announcement"}

# Billing period -> months it covers. The order sets the display order.
PRICE_PERIODS = {"month": 1, "quarter": 3, "year": 12}

# Field name -> (required, kind).
# Kinds: str, num, bool, date, list, links, prices, or "enum:a|b".
PLAN_SCHEMA = {
    "id": (True, "str"),
    "provider": (True, "str"),
    "plan": (True, "str"),
    "price_currency": (True, "enum:USD|CNY|EUR"),
    "prices": (True, "prices"),
    "limits": (True, "list"),
    "models": (True, "list"),
    "status": (True, "enum:active|beta|discontinued"),
    "notes": (False, "str"),
    "links": (True, "links"),
    "last_verified": (False, "date"),
    "discontinued_on": (False, "date"),
}

API_SCHEMA = {
    "id": (True, "str"),
    "provider": (True, "str"),
    "model": (True, "str"),
    "model_id": (False, "str"),
    "context_window": (False, "str"),
    "currency": (True, "enum:USD|CNY|EUR"),
    "input": (True, "num"),
    "cached_input": (False, "num"),
    "cache_write": (False, "num"),
    "output": (True, "num"),
    "notes": (False, "str"),
    "links": (True, "links"),
    "last_verified": (False, "date"),
}

MODEL_SCHEMA = {
    "id": (True, "str"),
    "name": (True, "str"),
    "provider": (True, "str"),
    "total_params": (False, "str"),
    "active_params": (False, "str"),
    "context_window": (False, "str"),
    "max_output": (False, "str"),
    # Nullable for the same reason as open_weights: a page that never mentions
    # image input does not say the model lacks it, so null means "unstated".
    "vision": (False, "bool"),
    # Nullable: some providers never state whether they publish the weights.
    # A guessed false is a claim we cannot source, so null means "unstated".
    "open_weights": (False, "bool"),
    "notes": (False, "str"),
    "links": (True, "links"),
    "last_verified": (False, "date"),
}

RATE_LIMIT_SCHEMA = {
    "id": (True, "str"),
    "provider": (True, "str"),
    "model": (True, "str"),
    "tier": (True, "str"),
    "requests_per_minute": (False, "num"),
    "input_tokens_per_minute": (False, "num"),
    "output_tokens_per_minute": (False, "num"),
    "tokens_per_minute": (False, "num"),
    "requests_per_day": (False, "num"),
    "concurrent_requests": (False, "num"),
    "notes": (False, "str"),
    "links": (True, "links"),
    "last_verified": (False, "date"),
}

CHANGELOG_SCHEMA = {
    "id": (False, "str"),
    "date": (True, "date"),
    "provider": (True, "str"),
    "type": (True, "enum:new provider|new model|price update|rate limit change|update"),
    "summary": (True, "str"),
    "links": (False, "links"),
    "last_verified": (False, "date"),
}

# Provider -> brand colour. Every value comes from a page the provider owns:
# a declared brand token, a logo SVG fill, or a theme colour. The trailing
# comment names the token and the host it came from.
PROVIDER_BRAND = {
    "Alibaba (Qwen)": "#082dff",   # --btn-brandprimary-fill, g.alicdn.com
    "Anthropic": "#d97757",        # --swatch--clay, anthropic.com
    "BytePlus": "#1664ff",         # --color-primary, byteplus.com
    "ClinePass": "#9f58fa",        # --brand-purple, cline.bot
    "CommandCode": "#2e1b9c",      # --brand, commandcode.ai
    "Cursor": "#14120b",           # dark theme-color, cursor.com/brand
    "Devin": "#317cff",            # docs site config primary, devin.ai
    "Factory": "#ef6f2e",          # --accent-100, factory.ai
    "GitHub": "#0fbf3e",           # GitHub Green, brand.github.com
    "Google": "#4285f4",           # wordmark G fill, Google brand hub
    "Kiro": "#c6a0ff",             # app icon SVG fill, kiro.dev
    "MiniMax": "#181e25",          # theme-color meta, minimax.io
    "Mistral": "#fa500f",          # logo SVG fill, mistral.ai
    "Moonshot (Kimi)": "#1783ff",  # --Colors-KMBlue, statics.moonshot.cn
    "Novita": "#23d57c",           # --brand-0, novita.ai
    "Ollama": "#000000",           # msapplication-TileColor, ollama.com
    "OpenAI": "#0d0d0d",           # --gray-1000, developers.openai.com
    "OpenCode": "#131010",         # favicon SVG plate, opencode.ai
    "Sakana (Fugu)": "#e10600",    # --ac, sakana.ai/fugu
    "Verboo": "#ad34fe",           # --primary-h/s/l, verboo.ai
    "Zhipu (GLM)": "#141618",      # --primary, docs.z.ai
}

# Fallback for a provider the map does not name.
BRAND_FALLBACK = "#6b7280"


def brand_for(provider: str) -> str:
    """Return the brand colour for a provider, or a neutral grey."""
    return PROVIDER_BRAND.get(provider, BRAND_FALLBACK)


def brand_ink(hex_colour: str) -> str:
    """Return the text colour that reads best on `hex_colour`."""
    value = (hex_colour or "").lstrip("#")
    if len(value) == 3:
        value = "".join(char * 2 for char in value)
    if len(value) != 6:
        return "#111111"
    try:
        channels = [int(value[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    except ValueError:
        return "#111111"

    def linear(channel: float) -> float:
        if channel <= 0.03928:
            return channel / 12.92
        return ((channel + 0.055) / 1.055) ** 2.4

    red, green, blue = (linear(c) for c in channels)
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    on_dark_ink = (1.0 + 0.05) / (luminance + 0.05)
    on_light_ink = (luminance + 0.05) / (0.0 + 0.05)
    return "#ffffff" if on_dark_ink >= on_light_ink else "#111111"


DATASETS = [
    ("plans.yaml", PLAN_SCHEMA),
    ("api_pricing.yaml", API_SCHEMA),
    ("models.yaml", MODEL_SCHEMA),
    ("rate_limits.yaml", RATE_LIMIT_SCHEMA),
    ("changelog.yaml", CHANGELOG_SCHEMA),
]

# One entry per rendered page. `name` also names the page in the sidebar state.
PAGES = [
    {
        "name": "index",
        "href": "index.html",
        "label": "Coding Plans",
        "template": "index.html.j2",
    },
    {
        "name": "api-pricing",
        "href": "api-pricing.html",
        "label": "API Pricing & Models",
        "template": "api_pricing.html.j2",
    },
    {
        "name": "rate-limits",
        "href": "rate-limits.html",
        "label": "Rate Limits",
        "template": "rate_limits.html.j2",
    },
    {
        "name": "changelog",
        "href": "changelog.html",
        "label": "Changelog",
        "template": "changelog.html.j2",
    },
]


def link_errors(value) -> list[str]:
    """Return one message per problem found in a `links` value."""
    if not isinstance(value, list):
        return ["must be a list of {label, url} mappings"]
    if not value:
        return ["must hold at least one link"]

    allowed = ", ".join(sorted(LINK_LABELS))
    errors: list[str] = []
    for index, item in enumerate(value, start=1):
        position = f"link {index}"
        if not isinstance(item, dict):
            errors.append(f"{position}: must be a mapping with 'label' and 'url'")
            continue
        extra = sorted(set(item) - {"label", "url"})
        for key in extra:
            errors.append(f"{position}: unknown key '{key}'")
        for key in ("label", "url"):
            if key not in item:
                errors.append(f"{position}: missing '{key}'")
        label = item.get("label")
        if "label" in item:
            if not isinstance(label, str):
                errors.append(f"{position}: label must be a string, got {label!r}")
            elif label not in LINK_LABELS:
                errors.append(
                    f"{position}: label {label!r} is not one of {allowed}"
                )
        url = item.get("url")
        if "url" in item:
            if not isinstance(url, str):
                errors.append(f"{position}: url must be a string, got {url!r}")
            elif not url.startswith("https://"):
                errors.append(f"{position}: url must start with https://")
    return errors


def price_errors(value) -> list[str]:
    """Return one message per problem found in a `prices` value."""
    if not isinstance(value, list):
        return ["must be a list of {period, amount} mappings"]
    if not value:
        return ["must hold at least one price"]

    allowed = ", ".join(PRICE_PERIODS)
    errors: list[str] = []
    seen_periods: set[str] = set()
    for index, item in enumerate(value, start=1):
        position = f"price {index}"
        if not isinstance(item, dict):
            errors.append(f"{position}: must be a mapping with 'period' and 'amount'")
            continue
        extra = sorted(set(item) - {"period", "amount"})
        for key in extra:
            errors.append(f"{position}: unknown key '{key}'")
        for key in ("period", "amount"):
            if key not in item:
                errors.append(f"{position}: missing '{key}'")
        period = item.get("period")
        if "period" in item:
            if not isinstance(period, str):
                errors.append(f"{position}: period must be a string, got {period!r}")
            elif period not in PRICE_PERIODS:
                errors.append(
                    f"{position}: period {period!r} is not one of {allowed}"
                )
            elif period in seen_periods:
                errors.append(f"{position}: duplicate period {period!r}")
            else:
                seen_periods.add(period)
        amount = item.get("amount")
        if "amount" in item:
            if not isinstance(amount, (int, float)) or isinstance(amount, bool):
                errors.append(f"{position}: amount must be a number, got {amount!r}")
            elif amount < 0:
                errors.append(f"{position}: amount must not be negative")
    return errors


def monthly_equivalent(entry: dict) -> float:
    """Return what one month costs under this billing term."""
    return entry["amount"] / PRICE_PERIODS[entry["period"]]


def price_view(record: dict) -> list[dict]:
    """Return one display entry per billing term, cheapest term last."""
    entries = sorted(record["prices"], key=lambda e: PRICE_PERIODS[e["period"]])
    monthly = {e["period"]: monthly_equivalent(e) for e in entries}

    if "month" in monthly:
        baseline = monthly["month"]
    else:
        baseline = max(monthly.values())

    view: list[dict] = []
    for entry in entries:
        each_month = monthly[entry["period"]]
        discount = None
        if baseline > 0:
            saved = round((1 - each_month / baseline) * 100)
            if saved > 0:
                discount = saved
        view.append(
            {
                "period": entry["period"],
                "amount": entry["amount"],
                "monthly": each_month,
                "discount": discount,
            }
        )
    return view


def sort_price(record: dict) -> float:
    """Return the monthly figure that orders a plan against its peers."""
    monthly = {e["period"]: monthly_equivalent(e) for e in record["prices"]}
    if "month" in monthly:
        return monthly["month"]
    return min(monthly.values())


def kind_matches(value, kind: str) -> bool:
    """Report whether `value` matches the declared `kind`."""
    if kind == "links":
        return not link_errors(value)
    if kind == "prices":
        return not price_errors(value)
    if kind == "str":
        return isinstance(value, str)
    if kind == "num":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "bool":
        return isinstance(value, bool)
    if kind == "date":
        return isinstance(value, dt.date)
    if kind == "list":
        return isinstance(value, list) and all(isinstance(i, str) for i in value)
    if kind.startswith("enum:"):
        return value in kind.split(":", 1)[1].split("|")
    raise ValueError(f"unknown kind: {kind}")


def validate(records: list, schema: dict, filename: str) -> list[str]:
    """Return every schema violation found in one dataset."""
    errors: list[str] = []
    seen_ids: set[str] = set()

    if not isinstance(records, list):
        return [f"{filename}: top level must be a list of records"]

    for index, record in enumerate(records):
        label = f"{filename}[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{label}: record must be a mapping")
            continue

        record_id = record.get("id")
        if isinstance(record_id, str):
            label = f"{filename}[{record_id}]"
            if record_id in seen_ids:
                errors.append(f"{label}: duplicate id")
            seen_ids.add(record_id)

        for field in record:
            if field not in schema:
                errors.append(f"{label}: unknown field '{field}'")

        for field, (required, kind) in schema.items():
            if field not in record:
                if required:
                    errors.append(f"{label}: missing required field '{field}'")
                continue
            value = record[field]
            if value is None:
                if required:
                    errors.append(f"{label}: '{field}' is required and cannot be null")
                continue
            if kind == "links":
                for message in link_errors(value):
                    errors.append(f"{label}: '{field}': {message}")
                continue
            if kind == "prices":
                for message in price_errors(value):
                    errors.append(f"{label}: '{field}': {message}")
                continue
            if not kind_matches(value, kind):
                errors.append(f"{label}: '{field}' must be {kind}, got {value!r}")

    return errors


def load_data() -> dict:
    """Load every dataset and fail loudly on the first schema violation."""
    data: dict = {}
    errors: list[str] = []

    for filename, schema in DATASETS:
        path = DATA_DIR / filename
        if path.exists():
            records = yaml.safe_load(path.read_text(encoding="utf-8")) or []
        else:
            # A dataset file that does not exist yet loads as an empty list.
            records = []
        errors.extend(validate(records, schema, filename))
        data[path.stem] = records

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        raise SystemExit(f"{len(errors)} validation error(s)")

    return data


def format_date(value) -> str:
    """Render a date, or an em dash when the value is missing."""
    return value.isoformat() if isinstance(value, dt.date) else "—"


def format_money(value, currency: str) -> str:
    """Render a rate with its currency symbol."""
    if value is None:
        return "—"
    symbol = {"USD": "$", "CNY": "¥", "EUR": "€"}.get(currency, "")
    return f"{symbol}{value:,.2f}"


def format_thousands(value) -> str:
    """Render a whole number with thousands separators, or an em dash."""
    if value is None:
        return "—"
    return f"{value:,.0f}"


def slugify(name: str) -> str:
    """Turn a provider name into an id-safe slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def group_by_provider(rows: list) -> list[dict]:
    """Group already-sorted rows into one entry per provider."""
    groups: dict[str, list] = {}
    for row in rows:
        groups.setdefault(row["provider"], []).append(row)
    return [
        {"provider": provider, "slug": slugify(provider), "rows": groups[provider]}
        for provider in sorted(groups)
    ]


def dedupe_links(links: list) -> list:
    """Return the links in order, with a repeated (label, url) pair dropped."""
    seen: set[tuple[str, str]] = set()
    kept: list = []
    for link in links:
        key = (link["label"], link["url"])
        if key in seen:
            continue
        seen.add(key)
        kept.append(link)
    return kept


def join_notes(*notes) -> str | None:
    """Join the notes that exist into one sentence run, or return None."""
    present = [note for note in notes if note]
    return " ".join(present) if present else None


def priced_row(api: dict, model: dict | None) -> dict:
    """Return one merged row built on an api_pricing record."""
    spec = model or {}
    return {
        "provider": api["provider"],
        "model": api["model"],
        "model_id": api.get("model_id"),
        # The api record wins. The model record only fills a gap.
        "context_window": api.get("context_window") or spec.get("context_window"),
        "currency": api["currency"],
        "input": api["input"],
        "cached_input": api.get("cached_input"),
        "cache_write": api.get("cache_write"),
        "output": api["output"],
        "total_params": spec.get("total_params"),
        "active_params": spec.get("active_params"),
        "max_output": spec.get("max_output"),
        "vision": spec.get("vision"),
        "open_weights": spec.get("open_weights"),
        "notes": join_notes(api.get("notes"), spec.get("notes")),
        "links": dedupe_links(api["links"] + spec.get("links", [])),
    }


def unpriced_row(model: dict) -> dict:
    """Return one row for a model that no api_pricing record covers."""
    return {
        "provider": model["provider"],
        "model": model["name"],
        "model_id": None,
        "context_window": model.get("context_window"),
        # No api record means no currency and no rates. Every rate cell is a dash.
        "currency": None,
        "input": None,
        "cached_input": None,
        "cache_write": None,
        "output": None,
        "total_params": model.get("total_params"),
        "active_params": model.get("active_params"),
        "max_output": model.get("max_output"),
        "vision": model.get("vision"),
        "open_weights": model.get("open_weights"),
        "notes": model.get("notes"),
        "links": dedupe_links(model["links"]),
    }


def merge_api_and_models(api_rows: list, model_rows: list) -> list[dict]:
    """Left-join api_pricing onto models, then keep the unmatched models too."""
    by_key = {(r["provider"], r["name"]): r for r in model_rows}
    matched: set[tuple[str, str]] = set()

    merged: list[dict] = []
    for api in api_rows:
        key = (api["provider"], api["model"])
        model = by_key.get(key)
        if model is not None:
            matched.add(key)
        merged.append(priced_row(api, model))

    for model in model_rows:
        key = (model["provider"], model["name"])
        if key not in matched:
            merged.append(unpriced_row(model))

    merged.sort(key=lambda r: (r["provider"], r["model"]))
    return merged


def provider_anchors(sections: list[tuple[str, list]]) -> list[dict]:
    """Return one sidebar anchor per provider block on the page."""
    return [
        {"href": f"#{section_id}-{group['slug']}", "label": group["provider"]}
        for section_id, groups in sections
        for group in groups
    ]


def build_nav(current: str, anchors: list[dict]) -> dict:
    """Return the page links and the in-page anchors for one page."""
    pages = [
        {"href": page["href"], "label": page["label"], "active": page["name"] == current}
        for page in PAGES
    ]
    return {"pages": pages, "anchors": anchors}


def render(data: dict, today: dt.date) -> None:
    """Write the rendered site into OUT_DIR."""
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["date"] = format_date
    env.filters["money"] = format_money
    env.filters["thousands"] = format_thousands
    env.filters["price_view"] = price_view

    plans = sorted(
        data["plans"],
        key=lambda r: (r["provider"], sort_price(r)),
    )
    api_pricing = sorted(data["api_pricing"], key=lambda r: (r["provider"], r["model"]))
    models = sorted(data["models"], key=lambda r: (r["provider"], r["name"]))
    rate_limits = sorted(
        data["rate_limits"], key=lambda r: (r["provider"], r["model"], r["tier"])
    )
    changelog = sorted(data["changelog"], key=lambda r: r["date"], reverse=True)

    plans_all = group_by_provider(plans)
    # The other three pages share group_by_provider, so the brand keys land here.
    for group in plans_all:
        group["brand"] = brand_for(group["provider"])
        group["ink"] = brand_ink(group["brand"])
    api_models = group_by_provider(merge_api_and_models(api_pricing, models))
    rate_limit_groups = group_by_provider(rate_limits)

    shared = {
        "built_at": today.isoformat(),
        "counts": {
            "plans": len(plans),
            "api_pricing": len(api_pricing),
            "models": len(models),
            "rate_limits": len(rate_limits),
            "changelog": len(changelog),
        },
    }

    pages = {
        "index": {
            "plans_all": plans_all,
            "nav": build_nav("index", provider_anchors([("plans", plans_all)])),
        },
        "api-pricing": {
            "api_models": api_models,
            "nav": build_nav(
                "api-pricing", provider_anchors([("api-pricing", api_models)])
            ),
        },
        "rate-limits": {
            "rate_limits": rate_limit_groups,
            "nav": build_nav(
                "rate-limits", provider_anchors([("rate-limits", rate_limit_groups)])
            ),
        },
        "changelog": {
            "changelog": changelog,
            "nav": build_nav("changelog", []),
        },
    }

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    for page in PAGES:
        html = env.get_template(page["template"]).render(
            **shared,
            **pages[page["name"]],
            site_url=SITE_URL,
            page_href=page["href"],
        )
        (OUT_DIR / page["href"]).write_text(html, encoding="utf-8")

    shutil.copytree(ASSET_DIR, OUT_DIR / "assets")
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the data and exit without writing the site",
    )
    args = parser.parse_args()

    data = load_data()
    if args.check:
        total = sum(len(v) for v in data.values())
        print(f"ok: {total} records passed validation")
        return

    render(data, dt.date.today())
    print(f"Rendered {len(data['models'])} models and {len(data['plans'])} plans")
    print(f"ok: wrote {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
