# 10_DEPLOY/trace.py — Execution Trace System

import json
import threading
from datetime import datetime

from deploy_config import DEPLOY_TRACE_FILE

_lock = threading.Lock()


def build_trace_entry(
    request_id: str,
    task: str,
    raw: dict,
    latency: float,
) -> dict:
    return {
        "request_id": request_id,
        "task": task,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "latency": latency,
        "planner_output": raw.get("plan"),
        "policy_decision": raw.get("pipeline_policy"),
        "execution_hash": raw.get("execution_hashes"),
        "memory_event": raw.get("memory"),
    }


def write_trace(entry: dict) -> None:
    DEPLOY_TRACE_FILE.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False, default=str)
    with _lock:
        with DEPLOY_TRACE_FILE.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
