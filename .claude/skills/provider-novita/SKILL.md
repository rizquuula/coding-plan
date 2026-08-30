---
name: provider-novita
description: How to source Novita prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh a Novita row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Novita, Novita AI, novita.ai, docs.novita.ai, api-server.novita.ai, Novita Coding, the Novita coding plan, or the Lite, Pro, and Max resource packs. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Novita — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Novita, so you do not repeat work that already failed.

Everything here was checked on 2026-08-30. Re-check a status before you trust it.

**The coding-plan page states no price in its HTML.** `WebFetch` on
`https://novita.ai/coding-plan` returns the page and no number. So does `curl`.
The prices come from a JSON endpoint the page calls at run time. Run
`python3 scripts/read_coding_plan.py`, or call the endpoint yourself:

    curl -sS -A "Mozilla/5.0" https://api-server.novita.ai/v1/product/resource-pack-specs/list

That one line is the most valuable thing in this skill. It needs no key.

## Constants

Write the provider as `Novita` in all five data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

`region` is `global`. `price_currency` and `currency` are `USD`. Novita prints
no other currency. The Alipay fields in the plan JSON are empty strings.

Novita sells the subscription as **Novita Coding**. It has three tiers: Lite,
Pro, and Max. The term is monthly only. There is no quarterly and no yearly
price.

Novita resells other companies' models. A Novita row describes Novita's price
for that model, not the model owner's price. Nine models sit in the coding plan.

## Where each value lives

| You need | Source | Tool |
|---|---|---|
| Plan tier prices, quotas, per-tier RPM and TPM | `https://api-server.novita.ai/v1/product/resource-pack-specs/list` | `curl` or `scripts/read_coding_plan.py` |
| Which nine models the plan covers | the same endpoint, `deductRules[].displayName` | `curl` |
| Per-model API rates | the same endpoint, `deductRules[].priceInfo.*Decimal` | `curl` |
| Per-model API rates, second source | `https://api.novita.ai/openai/v1/models` | `curl` |
| Per-model rates for a reader | `https://novita.ai/pricing` | `curl` |
| Context window, max output, modalities | `https://api-server.novita.ai/v1/product/model/list` | `curl` |
| One model's specification for a reader | `https://novita.ai/models/model-detail/<slug>` | `WebFetch` or `curl` |
| Rate limits per model, tiers T1 to T5 | `https://api-server.novita.ai/v1/product/model/list`, `quota_items` | `curl` |
| How an account reaches T1 to T5 | `https://novita.ai/docs/guides/llm-rate-limits.md` | `curl` |
| Quota unit, cache billing, fallback billing | `https://novita.ai/docs/guides/LLM-FAQ.md` | `curl` |
| The plan terms and the FAQ text | the page's JavaScript bundle | see trap 2 |

`<slug>` is the model id with each `/` replaced by `-`. `zai-org/glm-5` becomes
`https://novita.ai/models/model-detail/zai-org-glm-5`. That page is server
rendered, so it states the price, the context length, and the description in its
HTML. It is the right `model card` link for a reader.

Novita serves `https://novita.ai/llms.txt`, `https://novita.ai/llms-full.txt`,
and a `.md` twin for every docs page. The docs live on `novita.ai/docs`, not on
`docs.novita.ai`. See trap 8.

## Nine things that produce a wrong number

**1. Divide `price` and `quota` by 10000.** The plan JSON holds `"price":
"199000"` and `"quota": "500000000000"`. The site divides both by `1e4` before
it prints them, so the Lite tier is $19.90 per month for 50,000,000 tokens.
Copy `199000` into `amount` and you overstate the price by 10000 times. Three
facts confirm the divisor: the checkout payload divides by `1e4`, the docs FAQ
calls the entry tier "the 50M tokens in the Coding Plan", and the saving math in
trap 4 only works at this scale.

**2. The prices are not in the page HTML and not in the page bundle.** The page
is a Next.js App Router page. Its flight payload carries a `modelProductPrice`
map, but that map holds image and video rates, not plan tiers and not LLM token
rates. The bundle holds the layout, the FAQ text, and the terms text only. Use
the endpoint. Details in `references/pages.md`.

**3. The plan quota is not a raw token count.** `https://novita.ai/docs/guides/LLM-FAQ`
says tokens "are calculated based on base-rate equivalent token counts", and the
page terms name the base: "DeepSeek V3.2 output price ($0.4/Mt) serves as the
standard unit price". Every model burns quota at its own coefficient, and both
input and output tokens count. So 50M is 50M DeepSeek-V3.2-output equivalents,
not 50M tokens of GLM-5. Say so in `notes`. Never write "50M tokens" alone.

**4. Check a price against the saving badge.** The bundle hardcodes the badge
values `{Lite: "", Pro: "17%", Max: "33%"}`. Quota divided by 1e4, times the
$0.4 base rate, against the price, reproduces them: Pro is 150M x $0.4 = $60 of
value for $49.90, which is 17%. Max is 750M x $0.4 = $300 for $199.90, which is
33%. Lite is 50M x $0.4 = $20 for $19.90, which is 0%. Run this check after any
price change. It catches a wrong divisor at once.

**5. Model ids collide on a prefix.** Novita serves `zai-org/glm-5`,
`zai-org/glm-5.1`, `zai-org/glm-5.2`, `zai-org/glm-5.3`, `zai-org/glm-5-turbo`,
and `zai-org/glm-5.3-flash`. `minimax/minimax-m2.5` sits next to
`minimax/minimax-m2.5-highspeed`, and `zai-org/glm-4.7` next to `zai-org/glm-4.7-h`
and `zai-org/glm-4.7-flash`. A substring search for `zai-org/glm-5` matches
`zai-org/glm-5.3-flash` first and returns that model's 1M context window. Match
the full id, not a prefix.

**6. Novita rounds a context window to binary K.** `context_size` is 202800 and
the site prints `198K`, because it divides by 1024. It prints `1M` for 1048576.
Use the short form the site prints. Do not convert 202800 to `200K` yourself,
and do not write the raw integer.

**7. "Open-source SOTA" is a ranking claim.** Novita writes both forms in its
model descriptions. GLM-5 "is an open-source foundation model", MiniMax M2.7 is
"a versatile open-source large language model", and DeepSeek V4 Pro is "the
next-generation flagship open-source large language model". Those three state
membership, so `open_weights` is `true`. Kimi K2.5 only "achieves new
open-source state-of-the-art performance", which compares it to a group and does
not put it in one. That is `null`. Read the sentence, never the grep hit.

**8. `docs.novita.ai` is a redirect, not a host.** Every path on it 301s to
`https://novita.ai/docs/...`, and `https://docs.novita.ai/sitemap.xml` lands on
the quickstart guide with a 200. A naive fetch of a docs sitemap therefore
returns a guide page and looks like a success. Fetch `https://novita.ai/llms.txt`
instead. It lists every docs page as a `.md` URL.

**9. `https://novita.ai/model-api/pricing` redirects to `https://novita.ai/pricing`.**
Both return the same 1 MB body. Cite `https://novita.ai/pricing`.

## The endpoints

Both are public. Neither needs a key. The base host is `api-server.novita.ai`,
which the site's bundle defines as its default `base_url`.

```bash
# Plan tiers, quotas, per-tier RPM and TPM, and the nine covered models.
curl -sS -A "Mozilla/5.0" https://api-server.novita.ai/v1/product/resource-pack-specs/list

# Every model: context size, max output, modalities, T1-T5 rate limits.
curl -sS -A "Mozilla/5.0" https://api-server.novita.ai/v1/product/model/list

# The same rates in OpenAI model-list shape. Use it to cross-check.
curl -sS -A "Mozilla/5.0" https://api.novita.ai/openai/v1/models
```

Keep only entries with `type == 1` in the first response. The page filters on
that value, and other types are not the coding plan.

## Workflow

**Plans**

1. Run `python3 scripts/read_coding_plan.py`.
2. Divide nothing further. The script already divides by 10000.
3. Write one record per tier: Lite, Pro, Max. Monthly term only.
4. Put the quota, the RPM, and the TPM in `limits`. Keep each under 12 words.
5. Say in `notes` that the quota counts base-rate equivalent tokens.
6. Run the saving check in trap 4 before you finish.

**API pricing**

7. Take `input`, `output`, and `cached_input` from `priceInfo.*Decimal`.
8. Leave `cache_write` `null`. Every `cacheCreationInputTokenDecimal` is `0`,
   and `0` is the absence of a published rate, not a free rate.
9. Take `context_window` from the short form the site prints, not from the raw
   integer. See trap 6.
10. Cross-check every rate against `https://api.novita.ai/openai/v1/models`.

**Models**

11. Take `context_window` and `max_output` from the short forms.
12. Set `total_params` and `active_params` to `null`. Novita publishes no
    parameter count. The `labels` field says only `MoE`, and one model carries
    `> 100B`, which is a range and not a count.
13. Set `open_weights` by trap 7. Set `vision` only where the description names
    image or visual input.

**Rate limits**

14. Write one record per model and per tier, T1 to T5, from `quota_items`.
15. TPM is a combined limit, so write it into `tokens_per_minute` and leave the
    split fields `null`.
16. Add both links: the model page and
    `https://novita.ai/docs/guides/llm-rate-limits`.

**Finish**

17. Set `last_verified` to the date you read the pages.
18. Append one `data/changelog.yaml` record.
19. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, and the dead ends |
| `scripts/read_coding_plan.py` | Prints every tier, rate, and rate limit |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
