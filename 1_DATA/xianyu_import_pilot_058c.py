# 1_DATA/xianyu_import_pilot_058c.py — Entry 058C Real Xianyu Import Pilot
#
# Does NOT fabricate REAL data.
# If drop zone empty → WAITING_FOR_REAL_SOURCE_FILE / IMPORT_READY.
# Does NOT run Opportunity / CF / Publish / Commercial Learning.

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
from connectors.xianyu_import_connector import (  # noqa: E402
    import_file,
    import_readiness,
    list_import_candidates,
    reject_legacy_sample_import,
)


def assert_current_db_clean_of_legacy_samples() -> dict:
    """Confirm Current DB has no SAMPLE-style product rows; do not DROP schema."""
    database.ensure_schema()
    msc.ensure_market_source_schema()
    with database.get_connection() as conn:
        products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        scores = conn.execute("SELECT COUNT(*) FROM scores").fetchone()[0]
        signals = 0
        try:
            signals = conn.execute("SELECT COUNT(*) FROM market_signals").fetchone()[0]
        except Exception:
            pass
        selection = 0
        try:
            selection = conn.execute("SELECT COUNT(*) FROM selection_results").fetchone()[0]
        except Exception:
            pass
        sampleish = conn.execute(
            """
            SELECT COUNT(*) FROM products
            WHERE lower(source_url) LIKE '%sample%'
               OR lower(source_url) LIKE '%/item/test%'
               OR title LIKE '测试%'
            """
        ).fetchone()[0]
    return {
        "products": products,
        "scores": scores,
        "market_signals": signals,
        "selection_results": selection,
        "sampleish_products": sampleish,
        "legacy_business_rows_absent": sampleish == 0,
        "ok": sampleish == 0,
    }


def run_pilot(*, declared_origin: str = msc.ORIGIN_UNKNOWN, auto_import: bool = False) -> dict:
    """
    Pilot entrypoint.

    auto_import=False (default): only readiness check — never invent files.
    auto_import=True: import candidates with declared_origin (operator must set REAL intentionally).
    """
    readiness = import_readiness()
    clean = assert_current_db_clean_of_legacy_samples()
    out = {
        "entry": "058C",
        "date": "2026-08-30",
        "readiness": readiness,
        "current_db_clean": clean,
        "live_collection": msc.live_collection_status(),
        "opportunity_discovery_run": False,
        "product_generation_run": False,
        "commercial_learning_run": False,
        "sales_platform": None,
        "imports": [],
    }

    if readiness["status"] == "WAITING_FOR_REAL_SOURCE_FILE":
        out["entry_status"] = "READY_FOR_REAL_IMPORT"
        out["waiting"] = "WAITING_FOR_REAL_SOURCE_FILE"
        out["note"] = "Import capability ready; no real source file present. No data fabricated."
        return out

    if not auto_import:
        out["entry_status"] = "CANDIDATES_PRESENT_AWAITING_OPERATOR"
        out["waiting"] = None
        out["note"] = (
            "Candidates found but auto_import=False. "
            "Re-run with auto_import=True and declared_origin=REAL only if attested."
        )
        return out

    for path in list_import_candidates():
        result = import_file(
            path,
            declared_origin=declared_origin,
            collection_mode=msc.MODE_IMPORT,
            allow_sample=False,
            mirror_to_products=False,
        )
        out["imports"].append(result)

    accepted = sum(int((i.get("stats") or {}).get("accepted_count") or 0) for i in out["imports"])
    out["entry_status"] = "IMPORTED" if accepted else "IMPORT_ATTEMPTED_ZERO_ACCEPTED"
    out["market_observations"] = msc.count_observations()
    out["real_observations"] = msc.count_observations(data_origin=msc.ORIGIN_REAL)
    return out


def main() -> None:
    # Default: readiness only — never fabricate, never auto-declare REAL
    report = run_pilot(declared_origin=msc.ORIGIN_UNKNOWN, auto_import=False)
    print(json.dumps(report, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
