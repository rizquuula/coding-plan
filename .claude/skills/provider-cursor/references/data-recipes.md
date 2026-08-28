# Cursor rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to Cursor.

Constants for every Cursor row in every file:

- `provider: Cursor` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `region: global` in `data/plans.yaml`.
- `price_currency` is `USD`. Cursor prints USD everywhere except the India-only
  Start tier.

## `data/plans.yaml`

Three rows today: `cursor-pro`, `cursor-pro-plus`, `cursor-ultra`.

```yaml
- id: cursor-pro-plus
  provider: Cursor
  plan: Pro+
  region: global
  price_currency: USD
  prices:
    - period: month
      amount: 60
    - period: year
      amount: 576
  limits:
    - 3x the Pro agent limits
    - On-demand billing past the included usage
  models:
    - Claude
    - GPT
    - Gemini
    - Grok
    - Composer
  status: active
  notes: Cursor prints a rate per month; the year total is that rate times 12.
  links:
    - label: pricing
      url: https://cursor.com/docs/models-and-pricing
    - label: plans
      url: https://cursor.com/pricing
    - label: rate limit
      url: https://cursor.com/help/models-and-usage/usage-limits
  last_verified: 2026-08-28
```

Four notes on this dataset.

1. `plan` uses the spelling Cursor uses: `Pro`, `Pro+`, `Ultra`. The help page
   writes `Pro+` and the marketing page writes `Pro Plus`. Pick `Pro+`, which is
   what the pricing table uses.
2. Cursor offers `month` and `year` only. There is no quarterly term.
3. `amount` for `year` is the yearly rate times 12. See `pricing.md`.
4. No Hobby row, no Start row, and no Team row exists today. Hobby is free and
   Start is priced in INR, which `price_currency` does not allow. Adding a Team
   row is a scope decision. Ask first.

## What the three rows hold on 2026-08-28

| Row | `month` | `year` | `limits` |
|---|---|---|---|
| `cursor-pro` | 20 | absent | Extended agent request limits |
| `cursor-pro-plus` | 60 | absent | 3x the Pro agent limits |
| `cursor-ultra` | 200 | absent | 20x the Pro agent limits |

Every monthly price matches the provider page. No row carries the yearly term
yet, and every row still cites the redirect path
`https://cursor.com/docs/account/pricing`. Fix both on the next refresh.

A full refresh proposal was drafted on 2026-08-28. It adds the yearly term to
all three rows, repoints `pricing` to `https://cursor.com/docs/models-and-pricing`,
adds `Grok`, `Kimi`, and `GLM` to `models`, and adds two Teams rows. It was
validated in a sandbox: `ok: 138 records passed validation`. It was not applied.

## `data/api_pricing.yaml`

**No Cursor row, on purpose.**

Cursor sells no public per-token API. The rates on
`https://cursor.com/docs/models-and-pricing` are in-product resale rates. Most
of them belong to other providers, and the build script groups every table by
`provider`, so a resold rate never goes on a Cursor row.

Three models on that page are Cursor's own: Grok 4.6, Grok 4.5, and Composer
2.5. Their rates are sourced and reachable, listed in `pricing.md`. Adding them
is a scope decision, not a sourcing problem. Ask before you add one.

If you do add one, set `cache_write: null`. Cursor prints `-` in that column for
all six of its own entries.

## `data/rate_limits.yaml`

**No Cursor row, on purpose.** See `quotas.md`. Cursor publishes numeric limits
for its Admin, Analytics, Bugbot, and Cloud Agents REST APIs, and none of them
is a per-model limit. Do not add a row of nulls.

## `data/models.yaml`

**No Cursor row, on purpose.**

The schema needs a `vision` boolean. No Cursor page states it for Composer or
Grok. Do not guess it.

`open_weights` no longer blocks a row. It is nullable now, and `null` is the
correct value for all three Cursor models. Do not read the Composer 2.5 blog
sentence "built on the same open-source checkpoint as Composer 2, Moonshot's
Kimi K2.5" as an open-weights claim. It describes the base checkpoint. Cursor
publishes no Composer weights.

The model card does publish a context window and a model ID. Read the HTML, not
the `.md` twin, which drops the card. See `pages.md`. If a page ever states the
missing booleans, use `model card` as the link label and
`https://cursor.com/docs/models/cursor-composer-2-5` as the URL.

## Link labels

Only these four fit a Cursor row. The label describes what the page is.

| Label | URL |
|---|---|
| `pricing` | `https://cursor.com/docs/models-and-pricing` |
| `plans` | `https://cursor.com/pricing` |
| `rate limit` | `https://cursor.com/help/models-and-usage/usage-limits` |
| `model card` | `https://cursor.com/docs/models/cursor-composer-2-5`, once a model row exists |

Never link a `https://cursor.com/dashboard/...` page. It needs a login.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
