# DeepSeek prices and model specifications

Read from `https://api-docs.deepseek.com/quick_start/pricing` on 2026-08-28.
Rates are USD per 1M tokens.

## The full rate table

| Rate | deepseek-v4-flash | deepseek-v4-pro | deepseek-v4-flash-vision-exp |
|---|---|---|---|
| Input, cache hit, off-peak | 0.007 | 0.022 | 0.007 |
| **Input, cache hit, peak** | **0.014** | **0.044** | **0.014** |
| Input, cache miss, off-peak | 0.22 | 0.66 | 0.22 |
| **Input, cache miss, peak** | **0.44** | **1.32** | **0.44** |
| Output, off-peak | 0.66 | 1.98 | 0.66 |
| **Output, peak** | **1.32** | **3.96** | **1.32** |

The bold rows are the ones `data/api_pricing.yaml` records.

## How the table maps to the schema

| Schema field | Table row |
|---|---|
| `input` | Input, cache miss, peak |
| `cached_input` | Input, cache hit, peak |
| `cache_write` | Always `null`. DeepSeek publishes no cache-write rate. |
| `output` | Output, peak |

## Peak and off-peak

The page states: "Off-peak rates are half of the peak rates. Peak hours are
01:00 - 04:00 and 06:00 - 10:00 UTC, Monday through Friday (all other hours are
off-peak)."

The Chinese twin states the same window in Beijing time, 09:00-12:00 and
14:00-18:00, Monday to Friday. The two agree. Write the UTC form.

Record the schedule in `notes`. Keep it to the two sentences the current rows
use, so every DeepSeek row reads the same way.

DeepSeek introduced peak and off-peak rates with the V4-Pro launch. The change
took effect at 16:00 UTC on 2026-08-16, per
`https://api-docs.deepseek.com/news/news260813`.

## Currency trap

`https://api-docs.deepseek.com/zh-cn/quick_start/pricing` prints CNY, not a
converted USD figure. Side by side, for `deepseek-v4-pro`:

| Rate | Default page (USD) | `zh-cn` page (CNY) |
|---|---|---|
| Input, cache hit, peak | 0.044 | 0.30 |
| Input, cache miss, peak | 1.32 | 9.0 |
| Output, peak | 3.96 | 27.0 |

The datasets use USD, so read the path without a language prefix.

## Model specifications on the pricing page

| Field | deepseek-v4-flash | deepseek-v4-pro | deepseek-v4-flash-vision-exp |
|---|---|---|---|
| Model version | DeepSeek-V4-Flash-0731 | DeepSeek-V4-Pro-0813 | DeepSeek-V4-Flash-Vision-Exp |
| Context length | 1M | 1M | 1M |
| Max output | 384K | 384K | 384K |
| Concurrency limit | 2500 | 500 | 2500 |

Every model takes both an OpenAI-format base URL, `https://api.deepseek.com`,
and an Anthropic-format base URL, `https://api.deepseek.com/anthropic`.

## Parameter counts

From `https://www.deepseek.com/en/news/v4-preview/`, dated 2026-04-24.

| Model | Total params | Active params |
|---|---|---|
| DeepSeek-V4-Pro | 1.6T | 49B |
| DeepSeek-V4-Flash | 284B | 13B |

The same page states that DeepSeek open-sourced the V4 weights. It links Hugging
Face and arXiv. Set `open_weights: true` and cite the DeepSeek page, not the
Hugging Face page. The page states no parameter count for
`deepseek-v4-flash-vision-exp`.

## Vision

`deepseek-v4-flash-vision-exp` is the only model that reads images. It is
experimental. The launch note at
`https://api-docs.deepseek.com/news/news260821` says an image bills as up to 384
input tokens at V4-Flash rates. Set `vision: false` for V4-Pro and V4-Flash.

## Retired models

DeepSeek withdrew `deepseek-chat` and `deepseek-reasoner` after 2026-07-24
15:59 UTC, per `https://www.deepseek.com/en/news/v4-preview/`. Both routed to
`deepseek-v4-flash` until then. No page states their rates now, so you cannot
source a row for either.
