# EMEX

EMEX (Emergency Medicine Engagement Exchange) is a synthetic-first Phase 1 pilot for a manual OpenEvidence DotFlow workflow.

It does not connect to an EHR, does not call OpenEvidence directly, and does not produce patient-facing advice. The first runnable milestone uses synthetic EHR-like fixtures only.

## Demo

```bash
python -m emex.cli run-demo \
  --input fixtures/synthetic_ed/chest_pain_t0.json \
  --oe-output fixtures/oe_outputs/chest_pain_oe_output.md \
  --out artifacts/shadow_demo
```

Artifacts:

```text
artifacts/shadow_demo/
  redacted_oe_input.md
  phi_redaction_report.json
  leakage_report.json
  oe_input_packet.json
  oe_output_raw.md
  structured_suggestions.json
  trace.json
  report.html
  PI_SUMMARY.md
```

## Local Web UX

Open `web/index.html` in a browser, or serve it locally:

```bash
python3 -m http.server 4174
```

The web page mirrors the pilot flow: paste synthetic EHR-like context, redact and package it for OE, paste OE output back, and view clinician-draft structured suggestions.

The static web page is a workflow demo. The CLI/backend artifact path is authoritative for safety checks and audit artifacts until the web UI shares the Python validation/redaction engine.

## Safety Boundaries

- Synthetic mode only for the first runnable milestone.
- No real PHI.
- No Epic/EHR integration.
- No OE API integration.
- No autonomous orders, diagnosis, disposition, routing, or patient-facing advice.
- Clinician-draft output is for PI review and clinician review only.
- Invalid or leaky input does not produce a copy-ready OE packet in the authoritative CLI workflow.
