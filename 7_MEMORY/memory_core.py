# 7_MEMORY/memory_core.py — Memory System（含 policy snapshot 回滚）
# Entry 050 — Commercial Learning Integrity：Execution Success ≠ Commercial Success

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
import config  # noqa: E402

# --- Outcome Ontology（最小语义 · Entry 050）---
# EXECUTION_OUTCOME / PRODUCTION_OUTCOME / QUALITY_OUTCOME /
# COMMERCIAL_OUTCOME / MARKET_OUTCOME 不得互相冒充。

LEARNING_LANE_EXECUTION = "EXECUTION"
LEARNING_LANE_COMMERCIAL = "COMMERCIAL"
LEARNING_LANE_SIMULATION = "SIMULATION"

DATA_ORIGIN_REAL = "REAL"
DATA_ORIGIN_SIMULATION = "SIMULATION"
DATA_ORIGIN_SYNTHETIC = "SYNTHETIC"
DATA_ORIGIN_UNKNOWN = "UNKNOWN"

PATTERN_ORIGIN_EXECUTION = "EXECUTION"
PATTERN_ORIGIN_SIMULATION = "SIMULATION"
PATTERN_ORIGIN_REAL_MARKET = "REAL_MARKET"

COMMERCIAL_OUTCOME_TYPES = frozenset({
    "purchase",
    "revenue",
    "refund",
    "conversion",
    "profit",
})

# published_local 等仅为执行层状态，永远不能单独构成商业成功
NON_COMMERCIAL_EXEC_STATUSES = frozenset({
    "published_local",
    "executed",
    "completed",
    "error",
    "skipped",
    "unknown",
})


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _ensure_dirs() -> None:
    config.MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default: dict | list) -> dict | list:
    if not path.exists() or path.stat().st_size == 0:
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _save_json(path: Path, data: dict | list) -> None:
    _ensure_dirs()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_pattern_memory() -> dict:
    return _load_json(config.PATTERN_MEMORY_PATH, {"patterns": []})


def load_strategy_memory() -> dict:
    return _load_json(
        config.STRATEGY_MEMORY_PATH,
        {
            "rules": [{
                "id": "default_publish",
                "if": {"min_score": config.PUBLISH_SCORE_THRESHOLD},
                "then": "publish",
                "confidence": 0.5,
                "source": "bootstrap",
            }],
            "updated_at": _now_str(),
        },
    )


def load_runtime_policy() -> dict:
    policy = _load_json(config.RUNTIME_POLICY_PATH, {})
    if not isinstance(policy, dict):
        policy = {}
    return enforce_immutable_policy(policy)


def enforce_immutable_policy(policy: dict) -> dict:
    """注入 immutable_rules — Self-Evolution 无法覆盖。"""
    merged = config.DEFAULT_RUNTIME_POLICY.copy()
    merged.update(policy)
    merged["policy_core_lock"] = config.POLICY_CORE_LOCK
    merged["llm_routing"] = config.LLM_ROUTING.copy()
    merged["executor_allowlist"] = list(config.EXECUTOR_ALLOWLIST)
    merged["llm_cost_budget"] = config.LLM_COST_BUDGET_CEILING
    return merged


def save_runtime_policy(policy: dict) -> None:
    locked = enforce_immutable_policy(policy)
    locked["updated_at"] = _now_str()
    _save_json(config.RUNTIME_POLICY_PATH, locked)


def save_policy_patch(patch: dict, source: str = "self_evolution") -> dict:
    record = {"time": _now_str(), "source": source, "patch": patch}
    _save_json(config.POLICY_PATCH_PATH, record)
    return record


def load_policy_patch() -> dict:
    return _load_json(config.POLICY_PATCH_PATH, {})


def save_policy_snapshot() -> dict:
    policy = load_runtime_policy()
    snapshot = {
        "id": str(uuid.uuid4())[:8],
        "saved_at": _now_str(),
        "policy": {k: v for k, v in policy.items() if k not in ("session_llm_cost",)},
    }
    _save_json(config.RUNTIME_POLICY_SNAPSHOT_PATH, snapshot)
    return snapshot


def rollback_policy_snapshot() -> dict:
    snapshot = _load_json(config.RUNTIME_POLICY_SNAPSHOT_PATH, {})
    if not snapshot or "policy" not in snapshot:
        default = config.DEFAULT_RUNTIME_POLICY.copy()
        save_runtime_policy(default)
        return {"rolled_back": True, "source": "default"}

    restored = snapshot["policy"]
    restored["cooldown_remaining"] = config.COOLDOWN_STEPS
    restored["updated_at"] = _now_str()
    save_runtime_policy(restored)
    write_event({"type": "policy_rollback", "snapshot_id": snapshot.get("id")})
    return {"rolled_back": True, "source": "snapshot", "snapshot_id": snapshot.get("id")}


def write_event(event: dict) -> None:
    _ensure_dirs()
    record = {"time": _now_str(), **event}
    with open(config.EVENT_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def log_event(event: dict) -> None:
    write_event(event)


def get_recent_events(limit: int = 50) -> list[dict]:
    if not config.EVENT_LOG_PATH.exists():
        return []
    lines = config.EVENT_LOG_PATH.read_text(encoding="utf-8").strip().splitlines()
    events = []
    for line in lines[-limit:]:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def is_execution_learning_pattern(pattern: dict) -> bool:
    """Execution Strategy 可用的 pattern（含历史未标注字段，默认 EXECUTION）。"""
    if pattern.get("commercial_success") is True:
        return False
    lane = pattern.get("learning_lane") or LEARNING_LANE_EXECUTION
    return lane in (LEARNING_LANE_EXECUTION, LEARNING_LANE_SIMULATION)


def get_pattern_stats(learning_lane: str = LEARNING_LANE_EXECUTION) -> dict:
    """
    默认仅统计 Execution Learning。
    禁止把 commercial_success 混入执行策略进化统计。
    """
    patterns = load_pattern_memory().get("patterns", [])
    if learning_lane == LEARNING_LANE_EXECUTION:
        patterns = [p for p in patterns if is_execution_learning_pattern(p)]
    elif learning_lane == LEARNING_LANE_COMMERCIAL:
        patterns = [
            p for p in patterns
            if p.get("learning_lane") == LEARNING_LANE_COMMERCIAL
            and p.get("commercial_success") is True
        ]
    if not patterns:
        return {
            "success_rate": 0.0,
            "fail_rate": 0.0,
            "total": 0,
            "learning_lane": learning_lane,
            "strategy_domain": "EXECUTION" if learning_lane != LEARNING_LANE_COMMERCIAL else "COMMERCIAL",
        }
    success = sum(1 for p in patterns if p.get("outcome") == "success")
    failure = sum(1 for p in patterns if p.get("outcome") == "failure")
    total = len(patterns)
    return {
        "success_rate": round(success / total, 3),
        "fail_rate": round(failure / total, 3),
        "total": total,
        "learning_lane": learning_lane,
        "strategy_domain": "EXECUTION" if learning_lane != LEARNING_LANE_COMMERCIAL else "COMMERCIAL",
    }


def classify_execution_outcome(action: str, exec_status: str) -> str:
    """Map execution layer status to EXECUTION_OUTCOME label."""
    if exec_status:
        return str(exec_status)
    if action == "skip":
        return "skipped"
    return "unknown"


def is_execution_success(action: str, exec_status: str) -> bool:
    """Execution-layer success only（含 published_local）。≠ Commercial Success。"""
    return action == "publish" and exec_status == "published_local"


def is_commercial_learning_eligible(record: dict) -> tuple[bool, str]:
    """
    Real Commercial Learning 最低安全门（Entry 050）。

    必须同时满足：
    - data_origin == REAL
    - commercial_outcome 为可信商业结果类型
    - verified_source 存在
    - 不得仅凭 published_local / quality_pass / production_completed

    Returns: (eligible, reason)
    """
    if not isinstance(record, dict):
        return False, "record_not_dict"

    exec_status = str(record.get("exec_status") or record.get("execution_outcome") or "")
    commercial = record.get("commercial_outcome")
    has_commercial = bool(commercial)

    # published_local alone never qualifies（即使有 has_real_commercial_evidence 也需 commercial_outcome）
    if exec_status == "published_local" and not has_commercial:
        return False, "published_local_alone_not_commercial_success"

    if record.get("quality_outcome") in ("quality_pass", "quality_fail") and not has_commercial:
        return False, "quality_outcome_alone_not_commercial_success"

    if record.get("production_outcome") in (
        "generated",
        "validation_passed",
        "production_completed",
        "completed",
    ) and not has_commercial:
        return False, "production_completion_alone_not_commercial_success"

    origin = str(record.get("data_origin") or DATA_ORIGIN_UNKNOWN).upper()
    if origin == DATA_ORIGIN_SIMULATION:
        return False, "simulation_rejected_from_real_commercial_learning"
    if origin == DATA_ORIGIN_SYNTHETIC:
        return False, "synthetic_rejected_from_real_commercial_learning"
    if origin != DATA_ORIGIN_REAL:
        return False, f"data_origin={origin}_rejected_from_real_commercial_learning"

    if not commercial:
        return False, "missing_commercial_outcome"
    commercial_s = str(commercial).lower()
    if commercial_s not in COMMERCIAL_OUTCOME_TYPES:
        return False, f"commercial_outcome={commercial}_not_in_allowed_types"

    verified = record.get("verified_source")
    if not verified or str(verified).strip() in ("", "unknown", "UNKNOWN", "simulation", "SIMULATION"):
        return False, "missing_or_invalid_verified_source"

    return True, "eligible_for_real_commercial_learning"


def ingest_commercial_learning_event(record: dict) -> dict:
    """
    Commercial Learning 摄入入口（Guardrail Interface）。
    不满足条件则拒绝；不写入假商业成功。
    """
    ok, reason = is_commercial_learning_eligible(record)
    result = {
        "accepted": ok,
        "reason": reason,
        "learning_lane": LEARNING_LANE_COMMERCIAL if ok else None,
        "commercial_success": bool(ok),
    }
    write_event({
        "type": "commercial_learning_ingest",
        "accepted": ok,
        "reason": reason,
        "data_origin": record.get("data_origin"),
        "commercial_outcome": record.get("commercial_outcome"),
        "exec_status": record.get("exec_status"),
    })
    if not ok:
        return result

    # 最小记录：写入 pattern_memory，明确 REAL_MARKET / COMMERCIAL
    store = load_pattern_memory()
    patterns = store.get("patterns", [])
    pattern = {
        "id": str(uuid.uuid4())[:8],
        "task": record.get("task") or record.get("keyword") or "commercial_event",
        "keyword": record.get("keyword") or record.get("task") or "",
        "action": record.get("action") or "commercial_event",
        "exec_status": record.get("exec_status"),
        "execution_outcome": record.get("execution_outcome") or record.get("exec_status"),
        "commercial_outcome": record.get("commercial_outcome"),
        "market_outcome": record.get("market_outcome"),
        "quality_outcome": record.get("quality_outcome"),
        "production_outcome": record.get("production_outcome"),
        "outcome": "success",
        "outcome_domain": "COMMERCIAL",
        "learning_lane": LEARNING_LANE_COMMERCIAL,
        "pattern_origin": PATTERN_ORIGIN_REAL_MARKET,
        "data_origin": DATA_ORIGIN_REAL,
        "commercial_success": True,
        "verified_source": record.get("verified_source"),
        "commercial_evidence_id": record.get("commercial_evidence_id"),
        "has_real_commercial_evidence": True,
        # Entry 051 — 证据链（可追溯至 Market Event）
        "source_event_id": record.get("source_event_id") or record.get("commercial_evidence_id"),
        "source": record.get("source"),
        "platform": record.get("platform"),
        "event_timestamp": record.get("timestamp") or record.get("event_timestamp"),
        "product_id": record.get("product_id"),
        "product_asset_id": record.get("product_asset_id"),
        "experiment_id": record.get("experiment_id"),
        "listing_id": record.get("listing_id"),
        "original_event_type": record.get("original_event_type"),
        "original_value": record.get("original_value"),
        "currency": record.get("currency"),
        "verification_status": record.get("verification_status"),
        "score": record.get("score"),
        "extracted_at": _now_str(),
        "source_module": "commercial_learning_ingest",
    }
    pattern["confidence"] = compute_pattern_confidence(pattern)
    patterns.append(pattern)
    store["patterns"] = patterns[-200:]
    store["updated_at"] = _now_str()
    _save_json(config.PATTERN_MEMORY_PATH, store)
    result["pattern_id"] = pattern["id"]
    return result


def compute_pattern_confidence(pattern: dict) -> float:
    """计算 pattern 置信度（0-1）。"""
    score = float(pattern.get("score") or 0)
    scored_count = int(pattern.get("scored_count") or 0)
    outcome = pattern.get("outcome", "neutral")

    confidence = 0.45
    if scored_count >= 3:
        confidence += 0.15
    if scored_count >= 10:
        confidence += 0.10
    if score >= config.PUBLISH_SCORE_THRESHOLD:
        confidence += 0.15
    if outcome == "success":
        confidence += 0.15
    elif outcome == "failure":
        confidence -= 0.10
    return round(min(1.0, max(0.0, confidence)), 3)


def extract_pattern(run_context: dict) -> dict:
    """
    从 Track A 运行上下文提取 **Execution Learning** pattern。

    Entry 050 硬规则：
    - published_local → execution success only
    - commercial_success 永远为 False（本路径无真实商业证据）
    - data_origin = SIMULATION（本地模拟发布）
    - 不得进入 Real Commercial Learning
    """
    task = run_context.get("task", "")
    nodes = run_context.get("nodes", {})
    decision_out = nodes.get("decision", {})
    execution_out = nodes.get("execution", {})
    scoring_out = nodes.get("scoring", {})
    decision = decision_out.get("result", {})
    execution = execution_out.get("result", {})
    score = decision_out.get("score") or (decision.get("best") or {}).get("scores", {}).get("total", 0)
    action = decision.get("action", "skip")
    exec_status = execution.get("status", "unknown")
    execution_outcome = classify_execution_outcome(action, exec_status)
    exec_ok = is_execution_success(action, exec_status)
    failure = action == "skip" or exec_status in ("skipped", "error")

    # Integrity：本路径绝不宣称商业成功
    commercial_success = False
    data_origin = DATA_ORIGIN_SIMULATION if exec_status == "published_local" else DATA_ORIGIN_UNKNOWN
    if exec_status == "published_local":
        pattern_origin = PATTERN_ORIGIN_SIMULATION
        learning_lane = LEARNING_LANE_EXECUTION
    else:
        pattern_origin = PATTERN_ORIGIN_EXECUTION
        learning_lane = LEARNING_LANE_EXECUTION

    pattern = {
        "id": str(uuid.uuid4())[:8],
        "task": task,
        "keyword": decision.get("keyword", task),
        "action": action,
        "exec_status": exec_status,
        "execution_outcome": execution_outcome,
        "production_outcome": None,
        "quality_outcome": None,
        "commercial_outcome": None,
        "market_outcome": None,
        "score": score,
        "scored_count": scoring_out.get("result", {}).get("count", 0),
        # outcome = Execution Learning 语义（保持 SelfEvolution 可用）
        "outcome": "success" if exec_ok else ("failure" if failure else "neutral"),
        "outcome_domain": "EXECUTION",
        "learning_lane": learning_lane,
        "pattern_origin": pattern_origin,
        "data_origin": data_origin,
        "commercial_success": commercial_success,
        "strategy_domain": "EXECUTION",
        "extracted_at": _now_str(),
        "integrity_note": (
            "published_local_is_execution_success_not_commercial_success"
            if exec_status == "published_local"
            else "execution_pattern_only"
        ),
    }
    # 双保险：即使外部误传 commercial 字段，Track A extract 也清除
    if pattern["commercial_success"] is True and exec_status == "published_local":
        pattern["commercial_success"] = False

    pattern["confidence"] = compute_pattern_confidence(pattern)
    if pattern["confidence"] < config.PATTERN_CONFIDENCE_THRESHOLD:
        pattern["discarded"] = True
        write_event({
            "type": "pattern_noise_filtered",
            "pattern_id": pattern["id"],
            "confidence": pattern["confidence"],
            "threshold": config.PATTERN_CONFIDENCE_THRESHOLD,
        })
    store = load_pattern_memory()
    patterns = store.get("patterns", [])
    patterns.append(pattern)
    store["patterns"] = patterns[-200:]
    store["updated_at"] = _now_str()
    _save_json(config.PATTERN_MEMORY_PATH, store)
    write_event({
        "type": "pattern_extracted",
        "pattern_id": pattern["id"],
        "learning_lane": learning_lane,
        "commercial_success": False,
        "exec_status": exec_status,
        "data_origin": data_origin,
    })
    return pattern


def update_strategy(pattern: dict) -> dict:
    """
    仅更新 **Execution Strategy**（Track A 发布阈值等）。
    明确拒绝将 commercial_success / Real Commercial Learning 混入此路径。
    """
    if pattern.get("commercial_success") is True:
        write_event({
            "type": "strategy_update_skipped",
            "reason": "commercial_pattern_not_for_execution_strategy",
            "pattern_id": pattern.get("id"),
        })
        return {
            **load_strategy_memory(),
            "skipped": True,
            "reason": "commercial_pattern_blocked_from_execution_strategy",
        }

    if pattern.get("learning_lane") == LEARNING_LANE_COMMERCIAL:
        write_event({
            "type": "strategy_update_skipped",
            "reason": "commercial_lane_blocked_from_execution_strategy",
            "pattern_id": pattern.get("id"),
        })
        return {
            **load_strategy_memory(),
            "skipped": True,
            "reason": "commercial_lane_blocked",
        }

    confidence = pattern.get("confidence", compute_pattern_confidence(pattern))
    if confidence < config.PATTERN_CONFIDENCE_THRESHOLD or pattern.get("discarded"):
        write_event({
            "type": "strategy_update_skipped",
            "reason": "low confidence",
            "confidence": confidence,
            "threshold": config.PATTERN_CONFIDENCE_THRESHOLD,
        })
        return {**load_strategy_memory(), "skipped": True, "reason": "confidence below threshold"}

    store = load_strategy_memory()
    rules = store.get("rules", [])
    keyword = pattern.get("keyword", pattern.get("task", ""))
    threshold = load_runtime_policy().get("threshold", config.PUBLISH_SCORE_THRESHOLD)
    if pattern.get("outcome") == "success" and pattern.get("score", 0) >= threshold:
        rule_id = f"learned_publish_{keyword[:10]}"
        existing = next((r for r in rules if r.get("id") == rule_id), None)
        new_conf = min(0.95, (existing or {}).get("confidence", 0.4) + 0.05)
        rule = {
            "id": rule_id,
            "if": {"keyword": keyword, "min_score": threshold},
            "then": "publish",
            "confidence": round(new_conf, 3),
            "source": "execution_pattern_learning",
            "strategy_domain": "EXECUTION",
            "last_pattern_id": pattern.get("id"),
            "note": "Not commercial learning; published_local ≠ commercial success",
        }
        rules = [rule if r.get("id") == rule_id else r for r in rules] if existing else rules + [rule]
    if pattern.get("outcome") == "failure":
        rule_id = f"learned_skip_{keyword[:10]}"
        if not any(r.get("id") == rule_id for r in rules):
            rules.append({
                "id": rule_id,
                "if": {"keyword": keyword, "outcome": "failure"},
                "then": "observe",
                "confidence": 0.6,
                "source": "execution_pattern_learning",
                "strategy_domain": "EXECUTION",
                "last_pattern_id": pattern.get("id"),
            })
    store["rules"] = rules
    store["strategy_domain"] = "EXECUTION"
    store["updated_at"] = _now_str()
    _save_json(config.STRATEGY_MEMORY_PATH, store)
    return store


def log_execution_hash(record: dict) -> None:
    """execution_hash_log — 可回放验证。"""
    _ensure_dirs()
    with open(config.EXECUTION_HASH_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps({"time": _now_str(), **record}, ensure_ascii=False) + "\n")


def init_memory() -> dict:
    _ensure_dirs()
    for path in (
        config.EVENT_LOG_PATH,
        config.PATTERN_MEMORY_PATH,
        config.STRATEGY_MEMORY_PATH,
        config.RUNTIME_POLICY_PATH,
        config.POLICY_PATCH_PATH,
        config.RUNTIME_POLICY_SNAPSHOT_PATH,
        config.EXECUTION_HASH_LOG_PATH,
    ):
        if not path.exists():
            path.touch()
    if config.PATTERN_MEMORY_PATH.stat().st_size == 0:
        _save_json(config.PATTERN_MEMORY_PATH, {"patterns": [], "updated_at": _now_str()})
    if config.STRATEGY_MEMORY_PATH.stat().st_size == 0:
        _save_json(config.STRATEGY_MEMORY_PATH, load_strategy_memory())
    if config.RUNTIME_POLICY_PATH.stat().st_size == 0:
        save_runtime_policy(load_runtime_policy())
    if config.RUNTIME_POLICY_SNAPSHOT_PATH.stat().st_size == 0:
        save_policy_snapshot()
    return {
        "pattern_count": len(load_pattern_memory().get("patterns", [])),
        "strategy_rules": len(load_strategy_memory().get("rules", [])),
    }
