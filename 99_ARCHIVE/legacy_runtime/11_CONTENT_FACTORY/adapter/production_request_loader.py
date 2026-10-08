# 11_CONTENT_FACTORY/adapter/production_request_loader.py — 读取 commercial_assets PR + Approval

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_REQUESTS_PATH = REPO_ROOT / "commercial_assets" / "production_requests" / "production_requests_v1.json"
DEFAULT_REVIEWS_PATH = REPO_ROOT / "commercial_assets" / "production_request_reviews" / "production_request_reviews_v1.json"


class ProductionRequestLoader:
    """从 commercial_assets JSON 加载 Production Request 与 Approval（只读）。"""

    def __init__(
        self,
        requests_path: Path | None = None,
        reviews_path: Path | None = None,
    ):
        self.requests_path = requests_path or DEFAULT_REQUESTS_PATH
        self.reviews_path = reviews_path or DEFAULT_REVIEWS_PATH

    def load_requests_dataset(self) -> dict[str, Any]:
        return self._load_json(self.requests_path)

    def load_reviews_dataset(self) -> dict[str, Any]:
        return self._load_json(self.reviews_path)

    def load_production_request(self, production_request_id: str) -> dict[str, Any]:
        dataset = self.load_requests_dataset()
        for item in dataset.get("production_requests", []):
            if item.get("production_request_id") == production_request_id:
                return item
        raise KeyError(f"production_request_id not found: {production_request_id}")

    def load_approval_for_request(self, production_request_id: str) -> dict[str, Any] | None:
        dataset = self.load_reviews_dataset()
        for item in dataset.get("production_request_reviews", []):
            if item.get("source_production_request_id") == production_request_id:
                return item
        return None

    def load_input_package(self, production_request_id: str) -> dict[str, Any]:
        """加载 PR + Approval，返回统一 input package（未做 gate 校验）。"""
        pr = self.load_production_request(production_request_id)
        approval = self.load_approval_for_request(production_request_id)
        return {
            "production_request": pr,
            "approval": approval,
            "production_request_id": production_request_id,
            "source_experiment_id": pr.get("source_experiment_id", ""),
            "approval_id": approval.get("approval_id") if approval else None,
        }

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"commercial_assets file not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))
