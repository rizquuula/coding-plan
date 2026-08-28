---
name: provider-deepseek
description: How to source DeepSeek prices, model specifications, and concurrency limits for the datasets in this repository. Use when you add or refresh a DeepSeek row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions DeepSeek, deepseek-chat, deepseek-reasoner, deepseek-v4-pro, deepseek-v4-flash, or DeepSeek Harness. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# DeepSeek — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to DeepSeek, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `DeepSeek` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`currency` is `USD` in `data/api_pricing.yaml`. The English pricing page prints
USD. The Chinese twin prints CNY. See trap 2.

DeepSeek sells no subscription plan. `data/plans.yaml` holds zero DeepSeek rows
and that is correct. See trap 5. A future plan row would take `region: china`,
because DeepSeek is a Chinese company and files a Chinese ICP number on
`https://www.deepseek.com/`.

DeepSeek serves three models today: `deepseek-v4-pro`, `deepseek-v4-flash`, and
`deepseek-v4-flash-vision-exp`.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| API rates per token, peak and off-peak | `https://api-docs.deepseek.com/quick_start/pricing` | `WebFetch` |
| Context length, max output, model version | `https://api-docs.deepseek.com/quick_start/pricing` | `WebFetch` |
| Concurrency limit per model | `https://api-docs.deepseek.com/quick_start/rate_limit` | `WebFetch` |
| Parameter counts, open weights | `https://www.deepseek.com/en/news/v4-preview/` | `WebFetch` |
| Every docs URL | `https://api-docs.deepseek.com/sitemap.xml` | `curl` |

`WebFetch` reads every page in that table. DeepSeek renders the docs server
side, so no bundle recipe and no script are needed. This skill ships no
`scripts/` directory.

## Eight things that produce a wrong number

**1. `api-docs.deepseek.com` answers an unknown path with 200 and the wrong
page.** It serves the "Your First API Call" home page, 46100 bytes, for any path
it does not know. So `quick_start/pricing.md`, `llms.txt`, `llms-full.txt`, and
`/en/quick_start/pricing` all look like successes and all hold the wrong
content. There is no `.md` twin and no `llms.txt` on this site. Read
`sitemap.xml` to find a page. Details in `references/pages.md`.

**2. The `zh-cn` page prices in CNY, the default page prices in USD.** The two
pages hold different numbers, not a converted pair. `deepseek-v4-pro` cache-miss
peak is `$1.32` on the default page and `9.0元` on the Chinese twin.
`https://www.deepseek.com/` links to the Chinese docs by default, so it is easy
to land on the wrong one. Always read the path without a language prefix.

**3. The pricing table stacks off-peak above peak in every row.** Each rate
appears twice. `data/api_pricing.yaml` records the peak rate, which is the
second number. A naive read takes the first number and halves every rate. Table
in `references/pricing.md`.

**4. DeepSeek publishes a concurrency limit, not a per-minute rate limit.** No
page states requests per minute or tokens per minute. Every numeric field in a
DeepSeek `data/rate_limits.yaml` row stays `null`, and the concurrency number
goes in `notes`. Reasoning in `references/rate-limits.md`.

**5. DeepSeek sells no subscription plan.** No page on `www.deepseek.com` or
`api-docs.deepseek.com` states a plan price. The API is pay per token, from a
topped-up balance. Add no row to `data/plans.yaml`.

**6. The Chinese launch page omits the parameter counts; the English one states
them.** `https://www.deepseek.com/news/v4-preview/` says only that the models
split into two sizes. `https://www.deepseek.com/en/news/v4-preview/` prints
`1.6T total / 49B active` and `284B total / 13B active`. Use the `/en/` path for
`data/models.yaml`.

**7. `deepseek-chat` and `deepseek-reasoner` are retired.** DeepSeek withdrew
both on 2026-07-24. The pricing page no longer lists them. Add no row for
either. Treat the names as search terms only.

**8. `deepseek-v4-pro[1m]` is not a `model_id`.** That string appears in
`https://api-docs.deepseek.com/guides/coding_agents` as an environment variable
for Claude Code. The pricing page states the API model string, which is
`deepseek-v4-pro`. Copy the pricing page value.

## Workflow

1. Read `https://api-docs.deepseek.com/quick_start/pricing`.
2. Take the peak rate from each pricing row. Ignore the off-peak rate.
3. Take `CONTEXT LENGTH` and `MAX OUTPUT` from the same page.
4. Read `https://api-docs.deepseek.com/quick_start/rate_limit`.
5. Copy the concurrency limit into `notes`. Leave every numeric field `null`.
6. Read `https://www.deepseek.com/en/news/v4-preview/` for parameter counts.
7. Cross-check: the concurrency table appears on both docs pages. The two must
   agree. Report a mismatch rather than picking a side.
8. Write the rows. Copy the shapes in `references/data-recipes.md`.
9. Add no row to `data/plans.yaml`.
10. Set `last_verified` to the date you read the pages.
11. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the soft-404 trap, the sitemap |
| `references/pricing.md` | The full rate table, peak hours, model specifications |
| `references/rate-limits.md` | Concurrency limits and why every number stays null |
| `references/data-recipes.md` | A worked row for each of the four datasets |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
