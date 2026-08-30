#!/usr/bin/env python3
"""Print the Cognition token rates from the Devin Desktop models page.

The page embeds every rate in one JavaScript array named `modelCostData`. This
script fetches the Markdown twin, parses that array, and prints the rows whose
vendor is Cognition. The page's own tab bar labels `MODEL_PROVIDER_WINDSURF` as
"Cognition", so that string is the filter.

Usage:
    python3 model_rates.py            # Cognition rows only
    python3 model_rates.py --all      # every vendor, for a spot check

Read `SKILL.md` trap 8 before you copy a value. A `0` means the page prints an
em dash, so write `null` in `data/api_pricing.yaml`.
"""

import argparse
import json
import re
import sys
import urllib.request

URL = "https://docs.devin.ai/desktop/models.md"
COGNITION = "MODEL_PROVIDER_WINDSURF"


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


def parse(page: str) -> list[dict]:
    match = re.search(r"export const modelCostData = (\[.*?\]);", page, re.S)
    if not match:
        sys.exit("modelCostData not found. The page changed. Update this script.")
    return json.loads(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="print every vendor")
    args = parser.parse_args()

    rows = parse(fetch(URL))
    if not args.all:
        rows = [r for r in rows if r["model_provider"] == COGNITION]

    seen = set()
    header = ("model_uid", "label", "tier", "input", "cache_read", "output", "cache_write")
    print("\t".join(header))
    for row in sorted(rows, key=lambda r: (r["model_uid"], r["tier"])):
        key = (
            row["model_uid"],
            row["input_cost_per_million_usd"],
            row["cache_read_cost_per_million_usd"],
            row["output_cost_per_million_usd"],
            row["cache_write_cost_per_million_usd"],
        )
        if key in seen:
            continue
        seen.add(key)
        print(
            "\t".join(
                str(v)
                for v in (
                    row["model_uid"],
                    row["label"],
                    row["tier"],
                    row["input_cost_per_million_usd"],
                    row["cache_read_cost_per_million_usd"],
                    row["output_cost_per_million_usd"],
                    row["cache_write_cost_per_million_usd"],
                )
            )
        )
    print(f"\n{len(seen)} distinct rate rows. Source: {URL}", file=sys.stderr)


if __name__ == "__main__":
    main()
