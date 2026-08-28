# DeepSeek page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## Pages that carry data this repository needs

| Page | Publishes | Tool |
|---|---|---|
| `https://api-docs.deepseek.com/quick_start/pricing` | API rates, context length, max output, model version, concurrency | `WebFetch` |
| `https://api-docs.deepseek.com/quick_start/rate_limit` | Concurrency limit per model, `user_id` isolation | `WebFetch` |
| `https://www.deepseek.com/en/news/v4-preview/` | Parameter counts, open weights, 1M context | `WebFetch` |
| `https://api-docs.deepseek.com/news/news260813` | V4-Pro launch, the peak and off-peak pricing change | `WebFetch` |
| `https://api-docs.deepseek.com/news/news260821` | V4-Flash-Vision-Exp launch, image token billing | `WebFetch` |
| `https://api-docs.deepseek.com/sitemap.xml` | Every docs URL | `curl` |

`WebFetch` returned the real content for each page above. `curl` on the HTML
also works, because the site renders server side. The pricing numbers sit in the
HTML source, so you do not need a JavaScript bundle.

## The soft 404

`api-docs.deepseek.com` runs Docusaurus v3.1.0. It answers an unknown path with
**HTTP 200 and the site home page**, not with a 404. The body is 46100 bytes and
its title is `Your First API Call | DeepSeek API Docs`.

Every one of these returned that same body:

| URL | What you get |
|---|---|
| `https://api-docs.deepseek.com/quick_start/pricing.md` | 200, home page. No `.md` twin exists. |
| `https://api-docs.deepseek.com/quick_start/rate_limit.md` | 200, home page. |
| `https://api-docs.deepseek.com/llms.txt` | 200, home page. No `llms.txt` exists. |
| `https://api-docs.deepseek.com/llms-full.txt` | 200, home page. |
| `https://api-docs.deepseek.com/en/quick_start/pricing` | 200, home page. English needs no prefix. |
| `https://api-docs.deepseek.com/this_page_does_not_exist_xyz` | 200, home page. |

Two consequences:

1. A 200 from this host proves nothing. Check the page title or the body length.
   46100 bytes means you fetched the home page.
2. The `.md` twin trick that works on `docs.z.ai` does not work here. Do not
   spend time on it.

Use `https://api-docs.deepseek.com/sitemap.xml` to find a page. It lists every
real URL and it returns `application/xml`.

## Language paths

English is the default and takes no prefix. Chinese takes `/zh-cn/`.

    https://api-docs.deepseek.com/quick_start/pricing         USD
    https://api-docs.deepseek.com/zh-cn/quick_start/pricing   CNY

`https://www.deepseek.com/` links to the **Chinese** docs in its footer and
navigation. Do not follow those links into a data row. See `pricing.md`.

`www.deepseek.com` inverts the rule: `/news/v4-preview/` is Chinese and
`/en/news/v4-preview/` is English. The English page states more.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://platform.deepseek.com/` | 403 to `curl` and to `WebFetch`. |
| `https://platform.deepseek.com/api_docs/pricing` | 403. |
| `https://api.deepseek.com/models` | 401. Needs an API key. |
| `https://api-docs.deepseek.com/faq` | A redirect stub, 10715 bytes. It holds no data. |

The console at `platform.deepseek.com` blocks every unauthenticated read. Never
cite it. `AGENTS.md` rule 4 needs a page a reader can open.

## What each page does not say

- The pricing page prints no parameter count and no license.
- The rate-limit page prints no requests per minute and no tokens per minute.
- `https://www.deepseek.com/` prints no price and no plan.
- `https://www.deepseek.com/harness/` describes the agent framework and prints
  no price and no quota.
- `https://www.deepseek.com/news/v4-preview/`, the Chinese one, prints no
  parameter count.

## Citation rule

`AGENTS.md` requires a page the provider owns. `www.deepseek.com` and
`api-docs.deepseek.com` both qualify. The Hugging Face and arXiv links on the
launch page do not: DeepSeek does not own those hosts. Take the parameter counts
from the DeepSeek page that states them, and link that page.
