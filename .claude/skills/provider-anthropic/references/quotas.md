# Anthropic quotas and rate limits

Two different things live here. Keep them apart:

- A **plan usage limit** is the allowance a subscription gets. Anthropic states
  every one as a multiple, never as a number. It belongs in `limits` in
  `data/plans.yaml`.
- An **API rate limit** is requests or tokens per minute on the API. Anthropic
  publishes a full numeric table. It belongs in `data/rate_limits.yaml`.

## API rate limits

Source: `https://platform.claude.com/docs/en/api/rate-limits`, read 2026-08-28.

Anthropic measures three things per model class: requests per minute (RPM), input
tokens per minute (ITPM), and output tokens per minute (OTPM). It publishes no
combined tokens-per-minute figure. So set `tokens_per_minute: null` on every
Anthropic row. Set `requests_per_day: null` too; Anthropic publishes no daily
cap.

### Start tier

| Model class | RPM | ITPM | OTPM |
|---|---|---|---|
| Claude Fable 5 | 1000 | 500000 | 100000 |
| Claude Opus 5 | 1000 | 2000000 | 400000 |
| Claude Opus 4.x | 1000 | 2000000 | 400000 |
| Claude Sonnet 5 | 1000 | 2000000 | 400000 |
| Claude Sonnet 4.x | 1000 | 2000000 | 400000 |
| Claude Haiku 4.5 | 1000 | 2000000 | 400000 |

### Build tier

| Model class | RPM | ITPM | OTPM |
|---|---|---|---|
| Claude Fable 5 | 2000 | 1500000 | 300000 |
| Claude Opus 5 | 5000 | 5000000 | 1000000 |
| Claude Opus 4.x | 5000 | 5000000 | 1000000 |
| Claude Sonnet 5 | 5000 | 5000000 | 1000000 |
| Claude Sonnet 4.x | 5000 | 5000000 | 1000000 |
| Claude Haiku 4.5 | 5000 | 5000000 | 1000000 |

### Scale tier

| Model class | RPM | ITPM | OTPM |
|---|---|---|---|
| Claude Fable 5 | 4000 | 4000000 | 800000 |
| Claude Opus 5 | 10000 | 10000000 | 2000000 |
| Claude Opus 4.x | 10000 | 10000000 | 2000000 |
| Claude Sonnet 5 | 10000 | 10000000 | 2000000 |
| Claude Sonnet 4.x | 10000 | 10000000 | 2000000 |
| Claude Haiku 4.5 | 10000 | 10000000 | 2000000 |

Claude Haiku 3.5 also appears in each table, at a much lower limit. It is
retired. Skip it.

### Trap: Claude Fable 5 gets the smallest limit

Claude Fable 5 is the most expensive model and the most capable, and it carries
the lowest rate limit of the current lineup. At the Start tier it gets 500,000
ITPM against 2,000,000 for every other model. Do not assume the top model gets
the top limit. Copy each row.

### Trap: two rows are pooled buckets

`Claude Opus 4.x` and `Claude Sonnet 4.x` are not models. The page footnotes say:

- The Opus limit is a total across Claude Opus 4.8, 4.7, 4.6, and 4.5. Claude
  Opus 5 sits outside that bucket.
- The Sonnet 4.x limit is a total across Claude Sonnet 4.6 and Sonnet 4.5.
  Claude Sonnet 5 sits outside that bucket.

`AGENTS.md` wants one record per provider, model, and tier. So record the pooled
figure under one display model and state the pooling in `notes`:

```yaml
  notes: Anthropic shares this limit across Claude Opus 4.8, 4.7, 4.6, and 4.5.
```

Do not write three more rows at the same numbers for the other members. Do not
divide the pooled figure between them.

### Trap: two tiers publish no number

The page names five tiers. Only three carry figures.

| Tier | What it publishes | Write a row? |
|---|---|---|
| Evaluation | "limits below the standard limits", no number | No |
| Start | Full table | Yes |
| Build | Full table | Yes |
| Scale | Full table | Yes |
| Custom | "contact sales" | No |

Zero rows for Evaluation and Custom is the correct result. Do not add a row of
nulls to record the absence.

### Cached reads do not count

The page states that `cache_read_input_tokens` do not count toward ITPM on any
current model. Only `input_tokens` and `cache_creation_input_tokens` count. Say
so in `notes` on the Start-tier row of each model:

```yaml
  notes: Cached read tokens do not count toward this input limit.
```

One retired model breaks the rule. Claude Haiku 3.5 carries a dagger marker and
does count cached reads. It has no row here.

### Limits this repository does not track

The same page publishes four more limits. None fits the schema in `AGENTS.md`,
which is one row per model and tier.

- **Message Batches API**: RPM and queue depth, shared across all models.
- **Managed Agents**: 300 create requests per minute, 1200 read requests per
  minute, per organization.
- **Files API**: one per-organization limit, stated on another page.
- **Monthly spend caps**: $500 at Start, $1,000 at Build, $200,000 at Scale.

Add none of them without a scope decision.

## Plan usage limits

Anthropic publishes **no numeric quota** for any subscription plan. Every
statement is a multiple or a window. Read on 2026-08-28 from
`https://claude.com/pricing`:

- "every plan has usage limits that reset on a rolling five-hour session window,
  and paid plans add weekly limits on top"
- "Pro gives you at least 5x more usage per 5-hour session than Free"
- "Max gives you 5x or 20x more usage per 5-hour session than Pro"
- "Higher output limits for all tasks", on the Max card

### Trap: the Fable rule is a table row, not a sentence

An earlier version of this file quoted a sentence: "Claude Fable 5 is included on
Max plans at 50% of your weekly usage limit." That sentence is not on the page.
A fetch on 2026-08-28 found no such prose anywhere in the HTML.

Anthropic states the rule in the "Models and usage" comparison table instead.
Read the cells, not the prose:

| Plan | The `Fable` row prints |
|---|---|
| Free | nothing |
| Pro | `Usage credits` |
| Max 5x | `50% of weekly limits*` |
| Max 20x | `50% of weekly limits*` |

So Max unlocks Fable as part of the subscription, at half the weekly limit. Pro
does not. A Pro user reaches Fable only by turning on usage credits, which the
FAQ prices "at standard API rates". Put Fable in `models` on the two Max rows.
Keep it out of `models` on the Pro row.

The same table prints a `Context window` row: 200k on Free, Pro, Max 5x, and
Max 20x. The Team table prints 200k for Team and "500k on default model" for
both Enterprise tiers.

So a `limits` item is a sentence, not a number:

```yaml
  limits:
    - 20x the Pro usage
    - Higher output limits for all tasks
```

Two support articles look like they hold the missing numbers. Neither does.
`11647753-how-do-usage-and-length-limits-work` explains the mechanism and states
no figure. `9797557-usage-limit-best-practices` states no figure either. The
Anthropic page that says the most is `11049741-what-is-the-max-plan`, and it too
gives only multiples: "Max 5x provides five times more usage per session than the
Pro plan."

Do not fill this gap from a comparison site or a blog. Rule 4 in `AGENTS.md`
forbids it.

## The `rate limit` link on a plan row

An Anthropic plan row needs a `rate limit` entry that a reader can open. Use
`https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work`.
The page is qualitative, which is honest: it is what Anthropic publishes about
subscription limits.
