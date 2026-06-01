# EMEX DotFlow: Risk Resource Forecast

## Purpose
Forecast risk bucket and likely ED resource needs from a redacted EMEX T0 packet.

## Hard Rules
- Clinician-draft only.
- No disposition decision.
- No bed request authority.
- If the input does not support a resource forecast, return `insufficient_information`.

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
  "safety_flags": ["clinician-draft only; no disposition authority"]
}
```
