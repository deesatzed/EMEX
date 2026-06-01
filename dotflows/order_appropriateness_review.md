# EMEX DotFlow: Order Appropriateness Review

## Purpose
Review whether proposed order considerations are guideline-plausible, excessive, duplicative, or insufficient using the redacted EMEX T0 packet.

## Hard Rules
- Output is clinician-draft only.
- Do not grade outcomes with a knowledge base.
- Use `insufficient_information` when the T0 packet lacks key details.
- Identify low-value or duplicative testing risk explicitly.

## Expected Output Schema
Return fenced JSON with:

```json
{
  "risk_bucket": "insufficient_information",
  "suggested_order_considerations": [],
  "resource_forecast": [],
  "cost_restraint_cautions": [],
  "missing_information": [],
  "evidence_notes": [],
  "safety_flags": ["clinician-draft only"]
}
```
