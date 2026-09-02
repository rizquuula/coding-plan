# ⚡ Coding Plan Tracker

[![Deploy](https://github.com/rizquuula/coding-plan/actions/workflows/deploy.yml/badge.svg)](https://github.com/rizquuula/coding-plan/actions/workflows/deploy.yml)

**Every AI coding plan. Every API rate. Every rate limit. One site, every number sourced.**

### 👉 **[rizquuula.github.io/coding-plan](https://rizquuula.github.io/coding-plan/)** 👈

Stop tab-hopping between 13 pricing pages to figure out whether Claude Max
beats Cursor Ultra, or what GLM Coding Pro actually costs per year. This
tracker puts **227 rows of plans, per-token rates, rate limits, and model
specs** side by side — and every single value links straight to the provider
page it came from.

## 🔥 Why it's different

- **🧾 Receipts on every row.** No number lives here without a link to the
  provider's own page — labelled `pricing`, `rate limit`, `model card`. No
  blogs, no aggregators, no vibes.
- **🌏 Global *and* China regions.** Qwen, Kimi, GLM, DeepSeek tracked
  alongside Anthropic, OpenAI, Google, Cursor, GitHub, and more.
- **💰 Real math, done for you.** Yearly billing? The site derives the monthly
  equivalent and the % saved against monthly — you just read the table.
- **🔍 Sortable, themeable, fast.** Static HTML, zero backend, dark mode.
  Click a header, sort a column, done.
- **📱 Reads on a phone.** Under 720px every table folds into cards — no
  pinching, no sideways scrolling, even on the 12-column pricing table. Rows
  animate in as you scroll, and if you've asked your OS for less motion, the
  animation library is never even downloaded.
- **🤖 Built to be maintained by agents.** Strict YAML schemas, a validating
  build, and per-provider sourcing skills mean updates are verifiable, not
  hand-wavy.

## 📊 What it tracks

| Dataset | File | Contents |
|---|---|---|
| 💳 Plans | `data/plans.yaml` | Subscription tiers, prices, quotas, models |
| 🪙 API pricing | `data/api_pricing.yaml` | Input, cached input, cache write, and output rates per 1M tokens |
| 🚦 Rate limits | `data/rate_limits.yaml` | Requests and tokens per minute, per model and usage tier |
| 🧠 Model specs | `data/models.yaml` | Parameter counts, context window, vision, open weights |

Every row also carries a `last_verified` date, so staleness is tracked — not
hidden.

## ⚙️ How it works

YAML in, website out. A Python script validates the four datasets, renders
Jinja templates into static HTML, and GitHub Actions ships it to GitHub Pages
on every push to `main`. No database, no server, no build farm.

```bash
# Requires Python 3.8 or later.
pip install -r requirements.txt
python3 build.py           # renders site/
python -m http.server -d site 8000
```

Output lands in `site/`. Open `site/index.html` in your browser or run the
HTTP server above and visit http://localhost:8000.

## 🚀 Deploy your own

Push to `main`. The workflow in `.github/workflows/deploy.yml` validates,
builds, and publishes. Enable Pages once, before the first deploy:
**Settings → Pages → Build and deployment → Source → GitHub Actions**.

## ✍️ Update the data

Read `AGENTS.md` — it holds the schema for each file, the sourcing rules, and
the step-by-step tasks. `CLAUDE.md` points at the same file, so Claude Code
picks up the rules automatically and can refresh the data for you.

## 🤝 Contributing

Spotted a stale price? PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
Licensed under [MIT](LICENSE).

## ⚠️ Accuracy

Providers change prices without notice. Every row links to its source —
confirm a figure there before you act on it.

---

Inspired by [jia.je/kb — coding plan](https://jia.je/kb/en/software/coding_plan.html),
reshaped into sortable, sourced tables.
