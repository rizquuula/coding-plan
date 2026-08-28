# Z.ai prices

Read `fetching.md` first. It tells you how to get these numbers off the page.

## The trap: the page and the bundle print different figures

The **rendered page** prints a per-month figure under every toggle, such as
`$12.6/month` with `$18/month` struck through. It never prints what it charges
for the whole term.

The **JavaScript bundle** holds the term total in `money`. `fetching.md` tells
you how to read it. That is the source you use.

`AGENTS.md` defines `amount` as the price charged for one seat for that whole
term. So copy `money` into `amount` with no arithmetic. Do not multiply by 3 or
by 12. An agent that multiplies writes 129.6 where 43.2 is right.

| Term | Months | Page prints | Bundle `money` | `amount` to write |
|---|---|---|---|---|
| `month` | 1 | 18 | 18 | 18 |
| `quarter` | 3 | 14.4 | 43.2 | 43.2 |
| `year` | 12 | 12.6 | 151.2 | 151.2 |

The term total is not a figure the page prints, so `notes` says where it comes
from:

    notes: Z.ai prints a rate per month; the quarter and year totals are that
      rate times the term.

`build.py` derives the monthly equivalent back from `amount` and prints it under
the term. Check the rendered cell shows the rate the page prints. For the yearly
Lite row it must read `$12.60/mo · save 30%`.

## Individual plan prices

Read on 2026-08-28 from the bundle. USD, whole-term totals, ready for `amount`.

| Tier | `month` | `quarter` | `year` |
|---|---|---|---|
| Lite | 18 | 43.2 | 151.2 |
| Pro | 80 | 192 | 672 |
| Max | 168 | 403.2 | 1411.2 |

The same prices as the page prints them, per month:

| Tier | Monthly | Quarterly | Yearly |
|---|---|---|---|
| Lite | 18 | 14.4 | 12.6 |
| Pro | 80 | 64 | 56 |
| Max | 168 | 134.4 | 117.6 |

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

No Team row exists in `data/plans.yaml`. A price is now reachable: the public
JSON API in `pages.md` returned PRO at 88 per month and MAX at 188 per month on
2026-08-28. Adding a Team row is a scope decision, not a sourcing problem. Ask
before you add one, and never mix a Team figure into an Individual row.

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
