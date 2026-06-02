# OE Companion Mode Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a provider-facing companion mode that helps users run OpenEvidence alongside EMEX without embedding, automating, or reading OE.

**Architecture:** Keep EMEX as a static local workflow page. Add an external OE launch button, explicit split-view/window-snapping guidance, and tests that preserve the non-embedding boundary. No API calls, iframe, or cross-site scripting are added.

**Tech Stack:** Static HTML/CSS/JavaScript, pytest static assertions, README documentation.

---

### Task 1: Add Static Web Regression Coverage

**Files:**
- Modify: `tests/test_static_web.py`

**Step 1: Write the failing test**

Add assertions that `web/index.html` contains:
- `OE Companion Mode`
- `Open OpenEvidence`
- `Use browser split view or two side-by-side windows`
- `Do not embed OpenEvidence`
- `target="_blank"`

**Step 2: Run test to verify it fails**

Run: `pytest -q tests/test_static_web.py`

Expected before implementation: failure on missing companion-mode strings.

### Task 2: Add OE Companion UI

**Files:**
- Modify: `web/index.html`

**Step 1: Add companion panel**

Add a top workflow panel explaining:
- Authenticate into OE separately.
- Click `Open OpenEvidence` to open OE in a new tab/window.
- Use browser split view or two side-by-side windows.
- Copy redacted EMEX packet into OE.
- Paste OE result back into EMEX.
- EMEX does not embed OE, read OE, or automate OE.

**Step 2: Add external link button**

Add:

```html
<a class="button primary" href="https://www.openevidence.com/" target="_blank" rel="noopener noreferrer">Open OpenEvidence</a>
```

Style links with the existing button styling.

### Task 3: Update README

**Files:**
- Modify: `README.md`

Add OE Companion Mode usage under Local Web UX:
- Open/login to OE separately.
- Open EMEX.
- Put both pages side-by-side.
- Keep manual copy/paste; no iframe or direct integration.

### Task 4: Verify

Run:

```bash
pytest -q
node -e "const fs=require('fs'); const html=fs.readFileSync('web/index.html','utf8'); const m=html.match(/<script>([\\s\\S]*)<\\/script>/); if(!m) throw new Error('script not found'); new Function(m[1]); console.log('inline-script-parse-ok');"
python -m emex.cli run-demo --input fixtures/synthetic_ed/chest_pain_t0.json --oe-output fixtures/oe_outputs/chest_pain_oe_output.md --out artifacts/final_demo
```

Expected:
- pytest exits 0.
- inline script parses.
- CLI demo completes with `status=clinician_draft`.

### Task 5: Commit and Push

Run:

```bash
git add README.md web/index.html tests/test_static_web.py docs/plans/2026-06-02-oe-companion-mode.md
git commit -m "Add OE companion mode"
git push
```
