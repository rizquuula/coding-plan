# BytePlus page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## Probe results

| URL | Status and size | Tool | Verdict |
|---|---|---|---|
| `https://www.byteplus.com/en/activity/codingplan` | 200, 29 KB | `curl`, `WebFetch` | Client-side React shell. "You need to enable JavaScript". Zero data. `WebFetch` returns an empty body. |
| `https://ai.byteplus.com/en/activity/codingplan` | 200, ~543 KB | `curl -sL -A "Mozilla/5.0"` | The server-rendered twin. Tier cards, features, FAQ. Use this one. The card price arrives client-side, so the HTML still reads "Loading pricing…". A logged-out browser shows the real prices on the Monthly and Quarterly toggle. |
| `https://ai.byteplus.com/en/activity/arkcodingplan` | 200 | `curl -sL -A "Mozilla/5.0"` | Same campaign shape. No extra value. |
| `https://docs.byteplus.com/en/docs/ModelArk/1925114` | 200 | `scripts/extract_doc_text.py` | The Coding Plan overview. Authoritative for quotas, models, refresh rules, tools. |
| `https://docs.byteplus.com/en/docs/ModelArk/2165246` | 200 | `scripts/extract_doc_text.py` | Time-limited referral campaign terms. |
| `https://docs.byteplus.com/en/docs/ModelArk/1928265` | 200 | `scripts/extract_doc_text.py` | First-purchase offers notice. |
| `https://docs.byteplus.com/en/docs/ModelArk/2276791` | 200 | `scripts/extract_doc_text.py` | Coding Plan Team overview. Price table header with no values. |
| `https://docs.byteplus.com/en/docs/ModelArk/2252928` | 200 | `scripts/extract_doc_text.py` | "Agent Plan / Coding Plan" pricing doc. Zero insert ops, no extractable text. Dead end. |
| `https://docs.byteplus.com/en/docs/ModelArk/1928262` | 200 | `scripts/extract_doc_text.py` | Integrate with AI programming tools. |
| `https://docs.byteplus.com/en/docs/ModelArk/coding-plan` | 200, 319 KB | `curl` | Renders its body client-side. No article text in the HTML. |
| `https://www.byteplus.com/en/pricing` | 200, 106 KB | `curl` | Renders its body client-side. No price in the HTML. |
| `POST https://www.byteplus.com/api/sales/calculatePriceV5` | 200, JSON | `scripts/query_price.py` | The price API. Answers anonymous calls. Verified 2026-08-28: Lite 1 month 10 USD, Lite 3 months 30, Pro 1 month 50, Pro 3 months 150. Needs `Period`, `Times`, and `Region` in the payload. |
| `POST https://console.byteplus.com/api/sales/calculatePriceV5` | 302 to `/signin/login` | `curl` | The same path on the console host. Login-gated. Use the `www` host instead. |
| `eps-common-private-johor.dualstack.ap-southeast-1.tos.bytepluses.com` | DNS does not resolve | `curl` | The docs PDF export bucket named in the router data. Dead host. |
| `https://www.byteplus.com/sitemap.xml` | 200, ~637 KB | `curl` | Real XML, about 444 entries. Top-level pages only, each with about 12 locale twins. No blog posts. |
| `res.gcloudcache.com/bp-fe/portal/byteplus-campaign/` | 200 per chunk | `curl` | About 65 webpack chunks. Header and footer i18n strings only. No prices. |

## The price API

The campaign page calls one endpoint for every tier card:

    POST https://www.byteplus.com/api/sales/calculatePriceV5

Pick the host with care. `console.byteplus.com` serves the same path but 302s to
`/signin/login`. `www.byteplus.com` and `ai.byteplus.com` answer anonymous
calls. Send a `Mozilla/5.0` User-Agent.

The full `ConfigItems` entry:

```json
{
  "Product": "ModelArk",
  "ConfigurationCode": "Coding_Plan_Lite_monthly",
  "ChargeItems": [
    {"ChargeItemCode": "Coding_Plan_Lite_monthly_ap-southeast-1", "AttrValue": "1"}
  ],
  "Quantity": 1,
  "Period": "monthly",
  "Times": 1,
  "Region": "ap-southeast-1",
  "OrderType": 1,
  "SerialNo": "0"
}
```

`Coding_Plan_Pro_monthly` is the Pro form. `Times` is the number of months: 1
for the monthly tier card, 3 for the quarterly one.

Drop `Period`, `Times`, or `Region` and the API still returns HTTP 200, with
`"TotalOriginalAmount":"0"`. Treat a zero as a broken payload, never as a price.

`scripts/query_price.py` runs all four calls and prints the amounts.

Verified on 2026-08-28, in USD:

| Tier | Times | TotalOriginalAmount | TotalDiscountAmount |
|---|---|---|---|
| Lite | 1 | 10 | 10 |
| Lite | 3 | 30 | 30 |
| Pro | 1 | 50 | 50 |
| Pro | 3 | 150 | 150 |

The discount amount equals the original amount, so no discount was live that
day. A gap between the two columns means a live promotion.

## How to read a docs page

The HTML is a shell plus the whole article, embedded as escaped Quill-delta JSON
inside `window._ROUTER_DATA`. Match the insert ops with this regex over the raw
HTML:

    \\"insert\\":\\"((?:[^"\\\\]|\\\\.)*?)\\"

Decode each capture with `unicode_escape`, then re-encode latin1 and decode
utf-8. `scripts/extract_doc_text.py` does all of it. Table cells arrive as
separate inserts and out of reading order.

The same JSON holds the `DocumentID` and `DocumentCode` fields. That is the only
public map between the two id spaces.

## Verified quota values

From doc `1925114`. Every request count carries "approximately" on the page.

| Tier | Per 5 hours | Per week | Per subscription month |
|---|---|---|---|
| Lite | 1,900 | 12,000 | 24,000 |
| Pro | 9,500 | 60,000 | 120,000 |

Pro is 5x Lite and runs a higher TPM. The campaign cards describe Lite as "3x
usage of the Claude Pro plan" and Pro as "3x Claude Max's usage". Both are
comparative marketing claims. Do not derive numbers from them.

Refresh rules:

- The 5-hour window slides from the first request.
- The weekly counter resets Monday 00:00:00.
- The monthly counter resets on the subscription date.
- An exhausted quota does not spill into another package or the account balance.
- The quota is shared across every supported tool.
- The quota is not usable for API calls. Using the plan's Base URL and API key
  outside an AI coding tool counts as abuse and can suspend the account.

One request is one model invocation. One user prompt triggers 5 to 15
invocations for simple work, and 15 to 30 or more for complex work.

## Verified model list

From doc `1925114`.

| Model | Context | Max output | Note |
|---|---|---|---|
| Auto (`ark-code-latest`) | — | — | Router alias |
| Dola-Seed-2.0-Code | — | — | |
| Dola-Seed-2.0-Pro | — | — | |
| Dola-Seed-2.0-Lite | — | — | |
| ByteDance-Seed-Code | — | — | |
| GLM-5.2 | 1024K | 128K | 1M context in tools |
| GLM-5.1 | 200K | 128K | |
| DeepSeek-V4-Flash | 1024K | 384K | Early-access preview, 1M context in tools |
| DeepSeek-V4-Pro | 1024K | 384K | Preview, "relatively high quota deduction coefficient", 1M context in tools |
| Kimi-K2.5 | 256K | 32K | Max input 224K |
| GPT-OSS-120b | — | — | |
| Skylark-Embedding-Vision | — | — | |

These are resale terms. Never cite a BytePlus page as the source for a Zhipu,
DeepSeek, Moonshot, or OpenAI row in `data/models.yaml`.

## Supported tools

Doc `1925114` lists Claude Code, OpenCode, OpenClaw, TraeCode, Cline, Cursor,
Codex, Roo Code, and Kilo Code. The campaign page adds Kilo Code and Hermes
Agent.

## Team edition

From doc `2276791`:

- Minimum 5 seats.
- Up to 12 months per order, 24 months in total.
- No cancellation. No upgrade and no downgrade.
- One seat equals 1x the usage of the matching personal plan.
- The "Monthly price" table header carries no values.

## Promotion dates

| Promotion | Source | Period and status |
|---|---|---|
| Referral campaign | doc `2165246` | 2026.01.13 to 2026.09.30. The referrer gets a 10% voucher per referral, uncapped. The referee gets 10% off the first order, once. |
| New-user first-purchase offer | doc `1928265` | Original period 2026.01.13 to 2026.07.13. Suspended from 2026-03-17 (UTC+8). |

## What no page states

**The Team and Agent Plan prices.** No page and no verified API call states what
Team Lite, Team Pro, or any Agent Plan SKU costs. The Lite and Pro prices come
from the price API above.

**A plain-text price against a tier name.** No page renders a price as readable
text next to the tier it belongs to. Two promotional blurbs carry a dollar
figure, and neither names a tier:

- "First month from $10 USD. Flexible models, unlimited tools" — site-header
  i18n strings. The figure matches the verified Lite monthly price, so it is
  consistent marketing. It still names no tier.
- "the first month from $4.50 USD" — the referral share text. No page explains
  this figure. Never copy it anywhere.

Read every price from the API, not from either blurb.

No page states an API rate limit either. The plan quotas above are plan quotas,
and the doc says they cannot serve API calls at all.
