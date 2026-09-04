# 1_DATA/connectors/xianyu_market_observation_import_066.py — Entry 066
#
# Test Sink → Verification Report → optional Current DB market_observations import.
# SEARCH_RESULT only for query-specific evidence. No products/signals/opportunities.
# Human verification gate required before DB write.

from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import market_source_core as msc  # noqa: E402
from connectors import xianyu_extension_bridge_065 as bridge  # noqa: E402
from connectors import xianyu_targeted_search_062 as ts062  # noqa: E402

ENTRY_VERSION = "066.1.0"
COLLECTOR_ID = "col_xianyu_browser_extension"
ARTIFACT_DIR = ROOT / "1_DATA" / "_tests" / "xianyu_entry_066"


def _required_fields_present(obs: dict) -> bool:
    return bool(
        obs.get("title")
        and obs.get("source_url")
        and obs.get("source_item_id")
        and obs.get("price") is not None
    )


def build_verification_report(
    batch: dict[str, Any],
    normalized: list[dict[str, Any]],
) -> dict[str, Any]:
    search = [c for c in normalized if c.get("result_origin") == ts062.ORIGIN_SEARCH]
    rec = [c for c in normalized if c.get("result_origin") == ts062.ORIGIN_RECOMMENDED]
    unknown = [c for c in normalized if c.get("result_origin") == ts062.ORIGIN_UNKNOWN]

    def _avail(key: str, pred) -> int:
        return sum(1 for c in normalized if pred(c))

    report = {
        "entry": "066",
        "run_id": batch.get("run_id"),
        "query": batch.get("query"),
        "page_state": batch.get("page_state"),
        "result_origin_page": batch.get("result_origin"),
        "result_count": len(normalized),
        "search_result_count": len(search),
        "recommended_count": len(rec),
        "unknown_origin_count": len(unknown),
        "field_availability": {
            "title": _avail("title", lambda c: bool(c.get("title"))),
            "price": _avail("price", lambda c: c.get("price") is not None),
            "want_count_visible": _avail(
                "want_count",
                lambda c: c.get("want_count_status") == ts062.WANT_VISIBLE_ON_CARD,
            ),
            "want_count_missing": _avail(
                "want_count_missing",
                lambda c: c.get("want_count_status") == ts062.WANT_MISSING_ON_CARD,
            ),
            "source_url": _avail("url", lambda c: bool(c.get("source_url"))),
            "source_item_id": _avail("item_id", lambda c: bool(c.get("source_item_id"))),
        },
        "search_result_eligible": [
            c for c in search if _required_fields_present(c)
        ],
        "filter_simulation_min_want_50": {
            "match": sum(
                1
                for c in search
                if c.get("want_count") is not None and c.get("want_count") >= 50
            ),
            "below_threshold": sum(
                1
                for c in search
                if c.get("want_count") is not None and c.get("want_count") < 50
            ),
            "unknown_null": sum(1 for c in search if c.get("want_count") is None),
            "note": "Simulation only — all observations retained in import set",
        },
        "import_gate": {
            "requires_human_verified": True,
            "requires_search_result": True,
            "min_search_result_with_required_fields": 1,
        },
    }
    report["ready_for_human_review"] = len(report["search_result_eligible"]) >= 1
    return report


def prepare_db_observations(
    normalized: list[dict[str, Any]],
    *,
    run_id: str,
    raw_reference: str | None,
) -> list[dict[str, Any]]:
    """SEARCH_RESULT with required fields only."""
    out: list[dict[str, Any]] = []
    for c in normalized:
        if c.get("result_origin") != ts062.ORIGIN_SEARCH:
            continue
        if not _required_fields_present(c):
            continue
        notes = {
            "result_origin": c.get("result_origin"),
            "want_count_status": c.get("want_count_status"),
            "query": c.get("query"),
            "session_id": c.get("session_id"),
            "entry_import": ENTRY_VERSION,
            "sales_platform": None,
            "not_our_product": True,
        }
        out.append(
            {
                "run_id": run_id,
                "source_id": c.get("source_id") or bridge.SOURCE_ID,
                "source": c.get("source") or bridge.SOURCE,
                "platform": c.get("platform") or bridge.PLATFORM,
                "source_type": "marketplace",
                "source_item_id": c.get("source_item_id"),
                "source_url": c.get("source_url"),
                "title": c.get("title"),
                "price": c.get("price"),
                "currency": c.get("currency") or "CNY",
                "want_count": c.get("want_count"),
                "view_count": c.get("view_count"),
                "comment_count": c.get("comment_count"),
                "share_count": c.get("share_count"),
                "observed_at": c.get("observed_at"),
                "raw_reference": raw_reference,
                "data_origin": msc.ORIGIN_REAL,
                "verification_status": msc.VERIF_UNVERIFIED,
                "collector_version": c.get("collector_version") or bridge.COLLECTOR_VERSION,
                "normalizer_version": msc.NORMALIZER_VERSION,
                "dedupe_key": c.get("dedupe_key"),
                "content_hash": c.get("content_hash"),
                "notes": json.dumps(notes, ensure_ascii=False),
            }
        )
    return out


def import_verified_observations(
    batch: dict[str, Any],
    normalized: list[dict[str, Any]],
    *,
    human_verified: bool = False,
    raw_reference: str | None = None,
) -> dict[str, Any]:
    """
    Write market_observations only when human_verified and SEARCH_RESULT eligible.
    Never writes products / signals / selection_results / market_events.
    """
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = batch.get("run_id") or f"run_{uuid.uuid4().hex[:12]}"
    report = build_verification_report(batch, normalized)
    (ARTIFACT_DIR / "verification_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    result: dict[str, Any] = {
        "entry": "066",
        "run_id": run_id,
        "human_verified": human_verified,
        "verification_report": report,
        "db_write_attempted": False,
        "inserted": 0,
        "skipped": 0,
        "duplicates": 0,
        "errors": [],
    }

    if not human_verified:
        result["status"] = "PENDING_HUMAN_VERIFICATION"
        result["first_real_market_observation"] = False
        (ARTIFACT_DIR / "import_result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return result

    candidates = prepare_db_observations(
        normalized, run_id=run_id, raw_reference=raw_reference
    )
    if not candidates:
        result["status"] = "NO_ELIGIBLE_SEARCH_RESULT"
        result["first_real_market_observation"] = False
        (ARTIFACT_DIR / "import_result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return result

    msc.ensure_market_source_schema()
    collection_run_id = msc.start_collection_run(
        source_id=bridge.SOURCE_ID,
        source=bridge.SOURCE,
        platform=bridge.PLATFORM,
        collection_mode=msc.MODE_LIVE,
        raw_reference=raw_reference,
        notes=f"Entry 066 extension import gate; human_verified={human_verified}",
        collection_query=batch.get("query"),
        acquisition_mode=bridge.MODE,
    )

    inserted = dup = skipped = 0
    for obs in candidates:
        obs["run_id"] = collection_run_id
        obs["verification_status"] = msc.VERIF_MANUAL
        ok, msg = msc.insert_market_observation(obs)
        if ok:
            inserted += 1
        elif msg == "duplicate":
            dup += 1
        else:
            skipped += 1
            result["errors"].append(msg)

    msc.finish_collection_run(
        collection_run_id,
        {
            "raw_count": len(normalized),
            "accepted_count": inserted,
            "rejected_count": skipped,
            "duplicate_count": dup,
            "normalized_count": inserted,
        },
        status="done" if inserted else "partial",
    )

    result.update(
        {
            "db_write_attempted": True,
            "collection_run_id": collection_run_id,
            "inserted": inserted,
            "duplicates": dup,
            "skipped": skipped,
            "status": "IMPORTED" if inserted else "IMPORT_FAILED",
            "first_real_market_observation": inserted > 0,
        }
    )
    (ARTIFACT_DIR / "import_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def process_extension_batch_for_entry(
    batch: dict[str, Any],
    *,
    human_verified: bool = False,
) -> dict[str, Any]:
    """Full pipeline: validate → test sink artifacts → verification → optional DB."""
    sink = bridge.ingest_market_record_batch(batch, test_mode=True)
    if not sink.get("ok"):
        return {"ok": False, "stage": "bridge_validation", **sink}

    normalized = json.loads(
        (bridge.ARTIFACT_DIR / "normalized_preview.json").read_text(encoding="utf-8")
    )
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACT_DIR / "batch.json").write_text(
        json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (ARTIFACT_DIR / "normalized_preview.json").write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    import_result = import_verified_observations(
        batch,
        normalized,
        human_verified=human_verified,
        raw_reference=sink.get("raw_reference"),
    )
    return {
        "ok": True,
        "sink": sink,
        "import": import_result,
        "observation_count_after": msc.count_observations(),
        "observation_count_real_after": msc.count_observations(data_origin=msc.ORIGIN_REAL),
    }
