# 11_CONTENT_FACTORY/adapter/output_mapper.py — Pipeline result → Product Asset Object 草稿

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any

TZ_CN = timezone(timedelta(hours=8))


def _now_iso() -> str:
    return datetime.now(TZ_CN).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def _normalize_quality_score(raw: float | None) -> float:
    """CF QualityAgent 使用 0–100；Product Asset Contract 使用 0–1。"""
    if raw is None:
        return 0.0
    if raw > 1.0:
        return round(raw / 100.0, 4)
    return round(float(raw), 4)


def _primary_file_type(artifact_files: list[str], deliverable_format: str) -> str:
    if deliverable_format:
        return deliverable_format.lower()
    for f in artifact_files:
        suffix = f.rsplit(".", 1)[-1].lower() if "." in f else ""
        if suffix in ("pptx", "xlsx", "docx", "pdf"):
            return suffix
    return ""


def _generation_status(pipeline_result: dict[str, Any]) -> str:
    status = pipeline_result.get("status", "")
    if status == "ok":
        return "completed"
    if status == "dry_run":
        return "adapter_ready"
    return "failed"


def map_pipeline_result_to_product_asset(
    input_package: dict[str, Any],
    pipeline_result: dict[str, Any],
) -> dict[str, Any]:
    """
    生成 Product Asset Object 草稿 dict — 不写 commercial_assets/product_assets/。
    """
    product = pipeline_result.get("product") or {}
    artifacts = pipeline_result.get("artifacts") or {}
    artifact_files = pipeline_result.get("artifact_files") or artifacts.get("artifact_files") or []
    product_id = pipeline_result.get("product_id") or product.get("id") or ""
    deliverable = input_package.get("deliverable_format") or input_package.get("product_type", "")

    raw_quality = pipeline_result.get("quality_score")
    if raw_quality is None and pipeline_result.get("quality"):
        raw_quality = pipeline_result["quality"].get("quality_score")

    now = _now_iso()
    gen_status = _generation_status(pipeline_result)

    validation_context = {
        "validation_goal": input_package.get("validation_goal"),
        "asset_requirements": input_package.get("asset_requirements"),
        "quality_requirements": input_package.get("quality_requirements"),
    }

    return {
        "object_type": "product_asset",
        "contract_version": "1.0",
        "product_asset_id": product_id or f"passet_draft_{input_package.get('production_request_id', 'unknown')}",
        "source_production_request_id": input_package.get("production_request_id"),
        "source_experiment_id": input_package.get("source_experiment_id") or input_package.get("experiment_id"),
        "experiment_id": input_package.get("experiment_id") or input_package.get("source_experiment_id"),
        "source_opportunity_id": input_package.get("source_opportunity_id"),
        "approval_id": input_package.get("approval_id"),
        "product_name": input_package.get("product_name"),
        "product_type": input_package.get("product_type"),
        "asset_category": "office_template",
        "validation_context": validation_context,
        "artifact_information": {
            "artifact_path": pipeline_result.get("artifact_path") or artifacts.get("artifact_path"),
            "primary_file": artifact_files[0] if artifact_files else None,
            "file_type": _primary_file_type(artifact_files, deliverable),
            "artifact_files": artifact_files,
            "quality_result": pipeline_result.get("quality"),
            "generation_log_ref": pipeline_result.get("pipeline_trace"),
            "dry_run": pipeline_result.get("dry_run", False),
        },
        "generation_status": gen_status,
        "quality_score": _normalize_quality_score(raw_quality),
        "creation_method": "adapter_generated",
        "created_at": now,
        "updated_at": now,
    }
