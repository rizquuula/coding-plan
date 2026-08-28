#!/usr/bin/env python3
"""Validate the YAML data and render the static coding-plan tracker site."""

from __future__ import annotations

import argparse
import datetime as dt
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

# Field name -> (required, kind). Kinds: str, num, bool, date, list, or "enum:a|b".
PLAN_SCHEMA = {
    "id": (True, "str"),
    "provider": (True, "str"),
    "plan": (True, "str"),
    "region": (True, "enum:global|china"),
    "price_amount": (True, "num"),
    "price_currency": (True, "enum:USD|CNY|EUR"),
    "price_period": (True, "enum:month|year"),
    "limits": (True, "list"),
    "models": (True, "list"),
    "status": (True, "enum:active|beta|discontinued"),
    "notes": (False, "str"),
    "source": (True, "str"),
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
    "source": (True, "str"),
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
    "vision": (True, "bool"),
    "open_weights": (True, "bool"),
    "notes": (False, "str"),
    "source": (True, "str"),
    "last_verified": (False, "date"),
}

DATASETS = [
    ("plans.yaml", PLAN_SCHEMA),
    ("api_pricing.yaml", API_SCHEMA),
    ("models.yaml", MODEL_SCHEMA),
]


def kind_matches(value, kind: str) -> bool:
    """Report whether `value` matches the declared `kind`."""
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
            if not kind_matches(value, kind):
                errors.append(f"{label}: '{field}' must be {kind}, got {value!r}")

    return errors


def load_data() -> dict:
    """Load every dataset and fail loudly on the first schema violation."""
    data: dict = {}
    errors: list[str] = []

    for filename, schema in DATASETS:
        path = DATA_DIR / filename
        records = yaml.safe_load(path.read_text(encoding="utf-8")) or []
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

    plans = sorted(
        data["plans"],
        key=lambda r: (r["region"], r["provider"], r["price_amount"]),
    )
    api_pricing = sorted(data["api_pricing"], key=lambda r: (r["provider"], r["model"]))
    models = sorted(data["models"], key=lambda r: (r["provider"], r["name"]))

    context = {
        "plans_global": [r for r in plans if r["region"] == "global"],
        "plans_china": [r for r in plans if r["region"] == "china"],
        "api_pricing": api_pricing,
        "models": models,
        "built_at": today.isoformat(),
        "counts": {
            "plans": len(plans),
            "api_pricing": len(api_pricing),
            "models": len(models),
        },
    }

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    (OUT_DIR / "index.html").write_text(
        env.get_template("index.html.j2").render(**context), encoding="utf-8"
    )
    shutil.copytree(ASSET_DIR, OUT_DIR / "assets")
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
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
    print(f"ok: wrote {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
