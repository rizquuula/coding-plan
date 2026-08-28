---
name: provider-github
description: How to source GitHub Copilot prices, credit allowances, and model rates for the datasets in this repository. Use when you add or refresh a GitHub row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions GitHub, GitHub Copilot, Copilot Pro, Copilot Pro+, Copilot Max, GitHub AI Credits, or premium requests. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# GitHub (Copilot) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to GitHub, so you do not repeat work that already failed.

Every status below comes from a fetch on 2026-08-28. Re-check a status before
you trust it.

## Constants

Write the provider as `GitHub` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables. `region` is `global`. Prices are USD.

GitHub sells Copilot as a subscription. It sells no public model API, so this
repository tracks the subscription only.

Three paid individual tiers exist: **Copilot Pro**, **Copilot Pro+**, and
**Copilot Max**. `data/plans.yaml` carries one row for each.

GitHub bills Copilot usage in **GitHub AI Credits**. One credit costs 0.01 USD.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices, credit totals in USD | `https://github.com/features/copilot/plans` | `WebFetch` |
| Credit allowance per tier, in credits | `https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals` | `WebFetch` |
| Tier summary, model availability per tier | `https://docs.github.com/en/copilot/get-started/plans` | `curl` on the `.md` twin |
| Rate per 1M tokens, per model | `https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing` | `curl` on the `.md` twin |
| Model list and release status | `https://docs.github.com/en/copilot/reference/ai-models/supported-models` | `WebFetch` |
| What GitHub says about rate limits | `https://docs.github.com/en/copilot/concepts/usage-limits` | `WebFetch` |
| Every docs URL | `https://docs.github.com/llms.txt` | `curl` |

Both `github.com` and `docs.github.com` render on the server. `WebFetch` and
`curl` each return the data. You need no script and no browser.

## Six things that produce a wrong number

**1. Premium requests are legacy. Do not write one into an active row.**
GitHub replaced request-based billing with usage-based billing on 2026-06-01.
Premium requests and model multipliers now apply to one closed group: Copilot
Pro and Pro+ subscribers who hold an existing annual plan. Every current tier
bills in AI credits. Detail in `references/billing-model.md`.

**2. The marketing page still prints the label "Premium requests".** The
comparison table on `https://github.com/features/copilot/plans` names its rows
`Premium requests: Base credits`, `Premium requests: Flex allotment`, and
`Premium requests: Total GitHub AI Credits`. The label is stale. The cells hold
AI credits. A grep for "Premium requests" therefore returns current rows under a
dead name.

**3. The same allowance appears in two units.** The marketing page prints
dollars: 15, 70, and 200 per month. The docs print credit counts: 1,500, 7,000,
and 20,000 per month. One credit costs 0.01 USD, so the two forms agree. Pick
one unit per row and state the unit. Table in `references/pricing.md`.

**4. GitHub sells Copilot per month only.** No page prints a yearly price.
Annual plans are legacy and closed to new subscribers. Write one `month` entry
in `prices`. Never multiply the monthly price into a year.

**5. GitHub publishes no numeric rate limit for Copilot.**
`https://docs.github.com/en/copilot/concepts/usage-limits` explains why rate
limits exist and prints no number. `data/rate_limits.yaml` holds zero GitHub
rows and that is correct. Do not add a row of nulls.

**6. The Copilot token rates are resale rates, not the vendor's API price.**
`models-and-pricing` prices another company's model inside Copilot, and it
carries promotions. On 2026-08-28 it listed GPT-5.6 Sol at 2.00 input and 10.00
output, which is a 50 percent promotion that ends on 2026-09-03. OpenAI's own
rate for the same model, already in `data/api_pricing.yaml`, is 4.00 and 20.00.
Never copy a Copilot rate into another provider's row.

## Workflow

1. Read `https://github.com/features/copilot/plans`. Take the price and the
   credit total for each tier.
2. Read `https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals`.
   Take the credit allowance table.
3. Cross-check the two: 15 USD must equal 1,500 credits, 70 must equal 7,000,
   and 200 must equal 20,000. Report a disagreement rather than picking a side.
4. Read `https://docs.github.com/en/copilot/get-started/plans` for the model
   list per tier. Pro unlocks fewer models than Pro+ and Max.
5. Write one `month` entry per tier in `prices`. Add no other billing term.
6. Add no row to `data/api_pricing.yaml`, `data/rate_limits.yaml`, or
   `data/models.yaml`. See below.
7. Set `last_verified` to the date you read the pages.
8. Run `python3 build.py --check`.

## Which datasets hold zero GitHub rows

Three of the four datasets correctly hold no GitHub row today.

| Dataset | Rows | Why |
|---|---|---|
| `data/plans.yaml` | 3 | Copilot Pro, Pro+, and Max. |
| `data/api_pricing.yaml` | 0 | GitHub sells no public model API. The rates on `models-and-pricing` bill Copilot usage, and every model except Raptor mini belongs to another vendor. |
| `data/rate_limits.yaml` | 0 | GitHub publishes no numeric request or token limit for Copilot. |
| `data/models.yaml` | 0 | GitHub publishes one own model, Raptor mini, and no specification page for it. No parameter count and no context window exist. |

A zero-row dataset is a finding, not a gap to fill. Read
`references/data-recipes.md` before you change one of these counts.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the `.md` twin rule |
| `references/billing-model.md` | AI credits, the legacy premium-request system, the switch date |
| `references/pricing.md` | Tier prices, credit allowances, the per-token table |
| `references/data-recipes.md` | A worked row, and the case against each empty dataset |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
