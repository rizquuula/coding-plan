---
name: provider-mistral
description: How to source Mistral prices, quotas, and API rates for the datasets in this repository. Use when you add or refresh a Mistral row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Mistral, mistral.ai, Vibe, Le Chat, Mistral Large, Mistral Medium, Mistral Small, Mistral OCR, or the Mistral API. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Mistral — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Mistral, so you do not repeat work that already failed.

Everything here was checked on 2026-08-30. Re-check a status before you trust it.

**Two pages hold every number.** `https://mistral.ai/pricing/` states the
subscription tiers (Free, Pro, Team, Enterprise). `https://mistral.ai/pricing/api/`
states the per-model API rates. Both are server-rendered and return the full
body to `curl -sL -A "Mozilla/5.0"`. No bundle recipe and no script are needed.
This skill ships no `scripts/` directory.

## Constants

Write the provider as `Mistral` in all five data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`price_currency` is `USD` in `data/plans.yaml`. `currency` is `USD` in
`data/api_pricing.yaml`. The page has a USD/EUR toggle; the USD figure is the
one to record. `region` is `global`.

Mistral is a French model lab that sells both subscriptions (Vibe) and a
pay-as-you-go API. Its own models are Large 3, Medium 3.5, Small 4, and the
OCR/audio/embedding family. It also resells one third-party model, GLM 5.2
from Z.ai, on its API. See trap 4.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Free / Pro / Team / Enterprise tier prices | `https://mistral.ai/pricing/` | `curl -sL -A "Mozilla/5.0"` |
| API credits included per tier | `https://mistral.ai/pricing/` | same |
| Per-model API rates (Large 3, Medium 3.5, Small 4, GLM 5.2) | `https://mistral.ai/pricing/api/` | same |
| Model ids (`mistral-large-latest`, etc.) | `https://mistral.ai/pricing/api/` | same |
| OCR / audio / embedding pricing | `https://mistral.ai/pricing/api/` | same (not token-based) |
| Enterprise / private deployment | `https://mistral.ai/pricing/enterprise-deployments/` | `curl` |

The pricing page is server-rendered. The API page is also server-rendered and
lists ~25 model cards; the token-based models appear with `Input (/M tokens)`
and `Output (/M tokens)` rows.

## Four things that produce a wrong number

**1. The pricing page and the API page are two different pages.** The plans
page (`/pricing/`) holds the subscription tiers. The API page (`/pricing/api/`)
holds the per-model rates. A model's price is NOT on the plans page, and the
plan prices are NOT on the API page. Fetch both. Do not guess a URL — the links
are `https://mistral.ai/pricing/` and `https://mistral.ai/pricing/api/`.

**2. Pro has two prices.** The card shows `$14.99/mo`, and a student footnote
says verified students pay `$5.99/mo` (normally `$14.99`). Record the standard
`$14.99`. The student price is a discount, not a tier.

**3. Some API products are not per-token.** OCR 4.1 is `$4` per 1,000 pages,
Voxtral TTS is `$0.016` per 1k characters, audio transcription is per minute,
and the classifier/fine-tune APIs are per job or per token with a `$4` minimum.
These do not fit the `api_pricing.yaml` schema (input/output per 1M tokens).
Add rows only for the token-based models: Large 3, Medium 3.5, Small 4, and the
GLM 5.2 resale. Leave OCR/audio/embedding out.

**4. GLM 5.2 is a resale.** Mistral resells Z.ai's GLM 5.2 at `$1.4` in /
`$4.4` out / `$0.14` cached. A GLM 5.2 row already exists under `Zhipu (GLM)`
in the data. The Mistral row is legitimate — it is Mistral's own published
rate for the model on its API — but keep the provider spelling `Mistral` and
the model name `GLM 5.2` exactly as the page writes it, so the two rows do not
collide in the left-join.

**5. `context_window` is not stated.** The API page lists no context window
for Large 3, Medium 3.5, Small 4, or GLM 5.2. Write `null`. The page also
states no parameter count, so `models.yaml` rows carry `null` params.

**6. Vision and open-weights are only stated for Large 3.** The API page calls
Large 3 "multimodal" and "open-weight". For Medium 3.5 and Small 4 it states
neither, so write `null` for both fields on those rows (per the AGENTS.md
`open_weights`/`vision` rule).

## Workflow

1. Read `https://mistral.ai/pricing/` for the four tier prices and the included
   API-credit figures.
2. Read `https://mistral.ai/pricing/api/` for the per-model rates.
3. Write one `data/plans.yaml` record per tier: Free ($0), Pro ($14.99), Team
   ($24.99/user). Add no Enterprise row — it is "Contact us" with no price and
   the schema requires a `prices` amount.
4. Write `data/api_pricing.yaml` rows for Large 3, Medium 3.5, Small 4, and
   GLM 5.2 with the token rates and `model_id` from the page.
5. Write `data/models.yaml` rows matching those four, with `null` specs except
   where the page states a value.
6. Add no row to `data/rate_limits.yaml`. The API page mentions "increased
   rate limits" only as an Enterprise-API selling point; it publishes no RPM
   or TPM number anywhere.
7. Use only `mistral.ai` URLs in `links`. Label the plans page `plans` and the
   API page `pricing`.
8. Set `last_verified` to the date you read the pages.
9. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, the tier values, the model rates, and the traps |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
