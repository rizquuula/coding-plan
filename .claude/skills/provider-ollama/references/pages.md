# Ollama — page inventory

Checked 2026-08-28. Every URL below is a page Ollama owns.

## `https://ollama.com/pricing`

Holds every plan card: Free, Pro, Max, Team, and Enterprise. Each card states
its price, its feature bullets, and, for Max, the sign-up-paused notice. Below
the cards sits a full FAQ, grouped under Plans, Team, Models, Usage, Accounts,
and Privacy headings. The Usage section states the 5-hour and 7-day reset
windows, the four usage levels, and the three concurrency limits.

The page is server-rendered HTML, not a client-side app. `curl -sL` returns
every price and every FAQ answer in one request. Strip tags with
`sed 's/<[^>]*>/ /g'` and drop blank lines to read it as plain text. No `.md`
twin exists for this page; it lives on the marketing domain, not on
`docs.ollama.com`.

## `https://ollama.com/search?c=cloud`

Lists every cloud-enabled model as a card linking to `/library/<name>`.
Extract the list with:

```
curl -sL "https://ollama.com/search?c=cloud" | grep -o 'href="/library/[^"]*"' | sort -u
```

17 models returned on 2026-08-28: `deepseek-v4-flash`, `deepseek-v4-pro`,
`gemma4`, `glm-5.1`, `glm-5.2`, `glm-5.3-flash`, `gpt-oss`, `kimi-k2.6`,
`kimi-k2.7-code`, `kimi-k3`, `minimax-m2.7`, `minimax-m3`, `mistral-large-3`,
`nemotron-3-nano`, `nemotron-3-super`, `nemotron-3-ultra`, `qwen3.5`. These are
base library names; a runnable model tag adds a `-cloud` suffix and a size,
for example `gpt-oss:120b-cloud`. Cite the base names in `data/plans.yaml`.

## `https://docs.ollama.com/cloud.md`

Explains what a cloud model is and how to run one, in CLI, Python, JavaScript,
and cURL form. Links to the search page above for the model list. Lists
upcoming and past model retirements with recommended replacements. Holds no
price and no usage quota anywhere on the page.

`docs.ollama.com` is Mintlify. Every page serves a `.md` twin at the same path
with `.md` appended, and `https://docs.ollama.com/llms.txt` indexes them all.

## `https://ollama.com/llms.txt`

A second, separate llms.txt on the marketing domain, distinct from
`docs.ollama.com/llms.txt`. Confirmed to exist and return `text/plain` on
2026-08-28. Not needed for pricing or the model list; both live at the URLs
above.

## `https://ollama.com/settings`

The per-account usage dashboard the FAQ points to for checking quota
consumption ("Check your usage here anytime"). Returns HTTP 200 but the body
is a sign-in redirect; the real dashboard sits behind login. A dead end for
sourcing any public number — do not attempt to scrape it.

## Datasets that get no page

Ollama publishes no numbered rate-limit page and no per-token pricing page.
There is nothing to add to `references/` for those datasets — see "Datasets
with zero rows" in `SKILL.md`.
