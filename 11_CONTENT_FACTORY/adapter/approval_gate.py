# 11_CONTENT_FACTORY/adapter/approval_gate.py — Production Request Approval 门禁

from __future__ import annotations

from typing import Any

PILOT_WHITELIST = frozenset({"preq_20260712_005"})


class ApprovalGateError(Exception):
    """Approval Gate 拒绝执行。"""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

    def to_dict(self) -> dict[str, str]:
        return {"gate_error": self.code, "message": self.message}


class ApprovalGate:
    """校验 Production Request 是否具备进入 Pipeline 的授权。"""

    def __init__(self, *, pilot_only: bool = True, pilot_whitelist: frozenset[str] | None = None):
        self.pilot_only = pilot_only
        self.pilot_whitelist = pilot_whitelist if pilot_whitelist is not None else PILOT_WHITELIST

    def validate(self, loaded: dict[str, Any]) -> dict[str, Any]:
        """
        验证 loaded package（来自 ProductionRequestLoader.load_input_package）。

        必须：PR 存在、Approval 存在、decision == approved、ID 匹配。
        Pilot 阶段：仅 whitelist 内 production_request_id 允许通过。
        """
        production_request_id = loaded.get("production_request_id", "")
        pr = loaded.get("production_request")
        approval = loaded.get("approval")

        if not production_request_id:
            raise ApprovalGateError("MISSING_REQUEST_ID", "production_request_id is required")

        if pr is None:
            raise ApprovalGateError("NO_PRODUCTION_REQUEST", f"Production Request not found: {production_request_id}")

        if approval is None:
            raise ApprovalGateError("NO_APPROVAL", f"No Approval Object for {production_request_id}")

        if approval.get("decision") != "approved":
            raise ApprovalGateError(
                "NOT_APPROVED",
                f"Approval decision is {approval.get('decision')!r}, expected 'approved'",
            )

        if approval.get("source_production_request_id") != production_request_id:
            raise ApprovalGateError(
                "ID_MISMATCH",
                "approval.source_production_request_id does not match production_request_id",
            )

        if self.pilot_only and production_request_id not in self.pilot_whitelist:
            raise ApprovalGateError(
                "PILOT_NOT_ALLOWED",
                f"{production_request_id} is not in Pilot whitelist — only preq_20260712_005 allowed",
            )

        return {
            "gate_status": "passed",
            "production_request_id": production_request_id,
            "approval_id": approval.get("approval_id"),
            "source_experiment_id": pr.get("source_experiment_id"),
        }
