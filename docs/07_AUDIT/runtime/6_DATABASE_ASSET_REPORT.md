# Database Asset Report

> Entry 038-A | data/ 存储审计

---

## 存储清单

| 文件 | 类型 | 存在 | 说明 |
|------|------|------|------|
| `data/ai_factory.db` | SQLite | ✅ | 主 Operational Database |
| `data/raw/xianyu/` | 目录 | ⚠️ 配置存在 | config.RAW_XIANYU_DIR；工作区 glob 未列出文件（可能 gitignore 或空） |

**JSON DB：** 无独立 JSON 数据库文件于 `data/`。

**其他存储：**
- `7_MEMORY/*.json` — OS 运行时记忆（非 data/ 目录）
- `11_CONTENT_FACTORY/storage/product_memory.json` — CF 产品记忆
- `commercial_assets/**/*.json` — 商业对象（Governance Protocol 定义的 Commercial Object SoT）

---

## data/ai_factory.db 详情

**路径：** `d:\AI_FACTORY_OS\data\ai_factory.db`  
**读取方式：** Python sqlite3 只读查询（2026-07-13 审计）

### 表：platforms

| 字段 | 类型 | 行数 |
|------|------|------|
| id | INTEGER | 1 |
| name | TEXT | |
| base_url | TEXT | |
| status | TEXT | |

**写入模块：** `1_DATA/database.py` — `ensure_schema()` INSERT OR IGNORE xianyu  
**读取模块：** collector（platform_id=1）  
**生命周期：** 静态平台注册  
**与 JSON 重复：** ❌  
**Schema 漂移：** ⚠️ `database.py ensure_schema` 仅定义 id+name；DB 实际含 base_url, status

---

### 表：products

| 字段 | 类型 |
|------|------|
| id, platform_id, keyword, title, price, want_count, view_count, comment_count, share_count, seller, tags, publish_time, source_url, raw_json, collect_date | 见 database.py |

**行数：** 61  
**写入模块：** `1_DATA/collector.py` → `database.insert_product()`  
**读取模块：** `ScoringAgent`, `decision_engine`, `get_products_by_keyword`  
**生命周期：** 按 collect_date 累积；无自动 purge  
**与 JSON 重复：** ❌ 与 commercial_assets Product Asset **不同对象**（市场 listing vs 自产数字商品）

---

### 表：keywords

**行数：** 6  
**写入模块：** `database.upsert_keyword()`  
**读取模块：** collector  
**生命周期：** 首次/末次 seen 日期追踪

---

### 表：collection_log

**行数：** 29  
**写入模块：** `start_collection_log` / `finish_collection_log`  
**读取模块：** 无专用读取代码  
**生命周期：** 每次采集任务一条 log

---

### 表：scores

| 字段 | hot_score, trend_score, comp_score, profit_score, difficulty_score, total_score, scored_date, product_id |
|------|------|

**行数：** 519  
**写入模块：** `3_DECISION/scoring_agent.py` → `database.save_score()`  
**读取模块：** `decision_engine`, `get_top_scored_products`  
**生命周期：** 每次评分 INSERT（无 upsert）

---

### 表：trends

| 字段 | id, snapshot_date, platform_id, keyword, total_products, avg_price, avg_want, growth_rate |
|------|------|

**行数：** 0  
**写入模块：** ❌ **无 Python 代码引用**  
**读取模块：** ❌ 无  
**生命周期：** 未知 — 可能来自历史 migration 或手动 schema  
**与 Blueprint 关系：** `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` 可能定义；**当前 database.py 未创建**

---

### 表：audit_log

| 字段 | id, audit_type, target, passed, score, issues, suggestions, created_at |
|------|------|

**行数：** 1  
**写入模块：** ❌ **无 Python 代码引用**  
**读取模块：** ❌ 无  
**生命周期：** 孤立数据 — 来源不可从当前代码追溯

---

### 表：sqlite_sequence

**行数：** 6 — SQLite 内部 autoincrement 元数据

---

## database.py vs 实际 DB 一致性

| 项 | ensure_schema() 定义 | DB 实际 | 状态 |
|----|---------------------|---------|------|
| platforms 列 | id, name | + base_url, status | ⚠️ 漂移 |
| trends 表 | ❌ 未定义 | ✅ 存在 | ⚠️ 漂移 |
| audit_log 表 | ❌ 未定义 | ✅ 存在 | ⚠️ 漂移 |

**风险：** 新环境 `ensure_schema()` 可能不会创建 trends/audit_log；已有 DB 保留历史 schema。

---

## 读写模块矩阵

| 模块 | 读 DB | 写 DB |
|------|-------|-------|
| 0_START/controller | ✅ boot ensure_schema | 间接 |
| 1_DATA/collector | ✅ | ✅ |
| 1_DATA/database | ✅ | ✅ |
| 3_DECISION/scoring_agent | ✅ | ✅ scores |
| 3_DECISION/decision_engine | ✅ via products | ❌ |
| 11_CONTENT_FACTORY | ❌ | ❌ |
| commercial_assets 链 | ❌ | ❌ |

---

## 与 JSON 重复分析

| 数据语义 | SQLite | JSON | 重复？ |
|----------|--------|------|--------|
| 市场商品 listing | products | — | 否 |
| 机会/实验 | — | commercial_assets | 否（不同域） |
| 自产数字商品 | — | product_assets_v1.json | 否 |
| CF 生产历史 | — | product_memory.json | ⚠️ 与 product_assets 部分重叠 |
| OS 学习模式 | — | 7_MEMORY/pattern_memory.json | 否 |
| 评分 | scores 表 | selection_score in JSON | ⚠️ 语义重叠，数据不同源 |

---

## 结论

1. **Operational Database 存在且有数据** — 61 products, 519 scores
2. **Schema 与 database.py 不同步** — trends/audit_log/platforms 扩展列
3. **Commercial 链完全不使用 SQLite** — 符合 Governance Protocol 边界，但造成双轨
4. **2_COGNITION 规划的 DB 扩展** — Blueprint 存在，Runtime 未实现
