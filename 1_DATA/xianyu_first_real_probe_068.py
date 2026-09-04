# 1_DATA/xianyu_first_real_probe_068.py — Entry 068 live probe
#
# Route A: Search Session → Extension-format batch → 068 pipeline (Filter wired).
# Current DB write only with --human-verified AND real SEARCH_RESULT.
# Never imports RECOMMENDED as query evidence.

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
from connectors import xianyu_entry_068_pipeline as pipe068  # noqa: E402
from connectors import xianyu_extension_bridge_065 as bridge  # noqa: E402
from connectors import xianyu_search_session_063 as ss063  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402

ARTIFACT_DIR = pipe068.ARTIFACT_DIR
MAX_RECORDS = 20
# Prefer queries that may yield SEARCH_RESULT in normal browser (062/066 evidence)
DEFAULT_QUERIES = ("手机壳", "Excel模板", "简历模板")


def _db_counts() -> dict:
    with sqlite3.connect(config.DB_PATH) as conn:
        out: dict = {}
        for table in (
            "market_observations",
            "products",
            "market_signals",
            "selection_results",
            "market_events",
        ):
            if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,),
            ).fetchone():
                out[table] = int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            else:
                out[table] = None
        return out


def _session_to_batch(session_result: dict, *, run_id: str, query: str) -> dict:
    coll = session_result.get("collection") or {}
    search_recs = coll.get("search_records") or []
    rec_recs = coll.get("recommended_records") or []
    # SEARCH_RESULT first only in records for evidence path; recommended tracked separately
    all_recs = (search_recs + rec_recs)[:MAX_RECORDS]
    session = session_result.get("session") or {}
    session_id = session.get("session_id") or f"sess_{uuid.uuid4().hex[:12]}"
    state = coll.get("search_state") or {}
    page_state = state.get("search_state", ss063.STATE_UNKNOWN)

    if page_state == ss063.STATE_SEARCH_RESULT:
        page_origin = ts062.ORIGIN_SEARCH
    elif page_state in (ss063.STATE_RECOMMENDED, ss063.STATE_EMPTY):
        page_origin = ts062.ORIGIN_RECOMMENDED
    else:
        page_origin = ts062.ORIGIN_UNKNOWN

    records = []
    for i, c in enumerate(all_recs, start=1):
        records.append(
            {
                "source": "xianyu",
                "platform": "xianyu",
                "source_item_id": c.get("source_item_id"),
                "source_url": c.get("source_url"),
                "title": c.get("title"),
                "price": c.get("price"),
                "currency": "CNY",
                "want_count": c.get("want_count"),
                "want_count_status": c.get("want_count_status"),
                "result_origin": c.get("result_origin"),
                "observed_at": c.get("observed_at"),
                "query": query,
                "session_id": session_id,
                "collector_version": bridge.COLLECTOR_VERSION,
                "result_position": i,
                "sales_platform": None,
            }
        )

    status = "SUCCESS" if search_recs else "NO_RESULTS"
    if page_state == ss063.STATE_BLOCKED:
        status = "ACCESS_BLOCKED"

    return {
        "contract_version": bridge.CONTRACT_VERSION,
        "message_type": "MARKET_RECORD_BATCH",
        "request_id": run_id,
        "run_id": run_id,
        "session_id": session_id,
        "source": "xianyu",
        "platform": "xianyu",
        "query": query,
        "result_origin": page_origin,
        "page_state": page_state,
        "observed_at": ts062._now(),
        "collector_version": bridge.COLLECTOR_VERSION,
        "adapter_version": bridge.ADAPTER_VERSION,
        "status": status,
        "filter_metadata": {"min_want_count": 50},
        "records": records,
        "stats": {
            "records_extracted": len(records),
            "search_result_count": len(search_recs),
            "recommended_count": len(rec_recs),
        },
        "probe_meta": {
            "entry": "068",
            "route": "A_search_session",
            "method": "search_session_063_dom + extension_batch + filter_068",
        },
    }


def run_probe(
    queries: tuple[str, ...] | list[str],
    *,
    human_verified: bool = False,
) -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    before = _db_counts()
    (ARTIFACT_DIR / "db_before.json").write_text(
        json.dumps(before, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    attempts = []
    first_real = False
    blocker = None

    for query in queries:
        run_id = f"run068_{uuid.uuid4().hex[:10]}"
        session_result = ss063.run_search_session(
            query=query,
            max_records=MAX_RECORDS,
            minimum_want_count=None,
            also_prove_collector_on_fixture=False,
        )
        batch = _session_to_batch(session_result, run_id=run_id, query=query)
        (ARTIFACT_DIR / f"extension_batch_{query}.json").write_text(
            json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        search_n = batch["stats"]["search_result_count"]
        coll = session_result.get("collection") or {}
        sc = session_result.get("search_control") or {}

        attempt = {
            "query": query,
            "run_id": run_id,
            "search_control_feasibility": session_result.get("search_control_feasibility")
            or sc.get("search_control_feasibility"),
            "search_control_status": sc.get("status"),
            "page_state": batch.get("page_state"),
            "search_result_count": search_n,
            "recommended_count": batch["stats"]["recommended_count"],
            "collector_status": coll.get("collector_status"),
            "access_control": (coll.get("search_state") or {}).get("access_control"),
        }

        # Only attempt DB path when SEARCH_RESULT present
        do_verify = human_verified and search_n > 0
        pipeline = pipe068.run_pipeline(
            batch, human_verified=do_verify, filters={"min_want_count": 50}
        )
        attempt["pipeline"] = {
            "ok": pipeline.get("ok"),
            "first_real": pipeline.get("first_real_xianyu_market_observation"),
            "filter": pipeline.get("filter"),
            "block_reason": pipeline.get("block_reason"),
            "import_status": (pipeline.get("pipeline") or {}).get("import", {}).get("status"),
        }
        attempts.append(attempt)

        if pipeline.get("first_real_xianyu_market_observation"):
            first_real = True
            break

        if search_n == 0:
            blocker = {
                "stage": "Search Controller / Page State",
                "detail": attempt["page_state"],
                "search_control": attempt["search_control_feasibility"],
                "note": "EMPTY or non-SEARCH_RESULT; recommended not used as substitute",
            }
        elif not pipeline.get("ok"):
            blocker = {"stage": "Bridge/Validation", "detail": pipeline}

    after = _db_counts()
    summary = {
        "entry": "068",
        "route": "A_search_session",
        "queries": list(queries),
        "human_verified": human_verified,
        "FIRST_REAL_XIANYU_MARKET_OBSERVATION": first_real,
        "attempts": attempts,
        "blocker": None if first_real else blocker,
        "db_before": before,
        "db_after": after,
        "db_delta_observations": (after.get("market_observations") or 0)
        - (before.get("market_observations") or 0),
        "products_unchanged": before.get("products") == after.get("products"),
        "signals_unchanged": before.get("market_signals") == after.get("market_signals"),
        "selection_unchanged": before.get("selection_results")
        == after.get("selection_results"),
        "events_unchanged": before.get("market_events") == after.get("market_events"),
        "artifact_dir": str(ARTIFACT_DIR),
    }
    (ARTIFACT_DIR / "probe_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    (ARTIFACT_DIR / "db_after.json").write_text(
        json.dumps(after, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Entry 068 first real Xianyu probe")
    parser.add_argument("--query", action="append", dest="queries", default=None)
    parser.add_argument("--human-verified", action="store_true")
    args = parser.parse_args()
    queries = tuple(args.queries) if args.queries else DEFAULT_QUERIES
    result = run_probe(queries, human_verified=args.human_verified)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
