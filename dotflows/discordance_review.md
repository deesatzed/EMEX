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

If timing is unclear, set `risk_bucket` to `insufficient_information` or `uncertain` and add a `safety_flags` entry.

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
- `suggested_order_considerations` with items that may need PI chart review, using non-imperative language.
- `resource_forecast` with operational deltas if relevant.
- `cost_restraint_cautions` with duplicate or low-value review questions if relevant.
- `missing_information` with facts needed for a fair review.
- `evidence_notes` with OpenEvidence-cited rationale or explicit uncertainty.
- `safety_flags` with timing, PHI, or review-limit flags.

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

## Expected Output Schema
Return fenced JSON compatible with EMEX:

```json
{
  "risk_bucket": "low_risk | moderate_risk | high_risk | uncertain | insufficient_information",
  "suggested_order_considerations": [],
  "resource_forecast": [],
  "cost_restraint_cautions": [],
  "missing_information": [],
  "evidence_notes": [],
  "safety_flags": ["clinician-draft only; discordance review only"]
}
```

## Final Quality Check
Before answering, verify:
- The output is fenced JSON.
- Every required EMEX key is present.
- T0 facts are separated from later facts.
- Discordance is framed as a PI review signal, not a correctness verdict.
- No direct identifiers are repeated.
