---
name: provider-meta
description: How to source Meta Muse Code plan prices, API rates, and model specs for the datasets in this repository. Use when you add or refresh a Meta row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, data/models.yaml, or data/changelog.yaml, or when the user mentions Meta, Muse Code, Muse Spark, muse-spark, developer.meta.com, or Meta Model API. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Meta (Muse Code) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Meta, so you do not repeat work that already failed.

Everything here was checked on 2026-09-03. Re-check a status before you trust it.

## Constants

Write the provider as `Meta` in all five data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

Prices and rates are USD. Muse Spark 1.3 is the newest model; the subscription
tiers unlock Muse Spark 1.2.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices, plan quotas | `https://developer.meta.com/ai/products/muse-code/` | `curl` with a browser UA — see trap 1 |
| API rates per 1M tokens, context window | same page, the "Models and pricing" table | same |
| Model specs, vision, contributor rows | `https://developer.meta.com/ai/models/muse-spark/` | `curl` with a browser UA |
| Brand colour | Meta blue `#0064E0`, the most frequent brand blue in the page CSS | page CSS |

## Five things that produce a wrong number

**1. A plain `curl` returns an error shell.** Without browser headers every
`developer.meta.com/ai/` page returns HTTP 400 and a "This page isn't
available" shell. Fetch with a browser user agent plus navigation headers:

```bash
curl -sL --max-time 30 --http2 \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml" \
  -H "Accept-Language: en-US,en;q=0.9" \
  -H "Sec-Fetch-Site: none" -H "Sec-Fetch-Mode: navigate" -H "Sec-Fetch-User: ?1" \
  -H "Upgrade-Insecure-Requests: 1" \
  "https://developer.meta.com/ai/products/muse-code/"
```

With headers the Muse Code page returns HTTP 200 (~930 KB) and the Muse Spark
page returns HTTP 200 (~914 KB). The reader-mode `read` tool returns only meta
tags on both pages; `curl` on the page HTML is the working route (sourcing-rule
step 3). Save cookies between requests with `-b`/`-c`; sibling pages probed
with a fresh jar returned HTTP 400.

**2. The prose is not in the DOM text.** The page body is a React shell plus
Relay-prefetched CMS JSON (`json_cms_content`). Stripping tags yields only nav,
footer, and hero copy — no prices. Extract the leaf strings with:

```bash
python3 -c "
import re,json
t=open('page.html',encoding='utf-8',errors='replace').read()
for s in re.findall(r'children\\\\\":\[\\\\*\"((?:[^\"\\\\]|\\\\.)*?)\\\\*\"\]', t):
    try: s=json.loads('\"'+s+'\"')
    except: pass
    print(s.strip())
"
```

**3. Two rows per generation: standard and contributor.** The "Models and
pricing" table prices each generation twice. The `-contributor` row ("Used to
improve our products") is the cheap discounted tier; the plain row ("Not used
to improve our products") is the standard tier. Write both as separate
`data/api_pricing.yaml` rows and put the training-use sentence in `notes`.
Do not average them.

**4. The plan tiers sell requests, not tokens.** Everyday ($5), High ($15), and
Power ($50) Usage are subscription quotas: "Send 10–50 requests every 5 hours",
then "3x" and "10x more usage than the Everyday Usage plan". They carry no
per-1M-token rate. Model the multipliers as `limits` strings, not numbers,
and keep the plan `models` list to `muse-spark-1.2`, the model the tiers name.

**5. Meta publishes no numeric API rate limit.** Neither the Muse Code page nor
the Muse Spark page states an RPM, TPM, or RPD number. `data/rate_limits.yaml`
gets zero Meta rows. Zero rows is the correct result here. Do not fill the gap
with a third-party number.

## Workflow

1. Fetch the Muse Code page with browser headers. Take the three tier prices
   ($5.00, $15.00, $50.00 per month) and the quota strings.
2. From the same page, take the "Models and pricing" table: context window
   (1M), input, cached input, and output per 1M tokens, for both the standard
   and the `-contributor` row of the generation the page prices.
3. Fetch the Muse Spark page. Take the model prose: agentic coding tuning,
   long-horizon workflows, native multimodal perception (video, images,
   documents) — the stated basis for `vision: true` on the 1.3 row.
4. Write one `data/plans.yaml` record per tier. Write `data/api_pricing.yaml`
   rows for the priced generation. Write `data/models.yaml` rows: `vision:
   true` only where the page states multimodal perception; `open_weights:
   null` everywhere (Meta states neither open nor closed weights).
5. Add no row to `data/rate_limits.yaml`.
6. Use only `developer.meta.com` URLs in `links`. Label the product page
   `plans` on plan rows and `pricing` on API rows; label the model page
   `model card`.
7. Set `last_verified` to the date you read the pages.
8. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, the tier values, the rate table, and the model prose |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
