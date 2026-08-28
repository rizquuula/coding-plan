---
name: provider-minimax
description: How to source MiniMax (Token Plan) tiers, quotas, and rate limits for the datasets in this repository. Use when you add or refresh a MiniMax row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions MiniMax, minimax.io, Token Plan, MiniMax Code, MiniMax M3, MiniMax M2.7, Hailuo, or platform.minimax.io. Records which page holds each value, which tool reads it, and the traps that produce a wrong number — including the .md docs twins that make every value readable without a browser.
---

# MiniMax — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to MiniMax, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

**Every published price and limit is readable without a login.** The docs site
serves a Markdown twin of every page: append `.md` to any
`platform.minimax.io/docs/...` URL. The full docs index sits at
`https://platform.minimax.io/docs/llms.txt`. Start there.

## Constants

Write the provider as `MiniMax` in all four data files. The build script groups
rows by that exact string.

`price_currency` and `currency` are `USD`. The international platform prices in
dollars.

`region` is `china`. This repository classifies a provider by its parent
company, and MiniMax is a Chinese company. `platform.minimax.io` is the
international platform, but the Zhipu, Alibaba, Moonshot, and BytePlus rows all
carry `china` on the same rule.

The Token Plan is MiniMax's coding subscription. The route
`/subscribe/coding-plan` redirects to `/subscribe/token-plan` — they are one
product. The public tiers are Plus, Max, and Ultra. MiniMax Code is the official
agent; the plan also works in Claude Code, Cline, and other OpenAI-compatible
tools through an `sk-cp` Subscription Key. Legacy tiers Starter ($10) and
Plus-hs ($40) remain for existing subscribers only, and Max-hs ($80) and
Ultra-hs ($150) are retired — see the migration doc before you touch a legacy
row.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Tier prices, agent usage, quota windows, model coverage | `https://platform.minimax.io/docs/guides/pricing-token-plan.md` | `curl` or `WebFetch` |
| Comparison table: per-model call estimates, agent concurrency, video quotas | `GET https://api.minimax.io/setting/get_app_settings?fe_setting_key=code_plan_landing` | `curl` |
| Team seat rules | `https://platform.minimax.io/docs/guides/pricing-token-plan-team.md` | `curl` |
| Migration rules, legacy tier prices, Ultra monthly capacity | `https://platform.minimax.io/docs/token-plan/migration.md` | `curl` |
| Per-model API rate limits | `https://platform.minimax.io/docs/guides/rate-limits.md` | `curl` |
| Every docs page URL | `https://platform.minimax.io/docs/llms.txt` | `curl` |
| Tier cards as a human sees them | `https://platform.minimax.io/subscribe/token-plan` | browser only — see trap 1 |
| The 22 Token Plan FAQ answers | `/_next/data/<buildId>/en/subscribe/token-plan.json` | `curl` — see trap 5 |

Probe results for every URL sit in `references/pages.md`.

## Eleven things that produce a wrong number

**1. The subscribe page is a Next.js shell.** `WebFetch` on
`https://platform.minimax.io/subscribe/token-plan` returns only the page title.
The prices are not in the HTML and not in the JS bundles; the tier cards load
from an API that needs a login. The docs pricing page is the anonymous source.
Keep the `plans` link pointing at the subscribe page anyway, because a human
reader's browser renders it.

**2. No page prints the yearly total — derive it and state the derivation.**
The cycle toggle publishes the discount ("Save 2 months with yearly plan"),
and the docs pricing page publishes the monthly rate. Write the yearly
`amount` as the monthly rate times 10, and say so in `notes`, per the
AGENTS.md rule on discounted rates. The migration doc quotes annual plans at
a monthly rate ("Ultra-hs $150/month annual plan"), which confirms MiniMax
prices yearly terms this way.

**3. The public products API never returns the Token Plan.**
`GET https://api.minimax.io/public/api/openplatform/charge/combo/products`
answers anonymous calls, but it serves audio and media resource packs only. It
returns `"GetResourcePkgCard failed"` with every parameter combination tried.
Do not burn time on it.

**4. The quota is usage-based, with no published numbers.** Included usage sits
in a 5-hour rolling window and a weekly window. MiniMax publishes no token or
request count for either window. "3-4 agents" is the published capacity
statement — copy it as written and never invent a request count.

**5. The `_next/data` build id changes on every deploy.** The FAQ JSON at
`/_next/data/<buildId>/en/subscribe/token-plan.json` holds 22 FAQ answers and
the page i18n, but no prices. Read the current build id from the
`_buildManifest.js` script URL in the page HTML first. On 2026-08-28 the id was
`Abwp9rFspSH47uXEKl3cs`.

**6. Credits are a top-up, not a tier.** 1,000 credits cost $1, packs sell at
$5, $25, and $100, and each purchase is valid 365 days. Credits cover overflow
beyond the plan quota. Never add a plans row for a credits pack.

**7. The plan excludes some models.** Coverage is the full MiniMax lineup — M3,
M2.7, image, speech — but MiniMax H3 (video), voice design, and rapid voice
cloning are excluded. The pricing doc states this under the tier table.

**8. API rate limits are not plan quotas.** The rate-limits doc publishes
per-model RPM and TPM for the pay-as-you-go API (M3: 200 RPM, 10,000,000 TPM;
M2.x: 500 RPM, 20,000,000 TPM). Those are account limits on the open platform.
Never present them as Token Plan quotas, and never present plan quotas as rate
limits.

**9. Hidden tiers exist in the frontend enum.** The bundle defines
CodePlanStarter (24), Plus (25), Max (26), TrialCodePlan (28), and four High
Speed variants (101001-101004). Only Plus, Max, and Ultra are publicly sold —
the FAQ says so. Do not add rows for enum-only tiers.

**10. The landing config endpoint is the anonymous source for the comparison
table.** `GET https://api.minimax.io/setting/get_app_settings?fe_setting_key=code_plan_landing`
answers anonymous calls with ~72 KB of JSON. `data.en.comparison.rows` holds
the "Which plan fits you?" table: M3 monthly call estimates, M2.7 and
M2.7-highspeed calls per 5-hour window, OpenClaw Agent concurrency, and video
generations per day. `data.en.serviceNotice` holds service notices, and
`data.en.apiPricing` holds the pay-as-you-go teaser rates. The call estimates
carry a stated assumption — about 50K tokens per M3 call — so copy the
assumption together with the number.

**11. Two MiniMax pages disagree on the tier prices.** The landing config's
comparison section states $20, $50, and $120 per month. The docs pricing page
states $22, $55, and $132. The tier-card purchase API needs a login, so an
anonymous agent cannot see the charged amount. This repository keeps the docs
prices. The migration doc repeats $20, $50, and $120 as contracted prices for
existing subscribers, and each docs-page figure is exactly 10% higher. The
docs pricing page stays the source for new-subscriber rows. Re-check both
sources on every refresh, and update this trap when they converge.

## Workflow

`data/plans.yaml` holds a `minimax-plus`, a `minimax-max`, and a
`minimax-ultra` row. A refresh updates those three rows. It does not create
them.

1. Fetch `https://platform.minimax.io/docs/guides/pricing-token-plan.md`.
2. Copy each monthly price into `prices` as the `month` amount.
3. Copy the agent-usage and quota-window statements into `limits`.
4. Copy the model coverage and the exclusions from the note under the table.
5. Fetch the landing config endpoint (trap 10) and copy the comparison rows
   into `limits`: M3 calls per month, M2.7 calls per window, agent
   concurrency, and video generations per day.
6. For rate-limit rows, fetch `rate-limits.md` and copy the RPM and TPM
   columns as plain integers.
7. Set `last_verified` to the date you read the pages, on every row you touch.
8. Run `python build.py --check` and fix every error it prints.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, the verified prices, quotas, and rate limits |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
