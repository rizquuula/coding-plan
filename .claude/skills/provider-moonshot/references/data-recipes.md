# Moonshot rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to
Moonshot.

Constants for every Moonshot row in every file:

- `provider: Moonshot (Kimi)` — exact string. The build script groups by it, so
  a different spelling splits the provider into two tables.
- `region: global` in `data/plans.yaml`. The membership records carry
  `useRegion: REGION_OVERSEA` and state USD.
- `price_currency` and `currency` are `USD`.
- Use the display names `Kimi K3` and `Kimi K2.7 Code` in `model` and in
  `models`. `data/rate_limits.yaml` must match `data/api_pricing.yaml` exactly.

## `data/api_pricing.yaml`

Two rows today: `moonshot-kimi-k3` and `moonshot-kimi-k2-7-code`.

```yaml
- id: moonshot-kimi-k3
  provider: Moonshot (Kimi)
  model: Kimi K3
  model_id: kimi-k3
  context_window: 1M
  currency: USD
  input: 3.00
  cached_input: 0.30
  cache_write: null
  output: 15.00
  notes: The exact context window is 1048576 tokens.
  links:
    - label: pricing
      url: https://platform.kimi.ai/docs/pricing/chat-k3
    - label: rate limit
      url: https://platform.kimi.ai/docs/pricing/limits
  last_verified: 2026-08-28
```

Notes on this dataset:

- `input` is the page's "Cache Miss" column. `cached_input` is "Cache Hit".
- `cache_write` is always `null`. Moonshot publishes no cache-write rate.
- `context_window` is the short form. Put the exact token count in `notes`.
- The high-speed variant is not a separate row today. Its rates sit in the
  `notes` of the `kimi-k2.7-code` row. Split it into its own row only if the
  maintainer asks.

## `data/rate_limits.yaml`

Twelve rows today: six tiers for `Kimi K3` and six for `Kimi K2.7 Code`.

```yaml
- id: moonshot-kimi-k3-tier1
  provider: Moonshot (Kimi)
  model: Kimi K3
  tier: Tier1
  requests_per_minute: 200
  input_tokens_per_minute: null
  output_tokens_per_minute: null
  tokens_per_minute: 2000000
  requests_per_day: null
  notes: Kimi applies this limit account-wide, not per model.
  links:
    - label: rate limit
      url: https://platform.kimi.ai/docs/pricing/limits
  last_verified: 2026-08-28
```

Notes on this dataset:

- The published limit is account-wide. Every model repeats the same six rows.
  The `notes` field says so, on every row. Keep that sentence.
- `requests_per_day` is `null` on every row. The page caps tokens per day, not
  requests. The Tier0 rows carry that cap in `notes`.
- The `id` pattern is `moonshot-<model>-<tier>`, lower kebab-case, with the dot
  in a version number written as a dash: `moonshot-kimi-k2-7-code-tier0`.
- Add a model here only after you add it to `data/api_pricing.yaml`, and copy
  the `model` string across without editing it.

## `data/plans.yaml`

**No Moonshot row exists yet.** The prices are now sourceable. Run
`python3 scripts/read_plans.py` and read `quotas.md` for the `limits` wording.

A row would look like this. The prices come from the RPC on 2026-08-28. The
`limits` items come from the Kimi Code docs, because no page states a per-tier
number.

```yaml
- id: moonshot-kimi-allegretto
  provider: Moonshot (Kimi)
  plan: Allegretto
  region: global
  price_currency: USD
  prices:
    - period: month
      amount: 39
    - period: year
      amount: 372
  limits:
    - Quota refreshes every 7 days, no rollover
    - Rolling 5-hour window caps the request rate
    - Devices and API keys share one account quota
  models:
    - Kimi K3
    - Kimi K2.7 Code
  status: active
  notes: Kimi Code is the coding client inside this membership, not a separate
    subscription.
  links:
    - label: pricing
      url: https://www.kimi.com/membership/pricing
    - label: docs
      url: https://www.kimi.com/code/docs/en/kimi-code/models.html
  last_verified: 2026-08-28
```

Four rules for a plans row:

1. Moonshot sells no quarterly term. Write `month` and `year` only.
2. `amount` is the term total. The script already divides the cents. Copy what
   it prints.
3. Adagio is free. Give it one `month` entry with `amount: 0` and no `year`.
4. Use the `DOMAIN_NEXUS` tier names: Adagio, Moderato, Allegretto, Allegro,
   Vivace. See `pricing.md`.

## `data/models.yaml`

**No Moonshot row exists yet.** To add one, read
`https://platform.kimi.ai/docs/guide/kimi-k3-quickstart` and use `model card` as
the link label.

What that page states about Kimi K3, read 2026-08-28:

- 2.8 trillion parameters.
- A 1M-token context window.
- Native visual understanding, so `vision: true`.
- "the world's first open-source model in the 3-trillion-parameter class", and
  the full weights release by 2026-07-27. Set `open_weights: true` and cite the
  page.

Two gaps you cannot fill from any page found on 2026-08-28:

- No page prints a maximum output for any Kimi model. Leave `max_output` as
  `null`.
- No page prints active parameters per token. Leave `active_params` as `null`.

`https://platform.kimi.ai/docs/models` lists `kimi-k2.7-code` under the heading
"Multi-modal Model" and states a 256K context. Its description names no image
input. `https://www.kimi.com/code/docs/en/kimi-code/models.html` states that the
same model takes image and video input. Neither page states `vision` outright.
Read both before you set `vision` on a K2.7 Code row, and record what you
decide.

## Link labels

Only these four fit a Moonshot row.

| Label | URL |
|---|---|
| `pricing` | `https://platform.kimi.ai/docs/pricing/chat-k3` and the sibling model pages; `https://www.kimi.com/membership/pricing` for plans |
| `rate limit` | `https://platform.kimi.ai/docs/pricing/limits` |
| `model card` | `https://platform.kimi.ai/docs/guide/kimi-k3-quickstart`, once a model row exists |
| `docs` | `https://www.kimi.com/code/docs/en/kimi-code/models.html` |

Never link a `platform.moonshot.ai` path. It 301s to `platform.kimi.ai`, so it
hides which stack the value came from.

Never link `https://platform.kimi.com/...`. That is the china stack and it
publishes different numbers.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` may not be on PATH in this environment.
