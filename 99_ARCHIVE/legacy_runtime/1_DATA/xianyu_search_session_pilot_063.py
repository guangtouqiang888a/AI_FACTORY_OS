# 1_DATA/xianyu_search_session_pilot_063.py — Entry 063 runner

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import database  # noqa: E402
from connectors.xianyu_search_session_063 import ARTIFACT_DIR, run_search_session  # noqa: E402


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
    # One query — do not burn many (062 already showed empty for templates)
    result = run_search_session(query="Excel模板", max_records=20, minimum_want_count=50)
    after = {
        "market_observations": _count("market_observations"),
        "products": _count("products"),
        "market_signals": _count("market_signals"),
        "selection_results": _count("selection_results"),
    }
    safe = after["market_observations"] == before["market_observations"] and after[
        "products"
    ] == before["products"]
    summary = {
        "entry": "063",
        "Search_Control": result.get("search_control_feasibility"),
        "search_control_status": (result.get("search_control") or {}).get("status"),
        "Page_Collection_live": result.get("collector_feasibility_live"),
        "Page_Collection_fixture_SEARCH_RESULT": result.get(
            "collector_feasibility_when_search_dom_present"
        ),
        "FIRST_REAL_XIANYU_SEARCH_CANDIDATE": bool(
            result.get("first_real_xianyu_search_candidate")
        ),
        "session": result.get("session"),
        "current_db_before": before,
        "current_db_after": after,
        "current_db_unchanged": safe,
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
