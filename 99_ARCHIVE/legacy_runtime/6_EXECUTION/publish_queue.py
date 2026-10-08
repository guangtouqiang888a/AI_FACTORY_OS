# 6_EXECUTION/publish_queue.py — Publish Queue + Human External Action Gate
# Entry 052
#
# System: Candidate → Gates → Publish Queue
# Human: External Action (login / publish click / payment / ads)
# Human Gate ≠ Product Approval Gate
# READY ≠ PUBLISHED; PUBLISHED ≠ Commercial Success
# Forbidden: auto platform login / publish / payment / ads

from __future__ import annotations

import hashlib
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402

QUEUE_CANDIDATE = "CANDIDATE"
QUEUE_READY = "READY"
QUEUE_BLOCKED = "BLOCKED"
QUEUE_AWAITING_HUMAN = "AWAITING_HUMAN_ACTION"
QUEUE_PUBLISHED = "PUBLISHED"
QUEUE_REJECTED = "REJECTED"
QUEUE_EXPIRED = "EXPIRED"
QUEUE_CANCELLED = "CANCELLED"

RISK_UNKNOWN = "unknown"
COMMERCIAL_UNAVAILABLE = "unavailable"

VERIFICATION_UNVERIFIED = "UNVERIFIED"
VERIFICATION_VERIFIED = "VERIFIED"
VERIFICATION_MANUAL = "MANUAL_VERIFIED"

REQUIRED_PACKAGE_FILES = (
    "title.txt",
    "description.txt",
    "keywords.txt",
    "faq.txt",
    "delivery_description.txt",
    "version_information.txt",
    "pricing.json",
)


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_publish_queue_schema() -> None:
    with database.get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS publish_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                publish_queue_id TEXT UNIQUE NOT NULL,
                product_id TEXT,
                product_asset_id TEXT,
                product_type TEXT,
                experiment_id TEXT,
                production_request_id TEXT,
                platform TEXT,
                listing_title TEXT,
                price REAL,
                currency TEXT,
                risk_status TEXT,
                quality_status TEXT,
                commercial_status TEXT,
                commercial_score REAL,
                queue_status TEXT NOT NULL,
                blockers TEXT,
                package_path TEXT,
                notes TEXT,
                observation_eligible INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS publish_evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evidence_id TEXT UNIQUE NOT NULL,
                queue_id TEXT NOT NULL,
                platform TEXT,
                listing_reference TEXT,
                published_at TEXT,
                source TEXT,
                verification_status TEXT NOT NULL,
                human_operator TEXT,
                notes TEXT,
                dedupe_key TEXT UNIQUE,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_publish_queue_status
                ON publish_queue(queue_status);
            CREATE INDEX IF NOT EXISTS idx_publish_evidence_queue
                ON publish_evidence(queue_id);
            """
        )
        conn.commit()


def check_publish_package(package_dir: str | Path | None) -> tuple[bool, list[str]]:
    missing: list[str] = []
    if not package_dir:
        return False, ["missing_package_path"]
    path = Path(package_dir)
    if not path.is_dir():
        return False, ["package_path_not_directory"]
    for name in REQUIRED_PACKAGE_FILES:
        if not (path / name).exists():
            missing.append(f"missing_package_file:{name}")
    return len(missing) == 0, missing


def evaluate_publish_gates(candidate: dict) -> dict:
    blockers: list[str] = []

    if not (candidate.get("product_id") or candidate.get("product_asset_id")):
        blockers.append("missing_product_or_asset")
    if not candidate.get("product_asset_id"):
        blockers.append("missing_product_asset")

    quality = str(candidate.get("quality_status") or "").lower()
    if quality in ("failed", "fail", "quality_fail", "rejected"):
        blockers.append("quality_failed")
    elif quality not in ("passed", "pass", "quality_pass", "ok"):
        blockers.append("quality_not_passed")

    if candidate.get("validation_passed") is False:
        blockers.append("production_validation_failed")
    elif candidate.get("validation_status") and str(
        candidate.get("validation_status")
    ).lower() not in ("passed", "pass", "ok"):
        blockers.append("production_validation_failed")

    risk = str(candidate.get("risk_status") or RISK_UNKNOWN).lower()
    if risk in ("failed", "fail", "high", "blocked"):
        blockers.append("risk_failed")
    elif risk in ("unknown", "", "none"):
        blockers.append("risk_unknown")

    commercial = str(candidate.get("commercial_status") or COMMERCIAL_UNAVAILABLE).lower()
    if commercial in ("rejected", "reject", "fail", "failed"):
        blockers.append("commercial_rejected")
    elif commercial in ("unavailable", "missing", "none", ""):
        blockers.append("commercial_unavailable")

    pkg_ok, pkg_missing = check_publish_package(candidate.get("package_path"))
    if not pkg_ok:
        blockers.extend(pkg_missing)

    return {
        "eligible": len(blockers) == 0,
        "blockers": blockers,
        "quality_status": quality or "unknown",
        "risk_status": risk or RISK_UNKNOWN,
        "commercial_status": commercial or COMMERCIAL_UNAVAILABLE,
        "commercial_score": candidate.get("commercial_score"),
        "note": "Commercial Score is eligibility only — not Commercial Success",
    }


def get_queue_entry(publish_queue_id: str) -> dict | None:
    ensure_publish_queue_schema()
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM publish_queue WHERE publish_queue_id = ?",
            (publish_queue_id,),
        ).fetchone()
    return dict(row) if row else None


def list_queue(status: str | None = None) -> list[dict]:
    ensure_publish_queue_schema()
    with database.get_connection() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM publish_queue WHERE queue_status = ? ORDER BY id",
                (status,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM publish_queue ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def enqueue_publish_candidate(candidate: dict) -> dict:
    ensure_publish_queue_schema()
    gates = evaluate_publish_gates(candidate)

    queue_id = candidate.get("publish_queue_id") or f"pq_{uuid.uuid4().hex[:12]}"
    existing = get_queue_entry(queue_id)
    if existing:
        return {
            "accepted": False,
            "reason": "duplicate_queue_id",
            "publish_queue_id": queue_id,
            "existing_status": existing.get("queue_status"),
        }

    asset = candidate.get("product_asset_id")
    platform = candidate.get("platform")
    experiment_id = candidate.get("experiment_id")
    if asset:
        with database.get_connection() as conn:
            row = conn.execute(
                """
                SELECT publish_queue_id, queue_status FROM publish_queue
                WHERE product_asset_id = ?
                  AND IFNULL(platform,'') = IFNULL(?, '')
                  AND IFNULL(experiment_id,'') = IFNULL(?, '')
                  AND queue_status NOT IN ('PUBLISHED','REJECTED','EXPIRED','CANCELLED')
                LIMIT 1
                """,
                (asset, platform, experiment_id),
            ).fetchone()
        if row:
            return {
                "accepted": False,
                "reason": "duplicate_active_queue_entry",
                "publish_queue_id": row["publish_queue_id"],
                "existing_status": row["queue_status"],
            }

    if gates["eligible"]:
        want_human = bool(candidate.get("enter_human_gate")) or (
            candidate.get("target_status") == QUEUE_AWAITING_HUMAN
        )
        status = QUEUE_AWAITING_HUMAN if want_human else QUEUE_READY
        blockers: list[str] = []
    else:
        status = QUEUE_BLOCKED
        blockers = list(gates["blockers"])

    now = _now_str()
    record = {
        "publish_queue_id": queue_id,
        "product_id": candidate.get("product_id"),
        "product_asset_id": candidate.get("product_asset_id"),
        "product_type": candidate.get("product_type") or "document",
        "experiment_id": candidate.get("experiment_id"),
        "production_request_id": candidate.get("production_request_id"),
        "platform": platform,
        "listing_title": candidate.get("listing_title"),
        "price": candidate.get("price"),
        "currency": candidate.get("currency") or "CNY",
        "risk_status": gates["risk_status"],
        "quality_status": gates["quality_status"],
        "commercial_status": gates["commercial_status"],
        "commercial_score": gates.get("commercial_score"),
        "queue_status": status,
        "blockers": json.dumps(blockers, ensure_ascii=False),
        "package_path": str(candidate.get("package_path") or ""),
        "notes": candidate.get("notes") or gates.get("note"),
        "observation_eligible": 0,
        "created_at": now,
        "updated_at": now,
    }
    cols = list(record.keys())
    with database.get_connection() as conn:
        conn.execute(
            f"INSERT INTO publish_queue ({', '.join(cols)}) "
            f"VALUES ({', '.join('?' * len(cols))})",
            [record[c] for c in cols],
        )
        conn.commit()

    return {
        "accepted": True,
        "publish_queue_id": queue_id,
        "queue_status": status,
        "blockers": blockers,
        "gates": gates,
        "published": False,
        "commercial_success": False,
        "auto_external_publish": False,
    }


def advance_to_awaiting_human(publish_queue_id: str) -> dict:
    entry = get_queue_entry(publish_queue_id)
    if not entry:
        return {"ok": False, "reason": "queue_not_found"}
    if entry["queue_status"] == QUEUE_AWAITING_HUMAN:
        return {"ok": True, "reason": "already_awaiting_human", "entry": entry}
    if entry["queue_status"] != QUEUE_READY:
        return {
            "ok": False,
            "reason": f"invalid_transition_from_{entry['queue_status']}",
        }
    now = _now_str()
    with database.get_connection() as conn:
        conn.execute(
            """UPDATE publish_queue
               SET queue_status=?, updated_at=?
               WHERE publish_queue_id=?""",
            (QUEUE_AWAITING_HUMAN, now, publish_queue_id),
        )
        conn.commit()
    return {
        "ok": True,
        "queue_status": QUEUE_AWAITING_HUMAN,
        "note": "Human External Action Gate — no auto publish",
    }


def _evidence_dedupe_key(payload: dict) -> str:
    material = "|".join([
        str(payload.get("queue_id") or ""),
        str(payload.get("platform") or "").lower(),
        str(payload.get("listing_reference") or ""),
        str(payload.get("published_at") or ""),
    ])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:32]


def record_publish_evidence(payload: dict) -> dict:
    ensure_publish_queue_schema()
    queue_id = payload.get("queue_id") or payload.get("publish_queue_id")
    if not queue_id:
        return {"accepted": False, "reason": "missing_queue_id"}

    entry = get_queue_entry(queue_id)
    if not entry:
        return {"accepted": False, "reason": "queue_not_found"}
    if entry["queue_status"] in (QUEUE_REJECTED, QUEUE_CANCELLED, QUEUE_EXPIRED):
        return {"accepted": False, "reason": f"queue_terminal_{entry['queue_status']}"}

    listing_ref = payload.get("listing_reference")
    if not listing_ref or str(listing_ref).strip() == "":
        return {"accepted": False, "reason": "missing_listing_reference"}

    vstatus = str(payload.get("verification_status") or VERIFICATION_UNVERIFIED).upper()
    if vstatus not in (
        VERIFICATION_UNVERIFIED,
        VERIFICATION_VERIFIED,
        VERIFICATION_MANUAL,
    ):
        return {"accepted": False, "reason": "invalid_verification_status"}
    if vstatus == VERIFICATION_UNVERIFIED:
        return {
            "accepted": False,
            "reason": "unverified_evidence_rejected",
            "commercial_success": False,
        }

    dedupe = _evidence_dedupe_key({**payload, "queue_id": queue_id})
    with database.get_connection() as conn:
        dup = conn.execute(
            "SELECT evidence_id FROM publish_evidence WHERE dedupe_key = ?",
            (dedupe,),
        ).fetchone()
    if dup:
        return {
            "accepted": False,
            "reason": "duplicate_evidence",
            "evidence_id": dup["evidence_id"],
        }

    evidence_id = payload.get("evidence_id") or f"pev_{uuid.uuid4().hex[:12]}"
    now = _now_str()
    with database.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO publish_evidence (
                evidence_id, queue_id, platform, listing_reference,
                published_at, source, verification_status, human_operator,
                notes, dedupe_key, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evidence_id,
                queue_id,
                payload.get("platform") or entry.get("platform"),
                listing_ref,
                payload.get("published_at") or now,
                payload.get("source") or "human_manual_entry",
                vstatus,
                payload.get("human_operator"),
                payload.get("notes"),
                dedupe,
                now,
            ),
        )
        conn.execute(
            """
            UPDATE publish_queue
            SET queue_status=?, observation_eligible=1, updated_at=?,
                platform=COALESCE(?, platform)
            WHERE publish_queue_id=?
            """,
            (QUEUE_PUBLISHED, now, payload.get("platform"), queue_id),
        )
        conn.commit()

    return {
        "accepted": True,
        "evidence_id": evidence_id,
        "queue_status": QUEUE_PUBLISHED,
        "observation_eligible": True,
        "observation_started": False,
        "commercial_success": False,
        "note": (
            "Publish Evidence recorded. Observation Eligible only — "
            "Observation Start is a separate Entry. Not Commercial Success."
        ),
    }


def get_human_action_pack(publish_queue_id: str) -> dict:
    entry = get_queue_entry(publish_queue_id)
    if not entry:
        return {"ok": False, "reason": "queue_not_found"}
    return {
        "ok": True,
        "queue_status": entry.get("queue_status"),
        "platform": entry.get("platform"),
        "suggested_price": entry.get("price"),
        "currency": entry.get("currency"),
        "listing_title": entry.get("listing_title"),
        "product_asset_id": entry.get("product_asset_id"),
        "experiment_id": entry.get("experiment_id"),
        "risk_status": entry.get("risk_status"),
        "quality_status": entry.get("quality_status"),
        "commercial_status": entry.get("commercial_status"),
        "package_path": entry.get("package_path"),
        "forbidden": [
            "auto_platform_login",
            "auto_publish_click",
            "auto_payment",
            "auto_advertisement",
        ],
        "required_next": "human_external_publish_then_record_publish_evidence",
    }


def build_pilot_candidate() -> dict:
    package = (
        ROOT
        / "commercial_assets"
        / "pilot_outputs"
        / "preq_20260712_005"
        / "artifacts"
        / "package"
        / "publish_package"
    )
    title = ""
    if (package / "title.txt").exists():
        title = (package / "title.txt").read_text(encoding="utf-8").strip().splitlines()[0]
    return {
        "publish_queue_id": "pq_pilot_preq_20260712_005",
        "product_id": "pilot_excel_attendance",
        "product_asset_id": "8523329941d4",
        "product_type": "document",
        "experiment_id": "exp_20260708_005",
        "production_request_id": "preq_20260712_005",
        "platform": "taobao",
        "listing_title": title or "Excel考勤记录表",
        "price": 12.9,
        "currency": "CNY",
        "quality_status": "passed",
        "validation_status": "passed",
        "validation_passed": True,
        "risk_status": "passed",
        "commercial_status": "acceptable",
        "commercial_score": 80.0,
        "package_path": str(package),
        "enter_human_gate": True,
        "notes": (
            "Pilot Entry 052: AWAITING_HUMAN_ACTION. "
            "Observation remains NOT_STARTED until verified Publish Evidence "
            "and a future Observation Entry. Price 12.9 = AI recommendation only."
        ),
    }


def enqueue_pilot_awaiting_human() -> dict:
    candidate = build_pilot_candidate()
    existing = get_queue_entry(candidate["publish_queue_id"])
    if existing:
        return {
            "accepted": True,
            "already_present": True,
            "publish_queue_id": existing["publish_queue_id"],
            "queue_status": existing["queue_status"],
            "published": existing["queue_status"] == QUEUE_PUBLISHED,
            "commercial_success": False,
        }
    return enqueue_publish_candidate(candidate)
