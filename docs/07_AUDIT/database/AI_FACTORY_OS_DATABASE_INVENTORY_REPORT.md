# AI_FACTORY_OS Database Inventory Report

> Entry 039-A — Database Alignment & State Authority Design v1  
> 审计日期：2026-07-14  
> **方法：** 只读检查 `data/` 与 `data/ai_factory.db`  
> **禁止：** 本 Entry 未修改数据库、未 CREATE/ALTER TABLE

**原则：** Database Reality ≠ Documentation Reality · Design Schema ≠ Runtime Schema

---

## Database Overview

| 项 | 事实 |
|----|------|
| **主数据库文件** | `data/ai_factory.db` |
| **文件大小** | 81,920 bytes（80 KB） |
| **引擎** | SQLite |
| **用户表数量** | 7（不含 `sqlite_sequence`） |
| **含内部表合计** | 8 |
| **其他 data/ 文件** | `data/raw/xianyu/2026-07-04/` 下 1 个 Excel sample（~5 KB） |
| **JSON DB** | `data/` 下无独立 JSON 数据库 |

---

## Table Inventory

### platforms

| 字段 | 值 |
|------|-----|
| **table_name** | `platforms` |
| **columns** | id (INTEGER PK), name (TEXT NOT NULL), base_url (TEXT), status (TEXT) |
| **primary_key** | `id` |
| **record_count** | 1 |
| **created_by** | `1_DATA/database.py` — `ensure_schema()` INSERT OR IGNORE xianyu（仅 id/name）；`base_url`/`status` 列来源不可从当前 Python 追溯 |
| **used_by** | `1_DATA/collector.py`（platform_id=1 常量引用） |

---

### products

| 字段 | 值 |
|------|-----|
| **table_name** | `products` |
| **columns** | id, platform_id, keyword, title, price, want_count, view_count, comment_count, share_count, seller, tags, publish_time, source_url, raw_json, collect_date |
| **primary_key** | `id` |
| **record_count** | 61 |
| **created_by** | `1_DATA/collector.py` → `database.insert_product()` |
| **used_by** | `1_DATA/collector.py`（读）, `3_DECISION/scoring_agent.py`（读）, `database.get_products_by_keyword` / `get_top_scored_products` |

---

### keywords

| 字段 | 值 |
|------|-----|
| **table_name** | `keywords` |
| **columns** | id, keyword, category, first_seen_date, last_seen_date, is_sensitive, is_low_efficiency, last_search_date |
| **primary_key** | `id` |
| **record_count** | 6 |
| **created_by** | `1_DATA/collector.py` → `database.upsert_keyword()` |
| **used_by** | collector（写为主）；无独立跨模块读专用路径 |

---

### collection_log

| 字段 | 值 |
|------|-----|
| **table_name** | `collection_log` |
| **columns** | id, task_date, platform_id, keyword, total_items, valid_items, status, started_at, finished_at |
| **primary_key** | `id` |
| **record_count** | 29 |
| **created_by** | `database.start_collection_log` / `finish_collection_log` |
| **used_by** | `1_DATA/collector.py`（写）；无专用业务读取代码 |

---

### scores

| 字段 | 值 |
|------|-----|
| **table_name** | `scores` |
| **columns** | id, product_id, hot_score, trend_score, comp_score, profit_score, difficulty_score, total_score, scored_date |
| **primary_key** | `id` |
| **record_count** | 519 |
| **created_by** | `3_DECISION/scoring_agent.py` → `database.save_score()` |
| **used_by** | `database.get_top_scored_products`；Decision 主要用内存中已评分 products |

---

### trends

| 字段 | 值 |
|------|-----|
| **table_name** | `trends` |
| **columns** | id, snapshot_date, platform_id, keyword, total_products, avg_price, avg_want, growth_rate |
| **primary_key** | `id` |
| **record_count** | 0 |
| **created_by** | ❌ **当前 `database.py` 无 CREATE**；表存在于文件但写入模块未知 |
| **used_by** | ❌ 无 Python 读写引用（038-A/039 grep 确认） |

---

### audit_log

| 字段 | 值 |
|------|-----|
| **table_name** | `audit_log` |
| **columns** | id, audit_type, target, passed, score, issues, suggestions, created_at |
| **primary_key** | `id` |
| **record_count** | 1 |
| **created_by** | ❌ **当前 `database.py` 无 CREATE / INSERT**；1 行来源不可从现行代码追溯 |
| **used_by** | ❌ 无 Python 读写引用 |

---

### sqlite_sequence

| 字段 | 值 |
|------|-----|
| **table_name** | `sqlite_sequence` |
| **columns** | name, seq |
| **primary_key** | （内部） |
| **record_count** | 6 |
| **created_by** | SQLite AUTOINCREMENT 元数据 |
| **used_by** | SQLite 内部 |

---

## Module Usage Matrix

| 模块 | 读 DB | 写 DB |
|------|-------|-------|
| `0_START/controller.py` | — | boot → `ensure_schema()` |
| `1_DATA/collector.py` | ✅ products | ✅ products/keywords/collection_log |
| `1_DATA/database.py` | ✅ | ✅ |
| `3_DECISION/scoring_agent.py` | ✅ products | ✅ scores |
| `3_DECISION/decision_engine.py` | 间接（经 agents） | ❌ |
| `11_CONTENT_FACTORY` | ❌ | ❌ |
| `commercial_assets` 链 | ❌ | ❌ |
| `7_MEMORY` | ❌ | ❌ |

---

## Summary

| 指标 | 值 |
|------|-----|
| Active tables（有代码读写） | platforms*, products, keywords, collection_log, scores |
| Orphan / drift tables | trends (0 rows), audit_log (1 row) |
| Total business rows（products+scores+logs+keywords+platforms） | 61+519+29+6+1 = 616+ |
| Commercial objects in SQLite | **0** |

\* platforms：代码只保证 id/name；extra 列存在但未读写。

---

## 本 Entry 操作

- ✅ 只读 inventory
- ❌ 未修改 `data/ai_factory.db`
- ❌ 未修改任何 Python
