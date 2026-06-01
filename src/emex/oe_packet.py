"""Generate OpenEvidence DotFlow-ready packets from validated local case input."""

from __future__ import annotations

import json
from typing import Any

from .contracts import validate_case_payload
from .hashing import hash_json, hash_text
from .redaction import redact_text


def case_to_text(payload: dict[str, Any]) -> str:
    """Render the user-provided EHR-like context into a deterministic text packet."""
    ehr = payload.get("ehr_context", {})
    triage = payload.get("triage", {})
    sections = [
        ("Case ID", payload.get("case_id", "")),
        ("Past History Summary", ehr.get("past_history_summary", "")),
        ("Medications and Allergies", "\n".join(ehr.get("medications_allergies", []))),
        ("Historical Diagnostics", "\n".join(ehr.get("historical_diagnostics", []))),
        ("Historical Procedures", "\n".join(ehr.get("historical_procedures", []))),
        ("Relevant Prior Consults", "\n".join(ehr.get("prior_consult_notes", []))),
        ("Chief Complaint", triage.get("chief_complaint", "")),
        ("Triage Note", triage.get("triage_note", "")),
        ("Vitals", json.dumps(triage.get("vitals", {}), sort_keys=True)),
        ("Acuity", triage.get("acuity", "")),
    ]
    return "\n\n".join(f"## {title}\n{body}" for title, body in sections)


def build_oe_packet(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate, redact, and package an EMEX case for manual OE DotFlow use."""
    validation = validate_case_payload(payload)
    source_text = case_to_text(payload)
    redaction = redact_text(source_text)

    packet_md = "\n\n".join(
        [
            "# EMEX Redacted OE DotFlow Input",
            "SAFETY BOUNDARY: This packet is for clinician review and PI shadow evaluation only.",
            "T0 BOUNDARY: Use only pre-T0 historical context and current triage information. Do not infer from labs, imaging results, ED course, diagnosis, disposition, or outcomes.",
            "OUTPUT REQUEST: Return structured clinician-draft suggestions with risk bucket, suggested order considerations, resource forecast, cost/restraint cautions, missing information, and evidence/citation notes. Use insufficient_information instead of forced recommendations.",
            redaction.redacted_text,
        ]
    )

    return {
        "schema_version": "emex.oe_input_packet.v0.1",
        "case_id": payload.get("case_id", ""),
        "mode": payload.get("mode", ""),
        "valid": validation.valid,
        "validation_errors": validation.errors,
        "validation_warnings": validation.warnings,
        "raw_input_hash": hash_json(payload),
        "redacted_packet_hash": hash_text(packet_md),
        "redacted_oe_input": packet_md,
        "phi_redaction_report": {
            "schema_version": "emex.phi_redaction_report.v0.1",
            "case_id": payload.get("case_id", ""),
            "findings": redaction.findings,
            "copy_ready": validation.valid,
            "note": "Synthetic-first redaction report. Real PHI use remains blocked without approved environment.",
        },
        "leakage_report": {
            "schema_version": "emex.leakage_report.v0.1",
            "case_id": payload.get("case_id", ""),
            "blocked": not validation.valid,
            "errors": validation.errors,
            "warnings": validation.warnings,
        },
    }
