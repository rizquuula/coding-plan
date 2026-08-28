# Coding Plan Tracker

**Live site: <https://rizquuula.github.io/coding-plan/>**

Tables of AI coding subscription plans, API rates, rate limits, and model
specifications. The data lives in YAML. A Python script renders it into a static
site that GitHub Actions deploys to GitHub Pages on every push to `main`.

Each provider gets its own table. Every row links to the provider pages its
values came from, labelled by what each page is — `pricing`, `rate limit`,
`model card`.

Inspired by [jia.je/kb — coding plan](https://jia.je/kb/en/software/coding_plan.html),
reshaped into sortable tables.

## What it tracks

| Dataset | File | Contents |
|---|---|---|
| Plans | `data/plans.yaml` | Subscription tiers, prices, quotas, models |
| API pricing | `data/api_pricing.yaml` | Input, cached input, cache write, and output rates per 1M tokens |
| Rate limits | `data/rate_limits.yaml` | Published requests and tokens per minute, per model and usage tier |
| Model specs | `data/models.yaml` | Parameter counts, context window, vision, open weights |

The data files also record a `last_verified` date for each row, which the tables
do not display.

## Build it locally

```bash
pip install -r requirements.txt
python build.py --check   # validate the data only
python build.py           # write site/
python -m http.server -d site 8000
```

Open <http://localhost:8000>.

## Deploy

Push to `main`. The workflow in `.github/workflows/deploy.yml` validates the
data, builds the site, and publishes it to GitHub Pages.

Enable Pages once, before the first deploy:
**Settings → Pages → Build and deployment → Source → GitHub Actions**.

## Update the data

Read `AGENTS.md`. It holds the schema for each file and the steps for adding a
plan or refreshing prices. `CLAUDE.md` points at the same file, so Claude Code
picks up the instructions automatically.

## Accuracy

Providers change prices without notice. Confirm a figure at its source link
before you act on it.
