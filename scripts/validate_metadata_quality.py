#!/usr/bin/env python3
"""
validate_metadata_quality.py — quick report of metadata completeness.

Outputs:
  • Console table with total files scanned, missing JSON, empty/undefined fields.
  • reports/metadata_gaps.json for downstream tooling.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)
GAPS_JSON = REPORT_DIR / "metadata_gaps.json"

REQUIRED = ["document_id", "document_type", "agency", "case_number", "created_date"]


def audit() -> Dict:
    processed_root = Path("docs/processed")
    stats = {
        "total_files": 0,
        "no_metadata": 0,
        "missing_fields": Counter(),
        "empty_document_type": 0,
    }
    per_file: List[Dict] = []

    for data_file in processed_root.rglob("*.*"):
        if data_file.suffix.lower() in {".json", ".txt"}:
            continue  # skip sidecars
        stats["total_files"] += 1
        meta_path = data_file.with_suffix(".json")
        if not meta_path.exists():
            stats["no_metadata"] += 1
            per_file.append({"file": str(data_file), "issue": "NO_METADATA"})
            continue
        try:
            meta = json.loads(meta_path.read_text("utf-8"))
        except Exception:
            per_file.append({"file": str(data_file), "issue": "BROKEN_JSON"})
            continue
        # missing fields
        for fld in REQUIRED:
            val = meta.get(fld)
            if not val:
                stats["missing_fields"][fld] += 1
                per_file.append({"file": str(data_file), "issue": f"MISSING_{fld}"})
        if not meta.get("document_type"):
            stats["empty_document_type"] += 1
    report = {"summary": stats, "issues": per_file}
    GAPS_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def print_summary(rep: Dict):
    s = rep["summary"]
    print("\nMetadata Quality Report")
    print("-----------------------")
    print(f"Files scanned       : {s['total_files']}")
    print(f"No metadata JSON    : {s['no_metadata']}")
    print(f"Empty doc_type      : {s['empty_document_type']}")
    for fld, cnt in s["missing_fields"].items():
        print(f"Missing {fld:<13}: {cnt}")
    print(f"\nDetailed list written to {GAPS_JSON}")


if __name__ == "__main__":
    print_summary(audit()) 