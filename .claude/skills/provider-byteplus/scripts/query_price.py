#!/usr/bin/env python3
"""Print the BytePlus Coding Plan prices. Usage: python3 query_price.py"""

import json
import urllib.request

URL = "https://www.byteplus.com/api/sales/calculatePriceV5"
REGION = "ap-southeast-1"


def payload(tier: str, times: int) -> dict:
    code = f"Coding_Plan_{tier}_monthly"
    return {
        "ConfigItems": [
            {
                "Product": "ModelArk",
                "ConfigurationCode": code,
                "ChargeItems": [
                    {"ChargeItemCode": f"{code}_{REGION}", "AttrValue": "1"}
                ],
                "Quantity": 1,
                "Period": "monthly",
                "Times": times,
                "Region": REGION,
                "OrderType": 1,
                "SerialNo": "0",
            }
        ]
    }


def query(tier: str, times: int) -> dict:
    body = json.dumps(payload(tier, times)).encode()
    req = urllib.request.Request(
        URL,
        data=body,
        headers={"content-type": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    print(f"{'tier':<6} {'months':>6} {'original':>10} {'discount':>10}")
    for tier in ("Lite", "Pro"):
        for times in (1, 3):
            data = query(tier, times)
            result = data.get("Result") or data.get("result") or data
            original = result.get("TotalOriginalAmount")
            discount = result.get("TotalDiscountAmount")
            print(f"{tier:<6} {times:>6} {str(original):>10} {str(discount):>10}")


if __name__ == "__main__":
    main()
