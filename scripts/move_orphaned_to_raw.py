#!/usr/bin/env python3
"""
move_orphaned_to_raw.py — housekeeping utility

Some documents were copied directly into docs/processed/ without ever going through
run_pipeline.py.  Those items have **no** side-car JSON metadata and therefore are
ignored during indexing.  This script finds such orphaned files (of supported
document types), moves them back to docs/raw/ (mirroring their processed
relative path), and deletes any stale .txt sidecars so the main pipeline can
re-create a clean set.

Run:
    python scripts/move_orphaned_to_raw.py
"""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SUPPORTED_SUFFIXES = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".eml", ".msg"}


def move_orphans() -> None:
    processed_root = Path("docs/processed")
    raw_root = Path("docs/raw")

    if not processed_root.exists():
        logger.error("docs/processed directory missing – nothing to do.")
        return

    moved = 0
    scanned = 0

    for file_path in processed_root.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue

        scanned += 1
        json_path = file_path.with_suffix(".json")
        if json_path.exists():
            continue  # Already has metadata – skip

        # Compute relative path under processed/, then build target under raw/
        rel_path = file_path.relative_to(processed_root)
        target_path = raw_root / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info("Moving orphaned file to raw/: %s -> %s", file_path, target_path)
        try:
            shutil.move(str(file_path), str(target_path))
            # Remove any stray .txt that may exist
            txt_path = file_path.with_suffix(".txt")
            if txt_path.exists():
                txt_path.unlink()
            moved += 1
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to move %s: %s", file_path, exc)

    logger.info("Orphan scan complete – %s/%s files relocated", moved, scanned)


if __name__ == "__main__":
    move_orphans() 