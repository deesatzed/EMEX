from pathlib import Path


def test_static_web_declares_demo_only_and_cli_authority():
    html = Path("web/index.html").read_text()

    assert "Workflow demo only" in html
    assert "CLI/backend artifact path is authoritative" in html
    assert "would not emit copy-ready OE input" in html
    assert "Provider Workflow" in html
    assert "1. Load Clinical Information" in html
    assert "narrative text" in html
    assert "2. Prepare OE" in html
    assert "3. Copy Redacted OE Input" in html
    assert "4. Paste OE Output" in html
    assert "5. Parse OE" in html
    assert "First: ed_shadow_recommender" in html
    assert "Second: order_appropriateness_review" in html
    assert "Third: risk_resource_forecast" in html
    assert "Fourth: cost_restraint_review" in html
    assert "Last: discordance_review" in html
    assert "Copy OE Input" in html
    assert "Copy Parsed Output" in html
    assert "Parsed Structured Data" in html
    assert "parsePlainTextOe" in html
    assert "OE output lacks parseable plain text labels" in html
    assert "OE output lacks parseable fenced JSON" not in html
    assert "SUGGESTED_ORDER_CONSIDERATIONS:" in html
    assert "OE Companion Mode" in html
    assert "Open OpenEvidence" in html
    assert "Use browser split view or two side-by-side windows" in html
    assert "Do not embed OpenEvidence" in html
    assert 'target="_blank"' in html
    assert "inputToRenderableText" in html
    assert "Free Text Clinical Context" in html
    assert "invalid json" not in html.lower()
    assert "forbiddenTextPatterns" in html
