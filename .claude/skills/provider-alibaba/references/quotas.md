# Alibaba quotas, plans, and rate limits

Three different things live here. Keep them apart.

- A **plan quota** is the allowance a subscription buys. It belongs in `limits`
  in `data/plans.yaml`.
- An **API rate limit** is the RPM and TPM ceiling on the pay-as-you-go API. It
  belongs in `data/rate_limits.yaml`.
- A **free quota** is a one-off trial allowance. This repository does not track
  it.

## Trap: two subscription products, both with a Pro tier

| Product | Page slug | Billing unit | Region |
|---|---|---|---|
| Coding Plan | `coding-plan` | requests | not stated |
| Token Plan | `token-plan-overview` | Credits | Singapore only |

They are separate products with separate prices. Never mix a figure from one
into a row for the other. Name the product in the `plan` field.

## Coding Plan

From `https://www.alibabacloud.com/help/en/model-studio/coding-plan.md`, read
2026-08-28.

One tier is on sale.

| Tier | Price | Quota |
|---|---|---|
| Pro | $50 per month | 6,000 requests per 5 hours; 45,000 per week; 90,000 per month |

Models the plan unlocks, as the page lists them:

    Recommended: qwen3.7-plus, qwen3.6-plus, kimi-k2.5, glm-5, MiniMax-M2.5
    More:        qwen3.5-plus, qwen3-max-2026-01-23, qwen3-coder-next,
                 qwen3-coder-plus, glm-4.7

The page states that models outside that list are not supported.

### The Lite tier is discontinued

The page states two dates:

- 2026-03-20, 00:00:00 (UTC+08:00): the Lite tier stopped accepting new
  subscriptions.
- 2026-04-13: renewals and upgrades for the Lite tier stopped.

**The page prints no price for Lite.** The comparison table has a Pro column
only. So you cannot write a Lite row. `AGENTS.md` rule 3 forbids a guessed
price. If a Lite row ever exists, set `status: discontinued`, set
`discontinued_on: 2026-04-13`, and say so in `notes`, because the site does not
render `status`.

### Only a monthly term is published

`coding-plan` prints one price and one term. The purchase page at
`https://common-buy-intl.alibabacloud.com/coding-plan/` redirects to a login, so
no quarterly or yearly total is readable. Write one `prices` entry with
`period: month`.

The China page adds a first-month offer of ¥39.90 against a ¥200 list price.
The English page states no such offer. Do not carry a CNY offer into a USD row.

## Token Plan

From `https://www.alibabacloud.com/help/en/model-studio/token-plan-overview.md`,
read 2026-08-28. The page states that Token Plan runs in the Singapore region
only.

Personal Edition:

| Tier | List price | Limited-time price | 7-day quota | Concurrent agents |
|---|---|---|---|---|
| Lite | $8 per month | $6 per month | 2,500 Credits | 1-2 |
| Standard | $25 per month | $18 per month | 10,000 Credits | 3-4 |
| Pro | $80 per month | $68 per month | 40,000 Credits | 6-8 |
| Extra Bundle | $15 per bundle per month | — | 20,000 Credits per bundle | — |

Team Edition:

| Tier | List price | Limited-time price | Monthly quota |
|---|---|---|---|
| Standard seat | $30 per seat per month | $20 | 25,000 Credits per seat |
| Pro seat | $100 per seat per month | $75 | 100,000 Credits per seat |
| Max seat | $200 per seat per month | — | 250,000 Credits per seat |
| Shared quota pack | $700 per pack per month | — | 625,000 Credits per pack |

Copy the list price into `amount`, the same rule as `pricing.md` states for API
rates. Say in `notes` that a limited-time price applies.

**No Alibaba row exists in `data/plans.yaml` today.** Adding one is a scope
decision, not a sourcing problem. Ask before you add a Team row or an Extra
Bundle row, and never mix a Team seat figure into a Personal row.

## API rate limits

From `https://www.alibabacloud.com/help/en/model-studio/rate-limit.md`, read
2026-08-28.

The page states three rules:

1. Rate limiting applies at the Alibaba Cloud account level. Usage of every RAM
   user, workspace, and API key under the account is combined.
2. Each model has its own limit.
3. TPM counts input tokens plus output tokens. The service may also enforce
   RPS = RPM / 60 and TPS = TPM / 60.

### Trap: a region is not a usage tier

Alibaba publishes one limit per model per region. It publishes no Free, Tier 1,
or Tier 2 ladder. The `tier` field in `data/rate_limits.yaml` is required, so the
existing rows put the region name there: `Singapore`, `US (Virginia)`,
`China (Beijing)`. Keep that convention. Say in `notes` that the split is by
region.

Because TPM is a combined limit, set `tokens_per_minute` and leave
`input_tokens_per_minute` and `output_tokens_per_minute` as `null`. `AGENTS.md`
forbids setting both forms on one row.

### Trap: a model missing from a region table has no limit there

The region tables do not list the same models. Read the table for each region
you write a row for. Do not copy a figure across regions.

On 2026-08-28, `qwen-max` appeared in the Singapore table and the China
(Beijing) table. It did **not** appear in the US (Virginia) table.

| Model | Region | RPM | TPM |
|---|---|---|---|
| `qwen-max` | Singapore | 600 | 1,000,000 |
| `qwen-max` | China (Beijing) | 1,200 | 1,000,000 |
| `qwen-max` | US (Virginia) | not listed | not listed |
| `qwen3-max` | Singapore | 600 | 1,000,000 |
| `qwen3-max` | US (Virginia) | 600 | 1,000,000 |
| `qwen3.8-max` | Singapore | 15,000 | 2,000,000 |
| `qwen3.8-max` | US (Virginia) | 30,000 | 5,000,000 |
| `qwen3-coder-plus` | Singapore | 2,400 | 2,000,000 |
| `qwen3-coder-plus` | US (Virginia) | 2,400 | 2,000,000 |
| `qwen3-coder-plus` | China (Beijing) | 5,000 | 5,000,000 |
| `qwen3-coder-plus` | Germany (Frankfurt) | 5,000 | 5,000,000 |
| `qwen3-coder-flash` | Singapore | 600 | 5,000,000 |
| `qwen3-coder-flash` | US (Virginia) | 1,200 | 1,000,000 |

`data/rate_limits.yaml` holds a row `alibaba-qwen-max-us-virginia` with 600 RPM
and 1,000,000 TPM. The page does not support it. Those are the `qwen3-max`
figures for that region. Delete the row, or change its `model` to `qwen3-max`
and add a matching row to `data/api_pricing.yaml`.

### Trap: a dated snapshot has a much lower limit

A snapshot ID such as `qwen3-max-2025-09-23` carries its own limit, often far
below the alias. On 2026-08-28 the alias `qwen3-max` allowed 600 RPM in
Singapore, and the snapshot `qwen3-max-2025-09-23` allowed 60 RPM. Match the
model ID character for character.

### Writing the numbers

`AGENTS.md` requires plain integers. The page prints `1,000,000`. Write
`1000000`.
