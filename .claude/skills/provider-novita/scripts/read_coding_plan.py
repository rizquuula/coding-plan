#!/usr/bin/env python3
"""Print every value the Novita Coding Plan page shows, from Novita's own APIs.

The page at https://novita.ai/coding-plan renders its prices client side. This
script reads the two JSON endpoints that the page and the docs call. It needs
no key, no install, and no browser.

Endpoint 1  https://api-server.novita.ai/v1/product/resource-pack-specs/list
            Plan tiers, prices, quotas, per-tier RPM and TPM, and the nine
            models the plan covers with their pay-as-you-go rates.
Endpoint 2  https://api-server.novita.ai/v1/product/model/list
            Per-model context size, max output, modalities, and the T1-T5
            rate limits that https://novita.ai/docs/guides/llm-rate-limits
            renders.

Divide `price` and `quota` by 10000. The site does the same. See SKILL.md trap 3.

Usage:  python3 read_coding_plan.py
"""

import json
import urllib.request

BASE = "https://api-server.novita.ai"
SPECS = BASE + "/v1/product/resource-pack-specs/list"
MODELS = BASE + "/v1/product/model/list"
SCALE = 10000


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    specs = get(SPECS)
    models = {row["id"]: row for row in get(MODELS)["data"]}

    for pack in specs["list"]:
        if pack.get("type") != 1:
            continue  # The page keeps only type 1. Other types are not the plan.
        print(f"# {pack['name']}  (id {pack['id']})")
        print(f"  billing cycle {pack['billingCycle']}, validity "
              f"{pack['validityPeriod']} {pack.get('validityPeriodUnit', '')}, "
              f"buy limit {pack['userBuyLimit']}")
        print()
        print(f"  {'tier':6s} {'USD/month':>10s} {'quota':>14s} {'RPM':>6s} {'TPM':>10s}")
        for tier in pack["tierList"]:
            price = int(tier["price"]) / SCALE
            discount = int(tier["discountPrice"]) / SCALE
            quota = int(tier["quota"]) / SCALE
            flag = "" if price == discount else f"  (list {price:g})"
            print(f"  {tier['tier']:6s} {discount:>10.2f} {quota:>14,.0f} "
                  f"{tier['rpm']:>6s} {int(tier['tpm']):>10,d}{flag}")
        print()

        print("  Models covered, pay-as-you-go USD per 1M tokens:")
        head = f"  {'model id':26s} {'display':22s} {'in':>7s} {'out':>7s} {'cache read':>10s} {'ctx':>9s} {'max out':>9s}"
        print(head)
        for rule in pack["deductRules"]:
            info = rule["priceInfo"]
            model = models.get(rule["displayName"], {})
            print(f"  {rule['displayName']:26s} {model.get('display_name', '?'):22s} "
                  f"{info['inputTokenDecimal'] or '-':>7s} "
                  f"{info['outputTokenDecimal'] or '-':>7s} "
                  f"{info['cacheReadInputTokenDecimal'] or '-':>10s} "
                  f"{model.get('context_size', '?'):>9} "
                  f"{model.get('max_output_tokens', '?'):>9}")
        print()

        print("  Rate limits per model and account tier, RPM / TPM:")
        for rule in pack["deductRules"]:
            model = models.get(rule["displayName"])
            if not model:
                print(f"  {rule['displayName']:26s} not in model/list")
                continue
            cells = "  ".join(
                f"{item['tier']} {item['rpm']}/{item['tpm']:,}"
                for item in model.get("quota_items", [])
            )
            print(f"  {rule['displayName']:26s} {cells}")
        print()


if __name__ == "__main__":
    main()
