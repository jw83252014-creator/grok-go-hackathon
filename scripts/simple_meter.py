#!/usr/bin/env python3
"""Simple readiness meter for the Grok Go / Living Dashboard Nous package.

No network dependencies. It checks local files and emits a receipt-shaped JSON meter
plus a human-readable score. Use --json for machine output only.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHECKS = [
    ("submission", ROOT / "SUBMISSION.md", 2.0),
    ("null_scorecard", ROOT / "NULL-SUBMISSION-SCORECARD-2026-06-29.md", 1.0),
    ("hackathon_receipt_schema", ROOT / "schemas" / "hackathon-receipt.schema.json", 1.0),
    ("agent_resume_schema", ROOT / "schemas" / "agent-resume.schema.json", 1.0),
    ("jade_agent_resume", ROOT / "examples" / "jade.agent-resume.json", 0.5),
    ("conscious_layer_reference_image", ROOT / "assets" / "conscious-layer-girl-reference.jpg", 0.75),
    ("conscious_layer_reference_note", ROOT / "assets" / "conscious-layer-girl-reference.md", 0.25),
    ("living_dashboard_html", ROOT / "living-dashboard.html", 1.0),
    ("audit_receipt", ROOT / "receipts" / "2026-06-29-null-submission-scorecard.receipt.json", 1.0),
    ("agent_resume_receipt", ROOT / "receipts" / "2026-06-29-agent-resume-schema.receipt.json", 0.5),
]


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "not-a-git-repo-or-unavailable"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="print machine JSON only")
    args = ap.parse_args()

    total = sum(weight for _, _, weight in CHECKS)
    passed = []
    failed = []
    score = 0.0
    for name, path, weight in CHECKS:
        if path.exists() and path.stat().st_size > 0:
            passed.append(f"{name}: {path}")
            score += weight
        else:
            failed.append(f"{name}: missing-or-empty {path}")

    pct = round((score / total) * 100, 1)
    readiness = round((score / total) * 10, 1)
    if readiness >= 8.5 and not failed:
        gate = "submit_allowed"
    elif readiness >= 7.0:
        gate = "submit_after_human_review"
    else:
        gate = "do_not_submit"

    receipt = {
        "schema_version": "1.0",
        "receipt_id": "simple-meter-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "agent_id": "null",
        "task": "Compute local readiness meter for Nous hackathon submission package.",
        "status": "needs_review" if gate != "submit_allowed" else "completed_with_receipt",
        "artifact_refs": [str(ROOT), f"git_head:{git_head()}"],
        "verification": {
            "checks_passed": passed,
            "checks_failed": failed,
            "unverified_claims": [
                "This meter is local-file-only; it does not prove public URLs, live services, Stripe, NVIDIA, or GitHub freshness."
            ],
            "confidence": "medium" if failed else "high",
        },
        "scores": {
            "readiness_0_to_10": readiness,
            "local_file_percent": pct,
        },
        "promotion_gate": gate,
        "notes": [
            "Use this as the simple dashboard/submission meter, not as final judge scoring.",
            "Null scorecard remains the higher-context review artifact."
        ],
    }

    if args.json:
        print(json.dumps(receipt, indent=2))
    else:
        print(f"Grok Go submission meter: {readiness}/10 ({pct}%) — {gate}")
        print(f"Passed: {len(passed)}  Failed: {len(failed)}  Git: {git_head()}")
        if failed:
            print("Failed checks:")
            for item in failed:
                print(f"- {item}")
        print("\nReceipt JSON:")
        print(json.dumps(receipt, indent=2))
    return 0 if gate != "do_not_submit" else 2


if __name__ == "__main__":
    raise SystemExit(main())
