# Z.ai page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## Pages that carry data this repository needs

| Page | Publishes | Tool |
|---|---|---|
| `https://z.ai/subscribe` | Plan prices, billing terms, discount labels | Playwright |
| `https://docs.z.ai/devpack/overview` | Individual tier quotas, models, tool support | `WebFetch` |
| `https://docs.z.ai/devpack/teamplan` | Team seat quotas | `WebFetch` |
| `https://docs.z.ai/guides/overview/pricing` | API rates per token, every model | `WebFetch` |
| `https://docs.z.ai/guides/llm/glm-5.3` | Model specification | `WebFetch` |
| `https://docs.z.ai/devpack/usage-policy` | Concurrency ranking, no numbers | `WebFetch` |

## The docs index

`https://docs.z.ai/llms.txt` lists every documentation URL on the site. Read it
first when a page you expect is missing. It is how `devpack/teamplan` and
`guides/llm/glm-5.3` were found, neither of which is linked from the pages above.

Every docs page also serves a markdown twin. Append `.md` to the path:

    https://docs.z.ai/devpack/overview  ->  https://docs.z.ai/devpack/overview.md

The `.md` form returns clean markdown and is easier to read. It does **not**
bypass a redirect. See the dead ends below.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://docs.z.ai/guides/overview/rate-limits` | 404 |
| `https://docs.z.ai/api-reference/rate-limit` | 307 to `https://z.ai/manage-apikey/rate-limits` |
| `https://docs.z.ai/api-reference/rate-limit.md` | Same 307. The `.md` twin does not help. |
| `https://z.ai/manage-apikey/rate-limits` | Needs a login. Never cite it. |

The console page is the only place Z.ai publishes numeric API rate limits, and
it is behind an account. That is why `data/rate_limits.yaml` holds no Zhipu row.

## What each page does not say

- `devpack/overview` prints "Starting at just 18 USD per month" and no other
  price. One figure is not enough to fill a row.
- `guides/overview/pricing` publishes no context window and no maximum output.
  `data/models.yaml` needs those, so read `guides/llm/glm-5.3` instead.
- `devpack/teamplan` publishes seat quotas and no price at all.
- `devpack/usage-policy` ranks concurrency as `Max > Pro > Lite` and prints no
  number.

## Citation rule

`AGENTS.md` requires a page the provider owns. `z.ai` and `docs.z.ai` both
qualify. A login-gated console page does not qualify, because no reader can
open it to check your figure.
