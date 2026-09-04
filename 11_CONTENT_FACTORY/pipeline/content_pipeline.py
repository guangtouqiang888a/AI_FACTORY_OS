# 11_CONTENT_FACTORY/pipeline/content_pipeline.py — 真实数字商品生产流水线

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

FACTORY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FACTORY_ROOT / "agents"))
sys.path.insert(0, str(FACTORY_ROOT / "schemas"))
sys.path.insert(0, str(FACTORY_ROOT / "artifacts"))

from creator_agent import CreatorAgent  # noqa: E402
from market_agent import MarketAgent  # noqa: E402
from packaging_agent import PackagingAgent  # noqa: E402
from product_generator import ProductGeneratorAgent  # noqa: E402
from product_schema import DigitalProduct  # noqa: E402
from quality_agent import QualityAgent  # noqa: E402
from release_gate import ReleaseGateAgent  # noqa: E402

STORAGE_PATH = FACTORY_ROOT / "storage" / "product_memory.json"
REAL_EXTENSIONS = {".pptx", ".xlsx", ".docx", ".pdf"}


def validate_artifacts_experiment(
    product_id: str,
    artifact_files: list[str],
    artifact_path: str,
    product_type: str = "",
) -> dict:
    """Experiment 路径 Artifact Validation — Excel 等允许 xlsx + manual pdf，不强制 pptx。"""
    real = [f for f in artifact_files if Path(f).suffix.lower() in REAL_EXTENSIONS]
    missing = []
    if not real:
        missing.append("no real file (.pptx/.xlsx/.docx/.pdf)")

    has_pptx = any(f.endswith(".pptx") for f in real)
    has_xlsx = any(f.endswith(".xlsx") for f in real)
    has_docx = any(f.endswith(".docx") for f in real)
    has_pdf = any(f.endswith(".pdf") for f in real)

    type_lower = product_type.lower()
    if "excel" in type_lower or has_xlsx:
        passed = has_xlsx and (has_pdf or len(real) >= 1)
    elif "word" in type_lower or has_docx:
        passed = has_docx and (has_pdf or len(real) >= 1)
    elif "ppt" in type_lower or has_pptx:
        passed = has_pptx and has_pdf
    else:
        passed = len(real) > 0 and has_pdf

    return {
        "status": "ok" if passed else "failed",
        "product_id": product_id,
        "artifact_files": real,
        "has_pptx": has_pptx,
        "has_xlsx": has_xlsx,
        "has_pdf": has_pdf,
        "passed": passed,
        "missing": missing,
        "validation_mode": "experiment",
    }


def validate_artifacts(product_id: str, artifact_files: list[str], artifact_path: str) -> dict:
    """Artifact Validation — 检查真实交付文件是否存在。"""
    product_dir = Path(artifact_path)
    real = [f for f in artifact_files if Path(f).suffix.lower() in REAL_EXTENSIONS]
    missing = []
    if not real:
        missing.append("no real file (.pptx/.xlsx/.docx/.pdf)")
    has_pptx = any(f.endswith(".pptx") for f in real)
    has_pdf = any(f.endswith(".pdf") for f in real)
    passed = len(real) > 0 and has_pdf
    return {
        "status": "ok" if passed else "failed",
        "product_id": product_id,
        "artifact_files": real,
        "has_pptx": has_pptx,
        "has_pdf": has_pdf,
        "passed": passed,
        "missing": missing,
    }


class ContentPipeline:
    """
    market → creator → product_generator → artifact_validation
         → quality → packaging → release_gate → memory
    """

    def __init__(self):
        self.market = MarketAgent()
        self.creator = CreatorAgent()
        self.generator = ProductGeneratorAgent()
        self.quality = QualityAgent()
        self.packaging = PackagingAgent()
        self.release_gate = ReleaseGateAgent()

    def run(self, keyword: str, platform: str = "xianyu") -> dict:
        context: dict = {"keyword": keyword, "platform": platform}
        trace: list[dict] = []

        market_out = self.market.execute({"keyword": keyword}, context)
        trace.append({"step": "market", **market_out})
        if market_out["status"] != "ok":
            return self._fail("market", market_out, trace)
        context["market"] = market_out["result"]

        creator_out = self.creator.execute(
            {
                "keyword": keyword,
                "market": market_out["result"],
                "platform": platform,
                "market_requirement": market_out["result"].get("recommendation"),
            },
            context,
        )
        trace.append({"step": "creator", **creator_out})
        if creator_out["status"] != "ok":
            return self._fail("creator", creator_out, trace)

        product = DigitalProduct.from_dict(creator_out["result"]["product"])
        product_dict = product.to_dict()
        context["product"] = product_dict

        gen_out = self.generator.execute(
            {"product": product_dict, "keyword": keyword, "product_type": product_dict.get("product_type")},
            context,
        )
        trace.append({"step": "product_generator", **gen_out})
        if gen_out["status"] != "ok":
            return self._fail("product_generator", gen_out, trace)

        artifacts = {
            "artifact_path": gen_out["result"]["artifact_path"],
            "artifact_files": gen_out["result"]["artifact_files"],
            "product_type": gen_out["result"]["product_type"],
        }
        product_dict["artifact_path"] = artifacts["artifact_path"]
        context["artifacts"] = artifacts

        validation = validate_artifacts(product.id, artifacts["artifact_files"], artifacts["artifact_path"])
        trace.append({"step": "artifact_validation", "status": "ok", "result": validation, "logs": []})
        if not validation["passed"]:
            return {
                "status": "error",
                "failed_step": "artifact_validation",
                "error": validation,
                "pipeline_trace": trace,
            }

        quality_out = self.quality.execute({"product": product_dict, "artifacts": artifacts}, context)
        trace.append({"step": "quality", **quality_out})
        if quality_out["status"] != "ok":
            return self._fail("quality", quality_out, trace)

        product.quality_score = quality_out["result"]["quality_score"]
        product.update_scores(market=product.market_score, quality=quality_out["result"]["commercial_score"])
        product.status = quality_out["result"]["status"]
        product_dict = product.to_dict()
        context["product"] = product_dict
        context["quality"] = quality_out["result"]

        packaging_out = self.packaging.execute(
            {"keyword": keyword, "product": product_dict, "quality": quality_out["result"]},
            context,
        )
        trace.append({"step": "packaging", **packaging_out})
        if packaging_out["status"] != "ok":
            return self._fail("packaging", packaging_out, trace)
        context["packaging"] = packaging_out["result"]

        gate_out = self.release_gate.execute(
            {"product": product_dict, "quality": quality_out["result"], "packaging": packaging_out["result"], "artifacts": artifacts},
            context,
        )
        trace.append({"step": "release_gate", **gate_out})
        if gate_out["status"] != "ok":
            return self._fail("release_gate", gate_out, trace)

        result = {
            "status": "ok",
            "product_id": product.id,
            "artifact_path": artifacts["artifact_path"],
            "artifact_files": artifacts["artifact_files"],
            "quality_score": quality_out["result"]["quality_score"],
            "commercial_score": quality_out["result"]["commercial_score"],
            "release_status": gate_out["result"]["release_status"],
            "zip_path": packaging_out["result"].get("zip_path"),
            "product": product_dict,
            "artifacts": artifacts,
            "quality": quality_out["result"],
            "packaging": packaging_out["result"],
            "release_gate": gate_out["result"],
            "pipeline_trace": trace,
        }
        self._save_product(result)
        return result

    def run_from_production_request(self, input_package: dict, *, dry_run: bool = False) -> dict:
        """
        Experiment Production Path — 跳过 MarketAgent，从 Creator 开始。

        dry_run=True：仅执行 Creator 阶段，不调用 Generator / 不写入 product_memory。
        """
        production_request_id = input_package.get("production_request_id", "")
        product_name = input_package.get("product_name") or input_package.get("keyword", "")
        platform = input_package.get("platform", "xianyu")
        cf_product_type = input_package.get("cf_product_type") or input_package.get("product_type", "")
        market_stub = input_package.get("market_stub") or {}

        context: dict = {
            "keyword": product_name,
            "platform": platform,
            "production_request_id": production_request_id,
            "source_experiment_id": input_package.get("source_experiment_id"),
            "experiment_id": input_package.get("experiment_id"),
            "approval_id": input_package.get("approval_id"),
            "validation_goal": input_package.get("validation_goal"),
            "priority": input_package.get("priority"),
            "asset_requirements": input_package.get("asset_requirements"),
            "quality_requirements": input_package.get("quality_requirements"),
            "production_path": "experiment",
        }
        trace: list[dict] = []

        trace.append({
            "step": "market",
            "status": "skipped",
            "result": {"reason": "Experiment path bypasses MarketAgent", "market_stub": market_stub},
            "logs": ["MarketAgent bypassed for approved Production Request"],
        })

        creator_out = self.creator.execute(
            {
                "keyword": product_name,
                "product_type": cf_product_type,
                "target_customer": input_package.get("target_customer"),
                "platform": platform,
                "market": market_stub,
                "market_requirement": market_stub.get("recommendation"),
                "structure_outline": input_package.get("structure_outline"),
                "asset_requirements": input_package.get("asset_requirements"),
            },
            context,
        )
        trace.append({"step": "creator", **creator_out})
        if creator_out["status"] != "ok":
            return self._fail("creator", creator_out, trace)

        product = DigitalProduct.from_dict(creator_out["result"]["product"])
        product_dict = product.to_dict()
        product_dict["production_request_id"] = production_request_id
        product_dict["source_experiment_id"] = input_package.get("source_experiment_id")
        context["product"] = product_dict

        if dry_run:
            return {
                "status": "dry_run",
                "dry_run": True,
                "product_id": product.id,
                "artifact_path": creator_out["result"]["artifacts"].get("artifact_path"),
                "artifact_files": [],
                "product": product_dict,
                "artifacts": creator_out["result"].get("artifacts", {}),
                "pipeline_trace": trace,
                "production_request_id": production_request_id,
                "message": "Dry run — Generator skipped; no commercial deliverable files created",
            }

        gen_out = self.generator.execute(
            {
                "product": product_dict,
                "keyword": product_name,
                "product_type": cf_product_type,
                "structure_outline": input_package.get("structure_outline"),
                "asset_requirements": input_package.get("asset_requirements"),
            },
            context,
        )
        trace.append({"step": "product_generator", **gen_out})
        if gen_out["status"] != "ok":
            return self._fail("product_generator", gen_out, trace)

        artifacts = {
            "artifact_path": gen_out["result"]["artifact_path"],
            "artifact_files": gen_out["result"]["artifact_files"],
            "product_type": gen_out["result"]["product_type"],
        }
        product_dict["artifact_path"] = artifacts["artifact_path"]
        context["artifacts"] = artifacts

        validation = validate_artifacts_experiment(
            product.id,
            artifacts["artifact_files"],
            artifacts["artifact_path"],
            product_type=input_package.get("product_type", cf_product_type),
        )
        trace.append({"step": "artifact_validation", "status": "ok", "result": validation, "logs": []})
        if not validation["passed"]:
            return {
                "status": "error",
                "failed_step": "artifact_validation",
                "error": validation,
                "pipeline_trace": trace,
                "production_request_id": production_request_id,
            }

        quality_out = self.quality.execute({"product": product_dict, "artifacts": artifacts}, context)
        trace.append({"step": "quality", **quality_out})
        if quality_out["status"] != "ok":
            return self._fail("quality", quality_out, trace)

        product.quality_score = quality_out["result"]["quality_score"]
        product.update_scores(market=product.market_score, quality=quality_out["result"]["commercial_score"])
        product.status = quality_out["result"]["status"]
        product_dict = product.to_dict()
        product_dict["production_request_id"] = production_request_id
        context["product"] = product_dict
        context["quality"] = quality_out["result"]

        packaging_out = self.packaging.execute(
            {"keyword": product_name, "product": product_dict, "quality": quality_out["result"]},
            context,
        )
        trace.append({"step": "packaging", **packaging_out})
        if packaging_out["status"] != "ok":
            return self._fail("packaging", packaging_out, trace)
        context["packaging"] = packaging_out["result"]

        gate_out = self.release_gate.execute(
            {
                "product": product_dict,
                "quality": quality_out["result"],
                "packaging": packaging_out["result"],
                "artifacts": artifacts,
            },
            context,
        )
        trace.append({"step": "release_gate", **gate_out})
        if gate_out["status"] != "ok":
            return self._fail("release_gate", gate_out, trace)

        result = {
            "status": "ok",
            "product_id": product.id,
            "artifact_path": artifacts["artifact_path"],
            "artifact_files": artifacts["artifact_files"],
            "quality_score": quality_out["result"]["quality_score"],
            "commercial_score": quality_out["result"]["commercial_score"],
            "release_status": gate_out["result"]["release_status"],
            "zip_path": packaging_out["result"].get("zip_path"),
            "product": product_dict,
            "artifacts": artifacts,
            "quality": quality_out["result"],
            "packaging": packaging_out["result"],
            "release_gate": gate_out["result"],
            "pipeline_trace": trace,
            "production_request_id": production_request_id,
            "source_experiment_id": input_package.get("source_experiment_id"),
        }
        self._save_product(result)
        return result

    def _fail(self, step: str, agent_out: dict, trace: list) -> dict:
        return {"status": "error", "failed_step": step, "error": agent_out.get("result", {}), "pipeline_trace": trace}

    def _save_product(self, result: dict) -> None:
        STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        memory = self._load_memory()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p = result["product"]
        entry = {
            "product_id": p["id"],
            "category": p.get("category", ""),
            "score": result["quality_score"],
            "artifact_path": result["artifact_path"],
            "artifact_files": result.get("artifact_files", []),
            "zip_path": result.get("zip_path"),
            "commercial_score": result.get("commercial_score"),
            "release_status": result.get("release_status"),
            "status": p.get("status", ""),
            "created_time": p.get("created_at", now),
            "saved_at": now,
            "product": p,
            "quality": result["quality"],
        }
        memory.setdefault("products", []).append(entry)
        memory.setdefault("history", []).append(
            {
                "product_id": p["id"],
                "category": p.get("category"),
                "score": result["quality_score"],
                "commercial_score": result.get("commercial_score"),
                "artifact_path": result["artifact_path"],
                "zip_path": result.get("zip_path"),
                "release_status": result.get("release_status"),
                "status": p.get("status"),
                "created_time": entry["created_time"],
            }
        )
        memory["updated_at"] = now
        STORAGE_PATH.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")

    def _load_memory(self) -> dict:
        if STORAGE_PATH.exists():
            data = json.loads(STORAGE_PATH.read_text(encoding="utf-8"))
            data.setdefault("products", [])
            data.setdefault("history", [])
            return data
        return {"products": [], "history": [], "updated_at": None}


def main() -> None:
    keyword = sys.argv[1] if len(sys.argv) > 1 else "办公PPT模板"
    print("=" * 60)
    print("11_CONTENT_FACTORY — Real Digital Product Production")
    print("=" * 60)
    print(f"[Input] keyword={keyword}\n")

    pipeline = ContentPipeline()
    result = pipeline.run(keyword)

    if result["status"] == "ok":
        print("--- market → creator → generator → validation → quality → packaging → release_gate → memory ---")
        print(f"[Product] product_id={result['product_id']}")
        print(f"[Artifact] artifact_path={result['artifact_path']}")
        print(f"[Files] {result.get('artifact_files')}")
        print(f"[Quality] quality_score={result['quality_score']}")
        print(f"[Commercial] commercial_score={result['commercial_score']}")
        print(f"[Release] release_status={result['release_status']}")
        print(f"[Bundle] zip_path={result.get('zip_path')}")
        print(f"\n[Storage] saved to {STORAGE_PATH}")
        print("=" * 60)
        print("[OK] Real product pipeline complete")
    else:
        print(f"[ERROR] failed at step={result.get('failed_step')}")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
