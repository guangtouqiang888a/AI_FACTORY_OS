# AI_FACTORY_OS Database Migration Plan v1

> 架构设计文档 | 最后更新：2026-07-07  
> **状态：Migration Plan Completed — 无 SQL 执行，无表创建，无数据修改**

**依据文档：**

- [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md](../../07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md)
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md)

---

## 1. Migration Philosophy

### 策略名称

**Additive Evolution Strategy**（_additive 演化策略_）

### 定义

AI_FACTORY_OS 数据库采用：

```
Existing Capability
        +
Future Intelligence Layer
```

### 原则

- **禁止破坏已有数据资产** — 617 行现有用户数据（products、scores、keywords 等）必须保留
- **禁止暴力替换** — 不重命名运行中表、不删除 Legacy Active 表
- **新增优于改写** — Blueprint 目标表以 `CREATE TABLE IF NOT EXISTS` 增量添加
- **语义隔离** — 两套评分体系并存，文档与字段命名明确区分
- **先设计后执行** — 本 Plan 仅为路线图；Implementation 须单独审批

### 演化公式

```
Legacy Active Capability（当前 SQLite）
        +
Extended Intelligence Schema（Blueprint 新表）
        =
Market Intelligence Database（目标态）
```

---

## 2. Existing Database Reality

### 当前引擎

**SQLite 3.45.1** — 文件 `data/ai_factory.db`（~80 KB）

### 现有表（Legacy Active Capability）

| 表 | 行数 | 分类 |
|----|------|------|
| `platforms` | 1 | 采集平台 |
| `keywords` | 6 | 关键词追踪 |
| `products` | 61 | 市场商品采集 |
| `collection_log` | 29 | 采集任务历史 |
| `scores` | 519 | 商品/市场项评分 |
| `trends` | 0 | 趋势快照（空，预留） |
| `audit_log` | 1 | 历史审计（遗留） |

### 说明

这些表属于 **Legacy Active Capability**，**不是废弃资产**。

- `1_DATA/collector.py` 与 `3_DECISION/scoring_agent.py` **正在使用** `products`、`keywords`、`scores`、`collection_log`
- `0_START/controller.py` boot 时调用 `database.ensure_schema()`
- 删除或重命名任一活跃表将**中断当前 CLI/API 运行链**

---

## 3. Target Database Architecture

### 五层目标架构

| 层级 | 职责 | 主要模块 | 代表表（目标） |
|------|------|----------|----------------|
| **Raw Data Layer** | 原始采集与事实存储 | `1_DATA` | `market_sources`, `market_keywords`, `market_products`, `market_demands` + Legacy: `products`, `keywords`, `platforms` |
| **Analysis Layer** | AI 市场分析中间结果 | `2_COGNITION` | 分析字段 / 扩展列 / 可选中间表 |
| **Decision Layer** | 机会评分与生产裁决输入 | `3_DECISION` | `opportunity_scores` + Legacy: `scores` |
| **Production Layer** | 已生成数字产品记录 | `11_CONTENT_FACTORY` | `generated_products` |
| **Feedback Layer** | 商业结果与用户反馈 | `11_CONTENT_FACTORY` + Feedback 闭环 | `product_feedback` |

### 模块映射

```
1_DATA          → Raw Data Layer（写入）
2_COGNITION     → Analysis Layer（读 Raw、写 Analysis / opportunity_scores）
3_DECISION      → Decision Layer（读 opportunity_scores、Legacy scores）
11_CONTENT_FACTORY → Production + Feedback Layer（写 generated_products、product_feedback）
```

---

## 4. Table Evolution Mapping

### `platforms` → `market_sources`

| 项 | 说明 |
|----|------|
| **策略** | **保留 `platforms`**；新建 `market_sources` 或扩展映射 |
| **演化** | 未来扩展 `api_or_method`、`created_at` 等 Blueprint 字段 |
| **禁止** | 直接 `DROP` / `RENAME platforms` |
| **迁移** | 可选：双写期将 `platforms` 行同步至 `market_sources`；或 `market_sources` 作为 superset 表 |

---

### `keywords` → `market_keywords`

| 项 | 说明 |
|----|------|
| **策略** | **保留 `keywords` 及全部历史** |
| **演化** | 新建 `market_keywords`，含 `search_volume`、`trend_score`、`growth_rate`、`source_id` |
| **历史** | `keywords` 6 行关键词记录为 Intelligence Asset，须可追溯到新表 |
| **禁止** | 覆盖或清空 `keywords` |

---

### `products` → `market_products`

| 项 | 说明 |
|----|------|
| **策略** | **保留 `products`（61 行）** |
| **演化** | 新建 `market_products` 对齐 Blueprint 字段（`rating`, `review_count` 等） |
| **说明** | 当前 `products` 为闲鱼采集的市场商品数据资产 |
| **可选** | 视图或 ETL 将 `products` 映射至 `market_products` 统一查询 |

---

### `scores` → **保留** + 新增 `opportunity_scores`

| 项 | 说明 |
|----|------|
| **`scores`** | **保留** — 519 行 Product / Market Item Scoring |
| **`opportunity_scores`** | **新增** — Market Opportunity Score（`2_COGNITION` 输出） |
| **禁止** | 合并、重命名、语义混用两个评分系统 |

---

### `collection_log` → **保留**

| 项 | 说明 |
|----|------|
| **角色** | **Data Collection History**（采集任务审计链） |
| **策略** | 保留并继续由 `1_DATA` 写入 |
| **未来** | 可与 `market_sources` 关联 `platform_id` |

---

### 新增表

| 表 | 层级 | 写入方 |
|----|------|--------|
| `market_demands` | Raw Data / Analysis | `1_DATA` / `2_COGNITION` |
| `generated_products` | Production | `11_CONTENT_FACTORY` |
| `product_feedback` | Feedback | `11_CONTENT_FACTORY` / 人工录入 |

### 遗留表处理

| 表 | 策略 |
|----|------|
| `trends` | Review — 可演进为 Trend Intelligence 写入目标，或 Archive |
| `audit_log` | Review — Deprecated 遗留；保留 1 行历史，不主动写入 |

---

## 5. Score System Migration

### 当前：`scores`

| 属性 | 值 |
|------|-----|
| **用途** | Product / Market Item Scoring |
| **粒度** | 每条 `product_id` |
| **写入** | `3_DECISION/scoring_agent.py` → `database.save_score()` |
| **字段** | hot_score, trend_score, comp_score, profit_score, difficulty_score, total_score |
| **未来角色** | **产品表现分析** — 评估已采集市场商品相对竞争力 |

### 未来：`opportunity_scores`（新增）

| 属性 | 值 |
|------|-----|
| **用途** | 市场机会发现 — 是否值得进入 Content Factory 生产 |
| **粒度** | 每条 `keyword_id` / 产品机会 |
| **写入** | `2_COGNITION`（待建） |
| **字段** | demand_score, trend_score, competition_score, profit_score, difficulty_score, opportunity_score, recommendation |
| **消费** | `3_DECISION` |

### 关系图

```
scores（保留）
    ↓
产品表现分析（已采集商品竞争力）

opportunity_scores（新增）
    ↓
市场机会发现（是否生产什么）
```

### 禁止

- ❌ 合并两个评分系统
- ❌ 将 `scores.total_score` 直接当作 `opportunity_score`
- ❌ 删除 `scores` 表或 519 行历史

---

## 6. Migration Order

| Phase | 名称 | 内容 | 状态 |
|-------|------|------|------|
| **Phase 1** | Schema documentation | Blueprint + Reality Audit + Migration Plan | **Completed** |
| **Phase 2** | Database version management | `schema_version`、`migration_history` 表或文件 | Future |
| **Phase 3** | Create new tables | 仅 ADDITIVE `CREATE TABLE IF NOT EXISTS` | Future |
| **Phase 4** | Update 1_DATA writers | 双写或扩展 collector 写入新 Raw 表 | Future |
| **Phase 5** | Connect 2_COGNITION | 读 Raw、写 `opportunity_scores` | Future |
| **Phase 6** | Connect Content Factory feedback | 写 `generated_products`、`product_feedback` | Future |

**Phase 3–6 每一阶段均须：** backup → migration script → validation → rollback 预案

---

## 7. Rollback Strategy

任何数据库变更必须满足：

| 步骤 | 要求 |
|------|------|
| 1 | **backup database** — 复制 `data/ai_factory.db` 至带时间戳备份路径 |
| 2 | **version migration** — 每条 migration 有唯一 version id |
| 3 | **rollback script** — 对应 down migration 或 restore from backup |

### 禁止

- ❌ 直接修改生产数据库而无备份
- ❌ 不可逆 DDL（DROP COLUMN、DROP TABLE）在未 Archive 数据前执行
- ❌ 在生产环境手动 SQL 无文档记录

### 建议备份路径（未来）

```
data/backups/ai_factory_YYYYMMDD_HHMMSS.db
```

---

## 8. Data Preservation Rules

### 必须保留的历史数据

| 表 | 行数 | 原因 |
|----|------|------|
| `products` | 61 | 市场采集样本 — Intelligence Asset |
| `scores` | 519 | 评分历史 — 可分析评分分布与决策链 |
| `keywords` | 6 | 关键词首次/末次出现记录 |
| `collection_log` | 29 | 采集任务完整审计链 |
| `platforms` | 1 | 平台配置基准 |
| `audit_log` | 1 | 历史审计追溯 |

### 原则

历史数据是 **AI Factory Intelligence Asset**。

- 测试行（如 `测试关键词_db`）在迁移时可**标记**为 experimental，但**默认保留**
- Archive 须走 [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md) 流程，本 Plan 阶段不执行

---

## 9. Future Database Versioning

### 设计目标

| 组件 | 说明 |
|------|------|
| **`schema_version`** | 单表单行，当前 schema 版本号（如 `v1.0.0-legacy`, `v2.0.0-intelligence`） |
| **`migration_history`** | 记录每次 migration：version、applied_at、description、checksum |
| **backup strategy** | 每次 migration 前自动 backup；保留最近 N 份 |

### 版本命名建议

```
v1.x — Legacy Active（platforms/products/scores 为主）
v2.x — Intelligence Extension（market_* + opportunity_scores 新增）
v2.x — Content Factory Integration（generated_products + product_feedback）
```

### 与代码同步

`1_DATA/database.py` 的 `ensure_schema()` 须在 Phase 2 后与 `schema_version` 对齐，消除 Reality Audit 发现的 Schema 漂移。

---

## 10. Migration Risks

| # | 风险 | 等级 | 缓解措施 |
|---|------|------|----------|
| 1 | **scores 语义混淆** | 🔴 高 | 文档 + 表名隔离；禁止合并；Code review 检查字段用途 |
| 2 | **历史数据兼容** | 🟠 中 | Additive only；双写过渡期；映射表文档化 |
| 3 | **collector 改造影响** | 🟠 中 | Phase 4 独立 PR；保留旧写入路径直至验证 |
| 4 | **Cognition 接口设计** | 🟠 中 | 先完成 Database Integration Design（1_DATA ↔ 2_COGNITION 协议） |
| 5 | **Schema 漂移** | 🟡 中 | Phase 2 同步 `ensure_schema()` 与 DB Reality |
| 6 | **遗留表 trends/audit_log** | 🟡 低 | Review 后决定复用或 Archive，不阻塞 Phase 3 |

---

## 11. Recommended Next Step

### 下一阶段：**Database Integration Design**（不是立即迁移）

在编写任何 migration SQL 或修改 Python 之前，先设计：

```
1_DATA
    ↔  Database（Raw Layer 读写协议）
        ↔  2_COGNITION（Opportunity Object 输入/输出）
            ↔  3_DECISION（Decision Input 消费协议）
```

### 建议交付物（docs 任务）

1. **`AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md`** — 模块间 JSON 对象与表读写边界
2. **`2_COGNITION` 与 `opportunity_scores` 写入规范** — 对齐 Cognition Blueprint §8
3. **`11_CONTENT_FACTORY` 与 `generated_products` 关联规范** — artifact_path 映射

### 明确不做（直至 Integration Design 审批）

- ❌ 执行 CREATE TABLE
- ❌ 修改 `database.py`
- ❌ 修改 `collector.py` / `scoring_agent.py`

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Schema Blueprint | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` |
| Reality Audit | `docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md` |
| Cognition Blueprint | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| 模块注册表 | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
| 工作准则 | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` |
