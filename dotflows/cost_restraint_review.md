# EMEX DotFlow: Cost Restraint Review

## Purpose
Identify clinician-draft cost, duplication, and low-value care cautions for an EMEX redacted T0 packet. The goal is to prevent the pilot from rewarding faster over-testing. Patient safety overrides cost restraint.

## Provided Input
Use only the pasted EMEX packet:
- Redacted T0 history and triage context.
- Prior diagnostics, procedures, and consult summaries when supplied.
- Medication and comorbidity context relevant to risk.
- Existing clinician-draft suggestions if supplied.
- EMEX redaction and leakage notes.

Do not use post-T0 final outcomes to declare that avoided care was appropriate.

## Step 1 - Input Completeness Check
Identify whether enough information exists to discuss cost restraint:
- Prior recent imaging or testing relevant to the current complaint.
- Clinical instability or high-risk features that would make restraint unsafe.
- Contraindications, pregnancy status, renal risk, anticoagulation, or allergy context when relevant.
- Whether the proposed test appears duplicate, low yield, or guideline-supported.

Put absent context in `missing_information`.

## Step 2 - Safety-First Cost Screen
For each caution, state whether it is:
- Duplicate testing concern.
- Low-value testing concern.
- More conservative sequencing option.
- Unable to judge from supplied T0 facts.

Do not frame cost reduction as success unless the evidence and safety context support it.

## Step 3 - Structured Output
Populate:
- `cost_restraint_cautions` with concrete but non-imperative cautions.
- `suggested_order_considerations` only when safer sequencing or alternative evaluation should be reviewed.
- `resource_forecast` if cost and resource intensity are linked.
- `evidence_notes` with cited support or uncertainty.
- `safety_flags` for any reason restraint could be unsafe.

## Evidence Rules
- Use OpenEvidence-cited evidence or guideline rationale where available.
- Do not invent dollar amounts, savings, utilization rates, or risk reductions.
- Do not penalize high-cost testing that is safety-justified by T0 facts.
- If the evidence does not support a low-value judgment, state `insufficient_information`.

## Privacy Rules
- Do not reproduce direct identifiers, exact dates, facility names, clinician names, MRNs, accession numbers, phone numbers, addresses, zip codes, or unredacted PHI.
- Do not request raw PHI or direct EHR access.
- If identifiers appear, flag them and avoid substantive review.

## Forbidden Output
Do not write:
- "Do not order..."
- "Cancel..."
- "Deny..."
- "Withhold..."
- "The cheaper pathway is..."
- Patient instructions.
- Hidden chain-of-thought or internal deliberation.

## Expected Plain Text Output
Return plain text only. Do not return JSON. Do not use code fences. Use these labels exactly:

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

## Final Quality Check
Before answering, verify:
- The output is plain text with every required EMEX label present.
- Patient safety is explicitly preserved when cost restraint is discussed.
- No imperative cancellation or withholding language is used.
- No direct identifiers are repeated.
