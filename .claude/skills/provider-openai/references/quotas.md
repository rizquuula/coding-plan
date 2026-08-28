# OpenAI quotas and rate limits

Two different things live here. Keep them apart:

- A **plan message limit** is how many messages a ChatGPT plan tier allows in a
  five-hour window. It belongs in `limits` in `data/plans.yaml`.
- An **API rate limit** is requests or tokens per minute on the API. It belongs
  in `data/rate_limits.yaml`.

OpenAI publishes both. Neither needs a login.

## Plan message limits

From `https://learn.chatgpt.com/docs/pricing`, read 2026-08-28. The page states
these as local messages per five-hour window.

| Model | Plus | Pro 5x | Pro 20x | Business |
|---|---|---|---|---|
| GPT-5.6 Sol | 10-100 | 50-500 | 200-2,000 | 10-100 |
| GPT-5.6 Terra | 25-200 | 125-1,000 | 500-4,000 | 25-200 |
| GPT-5.6 Luna | 250-2,000 | 1,250-10,000 | 5,000-40,000 | 250-2,000 |
| GPT-5.5 | 15-80 | 75-400 | 300-1,600 | 15-80 |
| GPT-5.4 | 20-100 | 100-500 | 400-2,000 | 20-100 |
| GPT-5.4 mini | 60-350 | 300-1,750 | 1,200-7,000 | 60-350 |

Write one `limits` item per model, under 12 words each:

```yaml
  limits:
    - Sol 50 to 500 messages per 5 hours
    - Terra 125 to 1000 messages per 5 hours
    - Luna 1250 to 10000 messages per 5 hours
```

Three facts the page prints alongside the table:

1. Local messages and cloud chats share the same five-hour window.
2. Weekly limits may also apply. The page states no weekly number.
3. A cloud chat runs on GPT-5.6 Sol and may use more allowance than a local
   message.

The table publishes no row for the Go tier. `data/plans.yaml` records Go as
`Sized for lightweight coding tasks`, which paraphrases the Go card subtitle,
"Use Codex for lightweight coding tasks". Do not invent a number for Go.

Pro 20x also gets unlimited ChatGPT Voice. The page states that a task started
through Voice still draws on the Codex usage budget.

## API rate limits: the model page holds the numbers

`https://developers.openai.com/api/docs/guides/rate-limits` looks like the right
page and is not. It publishes:

- Why rate limits exist.
- The metrics: RPM, RPD, TPM, TPD, IPM, and audio minutes per minute.
- The spend that promotes an account between usage tiers.
- The `x-ratelimit-*` response headers.
- Retry and backoff advice.

It publishes **no per-model RPM and no per-model TPM**. Its own closing line
sends you elsewhere: "To view a high-level summary of rate limits per model,
visit the models page."

Every number sits in the `## Rate limits` section at the foot of each model
page. Read `https://developers.openai.com/api/docs/models/<model-id>.md`.

## Usage tier thresholds

From the rate-limit guide, read 2026-08-28. This table qualifies an account for
a tier. It is not a rate limit.

| Tier | Qualification | Monthly usage limit |
|---|---|---|
| Free | Allowed geography | $100 / month |
| Tier 1 | $5 paid | $100 / month |
| Tier 2 | $50 paid | $500 / month |
| Tier 3 | $100 paid | $1,000 / month |
| Tier 4 | $250 paid | $5,000 / month |
| Tier 5 | $1,000 paid | $200,000 / month |

`data/rate_limits.yaml` uses `Tier 1` through `Tier 5` as the `tier` string,
which is how the model pages write them. Keep that spelling.

## Published rate limits, per model

Read 2026-08-28 from the three model pages. Every value is a plain integer, as
`AGENTS.md` requires.

GPT-5.6 Sol and GPT-5.6 Terra publish the same table:

| Tier | RPM | TPM | Batch queue limit |
|---|---|---|---|
| Tier 1 | 500 | 500000 | 1500000 |
| Tier 2 | 5000 | 1000000 | 3000000 |
| Tier 3 | 5000 | 2000000 | 100000000 |
| Tier 4 | 10000 | 4000000 | 200000000 |
| Tier 5 | 15000 | 40000000 | 15000000000 |

GPT-5.6 Luna publishes higher numbers:

| Tier | RPM | TPM | Batch queue limit |
|---|---|---|---|
| Tier 1 | 500 | 500000 | 5000000 |
| Tier 2 | 5000 | 2000000 | 20000000 |
| Tier 3 | 5000 | 4000000 | 40000000 |
| Tier 4 | 10000 | 10000000 | 1000000000 |
| Tier 5 | 30000 | 180000000 | 15000000000 |

Map the columns like this:

| Page column | Field |
|---|---|
| RPM | `requests_per_minute` |
| TPM | `tokens_per_minute` |
| Batch queue limit | no field. Drop it. |

TPM is a combined input and output limit. So set `tokens_per_minute` and leave
`input_tokens_per_minute` and `output_tokens_per_minute` as `null`.
`AGENTS.md` forbids setting both forms on one row.

The batch queue limit is a token count for queued batch jobs, not a per-minute
limit. `data/rate_limits.yaml` has no field for it. Do not force it into
`tokens_per_minute`.

## Trap: the heading differs between model pages

Sol and Terra head the section `### Standard`. Luna heads the same section
`### default`. The table shape is identical. Read the table, not the heading.

## Trap: long-context limits are not published

The rate-limit guide states that a long-context request has a separate rate
limit, and that you view it in the developer console. The console needs a login,
so no agent can read it and no reader can check it.

Write only the published table. Do not add a long-context row.

## Trap: shared limits

The guide states that some model families share one rate limit, and that the
organization limit page names them. That page needs a login. The published
per-model table is what this repository tracks.

## Compare with the other providers

OpenAI publishes a full per-model, per-tier table on a page with no login. Z.ai
publishes none. A provider with no rows is a finding, not a to-do. See
`.claude/skills/provider-zai/references/quotas.md`.
