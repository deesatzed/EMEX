# Triage Synthesis Gap Plan Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert EMEX from generic OE parsing into a provider-facing next-step triage synthesis workflow.

**Architecture:** Keep the Phase 1 manual OE round trip: local intake/redaction, manual OE companion use, manually pasted OE output, then local parsing and artifact generation. Add a triage synthesis data contract on top of the existing plain-text parser so the final output maps to actionable clinician-draft triage categories without autonomous orders, diagnoses, or disposition.

**Tech Stack:** Python stdlib package, pytest, static HTML/CSS/JavaScript, Markdown DotFlow prompts.

---

## Gap Register

| Gap | Current State | Required State | Implementation Target |
| --- | --- | --- | --- |
| Login | On hold, no auth | Keep explicitly on hold during dev | Document only; no auth implementation |
| Clinical intake | GUI accepts text/JSON and prepares OE packet | Provider understands triage-complete-only input boundary | Keep current behavior; strengthen instructions if needed |
| Redaction | Local redaction/leakage reports exist | Continue local redaction before OE copy | Preserve current checks |
| OE handoff | Plain-text packet plus DotFlow sequence exists | DotFlow must ask for next-step triage fields | Update DotFlows and OE packet output request |
| OE output parsing | Parses `risk_bucket`, order/resource/cost fields | Parse next-step triage category and pathway-specific fields | Update parser and tests |
| Final synthesis | Report/web output shows risk/order/resource/cost | Show next-step triage category, rationale, labs/DI, provider eval, outpatient/telehealth, hybrid considerations | Update reporting and web UI |
| Output taxonomy | No explicit category enum | Four pilot categories plus insufficient information | Add field validation and tests |
| Demo fixture | OE output is generic risk/order/resource/cost | Plain-text OE output uses triage synthesis labels | Update synthetic fixture |

## Target Triage Categories

- `immediate_acute_critical_care_provider_eval`
- `provider_eval_with_labs_di_plan`
- `structured_outpatient_or_telehealth_review`
- `hybrid_labs_di_then_outpatient_review`
- `insufficient_information`

## Target Plain Text OE Labels

OE DotFlows should return plain text with these labels:

- `NEXT_STEP_TRIAGE_CATEGORY:`
- `TRIAGE_RATIONALE:`
- `SUGGESTED_NEXT_STEP_LABS_DI:`
- `SUGGESTED_PROVIDER_EVAL:`
- `OUTPATIENT_OR_TELEHEALTH_CONSIDERATIONS:`
- `HYBRID_PATHWAY_CONSIDERATIONS:`
- `MISSING_INFORMATION:`
- `EVIDENCE_NOTES:`
- `SAFETY_FLAGS:`

## Task 1: Parser Contract

**Files:**
- Modify: `tests/test_oe_output.py`
- Modify: `src/emex/oe_output.py`

**Step 1: Write failing tests**

Add tests that a plain-text OE output with the target labels returns:
- `next_step_triage_category`
- `triage_rationale`
- `suggested_next_step_labs_di`
- `suggested_provider_eval`
- `outpatient_or_telehealth_considerations`
- `hybrid_pathway_considerations`

Add a test that an unknown triage category becomes `needs_review`.

**Step 2: Implement parser changes**

Extend the label map and output object. Keep legacy fields for compatibility.

## Task 2: DotFlow and Packet Contract

**Files:**
- Modify: `dotflows/*.md`
- Modify: `dotflows/README.md`
- Modify: `src/emex/oe_packet.py`
- Modify: `tests/test_dotflows.py`
- Modify: `tests/test_redaction_packet.py`

**Step 1: Write failing tests**

Require target triage labels in every DotFlow and packet request.

**Step 2: Update prompts**

Replace generic output labels with next-step triage labels.

## Task 3: Artifacts and Reports

**Files:**
- Modify: `tests/test_workflow.py`
- Modify: `src/emex/reporting.py`
- Modify: `fixtures/oe_outputs/chest_pain_oe_output.md`

**Step 1: Write failing tests**

Assert `structured_suggestions.json`, `report.html`, and `PI_SUMMARY.md` contain the new triage synthesis fields.

**Step 2: Update reporting**

Render next-step triage category, rationale, labs/DI, provider eval, outpatient/telehealth, and hybrid considerations.

## Task 4: Web UX

**Files:**
- Modify: `tests/test_static_web.py`
- Modify: `web/index.html`

**Step 1: Write failing tests**

Assert the static page contains the new labels and output section names.

**Step 2: Update web parser/display**

Parse and display the target labels in the GUI.

## Task 5: Docs and Verification

**Files:**
- Modify: `GOAL.md`
- Modify: `README.md`

**Step 1: Update docs**

Document the exact seven-step workflow and final triage synthesis categories.

**Step 2: Verify**

Run:

```bash
pytest -q
node -e "const fs=require('fs'); const html=fs.readFileSync('web/index.html','utf8'); const m=html.match(/<script>([\\s\\S]*)<\\/script>/); if(!m) throw new Error('script not found'); new Function(m[1]); console.log('inline-script-parse-ok');"
python -m emex.cli run-demo --input fixtures/synthetic_ed/chest_pain_t0.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/final_demo
```

Expected:
- All tests pass.
- Inline JS parses.
- Demo status is `clinician_draft`.
