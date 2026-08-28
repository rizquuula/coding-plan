# Moonshot page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## Pages that carry data this repository needs

| Page | Publishes | Tool |
|---|---|---|
| `https://platform.kimi.ai/docs/llms.txt` | Every documentation URL and its markdown twin | `curl` |
| `https://platform.kimi.ai/docs/pricing/chat-k3` | Kimi K3 rates per token | `WebFetch` |
| `https://platform.kimi.ai/docs/pricing/chat-k27-code` | Kimi K2.7 Code rates per token | `WebFetch` |
| `https://platform.kimi.ai/docs/pricing/limits` | RPM, TPM, TPD, concurrency, per tier | `WebFetch` |
| `https://platform.kimi.ai/docs/pricing/chat` | Billing concepts, no number | `WebFetch` |
| `https://platform.kimi.ai/docs/models` | Model list, context windows, parameter count | `WebFetch` |
| `https://platform.kimi.ai/docs/guide/kimi-k3-quickstart` | K3 parameters, open weights, architecture | `WebFetch` |
| `https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart` | K2.7 Code context, vision, high-speed output rate | `WebFetch` |
| `https://platform.kimi.ai/docs/api/models-overview` | Per-model request parameters and context windows | `curl` |
| `https://platform.kimi.ai/docs/guide/product-plans` | How the API, the membership, and Kimi Code differ | `curl` |
| `https://www.kimi.com/code/docs/en/` | Kimi Code overview, concurrency wording | `curl` |
| `https://www.kimi.com/code/docs/en/kimi-code/models.html` | Which tier unlocks which model | `curl` |
| `https://www.kimi.com/code/docs/en/kimi-code/membership.html` | Quota rules, extra usage, no tier number | `curl` |
| `https://www.kimi.ai/blog/kimi-k3` | K3 launch note | `curl` |
| `https://www.kimi.com/apiv2/kimi.gateway.order.v1.GoodsService/ListGoods` | Every membership tier price | `scripts/read_plans.py` |

## The markdown twin

Every page under `platform.kimi.ai/docs/` serves a markdown twin. Append `.md`
to the path:

    https://platform.kimi.ai/docs/pricing/limits
    https://platform.kimi.ai/docs/pricing/limits.md

The twin returns MDX, not plain markdown. Numbers sit inside a `<DocTable>` JSX
block as quoted strings, so a table reads as a list of rows:

    ["Tier1", <>{"$"}10</>, "50", "200", "2,000,000", "Unlimited"],

That form is exact and easy to grep. `WebFetch` reads the rendered page and
returns the same numbers in a normal table. Use whichever you prefer.

The `.md` twin does **not** exist under `www.kimi.com/code/docs/`. That site
serves plain HTML. `curl` reads it. `WebFetch` reads it too, but it drops table
rows, so prefer `curl` when you need a per-tier table.

## The docs index

`https://platform.kimi.ai/docs/llms.txt` lists every documentation URL. It is
how `guide/product-plans`, `models`, and `guide/kimi-k3-quickstart` were found.
None of the three is linked from the pricing pages.

## Redirects, not sources

| URL | Redirects to |
|---|---|
| `https://platform.moonshot.ai/` | `https://platform.kimi.ai/` (301) |
| `https://platform.moonshot.ai/docs/pricing/limits` | `https://platform.kimi.ai/docs/pricing/limits` (301) |
| `https://platform.moonshot.cn/docs/pricing/limits` | `https://platform.kimi.com/docs/pricing/limits` (301) |
| `https://kimi.moonshot.cn/` | `https://www.kimi.com/` (302) |
| `https://www.kimi.com/blog/kimi-k3` | `https://www.kimi.ai/blog/kimi-k3` (302) |

Every `moonshot.ai` and `moonshot.cn` path now lands on a `kimi` host. Cite the
destination. A `moonshot.ai` link in `links` still resolves, but it hides which
stack the value came from, and this repository tracks two stacks.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://platform.kimi.ai/llms.txt` | 404. The index is under `/docs/`. |
| `https://www.kimi.com/pricing` | 302 to `https://www.kimi.com/`. No pricing page at that path. |
| `https://kimi.com/pricing` | 302 to `https://www.kimi.com/pricing`, which then 302s to the home page. |
| `https://www.kimi.com/code/docs/en/pricing` | 404. Kimi Code publishes no price of its own. |
| `https://www.kimi.com/code/docs/en/llms.txt` | 404. The Kimi Code docs serve no index. |
| `https://www.kimi.com/membership/pricing` with `WebFetch` | 200 and a page title only. No tier, no price. |
| `https://www.kimi.com/membership/pricing` with `curl` | 200 and about 15 KB of SPA shell. No tier, no price. |

The membership page is not a dead end in the end. Its prices come from a public
RPC. See `fetching.md`.

## What each page does not say

- `platform.kimi.ai/docs/pricing/chat` explains billing and prints no rate. Read
  the per-model page instead.
- `platform.kimi.ai/docs/models` prints context windows and no maximum output.
  No page found on 2026-08-28 prints a maximum output for any Kimi model.
  `docs/api/models-overview` compares every request parameter per model and
  states no output cap either. Check that page before you claim the gap again.
- `platform.kimi.ai/docs/pricing/limits` publishes a concurrency limit per tier.
  `data/rate_limits.yaml` has no field for it. Put it in `notes` or drop it.
- `kimi-code/membership.html` explains the weekly quota and the 5-hour window in
  words and prints no per-tier number.
- The `ListGoods` RPC returns prices and no quota. Its `features` field comes
  back empty for every tier.

## Citation rule

`AGENTS.md` requires a page the provider owns. `platform.kimi.ai`,
`www.kimi.com`, and `www.kimi.ai` all qualify. The `ListGoods` endpoint sits on
`www.kimi.com`, so it qualifies too, but no reader can open a POST endpoint in a
browser. Link the human page in `links` and record the endpoint here.
