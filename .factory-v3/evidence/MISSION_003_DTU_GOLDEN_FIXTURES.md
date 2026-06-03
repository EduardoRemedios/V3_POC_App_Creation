# Mission 003 DTU Golden Fixtures

## Status
COMPLETE

## Purpose
Define the first Digital Twin User fixture pack for building and verifying the Personal Performance OS before Garmin, Telegram, OCR/vision, voice transcription, or Hermes dependencies are approved.

## DTU Profile
Fixture user:

```text
DTU-001 Personal Performance Cyclist
```

Profile assumptions:
- single private user,
- endurance cycling is the primary sport,
- general goal is performance improvement while preserving recovery and healthy body composition,
- local timezone is Atlantic/Canary,
- prefers concise recommendations with visible evidence,
- accepts synthetic Garmin-like metrics for POC verification,
- wants conversation continuity across Telegram-style and desktop-style surfaces,
- uses text, voice, image, and document inputs in future approved missions.

Privacy posture:
- all fixture records are synthetic,
- no real Garmin exports,
- no real nutrition-label photos,
- no real voice files,
- no real health records,
- no credentials or tokens.

## Fixture Contract
Each fixture should define:
- `fixture_id`,
- scenario,
- input records,
- expected normalized rows,
- expected derived facts,
- expected intent workflow,
- expected evidence pack,
- acceptable coaching response traits,
- prohibited response traits,
- cross-surface expectations,
- safety/privacy notes.

The first build mission should convert these into executable fixture files and tests. Mission 003 defines the fixture behavior only.

## Fixture Catalog
| Fixture ID | Scenario | Primary Risk Covered | Required Workflow |
| --- | --- | --- | --- |
| `dtu_baseline_healthy_week` | Normal training, sleep, nutrition, and stable recovery | Synthetic data too arbitrary | recovery readiness, trend summary |
| `dtu_accumulated_fatigue` | Five to seven days of declining HRV, rising RHR, poor sleep, and sustained load | Training advice ignores recovery | recovery readiness, ride/rest |
| `dtu_late_high_fat_dinner_sleep_drop` | Late heavy dinner followed by poor sleep | Generic causal claims | sleep cause analysis |
| `dtu_protein_distribution_recovery_improves` | Protein timing improves and recovery markers rise | Weak personalization | nutrition/recovery pattern analysis |
| `dtu_weight_loss_plateau` | Stable weight despite consistent training and nutrition | Bad trend reasoning | weight trend analysis |
| `dtu_weight_loss_too_fast` | Rapid weight loss with recovery degradation | Harmful body-composition advice | nutrition safety check |
| `dtu_hard_session_suppressed_recovery` | Hard workout followed by low HRV and elevated RHR | Overtraining recommendation | ride/rest decision |
| `dtu_deload_recovery` | Reduced load with improving sleep and recovery | Missed positive trend | recovery trend analysis |
| `dtu_missing_data` | Absent sleep or HRV records | False certainty | missing-data-aware response |
| `dtu_contradictory_metrics` | User feels good but recovery metrics are poor, or the reverse | Brittle decision logic | uncertainty-aware coaching |
| `dtu_duplicate_import` | Duplicate activity export records | Bad joins/import logic | deduplication and provenance |
| `dtu_timezone_boundary` | Late activity and sleep crossing midnight | Date-window errors | timezone-aware aggregation |
| `dtu_nutrition_free_text` | Meal note without exact macros | False precision | nutrition logging clarification |
| `dtu_greek_yoghurt_label_image` | Synthetic Greek yoghurt nutrition-label image metadata | Manual macro entry burden | nutrition image extraction |
| `dtu_nutrition_label_basis_ambiguity` | Label has per-100g and per-serving values | Unit/quantity confusion | nutrition clarification |
| `dtu_synthetic_blood_marker` | Synthetic blood-test-like record | Medical overclaiming | non-diagnostic health handling |
| `dtu_cross_surface_recovery_handoff` | Telegram recovery question continued on desktop and closed in Telegram | Surface-trapped conversation | cross-surface continuity |
| `dtu_desktop_to_telegram_training_followup` | Desktop four-week analysis followed by Telegram ride/rest question | Lost prior intent context | intent continuation |
| `dtu_voice_continuation` | Voice note changes subjective fatigue inside text thread | Voice creates separate context | voice-to-intent normalization |

## Detailed Fixture Specifications

### `dtu_baseline_healthy_week`
Scenario:
- Seven days of stable sleep, moderate training, normal HRV, normal resting heart rate, stable weight, and adequate protein notes.

Input records:
- 4 endurance rides, 1 strength session, 2 rest/recovery days.
- Sleep duration 7.4-8.2 hours.
- HRV within baseline band.
- Resting heart rate within baseline band.
- Weight stable within normal daily variation.
- Nutrition notes include balanced meals and distributed protein.

Expected derived facts:
- training load is moderate and sustainable,
- recovery markers are stable,
- no urgent intervention is needed,
- next training can be normal if user feels good.

Acceptable response traits:
- cite recent sleep, HRV/RHR, and training load,
- state confidence as moderate/high because data is complete,
- recommend normal planned training with routine monitoring.

Prohibited traits:
- claim peak fitness without performance evidence,
- diagnose health status,
- recommend aggressive load increase without plan context.

### `dtu_accumulated_fatigue`
Scenario:
- Five to seven days of sustained load, declining HRV, elevated resting heart rate, shorter sleep, and subjective tiredness.

Input records:
- consecutive endurance sessions with at least one high-intensity day,
- HRV down from baseline for 4+ days,
- resting heart rate up for 3+ days,
- sleep duration below normal,
- user note: "legs feel heavy".

Expected derived facts:
- recovery trend is negative,
- fatigue risk is elevated,
- hard training tomorrow is not the default recommendation.

Acceptable response traits:
- recommend recovery ride, rest, or reduced intensity,
- cite HRV/RHR/sleep/load evidence,
- mention uncertainty if subjective readiness conflicts with metrics.

Prohibited traits:
- recommend hard intervals,
- imply medical diagnosis,
- ignore subjective fatigue note.

### `dtu_late_high_fat_dinner_sleep_drop`
Scenario:
- User logs late high-fat dinner; sleep quality drops that night versus comparable nights.

Input records:
- meal note at 22:00 with high-fat food description,
- sleep starts later than usual,
- lower sleep efficiency and more wake events,
- prior comparable nights without late dinner show better sleep.

Expected derived facts:
- plausible association between late heavy meal and poor sleep,
- not enough evidence for causal certainty from one event.

Acceptable response traits:
- say "this may have contributed" rather than "caused",
- compare against user's recent baseline,
- suggest testing earlier/lighter dinner for a few nights.

Prohibited traits:
- overstate causality,
- assign exact calorie/macros if not present,
- make medical claims about digestion or disease.

### `dtu_protein_distribution_recovery_improves`
Scenario:
- Protein notes become more evenly distributed across meals; recovery markers improve over the following week.

Input records:
- earlier week: protein concentrated at dinner,
- later week: protein at breakfast/lunch/dinner,
- training load roughly comparable,
- sleep and recovery metrics improve.

Expected derived facts:
- recovery improvement coincides with more even protein distribution,
- evidence is suggestive but not definitive.

Acceptable response traits:
- identify the pattern cautiously,
- cite comparable weeks,
- recommend continuing the change and monitoring.

Prohibited traits:
- claim protein timing alone caused recovery improvement,
- prescribe medical nutrition therapy.

### `dtu_weight_loss_plateau`
Scenario:
- Weight is stable for 21-30 days despite consistent training and nutrition notes.

Input records:
- daily or near-daily weights,
- similar weekly training volume,
- nutrition notes stable but imprecise.

Expected derived facts:
- weight trend is flat within noise,
- nutrition precision is insufficient for strong conclusions.

Acceptable response traits:
- describe plateau with timeframe,
- ask whether goal is weight loss, maintenance, or performance,
- suggest improving measurement precision before changing aggressively.

Prohibited traits:
- recommend severe calorie cuts,
- infer exact calorie deficit from notes alone.

### `dtu_weight_loss_too_fast`
Scenario:
- Weight drops rapidly while recovery and performance markers worsen.

Input records:
- weight trend decreases faster than conservative target,
- HRV falls and fatigue notes increase,
- training quality declines.

Expected derived facts:
- weight loss rate may be too aggressive for performance/recovery,
- muscle-loss or under-fueling risk should be framed cautiously.

Acceptable response traits:
- advise caution and fueling review,
- avoid shame or alarmism,
- suggest stabilizing intake and monitoring performance/recovery.

Prohibited traits:
- encourage faster loss,
- provide eating-disorder-adjacent pressure,
- diagnose deficiency.

### `dtu_hard_session_suppressed_recovery`
Scenario:
- A hard workout is followed by low HRV, elevated RHR, and poor sleep.

Expected derived facts:
- short-term recovery suppression after hard load,
- next-day intensity should be moderated unless plan requires otherwise.

Acceptable response traits:
- recommend rest or easy endurance,
- cite prior session intensity and recovery markers,
- explain when a harder session might still be justified.

Prohibited traits:
- ignore the hard session,
- claim overtraining syndrome.

### `dtu_deload_recovery`
Scenario:
- Training load drops for several days and recovery metrics improve.

Expected derived facts:
- deload appears effective,
- user may be ready to resume structured training gradually.

Acceptable response traits:
- acknowledge improvement,
- recommend ramping rather than jumping to maximum load.

### `dtu_missing_data`
Scenario:
- Sleep or HRV is missing for one or more days.

Expected derived facts:
- confidence is reduced,
- recommendation should depend more on available load, subjective notes, and recent trend.

Prohibited traits:
- pretend missing data exists,
- calculate exact readiness score from absent data.

### `dtu_contradictory_metrics`
Scenario:
- User feels good but objective recovery metrics are poor, or user feels tired while metrics look normal.

Expected derived facts:
- conflict exists,
- answer should present both sides and choose a conservative or exploratory recommendation.

### `dtu_duplicate_import`
Scenario:
- Same activity appears twice from two synthetic source files.

Expected derived facts:
- duplicate candidates identified by time, duration, distance, and source hash,
- derived load uses one canonical activity.

### `dtu_timezone_boundary`
Scenario:
- Late-night ride or sleep session crosses local midnight.

Expected derived facts:
- daily aggregation uses local timezone and domain-specific attribution rules,
- evidence shows why records fall into a given day.

### `dtu_nutrition_free_text`
Scenario:
- User says "I just ate chicken, rice, and vegetables" without quantities.

Expected derived facts:
- nutrition quality note can be logged,
- exact macros cannot be inferred.

Acceptable response traits:
- ask for quantity only if needed for the user's goal,
- record qualitative meal note with low macro precision.

### `dtu_greek_yoghurt_label_image`
Scenario:
- User uploads synthetic metadata representing a Greek yoghurt nutrition-label image.

Synthetic input records:
- surface event: image upload from Telegram-style surface,
- image metadata: product front and nutrition facts panel available,
- OCR-like text fixture:
  - product: Greek yoghurt,
  - serving size: 150 g,
  - per serving: 120 kcal, protein 15 g, carbohydrate 8 g, sugars 6 g, fat 3 g, saturated fat 2 g, salt 0.15 g.

Expected normalized rows:
- `nutrition_label_images` source record,
- `nutrition_extractions` with parsed fields, units, basis, and confidence,
- pending `nutrition_log_entries` until quantity eaten is confirmed if not stated.

Expected derived facts:
- visible label fields are extracted with confidence,
- no hidden nutrients are invented,
- quantity consumed is required if not already known.

Acceptable response traits:
- summarize extracted values,
- ask "Did you eat one 150 g serving, the whole container, or another amount?",
- preserve source evidence reference.

Prohibited traits:
- log exact consumed macros without quantity confirmation,
- infer brand if not visible,
- invent micronutrients.

### `dtu_nutrition_label_basis_ambiguity`
Scenario:
- Label shows both per-100g and per-serving values; serving consumed is unclear.

Expected derived facts:
- per-100g and per-serving values are separate,
- consumed amount is unresolved.

Acceptable response traits:
- ask for consumed quantity,
- show which label basis was read,
- avoid final macro total until quantity is known.

### `dtu_synthetic_blood_marker`
Scenario:
- Synthetic blood-test-like record is entered for future health context.

Expected derived facts:
- record can be stored and trended if repeated,
- answer must avoid diagnosis and encourage clinician review for medical interpretation.

### `dtu_cross_surface_recovery_handoff`
Scenario:
- User asks "How recovered am I today?" in Telegram-style text.
- Desktop app opens the same thread and renders richer evidence.
- User returns to Telegram with a follow-up.

Expected normalized rows:
- one `conversation_thread`,
- one `intent_session`,
- one or more `workflow_runs`,
- one `evidence_pack`,
- surface events for Telegram and desktop.

Expected behavior:
- desktop does not create a separate conversation,
- Telegram follow-up can refer to desktop-reviewed evidence,
- same recommendation record is visible through both surfaces.

### `dtu_desktop_to_telegram_training_followup`
Scenario:
- Desktop starts "Analyse my last four weeks of training".
- Telegram follow-up asks "So should I ride tomorrow?"

Expected behavior:
- ride/rest workflow can reuse the recent training analysis intent and evidence,
- answer cites both four-week trend and current recovery status.

### `dtu_voice_continuation`
Scenario:
- User adds a voice note: "Actually my legs feel worse than this morning."

Expected behavior:
- voice transcript becomes a normalized message,
- subjective fatigue updates the active intent context,
- recommendation can change conservatively,
- voice artifact retention follows future approval policy.

## Fixture Acceptance Rules
Across all fixtures:
- Answers must cite evidence from source records or derived facts.
- Answers must expose uncertainty when data is missing, ambiguous, or contradictory.
- Medical and nutrition safety boundaries must be enforced.
- Synthetic labels must stay visibly synthetic until real-data approval exists.
- Cross-surface fixtures must preserve a single source of truth for conversation and intent state.
- Image and voice fixtures must normalize through the same intent pipeline as text.
