# GOAL.md

## Copy-Paste Codex Goal

```text
/goal
OUTCOME:
Create EMEX (Emergency Medicine Engagement Exchange) Phase 1 as a synthetic-first local web and CLI pilot for a manual OpenEvidence (OE) DotFlow workflow. EMEX lets a clinician-user paste or upload EHR-derived context that was obtained outside the application, redacts PHI, rejects current-visit post-triage leakage, generates OE DotFlow-ready input, accepts manually pasted OE output, and converts that output into clinician-draft next-step triage synthesis plus auditable PI artifacts. Phase 1 must not connect to Epic/EHR, must not call OE directly, must not use real PHI in the runnable milestone, and must not perform autonomous diagnosis, orders, disposition, routing, or patient-facing advice.

PROOF OF DONE:
1. Create the EMEX repo at `/Volumes/WS4TB/WS4TBr/clinclaw/EMEX` with project docs, source, tests, fixtures, DotFlows, and a local web UX.
2. Create docs: `docs/PROJECT_CHARTER.md`, `docs/PI_METRICS_CHARTER.md`, `docs/DATA_DICTIONARY_DRAFT.md`, `docs/ORDER_MATCHING_RULES_DRAFT.md`, `docs/SAFETY_AND_CALIBRATION_PLAN.md`, `docs/COST_RESTRAINT_METRICS.md`, `docs/DISCORDANCE_REVIEW_PLAN.md`, `docs/UNRESOLVED_FAULTS.md`, and `docs/CODEX_RESUME.md`.
3. Create OE DotFlows in `dotflows/`: `ed_shadow_recommender.md`, `order_appropriateness_review.md`, `risk_resource_forecast.md`, `cost_restraint_review.md`, and `discordance_review.md`.
4. Implement a local web UX where the user can paste/upload synthetic EHR-like context, review redaction/leakage results, copy OE-ready input, paste OE output, and view clinician-draft structured suggestions.
5. Implement CLI commands:
   - `python -m emex.cli validate-fixture --input fixtures/synthetic_ed/chest_pain_t0.json`
   - `python -m emex.cli prepare-oe --input fixtures/synthetic_ed/chest_pain_t0.json --out artifacts/shadow_demo`
   - `python -m emex.cli ingest-oe --case artifacts/shadow_demo/oe_input_packet.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/shadow_demo`
   - `python -m emex.cli run-demo --input fixtures/synthetic_ed/chest_pain_t0.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/shadow_demo`
6. Confirm the demo emits: `redacted_oe_input.md`, `phi_redaction_report.json`, `leakage_report.json`, `oe_input_packet.json`, `oe_output_raw.md`, `structured_suggestions.json`, `trace.json`, `report.html`, and `PI_SUMMARY.md`.
7. Run `pytest -q` and confirm it exits 0.
8. Run `python -m py_compile $(find src -name '*.py')` or an equivalent syntax check and confirm it exits 0.
9. Confirm no real PHI, credentials, secrets, API keys, Epic exports, or real patient data are committed.
10. Provide a final changed-file summary, verification-command summary, demo URL/path, and remaining-risk summary.

FIRST-PILOT UX:
1. User has EHR access outside EMEX and gathers the pertinent information for each patient to be analyzed.
2. Source material may include past history summary, medications/allergies, recent or key historical diagnostic imaging, procedures, relevant prior consult notes, and current-visit triage information.
3. User manually pastes text or uploads a local text/JSON file into EMEX.
4. EMEX processes the material locally, redacts PHI, and rejects current-visit post-triage leakage before generating OE DotFlow-ready input.
5. User copies the redacted packet into OE and runs the appropriate DotFlow manually.
6. OE outputs its evaluation to the OE screen.
7. User copies the plain-text OE output back into EMEX.
8. EMEX preserves the raw OE output, parses labeled plain-text sections into structured clinician-draft next-step triage synthesis, and emits audit artifacts.

FINAL TRIAGE SYNTHESIS:
- `immediate_acute_critical_care_provider_eval`: needs acute/critical care or immediate provider evaluation.
- `provider_eval_with_labs_di_plan`: needs provider evaluation plus suggested next-step labs/DI to complete triage.
- `structured_outpatient_or_telehealth_review`: potentially stable for outpatient, telehealth, or triage-provider review after clinician confirmation.
- `hybrid_labs_di_then_outpatient_review`: needs targeted labs/DI or provider review before outpatient-style planning can be considered.
- `insufficient_information`: cannot safely classify from the supplied triage-complete information.

EXPECTED SYNTHESIS FIELDS:
- `next_step_triage_category`
- `triage_rationale`
- `suggested_next_step_labs_di`
- `suggested_provider_eval`
- `outpatient_or_telehealth_considerations`
- `hybrid_pathway_considerations`
- `missing_information`
- `evidence_notes`
- `safety_flags`

SAFETY / PROVENANCE:
- Synthetic mode is the only runnable milestone. Real PHI mode is blocked until an approved environment, QI/IRB/compliance path, and privacy controls are documented.
- EHR extraction is outside EMEX scope. EMEX does not connect to Epic, Clarity, Caboodle, FHIR, or any production clinical system in Phase 1.
- OE use is manual. EMEX does not call OE APIs or transmit content to external services.
- Redaction must run before the OE packet is shown as copy-ready.
- Invalid or leaky input must not emit `redacted_oe_input.md`; only redaction/leakage reports may be written.
- Every OE packet must include a T0 boundary warning and a clinician-review warning.
- The app must reject current-visit post-triage fields such as current labs, imaging results, ED-course notes, final diagnosis, disposition, or downstream outcomes as recommender input.
- Historical prior diagnostics/procedures/consults are allowed only when represented as pre-T0 context.
- Clinician-draft suggestions are for PI review and clinician review only. They are not patient-facing and are not orders, diagnoses, disposition instructions, or autonomous clinical decisions.
- Unknown or unparseable OE output must be marked `needs_review`; EMEX must not force a recommendation.
- Preserve raw input hash, redacted packet hash, OE output hash, and hash-chained trace events for auditability.
- Preserve one end-to-end trace across prepare and ingest; do not overwrite prepare events during OE ingestion.
- Carry forward only useful ClinClaw patterns: synthetic fixture discipline, PHI-mode/source hashing, provenance ledger, fail-closed gating, and hash-chained trace output.
- Do not carry forward ClinClaw/CHI-Bench/PGx/PA/UM/CM product surface into EMEX Phase 1.

CONSTRAINTS:
- Keep the first milestone local, offline, and reproducible.
- Use no network-required runtime dependency for the core workflow.
- Do not add authentication-exposed HTTP APIs in Phase 1. The first web UX may be a static local page or localhost-only server.
- The static web UX is a workflow demo. CLI/backend artifacts are authoritative until web and CLI share the same Python safety logic.
- Do not remove or weaken safety checks to make demos pass.
- Do not invent Temple-specific Epic fields, legal status, order sets, QI/IRB determinations, or pilot approval.
- Mark unverified operational, Epic, legal, compliance, dataset, order-mapping, and Temple-specific facts as `FAULT [UNRESOLVED]`.

ITERATION:
1. Scaffold docs and control files first.
2. Implement data contracts for raw case input, redacted OE packet, OE output, structured suggestions, redaction report, leakage report, and trace.
3. Build tests for PHI redaction, T0 leakage rejection, OE packet generation, OE output parsing, and artifact emission.
4. Implement CLI workflow.
5. Implement local web UX over the same core logic or equivalent client-side logic with matching fixture schema.
6. Add DotFlows and ensure each expected output schema matches EMEX ingestion tests.
7. Run verification commands and update `docs/CODEX_RESUME.md` with current status, commands, assumptions, and remaining risks.

STOP:
Pause and summarize instead of continuing if:
- Real PHI, Epic credentials, production clinical data, external APIs, or legal/compliance approval are required.
- A required change would make EMEX provide patient-facing medical advice or autonomous orders/diagnosis/disposition.
- The same verification failure persists after three distinct repair attempts.
- A product decision is required for real-world pilot approval, QI/IRB, data access, or OE account/API terms.

COMPLETE:
Mark complete only when every PROOF OF DONE item passes using actual command output or direct artifact inspection, the implementation remains synthetic-first and local, and the final report clearly distinguishes implemented demo behavior from deferred real-PHI, Epic, OE integration, and clinical deployment.
```

## Goal Type

Synthetic-first local ED PI workflow prototype with manual OE DotFlow round trip, redaction/leakage controls, clinician-draft outputs, and audit artifacts.
