#!/usr/bin/env python3
"""Print the GLM Coding Plan prices that https://z.ai/subscribe compiles into its
JavaScript bundle. Standard library only. No browser, no install.

The page renders client-side, so the HTML holds no price. The prices sit in a
Next.js chunk. This script reads the chunk list out of the HTML, fetches each
chunk, and matches the product objects.
"""

import re
import sys
import urllib.error
import urllib.request

PAGE_URL = "https://z.ai/subscribe"
CHUNK_BASE = "https://z.ai"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

CHUNK_RE = re.compile(r'/_next/static/chunks/[^"\'\s]+?\.js')

PRODUCT_RE = re.compile(
    r'\{productId:"(product-[0-9a-f]+)",name:"(Lite|Pro|Max)"'
    r'.*?money:([0-9.]+),oldMoney:([0-9.]+)'
    r'.*?value:"(Monthly|Quarterly|Yearly)"'
    r'.*?version:"(V\d)"'
)

TIER_ORDER = ["Lite", "Pro", "Max"]
TERM_ORDER = ["Monthly", "Quarterly", "Yearly"]


def fetch(url):
    """Return the body of one URL as text."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


def chunk_urls(html):
    """Return every chunk URL in the page, in order, without duplicates."""
    seen = []
    for path in CHUNK_RE.findall(html):
        url = CHUNK_BASE + path
        if url not in seen:
            seen.append(url)
    return seen


def read_products():
    """Fetch the page, then scan chunks until one holds the product list."""
    html = fetch(PAGE_URL)
    urls = chunk_urls(html)
    if not urls:
        raise RuntimeError("The page lists no chunk. The page shape changed.")

    products = []
    for url in urls:
        try:
            text = fetch(url)
        except (urllib.error.URLError, urllib.error.HTTPError):
            continue
        matches = PRODUCT_RE.findall(text)
        if matches:
            products = matches
            print("Chunk with the product list: " + url)
            print("")
            break
    return products


def sort_key(product):
    _, tier, _, _, term, version = product
    return (version, TIER_ORDER.index(tier), TERM_ORDER.index(term))


def print_table(products):
    """Print one block per version, newest last, current version marked."""
    versions = sorted({product[5] for product in products})
    current = versions[-1]
    rows = sorted(products, key=sort_key)

    for version in versions:
        mark = "  <- current, this is the plan Z.ai sells today" if version == current else "  (legacy, do not use)"
        print(version + mark)
        print("  {:<6} {:<10} {:>10} {:>10}".format("tier", "term", "money", "oldMoney"))
        for product_id, tier, money, old_money, term, row_version in rows:
            if row_version != version:
                continue
            print("  {:<6} {:<10} {:>10} {:>10}".format(tier, term, money, old_money))
        print("")


def main():
    try:
        products = read_products()
    except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as error:
        print("Fetch failed: " + str(error), file=sys.stderr)
        return 1

    if not products:
        print(
            "No product matched in any chunk. The bundle shape changed.\n"
            "Fetch the page, list the chunk paths, and grep a chunk for "
            "productId:\"product-. Then fix PRODUCT_RE.",
            file=sys.stderr,
        )
        return 1

    print_table(products)
    print("money is the total charged for the whole term. Copy it into amount.")
    print("Do not multiply it by 3 or by 12.")
    print("Only the highest version is live. V1 and V2 are dead legacy prices.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
