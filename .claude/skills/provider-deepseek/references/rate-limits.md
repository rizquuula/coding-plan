# DeepSeek rate limits

Read from `https://api-docs.deepseek.com/quick_start/rate_limit` on 2026-08-28.

## DeepSeek publishes a concurrency limit, not a rate limit

The page is titled "Rate Limit & Isolation". It publishes one number per model,
and that number is a **concurrency limit**, not a per-minute quota.

| Model | Concurrency limit |
|---|---|
| deepseek-v4-pro | 500 |
| deepseek-v4-flash | 2500 |
| deepseek-v4-flash-vision-exp | 2500 |

The page defines the unit: "A request counts as one concurrent connection from
the time it is sent until the model response is complete." It counts at the
account level, across every API key. Over the limit, the API returns HTTP 429.

The same table appears on `https://api-docs.deepseek.com/quick_start/pricing`.
Both pages state the same three numbers. Check that they still agree on every
refresh. Report a mismatch rather than picking a side.

## How this maps to `data/rate_limits.yaml`

The schema in `AGENTS.md` holds five numeric fields:
`requests_per_minute`, `input_tokens_per_minute`, `output_tokens_per_minute`,
`tokens_per_minute`, and `requests_per_day`.

A concurrency limit fits none of them. `AGENTS.md` covers this case: "When the
published limit is not a number, such as 'contact sales', leave the numeric
fields `null` and explain in `notes`."

So a DeepSeek row sets every numeric field to `null` and states the concurrency
number in `notes`:

```yaml
  notes: DeepSeek publishes a concurrency limit of 500 for this model, not a
    per-minute rate limit.
```

Do not convert a concurrency limit into requests per minute. The page gives no
duration per request, so any conversion is invented.

## What the page does not publish

- No requests per minute.
- No tokens per minute.
- No requests per day.
- No usage tiers. Every account starts at the same limit, so `tier` is
  `Default`.

The page states one time-based rule: "If the request has not started inference
after 10 minutes, the server will close the connection." That is a timeout, not
a quota. Leave it out of the row.

## Capacity expansion

The page says an account can request higher concurrency at no extra cost, and
that DeepSeek matches the number to the account's needs. It publishes no
expanded number, so there is no second tier to record.

For an expanded account, the same per-model limit then applies to each `user_id`
the account passes. That is an isolation rule, not a second published quota.

## Why DeepSeek carries rows and Zhipu does not

Zhipu publishes no numeric limit an agent can reach, so `data/rate_limits.yaml`
holds no Zhipu row. DeepSeek publishes a number on an open page, so DeepSeek
carries a row — one per model — with the number in `notes`.
