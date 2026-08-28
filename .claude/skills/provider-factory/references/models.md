# Factory — model catalog and multipliers

A multiplier is not a per-token USD rate. This table exists as sourcing
context only, so an agent can check a claim without re-fetching the page. It
is not a source for `data/api_pricing.yaml`, which holds zero Factory rows.

Copied from `https://docs.factory.ai/models.md`, checked 2026-08-28.

## Anthropic

| Model | Model ID | Multiplier | Reasoning |
|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | 4× | off, low, medium, high (default), xhigh, max |
| Claude Opus 5 | `claude-opus-5` | 2× | off, low, medium, high (default), xhigh, max |
| Claude Opus 5 Fast | `claude-opus-5-fast` | 4× | off, low, medium, high (default), xhigh, max |
| Claude Opus 4.8 | `claude-opus-4-8` | 2× | off, low, medium, high (default), xhigh, max |
| Claude Opus 4.8 Fast | `claude-opus-4-8-fast` | 4× | off, low, medium, high (default), xhigh, max |
| Claude Opus 4.7 | `claude-opus-4-7` | 2× | off, low, medium, high (default), xhigh, max |
| Claude Opus 4.6 | `claude-opus-4-6` | 2× | off, low, medium, high (default), max |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | 2× | off (default), low, medium, high |
| Claude Sonnet 5 | `claude-sonnet-5` | 0.8× | off, low, medium, high (default), xhigh, max |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1.2× | off, low, medium, high (default), max |
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | 1.2× | off (default), low, medium, high |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 0.4× | off (default), low, medium, high |

Claude Fable 5 carries a footnote: Anthropic requires Mythos-class models
comply with 30-day data retention, and organization admins opt in on the
model access settings page.

## OpenAI

| Model | Model ID | Multiplier | Reasoning |
|---|---|---|---|
| GPT-5.6 Sol † | `gpt-5.6-sol` | 1.6× | none, low, medium (default), high, xhigh, max |
| GPT-5.6 Sol Fast † | `gpt-5.6-sol-fast` | 3.2× | none, low, medium (default), high, xhigh, max |
| GPT-5.6 Terra | `gpt-5.6-terra` | 0.8× | none, low, medium (default), high, xhigh, max |
| GPT-5.6 Luna | `gpt-5.6-luna` | 0.08× | none, low, medium (default), high, xhigh, max |
| GPT-5.5 | `gpt-5.5` | 2× | low, medium (default), high, xhigh |
| GPT-5.5 Fast | `gpt-5.5-fast` | 5× | low, medium (default), high, xhigh |
| GPT-5.5 Pro | `gpt-5.5-pro` | 12× | medium (default), high, xhigh |
| GPT-5.4 | `gpt-5.4` | 1× | low, medium (default), high, xhigh |
| GPT-5.4 Fast | `gpt-5.4-fast` | 2× | low, medium (default), high, xhigh |
| GPT-5.4 Mini | `gpt-5.4-mini` | 0.3× | low, medium, high (default), xhigh |
| GPT-5.4 Mini Fast | `gpt-5.4-mini-fast` | 0.6× | low, medium, high (default), xhigh |
| GPT-5.3-Codex | `gpt-5.3-codex` | 0.7× | low, medium (default), high, xhigh |
| GPT-5.3-Codex Fast | `gpt-5.3-codex-fast` | 1.4× | low, medium (default), high, xhigh |
| GPT-5.2 | `gpt-5.2` | 0.7× | off, low (default), medium, high, xhigh |

† Promotional pricing. GPT-5.6 Sol bills 1.6× through 2026-11-22, then reverts
to 2×. GPT-5.6 Sol Fast bills 3.2× through 2026-11-22, then reverts to 4×.

## Google

| Model | Model ID | Multiplier | Reasoning |
|---|---|---|---|
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | 0.8× | low, medium, high (default) |
| Gemini 3.7 Flash † | `gemini-3.7-flash` | 0.3× | low, medium, high (default) |
| Gemini 3.6 Flash | `gemini-3.6-flash` | 0.6× | low, medium, high (default) |
| Gemini 3.5 Flash | `gemini-3.5-flash` | 0.6× | minimal, low, medium, high (default) |
| Gemini 3 Flash | `gemini-3-flash-preview` | 0.2× | minimal, low, medium, high (default) |

† Promotional pricing. Gemini 3.7 Flash bills 0.3× through 2027-01-01, then
reverts to 0.6×.

## xAI

| Model | Model ID | Multiplier | Reasoning |
|---|---|---|---|
| Grok 4.6 | `grok-4.6` | 0.8× | low, medium, high (default), xhigh |
| Grok 4.5 | `grok-4.5` | 0.8× | low, medium, high (default) |

## Droid Core (open models)

| Model | Model ID | Multiplier | Reasoning |
|---|---|---|---|
| Inkling | `inkling` | 0.4× | off, minimal, low, medium, high (default), xhigh, max |
| GLM-5.2 | `glm-5.2` | 0.56× | off, high (default), max |
| GLM-5.2 Fast | `glm-5.2-fast` | 0.84× | off, high (default), max |
| Kimi K3 | `kimi-k3` | 1.2× | off, low, high (default), max |
| Kimi K2.7 Code | `kimi-k2.7-code` | 0.38× | off, high (default) |
| Kimi K2.6 | `kimi-k2.6` | 0.4× | off, high (default) |
| Nemotron 3 Ultra | `nemotron-3-ultra` | 0.24× | off, high (default) |
| DeepSeek V4 Flash 0731 | `deepseek-v4-flash-0731` | 0.176× | off, low, high (default), max |
| DeepSeek V4 Pro | `deepseek-v4-pro` | 0.528× | off, low, high (default), max |
| MiniMax M3 | `minimax-m3` | 0.12× | high (default) |
| MiniMax M2.7 ‡ | `minimax-m2.7` | 0.12× | high (default) |
| Kimi K2.5 ‡ | `kimi-k2.5` | 0.25× | off, high (default) |
| GLM-5.1 ‡ | `glm-5.1` | 0.55× | off, high (default) |

‡ Deprecated. MiniMax M2.7, Kimi K2.5, and GLM-5.1 remain available for now
and will be removed in a future release.
