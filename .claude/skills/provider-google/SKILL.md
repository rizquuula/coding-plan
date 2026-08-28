---
name: provider-google
description: How to source Google (Gemini) prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh a Google row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Google, Gemini, Gemini API, Gemini Code Assist, Google Antigravity, Jules, AI Plus, AI Pro, or AI Ultra. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Google (Gemini) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Google, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Google` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables. `region` is `global`. `price_currency` and `currency` are `USD`.

Google splits the data across two brands. Keep them apart:

- The **Gemini API** sells tokens. Its pages live on `ai.google.dev`.
- The **Google AI subscription** sells consumer plans: Google AI Plus, Google AI
  Pro, and Google AI Ultra. Its pages live on `gemini.google`.

Google AI Ultra is one plan name with two price points. Google prints them as
`5x higher usage limits vs. AI Pro` and `20x higher usage limits vs. AI Pro`.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices in USD | `https://gemini.google/us/subscriptions/` | `WebFetch` |
| Plan usage multipliers, per-plan context window | `https://support.google.com/gemini/answer/16275805?hl=en` | `WebFetch` |
| API rates per 1M tokens | `https://ai.google.dev/gemini-api/docs/pricing` | `WebFetch` |
| Model list and every model id | `https://ai.google.dev/gemini-api/docs/models` | `WebFetch` |
| Context window, maximum output | `https://ai.google.dev/gemini-api/docs/models/<model-id>` | `WebFetch` |
| Usage tiers, batch enqueued tokens | `https://ai.google.dev/gemini-api/docs/rate-limits` | `WebFetch` |
| Jules task limits per plan | `https://jules.google/docs/usage-limits` | `WebFetch` |
| Gemini Code Assist request quota | `https://docs.cloud.google.com/gemini/docs/quotas` | `WebFetch` |

`WebFetch` reads every page in this table. Google needs no bundle trick and no
script. Use `curl` only when you must confirm exact markup.

## Six things that produce a wrong number

**1. `gemini.google/subscriptions/` prints the price in your local currency.**
From this machine it returns Indonesian rupiah, such as `Rp 1.579.000 IDR /
bulan`. Fetch `https://gemini.google/us/subscriptions/` instead. That path
returns USD. Details in `references/fetching.md`.

**2. `one.google.com/about/google-ai-plans/` never prints a price to a fetch
tool.** The price sits in an empty `<g1-localized-price>` element that the
browser fills. `?hl=en` and `?gl=US` do not change it. Never cite this page for a
price.

**3. The blog post rounds the price. The subscriptions page does not.** The blog
says `$100/month` and `$200`. `gemini.google/us/subscriptions/` says `$99.99` and
`$199.99`. Copy the subscriptions page. Table in `references/pricing.md`.

**4. The API pricing page prints three tables per model.** They run in order:
Standard, Batch, then Flex. Batch and Flex cost half. Take Standard. A naive read
writes the Batch rate into `input`.

**5. Two Flash models carry a dated rate that doubles in 2027.** Gemini 3.7 Flash
and Gemini 3.6 Flash both print `$0.75 through December 31, 2026. $1.50 starting
January 1, 2027.` Copy the current rate. Record the future rate in `notes`.

**6. Google publishes no per-model RPM, TPM, or RPD.** The rate-limits page names
four usage tiers and then sends you to AI Studio, which needs a login.
`data/rate_limits.yaml` holds zero Google rows and that is correct. Do not add a
row of nulls. Reasoning in `references/quotas.md`.

## Workflow

1. For a plan row, read `https://gemini.google/us/subscriptions/`. Take the USD
   price from the plan card.
2. Read `https://support.google.com/gemini/answer/16275805?hl=en`. Take the usage
   multiplier and the per-plan context window.
3. For an absolute plan quota, read `https://jules.google/docs/usage-limits`. It
   prints tasks per day per plan.
4. For an API rate, read `https://ai.google.dev/gemini-api/docs/pricing`. Take
   the Standard table only.
5. For a context window, read `https://ai.google.dev/gemini-api/docs/models/<model-id>`.
   The pricing page prints none.
6. Write the rows. Copy the shapes in `references/data-recipes.md`.
7. Add no row to `data/rate_limits.yaml`.
8. Set `last_verified` to the date you read the pages.
9. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the missing `.md` twin |
| `references/fetching.md` | The `/us/` locale recipe, the localized-price trap, curl notes |
| `references/pricing.md` | Plan prices, API token rates, the dated rates |
| `references/quotas.md` | Plan multipliers, Jules and Code Assist quotas, why rate limits are absent |
| `references/data-recipes.md` | A worked row for each of the four datasets |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
