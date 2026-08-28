# Google page inventory

Every status below was checked on 2026-08-28. Re-check before you trust one.

## Pages that carry data this repository needs

| Page | Publishes | Tool |
|---|---|---|
| `https://gemini.google/us/subscriptions/` | Plan prices in USD, usage multipliers | `WebFetch` |
| `https://support.google.com/gemini/answer/16275805?hl=en` | Plan multipliers, per-plan context window | `WebFetch` |
| `https://ai.google.dev/gemini-api/docs/pricing` | API rates per 1M tokens, every model | `WebFetch` |
| `https://ai.google.dev/gemini-api/docs/models` | Model list, every model id | `WebFetch` |
| `https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash` | Context window, maximum output | `WebFetch` |
| `https://ai.google.dev/gemini-api/docs/rate-limits` | Usage tiers, spend limits, batch enqueued tokens | `WebFetch` |
| `https://jules.google/docs/usage-limits` | Jules tasks per day per plan | `WebFetch` |
| `https://docs.cloud.google.com/gemini/docs/quotas` | Code Assist requests per user per day, 2 requests per second | `WebFetch` |
| `https://cloud.google.com/products/gemini/pricing` | Code Assist per-seat price | `curl` |
| `https://codeassist.google/products/business` | The same per-seat price, in plain text | `curl` |
| `https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/` | Launch note, rounded prices | `WebFetch` |

`WebFetch` returned the full content of every page above except the two Code
Assist price pages. Both are large, and `WebFetch` truncates each one before the
price table. Use `curl` on those two. Google still needs no JavaScript bundle
trick.

## The Gemini Code Assist price pages

Checked 2026-08-28. Two Google pages print the same four figures.

| Edition | Monthly commitment | 12-month commitment |
|---|---|---|
| Gemini Code Assist Standard | $22.80 per seat per month | $19.00 per seat per month |
| Gemini Code Assist Enterprise | $54.00 per seat per month | $45.00 per seat per month |

`https://cloud.google.com/products/gemini/pricing` buries the table in an escaped
JSON payload, about 2.1 MB in. Grep the raw file for the price string, then read
the surrounding text:

```bash
curl -sL https://cloud.google.com/products/gemini/pricing -o gp.html
grep -o '\$[0-9][0-9.]*' gp.html | sort -u
```

`https://codeassist.google/products/business` is easier. It prints a plain table:

    Gemini Code Assist Standard (monthly) | $22.80 per user per month.
    Gemini Code Assist Standard (annual)  | $19 per user per month with an upfront annual commitment.

`https://codeassist.google/` redirects to `/products/business`.

The two pages disagree on how Google bills the annual term. The cloud page says
`All subscriptions are billed monthly.` The codeassist page says `with an upfront
annual commitment.` The 12-month total is the same either way.

## The per-model page

`https://ai.google.dev/gemini-api/docs/models` lists every model and links each
one to its own page:

    https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash
    https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash

Only the per-model page prints the token limits. All seven text models were read
on 2026-08-28 and every one printed the same three values.

| Model id | Input token limit | Output token limit | Supported inputs |
|---|---|---|---|
| `gemini-3.7-flash` | 1,048,576 | 65,536 | Text, Image, Video, Audio, PDF |
| `gemini-3.6-flash` | 1,048,576 | 65,536 | Text, Image, Video, Audio, PDF |
| `gemini-3.5-flash` | 1,048,576 | 65,536 | Text, Image, Video, Audio, PDF |
| `gemini-3.5-flash-lite` | 1,048,576 | 65,536 | Text, Image, Video, Audio, PDF |
| `gemini-3.1-flash-lite` | 1,048,576 | 65,536 | Text, Image, Video, Audio, PDF |
| `gemini-3.1-pro-preview` | 1,048,576 | 65,536 | Text, Image, Video, Audio, PDF |
| `gemini-3-flash-preview` | 1,048,576 | 65,536 | Text, Image, Video, Audio, PDF |

Write `1M` in `context_window`. 1,048,576 is 1M. Write `64K` in `max_output`.
Write `true` in `vision`, because the input list holds Image and Video.

A preview model's page URL keeps the `-preview` suffix. Drop it and the site
returns 404, not a redirect. Take the id from the model list page.

## `ai.google.dev` serves no markdown twin and no `llms.txt`

Both tricks from `AGENTS.md` fail here. Do not spend time on them.

| URL | What happens |
|---|---|
| `https://ai.google.dev/gemini-api/docs/pricing.md` | 200, and returns the same HTML page, byte for byte |
| `https://ai.google.dev/gemini-api/docs/rate-limits.md` | 200, and returns the same HTML page, byte for byte |
| `https://ai.google.dev/gemini-api/docs/models.md` | 200, and returns the same HTML page, byte for byte |
| `https://ai.google.dev/llms.txt` | 404 |

The `.md` suffix returns 200 because the site ignores it. A 200 is not evidence
of a markdown twin. Compare the byte count against the plain URL before you
believe one.

## Dead ends

Do not spend time on these. Each was tried and failed.

| URL | What happens |
|---|---|
| `https://one.google.com/about/google-ai-plans/` | 200, and the price element is empty. See `fetching.md`. |
| `https://one.google.com/about/google-ai-plans/?hl=en&gl=us` | Same empty price element. The locale query does nothing. |
| `https://one.google.com/us/about/google-ai-plans/` | 404. This site has no `/us/` path. |
| `https://gemini.google/intl/en_us/subscriptions/` | 302 back to `https://gemini.google/subscriptions/`, which returns IDR. |
| `https://aistudio.google.com/rate-limit` | Needs a login. Never cite it. |
| `https://antigravity.google/pricing` | 200, and prints no price and no number. |
| `https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro` | 404. A preview model keeps its `-preview` suffix. |
| `https://ai.google.dev/gemini-api/docs/models/gemini-3-flash` | 404. Same reason. |
| `https://codeassist.google/products/` | 200, and returns a 1,652-byte JavaScript shell with no text. |

`https://aistudio.google.com/rate-limit` is the only place Google publishes a
per-model RPM figure, and it needs an account. That is why
`data/rate_limits.yaml` holds no Google row.

## What each page does not say

- `ai.google.dev/gemini-api/docs/pricing` publishes no context window and no
  maximum output. The string `Context window` appears zero times. Read the
  per-model page instead.
- `ai.google.dev/gemini-api/docs/models` publishes no token limit either. It
  lists names, one-line descriptions, and endpoints.
- `ai.google.dev/gemini-api/docs/rate-limits` publishes no RPM, TPM, or RPD
  number for any model. See `quotas.md`.
- `ai.google.dev/gemini-api/docs/google-ai-plans` names Free, AI Pro, and AI
  Ultra, prints no price, and links to `one.google.com`, which is a dead end.
- `antigravity.google/pricing` names four tiers and prints `$0/month` for the
  free one only. The paid tiers say `More generous rate limits` with no number.
- No Google page publishes a parameter count for any Gemini model. Leave
  `total_params` and `active_params` as `null`.
- No per-model page states whether Google publishes the weights. See
  `data-recipes.md` for what to write in `open_weights`.
- No Google page states a generation speed in tokens per second. Ten pages were
  searched on 2026-08-28. The string appears zero times on every one.

## Google publishes only a monthly price

`gemini.google/us/subscriptions/` prints one price per plan, per month. It offers
no quarterly term and no yearly term. The word `annual` appears zero times. So
every Google record in `data/plans.yaml` carries exactly one `prices` entry with
`period: month`.

## Citation rule

`AGENTS.md` requires a page the provider owns. `ai.google.dev`, `gemini.google`,
`support.google.com`, `jules.google`, `blog.google`, and `docs.cloud.google.com`
all qualify. A login-gated AI Studio page does not qualify, because no reader can
open it to check your figure.
