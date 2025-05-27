#!/usr/bin/env python3
"""
calculate_damages.py — very rough exposure estimator

Logic:
1. Find earliest Agency_Action termination date (metadata.created_date).
2. Compute days_since_termination to today; assume $400/day back-pay.
3. Non-economic component = sum(violation weights) * $5 000.
4. Total exposure = back + non-economic.
   low = total * 0.8 ; high = total * 1.2  (±20 %).
5. Retaliation gap = days between first EEOC_Charge date and termination date.
Writes fields into search_index/summary_metrics.json { exposure_low, exposure_high, retaliation_days }.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List

PROCESSED_ROOT = Path("docs/processed")
SM_PATH = Path("search_index/summary_metrics.json")
VIOLATIONS = Path("search_index/violations_summary.json")


def load_json(p: Path, default):
    try:
        return json.loads(p.read_text("utf-8"))
    except Exception:
        return default


def main():
    # gather termination and charge dates
    termination_dates: List[str] = []
    charge_dates: List[str] = []

    for meta_path in PROCESSED_ROOT.rglob("*.json"):
        meta = load_json(meta_path, {})
        doc_types = meta.get("document_type", [])
        created_date = meta.get("created_date")
        if not created_date:
            continue
        if "Agency_Action" in doc_types and any(k in meta_path.name.lower() for k in ["termination", "removal"]):
            termination_dates.append(created_date)
        if "EEOC_Charge" in doc_types:
            charge_dates.append(created_date)

    termination_date = min(termination_dates) if termination_dates else None
    charge_date = min(charge_dates) if charge_dates else None

    # days since termination
    back_pay_days = 0
    if termination_date:
        try:
            tdt = datetime.fromisoformat(termination_date)
            back_pay_days = (datetime.now() - tdt).days
        except Exception:
            back_pay_days = 0

    DAILY_RATE = 400  # ≈$104k/yr
    back_pay = back_pay_days * DAILY_RATE

    # non-economic via violation weights
    violations = load_json(VIOLATIONS, [])
    total_weight = sum(v.get("weight", 0) for v in violations)
    non_econ = total_weight * 5_000

    total = back_pay + non_econ
    exposure_low = round(total * 0.8)
    exposure_high = round(total * 1.2)

    retaliation_days = None
    if termination_date and charge_date:
        try:
            tdt = datetime.fromisoformat(termination_date)
            cdt = datetime.fromisoformat(charge_date)
            retaliation_days = (tdt - cdt).days
        except Exception:
            pass

    sm = load_json(SM_PATH, {})
    sm.update({
        "exposure_low": exposure_low,
        "exposure_high": exposure_high,
        "retaliation_days": retaliation_days if retaliation_days is not None else "N/A",
    })
    SM_PATH.write_text(json.dumps(sm, indent=2), encoding="utf-8")
    print("Damages appended to summary_metrics.json")


if __name__ == "__main__":
    main() 