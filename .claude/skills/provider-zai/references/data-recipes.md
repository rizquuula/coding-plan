# Zhipu rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to Zhipu.

Constants for every Zhipu row in every file:

- `provider: Zhipu (GLM)` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `region: china` in `data/plans.yaml`.
- `price_currency` and `currency` are `USD`. Z.ai prints USD on its
  international pages.

## `data/plans.yaml`

Three rows: `zhipu-glm-coding-lite`, `zhipu-glm-coding-pro`,
`zhipu-glm-coding-max`.

```yaml
- id: zhipu-glm-coding-pro
  provider: Zhipu (GLM)
  plan: GLM Coding Plan Pro
  region: china
  price_currency: USD
  prices:
    - period: month
      amount: 80
    - period: quarter
      amount: 192
    - period: year
      amount: 672
  limits:
    - 12000 credits per 5 hours
    - 60000 credits per week
  models:
    - GLM-5.3
    - GLM-5.3-Flash
  status: active
  notes: Z.ai prints a rate per month; the quarter and year totals are that rate
    times the term.
  links:
    - label: pricing
      url: https://z.ai/subscribe
    - label: plans
      url: https://docs.z.ai/devpack/overview
    - label: rate limit
      url: https://docs.z.ai/devpack/usage-policy
  last_verified: 2026-08-28
```

`amount` is the term total. Copy `money` from the bundle without arithmetic. See
`pricing.md`.

The Lite row carries one extra sentence in `notes` about off-peak half rate. Do
not copy it to the other tiers.

## `data/api_pricing.yaml`

Two rows today: `zhipu-glm-5-3` and `zhipu-glm-5-3-flash`.

```yaml
- id: zhipu-glm-5-3
  provider: Zhipu (GLM)
  model: GLM-5.3
  model_id: glm-5.3
  context_window: null
  currency: USD
  input: 1.40
  cached_input: 0.26
  cache_write: null
  output: 4.40
  notes: null
  links:
    - label: pricing
      url: https://docs.z.ai/guides/overview/pricing
    - label: rate limit
      url: https://docs.z.ai/devpack/usage-policy
  last_verified: 2026-08-28
```

Notes on this dataset:

- `cache_write` is always `null`. Z.ai publishes a cached-read rate and no
  cache-write rate.
- `context_window` is `null` because the pricing page does not print one. Fill
  it only from `https://docs.z.ai/guides/llm/glm-5.3`.
- The pricing page lists many more models. Add one only when it belongs in a
  coding-plan tracker.

## `data/models.yaml`

**No Zhipu row exists yet.** To add one, read
`https://docs.z.ai/guides/llm/glm-5.3` and use `model card` as the link label.

GLM models are open weights, unlike every model in that file today. Check the
model page and set `open_weights` from what it states, not from reputation. Set
`total_params` and `active_params` only when the page prints them.

## `data/rate_limits.yaml`

**No Zhipu row, on purpose.** See `quotas.md`. Do not add a row of nulls.

## Link labels

Only these three fit a Zhipu row. The label describes what the page is.

| Label | URL |
|---|---|
| `pricing` | `https://z.ai/subscribe` for plans, `https://docs.z.ai/guides/overview/pricing` for API |
| `plans` | `https://docs.z.ai/devpack/overview` |
| `rate limit` | `https://docs.z.ai/devpack/usage-policy` |
| `model card` | `https://docs.z.ai/guides/llm/glm-5.3`, once a model row exists |

Never link `https://z.ai/manage-apikey/rate-limits`. It needs a login.

## Known inconsistency

`docs.z.ai/devpack/overview` calls the small model `GLM-5.3-Flash`. Older
wording on the same site said `GLM-5-Flash`, and `data/plans.yaml` carried that
until 2026-08-28. Use `GLM-5.3-Flash` everywhere. When you see `GLM-5-Flash` in
this repository again, it is a regression.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
