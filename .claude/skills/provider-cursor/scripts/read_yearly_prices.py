#!/usr/bin/env python3
"""Print the Cursor plan prices under both billing terms.

https://cursor.com/pricing renders one tier at a time. The HTML carries the
monthly price only. The yearly price sits in a JavaScript chunk. This script
downloads the page, downloads every chunk it references, and prints each
monthly/yearly pair it finds.

The printed yearly figure is a rate per month, not a term total. Multiply it by
12 before you write it into `amount`. See references/pricing.md.

Usage:
    python3 read_yearly_prices.py

No install. No browser. Standard library only.
"""

import re
import urllib.request

PAGE = "https://cursor.com/pricing"
ORIGIN = "https://cursor.com"
AGENT = "Mozilla/5.0 (X11; Linux x86_64) provider-cursor-skill"

CHUNK_RE = re.compile(r'src="(/[^"]*?/_next/static/chunks/[^"]+)"')
PAIR_RE = re.compile(r'\{monthly:"(\$[^"]+)",yearly:"(\$[^"]+)"\}')
NUM_RE = re.compile(r"\$([0-9]+(?:\.[0-9]+)?)")


def get(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "replace")


def main() -> None:
    page = get(PAGE)
    chunks = sorted(set(CHUNK_RE.findall(page)))
    print(f"page bytes: {len(page)}")
    print(f"chunks:     {len(chunks)}")

    pairs = []
    for path in chunks:
        try:
            body = get(ORIGIN + path)
        except Exception as error:  # a single dead chunk must not stop the run
            print(f"skip {path}: {error}")
            continue
        for monthly, yearly in PAIR_RE.findall(body):
            if (monthly, yearly) not in pairs:
                pairs.append((monthly, yearly))

    if not pairs:
        print("\nNo price pair found. The markup changed. Read references/pages.md.")
        return

    print("\nmonthly            yearly (per month)  year total")
    print("-----------------  ------------------  ----------")
    for monthly, yearly in pairs:
        rate = NUM_RE.search(yearly)
        total = f"{float(rate.group(1)) * 12:g}" if rate else "?"
        print(f"{monthly:<17}  {yearly:<18}  {total}")

    print("\nThe yearly column is a rate per month. `amount` takes the year total.")


if __name__ == "__main__":
    main()
