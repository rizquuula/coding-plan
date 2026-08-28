# Moonshot prices

Read `fetching.md` first. It tells you how to get the plan prices off the page.

## Membership prices

Read on 2026-08-28 from the `ListGoods` RPC, `DOMAIN_NEXUS`. USD, whole-term
totals, ready for `amount`.

| Tier | `month` | `year` |
|---|---|---|
| Adagio | 0 | — |
| Moderato | 19 | 180 |
| Allegretto | 39 | 372 |
| Allegro | 99 | 948 |
| Vivace | 199 | 1908 |

The same prices as a rate per month, which is the form the page prints:

| Tier | Monthly | Yearly |
|---|---|---|
| Moderato | 19 | 15 |
| Allegretto | 39 | 31 |
| Allegro | 99 | 79 |
| Vivace | 199 | 159 |

Two facts about that table:

1. Moonshot sells no quarterly term. `billingCycle.timeUnit` is only
   `TIME_UNIT_MONTH` or `TIME_UNIT_YEAR`. A `prices` list with a `quarter` entry
   is wrong.
2. Adagio is free and has no yearly record. Write one `month` entry with
   `amount: 0`.

The rate per month is derived, not published. `build.py` derives it back from
`amount` and prints it under the term. Check the rendered cell for yearly
Allegretto reads `$31.00/mo`.

## Trap: three domains, three tier namings

The RPC serves three product domains. `domains: []` returns `DOMAIN_NEXUS`,
which is what the membership page itself requests. All prices are USD and all
records say `REGION_OVERSEA`.

| Level | `DOMAIN_NEXUS` | `DOMAIN_KIMI` | `DOMAIN_CODE` |
|---|---|---|---|
| FREE | Adagio, 0 | Free, 0 | Free, 0 |
| BASIC | Moderato, 19 / 180 | Plus, 19 / 180 | Starter, 19 / 180 |
| INTERMEDIATE | Allegretto, 39 / 372 | Pro, 39 / 372 | Explorer, 49 / 468 |
| ADVANCED | Allegro, 99 / 948 | Max, 99 / 948 | Expert, 99 / 948 |
| STANDARD | Vivace, 199 / 1908 | Ultra, 199 / 1908 | Master, 219 / 2100 |

**Take `DOMAIN_NEXUS`.** Two things confirm it is the live naming:

1. The membership page sends an empty `domains` list, and the RPC answers with
   `DOMAIN_NEXUS`.
2. `https://www.kimi.com/code/docs/en/kimi-code/models.html` names Moderato,
   Allegretto, and Allegro when it says which tier unlocks which model. It names
   no tier from the other two domains.

`DOMAIN_KIMI` and `DOMAIN_CODE` differ from `DOMAIN_NEXUS` in two rows, not
zero. A price copied from the wrong domain is wrong by 10 USD per month at the
INTERMEDIATE level and by 20 USD per month at the top. Do not treat the three
namings as aliases.

## API rates per token

USD per 1M tokens, read 2026-08-28. `data/api_pricing.yaml` carries the first
and the third.

| Model | Page | Input | Cached input | Output | Context |
|---|---|---|---|---|---|
| `kimi-k3` | `docs/pricing/chat-k3` | 3.00 | 0.30 | 15.00 | 1,048,576 |
| `kimi-k2.7-code-highspeed` | `docs/pricing/chat-k27-code` | 1.90 | 0.38 | 8.00 | 262,144 |
| `kimi-k2.7-code` | `docs/pricing/chat-k27-code` | 0.95 | 0.19 | 4.00 | 262,144 |

Each pricing page prints two input columns, "Cache Hit" and "Cache Miss". Cache
Miss is the uncached rate, so it goes in `input`. Cache Hit goes in
`cached_input`.

**Moonshot publishes no cache-write rate.** Leave `cache_write` as `null`.

`llms.txt` also lists pricing pages for `kimi-k2.6`, `kimi-k2.5`, the
`moonshot-v1` series, BatchJob, and WebSearch. Add a model only when it belongs
in a coding-plan tracker. `kimi-k2.5` and the `moonshot-v1` series reach full
platform sunset on August 31, and `kimi-k2` was discontinued on 2026-05-25.

## Trap: Kimi Code uses different model IDs

The API platform sells `kimi-k2.7-code`. Kimi Code exposes the same model as
`kimi-for-coding`, and the fast variant as `kimi-for-coding-highspeed`. Kimi
Code also splits K3 into `k3` and `k3-256k`.

`data/api_pricing.yaml` tracks the API platform, so use the platform IDs:
`kimi-k3` and `kimi-k2.7-code`. Never write `kimi-for-coding` into `model_id`.

## Trap: the china stack prints different numbers

`platform.kimi.com` is the china platform. It prints CNY and Chinese text. Its
rate-limit tiers carry the same RPM and TPM as the global page, which makes it
look like confirmation. Its token rates do not match.

`https://platform.kimi.com/docs/pricing/chat-k3.md` returned this row on
2026-08-28:

    ["kimi-k3", "1M tokens", "¥2.00", "¥20.00", "¥100.00", "1,048,576 tokens"]

That is 2.00 cache hit, 20.00 cache miss, and 100.00 output, in CNY. The global
page states 0.30, 3.00, and 15.00 in USD. The two are not one price in two
currencies. The recharge thresholds differ as well. See `quotas.md`.

Every Moonshot row in this repository comes from the global stack. Do not mix.
