---
name: provider-meta
description: How to source Meta Muse Code and Muse Spark data for the datasets in this repository. Use when you add or refresh a Meta row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Meta, Muse Code, Muse Spark, dev.meta.ai, or the Meta Model API. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Meta (Muse Code / Muse Spark) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Meta, so you do not repeat work that already failed.

Everything here was checked on 2026-09-04. Re-check a status before you trust it.

## Constants

Write the provider as `Meta` in all five data files. The build script groups
rows by that exact string, so any other spelling splits the provider into two
tables.

Meta's product is Muse Code, a terminal coding agent powered by the Muse Spark
model family (1.1, 1.2, 1.3). The API surface is the Meta Model API. The CLI
installs with `curl -fsSL https://dev.meta.ai/install.sh | bash`.

**Meta publishes no plan prices, no per-token rates, and no numeric rate limits
on any page readable without login as of 2026-09-04.** `data/plans.yaml`,
`data/api_pricing.yaml`, and `data/rate_limits.yaml` therefore carry zero Meta
rows. Zero rows is the correct result here, not a gap to fill from a third
party. The only Meta row is the Muse Spark 1.3 specification in
`data/models.yaml`.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Muse Spark 1.3 availability, efficiency claims | `https://research.meta.ai/blog/introducing-muse-spark-1-3` | `read` |
| 1M context window, multimodal support | `https://research.meta.ai/blog/introducing-muse-spark-meta-model-api` | `read` |
| Muse Code install command, 1.2 availability | `https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2` | `read` |
| Product surface (do not source values from it) | `https://developer.meta.com/ai/products/muse-code/` | none — empty CSR shell |
| Model surface (do not source values from it) | `https://developer.meta.com/ai/models/muse-spark/` | none — empty CSR shell |
| API surface (do not source values from it) | `https://developer.meta.com/ai/products/meta-model-api/` | none — empty CSR shell |
| CLI installer (install only, no prices) | `https://dev.meta.ai/install.sh` | `read` |

## Six things that produce a wrong number

**1. The developer.meta.com pages render an empty shell.** Every page under
`developer.meta.com/ai/` returns HTTP 200 with ~500 KB of CSS and bootstrapper
scripts and no CMS copy: no tier names, no prices, no rates, no quotas. `read`
returns only meta tags. The copy loads client-side through an authenticated
Relay/GraphQL layer (`/api/graphql/` returns nothing useful without credentials).
Do not cite these pages for a value. They are link targets only.

**2. `dev.meta.ai` needs a login.** `/`, `/docs`, `/docs/pricing`, and every
`/docs/*` path tried return either the Facebook "Sorry, something went wrong"
error page or an empty shell to an anonymous fetcher (`/docs/pricing` is HTTP
200 with zero readable text; `/pricing` is HTTP 404). Only `/install.sh` is
public, and it holds an installer, not prices. Treat any plan or rate figure
attributed to `dev.meta.ai` docs as unverified until you read it yourself while
logged in.

**3. `api.meta.ai` needs an API key.** Unauthenticated `GET` calls to `/v1/*`
return `invalid_api_key`. The only public route found is
`/muse-code/channels/muse-stable`, which reports the CLI release version, not a
price. Never copy a rate from an error body.

**4. Third-party Spark rates are not a source.** Several aggregators print
$1.25 per 1M input and $4.25 per 1M output for Muse Spark 1.1. Rule 4 in
`AGENTS.md` forbids citing them, and the figures describe 1.1, not the tracked
1.3 model. Leave `data/api_pricing.yaml` empty for Meta until a Meta-owned page
states a 1.3 rate.

**5. The "Everyday / High / Power" tiers have no readable price.** The issue
names these subscription tiers, but no provider-owned page readable without
login states their prices or quotas as of 2026-09-04. Do not add
`data/plans.yaml` rows with guessed amounts or with `amount: 0`. Zero rows is
correct.

**6. The 1.3 post states no context window and no weights release.** The 1M
context window comes from the 1.1 announcement post, which says Spark 1.1
"can actively manage its context window of 1 million tokens". The 1.3 post says
only that 1.3 rolls out in Muse Code and Meta Model API. The 1.3 post names a
"Muse Spark open weights release" as roadmap, not as shipped, so `open_weights`
is `null`, not `false`. The 1.3 post never says the model reads images, so
`vision` is `null`.

## Workflow

1. Read the three research posts above. Take availability, the 1M context
   window, and the multimodal statement.
2. Write one `data/models.yaml` row for Muse Spark 1.3. Link the product page
   as `model card` and the 1.3 post as `announcement`.
3. Add no row to `data/plans.yaml`, `data/api_pricing.yaml`, or
   `data/rate_limits.yaml` until a provider-owned page states a value.
4. Set `last_verified` to the date you read the pages.
5. Run `python build.py --check`.

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
