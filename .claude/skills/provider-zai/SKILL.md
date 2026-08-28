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
| Plan prices, billing terms | `https://z.ai/subscribe` | `scripts/read_subscribe.py` |
| Tier quotas, models | `https://docs.z.ai/devpack/overview` | `WebFetch` |
| API rates per token | `https://docs.z.ai/guides/overview/pricing` | `WebFetch` |
| Model specification | `https://docs.z.ai/guides/llm/glm-5.3` | `WebFetch` |
| Every docs URL | `https://docs.z.ai/llms.txt` | `WebFetch` |

## Four things that produce a wrong number

**1. The subscribe page defeats `WebFetch` and `--dump-dom`.** Both return a
success code and no price. The prices are compiled into the page's JavaScript
bundle, so fetch the bundle instead. Run `python3 scripts/read_subscribe.py`. It
needs no install and no browser. Details in `references/fetching.md`.

**2. The bundle ships three generations of the plan at once.** V1, V2, and V3 sit
side by side. V1 and V2 are dead legacy pricing. Take only the highest `version`
string. A naive read returns nine wrong prices next to the nine right ones.

**3. `money` in the bundle is the term total. Do not multiply it.** The rendered
page prints a rate per month, such as `$12.6/month` under the yearly toggle. The
bundle does not: it holds `151.2` for the whole year. You read the bundle, so
copy `money` straight into `amount`. Table in `references/pricing.md`.

**4. Z.ai publishes no numeric API rate limit.** Every path to one either 404s
or redirects behind a login. `data/rate_limits.yaml` holds zero Zhipu rows and
that is correct. Do not add a row of nulls. Reasoning in `references/quotas.md`.

## Workflow

1. Read `https://docs.z.ai/devpack/overview`. Take the quota and the model list.
2. Run `python3 scripts/read_subscribe.py`. Take the block for the highest
   version only.
3. Copy each `money` value into `amount`. It is the term total. Do not multiply.
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
| `references/fetching.md` | The bundle recipe, the regex, failure modes, troubleshooting |
| `references/pricing.md` | Plan prices, the term totals, API token rates |
| `references/quotas.md` | Credit quotas, Team seats, why rate limits are absent |
| `references/data-recipes.md` | A worked row for each of the four datasets |
| `scripts/read_subscribe.py` | Prints every tier under every billing term |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
