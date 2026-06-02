"""Parse manually pasted OpenEvidence output into EMEX clinician-draft suggestions."""

from __future__ import annotations

import json
import re
from typing import Any

from .hashing import hash_text


JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)
ALLOWED_TRIAGE_CATEGORIES = {
    "immediate_acute_critical_care_provider_eval",
    "provider_eval_with_labs_di_plan",
    "structured_outpatient_or_telehealth_review",
    "hybrid_labs_di_then_outpatient_review",
    "insufficient_information",
}
UNSAFE_IMPERATIVE_RE = re.compile(
    r"^\s*(order|discharge|admit|prescribe|administer|give|send\s+home|route)\b",
    re.I,
)


def parse_oe_output(text: str, case_id: str) -> dict[str, Any]:
    """Parse OE output. Prefer plain text labels; keep fenced JSON as a legacy fallback."""
    parsed: dict[str, Any] | None = None
    parse_warnings: list[str] = []

    parsed = _parse_plain_text_sections(text)
    if _has_minimum_structure(parsed):
        parse_warnings.append("Parsed plain text labeled OE output")

    if not _has_minimum_structure(parsed):
        parsed = None

    match = JSON_BLOCK_RE.search(text)
    if parsed is None and match:
        try:
            parsed = json.loads(match.group(1))
            parse_warnings.append("Parsed legacy fenced JSON OE output")
        except json.JSONDecodeError as exc:
            parse_warnings.append(f"Fenced JSON could not be parsed: {exc}")

    if parsed is None:
        parsed = _parse_markdown_fallback(text)
        parse_warnings.append("Used conservative Markdown fallback parser; clinician review required")

    unsafe_phrases = _unsafe_order_or_disposition_phrases(parsed)
    unknown_category = _has_unknown_triage_category(parsed)
    status = (
        "clinician_draft"
        if _has_minimum_structure(parsed) and not unsafe_phrases and not unknown_category
        else "needs_review"
    )
    suggestions = {
        "schema_version": "emex.structured_suggestions.v0.1",
        "case_id": case_id,
        "status": status,
        "use_limitation": (
            "Clinician draft for PI review and clinician review only. Not patient-facing, "
            "not autonomous orders, diagnosis, disposition, or routing."
        ),
        "next_step_triage_category": parsed.get("next_step_triage_category", "insufficient_information"),
        "triage_rationale": parsed.get("triage_rationale", []),
        "suggested_next_step_labs_di": parsed.get("suggested_next_step_labs_di", []),
        "suggested_provider_eval": parsed.get("suggested_provider_eval", []),
        "outpatient_or_telehealth_considerations": parsed.get(
            "outpatient_or_telehealth_considerations", []
        ),
        "hybrid_pathway_considerations": parsed.get("hybrid_pathway_considerations", []),
        "risk_bucket": parsed.get("risk_bucket", "insufficient_information"),
        "suggested_order_considerations": parsed.get("suggested_order_considerations", []),
        "resource_forecast": parsed.get("resource_forecast", []),
        "cost_restraint_cautions": parsed.get("cost_restraint_cautions", []),
        "missing_information": parsed.get("missing_information", []),
        "evidence_notes": parsed.get("evidence_notes", []),
        "safety_flags": parsed.get("safety_flags", []),
        "parse_warnings": parse_warnings,
        "oe_output_hash": hash_text(text),
    }
    if suggestions["status"] == "needs_review":
        suggestions["safety_flags"].append("OE output lacked minimum expected structure")
    if unknown_category:
        suggestions["safety_flags"].append("Unknown next-step triage category")
    if unsafe_phrases:
        suggestions["safety_flags"].append(
            "OE output contained order/disposition imperative language requiring clinician review"
        )
        suggestions["unsafe_phrases"] = unsafe_phrases
    return suggestions


def _has_minimum_structure(parsed: dict[str, Any]) -> bool:
    has_triage_synthesis = (
        parsed.get("next_step_triage_category") not in {None, "", "insufficient_information"}
        and isinstance(parsed.get("suggested_next_step_labs_di", []), list)
        and bool(parsed.get("suggested_next_step_labs_di", []))
        and isinstance(parsed.get("suggested_provider_eval", []), list)
        and bool(parsed.get("suggested_provider_eval", []))
    )
    has_legacy_structure = (
        parsed.get("risk_bucket") not in {None, "", "insufficient_information"}
        and isinstance(parsed.get("suggested_order_considerations", []), list)
        and bool(parsed.get("suggested_order_considerations", []))
    )
    return has_triage_synthesis or has_legacy_structure


def _parse_markdown_fallback(text: str) -> dict[str, Any]:
    sections: dict[str, list[str]] = {}
    current = "notes"
    sections[current] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            current = stripped.strip("# ").lower().replace(" ", "_").replace("/", "_")
            sections.setdefault(current, [])
            continue
        if stripped.startswith("-"):
            sections.setdefault(current, []).append(stripped.lstrip("- ").strip())

    return {
        "next_step_triage_category": _first_value(sections, ["next_step_triage_category"]),
        "triage_rationale": _values(sections, ["triage_rationale"]),
        "suggested_next_step_labs_di": _values(sections, ["suggested_next_step_labs_di"]),
        "suggested_provider_eval": _values(sections, ["suggested_provider_eval"]),
        "outpatient_or_telehealth_considerations": _values(
            sections, ["outpatient_or_telehealth_considerations"]
        ),
        "hybrid_pathway_considerations": _values(sections, ["hybrid_pathway_considerations"]),
        "risk_bucket": _first_value(sections, ["risk_bucket", "risk"]),
        "suggested_order_considerations": _values(sections, ["suggested_order_considerations", "orders"]),
        "resource_forecast": _values(sections, ["resource_forecast", "resources"]),
        "cost_restraint_cautions": _values(sections, ["cost_restraint_cautions", "cost_restraint"]),
        "missing_information": _values(sections, ["missing_information", "missing"]),
        "evidence_notes": _values(sections, ["evidence_notes", "evidence"]),
        "safety_flags": _values(sections, ["safety_flags", "safety"]),
    }


def _parse_plain_text_sections(text: str) -> dict[str, Any]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    label_aliases = {
        "RISK_BUCKET": "risk_bucket",
        "RISK": "risk_bucket",
        "NEXT_STEP_TRIAGE_CATEGORY": "next_step_triage_category",
        "TRIAGE_RATIONALE": "triage_rationale",
        "SUGGESTED_NEXT_STEP_LABS_DI": "suggested_next_step_labs_di",
        "SUGGESTED_PROVIDER_EVAL": "suggested_provider_eval",
        "OUTPATIENT_OR_TELEHEALTH_CONSIDERATIONS": "outpatient_or_telehealth_considerations",
        "HYBRID_PATHWAY_CONSIDERATIONS": "hybrid_pathway_considerations",
        "SUGGESTED_ORDER_CONSIDERATIONS": "suggested_order_considerations",
        "ORDER_CONSIDERATIONS": "suggested_order_considerations",
        "RESOURCE_FORECAST": "resource_forecast",
        "COST_RESTRAINT_CAUTIONS": "cost_restraint_cautions",
        "COST_RESTRAINT": "cost_restraint_cautions",
        "MISSING_INFORMATION": "missing_information",
        "EVIDENCE_NOTES": "evidence_notes",
        "SAFETY_FLAGS": "safety_flags",
    }
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        label_match = re.match(r"^([A-Z][A-Z0-9_ ]{2,}):\s*(.*)$", stripped)
        if label_match:
            raw_label, value = label_match.groups()
            key = label_aliases.get(raw_label.replace(" ", "_"))
            if key:
                current = key
                sections.setdefault(current, [])
                if value:
                    sections[current].append(value.strip())
                continue
        if current and stripped.startswith(("-", "*")):
            sections.setdefault(current, []).append(stripped.lstrip("-* ").strip())

    return {
        "next_step_triage_category": _first_value(sections, ["next_step_triage_category"]),
        "triage_rationale": sections.get("triage_rationale", []),
        "suggested_next_step_labs_di": sections.get("suggested_next_step_labs_di", []),
        "suggested_provider_eval": sections.get("suggested_provider_eval", []),
        "outpatient_or_telehealth_considerations": sections.get(
            "outpatient_or_telehealth_considerations", []
        ),
        "hybrid_pathway_considerations": sections.get("hybrid_pathway_considerations", []),
        "risk_bucket": _first_value(sections, ["risk_bucket"]),
        "suggested_order_considerations": sections.get("suggested_order_considerations", []),
        "resource_forecast": sections.get("resource_forecast", []),
        "cost_restraint_cautions": sections.get("cost_restraint_cautions", []),
        "missing_information": sections.get("missing_information", []),
        "evidence_notes": sections.get("evidence_notes", []),
        "safety_flags": sections.get("safety_flags", []),
    }


def _unsafe_order_or_disposition_phrases(parsed: dict[str, Any]) -> list[str]:
    phrases: list[str] = []
    for key in (
        "suggested_order_considerations",
        "resource_forecast",
        "suggested_next_step_labs_di",
        "suggested_provider_eval",
        "outpatient_or_telehealth_considerations",
        "hybrid_pathway_considerations",
        "safety_flags",
    ):
        values = parsed.get(key, [])
        if not isinstance(values, list):
            continue
        for value in values:
            text = str(value)
            if UNSAFE_IMPERATIVE_RE.search(text):
                phrases.append(text)
    return phrases


def _has_unknown_triage_category(parsed: dict[str, Any]) -> bool:
    category = parsed.get("next_step_triage_category")
    return bool(category) and category not in ALLOWED_TRIAGE_CATEGORIES


def _values(sections: dict[str, list[str]], names: list[str]) -> list[str]:
    for name in names:
        if sections.get(name):
            return sections[name]
    return []


def _first_value(sections: dict[str, list[str]], names: list[str]) -> str:
    values = _values(sections, names)
    return values[0] if values else "insufficient_information"
