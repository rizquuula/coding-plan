# Meta (Muse Code) — pages, probe results, and sourced values

Every probe below ran on 2026-09-03. Re-run a probe before you trust its status.

## URLs and probe results

| URL | Result |
|---|---|
| `https://developer.meta.com/ai/products/muse-code/` | HTTP 200 (~930 KB) with a browser UA plus navigation headers. Plain `curl` and the reader-mode fetch return HTTP 400 or meta tags only. Holds the three plan tiers and the "Models and pricing" table. |
| `https://developer.meta.com/ai/models/muse-spark/` | HTTP 200 (~914 KB) with the same headers. Holds the Muse Spark 1.3 prose and the same pricing table. |
| `https://developer.meta.com/ai/products/meta-model-api/` | HTTP 400 without full headers; sibling pages needed the cookie jar warmed by the Muse Code fetch. |
| `https://developer.meta.com/ai/products/meta-model-api/pricing/` | HTTP 400 (guessed path, no such page). |
| `https://developer.meta.com/ai/subscribe/` | HTTP 200 but a newsletter signup page ("Subscribe to AI Developer Updates"), not plan pricing. |
| `https://dev.meta.ai/docs/`, `https://dev.meta.ai/docs/cookbook/` | HTTP 500 error shells. |
| `https://dev.meta.ai/install.sh` | HTTP 200, the Muse Code CLI installer (`curl -fsSL https://dev.meta.ai/install.sh \| bash`). No prices. |
| `https://dev.meta.ai/llms.txt`, `https://developer.meta.com/ai/llms.txt` | 404 / error shell. No `.md` twin. |

The recipe that works: browser UA + `Accept: text/html` + `Accept-Language` +
`Sec-Fetch-*` + `Upgrade-Insecure-Requests`, reusing one cookie jar. Then
extract the Relay CMS leaf strings with the `children\":[\"...` regex in the
skill. Tag-stripping the DOM finds no prices.

## Plan tiers, USD per month

Source: the Muse Code page, "Muse Code subscription" block, read on 2026-09-03.

| Tier | month | quota as stated |
|---|---|---|
| Everyday Usage | 5.00 | Send 10–50 requests every 5 hours, including image and video uploads; access to Muse Spark 1.2; voice mode; web search |
| High Usage | 15.00 | Everything from Everyday, 3x more usage, more Muse Spark 1.2 usage, more requests, more multimodal inputs, latest models |
| Power Usage | 50.00 | Everything from High, 10x more usage than Everyday, expanded Muse Spark 1.2 usage, early access to new features, higher file uploads |

Taglines: Everyday "Best for shipping your first projects"; High "Best for
bigger, code-heavy projects"; Power "Best for ambitious, coding workflows".

## API rates per 1M tokens, USD

Source: the "Models and pricing" table on the same page, read on 2026-09-03.
The table prices both the 1.3 and the 1.2 generations at identical rates
(standard 1.25/0.15/4.25, contributor 0.10/0.002/0.20 per 1M tokens).

| Model on the page | model id | context | input | cached input | output | training use |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | muse-spark-1.3-contributor | 1M | 0.10 | 0.002 | 0.20 | Used to improve our products |
| muse-spark-1.3 | muse-spark-1.3 | 1M | 1.25 | 0.15 | 4.25 | Not used to improve our products |
| muse-spark-1.2-contributor | muse-spark-1.2-contributor | 1M | 0.10 | 0.002 | 0.20 | Used to improve our products |
| muse-spark-1.2 | muse-spark-1.2 | 1M | 1.25 | 0.15 | 4.25 | Not used to improve our products |

No `cache_write` rate is published; the column does not exist in the table.

## Model prose

Source: the Muse Spark page, read on 2026-09-03.

- "Muse Spark 1.3 is trained for agentic workflows and optimized for
  competitive coding performance. Developers can expect higher first-attempt
  accuracy and reliable tool calling."
- "Trained for long-horizon, agentic workflows" — tracks context and prior
  results, works through messy or conflicting inputs.
- "Native multimodal perception" — "Muse Spark perceives video, images and
  documents, and its visual reasoning runs through a real execution
  environment". This sentence is the stated basis for `vision: true` on the
  1.3 row.
- No page states parameter counts, maximum output length, or whether weights
  are open, so `total_params`, `active_params`, `max_output` are null and
  `open_weights` is null on every Meta row.

## Rate limits

Neither page states an RPM, TPM, RPD, or concurrency number, so Meta gets zero
rows in `data/rate_limits.yaml`. The plan quotas (requests per 5 hours, 3x/10x
multipliers) live in the `limits` list of each `data/plans.yaml` record.
