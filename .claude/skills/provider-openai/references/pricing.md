# OpenAI prices and rates

Read `pages.md` first. It tells you which host answers and which one returns 403.

Two separate things live here. Keep them apart:

- A **plan price** is what a ChatGPT subscription costs per month. It sits on
  `https://learn.chatgpt.com/docs/pricing`.
- An **API rate** is the price per 1M tokens. It sits on
  `https://developers.openai.com/api/docs/pricing` and on each model page.

## Plan prices

Read on 2026-08-28 from `https://learn.chatgpt.com/docs/pricing.md`. USD per
month. The page publishes no yearly price for an individual plan tier.

| Plan tier | Price | Where the page states it |
|---|---|---|
| Free | 0 | `PricingCard name="Free" price="$0"` |
| Go | 8 | `PricingCard name="Go" price="$8"` |
| Plus | 20 | `PricingCard name="Plus" price="$20"` |
| Pro 5x | 100 | Card prints `From $100`; the ChatGPT Voice section confirms 100 |
| Pro 20x | 200 | ChatGPT Voice section only |
| Business | 20 per seat, billed yearly | Card footnote: 25 per seat when billed monthly |
| Enterprise & Edu | none | Card says "Contact sales" |

## Trap: one card holds two Pro tiers

The Pro card prints one price, `From $100`, and the subtitle "Choose 5x or 20x
higher rate limits than Plus". It never prints 200.

The ChatGPT Voice section, further down the same page, prints both:

    - **Plus:** Approximately 15–30 minutes
    - **Pro 5x ($100/month):** Approximately 1–2.5 hours
    - **Pro 20x ($200/month):** Unlimited voice access

The plan message table on the same page also names the two columns `Pro 5x` and
`Pro 20x`. Those two sources are what make 100 and 200 safe to write.

`data/plans.yaml` splits Pro into two records, `openai-chatgpt-pro-5x` and
`openai-chatgpt-pro-20x`. Rule 8 in `AGENTS.md` requires that split. Do not
merge them back into one record.

## Trap: Free and Business have no row yet

`data/plans.yaml` holds four OpenAI records: Go, Plus, Pro 5x, and Pro 20x. The
page also publishes Free at 0 and Business at 20 per seat. Adding either is a
scope decision, not a sourcing problem. Ask before you add one.

Never mix a Business seat price into an individual plan record.

## Business: two rates in one card

The Business card prints the annual rate in the headline and the monthly rate in
the footnote. Read on 2026-08-28:

    <PricingCard
      name="Business"
      price="$20"
      interval="/ user / month*"
      footnoteLabel="*2+ users, billed annually. $25 per user per month when billed monthly."
    />

Two consequences for `data/plans.yaml`:

1. The `month` amount is 25, not 20. 20 is the annual rate.
2. The page prints no annual term total. Multiply 20 by 12 and write `year: 240`.
   `AGENTS.md` requires you to say so in `notes`.

Free is easier. The card prints `price="$0"`, so `month: 0` is exact.

## Trap: the Free and Go cards carry no bullets

Both cards are self-closing tags. Neither lists a model. The message-limit table
starts at Plus, and the feature matrix starts at Plus. So no page on this host
ties a model list to the Free tier or the Go tier.

`openai-chatgpt-go` in `data/plans.yaml` lists three GPT-5.6 models anyway. That
claim is unsourced. Flag it rather than copying it into a new Free record.

## API rates: the four service tiers

`https://developers.openai.com/api/docs/pricing` prints four tables, one per
service tier. The rendered page shows one tab at a time. The `.md` twin prints
all four, each under its own heading.

| Service tier | Heading in the `.md` | Relation to Standard |
|---|---|---|
| Standard | `### Standard pricing data` | The rate this repository tracks |
| Batch | `### Batch pricing data` | Half of Standard |
| Flex | `### Flex pricing data` | Half of Standard |
| Fast mode | `### Fast pricing data` | Double Standard |

**Take the Standard table.** An agent that grabs the first table it parses can
write half the right rate and never notice.

OpenAI renamed Priority processing to Fast mode on 2026-07-30. Both
`service_tier: "priority"` and `service_tier: "fast"` still work in the API.

## API rates: short context and long context

Every row in every table carries eight columns, not four:

    Short context input | Short context cached input | Short context cache writes | Short context output |
    Long context input  | Long context cached input  | Long context cache writes  | Long context output

**Take the short context columns.** Long context applies to a prompt above
272,000 input tokens. Each model page states the rule:

    Prompts with >272K input tokens are priced at 2x input and 1.5x output for
    the full request.

## Standard rates, short context

Read on 2026-08-28. USD per 1M tokens. `data/api_pricing.yaml` carries these
three rows.

| Model | Input | Cached input | Cache write | Output |
|---|---|---|---|---|
| gpt-5.6-sol | 4.00 | 0.40 | 5.00 | 20.00 |
| gpt-5.6-terra | 2.00 | 0.20 | 2.50 | 12.00 |
| gpt-5.6-luna | 0.20 | 0.02 | 0.25 | 1.20 |

The long context rates, for the same three models, on the same page:

| Model | Input | Cached input | Cache write | Output |
|---|---|---|---|---|
| gpt-5.6-sol | 8.00 | 0.80 | 10.00 | 30.00 |
| gpt-5.6-terra | 4.00 | 0.40 | 5.00 | 18.00 |
| gpt-5.6-luna | 0.40 | 0.04 | 0.50 | 1.80 |

The pricing page also lists GPT-5.5, GPT-5.4, GPT-5.2, GPT-5.1, GPT-5, GPT-4.1,
GPT-4o, the o-series, and the legacy models. It lists image, video, audio,
realtime, transcription, embedding, and tool pricing, which this repository does
not track. Add a model row only when the model belongs in a coding-plan tracker.

## The Codex row sits in a different table

`gpt-5.3-codex` is the only Codex-branded model with a published API rate. It is
not in the Standard table at the top of the page. It sits far down, in a
four-column grouped table under a `Specialized models` group:

    | Category | Model | Input | Cached input | Output |
    | Codex | gpt-5.3-codex | $1.75 | $0.175 | $14.00 |

That table has no cache-write column, so `cache_write` is `null`. The Fast mode
copy of the same table prints double: $3.50, $0.35, $28.00.

Before you add the row, read the deprecation note on
`https://learn.chatgpt.com/docs/models`:

    The `gpt-5.2` and `gpt-5.3-codex` models are already deprecated in Codex when
    you sign in with ChatGPT.

The API still serves and prices the model. Codex users cannot select it. Adding
it is a scope decision. Ask before you add it.

## gpt-oss models carry no rate at all

`gpt-oss-120b` and `gpt-oss-20b` appear on no pricing table. `gpt-oss-120b`
publishes a rate-limit table whose every cell reads 0, across all five tiers.
OpenAI does not serve these models through its own API. They fit
`data/models.yaml` only. Never write an `data/api_pricing.yaml` row or a
`data/rate_limits.yaml` row for one.

## OpenAI does publish a cache-write rate

Every GPT-5.6 row prints a cache-write rate, so `cache_write` is a real number,
not `null`. Each model page states the rule that produces it:

    Cache writes are billed at 1.25x the uncached input token rate.

Check the rule against the table. On 2026-08-28, 4.00 × 1.25 = 5.00 for Sol,
2.00 × 1.25 = 2.50 for Terra, and 0.20 × 1.25 = 0.25 for Luna. All three agree.

Older models such as GPT-5.5 and GPT-4o print `-` in the cache-write column.
Write `null` for those.

## The cross-check that makes a rate safe

Each model page repeats the input, cached input, and output rate in its own
`### Text tokens` table. Two OpenAI pages agreeing is what makes a rate safe to
write. Run this check every refresh.

From `https://developers.openai.com/api/docs/models/gpt-5.6-sol.md`:

| Metric | Price | Unit |
|---|---|---|
| Input | $4 | 1M tokens |
| Cached input | $0.4 | 1M tokens |
| Output | $20 | 1M tokens |

The model page prints no cache-write rate. Read that from the pricing page, then
confirm it against the 1.25x rule above.

When the pricing page and the model page disagree, one page is stale. Report it
rather than picking a side.

## Trap: credits are not dollars

`https://learn.chatgpt.com/docs/pricing` prints a second rate card, headed
"Credits per 1M tokens":

| Model | Input | Cached input | Output |
|---|---|---|---|
| GPT-5.6 Sol | 100 credits | 10 credits | 500 credits |
| GPT-5.6 Terra | 50 credits | 5 credits | 300 credits |
| GPT-5.6 Luna | 5 credits | 0.5 credits | 30 credits |

A credit is a consumption unit inside a ChatGPT plan. It is not USD. The page
states that a GPT-5.6 message averages 5 to 30 credits.

Never copy a credit figure into `data/api_pricing.yaml`. This repository has no
field for a credit rate.

## Promotional pricing

Both pages carry the same sentence about GPT-5.6 Sol:

    GPT-5.6 Sol's promotional pricing is available at least through November 21, 2026.

`data/api_pricing.yaml` records that in `notes` on the Sol row. Re-check the Sol
rate after that date.

The Sol model page also states the size of the cut: a 20 percent reduction in
input pricing and a 33 percent reduction in output pricing, against GPT-5.5.

## Aliases

Three aliases route to a GPT-5.6 model and bill at that model's rate:

| Alias | Points at |
|---|---|
| `gpt-5.6` | `gpt-5.6-sol` |
| `daybreak-blue-latest` | `gpt-5.6-sol` |
| `daybreak-red-latest` | `gpt-5.6-cyber` |

The pricing page states that OpenAI repoints these aliases as new models ship,
and adjusts the price to match. Track the concrete model ID, not the alias.
