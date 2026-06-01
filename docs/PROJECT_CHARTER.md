# EMEX Project Charter

EMEX (Emergency Medicine Engagement Exchange) Phase 1 is a synthetic-first local pilot for a manual OpenEvidence DotFlow workflow. It helps a clinician-user transform EHR-derived context into a redacted OE packet, then transform manually pasted OE output into structured clinician-draft suggestions and audit artifacts.

## Phase 1 Boundary

- Synthetic runnable milestone only.
- No Epic/EHR integration.
- No OE API integration.
- No real PHI.
- No autonomous diagnosis, orders, disposition, routing, or patient-facing advice.

## First Pilot UX

1. User gathers EHR-derived context outside EMEX.
2. User pastes/uploads synthetic EHR-like context into EMEX.
3. EMEX redacts PHI-like tokens and rejects post-T0 leakage.
4. User copies redacted OE input into OpenEvidence and runs an EMEX DotFlow.
5. User pastes OE output back into EMEX.
6. EMEX emits clinician-draft structured suggestions and audit artifacts.

The static web UX is a workflow demo. The authoritative Phase 1 artifact path is the CLI/backend workflow because it uses the Python validation, redaction, parser, and trace code.

## Value Proposition

The first pilot tests whether a manual, auditable OE round trip can structure ED post-triage reasoning without changing care and without leaking post-T0 information into the recommender.
