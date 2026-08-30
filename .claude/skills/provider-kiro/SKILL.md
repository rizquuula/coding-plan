---
name: provider-kiro
description: How to source Kiro prices, credit allowances, and model access for the datasets in this repository. Use when you add or refresh a Kiro row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Kiro, kiro.dev, Kiro credits, Kiro Free, Kiro Pro, Kiro Pro+, Kiro Pro Max, Kiro Power, Kiro add-on credits, or Kiro GovCloud. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Kiro — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Kiro, so you do not repeat work that already failed.

Everything here was checked on 2026-08-30. Re-check a status before you trust it.

**Kiro is easy to source.** The site serves an `llms.txt` index and a Markdown
twin for every docs page. Two pages carry every value this repository needs:
`https://kiro.dev/pricing/` for the prices, and
`https://kiro.dev/docs/models.md` for the model access matrix.

## Constants

Write the provider as `Kiro` in all five data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`price_currency` is `USD` in `data/plans.yaml`. Kiro publishes no other
currency. Prices exclude tax.

`region` is `global`. Kiro sells to a long country list and serves inference
from US and EU AWS geographies. The enum holds no finer value.

Kiro sells credits, not tokens. A credit is "a unit of work in response to user
prompts". Each model carries a credit multiplier relative to `Auto` at 1.0x.
Kiro publishes no price per 1M tokens anywhere. See trap 1.

Kiro is an AWS product. It runs on Amazon Bedrock and bills enterprise seats
through AWS.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Tier prices for Free, Pro, Pro+, Pro Max, Power | `https://kiro.dev/pricing/` | `WebFetch` or `curl -sL` |
| Credits per month per tier | `https://kiro.dev/docs/billing.md` | `curl -sL` |
| Add-on credit price and pack sizes | `https://kiro.dev/docs/billing/add-on-credits.md` | `curl -sL` |
| Which models each tier unlocks | `https://kiro.dev/docs/models.md` | `curl -sL` |
| Context window per model | `https://kiro.dev/docs/models.md` | `curl -sL` |
| Credit multiplier per model | `https://kiro.dev/docs/models.md` | `curl -sL` |
| Which models are open weight | `https://kiro.dev/docs/models/available-models.md` | `curl -sL` |
| GovCloud uplift, credit reset, metering | `https://kiro.dev/pricing/` FAQ | `curl -sL` |
| Enterprise tier structure | `https://kiro.dev/docs/enterprise/billing.md` | `curl -sL` |
| The full docs page index | `https://kiro.dev/llms.txt` | `curl -sL` |

The pricing page is server-rendered. `curl -sL -A "Mozilla/5.0"` returns the
full body, 200 and about 185 KB, FAQ answers included. No bundle recipe and no
script are needed. This skill ships no `scripts/` directory.

## Eight things that produce a wrong number

**1. Kiro publishes no per-token rate.** The site states credit multipliers, not
dollars per 1M tokens. `data/api_pricing.yaml` needs `input` and `output` as
numbers per 1M tokens, and Kiro states neither. Add no Kiro row to that file.
Never convert `$0.04 per credit` into a token rate. A credit is a unit of work,
not a token count.

**2. Kiro publishes no numeric rate limit.** The pricing page says Free tier
"Access is subject to rate limits" and names no number. No docs page states
requests per minute, tokens per minute, or a concurrency limit. Zero Kiro rows
in `data/rate_limits.yaml` is the correct result. Do not fill the gap.

**3. The `.md` twin lives only under `/docs/`.** `https://kiro.dev/docs/models.md`
returns 200. `https://kiro.dev/pricing.md` and
`https://kiro.dev/pricing/index.md` both return 404. Use `WebFetch` or `curl`
on the pricing HTML instead.

**4. A Kiro 404 returns about 97 KB.** The not-found page is large, so body size
is not a signal that a page exists. Check the HTTP status code, never the size.

**5. The pricing page and the models page disagree about the Free tier.** The
pricing footnote says Free gets "Claude Sonnet 4.5 and open weight models such
as Qwen3 Coder Next, DeepSeek 3.2, and MiniMax M2.1". The quick-comparison table
on `docs/models.md` marks eight models free: Auto, Claude Sonnet 4.5, Claude
Sonnet 4.0, DeepSeek 3.2, MiniMax M2.5, MiniMax M2.1, GLM-5, and Qwen3 Coder
Next. The footnote says "such as", so it is a sample, not the list. Take the
list from the table.

**6. GovCloud is "approximately 20% higher", not a price.** The FAQ states no
GovCloud dollar figure. Never multiply a commercial price by 1.2 and write the
result. State the uplift in `notes` and leave `prices` at the commercial figure.

**7. Enterprise is not a sixth tier.** `docs/enterprise/billing.md` sells the
same four paid tiers through AWS with the same credit allowances. The pricing
page shows an Enterprise card with "Contact sales" and no price. Add no
Enterprise row to `data/plans.yaml`. The schema requires a `prices` amount.

**8. Credits do not roll over, but add-on credits do.** Plan credits reset at
the start of each billing month and unused ones expire. Purchased add-on credits
roll over and expire 12 months from purchase. These are two different rules.
Do not merge them into one `limits` item.

## Workflow

1. Read `https://kiro.dev/pricing/` for the five tier prices.
2. Read `https://kiro.dev/docs/billing.md` for the credit allowance table.
3. Read `https://kiro.dev/docs/models.md` for the per-tier model matrix.
4. Write one `data/plans.yaml` record per tier: Free, Pro, Pro+, Pro Max, Power.
5. Use `month` as the only `prices` period. Kiro publishes no yearly term.
6. Add no Enterprise row and no GovCloud row.
7. Add no row to `data/api_pricing.yaml`.
8. Add no row to `data/rate_limits.yaml`.
9. Add no row to `data/models.yaml`. See trap 1 and the note below.
10. Use only `kiro.dev` URLs in `links`. Label the pricing page `pricing` and a
    docs page `docs`.
11. Set `last_verified` to the date you read the page.
12. Run `python3 build.py --check`.

### Why `data/models.yaml` stays empty

Kiro resells models from OpenAI, Anthropic, MiniMax, Zhipu, DeepSeek, and
Alibaba. `docs/models.md` states a context window and a credit multiplier for
each, and `docs/models/available-models.md` names five of them open weight. It
states no parameter count, no max output, and no vision claim. A Kiro-provider
row would duplicate a row that already sits under the model's real provider.
Add none unless the maintainer asks for Kiro-scoped model rows.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, and the values each page states |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
