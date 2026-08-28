# GitHub page inventory

Every status below comes from a fetch on 2026-08-28. Re-check before you trust
one.

## Pages that carry data this repository needs

| Page | Publishes | Tool | Status |
|---|---|---|---|
| `https://github.com/features/copilot/plans` | Tier prices, credit totals in USD | `WebFetch`, `curl` | 200 |
| `https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals` | Credit allowance per tier, credit value | `WebFetch`, `.md` twin | 200 |
| `https://docs.github.com/en/copilot/get-started/plans` | Tier summary, model availability per tier | `.md` twin | 200 |
| `https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing` | Rate per 1M tokens, per model | `.md` twin | 200 |
| `https://docs.github.com/en/copilot/reference/ai-models/supported-models` | Model list, release status, retirement dates | `WebFetch`, `.md` twin | 200 |
| `https://docs.github.com/en/copilot/concepts/usage-limits` | Rate-limit policy, no number | `.md` twin | 200 |
| `https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/what-changed-with-billing` | The 2026-06-01 billing switch | `.md` twin | 200 |
| `https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/copilot-requests` | Legacy premium-request allowances | `.md` twin | 200 |
| `https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/model-multipliers-for-annual-plans` | Legacy model multipliers | `.md` twin | 200 |
| `https://docs.github.com/llms.txt` | Index of every docs URL | `curl` | 200, 28 KB |

## The `.md` twin

Append `.md` to a `docs.github.com` path. The server returns clean markdown:

    https://docs.github.com/en/copilot/get-started/plans
    https://docs.github.com/en/copilot/get-started/plans.md

The twin is the fastest way to read a large table. It is not universal. See the
dead ends below for one page that answers 200 as HTML and 404 as markdown.

The twin works on `docs.github.com` only. `github.com` serves no markdown twin.

## The docs index

`https://docs.github.com/llms.txt` lists documentation URLs for the whole site.
It named 116 URLs on 2026-08-28, and 22 of them cover Copilot. Read it first
when a page you expect is missing.

Note the path. The index sits at the site root, not under a product. There is no
`/en/copilot/llms.txt`.

## Dead ends

Do not spend time on these. Each one was tried and failed.

| URL | What happens |
|---|---|
| `https://docs.github.com/en/copilot/concepts/billing/individual-plans.md` | 404, while the HTML page returns 200 |
| `https://docs.github.com/en/copilot/llms.txt` | 404. The index is at the site root. |
| `https://github.com/features/copilot/plans.md` | 404. No `.md` twin on `github.com`. |
| `https://docs.github.com/en/copilot/reference/copilot-rate-limits.md` | 404 |
| `https://docs.github.com/en/copilot/concepts/rate-limits.md` | 404 |
| `https://docs.github.com/en/github-models/about-github-models.md` | 404 |

## Trap: the markdown embeds inline SVG

GitHub renders a check mark and a cross as an inline `<svg>` element, and the
`.md` twin keeps the markup. Two pages grow very large as a result:

| Page | Size of the `.md` twin |
|---|---|
| `copilot/get-started/plans.md` | 222 KB |
| `copilot/reference/ai-models/supported-models.md` | 433 KB |

Read a cell by its class, not by its text:

- `octicon-check` means the feature is included.
- `octicon-x` means the feature is not included.

Do not test a whole table row for `octicon-check`. A row holds both classes, so
a row-level test marks every cell as included. Split the row on `|` first, then
test each cell.

## Trap: `WebFetch` summarises a large page

`WebFetch` answered on both large pages, but it reported no per-tier model table
on `supported-models`. That report is correct: the per-tier table sits on
`get-started/plans`, not on `supported-models`. Read the `.md` twin yourself
when you need a full table.

## Values no GitHub page publishes

Searched on 2026-08-28 across five pages: `get-started/plans.md`,
`models-and-pricing.md`, `supported-models.md`, `usage-limits.md`, and the raw
HTML of `github.com/features/copilot/plans` (1.26 MB).

| Term searched | Matches |
|---|---|
| `tokens per second`, `tokens/second`, `tok/s`, `per second` | 0 |
| `latency`, `throughput` | 0 |
| `requests per minute`, `requests per hour`, `requests per day` | 0 |
| `parameter` (on `supported-models.md`) | 0 |

Do not repeat this search. GitHub grades model speed by word, not by number.
`models-and-pricing` sorts every model into a `Category` of `Lightweight`,
`Versatile`, or `Powerful`. Raptor mini sits in `Versatile`.

`supported-models` publishes no vision column and no context window column. It
describes a 1 million token context window as an optional extended capability on
selected models, and Raptor mini is not one of them.

## Citation rule

`AGENTS.md` requires a page the provider owns. `github.com` and
`docs.github.com` both qualify. Every page in this file is public and needs no
login.
