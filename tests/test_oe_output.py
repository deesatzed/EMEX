from pathlib import Path

from emex.oe_output import parse_oe_output


def test_parse_fenced_json_oe_output():
    text = Path("fixtures/oe_outputs/chest_pain_oe_output.md").read_text()
    suggestions = parse_oe_output(text, "SYN-ED-CP-001")
    assert suggestions["status"] == "clinician_draft"
    assert suggestions["risk_bucket"] == "moderate_risk"
    assert suggestions["suggested_order_considerations"]
    assert "not autonomous orders" in suggestions["use_limitation"]


def test_unstructured_oe_output_needs_review():
    suggestions = parse_oe_output("No structure here.", "SYN-X")
    assert suggestions["status"] == "needs_review"
    assert suggestions["safety_flags"]
