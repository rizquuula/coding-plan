# OpenCode page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## The page that carries data

| Page | Publishes | Tool |
|---|---|---|
| `https://opencode.ai/docs/go.md` | Usage limits, per-model rates, endpoints, privacy table | `curl -sL` |

The `.md` twin returns `text/plain`, about 19 KB. It is the authoritative
source. The HTML page `https://opencode.ai/docs/go/` holds the same tables in
about 79 KB of markup. Read the `.md` twin, because a plain-text table is harder
to misread.

## Probe results

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://opencode.ai/docs/go.md` | 200 | ~19 KB | `curl -sL`, `WebFetch` | The source for every OpenCode value. |
| `https://opencode.ai/docs/go/` | 200 | ~79 KB | `WebFetch`, `curl -sL -A "Mozilla/5.0"` | Same tables as the `.md` twin, in HTML. |
| `https://opencode.ai/go` | 200 | ~45 KB | `WebFetch`, `curl -sL -A "Mozilla/5.0"` | States the $10 price. The usage chart is a trap. See trap 1. |
| `https://opencode.ai/go.md` | 404 | 5598 B | `curl` | No `.md` twin outside `/docs`. |
| `https://opencode.ai/llms.txt` | 404 | 5598 B | `curl` | No `llms.txt`. |
| `https://opencode.ai/sitemap.xml` | 200 | ~97 KB | `curl` | Real XML. Large because every page has 18 locale twins. |
| `https://opencode.ai/ja/go`, `/de/go`, `/zh/go`, and 15 more | 200 | — | `curl` | Locale twins. Same USD numbers. Read the root path. |
| `https://opencode.ai/enterprise` | 200 | ~19 KB | `curl` | Not probed for values. Unchecked. |
| `https://opencode.ai/zen` | unchecked | — | — | The console page. Not probed. |
| `https://opencode.ai/zen/go/v1/models` | unchecked | — | — | A public JSON model list named in the docs. Not probed. |

`opencode.ai` returns a real 404 with the correct HTTP status and a 5598-byte
body. It does not serve soft 404s, unlike `api-docs.deepseek.com`. A 200 from
this host means the page exists.

## Values the pages state

The plan. One tier, monthly term only.

| Plan | Price per month | Note |
|---|---|---|
| Go | $10 | Curated access to open coding models. Cancel anytime. |

The docs say the aim is to give about 6x the subscription price in usage. That
is a marketing aim, not a quota. Record nothing from it.

Sample requests per 5 hours, from the usage-limit table. The full table lists
every model.

| Model | Requests per 5 hours |
|---|---|
| Grok 4.6 | 169 |
| GPT 5.6 Luna | 2050 |
| Kimi K3 | 110 |
| GLM-5.3-Flash | 1580 |
| DeepSeek V4 Flash | 7600 |
| Muse Spark 1.2 Contributor | 45300 |

The same table states a per-week and a per-month figure for each model. The
three columns are three time windows for the one plan, not three tiers.

The price table states Input, Output, Cached Read, and Cached Write per 1M
tokens for each model. It also states a monthly included "Usage" dollar amount
per model: $15, $30, or $60.

Tiered rates. One schema field holds one rate, so record the lower tier and
state the other in `notes`.

| Model | Threshold |
|---|---|
| Grok 4.6 | At or below 200K, above 200K |
| GPT 5.6 Luna | 272K |
| Qwen3.7 Plus | 256K |
| Qwen3.6 Plus | 256K |
| DeepSeek models | Peak and off-peak |

The endpoints table states the API model ids: `grok-4.6`, `gpt-5.6-luna`,
`glm-5.3-flash`, `kimi-k3`, `deepseek-v4-pro`, and about 20 more. The config
format is `opencode-go/<model-id>`.

Muse Spark 1.2 Contributor is a special tier. It is heavily discounted in
exchange for training permission, and it is limited to some regions.

The docs also carry a privacy table, which states model training and data
retention per model.

The docs state: "Usage limits may change as we learn from early usage and
feedback." Treat any recorded quota as short-lived.

## What the pages do not say

- No parameter count and no context window for any model. Add no
  `data/models.yaml` row.
- No requests per minute, no tokens per minute, no requests per day. The quotas
  are per 5 hours, per week, and per month, so no `data/rate_limits.yaml` field
  fits. Add no row.
- No quarterly and no yearly price. The Go plan is monthly only.
- No non-USD price. The locale twins repeat the same USD figures.

## Outbound links found on the OpenCode pages

| Link | Owner | Citable |
|---|---|---|
| `https://opencode.ai/...` other OpenCode pages | Anomaly | Yes. Rule 4 accepts a page the provider owns. |
| `https://github.com/anomalyco/opencode` | GitHub | No. GitHub owns the host. |
| `https://anoma.ly` | Anomaly | Yes. Anomaly builds OpenCode. It states no price. |
| `https://x.com/opencode` | X | No. Third-party host. |
| The Meta geographic use policy link | Meta | No. Third-party host, and it states no OpenCode value. |

`AGENTS.md` rule 4 asks who owns the host, not who wrote the text. Prefer an
`opencode.ai` URL in every `links` entry.
