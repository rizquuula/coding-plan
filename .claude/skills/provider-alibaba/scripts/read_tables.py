#!/usr/bin/env python3
"""Print the table rows of an Alibaba Cloud Model Studio doc page.

The Model Studio docs serve a markdown twin at `<page>.md`. That twin keeps
every table as raw HTML on one long line, so `grep` returns a 40 KB line and
`WebFetch` truncates the page. This script fetches the twin, flattens each
HTML table into pipe-delimited rows, and prints the rows you ask for.

Python 3 standard library only. There is nothing to install.

Usage:
    python3 read_tables.py <page> <pattern>
    python3 read_tables.py <page> <pattern> --context

    <page>     a page slug, such as `model-pricing`, or a full https URL.
               A slug reads the English site at
               https://www.alibabacloud.com/help/en/model-studio/<slug>.md
    <pattern>  a case-insensitive regular expression.
    --context  also print the headings and paragraphs that match.

Examples:
    python3 read_tables.py model-pricing '^qwen-max$'
    python3 read_tables.py rate-limit 'qwen3-coder-plus'
    python3 read_tables.py coding-plan '.'
    python3 read_tables.py https://help.aliyun.com/zh/model-studio/coding-plan.md '.'

Every printed row starts with the line number of its table in the twin. Use
that number to find the region heading above the table:

    python3 read_tables.py model-pricing '^####' --context
"""

import html
import re
import sys
import urllib.request

EN_BASE = "https://www.alibabacloud.com/help/en/model-studio/"
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)


def page_url(page):
    """Turn a slug into the URL of its markdown twin."""
    if page.startswith("https://"):
        return page if page.endswith(".md") else page + ".md"
    return EN_BASE + page + ".md"


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read().decode("utf-8", "replace")


def clean(cell):
    """Strip tags and whitespace out of one table cell."""
    text = re.sub(r"<[^>]+>", " ", cell)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def rows_of(line):
    """Yield one list of cell strings per <tr> in an HTML table."""
    for row in re.findall(r"<tr>(.*?)</tr>", line, re.S):
        cells = re.findall(r"<t[dh]>(.*?)</t[dh]>", row, re.S)
        yield [clean(cell) for cell in cells]


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    page, pattern = argv[1], argv[2]
    want_context = "--context" in argv[3:]
    match = re.compile(pattern, re.I).search

    url = page_url(page)
    try:
        body = fetch(url)
    except Exception as error:  # noqa: BLE001 - report and stop
        print(f"fetch failed: {url}\n{error}", file=sys.stderr)
        return 1

    hits = 0
    for number, line in enumerate(body.split("\n"), 1):
        if "<table>" not in line:
            if want_context and line.strip() and match(line):
                print(f"{number}: {line[:300]}")
                hits += 1
            continue
        printed = False
        for cells in rows_of(line):
            if not any(match(cell) for cell in cells):
                continue
            print(f"{number} | " + " | ".join(cells))
            printed = True
            hits += 1
        if printed:
            print("-" * 78)

    if hits == 0:
        print(f"no match for {pattern!r} in {url}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
