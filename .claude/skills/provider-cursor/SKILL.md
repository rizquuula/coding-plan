---
name: provider-cursor
description: How to source Cursor plan prices, usage limits, and model rates for the datasets in this repository. Use when you add or refresh a Cursor row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Cursor, cursor.com, Cursor Pro, Cursor Pro+, Cursor Ultra, Cursor Teams, Composer, or the Cursor Models pool. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Cursor — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Cursor, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Cursor` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables. `region` is `global`. `price_currency` is `USD`.

Cursor sells four individual tiers: Hobby, Pro, Pro+, and Ultra. It sells two
Team seats: Standard and Premium. It sells one India-only tier called Start,
priced in INR. `data/plans.yaml` holds Pro, Pro+, and Ultra today.

Cursor resells third-party models. It does not sell a public per-token API, so
three of the four datasets hold zero Cursor rows. See "Datasets with zero rows".

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices, monthly term | `https://cursor.com/help/account-and-billing/pricing.md` | `curl` |
| Plan prices, yearly term | `https://cursor.com/pricing` | `scripts/read_yearly_prices.py` |
| Tier limits, usage pools | `https://cursor.com/docs/models-and-pricing.md` | `curl` |
| Tier feature lines | `https://cursor.com/pricing` | `curl` |
| Usage-limit wording | `https://cursor.com/help/models-and-usage/usage-limits.md` | `curl` |
| Per-model token rates | `https://cursor.com/docs/models-and-pricing.md` | `curl` |
| Model context window | `https://cursor.com/docs/models/<model>` | `curl` |
| Team seat prices | `https://cursor.com/docs/account/teams/pricing.md` | `curl` |
| Every documentation URL | `https://cursor.com/llms.txt` | `curl` |

## Six things that produce a wrong number

**1. The pricing page ships one price per picker, not one tier.** `WebFetch` on
`https://cursor.com/pricing` returned "Not specified" for Pro+ and Ultra, and it
read the Teams Premium price as `$40`. The real Premium price is `$120`. Take
plan prices from `help/account-and-billing/pricing.md` instead. Detail in
`references/pages.md`.

Only the **price** is toggle-gated. `curl` on the same page returns the feature
lines for all three individual tiers and both Teams seats, in picker order.
Confirmed 2026-08-28. Use `curl` for `limits` text; never for a price.

**2. The yearly price is not in the HTML.** The page carries a monthly/yearly
toggle, and the server sends the monthly figures only. The yearly figures sit in
a JavaScript chunk. Run `python3 scripts/read_yearly_prices.py`. It needs no
install and no browser.

**3. Cursor prints a rate per month under the yearly toggle, never a term
total.** Pro reads `$16/mo.` under Yearly. `AGENTS.md` defines `amount` as the
price for the whole term, so write `192` for the year. Multiply by 12 and say so
in `notes`. Table in `references/pricing.md`.

**4. A `.md` twin exists for `/docs/` and `/help/` pages only.** Marketing pages
have none. `https://cursor.com/pricing.md` returns 200 and serves HTML, not
markdown. A caller that trusts the status code reads the wrong body.

**5. A `.md` twin of a redirect path returns 404.** `data/plans.yaml` cites
`https://cursor.com/docs/account/pricing`, which 308-redirects to
`https://cursor.com/docs/models-and-pricing`. Appending `.md` to the old path
404s. Resolve the redirect first, then append `.md`.

**6. Cursor publishes rate limits, but none of them are per model.** The limits
on `https://cursor.com/docs/api` cover the Admin, Analytics, Bugbot, and Cloud
Agents REST APIs. `data/rate_limits.yaml` needs a per-model limit, so it holds
zero Cursor rows. Reasoning in `references/quotas.md`.

**7. "Hidden by default" is a picker state, not an entitlement.** The model
table notes that Kimi, GLM, and most Claude models are "Hidden by default". They
are still included. `help/models-and-usage/available-models.md` states: "Hobby
users have access to a smaller set, while paid plans unlock all models." List a
hidden model in `models` on a paid tier. Detail in `references/quotas.md`.

**8. Composer's base checkpoint is open, Composer is not.** The Composer 2.5
blog says it "is built on the same open-source checkpoint as Composer 2,
Moonshot's Kimi K2.5". That describes the base model. Cursor publishes no
Composer weights, so `open_weights` is `null`, never `true`.

## Datasets with zero rows

Three datasets hold no Cursor row, and each zero is correct.

- `data/api_pricing.yaml` — Cursor sells no public per-token API. The rates on
  `docs/models-and-pricing` are in-product resale rates for other companies'
  models. Only Grok 4.6, Grok 4.5, and Composer 2.5 are Cursor's own. Adding
  those three is a scope decision, not a sourcing problem. Ask first.
- `data/rate_limits.yaml` — Cursor publishes no per-model limit. See trap 6.
- `data/models.yaml` — blocked on `vision` alone. `open_weights` became
  nullable, so it no longer blocks a row. `vision` is still required and
  non-nullable in `build.py`, and no Cursor page states it for Composer or
  Grok. Checked 2026-08-28 across both spec cards, both help pages, the docs
  twins, and the Composer blog. Do not guess it.

Do not add a row of nulls to record any of these absences.

## Workflow

1. Read `https://cursor.com/help/account-and-billing/pricing.md`. Take the
   monthly price of every tier.
2. Run `python3 scripts/read_yearly_prices.py`. Take the yearly rate per month.
3. Multiply each yearly rate by 12. Write the product into `amount`.
4. Read `https://cursor.com/docs/models-and-pricing.md`. Take the usage pools
   and the model list.
5. Read `https://cursor.com/pricing` with `curl`. Take the tier feature lines,
   such as `3x Pro limits on Agent`.
6. Cross-check: every yearly rate is 20 percent under the monthly rate. A tier
   that breaks the pattern is a transcription error.
7. Write the rows. Copy the shapes in `references/data-recipes.md`.
8. Add no row to `data/api_pricing.yaml`, `data/rate_limits.yaml`, or
   `data/models.yaml`.
9. Set `last_verified` to the date you read the pages.
10. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the `.md` twin rules |
| `references/pricing.md` | Plan prices under both terms, the model token rates |
| `references/quotas.md` | Usage pools, tier multipliers, why rate limits are absent |
| `references/data-recipes.md` | A worked row, and why three datasets stay empty |
| `scripts/read_yearly_prices.py` | Prints every tier under both billing terms |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
