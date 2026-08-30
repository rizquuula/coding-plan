---
name: check-plan-drift
description: How to sweep every plan price in data/plans.yaml against the provider page that states it, so you only open the pages that look wrong. Use when you check for drift, suspect a price change, refresh prices, check providers, hunt stale data, or want to know which rows to re-verify first. Runs one script that fetches currency-marked prices, compares them, and prints a short report; it names the provider skill for every page it cannot read a price from.
---

# Check plan drift

Read `AGENTS.md` first. Its sourcing rules bind you. This skill adds one script
that does the boring sweep. You read the report and open only the flagged pages.

## What the script checks

The script reads `data/plans.yaml` only. It ignores `data/api_pricing.yaml`,
`data/rate_limits.yaml`, and `data/models.yaml`.

For each plan record it takes the `links` entries labelled `pricing` or `plans`.
Those are the pages that state a price. It skips `docs`, `rate limit`, and
`announcement`. It fetches each unique page once, then runs two checks.

1. Price presence. It compares every `amount` against the prices on the page.
2. Snapshot diff. It compares the page text against the previous run.

## How the script reads a price

The script never searches for a bare number. A bare `18` matches a token count,
and a bare `20` matches the `20` inside `2026`. Both produce a false FOUND, which
hides real drift.

Instead the script extracts only numbers that carry a marker:

- a currency symbol before the number, such as `$20`, `US$20`, `¥199`, `€30`
- a currency code beside the number, such as `20 USD` or `CNY 199`
- a per-period phrase after the number, such as `20 / mo` or `20 per seat per month`

It normalizes each one to a number, handling `1,234.56` and `1.234,56`. Then it
compares your `amount` against that set, within a tolerance of 0.005.

## Quarter and year rows

`AGENTS.md` defines `amount` as the total for the whole term. Many providers
print only a discounted monthly rate, so the term total never appears literally.

The script accepts either form. For a `quarter` row it also tries `amount / 3`,
and for a `year` row it also tries `amount / 12`. When the match came from the
equivalent, the report says `matched as monthly equivalent 19`. Read that line as
"the page states 19 per month", not "the page states 228".

The script tries those two divisors only. A provider that gives free months
breaks the pattern. MiniMax bills a year at ten times the monthly rate, so its
`year` rows report MISSING even when the price never moved. Check the record
`notes` before you treat such a row as drift.

## What the script does not check

- It does not tell you the new price. It only asks whether your number is still there.
- It does not detect a new tier, a renamed plan, or a changed quota.
- It does not open a page that renders client-side. It reports the page instead.
- It does not see a price the page draws as an image or builds in JavaScript.
- It never edits any file under `data/`. It writes only under `.plan-drift/`.

## How to run it

```bash
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --provider Cursor
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --json
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --timeout 60
python .claude/skills/check-plan-drift/scripts/check_plan_drift.py --update-snapshots
```

`--provider` matches the `provider` field without case. `--json` prints the whole
report as JSON. `--timeout` sets the fetch timeout in seconds, default 30.
`--update-snapshots` writes the snapshots and skips the diff section.

Exit codes: `0` when nothing needs attention, `1` when a price is `MISSING` or a
snapshot changed, `2` when the script itself failed.

## How to read each status

| Status | Meaning | Do this |
|---|---|---|
| `MISSING PRICE` | The amount is not on the page text. | Open the page and read the tier. |
| `CHANGED SNAPSHOT` | The page text moved since the last run. | Skim the page for a price or a tier change. |
| `BLOCKED` | The page returned 401 or 403, or served a bot challenge. | Read the provider skill the report names. |
| `UNREADABLE` | The page returned 200 but almost no text. | Read the provider skill the report names. |
| `NO PRICES FOUND` | The page has text but states fewer than 2 prices. | Read the provider skill the report names. |
| `ERROR` | The network call failed. | Re-run. Raise `--timeout` when it times out. |
| `UNCHANGED` | Counts only. | Do nothing. |

`BLOCKED`, `UNREADABLE`, and `NO PRICES FOUND` say nothing about the price.
Claim nothing from them.

`NO PRICES FOUND` means the page builds its prices in the browser. Cursor hides
its higher tiers behind a toggle, and Novita ships a shell page. The script
reports one line for such a page instead of one MISSING row per amount. Read the
provider skill, which names the script or the bundle that holds the real figure.

## `MISSING` is a hint, not evidence

A `MISSING` row means the page states at least two prices, and yours is not among
them. That is a real signal, but it is not proof. The page may write the figure
in a shape the extractor misses, or state it only under a toggle.

Before you change a number in `data/plans.yaml`, open the page yourself and read
it. `AGENTS.md` rule 3 and rule 5 still bind you. A search result summary is not
a source, and a script report is not a source either.

## Workflow after a flag

1. Read the provider skill under `.claude/skills/provider-<name>/SKILL.md`.
2. Open the page with the tool that skill names. Read the tier.
3. Update the record in `data/plans.yaml` when the value really changed.
4. Set `last_verified` to today. Use `YYYY-MM-DD`.
5. Append one record to `data/changelog.yaml`, newest first.
6. Run `python build.py --check`. Fix every error it prints.

## Known limitation

`.plan-drift/` is gitignored. A fresh clone carries no baseline, so the first run
reports `NEW BASELINE` for every page and finds no snapshot change. Run the
script once to take the baseline, then again later to see drift.

The price presence check needs no baseline. It works on the first run.

The script snapshots every page that returned text, including a
`NO PRICES FOUND` page. A diff on such a page still tells you the page changed.
