# AI_FACTORY_OS Schema Drift Report

> Entry 039-A | Schema Drift Audit | 2026-07-14  
> **对照：** `1_DATA/database.py` `ensure_schema()` vs `data/ai_factory.db`  
> **禁止修改：** 本报告只读

**原则：** Design Schema ≠ Runtime Schema · Database Reality ≠ Code Reality

**相关：** `docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_ALIGNMENT_REPORT.md`（038-B）— 本报告为正式 Conflict 台账

---

## Code Schema Source

**唯一数据库定义文件：** `1_DATA/database.py`

`ensure_schema()` 创建并维护的表：

1. `platforms` — columns: `id`, `name`
2. `products` — 15 列（与 DB 一致）
3. `keywords` — 8 列（与 DB 一致）
4. `collection_log` — 9 列（与 DB 一致）
5. `scores` — 9 列（与 DB 一致）

**未在代码中定义：** `trends`, `audit_log`

**相关读写模块：** `collector.py`, `scoring_agent.py`, `controller.py`（boot ensure_schema）

---

## Conflicts

### Conflict ID: SD-001

| 项 | 内容 |
|----|------|
| **Table** | `platforms` |
| **Database Reality** | columns: id, name, **base_url**, **status**；rows=1 |
| **Code Reality** | `CREATE TABLE platforms (id, name)` — 无 base_url / status |
| **Risk** | 新环境 bootstrap 只含两列；现网文件多两列无人读写；文档若按 DB 假设读写会失败 |
| **Recommendation** | 未来 Entry：additive 对齐 ensure_schema（加入列）或文档声明列为 deprecated orphan |

---

### Conflict ID: SD-002

| 项 | 内容 |
|----|------|
| **Table** | `trends` |
| **Database Reality** | 表存在；8 列；**0 rows** |
| **Code Reality** | `ensure_schema()` **不创建**；全 repo 无 Python 读/写 |
| **Risk** | Bootstrap 后新库无此表；Blueprint 可能引用但 Runtime 不可依赖 |
| **Recommendation** | 标记 Orphan Schema；实现 writer 前不得当作 Cognition 数据源；或未来 additive CREATE |

---

### Conflict ID: SD-003

| 项 | 内容 |
|----|------|
| **Table** | `audit_log` |
| **Database Reality** | 表存在；8 列；**1 row**（写入来源未知） |
| **Code Reality** | `ensure_schema()` **不创建**；全 repo 无 Python 读/写 |
| **Risk** | 孤儿数据；新环境无表；审计/合规误以为有 Runtime audit trail |
| **Recommendation** | 只读归档该行语义或 deprecate；正式审计走 `7_MEMORY/event_log.jsonl` |

---

### Conflict ID: SD-004

| 项 | 内容 |
|----|------|
| **Table** | （bootstrap set） |
| **Database Reality** | 现网含 7 用户表 |
| **Code Reality** | 新机 `ensure_schema()` 仅 5 表；无 trends/audit_log；platforms 少 2 列 |
| **Risk** | **环境分叉** — 同一 codebase 不同库文件 schema 不一致 |
| **Recommendation** | 单独授权 Schema Alignment Entry；Additive 优先；禁止破坏 61 products / 519 scores |

---

### Conflict ID: SD-005

| 项 | 内容 |
|----|------|
| **Table** | Blueprints vs Runtime（文档层） |
| **Database Reality** | 仅市场 listing 采集表 + scores；**无** Opportunity / Experiment / Product Asset 表 |
| **Code Reality** | 同上；Commercial 全在 `commercial_assets/*.json` |
| **Risk** | DATABASE_SCHEMA_BLUEPRINT / Migration Plan 易被误读为「表已存在」 |
| **Recommendation** | 本 Entry State Authority / Boundary 文档固化：**Commercial Object SoT = JSON**；DB Extension Implementation **Pending** |

---

### Non-Conflicts（对齐确认）

| Table | Status |
|-------|--------|
| products | ✅ Code schema = DB schema |
| keywords | ✅ |
| collection_log | ✅ |
| scores | ✅ |

---

## Severity Summary

| Conflict ID | Severity | Type |
|-------------|----------|------|
| SD-001 | P1 | Column drift |
| SD-002 | P1 | Orphan table |
| SD-003 | P1 | Orphan table + orphan row |
| SD-004 | P0 | Environment bootstrap divergence |
| SD-005 | P1 | Blueprint vs Reality confusion |

---

## 本 Entry 操作

- ✅ 冲突台账
- ❌ 未修改 database.py
- ❌ 未修改 ai_factory.db
