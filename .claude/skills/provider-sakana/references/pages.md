# Sakana page inventory

Every status below was checked on 2026-08-30. Re-check before you trust one.

## The one page that carries data

| Page | Publishes | Tool |
|---|---|---|
| `https://sakana.ai/fugu/` | Plan prices, Fugu Ultra token rates, model ids, the FAQ | `WebFetch` |

`WebFetch` returns the real content. `curl -sL -A "Mozilla/5.0"` returns the
same body: HTTP 200, 164385 bytes on 2026-08-30. The page renders server side, so every number
sits in the HTML source. You do not need a JavaScript bundle and you do not need
a headless browser.

## Probe results

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://sakana.ai/fugu/` | 200 | 164385 B | `WebFetch`, `curl -sL -A "Mozilla/5.0"` | The source for every Sakana value. |
| `https://docs.sakana.ai/` | no DNS | — | `curl` | Does not resolve. No docs host exists. |
| `https://sakana.ai/fugu/index.md` | 404 | 2271 B | `curl` | No `.md` twin. |
| `https://sakana.ai/llms.txt` | 404 | 2271 B | `curl` | No `llms.txt`. |
| `https://sakana.ai/sitemap.xml` | 404 | 2271 B | `curl` | No sitemap. |
| `https://console.sakana.ai/` | 200 | ~64 KB | `curl` | Redirects to `/login`. Login-gated SPA. No public price or quota. |
| `https://console.sakana.ai/<unknown path>` | 404 | ~42 KB shell | `curl` | Returns the app shell. |
| `https://chat.sakana.ai/` | 200 | ~46 KB | `curl` | Sakana Chat, a Japanese consumer chat product on the Namazu model. Login-gated. No Fugu price, rate, or quota. |

`sakana.ai` returns a real 404 with the correct HTTP status and a 2271-byte
body. It does not serve soft 404s, unlike `api-docs.deepseek.com`. A 200 from
this host means the page exists.

## Values the Fugu page states

Subscription plans, monthly term only. The page publishes no quarterly and no
yearly price.

| Plan | Price per month | Allowance |
|---|---|---|
| Standard | $20 | Baseline allowance, lightweight daily usage |
| Pro | $100 | 10x Standard usage |
| Max | $200 | 20x Standard usage |

Every tier includes both Fugu and Fugu Ultra.

Token plan, Fugu Ultra. Rates are per 1M tokens.

| Context | Input | Output | Cached input |
|---|---|---|---|
| At or below 272K | $5 | $30 | $0.50 |
| Above 272K | $10 | $45 | $1.00 |

No cache-write rate is published. Model ids are `fugu-ultra-v1.1` and
`fugu-ultra-v1.0`. The page names `fugu-ultra-20260615` as the former id, in a
sentence that misspells "previously" as "previouly".

Token plan, Fugu base. The page states no fixed rate. It says usage is billed
"at a single rate based on the top tier model involved".

Fugu Cyber. Contact sales. No public price. The page says "Please contact our
sales team for details on Fugu Cyber usage and pricing."

The page states every figure twice over. The pricing card carries them, then FAQ
answer Q5 restates them in prose: "Standard ($20/month)", "Pro ($100/month)
provides 10x the usage of Standard", "Max ($200/month) provides 20x the usage of
Standard", and "priced per 1M tokens at $5 input, $30 output, and $0.50 cached
input, with higher rates ($10 / $45 / $1.00) for contexts above 272K tokens".
The two statements agree on every number. They disagree on the model id: the FAQ
still writes `fugu-ultra-20260615`, while the pricing card names
`fugu-ultra-v1.1` and `fugu-ultra-v1.0`. Trust the card.

## What the page does not say

- No rate limit. No requests per minute, no tokens per minute, no concurrency.
- No parameter count, no context window, no max output, no vision claim.
- No JPY price. The Japanese half of the page repeats the same USD figures.
- No quarterly price and no yearly price. The word "annual" does not appear.
- No cache-write rate. The card lists input, output, and cached input only.
- No absolute quota for any subscription tier. Pro and Max are stated only as
  multiples of Standard, and Standard carries no number.

The Token Plan card says consumption-based tokens "are served at higher priority
than monthly-plan tokens". That is a scheduling claim, not a quota. It gives you
no number for `data/rate_limits.yaml`.

## Outbound links found on the Fugu page

| Link | Owner | Citable |
|---|---|---|
| `https://sakana.ai/...` other Sakana pages | Sakana | Yes. Rule 4 accepts a page the provider owns. |
| `https://console.sakana.ai/` | Sakana | Yes as `docs`, but it states no value. |
| `https://chat.sakana.ai/` | Sakana | Yes in principle. Probed on 2026-08-30 and it states no value, so do not cite it. |
| `https://models.dev/providers/sakana/` | models.dev | No. Third-party aggregator. |
| `https://openrouter.ai/sakana/fugu-ultra` | OpenRouter | No. Third-party reseller. |
| `https://vercel.com/ai-gateway/models/fugu-ultra` | Vercel | No. Third-party gateway. |
| `arXiv:2606.21228` Fugu technical report | arXiv | No. Sakana-authored, arXiv-hosted. |
| `arXiv:2512.04695` TRINITY | arXiv | No. Same reason. |
| `arXiv:2512.04388` Conductor | arXiv | No. Same reason. |

`AGENTS.md` rule 4 asks who owns the host, not who wrote the text. A
Sakana-authored paper on arXiv is still an arXiv page. An `announcement` link
must point at `sakana.ai`.
