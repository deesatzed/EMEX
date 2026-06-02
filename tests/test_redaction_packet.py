from pathlib import Path

from emex.oe_packet import build_oe_packet
from emex.redaction import contains_phi_like_text, redact_text
from emex.workflow import load_json


def test_redacts_phi_like_tokens():
    result = redact_text("Jane Smith DOB: 01/02/1970 MRN: ABC12345 phone 215-555-1212")
    assert "[NAME]" in result.redacted_text
    assert "[DOB]" in result.redacted_text
    assert "[MRN]" in result.redacted_text
    assert "[PHONE]" in result.redacted_text
    assert not contains_phi_like_text(result.redacted_text)


def test_oe_packet_contains_t0_and_clinician_review_warnings():
    payload = load_json(Path("fixtures/synthetic_ed/chest_pain_t0.json"))
    packet = build_oe_packet(payload)
    assert packet["valid"]
    assert "T0 BOUNDARY" in packet["redacted_oe_input"]
    assert "clinician review" in packet["redacted_oe_input"].lower()
    assert "Return plain text only" in packet["redacted_oe_input"]
    assert "Do not return JSON or code fences" in packet["redacted_oe_input"]
    assert "NEXT_STEP_TRIAGE_CATEGORY" in packet["redacted_oe_input"]
    assert "SUGGESTED_NEXT_STEP_LABS_DI" in packet["redacted_oe_input"]
    assert "SUGGESTED_PROVIDER_EVAL" in packet["redacted_oe_input"]
    assert packet["phi_redaction_report"]["copy_ready"] is True
