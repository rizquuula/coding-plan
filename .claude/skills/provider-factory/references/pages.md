# Factory — page inventory

Checked 2026-08-28. Every URL below is a page Factory owns.

## `https://docs.factory.ai/pricing/individuals.md`

Holds the Pro, Plus, and Max cards: monthly price, tier feature bullets, and
the "How individual usage works" section that names the three rate-limit
windows, Standard Usage, Droid Core, Extra Usage, and BYOK. Read it with
`curl -sL`. It serves `text/markdown` and needs no `-L` when you request the
`.md` path directly, but the un-suffixed `/pricing` marketing page 308s to
`/pricing/individuals`, so always fetch the `.md` twin of the resolved path.

## `https://docs.factory.ai/pricing/organizations.md`

Holds the Business and Enterprise cards, both "Custom pricing", and the
comparison table of what each tier adds. Read it with `curl -sL`. Confirms
neither tier carries a numeric price — see trap 7 in `SKILL.md`.

## `https://docs.factory.ai/models.md`

Holds the full model catalog, grouped by provider heading (Anthropic, OpenAI,
Google, xAI, Droid Core), each with a `Model`, `Model ID`, `Multiplier`, and
`Reasoning` column. Read it with `curl -sL`.

`WebFetch` on the HTML twin, `https://docs.factory.ai/models`, is a dead end.
It summarized the OpenAI table as "12 models total" and returned no rows.
Always use `curl` on the `.md` path for this page.

## `https://docs.factory.ai/llms.txt`

Lists every documentation page and its `.md` URL, in one plain-text file. Use
it to confirm a page's markdown path before you guess one, or to find a page
this skill does not yet list.

## `https://docs.factory.ai/pricing.md`

A redirect, not a page. It 308s to `/pricing/individuals.md`. Pass `-L` to
`curl` so the redirect resolves, or fetch `/pricing/individuals.md` directly.

## `https://factory.ai/pricing`

The marketing twin of the docs pricing page. It is a Next.js page, not a
Mintlify doc, and carries no `.md` twin. Cite it as a second `plans` link
alongside the docs page; do not use it as the sole source for a number that
`pricing/individuals.md` already states.

## Datasets that get no page

Factory publishes no numbered rate limit page and no per-token pricing page.
There is nothing to add to `references/` for those datasets — see "Datasets
with zero rows" in `SKILL.md`.
