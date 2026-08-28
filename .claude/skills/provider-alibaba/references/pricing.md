# Alibaba API prices

Read `fetching.md` first. It tells you how to get these numbers off the page.

Source: `https://www.alibabacloud.com/help/en/model-studio/model-pricing.md`
Read on 2026-08-28. Every figure below is USD per 1M tokens.

## How the page is organised

The page has one `###` section per model family, such as `Qwen-Max` or
`Qwen-Coder`. Inside each family it has one `####` section per region.

| Region heading | Deployment scope in the rows |
|---|---|
| `Singapore` | `International` |
| `China (Beijing)` | `Chinese mainland` |
| `Hong Kong (China)` | `Global` |
| `Germany (Frankfurt)` | `Global` |
| `US (Virginia)` | `Global` |
| `Japan (Tokyo)` | `Japan` or `Global` |

The existing row in `data/api_pricing.yaml` uses the Singapore section. Keep
using it unless a task says otherwise. Name the region in `notes`.

## Trap: the legacy model hides under "More models"

Each region section opens with the current models. A second heading, `##### More
models`, holds the legacy ones. `qwen-max` is a legacy model. It is not the
newest Qwen Max.

Read on 2026-08-28, Singapore section:

| Model ID | Where in the section | Input | Output |
|---|---|---|---|
| `qwen3.8-max` | main table | 2 | 6 |
| `qwen3.7-max` | main table | 2.5 (list price) | 7.5 (list price) |
| `qwen3-max` | main table | 1.2 / 2.4 / 3 by range | 6 / 12 / 15 by range |
| `qwen-max` | **More models** | 1.6 | 6.4 |

`qwen-max` in China (Beijing), also under **More models**: 0.345 input, 1.377
output.

`data/api_pricing.yaml` carries one row, `alibaba-qwen-max`, with `input: 2.50`
and `output: 7.50`. Those are the `qwen3.7-max` figures, not the `qwen-max`
figures. Fix the row or rename it, but do not leave both wrong at once.

## Trap: one model, several input rates

Most Qwen 3 models bill by input token range. `data/api_pricing.yaml` holds one
`input` number and one `output` number.

`qwen3-coder-plus`, Singapore, read 2026-08-28:

| Input token range | Input | Output |
|---|---|---|
| 0 < T ≤ 32K | 1 | 5 |
| 32K < T ≤ 128K | 1.8 | 9 |
| 128K < T ≤ 256K | 3 | 15 |
| 256K < T ≤ 1M | 6 | 60 |

`qwen3-coder-flash`, Singapore:

| Input token range | Input | Output |
|---|---|---|
| 0 < T ≤ 32K | 0.3 | 1.5 |
| 32K < T ≤ 128K | 0.5 | 2.5 |
| 128K < T ≤ 256K | 0.8 | 4 |
| 256K < T ≤ 1M | 1.6 | 9.6 |

Write the lowest range and name that range in `notes`:

    notes: Rate for requests up to 32K input tokens; longer requests cost more.

`qwen-max` prints `No tiered pricing`, so its row needs no such note.

## Trap: the page prints two prices in one cell

A discounted cell reads:

    List price $2.5 Limited-time 50% off

Copy the list price. It is the figure the page labels as a price. Say in `notes`
that a limited-time discount applies. Do not compute the discounted figure and
do not write it into `input` or `output`.

Some regions carry a different discount wording:

    List price $1.65 Limited-time night 80% off, daytime 50% off

The page defines night as 22:00 to 08:00 (UTC+8), by billing time.

## Cached input and cache write

The pricing page states this at the top:

> The input prices in the tables below do **not** include cache prices.

`https://www.alibabacloud.com/help/en/model-studio/context-cache.md` publishes
the cache rules as percentages of the standard input rate, not as absolute
rates:

| Event | Billed at |
|---|---|
| Explicit cache creation | 125% of the standard input rate |
| Explicit cache hit | 10% of the standard input rate |
| Implicit cache hit | 20% of the standard input rate |

Two rules follow for `data/api_pricing.yaml`.

1. A model that the cache page does not list gets `cached_input: null` and
   `cache_write: null`. `qwen-max` is not in the Singapore list, so its nulls
   are correct.
2. `qwen3.8-max` and `qwen3.8-2.4t-a95b` are an explicit exception. The page
   says their cache-hit price is **not** 10%, and it names the console as the
   only place that publishes the real figure. The console needs a login, so
   leave both fields `null` for those two models.

For any other listed model you may compute the two rates from the percentages
and the standard input rate. If you do, say so in `notes`. The page publishes
the rule, not the number.

Models the cache page lists for Singapore, read 2026-08-28:

    Qwen Max:    qwen3.8-max, qwen3.7-max, qwen3.7-max-2026-05-20,
                 qwen3.7-max-2026-06-08, qwen3.6-max-preview, qwen3-max
    Qwen Plus:   qwen3.7-plus, qwen3.7-plus-2026-05-26, qwen3.6-plus,
                 qwen3.5-plus, qwen3.5-plus-2026-04-20, qwen-plus
    Qwen Flash:  qwen3.7-flash, qwen3.7-flash-2026-07-15, qwen3.6-flash,
                 qwen3.5-flash, qwen-flash
    Qwen Coder:  qwen3-coder-plus, qwen3-coder-flash

## Batch inference

`qwen-max` carries a `50% batch inference discount` label. The page states that
batch calls cost 50% of the real-time rate, and that the batch discount and the
cache discount cannot apply at the same time.

This repository tracks the real-time rate. Ignore the batch figure.

## Context windows

`model-pricing` publishes no context window. Read
`https://www.alibabacloud.com/help/en/model-studio/text-generation-model.md`.

Read 2026-08-28:

| Model ID | Context |
|---|---|
| `qwen3.8-max` | 1M |
| `qwen3.7-plus` | 1M |
| `qwen3.7-flash` | 1M |
| `qwen3.7-max` | 1M |
| `qwen3-max` | 256k |
| `qwen-max` | 128k |
| `qwen-plus` | 1M |
| `qwen-flash` | 1M |
| `qwen3-coder-plus` | 1M |
| `qwen3-coder-flash` | 1M |
| `qwen3-coder-next` | 256k |
| `qwen3-coder-480b-a35b-instruct` | 256k |
| `qwen3-coder-30b-a3b-instruct` | 256k |

That page lists `qwen-max` under a heading called `Legacy models`. It recommends
`qwen3.7-plus` and `qwen3.8-max` for coding tools.

**No page read in this session publishes a maximum output length.** Leave
`max_output` as `null` in `data/models.yaml` until you find a page that states
it. The same holds for parameter counts of the closed models.
