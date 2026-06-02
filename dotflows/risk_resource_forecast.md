# EMEX DotFlow: Risk Resource Forecast

## Purpose
Forecast draft ED risk and likely resource intensity from an EMEX redacted T0 packet. The output is for clinician review and PI workflow only. It is not a bed request, throughput directive, admission recommendation, or discharge recommendation.

## Provided Input
Use only the pasted EMEX packet:
- T0 case summary.
- Redacted past history, medications, key diagnostics, procedures, and consult history.
- Current triage facts available at T0.
- EMEX redaction and leakage notes.

Do not use post-T0 diagnostics, ED course, final disposition, or outcomes. If the packet includes them, flag the issue and avoid substantive resource forecasting.

## Step 1 - Input Completeness Check
Check whether these resource-relevant facts are present:
- Triage acuity and vital sign pattern.
- Complaint category and symptom severity.
- Comorbidity and medication risk.
- Prior utilization or procedural history when supplied.
- Known social or follow-up constraints only if already redacted and supplied.

List missing facts in `missing_information`.

## Step 2 - Next-Step Triage Category
Select one:
- `immediate_acute_critical_care_provider_eval`
- `provider_eval_with_labs_di_plan`
- `structured_outpatient_or_telehealth_review`
- `hybrid_labs_di_then_outpatient_review`
- `insufficient_information`

Do not translate this bucket into a disposition.

## Step 3 - Next-Step Resource and Evaluation Forecast
Describe likely review needs using cautious language:
- Monitoring intensity to consider.
- Diagnostic complexity to anticipate.
- Consultation or reassessment pressure if supported by T0 facts.
- Bottleneck risks such as serial testing, imaging pathway, or observation needs.

Keep the forecast operational and non-authoritative.

## Evidence Rules
- Use OpenEvidence-cited literature or guideline rationale when available.
- Do not invent admission probabilities, length of stay, bed demand, or return visit rates.
- Use `uncertain` or `insufficient_information` instead of overfitting weak context.
- Distinguish clinical risk from operational resource intensity.

## Privacy Rules
- Do not reproduce direct identifiers, exact dates, facility names, clinician names, MRNs, accession numbers, phone numbers, addresses, zip codes, or unredacted PHI.
- Do not request raw PHI or direct EHR access.
- If identifiers appear, flag them in `safety_flags`.

## Forbidden Output
Do not write:
- "Admit..."
- "Discharge..."
- "Place in observation..."
- "Assign a bed..."
- "The correct disposition is..."
- Patient instructions.
- Hidden chain-of-thought or internal deliberation.

## Expected Plain Text Output
Return plain text only. Do not return JSON. Do not use code fences. Use these labels exactly:

NEXT_STEP_TRIAGE_CATEGORY: immediate_acute_critical_care_provider_eval | provider_eval_with_labs_di_plan | structured_outpatient_or_telehealth_review | hybrid_labs_di_then_outpatient_review | insufficient_information

TRIAGE_RATIONALE:
- Rationale...

SUGGESTED_NEXT_STEP_LABS_DI:
- Consider...

SUGGESTED_PROVIDER_EVAL:
- Provider evaluation needed...

OUTPATIENT_OR_TELEHEALTH_CONSIDERATIONS:
- Outpatient or telehealth consideration...

HYBRID_PATHWAY_CONSIDERATIONS:
- Hybrid pathway consideration...

MISSING_INFORMATION:
- Missing...

EVIDENCE_NOTES:
- Evidence...

SAFETY_FLAGS:
- clinician-draft only; no disposition authority

## Final Quality Check
Before answering, verify:
- The output is plain text with every required EMEX label present.
- Resource language is a forecast for review, not a command.
- No disposition, bed, or patient-facing instruction is given.
- No direct identifiers are repeated.
