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

## Team seat prices

`data/plans.yaml` carries two Team rows: `Standard Seat` and `Premium Seat`.
Their prices come from the public JSON endpoint in `pages.md`, not from a
rendered page.

```bash
curl -s https://api.z.ai/api/biz/overseas/team/subscribe/product/public_pricing
```

### Trap: the endpoint serves products nobody can buy

`data.productList` holds ten entries. **Four are `purchasable: false`.** Treat
this with the same weight as the V1/V2/V3 trap on the subscribe bundle.

| `tier` | `subscribeMode` | `subscribePeriod` | `payAmount` | `purchasable` |
|---|---|---|---|---|
| PRO | CONTINUOUS | MONTHLY | 88 | true |
| PRO | CONTINUOUS | YEARLY | 1056 | true |
| PRO | ONE_TIME | MONTHLY | 88 | true |
| PRO | ONE_TIME | QUARTERLY | 264 | **false** |
| PRO | ONE_TIME | YEARLY | 1056 | **false** |
| MAX | CONTINUOUS | MONTHLY | 188 | true |
| MAX | CONTINUOUS | YEARLY | 2256 | true |
| MAX | ONE_TIME | MONTHLY | 188 | true |
| MAX | ONE_TIME | QUARTERLY | 564 | **false** |
| MAX | ONE_TIME | YEARLY | 2256 | **false** |

**Filter on `purchasable: true` before you copy any amount.**

**Z.ai does not sell a quarterly Team seat.** Both quarterly entries are
`purchasable: false`. A first pass wrote 264 and 564 into `data/plans.yaml` and
they were removed. The Team rows carry a `month` and a `year` term only.

The yearly term survives only because its `CONTINUOUS` variant is purchasable at
the same price. The `ONE_TIME` yearly entry is not purchasable. Never conclude
that a period is on sale from one entry alone. Check every entry for that
period.

### `payAmount` against `renewAmount`

`payAmount` is what a new subscriber pays. Write it into `amount`.

`renewAmount` is lower on both yearly entries: 950.40 for PRO and 2030.40 for
MAX. That is a 10 percent renewal discount. It is not a first-term price, so it
does not belong in `amount`. Put it in `notes`.

### Tier names

The API returns `PRO` and `MAX`. The subscribe page bundle maps them to display
names in a `LEVEL_RIGHTS` constant: `pro:{productName:"Standard Seat"...}` and
`max:{productName:"Premium Seat"...}`.

A `PLAN_ITEMS` list in the same module maps each tier and period to the same
`productId` values the API returns. That mapping is what ties the API tier to
the display name. Write the display name into `plan`.

Do not write `PRO` or `MAX` into `plan`. A reader never sees those strings.

### Team seat quotas

From `https://docs.z.ai/devpack/teamplan`. The page publishes quotas and no
price.

| Seat | Credits per 5 hours | Credits per week |
|---|---|---|
| Standard | 15,000 | 66,000 |
| Premium | 35,000 | 155,000 |

The page also states that overage bills at a 10 percent discount off the model
API list price, as a limited-time offer.

Never mix a Team figure into an Individual row, or an Individual figure into a
Team row.

## API rates per token

`https://docs.z.ai/guides/overview/pricing` publishes every rate, in USD per 1M
tokens. `data/api_pricing.yaml` carries 22 Zhipu rows read from it on
2026-08-28.

**The data file is the current record. Read it rather than a copy here.** A
table in this file would duplicate 22 rows and go stale first.

What the page does and does not give you:

- Z.ai publishes no cache-write rate. Leave `cache_write` as `null` on every
  row.
- Z.ai publishes a cached-read rate for most models. It is roughly a fifth of
  the input rate, but read it. Do not derive it.
- `GLM-4.7-Flash`, `GLM-4.5-Flash`, and `GLM-4.6V-Flash` are free. Write `0`,
  not `null`, and say "Free tier." in `notes`.
- The page publishes no context window and no maximum output. Read `models.md`
  for where those live.
- The page also lists image, video, audio, and agent pricing. This repository
  does not track those.

### Trap: GLM-5.3-Flash is on a promotion that expires

GLM-5.3-Flash bills at 50 percent off: 0.075 input, 0.015 cached input, and 0.25
output. Its list prices are 0.15, 0.03, and 0.50.

**The promotion ends at 24:00 on September 9, 2026, Singapore time (UTC+8).**

After that date the rates in `data/api_pricing.yaml` are stale. Re-read the
pricing page and write the list prices in. The row already names the date and
the list prices in `notes`, so update `notes` in the same edit.

This is the only Zhipu row with a known expiry date. Check it first on any
refresh.
