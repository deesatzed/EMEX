import json
from pathlib import Path

from emex.workflow import run_demo


def test_run_demo_emits_required_artifacts(tmp_path):
    run_demo(
        Path("fixtures/synthetic_ed/chest_pain_t0.json"),
        Path("fixtures/oe_outputs/chest_pain_oe_output.md"),
        tmp_path,
    )
    expected = {
        "redacted_oe_input.md",
        "phi_redaction_report.json",
        "leakage_report.json",
        "oe_input_packet.json",
        "oe_output_raw.md",
        "structured_suggestions.json",
        "trace.json",
        "report.html",
        "PI_SUMMARY.md",
    }
    assert expected.issubset({p.name for p in tmp_path.iterdir()})
    suggestions = json.loads((tmp_path / "structured_suggestions.json").read_text())
    assert suggestions["status"] == "clinician_draft"


def test_trace_file_is_hash_chained(tmp_path):
    run_demo(
        Path("fixtures/synthetic_ed/chest_pain_t0.json"),
        Path("fixtures/oe_outputs/chest_pain_oe_output.md"),
        tmp_path,
    )
    trace = json.loads((tmp_path / "trace.json").read_text())
    assert trace["event_count"] >= 1
    assert trace["events"][0]["prev_hash"] == "0" * 64
