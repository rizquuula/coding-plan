# OpenAI rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to OpenAI.

Constants for every OpenAI row in every file:

- `provider: OpenAI` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `region: global` in `data/plans.yaml`.
- `price_currency` and `currency` are `USD`.

Write the model display name as OpenAI writes it: `GPT-5.6 Sol`, `GPT-5.6
Terra`, `GPT-5.6 Luna`. Write the API string in `model_id` in lower case:
`gpt-5.6-sol`. `data/rate_limits.yaml` must match the display name in
`data/api_pricing.yaml`.

## `data/plans.yaml`

Four rows today: `openai-chatgpt-go`, `openai-chatgpt-plus`,
`openai-chatgpt-pro-5x`, `openai-chatgpt-pro-20x`.

```yaml
- id: openai-chatgpt-pro-5x
  provider: OpenAI
  plan: ChatGPT Pro 5x
  region: global
  price_currency: USD
  prices:
    - period: month
      amount: 100
  limits:
    - Sol 50 to 500 messages per 5 hours
    - Terra 125 to 1000 messages per 5 hours
    - Luna 1250 to 10000 messages per 5 hours
  models:
    - GPT-5.6 Sol
    - GPT-5.6 Terra
    - GPT-5.6 Luna
  status: active
  notes: null
  links:
    - label: pricing
      url: https://learn.chatgpt.com/docs/pricing
  last_verified: 2026-08-28
```

Notes on this dataset:

- One `month` entry per individual record. `learn.chatgpt.com/docs/pricing`
  publishes no yearly price for Go, Plus, or Pro. Do not derive one.
- Business is the exception. Its card prints 20 per seat billed annually and 25
  per seat billed monthly, so the record carries `month: 25` and `year: 240`.
  See `pricing.md` for the footnote and the multiplication rule.
- Pro is two records, not one. The page names the tiers `Pro 5x` and `Pro 20x`
  and prices them at 100 and 200. See `pricing.md`.
- Write the message limits as plain integers with no comma. The page prints
  `1,250-10,000`. Write `1250 to 10000`.
- The Go row carries no number, because the page publishes none for Go.

## `data/api_pricing.yaml`

Three rows today: `openai-gpt-5-6-sol`, `openai-gpt-5-6-terra`,
`openai-gpt-5-6-luna`.

```yaml
- id: openai-gpt-5-6-sol
  provider: OpenAI
  model: GPT-5.6 Sol
  model_id: gpt-5.6-sol
  context_window: 1.05M
  currency: USD
  input: 4.00
  cached_input: 0.40
  cache_write: 5.00
  output: 20.00
  notes: Promotional pricing runs at least through 2026-11-21.
  links:
    - label: pricing
      url: https://developers.openai.com/api/docs/pricing
    - label: model card
      url: https://developers.openai.com/api/docs/models/gpt-5.6-sol
  last_verified: 2026-08-28
```

Notes on this dataset:

- Take the Standard table, short context columns. See `pricing.md`.
- `cache_write` is a real number for a GPT-5.6 model. The pricing page prints
  it, and each model page states the 1.25x rule that produces it.
- `context_window` comes from the model page, not the pricing page. All three
  GPT-5.6 models state a 1,050,000 context window. Write `1.05M`. `1M`
  understates the window by 50,000 tokens.
- Use `model card` as the label for a model page. Use `pricing` for the pricing
  page. Use `rate limit` only for a page that states a quota.

## `data/rate_limits.yaml`

Fifteen rows today: three models times five usage tiers.

```yaml
- id: openai-gpt-5-6-sol-tier-1
  provider: OpenAI
  model: GPT-5.6 Sol
  tier: Tier 1
  requests_per_minute: 500
  input_tokens_per_minute: null
  output_tokens_per_minute: null
  tokens_per_minute: 500000
  requests_per_day: null
  notes: null
  links:
    - label: rate limit
      url: https://developers.openai.com/api/docs/models/gpt-5.6-sol
  last_verified: 2026-08-28
```

Notes on this dataset:

- The model page holds the numbers. The rate-limit guide does not. See
  `quotas.md`.
- TPM is a combined limit, so set `tokens_per_minute` and leave the input and
  output split as `null`.
- OpenAI publishes no RPD for these models. Leave `requests_per_day` as `null`.
- Drop the batch queue limit. This repository has no field for it.
- One record per model and usage tier. Five tiers make five records. Do not
  average two tiers into one row.

## `data/models.yaml`

**No OpenAI row exists yet.** To add one, read the model page and use
`model card` as the link label.

Values a GPT-5.6 model page publishes, read 2026-08-28. All three models state
the same specification:

| Field | Value | Source line on the page |
|---|---|---|
| `context_window` | `1.05M` | `1,050,000 context window` |
| `max_output` | `128K` | `128,000 max output tokens` |
| `vision` | `true` | `Input modalities: text, image` |
| `open_weights` | `null` | No download link, no licence statement |
| `total_params` | `null` | The page prints no parameter count |
| `active_params` | `null` | The page prints no parameter count |

Set `open_weights` from what the page states, not from reputation. `AGENTS.md`
makes the field nullable, and `null` means unstated. A GPT-5.6 page says nothing
about its weights, so it gets `null`. Writing `false` there is an unsourced
claim, which breaks rule 3.

`gpt-oss-120b` is the opposite case, and every value is on its page:

| Field | Value | Source line on the page |
|---|---|---|
| `total_params` | `117B` | `(117B parameters with 5.1B active parameters)` |
| `active_params` | `5.1B` | the same line |
| `context_window` | `131K` | `131,072 context window` |
| `max_output` | `131K` | `131,072 max output tokens` |
| `vision` | `false` | `Input modalities: text` |
| `open_weights` | `true` | `Download gpt-oss-120b on HuggingFace`, `Permissive Apache 2.0 license` |

`vision: false` is safe here only because the page lists the input modalities and
omits image. `gpt-oss-20b` has its own page with its own numbers.

Each model page also prints a knowledge cutoff, `Feb 16, 2026` for the GPT-5.6
family. This repository has no field for it. Do not force it into `notes`
unless it adds something a reader needs.

## Link labels

Only these four fit an OpenAI row. The label describes what the page is.

| Label | URL |
|---|---|
| `pricing` | `https://learn.chatgpt.com/docs/pricing` for plans, `https://developers.openai.com/api/docs/pricing` for the API |
| `model card` | `https://developers.openai.com/api/docs/models/<model-id>` |
| `rate limit` | `https://developers.openai.com/api/docs/models/<model-id>` for the numbers, `https://developers.openai.com/api/docs/guides/rate-limits` for the usage tiers |
| `docs` | Any other page on either documentation host |

Never link `https://openai.com/chatgpt/pricing/` or `https://chatgpt.com/pricing`.
Both return 403 to every tool this repository allows, so no reader and no agent
can check the figure. Never link `https://platform.openai.com/settings/...`,
which needs a login.

## Known gaps in the current rows

Checked on 2026-08-28. Each gap is a value the page publishes and the data does
not carry. Fixing one is a data edit, so do it under the "refresh prices" task
in `AGENTS.md`, not from this file.

| File | Gap |
|---|---|
| `data/api_pricing.yaml` | `cache_write` is `null` on all three rows. The pricing page publishes 5.00, 2.50, and 0.25. |
| `data/api_pricing.yaml` | `context_window` is `null` on all three rows. Every model page states 1,050,000. |
| `data/api_pricing.yaml` | The `rate limit` link points at `guides/rate-limits`, which publishes no per-model number. The model page does. |
| `data/models.yaml` | No OpenAI row exists. Three model pages publish a full specification. |
| `data/plans.yaml` | No Business row exists. The pricing page publishes a seat price for it. |
| `data/plans.yaml` | The `models` list on `openai-chatgpt-go` is unsourced. No page ties a model to the Go tier. |

A drafted, schema-valid replacement for every row above lives in the refresh
proposal written on 2026-08-28. It passed `python3 build.py --check` against a
scratch copy of the datasets. Re-verify the values before you paste them, since
a price can move after the draft.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
