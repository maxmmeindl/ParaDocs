#!/usr/bin/env python3
"""
generate_document_library.py — build paradocs-index.html

Scans docs/processed for metadata JSON, builds an HTML table of all documents
with columns: Case #, File Name, Document Type, Date, Size, Open link.
Run every time the pipeline is re-processed.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

OUTPUT = Path("paradocs-index.html")
CSS = "table{width:100%;border-collapse:collapse}th,td{padding:.5rem;border-bottom:1px solid #e0e0e0;}th{background:#f5f5f5;text-align:left;}"

def rows() -> list[str]:
    processed_root = Path("docs/processed")
    for meta_path in processed_root.rglob("*.json"):
        data = json.loads(meta_path.read_text("utf-8"))
        file_path = meta_path.with_suffix("")
        case = data.get("case_number","–")
        doc_type = ", ".join(data.get("document_type",[]))
        date = data.get("created_date","")
        size = data.get("file_info",{}).get("file_size",0)
        size_kb = f"{size//1024} KB" if size else ""
        rel_path = file_path.as_posix()
        yield f"<tr><td>{case}</td><td>{file_path.name}</td><td>{doc_type}</td><td>{date}</td><td>{size_kb}</td><td><a href='{rel_path}' target='_blank'>open</a></td></tr>"

def build_page():
    body_rows = "\n".join(rows())
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"""<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>Document Library</title><style>{CSS}</style></head><body><h2>ParaDocs Document Library</h2><p>Generated {generated}</p><table><thead><tr><th>Case</th><th>File</th><th>Type</th><th>Date</th><th>Size</th><th>Link</th></tr></thead><tbody>{body_rows}</tbody></table></body></html>"""
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Document library written to {OUTPUT}")

if __name__ == "__main__":
    build_page() 