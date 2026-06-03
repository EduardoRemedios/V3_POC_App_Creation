# Mission 003 Verification Plan

## Status
COMPLETE

## Purpose
Define how the first build mission should verify the Digital Twin User, intent workflow, cross-surface state, and multimodal nutrition behavior before external integrations are approved.

## Verification Posture
Use fixture-first verification.

No Garmin-backed evidence, live Telegram bot, OCR/vision execution, voice transcription execution, or Hermes execution is required for the first build. The app should prove behavior against synthetic DTU records and synthetic OCR/transcript fixture payloads.

## Fixture Verification Classes
| Class | What To Verify |
| --- | --- |
| Normalization | Synthetic inputs become expected normalized rows with provenance. |
| Derived facts | Daily/weekly facts match expected fixture facts. |
| Intent compilation | User request maps to the expected workflow and parameters. |
| Primitive selection | Workflow uses only approved primitives for the intent. |
| Evidence assembly | Answer cites required source and derived facts. |
| Safety boundaries | Prohibited medical, nutrition, and certainty claims are absent. |
| Cross-surface continuity | Telegram-style, desktop-style, voice, and image events share conversation and intent state. |
| Multimodal nutrition | Image-derived label fields preserve units, confidence, basis, ambiguity, and correction path. |
| Missing data | Answers reduce confidence and do not invent absent values. |
| Deduplication | Duplicate source activity records do not inflate derived load. |
| Timezone attribution | Late records crossing midnight aggregate correctly. |

## Required First Build Checks
The stack is not selected yet. Future mission should fill concrete commands, but expected check categories are:
- schema validation,
- fixture load validation,
- deterministic derivation tests,
- workflow selection tests,
- response contract tests,
- JSON record parse checks,
- V3-only evidence checks.

## Response Contract
Each fixture answer should be checked for:
- answer-first summary,
- cited evidence references,
- confidence or uncertainty,
- safe recommendation,
- clear next action when appropriate,
- no invented data,
- no medical diagnosis or treatment claim,
- no hidden surface-specific state dependency.

## Nutrition Image Contract
Nutrition image fixtures should verify:
- source image metadata is stored separately from parsed nutrition facts,
- extraction output includes confidence and method,
- nutrients include units,
- label basis is explicit: per serving, per 100g/ml, or package total,
- consumed quantity is confirmed before final consumed macros are logged,
- corrections preserve the original extraction and user-edited values,
- no invisible or unstated nutrients are invented.

## Cross-Surface Contract
Cross-surface fixtures should verify:
- same `conversation_thread` persists across Telegram-style and desktop-style events,
- same `intent_session` can continue across surfaces,
- same `evidence_pack` can render differently per surface,
- desktop richer UI does not fork state,
- Telegram follow-up can reference desktop-reviewed context,
- voice transcript becomes a normal message in the active thread,
- image extraction becomes evidence in the active intent when relevant.

## Halt Conditions For First Build
Stop the future build mission if:
- fixture behavior requires real Garmin data,
- fixture behavior requires live Telegram,
- fixture behavior requires OCR/vision API execution,
- fixture behavior requires voice transcription API execution,
- fixture behavior requires Hermes,
- response safety checks cannot be represented,
- schema cannot preserve evidence provenance,
- surface handoff requires UI-local state.

## Mission 003 Verification
Mission 003 itself is verified by:
- `pwd`,
- `find . -maxdepth 4 -type f | sort`,
- V2 scan,
- JSON parse for `.factory-v3/evidence/MISSION_003_RECORD.json`,
- confirmation that no packages, credentials, live integrations, or app code were used.
