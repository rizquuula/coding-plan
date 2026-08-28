---
name: provider-opencode
description: How to source OpenCode (Go) prices, quotas, and usage limits for the datasets in this repository. Use when you add or refresh an OpenCode row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions OpenCode, opencode.ai, OpenCode Go, OpenCode Zen, opencode-go, or Anomaly. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# OpenCode — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to OpenCode, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

**One page holds every number.** `https://opencode.ai/docs/go.md` is the `.md`
twin of the Go docs page. It states the usage-limit table, the per-model rate
table, and the endpoints table. Start there. The `/go` marketing page states the
plan price and nothing else you should copy. See trap 1.

## Constants

Write the provider as `OpenCode` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`currency` is `USD` in `data/api_pricing.yaml`. `price_currency` is `USD` in
`data/plans.yaml`. `region` is `global`.

OpenCode is an open-source coding agent, a CLI and TUI, built by Anomaly. The
source sits at `https://github.com/anomalyco/opencode`.

OpenCode Go is the subscription: $10 per month for curated access to open coding
models. One tier, monthly term only, cancel anytime.

OpenCode Zen is the console. It signs the user in, issues the API key, and holds
an optional top-up credit balance. Go falls back to the Zen balance after the
usage limit, when the user turns on "Use balance".

Every page is server-rendered, or serves an `.md` twin. `WebFetch` and
`curl -sL -A "Mozilla/5.0"` both return the full body. No bundle recipe and no
script are needed. This skill ships no `scripts/` directory.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| The Go plan price | `https://opencode.ai/go` | `WebFetch` |
| Per-model requests per 5 hours, per week, per month | `https://opencode.ai/docs/go.md` | `curl -sL` |
| Per-model input, output, cached read, cached write rates | `https://opencode.ai/docs/go.md` | `curl -sL` |
| The monthly included usage amount per model | `https://opencode.ai/docs/go.md` | `curl -sL` |
| API model ids and the config format | `https://opencode.ai/docs/go.md` | `curl -sL` |
| Model training and data retention | `https://opencode.ai/docs/go.md` | `curl -sL` |
| Every page URL | `https://opencode.ai/sitemap.xml` | `curl` |

`.md` twins exist on the `/docs` subtree only. `https://opencode.ai/go.md` and
`https://opencode.ai/llms.txt` return real 404s. Details in
`references/pages.md`.

## Nine things that produce a wrong number

**1. Never read a limit off the `/go` chart.** The chart interleaves numbers,
model names, and boost badges. A text strip or a summarizing fetch misaligns the
model and the number. A fetch on 2026-08-28 attributed 2,050 requests to Grok
4.6; the docs table says 169. Read the table in
`https://opencode.ai/docs/go.md`.

**2. The limit table's three columns are three time windows, not three tiers.**
The columns state requests per 5 hours, per week, and per month, all for the one
$10 plan. Do not turn the columns into three plan rows.

**3. The quotas are per 5 hours, and no schema field holds that.**
`data/rate_limits.yaml` fields are per minute or per day. An OpenCode row there
stays empty, so add none. Put the per-model quotas in the plan row's `limits`
list. Keep each item under 12 words.

**4. Boost badges such as "2x usage" are promotions, not the baseline.** The
chart shows a boosted number for some models. The docs table holds the baseline.
Copy the docs table.

**5. Eighteen locale twins duplicate every number.** `/ja/go`, `/de/go`,
`/zh/go`, and 15 more repeat the same USD figures. Always read the root path.

**6. `.md` twins exist for docs pages only.** `/docs/go.md` works. `/go.md` and
`/llms.txt` are real 404s with a correct 404 status, not soft 404s.

**7. Some per-model rates are tiered, and one schema field holds one rate.**
Grok 4.6 changes rate above 200K, GPT 5.6 Luna at 272K, Qwen3.7 Plus and Qwen3.6
Plus at 256K. The DeepSeek models split into peak and off-peak. Record the
at-or-below-threshold rate, and for DeepSeek the peak rate, in the numeric
fields. State the other tier in `notes`. This matches the Sakana convention.

**8. OpenCode's model prices are resale terms, not the upstream provider's
rates.** Cite an `opencode.ai` page for an OpenCode row only. Never use one as a
source for a DeepSeek, an Alibaba, or a Moonshot row.

**9. The "6x usage" figure is an aim, not a quota.** The docs say the aim is to
give about 6x the subscription price in usage. It is marketing, not a published
limit. Record nothing from it.

## Workflow

1. Read `https://opencode.ai/docs/go.md` with `curl -sL` or `WebFetch`.
2. Take the plan price from that page or from `https://opencode.ai/go`. It is
   $10 per month, monthly term only.
3. Put the per-model 5-hour quotas in the plan row's `limits` list.
4. Add `data/api_pricing.yaml` rows from the docs price table only.
5. Take each `model_id` from the endpoints table on the same page.
6. For a tiered rate, record the lower-threshold rate and state the other tier
   in `notes`.
7. Add no row to `data/rate_limits.yaml`. See trap 3.
8. Add no row to `data/models.yaml`. The pages state no parameter count and no
   context window.
9. Label the `/go` link `plans` and the docs link `docs`.
10. Set `last_verified` to the date you read the pages.
11. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, the sample values, and every outbound link |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
