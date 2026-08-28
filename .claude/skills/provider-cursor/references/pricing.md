# Cursor prices

Read `pages.md` first. It tells you how to get these numbers off the page.

Every figure below was read on 2026-08-28.

## The trap: the page prints a rate per month under both toggles

`https://cursor.com/pricing` carries a Monthly/Yearly toggle. Under Yearly it
prints `$16/mo.` for Pro, with the callout `$16/mo. if billed yearly`. It never
prints what it charges for the whole year.

`AGENTS.md` defines `amount` as the price charged for one seat for that whole
term. So multiply the yearly rate by 12 before you write it.

| Tier | Monthly rate | Yearly rate per month | `amount` for `month` | `amount` for `year` |
|---|---|---|---|---|
| Pro | 20 | 16 | 20 | 192 |
| Pro+ | 60 | 48 | 60 | 576 |
| Ultra | 200 | 160 | 200 | 1920 |
| Teams Standard | 40 | 32 | 40 | 384 |
| Teams Premium | 120 | 96 | 120 | 1152 |

Cursor offers no quarterly term. Write `month` and `year` only.

Because the term total is not a figure the page prints, `notes` must say where
it comes from:

    notes: Cursor prints a rate per month; the year total is that rate times 12.

`build.py` derives the monthly equivalent back from `amount`. Check the rendered
cell shows the rate the page prints. For the yearly Pro row it must read
`$16.00/mo · save 20%`.

## Where each figure comes from

The monthly prices sit in one table on
`https://cursor.com/help/account-and-billing/pricing.md`:

| Plan | Price |
|---|---|
| Hobby | Free |
| Start (India only) | ₹649/mo, tax inclusive |
| Pro | $20/mo |
| Pro+ | $60/mo |
| Ultra | $200/mo |
| Teams Standard | $40/user/mo |
| Teams Premium | $120/user/mo |

The yearly prices are not in any HTML. Run the script:

```bash
python3 scripts/read_yearly_prices.py
```

It downloads `https://cursor.com/pricing`, downloads the 20 JavaScript chunks
the page references, and prints every `{monthly, yearly}` pair it finds. It uses
the standard library only.

## The discount

Every tier takes 20 percent off for the yearly term. Cursor prints no discount
label, so the percentage is derived, not sourced. Use it as a cross-check only.
A tier that breaks the pattern is a transcription error. Confirm it before you
write it.

Do not compute a price from the percentage. Read the price.

## The INR trap in the chunk

The chunk holds a second copy of the same numbers, wrapped in a call that
converts USD to INR for the India layout:

    e5=s(20,eh), e8=s(16,eh), e7=s(60,eh), e9=s(48,eh), re=s(200,eh), rr=s(160,eh)

`s(amount, rate)` formats `amount * rate` as INR. The literals are the USD
prices, so they are safe to read. The formatted output is not. The script reads
the plain USD strings instead, such as `{monthly:"$20/mo.",yearly:"$16/mo."}`.

## Start (India only)

Start costs ₹649 per month, tax inclusive, billed monthly in INR. No yearly term
exists. `price_currency` allows `USD`, `CNY`, and `EUR` only, so a Start row
does not validate. `data/plans.yaml` holds no Start row for that reason.

## Team plans

`https://cursor.com/docs/account/teams/pricing.md` states two paid seats and one
free seat:

| Seat | Price | Usage |
|---|---|---|
| Standard | $40/user/mo | The standard Teams allowance |
| Premium | $120/user/mo | 5x a Standard seat |
| Free | $0/user/mo | Unpaid Admins, no Cursor access |

Enterprise is priced by contact only. Leave every numeric field `null` if you
ever add an Enterprise row, and explain in `notes`.

No Team row exists in `data/plans.yaml` today. Adding one is a scope decision,
not a sourcing problem. Ask before you add one.

## Per-model token rates

`https://cursor.com/docs/models-and-pricing.md` prints two tables, both in USD
per 1M tokens.

**Cursor's own models**, in the Cursor Models pool:

| Model | Input | Cache read | Output |
|---|---|---|---|
| Grok 4.6 | 2 | 0.5 | 6 |
| Grok 4.6 (Fast) | 4 | 1 | 12 |
| Grok 4.5 | 2 | 0.5 | 6 |
| Grok 4.5 (Fast) | 4 | 1 | 18 |
| Composer 2.5 | 0.5 | 0.2 | 2.5 |
| Composer 2.5 (Fast) | 3 | 0.5 | 15 |

Cursor publishes no cache-write rate for these six. The column prints `-`.

**Third-party models** sit in the Other Models pool. Cursor states it charges
"these published API rates with no markup". The page lists about 40 models from
Anthropic, OpenAI, Google, Moonshot, and Z.ai.

Do not copy a third-party rate into a Cursor row. The provider of GPT-5.6 is
OpenAI, and the build script groups every table by `provider`. A resold rate
belongs on the originating provider's row, sourced from that provider's own
page.

## The Cursor Token Rate

On Teams and Enterprise plans, a third-party model request costs an extra $0.25
per 1M tokens on top of the model rate. First-party Grok and Composer requests
are exempt. Individual plans pay no token rate.

## Two surcharges that are easy to miss

- Regional data residency adds 10 percent to model pricing for eligible models.
- Max Mode, on legacy request-based plans only, bills at the model API rate plus
  20 percent.

Neither applies to a `data/plans.yaml` row today. Record them if you ever add an
API row.
