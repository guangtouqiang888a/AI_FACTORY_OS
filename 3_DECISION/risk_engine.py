# 3_DECISION/risk_engine.py — 风险过滤

SENSITIVE_KEYWORDS = {"赌博", "色情", "盗版", "侵权", "假货"}


def assess_risk(product: dict) -> dict:
    """返回风险等级与是否通过。"""
    title = str(product.get("title") or "")
    keyword = str(product.get("keyword") or "")
    text = title + keyword

    flags = [w for w in SENSITIVE_KEYWORDS if w in text]
    if flags:
        return {"passed": False, "level": "high", "reason": f"敏感词: {','.join(flags)}"}

    price = float(product.get("price") or 0)
    if price <= 0:
        return {"passed": True, "level": "low", "reason": "价格为零，标记低风险"}

    return {"passed": True, "level": "low", "reason": "通过"}
