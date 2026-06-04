# Mission 013 Garmin Export Shape Research

## Scope And Source Rules
This research used public Garmin support/developer documentation only. It did not use a Garmin login, account, credentials, API calls, scraping, downloaded export files, or public sample export files. Fixture design below is synthetic shape modeling, not real-data reproduction.

## Public Documentation Consulted
- Garmin Support, "How Do I Export Data Out of Garmin Connect?"  
  URL: https://support.garmin.com/en-MY/?faq=W1TvTPW8JZ6LfJSfK512Q8  
  Public shape notes: Garmin Connect activity exports offer original-device export files, usually `.fit`, plus TCX, GPX, Google Earth, and split CSV options. The same support result describes exporting all uploaded timed activities as CSV, wellness data including steps, sleep, stress, HRV, and more, and longer-range weight/blood-pressure CSV reports.
- Garmin Support, "Export Training Data from Garmin Connect to View it in Microsoft Excel"  
  URL: https://support.garmin.com/en-GB/?faq=euV2pTGMOJ8RtTytcXLJ8A  
  Public shape notes: Garmin positions TCX and CSV as user-visible export formats for training data analysis in Excel.
- Garmin Support, "How to Manually Upload Activities to Garmin Connect"  
  URL: https://support.garmin.com/en-MY/?faq=Ht3ZP52Kju075uKvqTqu99  
  Public shape notes: manual activity interchange accepts `.fit`, `.gpx`, and `.tcx`, with size limits; this confirms those formats as realistic file-family peers for manual bridge shape, though Mission 013 only implements synthetic fixture parsing.
- Garmin Developers, FIT SDK Activity File documentation  
  URL: https://developer.garmin.com/fit/file-types/activity/  
  Public shape notes: FIT Activity files store date/time, sport type, laps/splits, GPS track, sensor data, and events. Required messages include File Id, Activity, Session, Lap, and Record. Summary messages require start time, total elapsed time, total timer time, and timestamp. Record messages hold moment-by-moment values such as GPS, speed, distance, heart rate, and power. HRV messages can exist and are synchronized around timestamps rather than carrying ordinary timestamps themselves.
- Garmin Developers, FIT SDK Decoding Activity Files cookbook  
  URL: https://developer.garmin.com/fit/cookbook/decoding-activity-files/  
  Public shape notes: FIT timestamps are generally seconds since the Garmin epoch `1989-12-31T00:00:00Z`; local timestamp can be used to calculate timezone offset. Pool length examples call out meter values with display units. This informs synthetic timestamp and unit-boundary cases without decoding real FIT files.
- Garmin Developers, Garmin Connect Health API overview  
  URL: https://developer.garmin.com/gc-developer-program/health-api/  
  Public shape notes: Garmin publicly lists health domains including steps, intensity minutes, sleep, calories, heart rate, stress, pulse ox, Body Battery, body composition, respiration, and blood pressure. It describes JSON summaries after consent for enterprise API use. Mission 013 does not use that API, but the public domain list guides optional synthetic fixture families.
- Garmin Developers, Health SDK overview  
  URL: https://developer.garmin.com/health-sdk/overview/  
  Public shape notes: public domain names include activity data, heart rate, stress scores, respiration, advanced sleep data, Index Scale biometrics, steps, calories, distance, Body Battery, and pulse ox. This reinforces Garmin-shaped wellness/body-composition category names.

## Export Families Observed Publicly
- Timed activities:
  - Manual export file types: original device format, usually FIT; TCX; GPX; Google Earth; split CSV.
  - Common shape: activity/session-level rows can include start time, elapsed/timer duration, sport/subsport, distance, elevation, speed/pace, heart rate, power, laps/splits, GPS records, and device/source identity.
  - Synthetic bridge implication: implement CSV summaries rather than binary FIT decoding, with normalized fields for `activity_type`, `start_time`, `duration_seconds`, `distance_meters`, `calories_kcal`, `average_hr_bpm`, and `training_load`.
- Sleep and wellness:
  - Public Garmin support/developer docs list sleep, stress, HRV, respiration, Body Battery, pulse ox, steps, calories, and heart rate as Garmin health/wellness domains.
  - Common shape: daily or interval summaries with local date attribution, start/end timestamps, measured values, and sometimes epoch/interval detail.
  - Synthetic bridge implication: implement sleep CSV/JSON rows with `sleep_start`, `sleep_end`, `sleep_hours`, `sleep_score`, `hrv_rmssd_ms`, `resting_hr_bpm`, and timezone fields; optional wellness/HRV/stress rows are valid fixture candidates if HDI-013-001 selects them.
- Body composition:
  - Garmin support documents longer-range CSV reports for weight and blood pressure; Garmin developer docs list body composition and Index Scale biometrics.
  - Common shape: dated measurements with weight and composition fields. Public docs do not guarantee every column name in manual exports, so synthetic fields must be clearly labeled modeled fields.
  - Synthetic bridge implication: implement body-composition CSV rows with `measured_at`, `weight_kg`, `weight_lb`, `body_fat_percent`, `muscle_mass_kg`, `bone_mass_kg`, and explicit `unit_system`.

## Timestamp And Timezone Implications
- FIT activity data has UTC-like timestamp semantics and local timestamp/timezone offset concerns. Synthetic fixtures should include both ISO timestamps and explicit timezone labels to force local-date attribution tests.
- Sleep spans cross midnight by nature; synthetic sleep fixtures must include start/end windows and local date fields, not only a single observed timestamp.
- Timezone-boundary edge cases should include rows around `23:xx`/`00:xx` and UTC offset rows where the local date differs from UTC.
- Duplicate signatures should combine source family, domain, normalized time window, and stable normalized value rather than only source row id.

## Units And Field Mapping Implications
- Activity distance should support meters as a canonical normalized unit while synthetic CSV inputs may present kilometers or miles.
- Duration should normalize to seconds while preview can display minutes/hours.
- Heart rate is beats per minute, HRV fixture fields can use RMSSD milliseconds, and calories can use kcal.
- Body composition must exercise kg/lb conflicts because public support mentions CSV reports while Garmin devices/scales can operate across unit systems. Mission 013 synthetic rows should include a clean metric row, an imperial row requiring conversion, and a conflicting kg/lb row requiring review.

## Duplicate, Missing, And Malformed Cases
- Duplicate activity rows should share domain, start time, duration, distance, and activity type while differing in source row id.
- Timezone-boundary rows should be warnings, not hard errors, unless required timestamps are missing.
- Missing required fields should block reviewed commit until rejected or corrected through review state.
- Malformed numeric values should remain previewable with validation errors and should not materialize.

## Synthetic Fixture Design Constraints
- All files under `fixtures/garmin_exports/` must carry `synthetic_only: true` in manifest metadata or a visible synthetic label/header in CSV metadata.
- No file may claim to be an actual Garmin export or include real-person identifiers.
- Fixture families required before HDI-013-001 expansion:
  - `activities`
  - `sleep`
  - `body_composition`
- Edge cases required across the pack:
  - clean rows
  - duplicate candidates
  - timezone boundary
  - unit conflicts
  - missing fields
  - malformed rows
- Optional families to present in HDI-013-001:
  - wellness/HRV/stress, because public docs list HRV and stress and Mission 012 named Garmin as the target bridge.
  - hydration is lower-confidence from the public docs consulted in this mission and should not be recommended unless the sponsor explicitly wants broader fixture breadth.

## Implementation Recommendation For HDI-013-001
Recommend adding a compact wellness/HRV/stress fixture family beyond the three required families and setting default future-real-import retention to `keep-raw-until-verified`. This maximizes bridge-shape learning for public Garmin wellness categories while keeping the future real-data posture local, short, and reversible.

