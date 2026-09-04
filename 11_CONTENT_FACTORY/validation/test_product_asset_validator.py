# 11_CONTENT_FACTORY/validation/test_product_asset_validator.py — Entry 033-A Validation Runtime Tests

from __future__ import annotations

import sys
from pathlib import Path

VALIDATION_ROOT = Path(__file__).resolve().parent
FACTORY_ROOT = VALIDATION_ROOT.parent
sys.path.insert(0, str(VALIDATION_ROOT))

from product_asset_validator import ProductAssetValidator  # noqa: E402

EXISTING_ARTIFACT_DIR = FACTORY_ROOT / "artifacts" / "products" / "e601c17c6977"


def _base_valid_asset() -> dict:
    return {
        "object_type": "product_asset",
        "contract_version": "1.0",
        "product_asset_id": "passet_test_valid_001",
        "source_production_request_id": "preq_20260712_005",
        "source_experiment_id": "exp_20260708_005",
        "approval_id": "appr_20260713_005",
        "product_name": "Excel 考勤记录表",
        "product_type": "excel",
        "asset_category": "office_template",
        "quality_score": 0.90,
        "creation_method": "adapter_generated",
        "artifact_information": {
            "artifact_path": str(EXISTING_ARTIFACT_DIR),
            "primary_file": "documents/product_manual.pdf",
            "file_type": "pdf",
            "artifact_files": ["documents/product_manual.pdf"],
        },
        "validation_context": {
            "validation_goal": "验证低竞争细分小团队考勤 Excel 是否有首单转化",
            "asset_requirements": {
                "deliverable_format": "xlsx",
                "structure_outline": ["考勤明细表", "月度汇总", "使用说明"],
            },
            "quality_requirements": {
                "min_quality_score": 0.85,
            },
        },
    }


def test_1_valid_product_asset_passed() -> None:
    validator = ProductAssetValidator()
    result = validator.validate_check_only(_base_valid_asset())
    assert result["validation_status"] == "passed", result
    print("[PASS] TEST1: valid Product Asset -> passed")


def test_2_missing_artifact_path_failed() -> None:
    asset = _base_valid_asset()
    asset["artifact_information"] = {
        "artifact_path": None,
        "file_type": "pdf",
        "artifact_files": [],
    }
    validator = ProductAssetValidator()
    result = validator.validate_check_only(asset)
    assert result["validation_status"] == "failed", result
    failed_ids = result["validation_result"]["blockers"]
    assert "artifact.path_valid" in failed_ids
    print("[PASS] TEST2: missing artifact_path -> failed")


def test_3_quality_score_below_threshold_failed() -> None:
    asset = _base_valid_asset()
    asset["quality_score"] = 0.70
    validator = ProductAssetValidator()
    result = validator.validate_check_only(asset)
    assert result["validation_status"] == "failed", result
    assert "quality.threshold_met" in result["validation_result"]["blockers"]
    print("[PASS] TEST3: quality_score < 0.85 -> failed")


def test_4_missing_production_request_id_failed() -> None:
    asset = _base_valid_asset()
    asset["source_production_request_id"] = ""
    validator = ProductAssetValidator()
    result = validator.validate_check_only(asset)
    assert result["validation_status"] == "failed", result
    assert "contract.production_request_id" in result["validation_result"]["blockers"]
    print("[PASS] TEST4: missing production_request_id -> failed")


def test_validation_object_shape() -> None:
    validator = ProductAssetValidator()
    obj = validator.validate(_base_valid_asset())
    assert obj["object_type"] == "product_asset_validation"
    assert obj["contract_version"] == "1.0"
    assert obj["validation_method"] == "human_assisted"
    assert obj["validation_status"] == "passed"
    assert "validation_id" in obj
    assert obj["validation_id"].startswith("pval_")
    assert "review_items" in obj
    assert "validation_result" in obj
    print("[PASS] TEST5: product_asset_validation object shape")


def main() -> int:
    print("=" * 60)
    print("Entry 033-A — Product Asset Validation Runtime Tests")
    print("Validation Runtime Completed ≠ Production Started")
    print("=" * 60)
    test_1_valid_product_asset_passed()
    test_2_missing_artifact_path_failed()
    test_3_quality_score_below_threshold_failed()
    test_4_missing_production_request_id_failed()
    test_validation_object_shape()
    print("=" * 60)
    print("SUMMARY: 5/5 PASS")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
