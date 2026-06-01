"""End-to-end EMEX workflow orchestration."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from .oe_output import parse_oe_output
from .oe_packet import build_oe_packet
from .reporting import render_html_report, render_pi_summary, write_json
from .trace import Trace


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def prepare_oe(input_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = load_json(input_path)
    trace = Trace(session_id=str(uuid4()))
    trace.add("case_loaded", {"input_path": str(input_path), "case_id": payload.get("case_id", "")})
    packet = build_oe_packet(payload)
    trace.add(
        "oe_packet_prepared",
        {
            "case_id": packet["case_id"],
            "valid": packet["valid"],
            "redacted_packet_hash": packet["redacted_packet_hash"],
            "validation_errors": packet["validation_errors"],
        },
    )

    if packet["valid"]:
        (out_dir / "redacted_oe_input.md").write_text(packet["redacted_oe_input"], encoding="utf-8")
    write_json(out_dir / "phi_redaction_report.json", packet["phi_redaction_report"])
    write_json(out_dir / "leakage_report.json", packet["leakage_report"])
    packet_for_file = {k: v for k, v in packet.items() if k != "redacted_oe_input"}
    write_json(out_dir / "oe_input_packet.json", packet_for_file)
    (out_dir / "trace.json").write_text(trace.to_json(), encoding="utf-8")
    return packet


def ingest_oe(case_packet_path: Path, oe_output_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    packet = load_json(case_packet_path)
    oe_text = oe_output_path.read_text(encoding="utf-8")
    suggestions = parse_oe_output(oe_text, case_id=packet["case_id"])
    trace = _load_existing_trace(out_dir) or Trace(session_id=str(uuid4()))
    trace.add("oe_output_loaded", {"case_id": packet["case_id"], "oe_output_path": str(oe_output_path)})
    trace.add(
        "oe_output_parsed",
        {
            "case_id": packet["case_id"],
            "status": suggestions["status"],
            "oe_output_hash": suggestions["oe_output_hash"],
            "parse_warnings": suggestions["parse_warnings"],
        },
    )

    (out_dir / "oe_output_raw.md").write_text(oe_text, encoding="utf-8")
    write_json(out_dir / "structured_suggestions.json", suggestions)
    (out_dir / "report.html").write_text(render_html_report(packet, suggestions), encoding="utf-8")
    (out_dir / "PI_SUMMARY.md").write_text(render_pi_summary(packet, suggestions), encoding="utf-8")
    trace.add(
        "artifacts_emitted",
        {
            "case_id": packet["case_id"],
            "artifacts": [
                "oe_output_raw.md",
                "structured_suggestions.json",
                "report.html",
                "PI_SUMMARY.md",
                "trace.json",
            ],
        },
    )
    (out_dir / "trace.json").write_text(trace.to_json(), encoding="utf-8")
    return suggestions


def run_demo(input_path: Path, oe_output_path: Path, out_dir: Path) -> dict:
    packet = prepare_oe(input_path, out_dir)
    if not packet["valid"]:
        raise ValueError("Input failed validation; refusing to ingest OE output")
    suggestions = ingest_oe(out_dir / "oe_input_packet.json", oe_output_path, out_dir)
    return {"packet": packet, "suggestions": suggestions}


def _load_existing_trace(out_dir: Path) -> Trace | None:
    trace_path = out_dir / "trace.json"
    if not trace_path.exists():
        return None
    return Trace.from_dict(load_json(trace_path))
