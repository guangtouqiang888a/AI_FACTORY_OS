# 1_DATA/connectors/xianyu_entry_068_pipeline.py — Entry 068
#
# Observation → Filter wiring (reuse apply_observation_filters from 067).
# Import gate reuse from 066. No parallel filter module.
# REAL SEARCH_RESULT only for Current DB; never recommended/fixture/sample.

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import acquisition_engine as eng  # noqa: E402
import market_source_core as msc  # noqa: E402
from connectors import xianyu_extension_bridge_065 as bridge  # noqa: E402
from connectors import xianyu_market_observation_import_066 as imp066  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402

ENTRY_VERSION = "068.1.0"
ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_entry_068"
DEFAULT_FILTER = {"min_want_count": 50, "min_price": None, "max_price": None}


def want_count_status_report(records: list[dict]) -> dict[str, Any]:
    buckets = {
        ts062.WANT_VISIBLE_ON_CARD: 0,
        ts062.WANT_MISSING_ON_CARD: 0,
        ts062.WANT_AVAILABLE_ON_DETAIL: 0,
        ts062.WANT_UNAVAILABLE: 0,
        ts062.WANT_UNKNOWN: 0,
    }
    for r in records:
        st = r.get("want_count_status") or ts062.WANT_UNKNOWN
        if st not in buckets:
            st = ts062.WANT_UNKNOWN
        buckets[st] += 1
    total = len(records) or 1
    return {
        "counts": buckets,
        "rates": {k: round(v / total, 4) for k, v in buckets.items()},
        "total": len(records),
    }


def data_quality_report(
    *,
    all_records: list[dict],
    search_records: list[dict],
    recommended_records: list[dict],
    accepted: int = 0,
    duplicates: int = 0,
    rejected: int = 0,
) -> dict[str, Any]:
    def rate(pred) -> float:
        if not search_records:
            return 0.0
        return round(sum(1 for r in search_records if pred(r)) / len(search_records), 4)

    return {
        "total_seen": len(all_records),
        "search_results": len(search_records),
        "recommended_results": len(recommended_records),
        "accepted": accepted,
        "duplicate": duplicates,
        "rejected": rejected,
        "title_rate": rate(lambda r: bool(r.get("title"))),
        "price_rate": rate(lambda r: r.get("price") is not None),
        "want_count_rate": rate(
            lambda r: r.get("want_count_status") == ts062.WANT_VISIBLE_ON_CARD
        ),
        "url_rate": rate(lambda r: bool(r.get("source_url"))),
        "item_id_rate": rate(lambda r: bool(r.get("source_item_id"))),
    }


def apply_filter_to_observation_candidates(
    candidates: list[dict],
    *,
    filters: dict | None = None,
) -> dict[str, Any]:
    """
    MarketObservation candidates → Filter Result.
    Reuses eng.apply_observation_filters — does NOT delete observations.
    """
    f = filters if filters is not None else DEFAULT_FILTER
    result = eng.apply_observation_filters(candidates, f)
    # Preserve originals separately from classification
    return {
        "entry": "068",
        "filters_applied": result["filters"],
        "observations_input": len(candidates),
        "observations_retained": len(result["classified"]),
        "filter_deleted_observations": False,
        "MATCH": len(result["MATCH"]),
        "BELOW_THRESHOLD": len(result["BELOW_THRESHOLD"]),
        "ABOVE_THRESHOLD": len(result["ABOVE_THRESHOLD"]),
        "UNKNOWN": len(result["UNKNOWN"]),
        "counts": result["counts"],
        "classified": result["classified"],
        "originals": candidates,
        "note": result.get("note"),
    }


def run_pipeline(
    batch: dict[str, Any],
    *,
    human_verified: bool = False,
    filters: dict | None = None,
    allow_db_write: bool = True,
) -> dict[str, Any]:
    """
    MarketRecord → Bridge → Raw → Normalize → (optional Observation DB)
    → Filter on SEARCH_RESULT candidates.

    DB write only when human_verified and SEARCH_RESULT eligible and allow_db_write.
    Recommended never imported as REAL query evidence.
    """
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    filters = filters if filters is not None else DEFAULT_FILTER

    # Hard block: refuse writing if batch claims recommended as search evidence
    page_state = batch.get("page_state")
    result_origin = batch.get("result_origin")
    records = batch.get("records") or []
    search_recs = [r for r in records if r.get("result_origin") == ts062.ORIGIN_SEARCH]
    rec_recs = [r for r in records if r.get("result_origin") == ts062.ORIGIN_RECOMMENDED]

    # Never use recommended to fill empty search for DB
    if not search_recs and rec_recs:
        human_verified_effective = False
        block_reason = "RECOMMENDED_ONLY_NOT_SEARCH_EVIDENCE"
    else:
        human_verified_effective = human_verified and allow_db_write
        block_reason = None

    pipe = imp066.process_extension_batch_for_entry(
        batch, human_verified=human_verified_effective
    )

    # Prefer normalized SEARCH_RESULT candidates for filter
    normalized_path = ARTIFACT_DIR / "normalized_preview.json"
    if (bridge.ARTIFACT_DIR / "normalized_preview.json").exists():
        normalized = json.loads(
            (bridge.ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8")
        )
        (ARTIFACT_DIR / "normalized_preview.json").write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    else:
        normalized = []

    search_candidates = [
        c for c in normalized if c.get("result_origin") == ts062.ORIGIN_SEARCH
    ]
    # Also copy batch
    (ARTIFACT_DIR / "batch.json").write_text(
        json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    filter_result = apply_filter_to_observation_candidates(
        search_candidates, filters=filters
    )
    (ARTIFACT_DIR / "filter_report.json").write_text(
        json.dumps(
            {k: v for k, v in filter_result.items() if k not in ("classified", "originals")}
            | {
                "classified_summary": [
                    {
                        "title": c.get("title"),
                        "want_count": c.get("want_count"),
                        "price": c.get("price"),
                        "filter_status": c.get("filter_status"),
                        "source_item_id": c.get("source_item_id"),
                    }
                    for c in filter_result.get("classified", [])
                ]
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    want_report = want_count_status_report(search_candidates)
    (ARTIFACT_DIR / "want_count_report.json").write_text(
        json.dumps(want_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    imp = pipe.get("import") or {}
    quality = data_quality_report(
        all_records=records,
        search_records=search_recs,
        recommended_records=rec_recs,
        accepted=int(imp.get("inserted") or 0),
        duplicates=int(imp.get("duplicates") or 0),
        rejected=int(imp.get("skipped") or 0),
    )
    (ARTIFACT_DIR / "data_quality_report.json").write_text(
        json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    first_real = bool(imp.get("first_real_market_observation")) and not block_reason
    out = {
        "entry": "068",
        "ok": bool(pipe.get("ok")),
        "page_state": page_state,
        "result_origin": result_origin,
        "search_result_count": len(search_recs),
        "recommended_result_count": len(rec_recs),
        "block_reason": block_reason,
        "human_verified": human_verified,
        "human_verified_effective": human_verified_effective,
        "pipeline": pipe,
        "filter": {
            "MATCH": filter_result["MATCH"],
            "BELOW_THRESHOLD": filter_result["BELOW_THRESHOLD"],
            "UNKNOWN": filter_result["UNKNOWN"],
            "observations_retained": filter_result["observations_retained"],
            "filter_deleted_observations": False,
            "filters_applied": filter_result["filters_applied"],
        },
        "want_count_report": want_report,
        "data_quality": quality,
        "first_real_xianyu_market_observation": first_real,
        "observation_ids": _observation_ids_for_run(imp.get("collection_run_id")),
        "artifact_dir": str(ARTIFACT_DIR),
        "entry_version": ENTRY_VERSION,
    }
    (ARTIFACT_DIR / "pipeline_summary.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    return out


def _observation_ids_for_run(run_id: str | None) -> list[str]:
    if not run_id:
        return []
    with msc.database.get_connection() as conn:
        rows = conn.execute(
            "SELECT observation_id FROM market_observations WHERE run_id=?",
            (run_id,),
        ).fetchall()
    return [r[0] if not hasattr(r, "keys") else r["observation_id"] for r in rows]
