# AGENTS.md

Instructions for any agent that updates this repository.

## What this repository is

A tracker for AI coding plans. It holds five datasets in YAML, a Python build
script, and a set of Jinja templates. GitHub Actions renders the datasets into
static HTML tables and deploys them to GitHub Pages on every push to `main`.

The build script writes four pages. `index.html` holds the plans,
`api-pricing.html` holds the API rates merged with the model specifications,
`rate-limits.html` holds the rate limits, and `changelog.html` holds the notable
dataset changes. Every data page groups its dataset by provider.

`index.html` holds one table for every plan. A provider column carries the
provider name, and the rows of one provider sit together in one band. The other
two data pages still split their dataset. Each provider gets its own table under
its own heading, and neither table has a provider column.

`api-pricing.html` left-joins `data/api_pricing.yaml` onto `data/models.yaml` on
the provider and the model name. A model with no rate row still gets a row, and
a rate row with no model record still gets a row. Keep the model name in
`data/api_pricing.yaml` equal to the `name` in `data/models.yaml`, or the two
records render as two rows.

## Rules

1. Edit only the files under `data/`. The build script derives everything else.
2. Never edit `site/`. The build script deletes and rewrites that directory.
3. Never invent a price, a quota, or a parameter count. Copy the value from a
   page in `links`. If you cannot reach the page, leave the row unchanged.
4. Every `links` URL must be a page the provider owns. Do not cite a blog, a
   comparison site, or an aggregator. Delete a row before you cite a third party.
5. Read the page yourself before you add or change a value. A search result
   summary is not a source.
6. Set `last_verified` to the date you read the page. Use `YYYY-MM-DD`.
7. Run `python build.py --check` before you finish. Fix every error it prints.
8. Keep one record per plan tier. Do not merge two tiers into one row.
9. Use the same provider spelling in all five data files. The build script
   groups rows by that exact string, so a typo splits one provider into two
   tables.
10. Append a changelog record whenever you add or change a row in another
    dataset. Newest entry first, one entry per change.

## Layout

| Path | Purpose |
|---|---|
| `data/plans.yaml` | Subscription plans |
| `data/api_pricing.yaml` | Per-model API rates |
| `data/rate_limits.yaml` | Published API rate limits |
| `data/models.yaml` | Model specifications |
| `data/changelog.yaml` | Notable dataset changes |
| `build.py` | Validation and rendering |
| `templates/base.html.j2` | Page skeleton: head, sidebar, main, footer |
| `templates/macros.html.j2` | Shared table macros |
| `templates/index.html.j2` | The plans page |
| `templates/api_pricing.html.j2` | The API pricing and models page |
| `templates/rate_limits.html.j2` | The rate limits page |
| `templates/changelog.html.j2` | The changelog page |
| `assets/` | CSS and JavaScript, copied into the site |
| `assets/anime.umd.min.js` | anime.js 4.5.0, vendored. Do not edit it |
| `.claude/skills/provider-*/` | How to source one provider's data |
| `.github/workflows/deploy.yml` | Build and deploy workflow |

## Provider skills

Each provider that is hard to source gets a skill under
`.claude/skills/provider-<name>/`. It records which of that provider's pages an
agent can read, which pages look right and are not, and the traps that produce a
wrong number.

    provider-<name>/
      SKILL.md        the page map, the traps, the workflow
      references/     the detail, read on demand
      scripts/        anything runnable

Read the skill for a provider before you touch one of its rows. Write back to it
whenever you learn something it does not say — a page that moved, a value that is
not where you expected, a fetch that fails. A wrong claim in a skill costs the
next agent more than a gap.

| Provider | Skill |
|---|---|
| Alibaba (Qwen) | `provider-alibaba` |
| Anthropic | `provider-anthropic` |
| BytePlus (ModelArk) | `provider-byteplus` |
| ClinePass | `provider-clinepass` |
| CommandCode | `provider-commandcode` |
| Cursor | `provider-cursor` |
| DeepSeek | `provider-deepseek` |
| Devin | `provider-devin` |
| Factory | `provider-factory` |
| GitHub | `provider-github` |
| Google | `provider-google` |
| Kiro | `provider-kiro` |
| MiniMax | `provider-minimax` |
| Meta | `provider-meta` |
| Mistral | `provider-mistral` |
| Moonshot (Kimi) | `provider-moonshot` |
| Novita | `provider-novita` |
| Ollama | `provider-ollama` |
| OpenAI | `provider-openai` |
| OpenCode (Go) | `provider-opencode` |
| Sakana (Fugu) | `provider-sakana` |
| Verboo | `provider-verboo` |
| Zhipu (GLM) | `provider-zai` |

Every provider in the data has a skill. When you add a new provider, add a
skill for it and extend this table.

### Cross-provider skills

One skill works across every provider. It is not a provider skill, so it stays
out of the table above.

| Skill | Purpose |
|---|---|
| `check-plan-drift` | Sweep every plan price against the page that states it. |

## Sourcing tools

Do not use Playwright, Puppeteer, Selenium, or a headless browser to source a
value. Rule 5 stands: read the page yourself. A scraped string is not a source.

A browser is allowed for one job only. Use it to check the rendered site after
you change a template or the stylesheet. Never use it to read a price.

Try these in order:

1. `WebFetch` on the page.
2. The provider's `.md` twin, when it serves one.
3. `curl` on the page HTML.
4. `curl` on the JavaScript bundle, or on a public JSON endpoint the page calls.

A page that only renders client-side is not a dead end. Its data usually sits in
a bundle or in an API the page calls. The `provider-zai` skill is the worked
example.

## Commands

```bash
pip install -r requirements.txt
python build.py --check   # validate the data only
python build.py           # validate, then write site/
python -m http.server -d site 8000   # preview at http://localhost:8000
```

## Schema: `links`

Every record in every dataset carries a `links` list. The site renders one
labelled link per entry, so a reader can go straight to the page that states a
price or a quota. Every table link opens in a new tab. The `links_cell` macro
in `templates/macros.html.j2` is the only place that renders one.

```yaml
  links:
    - label: pricing
      url: https://claude.com/pricing
    - label: rate limit
      url: https://platform.claude.com/docs/en/api/rate-limits
```

Rules:

1. The list needs at least one entry.
2. Each entry has exactly two keys, `label` and `url`. No other key validates.
3. `url` must start with `https://`.
4. `label` must be one of these six strings. Nothing else validates.

| Label | Use it for |
|---|---|
| `pricing` | A page that states a price or a per-token rate. |
| `plans` | A page that compares subscription tiers. |
| `rate limit` | A page that states a request or token quota. |
| `model card` | A page that states a model's specifications. |
| `docs` | Provider documentation that is none of the above. |
| `announcement` | A provider blog post or launch note. |

Pick the label by what the page is, not by which table the row sits in. Add a
second entry when the provider states the quota on a different page from the
price.

## Schema: `data/plans.yaml`

One record per plan tier.

| Field | Required | Type | Rule |
|---|---|---|---|
| `id` | yes | string | Unique across the file. Lower kebab-case, `provider-plan`. |
| `provider` | yes | string | Company name. Use the same spelling in every file. |
| `plan` | yes | string | Tier name as the provider writes it. |
| `price_currency` | yes | enum | `USD`, `CNY`, or `EUR`. |
| `prices` | yes | list | One entry per billing term. See the `prices` schema below. |
| `limits` | yes | list of strings | One quota statement per item. Keep each under 12 words. Name the model when the provider publishes a per-model quota. |
| `models` | yes | list of strings | Model families the plan unlocks. |
| `status` | yes | enum | `active`, `beta`, or `discontinued`. |
| `notes` | no | string | One sentence. Use `null` when there is nothing to add. |
| `links` | yes | list | See the `links` schema above. |
| `last_verified` | no | date | Date you read the page. `null` means unverified. |
| `discontinued_on` | no | date | Set only when `status` is `discontinued`. |

## Schema: `prices`

A tier is often billed monthly, quarterly, and yearly, and the longer terms cost
less. One record holds every term the provider offers. Do not split a tier into
one record per term.

```yaml
  price_currency: USD
  prices:
    - period: month
      amount: 80
    - period: quarter
      amount: 192
    - period: year
      amount: 672
```

Rules:

1. The list needs at least one entry.
2. Each entry has exactly two keys, `period` and `amount`. No other key validates.
3. `period` is `month`, `quarter`, or `year`. No period repeats in one record.
4. `amount` is the price charged for one seat for that whole term. It is not the
   monthly equivalent. Write `672` for a year billed at 56 per month.
5. `amount` must not be negative. Use `0` for a free tier.

Every price renders per month. The build script divides each term total by its
months and prints that figure as the headline. When the term is not a month it
also prints the term total and the saving, as `billed $200.00/year - save 17%`.
Do not write the monthly figure or the saving into the data.

Some providers print only a discounted monthly rate, not the term total. Copy
the rate, multiply it by the term, and say so in `notes`. Z.ai is the worked
example in `data/plans.yaml`.

## Schema: `data/api_pricing.yaml`

One record per model. Every rate is per 1M tokens.

| Field | Required | Type | Rule |
|---|---|---|---|
| `id` | yes | string | Unique across the file. |
| `provider` | yes | string | Company name. |
| `model` | yes | string | Display name. |
| `model_id` | no | string | API model string. |
| `context_window` | no | string | Short form, such as `200K` or `1M`. |
| `currency` | yes | enum | `USD`, `CNY`, or `EUR`. |
| `input` | yes | number | Uncached input rate. |
| `cached_input` | no | number | Cache-read rate. `null` when the provider publishes none. |
| `cache_write` | no | number | Cache-write rate. `null` when the provider publishes none. |
| `output` | yes | number | Output rate. |
| `notes` | no | string | One sentence. |
| `links` | yes | list | See the `links` schema above. |
| `last_verified` | no | date | Date you read the page. |

## Schema: `data/rate_limits.yaml`

One record per provider, model, and usage tier. A provider that publishes three
tiers for one model gets three records. Do not average two tiers into one row.

| Field | Required | Type | Rule |
|---|---|---|---|
| `id` | yes | string | Unique across the file. Lower kebab-case, `provider-model-tier`. |
| `provider` | yes | string | Company name. Match the spelling in `data/api_pricing.yaml`. |
| `model` | yes | string | Display name. Match `data/api_pricing.yaml`. |
| `tier` | yes | string | Tier name as the provider writes it. Use `Default` when the provider publishes one set. |
| `requests_per_minute` | no | number | `null` when unpublished. |
| `input_tokens_per_minute` | no | number | `null` when unpublished. |
| `output_tokens_per_minute` | no | number | `null` when unpublished. |
| `tokens_per_minute` | no | number | Combined input and output limit. `null` when the provider publishes a split instead. |
| `requests_per_day` | no | number | `null` when unpublished. |
| `concurrent_requests` | no | number | `null` when unpublished. Concurrent connections, counted as the provider defines them. |
| `notes` | no | string | One sentence. |
| `links` | yes | list | See the `links` schema above. Include a `rate limit` entry. |
| `last_verified` | no | date | Date you read the page. |

Write every number as a plain integer. Write `5000000`, not `5,000,000` and not
`5M`. Never set both a split limit and a combined `tokens_per_minute` on one
row. Use the form the provider publishes and leave the other form `null`.

When the published limit is not a number, such as "contact sales", leave the
numeric fields `null` and explain in `notes`.

## Schema: `data/changelog.yaml`

One record per notable dataset change. The page renders newest first, so keep
the file newest first too. A change to several providers is one record per
provider.

| Field | Required | Type | Rule |
|---|---|---|---|
| `id` | no | string | Lower kebab-case. Optional; omit when the date and provider identify the entry. |
| `date` | yes | date | The day the change landed in the repository. |
| `provider` | yes | string | Company name. Match the spelling in the dataset the change touches. |
| `type` | yes | enum | `new provider`, `new model`, `price update`, `rate limit change`, or `update`. |
| `summary` | yes | string | One sentence describing the change. |
| `links` | no | list | See the `links` schema above. Point at the page that states the change. |
| `last_verified` | no | date | Date you read the page. |

## Schema: `data/models.yaml`

One record per model.

| Field | Required | Type | Rule |
|---|---|---|---|
| `id` | yes | string | Unique across the file. |
| `name` | yes | string | Display name. |
| `provider` | yes | string | Company name. |
| `total_params` | no | string | Short form, such as `1.6T`. `null` when unpublished. |
| `active_params` | no | string | Active parameters per token. `null` when unpublished. |
| `context_window` | no | string | Short form. |
| `max_output` | no | string | Short form. |
| `vision` | no | boolean | `true`, `false`, or `null`. See the rule below. |
| `open_weights` | no | boolean | `true`, `false`, or `null`. See the rule below. |
| `notes` | no | string | One sentence. |
| `links` | yes | list | See the `links` schema above. |
| `last_verified` | no | date | Date you read the page. |

### The `open_weights` and `vision` rule

Both fields carry the same three states. A page in `links` must state the
capability before you write `true`. A page must state its absence before you
write `false`. Silence means `null`.

For `open_weights`, set `true` only when a page says that model is open-source
or open-weight, or links its weights. Set `false` only when a page says the
weights are closed. Otherwise set `null`.

For `vision`, set `true` only when a page says that model reads images. Set
`false` only when a page says it takes text only. Otherwise set `null`.

A ranking claim is not a membership claim. "SOTA among open-source models"
compares the model to a group. It does not say the model belongs to that group.
Treat it as unstated and write `null`.

Never write `false` because you found nothing. `false` is a claim, and an
unsourced claim breaks rule 3. The site renders `null` as an em dash.

## Fields the site does not render

The tables show `links` but not `status` or `last_verified`. Both fields stay in
the data as provenance for you, the agent. Two consequences:

- A reader cannot see that a plan is discontinued. When you set
  `status: discontinued`, also say so in `notes`, which does render.
- A reader cannot see how old a row is. Keep `last_verified` accurate anyway —
  it tells the next agent which rows to re-check first.

## Task: add a plan

1. Open the provider's pricing page and read the tier.
2. Append a record to `data/plans.yaml` following the schema above.
3. Set `last_verified` to today.
4. Run `python build.py --check`.

## Task: refresh prices

1. For each record, open every URL in its `links` list.
2. Update every field that changed.
3. Set `last_verified` to today, even when nothing changed.
4. When a plan disappears, set `status: discontinued` and
   `discontinued_on` to today. Do not delete the record.
5. Run `python build.py --check`.

## Task: check for drift

1. Run `python .claude/skills/check-plan-drift/scripts/check_plan_drift.py`.
2. Read the report. It marks every stored price MATCH, DRIFT, or CANNOT COMPARE.
3. Open each flagged page yourself and read the value. The report is not a source.
4. Update the record in `data/plans.yaml` and append a `data/changelog.yaml` entry.
5. Run `python build.py --check`.

## Task: add a rate limit

1. Open the provider's own rate-limit page.
2. Append one record per model and tier to `data/rate_limits.yaml`.
3. Add a `rate limit` entry to `links` pointing at that page.
4. Set `last_verified` to today.
5. Run `python build.py --check`.

A provider that publishes no per-model limit gets no record. Zero rows is a
correct result. Do not fill the gap with a number from a third party.

## Task: log a dataset change

1. After you add or change a row in another dataset, append one record to
   `data/changelog.yaml`.
2. Set `date` to today, `provider` to the provider spelling from the dataset,
   and `type` to the change kind. Write a one-sentence `summary`.
3. Keep the file newest first.
4. Run `python build.py --check`.

## Task: change the page layout

Edit the templates and `assets/style.css`. Run `python build.py` and open the
page you changed. Keep every wide table inside its `.table-wrap` container so
the page never scrolls sideways.

`.content` sets no width cap, so a table fills the window. Prose stays readable
because `.lede` and `.section-note` cap themselves at 60ch.

`.table-wrap` scrolls inside its own box above 720 pixels. The plans table adds
`table-wrap-flow`, which drops that box. Three rules follow from it:

1. The plans table must fit the content width. It carries no scroller, so an
   overflow is clipped, not scrolled. Measure the table before you add a column.
2. With no scroll container the header row sticks to the viewport. Under 960
   pixels the sidebar is sticky too, so `--stick-top` pushes the header clear of
   it. Change one and you must check the other.
3. `.price-equiv` may wrap. `.num` sets `nowrap`, and that held the Price column
   open past the content width. `th.num` carries a preferred width, not a
   minimum, so the line only wraps on a narrow screen.

The templates split three ways. `templates/base.html.j2` holds the skeleton, the
sidebar, and the theme switcher. `templates/macros.html.j2` holds every table
macro. Each page template extends the base and fills its blocks.

The API pricing page and the rate limits page render one `.provider-block` per
provider. The plans page renders one table instead. When you add a column, do
three things. Update the `colspan` on that table's note row. Add a `data-label`
to the new cell. Copy the label text from the new `<th>` exactly.

The plans note row keeps `colspan="5"`, not 6. The provider band already covers
the first column of that row.

### The plans table

`templates/macros.html.j2` renders the plans page through
`plan_table_grouped(groups)`. It writes one table with one `<tbody>`, and it
sorts the rows by provider first.

1. Every data row carries `data-provider` and an inline `--brand` and
   `--brand-ink` pair. `build.py` reads both colours from `PROVIDER_BRAND`.
2. The first row of a provider run carries an extra first cell,
   `<td class="provider-cell" rowspan="N">`. `N` counts every `<tr>` the run
   emits, so a note row counts too.
3. The cell prints the provider name sideways through `.provider-label`.
   A run under 3 rows tall gets the class `is-short`, which prints the name flat.
4. The first run of a provider keeps `id="plans-<slug>"`. The sidebar anchor
   points at that id.
5. `rebuildSpans(table)` in `assets/app.js` must run after any filter pass and
   after any sort. A sort interleaves providers, so every band changes. The
   function deletes every `.provider-cell` and builds the runs again.
6. A header click cycles three states: ascending, descending, then the default
   order. `stampOrder` writes `data-order` on each row before any sort runs,
   and `resetSort` reads it back. Never reorder the rows before `stampOrder`.
7. Under 720 pixels the band disappears. The card prints the provider as a tag
   from the `data-provider` attribute instead.

### The card layout

Under 720 pixels every table becomes a list of cards. One row becomes one card.
The stylesheet prints the column name from the cell's `data-label`, so a cell
without one prints no label. The first cell of a row carries `class="cell-title"`
and renders as the card title, so it needs no `data-label`.

Above 720 pixels the tables render as tables. Nothing changes there.

Three rules keep the card layout working:

1. Never set `display` on an element that the filter hides. The filter sets the
   `hidden` property. A `display` rule beats the browser's own `[hidden]` rule,
   so the filter stops hiding rows. The stylesheet restores it with
   `.data-table tr[hidden] { display: none !important; }`.
2. Never hide a row in the base stylesheet. `assets/app.js` adds the
   `motion-ready` class to `<html>` only after anime.js loads. Every start state
   for an animation sits behind that class. A reader without JavaScript then
   sees every row.
3. `assets/app.js` loads anime.js only when the reader allows motion. Keep that
   gate. The file weighs 115 KB, and a reader who sets
   `prefers-reduced-motion: reduce` must never download it.

`build.py` passes a `nav` value to every page. It carries the page links and one
anchor per provider block on the current page. Add a section to a page and you
must extend the `provider_anchors` call for that page, or the sidebar misses it.
The changelog page carries no provider anchors, so its `nav` passes an empty
list.

## Style

- Write plain English. Keep instruction sentences under 20 words.
- Use the same provider spelling in all four data files.
- Sort nothing by hand. The build script sorts and groups rows for display.
