# GitHub rows, dataset by dataset

Schemas live in `AGENTS.md`. This file records only what is specific to GitHub.

Constants for every GitHub row in every file:

- `provider: GitHub` — exact string. The build script groups by it, so a
  different spelling splits the provider into two tables.
- `region: global` in `data/plans.yaml`.
- `price_currency` and `currency` are `USD`.

## `data/plans.yaml`

Three rows: `github-copilot-pro`, `github-copilot-pro-plus`,
`github-copilot-max`.

```yaml
- id: github-copilot-pro
  provider: GitHub
  plan: Copilot Pro
  region: global
  price_currency: USD
  prices:
    - period: month
      amount: 10
  limits:
    - 15 USD of AI credits per month
    - Unlimited code completions
  models:
    - Claude
    - GPT
    - Gemini
  status: active
  notes: GitHub bills AI usage in credits. One credit costs 0.01 USD.
  links:
    - label: plans
      url: https://github.com/features/copilot/plans
    - label: rate limit
      url: https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals
  last_verified: 2026-08-28
```

Notes on this dataset:

- `prices` holds one `month` entry and nothing else. GitHub sells no yearly
  term. See `pricing.md`.
- `limits` states the allowance in the marketing page's unit, dollars per month.
  The equivalent credit count is 1,500. Pick one unit and keep it.
- "Unlimited code completions" is sourced. GitHub states that completions and
  next edit suggestions cost no credits on any paid plan.
- The `rate limit` link points at the billing page, because that page states the
  numeric monthly quota. `https://docs.github.com/en/copilot/concepts/usage-limits`
  is the page about rate limits, and it prints no number.

### Known gap in `models`

All three rows list `Claude`, `GPT`, and `Gemini`. The provider's page lists
seven vendors and separates Pro from Pro+ and Max. See the model table in
`pricing.md`. Two facts the current rows do not carry:

- Copilot also unlocks Grok, Kimi, MAI-Code, and Raptor mini.
- Copilot Pro unlocks no Opus model, no GPT-5.5, and no GPT-5.6 Sol.

Widening the lists is a scope decision. Ask before you change a `models` list.

## `data/api_pricing.yaml`

**No GitHub row, on purpose.**

`AGENTS.md` describes this dataset as per-model API rates. GitHub sells no
public model API. The rates on
`https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing`
price additional usage inside a Copilot subscription. A reader cannot buy tokens
at those rates without a Copilot seat.

Two further reasons not to add a row:

1. Every model on that page except Raptor mini belongs to another vendor. A
   `GitHub` row for Claude Opus 5 would duplicate the Anthropic row under the
   wrong provider.
2. The page carries promotions and a long-context tier. Its figures therefore
   drift from the vendor's own rate. On 2026-08-28 it priced GPT-5.6 Sol at 2.00
   input, while OpenAI's own rate in this repository is 4.00.

Raptor mini is the one GitHub model with a published rate: 0.25 input, 0.025
cached input, 2.00 output, per 1M tokens. Adding it is a scope decision. It is
still not an API. Ask first.

## `data/rate_limits.yaml`

**No GitHub row, on purpose.**

GitHub publishes no numeric request or token limit for Copilot.
`https://docs.github.com/en/copilot/concepts/usage-limits` states that rate
limits exist, gives four reasons for them, and prints no figure.

The monthly credit allowance is a spend quota, not a rate limit. It belongs in
`limits` in `data/plans.yaml`, and it already sits there.

Do not add a row of nulls to record the absence. Do not take a number from a
comparison site, a blog, or an aggregator. `AGENTS.md` rule 4 forbids it.

## `data/models.yaml`

**No GitHub row, on purpose.**

GitHub publishes one model of its own, Raptor mini.
`https://docs.github.com/en/copilot/reference/ai-models/supported-models`
describes it as a fine-tuned GPT-5 mini and prints no specification. No
parameter count and no context window appear on any GitHub page.

That page also states a retirement date for Raptor mini of 2026-09-01, with
MAI-Code-1-Flash as the replacement. Check that date before you invest in a row.

The same page prints no context window for any model. It describes a 1 million
token context window as an optional extended capability on selected models, and
names no default size. So `context_window` stays `null` for any GitHub-sourced
row.

## Link labels

Only these fit a GitHub row. The label describes what the page is.

| Label | URL |
|---|---|
| `plans` | `https://github.com/features/copilot/plans` |
| `pricing` | `https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing` |
| `rate limit` | `https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals` |
| `docs` | `https://docs.github.com/en/copilot/get-started/plans` |

Never link a page under `copilot-billing/request-based-billing-legacy/`. Those
pages describe a billing model GitHub retired on 2026-06-01.

## After any change

```bash
python3 build.py --check
```

Use `python3`. Plain `python` is not on PATH in this environment.
