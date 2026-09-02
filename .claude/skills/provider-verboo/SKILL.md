---
name: provider-verboo
description: How to source Verboo prices, quotas, and API rates for the datasets in this repository. Use when you add or refresh a Verboo row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, data/models.yaml, or data/changelog.yaml, or when the user mentions Verboo, Verboo Code, verboo.ai, code.verboo.ai, Boo, or the Verboo API. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Verboo — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Verboo, so you do not repeat work that already failed.

Everything here was checked on 2026-09-02. Re-check a status before you trust it.

**The plan prices are not in any HTML page.** `https://verboo.ai/en` renders its
plan cards client-side. A public JSON route at
`https://code.verboo.ai/api/marketplace` holds every plan price. The API rate
table and the model catalogue are server-rendered, so `curl -sL` reads them.
This skill ships no `scripts/` directory.

## Constants

Write the provider as `Verboo` in all five data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`price_currency` is `USD` in `data/plans.yaml`. `currency` is `USD` in
`data/api_pricing.yaml`. See trap 6 before you copy an amount.

Verboo Tecnologia is a Brazilian company. Its product is Verboo Code, an AI
coding agent that runs in the terminal on dedicated GPUs in Brazil. The selling
point is unlimited tokens for a fixed monthly price, with a per-minute request
cap instead of a token cap. The CLI installs with `npm i -g @verboo/code`. It is
an Apache 2.0 fork of OpenClaw, at `https://github.com/verbeux/verboo-code`.
Verboo hosts open-weight third-party models only. It trains no model of its own.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Junior / Pro / Max / Ultra prices | `https://code.verboo.ai/api/marketplace` | `curl` — see trap 1 |
| Annual price per tier | same endpoint, `annualPriceCents` | same |
| Which models a tier unlocks | same endpoint, `instances[].models[].modelName` | same |
| Requests per minute, concurrent requests | same endpoint, `apiRateLimitRpm` and `concurrentRequests` | same |
| Per-model API rates | `https://verboo.ai/en/api` | `curl -sL` |
| The 14-model catalogue, context, tok/s | `https://verboo.ai/en` | `curl -sL` |
| HTTP errors and rate-limit headers | `https://code.verboo.ai/en/docs/api/errors` | `curl -sL` |
| Brand colour | verboo.ai stylesheets, `--primary-h/s/l` | `curl -sL` |

## Nine things that produce a wrong number

**1. The plans page renders its prices client-side.** `https://verboo.ai/en`
returns HTTP 200 and about 100 KB, but the plan cards say only "Loading prices
for your region…". No price sits in that HTML. The page calls a public,
unauthenticated JSON route at runtime. Fetch that route directly:

```bash
curl -sL "https://code.verboo.ai/api/marketplace?sortBy=priceCents&order=asc&apiOnly=false&includeMetrics=false"
```

It returns `{"data": [...]}` with five records. Prices sit in `priceCents`, so
divide by 100. This endpoint is the only way to read a Verboo plan price. A
reader who trusts the rendered HTML finds nothing.

**2. Two model names are capitalised, twelve are not.** The API pricing page
prints display names. Two differ from the model id: `Qwen 3.6 27b` for
`qwen3.6-27b`, and `Kimi K3` for `kimi-k3`. `build.py` left-joins
`data/api_pricing.yaml` onto `data/models.yaml` on the exact `(provider, model)`
and `(provider, name)` pair. A capitalisation slip splits one model into two
rows. Use the API page display name in both files. Put the lowercase id in
`model_id`.

**3. One marketplace record is not a plan.** The record with slug
`deepseek-v4-flash-0731` carries `priceCents: 0` and
`billingMode: "prepaid_tokens"`. It is the usage-based API product, not a
subscription tier. Only the four records with `billingMode: "subscription"`
become `data/plans.yaml` rows: Junior, Pro, Max, and Ultra. Take the API rates
from `https://verboo.ai/en/api`, which prices five models. Do not take them from
this single record.

**4. Verboo publishes no per-model rate limit.**
`https://code.verboo.ai/en/docs/api/errors` documents the `X-RateLimit-Limit`,
`X-RateLimit-Remaining`, `X-RateLimit-Reset`, and `Retry-After` headers, and the
429 status. It states no RPM or TPM number. The marketplace endpoint publishes
`apiRateLimitRpm: 40` and `concurrentRequests: 2`, but per plan tier, not per
model. `data/rate_limits.yaml` keys on provider, model, and tier, so Verboo gets
zero rows in that file. Zero rows is the correct result here. Put the 40 RPM and
the 2 concurrent requests in the `limits` list of each `data/plans.yaml` record.

**5. The model catalogue needs an API key.** `GET /router/v1/models`,
`/api/models`, and `/api/public/models` all return HTTP 401. That response
carries `context_window` and a per-model `vision` boolean, which no public page
states. Until someone holds a key, write `vision: null` on every Verboo row in
`data/models.yaml`. The `instances[].models[].contextWindow` field in the
marketplace JSON does give the context window without a key: 1048576 for most
models, 262144 for the two Qwen models.

**6. The currency may follow the reader's location.** The landing page promises
"Fixed pricing in your regional currency, with Pix or card where available".
Read from outside Brazil on 2026-09-02, the marketplace endpoint returned
`"currency": "usd"` on every record. A Brazilian IP may return BRL. Check the
`currency` field on the record before you copy an amount. Record USD only when
the field says `usd`.

**7. A year costs ten months.** Each tier's `annualPriceCents` is exactly ten
times its monthly `priceCents`. Write the full term total in `data/plans.yaml`,
for example `240` for Junior's year. The build script derives the monthly
equivalent and the roughly 17% saving. Never write the saving into the data.

**8. Two models are marked temporary.** The landing page tags `glm-5.3` and
`kimi-k3` "Temporary". That is a capacity note, not a lifecycle state. Record it
in `notes`. Leave `status` alone.

**9. Enterprise has no price.** The landing page offers an Enterprise tier as
"Talk to sales", with a dedicated GPU cluster and mTLS. The schema requires
`prices.amount`, so Enterprise gets no record.

## Workflow

1. Read the marketplace endpoint for the four tier prices, the annual prices,
   the RPM, the concurrency, and the model set per tier.
2. Read `https://verboo.ai/en/api` for the per-model rates.
3. Read `https://verboo.ai/en` for the full 14-model catalogue.
4. Write one `data/plans.yaml` record per subscription tier. Skip Enterprise and
   skip the prepaid record.
5. Write `data/api_pricing.yaml` rows for the models the API page prices.
6. Write `data/models.yaml` rows for all 14 models, with `vision: null`.
7. Add no row to `data/rate_limits.yaml`.
8. Use only `verboo.ai` and `code.verboo.ai` URLs in `links`. Label the landing
   page `plans`, the API page `pricing`, and the docs `docs`.
9. Set `last_verified` to the date you read the pages.
10. Run `python build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, the tier values, the model rates, and the model catalogue |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
