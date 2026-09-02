# Verboo — pages, probe results, and sourced values

Every probe below ran on 2026-09-02. Re-run a probe before you trust its status.

## URLs and probe results

| URL | Result |
|---|---|
| `https://verboo.ai/en` | HTTP 200, ~102 KB. Server-rendered prose and the 14-model list. Plan prices absent. |
| `https://verboo.ai/en/api` | HTTP 200, ~101 KB, server-rendered. The 5-model rate table sits in the HTML. |
| `https://code.verboo.ai/api/marketplace?sortBy=priceCents&order=asc&apiOnly=false&includeMetrics=false` | HTTP 200, ~18 KB JSON, no auth. The only source of plan prices. |
| `https://code.verboo.ai/api/marketplace?...&apiOnly=true` | HTTP 200, zero records. Do not use it to find API models. |
| `https://code.verboo.ai/en/docs` | HTTP 200. The docs index. |
| `https://code.verboo.ai/en/docs/api/errors` | HTTP 200. Statuses and rate-limit headers, no numbers. |
| `https://code.verboo.ai/en/docs/api/models` | HTTP 200. Documents the `/models` response shape. |
| `https://code.verboo.ai/router/v1/models` | HTTP 401. |
| `https://code.verboo.ai/api/models` | HTTP 401. |
| `https://code.verboo.ai/api/public/models` | HTTP 401. |
| `https://code.verboo.ai/api/marketplace/models` | HTTP 404. |

## Plan tiers, USD

Source: the marketplace endpoint, read on 2026-09-02.

| Tier | slug | month | year | RPM | concurrent | models unlocked |
|---|---|---|---|---|---|---|
| Junior | junior | 24 | 240 | 40 | 2 | 2 |
| Pro | pro | 69 | 690 | 40 | 2 | 7 |
| Max | max | 129 | 1290 | 40 | 2 | 11 |
| Ultra | ultra | 269 | 2690 | 40 | 2 | 14 |

Pro carries a 1-day trial (`trialDays: 1`). Pro, Max, and Ultra allow seat
purchases (`seatPurchasesEnabled: true`). Junior does not.

## API rates per 1M tokens, USD

Source: `https://verboo.ai/en/api`, read on 2026-09-02.

| Model on the page | model id | context | input | cached | output |
|---|---|---|---|---|---|
| deepseek-v4-flash | deepseek-v4-flash | 1,048,576 | 0.14 | 0.006 | 0.22 |
| deepseek-v4-flash-0731 | deepseek-v4-flash-0731 | 1,048,576 | 0.14 | 0.006 | 0.22 |
| Qwen 3.6 27b | qwen3.6-27b | 262,144 | 0.15 | 0.03 | 1.50 |
| glm-5.2 | glm-5.2 | 1,048,576 | 0.70 | 0.15 | 2.20 |
| Kimi K3 | kimi-k3 | 1,048,576 | 2.50 | 0.30 | 9.00 |

The page marks all five ZDR (zero data retention).

## The 14 models on the platform

Context window comes from `instances[].models[].contextWindow` in the
marketplace JSON.

Context window 1048576: `deepseek-v4-flash`, `deepseek-v4-flash-0731`,
`deepseek-v4-pro`, `deepseek-v4-pro-0813`, `glm-5.2`, `glm-5.3`,
`glm-5.3-flash`, `kimi-k2.7`, `kimi-k3`, `mimo-v2.5`, `mimo-v2.5-pro`,
`minimax-m3`.

Context window 262144: `qwen3.6-27b`, `qwen3.8-27b`.

## The open-weights decision

`https://verboo.ai/en` states "The models are open source" and "All open source,
all running on our GPUs". That is Verboo's own page making the claim. Verboo
rows therefore carry `open_weights: true`, cited to `https://verboo.ai/en`.
