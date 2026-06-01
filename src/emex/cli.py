"""Command-line interface for EMEX."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contracts import validate_case_payload
from .workflow import ingest_oe, load_json, prepare_oe, run_demo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="emex")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate-fixture")
    validate.add_argument("--input", required=True, type=Path)

    prep = sub.add_parser("prepare-oe")
    prep.add_argument("--input", required=True, type=Path)
    prep.add_argument("--out", required=True, type=Path)

    ingest = sub.add_parser("ingest-oe")
    ingest.add_argument("--case", required=True, type=Path)
    ingest.add_argument("--oe-output", required=True, type=Path)
    ingest.add_argument("--out", required=True, type=Path)

    demo = sub.add_parser("run-demo")
    demo.add_argument("--input", required=True, type=Path)
    demo.add_argument("--oe-output", required=True, type=Path)
    demo.add_argument("--out", required=True, type=Path)

    args = parser.parse_args(argv)

    if args.command == "validate-fixture":
        result = validate_case_payload(load_json(args.input))
        print(json.dumps(result.__dict__, indent=2))
        return 0 if result.valid else 1
    if args.command == "prepare-oe":
        packet = prepare_oe(args.input, args.out)
        print(f"Prepared OE packet for {packet['case_id']} at {args.out}")
        return 0 if packet["valid"] else 1
    if args.command == "ingest-oe":
        suggestions = ingest_oe(args.case, args.oe_output, args.out)
        print(f"Parsed OE output for {suggestions['case_id']} with status={suggestions['status']}")
        return 0 if suggestions["status"] in {"clinician_draft", "needs_review"} else 1
    if args.command == "run-demo":
        result = run_demo(args.input, args.oe_output, args.out)
        print(
            f"Demo complete for {result['packet']['case_id']} "
            f"with status={result['suggestions']['status']} at {args.out}"
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
