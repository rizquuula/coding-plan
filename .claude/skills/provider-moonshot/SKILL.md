---
name: provider-moonshot
description: How to source Moonshot (Kimi) prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh a Moonshot row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Moonshot, Kimi, kimi-k2, kimi-k2.7-code, kimi-k3, Kimi Code, Kimi for Coding, or Kimi membership. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Moonshot (Kimi) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Moonshot, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Moonshot (Kimi)` in all four data files. The build script
groups rows by that exact string, so any other spelling splits the provider into
two tables.

Every Moonshot row in the data today comes from the global site and states USD.
A `data/plans.yaml` row therefore takes `region: global`. `currency` and
`price_currency` are `USD`.

Moonshot runs two separate stacks. Use the global one:

| Stack | API platform | Consumer site | Currency |
|---|---|---|---|
| Global — use this | `platform.kimi.ai` | `www.kimi.com` | USD |
| China — do not mix in | `platform.kimi.com` | — | CNY |

Moonshot sells one coding subscription, **Kimi membership**, in five tiers:
Adagio (free), Moderato, Allegretto, Allegro, and Vivace. Kimi Code is the
coding client inside that membership. It is not a separate subscription.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Plan prices, billing terms | `https://www.kimi.com/membership/pricing` | `scripts/read_plans.py` |
| Which tier unlocks which model | `https://www.kimi.com/code/docs/en/kimi-code/models.html` | `curl` |
| Plan quota wording | `https://www.kimi.com/code/docs/en/kimi-code/membership.html` | `curl` |
| API rate per token, K3 | `https://platform.kimi.ai/docs/pricing/chat-k3` | `WebFetch` |
| API rate per token, K2.7 Code | `https://platform.kimi.ai/docs/pricing/chat-k27-code` | `WebFetch` |
| RPM, TPM, TPD per tier | `https://platform.kimi.ai/docs/pricing/limits` | `WebFetch` |
| Model list, context windows | `https://platform.kimi.ai/docs/models` | `WebFetch` |
| K3 parameters, open weights | `https://platform.kimi.ai/docs/guide/kimi-k3-quickstart` | `WebFetch` |
| K2.7 Code specs, vision, output speed | `https://platform.kimi.ai/docs/guide/kimi-k2-7-code-quickstart` | `WebFetch` |
| Every docs URL | `https://platform.kimi.ai/docs/llms.txt` | `curl` |

Every page under `platform.kimi.ai/docs/` serves a markdown twin. Append `.md`
to the path. `WebFetch` reads either form.

## Six things that produce a wrong number

**1. `platform.moonshot.ai` is a redirect, not a source.** It returns 301 to
`platform.kimi.ai`. `platform.moonshot.cn` returns 301 to `platform.kimi.com`.
Cite the destination URL, never the redirect. A reader who follows a
`moonshot.ai` link lands somewhere the price is not.

**2. The docs index is not at `/llms.txt`.** That path returns 404. The index
sits at `https://platform.kimi.ai/docs/llms.txt`. It lists every documentation
page and its markdown twin. Read it first when a page you expect is missing.

**3. The membership pricing page defeats `WebFetch` and `curl`.** Both return a
success code and no price. The page fetches its prices from one public RPC. Run
`python3 scripts/read_plans.py`. It needs no install and no browser. Details in
`references/fetching.md`.

**4. The RPC returns `priceInCents`, and the value is the term total.** Divide
by 100. Do not multiply by the term. Moderato yearly returns `18000`, so
`amount` is `180` for the whole year. Table in `references/pricing.md`.

**5. The RPC serves three tier namings at once.** `DOMAIN_NEXUS`,
`DOMAIN_KIMI`, and `DOMAIN_CODE` return different tier names and two different
prices. `DOMAIN_NEXUS` is the naming the site shows. Take it. Reasoning in
`references/pricing.md`.

**6. The china rate-limit page prints the same RPM and TPM.** Only the recharge
threshold differs, in CNY. So a page in Chinese looks like confirmation and is
not. Cite `platform.kimi.ai`, not `platform.kimi.com`. Detail in
`references/quotas.md`.

## Workflow

1. Read `https://platform.kimi.ai/docs/llms.txt` and find the pages you need.
2. For an API rate, read the per-model pricing page with `WebFetch`.
3. For a rate limit, read `https://platform.kimi.ai/docs/pricing/limits`.
4. For a plan price, run `python3 scripts/read_plans.py`.
5. Divide each printed amount by nothing. The script already divides the cents.
6. Read `kimi-code/models.html` for the model list each tier unlocks.
7. Write the rows. Copy the shapes in `references/data-recipes.md`.
8. Set `last_verified` to the date you read the pages.
9. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the redirects |
| `references/fetching.md` | The RPC recipe, the endpoint, failure modes, troubleshooting |
| `references/pricing.md` | Plan prices, the three domains, API token rates |
| `references/quotas.md` | Rate-limit tiers, plan quotas, the china split |
| `references/data-recipes.md` | A worked row for each of the four datasets |
| `scripts/read_plans.py` | Prints every tier under every billing term |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
