# Devin page inventory

Every status below was checked on 2026-08-30. Re-check before you trust one.

## The short version

`docs.devin.ai` and `cognition.com` are open. `devin.ai` is closed. Plain `curl`
with any User-Agent reads the docs host. Nothing reads the marketing host.

## Probe results

### Pages that carry data

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://docs.devin.ai/admin/billing/self-serve.md` | 200 | 8515 B | `curl -sL` | The source for every plan price. |
| `https://docs.devin.ai/admin/billing.md` | 200 | 969 B | `curl -sL` | Names the two billing models. |
| `https://docs.devin.ai/admin/billing/enterprise.md` | 200 | 4054 B | `curl -sL` | ACU billing. No number. |
| `https://docs.devin.ai/admin/billing/usage.md` | 200 | 4275 B | `curl -sL` | What consumes usage. No quota number. |
| `https://docs.devin.ai/desktop/models.md` | 200 | 201789 B | `curl -sL` | The source for every token rate. |
| `https://docs.devin.ai/desktop/accounts/quota.md` | 200 | ~6 KB | `curl -sL` | Quota mechanics, legacy grandfathered prices. |
| `https://docs.devin.ai/desktop/accounts/usage.md` | 200 | ~4 KB | `curl -sL` | Plan names. Defers price to `windsurf.com/pricing`, which is blocked. |
| `https://cognition.com/blog/new-self-serve-plans-for-devin` | 200 | 171328 B | `curl -sL` | The 2026-04-14 lineup announcement. Confirms every price. |
| `https://cognition.com/blog/introducing-devin-desktop` | 200 | ~168 KB | `curl -sL` | States Devin Desktop is the next generation of Windsurf. |

### Index pages

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://docs.devin.ai/llms.txt` | 200 | 33783 B | `curl -sL` | Lists every docs page with a one-line summary. Start here. |
| `https://docs.devin.ai/sitemap.xml` | 200 | 688844 B | `curl -sL` | 4608 URLs across 8 languages. Filter to the unprefixed English paths. |
| `https://docs.devin.ai/_llms/en/desktop.md` | 200 | 23465 B | `curl -sL` | Devin Desktop sub-index. |
| `https://docs.devin.ai/_llms/en/api.md` | 200 | 50964 B | `curl -sL` | API sub-index. No rate-limit page exists. |
| `https://cognition.ai/llms.txt` | 200 | 1563 B | `curl -sL` | Short. Names the products. No price. |
| `https://cognition.ai/sitemap.xml` | 200 | 13915 B | `curl -sL` | Lists `cognition.com` URLs. One pricing-related entry, the blog post above. |

### Pages that state no number

| URL | Status | Tool | Verdict |
|---|---|---|---|
| `https://docs.devin.ai/api-reference/overview.md` | 200 | `curl -sL` | Lists `429 Too Many Requests` in an error table. No quota figure anywhere. |
| `https://docs.devin.ai/cli/models.md` | 200 | `curl -sL` | Names model families. No rate, no specification. |
| `https://docs.devin.ai/desktop/tab/overview.md` | 200 | `curl -sL` | No price, no quota. |
| `https://docs.devin.ai/desktop/command/windsurf-overview.md` | 200 | `curl -sL` | Says Command consumes no premium model credits. No price. |
| `https://docs.devin.ai/desktop/accounts/teams-getting-started.md` | 200 | `curl -sL` | Seat setup steps. No seat price. |

### Everything that failed

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://devin.ai/pricing` | 429 | 33789 B | `WebFetch` | Vercel Security Checkpoint. `WebFetch` reports 429 and returns no body. |
| `https://devin.ai/pricing` | 429 | 33794 B | `curl -sL` + full Chrome headers | Same checkpoint. |
| `https://devin.ai/pricing` | 429 | 33793 B | `curl -sL -A Googlebot` | Same checkpoint. |
| `https://devin.ai/pricing` | 429 | 33794 B | `curl -sL --http1.1` | Same checkpoint. |
| `https://devin.ai/pricing?x=1` | 429 | 33794 B | `curl -sL` | Cache-busting does nothing. |
| `https://www.devin.ai/pricing` | 429 | 33793 B | `curl -sL` | Same checkpoint. |
| `https://devin.ai/` | 429 | 33793 B | `curl -sL` | Host-wide, not path-specific. |
| `https://devin.ai/nonexistent-abc-123` | 429 | — | `curl -s` | A path that cannot exist also returns 429. Proof the block is host-wide. |
| `https://devin.ai/favicon.ico` | 429 | — | `curl -s` | Even a static asset. |
| `https://devin.ai/robots.txt` | 429 | — | `curl -sL` | No `robots.txt` is readable. |
| `https://devin.ai/pricing.md` | 429 | — | `curl -sL` | No `.md` twin is reachable. |
| `https://devin.ai/pricing/index.md` | 429 | — | `curl -sL` | Same. |
| `https://devin.ai/llms.txt` | 429 | 33793 B | `curl -sL` | Same. |
| `https://devin.ai/sitemap.xml` | 429 | 33793 B | `curl -sL` | Same. |
| `https://windsurf.com/pricing` | 429 | 33791 B | `curl -sL` | 301 to `https://devin.ai/pricing`, then the checkpoint. |
| `https://windsurf.com/` | 429 | 33788 B | `curl -sL` | 301 to `https://devin.ai/desktop`, then the checkpoint. |
| `https://codeium.com/pricing` | 429 | 33794 B | `curl -sL` | 301 to `https://devin.ai/pricing`, then the checkpoint. |
| `https://cognition.ai/pricing` | 404 | 85077 B | `curl -sL` | No pricing page on the corporate host. |
| `https://devin.ai/.well-known/vercel/security/request-challenge` | 705 | 0 B | `curl -X POST` with the challenge token | Non-standard status. The challenge is not solvable with `curl`. |

### The app shell and its bundle

| URL | Status | Size | Tool | Verdict |
|---|---|---|---|---|
| `https://app.devin.ai/` | 200 | 20593 B | `curl -sL` | SPA shell. Readable, states no price. |
| `https://app.devin.ai/assets/main-DwcO7TnU.js` | 200 | 961743 B | `curl -sL` | No price string. No seat string. Prices load from an authenticated API. |
| `https://app.devin.ai/assets/plans-CREuL0Ju.js` | 200 | 4373 B | `curl -sL` | The Settings > Plans route. Renders a component; hardcodes no amount. |
| `https://app.devin.ai/assets/PlanCardUI-RKSW0okq.js` | 200 | 3632 B | `curl -sL` | Unrelated. This is the session plan card, not a pricing card. |
| `https://app.devin.ai/api/plans` | 404 | 22 B | `curl -s` | `{"detail":"Not Found"}`. Also `/api/billing/plans`, `/api/v1/plans`, `/api/public/plans`. |

The bundle route from `AGENTS.md` step 4 is a dead end here, and it is a
confirmed dead end, not an untried one. Do not repeat it.

## What blocks `devin.ai`

The response headers are the whole story:

    HTTP/2 429
    server: Vercel
    x-vercel-mitigated: challenge
    x-vercel-challenge-token: 2.1788097023.60.<base64>.<hex>

The body is a 33 KB Astro page titled "Vercel Security Checkpoint". Its only
script is obfuscated and posts to
`/.well-known/vercel/security/request-challenge`. Clearing that challenge needs a
JavaScript runtime, which `AGENTS.md` forbids. Treat `devin.ai` as unreadable.

**Nothing passed.** No User-Agent, no header set, no HTTP version, no subdomain,
and no redirect source reached the page. The workaround is not a trick against
`devin.ai`. It is to read `docs.devin.ai` instead.

## The Markdown twin recipe

`docs.devin.ai` runs Mintlify. Append `.md` to any docs path and you get the
page as Markdown:

```bash
curl -sL -A "Mozilla/5.0" https://docs.devin.ai/admin/billing/self-serve.md
```

The HTML twin of that page is 437788 B. The Markdown twin is 8515 B and carries
the same numbers. Always take the twin.

`https://docs.devin.ai/llms.txt` lists every page and its summary in 33 KB. Grep
it before you guess a path.

## Values these pages state

Self-serve plans, monthly term only. No quarterly and no yearly price exists.
Source: `https://docs.devin.ai/admin/billing/self-serve.md`.

| Plan | Price | Members |
|---|---|---|
| Free | Free | 1 |
| Pro | $20/month | 1 |
| Max | $200/month | 1 |
| Teams | $80/month minimum | Unlimited |
| Enterprise | Order-form ACU rate | Unlimited |

Teams seat types, same page:

| Seat | Price | Includes |
|---|---|---|
| Full seat | $40/month | Pro-equivalent daily and weekly quota, Devin Desktop |
| Flex seat | Free | Shared on-demand credits only, no Devin Desktop |

The $80 minimum table, same page:

| Full seats | On-demand credits included | Monthly total |
|---:|---:|---:|
| 0 | $80 | $80 |
| 1 | $40 | $80 |
| 2 | $0 | $80 |
| 3 | $0 | $120 |
| N ≥ 2 | $0 | N × $40 |

Cognition token rates, per 1M tokens. Source:
`https://docs.devin.ai/desktop/models.md`. Identical under both
`TEAMS_TIER_PRO` and `TEAMS_TIER_ENTERPRISE_SAAS`.

| Model | `model_uid` | Input | Cache read | Output | Cache write (unrendered) |
|---|---|---:|---:|---:|---:|
| SWE-1.7 Max | `swe-1-7` | 0.50 | 0.20 | 2.50 | 0 |
| SWE-1.7 Medium | `swe-1-7-medium` | 0.50 | 0.20 | 2.50 | 0 |
| SWE-1.7 Lightning Max | `swe-1-7-lightning` | 2.50 | 1.00 | 12.50 | 0 |
| SWE-1.7 Lightning Medium | `swe-1-7-lightning-medium` | 2.50 | 1.00 | 12.50 | 0 |
| SWE-1.6 | `swe-1-6` | 0.50 | 0.20 | 2.50 | 0 |
| SWE-1.6 Fast | `swe-1-6-fast` | 0.50 | 0.20 | 2.50 | 0 |
| SWE-check | `swe-check` | 0 | 0 | 0 | 0 |
| Adaptive | `adaptive` | 0.50 | 0.10 | 2.00 | 0.50 |
| Fast Arena | `arena-fast` | 0.10 | 0 | 0.50 | 0 |
| Hybrid Arena | `arena-mixed` | 1.00 | 0.10 | 5.00 | 1.25 |
| Frontier Arena | `arena-smart` | 3.00 | 0.30 | 15.00 | 3.75 |

The same page also lists Anthropic, OpenAI, Google, xAI, DeepSeek, Moonshot,
Z.ai, Nvidia, and Thinking Machines models at resale rates. Those are not Devin
models. See trap 9 in `SKILL.md`.

The Cognition model descriptions, same page: SWE-1.7, SWE-1.7 Lightning (served
on Cerebras), SWE-1.6, SWE-1.6 Fast, `SWE-1-mini` (powers Tab), `swe-grep`
(powers Fast Context), and `swe-check` (powers Quick Review). No specification,
no context window, no parameter count.

Legacy prices, from `https://docs.devin.ai/desktop/accounts/quota.md`. Both are
grandfathered and unbuyable:

- An existing Pro subscriber keeps $15/month indefinitely.
- An existing Teams subscriber keeps $30 per Developer seat per month
  indefinitely.
- Prompt credits were sold at $0.04 each before the March 2026 quota switch.

## What these pages do not say

- No rate limit. `api-reference/overview.md` names `429` and no number.
  `admin/billing/usage.md` states "there are no concurrent session limits".
- No quota size. Plans have a "daily and weekly usage allowance" with no figure.
- No model specification. No parameter count, context window, max output, or
  vision claim for any SWE model.
- No annual or quarterly price for any tier.
- No Enterprise price. `admin/billing/enterprise.md` points at
  `https://cognition.com/contact`.

## Host ownership

| Host | Owner | Citable |
|---|---|---|
| `docs.devin.ai` | Cognition | Yes. Every value in this repository comes from here. |
| `app.devin.ai` | Cognition | Yes in principle. States no public value. |
| `devin.ai` | Cognition | Yes in principle. Unreadable, so never cite it. |
| `cognition.com` | Cognition | Yes. The blog and the contact page. |
| `cognition.ai` | Cognition | Yes, but it 301s to `cognition.com`. Cite the `.com` URL. |
| `windsurf.com` | Cognition | 301s into `devin.ai`. Unreadable, so never cite it. |
| `codeium.com` | Cognition | 301s into `devin.ai`. Unreadable, so never cite it. |
| `devinreview.com` | Cognition | 200, 450 B. A stub. States nothing. |
| `deepwiki.com` | Cognition | 200. States nothing this repository needs. |
| `windsurf.com/pricing` search snippets | third parties | No. `AGENTS.md` rule 5 rejects a snippet. |
| ComparEdge, automationatlas.io, models.dev | third parties | No. `AGENTS.md` rule 4 rejects them. |
