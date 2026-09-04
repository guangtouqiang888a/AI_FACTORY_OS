# 3_DECISION/candidate_selector.py — Minimal Autonomous Candidate Selection
# Entry 052
#
# 建立在现有 scorer / risk_engine 之上，不重写 Decision Engine。
# Production Candidate ≠ Publish Candidate（发布仍须 Publish Queue 门控）
# 当前评分模型（hot/trend/comp/profit/difficulty）= 当前模型，非最终商业智慧。

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "3_DECISION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

from risk_engine import assess_risk  # noqa: E402
import config  # noqa: E402


MODEL_NOTE = (
    "Current score dimensions: hot/trend/competition/profit/difficulty. "
    "This is the present model — not final commercial intelligence. "
    "Future may add demand/conversion/historical outcome/learning value."
)


def select_candidates(
    products: list[dict],
    *,
    top_n: int = 5,
    min_score: float | None = None,
) -> dict:
    """
    Candidate Pool → Score → Risk Filter → Rank → Production/Publish Candidates.

    Expects products with optional scores{total,...}. Does not auto-publish.
    """
    threshold = (
        min_score
        if min_score is not None
        else float(getattr(config, "PUBLISH_SCORE_THRESHOLD", 60))
    )

    scored = []
    for p in products:
        scores = p.get("scores") or {}
        total = float(scores.get("total") or p.get("total_score") or 0)
        risk = assess_risk(p)
        scored.append({**p, "scores": scores, "total_score": total, "risk": risk})

    risk_passed = [p for p in scored if p["risk"].get("passed")]
    risk_passed.sort(key=lambda x: x.get("total_score", 0), reverse=True)

    production_candidates = [
        {
            "product_ref": p.get("id") or p.get("title"),
            "title": p.get("title"),
            "keyword": p.get("keyword"),
            "total_score": p.get("total_score"),
            "risk": p.get("risk"),
            "candidate_type": "PRODUCTION_CANDIDATE",
            "eligible_for_production_consideration": p.get("total_score", 0) >= threshold,
        }
        for p in risk_passed[:top_n]
    ]

    publish_candidates = [
        c for c in production_candidates if c["eligible_for_production_consideration"]
    ]
    # Publish candidates still require Quality/Commercial/Package gates via publish_queue
    for c in publish_candidates:
        c["candidate_type"] = "PUBLISH_CANDIDATE_PREGATE"
        c["requires_publish_queue_gates"] = True
        c["auto_publish_forbidden"] = True

    return {
        "model_note": MODEL_NOTE,
        "threshold": threshold,
        "pool_size": len(products),
        "risk_filtered": len(risk_passed),
        "production_candidates": production_candidates,
        "publish_candidates_pregate": publish_candidates,
        "action": "rank_only",
        "auto_external_publish": False,
    }
