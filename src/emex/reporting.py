"""Artifact rendering for EMEX demo runs."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def render_html_report(packet: dict[str, Any], suggestions: dict[str, Any]) -> str:
    orders = "".join(f"<li>{html.escape(str(item))}</li>" for item in suggestions["suggested_order_considerations"])
    resources = "".join(f"<li>{html.escape(str(item))}</li>" for item in suggestions["resource_forecast"])
    cautions = "".join(f"<li>{html.escape(str(item))}</li>" for item in suggestions["cost_restraint_cautions"])
    missing = "".join(f"<li>{html.escape(str(item))}</li>" for item in suggestions["missing_information"])
    flags = "".join(f"<li>{html.escape(str(item))}</li>" for item in suggestions["safety_flags"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>EMEX Shadow Report - {html.escape(packet.get('case_id', 'unknown'))}</title>
  <style>
    body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif; margin: 32px; color: #17202a; }}
    main {{ max-width: 980px; margin: 0 auto; }}
    section {{ border-top: 1px solid #ccd3da; padding: 18px 0; }}
    code, pre {{ background: #f4f6f8; padding: 2px 4px; }}
    .badge {{ display: inline-block; padding: 4px 8px; border-radius: 6px; background: #e8eef5; font-weight: 700; }}
    .warning {{ border-left: 4px solid #a33; padding-left: 12px; }}
  </style>
</head>
<body>
<main>
  <h1>EMEX Shadow Report</h1>
  <p><span class="badge">{html.escape(suggestions.get('status', 'unknown'))}</span></p>
  <section class="warning">
    <strong>Use limitation:</strong> {html.escape(suggestions.get('use_limitation', ''))}
  </section>
  <section>
    <h2>Case</h2>
    <p><strong>Case ID:</strong> {html.escape(packet.get('case_id', ''))}</p>
    <p><strong>Raw hash:</strong> <code>{html.escape(packet.get('raw_input_hash', ''))}</code></p>
    <p><strong>Redacted packet hash:</strong> <code>{html.escape(packet.get('redacted_packet_hash', ''))}</code></p>
  </section>
  <section>
    <h2>Risk Bucket</h2>
    <p>{html.escape(str(suggestions.get('risk_bucket', 'insufficient_information')))}</p>
  </section>
  <section><h2>Suggested Order Considerations</h2><ul>{orders}</ul></section>
  <section><h2>Resource Forecast</h2><ul>{resources}</ul></section>
  <section><h2>Cost / Restraint Cautions</h2><ul>{cautions}</ul></section>
  <section><h2>Missing Information</h2><ul>{missing}</ul></section>
  <section><h2>Safety Flags</h2><ul>{flags}</ul></section>
</main>
</body>
</html>
"""


def render_pi_summary(packet: dict[str, Any], suggestions: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# EMEX PI Summary",
            "",
            f"- Case ID: `{packet.get('case_id', '')}`",
            f"- Output status: `{suggestions.get('status', '')}`",
            f"- Risk bucket: `{suggestions.get('risk_bucket', '')}`",
            "- Use limitation: clinician draft for PI review and clinician review only.",
            f"- Redaction findings: `{packet.get('phi_redaction_report', {}).get('findings', {})}`",
            f"- Leakage errors: `{packet.get('leakage_report', {}).get('errors', [])}`",
            f"- OE output hash: `{suggestions.get('oe_output_hash', '')}`",
            "",
            "## Remaining Risks",
            "",
            "- Synthetic fixture only; no real PHI approval is implied.",
            "- OE output is manually pasted and must be clinician-reviewed.",
            "- No Epic/EHR integration exists in Phase 1.",
        ]
    )
