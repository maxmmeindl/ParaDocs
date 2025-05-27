#!/usr/bin/env python3
"""
find_duplicates.py — generate a simple duplicate-report

Reads every *.json metadata record in docs/processed and groups documents by
file_info.file_hash.  If two or more distinct file paths share the same hash we
consider them duplicates.  A JSON report is written to search_index/duplicates.json
and a short console table is printed.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

REPORT_PATH = Path("search_index/duplicates.json")


def load_hashes() -> Dict[str, List[str]]:
    processed_root = Path("docs/processed")
    hashes: Dict[str, List[str]] = defaultdict(list)

    for meta_path in processed_root.rglob("*.json"):
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        file_hash = data.get("file_info", {}).get("file_hash")
        if not file_hash:
            continue
        original_file = meta_path.with_suffix("")  # strip .json
        hashes[file_hash].append(str(original_file))
    return hashes


def write_report(hashes: Dict[str, List[str]]) -> None:
    duplicates = [{"sha256": h, "files": paths} for h, paths in hashes.items() if len(paths) > 1]
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(json.dumps(duplicates, indent=2), encoding="utf-8")
    print(f"Duplicate report written – {len(duplicates)} hash groups with >1 file (see {REPORT_PATH})")
    for item in duplicates[:20]:
        print(f"{item['sha256'][:8]}…  {len(item['files'])} files -> {item['files'][0]}")


if __name__ == "__main__":
    write_report(load_hashes()) 