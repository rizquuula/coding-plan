---
name: provider-ollama
description: How to source Ollama Cloud prices, quotas, and model availability for the datasets in this repository. Use when you add or refresh an Ollama row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Ollama, Ollama Cloud, ollama.com, cloud models, Ollama Pro, Ollama Max, or Ollama Team. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Ollama — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Ollama, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Ollama` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables. `region` is `global`. `price_currency` is `USD`.

Ollama sells six tiers: Free, Pro, Max, Team, and Enterprise, plus a paused-but-
active Max sign-up state. `data/plans.yaml` holds Free, Pro, Max, and Team
today. Enterprise carries no published price, so it gets no row. See trap 9.

Ollama Cloud resells other providers' open models. It publishes no per-token
USD rate and no numeric usage quota, so three of the four datasets hold zero
Ollama rows. See "Datasets with zero rows".

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| All five plan cards, prices, features, FAQ | `https://ollama.com/pricing` | `curl` |
| The cloud-enabled model list | `https://ollama.com/search?c=cloud` | `curl` |
| Cloud usage overview, no prices | `https://docs.ollama.com/cloud.md` | `curl` |
| Every docs page and its `.md` URL | `https://docs.ollama.com/llms.txt` | `curl` |
| Site-wide llms.txt on the marketing domain | `https://ollama.com/llms.txt` | `curl` |
| Per-account usage dashboard (auth-gated) | `https://ollama.com/settings` | dead end |

## Traps that produce a wrong number

**1. `ollama.com/pricing` is server-rendered.** `curl` returns every price,
every feature line, and the full FAQ in one request. No JavaScript bundle
chase is needed. Strip tags with `sed 's/<[^>]*>/ /g'` to read it.

**2. `docs.ollama.com` is Mintlify, and every page serves a `.md` twin.**
`https://docs.ollama.com/llms.txt` lists every page and its markdown URL.
`ollama.com/llms.txt` also exists, on the marketing domain. Neither docs page
states a price or a quota; pricing lives only on `ollama.com/pricing`.

**3. Ollama publishes no numeric usage quota.** Plans are described by
relative multipliers — Pro is "50x more cloud usage than Free", Max is "5x
more usage than Pro" — and by model usage levels 1 to 4. The 5-hour and 7-day
reset windows carry no published number. `data/rate_limits.yaml` holds zero
Ollama rows because there is no number to record.

**4. The concurrency limits are per plan, not per model.** Free runs 1 cloud
model at a time, Pro runs 3, Max runs 10. These belong in `limits` on the plan
rows in `data/plans.yaml`, not in `data/rate_limits.yaml`.

**5. No public per-token USD rate exists.** The Team FAQ mentions "the
model's token rate" for shared-balance overage, but no public page states any
rate. The usage dashboard sits behind login at `ollama.com/settings`.
`data/api_pricing.yaml` holds zero Ollama rows.

**6. Pro's yearly price is already the term total.** The page reads "$20/mo,
or $200/yr billed annually". Write `amount: 200` for the year directly. Do not
multiply the monthly rate by 12, unlike Z.ai or Cursor.

**7. Max sign-ups are paused, but the plan is not discontinued.** The FAQ
says new Max subscriptions are temporarily paused while Ollama adds capacity,
and that existing subscribers keep their plan, limits, and pricing. Keep
`status: active` and state the pause in `notes`.

**8. Team is priced per seat with a 5-seat minimum.** The card reads "$25 /
seat / mo, 5-seat minimum, usage included". The `prices` schema in
`AGENTS.md` defines `amount` as the price for one seat, so write `25` and
state the $125 minimum in `notes`.

**9. Enterprise has no published price.** The card reads "Custom" and links
to a contact form. The `prices` schema requires a numeric `amount`, so
Enterprise gets no row in `data/plans.yaml`.

**10. Every cloud model belongs to another provider.** DeepSeek, Google,
Zhipu, OpenAI's gpt-oss, Moonshot, MiniMax, Mistral, NVIDIA, and Alibaba each
keep their own model's specifications on their own provider's pages.
`data/models.yaml` holds zero Ollama rows because Ollama is a reseller, not
the source of those specifications.

**11. The library lists base names; runtime commands add a `-cloud` suffix.**
`ollama.com/search?c=cloud` lists `gpt-oss`, but running it needs
`ollama run gpt-oss:120b-cloud`. Cite the library names in `data/plans.yaml`.

**12. A model-access hint is not a model-list claim.** Pro's feature line
"Access larger, more powerful cloud models" implies Free excludes some
models, but no page states which models Free excludes. Use the same model
list on every tier; do not invent a per-tier difference.

## Datasets with zero rows

Three datasets hold no Ollama row, and each zero is correct.

- `data/api_pricing.yaml` — Ollama publishes no per-token USD rate for any
  cloud model. See trap 5.
- `data/rate_limits.yaml` — Ollama names two reset windows and two
  concurrency limits, and publishes no numeric quota for any of them.
  Concurrency belongs in `data/plans.yaml` instead. See traps 3 and 4.
- `data/models.yaml` — every cloud model belongs to another provider's own
  catalog. See trap 10.

Do not add a row of nulls to record any of these absences.

## Workflow

1. Read `https://ollama.com/pricing` with `curl -sL`, stripped of tags. Take
   the price, features, and FAQ wording for Free, Pro, Max, and Team.
2. Read `https://ollama.com/search?c=cloud` with `curl -sL`. Extract model
   names with `grep -o 'href="/library/[^"]*"'`.
3. Cross-check the four prices and the concurrency limits against the FAQ
   section on the same page.
4. Write or refresh the four plan rows in `data/plans.yaml`. Add no row to
   `data/api_pricing.yaml`, `data/rate_limits.yaml`, or `data/models.yaml`.
5. Set `last_verified` to the date you read the pages.
6. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its rendering behavior, and the settings dead end |
| `references/plans.md` | The tier detail as read on 2026-08-28, sourcing context only |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
