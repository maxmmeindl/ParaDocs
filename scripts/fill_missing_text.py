#!/usr/bin/env python3
"""
fill_missing_text.py — Backfill OCR/text extraction for already-processed documents

If the initial pipeline ran without certain optional libraries (pdfminer.six, python-docx, textract, mailparser,
etc.), many items in docs/processed may be missing their companion .txt full-text files.  This utility scans
all processed documents and, for any file that still lacks a .txt, re-invokes the same _extract_text() logic
used by DocumentProcessor to generate the file in-place.

Usage:
    python scripts/fill_missing_text.py

The script prints a short summary of how many files were updated.  It is safe to run multiple times; already
filled items are skipped.
"""

from __future__ import annotations

import sys
import logging
from pathlib import Path
import argparse

# Re-use extraction helper from pipeline
sys.path.append(str(Path(__file__).parent))  # allow `import run_pipeline`

from run_pipeline import DocumentProcessor  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


SUPPORTED_SUFFIXES = {".pdf", ".docx", ".doc", ".eml", ".msg"}


def backfill_missing_text(exts:set[str]) -> None:
    processed_root = Path("docs/processed")
    if not processed_root.exists():
        logger.error("docs/processed directory not found – run the main pipeline first.")
        return

    processor = DocumentProcessor()  # only used for its _extract_text helper

    updated = 0
    scanned = 0

    for file_path in processed_root.rglob("*"):
        if file_path.suffix.lower() not in exts:
            continue

        scanned += 1
        txt_path = file_path.with_suffix(".txt")
        if txt_path.exists():
            continue  # already has text

        logger.info(f"Extracting text for: {file_path}")
        text = processor._extract_text(file_path)  # pylint: disable=protected-access
        if text is None:
            logger.warning(f"Extraction failed or dependency missing for: {file_path}")
            continue

        try:
            with txt_path.open("w", encoding="utf-8") as f_txt:
                f_txt.write(text)
            updated += 1
        except Exception as exc:  # noqa: BLE001
            logger.error(f"Failed to write txt for {file_path}: {exc}")

    logger.info("Backfill complete – %s/%s files had text generated", updated, scanned)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill OCR/text for processed docs")
    parser.add_argument("--extensions", nargs="*", default=list(SUPPORTED_SUFFIXES), help="File extensions to process, e.g. .eml .msg")
    args = parser.parse_args()
    exts = {e.lower() if e.startswith('.') else f'.{e.lower()}' for e in args.extensions}
    backfill_missing_text(exts) 