# Cursor page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

Cursor serves the whole site from `cursor.com`. There is no separate docs host.

## Pages that carry data this repository needs

| Page | Publishes | Tool |
|---|---|---|
| `https://cursor.com/help/account-and-billing/pricing.md` | Monthly price of every tier, in one table | `curl` |
| `https://cursor.com/pricing` | Yearly prices, tier feature lines | `scripts/read_yearly_prices.py`, `curl` |
| `https://cursor.com/docs/models-and-pricing.md` | Usage pools, per-model token rates, Team seats | `curl` |
| `https://cursor.com/help/models-and-usage/usage-limits.md` | How the pools reset, on-demand billing | `curl` |
| `https://cursor.com/help/models-and-usage/available-models.md` | Model list, Grok rates in prose | `curl` |
| `https://cursor.com/docs/account/teams/pricing.md` | Team seat prices and seat types | `curl` |
| `https://cursor.com/docs/api.md` | REST API rate limits, not per model | `curl` |
| `https://cursor.com/docs/models/<model>` | Context window, model ID, provider | `curl` |
| `https://cursor.com/llms.txt` | Every documentation URL | `curl` |

## The docs index

`https://cursor.com/llms.txt` lists every `/docs/` and `/help/` URL on the site,
each in its `.md` form. Read it first when a page you expect is missing. It is
how `docs/account/teams/pricing.md` and `help/models-and-usage/token-rate.md`
were found, neither of which is linked from the pricing pages.

`https://cursor.com/docs/llms.txt` serves the same file. Both returned 19024
bytes on 2026-08-28.

## The `.md` twin rules

Cursor serves a markdown twin for `/docs/` and `/help/` pages. Append `.md` to
the path:

    https://cursor.com/docs/models-and-pricing
    https://cursor.com/docs/models-and-pricing.md

Three rules limit the trick.

1. **Marketing pages have no twin.** `https://cursor.com/pricing.md` returns
   200 with `content-type: text/html`. It is the marketing page, not markdown.
   Check the content type, not the status code.
2. **A redirect path has no twin.** `https://cursor.com/docs/account/pricing`
   308-redirects. `https://cursor.com/docs/account/pricing.md` returns 404.
   Resolve the redirect, then append `.md` to the target.
3. **The twin drops component-rendered blocks.** See the next section.

## The twin drops the model spec card

`https://cursor.com/docs/models/cursor-composer-2-5` prints a spec card and a
price table. Its `.md` twin prints neither. The twin says "On-demand usage is
charged at the rates below" and then stops.

Read the HTML with `curl` for a model specification. The card holds these
fields, read from the Composer page on 2026-08-28:

| Field | Value |
|---|---|
| Context window | 200k |
| Max context | - |
| Model ID | composer-2.5 |
| Provider | Cursor |
| Intelligence | Frontier |
| Speed | Fast |
| Cost | Low |

Two more cards, read the same way:

| Model | Context window | Max context | Model ID |
|---|---|---|---|
| Grok 4.6 | 256k | - | grok-4.6 |
| Claude Opus 5 | 300k | 1M | claude-opus-5 |

The card states no parameter count, no maximum output, and no vision flag.

## Redirects

| URL | Redirects to | Note |
|---|---|---|
| `https://cursor.com/docs/account/pricing` | `https://cursor.com/docs/models-and-pricing` | 308. `data/plans.yaml` cites the old path. |
| `https://docs.cursor.com/` | `https://cursor.com/docs` | 308. The old docs host still answers. |
| `https://docs.cursor.com/llms.txt` | `https://cursor.com/docs` | 308. The path is dropped, so you get the docs home page, not the index. |

`WebFetch` refuses a cross-host redirect and returns the target URL. Call it
again with the target. `curl -L` follows both kinds.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://cursor.com/docs/account/pricing.md` | 404. The path is a redirect stub. |
| `https://cursor.com/pricing.md` | 200 and serves HTML. Not a markdown twin. |
| `https://docs.cursor.com/llms.txt` | 308 to the docs home page. The path is dropped. |
| `https://cursor.com/dashboard/spending` | Needs a login. Never cite it. |
| `https://cursor.com/dashboard/usage` | Needs a login. Never cite it. |
| `https://cursor.com/api/auth/checkoutDeepControl` | Needs a login. Never cite it. |

## Where `WebFetch` reads the wrong number

`WebFetch` on `https://cursor.com/pricing` produced two wrong answers on
2026-08-28:

- It reported Pro+ and Ultra as "Not specified". Both prices exist.
- It reported Teams Premium as `$40/user (base)`. The real price is `$120`.

The cause is the markup. The page renders a radio picker and ships the selected
tier only, so the other tiers carry no price in the HTML text. Use
`help/account-and-billing/pricing.md` for prices. It is a plain table.

`WebFetch` reads `https://cursor.com/docs/account/pricing` correctly, because it
follows the same-host 308 and the target is prose.

## What each page does not say

- `help/models-and-usage/usage-limits.md` states no number. It names the two
  pools and points at a login-gated dashboard for the amounts.
- `cursor.com/pricing` states the tier multipliers and no absolute usage figure.
- `docs/models-and-pricing.md` states no context window. Read a model card.
- No page states a parameter count for Composer or Grok.

## Citation rule

`AGENTS.md` requires a page the provider owns. `cursor.com` qualifies. A
login-gated dashboard page does not qualify, because no reader can open it to
check your figure.
