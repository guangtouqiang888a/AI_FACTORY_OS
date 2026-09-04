# AI_FACTORY_OS Database Extension Implementation Plan v1

> 实施执行规范 | 最后更新：2026-07-07  
> **状态：Implementation Plan Completed — 无代码修改，无数据库变更，无 migration 执行**

**本文件性质：** Database Intelligence Layer 的**未来代码/SQL 实施前的执行规范**，非立即执行指令。

**最高优先级上下文（须先读）：**

| 文档 | 路径 |
|------|------|
| Schema Blueprint | [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md) |
| Reality Audit | [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md](../../07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md) |
| Migration Plan | [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md](AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md) |
| Integration Design | [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md) |
| Cognition Blueprint | [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md) |

---

## 1. Implementation Objective

### Database Extension 的目标

**不是替换现有数据库。**

而是：

```
Legacy Capability
        +
Intelligence Layer
```

采用：**Additive Evolution Strategy**（见 Migration Plan v1）

### 演化目标

将 `data/ai_factory.db` 从当前 **Legacy SQLite Database** 扩展为 **Market Intelligence Database**，在保留全部历史能力的前提下，增量接入 Blueprint 定义的 Intelligence 表与模块连接。

### Legacy 历史能力资产（禁止删除）

| 表 | 行数（Audit v1） | 性质 |
|----|------------------|------|
| `platforms` | 1 | 历史能力资产 |
| `keywords` | 6 | 历史能力资产 |
| `products` | 61 | 历史能力资产 |
| `collection_log` | 29 | 历史能力资产 |
| `scores` | 519 | 历史能力资产 |

**明确禁止：** 删除、重命名、清空上述表及数据。

### 不在本阶段执行

- ❌ 修改 Python
- ❌ 修改 `data/ai_factory.db`
- ❌ CREATE TABLE / migration SQL 执行
- ❌ 自动进入代码实现

---

## 2. Implementation Boundary

### 未来允许修改范围（须分 Phase 审批）

| Phase | 允许修改路径 | 内容 |
|-------|--------------|------|
| **Phase 1** | `1_DATA/database.py` | Schema version、migration history、Intelligence 表 DDL（`CREATE IF NOT EXISTS`）、Legacy 兼容 |
| **Phase 1** | `1_DATA/collector.py` | Raw 双写（Legacy + Blueprint 表）、Market Data Object 标准化 |
| **Phase 2** | `2_COGNITION/` | 新增 Intelligence Engine（Trend / Demand / Competition / Opportunity） |
| **Phase 3** | `3_DECISION/` | 增加 `opportunity_scores` 消费能力；扩展 Decision 输入 |
| **Phase 4** | `11_CONTENT_FACTORY/` | `generated_products`、`product_feedback` 写入 |

**说明：** 物理数据库文件位于 `data/ai_factory.db`；访问层代码位于 `1_DATA/database.py`（非 `data/database.py`）。

### 明确禁止（未经单独审批不得修改）

| 模块 | 路径 | 原因 |
|------|------|------|
| **Core OS** | `0_START/` | 冻结 — Controller / Planner / ExecutionRuntime |
| **Memory** | `7_MEMORY/` | 物理隔离 — 不直接混写 DB |
| **Deploy** | `10_DEPLOY/` | 冻结 — HTTP 部署层 |
| **Frozen Commercial** | `9_PRODUCT/` | 未接入主链 |

### 实施原则

- 每 Phase 独立 Cursor 指令 + Entry 写入 `CURSOR_EXECUTION_HISTORY.md`
- 每 Phase 完成后运行 Validation Checklist（§8）
- 失败即 rollback，不叠加下一 Phase

---

## 3. Database Implementation Sequence

> 以下步骤为**未来实施顺序**。当前均为 Pending，本文档阶段不执行。

| Step | 名称 | 内容 | 验证 | 回滚 |
|------|------|------|------|------|
| **Step 0** | Database Backup | 复制 `data/ai_factory.db` → `data/backups/ai_factory_YYYYMMDD_HHMMSS.db` | 备份文件存在且可打开 | 从备份 restore |
| **Step 1** | Schema Version Management | 引入 `schema_version` 表或元数据行 | 版本号可读 | 恢复备份 |
| **Step 2** | Migration History | 引入 `migration_history` 记录每次变更 | 历史可追溯 | down script 或 restore |
| **Step 3** | 新增 Intelligence Tables | ADDITIVE 创建 7 张 Blueprint 表 | `sqlite_master` 含新表；Legacy 表未动 | DROP 新表（仅新表）或 restore |
| **Step 4** | 验证 Legacy Data | 对比 Step 0 行数：platforms/keywords/products/scores/collection_log | 行数 ≥ 审计基准 | restore |
| **Step 5** | 启用模块连接 | Phase 1–4 代码按 Integration Design 接入 | CLI `python 0_START/main.py` 通过；collector + scoring 链正常 | 代码 revert + DB restore |

### 步骤依赖

```
Step 0 → Step 1 → Step 2 → Step 3 → Step 4 → Step 5
```

**禁止跳过 Step 0–4 直接改业务模块代码。**

---

## 4. Future Table Implementation Plan

> 表结构字段详见 Schema Blueprint §3；本节定义实施维度的用途与模块归属。

### `market_sources`

| 项 | 说明 |
|----|------|
| **用途** | 记录数据来源（平台、API、采集方式） |
| **数据来源** | 外部平台配置、人工录入、`platforms` 映射同步 |
| **写入模块** | `1_DATA` |
| **读取模块** | `2_COGNITION` |
| **生命周期** | Active — 长期资产 |

---

### `market_keywords`

| 项 | 说明 |
|----|------|
| **用途** | 市场关键词趋势（search_volume、trend_score 等） |
| **数据来源** | 采集、趋势 API、`keywords` 双写扩展 |
| **写入模块** | `1_DATA` |
| **读取模块** | `2_COGNITION`, `3_DECISION` |
| **生命周期** | Active — 时间序列积累 |

---

### `market_products`

| 项 | 说明 |
|----|------|
| **用途** | 市场已有产品样本（竞争分析） |
| **数据来源** | 平台采集、`products` 映射 ETL |
| **写入模块** | `1_DATA` |
| **读取模块** | `2_COGNITION` |
| **生命周期** | Active |

---

### `market_demands`

| 项 | 说明 |
|----|------|
| **用途** | 用户需求信号（problem_description、demand_score） |
| **数据来源** | 采集、内容平台、反馈归纳 |
| **写入模块** | `1_DATA`, `2_COGNITION`（分析补写） |
| **读取模块** | `2_COGNITION` |
| **生命周期** | Active |

---

### `opportunity_scores`

| 项 | 说明 |
|----|------|
| **用途** | Market Opportunity Score — Cognition 输出 |
| **数据来源** | `2_COGNITION` Intelligence Engine 计算 |
| **写入模块** | `2_COGNITION` |
| **读取模块** | `3_DECISION` |
| **生命周期** | Active — Decision 输入核心 |

---

### `generated_products`

| 项 | 说明 |
|----|------|
| **用途** | Content Factory 已生成数字产品记录 |
| **数据来源** | `11_CONTENT_FACTORY` pipeline 完成产物 |
| **写入模块** | `11_CONTENT_FACTORY` |
| **读取模块** | `3_DECISION`（可选）, Feedback 分析 |
| **生命周期** | Active — `artifact_path` 指向文件系统 |

---

### `product_feedback`

| 项 | 说明 |
|----|------|
| **用途** | 销售/用户商业反馈 |
| **数据来源** | 人工录入、半自动导入、平台数据 |
| **写入模块** | `11_CONTENT_FACTORY` / 人工工具 |
| **读取模块** | `2_COGNITION`, `3_DECISION` |
| **生命周期** | Active — 闭环优化资产 |

---

## 5. Scoring System Protection

### 现有：`scores` — 必须保留

| 属性 | 值 |
|------|-----|
| **语义** | **Product Performance Score**（已采集市场商品的表现评分） |
| **粒度** | `product_id` |
| **写入** | `3_DECISION/scoring_agent.py` → `database.save_score()` |
| **未来角色** | 产品表现分析 — 与 Opportunity 评分并存 |

### 未来：`opportunity_scores` — 新增

| 属性 | 值 |
|------|-----|
| **语义** | **Market Opportunity Score**（是否值得生产） |
| **粒度** | `keyword_id` / 机会级 |
| **写入** | `2_COGNITION` |
| **消费** | `3_DECISION` |

### 禁止

| 禁止项 | 说明 |
|--------|------|
| **合并** | 不得将两表合并为一张 |
| **重命名** | 不得将 `scores` 重命名为 `opportunity_scores` |
| **覆盖** | 不得用 opportunity 字段覆盖 scores 历史 |

---

## 6. Module Integration Rules

| 模块 | 职责 | DB 关系 |
|------|------|---------|
| **`1_DATA`** | 事实采集 | 写 Raw Layer（Legacy + market_*） |
| **Database** | 资产保存 | `data/ai_factory.db` — 跨层 Contract |
| **`2_COGNITION`** | 分析 | 读 Raw、写 `opportunity_scores` |
| **`3_DECISION`** | 决策 | 读 `opportunity_scores` + Legacy `scores`；accept/reject/prioritize |
| **`11_CONTENT_FACTORY`** | 生产 | 写 `generated_products`；经 OS 调度，不自行选品 |
| **Feedback** | 闭环 | 写 `product_feedback`；回读改进 Cognition/Decision |

### 禁止

- ❌ 跨模块直接读取内部文件（`storage/`、`artifacts/`、`*_memory.json`）
- ❌ 模块独立 `sqlite3.connect` — 统一经 `1_DATA/database.py`
- ❌ `2_COGNITION` 直接生产数字文件
- ❌ `7_MEMORY` 直接写 DB

**权威契约：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md)

---

## 7. Cursor Implementation Rules

### 以后所有数据库相关 Cursor 指令必须遵循

```
先备份 → 先审计 → 先计划 → 后执行
```

| 顺序 | 要求 |
|------|------|
| 1 | **先 backup** — Step 0 完成并记录路径 |
| 2 | **先审计** — 对照 Reality Audit + 当前 `sqlite_master` |
| 3 | **先计划** — 引用 Implementation Plan / Migration Plan / Integration Design |
| 4 | **后执行** — 单 Step 单 PR；附 Validation Checklist |

### Cursor 指令必须明确

1. 当前已有文件与表
2. 本 Step 新增/修改文件
3. **禁止修改**文件（0_START / 7_MEMORY / 10_DEPLOY）
4. backup 路径与 rollback 方式
5. 验证命令（如 `python 0_START/main.py`）

### 禁止

- ❌ 一次性重构整个数据库
- ❌ 单条指令同时改 DB + 4 个模块
- ❌ 未经用户审批执行 migration SQL

---

## 8. Validation Checklist

### Database Upgrade Checklist

实施 Phase 完成后，逐项确认：

- [ ] **backup created** — `data/backups/` 下存在时间戳备份
- [ ] **migration version recorded** — `schema_version` / `migration_history` 已更新
- [ ] **old data preserved** — Legacy 表行数 ≥ Reality Audit 基准（617 用户数据行）
- [ ] **new tables verified** — 7 张 Intelligence 表存在于 `sqlite_master`
- [ ] **rollback tested** — 备份可 restore 或 down migration 已文档化
- [ ] **existing pipeline unaffected** — `collector` → `scoring_agent` → `controller.run()` 正常

### 文档同步 Checklist

- [ ] `CURSOR_EXECUTION_HISTORY.md` 新增 Entry
- [ ] `PROJECT_STATUS.md` 更新 Database Layer 状态
- [ ] 若表结构变更，更新 Reality Audit 或附 Diff 附录

---

## 9. Related Documents & Next Phase

| 文档 | 用途 |
|------|------|
| 本文档 | 实施执行规范 |
| Migration Plan | 表映射与 Additive 策略 |
| Integration Design | Interface 1–5 契约 |
| WORK_PRINCIPLES | 数据库实施生命周期原则 |

**下一阶段（Pending 用户指令）：** **Database Implementation Phase** — 从 Step 0 Backup 开始，仍须单独审批。

**禁止：** 自动进入代码实现。

---

## 10. Implementation Roadmap Summary

| 文档阶段 | 状态 |
|----------|------|
| Schema Blueprint | ✅ Completed |
| Reality Audit | ✅ Completed |
| Migration Plan | ✅ Completed |
| Integration Design | ✅ Completed |
| **Implementation Plan（本文档）** | ✅ Completed |
| Database Implementation（Step 0–5） | ⏳ Pending |
