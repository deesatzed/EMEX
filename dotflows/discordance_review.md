# EMEX DotFlow: Discordance Review

## Purpose
Review differences between EMEX/OE clinician-draft suggestions and actual provider actions after the fact. This is PI and quality-review support only. Discordance is not proof that either the model or the clinician was correct.

## Provided Input
Use the pasted EMEX review packet:
- Original redacted T0 packet.
- EMEX/OE clinician-draft suggestions.
- Actual provider actions, final diagnoses, disposition, or outcomes only if the user explicitly includes them for after-the-fact review.
- EMEX redaction and leakage notes.

Keep T0 prediction review separate from after-the-fact observed outcomes.

## Step 1 - Input Completeness Check
Identify whether the review packet includes enough context:
- Original T0 facts used by the DotFlow.
- The draft suggestions being compared.
- Actual actions or outcomes, if discordance review is requested.
- Timing boundary between T0 facts and later facts.

If timing is unclear, set `NEXT_STEP_TRIAGE_CATEGORY` to `insufficient_information` and add a `SAFETY_FLAGS` entry.

## Step 2 - Discordance Classification
Classify differences without assigning blame:
- Suggested but not done.
- Done but not suggested.
- Suggested and done.
- Not assessable from supplied facts.
- Later-fact explanation, when post-T0 facts clarify why a difference occurred.

Do not treat provider concordance as correctness. Do not treat model disagreement as error without evidence.

## Step 3 - Review Output
Populate:
- `NEXT_STEP_TRIAGE_CATEGORY` with the after-the-fact review category.
- `TRIAGE_RATIONALE` with why the category fits the supplied review facts.
- `SUGGESTED_NEXT_STEP_LABS_DI` with items that may need PI chart review, using non-imperative language.
- `SUGGESTED_PROVIDER_EVAL` with provider review questions needed to complete the PI review.
- `OUTPATIENT_OR_TELEHEALTH_CONSIDERATIONS` when the review suggests outpatient-style planning could have been considered.
- `HYBRID_PATHWAY_CONSIDERATIONS` when targeted labs/DI or provider review separates pathways.
- `MISSING_INFORMATION` with facts needed for a fair review.
- `EVIDENCE_NOTES` with OpenEvidence-cited rationale or explicit uncertainty.
- `SAFETY_FLAGS` with timing, PHI, or review-limit flags.

## Evidence Rules
- Use OpenEvidence-cited evidence or guideline rationale where available.
- Do not invent standard-of-care conclusions, malpractice implications, probabilities, or outcome rates.
- Separate clinical evidence from hindsight. Later outcomes may explain discordance but must not be fed back into the original T0 recommendation.
- Use "requires chart review" when the answer depends on facts outside the packet.

## Privacy Rules
- Do not reproduce direct identifiers, exact dates, facility names, clinician names, MRNs, accession numbers, phone numbers, addresses, zip codes, or unredacted PHI.
- Do not request raw PHI or direct EHR access.
- If identifiers appear, flag the packet and avoid substantive review.

## Forbidden Output
Do not write:
- "The clinician was wrong"
- "The model was correct"
- "Standard of care was breached"
- "Order..."
- "Discharge..."
- "Admit..."
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
- clinician-draft only; discordance review only

## Final Quality Check
Before answering, verify:
- The output is plain text with every required EMEX label present.
- T0 facts are separated from later facts.
- Discordance is framed as a PI review signal, not a correctness verdict.
- No direct identifiers are repeated.
