# Kiro page inventory

Every status below was checked on 2026-08-30. Re-check before you trust one.

## The pages that carry data

| Page | Publishes | Tool |
|---|---|---|
| `https://kiro.dev/pricing/` | Five tier prices, credits, add-on price, GovCloud uplift, metering, reset rule | `WebFetch`, `curl -sL` |
| `https://kiro.dev/docs/billing.md` | Credit allowance per tier, proration, credit reset | `curl -sL` |
| `https://kiro.dev/docs/models.md` | Per-tier model matrix, context window, credit multiplier | `curl -sL` |
| `https://kiro.dev/docs/models/available-models.md` | Which models are open weight, per-model descriptions | `curl -sL` |
| `https://kiro.dev/docs/billing/add-on-credits.md` | $0.04 per credit, pack limits, 12-month expiry | `curl -sL` |
| `https://kiro.dev/docs/enterprise/billing.md` | Enterprise tier structure, overage opt-in | `curl -sL` |
| `https://kiro.dev/llms.txt` | The full docs page index | `curl -sL` |

Every page renders server side. Every number sits in the HTML or the Markdown
source. You do not need a JavaScript bundle and you do not need a headless
browser.

## Probe results

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://kiro.dev/pricing/` | 200 | 185047 B | `WebFetch`, `curl -sL -A "Mozilla/5.0"` | The source for every price. FAQ answers are in the HTML. |
| `https://kiro.dev/llms.txt` | 200 | 45291 B | `curl -sL` | Index of every docs page, with a one-line summary each. Start here. |
| `https://kiro.dev/sitemap.xml` | 200 | 471916 B | `curl -sL` | 1980 URLs. Mostly blog and changelog. No rate-limit page. |
| `https://kiro.dev/robots.txt` | 200 | 910 B | `curl -sL` | Present. Not needed for sourcing. |
| `https://kiro.dev/docs/models.md` | 200 | 11134 B | `curl -sL` | The model access matrix. |
| `https://kiro.dev/docs/models/available-models.md` | 200 | 14300 B | `curl -sL` | Per-model prose. Names the open weight models. |
| `https://kiro.dev/docs/billing.md` | 200 | 3563 B | `curl -sL` | Credit table. Points at the pricing page for the prices. |
| `https://kiro.dev/docs/billing/add-on-credits.md` | 200 | 2494 B | `curl -sL` | Add-on credit rules. |
| `https://kiro.dev/docs/enterprise/billing.md` | 200 | 4018 B | `curl -sL` | Enterprise tiers. No separate price list. |
| `https://kiro.dev/docs/billing/related-questions.md` | 200 | — | `curl -sL` | Billing FAQ. Repeats the credit definition. No quota number. |
| `https://kiro.dev/docs/` | 200 | 235590 B | `curl -sL` | Docs landing page. |
| `https://docs.kiro.dev/` | 200 | 235590 B | `curl -sL` | Redirects to `kiro.dev/docs/`. Same body. Not a separate host. |
| `https://kiro.dev/changelog/` | 200 | 289975 B | `curl -sL` | Product changelog. Not probed for values. |
| `https://app.kiro.dev/account/usage` | 200 | 3894 B | `curl -sL` | Login-gated app shell. No public price or quota. |
| `https://kiro.dev/pricing.md` | 404 | 96928 B | `curl -sL` | No `.md` twin outside `/docs/`. |
| `https://kiro.dev/pricing/index.md` | 404 | 96928 B | `curl -sL` | Same. |
| `https://kiro.dev/docs/models/index.md` | 404 | 96928 B | `curl -sL` | The twin is `models.md`, not `models/index.md`. |
| `https://kiro.dev/docs/nonexistent-page-xyz.md` | 404 | 96928 B | `curl -sL` | Control probe. Every 404 returns the same 96928-byte body. |

The 404 body is about 97 KB, so size never tells you whether a page exists.
Read the status code. `kiro.dev` returns a correct 404 status, so a 200 from
this host means the page exists.

## Fetches that failed

| URL | What happened |
|---|---|
| `https://kiro.dev/pricing.md` | 404. The Markdown twin convention applies only under `/docs/`. |
| `https://kiro.dev/pricing/index.md` | 404. Same reason. |
| `https://kiro.dev/docs/models/index.md` | 404. The twin for `/docs/models` is `/docs/models.md`. |

No fetch failed for a network reason. No page needed a browser.

## Values the pricing page states

Subscription tiers, monthly term only. The page publishes no quarterly and no
yearly price.

| Tier | Price | Credits per month | Model access |
|---|---|---|---|
| Kiro Free | $0 per month | 50 | Open weight models and Claude Sonnet 4.5. No add-on credits. |
| Kiro Pro | $20 per user / month | 1,000 | Premium models. Add-on credits at $0.04/credit. |
| Kiro Pro+ | $40 per user / month | 2,000 | Premium models. Add-on credits at $0.04/credit. |
| Kiro Pro Max | $100 per user / month | 5,000 | Premium models. Add-on credits at $0.04/credit. |
| Kiro Power | $200 per user / month | 10,000 | Premium models. Add-on credits at $0.04/credit. |

Enterprise: "Centralized billing, SSO, usage analytics, and enterprise security
controls." Contact sales. No price.

Other statements on the page:

- "Credits are metered to the second decimal point, so the least number of
  credits a task can consume is 0.01 credits."
- "Usage limits reset at the start of each billing month. Unused credits do not
  roll over to the next month."
- "Kiro pricing in AWS GovCloud (US) Regions is approximately 20% higher than
  standard commercial region pricing." No dollar figure.
- "The Free tier is not available in the AWS GovCloud (US) Regions."
- "Kiro processes paid subscriptions on the 1st day of each calendar month."
- New users get a $20 credit toward the first paid subscription.
- Free tier access "is subject to rate limits". No number.

## Values the add-on credit page states

- $0.04 per credit, on Pro, Pro+, Pro Max, and Power only.
- Minimum purchase $5 (125 credits). Maximum per pack $100. Up to 5 packs.
- Add-on credits roll over month to month and expire 12 months after purchase.
- Plan credits are consumed first. The earliest-expiring pack goes next.

## Values the models page states

Free column of the quick-comparison table, eight models:

| Model | Context | Credit multiplier |
|---|---|---|
| Claude Sonnet 4.5 | 200K | 1.3x |
| Claude Sonnet 4.0 | 200K | 1.3x |
| Auto | — | 1.0x |
| DeepSeek 3.2 | 128K | 0.25x |
| MiniMax M2.5 | 200K | 0.25x |
| GLM-5 | 200K | 0.5x |
| MiniMax M2.1 | 200K | 0.15x |
| Qwen3 Coder Next | 256K | 0.05x |

Paid tiers unlock all of the above plus eleven more. Pro, Pro+, Pro Max, and
Power carry the same model access. Only the credit allowance differs.

| Model | Context | Credit multiplier |
|---|---|---|
| GPT-5.6 Sol | 272K | 2.4x |
| GPT-5.6 Terra | 272K | 1.0x |
| GPT-5.6 Luna | 272K | 0.1x |
| Claude Opus 5 | 1M | 2.2x |
| Claude Opus 4.8 | 1M | 2.2x |
| Claude Opus 4.7 | 1M | 2.2x |
| Claude Opus 4.6 | 1M | 2.2x |
| Claude Opus 4.5 | 200K | 2.2x |
| Claude Sonnet 5 | 1M | 1.3x |
| Claude Sonnet 4.6 | 1M | 1.3x |
| Claude Haiku 4.5 | 200K | 0.4x |

`docs/models/available-models.md` calls MiniMax M2.5, GLM-5, DeepSeek 3.2,
MiniMax M2.1, and Qwen3 Coder Next "Open weight model". It makes no
open-weight or closed-weight claim about the GPT-5.6 or Claude models.

Cost is relative to Auto at 1.0x. The page warns that two models with the same
multiplier can still consume different credit counts, because tokenizers and
thinking depth differ.

## What no Kiro page says

- No price per 1M tokens for any model.
- No requests per minute, no tokens per minute, no concurrency limit.
- No parameter count, no max output, and no vision claim for any model.
- No yearly or quarterly subscription price.
- No GovCloud dollar figure, only "approximately 20% higher".

## Outbound links found on the Kiro pages

| Link | Owner | Citable |
|---|---|---|
| `https://kiro.dev/...` | Kiro | Yes. Rule 4 accepts a page the provider owns. |
| `https://app.kiro.dev/account/usage` | Kiro | Yes in principle, but it is login-gated and states no value. |
| `https://docs.aws.amazon.com/...` | AWS | Kiro is an AWS product, but the host is `amazon.com`. Prefer a `kiro.dev` page. |
| `https://www.minimax.io/news/minimax-m25` | MiniMax | No for a Kiro row. Cite it only on a MiniMax row. |
| `https://z.ai/blog/glm-5` | Zhipu | Same. |
| `https://api-docs.deepseek.com/news/news250325` | DeepSeek | Same. |
| `https://qwenlm.github.io/blog/qwen3-coder/` | Alibaba on GitHub Pages | No. Third-party host. |
| `https://platform.openai.com/docs/supported-countries` | OpenAI | No for a Kiro row. |
| `https://www.anthropic.com/supported-countries` | Anthropic | No for a Kiro row. |

`AGENTS.md` rule 4 asks who owns the host. A model page that Kiro links to is
still that model provider's page, not Kiro's.
