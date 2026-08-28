# MiniMax — probe results, 2026-08-28

## Pages

| URL | Result |
|---|---|
| `https://platform.minimax.io/subscribe/token-plan` | 200, ~70 KB Next.js shell; no prices in HTML; `WebFetch` sees the title only |
| `https://platform.minimax.io/subscribe/coding-plan` | Client-side redirect to `/subscribe/token-plan` |
| `https://platform.minimax.io/_next/data/Abwp9rFspSH47uXEKl3cs/en/subscribe/token-plan.json` | 200, ~62 KB; page i18n plus 22 FAQ answers; no prices; build id changes on deploy |
| `https://platform.minimax.io/docs/guides/pricing-token-plan` | 200, ~267 KB, server-rendered |
| `https://platform.minimax.io/docs/guides/pricing-token-plan.md` | 200, ~2.7 KB Markdown twin — the price source |
| `https://platform.minimax.io/docs/guides/pricing-token-plan-team.md` | 200, ~1.5 KB; team seat rules, no seat price |
| `https://platform.minimax.io/docs/guides/rate-limits.md` | 200; per-model RPM and TPM tables |
| `https://platform.minimax.io/docs/llms.txt` | 200, ~180 lines; full docs index with `.md` links |
| `GET https://api.minimax.io/setting/get_app_settings?fe_setting_key=code_plan_landing` | 200 anonymous, ~72 KB; `data.en` holds `comparison`, `serviceNotice`, `apiPricing`, `subscribeTags`, `comboTypeTipsMap`, `content` |
| `https://platform.minimax.io/guides/pricing-token-plan` | 404 — the docs prefix is `/docs/guides/`, not `/guides/` |
| `GET https://api.minimax.io/public/api/openplatform/charge/combo/products` | 200 anonymous, but resource-pack scope only; `"GetResourcePkgCard failed"` for every parameter set tried (`biz_line`, `combo_type`, `cycle_type`, `resource_package_type`) |
| `https://www.minimax.io/v1/token_plan/remains` | Usage endpoint from the FAQ; needs `Authorization: Bearer <API Key>` |

## Verified plan values (pricing-token-plan.md, 2026-08-28)

| | Plus | Max | Ultra |
|---|---|---|---|
| Price | $22 /month | $55 /month | $132 /month |
| Best for | Personal projects and prototyping | Daily coding with agents and multimodal work | Heavy Agent workflows and extended sessions |
| Quota windows | 5-hour rolling and weekly windows | same | same |
| Agent usage | 3-4 agents | 4-5 agents | 6-7 agents |

Model coverage: full MiniMax lineup (M3 / M2.7 / image / speech). Excluded:
MiniMax H3, voice design, rapid voice cloning. Credits usage is unrestricted.
Unused included quota does not carry over to the next billing cycle (FAQ).

Credits packages: 1,000 credits = $1; packs $5 / $25 / $100; valid 365 days.

## Verified API rate limits (rate-limits.md, 2026-08-28)

| Model | RPM | TPM |
|---|---|---|
| MiniMax-M3 | 200 | 10,000,000 |
| MiniMax-M2.7 / M2.7-highspeed | 500 | 20,000,000 |
| MiniMax-M2.5 / M2.5-highspeed | 500 | 20,000,000 |
| MiniMax-M2.1 / M2.1-highspeed | 500 | 20,000,000 |
| MiniMax-M2 | 500 | 20,000,000 |

Video: Hailuo series 20 RPM; MiniMax-H3 300 RPM, 30 max inflight tasks.
Speech T2A 60 RPM; voice cloning 60 RPM; voice design 20 RPM. Image
(image-01) 10 RPM. Music 120 RPM, 20 CONN. Higher limits: api@minimax.io.

## Frontend combo_type enum (from the JS bundle)

CodePlan=7, CodePlanStarter=24, CodePlanPlus=25, CodePlanMax=26,
TrialCodePlan=28, CodePlanStarterHighSpeed=101001, CodePlanPlusHighSpeed=101002,
CodePlanMaxHighSpeed=101003, CodePlanUltraHighSpeed=101004. Only Plus, Max, and
Ultra are publicly listed.

## Verified comparison table (landing config, 2026-08-28)

`data.en.comparison`, rendered as "Which plan fits you?" on the subscribe page.

| | Plus | Max | Ultra |
|---|---|---|---|
| Price (see trap 11) | $20 / mo | $50 / mo | $120 / mo |
| Daily coding calls (monthly, ~50K tokens per M3 call) | ~34,000 | ~102,000 | ~250,000 |
| OpenClaw Agent concurrency | 3-4 | 4-5 | 6-7 |
| Large codebase continuous editing | Medium-large projects | Large projects | Extra-large / multi-project |
| Multimodal understanding, image gen, voice gen | ✓ | ✓ | ✓ |
| Video generation | × | 3 / day | 5 / day |
| M2.7 calls (shares quota with M3) | 4,500 / 5 hours | 15,000 / 5 hours | 29,077 / 5 hours |
| M2.7-highspeed calls (shares quota with M3) | 2,250 / 5 hours | 7,500 / 5 hours | 14,538 / 5 hours |

Tier tips (`comboTypeTipsMap`): 24 entry-level, 25 professional, 26
high-volume. `subscribeTags` marks Max as "POPULAR".

Service notice: all Music-series models leave the Token Plan on 2026-08-20;
open weights stay on Hugging Face (MiniMaxAI/MiniMax-Music3).

Pay-as-you-go teaser (`apiPricing.m3`, per 1M tokens, "Permanent 50% off"):
context ≤ 512K — input $0.3, output $1.2, cache read $0.06 (original $0.6 /
$2.4 / $0.12); context 512K-1M — doubled. Full rates:
`https://platform.minimax.io/docs/guides/pricing-paygo`.
