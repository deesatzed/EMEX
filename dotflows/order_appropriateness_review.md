# EMEX DotFlow: Order Appropriateness Review

## Purpose
Review EMEX clinician-draft order considerations against the redacted T0 context. The goal is to identify plausible, missing, duplicative, excessive, or low-value considerations for clinician review. This DotFlow does not create orders and does not judge final provider care.

## Provided Input
Use only the pasted EMEX packet and any clinician-draft suggestions included with it:
- Redacted T0 clinical context.
- Current triage facts available at T0.
- Existing next-step triage synthesis fields if EMEX supplies them.
- Redaction and leakage notes supplied by EMEX.

Do not use post-T0 diagnostic results, ED course, final diagnoses, disposition, or outcomes.

## Step 1 - Input Completeness Check
Determine whether the packet is sufficient to assess order appropriateness:
- Complaint-specific risk factors are present or explicitly absent.
- Medication/allergy risks are present when relevant.
- Baseline diagnostics or prior procedures are present when relevant.
- Triage vital signs and symptoms are available.

Put unavailable information in `MISSING_INFORMATION`. If the missing data prevents review, set `NEXT_STEP_TRIAGE_CATEGORY` to `insufficient_information`.

## Step 2 - Appropriateness Screen
For each proposed consideration, classify the concern in plain language:
- Plausible based on supplied T0 facts.
- Possibly insufficient because a high-risk feature is not addressed.
- Possibly excessive, duplicative, or low value.
- Unable to assess from supplied facts.

Keep this as clinician-draft review language, not as an instruction.

## Step 3 - Structured Output
Populate the EMEX plain-text labels:
- `NEXT_STEP_TRIAGE_CATEGORY`: one allowed next-step category.
- `TRIAGE_RATIONALE`: why the category fits the supplied T0 facts.
- `SUGGESTED_NEXT_STEP_LABS_DI`: non-imperative labs/DI considerations needed to complete next-step triage.
- `SUGGESTED_PROVIDER_EVAL`: provider evaluation needed before next-step triage.
- `OUTPATIENT_OR_TELEHEALTH_CONSIDERATIONS`: outpatient or telehealth planning considerations when appropriate.
- `HYBRID_PATHWAY_CONSIDERATIONS`: targeted labs/DI or provider review that could make outpatient-style planning possible.
- `MISSING_INFORMATION`: data needed before confident review.
- `EVIDENCE_NOTES`: OpenEvidence-cited rationale or limitation.
- `SAFETY_FLAGS`: safety, redaction, post-T0, or uncertainty flags.

## Evidence Rules
- Use OpenEvidence-cited evidence or guideline rationale where available.
- Do not invent sensitivity, specificity, absolute risk, cost, or utilization numbers.
- Do not equate fewer tests with better care unless safety and follow-up conditions are explicit.
- Separate "low value" from "contraindicated"; use the weaker term unless evidence supports the stronger one.

## Privacy Rules
- Do not reproduce direct identifiers, exact dates, facility names, clinician names, MRNs, accession numbers, phone numbers, addresses, zip codes, or unredacted PHI.
- Do not request raw PHI.
- Do not request direct EHR access.
- If unredacted identifiers are present, flag the packet and avoid substantive clinical review.

## Forbidden Output
Do not write:
- "Order..."
- "Cancel..."
- "Discharge..."
- "Admit..."
- "The provider should have..."
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
- clinician-draft only

## Final Quality Check
Before answering, verify:
- The output is plain text with every required EMEX label present.
- No post-T0 results or outcomes are used.
- The language is non-imperative and clinician-draft.
- Cost restraint never overrides patient safety.
