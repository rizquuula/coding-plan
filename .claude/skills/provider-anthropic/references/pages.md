# Anthropic page inventory

Every status below comes from a fetch on 2026-08-28. Re-check before you trust
one.

Anthropic runs three hosts that publish data this repository needs:

| Host | Publishes | Reads with |
|---|---|---|
| `platform.claude.com` | API rates, rate limits, model specifications | `WebFetch`, and `.md` twins |
| `claude.com` | Subscription prices and plan features | `curl` |
| `support.claude.com` | Plan detail the marketing page omits | `WebFetch` |

All three are pages Anthropic owns, so all three pass rule 4 in `AGENTS.md`.

## Pages that carry data this repository needs

| Page | Publishes | Tool | Status |
|---|---|---|---|
| `https://platform.claude.com/docs/en/about-claude/pricing` | API rates per token, cache rates, batch rates, fast mode | `WebFetch` | 200 |
| `https://platform.claude.com/docs/en/api/rate-limits` | RPM, ITPM, and OTPM per model class per tier | `WebFetch` | 200 |
| `https://platform.claude.com/docs/en/about-claude/models/overview` | Context window, max output, model IDs | `WebFetch` | 200 |
| `https://claude.com/pricing` | Pro price, Max 5x price, Team seat prices, plan features | `curl` | 200 |
| `https://support.claude.com/en/articles/11049741-what-is-the-max-plan` | Max 5x and Max 20x monthly prices | `WebFetch` | 200 |
| `https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work` | How limits work, no numbers | `WebFetch` | 200 |
| `https://platform.claude.com/llms.txt` | Every documentation URL | `curl` | 200 |
| `https://claude.com/llms.txt` | Every marketing URL | `curl` | 200 |

## The markdown twins

Every page under `platform.claude.com/docs/` serves a markdown twin. Append `.md`
to the path:

    https://platform.claude.com/docs/en/api/rate-limits
    https://platform.claude.com/docs/en/api/rate-limits.md

Three twins returned 200 on 2026-08-28:

| Twin | Size |
|---|---|
| `docs/en/about-claude/pricing.md` | 43,663 bytes |
| `docs/en/api/rate-limits.md` | 32,814 bytes |
| `docs/en/models/overview.md` | 16,625 bytes |

`https://claude.com` serves no markdown twin. Its pages are HTML only.

## The two docs indexes

`https://platform.claude.com/llms.txt` lists every documentation URL, in `.md`
form. It returned 72,234 bytes and named 688 English pages. Read it first when a
page you expect is missing. `https://docs.claude.com/llms.txt` returns the same
bytes, so the two hosts serve one index.

`https://claude.com/llms.txt` is a separate, much smaller index of the marketing
site. It returned 4,146 bytes. Treat its entries with care; see the dead ends.

## Two URLs for the models page

`AGENTS.md` rows cite `docs/en/about-claude/models/overview`. That path serves
200. The page canonicalises itself to `docs/en/models/overview`, and
`platform.claude.com/llms.txt` lists only the short form. Both paths return the
same 16,625-byte body. Either citation is valid. Prefer the short form for a new
row.

## How to read `claude.com/pricing`

The page is a Webflow site of about 1.5 MB. Every price sits in the delivered
HTML, in an attribute named `data-plan`. You need no browser and no bundle.

```bash
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'
curl -sA "$UA" -L https://claude.com/pricing -o /tmp/claude_pricing.html
grep -o 'data-plan="[a-z0-9_]*"' /tmp/claude_pricing.html | sort -u
```

On 2026-08-28 that printed nine plan keys:

    free
    pro_annual
    pro_monthly
    max_5x_monthly
    team_annual_per_seat
    team_monthly_per_seat
    team_premium_annual_per_seat
    team_premium_monthly_per_seat

Note what is absent. There is no `max_20x` key of any kind.

To read a price, print the text around a key:

```bash
grep -o 'data-plan="pro_annual"[^>]*>[^<]*' /tmp/claude_pricing.html
```

`WebFetch` also reads this page, but not reliably. On 2026-08-28 the first call
returned "Command failed with no output" and a later call returned the prices.
The page is large enough to time out. Use `curl` when you need certainty.

## Trap: the page adds VAT to its own prices

`claude.com/pricing` ships a script titled "Location-Based Pricing". It fetches
`https://get.geojs.io/v1/ip/geo.json`, reads the visitor country, and applies EU
VAT to every element marked `data-tier-price` or `data-seat-price`. A manual
country selector overrides the detected country.

So a rendered figure can carry tax. The HTML source holds the tax-exclusive USD
figure. The page states this in a disclaimer: "Prices shown don't include
applicable tax."

Read the source. Never copy a figure from a screenshot or from a rendered view.

## Dead ends

Do not spend time on these. Each was tried on 2026-08-28.

| URL | What happens |
|---|---|
| `https://claude.com/pricing/max` | 301 to `/pricing`. It serves the same 1,483,852 bytes. `claude.com/llms.txt` lists it as a separate page, which misleads. |
| `https://support.claude.com/en/articles/9797557-usage-limit-best-practices` | 200, and no price and no numeric limit. |
| `https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work` | 200, and no numeric limit. It explains the mechanism only. |
| `https://platform.claude.com/settings/limits` | The console. It needs a login. Never cite it. |

## What each page does not say

- `claude.com/pricing` states no Max 20x price and no Max annual price.
- `claude.com/pricing` states no numeric usage quota for any plan. Every limit
  is a multiple of another plan.
- `platform.claude.com/docs/en/about-claude/pricing` states no context window for
  any single model. It states one rule: models from Claude 4.6 on carry the full
  1M context window.
- `platform.claude.com/docs/en/models/overview` compares four current models
  only. Legacy models get their own page under `docs/en/models/<model>/overview`.
  Nobody probed those pages on 2026-08-28.
- Anthropic publishes no parameter count for any model.

## Citation rule

`AGENTS.md` requires a page the provider owns. `platform.claude.com`,
`claude.com`, and `support.claude.com` all qualify. The Claude Console does not
qualify, because no reader can open it to check your figure.
