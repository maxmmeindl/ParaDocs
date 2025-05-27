#!/usr/bin/env python3
"""
generate_summary_metrics.py — consolidate high-level counts for dashboards.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

IDX_DIR = Path("search_index")
OUTPUT = IDX_DIR / "summary_metrics.json"


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text("utf-8"))
    except Exception:
        return default


def main() -> None:
    stats = load_json(IDX_DIR / "index_stats.json", {})
    dups = load_json(IDX_DIR / "duplicates.json", [])
    violations = load_json(IDX_DIR / "violations_summary.json", [])

    summary: Dict = {
        "generated_at": stats.get("generated_at"),
        "total_documents": stats.get("total_documents", 0),
        "total_keywords": stats.get("total_keywords", 0),
        "total_dates": stats.get("total_dates", 0),
        "duplicate_groups": len(dups),
        "violations": [{
            "violation": v["violation"],
            "docs": len(v["documents"]),
            "weight": v["weight"],
            "first_doc": v["documents"][0] if v.get("documents") else "",
            "doc_paths": v["documents"][:12]
        } for v in violations[:20]],
    }
    OUTPUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Summary metrics written to {OUTPUT}")


if __name__ == "__main__":
    main() 