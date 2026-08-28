---
name: provider-byteplus
description: How to source BytePlus (ModelArk Coding Plan) tiers, quotas, and promotions for the datasets in this repository. Use when you add or refresh a BytePlus row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions BytePlus, ModelArk, Coding Plan, ArkClaw, Dola-Seed, Seed-Code, byteplus.com, or ai.byteplus.com. Records which page holds each value, which tool reads it, and the traps that produce a wrong number — including the exact payload the price API needs.
---

# BytePlus — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to BytePlus, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

**The plan price is readable without a login.** Every tier card still
server-renders the literal text "Loading pricing…", so a text scraper finds no
number. The number is one script away. Run `scripts/query_price.py`. It POSTs to
the price API on the `www.byteplus.com` host, which answers anonymous calls. A
logged-out browser sees the same prices on the campaign page. See trap 1 for the
two mistakes that hide this.

## Constants

Write the provider as `BytePlus` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`price_currency` and `currency` would be `USD`. Every public figure on the
campaign page is a dollar figure.

`region` is `global`. BytePlus is ByteDance's international brand, run by
BytePlus Pte Ltd in Singapore.

BytePlus is the company. ModelArk is its model platform. The ModelArk Coding
Plan is a subscription for AI coding tools. ArkClaw is the BytePlus AI agent
product, free to Pro subscribers for the length of the subscription.

BytePlus sells two personal tiers, Lite and Pro, on a Monthly or Quarterly
toggle. A Team edition sells Team Lite and Team Pro by seat, minimum 5 seats. An
Agent Plan with Small, Medium, Large, and Max SKUs also exists in the buy-flow
code.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Tier quotas, models, refresh rules, tool list | `https://docs.byteplus.com/en/docs/ModelArk/1925114` | `scripts/extract_doc_text.py` |
| Tier cards, feature list, FAQ | `https://ai.byteplus.com/en/activity/codingplan` | `curl -sL -A "Mozilla/5.0"` |
| Team seat rules | `https://docs.byteplus.com/en/docs/ModelArk/2276791` | `scripts/extract_doc_text.py` |
| Referral campaign terms and dates | `https://docs.byteplus.com/en/docs/ModelArk/2165246` | `scripts/extract_doc_text.py` |
| First-purchase offer status | `https://docs.byteplus.com/en/docs/ModelArk/1928265` | `scripts/extract_doc_text.py` |
| Supported AI coding tools | `https://docs.byteplus.com/en/docs/ModelArk/1928262` | `scripts/extract_doc_text.py` |
| Every top-level page URL | `https://www.byteplus.com/sitemap.xml` | `curl` |
| The plan prices | `POST https://www.byteplus.com/api/sales/calculatePriceV5` | `scripts/query_price.py` |

`WebFetch` reads none of these usefully. The campaign host needs `curl`, and the
docs host needs the script. Details and every probe result sit in
`references/pages.md`.

## Twelve things that produce a wrong number

**1. The price API answers anonymously, but two mistakes make it look private.**
An earlier pass concluded the price was login-gated. That conclusion was wrong.
Two separate errors produced it.

First, the host. `POST https://console.byteplus.com/api/sales/calculatePriceV5`
does 302 to `/signin/login`. That is true of the console host only. Never
conclude from it that the price is private. The same path on
`https://www.byteplus.com` answers an unauthenticated call with the real amount,
and `ai.byteplus.com` answers too.

Second, the payload. Omit `Period`, `Times`, or `Region` and the API returns
HTTP 200 with `"TotalOriginalAmount":"0"`. That is a silent wrong-payload
failure, not a free plan. A zero here always means your payload is incomplete.
Send all three fields. `scripts/query_price.py` sends them.

The campaign cards still server-render "Loading pricing…" plus untranslated
Chinese placeholders (订阅时长, 协议), and the docs Team page still renders a
"Monthly price" header with no values. Neither fact means the price is
unreadable.

**2. "First month from $10 USD" names no tier, even though the figure is
right.** It comes from the site-header i18n strings. It matches the verified
Lite monthly price, so it is consistent marketing rather than a separate floor.
It still names no tier, so you cannot tell from it which plan costs 10 USD.
Never source a price from it. Run `scripts/query_price.py` instead.

The referral share text states a second figure, "the first month from $4.50
USD". No page explains that one. Never copy it into `prices`, into `notes`, or
anywhere else.

**3. `www.byteplus.com/en/activity/codingplan` is an empty JavaScript shell.**
It is 29 KB and says "You need to enable JavaScript". `WebFetch` returns an
empty body. Read `https://ai.byteplus.com/en/activity/codingplan` instead. The
`ai.` host server-renders the same campaign at about 543 KB. The
`/activity/arkcodingplan` sibling has the same shape. The `plans` link on both
`data/plans.yaml` rows points at the `www` URL on purpose, because a human
reader's browser renders it. Keep that link as it is, and read the `ai.` twin
yourself.

**4. Docs articles hide inside `window._ROUTER_DATA` as Quill JSON.** Stripping
the HTML tags yields only the nav, so the page looks like a client-side dead
end. It is not. Run `scripts/extract_doc_text.py <url>`. It matches the escaped
insert ops and decodes them.

**5. Quill table cells arrive out of reading order, and some cells are absent.**
The quota cells are present. The price cells are not. Read the extracted text
carefully before you conclude that a table is complete.

**6. The model lists disagree across pages.** The campaign hero names GLM-5.2
and DeepSeek-V4. The campaign FAQ names DeepSeek-V3.2, GLM-5.1, and GLM-4.7. The
referral doc adds MiniMax. Doc `1925114` holds the authoritative current list.
Use it and ignore the others.

**7. The quotas are plan quotas, not API rate limits.** The doc states that the
plan quota cannot be used for API calls at all. Calling the plan's Base URL
outside an AI coding tool counts as abuse and can suspend the account. Zero
BytePlus rows in `data/rate_limits.yaml` is the correct result.

**8. "3x Claude Pro" is a comparative marketing claim.** So is "3x Claude Max's
usage". Record the request counts BytePlus publishes. Never derive a BytePlus
number from Anthropic's published quotas.

**9. `DocumentID` is not the URL code.** They are two id spaces. Doc `84312` is
not the URL `/docs/ModelArk/84312`. Map an id through the `DocumentID` and
`DocumentCode` fields in the `window._ROUTER_DATA` JSON of any docs page before
you fetch.

**10. The docs PDF exports sit on a dead host.** The router data lists per-tab
PDF exports of the whole docs tree on
`eps-common-private-johor.dualstack.ap-southeast-1.tos.bytepluses.com`. That host
does not resolve in DNS. Do not burn time on it.

**11. BytePlus model specifications are resale terms.** BytePlus resells GLM,
DeepSeek, Kimi, and GPT-OSS models. Never cite a BytePlus page as the source for
a Zhipu, DeepSeek, Moonshot, or OpenAI row. Cite the model owner's own page.
This matches the convention in the OpenCode skill.

**12. Promotions carry dates and change.** BytePlus suspended first-purchase
discounts on 2026-03-17 (UTC+8). The referral campaign runs 2026.01.13 to
2026.09.30. Re-read docs `1928265` and `2165246` on every refresh before you
repeat a promotional claim.

## Workflow

`data/plans.yaml` holds a `byteplus-lite` row and a `byteplus-pro` row. A
refresh updates those two rows. It does not create them.

1. Run `python3 scripts/query_price.py`. It prints the four amounts: Lite and
   Pro, over 1 month and 3 months.
2. Copy each amount into `prices` as the whole-term price. `Times: 3` is the
   `quarter` entry. Never write the monthly equivalent.
3. Check `TotalDiscountAmount` against `TotalOriginalAmount`. A gap means a live
   discount. Record the original amount and state the discount in `notes`.
4. Run `python3 scripts/extract_doc_text.py https://docs.byteplus.com/en/docs/ModelArk/1925114`.
5. Take the tier quotas, the model list, and the refresh rules from that output.
6. Fetch `https://ai.byteplus.com/en/activity/codingplan` with
   `curl -sL -A "Mozilla/5.0"` for the tier cards and the FAQ.
7. Never add a `data/rate_limits.yaml` row from the plan quotas. See trap 7.
8. Re-read docs `1928265` and `2165246` for the current promotion dates.
9. Set `last_verified` to the date you read the pages, on every row you touch.
10. Run `python3 build.py --check` and fix every error it prints.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, the verified quotas and models, the promo dates |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
