---
name: provider-alibaba
description: How to source Alibaba (Qwen) prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh an Alibaba row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Alibaba, Alibaba Cloud, Qwen, qwen-max, qwen3-max, qwen3-coder, Model Studio, DashScope, Bailian, Coding Plan, or Token Plan. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Alibaba (Qwen) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Alibaba, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Alibaba (Qwen)` in all four data files. The build script
groups rows by that exact string, so any other spelling splits the provider into
two tables.

Alibaba runs two separate documentation sites for one product:

| Site | Host | Currency | Language |
|---|---|---|---|
| International | `www.alibabacloud.com/help/en/model-studio/` | USD | English |
| China | `help.aliyun.com/zh/model-studio/` | CNY | Chinese |

**This repository sources the international site.** Every Alibaba row today
carries a `www.alibabacloud.com` URL and `currency: USD`. Keep it that way. Use
`region: global` in `data/plans.yaml`.

The product is called **Model Studio** in English and **Bailian** in Chinese.
**DashScope** is the name of its native API protocol. All three names point at
the same service.

## Where each value lives

Every page below serves a markdown twin. Append `.md` to the path. The twin is
the source you read. See trap 2.

| You need | Page slug on the international site | Tool |
|---|---|---|
| API rates per token | `model-pricing` | `scripts/read_tables.py` |
| API rate limits | `rate-limit` | `WebFetch` or the script |
| Context window per model | `text-generation-model` | `scripts/read_tables.py` |
| Coding Plan price and quota | `coding-plan` | `scripts/read_tables.py` |
| Token Plan prices and quotas | `token-plan-overview` | `scripts/read_tables.py` |
| Cache billing rules | `context-cache` | `WebFetch` |

Full URL form:

    https://www.alibabacloud.com/help/en/model-studio/<slug>.md

## Six things that produce a wrong number

**1. `qwen-max` is not the newest Qwen Max model. It is the legacy one.** The
`Qwen-Max` section of `model-pricing` opens with a big table of `qwen3.8-max`,
`qwen3.7-max`, and `qwen3-max`. The plain `qwen-max` model sits below that table
under a collapsed **More models** heading. On 2026-08-28 `qwen-max` cost $1.6
input and $6.4 output, while `qwen3.7-max` cost $2.5 and $7.5. Match the model
ID character for character before you copy a rate.

**2. `WebFetch` truncates `model-pricing`.** The page runs to about 1.28 MB. On
2026-08-28 `WebFetch` stopped at the section `Text generation - third-party
models` and reported every later section as absent. It returns a success code
and partial content. Read the `.md` twin instead. Details in
`references/fetching.md`.

**3. One model can carry four input rates.** `model-pricing` charges most Qwen 3
models by input token range. `qwen3-coder-plus` costs $1, $1.8, $3, or $6 per 1M
input tokens depending on the range. `data/api_pricing.yaml` holds one `input`
number. Write the lowest range and name the range in `notes`. Table in
`references/pricing.md`.

**4. The page prints a list price and a discounted price side by side.** A cell
reads `List price $2.5 Limited-time 50% off`. Copy the list price, which is the
figure the page labels. Say in `notes` that a limited-time discount applies. Do
not compute the discounted figure.

**5. A region is not a usage tier.** Alibaba publishes one rate limit per model
per region, at the Alibaba Cloud account level. It publishes no usage tier. A
model that is absent from one region's table has no published limit for that
region. On 2026-08-28 `qwen-max` appeared under Singapore and China (Beijing)
and did **not** appear under US (Virginia). Reasoning in `references/quotas.md`.

**6. Alibaba sells two subscription products, and both have a Pro tier.**
**Coding Plan** bills a fixed monthly fee and counts requests. **Token Plan**
bills a fixed monthly fee and counts Credits. They have different pages,
different prices, and different quota units. Never mix a figure from one into a
row for the other. Both are in `references/quotas.md`.

## Workflow

1. Read `references/pages.md`. It tells you which page holds your value.
2. Fetch the `.md` twin of that page. Run `python3 scripts/read_tables.py`.
3. Confirm the model ID matches character for character. See trap 1.
4. Confirm the region heading above the table. Run the script with `--context`.
5. Copy the list price, not the discounted price. See trap 4.
6. Write the rows. Copy the shapes in `references/data-recipes.md`.
7. Set `last_verified` to the date you read the page.
8. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the two sites |
| `references/fetching.md` | The `.md` twin recipe, the script, failure modes |
| `references/pricing.md` | API token rates, tiered pricing, cache rules |
| `references/quotas.md` | Coding Plan, Token Plan, and the rate limits |
| `references/data-recipes.md` | A worked row for each of the four datasets |
| `scripts/read_tables.py` | Prints the table rows of any Model Studio doc page |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
