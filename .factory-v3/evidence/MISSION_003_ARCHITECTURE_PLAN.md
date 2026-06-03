# Mission 003 Architecture Plan

## Status
COMPLETE

## Architecture Principle
The Personal Performance OS should compile human intent into bounded executable workflows over small composable primitives.

Surfaces such as Telegram and the desktop conversational app are adapters. They do not own conversation state, memory, evidence, recommendations, or business logic.

## Layers
| Layer | Responsibility |
| --- | --- |
| Surface adapters | Receive/send Telegram-style, desktop, mobile, voice, image, and document interactions. |
| Normalization | Convert text, voice transcripts, OCR/vision outputs, files, and manual records into normalized input records. |
| Source facts | Store source-specific and source-agnostic health, training, nutrition, and conversation facts. |
| Derivation | Compute daily/weekly metrics, trends, missing-data flags, deduplication, and comparable periods. |
| Intent compiler | Convert user intent into an allowed workflow with parameters, limits, and required evidence. |
| Workflow executor | Run deterministic primitives and store intermediate workflow state. |
| Evidence assembler | Build cited evidence packs for answers and recommendations. |
| Safety checker | Enforce medical, nutrition, privacy, and confidence constraints. |
| Renderer | Produce surface-specific response forms from shared workflow/evidence records. |
| Memory promoter | Promote durable preferences, goals, observations, and follow-up outcomes separate from raw transcripts. |

## State Model
Initial source-agnostic tables or collections:

### Identity And Preferences
- `user_profile`: synthetic DTU profile and later private user settings.
- `user_preferences`: goals, constraints, response style, units, timezone, training preferences.
- `durable_memories`: promoted stable facts, preferences, patterns, and coaching observations.

### Source And Ingestion
- `source_files`: imported files or synthetic source bundles.
- `source_records`: raw or semi-raw source rows with provenance.
- `ingestion_runs`: import/generation runs, status, errors, and source hashes.
- `dedupe_candidates`: possible duplicate source records and resolution status.

### Performance And Health Facts
- `activities`: normalized workouts and activity summaries.
- `sleep_sessions`: sleep timing, duration, efficiency, and quality fields.
- `hrv_readings`: HRV values, baseline references, and source confidence.
- `resting_heart_rate_readings`: RHR values and source confidence.
- `recovery_metrics`: Body Battery-like, stress, readiness-like, and recovery scores where available.
- `weight_entries`: body weight and body-composition values if approved.
- `nutrition_logs`: text/manual food notes and confirmed nutrition logs.
- `nutrition_label_images`: image metadata, surface, hash, retention status, and source reference.
- `nutrition_extractions`: OCR/vision text, parsed nutrients, confidence, basis, and extraction errors.
- `nutrition_corrections`: user corrections and confirmed values.
- `health_records`: source-agnostic health observations.
- `blood_tests`: synthetic or later approved blood-test records with non-diagnostic handling.
- `manual_notes`: subjective notes, injuries, soreness, mood, fatigue, and context.

### Derived Analytics
- `derived_daily_metrics`: daily load, sleep, recovery, weight, nutrition, and missing-data facts.
- `derived_weekly_metrics`: weekly volume, intensity, consistency, recovery response, and trend facts.
- `similar_periods`: comparable historical windows used for analysis.
- `anomaly_flags`: unusual values, trend breaks, and missing-data markers.

### Conversation And Intent
- `conversation_threads`: user-facing thread independent of surface.
- `conversation_messages`: normalized messages, transcript text, attachments, and surface metadata.
- `surface_events`: Telegram/web/mobile delivery, upload, click, voice, image, and document events.
- `intent_sessions`: active or completed compiled intents with parameters, status, and parent thread.
- `workflow_runs`: selected primitives, execution limits, intermediate state references, and results.
- `evidence_packs`: source and derived facts used in an answer.
- `ui_render_specs`: optional runtime UI descriptors for desktop rich views.
- `recommendations`: recommendation claim, evidence, confidence, risk, action, and status.
- `follow_ups`: pending checks, reminders, review points, and outcomes.

## Primitive Catalog
Initial primitive candidates:

### Retrieval
- `load_user_profile`
- `get_metric_window`
- `get_recent_activities`
- `get_recent_sleep`
- `get_recent_recovery_metrics`
- `get_recent_nutrition_logs`
- `get_recent_weight_entries`
- `retrieve_relevant_memories`
- `retrieve_prior_recommendations`
- `get_conversation_context`

### Derivation
- `compute_training_load`
- `compute_sleep_summary`
- `compute_recovery_summary`
- `compute_weight_trend`
- `compute_nutrition_quality_signals`
- `detect_missing_data`
- `detect_duplicate_activity_candidates`
- `find_similar_periods`
- `compute_timezone_attribution`

### Multimodal Nutrition
- `extract_nutrition_from_image_candidate`
- `normalize_nutrition_label_values`
- `ask_nutrition_quantity_clarification`
- `confirm_nutrition_log_entry`
- `record_nutrition_correction`

### Workflow And Evidence
- `compile_intent_candidate`
- `select_allowed_workflow`
- `assemble_evidence_pack`
- `check_safety_boundaries`
- `render_surface_response`
- `write_recommendation_record`
- `schedule_follow_up_candidate`

## Initial Workflows

### Recovery Today
Intent examples:
- "How recovered am I today?"
- "Am I ready to train?"

Workflow:
- load profile and timezone,
- retrieve last 7-14 days of sleep, HRV, RHR, training load, recovery metrics, and subjective notes,
- compute recovery summary,
- detect missing or contradictory data,
- assemble evidence pack,
- run safety checks,
- render concise answer and recommendation.

Required evidence:
- current sleep,
- HRV vs baseline,
- RHR vs baseline,
- recent training load,
- subjective note if available,
- missing-data statement if relevant.

### Sleep Cause Analysis
Intent examples:
- "Why was my sleep poor last night?"

Workflow:
- retrieve last night's sleep,
- retrieve previous comparable nights,
- retrieve recent nutrition, caffeine/alcohol, stress, training load, and notes,
- identify plausible contributors,
- avoid causal overclaiming,
- propose an experiment.

Required evidence:
- sleep difference from baseline,
- relevant meal/training/stress timing,
- comparable windows.

### Four-Week Training Analysis
Intent examples:
- "Analyse my last four weeks of training."

Workflow:
- retrieve four weeks of activities and recovery data,
- compute weekly volume, intensity distribution, consistency, rest days, and recovery response,
- identify trend breaks and missing data,
- assemble executive summary and evidence.

Required evidence:
- weekly load table,
- intensity distribution,
- recovery response,
- notable sessions or gaps.

### Nutrition Label Capture
Intent examples:
- "I uploaded a photo of this yoghurt label. Log the nutrition."

Workflow:
- receive image surface event,
- store source image metadata,
- run extraction only after later approval; until then use synthetic OCR fixture,
- parse product and nutrient values,
- determine label basis,
- ask quantity clarification if needed,
- create pending or confirmed nutrition log,
- preserve correction path.

Required evidence:
- source image reference,
- OCR/vision output reference,
- parsed fields with units,
- confidence and ambiguity state.

### Ride Or Rest Tomorrow
Intent examples:
- "Should I ride tomorrow or take a recovery day?"

Workflow:
- retrieve active training context and recent analysis if available,
- retrieve current recovery and subjective notes,
- compute fatigue and readiness,
- compare options: rest, recovery ride, normal ride, hard ride,
- apply safety and uncertainty checks,
- write recommendation and follow-up.

Required evidence:
- recent load,
- recovery markers,
- sleep,
- subjective readiness,
- goal or plan context if available.

## Surface Rendering
Telegram-style rendering:
- compact answer,
- short evidence bullets,
- one next action,
- short clarification question when needed,
- no large tables unless summarized.

Desktop conversational rendering:
- full-screen conversation,
- evidence panels,
- trend charts or tables,
- editable assumptions,
- workflow status,
- correction controls for nutrition extraction,
- follow-up controls.

Shared rule:
- rendering is derived from `conversation_threads`, `intent_sessions`, `workflow_runs`, `evidence_packs`, and `ui_render_specs`.
- surface adapters do not own business state.

## Execution Limits For Future Build
Future executable workflows should define:
- allowed primitives,
- max records scanned,
- max workflow steps,
- timeout,
- evidence requirements,
- safety checks,
- persistence rules,
- retry and failure behavior.

No unbounded generated workflow execution is approved by Mission 003.
