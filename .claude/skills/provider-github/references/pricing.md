# GitHub Copilot prices

Read `billing-model.md` first. It explains the unit these figures use.

All figures below come from a fetch on 2026-08-28.

## Individual plan prices

Source: `https://github.com/features/copilot/plans` and
`https://docs.github.com/en/copilot/get-started/plans`.

| Tier | Price per month | Included AI credits |
|---|---|---|
| Copilot Free | 0 USD | An allowance, not stated as a number |
| Copilot Student | 0 USD | An allowance, not stated as a number |
| Copilot Pro | 10 USD | 1,500 |
| Copilot Pro+ | 39 USD | 7,000 |
| Copilot Max | 100 USD | 20,000 |

`data/plans.yaml` carries the three paid tiers. It carries no Free row and no
Student row, because GitHub prints no allowance figure for either.

## Trap: monthly billing only

No GitHub page prints a yearly price for Copilot. The plans page offers no
billing-term toggle. Annual plans exist only as a legacy contract, and GitHub
sells no new one.

So each GitHub record in `data/plans.yaml` holds exactly one `prices` entry,
with `period: month`. Never derive a `year` amount by multiplying.

## Trap: two units for one allowance

The marketing page and the docs state the same allowance in different units.

| Tier | Marketing page prints | Docs print |
|---|---|---|
| Copilot Pro | `$15 monthly total credits for Pro` | `1,500` total monthly AI credits |
| Copilot Pro+ | `$70 monthly total credits for Pro+` | `7,000` total monthly AI credits |
| Copilot Max | `$200 monthly total credits for Max` | `20,000` total monthly AI credits |

One credit costs 0.01 USD, so the two forms agree. Run that multiplication as a
cross-check on every refresh. A disagreement means one page is stale. Report it
rather than picking a side.

## The base and flex split

Source: `https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals`.

| Tier | Base credits | Flex allotment | Total |
|---|---|---|---|
| Copilot Pro | 1,000 | 500 | 1,500 |
| Copilot Pro+ | 3,900 | 3,100 | 7,000 |
| Copilot Max | 10,000 | 10,000 | 20,000 |

GitHub states that the flex allotment varies over time. The base credits do not.
Write the total in `limits`. Do not split the figure across two list items.

## Business and Enterprise seats

Source: `https://docs.github.com/en/copilot/get-started/plans`.

| Plan | Price per seat per month | AI credits per user per month |
|---|---|---|
| Copilot Business | 19 USD | 1,900 |
| Copilot Enterprise | 39 USD | 3,900 |

Credits pool across the billing entity. `data/plans.yaml` holds no row for
either plan today. Adding one is a scope decision, not a sourcing problem. Ask
before you add one.

## Model availability per tier

Source: `https://docs.github.com/en/copilot/get-started/plans`, section
"Available models".

Copilot Pro+ and Copilot Max unlock the same model list. Copilot Pro unlocks
fewer models. These models sat behind Pro+ and Max only on 2026-08-28:

- Claude Opus 4.7, Claude Opus 4.8, Claude Opus 4.8 fast mode, Claude Opus 5
- Claude Fable 5
- GPT-5.4 nano, GPT-5.5, GPT-5.6 Sol

Copilot Pro unlocks Claude Haiku 4.5, Claude Sonnet 4.5, Claude Sonnet 4.6,
Claude Sonnet 5, every listed Gemini model, GPT-5 mini, GPT-5.3-Codex, GPT-5.4,
GPT-5.4 mini, GPT-5.6 Luna, GPT-5.6 Terra, Grok 4.5, Grok 4.6, Kimi K2.7 Code,
Kimi K3, MAI-Code-1-Flash, MAI-Code-1.1-Flash, and Raptor mini.

Copilot Free and Copilot Student reach models through auto model selection only.

Copilot Max lists no extra model. It differs from Pro+ by its credit allowance
and by priority access to a new model.

Seven vendors appear in that table: Anthropic, Google, OpenAI, xAI, Moonshot AI,
Microsoft, and GitHub. Only Raptor mini belongs to GitHub.

## Rate per 1M tokens

Source: `https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing`.

This page prices additional usage inside Copilot, in USD per 1M tokens. **It is
not an API price list.** See `data-recipes.md` for why no GitHub row belongs in
`data/api_pricing.yaml`.

A sample, read 2026-08-28:

| Model | Input | Cached input | Cache write | Output |
|---|---|---|---|---|
| Claude Opus 5 | 5.00 | 0.50 | 6.25 | 25.00 |
| Claude Sonnet 5 | 2.00 | 0.20 | 2.50 | 10.00 |
| Claude Haiku 4.5 | 1.00 | 0.10 | 1.25 | 5.00 |
| GPT-5.6 Sol, default tier | 2.00 | 0.20 | 2.50 | 10.00 |
| GPT-5.6 Terra, default tier | 2.00 | 0.20 | 2.50 | 12.00 |
| Gemini 3.1 Pro, default tier | 2.00 | 0.20 | none | 12.00 |
| Kimi K3 | 3.00 | 0.30 | none | 15.00 |
| Raptor mini | 0.25 | 0.025 | none | 2.00 |

Two structures on this page break a naive read:

1. **A long-context tier costs more.** OpenAI, Google, and xAI models carry a
   `Default` row and a `Long context` row, with a token threshold. GPT-5.6 Sol
   costs 2.00 input at or under 272K tokens and 4.00 input above it.
2. **A promotion hides in a footnote.** GPT-5.6 Sol sells at 50 percent off
   until 2026-09-03. Gemini 3.6 Flash and Gemini 3.7 Flash sell at a promotional
   rate until 2026-12-31.

The promotion is why a Copilot rate can differ from the vendor's own rate.
`data/api_pricing.yaml` holds OpenAI's GPT-5.6 Sol at 4.00 input and 20.00
output, which is the standard rate. Copilot printed 2.00 and 10.00 on the same
day. Both figures are right for their own page. Never move one to the other.
