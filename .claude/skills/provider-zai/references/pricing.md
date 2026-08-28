# Z.ai prices

Read `fetching.md` first. It tells you how to get these numbers off the page.

## The trap: a rate per month, not the price of the term

Under the quarterly and yearly toggles, Z.ai still prints a **per-month**
figure, such as `$12.6/month` with `$18/month` struck through. It never prints
what it charges for the whole term.

`AGENTS.md` defines `amount` as the price charged for one seat for that whole
term. So you must multiply:

| Term | Months | What the page prints | `amount` to write |
|---|---|---|---|
| `month` | 1 | 18 | 18 |
| `quarter` | 3 | 14.4 | 43.2 |
| `year` | 12 | 12.6 | 151.2 |

The product is not a figure the page prints. Say so in `notes` on every row you
derive:

    notes: Z.ai prints a rate per month; the quarter and year totals are that
      rate times the term.

`build.py` derives the monthly equivalent back from `amount` and prints it under
the term. Check the rendered cell shows the rate you read on the page. For the
yearly Lite row it must read `$12.60/mo · save 30%`.

If Z.ai ever prints a term total, write that instead and delete the note.

## Individual plan prices

Read on 2026-08-28. Rates are USD per month, as printed.

| Tier | Monthly | Quarterly | Yearly |
|---|---|---|---|
| Lite | 18 | 14.4 | 12.6 |
| Pro | 80 | 64 | 56 |
| Max | 168 | 134.4 | 117.6 |

Converted to term totals for `amount`:

| Tier | `month` | `quarter` | `year` |
|---|---|---|---|
| Lite | 18 | 43.2 | 151.2 |
| Pro | 80 | 192 | 672 |
| Max | 168 | 403.2 | 1411.2 |

## Discounts

The toggles carry the discount as a printed label: `-20%` on Quarterly and
`-30%` on Yearly. Those figures are sourced, not derived.

Every tier takes the same percentage. A pasted or scraped figure that breaks the
pattern is a transcription error. Confirm it before you write it.

Do not compute a price from the percentage. Read the price.

## Team plans

`https://docs.z.ai/devpack/teamplan` describes two seat types and no price:

| Seat | Credits per 5 hours | Credits per week |
|---|---|---|
| Standard | 15,000 | 66,000 |
| Premium | 35,000 | 155,000 |

The page also states that overage bills at a 10 percent discount off the model
API list price, as a limited-time offer.

No Team row exists in `data/plans.yaml`. Adding one needs a price, and no page
an agent can reach publishes it.

## API rates per token

From `https://docs.z.ai/guides/overview/pricing`, USD per 1M tokens, read
2026-08-28. `data/api_pricing.yaml` carries the first two.

| Model | Input | Cached input | Output |
|---|---|---|---|
| GLM-5.3 | 1.4 | 0.26 | 4.4 |
| GLM-5.3-Flash | 0.075 | 0.015 | 0.25 |
| GLM-5.2 | 1.4 | 0.26 | 4.4 |
| GLM-5.1 | 1.4 | 0.26 | 4.4 |
| GLM-5 | 1.0 | 0.2 | 3.2 |
| GLM-5-Turbo | 1.2 | 0.24 | 4.0 |
| GLM-4.7 | 0.6 | 0.11 | 2.2 |
| GLM-4.7-FlashX | 0.07 | 0.01 | 0.4 |
| GLM-4.6 | 0.6 | 0.11 | 2.2 |
| GLM-4.5 | 0.6 | 0.11 | 2.2 |
| GLM-4.5-X | 2.2 | 0.45 | 8.9 |
| GLM-4.5-Air | 0.2 | 0.03 | 1.1 |
| GLM-4.5-AirX | 1.1 | 0.22 | 4.5 |

`GLM-4.7-Flash` and `GLM-4.5-Flash` are free. The page also lists vision, image,
video, audio, and agent pricing, which this repository does not track.

Z.ai publishes no cache-write rate. Leave `cache_write` as `null`.

This page publishes no context window and no maximum output. Read
`https://docs.z.ai/guides/llm/glm-5.3` for those.
