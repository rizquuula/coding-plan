---
name: provider-devin
description: How to source Devin (Cognition) prices, quotas, and per-model rates for the datasets in this repository. Use when you add or refresh a Devin row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Devin, Cognition, devin.ai, docs.devin.ai, app.devin.ai, cognition.com, ACU, Agent Compute Unit, on-demand credits, full seat, flex seat, Devin Desktop, Windsurf, windsurf.com, SWE-1.7, SWE-1.6, or Adaptive. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Devin — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Devin, so you do not repeat work that already failed.

Everything here was checked on 2026-08-30. Re-check a status before you trust it.

**`devin.ai` is unreadable. `docs.devin.ai` is not.** The whole `devin.ai` host
sits behind a Vercel challenge and returns 429 to every tool this repository
allows. The docs host serves the same numbers as plain Markdown. Start at
`https://docs.devin.ai/admin/billing/self-serve.md` and never touch `devin.ai`.

## Constants

Write the provider as `Devin` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`price_currency` is `USD` in `data/plans.yaml`. `currency` is `USD` in
`data/api_pricing.yaml`. Cognition publishes no other currency.

`region` is `global`.

Cognition sells one product family under three surfaces: Devin (cloud sessions),
Devin CLI, and Devin Desktop. One subscription covers all three. Devin Desktop
is the renamed Windsurf editor. See trap 1.

Devin bills two ways. Self-serve plans bill in dollars, against an included
quota plus prepaid on-demand credits. Enterprise bills in Agent Compute Units
(ACUs) at the rate in the customer's order form. See trap 4.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Free, Pro, Max, Teams prices | `https://docs.devin.ai/admin/billing/self-serve.md` | `curl -sL` |
| Full seat and flex seat prices | `https://docs.devin.ai/admin/billing/self-serve.md` | `curl -sL` |
| The $80 Teams minimum table | `https://docs.devin.ai/admin/billing/self-serve.md` | `curl -sL` |
| How quotas refresh | `https://docs.devin.ai/admin/billing/self-serve.md` | `curl -sL` |
| Enterprise billing unit | `https://docs.devin.ai/admin/billing/enterprise.md` | `curl -sL` |
| What consumes usage | `https://docs.devin.ai/admin/billing/usage.md` | `curl -sL` |
| Per-model token rates | `https://docs.devin.ai/desktop/models.md` | `curl -sL` + `scripts/model_rates.py` |
| Which models Cognition builds | `https://docs.devin.ai/desktop/models.md` | `curl -sL` |
| The plan-lineup announcement | `https://cognition.com/blog/new-self-serve-plans-for-devin` | `curl -sL` |
| Legacy grandfathered prices | `https://docs.devin.ai/desktop/accounts/quota.md` | `curl -sL` |

Append `.md` to any `docs.devin.ai` path to get the Markdown twin. The twin
carries the same numbers in a tenth of the bytes. `https://docs.devin.ai/llms.txt`
lists every page. Details in `references/pages.md`.

## Nine things that produce a wrong number

**1. Devin and Windsurf now share one pricing page, so a search snippet mixes
them.** `windsurf.com/pricing` and `codeium.com/pricing` both 301 to
`devin.ai/pricing`. Devin Desktop is Windsurf renamed, and Cognition sells both
under the same Free / Pro / Max / Teams / Enterprise lineup. A snippet that
pairs Devin's tier prices with "unlimited Tab completions", "unlimited inline
edits", or "SWE-1.7" is not two products merged by mistake. It is one page. Even
so, never copy a feature bullet you did not read on a Cognition page. Read
`docs.devin.ai/admin/billing/self-serve.md` for the plan facts and
`docs.devin.ai/desktop/` for the editor facts.

**2. `devin.ai` returns 429 to everything, not just `/pricing`.** The response
carries `x-vercel-mitigated: challenge` and an `x-vercel-challenge-token` header.
Every path fails the same way, including `/`, `/favicon.ico`, `/robots.txt`, and
a path that does not exist. A 429 from this host is the challenge, not a rate
limit you can wait out. Do not read it as "the page moved".

**3. Teams is a minimum spend, not a seat price.** Every Teams account pays at
least $80 per month. A full seat costs $40 per month. Two full seats clear the
minimum; fewer than two, and Cognition charges the remainder as prepaid
on-demand credits. Flex seats are free and draw on the shared credit pool. Write
`amount: 80` for the month period, because $80 is the floor a Teams account
pays, then state the $40 full seat and the free flex seat in `notes`. Never
write `amount: 40`.

**4. ACUs are Enterprise-only, and Enterprise publishes no price.** Since April
2026, self-serve usage bills in dollars against quota, not in ACUs. Only
Enterprise bills in ACUs, and only at the rate in a private order form. Add no
Enterprise row to `data/plans.yaml`: the `prices` schema needs a number, and
there is none. Never carry an old "$20 Core plan sells ACUs" claim forward.

**5. Core and Team are dead tiers.** Cognition retired the Core plan and the
$500 per month Team plan on 2026-04-14. Core users moved to Free. If a row for
either tier ever lands in `data/plans.yaml`, set `status: discontinued`,
`discontinued_on: 2026-04-14`, and say so in `notes`. Do not add them fresh.

**6. The grandfathered prices are not for sale.** `desktop/accounts/quota.md`
names $15 per month for an existing Pro subscriber and $30 per seat per month
for an existing Teams subscriber. Both are frozen legacy prices for people who
already subscribed. A new customer cannot buy either. Never put them in
`data/plans.yaml`.

**7. `credit_multiplier` in the model table is not a price.** Each entry in the
model cost data carries `input_cost_per_million_usd`,
`output_cost_per_million_usd`, `cache_read_cost_per_million_usd`,
`cache_write_cost_per_million_usd`, and `credit_multiplier`. Only the four cost
fields are dollars per 1M tokens. `credit_multiplier` belongs to the retired
credit system and means nothing in this repository.

**8. A `0` in the model cost data means the page prints an em dash.** The page's
own formatter renders `0` and `null` alike as `—`. So a `0` is "not published",
not "free". Write `null` in `data/api_pricing.yaml` for any field that reads `0`.
Separately, the rendered table has four columns — Model, Input, Cache Input,
Output — so `cache_write_cost_per_million_usd` never reaches a reader. Leave
`cache_write` `null` unless you decide the source field counts as published, and
say which you chose in `notes`.

**9. Only the Cognition models belong under provider `Devin`.** The model table
lists 413 entries across two billing tiers and ten model vendors. The page's own
tab bar labels `MODEL_PROVIDER_WINDSURF` as "Cognition". Every other vendor —
Anthropic, OpenAI, Google, xAI, DeepSeek, Moonshot, Z.ai, Nvidia, Thinking
Machines — is resale, and a row for it would duplicate that vendor's own row
elsewhere in the dataset. Take the SWE family, Adaptive, and the Arena routers.
Leave the rest.

## What Devin does not publish

- **No rate limit.** `https://docs.devin.ai/api-reference/overview.md` lists
  `429 Too Many Requests: Rate limit exceeded` in an error table and names no
  number. No page states requests per minute, tokens per minute, or a
  concurrency cap. `admin/billing/usage.md` says the opposite for sessions:
  "there are no concurrent session limits". Zero Devin rows in
  `data/rate_limits.yaml` is the correct result.
- **No quota number.** Every plan has a "daily and weekly usage allowance", and
  no page states its size in tokens, requests, or dollars. Write the shape of
  the quota in `limits`, never a number.
- **No model specification.** No page states a parameter count, a context
  window, a max output, or a vision capability for any SWE model. A
  `data/models.yaml` row would be nulls in every field. Add none.
- **No annual or quarterly price.** Every published amount is per month.

## Workflow

1. Read `https://docs.devin.ai/admin/billing/self-serve.md`.
2. Take the plan prices: Free $0, Pro $20, Max $200, Teams $80 minimum. Monthly
   only.
3. Encode Teams as `amount: 80`, and put the $40 full seat in `notes`. See
   trap 3.
4. Add no Enterprise row. See trap 4.
5. Write `limits` from the quota shape, not from a number. See "What Devin does
   not publish".
6. For token rates, run `python3 .claude/skills/provider-devin/scripts/model_rates.py`.
   It fetches `https://docs.devin.ai/desktop/models.md` and prints the Cognition
   rows.
7. Map `0` to `null`. See trap 8.
8. Add no row to `data/rate_limits.yaml` and no row to `data/models.yaml`.
9. Use only `docs.devin.ai` and `cognition.com` URLs in `links`. Label the plan
   pages `pricing`, the model rate page `pricing`, and the lineup blog post
   `announcement`.
10. Set `last_verified` to the date you read the page.
11. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL probed, its status, its size, and the verdict |
| `scripts/model_rates.py` | Extracts the Cognition token rates from the docs page |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.

If `devin.ai` ever answers 200, record the exact command that worked in
`references/pages.md`. That is the single most valuable line this skill can
carry.
