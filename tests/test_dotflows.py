from pathlib import Path


def test_required_dotflows_exist_and_name_emex_schema():
    required = [
        "ed_shadow_recommender.md",
        "order_appropriateness_review.md",
        "risk_resource_forecast.md",
        "cost_restraint_review.md",
        "discordance_review.md",
    ]
    for name in required:
        text = Path("dotflows", name).read_text()
        assert "EMEX" in text
        assert "clinician-draft" in text.lower()
        assert "insufficient_information" in text
