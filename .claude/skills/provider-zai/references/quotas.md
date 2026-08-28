# Z.ai quotas and rate limits

Two different things live here. Keep them apart:

- A **plan quota** is the credit allowance a subscription tier gets. Z.ai
  publishes these. They belong in `limits` in `data/plans.yaml`.
- An **API rate limit** is requests or tokens per minute on the API. Z.ai
  publishes no number an agent can reach. Nothing goes in
  `data/rate_limits.yaml`.

## Individual plan quotas

From `https://docs.z.ai/devpack/overview`, read 2026-08-28.

| Tier | Credits per 5 hours | Credits per week |
|---|---|---|
| Lite | 2,000 | 10,000 |
| Pro | 12,000 | 60,000 |
| Max | 28,000 | 140,000 |

Write them as two `limits` items, under 12 words each:

```yaml
  limits:
    - 12000 credits per 5 hours
    - 60000 credits per week
```

## The cross-check that makes these safe

`https://z.ai/subscribe` states the same quotas as multiples: Lite is
`10,000 Credits / week`, Pro is `6× Lite usage`, Max is `14× Lite usage`.

- 6 × 10,000 = 60,000, which matches Pro.
- 14 × 10,000 = 140,000, which matches Max.

Two provider pages agreeing is what makes the absolute number safe to write.
Run this check every refresh. When the multiple and the absolute number
disagree, one page is stale. Report it rather than picking a side.

## Team seat quotas

From `https://docs.z.ai/devpack/teamplan`.

| Seat | Credits per 5 hours | Credits per week |
|---|---|---|
| Standard | 15,000 | 66,000 |
| Premium | 35,000 | 155,000 |

`data/plans.yaml` carries both seats as rows: `Standard Seat` and
`Premium Seat`. Their quotas come from this page. Their prices come from the
public JSON endpoint, because this page publishes no price. See `pricing.md`.

The Premium Seat row also lists two non-numeric benefits in `limits`: early
access to the latest models, and priority resource allocation at peak hours.
Both are stated on the teamplan page.

## Off-peak

`data/plans.yaml` records on the Lite row that off-peak usage costs half rate.
That was read from the devpack pages. It is not stated per tier, so it sits on
Lite only. Do not copy it to Pro or Max without reading a page that says so.

## API rate limits: no rows, on purpose

Z.ai publishes **no numeric API rate limit** on any page an agent can reach.

- `https://docs.z.ai/guides/overview/rate-limits` returns 404.
- `https://docs.z.ai/api-reference/rate-limit` and its `.md` twin both redirect
  to `https://z.ai/manage-apikey/rate-limits`, which needs a login.
- `https://docs.z.ai/devpack/usage-policy` ranks concurrency as
  `Max > Pro > Lite` and prints no number.

So `data/rate_limits.yaml` holds zero Zhipu rows. **That is the correct
result**, not a gap to fill.

## What the console page would show

The paths above all fail, but the console page's own JavaScript bundle says what
the page renders. Reading it settles the question.

The table has three columns: "Model type", "Model name", and **"Concurrency
limit"**. The concurrency column binds to a field named `rpm`. The data comes
from `/biz/model/rate-limit`, which returns
`{"code":1001,"msg":"Authentication parameter not received in Header, unable to
authenticate"}`.

Two conclusions follow:

1. The limit Z.ai enforces is a **per-model concurrency limit**, and it is
   specific to an account. The field name `rpm` is misleading. It is not
   requests per minute and not tokens per minute. `data/rate_limits.yaml` has no
   column for concurrency.
2. The figure is per account, so no public page can state it. There is no
   number to find. Stop looking.

This is settled. Do not re-derive it.

## Z.ai publishes no speed figure

Every fetched doc was searched for tokens per second, TPS, output speed,
generation speed, throughput, latency, and TTFT. **Zero hits.**

Z.ai publishes efficiency ratios instead. The GLM-5.3-Flash page states that the
model reduces attention compute by 3.0x and KV cache size by 4.4x against
GLM-5.3. A ratio against another model is not a speed.

No dataset in this repository has a speed field anyway. So this changes nothing
and costs nothing. It is recorded so the next agent does not spend time hunting.

Do not add a row of nulls to record the absence. Do not take a number from a
comparison site, a blog, or an aggregator. `AGENTS.md` rule 4 forbids it, and a
reader cannot verify a figure behind a login.

The `rate limit` link on a Zhipu plan row points at
`https://docs.z.ai/devpack/usage-policy`. That page is qualitative, which is
honest: it is what Z.ai publishes about limits.

## Compare with the other providers

Anthropic, OpenAI, Moonshot, and Alibaba all publish per-model numeric limits,
so they carry rows. Google and Zhipu do not. A provider with no rows is a
finding, not a to-do.
