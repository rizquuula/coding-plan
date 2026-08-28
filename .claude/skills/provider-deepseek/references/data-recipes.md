# DeepSeek rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to
DeepSeek.

Constants for every DeepSeek row in every file:

- `provider: DeepSeek` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `currency: USD` in `data/api_pricing.yaml`. Read the page without a language
  prefix. The `zh-cn` twin prints CNY.

## `data/api_pricing.yaml`

Two rows today: `deepseek-v4-pro` and `deepseek-v4-flash`.

```yaml
- id: deepseek-v4-pro
  provider: DeepSeek
  model: DeepSeek-V4-Pro
  model_id: deepseek-v4-pro
  context_window: 1M
  currency: USD
  input: 1.32
  cached_input: 0.044
  cache_write: null
  output: 3.96
  notes: These are peak rates. Off-peak rates are half. Peak hours run 01:00-04:00
    and 06:00-10:00 UTC, Monday to Friday.
  links:
    - label: pricing
      url: https://api-docs.deepseek.com/quick_start/pricing
    - label: rate limit
      url: https://api-docs.deepseek.com/quick_start/rate_limit
  last_verified: 2026-08-28
```

Notes on this dataset:

- `model` is the display name with capitals, such as `DeepSeek-V4-Pro`.
  `model_id` is the API string in lower case, such as `deepseek-v4-pro`.
- `cache_write` is always `null`. DeepSeek publishes a cache-hit rate and no
  cache-write rate.
- `context_window` is `1M` for every model. The pricing page prints it.
- The V4-Flash row carries a shorter `notes`, without the hours, because the
  hours already sit on the V4-Pro row.
- `deepseek-v4-flash-vision-exp` has no row yet. It is an experimental vision
  model, not a coding model. Add it only when it belongs in a coding-plan
  tracker.

## `data/rate_limits.yaml`

Two rows today: `deepseek-v4-flash-default` and `deepseek-v4-pro-default`.

```yaml
- id: deepseek-v4-pro-default
  provider: DeepSeek
  model: DeepSeek-V4-Pro
  tier: Default
  requests_per_minute: null
  input_tokens_per_minute: null
  output_tokens_per_minute: null
  tokens_per_minute: null
  requests_per_day: null
  notes: DeepSeek publishes a concurrency limit of 500 for this model, not a
    per-minute rate limit.
  links:
    - label: rate limit
      url: https://api-docs.deepseek.com/quick_start/rate_limit
  last_verified: 2026-08-28
```

Every numeric field stays `null`. The concurrency number goes in `notes`. See
`rate-limits.md` for why. `tier` is `Default`, because DeepSeek publishes one
set of limits for every account.

`model` must match the spelling in `data/api_pricing.yaml`.

## `data/models.yaml`

**No DeepSeek row exists yet.** Two rows were drafted and validated on
2026-08-28, and the maintainer had not applied them at that date. The row below
passes `python3 build.py --check`. The V4-Flash row takes `total_params: 284B`
and `active_params: 13B`, and is otherwise identical.

To add one, read
`https://www.deepseek.com/en/news/v4-preview/` and use `model card` as the link
label. That page states the parameter counts. The Chinese twin does not.

```yaml
- id: deepseek-v4-pro
  name: DeepSeek-V4-Pro
  provider: DeepSeek
  total_params: 1.6T
  active_params: 49B
  context_window: 1M
  max_output: 384K
  vision: false
  open_weights: true
  notes: DeepSeek publishes the V4 weights.
  links:
    - label: model card
      url: https://www.deepseek.com/en/news/v4-preview/
    - label: pricing
      url: https://api-docs.deepseek.com/quick_start/pricing
  last_verified: 2026-08-28
```

`id` is unique per file, so `deepseek-v4-pro` is free here even though
`data/api_pricing.yaml` already uses it.

`context_window` and `max_output` come from the pricing page, not from the
launch page. `total_params` and `active_params` come from the launch page. That
is why the row carries two links.

Set `vision: false` for V4-Pro and V4-Flash. Only
`deepseek-v4-flash-vision-exp` reads images.

## `data/plans.yaml`

**No DeepSeek row, on purpose.** DeepSeek sells no subscription. The API bills
per token from a topped-up balance. Add no row.

Do not treat DeepSeek Harness as a plan. It is a free agent framework at
`https://www.deepseek.com/harness/` and that page states no price.

## Link labels

Only these three fit a DeepSeek row.

| Label | URL |
|---|---|
| `pricing` | `https://api-docs.deepseek.com/quick_start/pricing` |
| `rate limit` | `https://api-docs.deepseek.com/quick_start/rate_limit` |
| `model card` | `https://www.deepseek.com/en/news/v4-preview/`, once a model row exists |

Use `announcement` for a page under `https://api-docs.deepseek.com/news/` when
that page is the only source for a value.

Never link `https://platform.deepseek.com/`. It returns 403 to every
unauthenticated read.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
