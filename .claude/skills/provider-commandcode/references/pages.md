# CommandCode page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## The pages that carry data

| Page | Publishes | Tool |
|---|---|---|
| `https://commandcode.ai/pricing` | Plan prices, credits, request estimates, dated deals | `WebFetch` |
| `https://commandcode.ai/docs/resources/pricing-limits` | Full pricing detail and usage estimates | `WebFetch` |
| `https://commandcode.ai/docs/plans/goat` | Per-model allowances on the GOAT plan | `WebFetch` |

Every page renders server side, so every number sits in the HTML source. You do
not need a JavaScript bundle and you do not need a headless browser.

## Probe results

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://commandcode.ai/pricing` | 200 | ~313 KB | `WebFetch`, `curl -sL -A "Mozilla/5.0"` | The source for every plan value. |
| `https://commandcode.ai/docs/resources/pricing-limits` | 200 | ~633 KB | `WebFetch` | Pricing detail. States no numeric rate limit. |
| `https://commandcode.ai/docs/plans/goat` | 200 | ~582 KB | `WebFetch` | GOAT per-model allowances. |
| `https://commandcode.ai/docs/taste` | 200 | ~484 KB | `WebFetch` | taste-1 docs. Content unchecked. |
| `https://commandcode.ai/sitemap.xml` | 200 | ~15 KB | `curl` | Real `application/xml`. About 44 model slugs. |
| `https://commandcode.ai/models` | unchecked | — | — | Model index. Not probed. |
| `https://commandcode.ai/models/<slug>` | unchecked | — | — | Per-model cards. Not probed. Candidate source for resale rates. |
| `https://commandcode.ai/pricing.md` | 200 | ~36 KB shell | `curl` | Soft 404. No `.md` twin exists. |
| `https://commandcode.ai/llms.txt` | 200 | ~36 KB shell | `curl` | Soft 404. No `llms.txt` exists. |
| `https://commandcode.ai/docs/resources/pricing-limits.md` | 404 | ~163 KB HTML body | `curl` | Real 404 status. The docs subtree answers correctly. |

The site root serves soft 404s. A 200 from `commandcode.ai` does not mean the
page exists, so read the content before you trust it. The `/docs/` subtree
returns a real 404 status, but its 404 body is large HTML, not a short stub.

Model slugs seen in the sitemap include `claude-fable-5`, `fugu-ultra`,
`gpt-5-6-luna`, `glm-5-3`, and `deepseek-v4-pro`.

## Values the pricing page states

Every price is monthly. Every price adds an unstated processing fee. The page
publishes no quarterly and no yearly term.

| Plan | Price per month | Credits included | Estimated requests | Note |
|---|---|---|---|---|
| Go | $1 | $10 | ~15K | — |
| GOAT | $10 | $70 | ~75K | Per-model allowances, detail on the GOAT docs page |
| Pro | $20 | $80 | ~100K | — |
| Max 10× | $100 | $150 | ~219K | Rate limits described as "Higher" |
| Max 20× | $200 | $300 | ~437K | Rate limits described as "Highest" |
| Teams | $40 | Pooled | ~35K | "One team. One bucket." Per seat or per team is not stated |
| Provider | $15 | Pay as you go at model cost | — | Zero markup, OpenAI- and Anthropic-compatible endpoints |
| Enterprise | Custom | — | — | Contact sales. No number |

GOAT per-model allowances named on the pricing page: $70 on GPT-5.6 Sol, $70 on
GLM-5.2, $70 on Hy3. The GOAT docs page holds the full list.

Provider plan top-ups roll over and never expire.

Every plan includes taste-1 access, an "Up to 1M" context claim, credits that
roll over indefinitely, and auto top-up at API cost.

## Dated deals on the pricing page

| Model | Deal | Ends |
|---|---|---|
| Gemini 3.7 Flash | 50% off | 2026-12-31 |
| Qwen 3.7 Max | 2× credits | 2026-06-22 |
| Ling 3.0 Flash | Free | 2026-08-02 |
| MiniMax M3 | Free | 2026-09-05 |
| MiniMax M2.7 | Free | 2026-09-05 |
| Laguna S 2.1 | Free | While capacity lasts |

The Ling 3.0 Flash deal still showed on 2026-08-28, after its end date. The page
keeps expired deals. Never bake a deal into a rate.

## What the pages do not say

- No numeric rate limit. No per-minute limit, no RPM, no concurrency number.
  Checked by grep across `/docs/resources/pricing-limits`.
- No per-token rate on `/pricing`. The plan page prices credits, not tokens.
- No verified taste-1 specification. `https://commandcode.ai/docs/taste` was not
  probed, so no parameter count, context window, max output, or vision claim is
  confirmed.
- No processing fee amount.

## Outbound links found on the site

| Link | Owner | Citable |
|---|---|---|
| `https://commandcode.ai/...` other pages | Command Code AI | Yes. Rule 4 accepts a page the provider owns. |
| `https://github.com/CommandCodeAI` | GitHub | No. Third-party host. |
| `https://x.com/CommandCodeAI` | X | No. Third-party host. |
| LinkedIn company page | LinkedIn | No. Third-party host. |
| Discord invite | Discord | No. Third-party host. |
| Support `mailto:` address | — | No. Not a page. |

`AGENTS.md` rule 4 asks who owns the host, not who wrote the text. A
CommandCode-authored post on GitHub or X is still a third-party page.
