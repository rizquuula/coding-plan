# Ollama — tier detail

Read from `https://ollama.com/pricing` on 2026-08-28. This file is sourcing
context only; `data/plans.yaml` holds the record the site renders.

## Free — $0

- Access cloud models; run 1 cloud model at a time.
- "Light usage": chatting with models, evaluating larger models, coding and
  AI assistants with smaller models.
- Run models on own hardware, unlimited.
- CLI, API, and desktop apps; 40,000+ community integrations.

## Pro — $20/mo, or $200/yr billed annually

Everything in Free, plus:
- Access larger, more powerful cloud models.
- Run 3 cloud models at a time.
- 50x more cloud usage than Free.
- Upload and share private models.
- "Day-to-day work": larger models, coding automation, deep research.

The yearly figure ($200) is the term total as published, not a monthly rate
multiplied out.

## Max — $100/mo

Everything in Pro, plus:
- Run 10 cloud models at a time.
- 5x more usage than Pro.
- "Heavy, sustained usage": continuous agent tasks, multiple concurrent
  agents, large models over extended sessions.

New sign-ups are paused. FAQ wording: "New Max subscriptions are temporarily
paused while we add capacity." The linked answer explains Ollama's cloud
token volume has more than doubled every month, and that existing Max
subscribers keep their plan, limits, and pricing while Pro and Free stay
open. This is a sign-up pause, not a discontinuation — the plan keeps
`status: active`.

## Team — $25/seat/mo, introductory pricing, 5-seat minimum

- 5-seat minimum, so the minimum charge is $125/mo.
- Each additional seat adds $25/mo.
- Usage included per seat; usage beyond that draws from a shared team
  balance billed as you go, "at the model's token rate" (no public rate
  page exists — see trap 5 in `SKILL.md`).
- Access to powerful open models in the US and Europe.
- High performance, up to 2x more than model gateways.
- Zero data retention and logging.
- Shared billing and administration; priority support.
- Coming soon: SSO, model access controls, MDM installer for Windows and
  macOS.
- Sign-up state on 2026-08-28: "Join waitlist", not an open purchase button.
  The card still states a firm price, so it gets a row.

## Enterprise — Custom

- Custom terms and support for larger organizations.
- Everything in Team, plus volume pricing, custom terms, security and
  procurement support, deployment planning with Ollama.
- No numeric price is published. No row in `data/plans.yaml`; see trap 9 in
  `SKILL.md`.

## Usage-level system

The FAQ describes four usage levels, from small/light models (level 1, e.g.
`gpt-oss:20b`) to extra heavy models (level 4, e.g. `deepseek-v4-pro`). A
model's usage level is shown on its own library page. No numeric token cap
exists for any plan or level; usage is measured by weighted input, cached
input, and output tokens against the plan's included allowance.

## Reset windows

Each plan has session limits that reset every 5 hours and weekly limits that
reset every 7 days. No published number backs either window for any plan.

## Concurrency table (from the FAQ)

| Plan | Concurrent cloud models |
|---|---|
| Free | 1 |
| Pro | 3 |
| Max | 10 |

Requests beyond the limit queue up to a fixed depth; a full queue rejects new
requests until a slot opens. This detail is FAQ color, not a number to add to
`data/rate_limits.yaml` — see trap 4 in `SKILL.md`.
