---
name: provider-meta
description: How to source Meta Muse Code prices, quotas, and API rates for the datasets in this repository. Use when you add or refresh a Meta row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, data/models.yaml, or data/changelog.yaml, or when the user mentions Meta, Muse Code, Muse Spark, muse-spark, or dev.meta.ai. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Meta — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Meta, so you do not repeat work that already failed.

Everything here was checked on 2026-09-03. Re-check a status before you trust it.

The sandbox that added these rows could not fetch any Meta page: `WebFetch`
returned HTTP 403 for all three URLs, and `curl` failed at the proxy. The rows
transcribe values the maintainer quoted verbatim from Meta's own pages. Re-read
the pages yourself before you trust a number here.

## Constants

Write the provider as `Meta` in all five data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`price_currency` is `USD` in `data/plans.yaml`. `currency` is `USD` in
`data/api_pricing.yaml`. The API base URL is `https://api.meta.ai/v1`.

Meta sells Muse Code subscriptions in three tiers: Everyday Usage, High Usage,
and Power Usage. It prices the Muse Spark API per 1M tokens.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Everyday / High / Power prices, limits | `https://developer.meta.com/ai/products/muse-code/` | `WebFetch` |
| Per-model API rates | `https://dev.meta.ai/docs/pricing-rate-limits.md` | `WebFetch` |
| Rate limits, if Meta states per-minute caps | same pricing-rate-limits page | same |
| Model catalogue, context window | `https://dev.meta.ai/docs/models.md` | `WebFetch` |

## Seven things that produce a wrong number

**1. All three Meta pages block automated fetches.** `WebFetch` gets HTTP 403
on the product page and both docs pages, and proxied `curl` fails too. Try the
`.md` twin, then `curl` on the page HTML, then the JS bundle or a public JSON
endpoint the page calls, per `AGENTS.md`. Do not fall back to a third-party
source.

**2. No annual price is published.** The product page states monthly prices
only: Everyday Usage 5, High Usage 15, Power Usage 50. Do not invent a yearly
term.

**3. The 1.2 models share the 1.3 rates.** Meta lists `muse-spark-1.2` at the
same input / cached input / output rates as `muse-spark-1.3`, and
`muse-spark-1.2-contributor` at the same rates as `muse-spark-1.3-contributor`.
That is two rows per rate pair, not one.

**4. No cache-write price is published.** Write `cache_write: null`, not zero.
A zero would claim free cache writes.

**5. Max output is not stated.** Write `max_output: null`. The docs give the
context window (1,048,576 tokens, short form `1M`) and nothing else.

**6. The contributor variants are separate cheap models.** Do not average them
into the full models. `muse-spark-1.3-contributor` is 0.10 input, 0.002 cached
input, 0.20 output per 1M tokens.

**7. `vision` and `open_weights` stay null.** The Everyday plan mentions image
and video uploads, but that describes the plan, not a statement that the model
reads images. Silence means `null`, never `false`.
