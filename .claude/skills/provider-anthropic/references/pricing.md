# Anthropic prices

Read `pages.md` first. It tells you how to reach each page.

Anthropic prices two products. Keep them apart:

- **Subscription prices** sit on `claude.com` and feed `data/plans.yaml`.
- **API token rates** sit on `platform.claude.com` and feed
  `data/api_pricing.yaml`.

## Subscription prices

Read on 2026-08-28. USD, before tax.

| Plan | Key in the HTML | Page prints | `period` | `amount` |
|---|---|---|---|---|
| Pro, monthly | `pro_monthly` | `$20` | `month` | 20 |
| Pro, annual | `pro_annual` | `$17` per month, `$200` billed up front | `year` | 200 |
| Max 5x | `max_5x_monthly` | `From $100` per month | `month` | 100 |
| Max 20x | none | not on this page | `month` | 200 |

### Trap: the Pro card prints a rate, not the total

The Pro card shows `$17` under the annual toggle. The sentence below it reads:

    Per month with annual subscription discount ($200 billed up front).
    $20 if billed monthly.

`AGENTS.md` defines `amount` as the price charged for one seat for that whole
term. So write `200` for `period: year`. Do not multiply 17 by 12. An agent that
multiplies writes 204 where 200 is right.

`build.py` derives the monthly equivalent back from `amount`. 200 divided by 12
is 16.67, and the page rounds that to 17. A one-cent gap between the rendered
cell and the page is expected.

### Trap: the Max 20x price is on a different page

`claude.com/pricing` prints `From $100` on the Max card and stops there. Its
feature table names a `Max 20x` column with no price. Its FAQ says "See the cards
above for current pricing", which is a loop.

`https://support.claude.com/en/articles/11049741-what-is-the-max-plan` states
both prices:

    Max 5x: $100 per month
    Max 20x: $200 per month

The same article adds two qualifiers. Copy both into your reasoning, not into the
row:

- "These prices are for web subscriptions only. Mobile pricing may vary."
- "The Max plan is currently available as a monthly subscription only."

So a Max row carries one `prices` entry, with `period: month`. Do not invent a
yearly total for Max.

### Team and Enterprise

`claude.com/pricing` also publishes seat prices. No Team or Enterprise row exists
in `data/plans.yaml` today. Adding one is a scope decision, not a sourcing
problem. Ask before you add one.

| Seat | Billed annually | Billed monthly |
|---|---|---|
| Team, standard | $20 per seat per month | $25 |
| Team, premium | $100 per seat per month | $125 |
| Enterprise | $20 per seat per month, plus usage at API rates | not offered |

Never mix a seat price into an individual Pro or Max row.

## API rates per token

From `https://platform.claude.com/docs/en/about-claude/pricing`, USD per 1M
tokens, read 2026-08-28. The page prints five columns. This table maps them onto
the schema in `AGENTS.md`.

| Model | `input` | `cache_write` (5m) | 1h write | `cached_input` | `output` |
|---|---|---|---|---|---|
| Claude Fable 5 | 10 | 12.50 | 20 | 1 | 50 |
| Claude Mythos 5 | 10 | 12.50 | 20 | 1 | 50 |
| Claude Opus 5 | 5 | 6.25 | 10 | 0.50 | 25 |
| Claude Opus 4.8 | 5 | 6.25 | 10 | 0.50 | 25 |
| Claude Opus 4.7 | 5 | 6.25 | 10 | 0.50 | 25 |
| Claude Opus 4.6 | 5 | 6.25 | 10 | 0.50 | 25 |
| Claude Opus 4.5 | 5 | 6.25 | 10 | 0.50 | 25 |
| Claude Sonnet 5 | 2 | 2.50 | 4 | 0.20 | 10 |
| Claude Sonnet 4.6 | 3 | 3.75 | 6 | 0.30 | 15 |
| Claude Sonnet 4.5 | 3 | 3.75 | 6 | 0.30 | 15 |
| Claude Haiku 4.5 | 1 | 1.25 | 2 | 0.10 | 5 |

The page also lists retired models: Claude Opus 4.1, Claude Opus 4, Claude Sonnet
4, and Claude Haiku 3.5. Skip a retired model unless a row already exists for it.

Claude Mythos 5 carries a "limited availability" label. No row exists for it.

### The three cache columns

The page names them `5m Cache Writes`, `1h Cache Writes`, and `Cache Hits &
Refreshes`. The schema holds two cache fields, so one column goes into `notes`.

| Page column | Field |
|---|---|
| `5m Cache Writes` | `cache_write` |
| `1h Cache Writes` | a sentence in `notes` |
| `Cache Hits & Refreshes` | `cached_input` |

Anthropic states the rates as multipliers of the base input price: 1.25x for the
5-minute write, 2x for the 1-hour write, and 0.1x for a cache read. Use the
multiplier as a cross-check, never as the source. Read the printed rate.

### Three modifiers that are not the base rate

The same page prints all three. None belongs in `input` or `output`.

1. **Fast mode.** Claude Opus 5 and Claude Opus 4.8 charge 10 input and 50 output
   under `speed: "fast"`. Record it in `notes` if you record it at all.
2. **Batch API.** Every batch rate is half the base rate. The page prints a full
   second table of them, which is easy to copy by mistake.
3. **Data residency.** `inference_geo: "us"` multiplies every rate by 1.1.

Partner platforms have their own prices. Amazon Bedrock and Google Cloud add a
10 percent premium on regional endpoints. Those are pages Anthropic does not own,
so rule 4 in `AGENTS.md` forbids citing them.

### Long context

Anthropic charges one rate across the whole context window. The page states that
a 900k-token request bills at the same per-token rate as a 9k-token request. So
one row per model is enough. Do not split a model into a short-context row and a
long-context row.

## Currency

Every Anthropic price is USD. Set `price_currency: USD` and `currency: USD`.
