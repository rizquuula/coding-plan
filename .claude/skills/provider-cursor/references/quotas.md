# Cursor quotas and rate limits

Two different things live here. Keep them apart:

- A **plan limit** is what a subscription tier includes. Cursor publishes these
  as multipliers, never as absolute numbers. They belong in `limits` in
  `data/plans.yaml`.
- An **API rate limit** is requests or tokens per minute on a per-model API.
  Cursor sells no per-model API. Nothing goes in `data/rate_limits.yaml`.

Every figure below was read on 2026-08-28.

## The two usage pools

`https://cursor.com/docs/models-and-pricing.md` states that most plans include
two monthly pools:

- **Cursor Models** — Cursor Grok 4.6, Grok 4.5, and Composer 2.5.
- **Other Models** — third-party models, charged at the model's API price.

Pro, Pro+, and Ultra include both pools. Start includes the Cursor Models pool
only. Each pool resets with the monthly billing cycle. Unused usage does not
roll over.

## Plan limits, as Cursor states them

Cursor publishes no credit count and no request count for any tier. It publishes
a multiplier against a baseline tier. These strings are on
`https://cursor.com/pricing`:

| Tier | Published limit |
|---|---|
| Hobby | Limited Agent requests |
| Pro | Extended limits on Agent |
| Pro+ | 3x Pro limits on Agent |
| Ultra | 20x Pro limits on Agent |
| Teams Standard | The standard Teams allowance |
| Teams Premium | 5x Standard limits on Agent |

Two more strings sit in the same page markup and are not shown by default:
`3x usage on frontier models` for Pro+ and `20x usage on frontier models` for
Ultra.

`curl` on `https://cursor.com/pricing` returns every one of these strings, for
all five paid tiers, even though the page prices one tier at a time. Read the
feature lines from there. Confirmed 2026-08-28. Each tier also prints
`Generous limits for Grok`, and Pro+ and Ultra print a Grok Bot line.

## Which models a paid tier unlocks

`help/models-and-usage/available-models.md` settles this in one sentence:
"Hobby users have access to a smaller set, while paid plans unlock all models."

So a model marked "Hidden by default" in the pricing table is still included.
That note describes the model picker, not entitlement. Claude 4.5 Sonnet and
Claude 4.6 Opus carry it too. Kimi and GLM belong in `models` on every paid
individual tier and both Teams seats.

Write a multiplier as `limits` text, under 12 words:

```yaml
  limits:
    - 3x the Pro agent limits
```

The baseline is not a number Cursor publishes, so a multiplier is the whole
truth here. Do not convert it into a request count.

## The absolute numbers are behind a login

`https://cursor.com/help/models-and-usage/usage-limits.md` names the pools and
then points at `https://cursor.com/dashboard/spending` for the amounts. That
dashboard needs an account. `AGENTS.md` rule 4 forbids citing it, because no
reader can open it to check your figure.

The nearest public figure is a spending guide on
`https://cursor.com/docs/models-and-pricing.md`. It is advice, not an
allowance:

- Daily Tab users: typically stay within included usage.
- Daily Agent users: typically $60 to $100 per month of total usage.
- Power users: often $200 or more per month.

Do not write those figures into `limits`. They describe demand, not supply.

## On-demand billing

Every paid individual tier can continue past its included usage. Cursor bills
the extra at the same API rates, monthly, in arrears. Requests are never
downgraded in quality or speed. On-demand usage is on by default for Teams.

That is worth one `limits` line, such as:

```yaml
    - On-demand billing past the included usage
```

## API rate limits: no rows, on purpose

Cursor **does** publish rate limits, on `https://cursor.com/docs/api`. Read the
table before you decide it fits:

| API | Endpoint type | Rate limit |
|---|---|---|
| Admin API | Most endpoints | 20 requests/minute |
| Admin API | `filtered-usage-events` | 60 requests/minute |
| Admin API | `user-spend-limit` | 250 requests/minute |
| Analytics API | Most team-level endpoints | 100 requests/minute |
| Analytics API | `conversation-insights` | 20 requests/minute |
| Analytics API | By-user endpoints | 50 requests/minute |
| AI Code Tracking API | All endpoints | 20 requests/minute per endpoint |
| Bugbot API | `/bugbot/review` | 30 requests/minute |
| Bugbot API | `/bugbot/review` with `dryRun` | 10 requests/minute |
| Cloud Agents API | All endpoints | Standard rate limiting |

Every one of these governs a team administration endpoint. None governs model
inference. The limits are enforced per team and reset every minute.

`data/rate_limits.yaml` needs a `model` that matches a row in
`data/api_pricing.yaml`. No Cursor model row exists, and none of these limits
belongs to a model. So `data/rate_limits.yaml` holds zero Cursor rows. **That is
the correct result**, not a gap to fill.

Do not add a row of nulls to record the absence. Do not map `Admin API` into the
`model` field. It is not a model.

The `rate limit` link on a Cursor plan row points at
`https://cursor.com/help/models-and-usage/usage-limits`. That page is
qualitative, which is honest: it is what Cursor publishes about plan limits.

## Compare with the other providers

On 2026-08-28, `data/rate_limits.yaml` carried rows for four providers only:
Alibaba (Qwen), Anthropic, DeepSeek, and Moonshot (Kimi). Cursor is not among
them, and should not be. A provider with no rows is a finding, not a to-do.
