# AI_FACTORY_OS Database Alignment Report

> **文档角色（Document Role）：** 本文档为历史参考资料，用于理解演进过程，不作为当前最高判断来源。  
> Current highest judgment（当前最高判断）：CURRENT_STATE + Reality（`database.py` / `ai_factory.db`）。

> Entry 038-B | Database Reality Alignment | 审计日期：2026-07-13  
> **本阶段不修改数据库。**

**对照文件：** `1_DATA/database.py` — `ensure_schema()`  
**实际数据库：** `data/ai_factory.db`

---

## 1. 实际数据库概览

| 表名 | 行数 | Python 写入（当前代码） |
|------|------|-------------------------|
| platforms | 1 | ✅ ensure_schema INSERT |
| products | 61 | ✅ collector → insert_product |
| keywords | 6 | ✅ upsert_keyword |
| collection_log | 29 | ✅ start/finish_collection_log |
| scores | 519 | ✅ save_score |
| trends | 0 | ❌ 无 |
| audit_log | 1 | ❌ 无 |
| sqlite_sequence | 6 | SQLite 内部 |

---

## 2. 逐表对照

### 2.1 platforms

| 来源 | 字段 |
|------|------|
| **database.py ensure_schema** | id, name |
| **ai_factory.db 实际** | id, name, **base_url**, **status** |

**差异：** DB 含 2 个额外列，代码未创建、未读写。

---

### 2.2 products

| 来源 | 字段 |
|------|------|
| **database.py** | id, platform_id, keyword, title, price, want_count, view_count, comment_count, share_count, seller, tags, publish_time, source_url, raw_json, collect_date |
| **ai_factory.db 实际** | 与代码定义 **一致** |

**差异：** 无字段差异。

---

### 2.3 keywords

| 来源 | 字段 |
|------|------|
| **database.py** | id, keyword, category, first_seen_date, last_seen_date, is_sensitive, is_low_efficiency, last_search_date |
| **ai_factory.db 实际** | 与代码定义 **一致** |

**差异：** 无。

---

### 2.4 collection_log

| 来源 | 字段 |
|------|------|
| **database.py** | id, task_date, platform_id, keyword, total_items, valid_items, status, started_at, finished_at |
| **ai_factory.db 实际** | 与代码定义 **一致** |

**差异：** 无。

---

### 2.5 scores

| 来源 | 字段 |
|------|------|
| **database.py** | id, product_id, hot_score, trend_score, comp_score, profit_score, difficulty_score, total_score, scored_date |
| **ai_factory.db 实际** | 与代码定义 **一致** |

**差异：** 无。

---

### 2.6 trends

| 来源 | 字段 |
|------|------|
| **database.py ensure_schema** | ❌ **未定义** |
| **ai_factory.db 实际** | id, snapshot_date, platform_id, keyword, total_products, avg_price, avg_want, growth_rate |

**差异：** 表存在于 DB，代码不创建、不读写。0 行。

**可能来源：** 历史 migration 或手动 schema（不可从当前 Python 追溯）。

---

### 2.7 audit_log

| 来源 | 字段 |
|------|------|
| **database.py ensure_schema** | ❌ **未定义** |
| **ai_factory.db 实际** | id, audit_type, target, passed, score, issues, suggestions, created_at |

**差异：** 表存在于 DB，代码不创建、不读写。1 行 — 写入来源未知。

---

## 3. 差异汇总表

| ID | 类型 | 描述 | 严重度 |
|----|------|------|--------|
| DBA-001 | 列漂移 | platforms: DB 有 base_url, status；database.py 无 | P1 |
| DBA-002 | 表缺失（代码侧） | trends 在 DB 存在，ensure_schema 未创建 | P1 |
| DBA-003 | 表缺失（代码侧） | audit_log 在 DB 存在，ensure_schema 未创建 | P1 |
| DBA-004 | 孤儿数据 | audit_log 1 行，无 Python writer | P2 |
| DBA-005 | Bootstrap 风险 | 新环境 ensure_schema() 不会创建 trends/audit_log | P1 |

---

## 4. 代码定义表清单（ensure_schema）

`database.py` 仅定义并创建：

1. platforms  
2. products  
3. keywords  
4. collection_log  
5. scores  

---

## 5. 与 Blueprint 关系

- `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` 可能描述 trends 等扩展表
- **当前 Runtime 仅使用** products / keywords / collection_log / scores / platforms（部分列）
- Commercial 链 **不使用** SQLite

---

## 6. 建议方向（不实施 — 供未来 Entry）

| 优先级 | 建议 |
|--------|------|
| P1 | Entry 授权：database.py ensure_schema 与 DB  reality 对齐（additive migration） |
| P1 | 文档化 audit_log 1 行来源或归档 |
| P2 | trends 表：实现 writer 或标记 deprecated |
| P3 | Commercial Experiment 台账 DB 扩展（PROJECT_STATUS Pending） |

---

## 7. 本 Entry 操作

- ✅ 只读审计
- ❌ 未修改 `data/ai_factory.db`
- ❌ 未修改 `database.py`
