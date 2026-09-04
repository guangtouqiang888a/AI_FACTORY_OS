# 3_DECISION/scorer.py — 商品评分

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
import config  # noqa: E402


def _clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


def _get_weights() -> dict:
    try:
        sys.path.insert(0, str(ROOT / "7_MEMORY"))
        import memory_core  # noqa: E402
        w = memory_core.load_runtime_policy().get("weights")
        if isinstance(w, dict) and w:
            return w
    except Exception:
        pass
    return config.SCORE_WEIGHTS


def score_listing_metrics(
    *,
    want_count: int | None = None,
    view_count: int | None = None,
    price: float | None = None,
    null_as_zero: bool = True,
) -> dict | None:
    """
    Shared listing metric scoring.
    Product path (null_as_zero=True): missing metrics coerce to 0 (054 contract).
    Observation path (null_as_zero=False): want_count NULL → None (NULL ≠ 0).
    """
    if want_count is None and not null_as_zero:
        return None

    want = int(want_count or 0) if null_as_zero else int(want_count)
    if view_count is None:
        view_contrib = 0.01 if null_as_zero else 0.0
    else:
        view_contrib = max(int(view_count), 1) * 0.01

    price_val = float(price or 0) if null_as_zero else float(price or 0)

    hot = _clamp(want * 2 + view_contrib)
    trend = _clamp(hot * 0.85 + 10)
    comp = _clamp(100 - min(want / 5, 80))
    profit = _clamp(price_val * 3 + want * 0.5)
    difficulty = _clamp(50 - min(want, 40))

    w = _get_weights()
    total = (
        hot * w["hot"]
        + trend * w["trend"]
        + comp * w["competition"]
        + profit * w["profit"]
        + difficulty * w["difficulty"]
    )

    return {
        "hot": round(hot, 2),
        "trend": round(trend, 2),
        "comp": round(comp, 2),
        "profit": round(profit, 2),
        "difficulty": round(difficulty, 2),
        "total": round(total, 2),
    }


def score_product(product: dict) -> dict:
    """基于热度、竞争、利润等维度计算分数（Product contract: null_as_zero=True）。"""
    result = score_listing_metrics(
        want_count=product.get("want_count"),
        view_count=product.get("view_count"),
        price=product.get("price"),
        null_as_zero=True,
    )
    assert result is not None
    return result


def score_observation_listing(observation: dict) -> dict | None:
    """Observation listing score — NULL want_count is not coerced to 0."""
    return score_listing_metrics(
        want_count=observation.get("want_count"),
        view_count=observation.get("view_count"),
        price=observation.get("price"),
        null_as_zero=False,
    )
