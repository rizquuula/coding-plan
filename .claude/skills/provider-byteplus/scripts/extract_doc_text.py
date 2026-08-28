#!/usr/bin/env python3
"""Print the article text of a docs.byteplus.com page.

Usage: python3 extract_doc_text.py https://docs.byteplus.com/en/docs/ModelArk/1925114

The HTML is a shell. The article sits inside window._ROUTER_DATA as escaped
Quill-delta JSON. Tag-stripping returns only the nav. This script reads the
insert ops instead. Standard library only.
"""

import re
import sys
import urllib.request

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
INSERT_RE = re.compile(r'\\"insert\\":\\"((?:[^"\\\\]|\\\\.)*?)\\"')


def fetch(url):
    """Return the raw HTML of one URL as text."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


def decode(capture):
    """Turn one escaped insert into readable text."""
    try:
        return capture.encode("utf-8").decode("unicode_escape").encode("latin1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        try:
            return capture.encode("utf-8").decode("unicode_escape")
        except UnicodeDecodeError:
            return capture


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    html = fetch(sys.argv[1])
    parts = [decode(capture) for capture in INSERT_RE.findall(html)]
    text = "".join(part for part in parts if part.strip() != "*")
    if not text.strip():
        print("No insert op matched. The page shape changed, or the doc is empty.", file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
