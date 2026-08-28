# AGENTS.md

Instructions for any agent that updates this repository.

## What this repository is

A tracker for AI coding plans. It holds four datasets in YAML, a Python build
script, and a Jinja template. GitHub Actions renders the datasets into static
HTML tables and deploys them to GitHub Pages on every push to `main`.

The page groups every dataset by provider. Each provider gets its own table
under its own heading. No table has a provider column.

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
9. Use the same provider spelling in all four data files. The build script
   groups rows by that exact string, so a typo splits one provider into two
   tables.

## Layout

| Path | Purpose |
|---|---|
| `data/plans.yaml` | Subscription plans |
| `data/api_pricing.yaml` | Per-model API rates |
| `data/rate_limits.yaml` | Published API rate limits |
| `data/models.yaml` | Model specifications |
| `build.py` | Validation and rendering |
| `templates/index.html.j2` | Page template |
| `assets/` | CSS and JavaScript, copied into the site |
| `.github/workflows/deploy.yml` | Build and deploy workflow |

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
price or a quota.

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
| `region` | yes | enum | `global` or `china`. |
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

The build script derives the monthly equivalent and the saving against the
monthly price, then prints both. Do not write either into the data.

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
| `notes` | no | string | One sentence. |
| `links` | yes | list | See the `links` schema above. Include a `rate limit` entry. |
| `last_verified` | no | date | Date you read the page. |

Write every number as a plain integer. Write `5000000`, not `5,000,000` and not
`5M`. Never set both a split limit and a combined `tokens_per_minute` on one
row. Use the form the provider publishes and leave the other form `null`.

When the published limit is not a number, such as "contact sales", leave the
numeric fields `null` and explain in `notes`.

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
| `vision` | yes | boolean | `true` or `false`. |
| `open_weights` | yes | boolean | `true` or `false`. |
| `notes` | no | string | One sentence. |
| `links` | yes | list | See the `links` schema above. |
| `last_verified` | no | date | Date you read the page. |

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

## Task: add a rate limit

1. Open the provider's own rate-limit page.
2. Append one record per model and tier to `data/rate_limits.yaml`.
3. Add a `rate limit` entry to `links` pointing at that page.
4. Set `last_verified` to today.
5. Run `python build.py --check`.

A provider that publishes no per-model limit gets no record. Zero rows is a
correct result. Do not fill the gap with a number from a third party.

## Task: change the page layout

Edit `templates/index.html.j2` and `assets/style.css`. Run `python build.py` and
open `site/index.html`. Keep every wide table inside its `.table-wrap` container
so the page never scrolls sideways.

Each section renders one `.provider-block` per provider. When you add a column,
update the `colspan` on that table's note row to match the new column count.

## Style

- Write plain English. Keep instruction sentences under 20 words.
- Use the same provider spelling in all four data files.
- Sort nothing by hand. The build script sorts and groups rows for display.
