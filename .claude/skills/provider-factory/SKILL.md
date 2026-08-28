---
name: provider-factory
description: How to source Factory prices, quotas, and model multipliers for the datasets in this repository. Use when you add or refresh a Factory row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Factory, Factory AI, factory.ai, Droid, Droid CLI, Droid Core, Factory Pro, Factory Plus, or Factory Max. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Factory — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Factory, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Factory` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables. `region` is `global`. `price_currency` is `USD`.

Factory sells five tiers: three Individual tiers, Pro, Plus, and Max, and two
Organization tiers, Business and Enterprise. `data/plans.yaml` holds Pro, Plus,
and Max today. Business and Enterprise carry no published price, so they get no
row. See trap 7.

Factory resells other providers' models through the Droid platform. It publishes
a per-model token multiplier, not a per-token USD rate, so three of the four
datasets hold zero Factory rows. See "Datasets with zero rows".

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Individual plan prices and tier features | `https://docs.factory.ai/pricing/individuals.md` | `curl` |
| Usage-window wording, Extra Usage, Droid Core | `https://docs.factory.ai/pricing/individuals.md` | `curl` |
| Business and Enterprise terms | `https://docs.factory.ai/pricing/organizations.md` | `curl` |
| Full model catalog and multipliers | `https://docs.factory.ai/models.md` | `curl` |
| Every documentation URL | `https://docs.factory.ai/llms.txt` | `curl` |
| Marketing twin of the pricing page | `https://factory.ai/pricing` | `curl` |

## Traps that produce a wrong number

**1. docs.factory.ai is Mintlify, and every docs page serves a `.md` twin.**
`https://docs.factory.ai/llms.txt` lists every page and its markdown URL.
`https://docs.factory.ai/pricing.md` 308-redirects to
`https://docs.factory.ai/pricing/individuals.md`. Pass `-L` to `curl` so it
follows the redirect.

**2. `WebFetch` drops rows from the model catalog.** A `WebFetch` call on
`https://docs.factory.ai/models` compressed the OpenAI table down to "12 models
total" and did not return the rows. Read `https://docs.factory.ai/models.md`
with `curl` for the full catalog.

**3. A multiplier is not a per-token rate.** Factory publishes no absolute
USD-per-token price for any model. `data/api_pricing.yaml` holds zero Factory
rows because there is no rate to record.

**4. A promotional multiplier reverts on a stated date.** `GPT-5.6 Sol` bills
1.6× through 2026-11-22, then 2×. `GPT-5.6 Sol Fast` bills 3.2× through
2026-11-22, then 4×. `Gemini 3.7 Flash` bills 0.3× through 2027-01-01, then
0.6×. A multiplier copied during the promotion window misstates the steady
rate. Check the footnote under every table before you cite a number.

**5. Three Droid Core models are deprecated but still listed.** `MiniMax M2.7`,
`Kimi K2.5`, and `GLM-5.1` carry a `‡` footnote: "remain available for now and
will be removed in a future release." Treat them as current until the page
removes them.

**6. Factory names its rate-limit windows but publishes no number for any of
them.** The individuals page states three rolling windows, 5-hour, 7-day, and
30-day, and gives no request count, token count, or credit count for any
window. `data/rate_limits.yaml` holds zero Factory rows because there is no
number to record.

**7. Business and Enterprise have no published price.** Both cards read
"Custom pricing" and link to a contact-sales form. The `prices` schema in
`AGENTS.md` requires a numeric `amount`, so neither tier gets a row in
`data/plans.yaml`.

**8. The models in Factory's catalog belong to other providers.** Claude,
GPT, Gemini, and Grok models keep their specifications on their own provider's
pages, not on Factory's. `data/models.yaml` holds zero Factory rows because
Factory is a reseller, not the source of those specifications.

## Datasets with zero rows

Three datasets hold no Factory row, and each zero is correct.

- `data/api_pricing.yaml` — Factory bills by multiplier against Factory
  Standard Credits, not by a per-token USD rate. See trap 3.
- `data/rate_limits.yaml` — Factory names three rolling windows and publishes
  no number for any of them. See trap 6.
- `data/models.yaml` — every model in the catalog is another provider's model.
  Its specifications belong in that provider's own row. See trap 8.

Do not add a row of nulls to record any of these absences.

## Workflow

1. Read `https://docs.factory.ai/pricing/individuals.md`. Take the monthly
   price and the feature lines for Pro, Plus, and Max.
2. Read `https://docs.factory.ai/pricing/organizations.md`. Confirm Business
   and Enterprise still carry no numeric price.
3. Read `https://docs.factory.ai/models.md`. Cross-check any multiplier you
   cite against its promotional or deprecation footnote.
4. Write or refresh the three plan rows in `data/plans.yaml`. Add no row to
   `data/api_pricing.yaml`, `data/rate_limits.yaml`, or `data/models.yaml`.
5. Set `last_verified` to the date you read the pages.
6. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its `.md`-twin behavior, and the WebFetch dead end |
| `references/models.md` | The full model catalog and multipliers, sourcing context only |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
