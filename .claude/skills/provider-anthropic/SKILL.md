---
name: provider-anthropic
description: How to source Anthropic (Claude) prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh an Anthropic row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Anthropic, Claude, Claude Code, Opus, Sonnet, Haiku, Fable, the Max plan, or the Pro plan. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Anthropic (Claude) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Anthropic, so you do not repeat work that already failed.

Every status below comes from a fetch on 2026-08-28. Re-check a status before
you trust it.

## Constants

Write the provider as `Anthropic` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables. `region` is `global`. Prices are USD.

Anthropic sells two separate things, and this repository tracks both:

- **Subscriptions**, on `claude.com`. Pro, Max 5x, and Max 20x.
- **The API**, on `platform.claude.com`. Per-token rates and per-model limits.

The two live on different hosts and read with different tools. Keep them apart.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| API rates per token | `https://platform.claude.com/docs/en/about-claude/pricing.md` | `WebFetch` |
| API rate limits per model and tier | `https://platform.claude.com/docs/en/api/rate-limits.md` | `WebFetch` |
| Context window, max output, vision | `https://platform.claude.com/docs/en/models/overview.md` | `WebFetch` |
| Pro price, Max 5x price, plan features | `https://claude.com/pricing` | `curl`, then grep `data-plan` |
| Max 20x price | `https://support.claude.com/en/articles/11049741-what-is-the-max-plan` | `WebFetch` |
| Every docs URL | `https://platform.claude.com/llms.txt` | `curl` |

Every page under `platform.claude.com/docs/` serves a markdown twin. Append `.md`
to the path. The twin returns clean markdown and reads faster than the HTML.

## Six things that produce a wrong number

**1. `claude.com/pricing` publishes no Max 20x price.** The Max card prints
`From $100` and nothing else. The page names the 20x tier in its feature table
and then says "See the cards above for current pricing". The only Anthropic page
that states the 20x price is the support article
`11049741-what-is-the-max-plan`, which prints `Max 5x: $100 per month` and
`Max 20x: $200 per month`. Cite that article on the Max 20x row.

**2. The Pro card prints a monthly rate, not the annual total.** It shows `$17`
under the annual toggle, and the sentence below it says `$200 billed up front`.
`AGENTS.md` defines `amount` as the whole-term price, so write `200` for
`period: year`. An agent that multiplies 17 by 12 writes 204, which is wrong.

**3. `claude.com/pricing` rewrites its own displayed prices with VAT.** The page
runs a location-based pricing script. It reads the visitor country from
`get.geojs.io` and adds EU VAT to every element marked `data-tier-price`. The
HTML source holds the tax-exclusive USD figure. Read the source, never a
rendered figure. Details in `references/pages.md`.

**4. The API pricing page prints three cache columns.** They are `5m Cache
Writes`, `1h Cache Writes`, and `Cache Hits & Refreshes`. `cache_write` takes the
5-minute write. `cached_input` takes the cache hit. Put the 1-hour write in
`notes`. Table in `references/pricing.md`.

**5. The same page also prints fast mode rates and batch rates.** Fast mode
charges 10.00 input and 50.00 output on Claude Opus 5. The Batch API charges half
the base rate. Neither belongs in `input` or `output`. Copy the `Base Input
Tokens` and `Output Tokens` columns only.

**6. The rate-limit tables name model classes, not models.** One row reads
`Claude Opus 4.x`, and a footnote states that Anthropic pools Opus 4.8, 4.7, 4.6,
and 4.5 into one limit. A second row reads `Claude Sonnet 4.x` and pools Sonnet
4.6 and 4.5. Claude Opus 5 and Claude Sonnet 5 each hold a separate bucket. Write
the pooled figure under one display model and say so in `notes`. Reasoning in
`references/quotas.md`.

## Workflow

1. Read `https://platform.claude.com/docs/en/about-claude/pricing.md`. Take the
   `Base Input Tokens`, `5m Cache Writes`, `Cache Hits & Refreshes`, and `Output
   Tokens` columns.
2. Read `https://platform.claude.com/docs/en/api/rate-limits.md`. Take one row
   per model class per tier, for the Start, Build, and Scale tiers only.
3. Read `https://platform.claude.com/docs/en/models/overview.md`. Take the
   context window, the max output, and the model IDs.
4. Fetch `https://claude.com/pricing` with `curl`. Grep the `data-plan`
   attributes for the Pro and Max prices.
5. Read `https://support.claude.com/en/articles/11049741-what-is-the-max-plan`
   for the Max 20x price.
6. Write the rows. Copy the shapes in `references/data-recipes.md`.
7. Set `last_verified` to the date you read the pages.
8. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the `curl` recipe |
| `references/pricing.md` | Plan prices, API token rates, the modifiers to ignore |
| `references/quotas.md` | Rate limits per tier, plan usage limits, the pooled buckets |
| `references/data-recipes.md` | A worked row for each of the four datasets |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
