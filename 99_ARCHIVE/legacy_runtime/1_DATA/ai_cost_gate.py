# 1_DATA/ai_cost_gate.py — Entry 067 Minimal AI Cost Gate
#
# Control AI_COST (estimated/actual), NOT call_count as the primary metric.
# No paid model invocation in this Entry.
# Product Creation Capability = unified skill boundary (not split Design/Production agents).
# ModelSelector = interface only (manual/configured).

from __future__ import annotations

import json
import sqlite3
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import database  # noqa: E402

COST_GATE_VERSION = "067.1.0"

STATUS_PASS = "PASS"
STATUS_BLOCKED = "BLOCKED"
STATUS_REDESIGN_REQUIRED = "REDESIGN_REQUIRED"
STATUS_UNKNOWN = "UNKNOWN"

BASIS_ESTIMATE = "ESTIMATE"
BASIS_ACTUAL = "ACTUAL"
BASIS_HYPOTHESIS = "HYPOTHESIS"

# Reserved skills — not Agent implementations
SKILL_MARKET_ANALYSIS = "market_analysis"
SKILL_PRODUCT_CREATION = "product_creation"
SKILL_DOCUMENT_GENERATION = "document_generation"
SKILL_IMAGE_GENERATION = "image_generation"
SKILL_LISTING_ADAPTATION = "listing_adaptation"

AI_SKILLS = frozenset(
    {
        SKILL_MARKET_ANALYSIS,
        SKILL_PRODUCT_CREATION,
        SKILL_DOCUMENT_GENERATION,
        SKILL_IMAGE_GENERATION,
        SKILL_LISTING_ADAPTATION,
    }
)

# Future cost ledger dimensions — reserved, not implemented as full ledger
COST_LEDGER_RESERVED = (
    "product_cost",
    "ai_cost",
    "human_cost",
    "platform_cost",
    "payment_cost",
    "advertising_cost",
    "total_cost",
)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_ai_cost_schema() -> None:
    """Additive only — CREATE IF NOT EXISTS. No destructive migration."""
    with database.get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS ai_cost_estimates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estimate_id TEXT UNIQUE NOT NULL,
                task_id TEXT,
                product_or_project_id TEXT,
                skill TEXT NOT NULL,
                model TEXT,
                estimated_cost REAL,
                currency TEXT NOT NULL DEFAULT 'CNY',
                cost_basis TEXT NOT NULL,
                estimated_revenue REAL,
                revenue_basis TEXT,
                allowed_cost REAL,
                margin_floor REAL,
                call_count INTEGER,
                status TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS ai_execution_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_id TEXT UNIQUE NOT NULL,
                task_id TEXT,
                skill TEXT NOT NULL,
                model TEXT,
                estimated_cost REAL,
                actual_cost REAL,
                currency TEXT NOT NULL DEFAULT 'CNY',
                call_count INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                paid_invocation INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                notes TEXT
            );
            """
        )
        conn.commit()


def derive_allowed_cost(
    *,
    explicit_allowed_cost: float | None = None,
    estimated_revenue: float | None = None,
    margin_floor: float | None = None,
) -> dict[str, Any]:
    """
    allowed_cost from explicit input OR derived hypothesis.
    Never treat derived values as ACTUAL economics.
    """
    if explicit_allowed_cost is not None:
        return {
            "allowed_cost": float(explicit_allowed_cost),
            "derivation": "EXPLICIT",
            "cost_basis": BASIS_ESTIMATE,
            "hypothesis": False,
        }
    if estimated_revenue is not None and margin_floor is not None:
        # allowed AI spend ≤ revenue * (1 - margin_floor) — HYPOTHESIS only
        allowed = float(estimated_revenue) * (1.0 - float(margin_floor))
        return {
            "allowed_cost": max(0.0, allowed),
            "derivation": "REVENUE_MARGIN_FLOOR",
            "cost_basis": BASIS_HYPOTHESIS,
            "hypothesis": True,
            "formula": "estimated_revenue * (1 - margin_floor)",
            "note": "HYPOTHESIS — not real revenue or real margin",
        }
    return {
        "allowed_cost": None,
        "derivation": "UNAVAILABLE",
        "cost_basis": BASIS_ESTIMATE,
        "hypothesis": False,
        "note": "Cannot derive allowed_cost; gate status UNKNOWN",
    }


def evaluate_cost_gate(
    *,
    estimated_cost: float | None,
    allowed_cost: float | None,
) -> dict[str, Any]:
    """
    estimated_cost <= allowed_cost → PASS
    estimated_cost > allowed_cost → BLOCKED / REDESIGN_REQUIRED
    Unknown either side → UNKNOWN (never assume 0)
    """
    if estimated_cost is None or allowed_cost is None:
        return {
            "status": STATUS_UNKNOWN,
            "estimated_cost": estimated_cost,
            "allowed_cost": allowed_cost,
            "reason": "unknown_cost_or_budget",
            "note": "NULL cost ≠ 0; do not auto-pass",
        }
    if float(estimated_cost) <= float(allowed_cost):
        return {
            "status": STATUS_PASS,
            "estimated_cost": float(estimated_cost),
            "allowed_cost": float(allowed_cost),
            "reason": "within_budget",
        }
    return {
        "status": STATUS_BLOCKED,
        "gate_action": STATUS_REDESIGN_REQUIRED,
        "estimated_cost": float(estimated_cost),
        "allowed_cost": float(allowed_cost),
        "reason": "budget_exceeded",
        "note": "Do not continue spending; redesign required",
    }


def create_cost_estimate(
    *,
    task_id: str | None = None,
    product_or_project_id: str | None = None,
    skill: str,
    model: str | None = None,
    estimated_cost: float | None = None,
    currency: str = "CNY",
    estimated_revenue: float | None = None,
    allowed_cost: float | None = None,
    margin_floor: float | None = None,
    call_count: int | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    """
    Persist AICostEstimate. call_count is optional metadata — not the control metric.
    No paid model invocation.
    """
    ensure_ai_cost_schema()
    if skill not in AI_SKILLS:
        raise ValueError(f"unknown_skill:{skill}")

    derived = derive_allowed_cost(
        explicit_allowed_cost=allowed_cost,
        estimated_revenue=estimated_revenue,
        margin_floor=margin_floor,
    )
    effective_allowed = derived["allowed_cost"]
    gate = evaluate_cost_gate(
        estimated_cost=estimated_cost,
        allowed_cost=effective_allowed,
    )

    revenue_basis = None
    if estimated_revenue is not None:
        revenue_basis = BASIS_HYPOTHESIS  # never ACTUAL without sales evidence

    cost_basis = BASIS_ESTIMATE if estimated_cost is not None else STATUS_UNKNOWN
    if estimated_cost is None:
        cost_basis = STATUS_UNKNOWN

    estimate_id = f"aicost_{uuid.uuid4().hex[:12]}"
    now = _now()
    payload = {
        "estimate_id": estimate_id,
        "task_id": task_id,
        "product_or_project_id": product_or_project_id,
        "skill": skill,
        "model": model,
        "estimated_cost": estimated_cost,
        "currency": currency,
        "cost_basis": cost_basis,
        "estimated_revenue": estimated_revenue,
        "revenue_basis": revenue_basis,
        "allowed_cost": effective_allowed,
        "allowed_cost_derivation": derived,
        "margin_floor": margin_floor,
        "call_count": call_count,
        "status": gate["status"],
        "gate": gate,
        "notes": notes,
        "created_at": now,
        "paid_invocation": False,
        "economics_claim": "ESTIMATE_ONLY",
    }

    with database.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO ai_cost_estimates (
                estimate_id, task_id, product_or_project_id, skill, model,
                estimated_cost, currency, cost_basis, estimated_revenue,
                revenue_basis, allowed_cost, margin_floor, call_count,
                status, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                estimate_id,
                task_id,
                product_or_project_id,
                skill,
                model,
                estimated_cost,
                currency,
                cost_basis,
                estimated_revenue,
                revenue_basis,
                effective_allowed,
                margin_floor,
                call_count,
                gate["status"],
                json.dumps(
                    {
                        "notes": notes,
                        "gate": gate,
                        "allowed_cost_derivation": derived,
                        "economics_claim": "ESTIMATE_ONLY",
                    },
                    ensure_ascii=False,
                ),
                now,
            ),
        )
        conn.commit()
    return payload


def record_ai_execution(
    *,
    task_id: str | None = None,
    skill: str,
    model: str | None = None,
    estimated_cost: float | None = None,
    actual_cost: float | None = None,
    currency: str = "CNY",
    call_count: int = 0,
    status: str = "RECORDED",
    notes: str | None = None,
) -> dict[str, Any]:
    """
    Log execution metadata. paid_invocation always False in Entry 067.
    Distinguishes ESTIMATE vs ACTUAL costs.
    """
    ensure_ai_cost_schema()
    if skill not in AI_SKILLS:
        raise ValueError(f"unknown_skill:{skill}")
    execution_id = f"aiex_{uuid.uuid4().hex[:12]}"
    now = _now()
    with database.get_connection() as conn:
        conn.execute(
            """
            INSERT INTO ai_execution_records (
                execution_id, task_id, skill, model, estimated_cost, actual_cost,
                currency, call_count, status, paid_invocation, created_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (
                execution_id,
                task_id,
                skill,
                model,
                estimated_cost,
                actual_cost,
                currency,
                call_count,
                status,
                now,
                notes,
            ),
        )
        conn.commit()
    return {
        "execution_id": execution_id,
        "task_id": task_id,
        "skill": skill,
        "model": model,
        "estimated_cost": estimated_cost,
        "actual_cost": actual_cost,
        "cost_basis_estimated": BASIS_ESTIMATE if estimated_cost is not None else STATUS_UNKNOWN,
        "cost_basis_actual": BASIS_ACTUAL if actual_cost is not None else STATUS_UNKNOWN,
        "currency": currency,
        "call_count": call_count,
        "status": status,
        "paid_invocation": False,
        "created_at": now,
        "note": "call_count is metadata; control metric is cost",
    }


class ModelSelector:
    """
    Interface only — manual/configured selection.
    Future: cost-aware Model Router (NOT built).
    """

    def __init__(self, *, configured_model: str | None = None):
        self.configured_model = configured_model

    def select(
        self,
        *,
        skill: str,
        candidates: list[str] | None = None,
        prefer_cost: bool = False,
    ) -> dict[str, Any]:
        if skill not in AI_SKILLS:
            raise ValueError(f"unknown_skill:{skill}")
        model = self.configured_model
        if model is None and candidates:
            model = candidates[0]
        return {
            "skill": skill,
            "selected_model": model,
            "mode": "manual_configured",
            "prefer_cost_ignored": True,  # no auto optimizer
            "router_status": "NOT_BUILT",
            "note": "Cost-aware Model Router is future; do not claim auto selection",
            "candidates": candidates or [],
            "prefer_cost": prefer_cost,
        }


def product_creation_capability_boundary() -> dict[str, Any]:
    """Unified Product Creation Capability — not split Design/Production agents yet."""
    return {
        "capability": "ProductCreationCapability",
        "status": "BOUNDARY_ONLY",
        "split_agents": False,
        "forbidden_now": [
            "ProductDesignAI_as_separate_agent",
            "ProductProductionAI_as_separate_agent",
            "paid_model_invocation",
            "content_factory_generation_in_entry_067",
        ],
        "skill": SKILL_PRODUCT_CREATION,
        "requires_cost_gate": True,
    }


def assert_no_paid_invocation() -> dict[str, Any]:
    ensure_ai_cost_schema()
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS c FROM ai_execution_records WHERE paid_invocation=1"
        ).fetchone()
        c = int(row["c"] if hasattr(row, "keys") else row[0])
    return {"paid_invocations": c, "ok": c == 0}


def economics_honesty_check(
    *,
    estimated_revenue: float | None,
    claim_as_actual: bool = False,
) -> dict[str, Any]:
    """Reject fake economics — estimated revenue is never ACTUAL without sales."""
    if claim_as_actual and estimated_revenue is not None:
        return {
            "ok": False,
            "error": "estimated_revenue_cannot_be_claimed_as_actual",
            "revenue_basis": BASIS_HYPOTHESIS,
        }
    return {
        "ok": True,
        "estimated_revenue": estimated_revenue,
        "revenue_basis": BASIS_HYPOTHESIS if estimated_revenue is not None else STATUS_UNKNOWN,
        "economics_claim": "ESTIMATE_ONLY",
    }
