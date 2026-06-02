from pathlib import Path


REQUIRED_DOTFLOWS = [
    "ed_shadow_recommender.md",
    "order_appropriateness_review.md",
    "risk_resource_forecast.md",
    "cost_restraint_review.md",
    "discordance_review.md",
]

REQUIRED_SCHEMA_KEYS = [
    "risk_bucket",
    "suggested_order_considerations",
    "resource_forecast",
    "cost_restraint_cautions",
    "missing_information",
    "evidence_notes",
    "safety_flags",
]

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Provided Input",
    "## Step 1",
    "## Step 2",
    "## Step 3",
    "## Evidence Rules",
    "## Privacy Rules",
    "## Forbidden Output",
    "## Expected Output Schema",
    "## Final Quality Check",
]

FORBIDDEN_PROMPT_PATTERNS = [
    "tree of thought",
    "write down",
    "life on the line",
    "patient instructions",
]


def test_required_dotflows_exist_and_name_emex_schema():
    for name in REQUIRED_DOTFLOWS:
        text = Path("dotflows", name).read_text()
        assert "EMEX" in text
        assert "clinician-draft" in text.lower()
        assert "insufficient_information" in text
        assert "```json" in text
        for key in REQUIRED_SCHEMA_KEYS:
            assert key in text
        for section in REQUIRED_SECTIONS:
            assert section in text


def test_dotflows_preserve_emex_safety_boundaries():
    for name in REQUIRED_DOTFLOWS:
        text = Path("dotflows", name).read_text()
        lower = text.lower()
        assert "do not reproduce direct identifiers" in lower
        assert "do not request raw phi" in lower
        assert "do not use post-t0" in lower or name == "discordance_review.md"
        assert "hidden chain-of-thought" in lower
        for pattern in FORBIDDEN_PROMPT_PATTERNS:
            assert pattern not in lower.replace("- patient instructions.", "")


def test_dotflow_readme_maps_required_files_to_workflows():
    text = Path("dotflows", "README.md").read_text()
    for name in REQUIRED_DOTFLOWS:
        assert name in text
    for key in REQUIRED_SCHEMA_KEYS:
        assert key in text
