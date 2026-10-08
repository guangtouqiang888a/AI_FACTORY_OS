# 11_CONTENT_FACTORY/schemas/product_schema.py — DigitalProduct 统一产品对象

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class DigitalProduct:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    title: str = ""
    category: str = ""
    target_customer: str = ""
    problem: str = ""
    content: str = ""
    market_score: float = 0.0
    quality_score: float = 0.0
    profit_score: float = 0.0
    price: float = 0.0
    platform: str = "xianyu"
    status: str = "draft"
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DigitalProduct:
        known = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)

    def update_scores(self, market: float | None = None, quality: float | None = None) -> None:
        if market is not None:
            self.market_score = round(market, 2)
        if quality is not None:
            self.quality_score = round(quality, 2)
        self.profit_score = round(
            (self.market_score * 0.4 + self.quality_score * 0.6) * (self.price / 100 if self.price else 0.5),
            2,
        )
