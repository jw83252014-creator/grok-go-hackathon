#!/usr/bin/env python3
"""Emit a minimal Grok Go hackathon receipt JSON artifact.

This is the tiny receipt-first emitter: no network, no third-party deps, no
claims beyond what the caller passes in. It creates a schema-shaped receipt and
performs a lightweight built-in validation against the local hackathon receipt
contract.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from datetime import datetime, timezone
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_RECEIPTS_DIR = ROOT / "receipts"
VALID_STATUSES = {
    "completed_with_receipt",
    "prepared_not_submitted",
    "blocked",
    "failed",
    "needs_review",
}
VALID_GATES = {"do_not_submit", "submit_after_human_review", "submit_allowed"}
VALID_CONFIDENCE = {"low", "medium", "high"}
RECEIPT_ID_RE = re.compile(r"^[a-zA-Z0-9._:-]+$")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._:-]+", "-", value.strip().lower()).strip("-")
    return slug[:80] or "receipt"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Emit a minimal receipt JSON file.")
    ap.add_argument("--agent", default="null", help="agent_id/cell producing the receipt")
    ap.add_argument("--task", required=True, help="Plain-English task/outcome being receipted")
    ap.add_argument("--status", default="completed_with_receipt", choices=sorted(VALID_STATUSES))
    ap.add_argument("--artifact", action="append", default=[], help="Path/URL/commit/ref; repeatable")
    ap.add_argument("--passed", action="append", default=[], help="Verification check that passed; repeatable")
    ap.add_argument("--failed", action="append", default=[], help="Verification check that failed; repeatable")
    ap.add_argument("--unverified", action="append", default=[], help="Explicit unverified claim/caveat; repeatable")
    ap.add_argument("--confidence", default="medium", choices=sorted(VALID_CONFIDENCE))
    ap.add_argument("--gate", default="submit_after_human_review", choices=sorted(VALID_GATES))
    ap.add_argument("--note", action="append", default=[], help="Optional note; repeatable")
    ap.add_argument("--receipt-id", help="Override generated receipt_id")
    ap.add_argument("--out", help="Output path. Defaults to receipts/<receipt_id>.receipt.json")
    ap.add_argument("--stdout", action="store_true", help="Also print JSON to stdout")
    return ap.parse_args()


def build_receipt(args: argparse.Namespace) -> dict[str, Any]:
    now = utc_now()
    rid = args.receipt_id or f"{now[:10]}-{args.agent}-{slugify(args.task)}"
    receipt = {
        "schema_version": "1.0",
        "receipt_id": rid,
        "created_at": now,
        "agent_id": args.agent,
        "task": args.task,
        "status": args.status,
        "artifact_refs": args.artifact,
        "verification": {
            "checks_passed": args.passed,
            "checks_failed": args.failed,
            "unverified_claims": args.unverified,
            "confidence": args.confidence,
        },
        "promotion_gate": args.gate,
    }
    if args.note:
        receipt["notes"] = args.note
    return receipt


def validate_minimal(receipt: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "schema_version",
        "receipt_id",
        "created_at",
        "agent_id",
        "task",
        "status",
        "artifact_refs",
        "verification",
        "promotion_gate",
    ]
    for key in required:
        if key not in receipt:
            errors.append(f"missing required key: {key}")
    if receipt.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if not isinstance(receipt.get("receipt_id"), str) or not RECEIPT_ID_RE.match(receipt["receipt_id"]):
        errors.append("receipt_id must match ^[a-zA-Z0-9._:-]+$")
    if receipt.get("status") not in VALID_STATUSES:
        errors.append(f"status must be one of {sorted(VALID_STATUSES)}")
    if receipt.get("promotion_gate") not in VALID_GATES:
        errors.append(f"promotion_gate must be one of {sorted(VALID_GATES)}")
    if not isinstance(receipt.get("artifact_refs"), list):
        errors.append("artifact_refs must be a list")
    verification = receipt.get("verification")
    if not isinstance(verification, dict):
        errors.append("verification must be an object")
    else:
        for key in ["checks_passed", "checks_failed", "unverified_claims"]:
            if not isinstance(verification.get(key), list):
                errors.append(f"verification.{key} must be a list")
        if verification.get("confidence") not in VALID_CONFIDENCE:
            errors.append(f"verification.confidence must be one of {sorted(VALID_CONFIDENCE)}")
    return errors


def main() -> int:
    args = parse_args()
    receipt = build_receipt(args)
    errors = validate_minimal(receipt)
    if errors:
        for err in errors:
            print(f"validation-error: {err}", file=sys.stderr)
        return 2

    out = pathlib.Path(args.out) if args.out else DEFAULT_RECEIPTS_DIR / f"{receipt['receipt_id']}.receipt.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2) + "\n")

    if args.stdout:
        print(json.dumps(receipt, indent=2))
    else:
        print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
