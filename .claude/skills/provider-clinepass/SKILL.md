---
name: provider-clinepass
description: How to source ClinePass prices, quotas, and per-model reference rates for the datasets in this repository. Use when you add or refresh a ClinePass row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Cline, ClinePass, Cline Pass, cline.bot, docs.cline.bot, app.cline.bot, api.cline.bot, the cline-pass model slugs, or Cline Bot Inc. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# ClinePass — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to ClinePass, so you do not repeat work that already failed.

Everything here was checked on 2026-08-30. Re-check a status before you trust it.

**Two pages hold everything.** `https://docs.cline.bot/getting-started/clinepass`
states the recurring price, the model table with model ids, the per-model
reference rates, and the three usage windows. `https://cline.bot/cline-pass`
states the promotional first-month price. Read the docs page first. Read the
marketing page only for the promotion.

## Constants

Write the provider as `ClinePass` in all five data files. The maintainer chose
that spelling over `Cline`. The build script groups rows by that exact string,
so any other spelling splits the provider into two tables.

`price_currency` is `USD` in `data/plans.yaml`. `currency` is `USD` in
`data/api_pricing.yaml`. Cline publishes no other currency.

`region` is `global`. Cline Bot Inc. is a United States company.

ClinePass sells exactly one tier. One record in `data/plans.yaml` is the correct
result. The Cline pricing page sells a different product. See trap 2.

ClinePass is a reseller, not a model lab. It resells open-weight models from
Z.ai, Moonshot AI, DeepSeek, MiniMax, MiMo, and Qwen behind one
OpenAI-compatible endpoint at `https://api.cline.bot/api/v1/chat/completions`.

Every page is server-rendered. `WebFetch` and `curl -sL -A "Mozilla/5.0"` both
return the full body. No bundle recipe and no script are needed. This skill
ships no `scripts/` directory.

The docs host serves an `.md` twin. Append `.md` to any `docs.cline.bot` path.
`https://docs.cline.bot/getting-started/clinepass.md` returns 7360 bytes of
clean Markdown against 296284 bytes of HTML. Use the twin.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Recurring price, $9.99 per month | `https://docs.cline.bot/getting-started/clinepass.md` | `curl -sL` |
| Promotional first month, $4.99 | `https://cline.bot/cline-pass` | `WebFetch` |
| The quota statement, 2-5x | `https://docs.cline.bot/getting-started/clinepass.md` | `curl -sL` |
| The three usage windows | `https://docs.cline.bot/getting-started/clinepass.md` | `curl -sL` |
| Model list and model ids | `https://docs.cline.bot/getting-started/clinepass.md` | `curl -sL` |
| Per-model reference rates | `https://docs.cline.bot/getting-started/clinepass.md` | `curl -sL` |
| Which lab owns a model | `https://cline.bot/models/<slug>` | `curl -sL` |
| The launch note | `https://cline.bot/blog/clinepass-best-of-value-for-open-weight-models` | `curl -sL` |

`https://docs.cline.bot/llms-full.txt` carries every docs page in one 654 KB
file. One fetch replaces a crawl. The ClinePass section starts at the line
`# ClinePass`.

Details and every probe result sit in `references/pages.md`.

## Nine things that produce a wrong number

**1. Three prices exist, and only one is the recurring price.** The docs page
states $9.99 per month. The marketing page states $4.99 for the first month.
The launch blog post states $1.99 through the Cline CLI for a limited period.
Write `amount: 9.99` for `period: month`. The `prices` schema holds the price
for one whole term, and a first-month discount is not a term price. State the
promotion in `notes`. Never write 4.99 or 1.99 into `prices`.

**2. `https://cline.bot/pricing` is not the ClinePass page.** It sells the open
source tier at $0 and an Enterprise tier at a custom price. It names no
ClinePass price and no ClinePass quota. Do not read a ClinePass number from it.

**3. The marketing page lists Kimi K3 twice and omits GLM-5.3.** It shows 13
model cards but names only 12 distinct models. The docs table names 13 distinct
models and adds GLM-5.3. Take the model list from the docs table, never from the
marketing page. `https://cline.bot/models` disagrees again: it lists 11
ClinePass models and omits both GLM-5.3 and Qwen3.8 Max.

**4. Cline publishes no absolute quota.** "2-5x the usage compared to standard
API rate" names a multiplier and never names its base. The docs name three
windows — a 5-hour rolling window, a calendar week, and a calendar month — and
attach no number to any of them. Every field in `data/rate_limits.yaml` is a
plain integer, so ClinePass gets zero rows there. Keep the multiplier as a
`limits` string in `data/plans.yaml`. Never divide, multiply, or guess a base.

**5. The reference rates are not what a subscriber pays.** The docs say "you are
not charged the individual API prices below". They are the underlying per-1M
rates, published so a reader can see how usage meters against the quota. Put
that sentence in `notes` on every `data/api_pricing.yaml` row you add, or the
table claims ClinePass bills per token.

**6. Four models publish two rate rows each, not one.** DeepSeek V4 Pro and
DeepSeek V4 Flash each publish a peak and an off-peak rate. Qwen3.7 Plus
publishes one rate at or below 256K tokens and another above it. The schema
holds one rate per field. Record the peak rate and the at-or-below-256K rate in
the fields, then state the second rate in `notes`.

**7. `cline.bot/blog/<unknown>` returns a soft 404.** The blog route answers
HTTP 200 with a "404 not found" body, about 62 KB. Every other `cline.bot` path
returns a real 404 with a 34507-byte body. Read the body of a blog fetch before
you cite it. Take blog URLs from `https://cline.bot/sitemap.xml`.

**8. `https://api.cline.bot/api/v1/models` lists the wrong provider.** It
returns 396 models for Cline (usage-billing), and not one `cline-pass/` slug. It
carries only `id`, `object`, `created`, and `owned_by`. It states no context
window and no price. It cannot source a ClinePass value.

**9. Cline publishes no model specification.** No page states a parameter count,
a context window, a max output, or a vision capability for any ClinePass model.
The 256K threshold on Qwen3.7 Plus is a billing tier, not a context window.
Never write `context_window: 256K`. The pages under `https://cline.bot/models/`
do state `Availability: open-weight`, which sources `open_weights: true` and
nothing else.

## Workflow

1. Read `https://docs.cline.bot/getting-started/clinepass.md`.
2. Take the recurring price, $9.99 per month. It is the only term Cline sells.
3. Read `https://cline.bot/cline-pass` for the promotion, $4.99 first month.
   Put the promotion in `notes`.
4. Take the quota strings for `limits`: the 2-5x multiplier and the three usage
   windows. Keep each string under 12 words.
5. Take the 13 models and their ids from the docs table, not the marketing page.
6. Add no row to `data/rate_limits.yaml`. Cline publishes no integer.
7. Add an `data/api_pricing.yaml` row per model only when the maintainer wants
   the reference rates. Carry the "not charged" sentence in `notes` on each row.
8. Match every `data/models.yaml` name to its `data/api_pricing.yaml` model, or
   the left join renders two rows.
9. Use only `cline.bot` and `docs.cline.bot` URLs in `links`. Label the plan row
   `plans` and the docs page `pricing`.
10. Set `last_verified` to the date you read the page.
11. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, and every value the page states |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
