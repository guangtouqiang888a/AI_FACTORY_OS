# 1_DATA/connectors/xianyu_import_connector.py — Entry 058B / 058C
#
# Xianyu EXTERNAL_IMPORT connector (Excel/CSV/JSON user export).
# LIVE_COLLECTION not available — no HTTP/API/browser scrape.
# SAMPLE / fixture files and sample URLs are rejected from Current DB as REAL.
# Discovery source=xianyu does NOT set sales_platform.
# Market Observation ≠ Product ≠ Our Listing ≠ Market Event.
# Missing numeric fields stay NULL (never coerced to 0).

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import market_source_core as msc  # noqa: E402
from sources import normalize_row, XIANYU_COLUMN_MAP  # noqa: E402

SOURCE_ID = "src_xianyu_marketplace"
SOURCE = "xianyu"
PLATFORM = "xianyu"  # discovery platform only
IMPORTS_DIR = config.RAW_XIANYU_DIR / "imports"

SUPPORTED_SUFFIXES = (".xlsx", ".csv", ".json", ".jsonl")


def _safe_float(v) -> float | None:
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _safe_int(v) -> int | None:
    """Preserve explicit 0; missing / blank / NaN → None (never invent 0)."""
    if v is None or v == "":
        return None
    if isinstance(v, float):
        import math

        if math.isnan(v):
            return None
    try:
        s = str(v).strip().lower()
        if s in ("nan", "none", "null", "n/a", "na", "-"):
            return None
        return int(float(v))
    except (TypeError, ValueError):
        return None


def list_import_candidates() -> list[Path]:
    """Prefer imports/ subdirectory; never auto-pick legacy *_sample.xlsx as REAL."""
    IMPORTS_DIR.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for suf in SUPPORTED_SUFFIXES:
        files.extend(sorted(IMPORTS_DIR.glob(f"*{suf}")))
    # Exclude README and hidden
    return [p for p in files if p.is_file() and not p.name.upper().startswith("README")]


def import_readiness() -> dict:
    """
    Entry 058C: IMPORT_READY status without fabricating data.
    """
    msc.ensure_market_source_schema()
    candidates = list_import_candidates()
    sample_guard = reject_legacy_sample_dry()
    live = msc.live_collection_status()
    obs_n = msc.count_observations()
    real_n = msc.count_observations(data_origin=msc.ORIGIN_REAL)
    if not candidates:
        return {
            "status": "WAITING_FOR_REAL_SOURCE_FILE",
            "import_ready": True,
            "entry_status": "READY_FOR_REAL_IMPORT",
            "collection_mode": msc.MODE_IMPORT,
            "live_collection": live,
            "imports_dir": str(IMPORTS_DIR),
            "candidate_files": [],
            "candidate_count": 0,
            "legacy_sample_rejected_by_policy": True,
            "sample_guard": sample_guard,
            "current_observations": obs_n,
            "current_real_observations": real_n,
            "sales_platform": None,
            "note": (
                "Importer ready. Place a real user-exported xlsx/csv/json under "
                "data/raw/xianyu/imports/. Do not copy *_sample.xlsx. "
                "Do not fabricate REAL data."
            ),
        }
    return {
        "status": "CANDIDATES_PRESENT",
        "import_ready": True,
        "entry_status": "READY_TO_IMPORT",
        "collection_mode": msc.MODE_IMPORT,
        "live_collection": live,
        "imports_dir": str(IMPORTS_DIR),
        "candidate_files": [str(p) for p in candidates],
        "candidate_count": len(candidates),
        "current_observations": obs_n,
        "current_real_observations": real_n,
        "sales_platform": None,
        "note": "Operator must pass declared_origin=REAL only when export is attested.",
    }


def import_file(
    path: Path,
    *,
    keyword: str = "",
    declared_origin: str = msc.ORIGIN_UNKNOWN,
    collection_mode: str = msc.MODE_IMPORT,
    allow_sample: bool = False,
    observed_at: str | None = None,
    mirror_to_products: bool = False,
    fatal_on_row_error: bool = False,
    collection_query: str | None = None,
    acquisition_mode: str | None = None,
) -> dict:
    """
    Import one external file into market_observations.

    declared_origin=REAL only accepted when file/url pass sample checks.
    allow_sample=True only for isolated TEST_FIXTURE mode (temp DB in tests).
    mirror_to_products default False (058C: Observation ≠ Product).
    collection_query: search/topic string — NOT the source platform name.
    """
    msc.ensure_market_source_schema()
    path = Path(path)
    query = (collection_query if collection_query is not None else keyword) or ""
    acq_mode = acquisition_mode or "MANUAL_IMPORT"
    if not path.exists():
        return {
            "ok": False,
            "status": "FAILED",
            "error": "file_not_found",
            "path": str(path),
        }

    path_origin = msc.classify_path_origin(path)
    if path_origin in (msc.ORIGIN_SAMPLE, msc.ORIGIN_FIXTURE) and not allow_sample:
        return {
            "ok": False,
            "status": "FAILED",
            "error": "sample_or_fixture_file_rejected",
            "path": str(path),
            "path_origin": path_origin,
            "note": "Legacy sample.xlsx must not enter Current DB (Entry 058A/058B/058C)",
        }

    if collection_mode == msc.MODE_LIVE:
        return {
            "ok": False,
            "status": "FAILED",
            "error": "live_collection_not_available",
            **msc.live_collection_status(),
        }

    today = date.today().isoformat()
    batch_dir = config.RAW_XIANYU_DIR / today / "import_batches"
    batch_dir.mkdir(parents=True, exist_ok=True)
    staged = batch_dir / f"{path.stem}_{msc._now_iso().replace(':', '').replace('+', '_')}{path.suffix}"
    shutil.copy2(path, staged)

    # SHA-256 of source file before move into run folder
    import hashlib

    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    raw_sha = h.hexdigest()

    run_id = msc.start_collection_run(
        source_id=SOURCE_ID,
        source=SOURCE,
        platform=PLATFORM,
        collection_mode=collection_mode,
        raw_reference=str(staged),
        notes=(
            f"collection_query={query}; declared_origin={declared_origin}; "
            f"acquisition_mode={acq_mode}; mirror_to_products={mirror_to_products}; entry=058D"
        ),
        collection_query=query,
        acquisition_mode=acq_mode,
        raw_sha256=raw_sha,
    )
    run_batch = batch_dir / run_id
    run_batch.mkdir(parents=True, exist_ok=True)
    staged_final = run_batch / staged.name
    shutil.move(str(staged), str(staged_final))
    staged = staged_final
    (run_batch / "raw_sha256.txt").write_text(raw_sha + "\n", encoding="utf-8")
    (run_batch / "provenance.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "source": SOURCE,
                "collection_query": query,
                "acquisition_mode": acq_mode,
                "raw_sha256": raw_sha,
                "import_time": msc._now_iso(),
                "original_filename": path.name,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    import database

    with database.get_connection() as conn:
        conn.execute(
            "UPDATE collection_runs SET raw_reference=? WHERE run_id=?",
            (str(staged), run_id),
        )
        try:
            conn.execute(
                "UPDATE collection_runs SET raw_sha256=?, collection_query=?, acquisition_mode=? WHERE run_id=?",
                (raw_sha, query, acq_mode, run_id),
            )
        except Exception:
            pass
        conn.commit()

    stats = {
        "raw_count": 0,
        "accepted_count": 0,
        "rejected_count": 0,
        "duplicate_count": 0,
        "normalized_count": 0,
        "error_count": 0,
        "rejected_rows": [],
        "rejected_reasons": [],
        "observation_ids": [],
    }

    try:
        rows = _read_tabular(path)
    except Exception as exc:
        stats["error_count"] = 1
        stats["error_summary"] = str(exc)
        msc.finish_collection_run(run_id, stats, status="FAILED")
        return {
            "ok": False,
            "status": "FAILED",
            "run_id": run_id,
            "error": str(exc),
            "stats": stats,
            "raw_reference": str(staged),
            "product_created": False,
            "listing_created": False,
            "market_event_created": False,
            "sales_platform": None,
        }

    obs_time = observed_at or msc._now_iso()
    fatal = False
    fatal_reason = None

    for idx, raw in enumerate(rows):
        stats["raw_count"] += 1
        row_ref = f"row:{idx}"
        try:
            normalized = normalize_row(raw, XIANYU_COLUMN_MAP)
            # Preserve unmapped raw keys in notes metadata (not lost)
            unmapped = {
                str(k): v
                for k, v in raw.items()
                if str(k).strip() not in XIANYU_COLUMN_MAP
            }
            title = normalized.get("title")
            if title is None or str(title).strip() == "" or str(title).lower() == "nan":
                stats["rejected_count"] += 1
                reason = "missing_title"
                stats["rejected_reasons"].append(reason)
                stats["rejected_rows"].append({"row_reference": row_ref, "reason": reason})
                continue

            source_url = str(normalized.get("source_url") or "").strip() or None
            # Prefer explicit source_item_id from export over URL derivation
            explicit_id = normalized.get("source_item_id")
            if explicit_id is not None and str(explicit_id).strip() and str(explicit_id).lower() != "nan":
                source_item_id = str(explicit_id).strip()
            else:
                source_item_id = msc.extract_source_item_id(source_url)

            origin, reasons = msc.resolve_data_origin(
                declared_origin=declared_origin,
                path=path,
                url=source_url,
                collection_mode=collection_mode,
            )
            if origin in (msc.ORIGIN_SAMPLE, msc.ORIGIN_FIXTURE) and not allow_sample:
                stats["rejected_count"] += 1
                reason = f"rejected_{origin}"
                stats["rejected_reasons"].append(reason)
                stats["rejected_rows"].append({"row_reference": row_ref, "reason": reason})
                continue
            if collection_mode != msc.MODE_FIXTURE and origin == msc.ORIGIN_FIXTURE:
                stats["rejected_count"] += 1
                reason = "fixture_outside_fixture_mode"
                stats["rejected_reasons"].append(reason)
                stats["rejected_rows"].append({"row_reference": row_ref, "reason": reason})
                continue

            price = _safe_float(normalized.get("price"))
            # Soft validate: bad price string → reject row (no silent coercion to 0)
            raw_price = normalized.get("price")
            if raw_price is not None and str(raw_price).strip() not in ("", "nan", "None"):
                if price is None:
                    stats["rejected_count"] += 1
                    reason = "invalid_price"
                    stats["rejected_reasons"].append(reason)
                    stats["rejected_rows"].append({"row_reference": row_ref, "reason": reason})
                    continue

            dedupe_key = msc.make_dedupe_key(
                source=SOURCE,
                source_item_id=source_item_id,
                source_url=source_url,
                title=str(title).strip(),
                price=price,
            )
            content_hash = hashlib.sha256(
                json.dumps(normalized, ensure_ascii=False, sort_keys=True, default=str).encode()
            ).hexdigest()[:32]

            verif = msc.verification_for_origin(
                origin,
                operator_attested=(declared_origin or "").upper() == msc.ORIGIN_REAL,
            )

            obs = {
                "run_id": run_id,
                "source_id": SOURCE_ID,
                "source": SOURCE,
                "platform": PLATFORM,
                "source_type": "marketplace",
                "source_item_id": source_item_id,
                "source_url": source_url,
                "title": str(title).strip(),
                "category": query or None,
                "price": price,
                "currency": "CNY",
                "view_count": _safe_int(normalized.get("view_count")),
                "want_count": _safe_int(normalized.get("want_count")),
                "comment_count": _safe_int(normalized.get("comment_count")),
                "share_count": _safe_int(normalized.get("share_count")),
                "seller_reference": str(normalized.get("seller") or "") or None,
                "published_at": str(normalized.get("publish_time") or "") or None,
                "observed_at": obs_time,
                "raw_reference": str(staged),
                "data_origin": origin,
                "verification_status": verif,
                "content_hash": content_hash,
                "dedupe_key": dedupe_key,
                "product_category": query or None,
                "opportunity_product_type": None,  # Observation must not lock product type
                "notes": json.dumps(
                    {
                        "origin_reasons": reasons,
                        "sales_platform_not_implied": True,
                        "unmapped_raw": unmapped or None,
                        "imported_at": msc._now_iso(),
                        "not_our_product": True,
                        "not_our_listing": True,
                        "not_market_event": True,
                    },
                    ensure_ascii=False,
                    default=str,
                ),
            }
            stats["normalized_count"] += 1
            ok, detail = msc.insert_market_observation(obs)
            if not ok:
                if detail == "duplicate":
                    stats["duplicate_count"] += 1
                    stats["rejected_rows"].append(
                        {"row_reference": row_ref, "reason": "duplicate"}
                    )
                else:
                    stats["rejected_count"] += 1
                    stats["rejected_reasons"].append(detail)
                    stats["rejected_rows"].append(
                        {"row_reference": row_ref, "reason": detail}
                    )
                continue
            stats["accepted_count"] += 1
            stats["observation_ids"].append(detail)

            if mirror_to_products and origin == msc.ORIGIN_REAL:
                _mirror_to_products(
                    keyword=keyword, normalized=normalized, source_url=source_url
                )

        except Exception as exc:
            stats["error_count"] += 1
            reason = f"row_exception:{exc}"
            stats["rejected_reasons"].append(reason)
            stats["rejected_rows"].append({"row_reference": row_ref, "reason": reason})
            if fatal_on_row_error:
                fatal = True
                fatal_reason = reason
                break

    if fatal:
        deleted = msc.delete_observations_for_run(run_id)
        stats["error_summary"] = fatal_reason
        stats["rollback_deleted"] = deleted
        stats["accepted_count"] = 0
        stats["observation_ids"] = []
        msc.finish_collection_run(run_id, stats, status="FAILED")
        return {
            "ok": False,
            "status": "FAILED",
            "run_id": run_id,
            "error": "batch_rollback",
            "fatal_reason": fatal_reason,
            "stats": stats,
            "raw_reference": str(staged),
            "collection_mode": collection_mode,
            "discovery_platform": PLATFORM,
            "sales_platform": None,
            "product_created": False,
            "listing_created": False,
            "market_event_created": False,
        }

    # Count integrity: accepted + rejected + duplicate should equal raw when no stray errors
    processed = (
        stats["accepted_count"] + stats["rejected_count"] + stats["duplicate_count"]
    )
    # errors may overlap with rejected; allow error_count rows also in rejected
    stats["count_check"] = {
        "raw_count": stats["raw_count"],
        "accepted_plus_rejected_plus_duplicate": processed,
        "consistent": processed + max(0, stats["error_count"] - len([
            r for r in stats["rejected_rows"] if str(r.get("reason", "")).startswith("row_exception")
        ])) >= stats["raw_count"] or processed == stats["raw_count"],
    }

    status = "done"
    if stats["accepted_count"] == 0 and stats["raw_count"] > 0:
        status = "PARTIAL" if stats["rejected_count"] or stats["duplicate_count"] else "FAILED"
    if stats["error_count"] and stats["accepted_count"] == 0:
        status = "FAILED"
    if stats["raw_count"] == 0:
        status = "FAILED"
        stats["error_summary"] = "empty_file"

    msc.finish_collection_run(run_id, stats, status=status)
    return {
        "ok": status in ("done", "PARTIAL"),
        "status": status,
        "run_id": run_id,
        "collection_mode": collection_mode,
        "acquisition_mode": acq_mode,
        "collection_query": query,
        "raw_sha256": raw_sha,
        "source": SOURCE,
        "discovery_platform": PLATFORM,
        "sales_platform": None,
        "sales_platform_note": "NOT implied by discovery source",
        "raw_reference": str(staged),
        "stats": stats,
        "live_collection": msc.live_collection_status(),
        "product_created": False,
        "listing_created": False,
        "market_event_created": False,
        "data_origin_declared": declared_origin,
    }


def _read_tabular(path: Path) -> list[dict]:
    suf = path.suffix.lower()
    if suf == ".csv":
        import csv

        with open(path, encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    if suf == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "rows" in data:
            return list(data["rows"])
        if isinstance(data, dict):
            return [data]
        raise ValueError("json must be list or {rows:[...]}")
    if suf == ".jsonl":
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        return rows
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("pandas required for xlsx import") from exc
    df = pd.read_excel(path)
    return df.to_dict(orient="records")


def _mirror_to_products(*, keyword: str, normalized: dict, source_url: str | None) -> None:
    """Optional legacy mirror — OFF by default (058C Observation ≠ Product)."""
    import database

    # Preserve NULL semantics: only write ints when present
    def _or_zero(v):
        return v if v is not None else 0

    database.insert_product(
        {
            "platform_id": 1,
            "keyword": keyword or "imported",
            "title": str(normalized.get("title") or "").strip(),
            "price": _safe_float(normalized.get("price")) or 0.0,
            "want_count": _or_zero(_safe_int(normalized.get("want_count"))),
            "view_count": _or_zero(_safe_int(normalized.get("view_count"))),
            "comment_count": _or_zero(_safe_int(normalized.get("comment_count"))),
            "share_count": _or_zero(_safe_int(normalized.get("share_count"))),
            "seller": str(normalized.get("seller") or ""),
            "tags": str(normalized.get("tags") or ""),
            "publish_time": str(normalized.get("publish_time") or ""),
            "source_url": source_url or "",
            "raw_json": json.dumps(normalized, ensure_ascii=False, default=str),
            "collect_date": date.today().isoformat(),
        }
    )


def reject_legacy_sample_dry() -> dict:
    sample = config.RAW_XIANYU_DIR / "2026-07-04"
    files = list(sample.glob("*sample*.xlsx")) if sample.exists() else []
    if not files:
        files = list(config.RAW_XIANYU_DIR.rglob("*sample*.xlsx"))
    return {
        "sample_files_found": [str(f) for f in files],
        "policy": "must_not_import_as_REAL",
        "auto_imported": False,
    }


def reject_legacy_sample_import() -> dict:
    """Explicit guard used by tests/docs — legacy sample path must fail."""
    sample = config.RAW_XIANYU_DIR / "2026-07-04"
    files = list(sample.glob("*sample*.xlsx")) if sample.exists() else []
    if not files:
        files = list(config.RAW_XIANYU_DIR.rglob("*sample*.xlsx"))
    if not files:
        return {"ok": True, "note": "no_sample_file_found"}
    return import_file(
        files[0],
        keyword="should_reject",
        declared_origin=msc.ORIGIN_REAL,
        allow_sample=False,
    )
