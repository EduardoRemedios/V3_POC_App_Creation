# Mission 012 Real-Data Approval Design

## Scope
This design evidence is shaped by HDI-012-001 `option_a`: future manual Garmin export/import. It is design-only. It does not approve real data, real exports, credentials, Garmin account access, API calls, scraping, OCR/vision, or implementation in Mission 012.

## Future Approval Gate
A future mission may only handle a real Garmin export after a separate sponsor approval records:
- source type: manual Garmin export/import;
- file surface: local file selected by the sponsor, with no credentials;
- data categories expected in the file;
- retention setting before import starts;
- rollback expectation before commit starts;
- explicit confirmation that the file is real personal data.

## Consent And Source Labeling
The future workflow should show a pre-import approval screen before reading file contents. It should label the source as `real_garmin_manual_export` and distinguish it from Mission 012 synthetic rows. The consent record should include the approved file name or local reference, approval timestamp, source family, data categories, and whether the import is preview-only or commit-capable.

## Preview Before Commit
The first real-data bridge should preserve the synthetic workflow shape:
- parse into preview rows;
- show raw/normalized side-by-side diffs;
- require operator review states before commit;
- block commit while any row remains `needs_clarification`;
- preserve rejected rows in audit history without treating them as committed facts.

## Retention
Default retention should be short and local. A future real-data mission should decide whether raw file content is stored at all. If raw content is retained, it should be minimized, source-labeled, and covered by a retention period visible in the approval record. Normalized facts should keep provenance references back to source labels without requiring long-term raw-file storage.

## Rollback
Rollback should be provenance-preserving, not destructive. A future rollback should mark the committed import as reverted, record who/when/why, and leave an audit event trail. If normalized facts are materialized, rollback should mark those facts inactive or reverted rather than deleting the audit record.

## Future Mission 013 Research Priority
Mission 013+ should research the synthetic shape of manual Garmin exports first: file formats, fields, timestamps, duplicate signatures, and source labeling. It should not connect to Garmin, request credentials, call APIs, scrape websites, or use real exports without separate approval.
