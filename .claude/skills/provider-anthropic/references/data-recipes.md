# Anthropic rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to
Anthropic.

Constants for every Anthropic row in every file:

- `provider: Anthropic` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `region: global` in `data/plans.yaml`.
- `price_currency` and `currency` are `USD`.

## `data/plans.yaml`

Three rows: `anthropic-claude-pro`, `anthropic-claude-max-5x`,
`anthropic-claude-max-20x`.

```yaml
- id: anthropic-claude-max-20x
  provider: Anthropic
  plan: Claude Max 20x
  region: global
  price_currency: USD
  prices:
    - period: month
      amount: 200
  limits:
    - 20x the Pro usage
    - Higher output limits for all tasks
  models:
    - Claude Opus 5
    - Claude Sonnet 5
    - Claude Haiku 4.5
  status: active
  notes: Anthropic bills Max monthly only.
  links:
    - label: pricing
      url: https://claude.com/pricing
    - label: rate limit
      url: https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
  last_verified: 2026-08-28
```

Three rules this dataset needs:

1. Pro carries two `prices` entries, `month: 20` and `year: 200`. Write the
   annual total, not the rate the card prints. See `pricing.md`.
2. Max carries one `prices` entry, `month`. Anthropic bills Max monthly only.
3. The Max 20x price is not on `claude.com/pricing`. Add a second `pricing` link
   to `https://support.claude.com/en/articles/11049741-what-is-the-max-plan`,
   which is the page that states it.

Every `limits` item is a multiple, because Anthropic publishes no number. See
`quotas.md`.

## `data/api_pricing.yaml`

Six rows today: Claude Fable 5, Claude Opus 5, Claude Opus 4.8, Claude Sonnet 5,
Claude Sonnet 4.6, and Claude Haiku 4.5.

```yaml
- id: anthropic-claude-opus-5
  provider: Anthropic
  model: Claude Opus 5
  model_id: claude-opus-5
  context_window: 1M
  currency: USD
  input: 5.0
  cached_input: 0.5
  cache_write: 6.25
  output: 25.0
  notes: Fast mode is priced at 10.00 input and 50.00 output.
  links:
    - label: pricing
      url: https://platform.claude.com/docs/en/about-claude/pricing
    - label: rate limit
      url: https://platform.claude.com/docs/en/api/rate-limits
  last_verified: 2026-08-28
```

Notes on this dataset:

- `cache_write` is the 5-minute write. The 1-hour write goes in `notes`.
- `cached_input` is the `Cache Hits & Refreshes` column.
- Anthropic publishes both an alias and a dated ID for some models. The models
  overview lists Claude Haiku 4.5 as `claude-haiku-4-5-20251001`, with the alias
  `claude-haiku-4-5`. This file uses the alias. Keep that consistent.
- The pricing page publishes no context window. Take it from
  `https://platform.claude.com/docs/en/models/overview`.

### Where the context window for a legacy model comes from

The models overview compares four current models only: Fable 5, Opus 5, Sonnet 5,
and Haiku 4.5. Claude Opus 4.8 and Claude Sonnet 4.6 are not in that table.

The pricing page states one rule instead: models from Claude 4.6 on include the
full 1M token context window. That sentence is the source for the `1M` on those
two rows. It is a rule, not a printed cell, so re-read it every refresh.

Each legacy model also has its own page, at
`https://platform.claude.com/docs/en/models/opus-4-8/overview` and
`https://platform.claude.com/docs/en/models/sonnet-4-6/overview`. Nobody probed
those pages on 2026-08-28. Read one before you trust a per-model figure for a
legacy model.

## `data/rate_limits.yaml`

Eighteen rows today: six models times three tiers.

```yaml
- id: anthropic-claude-opus-4-8-build
  provider: Anthropic
  model: Claude Opus 4.8
  tier: Build
  requests_per_minute: 5000
  input_tokens_per_minute: 5000000
  output_tokens_per_minute: 1000000
  tokens_per_minute: null
  requests_per_day: null
  notes: Anthropic shares this limit across Claude Opus 4.8, 4.7, 4.6, and 4.5.
  links:
    - label: rate limit
      url: https://platform.claude.com/docs/en/api/rate-limits
  last_verified: 2026-08-28
```

Notes on this dataset:

- `tier` is `Start`, `Build`, or `Scale`. Write no row for the Evaluation tier
  or the Custom tier; neither publishes a number.
- `tokens_per_minute` is always `null`. Anthropic publishes a split, never a
  combined figure.
- `requests_per_day` is always `null`. Anthropic publishes no daily cap.
- The Claude Opus 4.8 rows and the Claude Sonnet 4.6 rows carry a pooled limit.
  State the pooling in `notes`. See `quotas.md`.

## `data/models.yaml`

Four rows today: Claude Fable 5, Claude Opus 5, Claude Sonnet 5, and Claude
Haiku 4.5.

```yaml
- id: claude-opus-5
  name: Claude Opus 5
  provider: Anthropic
  total_params: null
  active_params: null
  context_window: 1M
  max_output: 128K
  vision: true
  open_weights: false
  notes: Anthropic does not publish parameter counts.
  links:
    - label: model card
      url: https://platform.claude.com/docs/en/about-claude/models/overview
    - label: rate limit
      url: https://platform.claude.com/docs/en/api/rate-limits
  last_verified: 2026-08-28
```

Values read from `https://platform.claude.com/docs/en/models/overview` on
2026-08-28:

| Model | Context window | Max output | API ID |
|---|---|---|---|
| Claude Fable 5 | 1M tokens | 128K tokens | `claude-fable-5` |
| Claude Opus 5 | 1M tokens | 128K tokens | `claude-opus-5` |
| Claude Sonnet 5 | 1M tokens | 128K tokens | `claude-sonnet-5` |
| Claude Haiku 4.5 | 200K tokens | 64K tokens | `claude-haiku-4-5-20251001` |

Notes on this dataset:

- `total_params` and `active_params` are always `null`. Anthropic publishes no
  parameter count for any model.
- `open_weights` is always `false`.
- `vision` is `true` for every current model. The page states that all current
  models support text and image input.
- `max_output` is the synchronous Messages API limit. The Message Batches API
  accepts up to 300k output tokens behind a beta header. Do not write the beta
  figure into `max_output`.

## Link labels

Only these four fit an Anthropic row. The label describes what the page is.

| Label | URL |
|---|---|
| `pricing` | `https://claude.com/pricing` for plans, `https://platform.claude.com/docs/en/about-claude/pricing` for the API, `https://support.claude.com/en/articles/11049741-what-is-the-max-plan` for the Max 20x price |
| `plans` | `https://claude.com/pricing` |
| `rate limit` | `https://platform.claude.com/docs/en/api/rate-limits` for the API, `https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work` for a plan |
| `model card` | `https://platform.claude.com/docs/en/models/overview` |

Never link `https://platform.claude.com/settings/limits`. It needs a login.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
