# AGENTS.md

Instructions for any agent that updates this repository.

## What this repository is

A tracker for AI coding plans. It holds three datasets in YAML, a Python build
script, and a Jinja template. GitHub Actions renders the datasets into static
HTML tables and deploys them to GitHub Pages on every push to `main`.

## Rules

1. Edit only the files under `data/`. The build script derives everything else.
2. Never edit `site/`. The build script deletes and rewrites that directory.
3. Never invent a price, a quota, or a parameter count. Copy the value from the
   `source` URL. If you cannot reach the source, leave the row unchanged.
4. `source` must be a page the provider owns. Do not cite a blog, a comparison
   site, or an aggregator. Delete a row before you cite a third party for it.
5. Read the source page yourself before you add or change a value. A search
   result summary is not a source.
6. Set `last_verified` to the date you read the source page. Use `YYYY-MM-DD`.
7. Run `python build.py --check` before you finish. Fix every error it prints.
8. Keep one record per plan tier. Do not merge two tiers into one row.

## Layout

| Path | Purpose |
|---|---|
| `data/plans.yaml` | Subscription plans |
| `data/api_pricing.yaml` | Per-model API rates |
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

## Schema: `data/plans.yaml`

One record per plan tier.

| Field | Required | Type | Rule |
|---|---|---|---|
| `id` | yes | string | Unique across the file. Lower kebab-case, `provider-plan`. |
| `provider` | yes | string | Company name. Use the same spelling in every file. |
| `plan` | yes | string | Tier name as the provider writes it. |
| `region` | yes | enum | `global` or `china`. |
| `price_amount` | yes | number | List price for one seat. Use `0` for a free tier. |
| `price_currency` | yes | enum | `USD`, `CNY`, or `EUR`. |
| `price_period` | yes | enum | `month` or `year`. |
| `limits` | yes | list of strings | One quota statement per item. Keep each under 12 words. |
| `models` | yes | list of strings | Model families the plan unlocks. |
| `status` | yes | enum | `active`, `beta`, or `discontinued`. |
| `notes` | no | string | One sentence. Use `null` when there is nothing to add. |
| `source` | yes | string | URL of the page that states the price. |
| `last_verified` | no | date | Date you read the source. `null` means unverified. |
| `discontinued_on` | no | date | Set only when `status` is `discontinued`. |

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
| `source` | yes | string | URL of the pricing page. |
| `last_verified` | no | date | Date you read the source. |

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
| `source` | yes | string | URL of the model page. |
| `last_verified` | no | date | Date you read the source. |

## Fields the site does not render

The tables show `source` but not `status` or `last_verified`. Both fields stay in
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

1. For each record, open its `source` URL.
2. Update every field that changed.
3. Set `last_verified` to today, even when nothing changed.
4. When a plan disappears, set `status: discontinued` and
   `discontinued_on` to today. Do not delete the record.
5. Run `python build.py --check`.

## Task: change the page layout

Edit `templates/index.html.j2` and `assets/style.css`. Run `python build.py` and
open `site/index.html`. Keep every wide table inside its `.table-wrap` container
so the page never scrolls sideways.

## Style

- Write plain English. Keep instruction sentences under 20 words.
- Use the same provider spelling in all three data files.
- Sort nothing by hand. The build script sorts rows for display.
