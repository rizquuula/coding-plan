# Alibaba rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to Alibaba.

Constants for every Alibaba row in every file:

- `provider: Alibaba (Qwen)` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- **An `id` never holds a dot.** Alibaba model IDs do: `qwen3.7-max`. The
  repository writes a version dot as a hyphen, the same as every other provider
  in the data (`anthropic-claude-haiku-4-5`, `google-gemini-3-5-flash`,
  `moonshot-kimi-k2-7-code`). So `qwen3.7-max` becomes `alibaba-qwen3-7-max`.
  Check for a collision before you commit: `qwen3-max` and `qwen3.7-max` must not
  both map to `alibaba-qwen3-max`.
- `region: global` in `data/plans.yaml`. Alibaba sells the plans on its
  international site.
- `price_currency` and `currency` are `USD`. Source the international site, not
  the China site. See `pages.md`.

## `data/api_pricing.yaml`

One row today: `alibaba-qwen-max`.

```yaml
- id: alibaba-qwen-max
  provider: Alibaba (Qwen)
  model: Qwen-Max
  model_id: qwen-max
  context_window: 128K
  currency: USD
  input: 1.60
  cached_input: null
  cache_write: null
  output: 6.40
  notes: Singapore rate for the International deployment scope; mainland China
    deployments cost less.
  links:
    - label: pricing
      url: https://www.alibabacloud.com/help/en/model-studio/model-pricing
    - label: rate limit
      url: https://www.alibabacloud.com/help/en/model-studio/rate-limit
  last_verified: 2026-08-28
```

That block shows the values the page states, not the values in the file today.
The file holds `input: 2.50`, `output: 7.50`, `context_window: null`, and a
`pricing` link to the old slug `billing-for-model-studio`. See `pricing.md` for
why those three fields are wrong.

Notes on this dataset:

- `cached_input` and `cache_write` are `null` for `qwen-max`. The cache page
  does not list that model. See `pricing.md`.
- `context_window` comes from `text-generation-model`, not from the pricing
  page.
- A model with tiered pricing needs the range in `notes`. See `pricing.md`.
- The pricing page lists over 200 models, including third-party models such as
  DeepSeek, Kimi, GLM, and MiniMax. Add a Qwen model only when it belongs in a
  coding-plan tracker. A third-party model billed through Model Studio belongs
  under that vendor's own provider row, not under `Alibaba (Qwen)`.

## `data/rate_limits.yaml`

Three rows today, one per region: `alibaba-qwen-max-singapore`,
`alibaba-qwen-max-us-virginia`, `alibaba-qwen-max-china-beijing`.

```yaml
- id: alibaba-qwen-max-singapore
  provider: Alibaba (Qwen)
  model: Qwen-Max
  tier: Singapore
  requests_per_minute: 600
  input_tokens_per_minute: null
  output_tokens_per_minute: null
  tokens_per_minute: 1000000
  requests_per_day: null
  notes: Alibaba publishes limits per region, not per usage tier. TPM counts
    input plus output tokens.
  links:
    - label: rate limit
      url: https://www.alibabacloud.com/help/en/model-studio/rate-limit
  last_verified: 2026-08-28
```

Rules for this dataset:

- `tier` holds the region name, because Alibaba publishes no usage tier. Use the
  exact region heading: `Singapore`, `US (Virginia)`, `China (Beijing)`,
  `Germany (Frankfurt)`, `Hong Kong (China)`, `Japan (Tokyo)`.
- Set `tokens_per_minute`. Leave the input and output splits `null`. Alibaba
  publishes a combined TPM.
- `model` must match `data/api_pricing.yaml`. Add the pricing row first.
- Write one row per region that lists the model. Write no row for a region that
  omits it. See `quotas.md` for the US (Virginia) case.

## `data/plans.yaml`

**No Alibaba row exists yet.** Two products could fill one. Read `quotas.md`
first, then use this shape for the Coding Plan.

```yaml
- id: alibaba-coding-plan-pro
  provider: Alibaba (Qwen)
  plan: Coding Plan Pro
  region: global
  price_currency: USD
  prices:
    - period: month
      amount: 50
  limits:
    - 6000 requests per 5 hours
    - 45000 requests per week
    - 90000 requests per month
  models:
    - Qwen3.7-Plus
    - Qwen3-Coder-Plus
    - GLM
    - Kimi
    - MiniMax
  status: active
  notes: Alibaba publishes a monthly price only; the purchase page needs a login.
  links:
    - label: plans
      url: https://www.alibabacloud.com/help/en/model-studio/coding-plan
  last_verified: 2026-08-28
```

Write only a `month` entry in `prices`. Alibaba publishes no quarterly or yearly
total. Never multiply the monthly price to invent one.

Use `plan: Token Plan Personal Pro` and a separate `id` for a Token Plan row.
The two products must never share a row.

## `data/models.yaml`

**No Alibaba row exists yet.** To add one, read
`https://www.alibabacloud.com/help/en/model-studio/text-generation-model.md` and
use `docs` as the link label. That page is a model comparison page, not a model
card, so `model card` does not fit.

Fields you can fill and fields you cannot:

| Field | Source |
|---|---|
| `context_window` | `text-generation-model`. See the table in `pricing.md`. |
| `max_output` | `vision-model`, and only for the models it lists. Otherwise `null`. See `pricing.md`. |
| `total_params` | Not published for the closed models. Use `null`. |
| `active_params` | Not published for the closed models. Use `null`. |
| `vision` | Three pages, in this order of preference. See below. |
| `open_weights` | The section heading on `model-pricing`. See below. |

### `vision`

`text-generation-model` publishes no vision column. It publishes context,
thinking mode, function calling, built-in tools, and structured output. Three
other pages answer the question. Prefer them in this order.

1. `token-plan-personal-overview` and `token-plan-team-overview` have a
   `Capability` column that names visual understanding per model. This is a
   direct statement. Use it first. The table is in `quotas.md`.
2. `vision-model` has an `Input` column that reads `Text, images, video`. Also a
   direct statement, and it carries `max_output` as a bonus.
3. `coding-plan` writes `(vision)` after some model IDs and not others. This is
   weaker: it tells you what the tag means only by contrast within one page, and
   the page covers the plan models only.

`vision` is a required boolean, so you must write `true` or `false` even when no
page states either. When you fall back to an argument from absence, say so in the
row's `notes` and raise it with the user. Absence is the weakest evidence in this
skill.

### `open_weights`

`model-pricing` and `rate-limit` both split Qwen into two top-level sections:

    ## Text generation - Qwen
    ## Text generation - Qwen (open source)

That split is Alibaba classifying its own models, so it sources the flag. A model
in the second section gets `true`. A model in the first section gets `false`.

Read 2026-08-28, for the models this repository prices:

| Section | Models |
|---|---|
| `Text generation - Qwen` | `qwen-max`, `qwen3-max`, `qwen3.7-max`, `qwen3.8-max`, `qwen3.7-plus`, `qwen3-coder-plus`, `qwen3-coder-flash` |
| `Text generation - Qwen (open source)` | `qwen3-coder-next`, `qwen3-coder-480b-a35b-instruct`, `qwen3-coder-30b-a3b-instruct`, `qwen3.8-2.4t-a95b`, `qwen3.8-27b` |

Note `qwen3-coder-next`. Its ID carries **no** parameter count, and it is still
an open-weight release. So the old ID heuristic is not reliable on its own. Read
the section heading.

The ID heuristic still helps as a cross-check: an ID that carries a parameter
count, such as `qwen3-coder-480b-a35b-instruct` or `qwen3.5-27b`, has always
turned out to sit in the open-source section. An ID without one may sit in
either. Never set the flag from reputation.

A parameter count inside a model ID is not a published parameter count. Do not
copy `2.4t-a95b` into `total_params` and `active_params`. Find a page that states
the numbers, or leave both `null`.

## Link labels

Only these four fit an Alibaba row. The label describes what the page is.

| Label | URL |
|---|---|
| `pricing` | `https://www.alibabacloud.com/help/en/model-studio/model-pricing` |
| `plans` | `.../coding-plan`, `.../token-plan-personal-overview`, or `.../token-plan-team-overview` |
| `rate limit` | `https://www.alibabacloud.com/help/en/model-studio/rate-limit` |
| `docs` | `.../text-generation-model`, `.../vision-model`, or `.../context-cache` |

Add a second link when the value did not come from the first page. A pricing row
whose `cached_input` you computed from a percentage should carry a `docs` link to
`context-cache`, so the reader can check the rule you applied.

Cite the slug, never a `document_detail/<id>.html` link and never a `.md` twin.
The twin is how you read the page. The reader opens the page.

Never link the console, the purchase page, or `qwen.ai`. See `pages.md`.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
