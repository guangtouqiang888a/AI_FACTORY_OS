# 1_DATA/sources.py — 数据源字段映射 + origin helpers
#
# Entry 058B: normalization only. Source platform ≠ sales platform.

STANDARD_FIELDS = [
    "title", "price", "want_count", "view_count", "comment_count",
    "share_count", "seller", "tags", "publish_time", "source_url",
    "source_item_id",
]

# Schema-reserved vs Reality (058B audit):
# REALITY (via Excel/import columns if present): title, price, want_count, view_count,
#   comment_count, share_count, seller, tags, publish_time, source_url
# PARTIAL: source_item_id (derived from URL when possible)
# UNAVAILABLE in live scrape (no live connector): all live-fetched fields

XIANYU_COLUMN_MAP = {
    "标题": "title",
    "title": "title",
    "价格": "price",
    "price": "price",
    "想要数": "want_count",
    "want_count": "want_count",
    "浏览量": "view_count",
    "view_count": "view_count",
    "评论数": "comment_count",
    "comment_count": "comment_count",
    "分享数": "share_count",
    "share_count": "share_count",
    "卖家": "seller",
    "seller": "seller",
    "标签": "tags",
    "tags": "tags",
    "发布时间": "publish_time",
    "publish_time": "publish_time",
    "链接": "source_url",
    "source_url": "source_url",
    "商品ID": "source_item_id",
    "source_item_id": "source_item_id",
    "item_id": "source_item_id",
}


def normalize_row(raw: dict, column_map: dict | None = None) -> dict:
    """将原始行映射为标准字段。"""
    mapping = column_map or XIANYU_COLUMN_MAP
    out = {}
    for src_key, value in raw.items():
        key = str(src_key).strip()
        field = mapping.get(key)
        if field:
            out[field] = value
    return out


def field_availability_matrix() -> dict:
    """Document Reality vs schema for Xianyu path (Entry 058B)."""
    return {
        "collection_path": "EXTERNAL_IMPORT (Excel/CSV) — LIVE_COLLECTION MISSING",
        "fields": {
            "title": "REALITY_IF_PRESENT_IN_EXPORT",
            "price": "REALITY_IF_PRESENT_IN_EXPORT",
            "want_count": "REALITY_IF_PRESENT_IN_EXPORT",
            "view_count": "REALITY_IF_PRESENT_IN_EXPORT",
            "comment_count": "REALITY_IF_PRESENT_IN_EXPORT",
            "share_count": "REALITY_IF_PRESENT_IN_EXPORT",
            "seller": "REALITY_IF_PRESENT_IN_EXPORT",
            "publish_time": "REALITY_IF_PRESENT_IN_EXPORT",
            "source_url": "REALITY_IF_PRESENT_IN_EXPORT",
            "source_item_id": "PARTIAL_DERIVED_FROM_URL",
            "live_http_fetch": "MISSING",
        },
    }
