# 6_EXECUTION/publisher.py — 执行层（本地发布 / 输出）

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
import config  # noqa: E402


def publish(decision: dict) -> dict:
    """
    根据决策结果执行发布动作。
    当前实现：将候选商品写入 output/ 目录（模拟分发）。
    """
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    keyword = decision.get("keyword", "unknown")
    action = decision.get("action", "skip")

    if action == "skip":
        result = {"status": "skipped", "keyword": keyword, "reason": decision.get("reason")}
        out_path = config.OUTPUT_DIR / f"skip_{keyword}_{datetime.now():%Y%m%d_%H%M%S}.json"
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result

    best = decision.get("best") or {}
    payload = {
        "status": "published_local",
        "keyword": keyword,
        "title": best.get("title"),
        "price": best.get("price"),
        "total_score": (best.get("scores") or {}).get("total"),
        "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": "本地模拟发布 — 待接入真实平台 API",
    }
    out_path = config.OUTPUT_DIR / f"publish_{keyword}_{datetime.now():%Y%m%d_%H%M%S}.json"
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "published_local", "path": str(out_path), **payload}
