# 11_CONTENT_FACTORY/validation/product_asset_validator.py — Product Asset Validation Gate Runtime

from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

FACTORY_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = FACTORY_ROOT.parent
TZ_CN = timezone(timedelta(hours=8))

DEFAULT_MIN_QUALITY_SCORE = 0.85
CONTRACT_VERSION = "1.0"
ALLOWED_CREATION_METHODS = frozenset({"adapter_generated", "human_assisted", "automated"})
REAL_FILE_EXTENSIONS = {".pptx", ".xlsx", ".docx", ".pdf"}


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _new_validation_id() -> str:
    stamp = datetime.now(TZ_CN).strftime("%Y%m%d")
    suffix = uuid.uuid4().hex[:6]
    return f"pval_{stamp}_{suffix}"


def _review_item(
    check_id: str,
    category: str,
    description: str,
    expected: str,
    actual: Any,
    passed: bool,
    *,
    severity: str = "blocker",
) -> dict[str, Any]:
    return {
        "check_id": check_id,
        "category": category,
        "description": description,
        "expected": expected,
        "actual": actual,
        "passed": passed,
        "severity": severity,
    }


def _category_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [i["check_id"] for i in items if not i["passed"]]
    return {"passed": len(failed) == 0, "failed_checks": failed}


class ProductAssetValidator:
    """
    Product Asset Validation Gate Runtime — 只负责 check，不负责 create / write / publish。
    """

    def __init__(self, *, min_quality_score: float = DEFAULT_MIN_QUALITY_SCORE):
        self.min_quality_score = min_quality_score

    def validate(self, product_asset: dict[str, Any]) -> dict[str, Any]:
        """
        验收 Product Asset 草稿，返回完整 product_asset_validation Object。

        不写入 commercial_assets，不创建 Product Asset 实例。
        """
        check = self.validate_check_only(product_asset)
        now = _now_iso()
        ctx = product_asset.get("validation_context") or {}

        return {
            "validation_id": _new_validation_id(),
            "object_type": "product_asset_validation",
            "contract_version": CONTRACT_VERSION,
            "source_production_request_id": product_asset.get("source_production_request_id"),
            "source_product_asset_id": product_asset.get("product_asset_id"),
            "source_experiment_id": product_asset.get("source_experiment_id"),
            "source_approval_id": product_asset.get("approval_id"),
            "validation_method": "human_assisted",
            "validation_status": check["validation_status"],
            "validation_result": check["validation_result"],
            "review_items": check["review_items"],
            "validated_by": "system",
            "created_at": now,
            "completed_at": now,
            "validation_context_ref": {
                "validation_goal_present": bool(ctx.get("validation_goal") or product_asset.get("validation_goal")),
                "requirements_present": bool(ctx.get("asset_requirements") or product_asset.get("asset_requirements")),
            },
        }

    def validate_check_only(self, product_asset: dict[str, Any]) -> dict[str, Any]:
        """返回 { validation_status, validation_result, review_items }。"""
        review_items: list[dict[str, Any]] = []
        review_items.extend(self._check_artifact(product_asset))
        review_items.extend(self._check_contract(product_asset))
        review_items.extend(self._check_quality(product_asset))
        review_items.extend(self._check_commercial(product_asset))

        blockers_failed = [i for i in review_items if i["severity"] == "blocker" and not i["passed"]]
        warnings_failed = [i for i in review_items if i["severity"] == "warning" and not i["passed"]]

        if blockers_failed:
            status = "failed"
        elif warnings_failed:
            status = "pending_review"
        else:
            status = "passed"

        by_category = {
            "artifact_validation": [i for i in review_items if i["category"] == "artifact_validation"],
            "contract_validation": [i for i in review_items if i["category"] == "contract_validation"],
            "quality_validation": [i for i in review_items if i["category"] == "quality_validation"],
            "commercial_validation": [i for i in review_items if i["category"] == "commercial_validation"],
        }

        validation_result = {
            "overall": status,
            "artifact_validation": _category_summary(by_category["artifact_validation"]),
            "contract_validation": _category_summary(by_category["contract_validation"]),
            "quality_validation": _category_summary(by_category["quality_validation"]),
            "commercial_validation": _category_summary(by_category["commercial_validation"]),
            "summary": self._summary(status, blockers_failed),
            "blockers": [i["check_id"] for i in blockers_failed],
            "warnings": [i["check_id"] for i in warnings_failed],
        }

        return {
            "validation_status": status,
            "validation_result": validation_result,
            "review_items": review_items,
        }

    def _resolve_artifact_path(self, raw_path: str | None) -> Path | None:
        if not raw_path:
            return None
        path = Path(raw_path)
        if not path.is_absolute():
            for base in (FACTORY_ROOT, REPO_ROOT):
                candidate = base / path
                if candidate.exists():
                    return candidate
            candidate = FACTORY_ROOT / path
            return candidate if candidate.exists() else path
        return path if path.exists() else None

    def _check_artifact(self, product_asset: dict[str, Any]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        info = product_asset.get("artifact_information") or {}
        raw_path = info.get("artifact_path")
        artifact_files = info.get("artifact_files") or []
        file_type = (info.get("file_type") or product_asset.get("product_type") or "").lower().lstrip(".")

        resolved = self._resolve_artifact_path(raw_path)
        items.append(
            _review_item(
                "artifact.path_valid",
                "artifact_validation",
                "artifact_path exists on disk",
                "valid directory path",
                str(raw_path),
                resolved is not None and resolved.is_dir(),
            )
        )

        items.append(
            _review_item(
                "artifact.files_non_empty",
                "artifact_validation",
                "artifact file list is not empty",
                "at least one artifact file",
                artifact_files,
                len(artifact_files) > 0,
            )
        )

        type_match = False
        if file_type and artifact_files:
            for f in artifact_files:
                ext = Path(f).suffix.lower().lstrip(".")
                if ext == file_type or (file_type == "excel" and ext == "xlsx") or (file_type == "ppt" and ext == "pptx"):
                    type_match = True
                    break
        elif file_type and resolved:
            for f in resolved.rglob("*"):
                if f.is_file() and f.suffix.lower() in REAL_FILE_EXTENSIONS:
                    ext = f.suffix.lower().lstrip(".")
                    if ext == file_type or (file_type == "excel" and ext == "xlsx"):
                        type_match = True
                        break

        items.append(
            _review_item(
                "artifact.file_type_match",
                "artifact_validation",
                "file_type matches deliverable",
                f"file_type={file_type}",
                artifact_files,
                type_match,
            )
        )

        return items

    def _check_contract(self, product_asset: dict[str, Any]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []

        product_asset_id = product_asset.get("product_asset_id")
        items.append(
            _review_item(
                "contract.product_asset_id",
                "contract_validation",
                "product_asset_id present",
                "non-empty product_asset_id",
                product_asset_id,
                bool(product_asset_id),
            )
        )

        preq_id = product_asset.get("source_production_request_id")
        items.append(
            _review_item(
                "contract.production_request_id",
                "contract_validation",
                "source_production_request_id present",
                "non-empty production_request_id",
                preq_id,
                bool(preq_id),
            )
        )

        contract_version = product_asset.get("contract_version")
        items.append(
            _review_item(
                "contract.contract_version",
                "contract_validation",
                "contract_version is 1.0",
                CONTRACT_VERSION,
                contract_version,
                contract_version == CONTRACT_VERSION,
            )
        )

        creation_method = product_asset.get("creation_method")
        items.append(
            _review_item(
                "contract.creation_method",
                "contract_validation",
                "creation_method allowed",
                f"one of {sorted(ALLOWED_CREATION_METHODS)}",
                creation_method,
                creation_method in ALLOWED_CREATION_METHODS,
            )
        )

        object_type = product_asset.get("object_type")
        items.append(
            _review_item(
                "contract.object_type",
                "contract_validation",
                "object_type is product_asset",
                "product_asset",
                object_type,
                object_type == "product_asset",
            )
        )

        return items

    def _check_quality(self, product_asset: dict[str, Any]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        ctx = product_asset.get("validation_context") or {}
        quality_req = ctx.get("quality_requirements") or product_asset.get("quality_requirements") or {}
        threshold = float(quality_req.get("min_quality_score", self.min_quality_score))

        raw_score = product_asset.get("quality_score")
        score: float | None = None
        if raw_score is not None:
            score = float(raw_score)
            if score > 1.0:
                score = round(score / 100.0, 4)

        items.append(
            _review_item(
                "quality.score_present",
                "quality_validation",
                "quality_score present",
                "numeric quality_score",
                raw_score,
                score is not None,
            )
        )

        passed_threshold = score is not None and score >= threshold
        items.append(
            _review_item(
                "quality.threshold_met",
                "quality_validation",
                f"quality_score >= {threshold}",
                f">= {threshold}",
                score,
                passed_threshold,
            )
        )

        return items

    def _check_commercial(self, product_asset: dict[str, Any]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        ctx = product_asset.get("validation_context") or {}

        validation_goal = ctx.get("validation_goal") or product_asset.get("validation_goal")
        items.append(
            _review_item(
                "commercial.validation_goal",
                "commercial_validation",
                "validation_goal present",
                "non-empty validation_goal",
                validation_goal,
                bool(validation_goal),
            )
        )

        asset_req = ctx.get("asset_requirements") or product_asset.get("asset_requirements")
        quality_req = ctx.get("quality_requirements") or product_asset.get("quality_requirements")
        requirements_ok = bool(asset_req) and bool(quality_req)
        items.append(
            _review_item(
                "commercial.requirements",
                "commercial_validation",
                "asset_requirements and quality_requirements present",
                "both requirement objects",
                {"asset_requirements": bool(asset_req), "quality_requirements": bool(quality_req)},
                requirements_ok,
            )
        )

        return items

    @staticmethod
    def _summary(status: str, blockers_failed: list[dict[str, Any]]) -> str:
        if status == "passed":
            return "All blocker checks passed; eligible for product_assets persistence (Runtime does not write)"
        if status == "pending_review":
            return "Warning checks require human review before product_assets persistence"
        ids = ", ".join(i["check_id"] for i in blockers_failed)
        return f"Validation failed — blockers: {ids}"
