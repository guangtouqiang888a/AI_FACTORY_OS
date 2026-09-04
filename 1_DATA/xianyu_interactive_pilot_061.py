# 1_DATA/xianyu_interactive_pilot_061.py — Entry 061 runner
#
# Interactive browser collection → test artifacts only.
# Asserts Current DB market_observations / products unchanged.

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import database  # noqa: E402
from connectors.xianyu_interactive_connector import (  # noqa: E402
    ARTIFACT_DIR,
    propose_collector_registry_update,
    run_interactive_collection,
)


def _count(table: str) -> int:
    with database.get_connection() as conn:
        return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def main() -> int:
    before = {
        "market_observations": _count("market_observations"),
        "products": _count("products"),
    }
    # optional tables
    for t in ("market_signals", "selection_results"):
        try:
            before[t] = _count(t)
        except Exception:
            before[t] = None

    result = run_interactive_collection(query="虚拟资料", max_records=20)
    after = {
        "market_observations": _count("market_observations"),
        "products": _count("products"),
    }
    for t in ("market_signals", "selection_results"):
        try:
            after[t] = _count(t)
        except Exception:
            after[t] = None

    db_safe = after["market_observations"] == before["market_observations"] and after[
        "products"
    ] == before["products"]
    proposal = propose_collector_registry_update(result)
    summary = {
        "entry": "061",
        "result_status": result.get("status"),
        "ok": result.get("ok"),
        "records_extracted": result.get("records_extracted") or 0,
        "FIRST_REAL_XIANYU_CANDIDATE_BATCH": bool(
            result.get("first_real_xianyu_candidate_batch")
        ),
        "current_db_before": before,
        "current_db_after": after,
        "current_db_unchanged": db_safe,
        "collector_registry_proposal": proposal,
        "artifact_dir": str(ARTIFACT_DIR),
        "login_used": result.get("login_used", False),
        "bypass_attempted": result.get("bypass_attempted", False),
        "hidden_api_called": result.get("hidden_api_called", False),
    }
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / "pilot_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if db_safe else 2


if __name__ == "__main__":
    raise SystemExit(main())
