# How GitHub bills Copilot

GitHub changed the billing model on 2026-06-01. Two systems still appear in the
documentation. Keep them apart. Read this file before you write any allowance
into `data/plans.yaml`.

## The current system: GitHub AI Credits

Source: `https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals`,
read 2026-08-28.

An interaction consumes input, output, and cached tokens. GitHub prices each
token by the model, then converts the total into AI credits.

    1 AI credit = 0.01 USD

Every plan includes a monthly credit allowance. The allowance splits in two:

- **Base credits** match the subscription price and never change.
- **Flex allotment** is a variable extra amount. GitHub states that it adapts as
  model pricing changes.

Base credits draw down first. The flex allotment then applies automatically.

Credits do not carry over. The allowance resets at 00:00:00 UTC on the first day
of each calendar month. The reset date does not follow the subscription date.

Code completions and next edit suggestions cost no credits. They stay unlimited
on every paid plan.

These features consume credits: Copilot Chat, Copilot CLI, Copilot cloud agent,
Copilot Spaces, Spark, and third-party coding agents.

A paid plan earns a 10 percent discount on model cost under auto model
selection.

When the credits run out, a subscriber upgrades the plan, sets a budget for
additional usage, or waits for the reset.

## The legacy system: premium requests

Source: `https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/what-changed-with-billing`,
read 2026-08-28.

Before 2026-06-01, each model interaction cost one premium request unit. A model
multiplier scaled that cost. A powerful model consumed more premium requests.

GitHub replaced this system on 2026-06-01. It survives for one closed group:
Copilot Pro and Pro+ subscribers who hold an existing annual plan and who stayed
on the old model. GitHub states that these subscribers receive no new models and
no new features. Their plan ends in a downgrade to Copilot Free.

The legacy figures, for recognition only. **Never write one into a row.**

| Legacy value | Figure |
|---|---|
| Copilot Pro premium requests | 300 per month |
| Copilot Pro+ premium requests | 1500 per month |
| Additional premium request | 0.04 USD each |
| Copilot code review multiplier | 13 |
| Claude Opus 4.8 multiplier | 27 |
| GPT-5.5 multiplier | 57 |

Source for the allowance and the price: `.../request-based-billing-legacy/copilot-requests`.
Source for the multipliers: `.../request-based-billing-legacy/model-multipliers-for-annual-plans`.

## How to tell the two systems apart

Check the URL first. Any path under `copilot-billing/request-based-billing-legacy/`
describes the dead system. Every such page also opens with an `IMPORTANT` note
that names the annual-plan exception.

Check the unit second. A figure in requests or multipliers is legacy. A figure in
credits or in dollars per month is current.

## The label trap on the marketing page

`https://github.com/features/copilot/plans` still names its comparison rows with
the old term, while the cells hold the new unit. These row labels appeared in
the page HTML on 2026-08-28:

    Premium requests: Base credits
    Premium requests: Flex allotment
    Premium requests: Total GitHub AI Credits
    Premium requests: Purchase additional GitHub AI Credits
    Premium requests: Pooled usage

Read the cell, not the label. A grep for "Premium requests" on this page returns
current data under a dead name.

## What this means for the data

`data/plans.yaml` states the allowance in AI credits. The `limits` list for each
GitHub row therefore carries a credit figure, never a request figure.

When you refresh a GitHub row and you find a premium-request number, you read a
legacy page. Go back to `usage-based-billing-for-individuals`.
