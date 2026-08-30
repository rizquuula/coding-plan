---
name: provider-sakana
description: How to source Sakana (Fugu) prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh a Sakana row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Sakana, Sakana AI, Fugu, Fugu Ultra, Fugu Cyber, fugu-ultra-v1.1, fugu-ultra-v1.0, or console.sakana.ai. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Sakana — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Sakana, so you do not repeat work that already failed.

Everything here was checked on 2026-08-30. Re-check a status before you trust it.

**One page holds everything.** `https://sakana.ai/fugu/` states the plan prices,
the token rates, and a FAQ. No other Sakana page carries a number this
repository needs. Start there and stop there.

## Constants

Write the provider as `Sakana (Fugu)` in all five data files, including
`data/changelog.yaml`. This matches the provider table in `AGENTS.md` and the
`Alibaba (Qwen)`, `Moonshot (Kimi)`, and `Zhipu (GLM)` convention. The build
script groups rows by that exact string, so any other spelling splits the
provider into two tables.

`currency` is `USD` in `data/api_pricing.yaml`. `price_currency` is `USD` in
`data/plans.yaml`. The page prints no JPY figure. See trap 3.

`region` is `global`. Sakana AI is a Japanese company, and the enum holds no
`japan` value.

Fugu is not a model. It is an API-based multi-agent orchestration system. It
routes work across third-party models behind one OpenAI-compatible endpoint.
Sakana sells three variants: Fugu (balanced), Fugu Ultra (complex reasoning),
and Fugu Cyber (cybersecurity, contact sales only).

The page is server-rendered. `WebFetch` and `curl -sL -A "Mozilla/5.0"` both
return the full page, 200 and 164385 bytes on 2026-08-30. No bundle recipe and no script are
needed. This skill ships no `scripts/` directory.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices for Standard, Pro, Max | `https://sakana.ai/fugu/` | `WebFetch` |
| Fugu Ultra token rates | `https://sakana.ai/fugu/` | `WebFetch` |
| The above-272K rate tier | `https://sakana.ai/fugu/` | `WebFetch` |
| Model ids and the former id | `https://sakana.ai/fugu/` | `curl -sL` |
| What each variant does | `https://sakana.ai/fugu/` | `WebFetch` |

There is no docs host. `https://docs.sakana.ai/` does not resolve. There is no
`.md` twin, no `llms.txt`, and no `sitemap.xml` on `sakana.ai`. Each returns a
real 404. `https://console.sakana.ai/` redirects to `/login`, and
`https://chat.sakana.ai/` serves a separate consumer chat product. Neither
states a price or a quota. Details in `references/pages.md`.

## Nine things that produce a wrong number

**1. Fugu base publishes no per-token rate.** The page says usage is billed "at
a single rate based on the top tier model involved". It names no number. Add no
`data/api_pricing.yaml` row for Fugu base. Only Fugu Ultra gets a rate row.
Never invent a rate to fill the gap.

**2. 272K is a pricing threshold, not a context window.** Above 272K tokens the
rates change. That number describes a billing tier, not a model limit. Never
write `context_window: 272K` in any file. The schema holds one rate per field,
so record the rates at or below 272K in `input`, `output`, and `cached_input`,
then state the above-272K rates in `notes`: input $10, output $45, cached input
$1.00.

**3. The page is bilingual, so every number appears at least twice.** Each
sentence appears in English and again in Japanese. FAQ answer Q5 then restates
every plan price and every token rate a second time, so most figures appear four
times. A count-based sanity check such as "the price appears once" fails on this
page. The Japanese text repeats the same USD figures. It is not a JPY price
list.

**4. Third-party listings look official and are not.**
`models.dev/providers/sakana/`, `openrouter.ai/sakana/fugu-ultra`, and
`vercel.com/ai-gateway/models/fugu-ultra` are linked from the Fugu page itself.
Sakana does not own those hosts, so `AGENTS.md` rule 4 rejects them. Never cite
one.

**5. The arXiv papers are Sakana-authored and arXiv-hosted.** The technical
report `2606.21228`, TRINITY `2512.04695`, and Conductor `2512.04388` all fail
rule 4 for the same reason. An `announcement` link must point at `sakana.ai`.

**6. Sakana publishes no rate limit.** No page states requests per minute,
tokens per minute, or a concurrency limit. Zero Sakana rows in
`data/rate_limits.yaml` is the correct result. Do not fill the gap.

**7. `fugu-ultra-20260615` is the former model id.** The pricing card names it
as the previous name, and the page misspells "previously" as "previouly". Search
for the typo, not the correct spelling. The page contradicts itself: FAQ answer
Q5 still writes "Fugu Ultra (fugu-ultra-20260615) is priced per 1M tokens at $5
input". Trust the pricing card, not the FAQ. Use `fugu-ultra-v1.1` and
`fugu-ultra-v1.0`.

**8. Fugu is not a model, so `data/models.yaml` has nothing to state.** No page
states a parameter count, a context window, a max output, or a vision
capability. A models row would be nulls in every field. Add none until a
specification page appears.

**9. The subscription tiers publish no absolute quota.** The page states
"Baseline allowance" for Standard, "10x Standard usage" for Pro, and "20x
Standard usage" for Max. Every allowance is relative to Standard, and Standard
itself carries no number. Never multiply a token rate by a price to derive a
quota. Write each `limits` item as the relative statement the page makes.

## Workflow

1. Read `https://sakana.ai/fugu/`.
2. Take the plan prices: Standard $20, Pro $100, Max $200, monthly only.
3. Take the Fugu Ultra rates: input $5, output $30, cached input $0.50.
4. Put the above-272K rates in `notes`. Leave `cache_write` `null`.
5. Add no row for Fugu base and no row for Fugu Cyber.
6. Add no row to `data/rate_limits.yaml`.
7. Add no row to `data/models.yaml`.
8. Use only `sakana.ai/fugu/` URLs in `links`. Label a plan row `plans` and the
   rate row `pricing`.
9. Set `last_verified` to the date you read the page.
10. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every URL, its probe result, and every outbound link |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
