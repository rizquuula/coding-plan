# Google prices

Read `fetching.md` first. It tells you how to get the plan prices off the page.

## Plan prices

From `https://gemini.google/us/subscriptions/`, read 2026-08-28. USD per month.
Google offers no quarterly and no yearly term.

| Plan card | Price | Usage line the page prints |
|---|---|---|
| Free | $0 | `$0/ month with a Google Account` |
| Google AI Plus | $4.99 | `Get 2x higher usage access than Free` |
| Google AI Pro | $19.99 | `Get 4x higher usage access than Free` |
| Google AI Ultra | $99.99 | `$99.99/ month: 5x higher usage limits vs. AI Pro` |
| Google AI Ultra | $199.99 | `$199.99 / month: 20x higher usage limits vs. AI Pro` |

Google AI Ultra is one card with two price points. The card header reads
`Starting at: $99.99 / month`. Keep the two tiers as two records. `AGENTS.md`
rule 8 forbids merging them.

## The trap: the blog rounds, the subscriptions page does not

`https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/`
announced the tiers on 2026-05-19 and rounds every figure:

- `We're launching a $100/month AI Ultra plan`
- `reducing the monthly price of our top-tier AI Ultra plan from $250 to $200`
- `Gemini Spark (AI Ultra $100 and $200; U.S. only)`
- `Project Genie (AI Ultra $200; global)`

The blog names the tiers `AI Ultra $100` and `AI Ultra $200`. The price page says
$99.99 and $199.99. Copy the price page. Cite the blog only for the feature list
and the launch date.

`data/plans.yaml` carried 100 and 200 on 2026-08-28. Those came from the blog.
Correct them to 99.99 and 199.99 the next time you refresh the rows.

The blog also says the AI Ultra 20x tier `Adds Gemini Omni`. The subscriptions
page contradicts that. It lists Gemini Omni Flash under Google AI Plus and under
Google AI Pro as well. Do not write Gemini Omni as an Ultra-only feature.

## Two coding surfaces sit inside the plans

The subscriptions page names both under Google AI Pro and Google AI Ultra:

- **Google Antigravity**, the agentic development platform. AI Pro gets
  `Entry rate limits to agent model in Google Antigravity`.
- **Jules**, the asynchronous coding agent. AI Pro gets `Higher limits`.

The blog states the AI Ultra $200 tier has `a 20X higher usage limit in the
Gemini app and Google Antigravity than our Pro plan`. That sentence is the only
place a Google page ties the multiplier to Antigravity.

## API rates per token

From `https://ai.google.dev/gemini-api/docs/pricing`, USD per 1M tokens, read
2026-08-28. Every figure below comes from the **Standard** table.

| Model | Model id | Input | Cached input | Output |
|---|---|---|---|---|
| Gemini 3.7 Flash | `gemini-3.7-flash` | 0.75 | 0.075 | 3.75 |
| Gemini 3.6 Flash | `gemini-3.6-flash` | 0.75 | 0.075 | 3.75 |
| Gemini 3.5 Flash | `gemini-3.5-flash` | 1.50 | 0.15 | 9.00 |
| Gemini 3.5 Flash-Lite | `gemini-3.5-flash-lite` | 0.30 | 0.03 | 2.50 |
| Gemini 3.1 Flash-Lite | `gemini-3.1-flash-lite` | 0.25 | 0.025 | 1.50 |
| Gemini 3.1 Pro Preview | `gemini-3.1-pro-preview` | 2.00 | 0.20 | 12.00 |
| Gemini 3 Flash Preview | `gemini-3-flash-preview` | 0.50 | 0.05 | 3.00 |
| Gemini 2.5 Pro | `gemini-2.5-pro` | 1.25 | 0.125 | 10.00 |
| Gemini 2.5 Flash | `gemini-2.5-flash` | 0.30 | 0.03 | 2.50 |
| Gemini 2.5 Flash-Lite | `gemini-2.5-flash-lite` | 0.10 | 0.01 | 0.40 |

`data/api_pricing.yaml` carries the first and the third rows.

An earlier version of this file printed `—` for the Flash-Lite cached rate. That
was wrong. Google rates context caching on every model above.

## The trap: audio input costs more

Four models charge a second, higher input rate for audio. `data/api_pricing.yaml`
holds one `input` field, so write the text rate and state the audio rate in
`notes`.

| Model | Text, image, video input | Audio input | Audio cached input |
|---|---|---|---|
| Gemini 3.1 Flash-Lite | 0.25 | 0.50 | 0.05 |
| Gemini 3 Flash Preview | 0.50 | 1.00 | 0.10 |
| Gemini 2.5 Flash | 0.30 | 1.00 | 0.10 |
| Gemini 2.5 Flash-Lite | 0.10 | 0.30 | 0.03 |

## Gemini Code Assist per-seat prices

Read 2026-08-28 from `https://cloud.google.com/products/gemini/pricing` and
confirmed on `https://codeassist.google/products/business`. USD per seat.

| Edition | Monthly commitment | 12-month commitment |
|---|---|---|
| Gemini Code Assist Standard | 22.80 per month | 19.00 per month |
| Gemini Code Assist Enterprise | 54.00 per month | 45.00 per month |

Google prints a discounted monthly rate for the 12-month term, not a term total.
`AGENTS.md` requires a term total in `amount`. Multiply by 12, then say so in
`notes`:

```yaml
  prices:
    - period: month
      amount: 22.80
    - period: year
      amount: 228.00
  notes: Google prints 19.00 per seat per month on a 12-month commitment, so the
    year amount is that rate times 12.
```

`WebFetch` truncates both price pages before the table. Use `curl`. See
`pages.md`.

The page also lists audio, image, text-to-speech, video, music, embedding, and
robotics models. This repository does not track those.

## The trap: three tables per model

Each model block prints three tables in this order:

1. **Standard** — the rate you copy.
2. **Batch** — half the Standard rate.
3. **Flex** — half the Standard rate, with small differences on caching.

For Gemini 3.5 Flash the three input rates are 1.50, 0.75, and 0.75. A read that
lands on the second table writes 0.75 where 1.50 is right.

## The trap: a dated rate that doubles in 2027

Gemini 3.7 Flash and Gemini 3.6 Flash both print two rates in one cell:

    Input price:  $0.75 through December 31, 2026. $1.50 starting January 1, 2027.
    Output price: $3.75 through December 31, 2026. $7.50 starting January 1, 2027.

Copy the rate that applies today. Record the future rate in `notes`:

    notes: Promotional rate through 2026-12-31, after which input costs 1.50 and
      output costs 7.50.

Re-check these two rows in January 2027. Nothing else in the file expires.

## Cache write and cache storage

Google publishes a cache-read rate and a **storage** rate per hour. It publishes
no cache-write rate. So `cache_write` is always `null`.

The storage rate does not fit any schema field. Put it in `notes`:

| Model | Cached input | Storage per 1M tokens per hour |
|---|---|---|
| Gemini 3.7 Flash | 0.075 | 0.50, then 1.00 from 2027-01-01 |
| Gemini 3.6 Flash | 0.075 | 0.50, then 1.00 from 2027-01-01 |
| Gemini 3.5 Flash | 0.15 | 1.00 |
| Gemini 3.5 Flash-Lite | 0.03 | 1.00 |
| Gemini 3.1 Flash-Lite | 0.025 | 1.00 |
| Gemini 3.1 Pro Preview | 0.20 | 4.50 |
| Gemini 3 Flash Preview | 0.05 | 1.00 |
| Gemini 2.5 Pro | 0.125 | 4.50 |

The storage rate expires with the token rate on the two promotional models. The
cached input rate on those two also doubles, from 0.075 to 0.15.

## Models that charge two input rates

Gemini 3.1 Pro Preview and the 2.5 Pro family split the rate at 200k tokens:

| Model | Input, prompts <= 200k | Input, prompts > 200k | Output, <= 200k | Output, > 200k |
|---|---|---|---|---|
| Gemini 3.1 Pro Preview | 2.00 | 4.00 | 12.00 | 18.00 |
| Gemini 2.5 Pro | 1.25 | 2.50 | 10.00 | 15.00 |

`data/api_pricing.yaml` holds one `input` field and one `output` field. Write the
rate for prompts up to 200k, then state the higher rate in `notes`. Neither model
has a row today.

## Grounding and search

Every Gemini 3.x model shares `5,000 free search requests per month`, then $14
per 1,000 requests. That is a per-request charge, not a token rate, so it fits no
schema field. Leave it out.
