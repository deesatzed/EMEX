from pathlib import Path

from emex.oe_output import parse_oe_output


def test_parse_plain_text_labeled_oe_output():
    text = """OpenEvidence synthetic output

RISK_BUCKET: moderate_risk

SUGGESTED_ORDER_CONSIDERATIONS:
- Consider ECG early because exertional chest pressure is time-sensitive and low burden.
- Consider troponin pathway per local chest pain protocol after clinician review.

RESOURCE_FORECAST:
- Likely monitored evaluation area if symptoms continue or ECG/troponin abnormal.

COST_RESTRAINT_CAUTIONS:
- Avoid broad CT imaging as default without presentation-specific indication.

MISSING_INFORMATION:
- Exact onset time and symptom persistence.

EVIDENCE_NOTES:
- Follow local chest pain protocol and clinician judgment.

SAFETY_FLAGS:
- Clinician review required before any action.
"""
    suggestions = parse_oe_output(text, "SYN-ED-CP-001")
    assert suggestions["status"] == "clinician_draft"
    assert suggestions["risk_bucket"] == "moderate_risk"
    assert len(suggestions["suggested_order_considerations"]) == 2
    assert "Parsed plain text labeled OE output" in suggestions["parse_warnings"]


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
