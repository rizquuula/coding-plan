# ClinePass page inventory

Every status below was checked on 2026-08-30. Re-check before you trust one.

## The two pages that carry data

| Page | Publishes | Tool |
|---|---|---|
| `https://docs.cline.bot/getting-started/clinepass` | Recurring price, quota multiplier, three usage windows, 13 models with ids, per-model reference rates | `curl -sL` on the `.md` twin |
| `https://cline.bot/cline-pass` | The promotional first-month price, the six labs, the FAQ | `WebFetch` |

Both pages render server side, so every number sits in the source. You do not
need a JavaScript bundle and you do not need a headless browser.

## Probe results

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://cline.bot/cline-pass` | 200 | 90322 B | `WebFetch`, `curl -sL -A "Mozilla/5.0"` | The only page that states the $4.99 promotion. |
| `https://docs.cline.bot/getting-started/clinepass` | 200 | 296284 B | `curl -sL` | Full HTML. Prefer the `.md` twin below. |
| `https://docs.cline.bot/getting-started/clinepass.md` | 200 | 7360 B | `curl -sL` | Clean Markdown twin. The best source for every ClinePass value. |
| `https://docs.cline.bot/llms-full.txt` | 200 | 654219 B | `curl -sL` | Every docs page in one file. One fetch replaces a crawl. |
| `https://docs.cline.bot/llms.txt` | 200 | 18580 B | `curl -sL` | Docs page index. Useful to find a path. |
| `https://cline.bot/llms.txt` | 200 | 5090 B | `curl -sL` | Marketing index, stale. Stamped `Last-Updated: 2025-07-16`. Names no ClinePass page. |
| `https://cline.bot/sitemap.xml` | 200 | 23710 B | `curl -sL` | Lists `/cline-pass`, the model pages, and the real blog slugs. |
| `https://docs.cline.bot/sitemap.xml` | 200 | 15462 B | `curl -sL` | Lists `/getting-started/clinepass`. |
| `https://cline.bot/blog/clinepass-best-of-value-for-open-weight-models` | 200 | 104651 B | `curl -sL` | The launch note, dated June 29, 2026. States $9.99 and a $1.99 CLI offer. |
| `https://cline.bot/pricing` | 200 | 89806 B | `curl -sL` | Sells the open source tier and Enterprise. States no ClinePass number. |
| `https://cline.bot/models` | 200 | 50751 B | `curl -sL` | Model directory. Lists 11 ClinePass models. Incomplete. See trap 3. |
| `https://cline.bot/models/glm-5-2` and 15 siblings | 200 | — | `curl -sL` | State lab, family, and `Availability: open-weight`. No parameter count, no context window. |
| `https://cline.bot/faq` | 200 | 128486 B | `curl -sL` | Names ClinePass in the navigation only. No price, no quota. |
| `https://api.cline.bot/api/v1/models` | 200 | 36940 B | `curl -sL` | Public JSON, 396 models. Zero `cline-pass/` slugs. See trap 8. |
| `https://app.cline.bot/dashboard/subscription?personal=true` | 200 | 22719 B shell | `curl -sL` | Login-gated SPA shell. No public price or quota. |
| `https://cline.bot/cline-pass.md` | 404 | 34507 B | `curl -sL` | No `.md` twin on the marketing host. |
| `https://cline.bot/blog/clinepass` | 200 | 62404 B | `curl -sL` | Soft 404. HTTP 200 with a "404 not found" body. See trap 7. |

## The 404 behaviour differs by route

`cline.bot` returns a real HTTP 404 with a 34507-byte body for an unknown
top-level path. `docs.cline.bot` returns a real HTTP 404 for an unknown path.
`cline.bot/blog/<unknown>` returns HTTP 200 with a "404 not found" body of about
62 KB. Check the body of a blog fetch. Take blog URLs from the sitemap.

## Values the pages state

### Price

| Statement | Page | Wording |
|---|---|---|
| $9.99 per month | docs ClinePass | "ClinePass is a low-cost monthly subscription — **$9.99/month**" |
| $4.99 first month | `cline.bot/cline-pass` | "Limited time: $4.99 first month, then $9.99/month" |
| Processing fee | `cline.bot/cline-pass` | "*Additional processing fee may apply" |
| $1.99 through the CLI | launch blog post | "special discount for $1.99 via Cline CLI for a limited period" |

One tier only. No quarterly price and no yearly price. The cancel FAQ says
access runs to the end of the current term.

### Quota

The docs state "**2-5x the usage** on popular open coding models compared to
standard API rate". The marketing page states "quotas that offer 2-5x the usage
compared to standard API rate limits". Neither names the base.

The docs "Usage" section states three windows and no number:

- 5-hour rolling window — usage within a rolling 5-hour period
- Weekly — usage over the calendar week
- Monthly — usage over the calendar month

### Models, from the docs table

| Model | Model ID |
|---|---|
| GLM-5.3 | `cline-pass/glm-5.3` |
| GLM-5.2 | `cline-pass/glm-5.2` |
| Kimi K3 | `cline-pass/kimi-k3` |
| Kimi K2.7 Code | `cline-pass/kimi-k2.7-code` |
| Kimi K2.6 | `cline-pass/kimi-k2.6` |
| DeepSeek V4 Pro | `cline-pass/deepseek-v4-pro` |
| DeepSeek V4 Flash | `cline-pass/deepseek-v4-flash` |
| MiMo-V2.5 | `cline-pass/mimo-v2.5` |
| MiMo-V2.5-Pro | `cline-pass/mimo-v2.5-pro` |
| MiniMax M3 | `cline-pass/minimax-m3` |
| Qwen3.8 Max | `cline-pass/qwen3.8-max` |
| Qwen3.7 Max | `cline-pass/qwen3.7-max` |
| Qwen3.7 Plus | `cline-pass/qwen3.7-plus` |

Six labs: Z.ai, Moonshot AI, DeepSeek, MiniMax, MiMo, Qwen.

### Reference rates, per 1M tokens, USD

The docs head this table with "you are not charged the individual API prices
below". A subscriber pays the flat $9.99.

| Model | Input | Output | Cached read | Cache write |
|---|---|---|---|---|
| GLM-5.3 | 1.40 | 4.40 | 0.26 | none |
| GLM-5.2 | 1.40 | 4.40 | 0.26 | none |
| Kimi K3 | 3.00 | 15.00 | 0.30 | none |
| Kimi K2.7 Code | 0.95 | 4.00 | 0.19 | none |
| Kimi K2.6 | 0.95 | 4.00 | 0.16 | none |
| DeepSeek V4 Pro (peak) | 1.32 | 3.96 | 0.044 | none |
| DeepSeek V4 Pro (off-peak) | 0.66 | 1.98 | 0.022 | none |
| DeepSeek V4 Flash (peak) | 0.44 | 1.32 | 0.014 | none |
| DeepSeek V4 Flash (off-peak) | 0.22 | 0.66 | 0.007 | none |
| MiMo-V2.5 | 0.14 | 0.28 | 0.0028 | none |
| MiMo-V2.5-Pro | 1.74 | 3.48 | 0.0145 | none |
| MiniMax M3 | 0.30 | 1.20 | 0.06 | none |
| Qwen3.8 Max | 2.00 | 6.00 | 0.25 | 2.50 |
| Qwen3.7 Max | 2.50 | 7.50 | 0.50 | 3.125 |
| Qwen3.7 Plus (at or below 256K) | 0.40 | 1.60 | 0.04 | 0.50 |
| Qwen3.7 Plus (above 256K) | 1.20 | 4.80 | 0.12 | 1.50 |

The table writes `-` for every missing cache-write rate. Write `null`.

## What no Cline page says

- No requests per minute, no tokens per minute, no concurrency limit.
- No absolute number behind the 2-5x multiplier.
- No parameter count, no context window, no max output, no vision claim.
- No quarterly price and no yearly price.
- No second ClinePass tier.

## Outbound links found on the ClinePass pages

| Link | Owner | Citable |
|---|---|---|
| `https://cline.bot/...` and `https://docs.cline.bot/...` | Cline Bot Inc. | Yes. Rule 4 accepts a page the provider owns. |
| `https://app.cline.bot/dashboard/subscription?personal=true` | Cline Bot Inc. | Yes in principle. Login-gated, so it states no value. |
| `https://api.cline.bot/api/v1/models` | Cline Bot Inc. | Yes in principle. States no ClinePass value. |
| `https://api-docs.deepseek.com/quick_start/pricing/` | DeepSeek | No. DeepSeek owns that host, not Cline. It cannot back a ClinePass row. |
| `https://openrouter.ai/...` in the blog benchmark note | OpenRouter | No. Third party. |

`AGENTS.md` rule 4 asks who owns the host. The DeepSeek footnote is a real
source for a DeepSeek row, and it is not a source for a ClinePass row.
