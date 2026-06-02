from pathlib import Path

from emex.oe_output import parse_oe_output


def test_parse_plain_text_next_step_triage_synthesis():
    text = """OpenEvidence synthetic output

NEXT_STEP_TRIAGE_CATEGORY: provider_eval_with_labs_di_plan

TRIAGE_RATIONALE:
- Stable at triage but chest pressure with exertional component needs provider evaluation before pathway assignment.

SUGGESTED_NEXT_STEP_LABS_DI:
- Consider ECG and troponin pathway after clinician review.
- Consider basic labs if needed for medication safety or alternate diagnosis review.

SUGGESTED_PROVIDER_EVAL:
- Clinician should review chest pain features, vitals trend, ECG availability, and contraindications before next-step triage.

OUTPATIENT_OR_TELEHEALTH_CONSIDERATIONS:
- Outpatient-style planning is premature until targeted ED evaluation is reviewed.

HYBRID_PATHWAY_CONSIDERATIONS:
- If targeted tests and provider review remain reassuring, structured outpatient follow-up could be reviewed.

MISSING_INFORMATION:
- Exact onset time and current ECG are unavailable at T0.

EVIDENCE_NOTES:
- Follow local chest pain pathway and cited OE evidence.

SAFETY_FLAGS:
- Clinician review required before any action.
"""
    suggestions = parse_oe_output(text, "SYN-ED-CP-001")
    assert suggestions["status"] == "clinician_draft"
    assert suggestions["next_step_triage_category"] == "provider_eval_with_labs_di_plan"
    assert suggestions["triage_rationale"]
    assert suggestions["suggested_next_step_labs_di"]
    assert suggestions["suggested_provider_eval"]
    assert suggestions["outpatient_or_telehealth_considerations"]
    assert suggestions["hybrid_pathway_considerations"]


def test_unknown_next_step_triage_category_needs_review():
    text = """NEXT_STEP_TRIAGE_CATEGORY: send_home_now

TRIAGE_RATIONALE:
- Synthetic rationale.

SUGGESTED_NEXT_STEP_LABS_DI:
- Consider ECG.

SUGGESTED_PROVIDER_EVAL:
- Clinician review.

OUTPATIENT_OR_TELEHEALTH_CONSIDERATIONS:
- None.

HYBRID_PATHWAY_CONSIDERATIONS:
- None.

MISSING_INFORMATION:
- None.

EVIDENCE_NOTES:
- None.

SAFETY_FLAGS:
- Clinician review required.
"""
    suggestions = parse_oe_output(text, "SYN-X")
    assert suggestions["status"] == "needs_review"
    assert "Unknown next-step triage category" in suggestions["safety_flags"]


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


def test_parse_plain_text_fixture_output():
    text = Path("fixtures/oe_outputs/chest_pain_oe_output.md").read_text()
    suggestions = parse_oe_output(text, "SYN-ED-CP-001")
    assert suggestions["status"] == "clinician_draft"
    assert suggestions["next_step_triage_category"] == "provider_eval_with_labs_di_plan"
    assert suggestions["suggested_next_step_labs_di"]
    assert "not autonomous orders" in suggestions["use_limitation"]


def test_unstructured_oe_output_needs_review():
    suggestions = parse_oe_output("No structure here.", "SYN-X")
    assert suggestions["status"] == "needs_review"
    assert suggestions["safety_flags"]
