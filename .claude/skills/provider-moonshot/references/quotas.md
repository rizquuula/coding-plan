# Moonshot quotas and rate limits

## API rate limits

`https://platform.kimi.ai/docs/pricing/limits` publishes one table. It applies to
the whole account, not to one model.

Read on 2026-08-28. The recharge column is the cumulative amount that unlocks
the tier.

| Tier | Recharge | Concurrency | RPM | TPM | TPD |
|---|---|---|---|---|---|
| Tier0 | 1 USD | 1 | 3 | 500000 | 1500000 |
| Tier1 | 10 USD | 50 | 200 | 2000000 | unlimited |
| Tier2 | 20 USD | 100 | 500 | 3000000 | unlimited |
| Tier3 | 100 USD | 200 | 5000 | 3000000 | unlimited |
| Tier4 | 1000 USD | 400 | 5000 | 4000000 | unlimited |
| Tier5 | 3000 USD | 1000 | 10000 | 5000000 | unlimited |

Four rules follow from that table.

1. TPM is a combined limit. Write it into `tokens_per_minute`. Leave
   `input_tokens_per_minute` and `output_tokens_per_minute` as `null`.
2. `requests_per_day` stays `null`. The page publishes a **token** cap per day,
   not a request cap. Put the Tier0 token cap in `notes`.
3. `data/rate_limits.yaml` has no field for concurrency. Put it in `notes` or
   drop it. Never bend it into another field.
4. The limit is account-wide, so every model on the account gets the same six
   numbers. Repeat the six rows per model and say so in `notes`.

The page also carries a notice that Moonshot plans to update these rules in
August. Re-read the page before you trust a stored number.

## Trap: the china page repeats the numbers in CNY

`https://platform.kimi.com/docs/pricing/limits` publishes the same six tier
names, the same RPM, the same TPM, and the same TPD. Only the recharge column
differs.

| Tier | Global recharge | China recharge |
|---|---|---|
| Tier0 | 1 USD | 0 CNY |
| Tier1 | 10 USD | 50 CNY |
| Tier2 | 20 USD | 100 CNY |
| Tier3 | 100 USD | 500 CNY |
| Tier4 | 1000 USD | 5000 CNY |
| Tier5 | 3000 USD | 20000 CNY |

So a Chinese page reads like confirmation of a global number and is not
evidence for one. Cite `platform.kimi.ai`. Every rate-limit row in the data
today cites that host.

## Membership quotas

Moonshot publishes **no numeric per-tier quota** for the membership. Three
sources were checked and none carries one:

| Source | What it gives |
|---|---|
| The `ListGoods` RPC | Prices only. Its `features` field returns empty. |
| `kimi-code/membership.html` | Quota rules in words, no number per tier. |
| `code/docs/en/` overview | One range across all tiers, not per tier. |

What the pages do state, in words:

- The quota refreshes every 7 days from the subscription date. Unused quota does
  not roll over.
- A rolling 5-hour window limits the request rate on top of the weekly quota.
- All logged-in devices and API keys on one account share the quota.
- Kimi Code shares the quota with the Kimi membership. A membership that hits
  its monthly total freezes Kimi Code until the reset.
- The overview page states "approximately 300–1,200 requests per 5-hour window,
  with up to 30 concurrent requests". That range spans every paid tier. It is
  not a per-tier figure.

`AGENTS.md` requires each `limits` item to be one quota statement under 12
words. Write the rules above, not a number you split out of the range.

## Model access per tier

`https://www.kimi.com/code/docs/en/kimi-code/models.html` is the only page that
maps a tier to a model. Read on 2026-08-28:

| Kimi Code model ID | Model | Available to |
|---|---|---|
| `k3` | Kimi K3 | Moderato and above; 1M context on Allegretto and above |
| `k3-256k` | Kimi K3 at 256K | Moderato and above |
| `kimi-for-coding` | Kimi K2.7 Code | all members |
| `kimi-for-coding-highspeed` | Kimi K2.7 Code HighSpeed | Allegretto and above |

Use that table to fill `models` on a `data/plans.yaml` row. Write the display
names, `Kimi K3` and `Kimi K2.7 Code`, not the Kimi Code IDs.

The page also states that HighSpeed runs about 6 times faster and spends about
3 times the quota, and that `k3` at 1M spends about twice the quota of
`k3-256k`. Those are ratios, not quotas. Do not turn a ratio into a number.

## Why this differs from the API platform

`https://platform.kimi.ai/docs/guide/product-plans` states it plainly: the API
platform bills pay-as-you-go and sells no subscription. The membership and the
API platform are separate products with separate quotas. A rate-limit tier is
not a plan tier. Never put a Tier number in a `data/plans.yaml` row.
