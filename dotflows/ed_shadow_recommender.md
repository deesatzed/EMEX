# EMEX DotFlow: ED Shadow Recommender

## Purpose
Generate clinician-draft risk and order considerations from a redacted EMEX T0 packet.

## Required Input
- EMEX redacted OE packet.
- Pre-T0 historical context only.
- Current triage information only.

## Hard Rules
- Do not use or infer post-T0 labs, imaging results, ED course, diagnosis, disposition, or outcomes.
- Do not produce patient-facing advice.
- Do not present output as orders.
- If information is missing, return `insufficient_information`.

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
  "safety_flags": ["clinician-draft only"]
}
```

All output is clinician-draft for PI review and clinician review only.
