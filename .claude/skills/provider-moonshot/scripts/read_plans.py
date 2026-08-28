#!/usr/bin/env python3
"""Print every Kimi membership tier and its price for every billing term.

The membership pricing page renders client-side, so a fetch of the HTML returns
no price. The page calls one public Connect RPC. This script calls it directly.

    python3 read_plans.py            # the live tier names, DOMAIN_NEXUS
    python3 read_plans.py --all      # all three domains
    python3 read_plans.py --json     # the raw response

The endpoint needs no API key and no login. It needs only Python 3 and the
standard library.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

ENDPOINT = (
    "https://www.kimi.com/apiv2"
    "/kimi.gateway.order.v1.GoodsService/ListGoods"
)

# DOMAIN_NEXUS is the domain the membership pricing page itself reads.
# See references/pricing.md before you use another domain.
DOMAINS = ["DOMAIN_NEXUS", "DOMAIN_KIMI", "DOMAIN_CODE"]

TERM = {
    "TIME_UNIT_MONTH": "month",
    "TIME_UNIT_YEAR": "year",
}


def list_goods(domain):
    """Call ListGoods for one domain and return the decoded response."""
    body = json.dumps(
        {
            "domains": [] if domain is None else [domain],
            "pageSize": 0,
            "pageToken": "",
            "paymentChannel": "PAYMENT_CHANNEL_UNSPECIFIED",
        }
    ).encode()
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-msh-platform": "web",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def rows(payload):
    """Flatten one response into (tier, level, term, currency, amount) rows."""
    out = []
    for good in payload.get("goods", []):
        cycle = good.get("billingCycle") or {}
        unit = TERM.get(cycle.get("timeUnit"), cycle.get("timeUnit"))
        duration = cycle.get("duration")
        for amount in good.get("amounts", []):
            cents = int(amount.get("priceInCents", "0"))
            out.append(
                {
                    "tier": good.get("title"),
                    "level": good.get("membershipLevel"),
                    "term": unit,
                    "duration": duration,
                    "currency": amount.get("currency"),
                    "amount": cents / 100,
                    "region": good.get("useRegion"),
                }
            )
    return out


def report(domain):
    payload = list_goods(domain)
    label = domain or "default (empty domains list)"
    print(f"== {label}")
    table = rows(payload)
    if not table:
        print("   no goods returned")
        return
    width = max(len(str(row["tier"])) for row in table)
    for row in sorted(table, key=lambda r: (r["amount"], r["term"])):
        print(
            f"   {str(row['tier']):<{width}}  "
            f"{row['term']:<6} x{row['duration']}  "
            f"{row['currency']} {row['amount']:>9.2f}  "
            f"{row['level']}  {row['region']}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all",
        action="store_true",
        help="read every domain, not only DOMAIN_NEXUS",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the raw response instead of a table",
    )
    args = parser.parse_args()

    targets = DOMAINS if args.all else [None]
    try:
        if args.json:
            for domain in targets:
                json.dump(list_goods(domain), sys.stdout, indent=2)
                sys.stdout.write("\n")
            return 0
        for domain in targets:
            report(domain)
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code} from {ENDPOINT}", file=sys.stderr)
        print("Read references/fetching.md before you retry.", file=sys.stderr)
        return 1
    except urllib.error.URLError as error:
        print(f"cannot reach {ENDPOINT}: {error.reason}", file=sys.stderr)
        return 1
    print(
        "amount is the total for the whole term. "
        "Copy it into `amount` with no arithmetic."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
