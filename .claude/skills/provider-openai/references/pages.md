# OpenAI page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## Pages that carry data this repository needs

| Page | Publishes | Tool | Status |
|---|---|---|---|
| `https://learn.chatgpt.com/docs/pricing` | Plan prices, plan message limits, credit rate card | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/pricing` | API rates per token, every model, four service tiers | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/models` | Index of every model page | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/models/gpt-5.6-sol` | Sol specification, rates, rate limits | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/models/gpt-5.6-terra` | Terra specification, rates, rate limits | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/models/gpt-5.6-luna` | Luna specification, rates, rate limits | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/guides/rate-limits` | Usage tier thresholds, response headers, no per-model number | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/models/gpt-oss-120b` | Open-weight specification, parameter counts, an all-zero rate-limit table | `WebFetch` | 200 |
| `https://developers.openai.com/api/docs/models/gpt-5.3-codex` | Codex specification and rates; deprecated in Codex, still served by the API | `WebFetch` | 200 |
| `https://learn.chatgpt.com/docs/models` | Which surface each model runs on, Codex deprecations, speed as icons | `WebFetch` | 200 |
| `https://learn.chatgpt.com/docs/agent-configuration/speed` | Fast mode multiplier and credit multiplier | `WebFetch` | 200 |

## The `.md` twin

Both documentation hosts serve a markdown twin of every page. Append `.md` to
the path:

    https://developers.openai.com/api/docs/pricing
    https://developers.openai.com/api/docs/pricing.md

    https://learn.chatgpt.com/docs/pricing
    https://learn.chatgpt.com/docs/pricing.md

Every page in the table above returned 200 as a `.md` twin, under plain `curl`
with a desktop `User-Agent`. Prefer the `.md` form for a wide price table. It
prints the tab headings, so you can see which service tier each table belongs
to. The rendered page hides three of the four tabs.

The `learn.chatgpt.com` twin returns raw MDX. Prices sit in component
attributes, not in prose:

    <PricingCard name="Go" price="$8" interval="/month" ... />

That form is exact and easy to grep. Do not treat the surrounding JSX as noise.

## The docs indexes

Four index files map the sites. Read one when a page you expect is missing.

| Index | Lists |
|---|---|
| `https://developers.openai.com/llms.txt` | Every documentation set across the developer site |
| `https://developers.openai.com/api/llms.txt` | The API guides index and the endpoint reference index |
| `https://learn.chatgpt.com/docs/llms.txt` | Every ChatGPT and Codex docs page, with `.md` links |
| `https://learn.chatgpt.com/docs/llms-full.txt` | One 1.7 MB markdown export of the whole ChatGPT docs set |

`https://learn.chatgpt.com/llms.txt` returns 307 to
`https://learn.chatgpt.com/docs/llms.txt`. Both work.

`https://developers.openai.com/api/docs/models.md` is the fastest way to find a
model page. It lists every model with a `.md` link and a one-line description.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://openai.com/chatgpt/pricing/` | 403. Cloudflare challenge. `curl` and `WebFetch` both fail. |
| `https://openai.com/api/pricing/` | 403. Same challenge. |
| `https://openai.com/llms.txt` | 403. Same challenge. |
| `https://chatgpt.com/pricing` | 403. Same challenge. |
| `https://chatgpt.com/plans/go` | 403. Same challenge. |
| `https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans` | 403. Same challenge. |
| `https://platform.openai.com/llms.txt` | 404 |
| `https://platform.openai.com/settings/organization/limits` | Needs a login. Never cite it. |

The 403 does not depend on the `User-Agent`. Three agents were tried: `curl/8.0`,
a desktop Safari string, and the Googlebot string. All three returned 403. The
body carries `cdn-cgi` markers and the text "Enable JavaScript", which
identifies a Cloudflare challenge. A headless browser is the only way through,
and `AGENTS.md` forbids one.

**This costs you nothing.** `learn.chatgpt.com` and `developers.openai.com`
publish every value this repository needs, and OpenAI owns both hosts.

## Redirects

| From | To | Code |
|---|---|---|
| `https://platform.openai.com/docs/pricing` | `https://developers.openai.com/api/docs/pricing` | 301 |
| `https://platform.openai.com/docs/guides/rate-limits` | `https://developers.openai.com/api/docs/guides/rate-limits` | 301 |
| `https://platform.openai.com/docs/models` | `https://developers.openai.com/api/docs/models` | 301 |
| `https://developers.openai.com/codex/pricing` | `https://learn.chatgpt.com/docs/pricing` | 308 |
| `https://developers.openai.com/codex/pricing.md` | `https://learn.chatgpt.com/docs/pricing.md` | 308 |

Follow a redirect, then write the destination URL into `links`. A reader who
opens a stale `platform.openai.com` link lands on the right page today, but the
redirect is not a promise.

`learn.chatgpt.com/docs/pricing` still links out to
`https://platform.openai.com/docs/pricing` in several places. Those links are
stale on the page itself. Do not copy one into `links`.

## What each page does not say

- `developers.openai.com/api/docs/pricing` publishes no context window and no
  max output. Read the model page for those.
- `developers.openai.com/api/docs/guides/rate-limits` publishes no per-model
  RPM or TPM. It publishes the spend that promotes an account between usage
  tiers. Read the model page for the numbers.
- The GPT-5.6 model pages publish no parameter count. Leave `total_params` and
  `active_params` as `null`. They also state nothing about the weights, so
  `open_weights` is `null`, not `false`.
- No OpenAI page publishes a generation speed in tokens per second. No OpenAI
  page publishes a concurrent-request limit. Both were searched on 2026-08-28.
- `learn.chatgpt.com/docs/pricing` publishes a monthly price for each individual
  plan tier and no yearly price. Write one `month` entry per individual plan
  record. Business is the exception: it prints both a monthly and an annual seat
  rate.
- Long-context rate limits are separate from the published table. The rate-limit
  guide states that you view them in the developer console, which needs a login.

## Citation rule

`AGENTS.md` requires a page the provider owns. `developers.openai.com` and
`learn.chatgpt.com` both qualify. `openai.com` and `chatgpt.com` also qualify,
but no agent can read them, so you cannot verify a value there. A login-gated
console page does not qualify, because no reader can open it to check your
figure.
