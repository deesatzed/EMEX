# EMEX OpenEvidence DotFlows

These DotFlows are designed for the Phase 1 EMEX manual OpenEvidence round trip. EMEX prepares a redacted T0 packet locally; the user manually pastes that packet into OpenEvidence and runs one of these DotFlows; the user then pastes the OpenEvidence output back into EMEX.

EMEX does not call OpenEvidence directly, does not connect to an EHR, and does not send raw PHI to external services.

## Required Pilot DotFlows

| DotFlow | Use |
| --- | --- |
| `ed_shadow_recommender.md` | Primary T0 ED shadow review that produces clinician-draft risk, evaluation, resource, cost, missing-information, evidence, and safety fields. |
| `order_appropriateness_review.md` | Review of proposed order considerations for plausible, missing, excessive, duplicative, or low-value elements. |
| `risk_resource_forecast.md` | Resource-intensity forecast for PI review without disposition or bed authority. |
| `cost_restraint_review.md` | Safety-first review of cost, duplication, and low-value testing cautions. |
| `discordance_review.md` | After-the-fact PI review comparing EMEX/OE suggestions with observed provider actions while separating T0 facts from later facts. |

## Shared Plain Text Output Contract

Every DotFlow must return plain text with these labels. Do not return JSON. Do not use code fences.

RISK_BUCKET: low_risk | moderate_risk | high_risk | uncertain | insufficient_information

SUGGESTED_ORDER_CONSIDERATIONS:
- Consider...

RESOURCE_FORECAST:
- Likely...

COST_RESTRAINT_CAUTIONS:
- Avoid...

MISSING_INFORMATION:
- Missing...

EVIDENCE_NOTES:
- Evidence...

SAFETY_FLAGS:
- clinician-draft only

## Non-Negotiable Boundaries

- Output is clinician-draft only.
- Do not create orders, diagnoses, dispositions, bed requests, or patient-facing advice.
- Do not use post-T0 facts in T0 recommendation DotFlows.
- Do not reproduce direct identifiers or request raw PHI.
- Do not display hidden chain-of-thought or internal deliberation.
- Use `insufficient_information` rather than filling gaps with assumptions.
