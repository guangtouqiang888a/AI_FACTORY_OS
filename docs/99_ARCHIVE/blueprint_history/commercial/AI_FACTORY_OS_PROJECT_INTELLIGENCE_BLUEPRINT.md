# AI_FACTORY_OS Project Intelligence Layer Blueprint v1

> 架构设计文档 | Last updated: 2026-07-15（Entry **041-D** banner）

| Document Role | Architecture Reference |
|---------------|------------------------|
| Reality Status | Design Reference |
| Runtime Status | Requires Reality Validation |

**状态：Blueprint Completed — 认知层设计，不参与运行计算。**  
**禁止：** Design = Runtime · Blueprint = Production。

---

## 1. Purpose

### 定义

**Project Intelligence Layer（项目智能层）** 是 AI_FACTORY_OS 的**项目自描述与上下文恢复系统**。

它使未来 AI（或新协作者）在**不依赖聊天记忆、不猜测目录名称**的前提下，快速恢复项目**真实状态**。

### 核心目标

| 目标 | 说明 |
|------|------|
| **上下文恢复** | 读 docs 即可理解架构、进度、边界 |
| **状态真实** | Existing ≠ Target；规划 ≠ 已执行 |
| **变更可追溯** | 重大 Cursor 操作进入执行历史 |
| **资产可治理** | 审计、分类、生命周期、保护策略 |
| **实施可衔接** | 设计文档链指向 Database / Cognition 实施 |

### 不是什么

| 层 | 区别 |
|----|------|
| **`7_MEMORY/`** | 运行时机器记忆（event → pattern → strategy）— **参与执行** |
| **`2_COGNITION/`** | 市场智能运行时模块 — **未来代码** |
| **Data Intelligence Blueprint** | 商业数据智能战略 — 与 Project Intelligence **互补** |

**Project Intelligence Layer = `docs/` 认知体系**，物理隔离于运行数据。

---

## 2. Architecture Position

### 系统双层智能

```
┌─────────────────────────────────────────────────────────┐
│  Project Intelligence Layer（docs/ — 本文档体系）        │
│  模块注册 · 进度 · 快照 · 准则 · 资产 · 设计蓝图 · 历史   │
└─────────────────────────────────────────────────────────┘
                          ↕ 只读参考，不参与执行
┌─────────────────────────────────────────────────────────┐
│  AI Factory OS Runtime（0_START → … → 7_MEMORY）         │
│  Planner · PolicyEngine · ExecutionRuntime · Memory       │
└─────────────────────────────────────────────────────────┘
```

### 与运行架构关系

```
Project Intelligence（认知）
        │
        │ 描述、约束、恢复
        ▼
Runtime Architecture
    0_START → 1_DATA → 3_DECISION → 11_CONTENT_FACTORY → 10_DEPLOY
                        ↕
                    7_MEMORY（运行记忆，非 docs）
```

---

## 3. Layer Components

Project Intelligence Layer 由 **6 个子系统** 组成：

### 3.1 Context Recovery（上下文恢复）

| 文档 | 职责 |
|------|------|
| [MODULE_REGISTRY.md](../../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) | 模块状态、职责、架构流 |
| [PROJECT_STATUS.md](../../01_CURRENT_STATE/reference/PROJECT_STATUS.md) | 工程进度、Current Architecture Reality |
| [system_snapshot.md](../../01_CURRENT_STATE/reference/system_snapshot.md) | 架构快照、数据流、快速恢复清单 |

### 3.2 Governance（协作治理）

| 文档 | 职责 |
|------|------|
| [WORK_PRINCIPLES.md](../../99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md) | 升级原则、状态锁定、接口契约 |
| [BUSINESS_PLAN.md](../../99_ARCHIVE/AI_FACTORY_OS_BUSINESS_PLAN.md) | 商业目标与阶段规划 |

### 3.3 Execution Trace（执行追溯）

| 文档 | 职责 |
|------|------|
| [CURSOR_EXECUTION_HISTORY.md](../../05_EXECUTION/CURSOR_EXECUTION_HISTORY.md) | Cursor 重大修改台账 |

### 3.4 Asset Governance（资产治理）

| 文档 | 职责 |
|------|------|
| [ASSET_LIFECYCLE_POLICY.md](../policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md) | 资产分级、归属、清理策略 |
| [ASSET_AUDIT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md) | 审计规范 |
| [ASSET_SCAN_REPORT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md) | 扫描现状 |
| [ASSET_AUDIT_TEMPLATE.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md) | 登记模板 |

### 3.5 Domain Blueprints（领域设计蓝图）

| 文档 | 领域 |
|------|------|
| [COGNITION_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md) | 2_COGNITION 市场智能 |
| [CONTENT_FACTORY_BLUEPRINT.md](../runtime/AI_FACTORY_OS_CONTENT_FACTORY_BLUEPRINT.md) | 11_CONTENT_FACTORY 生产 |
| [DATA_INTELLIGENCE_BLUEPRINT.md](../runtime/AI_FACTORY_OS_DATA_INTELLIGENCE_BLUEPRINT.md) | 数据智能战略 |
| [MONETIZATION_BLUEPRINT.md](AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md) | 商业化路径 |

### 3.6 Database Intelligence Design Chain（数据库设计链）

| 文档 | 阶段 |
|------|------|
| [DATABASE_SCHEMA_BLUEPRINT.md](../database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md) | Schema 设计 |
| [DATABASE_REALITY_AUDIT.md](../../07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md) | 现状审计 |
| [DATABASE_MIGRATION_PLAN.md](../database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md) | 迁移策略 |
| [DATABASE_INTEGRATION_DESIGN.md](../database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md) | 接口契约 |
| [DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md](../database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md) | 实施规范 |

---

## 4. AI Recovery Workflow

### 标准恢复顺序

```
1. AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md（本文档 — 总览）
2. AI_FACTORY_OS_MODULE_REGISTRY.md
3. PROJECT_STATUS.md（Current Architecture Reality）
4. system_snapshot.md（Project / Data Flow Reality）
5. AI_FACTORY_OS_WORK_PRINCIPLES.md
6. CURSOR_EXECUTION_HISTORY.md（最近 Entry）
7. ASSET_LIFECYCLE_POLICY.md + ASSET_SCAN_REPORT.md（涉及文件/DB 时）
8. 领域 Blueprint（按任务选读）
```

### 恢复检查问题

AI 恢复后须能回答：

- 当前阶段是什么？（Construction / Commercial Validation / …）
- 哪些模块 Active / Frozen / Reserved？
- 当前真实数据流是什么？目标流是什么？
- 哪些文档是 Blueprint（未实现）vs Reality（已存在）？
- 最近 Cursor 做了什么？是否改了代码/DB？

---

## 5. Boundary Rules

| 规则 | 说明 |
|------|------|
| **docs 不参与运行** | 不写入 pattern、不触发 execution |
| **7_MEMORY 不参与规则定义** | 运行策略在 Memory；规则在 docs |
| **Blueprint ≠ Implemented** | 设计文档须标注状态 |
| **禁止目录名推测** | 必须以 MODULE_REGISTRY + STATUS 为准 |
| **变更同步** | 重大变更 → CURSOR_EXECUTION_HISTORY + 相关 STATUS/REGISTRY |

---

## 6. Completion Status

### Project Intelligence Layer 建设进度

| 子系统 | 状态 |
|--------|------|
| Context Recovery | ✅ Completed |
| Governance | ✅ Completed |
| Execution Trace | ✅ Completed |
| Asset Governance | ✅ Completed |
| Domain Blueprints | ✅ Completed（Cognition / CF / DI / Monetization） |
| Database Design Chain | ✅ Completed（Implementation Pending） |
| **Project Intelligence Blueprint（本文档）** | ✅ Completed |

### 运行时模块对照（摘要）

| 模块 | 状态 | Intelligence 文档 |
|------|------|-------------------|
| `0_START` ~ `11_CONTENT_FACTORY` | 见 MODULE_REGISTRY | 各 Blueprint |
| `2_COGNITION` | Blueprint Completed，代码 Pending | COGNITION_BLUEPRINT |
| Database | Design Chain Completed，Implementation Pending | DATABASE_* 系列 |

---

## 7. Relationship to Other Intelligence Concepts

| 概念 | 层级 | 位置 |
|------|------|------|
| **Project Intelligence Layer** | 项目认知 | `docs/` |
| **Market Intelligence（2_COGNITION）** | 运行时市场分析 | 未来 `2_COGNITION/` 代码 |
| **Data Intelligence Layer** | 商业数据战略 | DATA_INTELLIGENCE_BLUEPRINT |
| **Database Asset Layer** | 持久化商业数据 | `data/ai_factory.db` + DATABASE 设计链 |
| **7_MEMORY** | OS 运行时学习 | `7_MEMORY/*.json(l)` |

---

## 8. Future Evolution

| 方向 | 说明 |
|------|------|
| **自动 Recovery Checklist** | docs 内嵌验证脚本说明（仍不替代人工读 docs） |
| **Blueprint 版本号** | 各 Blueprint 统一 v1/v2 版本管理 |
| **Implementation 同步** | Database / Cognition 代码落地后更新 REALITY 章节 |
| **Commercial MVP 文档** | 30 产品实验模板纳入 Project Intelligence |

**禁止：** Project Intelligence Layer 膨胀为第二套运行系统。

---

## 9. Document Index（Master List）

| # | 文档 | 类别 |
|---|------|------|
| 0 | **AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md** | 总览 |
| 1 | AI_FACTORY_OS_MODULE_REGISTRY.md | Context |
| 2 | PROJECT_STATUS.md | Context |
| 3 | system_snapshot.md | Context |
| 4 | AI_FACTORY_OS_WORK_PRINCIPLES.md | Governance |
| 5 | AI_FACTORY_OS_BUSINESS_PLAN.md | Governance |
| 6 | CURSOR_EXECUTION_HISTORY.md | Trace |
| 7 | AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md | Asset |
| 8 | AI_FACTORY_OS_ASSET_AUDIT.md | Asset |
| 9 | AI_FACTORY_OS_ASSET_SCAN_REPORT.md | Asset |
| 10–19 | DATABASE_* / COGNITION_* / CONTENT_* / DATA_* / MONETIZATION_* | Domain |

---

## 相关文档

- [docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md](../../99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md) — 项目自描述原则
- [docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md](../../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) — 模块注册
