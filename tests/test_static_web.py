from pathlib import Path


def test_static_web_declares_demo_only_and_cli_authority():
    html = Path("web/index.html").read_text()

    assert "Workflow demo only" in html
    assert "CLI/backend artifact path is authoritative" in html
    assert "would not emit copy-ready OE input" in html
