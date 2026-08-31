# Mistral pages — probe log 2026-08-30

All probes used `curl -sL -A "Mozilla/5.0"`. Every page returned HTTP 200 and a
server-rendered body.

## Pages

| URL | HTTP | Size | Holds |
|---|---|---|---|
| `https://mistral.ai/pricing/` | 200 | ~477 KB | Free / Pro ($14.99) / Team ($24.99/user) / Enterprise (contact us); included API credits ($10 / $30 / $50 per month); feature matrix; FAQ |
| `https://mistral.ai/pricing/api/` | 200 | ~489 KB | Per-model API rates, model ids, OCR / audio / embedding pricing, Enterprise APIs note |
| `https://mistral.ai/pricing/enterprise-deployments/` | 200 | — | Enterprise / private deployment pitch (no numbers) |

No `.md` twin is served. The locale variants (`/fr/pricing/`, `/it/pricing/`)
mirror the same content.

## Subscription tiers (`/pricing/`)

| Tier | Price | Included API credits | Notes |
|---|---|---|---|
| Free | $0 | $10/mo | Limited messages, searches, coding sessions; 100+ connectors |
| Pro | $14.99/mo | $30/mo | Full Vibe access, all-day coding; student $5.99/mo (normally $14.99) |
| Team | $24.99/user/mo | $50/mo | Up to 30GB storage/user, domain verification, data export |
| Enterprise | Contact us | — | Custom models, agents, workflows; audit logs, SAML SSO, white label |

## Token-based API rates (`/pricing/api/`)

| Model | model_id | Input $/1M | Cached $/1M | Output $/1M | Notes |
|---|---|---|---|---|---|
| Mistral Large 3 | `mistral-large-latest` | 0.50 | — | 1.50 | Open-weight, multimodal |
| Mistral Medium 3.5 | `mistral-medium-latest` | 1.50 | — | 7.50 | Long-horizon, agentic coding |
| Mistral Small 4 | `mistral-small-latest` | 0.15 | — | 0.60 | — |
| GLM 5.2 (resale) | `zai-glm-5-2` | 1.40 | 0.14 | 4.40 | Third-party, long-context agentic |

Batch processing is 50% off; cached input up to 90% off (only GLM 5.2 shows a
cached-input figure on the page).

## Non-token products (do NOT add to api_pricing.yaml)

- OCR 4.1: $4 per 1,000 pages (`mistral-ocr-latest`)
- Voxtral TTS: $0.016 per 1k characters
- Voxtral Small / transcription: per-minute audio rates
- Classifier APIs / fine-tune: per-token training with $4 minimum job fee,
  $2/mo storage
- Embedding (Codestral Embed $0.15, Mistral Embed $0.1): per-token input only

## Rate limits

No RPM / TPM / RPD figure anywhere. The API page says Enterprise APIs get
"increased rate limits" as a selling point, with no number. Zero rows in
`data/rate_limits.yaml` is correct.

## Outbound links observed

- `https://docs.mistral.ai/api/` — API reference (no pricing)
- `https://mistral.ai/pricing/enterprise-deployments/`
- Locale variants `/fr/`, `/it/`
