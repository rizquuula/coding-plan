# Google rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to Google.

Constants for every Google row in every file:

- `provider: Google` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `region: global` in `data/plans.yaml`.
- `price_currency` and `currency` are `USD`. Read the USD price from
  `https://gemini.google/us/subscriptions/`. See `fetching.md`.

## `data/plans.yaml`

Two rows today: `google-ai-ultra-5x` and `google-ai-ultra-20x`.

```yaml
- id: google-ai-ultra-5x
  provider: Google
  plan: Google AI Ultra 5x
  region: global
  price_currency: USD
  prices:
    - period: month
      amount: 99.99
  limits:
    - 5x the AI Pro usage limits
    - 1M token context window
  models:
    - Gemini
  status: active
  notes: Usage limits weigh prompt complexity rather than counting requests.
  links:
    - label: pricing
      url: https://gemini.google/us/subscriptions/
    - label: rate limit
      url: https://support.google.com/gemini/answer/16275805?hl=en
  last_verified: 2026-08-28
```

Notes on this dataset:

- `prices` holds one entry. Google sells no quarterly and no yearly term.
- `plan` uses `Google AI Ultra 5x` and `Google AI Ultra 20x`. Google itself calls
  both cards `Google AI Ultra` and separates them by price. The blog calls them
  `AI Ultra $100` and `AI Ultra $200`. This repository names them by the
  multiplier so the two rows read apart.
- `limits` items stay relative, because the source page publishes no absolute
  count. See `quotas.md`.
- Google AI Plus at $4.99 and Google AI Pro at $19.99 have no row yet. Add them
  from the same page when the scope calls for it.

## Known mismatch, 2026-08-28

Both rows carry `amount: 100` and `amount: 200`. Those figures come from the blog
post, which rounds. `https://gemini.google/us/subscriptions/` states $99.99 and
$199.99. Correct the two rows on your next refresh, and switch the `pricing` link
from the blog to the subscriptions page.

## `data/api_pricing.yaml`

Two rows today: `google-gemini-3-7-flash` and `google-gemini-3-5-flash`.

```yaml
- id: google-gemini-3-7-flash
  provider: Google
  model: Gemini 3.7 Flash
  model_id: gemini-3.7-flash
  context_window: 1M
  currency: USD
  input: 0.75
  cached_input: 0.075
  cache_write: null
  output: 3.75
  notes: Promotional rate through 2026-12-31, after which input costs 1.50 and
    output costs 7.50. Cache storage costs 0.50 per 1M tokens per hour.
  links:
    - label: pricing
      url: https://ai.google.dev/gemini-api/docs/pricing
    - label: rate limit
      url: https://ai.google.dev/gemini-api/docs/rate-limits
  last_verified: 2026-08-28
```

Both rows matched the pricing page on 2026-08-28. Notes on this dataset:

- `cache_write` is always `null`. Google publishes a cache-read rate and an
  hourly storage rate, and no cache-write rate.
- Put the hourly storage rate in `notes`. No field holds it.
- `context_window` does not come from the pricing page. Read
  `https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash`, which prints
  an input token limit of 1,048,576. Write `1M`.
- Take every rate from the **Standard** table. Batch and Flex cost half.
- Re-check the Gemini 3.7 Flash and Gemini 3.6 Flash rows in January 2027. Their
  promotional rate expires on 2026-12-31.

## `data/models.yaml`

**No Google row exists yet.** To add one, read
`https://ai.google.dev/gemini-api/docs/models/<model-id>` and use `model card` as
the link label.

| Field | Value to write | Source |
|---|---|---|
| `context_window` | `1M` | Input token limit, 1,048,576 |
| `max_output` | `64K` | Output token limit, 65,536 |
| `vision` | `true` | Supported inputs list Image and Video |
| `open_weights` | `false` | Gemini models are closed. Gemma is not. |
| `total_params` | `null` | No Google page publishes one |
| `active_params` | `null` | No Google page publishes one |

Set `open_weights` from what the page states, not from reputation. Gemma 4
appears on the pricing page as free, and it is a different family from Gemini.

## `data/rate_limits.yaml`

**No Google row, on purpose.** See `quotas.md`. Do not add a row of nulls, and
never write a batch enqueued token count into `tokens_per_minute`.

## Link labels

Only these four fit a Google row. The label describes what the page is.

| Label | URL |
|---|---|
| `pricing` | `https://gemini.google/us/subscriptions/` for plans, `https://ai.google.dev/gemini-api/docs/pricing` for API |
| `rate limit` | `https://support.google.com/gemini/answer/16275805?hl=en` for plans, `https://ai.google.dev/gemini-api/docs/rate-limits` for API |
| `model card` | `https://ai.google.dev/gemini-api/docs/models/<model-id>` |
| `announcement` | `https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/` |

Never link `https://aistudio.google.com/rate-limit`. It needs a login. Never link
`https://one.google.com/about/google-ai-plans/` as a price source. It shows no
price to a reader who uses a fetch tool.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
