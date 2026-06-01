"""Local PHI-like redaction helpers for synthetic and future gated workflows."""

from __future__ import annotations

import re
from dataclasses import dataclass


REDACTION_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("provider", re.compile(r"\bDr\.\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b"), "[PROVIDER]"),
    ("facility", re.compile(r"\b[A-Z][A-Za-z]+\s+(?:University\s+)?(?:Hospital|Medical Center|Clinic|ED|Emergency Department)\b"), "[FACILITY]"),
    ("accession", re.compile(r"\b(?:accession|accession number|acc)\s*[:#]?\s*[A-Z]{2,}[-]?\d{4,}\b", re.I), "[ACCESSION]"),
    ("order_id", re.compile(r"\b(?:order|order id|order number|ord)\s*[:#]?\s*[A-Z]{2,}[-]?\d{4,}\b", re.I), "[ORDER_ID]"),
    ("zip", re.compile(r"\b(?:ZIP|zip code)\s*[:#]?\s*\d{5}(?:-\d{4})?\b"), "[ZIP]"),
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[EMAIL]"),
    ("phone", re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"), "[PHONE]"),
    ("mrn", re.compile(r"\b(?:MRN|Medical Record Number)\s*[:#]?\s*[A-Z0-9-]{5,}\b", re.I), "[MRN]"),
    ("dob", re.compile(r"\b(?:DOB|Date of Birth)\s*[:#]?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", re.I), "[DOB]"),
    ("date", re.compile(r"\b(?:19|20)\d{2}[/-]\d{1,2}[/-]\d{1,2}\b"), "[DATE]"),
    ("date", re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-](?:19|20)?\d{2}\b"), "[DATE]"),
    ("address", re.compile(r"\b\d{2,5}\s+[A-Z][A-Za-z0-9.\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln)\b"), "[ADDRESS]"),
    ("synthetic_name", re.compile(r"\b(?:Jane|John|Wayne|Mary|Robert|Patricia|Michael|William)\s+[A-Z][a-z]+\b"), "[NAME]"),
]


@dataclass(frozen=True)
class RedactionResult:
    redacted_text: str
    findings: dict[str, int]

    @property
    def clean(self) -> bool:
        return sum(self.findings.values()) == 0


def redact_text(text: str) -> RedactionResult:
    """Redact common PHI-like identifiers from local text."""
    findings: dict[str, int] = {}
    redacted = text
    for label, pattern, replacement in REDACTION_PATTERNS:
        redacted, count = pattern.subn(replacement, redacted)
        if count:
            findings[label] = findings.get(label, 0) + count
    return RedactionResult(redacted_text=redacted, findings=findings)


def contains_phi_like_text(text: str) -> bool:
    """Return true when PHI-like tokens remain detectable."""
    return any(pattern.search(text) for _, pattern, _ in REDACTION_PATTERNS)
