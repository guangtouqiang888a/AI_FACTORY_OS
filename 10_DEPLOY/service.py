# 10_DEPLOY/service.py — Service Wrapper（Service Lock: 仅 controller.run）

"""
Service Lock 规则：
- 唯一允许导入的核心入口：0_START/controller.py → SystemController
- 禁止直接导入 planner / policy_engine / execution_runtime / model_bridge
- 所有业务执行必须经过 controller.run()
"""

import sys
import threading
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "0_START"))

# Service Lock — 仅允许 controller 入口
from controller import SystemController  # noqa: E402

_lock = threading.Lock()
_controller: SystemController | None = None
_boot_info: dict | None = None

# 禁止在 deploy 层直接引用的核心模块（文档化约束）
_FORBIDDEN_DIRECT_IMPORTS = frozenset({
    "planner",
    "policy_engine",
    "execution_runtime",
    "model_bridge",
    "self_evolution",
    "memory_core",
})


def new_request_id() -> str:
    return uuid.uuid4().hex


def make_api_response(
    code: int,
    message: str,
    data: dict | list | None,
    latency: float,
    request_id: str,
) -> dict:
    """统一 API 响应协议。"""
    return {
        "code": code,
        "message": message,
        "data": data if data is not None else {},
        "meta": {
            "latency": round(latency, 6),
            "request_id": request_id,
        },
    }


def _get_controller() -> SystemController:
    global _controller, _boot_info
    with _lock:
        if _controller is None:
            _controller = SystemController()
            _boot_info = _controller.boot()
        return _controller


def get_boot_info() -> dict:
    _get_controller()
    return _boot_info or {}


def run_task(task: str) -> dict:
    """
    外部服务唯一执行入口 — 必须走 SystemController.run()。
    不绕过 Planner → PolicyEngine → ExecutionRuntime → Memory。
    """
    ctrl = _get_controller()
    return ctrl.run(task)


def get_status() -> dict:
    ctrl = _get_controller()
    last = ctrl.last_run
    return {
        "boot": _boot_info,
        "last_run": {
            "task": last.get("task") if last else None,
            "final_action": last.get("final_action") if last else None,
            "finished_at": last.get("finished_at") if last else None,
            "session_cost": last.get("session_cost") if last else 0,
        } if last else None,
        "controller_ready": True,
        "service_lock": "controller.run() only",
    }


def format_run_data(raw: dict) -> dict:
    """将 controller 结果格式化为 /run 的 data 字段。"""
    decision = raw.get("decision") or {}
    scoring = raw.get("scoring") or {}
    execution = raw.get("execution") or {}

    score = decision.get("score") or scoring.get("score")
    result_text = decision.get("reason") or execution.get("status") or raw.get("final_action", "")

    return {
        "task": raw.get("task", ""),
        "result": result_text,
        "score": score,
        "status": raw.get("final_action", "unknown"),
        "execution_status": execution.get("status"),
        "session_cost": raw.get("session_cost", 0),
        "version": raw.get("version"),
        "pattern_confidence": (raw.get("memory") or {}).get("pattern_confidence"),
    }


def format_health_data(boot: dict) -> dict:
    from deploy_config import SERVICE_NAME, SERVICE_VERSION

    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "os_version": boot.get("version"),
        "layers": boot.get("layers"),
    }


def format_status_data() -> dict:
    from deploy_config import SERVICE_NAME, SERVICE_VERSION
    from metrics import get_metrics

    return {
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "metrics": get_metrics(),
        **get_status(),
    }
