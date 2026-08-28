# Z.ai model specifications

This file covers `data/models.yaml` and the model fields in
`data/api_pricing.yaml`. It holds 21 Zhipu model rows and 22 API pricing rows,
read on 2026-08-28.

No single page carries a full model specification. Each field comes from a
different page. Read the table below before you fill a row.

## Where each model field comes from

| Field | Page |
|---|---|
| `context_window` | `https://docs.z.ai/guides/overview/overview.md` |
| `max_output` | `https://docs.z.ai/api-reference/llm/chat-completion.md` |
| `model_id` | `https://docs.z.ai/api-reference/llm/chat-completion.md` |
| `total_params`, `active_params` | Four guide pages only. See below. |
| `vision` | The model matrix, plus the `llm/` or `vlm/` path of its guide |
| `open_weights` | The model's own guide page. See the trap below. |

## Start at the model matrix

`https://docs.z.ai/guides/overview/overview.md` is the entry point. It lists
every model, its context window, and a link to that model's own guide page.

Do not start at one model's guide page. The old version of this skill sent
agents to `guides/llm/glm-5.3`, which covers one model out of 21.

## Trap: `chat-completion.md` states `max_tokens` twice

The page carries two request schemas. Each schema has its own `max_tokens`
description, and the two describe different models. Read both.

`ChatCompletionTextRequest` states:

| Series | Max output |
|---|---|
| GLM-5.3, GLM-5.2, GLM-5.1, GLM-5, GLM-4.7, GLM-4.6 | 128K |
| GLM-4.5 series | 96K |
| GLM-4.6v series | 32K |
| GLM-4.5v series | 16K |
| GLM-4-32B-0414-128K | 16K |

`ChatCompletionVisionRequest` states:

| Model | Max output |
|---|---|
| GLM-5.3-Flash | 128K |
| GLM-5V-Turbo | 128K |

**The vision schema is the only source for GLM-5.3-Flash and GLM-5V-Turbo.** An
agent that reads only the first `max_tokens` block finds nothing for those two
models. Do not guess the missing value.

The same split applies to `model_id`. The text enum holds 15 models. The vision
enum holds 7, including `glm-5.3-flash`. Read both enums.

## Trap: GLM-OCR has no `model_id`

GLM-OCR is absent from both enums. The matrix routes it to
`/api-reference/tools/layout-parsing`, not to chat completion.

Its `data/api_pricing.yaml` row carries `model_id: null` and
`context_window: null`. The matrix prints `/` for its context window, which is
not a number. GLM-OCR has no `data/models.yaml` row.

## Trap: GLM-5.3-Flash sits under `vlm/`, not `llm/`

Its guide page is `https://docs.z.ai/guides/vlm/glm-5.3-flash`. Z.ai classifies
it as a native multimodal model.

`https://docs.z.ai/guides/llm/glm-5.3-flash` returns 308 and redirects to the
`vlm/` path. The `.md` twin returns 307 to the same place. Follow the redirect
or use the `vlm/` path directly.

## Trap: "open-source" on a GLM page is usually a ranking claim

`AGENTS.md` has a section called "The `open_weights` rule". Read it. A ranking
claim is not a membership claim, and an unstated value is `null`.

The word "open-source" appears on nearly every GLM page. **A grep hit proves
nothing. Read the sentence.** Almost every page says only "SOTA among
open-source models" or "ranks first among open-source models". Both compare the
model to a group. Neither says the model belongs to it.

Exactly three Zhipu models clear the bar. Each has a sentence that applies the
noun phrase to the model itself:

| Model | The sentence |
|---|---|
| GLM-5.3-Flash | "It is the first open-source frontier model to adopt a hybrid architecture…" |
| GLM-5.2 | "GLM-5.2 is the strongest open-source model…" |
| GLM-4.5 | "GLM-4.5 demonstrates a strong competitive advantage over other open-source models…" |

The other 18 Zhipu rows carry `null`. **No Zhipu row carries `false`.**

No page on `docs.z.ai` links model weights or names a licence. The only
HuggingFace links point at `datasets/zai-org/CC-Bench-trajectories`, which is
benchmark data, not weights. `llms.txt` lists no licence page. So a weights link
is not available as a second source.

## Trap: only four pages publish a parameter count

A grep for "parameters" hits architecture prose on many pages. Only these four
pages state a count, and they cover five models.

| Model | `total_params` | `active_params` | Page |
|---|---|---|---|
| GLM-5.3-Flash | 320B | 18B | `/guides/vlm/glm-5.3-flash` |
| GLM-5 | 744B | 40B | `/guides/llm/glm-5` |
| GLM-4.5 | 355B | 32B | `/guides/llm/glm-4.5` |
| GLM-4.5-Air | 106B | 12B | `/guides/llm/glm-4.5` |
| GLM-4.5V | 106B | 12B | `/guides/vlm/glm-4.5v` |

Every other model carries `null` for both fields.

The GLM-5 sentence reads "Increased from 355B (32B activated) to 744B (40B
activated)". The "from" figure is GLM-4.5. The "to" figure is GLM-5. It is easy
to misattribute, so read the whole sentence.

**Do not extend a figure to a sibling variant.** The GLM-4.5 page names GLM-4.5
and GLM-4.5-Air only. GLM-4.5-X, GLM-4.5-AirX, and GLM-4.5-Flash have no
published count.

## Two values that look wrong and are right

- **GLM-4.5V context is 64K**, not 128K. Every other GLM-4.x vision model is
  128K, so 64K reads like a typo. It is not. Do not "correct" it.
- **GLM-4.5-Flash is 200K context and 96K max output.** The context comes from
  the matrix. The max output comes from the GLM-4.5 series rule on
  `chat-completion.md`. The two fields come from different pages and do not
  follow the same grouping.

## Link labels for a model row

| Label | URL |
|---|---|
| `model card` | The model's own guide page under `/guides/llm/` or `/guides/vlm/` |
| `docs` | `https://docs.z.ai/guides/overview/overview` |

Several variants share one guide page. GLM-4.7, GLM-4.7-FlashX, and
GLM-4.7-Flash all cite `/guides/llm/glm-4.7`. That is correct: it is the page
that describes them.
