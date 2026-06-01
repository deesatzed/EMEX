import json
from pathlib import Path

import pytest

from emex.oe_output import parse_oe_output
from emex.redaction import contains_phi_like_text, redact_text
from emex.workflow import prepare_oe, run_demo


def test_invalid_input_does_not_emit_copy_ready_oe_text(tmp_path):
    packet = prepare_oe(Path("fixtures/synthetic_ed/leaky_current_results.json"), tmp_path)

    assert not packet["valid"]
    assert not (tmp_path / "redacted_oe_input.md").exists()
    assert (tmp_path / "phi_redaction_report.json").exists()
    assert (tmp_path / "leakage_report.json").exists()


def test_run_demo_trace_keeps_prepare_and_ingest_events(tmp_path):
    run_demo(
        Path("fixtures/synthetic_ed/chest_pain_t0.json"),
        Path("fixtures/oe_outputs/chest_pain_oe_output.md"),
        tmp_path,
    )

    trace = json.loads((tmp_path / "trace.json").read_text())
    event_types = [event["event_type"] for event in trace["events"]]
    assert "case_loaded" in event_types
    assert "oe_packet_prepared" in event_types
    assert "oe_output_loaded" in event_types
    assert "oe_output_parsed" in event_types
    assert "artifacts_emitted" in event_types


def test_redaction_handles_facility_provider_zip_order_accession_and_absolute_dates():
    source = (
        "Dr. Ada Rivera at Temple University Hospital reviewed accession ACC-991122 "
        "for order ORD-123456 on 2026-05-31. ZIP 19140. MRN# ZY987654."
    )

    result = redact_text(source)

    assert "[PROVIDER]" in result.redacted_text
    assert "[FACILITY]" in result.redacted_text
    assert "[ACCESSION]" in result.redacted_text
    assert "[ORDER_ID]" in result.redacted_text
    assert "[DATE]" in result.redacted_text
    assert "[ZIP]" in result.redacted_text
    assert not contains_phi_like_text(result.redacted_text)


def test_oe_disposition_or_order_language_forces_review():
    oe_text = """```json
{
  "risk_bucket": "moderate_risk",
  "suggested_order_considerations": ["Order troponin now", "Discharge if repeat test is normal"],
  "resource_forecast": [],
  "cost_restraint_cautions": [],
  "missing_information": [],
  "evidence_notes": [],
  "safety_flags": []
}
```"""

    suggestions = parse_oe_output(oe_text, "SYN-ED-CP-001")

    assert suggestions["status"] == "needs_review"
    assert any("order/disposition" in flag.lower() for flag in suggestions["safety_flags"])


def test_run_demo_refuses_leaky_input_without_artifact_copy_packet(tmp_path):
    with pytest.raises(ValueError):
        run_demo(
            Path("fixtures/synthetic_ed/leaky_current_results.json"),
            Path("fixtures/oe_outputs/chest_pain_oe_output.md"),
            tmp_path,
        )

    assert not (tmp_path / "redacted_oe_input.md").exists()
