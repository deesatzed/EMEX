# EMEX DotFlow: Discordance Review

## Purpose
Review differences between EMEX/OE clinician-draft suggestions and actual provider actions after the fact.

## Hard Rules
- Clinician-draft only.
- Keep observed outcomes separate from appropriateness review.
- Do not treat provider concordance as correctness.
- Use `insufficient_information` when current facts cannot support a judgment.

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
  "safety_flags": ["clinician-draft only; discordance review only"]
}
```
