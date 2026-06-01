from pathlib import Path

from emex.contracts import validate_case_payload
from emex.workflow import load_json


FIXTURES = Path("fixtures/synthetic_ed")


def test_valid_synthetic_fixture_passes():
    result = validate_case_payload(load_json(FIXTURES / "chest_pain_t0.json"))
    assert result.valid
    assert result.errors == []


def test_rejects_post_t0_current_labs():
    result = validate_case_payload(load_json(FIXTURES / "leaky_current_results.json"))
    assert not result.valid
    assert any("current_labs" in err for err in result.errors)


def test_rejects_non_synthetic_mode():
    payload = load_json(FIXTURES / "chest_pain_t0.json")
    payload["mode"] = "real_phi"
    result = validate_case_payload(payload)
    assert not result.valid
    assert "mode='synthetic'" in " ".join(result.errors)
