# 10_DEPLOY/metrics.py — Standardized production metrics

import json
import threading
from datetime import datetime

from deploy_config import DEPLOY_METRICS_FILE

_lock = threading.Lock()

_state = {
    "request_count": 0,
    "success_count": 0,
    "error_count": 0,
    "total_latency_ms": 0.0,
    "cost_estimation": 0.0,
    "last_request_at": None,
    "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}


def _compute_view() -> dict:
    count = _state["request_count"]
    avg_latency = round(_state["total_latency_ms"] / count, 2) if count else 0.0
    success_rate = round(_state["success_count"] / count, 4) if count else 0.0
    return {
        "request_count": count,
        "avg_latency": avg_latency,
        "error_count": _state["error_count"],
        "cost_estimation": round(_state["cost_estimation"], 6),
        "success_rate": success_rate,
        "last_request_at": _state["last_request_at"],
        "started_at": _state["started_at"],
    }


def _persist() -> None:
    DEPLOY_METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEPLOY_METRICS_FILE.write_text(
        json.dumps(_compute_view(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def record_request(latency_ms: float, success: bool, session_cost: float = 0.0) -> None:
    with _lock:
        _state["request_count"] += 1
        if success:
            _state["success_count"] += 1
        else:
            _state["error_count"] += 1
        _state["total_latency_ms"] += latency_ms
        _state["cost_estimation"] += session_cost
        _state["last_request_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _persist()


def get_metrics() -> dict:
    with _lock:
        return _compute_view()


def reset_metrics() -> None:
    with _lock:
        global _state
        _state = {
            "request_count": 0,
            "success_count": 0,
            "error_count": 0,
            "total_latency_ms": 0.0,
            "cost_estimation": 0.0,
            "last_request_at": None,
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        _persist()
