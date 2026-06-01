"""Parse manually pasted OpenEvidence output into EMEX clinician-draft suggestions."""

from __future__ import annotations

import json
import re
from typing import Any

from .hashing import hash_text


JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)
UNSAFE_IMPERATIVE_RE = re.compile(
    r"^\s*(order|discharge|admit|prescribe|administer|give|send\s+home|route)\b",
    re.I,
)


def parse_oe_output(text: str, case_id: str) -> dict[str, Any]:
    """Parse OE output. Prefer fenced JSON; fall back to conservative Markdown extraction."""
    parsed: dict[str, Any] | None = None
    match = JSON_BLOCK_RE.search(text)
    parse_warnings: list[str] = []
    if match:
        try:
            parsed = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            parse_warnings.append(f"Fenced JSON could not be parsed: {exc}")

    if parsed is None:
        parsed = _parse_markdown_fallback(text)
        parse_warnings.append("Used conservative Markdown fallback parser; clinician review required")

    unsafe_phrases = _unsafe_order_or_disposition_phrases(parsed)
    status = "clinician_draft" if _has_minimum_structure(parsed) and not unsafe_phrases else "needs_review"
    suggestions = {
        "schema_version": "emex.structured_suggestions.v0.1",
        "case_id": case_id,
        "status": status,
        "use_limitation": (
            "Clinician draft for PI review and clinician review only. Not patient-facing, "
            "not autonomous orders, diagnosis, disposition, or routing."
        ),
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
    if unsafe_phrases:
        suggestions["safety_flags"].append(
            "OE output contained order/disposition imperative language requiring clinician review"
        )
        suggestions["unsafe_phrases"] = unsafe_phrases
    return suggestions


def _has_minimum_structure(parsed: dict[str, Any]) -> bool:
    return (
        parsed.get("risk_bucket") not in {None, "", "insufficient_information"}
        and isinstance(parsed.get("suggested_order_considerations", []), list)
        and bool(parsed.get("suggested_order_considerations", []))
    )


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
        "risk_bucket": _first_value(sections, ["risk_bucket", "risk"]),
        "suggested_order_considerations": _values(sections, ["suggested_order_considerations", "orders"]),
        "resource_forecast": _values(sections, ["resource_forecast", "resources"]),
        "cost_restraint_cautions": _values(sections, ["cost_restraint_cautions", "cost_restraint"]),
        "missing_information": _values(sections, ["missing_information", "missing"]),
        "evidence_notes": _values(sections, ["evidence_notes", "evidence"]),
        "safety_flags": _values(sections, ["safety_flags", "safety"]),
    }


def _unsafe_order_or_disposition_phrases(parsed: dict[str, Any]) -> list[str]:
    phrases: list[str] = []
    for key in ("suggested_order_considerations", "resource_forecast", "safety_flags"):
        values = parsed.get(key, [])
        if not isinstance(values, list):
            continue
        for value in values:
            text = str(value)
            if UNSAFE_IMPERATIVE_RE.search(text):
                phrases.append(text)
    return phrases


def _values(sections: dict[str, list[str]], names: list[str]) -> list[str]:
    for name in names:
        if sections.get(name):
            return sections[name]
    return []


def _first_value(sections: dict[str, list[str]], names: list[str]) -> str:
    values = _values(sections, names)
    return values[0] if values else "insufficient_information"
