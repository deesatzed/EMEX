# Safety And Calibration Plan

## Safety Floor

EMEX Phase 1 does not assert safety. It creates artifacts needed for later safety analysis.

## Calibration

Later real-data phases must compare risk buckets to observed outcomes. Unknown outcomes are safety debt, not success.

## Non-Negotiables

- No patient-facing advice.
- No autonomous orders.
- No autonomous diagnosis.
- No autonomous disposition.
- No post-T0 leakage.
- No real PHI without approved environment and compliance path.
- Invalid or leaky input must not produce copy-ready OE text.
- One trace must cover raw input, redaction, OE packet generation, OE output ingestion, parser status, and artifact emission.
