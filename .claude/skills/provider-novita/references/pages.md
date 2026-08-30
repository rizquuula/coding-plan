# Novita page inventory

Every status below was checked on 2026-08-30. Re-check before you trust one.

## Probe results

| URL | Status | Size | Tool that worked | Verdict |
|---|---|---|---|---|
| `https://api-server.novita.ai/v1/product/resource-pack-specs/list` | 200 | 10961 B | `curl` | **The source for every plan value.** No key. |
| `https://api-server.novita.ai/v1/product/model/list` | 200 | 289617 B | `curl` | **The source for context, max output, and T1-T5 rate limits.** No key. |
| `https://api.novita.ai/openai/v1/models` | 200 | 204267 B | `curl` | Same rates in OpenAI shape. Use to cross-check. No `quota_items`. |
| `https://novita.ai/pricing` | 200 | 1059345 B | `curl` | Server rendered. Holds `initialFullLLMModels` with every rate. Reader-facing `pricing` link. |
| `https://novita.ai/models/model-detail/zai-org-glm-5` | 200 | 136551 B | `WebFetch`, `curl` | Server rendered. States price, context, max output, description. Reader-facing `model card` link. |
| `https://novita.ai/coding-plan` | 200 | 131005 B | `curl` | The plan page. **States no price.** See "The dead ends". |
| `https://novita.ai/coding-plan.md` | 200 | 797 B | `curl` | A real `.md` twin, and it carries the marketing copy only. No tier, no price. |
| `https://novita.ai/llms.txt` | 200 | 33508 B | `curl` | Index of every docs page as a `.md` URL. No coding-plan entry. |
| `https://novita.ai/llms-full.txt` | 200 | 1447614 B | `curl` | Every docs page concatenated. Holds both Coding Plan FAQ blocks. |
| `https://novita.ai/docs/guides/LLM-FAQ.md` | 200 | 5694 B | `curl` | Quota unit, cache billing, fallback billing. |
| `https://novita.ai/docs/guides/faq.md` | 200 | 11258 B | `curl` | Says a negative balance blocks the Coding Plan. |
| `https://novita.ai/docs/guides/llm-rate-limits.md` | 200 | 5638 B | `curl` | How an account reaches T1 to T5. The table itself is client side. |
| `https://novita.ai/docs/guides/llm-billing.md` | 200 | 3497 B | `curl` | General LLM billing. No plan tier. |
| `https://novita.ai/sitemap.xml` | 200 | 806 B | `curl` | Sitemap index. `sitemap-llm-model.xml` lists every model page. |
| `https://novita.ai/_next/static/chunks/app/coding-plan/page-edeb653501b5ccc1.js` | 200 | 42191 B | `curl` | Page bundle. Holds the FAQ text. No price. Hash changes on deploy. |
| `https://novita.ai/_next/static/chunks/92111-59bbf80c0df4b349.js` | 200 | 31584 B | `curl` | Plan-list bundle. Holds the terms, the tier bullets, the saving badges, and the endpoint path. No price. Hash changes on deploy. |
| `https://novita.ai/model-api/pricing` | 308 | 15 B | `curl` | Redirects to `https://novita.ai/pricing`. Cite the target. |
| `https://docs.novita.ai/coding-plan` | 301 | 134 B | `curl` | `docs.novita.ai` is a redirect host. Everything 301s to `novita.ai/docs/...`. |
| `https://docs.novita.ai/llms.txt` | 200 after 2 hops | 361585 B | `curl -L` | **Looks like a success and is not.** It lands on `novita.ai/docs/guides/quickstart`. |
| `https://novita.ai/docs/coding-plan.md` | 404 | 4 B | `curl` | No docs page for the plan. |
| `https://api.novita.ai/v1/product/resource-pack-specs/list` | 404 | 18 B | `curl` | Wrong host. The plan API lives on `api-server`, not `api`. |
| `https://novita.ai/api/v1/product/resource-pack-specs/list` | 404 | 96252 B | `curl` | Returns the site's 404 page, 96 KB of HTML. A size check does not detect it. |

## The dead ends

`WebFetch` on `https://novita.ai/coding-plan` returns the page and answers "NO
PRICES PRESENT" when asked for a tier price. That is correct, not a fetch
failure.

`curl` on the same URL returns 131 KB. Its Next.js flight payload holds a
`modelProductPrice` map with about 200 entries. **Those are image, video, and
audio rates, not LLM rates and not plan tiers.** The payload holds no tier name,
no `quota`, no `rpm`, and no LLM token price. A grep for `$` in that HTML
returns `$22`, `$28`, `$29`, `$32`, `$17`, and `$2`, which are React server
component reference markers, not dollar amounts.

The 39 JavaScript chunks the page loads hold the layout, the FAQ text, the terms
text, and the tier bullet templates. They hold no price either. What they do
hold is the request: module 22177 in chunk `92111` defines

    function r(e,n){return (0,i.WY)({url:"/v1/product/resource-pack-specs/list",query:e,signal:n})}

and chunk `82347` defines the default base as `T="https://api-server.novita.ai"`.
That pair is how the endpoint was found.

## How the page turns the JSON into what a reader sees

| JSON field | Transform | Rendered |
|---|---|---|
| `tierList[].discountPrice` | `Decimal(v).div(1e4)` | `$19.9 monthly` |
| `tierList[].quota` | `round(v / 1e4)`, then a thousands formatter | `50,000,000 Tokens` |
| `tierList[].rpm` | none | `Performance up to 45 requests per minute` |
| `deductRules[].displayName` | de-duplicated into a list | the Model Access popover |

The saving badge is hardcoded in the bundle, not served: `{Lite: "", Pro: "17%",
Max: "33%"}`. The tier bullets are hardcoded too. Pro says "3X from lite token
usage" and Max says "15X from lite token usage", which match 150M / 50M and
750M / 50M.

## What the endpoints state

Plan tiers. Monthly term only. `billingCycle` is `cycle-based`,
`validityPeriod` is 1 month, `userBuyLimit` is 1.

| Tier | USD per month | Quota, base-rate tokens | RPM | TPM | Saving badge |
|---|---|---|---|---|---|
| Lite | 19.90 | 50,000,000 | 45 | 50,000,000 | none |
| Pro | 49.90 | 150,000,000 | 150 | 50,000,000 | 17% |
| Max | 199.90 | 750,000,000 | 450 | 50,000,000 | 33% |

The nine models the plan covers, with Novita's pay-as-you-go rate in USD per 1M
tokens.

| Model id | Display name | Input | Output | Cache read | Context | Max output |
|---|---|---|---|---|---|---|
| `zai-org/glm-5` | GLM-5 | 1 | 3.2 | 0.2 | 198K | 128K |
| `moonshotai/kimi-k2.5` | Kimi K2.5 | 0.6 | 3 | 0.1 | 256K | 256K |
| `zai-org/glm-4.7` | GLM-4.7 | 0.6 | 2.2 | 0.11 | 200K | 128K |
| `minimax/minimax-m2.1` | Minimax M2.1 | 0.3 | 1.2 | 0.03 | 200K | 128K |
| `deepseek/deepseek-v3.2` | Deepseek V3.2 | 0.269 | 0.4 | 0.1345 | 160K | 64K |
| `minimax/minimax-m2.5` | MiniMax M2.5 | 0.3 | 1.2 | 0.03 | 200K | 128K |
| `qwen/qwen3.5-397b-a17b` | Qwen3.5-397B-A17B | 0.6 | 3.6 | none | 256K | 64K |
| `minimax/minimax-m2.7` | MiniMax M2.7 | 0.3 | 1.2 | 0.06 | 200K | 128K |
| `deepseek/deepseek-v4-pro` | Deepseek V4 Pro | 1.6 | 3.2 | 0.135 | 1M | 384K |

Novita's own display names are inconsistent. It writes `Minimax M2.1` with a
lower-case m and `MiniMax M2.5` with an upper-case M. It writes `Deepseek`, not
`DeepSeek`. Copy the string Novita serves, and copy the same string into both
`data/api_pricing.yaml` and `data/models.yaml`, or the two rows do not join.

Rate limits, RPM / TPM, from `quota_items`.

| Model | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|
| GLM-5 | 30 / 2M | 100 / 6M | 1000 / 50M | 3000 / 50M | 6000 / 50M |
| Kimi K2.5 | 30 / 2M | 100 / 6M | 1000 / 50M | 3000 / 50M | 6000 / 50M |
| GLM-4.7 | 30 / 2M | 100 / 6M | 1000 / 50M | 3000 / 50M | 5000 / 50M |
| Minimax M2.1 | 30 / 2M | 100 / 6M | 1000 / 50M | 3000 / 50M | 5000 / 50M |
| Deepseek V3.2 | 30 / 2M | 100 / 6M | 300 / 50M | 500 / 50M | 3000 / 50M |
| MiniMax M2.5 | 30 / 50M | 100 / 50M | 1000 / 50M | 3000 / 50M | 6000 / 50M |
| Qwen3.5-397B-A17B | 30 / 50M | 100 / 50M | 1000 / 50M | 3000 / 50M | 6000 / 50M |
| MiniMax M2.7 | 30 / 50M | 100 / 50M | 1000 / 50M | 3000 / 50M | 6000 / 50M |
| Deepseek V4 Pro | 30 / 50M | 100 / 50M | 1000 / 50M | 3000 / 50M | 6000 / 50M |

`https://novita.ai/docs/guides/llm-rate-limits` states how an account reaches
each tier, by top-up in any of the last 3 calendar months: T1 under $50, T2 $50
to $500, T3 $500 to $3,000, T4 $3,000 to $10,000, T5 $10,000 or more.

## Sentences the terms and the docs state

From the plan page bundle, terms drawer:

- "Base Rate: DeepSeek V3.2 output price ($0.4/Mt) serves as the standard unit price."
- "Deduction Coefficients: Adjusted based on model-specific input/output value differences."
- "Deduction Amount = Actual Usage x Coefficient"
- "Validity: 1 calendar month from purchase date."
- "Auto-renewing monthly subscription." "Subscription can be canceled anytime."
- "Non-Refundable: Resource packages are non-refundable."
- "Usage of non-specified models triggers pay-as-you-go billing."
- "Package exhaustion automatically switches to real-time standard rates for the model used."

From the plan page bundle, FAQ:

- "you can share your API Key with team members, but please note that the quota is shared"
- "we recommend selecting the Max plans, which come with higher quotas suitable for team usage"
- "If your plan's quota runs out, the system will automatically switch to pay-as-you-go billing using your account balance"

From `https://novita.ai/docs/guides/LLM-FAQ`:

- "The system deducts from your Coding Plan quota first."
- "How are the 50M tokens in the Coding Plan calculated? Tokens are calculated based on base-rate equivalent token counts."
- "Cached read tokens are billed at a reduced rate, approximately 1/10th of the standard input token price."

From `https://novita.ai/docs/guides/faq`:

- "Can I use the Coding Plan with a negative account balance? No."

## What Novita does not state

- No quarterly and no yearly plan price. Monthly only.
- No parameter count for any model. `labels` says `MoE`, and Deepseek V4 Pro
  carries `> 100B`, which is a range.
- No cache-write rate. Every `cacheCreationInputTokenDecimal` is `0`.
- No per-tier price in any HTML page a reader can fetch.

## Third-party pages that are not citable

`https://openrouter.ai/provider/novita`, `https://models.dev/`, and any
comparison site. `AGENTS.md` rule 4 asks who owns the host. Only `novita.ai`,
`api.novita.ai`, and `api-server.novita.ai` qualify.
