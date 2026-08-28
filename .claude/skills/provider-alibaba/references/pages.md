# Alibaba page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

All slugs below live under one base path:

    https://www.alibabacloud.com/help/en/model-studio/

Append `.md` to any slug to get its markdown twin. Read `fetching.md` for why
the twin is the source you use.

## Pages that carry data this repository needs

| Slug | Publishes | Twin size | Tool |
|---|---|---|---|
| `model-pricing` | API rates per token, every model, every region | 376 KB | `scripts/read_tables.py` |
| `rate-limit` | RPM and TPM per model and region | 190 KB | `WebFetch` or the script |
| `text-generation-model` | Context window and tool support per model | 31 KB | `scripts/read_tables.py` |
| `coding-plan` | Coding Plan price, quota, model list | 9.5 KB | `scripts/read_tables.py` |
| `token-plan-overview` | Token Plan prices and Credit quotas | 7.8 KB | `scripts/read_tables.py` |
| `context-cache` | Cache billing rules and supported models | 60 KB | `WebFetch` |

## The two sites

Alibaba runs the same documentation twice.

| Site | Base path | Currency |
|---|---|---|
| International | `https://www.alibabacloud.com/help/en/model-studio/` | USD |
| China | `https://help.aliyun.com/zh/model-studio/` | CNY |

Both sites carry the same slugs and both serve `.md` twins. `read_tables.py`
accepts a full URL, so it reads either site.

The two sites print different numbers for the same thing:

| Value | International site | China site |
|---|---|---|
| Coding Plan Pro, per month | $50 | ¥200 |
| `qwen-max` input, Chinese mainland | $0.345 | 2.4元 |
| `qwen-max` input, International | $1.6 | 11.743元 |

**This repository sources the international site.** Cite `www.alibabacloud.com`
and write `currency: USD`. Never mix a CNY figure into a USD row.

Note the second row above. The international site prints a USD figure for the
Chinese mainland deployment too. That figure is not the CNY list price. It is a
separate published number. Read `pricing.md` before you use either one.

## Redirects that hide a stale URL

`curl` reports the redirect. `WebFetch` follows it and says nothing. So a stale
URL in `links` looks healthy until you check it with `curl`.

| URL in the repository or in a search result | Redirects to |
|---|---|
| `.../model-studio/billing-for-model-studio` | `.../model-studio/model-pricing` |
| `.../model-studio/billing-for-model-studio.md` | `.../model-studio/model-pricing.md` |
| `.../help/en/document_detail/2862577.html` | `.../model-studio/context-cache` |
| `.../help/en/document_detail/3026903.html` | `.../model-studio/text-generation-model/` |

`data/api_pricing.yaml` still cites `billing-for-model-studio`. It resolves, so
it is not broken. Replace it with `model-pricing` the next time you touch that
row.

Alibaba also publishes `document_detail/<id>.html` links inside its own pages.
Each one redirects to a slug. Resolve it and cite the slug, which is stable and
readable.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://www.alibabacloud.com/llms.txt` | 200, but the body is an HTML page, not an index |
| `.../model-studio/llms.txt` | 301 to `.../what-is-model-studio/llms.txt` |
| `.../what-is-model-studio/llms.txt` | 200 and the text `Sorry, this product does not have LLMS content yet.` |
| `https://qwen.ai/` | 200, 94 KB. `WebFetch` returns the single word `Qwen`. |
| `https://common-buy-intl.alibabacloud.com/coding-plan/` | 302 to `account.alibabacloud.com/login`. Never cite it. |
| `https://modelstudio.console.alibabacloud.com/` | 200, but the body is a login shell. Never cite it. |

**Alibaba serves no `llms.txt`.** There is no index of documentation URLs. Find
a page by its slug, or by the links inside a page you already read.

**`qwen.ai` is not a sourcing page.** It renders client-side, so `WebFetch`
returns an empty shell. Its raw HTML holds a long block of search-engine
keywords, including strings such as `qwen api pricing` and `qwen subscription`.
Those strings are keyword text, not prices. A grep for `pricing` on that host
returns keyword spam. Do not cite `qwen.ai` for any value.

## Pages that publish less than their name suggests

- `models` and its twin publish a grid of model icons that link into the
  console. No price. No context window. No parameter count. The twin is 10 KB
  and the HTML is 568 KB, and neither one holds a number. Read
  `text-generation-model` instead.
- `qwen-coder` publishes API request samples in Python, Node.js, Java, and curl.
  It publishes no price and no specification.
- The console **Models** page holds detailed model parameters. It needs a login,
  so no reader can check a figure taken from it. Never cite it.

## Pages read for status only

`https://qwenlm.github.io/blog/` answered 200 on 2026-08-28. Its content was not
read and its ownership was not confirmed. `github.io` is not an Alibaba domain,
so `AGENTS.md` rule 4 probably rules it out. Confirm ownership before you cite
it.

`https://chat.qwen.ai/` and `.../model-studio/qwen-code.md` both answered 200.
Neither was read. Neither is known to hold a value this repository needs.

## Citation rule

`AGENTS.md` requires a page the provider owns. `www.alibabacloud.com` and
`help.aliyun.com` both qualify. A login-gated console page and a purchase page
do not qualify, because no reader can open one to check your figure.
