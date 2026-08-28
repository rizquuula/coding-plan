# Zhipu rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to Zhipu.

Constants for every Zhipu row in every file:

- `provider: Zhipu (GLM)` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `region: china` in `data/plans.yaml`.
- `price_currency` and `currency` are `USD`. Z.ai prints USD on its
  international pages.

## `data/plans.yaml`

Five rows. Three Individual tiers: `zhipu-glm-coding-lite`,
`zhipu-glm-coding-pro`, `zhipu-glm-coding-max`. Two Team seats:
`zhipu-glm-coding-team-standard-seat`, `zhipu-glm-coding-team-premium-seat`.

### An Individual tier

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

### A Team seat

```yaml
- id: zhipu-glm-coding-team-standard-seat
  provider: Zhipu (GLM)
  plan: Standard Seat
  region: china
  price_currency: USD
  prices:
    - period: month
      amount: 88
    - period: year
      amount: 1056
  limits:
    - 15000 credits per 5 hours
    - 66000 credits per week
  models:
    - GLM-5.3
    - GLM-5.3-Flash
  status: active
  notes: Team plan seat; every price is per seat. Z.ai sells a monthly and a
    yearly term only. A yearly renewal costs 10 percent less than the first year.
  links:
    - label: plans
      url: https://docs.z.ai/devpack/teamplan
    - label: pricing
      url: https://z.ai/subscribe
  last_verified: 2026-08-28
```

Four things differ from an Individual row:

- **No `quarter` term.** Both quarterly products are `purchasable: false`. See
  `pricing.md`.
- `plan` holds the display name, `Standard Seat` or `Premium Seat`, not the
  `PRO` or `MAX` string the API returns.
- The price and the quota come from two different sources, so `links` carries
  both a `pricing` and a `plans` entry.
- `notes` states the per-seat basis and the 10 percent renewal discount.

The Premium Seat row lists two extra `limits` items, for early model access and
peak-hour priority. The Standard Seat row does not.

## `data/api_pricing.yaml`

Twenty-two rows, one per model on the pricing page. `zhipu-glm-5-3` is the
shape.

```yaml
- id: zhipu-glm-5-3
  provider: Zhipu (GLM)
  model: GLM-5.3
  model_id: glm-5.3
  context_window: 1M
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
- `context_window` comes from the model matrix, not from the pricing page. See
  `models.md`.
- `model_id` comes from `chat-completion.md`. GLM-OCR is absent from both enums
  there, so its row carries `model_id: null` and `context_window: null`.
- A free model carries `input: 0` and `output: 0`, never `null`.
- The GLM-5.3-Flash row is on a promotion that expires on 2026-09-09. Check it
  first on any refresh. See `pricing.md`.

## `data/models.yaml`

Twenty-one rows, one per model in the matrix. GLM-OCR has an API pricing row and
no model row, because the matrix publishes no context window for it.

Most rows look like this. Note `open_weights: null`, which is the common case.

```yaml
- id: zhipu-glm-4-7
  name: GLM-4.7
  provider: Zhipu (GLM)
  total_params: null
  active_params: null
  context_window: 200K
  max_output: 128K
  vision: false
  open_weights: null
  notes: Z.ai only ranks it first among open-source models on benchmarks.
  links:
    - label: model card
      url: https://docs.z.ai/guides/llm/glm-4.7
    - label: docs
      url: https://docs.z.ai/guides/overview/overview
  last_verified: 2026-08-28
```

Read `models.md` before you fill one of these. It records where each field
lives and the five traps that produce a wrong value. The short version:

- `open_weights` is `null` on 18 of the 21 rows. Only GLM-5.3-Flash, GLM-5.2,
  and GLM-4.5 carry `true`. No row carries `false`.
- `total_params` and `active_params` are `null` on 16 of the 21 rows. Four pages
  publish a count, covering five models.
- `context_window` comes from the matrix. `max_output` comes from
  `chat-completion.md`. They do not group the same way.
- `notes` says why a field is `null`, so the next agent does not re-search.

## `data/rate_limits.yaml`

**No Zhipu row, on purpose.** Do not add a row of nulls.

Z.ai enforces a per-model concurrency limit, which is specific to an account and
never public. This dataset has no concurrency column. `quotas.md` records how
that was settled. Do not re-open it.

## Link labels

Only these five fit a Zhipu row. The label describes what the page is.

| Label | URL |
|---|---|
| `pricing` | `https://z.ai/subscribe` for plans, `https://docs.z.ai/guides/overview/pricing` for API |
| `plans` | `https://docs.z.ai/devpack/overview`, or `https://docs.z.ai/devpack/teamplan` for a Team seat |
| `rate limit` | `https://docs.z.ai/devpack/usage-policy` |
| `model card` | The model's own guide page under `/guides/llm/` or `/guides/vlm/` |
| `docs` | `https://docs.z.ai/guides/overview/overview`, the model matrix |

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
