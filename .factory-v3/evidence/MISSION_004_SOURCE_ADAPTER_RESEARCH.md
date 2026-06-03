# Mission 004 Source Adapter Research

## Status
COMPLETE

## Mission
`.factory-v3/missions/MISSION_004_SOURCE_ADAPTERS_AND_MEDICAL_PDFS.md`

## Date
2026-06-03

## Core Decision
The Personal Performance OS must use a source-agnostic internal model with adapters.

```text
Garmin is one adapter, not the architecture.
```

The internal system should normalize all source data into common facts, derived metrics, evidence packs, memories, and recommendations. Source-specific payloads, files, identifiers, and permissions stay in the adapter/provenance layer.

## Adapter Principles
- Keep raw source payloads and normalized facts separate.
- Preserve source identity, source record IDs, file hashes, user consent, observed time, ingested time, confidence, and extraction method.
- Make derived analytics depend on normalized facts, not Garmin-specific or Strava-specific fields.
- Make recommendation evidence cite both normalized facts and source provenance.
- Allow multiple sources to contribute the same domain, such as activities from Garmin, Strava, Apple Health, Google Health/Fitbit, Polar, or manual imports.
- Support source priority and conflict resolution.
- Treat medical PDFs and nutrition images as evidence-bearing documents, not chat attachments.

## Medical PDF Uploads
Design target:

```text
The user should be able to upload doctor-provided PDF files containing blood work, lab analysis, and periodic medical reports.
```

Expected future behavior:
- store original PDF metadata, hash, page count, retention status, and upload surface,
- extract text and tables only after a later approved PDF extraction mission,
- preserve page/table references for every extracted value,
- normalize lab markers with collection date, marker name, value, unit, reference range, lab/provider, and confidence,
- keep doctor-written comments separate from generated summaries,
- allow user correction,
- trend repeated markers over time,
- provide non-diagnostic context only.

Candidate state model additions:
- `medical_documents`: file metadata, hash, source, upload surface, retention status.
- `medical_document_pages`: page-level extraction status and text/table references.
- `lab_results`: normalized marker, value, unit, reference range, collection date, provider, confidence.
- `medical_report_sections`: clinician comments, report summaries, and source page references.
- `medical_extraction_corrections`: user-corrected values and audit trail.

Golden fixture additions:
- `dtu_medical_pdf_blood_work_table`: synthetic PDF-like table extraction with marker units and reference ranges.
- `dtu_medical_pdf_repeated_markers`: two synthetic reports months apart requiring trend comparison.
- `dtu_medical_pdf_ambiguous_units`: unit ambiguity requiring clarification or low-confidence storage.
- `dtu_medical_pdf_clinician_comment`: doctor-written comment preserved without over-interpreting.

Safety rules:
- Do not diagnose.
- Do not recommend treatment changes.
- Do not override clinician interpretation.
- Flag uncertainty and suggest discussing clinically important questions with the doctor.

## Source Adapter Matrix
| Source | Main Value | Access Shape | Key Risks | POC Posture |
| --- | --- | --- | --- | --- |
| Garmin | Activities, sleep, HRV, recovery, weight, device-specific metrics | Manual export first; official API later; unofficial clients research only | Program approval, credentials, unofficial ToS/maintenance | Keep as one adapter; not core |
| Apple Health / HealthKit | Apple Watch/iPhone health, workouts, sleep, vitals, body metrics | iOS HealthKit permissioned app or manual export bridge | Requires Apple-platform implementation and privacy controls | Design adapter; implement later only if approved |
| Google Health / Fitbit | Fitbit/Google Health app ecosystem, Fitbit Air, AI health app data surface | Consumer app ecosystem; API access must be verified later | Newly changed product surface; public API availability uncertain | Treat as a source ecosystem, not guaranteed API |
| Health Connect | Android on-device health-data hub | Android API with user permission and metadata-rich records | Requires Android app/bridge; history and permissions must be verified | Preferred Android integration substrate |
| Google Fit | Legacy/transition Google fitness API/docs | REST API docs exist | Migration/deprecation uncertainty | Legacy/transition research only |
| Polar / AccessLink | Polar Flow exercise, activity, physical data | Official AccessLink API with transaction model | App registration, authorization, transaction/webhook handling | Adapter candidate; no live use yet |
| Strava | Activities, streams, segments, social training context | OAuth2 registered app and API | Scope limits, rate limits, activity-only bias | Activity adapter candidate |
| Medical PDFs | Blood work, doctor reports, lab references | User-uploaded documents, later PDF extraction | Privacy, extraction errors, medical overclaiming | Design now, extract later |
| Nutrition label images | Food labels and packaging | User-uploaded images, later OCR/vision | Hallucinated values, unit ambiguity, privacy | Design now, extract later |
| Manual notes/imports | User observations and simple data entry | Local form/chat/import | Low precision, subjective bias | Always supported |

## Apple Health / HealthKit
Sources:
- Apple HealthKit documentation: https://developer.apple.com/documentation/healthkit
- Apple health-data privacy support: https://support.apple.com/en-mide/guide/security/sec88be9900f/web

Findings:
- HealthKit is a central repository for health and fitness data on iPhone and Apple Watch.
- Apps need user permission to read/write health data.
- Apple emphasizes privacy and user control.

Recommendation:
- Add an Apple Health adapter design.
- Do not implement until a later mobile/platform mission approves HealthKit permissions and data handling.

## Google Health / Fitbit / Health Connect
Sources:
- Google Health app and Fitbit Air announcement: https://blog.google/products-and-platforms/products/google-health/google-health-fitbit/
- Google Health app announcement: https://blog.google/products-and-platforms/products/google-health/google-health-app/
- Health Connect data format: https://developer.android.com/health-and-fitness/guides/health-connect/data-format
- Android Help: Learn about Health Connect: https://support.google.com/android/answer/13770320
- Google Fit REST API: https://developers.google.com/fit/rest/

Findings:
- Google announced Fitbit Air and the Google Health app on May 7, 2026.
- Google says the Fitbit app is becoming the Google Health app, with existing Fitbit users upgraded and Google Fit users planned for migration later in 2026.
- Health Connect is an Android on-device health-data store and sharing layer with user permission.
- Health Connect records include useful metadata: IDs, last modified time, data origin, device, client IDs, record version, and recording method.
- Google Fit REST API docs still exist, but new architecture should not depend on Google Fit as the primary path.

Recommendation:
- Treat Google Health/Fitbit as a source ecosystem.
- Treat Health Connect as the likely Android integration substrate.
- Keep Google Fit as legacy/transition research only.
- Verify public API/data-export access in a later source-specific mission.

## Polar / AccessLink
Sources:
- Polar AccessLink API: https://www.polar.com/accesslink-api/
- Polar AccessLink announcement: https://www.polar.com/blog/introducing-polar-open-accesslink-api/

Findings:
- Polar AccessLink can fetch user training, activity, and physical data from Polar Flow.
- AccessLink uses transactions that must be retrieved and committed.
- Webhook/pull notification behavior may be relevant later.

Recommendation:
- Treat Polar as an official adapter candidate.
- Do not register apps or call APIs yet.

## Strava
Sources:
- Strava authentication documentation: https://developers.strava.com/docs/authentication
- Strava API reference: https://strava.github.io/api/

Findings:
- Strava uses OAuth2 and registered applications.
- API resources include athlete, activities, streams, segments, uploads, and related objects.
- Strava has API rate limits and is strongest for activity/training data.

Recommendation:
- Treat Strava as an activity adapter candidate.
- Do not register apps or use tokens yet.

## Adapter State Model
Candidate tables:
- `data_sources`: source type, status, display name, permission state.
- `source_credentials`: future encrypted credential references only; not used in current POC.
- `source_files`: uploaded/exported files with hash, path/reference, retention status.
- `source_records`: raw source records or replay references.
- `source_sync_runs`: adapter sync/import runs and errors.
- `normalized_facts`: source-agnostic fact registry.
- `fact_provenance`: mapping from normalized facts to source records/files/pages.
- `source_conflicts`: duplicate/conflicting facts and resolution status.
- `adapter_capabilities`: supported domains, data freshness, permissions, and limitations.

## Preferred Next Build Posture
The next build should implement source-agnostic synthetic fixtures and schema first.

Do not implement any live adapter. Use fixture sources such as:
- `synthetic_garmin_like`,
- `synthetic_apple_health_like`,
- `synthetic_google_health_like`,
- `synthetic_health_connect_like`,
- `synthetic_strava_like`,
- `synthetic_polar_like`,
- `synthetic_medical_pdf_like`,
- `manual_note`.

This proves adapter boundaries before credentials or real data enter the system.
