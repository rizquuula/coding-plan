---
name: provider-zai
description: How to source Z.ai (Zhipu / GLM) prices, quotas, and rate limits for the datasets in this repository. Use when you add or refresh a Zhipu row in data/plans.yaml, data/api_pricing.yaml, data/rate_limits.yaml, or data/models.yaml, or when the user mentions Z.ai, z.ai, Zhipu, GLM, GLM Coding Plan, GLM-5.3, or ZCode. Records which page holds each value, which tool reads it, and the traps that produce a wrong number.
---

# Z.ai (Zhipu / GLM) — how to source the data

Read `AGENTS.md` first. Its sourcing rules bind you. This file records what is
specific to Z.ai, so you do not repeat work that already failed.

Everything here was checked on 2026-08-28. Re-check a status before you trust it.

## Constants

Write the provider as `Zhipu (GLM)` in all four data files. The build script
groups rows by that exact string, so any other spelling splits the provider into
two tables. `region` is `china`. Prices are USD.

Z.ai sells the subscription as the **GLM Coding Plan**. Individual buyers get
three tiers: Lite, Pro, and Max. Teams get two seats: Standard and Premium.

The data holds 5 plan rows, 22 API pricing rows, 21 model rows, and 0 rate-limit
rows.

## Where each value lives

| You need | Page | Tool |
|---|---|---|
| Individual plan prices, billing terms | `https://z.ai/subscribe` | `scripts/read_subscribe.py` |
| Team seat prices | `https://api.z.ai/api/biz/overseas/team/subscribe/product/public_pricing` | `curl` |
| Individual tier quotas, models | `https://docs.z.ai/devpack/overview` | `WebFetch` |
| Team seat quotas | `https://docs.z.ai/devpack/teamplan` | `WebFetch` |
| API rates per token | `https://docs.z.ai/guides/overview/pricing` | `WebFetch` |
| Context window, every model | `https://docs.z.ai/guides/overview/overview.md` | `curl` or `WebFetch` |
| `max_output` and `model_id` | `https://docs.z.ai/api-reference/llm/chat-completion.md` | `curl` or `WebFetch` |
| Parameter counts, `open_weights` | The model's own guide page | `WebFetch` |
| Every docs URL | `https://docs.z.ai/llms.txt` | `WebFetch` |

`guides/overview/overview.md` is the model matrix. It is the entry point for
`data/models.yaml`, and it links every model's guide page. Do not start at one
model's page.

## Seven things that produce a wrong number

**1. The subscribe page defeats `WebFetch` and `--dump-dom`.** Both return a
success code and no price. The prices are compiled into the page's JavaScript
bundle, so fetch the bundle instead. Run `python3 scripts/read_subscribe.py`. It
needs no install and no browser. Details in `references/fetching.md`.

**2. The bundle ships three generations of the plan at once.** V1, V2, and V3 sit
side by side. V1 and V2 are dead legacy pricing. Take only the highest `version`
string. A naive read returns nine wrong prices next to the nine right ones.

**3. `money` in the bundle is the term total. Do not multiply it.** The rendered
page prints a rate per month, such as `$12.6/month` under the yearly toggle. The
bundle does not: it holds `151.2` for the whole year. You read the bundle, so
copy `money` straight into `amount`. Table in `references/pricing.md`.

**4. The Team pricing API serves products nobody can buy.** Four of its ten
entries are `purchasable: false`, including both quarterly seats. **Z.ai sells
no quarterly Team seat.** Filter on `purchasable: true` before you copy an
amount. Table in `references/pricing.md`.

**5. `chat-completion.md` states `max_tokens` twice.** The text schema and the
vision schema each carry a block, and they list different models. The vision
block is the only source for GLM-5.3-Flash and GLM-5V-Turbo. The `model_id` enum
splits the same way. Read both. Details in `references/models.md`.

**6. "Open-source" on a GLM page is usually a ranking claim.** "SOTA among
open-source models" compares the model to a group. It does not put the model in
it, so `open_weights` is `null`. Exactly three Zhipu models state membership. A
grep hit proves nothing; read the sentence. Details in `references/models.md`.

**7. Z.ai publishes no numeric API rate limit.** What it enforces is a per-model
concurrency limit, tied to an account and never public. Zero Zhipu rows in
`data/rate_limits.yaml` is correct. Reasoning in `references/quotas.md`.

## Workflow

Do the datasets in this order. Later steps reuse earlier values.

**Plans**

1. Read `https://docs.z.ai/devpack/overview`. Take the Individual quotas and the
   model list.
2. Read `https://docs.z.ai/devpack/teamplan`. Take the two seat quotas.
3. Run `python3 scripts/read_subscribe.py`. Take the block for the highest
   version only.
4. Copy each `money` value into `amount`. It is the term total. Do not multiply.
5. `curl` the Team pricing API. Keep only entries with `purchasable: true`.
   Write `payAmount` into `amount`, and the `renewAmount` discount into `notes`.
6. Cross-check the quotas: the subscribe page states Pro as `6x Lite` and Max as
   `14x Lite`, which must match the absolute credit numbers.

**API pricing**

7. Read `https://docs.z.ai/guides/overview/pricing`. Take input, cached input,
   and output for each model. Leave `cache_write` as `null`.
8. Take `context_window` from the model matrix and `model_id` from both enums in
   `chat-completion.md`.
9. Check the GLM-5.3-Flash promotion. It expires on 2026-09-09.

**Models**

10. Read the model matrix. Take `context_window` and each model's guide link.
11. Take `max_output` from both `max_tokens` blocks in `chat-completion.md`.
12. Open each guide page. Set `open_weights` and the parameter counts only from
    what that page states about that model.

**Finish**

13. Add no row to `data/rate_limits.yaml`.
14. Set `last_verified` to the date you read the pages.
15. Run `python3 build.py --check`.

## References

| File | Holds |
|---|---|
| `references/pages.md` | Every page, its status, the dead ends, the `.md` twin trick |
| `references/fetching.md` | The bundle recipe, the regex, failure modes, troubleshooting |
| `references/pricing.md` | Individual prices, Team seat prices, API token rates |
| `references/quotas.md` | Credit quotas, why rate limits and speeds are absent |
| `references/models.md` | Where each model field lives, and the five model traps |
| `references/data-recipes.md` | A worked row for each of the four datasets |
| `scripts/read_subscribe.py` | Prints every tier under every billing term |

## Keep this file true

When you learn something this skill does not say — a page that moved, a value
that is not where you expected, a fetch that fails — write it back here before
you finish. A wrong claim in this file costs the next agent more than a gap.
