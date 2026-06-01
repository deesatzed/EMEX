# Data Dictionary Draft

## Case Input

- `case_id`: synthetic case identifier.
- `mode`: must be `synthetic` for the runnable milestone.
- `ehr_context.past_history_summary`: pre-T0 historical context.
- `ehr_context.medications_allergies`: medication and allergy summary.
- `ehr_context.historical_diagnostics`: prior diagnostics only.
- `ehr_context.historical_procedures`: prior procedures only.
- `ehr_context.prior_consult_notes`: prior consult summaries only.
- `triage.chief_complaint`: current visit chief complaint.
- `triage.triage_note`: current triage note.
- `triage.vitals`: current triage vitals.
- `triage.acuity`: ESI/acuity if available.

## Blocked Input

Current-visit labs, imaging results, ED course, provider notes, final diagnosis, disposition, and outcomes are blocked as recommender input.
