# Codex Resume

## Current State

EMEX Phase 1 scaffold and implementation are present: synthetic-first local web and CLI workflow for manual OE DotFlow round trip.

## Commands

```bash
pytest -q
python -m emex.cli validate-fixture --input fixtures/synthetic_ed/chest_pain_t0.json
python -m emex.cli prepare-oe --input fixtures/synthetic_ed/chest_pain_t0.json --out artifacts/shadow_demo
python -m emex.cli ingest-oe --case artifacts/shadow_demo/oe_input_packet.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/shadow_demo
python -m emex.cli run-demo --input fixtures/synthetic_ed/chest_pain_t0.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/shadow_demo
python3 -m http.server 4174
```

## Verification Snapshot

- `pytest -q`: `16 passed`.
- `python -m emex.cli validate-fixture --input fixtures/synthetic_ed/chest_pain_t0.json`: valid.
- `python -m emex.cli prepare-oe --input fixtures/synthetic_ed/chest_pain_t0.json --out artifacts/shadow_demo`: prepared OE packet.
- `python -m emex.cli ingest-oe --case artifacts/shadow_demo/oe_input_packet.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/shadow_demo`: parsed OE output as `clinician_draft`.
- `python -m emex.cli run-demo --input fixtures/synthetic_ed/chest_pain_t0.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/shadow_demo`: demo complete.
- `python -m compileall -q src/emex emex`: passed.
- `pytest tests/test_hardening.py -q`: `5 passed`.
- Hardening demo: end-to-end trace includes prepare and ingest events.
- Leaky-input check: `artifacts/leaky_check/` contains reports and `trace.json`; it does not contain `redacted_oe_input.md`.

## Assumptions

- Synthetic data only.
- EHR extraction outside EMEX.
- OE use manual through user interface.
- Clinician-draft output only.

## Remaining Risks

- Real PHI and production use are blocked pending approved environment and compliance review.
- Synthetic redaction tests do not prove real PHI safety.
- DotFlows require user validation in OE.
- Static web UX is demo-only; CLI/backend artifacts are authoritative until web and CLI share one safety engine.
