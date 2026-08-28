# Coding Plan Tracker

**Live site: <https://rizquuula.github.io/coding-plan/>**

Tables of AI coding subscription plans, API rates, and model specifications.
The data lives in YAML. A Python script renders it into a static site that
GitHub Actions deploys to GitHub Pages on every push to `main`.

Inspired by [jia.je/kb — coding plan](https://jia.je/kb/en/software/coding_plan.html),
reshaped into sortable tables.

## What it tracks

| Dataset | File | Contents |
|---|---|---|
| Plans | `data/plans.yaml` | Subscription tiers, prices, quotas, models |
| API pricing | `data/api_pricing.yaml` | Input, cached input, cache write, and output rates per 1M tokens |
| Model specs | `data/models.yaml` | Parameter counts, context window, vision, open weights |

Every row carries a `source` URL and a `last_verified` date. The site marks each
row `fresh`, `stale`, or `unverified` so you can see what needs a check.

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

Seed rows marked `unverified` were entered without checking the provider page.
Confirm a price at its source before you act on it.
