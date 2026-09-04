# AI_FACTORY_OS Asset Lifecycle Policy v1

> 项目资产治理规范 | 最后更新：2026-07-07  
> **状态：Policy Completed — 仅文档，不参与运行计算**

**相关文档：**

- [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md) — 审计规范
- [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md) — 扫描报告
- [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md) — 登记模板
- [docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md](../../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) — 模块注册
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md](../database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md) — 数据库保护

---

## 1. Purpose

### 定义

**AI_FACTORY_OS 是长期演化系统。**

系统运行过程中产生的：

- **数据** — 数据库、采集样本、Memory、日志
- **代码** — 各层模块 Python、配置
- **产品文件** — Content Factory artifacts、final_product.zip
- **模型输出** — LLM 生成内容、评分结果、发布包装

**均属于系统资产**，不是一次性消耗品。

### 目标

| 目标 | 说明 |
|------|------|
| **保护资产价值** | 历史数据与产物具备长期 Intelligence 价值 |
| **避免误删除** | 不确定用途的文件默认保留 |
| **避免 AI 误判** | 未来 AI 恢复项目时不将 Temporary/Experimental 当作 Active |

### 治理原则

- 资产分类先于清理
- 审计先于删除
- 归档先于销毁
- 文档先于假设

---

## 2. Asset Classification

### 资产等级（A / B / C / D）

与 [ASSET_AUDIT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md) 生命周期状态对齐，按**商业与运行影响**分级：

---

### A. Active Asset（活跃资产）

**定义：** 正在运行或商业使用的资产。

| 示例 | 路径 |
|------|------|
| 商业数据库 | `data/ai_factory.db` |
| 数字商品生产层 | `11_CONTENT_FACTORY/`（代码 + artifacts） |
| 核心 OS | `0_START/` |
| 决策与采集 | `1_DATA/`、`3_DECISION/` |
| 运行 Memory | `7_MEMORY/event_log.jsonl` 等 |
| 项目认知文档 | `docs/` |

**规则：** 禁止删除；变更须审计 + 审批。

---

### B. Experimental Asset（实验资产）

**定义：** 实验、验证、试探性产物。

| 示例 | 路径 |
|------|------|
| 测试产品批次 | `artifacts/products/75f2feac9b04/`（无 final_product.zip） |
| 实验数据 | `data/raw/` 样本、`keywords` 中测试关键词 |
| 验证结果 | 早期 `9_PRODUCT/` 冻结代码 |
| 模型试验输出 | 未 release 的中间 artifact |

**规则：** 保留并标记来源；清理前须 Archive + 确认。

---

### C. Archive Asset（归档资产）

**定义：** 已完成历史使命、保留追溯价值的资产。

| 示例 | 路径 |
|------|------|
| 旧版本产品 | 已验证完毕的 product_id 批次（未来 `archive/products/`） |
| 旧日志 | 轮转后的 `logs/deploy/*` |
| 旧数据库备份 | `data/backups/ai_factory_*.db`（未来） |
| Deprecated 文档版本 | 被新版本替代的设计文档（保留只读） |

**规则：** 移入 archive 区，不参与运行；禁止直接删除。

---

### D. Temporary Asset（临时资产）

**定义：** 可再生、无长期保存必要的运行时产物。

| 示例 | 路径 |
|------|------|
| Python 缓存 | `__pycache__/`、`*.pyc` |
| 模拟发布输出 | `output/*.json` |
| 运行日志 | `logs/execution_hash.log`（可轮转） |
| 占位符 | `cover_placeholder.txt` |

**规则：** 可清理，但须经 Audit 确认无引用；`.gitignore` 已排除者优先视为 Temporary。

---

### 分类对照表

| 等级 | Audit 状态 | 删除优先级 |
|------|--------------|------------|
| A — Active | Active | 禁止删除 |
| B — Experimental | Experimental | Archive 后可选删除 |
| C — Archive | Archive / Deprecated | 长期保留；删除须 Approval |
| D — Temporary | Temporary | Review 后可清理 |

---

## 3. Asset Ownership Model

### 模块资产归属

| 模块 | 负责资产 | 典型路径 |
|------|----------|----------|
| **`1_DATA`** | Raw data、collection data | `data/ai_factory.db`（Legacy 表）、`data/raw/`、`collection_log` |
| **`2_COGNITION`** | Analysis result、opportunity intelligence | `opportunity_scores`（未来）、Cognition 分析报告 |
| **`3_DECISION`** | Decision records | `scores`、Decision 输出、`output/*.json`（模拟） |
| **`11_CONTENT_FACTORY`** | Products、artifacts | `artifacts/products/{product_id}/`、`storage/product_memory.json` |
| **`10_DEPLOY`** | Deployment logs | `logs/deploy/`（trace、metrics、requests） |
| **`7_MEMORY`** | System memory | `7_MEMORY/*.json(l)`、`PROJECT_CORE_MEMORY.md` |
| **Database** | Business data asset | `data/ai_factory.db` — 跨层，经 `1_DATA/database.py` 访问 |

### 跨层资产

| 资产 | 归属说明 |
|------|----------|
| **`docs/`** | Project Context Layer — 全员只读参考，AI 恢复优先 |
| **`8_CONFIG/`** | 全局配置 — Active |
| **`0_START/`** | Core OS — Active，冻结 |

**原则：** 模块只写自有归属资产；跨模块读写的须经 [Database Integration Design](../database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md)。

---

## 4. Lifecycle State Machine

### 状态流转

```
Create
    ↓
Active
    ↓
Experimental（可选分支 — 实验期）
    ↓
Archive
    ↓
Deprecated
```

### 规则

| 规则 | 说明 |
|------|------|
| **禁止 Deprecated 直接删除** | Deprecated 仍具历史参考价值 |
| **删除唯一路径** | Audit → Archive → Approval → Delete |

### 删除流程（强制）

```
Audit（ASSET_AUDIT + 登记模板）
    ↓
Archive（移入 archive/ 或标记 Archive）
    ↓
Approval（人工或用户明确指令）
    ↓
Delete（最后一步，可记录于 CURSOR_EXECUTION_HISTORY）
```

---

## 5. Database Protection Policy

### 定位

数据库属于：**Protected Business Asset**

物理路径：`data/ai_factory.db`

### 任何数据库操作必须

```
Backup
    ↓
Migration Plan（引用 IMPLEMENTATION_PLAN / MIGRATION_PLAN）
    ↓
Validation（Database Upgrade Checklist）
    ↓
Rollback（备份 restore 或 down migration）
```

### 禁止

| 禁止项 | 说明 |
|--------|------|
| 直接删除表 | Legacy 表为历史能力资产 |
| 覆盖历史数据 | 617+ 行用户数据须保留 |
| 改变字段语义 | 如将 `scores` 当作 `opportunity_scores` |

**权威规范：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md](../database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md)

---

## 6. Artifact Management Policy

### 范围

`11_CONTENT_FACTORY/artifacts/products/{product_id}/`

### 每个 artifact 必须具有（设计目标）

| 字段 | 来源 | 说明 |
|------|------|------|
| **`product_id`** | 目录名 / `metadata.json` | 唯一标识 |
| **`created_time`** | `metadata.json` | 创建时间 |
| **`status`** | pipeline / release_gate | draft / released / archived |
| **`source`** | opportunity / manual / experiment | 生产来源 |
| **`quality_score`** | QualityAgent | Product Quality Score（非 Opportunity Score） |

### 当前对照（Scan Report v1）

| product_id | status 推测 | 说明 |
|------------|-------------|------|
| `e601c17c6977` | Active / Released | 含 `final_product.zip` |
| `75f2feac9b04` | Experimental | 无 final_product.zip |

### 规则

- artifact 文件系统资产与 DB `generated_products`（未来）通过 `artifact_path` 关联
- 禁止跨模块直接读 `artifacts/` 内部文件做决策 — 经 Database Contract
- 清理 artifact 批次须走 §8 Cleanup Policy

---

## 7. AI Recovery Rules

### 未来 AI 接管项目时

**禁止：**

- 通过目录名称猜测用途
- 将 `output/`、`logs/` 误判为生产资产
- 将空 Reserved 目录当作已建设模块
- 未经审计建议删除 `data/ai_factory.db` 或 Legacy 表

### 必须优先读取（顺序）

| 优先级 | 文档 |
|--------|------|
| 1 | [docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md](../../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) |
| 2 | [docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md](../../01_CURRENT_STATE/reference/PROJECT_STATUS.md) |
| 3 | [docs/01_CURRENT_STATE/reference/system_snapshot.md](../../01_CURRENT_STATE/reference/system_snapshot.md) |
| 4 | [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)（本文档） |
| 5 | [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md) |
| 6 | [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md) |

### 恢复后行动

- 区分 Existing / Missing / Target
- 资产操作前更新或引用 ASSET_AUDIT_TEMPLATE
- 重大变更写入 CURSOR_EXECUTION_HISTORY

---

## 8. Cleanup Policy

### 标准删除流程

```
发现疑似无用文件
    ↓
Asset Audit（ASSET_AUDIT + SCAN_REPORT 对照）
    ↓
标记状态（Active / Experimental / Temporary / Deprecated / Archive）
    ↓
Archive（默认 — 移入 archive/ 或保留原位标记）
    ↓
确认（用户 Approval）
    ↓
Delete（最后手段）
```

### 禁止

- ❌ 直接 `rm` / `delete` / 批量清理无审计
- ❌ AI 自动清理未经用户确认
- ❌ 清理 Active 或 Protected Business Asset

### 可优先 Review 的候选（来自 Scan Report，本 Policy 不执行删除）

- `7_MEMORY/core_state.json` — Deprecated / Review
- `output/*.json` — Temporary，Archive 旧批次
- 根目录空 `README.md` — Deprecated / Review
- `__pycache__/` — Temporary，安全但非本 Policy 自动执行

---

## 9. Asset Governance Stack

```
Asset Lifecycle Policy（本文档 — 总规范）
    +
Asset Audit（审计规范）
    +
Asset Scan Report（现状快照）
    +
Module Registry（模块归属）
    +
Database Protection（DB 专项）
    =
Project Asset Governance
```

---

## 相关文档

| 文档 | 路径 |
|------|------|
| 工作准则 | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` |
| 工程进度 | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` |
| 执行历史 | `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` |
