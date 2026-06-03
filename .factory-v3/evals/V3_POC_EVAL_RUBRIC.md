# V3 POC Eval Rubric

## Version
v0.1

## Purpose
Judge whether V3 passed the operational POC.

## Decision Scale
| Decision | Meaning |
| --- | --- |
| `PASS_NAMED_POC` | V3 worked standalone for the named private POC scope. |
| `PASS_WITH_LIMITATIONS` | V3 worked, but limits must be recorded before baseline release. |
| `NO_GO_STANDALONE_GAP` | V3 required V2 or missed a required standalone capability. |
| `NO_GO_APP_INCOMPLETE` | V3 stayed standalone, but the POC app did not meet scope. |
| `CONTINUE_RESEARCH` | Garmin, Hermes, deployment, or verification questions remain unresolved. |

## Scoring
Score each dimension 0-2.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| V3-only compliance | V2 used or required. | No V2 used, but evidence is incomplete. | No V2 used and evidence is clear. |
| Mission clarity | Missions ambiguous. | Some mission gaps. | Clear objective, scope, commands, verification. |
| Scope discipline | Unapproved changes. | Minor ambiguity. | Every edit maps to mission authority. |
| App completeness | POC target missed. | Partial target met. | Approved POC target met. |
| Verification quality | Checks missing. | Checks partial. | Checks appropriate and passing or halted correctly. |
| Deployment evidence | Missing when required. | Partial/private smoke only. | Approved private target verified. |
| Evidence replay | Cannot reconstruct. | Reconstructable with gaps. | Mission records and closeouts are replayable. |
| Halt behavior | Continued after failure. | Halted but evidence weak. | Halted cleanly and recorded decision. |
| Dependency discipline | Unapproved dependency use. | Approved but weakly recorded. | Garmin/Hermes/other dependencies properly researched, approved, and labeled. |
| Operator friction | Too hard to use operationally. | Usable with notable friction. | Usable enough as first baseline. |

## Minimum Pass Bar
To record `PASS_NAMED_POC`:
- V3-only compliance must score 2.
- No dimension may score 0.
- Total score must be at least 16 of 20.
- App completeness, verification quality, and evidence replay must each score at least 1.
- Any Garmin or Hermes use must be separately approved and labeled.

## Baseline Release Note
A passing POC supports only a first operational baseline for the named scope. It does not approve:
- V3 as default for all work,
- required gates,
- public deployment,
- runtime authority,
- proof or lease enforcement,
- governance routing,
- V2 removal from the Factory_V3 repository.

