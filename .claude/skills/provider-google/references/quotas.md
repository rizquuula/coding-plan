# Google quotas and rate limits

Two different things live here. Keep them apart:

- A **plan quota** is the allowance a subscription tier gets. Google publishes
  these as multipliers, and as absolute numbers for Jules. They belong in
  `limits` in `data/plans.yaml`.
- An **API rate limit** is requests or tokens per minute on the Gemini API.
  Google publishes no number an agent can reach. Nothing goes in
  `data/rate_limits.yaml`.

## Plan quotas are multipliers, not counts

From `https://support.google.com/gemini/answer/16275805?hl=en`, read 2026-08-28.

| Plan | Usage limit | Context window |
|---|---|---|
| No AI plan | Standard limits | 32k tokens |
| Google AI Plus | 2x higher than standard limits | 128k tokens |
| Google AI Pro | 4x higher than standard limits | 1 million tokens |
| Google AI Ultra | 5x or 20x higher than AI Pro limits | 1 million tokens |

The page never defines the standard limit as a number. So every multiplier stays
relative. Write it as the page writes it:

```yaml
  limits:
    - 5x the AI Pro usage limits
    - 1M token context window
```

The page also states that limits `refresh every 5 hours until you reach your
weekly limit`. It prints neither the 5-hour count nor the weekly count.

Do not multiply a multiplier by a guess. Do not take an absolute prompt count
from a comparison site. `AGENTS.md` rule 4 forbids it.

## Jules publishes absolute numbers

`https://jules.google/docs/usage-limits` is the one Google page that ties a
subscription tier to a count. Read 2026-08-28.

| Plan | Tasks per day | Concurrent tasks |
|---|---|---|
| Jules | 15 | 3 |
| Jules in Pro | 100 | 15 |
| Jules in Ultra | 300 | 60 |

The page states that Jules in Pro comes with the Google AI Pro plan, and Jules in
Ultra with the Google AI Ultra plan. It publishes no standalone price.

These are a good second `limits` item on an AI Pro or AI Ultra row. The page does
not split Ultra into the 5x and the 20x tier, so it states one figure for both.
Say so in `notes` before you put 300 on one Ultra row and not the other.

## Gemini Code Assist publishes a daily request quota

`https://docs.cloud.google.com/gemini/docs/quotas` covers the Google Cloud
product, not the consumer plan. Read 2026-08-28.

The 1,500 and 2,000 figures cover agent mode and the Gemini CLI only.

| Edition | Maximum requests per user per day, agent mode and CLI |
|---|---|
| Standard | 1,500 |
| Enterprise | 2,000 |

The same page publishes three quotas that do not vary by edition. They apply per
user, per Google Cloud project.

| Quota | Value |
|---|---|
| Requests per second | 2 |
| Requests per day, code generation and completion | 6,000 |
| Requests per day, chat and Cloud Assist panel | 960 |
| Local codebase awareness | 1,000,000 token context window |
| Code customization repositories | 20,000 |

**The 2 requests per second figure is a Google Cloud quota.** It covers Gemini
Code Assist and the Gemini CLI. It does not cover `ai.google.dev`. Never write it
into a Gemini API row.

The page warns that `one prompt might result in multiple model requests` in agent
mode, and that the daily limit aggregates across every model. It publishes no
price. Read `pricing.md` for the per-seat price, which sits on a different page.

Reaching this page needs one redirect hop.
`https://developers.google.com/gemini-code-assist/resources/quotas` returns a 301
to the `docs.cloud.google.com` URL above.

## API rate limits: no rows, on purpose

`https://ai.google.dev/gemini-api/docs/rate-limits` publishes **no RPM, TPM, or
RPD figure for any model**. It names the three dimensions, names four usage
tiers, and then says:

    Rate limits depend on a variety of factors (such as your usage tier) and can
    be viewed in Google AI Studio.

    Specified rate limits are not guaranteed and actual capacity may vary.

AI Studio needs a login, so no reader can check a figure taken from it. That is
why `data/rate_limits.yaml` holds zero Google rows. **That is the correct
result**, not a gap to fill. Do not add a row of nulls.

## What the rate-limits page does publish

Three tables, none of which fits the `data/rate_limits.yaml` schema.

**Usage tiers and the billing cap:**

| Usage tier | Qualification | Billing tier cap |
|---|---|---|
| Free | Active project or free trial | N/A |
| Tier 1 | Set up and link an active billing account | $250 |
| Tier 2 | Paid $100 + 3 days from first successful payment | $2,000 |
| Tier 3 | Paid $1,000 + 30 days from first successful payment | $20,000 - $100,000+ |

**Spend-based rate limits**, on a rolling 10-minute window:

| Usage tier | Spend rate limit per 10 minutes |
|---|---|
| Free | N/A |
| Tier 1 | $10 |
| Tier 2 | $50 |
| Tier 3 | $200 |

**Batch enqueued tokens**, per model and tier. A sample from the text-out models:

| Model | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Gemini 3.7 Flash | 3,000,000 | — | 1,000,000,000 |
| Gemini 3.6 Flash | 3,000,000 | 400,000,000 | 1,000,000,000 |
| Gemini 3.5 Flash | 3,000,000 | 400,000,000 | 1,000,000,000 |
| Gemini 3.5 Flash-Lite | 10,000,000 | 500,000,000 | 1,000,000,000 |
| Gemini 3.1 Pro Preview | 5,000,000 | 500,000,000 | 1,000,000,000 |
| Gemini 2.5 Pro | 5,000,000 | 500,000,000 | 1,000,000,000 |

The Tier 2 table omits Gemini 3.7 Flash. That is a gap on Google's page, not a
transcription error.

**A batch enqueued token count is a queue depth, not a rate.** It is not tokens
per minute and not tokens per day. `data/rate_limits.yaml` has no field for it.
Never write it into `tokens_per_minute`.

The page also states two figures that fit no field: `Concurrent batch requests:
100`, and priority inference at `0.3x the standard rate limit for each model and
tier`.

## Speed: Google publishes none

No Google page states a generation speed in tokens per second. Ten pages were
searched on 2026-08-28: the pricing page, the rate-limits page, the model list,
seven per-model pages, the subscriptions page, the Code Assist quota page, and
the Code Assist price page. The string appears zero times on every one.

Google writes `low-latency`, `high-throughput`, and `fastest`. It prints no
number beside any of those words. Never turn an adjective into a figure.

## Concurrency: three figures, three pages

| Figure | Page | Fits a field? |
|---|---|---|
| `Concurrent batch requests: 100` | Gemini API rate limits | No. It is a batch queue depth. |
| 3, 15, and 60 concurrent tasks | Jules usage limits | Yes, as a `limits` item on a plan row. |
| `Requests per second: 2` | Gemini Code Assist quotas | Yes, as a `limits` item on a Code Assist row. |

## Compare with the other providers

Anthropic, OpenAI, Moonshot, DeepSeek, and Alibaba all publish per-model numeric
limits, so they carry rows. Google and Zhipu do not. A provider with no rows is a
finding, not a to-do.
