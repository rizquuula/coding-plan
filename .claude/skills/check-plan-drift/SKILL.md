---
name: check-plan-drift
description: How to compare every stored price in data/plans.yaml against the price the provider states online right now, so you only open the pages that disagree. Use when you check for drift, suspect a price change, refresh prices, check providers, hunt stale data, or want to know which rows to re-verify first. Runs one script that pairs each tier with its own price on the page and returns MATCH, DRIFT, or CANNOT COMPARE per stored amount.
---

# Check plan drift

Read `AGENTS.md` first. Its sourcing rules bind you. This skill adds one script
that does the boring sweep. You read the report and open only the flagged pages.

## What the script checks

The script reads `data/plans.yaml` only, and only the `prices` field. It ignores
`limits`, `models`, and quotas. It ignores `data/api_pricing.yaml`,
`data/rate_limits.yaml`, and `data/models.yaml`.

For each plan record it takes the `links` entries labelled `pricing` or `plans`,
fetches each unique page once, finds the tier name on the page, and reads the
price stated for that tier. Every stored amount gets exactly one verdict.

| Verdict | Meaning | Do this |
|---|---|---|
| `MATCH` | The stored amount equals the online amount for that tier. | Nothing. |
| `DRIFT` | The script read an online amount for that tier and it differs. | Open the page and read the tier. |
| `CANNOT COMPARE` | The script could not read an online amount for that tier. | Read the reason, then the provider skill. |

`CANNOT COMPARE` is a first-class result, not a footnote. An amount the script
cannot read online must never look like a `MATCH`.

## The principle behind the verdicts

The script reports `DRIFT` only when it is confident it read that tier's own
price. A number near a tier name is not the same thing as the price of that
tier. Where the script is not confident, the honest verdict is
`CANNOT COMPARE`, never `DRIFT`.

It prefers to say nothing over saying something wrong. A wrong `DRIFT` teaches
you to ignore the `DRIFT` list, which is worse than having no checker. A long
`CANNOT COMPARE` list costs you a manual check, which you were going to do
anyway.

## How the script pairs a tier with its price

1. It searches the page text for the record's `plan` string, without case.
2. It rejects a short name matching inside a longer one. `Pro` never matches the
   `Pro` inside `Pro+`, `Pro Plus`, or `Product`. The longest tier name wins.
3. It takes a window of 200 characters before and after each occurrence.
4. It extracts the currency-marked prices in that window.
5. It keeps the prices the tier **owns**. A price belongs to the closest tier
   name above it, because a pricing page names a tier and then prints its price.
   A price with no tier name above it belongs to the very next tier name, which
   covers a card that prints the price above the label.
6. It requires the winning price to sit within 120 characters of the tier name.

Step 5 is what makes the verdict mean something. Without it, a page listing
`Starter $20, Pro $60` would confirm a stale `Pro = 20` row, because `20` sits
somewhere on the page. Ownership assigns that `$20` to `Starter`, so the row
correctly reads `DRIFT`.

A price another tier owns never becomes a candidate for this tier. Cursor prints
`Individual $20 / mo. Pro Pro+ Ultra`, where the `$20` is the picker's current
value and belongs to `Pro`. Under the rule, `Pro+` gets nothing and reads
`CANNOT COMPARE` rather than a false `DRIFT` against `$20`.

## How the script reads a price

The script never searches for a bare number. A bare `18` matches a token count,
and a bare `20` matches the `20` inside `2026`. It extracts only numbers that
carry a marker:

- a currency symbol before the number, such as `$20`, `US$20`, `¥199`, `€30`
- a currency code beside the number, such as `20 USD` or `CNY 199`
- a per-period phrase after the number, such as `20 / mo` or `20 per seat per month`

It normalizes each one, handling `1,234.56` and `1.234,56`. Tolerance is 0.005.

## Currency gates the comparison

The script records each price's currency from its symbol or code. It drops a
candidate whose currency contradicts the record's `price_currency`. A token with
no detectable currency stays in the set. When every candidate drops this way, the
verdict is `CANNOT COMPARE` with reason `page states prices in another currency`.

Comparing a `¥` figure against a `USD` row is a false result. The gate stops it.

## Quarter and year rows

`AGENTS.md` defines `amount` as the total for the whole term. Many providers
print only a discounted monthly rate, so the term total never appears literally.

For a `quarter` row the script also tries `amount / 3`, and for a `year` row
`amount / 12`. On a match it states the form, for example
`online 19 per month, stored 228 per year`.

It tries those two divisors only. A provider that gives free months breaks the
pattern. MiniMax bills a year at ten times the monthly rate, so `÷12` cannot
match. The monthly-rate guard sends those rows to `CANNOT COMPARE` instead of
reporting a false `DRIFT`.

## The reasons for CANNOT COMPARE

| Reason | Meaning |
|---|---|
| `page blocked` | HTTP 401 or 403, or a bot challenge marker. |
| `page renders client-side` | 200, but under 400 characters of text. |
| `page states no prices` | Readable, but fewer than 2 currency-marked prices. |
| `tier name not found on page` | The `plan` string never appears on the page. |
| `no price near the tier name` | The name appears, but its windows hold no price. |
| `page states prices in another currency` | Every candidate failed the currency gate. |
| `tier name and price are too far apart` | Every price sits over 120 characters from the name. |
| `candidate prices are implausible for this tier` | Every candidate differs from the stored amount by over 10×. |
| `free tier prints no price` | The stored amount is `0` and no candidate is `0`. |
| `page states only the monthly rate for this tier` | A quarter or year row saw only the tier's monthly candidates. |
| `fetch failed: <detail>` | The network call failed. |

The last four reasons are confidence guards. Each one exists because a real page
broke the naive reading:

- **Too far apart.** GitHub names `Copilot Pro` only in FAQ prose, thousands of
  characters below the price table. A price that far from a name is prose.
- **Implausible.** The Gemini pricing page prints per-token rates like `$0.031`
  beside a `22.8` seat price. Those differ by three orders of magnitude, so the
  script read the wrong kind of number.
- **Free tier.** A free tier prints `Free`, never `$0`, so it would otherwise
  inherit the next tier's price.
- **Monthly rate only.** Cursor and MiniMax print the monthly figure only. A
  year row whose candidates are exactly the month row's candidates has no term
  total to compare against. This also covers a provider that gives free months,
  such as MiniMax at ten times the monthly rate, without a per-provider divisor.

Suppressing a genuine 10× price change into `CANNOT COMPARE` is the safe failure
direction. You read that list anyway.

The first three and a fetch failure name the provider skill that can read the
page. The other reasons are about the row, not the page.

## How to run it

```bash
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --provider Cursor
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --only-uncomparable
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --json
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --timeout 60
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --update-snapshots
```

`--provider` matches the `provider` field without case, and falls back to a
substring, so `Zhipu` selects `Zhipu (GLM)`. `--only-uncomparable` prints just
the `CANNOT COMPARE` section. `--json` prints the whole report as JSON.

Exit codes: `0` when no row drifted, `1` when at least one row is `DRIFT`, `2`
when the script itself failed. A `CANNOT COMPARE` row alone returns `0`. It is
missing information, not drift.

## DRIFT is a hint, not evidence

A `DRIFT` row means the script paired the tier with a different price. Before you
change a number in `data/plans.yaml`, open the page yourself and read it.
`AGENTS.md` rule 3 and rule 5 still bind you. A script report is not a source.

Two page shapes still defeat the pairing. Both now land in `CANNOT COMPARE`
rather than `DRIFT`, but they also explain why coverage is lower than you expect.

- **The stored `plan` string differs from the page label.** `data/plans.yaml`
  stores `Copilot Pro`, but the GitHub pricing table prints `Pro`. The tier name
  is then absent from the table, and the row reads `tier name not found on page`
  or `no price near the tier name`.
- **The page lists every tier name first, then every price.** A column-header
  table gives the last header ownership of all the prices. Most MiniMax rows
  read `no price near the tier name` for this reason.

A `MATCH` can still be luck. `github-copilot-max` stores `100` and the page says
`Copilot Max ... includes $100/month in GitHub AI Credits`. That is the credits
allowance, not the seat price; the two happen to be equal. Treat a `MATCH` on a
prose-heavy page as weak evidence.

## Snapshot diff

The script snapshots a page only when that page left at least one row
`CANNOT COMPARE`. For a page it can parse, the comparison is the answer and a
text diff is noise. For a page it cannot parse, "the page changed since your last
run" is the only signal left, so it earns its place.

`.plan-drift/` is gitignored. A fresh clone carries no baseline, so the first run
reports no snapshot change. The comparison needs no baseline and works at once.

## What the script never does

- It never edits any file under `data/`. It writes only under `.plan-drift/`.
- It does not detect a new tier, a renamed plan, or a changed quota.
- It does not read a price out of an image or a JavaScript bundle.

## Workflow after a flag

1. Read the provider skill under `.claude/skills/provider-<name>/SKILL.md`.
2. Open the page with the tool that skill names. Read the tier.
3. Update the record in `data/plans.yaml` when the value really changed.
4. Set `last_verified` to today. Use `YYYY-MM-DD`.
5. Append one record to `data/changelog.yaml`, newest first.
6. Run `python build.py --check`. Fix every error it prints.
