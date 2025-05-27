#!/usr/bin/env python3
"""
consolidate_duplicates.py — tag and move exact duplicate files

Policy:
  • From each SHA-256 duplicate group, keep the file whose path is lexicographically first (canonical).
  • For every extra copy:
        * Move the actual file to docs/duplicates/<same structure>/
        * Update its metadata JSON by adding {"duplicate_of": "<canonical_path>"}
        * Leave .txt sidecar (if any) alongside the moved file (not re-indexed).
  • Write a summary to reports/duplicates_moved.json so we have an audit trail.

Re-running is safe; already-moved files are skipped.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Dict, List

DUP_PATH = Path("search_index/duplicates.json")
REPORT = Path("reports/duplicates_moved.json")
PROCESSED = Path("docs/processed")
DUP_DIR = Path("docs/duplicates")
DUP_DIR.mkdir(parents=True, exist_ok=True)


def move_and_tag(extra: Path, canonical: str):
    rel = extra.relative_to(PROCESSED)
    target = DUP_DIR / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.move(str(extra), str(target))
    # move txt sidecar if exists
    txt = extra.with_suffix(".txt")
    if txt.exists():
        shutil.move(str(txt), str(target.with_suffix('.txt')))
    # update metadata
    meta_path = extra.with_suffix('.json')
    if meta_path.exists():
        meta = json.loads(meta_path.read_text('utf-8'))
        meta['duplicate_of'] = canonical
        target_meta = DUP_DIR / rel.with_suffix('.json')
        target_meta.parent.mkdir(parents=True, exist_ok=True)
        target_meta.write_text(json.dumps(meta, indent=2), encoding='utf-8')
        meta_path.unlink(missing_ok=True)


def main():
    moved: Dict[str, List[str]] = {}
    if not DUP_PATH.exists():
        print("duplicates.json not found – run find_duplicates first")
        return
    groups = json.loads(DUP_PATH.read_text('utf-8'))
    for grp in groups:
        files = grp['files']
        if len(files) < 2:
            continue
        canonical = sorted(files)[0]
        for f in files[1:]:
            src = Path(f)
            if not src.exists():
                continue  # already moved
            move_and_tag(src, canonical)
            moved.setdefault(canonical, []).append(str(src))
    REPORT.write_text(json.dumps(moved, indent=2), encoding='utf-8')
    print(f"Consolidated {sum(len(v) for v in moved.values())} duplicate files. Report: {REPORT}")


if __name__ == "__main__":
    main() 