---
name: provider-commandcode
description: How to source CommandCode prices, credits, and plan limits for the datasets in this repository. Use when you add or refresh a CommandCode row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions CommandCode, Command Code AI, commandcode.ai, GOAT, taste-1, Max 10x, Max 20x, or the Provider plan. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# CommandCode — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to CommandCode, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

**Start at the pricing page.** `https://commandcode.ai/pricing` states every plan
price, every included credit amount, and every estimated request count. The docs
pages add detail. No other page holds a plan number this repository needs.

## Constants

Write the provider as `CommandCode` in all four data files. The build script
groups rows by that exact string, so any other spelling splits the provider into
two tables.

`price_currency` is `USD` in `data/plans.yaml`. `currency` is `USD` in
`data/api_pricing.yaml`. The site prints no other currency.

`region` is `global`. The FAQ says the models run on US infrastructure.

Command Code AI sells a CLI coding agent plus an API reseller service. Its own
model, `taste-1`, learns the user's coding preferences. Every plan includes it.
Every other model is a third-party model resold at "API cost, zero markup".

Every page is server-rendered. `WebFetch` and `curl -sL -A "Mozilla/5.0"` both
return the full HTML. No bundle recipe is needed. This skill ships no `scripts/`
directory.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices, credits, request estimates | `https://commandcode.ai/pricing` | `WebFetch` |
| Dated promotional deals | `https://commandcode.ai/pricing` | `WebFetch` |
| Full pricing detail and usage estimates | `https://commandcode.ai/docs/resources/pricing-limits` | `WebFetch` |
| Per-model allowances on GOAT | `https://commandcode.ai/docs/plans/goat` | `WebFetch` |
| taste-1 specifications | `https://commandcode.ai/docs/taste` | `WebFetch` |
| Per-model resale rates | `https://commandcode.ai/models/<slug>` | `WebFetch` |
| Every page URL | `https://commandcode.ai/sitemap.xml` | `curl` |

The sitemap is real `application/xml`, 200 and about 15 KB. It lists about 44
model slugs, such as `claude-fable-5`, `fugu-ultra`, `gpt-5-6-luna`, `glm-5-3`,
and `deepseek-v4-pro`. Use it to find a page. Details in `references/pages.md`.

## Ten things that produce a wrong number

**1. Every advertised price excludes a processing fee.** The page prints
"$X/month + processing fee" and never states the fee. Record the listed price.
Say "plus processing fee" in `notes`.

**2. "Up to $X usage with deals" is marketing, not credits.** GOAT prints "$70 in
credits" and also "up to ~$100 usage with deals". Record the credit amount.
Never record the deal-inflated number.

**3. The estimated request counts carry a tilde.** "~75K requests" is an estimate
derived from credit math, not a quota. Keep the tilde when you quote one in
`limits`, or leave it out of the row.

**4. Deals expire, and the page keeps stale ones.** Ling 3.0 Flash "free through
August 2, 2026" still showed on 2026-08-28, after the date passed. Never bake a
dated deal into a rate. A deal belongs in `notes` with its end date, if anywhere.

**5. The site root soft-404s with HTTP 200.** `https://commandcode.ai/pricing.md`
and `https://commandcode.ai/llms.txt` return 200 and a ~36 KB app shell. There is
no `.md` twin and no `llms.txt`. A 200 from `commandcode.ai` does not mean the
page exists, so check the content. The `/docs/` subtree behaves differently and
returns a real 404 status.

**6. "Up to 1M" context is a plan claim about available models.** It is not a
model specification. Never write a `context_window` from it.

**7. Rate limits are words, not numbers.** The page prints Standard, Higher, and
Highest. No page states a per-minute limit, an RPM, or a concurrency number.
Zero CommandCode rows in `data/rate_limits.yaml` is the correct result. Put the
tier word in the plan's `notes` if it matters.

**8. taste-1 is the only CommandCode-owned model.** A `data/models.yaml` row
needs `https://commandcode.ai/docs/taste` read first. That page was not probed.
The third-party model cards under `/models/` are resale pages. Cite one for a
CommandCode row only. Never cite one as a source for the upstream provider's own
rows.

**9. The pages are huge, so a wide-context regex hangs.** The pricing page is
about 313 KB and the docs pages reach about 633 KB. A pattern such as
`.{0,150}foo.{0,150}` backtracks for minutes. Strip the tags in Python first,
then search the text. Same hazard as the DeepSeek skill's trap 11.

**10. The Teams price may not be per seat.** The `prices` schema defines `amount`
per seat. The page says "$40/month" and "One team. One bucket." Record the price
as written and flag the ambiguity in `notes`.

## Workflow

1. Read `https://commandcode.ai/pricing`.
2. Write one `data/plans.yaml` record per tier: Go, GOAT, Pro, Max 10×, Max 20×,
   Teams, Provider.
3. Add no Enterprise record. `prices` requires a numeric `amount`, and the page
   states custom pricing only.
4. Put the credit amount and the request estimate in `limits`.
5. Add no row to `data/rate_limits.yaml`. See trap 7.
6. Read `https://commandcode.ai/docs/resources/pricing-limits` for detail.
7. Read `https://commandcode.ai/docs/plans/goat` for the per-model allowances.
8. Add a `data/api_pricing.yaml` row only after you read a `/models/<slug>` card.
9. Label `/pricing` as `plans`, a docs page as `docs`, and a `/models/<slug>`
   page as `model card`.
10. Set `last_verified` to the date you read the pages.
11. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, the plan values, the deals, the outbound links |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
