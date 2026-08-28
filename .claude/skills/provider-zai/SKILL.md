---
name: provider-zai
description: How to source Z.ai (Zhipu / GLM) prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh a Zhipu row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Z.ai, z.ai, Zhipu, GLM, GLM Coding Plan, GLM-5.3, or ZCode. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Z.ai (Zhipu / GLM) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Z.ai, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Zhipu (GLM)` in all four data files. The build script
groups rows by that exact string, so any other spelling splits the provider into
two tables. `region` is `china`. Prices are USD.

Z.ai sells the subscription as the **GLM Coding Plan**, in three tiers: Lite,
Pro, and Max.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices, billing terms | `https://z.ai/subscribe` | Playwright |
| Tier quotas, models | `https://docs.z.ai/devpack/overview` | `WebFetch` |
| API rates per token | `https://docs.z.ai/guides/overview/pricing` | `WebFetch` |
| Model specification | `https://docs.z.ai/guides/llm/glm-5.3` | `WebFetch` |
| Every docs URL | `https://docs.z.ai/llms.txt` | `WebFetch` |

## Three things that produce a wrong number

**1. The subscribe page defeats `WebFetch` and `--dump-dom`.** Both return a
success code and no price. Only Playwright driving the system Chrome reads it.
Run `scripts/read-subscribe.js`. Details in `references/fetching.md`.

**2. Z.ai prints a rate per month, never the price of the term.** The yearly
toggle shows `$12.6/month`, not `$151.20/year`. The schema wants the term total,
so multiply by 3 or 12 and say so in `notes`. Table in `references/pricing.md`.

**3. Z.ai publishes no numeric API rate limit.** Every path to one either 404s
or redirects behind a login. `data/rate_limits.yaml` holds zero Zhipu rows and
that is correct. Do not add a row of nulls. Reasoning in `references/quotas.md`.

## Workflow

1. Read `https://docs.z.ai/devpack/overview`. Take the quota and the model list.
2. Run `scripts/read-subscribe.js`. Take the price under each billing term.
3. Multiply each printed monthly rate by its term to get `amount`.
4. Cross-check the quotas: the subscribe page states Pro as `6x Lite` and Max as
   `14x Lite`, which must match the absolute credit numbers.
5. Write the rows. Copy the shapes in `references/data-recipes.md`.
6. Add no row to `data/rate_limits.yaml`.
7. Set `last_verified` to the date you read the pages.
8. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the `.md` twin trick |
| `references/fetching.md` | The Playwright recipe, failure modes, selectors, troubleshooting |
| `references/pricing.md` | Plan prices, the term-total conversion, API token rates |
| `references/quotas.md` | Credit quotas, Team seats, why rate limits are absent |
| `references/data-recipes.md` | A worked row for each of the four datasets |
| `scripts/read-subscribe.js` | Prints every tier under every billing term |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
