# AI_FACTORY_OS Database Reality Audit v1

> 只读审计报告 | 审计日期：2026-07-07  
> **审计方式：** 读取 `data/ai_factory.db` 结构与元信息；未修改数据库、未迁移、未导出全量数据

**对比基准：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md)

---

## 1. Audit Scope

| 项 | 内容 |
|----|------|
| **目标文件** | `data/ai_factory.db` |
| **审计类型** | 只读结构审计 + Blueprint Gap Analysis |
| **禁止操作** | 修改 Python、修改 DB、建表、删数据、迁移 |
| **样本策略** | 每表最多 2 行样本 |
| **代码引用** | 只读搜索 `DB_PATH` / `database.py` / `sqlite` |

---

## 2. Current Database Reality

### 基本信息

| 属性 | 值 |
|------|-----|
| **数据库类型** | SQLite |
| **文件路径** | `data/ai_factory.db` |
| **文件大小** | 81,920 bytes（~80 KB） |
| **创建时间** | 2026-07-04 11:14:11 |
| **最后修改** | 2026-07-07 15:51:41 |
| **SQLite 版本** | 3.45.1（Python `sqlite3` 模块） |
| **是否可正常打开** | ✅ 是 |

### 结构概览

| 类型 | 数量 |
|------|------|
| **用户表** | 7 |
| **系统表** | 1（`sqlite_sequence`） |
| **索引** | 2（均为 UNIQUE 自动索引） |
| **视图** | 0 |

### 数据量汇总

| 表名 | 行数 |
|------|------|
| `platforms` | 1 |
| `keywords` | 6 |
| `products` | 61 |
| `collection_log` | 29 |
| `scores` | 519 |
| `trends` | 0 |
| `audit_log` | 1 |
| **合计（用户数据）** | **617** |

---

## 3. Existing Tables

### Table: `platforms`

**用途推测：** 采集平台注册表（类似 Blueprint `market_sources` 的简化版）

| Column | Type | Nullable | Default | PK |
|--------|------|----------|---------|-----|
| `id` | INTEGER | Yes | — | ✅ |
| `name` | TEXT | NOT NULL | — | |
| `base_url` | TEXT | Yes | — | |
| `status` | TEXT | Yes | `'active'` | |

**Primary Key:** `id`  
**Index:** `sqlite_autoindex_platforms_1`（UNIQUE on `name`）  
**Row count:** 1  
**Sample:** `{ id: 1, name: "xianyu", base_url: "https://goofish.com", status: "active" }`

**代码关系：** `ensure_schema()` 仅 `INSERT OR IGNORE (1, 'xianyu')`；`base_url` / `status` 列存在于 DB 但不在当前 `database.py` 的 `CREATE TABLE` 脚本中（**Schema 漂移**）。

---

### Table: `keywords`

**用途推测：** 采集关键词追踪（部分对应 Blueprint `market_keywords`）

| Column | Type | Nullable | Default | PK |
|--------|------|----------|---------|-----|
| `id` | INTEGER | Yes | — | ✅ |
| `keyword` | TEXT | NOT NULL UNIQUE | — | |
| `category` | TEXT | Yes | — | |
| `first_seen_date` | TEXT | Yes | — | |
| `last_seen_date` | TEXT | Yes | — | |
| `is_sensitive` | INTEGER | Yes | 0 | |
| `is_low_efficiency` | INTEGER | Yes | 0 | |
| `last_search_date` | TEXT | Yes | — | |

**Primary Key:** `id`  
**Index:** `sqlite_autoindex_keywords_1`（UNIQUE on `keyword`）  
**Row count:** 6  
**Sample keywords:** 含测试类关键词（如 `测试关键词_db`）及业务关键词（如 `虚拟资料`）

---

### Table: `products`

**用途推测：** 闲鱼等平台采集的**市场已有商品**原始记录（部分对应 Blueprint `market_products`）

| Column | Type | Nullable | Default | PK |
|--------|------|----------|---------|-----|
| `id` | INTEGER | Yes | — | ✅ |
| `platform_id` | INTEGER | Yes | — | FK → `platforms.id` |
| `keyword` | TEXT | Yes | — | |
| `title` | TEXT | Yes | — | |
| `price` | REAL | Yes | — | |
| `want_count` | INTEGER | Yes | — | |
| `view_count` | INTEGER | Yes | — | |
| `comment_count` | INTEGER | Yes | 0 | |
| `share_count` | INTEGER | Yes | 0 | |
| `seller` | TEXT | Yes | — | |
| `tags` | TEXT | Yes | — | |
| `publish_time` | TEXT | Yes | — | |
| `source_url` | TEXT | Yes | — | |
| `raw_json` | TEXT | Yes | — | |
| `collect_date` | TEXT | NOT NULL | — | |

**Primary Key:** `id`  
**Index:** 无显式索引  
**Row count:** 61  
**Sample:** 含 `raw_json: {"source": "unit_test"}` 的测试数据与真实采集数据混合

---

### Table: `collection_log`

**用途推测：** 数据采集任务日志

| Column | Type | Nullable | Default | PK |
|--------|------|----------|---------|-----|
| `id` | INTEGER | Yes | — | ✅ |
| `task_date` | TEXT | NOT NULL | — | |
| `platform_id` | INTEGER | Yes | — | FK → `platforms.id` |
| `keyword` | TEXT | Yes | — | |
| `total_items` | INTEGER | Yes | 0 | |
| `valid_items` | INTEGER | Yes | 0 | |
| `status` | TEXT | Yes | `'running'` | |
| `started_at` | TEXT | Yes | — | |
| `finished_at` | TEXT | Yes | — | |

**Primary Key:** `id`  
**Row count:** 29  

---

### Table: `scores`

**用途推测：** **商品维度评分**（`3_DECISION` ScoringAgent 写入）— **不是** Blueprint 的 Market Opportunity Score

| Column | Type | Nullable | Default | PK |
|--------|------|----------|---------|-----|
| `id` | INTEGER | Yes | — | ✅ |
| `product_id` | INTEGER | Yes | — | FK → `products.id` |
| `hot_score` | REAL | Yes | — | |
| `trend_score` | REAL | Yes | — | |
| `comp_score` | REAL | Yes | — | |
| `profit_score` | REAL | Yes | — | |
| `difficulty_score` | REAL | Yes | — | |
| `total_score` | REAL | Yes | — | |
| `scored_date` | TEXT | NOT NULL | — | |

**Primary Key:** `id`  
**Row count:** 519（高频写入，多次运行累积）  
**说明:** 每条记录绑定 `product_id`，为**已采集商品的质量/热度评分**，与 `opportunity_scores`（关键词级市场机会评分）语义不同。

---

### Table: `trends`

**用途推测：** 关键词趋势快照（设计预留，**当前未使用**）

| Column | Type | Nullable | Default | PK |
|--------|------|----------|---------|-----|
| `id` | INTEGER | Yes | — | ✅ |
| `snapshot_date` | TEXT | NOT NULL | — | |
| `platform_id` | INTEGER | Yes | — | FK → `platforms.id` |
| `keyword` | TEXT | Yes | — | |
| `total_products` | INTEGER | Yes | — | |
| `avg_price` | REAL | Yes | — | |
| `avg_want` | REAL | Yes | — | |
| `growth_rate` | REAL | Yes | — | |

**Primary Key:** `id`  
**Row count:** 0  
**代码关系:** 当前代码库**无引用**，不在 `database.py` 的 `ensure_schema()` 中

---

### Table: `audit_log`

**用途推测：** 历史审计/关键词审核日志（**当前未使用**）

| Column | Type | Nullable | Default | PK |
|--------|------|----------|---------|-----|
| `id` | INTEGER | Yes | — | ✅ |
| `audit_type` | TEXT | NOT NULL | — | |
| `target` | TEXT | Yes | — | |
| `passed` | INTEGER | Yes | 0 | |
| `score` | INTEGER | Yes | 0 | |
| `issues` | TEXT | Yes | — | |
| `suggestions` | TEXT | Yes | — | |
| `created_at` | TEXT | NOT NULL | — | |

**Primary Key:** `id`  
**Row count:** 1（2026-07-04 历史记录）  
**代码关系:** 当前代码库**无引用**，不在 `ensure_schema()` 中 — **疑似历史遗留表**

---

### Schema 漂移说明

`1_DATA/database.py` 中 `ensure_schema()` 定义的 CREATE TABLE 与**实际 DB 结构存在差异**：

| 差异 | 说明 |
|------|------|
| `platforms` | DB 含 `base_url`、`status`；代码脚本仅 `id, name` |
| `audit_log` / `trends` | 存在于 DB，代码未创建、未引用 |
| FOREIGN KEY | DB 中 `products`、`scores` 等有 FK；代码脚本无 FK 声明 |
| `get_top_scored_products()` | 代码已定义，**全项目无调用** |

---

## 4. Runtime Usage

### Database Runtime Dependency Map

```
8_CONFIG/config.py
    └── DB_PATH = data/ai_factory.db
            │
            ├── 0_START/controller.py
            │       └── database.ensure_schema()  [boot 时初始化]
            │
            ├── 1_DATA/database.py  [唯一 DB 访问层]
            │       ├── ensure_schema()
            │       ├── upsert_keyword()
            │       ├── insert_product()
            │       ├── start/finish_collection_log()
            │       ├── get_products_by_keyword()
            │       ├── save_score()
            │       └── get_top_scored_products()  [未使用]
            │
            ├── 1_DATA/collector.py
            │       └── XianyuCollector → database.*  [采集写入]
            │
            └── 3_DECISION/scoring_agent.py
                    └── get_products_by_keyword() + save_score()
```

| 模块 | 使用 DB | 方式 |
|------|---------|------|
| **`1_DATA`** | ✅ Active | 读写：`platforms`, `keywords`, `products`, `collection_log` |
| **`3_DECISION`** | ✅ Active | 读写：`products`（读）, `scores`（写） |
| **`0_START`** | ✅ Active | boot 时 `ensure_schema()` |
| **`11_CONTENT_FACTORY`** | ❌ 无 | 使用 `storage/product_memory.json` + `artifacts/` |
| **`7_MEMORY`** | ❌ 无 | 使用 `7_MEMORY/*.json(l)` |
| **`2_COGNITION`** | ❌ 无 | 目录为空，未建设 |

### 当前数据库用途判断

**分类：E — 混合数据库**

| 子类型 | 证据 |
|--------|------|
| **B — 数据采集数据库** | `products`（61 行）、`keywords`、`collection_log`、`platforms`；`collector.py` 从闲鱼 Excel 采集 |
| **C — 评分数据库** | `scores`（519 行）；`ScoringAgent` 对每个 product 打分并持久化 |
| **D — 测试数据库（部分）** | 含 `测试关键词_db`、`unit_test` raw_json、早期 audit 记录 |
| **运行数据库** | CLI/API boot 每次调用 `ensure_schema()`，为活跃运行依赖 |

**理由：** 同一库同时承担采集存储、商品评分持久化，并含测试/历史遗留表；**尚未承担** Content Factory 产物、商业反馈、Market Opportunity 评分职责。

---

## 5. Blueprint Gap Analysis

### Existing Schema VS Target Schema

| Blueprint 表 | 现状 | 状态 | 现有近似表 | 说明 |
|--------------|------|------|------------|------|
| `market_sources` | 不存在 | **Missing** | `platforms`（Partial） | `platforms` 仅 1 行 xianyu，缺 `api_or_method`、`created_at` 等 |
| `market_keywords` | 不存在 | **Partial** | `keywords` | 有关键词追踪，缺 `search_volume`、`trend_score`、`growth_rate`、`source_id` |
| `market_products` | 不存在 | **Partial** | `products` | 有市场商品采集，字段集不同（want/view vs rating/review_count） |
| `market_demands` | 不存在 | **Missing** | — | 无需求信号表 |
| `opportunity_scores` | 不存在 | **Missing** | `scores`（⚠️ 非等价） | `scores` 是 product 级评分，非 keyword 级机会评分 |
| `generated_products` | 不存在 | **Missing** | — | Content Factory 产物未入库 |
| `product_feedback` | 不存在 | **Missing** | — | 销售反馈未入库 |

### 额外存在、Blueprint 未定义表

| 表 | 状态 | 建议 |
|----|------|------|
| `collection_log` | **Existing** | 保留，可映射为采集审计资产 |
| `trends` | **Existing（空）** | Review — 可演进为 Trend Intelligence 或 Archive |
| `audit_log` | **Existing（遗留）** | Review — Deprecated，迁移规划时处理 |

### 评分体系差异（关键）

| 体系 | 现有 | Blueprint 目标 |
|------|------|----------------|
| **Market Opportunity Score** | ❌ 不存在 | `opportunity_scores` ← `2_COGNITION` |
| **Product Quality / Hot Score** | ✅ `scores` 表 | `generated_products.quality_score` ← QualityAgent |

**禁止混合：** 迁移时不应将 `scores` 直接重命名为 `opportunity_scores` 而不改语义。

---

## 6. Migration Risk Assessment

| 风险 | 等级 | 说明 |
|------|------|------|
| **运行链中断** | 🔴 高 | `collector.py` / `ScoringAgent` 依赖 `products`、`scores`；盲目改表名/删列会破坏 CLI |
| **Schema 漂移** | 🟠 中 | DB 实际结构 ≠ `ensure_schema()` 脚本；迁移须以 **DB Reality** 为准同步代码 |
| **scores 语义混淆** | 🟠 中 | 519 行 `scores` 为 product 评分；与 `opportunity_scores` 并存需命名与文档隔离 |
| **遗留表** | 🟡 低 | `audit_log`、`trends` 无代码引用；迁移时可 Archive 或复用 |
| **测试数据污染** | 🟡 低 | 测试 keyword/product 与生产数据共存；迁移前宜标记 |
| **Content Factory 未接入** | 🟢 规划 | 新增 `generated_products` / `product_feedback` 为 additive，风险较低 |
| **7_MEMORY 隔离** | 🟢 低 | Memory 不读 DB，迁移不影响 OS 记忆链 |

---

## 7. Recommendation

### 短期（Migration Planning 阶段）

1. **以本 Audit 为基准**，编写 `Database Migration Plan` 文档（Phase 3），不立即执行 SQL
2. **同步 `ensure_schema()` 与 DB Reality** — 作为独立代码任务，须用户审批
3. **保留现有表** `products`、`keywords`、`scores`、`collection_log` 继续服务当前运行链
4. **新增 Blueprint 表** 采用 `CREATE TABLE IF NOT EXISTS` additive 策略，不删除现有表

### 中期（Phase 4–5）

1. **`platforms` → `market_sources`** — 扩展列或视图映射，而非暴力重命名
2. **`keywords` → `market_keywords`** — 扩展 trend 字段；历史数据回填策略单独设计
3. **新建 `opportunity_scores`** — 与 `scores` 并存，明确注释与文档
4. **新建 `generated_products` / `product_feedback`** — 对接 `11_CONTENT_FACTORY` pipeline
5. **`audit_log` / 空 `trends`** — Review 后 Archive 或纳入 Trend Intelligence 设计

### 禁止事项（直至 Migration Plan 审批）

- ❌ 删除 `scores` / `products` 数据
- ❌ 重命名现有表而不更新 `database.py` 与 Agent
- ❌ 将 product score 写入 opportunity score 字段

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Schema Blueprint | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` |
| Cognition Blueprint | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| 资产扫描 | `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md` |
| 模块注册 | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
