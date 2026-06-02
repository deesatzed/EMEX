from pathlib import Path


REQUIRED_DOTFLOWS = [
    "ed_shadow_recommender.md",
    "order_appropriateness_review.md",
    "risk_resource_forecast.md",
    "cost_restraint_review.md",
    "discordance_review.md",
]

REQUIRED_PLAIN_TEXT_LABELS = [
    "RISK_BUCKET:",
    "SUGGESTED_ORDER_CONSIDERATIONS:",
    "RESOURCE_FORECAST:",
    "COST_RESTRAINT_CAUTIONS:",
    "MISSING_INFORMATION:",
    "EVIDENCE_NOTES:",
    "SAFETY_FLAGS:",
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
    "## Expected Plain Text Output",
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
        assert "```json" not in text
        assert "Do not return JSON" in text
        assert "Do not use code fences" in text
        for label in REQUIRED_PLAIN_TEXT_LABELS:
            assert label in text
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
    for label in REQUIRED_PLAIN_TEXT_LABELS:
        assert label in text
