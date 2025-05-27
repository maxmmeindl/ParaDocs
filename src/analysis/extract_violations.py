#!/usr/bin/env python3
"""
extract_violations.py — pass-one rule-based violation extractor

Scans every processed document (metadata JSON + optional .txt) and flags
files that contain keywords/phrases for common EEO/ADA/Privacy issues.

Outputs: search_index/violations_summary.json

Schema:
[
  {
    "violation": "Retaliatory Termination",
    "documents": ["docs/processed/.../file.pdf", ...],
    "first_date": "2019-11-01",
    "last_date": "2019-11-01",
    "weight": 10
  },
  ...
]

Weight = simple formula len(documents) + severity base.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

PROCESSED_ROOT = Path("docs/processed")
OUTPUT = Path("search_index/violations_summary.json")
OUTPUT.parent.mkdir(exist_ok=True)

# --- default keyword patterns (lower-case) ---------------------------------
VIOLATION_PATTERNS: Dict[str, List[str]] = {
    "Retaliatory Termination": ["retaliatory termination", "retaliated", "reprisal", "removed in retaliation"],
    "Failure to Accommodate (ADA)": ["failure to accommodate", "reasonable accommodation denied", "interactive process", "ra request denied"],
    "HIPAA / Privacy Act Breach": ["hipaa", "privacy act", "phi disclosure", "unauthorized disclosure"],
    "Due Process Violation": ["due process", "procedural violation", "notice of decision without hearing", "no opportunity to respond"],
    "Whistleblower Retaliation": ["whistleblower", "protected disclosure", "osc case"],
    "FMLA Interference": ["fmla", "family medical leave", "fmla denied"],
}

# Map each violation to a base severity weight (higher = more severe)
SEVERITY_MAP: Dict[str, int] = {
    "Retaliatory Termination": 50,
    "Failure to Accommodate (ADA)": 30,
    "HIPAA / Privacy Act Breach": 40,
    "Due Process Violation": 25,
    "Whistleblower Retaliation": 35,
    "FMLA Interference": 20,
}

# quick regex date matcher (ISO or mm/dd/yyyy)
DATE_RX = re.compile(r"(\d{4}-\d{2}-\d{2})|(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})")


def text_of(doc: Path) -> str:
    txt = doc.with_suffix(".txt")
    if txt.exists():
        try:
            return txt.read_text("utf-8", errors="ignore")
        except Exception:
            return ""
    return ""


def dates_in(text: str) -> List[str]:
    return DATE_RX.findall(text)


def main() -> None:
    findings: Dict[str, List[str]] = defaultdict(list)
    first_dates: Dict[str, str] = {}
    last_dates: Dict[str, str] = {}

    for meta_path in PROCESSED_ROOT.rglob("*.json"):
        doc_path = meta_path.with_suffix("")
        try:
            meta = json.loads(meta_path.read_text("utf-8"))
        except Exception:
            continue
        blob = "\n".join([
            json.dumps(meta),
            text_of(doc_path).lower()
        ]).lower()

        for vio, patterns in VIOLATION_PATTERNS.items():
            if any(p in blob for p in patterns):
                findings[vio].append(str(doc_path))
                # crude date extraction – first date in metadata or text
                date_candidates: List[str] = []
                for k in ("created_date", "event_date"):
                    if k in meta and re.match(r"\d{4}-\d{2}-\d{2}", str(meta[k])):
                        date_candidates.append(meta[k])
                date_candidates.extend([d[0] or d[1] for d in dates_in(blob)])
                if date_candidates:
                    try:
                        cur_date = sorted(date_candidates)[0][:10]
                        if vio not in first_dates or cur_date < first_dates[vio]:
                            first_dates[vio] = cur_date
                        cur_last = sorted(date_candidates)[-1][:10]
                        if vio not in last_dates or cur_last > last_dates[vio]:
                            last_dates[vio] = cur_last
                    except Exception:
                        pass

    # build summary list
    summary: List[Dict] = []
    for vio, docs in findings.items():
        # Use severity score (default 10) + #documents multiplier to prioritise seriousness, not just volume
        severity = SEVERITY_MAP.get(vio, 10)
        weight = severity + len(docs) * 2  # each supporting doc adds incremental weight
        summary.append({
            "violation": vio,
            "documents": docs,
            "first_date": first_dates.get(vio, ""),
            "last_date": last_dates.get(vio, ""),
            "weight": weight
        })

    # sort by weight desc
    summary.sort(key=lambda x: x["weight"], reverse=True)

    OUTPUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Violation summary written to {OUTPUT} (total {len(summary)})")


if __name__ == "__main__":
    main() 