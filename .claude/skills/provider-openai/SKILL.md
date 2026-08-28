---
name: provider-openai
description: How to source OpenAI prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh an OpenAI row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions OpenAI, ChatGPT, GPT, GPT-5.6, Codex, ChatGPT Go, ChatGPT Plus, or ChatGPT Pro. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# OpenAI — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to OpenAI, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `OpenAI` in all four data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables. `region` is `global`. Prices and rates are USD.

OpenAI sells the subscription as **ChatGPT**, in four paid individual tiers: Go,
Plus, Pro 5x, and Pro 20x. It sells the API per token.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices, plan message limits | `https://learn.chatgpt.com/docs/pricing.md` | `WebFetch` |
| API rates per token | `https://developers.openai.com/api/docs/pricing.md` | `WebFetch` |
| Rate limits per usage tier | `https://developers.openai.com/api/docs/models/<model-id>.md` | `WebFetch` |
| Model specification | `https://developers.openai.com/api/docs/models/<model-id>.md` | `WebFetch` |
| Usage tier thresholds | `https://developers.openai.com/api/docs/guides/rate-limits.md` | `WebFetch` |
| Every model page URL | `https://developers.openai.com/api/docs/models.md` | `WebFetch` |
| Every docs URL | `https://developers.openai.com/llms.txt` | `WebFetch` |

`WebFetch` reads every page in this table. You need no script and no browser.
Append `.md` to any docs path to get clean markdown. Details in
`references/pages.md`.

## Seven things that produce a wrong number

**1. `openai.com`, `chatgpt.com`, and `help.openai.com` all return 403.** A
Cloudflare challenge blocks them. `curl` and `WebFetch` both fail, under every
user agent tried. Do not spend time on `https://openai.com/chatgpt/pricing/`.
Read `https://learn.chatgpt.com/docs/pricing` instead. OpenAI owns that host, so
it satisfies rule 4 in `AGENTS.md`.

**2. `platform.openai.com/docs/...` moved.** Each path now returns 301 to
`developers.openai.com/api/docs/...`. The redirect works, but write the
destination URL into `links`. Never link `platform.openai.com/settings/...`,
which needs a login.

**3. The API pricing page ships four service tiers in one page.** Standard,
Batch, Flex, and Fast mode each get a full table. Take the **Standard** table.
Batch and Flex charge half of Standard. Fast mode charges double. An agent that
grabs the first table it parses can write half the right rate.

**4. Every pricing row splits short context and long context.** Take the
**short context** columns. Long context applies above 272,000 input tokens, and
costs 2x input and 1.5x output. The two column sets sit in one row, so a wide
table is easy to misread.

**5. The Pro card prints only "From $100".** The $200 price for Pro 20x appears
further down the same page, in the ChatGPT Voice section. Read that section
before you write a Pro row. Table in `references/pricing.md`.

**6. The credit rate card is not a price.** `learn.chatgpt.com/docs/pricing`
prints "Credits per 1M tokens", such as 100 credits for GPT-5.6 Sol input.
Credits are a consumption unit, not USD. Never copy a credit figure into
`data/api_pricing.yaml`.

**7. The rate-limit guide publishes no per-model number.** It states the spend
that promotes an account between usage tiers, and nothing else. Every RPM and
TPM figure sits on the model page. Reasoning in `references/quotas.md`.

## Workflow

1. Read `https://developers.openai.com/api/docs/models.md`. Take the model page
   URL for each model you need.
2. Read each model page as `.md`. Take the context window, the max output, the
   rates, and the rate-limit table.
3. Read `https://developers.openai.com/api/docs/pricing.md`. Take the Standard
   table, short context columns.
4. Cross-check: the model page and the pricing page must state the same input,
   cached input, and output rate. They agreed on 2026-08-28.
5. Read `https://learn.chatgpt.com/docs/pricing.md`. Take the plan prices from
   the cards and the message limits from the usage table.
6. Read the ChatGPT Voice section on that same page for the Pro 20x price.
7. Write the rows. Copy the shapes in `references/data-recipes.md`.
8. Set `last_verified` to the date you read the pages.
9. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the `.md` twin trick |
| `references/pricing.md` | Plan prices, API rates, the four service tiers |
| `references/quotas.md` | Plan message limits, API rate limits per usage tier |
| `references/data-recipes.md` | A worked row for each of the four datasets |

This skill ships no script. Every value is reachable with `WebFetch`.

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
