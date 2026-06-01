# EMEX DotFlow: Cost Restraint Review

## Purpose
Identify patient-cost and low-value testing cautions so EMEX does not reward faster over-testing.

## Hard Rules
- Clinician-draft only.
- Patient safety overrides cost.
- Do not recommend avoided care as success without outcome ascertainment.
- Use `insufficient_information` for uncertain cost/restraint judgments.

## Expected Output Schema
Return fenced JSON compatible with EMEX:

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
