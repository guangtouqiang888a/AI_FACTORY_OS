# 1_DATA/xianyu_first_real_probe_066.py — Entry 066 live probe
#
# Visible Chrome search session → Extension-format batch → import gate.
# Current DB write only with --human-verified (user attestation).

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
import market_source_core as msc  # noqa: E402
from connectors import xianyu_extension_bridge_065 as bridge  # noqa: E402
from connectors import xianyu_market_observation_import_066 as imp066  # noqa: E402
from connectors import xianyu_search_session_063 as ss063  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402

ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_entry_066"
MAX_RECORDS = 20
DEFAULT_QUERY = "手机壳"


def _db_counts() -> dict:
    with sqlite3.connect(config.DB_PATH) as conn:
        out = {"market_observations": 0, "products": 0}
        out["market_observations"] = int(
            conn.execute("SELECT COUNT(*) FROM market_observations").fetchone()[0]
        )
        out["products"] = int(
            conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        )
        for table in ("market_signals", "selection_results", "market_events"):
            if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,),
            ).fetchone():
                out[table] = int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        return out


def _session_result_to_batch(session_result: dict, *, run_id: str) -> dict:
    coll = session_result.get("collection") or {}
    search_recs = coll.get("search_records") or []
    rec_recs = coll.get("recommended_records") or []
    all_recs = (search_recs + rec_recs)[:MAX_RECORDS]
    session = (session_result.get("session") or {})
    query = session.get("query") or DEFAULT_QUERY
    session_id = session.get("session_id") or f"sess_{uuid.uuid4().hex[:12]}"
    state = coll.get("search_state") or {}

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

    page_state = state.get("search_state", ss063.STATE_UNKNOWN)
    if page_state == ss063.STATE_SEARCH_RESULT:
        page_origin = ts062.ORIGIN_SEARCH
    elif page_state in (ss063.STATE_RECOMMENDED, ss063.STATE_EMPTY):
        page_origin = ts062.ORIGIN_RECOMMENDED
    else:
        page_origin = ts062.ORIGIN_UNKNOWN

    status = "SUCCESS" if records else "NO_RESULTS"
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
        "filter_metadata": {"min_want_count": None},
        "records": records,
        "stats": {
            "records_extracted": len(records),
            "search_result_count": len(search_recs),
            "recommended_count": len(rec_recs),
        },
        "probe_meta": {
            "entry": "066",
            "method": "search_session_063_dom + extension_batch_format",
        },
    }


def run_probe(query: str, *, human_verified: bool) -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = f"run_{uuid.uuid4().hex[:12]}"
    before = _db_counts()
    (ARTIFACT_DIR / "db_before.json").write_text(
        json.dumps(before, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    session_result = ss063.run_search_session(
        query=query,
        max_records=MAX_RECORDS,
        minimum_want_count=None,
        also_prove_collector_on_fixture=False,
    )

    batch = _session_result_to_batch(session_result, run_id=run_id)
    (ARTIFACT_DIR / "extension_batch.json").write_text(
        json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    pipeline = imp066.process_extension_batch_for_entry(
        batch, human_verified=human_verified
    )
    after = _db_counts()

    summary = {
        "entry": "066",
        "query": query,
        "run_id": run_id,
        "human_verified": human_verified,
        "search_control": session_result.get("search_control_feasibility"),
        "search_state": (session_result.get("collection") or {}).get("search_state"),
        "search_result_cards": len((session_result.get("collection") or {}).get("search_records") or []),
        "recommended_cards": len(
            (session_result.get("collection") or {}).get("recommended_records") or []
        ),
        "first_real_market_observation": pipeline.get("import", {}).get(
            "first_real_market_observation", False
        ),
        "db_before": before,
        "db_after": after,
        "pipeline_ok": pipeline.get("ok"),
        "import_status": (pipeline.get("import") or {}).get("status"),
    }
    (ARTIFACT_DIR / "probe_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Entry 066 first real Xianyu probe")
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument(
        "--human-verified",
        action="store_true",
        help="User attests records are real SEARCH_RESULT from visible browser",
    )
    args = parser.parse_args()
    result = run_probe(args.query, human_verified=args.human_verified)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
