# 1_DATA/xianyu_targeted_search_pilot_062.py — Entry 062 runner

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import database  # noqa: E402
from connectors.xianyu_targeted_search_062 import (  # noqa: E402
    ARTIFACT_DIR,
    run_targeted_search,
)


def _count(table: str) -> int | None:
    try:
        with database.get_connection() as conn:
            return int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
    except Exception:
        return None


def main() -> int:
    before = {
        "market_observations": _count("market_observations"),
        "products": _count("products"),
        "market_signals": _count("market_signals"),
        "selection_results": _count("selection_results"),
    }
    result = run_targeted_search()
    after = {
        "market_observations": _count("market_observations"),
        "products": _count("products"),
        "market_signals": _count("market_signals"),
        "selection_results": _count("selection_results"),
    }
    safe = (
        after["market_observations"] == before["market_observations"]
        and after["products"] == before["products"]
    )
    summary = {
        "entry": "062",
        "status": result.get("status"),
        "ok": result.get("ok"),
        "query": result.get("query"),
        "search_results_count": result.get("search_results_count"),
        "FIRST_REAL_XIANYU_SEARCH_BATCH": bool(
            result.get("first_real_xianyu_search_batch")
        ),
        "want_count_audit": result.get("want_count_audit"),
        "field_availability": result.get("field_availability"),
        "query_attempts": result.get("query_attempts"),
        "current_db_before": before,
        "current_db_after": after,
        "current_db_unchanged": safe,
        "login_used": False,
        "bypass_attempted": False,
        "artifact_dir": str(ARTIFACT_DIR),
    }
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / "pilot_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    return 0 if safe else 2


if __name__ == "__main__":
    raise SystemExit(main())
