# Z.ai page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## Pages that carry data this repository needs

| Page | Publishes | Tool |
|---|---|---|
| `https://z.ai/subscribe` | Plan prices, billing terms, discount labels | `scripts/read_subscribe.py` |
| `https://docs.z.ai/devpack/overview` | Individual tier quotas, models, tool support | `WebFetch` |
| `https://docs.z.ai/devpack/teamplan` | Team seat quotas | `WebFetch` |
| `https://docs.z.ai/guides/overview/pricing` | API rates per token, every model | `WebFetch` |
| `https://docs.z.ai/guides/overview/overview.md` | The model matrix: every model, its context window, its guide link | `curl` or `WebFetch` |
| `https://docs.z.ai/api-reference/llm/chat-completion.md` | `max_output` per model family, and every `model_id` | `curl` or `WebFetch` |
| `https://docs.z.ai/guides/llm/<model>` | One text model's specification | `WebFetch` |
| `https://docs.z.ai/guides/vlm/<model>` | One vision model's specification | `WebFetch` |
| `https://docs.z.ai/devpack/usage-policy` | Concurrency ranking, no numbers | `WebFetch` |
| `https://api.z.ai/api/biz/overseas/team/subscribe/product/public_pricing` | Team seat prices | `curl` |

The model matrix is the entry point for `data/models.yaml`. Do not start at one
model's guide page. Details in `models.md`.

## The Team pricing API

That last row is a public JSON endpoint. It needs no auth and returned 200 on
2026-08-28.

```bash
curl -s https://api.z.ai/api/biz/overseas/team/subscribe/product/public_pricing
```

It returns `data.productList`, a list of ten entries. Each entry carries `tier`,
`subscribeMode`, `subscribePeriod`, `payAmount`, `renewAmount`, `purchasable`,
and `renewable`.

**Four entries are `purchasable: false`. Filter on `purchasable: true` before
you copy any amount.** The full table and the reasoning sit in `pricing.md`.

**It publishes Team seat prices, not the Individual GLM Coding Plan.** Never
copy a Team figure into an Individual row, and never copy an Individual figure
into a Team row.

The base URL for every `/biz/...` path is `https://api.z.ai/api`.

## The docs index

`https://docs.z.ai/llms.txt` lists every documentation URL on the site. Read it
first when a page you expect is missing. It is how `devpack/teamplan` and
`guides/llm/glm-5.3` were found, neither of which is linked from the pages above.

Every docs page also serves a markdown twin. Append `.md` to the path:

    https://docs.z.ai/devpack/overview  ->  https://docs.z.ai/devpack/overview.md

The `.md` form returns clean markdown and is easier to read. It does **not**
bypass a redirect. See the dead ends below.

## Redirects that are not dead ends

`https://docs.z.ai/guides/llm/glm-5.3-flash` returns 308 to
`https://docs.z.ai/guides/vlm/glm-5.3-flash`. The `.md` twin returns 307 to the
same place. Z.ai classifies GLM-5.3-Flash as a native multimodal model, so its
guide sits under `vlm/`. Follow the redirect. Cite the `vlm/` URL.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://docs.z.ai/guides/overview/rate-limits` | 404 |
| `https://docs.z.ai/api-reference/rate-limit` | 307 to `https://z.ai/manage-apikey/rate-limits` |
| `https://docs.z.ai/api-reference/rate-limit.md` | Same 307. The `.md` twin does not help. |
| `https://z.ai/manage-apikey/rate-limits` | Needs a login. Never cite it. |
| `https://api.z.ai/api/biz/model/rate-limit` | Returns `{"code":1001,"msg":"Authentication parameter not received in Header..."}`. Needs a login. |
| `https://api.z.ai/api/biz/customer/rate-limit` | Same code 1001. Needs a login. |
| `https://api.z.ai/api/biz/pay/coding-plan/batch-preview` | POST returns the same code 1001. Needs a login. |

`/biz/model/rate-limit` is the endpoint the console rate-limit page calls. It is
the only source of a per-model API limit, and it is behind an account. That is
why `data/rate_limits.yaml` holds no Zhipu row. Read `quotas.md` for what the
page would show.

## What each page does not say

- `devpack/overview` prints "Starting at just 18 USD per month" and no other
  price. One figure is not enough to fill a row.
- `guides/overview/pricing` publishes no context window and no maximum output.
  Read the model matrix and `chat-completion.md` for those.
- The model matrix publishes a context window and no maximum output.
- `devpack/teamplan` publishes seat quotas and no price at all.
- `devpack/usage-policy` ranks concurrency as `Max > Pro > Lite` and prints no
  number.
- No page publishes a speed figure. See `quotas.md`.
- No page links model weights or names a licence. See `models.md`.

## Citation rule

`AGENTS.md` requires a page the provider owns. `z.ai` and `docs.z.ai` both
qualify. A login-gated console page does not qualify, because no reader can
open it to check your figure.
