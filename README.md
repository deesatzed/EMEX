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

The web page mirrors the pilot flow: paste synthetic EHR-like text or JSON context, redact and package it for OE, paste OE output back, and view clinician-draft structured suggestions.

The static web page is a workflow demo. The CLI/backend artifact path is authoritative for safety checks and audit artifacts until the web UI shares the Python validation/redaction engine.

OE Companion Mode:

1. Open OpenEvidence and authenticate in the browser with the user's normal OE account.
2. Open EMEX at the local web URL.
3. Use browser split view or two side-by-side windows so OE and EMEX remain visible together.
4. Keep the workflow manual: EMEX does not iframe OE, read OE pages, automate OE, or send data to OE directly.

Provider web workflow:

1. Load clinical information by pasting or uploading deidentified/synthetic narrative text, `.txt`, `.md`, or structured JSON.
2. Click `Prepare OE` to redact identifiers, check post-triage leakage, and create copy-ready OE input.
3. Copy the redacted packet into OpenEvidence and run DotFlows in this order:
   - `ed_shadow_recommender`
   - `order_appropriateness_review`
   - `risk_resource_forecast`
   - `cost_restraint_review`
   - `discordance_review` only after actual provider actions/outcomes are available for retrospective PI review.
4. Paste the OE output back into EMEX. The expected OE output is plain text with the labels shown in the DotFlow, not JSON.
5. Click `Parse OE` to view clinician-draft next-step triage synthesis.

Expected final triage synthesis:

- `immediate_acute_critical_care_provider_eval`: needs acute/critical care or immediate provider evaluation.
- `provider_eval_with_labs_di_plan`: needs provider evaluation plus suggested next-step labs/DI to complete triage.
- `structured_outpatient_or_telehealth_review`: potentially stable for outpatient, telehealth, or triage-provider review after clinician confirmation.
- `hybrid_labs_di_then_outpatient_review`: needs targeted labs/DI or provider review before outpatient-style planning can be considered.
- `insufficient_information`: cannot safely classify from the supplied triage-complete information.

The parsed output includes triage rationale, suggested next-step labs/DI, suggested provider evaluation, outpatient/telehealth considerations, hybrid pathway considerations, missing information, evidence notes, and safety flags.

## Safety Boundaries

- Synthetic mode only for the first runnable milestone.
- No real PHI.
- No Epic/EHR integration.
- No OE API integration.
- No autonomous orders, diagnosis, disposition, routing, or patient-facing advice.
- Clinician-draft output is for PI review and clinician review only.
- Invalid or leaky input does not produce a copy-ready OE packet in the authoritative CLI workflow.
