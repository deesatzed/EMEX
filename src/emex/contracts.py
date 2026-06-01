"""Data contracts and validation for the EMEX Phase 1 synthetic workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


FORBIDDEN_POST_T0_KEYS = {
    "current_labs",
    "current_lab_results",
    "lab_results",
    "current_imaging",
    "current_imaging_results",
    "imaging_results",
    "ed_course",
    "provider_notes",
    "final_diagnosis",
    "diagnosis",
    "disposition",
    "outcomes",
    "outcome",
    "admission_decision",
    "resulted_orders",
}

REQUIRED_CASE_FIELDS = {
    "case_id",
    "mode",
    "ehr_context",
    "triage",
}

REQUIRED_TRIAGE_FIELDS = {
    "chief_complaint",
    "triage_note",
    "vitals",
    "acuity",
}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


def validate_case_payload(payload: dict[str, Any]) -> ValidationResult:
    """Validate the synthetic first-pilot case input."""
    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED_CASE_FIELDS - set(payload))
    if missing:
        errors.append(f"Missing required top-level fields: {', '.join(missing)}")

    if payload.get("mode") != "synthetic":
        errors.append("Phase 1 runnable milestone only accepts mode='synthetic'")

    triage = payload.get("triage")
    if isinstance(triage, dict):
        triage_missing = sorted(REQUIRED_TRIAGE_FIELDS - set(triage))
        if triage_missing:
            errors.append(f"Missing required triage fields: {', '.join(triage_missing)}")
    elif "triage" in payload:
        errors.append("triage must be an object")

    leakage_paths = find_post_t0_leakage(payload)
    if leakage_paths:
        errors.append(
            "Current-visit post-triage leakage fields are not allowed: "
            + ", ".join(leakage_paths)
        )

    if "ehr_context" in payload and not isinstance(payload["ehr_context"], dict):
        errors.append("ehr_context must be an object")

    if payload.get("source") == "real_ehr":
        errors.append("Real EHR exports are blocked in the first runnable milestone")

    if not payload.get("case_id"):
        errors.append("case_id must be non-empty")

    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)


def find_post_t0_leakage(value: Any, prefix: str = "") -> list[str]:
    """Return dotted paths for current-visit post-triage fields."""
    paths: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else key
            if key in FORBIDDEN_POST_T0_KEYS:
                paths.append(path)
            paths.extend(find_post_t0_leakage(child, path))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            paths.extend(find_post_t0_leakage(child, f"{prefix}[{idx}]"))
    return paths
