# AI Factory OS — System Snapshot

> 系统恢复说明 | 最后更新：2026-07-15（Entry 040-D1）

**Control Center（会话入口）：** [docs/00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md](../../00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md)

**Business Strategy（商业战略）：** [docs/03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md](../../03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md)

**Knowledge Update Protocol（知识更新协议）：** [docs/00_GOVERNANCE/AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md](../../00_GOVERNANCE/AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md)

**Project Intelligence Layer：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md)

**Unified Architecture：** [docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md](../../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md)

**State Authority：** [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_STATE_AUTHORITY_PROTOCOL.md](../../04_BLUEPRINT/policy/AI_FACTORY_OS_STATE_AUTHORITY_PROTOCOL.md)

**Commercial Lifecycle：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_LIFECYCLE_STATE_MACHINE.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_LIFECYCLE_STATE_MACHINE.md)

**Commercial Field Standard：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_STANDARD.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_STANDARD.md)

**Migration Strategy：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_MIGRATION_MATRIX.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_MIGRATION_MATRIX.md)

---

## 1. 项目名称

**AI Factory OS**

---

## 2. 当前架构

**目标统一架构（Blueprint — Entry 038-B）：**

```
Data → Cognition → Decision → Execution Runtime → Content Factory
  → Commercial Asset Layer → Feedback → Memory Learning
```

**当前 Runtime 现实（双轨 — 038-A 审计确认）：**

```
Track A (Core OS):
Planner → PolicyEngine → ExecutionRuntime → Memory
  (Data → Scoring → Decision → Local Publish)

Track B (Commercial / CF — Isolated):
commercial_assets JSON → Adapter → ContentPipeline → Product Asset (human-assisted)
```

**入口：**

- CLI：`python 0_START/main.py`
- HTTP：`10_DEPLOY/api.py` → `controller.run()`
- CF Adapter：`11_CONTENT_FACTORY/adapter/adapter_runner.py`（独立）

**Architecture Doc：** [docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md](../../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md)

**明确：** Architecture Alignment ≠ Full Refactor；Runtime Integration Not Started。

---

## 3. Memory 职责（`7_MEMORY/` — 运行记忆层）

| 文件 | 职责 |
|------|------|
| `event_log.jsonl` | 事实记录层 — 所有系统事件流水 |
| `pattern_memory.json` | 模式学习层 — 从执行结果提取模式 |
| `strategy_memory.json` | 策略层 — 基于模式更新决策策略 |
| `runtime_policy.json` | 运行策略层 — 当前生效的策略参数 |

**边界：** `7_MEMORY` 仅负责运行时数据读写，不参与系统规则定义。

---

## 4. docs 职责（`/docs/` — 系统认知层）

| 文件 | 职责 |
|------|------|
| `AI_FACTORY_OS_WORK_PRINCIPLES.md` | 系统规则参考 — 升级原则、协作规则、安全约束 |
| `AI_FACTORY_OS_BUSINESS_PLAN.md` | 商业目标参考 — 收入模型、阶段规划 |
| `system_snapshot.md` | 系统恢复说明 — 本文档 |

**边界：** `docs` 不参与 pattern extraction、strategy update、execution。

---

## Project Context Layer

`docs/` 目录构成 **Project Context Layer（项目上下文层）**，为 AI Factory OS 提供长期恢复与协作能力。

| 文档 | 职责 |
|------|------|
| `AI_FACTORY_OS_WORK_PRINCIPLES.md` | 系统协作规则 — 升级原则、人机协作、安全约束 |
| `AI_FACTORY_OS_BUSINESS_PLAN.md` | 商业目标 — 收入模型、阶段规划、风险控制 |
| `system_snapshot.md` | 架构恢复说明 — 系统结构、Memory 边界、快速恢复清单 |
| `PROJECT_STATUS.md` | 工程进度说明 — 已完成建设、未完成模块、下一阶段规划 |
| `AI_FACTORY_OS_CONTENT_FACTORY_BLUEPRINT.md` | Content Factory 设计层 |
| `AI_FACTORY_OS_DATA_INTELLIGENCE_BLUEPRINT.md` | Data Intelligence 战略设计层 |
| `AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md` | Content Factory 商业化战略设计层 |
| `AI_FACTORY_OS_MODULE_REGISTRY.md` | 模块注册表 — 各目录状态与职责 |
| `AI_FACTORY_OS_COGNITION_BLUEPRINT.md` | 2_COGNITION Market Intelligence Layer 设计层 |
| `AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` | 商业数据资产 Schema 设计层 |
| `AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md` | 现有 ai_factory.db 只读审计报告 |
| `AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md` | 数据库 Additive 演化计划 |
| `AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md` | 跨模块 Database Contract 设计 |
| `AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md` | Database Extension 实施执行规范 |
| `AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md` | 项目资产治理总规范 |
| `CURSOR_EXECUTION_HISTORY.md` | Cursor 重大修改执行历史 |
| `AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md` | 项目资产治理 — 分级、归属、生命周期 |
| `AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md` | Project Intelligence Layer 总架构 |
| `AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` | 商业智能 Object 契约 v1 |
| `AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md` | 2_COGNITION Agent 架构 v1 |
| `AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md` | Commercial Validation Layer — 商业 MVP 验证设计 v1 |
| `AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md` | Commercial Experiment Layer — 商业实验管理体系 v1 |
| `AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` | Commercial Experiment Asset Layer — 实验对象登记规范 v1 |
| `AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md` | Commercial Experiment Selection Layer — 实验选择规则 v1 |
| `AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md` | Production Request Contract Layer — 生产请求协议 v1 |
| `AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md` | Production Pipeline Integration Layer — CF 集成设计 v1 |
| `AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md` | Adapter Layer Planning — Adapter 实施方案 v1 |
| `AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md` | Product Asset Layer — 产品资产契约 v1 |
| `AI_FACTORY_OS_PRODUCT_ASSET_VALIDATION_GATE.md` | Product Asset Validation Gate — 验收门禁设计 v1 |
| `AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md` | Feedback Layer — 反馈对象契约 v1 |
| `AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md` | Experiment Evaluation — 实验评估框架 v1 |
| `AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md` | Adapter Architecture Audit — Runtime 审计 v1 |
| `AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md` | Experiment Prepared Review Layer — 实验准备审核协议 v1 |
| `AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md` | Opportunity Candidate Asset Layer — 商业机会候选登记 v1 |
| `AI_FACTORY_OS_OPPORTUNITY_DATASET_GENERATION_RULE.md` | Opportunity Dataset Generation Layer — 数据生成规范 v1 |

**原则：** Project Context Layer 仅服务于人类与 AI 的系统认知，不参与任何运行计算。

---

# Project Intelligence Layer

**Blueprint：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md)

`docs/` 构成 **Project Intelligence Layer** — 与 `7_MEMORY/` 运行记忆物理隔离。

| 子系统 | 核心文档 | 状态 |
|--------|----------|------|
| Context Recovery | MODULE_REGISTRY, PROJECT_STATUS, system_snapshot | ✅ |
| Governance | WORK_PRINCIPLES, BUSINESS_PLAN | ✅ |
| Execution Trace | CURSOR_EXECUTION_HISTORY | ✅ |
| Asset Governance | ASSET_LIFECYCLE_POLICY, ASSET_AUDIT, SCAN_REPORT | ✅ |
| Domain Blueprints | COGNITION, CONTENT_FACTORY, DATA_INTELLIGENCE, COMMERCIAL_CONTRACT, COMMERCIAL_MVP, COMMERCIAL_EXPERIMENT, … | ✅ |
| Database Design Chain | DATABASE_SCHEMA → … → IMPLEMENTATION_PLAN | ✅ |

**AI 恢复入口：** 先读 PROJECT_INTELLIGENCE_BLUEPRINT，再按 §4 Recovery Workflow 顺序读子文档。

---

# Commercial Intelligence Contract Layer

**Contract：** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../../04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)

商业智能链路标准对象（v1.0）：

```
Market Signal → Opportunity → Production Request → Product Asset → Feedback
```

| Object | 模块边界 |
|--------|----------|
| Market Signal | `1_DATA` → DB |
| Opportunity | `2_COGNITION` → `3_DECISION` |
| Production Request | `3_DECISION` → `11_CONTENT_FACTORY` |
| Product Asset | `11_CONTENT_FACTORY` → DB |
| Feedback | → Cognition / Decision 闭环 |

与 Database Integration Design 互补：Integration 定义 DB 接口；Contract 定义 Object 语义与 Agent 规则。

---

# 2_COGNITION Agent Architecture

**Blueprint：** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md)

```
Market Signal → TrendAgent / DemandAgent / CompetitionAgent
                        ↓
                 OpportunityAgent → Opportunity Object
                        ↓
                 InsightAgent → Business Insight
                        ↓
                 3_DECISION
```

| Agent | 输出 Object |
|-------|-------------|
| TrendAgent | Trend Insight |
| DemandAgent | Demand |
| CompetitionAgent | Competition |
| OpportunityAgent | Opportunity（Contract v1） |
| InsightAgent | Business Insight |

**状态：** Blueprint ✅ | 代码 Pending | 目录 `2_COGNITION/` 当前为空

---

# Asset Governance Layer

项目资产已具备完整治理文档栈：

| 能力 | 文档 | 状态 |
|------|------|------|
| **Audit** | `AI_FACTORY_OS_ASSET_AUDIT.md` + `ASSET_SCAN_REPORT.md` | ✅ |
| **Classification** | `AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md` §2 | ✅ |
| **Lifecycle** | `AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md` §4 + `ASSET_AUDIT_TEMPLATE.md` | ✅ |
| **Protection** | DB / Artifact / Cleanup 策略 — Policy §5–§8 | ✅ |

**总规范：** [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](../../04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)

---

## Content Factory Monetization Layer

**引用：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md)

定义 Content Factory 商业化路径、产品验证方法、销售反馈闭环。

**性质：** 商业认知层，**不参与运行**。

---

## Content Factory Blueprint Layer

`docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_BLUEPRINT.md` 构成 **Content Factory Blueprint Layer（内容工厂设计层）**。

| 内容 | 说明 |
|------|------|
| 战略定位 | AI 数字资产生产系统，完整商业闭环设计 |
| 产品方向 | A/B/C 级数字产品优先级分析 |
| 未来架构 | `11_CONTENT_FACTORY/` 目录与 Agent 职责（**当前未创建**） |
| 核心连接 | Content Agent 经 ExecutionRuntime 调度，不绕过 Controller |
| Memory 扩展 | `product_pattern` 设计，event → pattern → strategy 闭环 |
| 发布策略 | 半自动发布辅助，禁止高风险自动化 |
| 模型规划 | DeepSeek / GPT / Claude / Gemini 任务映射 |
| 三层关系 | Content Factory → 9_PRODUCT → 10_DEPLOY |

**状态：** 设计阶段 — 11_CONTENT_FACTORY 已建设并运行，本蓝图仍为设计参考。

---

## Future Layer: Data Intelligence Layer

**引用：** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_DATA_INTELLIGENCE_BLUEPRINT.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_DATA_INTELLIGENCE_BLUEPRINT.md)

Data Intelligence Layer 位于 `1_DATA` 与 `11_CONTENT_FACTORY` 之间，负责数据采集、市场分析、产品机会评分。

**当前状态：** 设计规划阶段，**不参与当前运行**。

---

# Project Reality Snapshot

## 当前系统不是从零建设

**已有能力：**

- Core OS（`0_START`）
- Data Foundation（`1_DATA`）
- Decision Engine（`3_DECISION`）
- Memory System（`7_MEMORY`）
- Deployment Layer（`10_DEPLOY`）
- Content Factory Production（`11_CONTENT_FACTORY`）

**当前缺失：**

- Market Intelligence Layer（`2_COGNITION` — 设计待定）
- Opportunity Discovery Layer（机会发现流程未建）
- Commercial Feedback Loop（商业反馈闭环未跑通）

**模块注册：** 见 [docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md](../AI_FACTORY_OS_MODULE_REGISTRY.md)

---

# Current Data Flow Reality

## 当前真实流程

```
1_DATA
    Data Collection
        ↓
3_DECISION
    Decision Scoring
        ↓
11_CONTENT_FACTORY
    Product Production
        ↓
10_DEPLOY
    External Access
        ↓
Feedback
        ↓
7_MEMORY
```

## 当前缺失

**`2_COGNITION`** — 负责 Market Intelligence

目标链路（尚未接通）：

```
1_DATA → 2_COGNITION → 3_DECISION → 11_CONTENT_FACTORY
```

**说明：** 当前 Decision 直接接收 Data 层输出，缺少市场理解与机会发现环节。详见 [docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md](PROJECT_STATUS.md) — Current Architecture Reality Update。

---

# Commercial Loop Reality（商业闭环现实）

## Current Runtime（当前运行流）

**实际已跑通的能力：**

```
1_DATA（Market Signal 采集 — Legacy）
        ↓
3_DECISION（Scoring / Decision — 未标准化 Opportunity Object）
        ↓
11_CONTENT_FACTORY（Product Asset 生产 — 真实 artifact）
        ↓
Publish（半自动发布辅助 + 人工上架）
        ↓
Feedback（人工记录 → product_memory.json — 非标准 Feedback Object）
        ↓
7_MEMORY（OS 运行记忆 — 与商业 DB 物理隔离）
```

| 环节 | 当前状态 | 缺口 |
|------|----------|------|
| Market Signal | ✅ `1_DATA` Legacy 采集 | 未对齐 Contract v1 Object |
| Opportunity | ❌ 缺失 | `2_COGNITION` 未实现，MVP 人工选品 |
| Production Request | ⚠️ Partial | Decision 产出未完全标准化 |
| Product Asset | ✅ Active | DB `generated_products` 未建 |
| Publish | ✅ 半自动 | 人工确认必需 |
| Customer Feedback | ⚠️ Partial | `product_feedback` 表未建 |
| Database 闭环 | ❌ 缺失 | Feedback 未沉淀至 DB |
| Optimization | ❌ 缺失 | 无 Feedback 驱动 Cognition |

## Future Commercial Loop（目标商业闭环）

**Blueprint 定义 — 尚未接通：**

```
Market Signal（1_DATA）
        ↓
Opportunity Object（2_COGNITION）
        ↓
Production Request（3_DECISION）
        ↓
Content Factory（11_CONTENT_FACTORY）
        ↓
Product Asset
        ↓
Publish（半自动 + 人工）
        ↓
Customer Feedback → Feedback Object
        ↓
Database（product_feedback / generated_products）
        ↓
Optimization（2_COGNITION + 3_DECISION）
        ↓
（循环）
```

**Blueprint：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md)

**Commercial Validation Layer（商业验证层）：** Blueprint Completed — 定义 30 产品实验、成功标准、Feedback 架构与 MVP Timeline；**不参与运行**。

### Current vs Future 对照

| 维度 | Current Runtime | Future Commercial Loop |
|------|-----------------|------------------------|
| 选品 | 人工 / Legacy Scoring | `2_COGNITION` Opportunity Score |
| 生产 | ✅ Content Factory | ✅ 同左 |
| 反馈存储 | product_memory.json | `product_feedback` 表 |
| 优化 | 无自动闭环 | Feedback → Cognition 权重校准 |
| MVP 阶段 | Phase 0（设计完成） | Phase 1–5（见 Commercial MVP Blueprint §8） |

---

# Commercial Experiment Layer（商业实验层）

**Blueprint：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md)

Commercial Experiment Layer（商业实验层）管理 30 产品验证实验的**设计、记录、评估、反馈沉淀** — docs 认知层，**不参与运行**。

## Current Runtime（当前运行 — 实验能力）

**实验管理体系尚未接入运行链：**

| 能力 | 当前状态 |
|------|----------|
| Experiment Object 台账 | ⚠️ Registry 规范 ✅ — 实例 JSON 未建 |
| Opportunity Candidate 实例 | ✅ 5 条 — commercial_assets/opportunity_candidates_v1.json |
| Experiment Lifecycle 追踪 | ❌ 未建 — 无状态机代码 |
| Feedback Object v1 录入 | ⚠️ Partial — product_memory.json 非标准格式 |
| Evaluation Model | ❌ 未建 — 人工判断 |
| Category A/B/C 30 批次 | ❌ 未启动 |

**当前仍可用的生产相关能力：**

```
3_DECISION → 11_CONTENT_FACTORY → Publish（人工）→ product_memory.json
```

## Future Commercial Validation System（目标商业验证体系）

**Blueprint 定义 — 尚未接通：**

```
Market Signal
        ↓
Opportunity
        ↓
Experiment Design（Experiment Object — Draft → Prepared）
        ↓
Content Factory（Production → Published）
        ↓
Feedback（Feedback Object v1 — Testing）
        ↓
Evaluation（Success / Promising / Failed）
        ↓
Database（commercial_experiments / generated_products / product_feedback）
        ↓
Cognition（Opportunity Score 优化）
        ↓
（循环）
```

### Current Runtime vs Future Commercial Validation System

| 维度 | Current Runtime | Future Commercial Validation System |
|------|-----------------|-------------------------------------|
| 实验设计 | 无标准 Experiment Object | Experiment Object + Hypothesis 五问 |
| 生命周期 | 无状态追踪 | Draft → … → Archived |
| 实验分类 | 无 | Category A/B/C 各 10 |
| 反馈结构 | product_memory.json | Feedback Object v1 → product_feedback |
| 评估 | 无 | Success / Promising / Failed |
| Cognition 学习 | 无 | Feedback → opportunity_scores 权重 |

**层级关系：**

```
Commercial Validation Layer（MVP 目标 — COMMERCIAL_MVP_BLUEPRINT）
        ↓
Commercial Experiment Layer（实验管理 — COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT）
        ↓
Runtime Modules（1_DATA / 2_COGNITION / 3_DECISION / 11_CONTENT_FACTORY）
```

---

# Commercial Experiment Asset Layer（商业实验资产层）

**Registry：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)

Commercial Experiment Asset Layer（商业实验资产层）定义 **Experiment Object（实验对象）** 的标准登记格式与生命周期 — docs 认知层，**不参与运行**。

## 当前状态（Registry vs Implementation）

| 资产 | 状态 |
|------|------|
| Experiment Object Registry v1（登记规范） | ✅ Blueprint Completed |
| 实验台账 JSON 文件 | ❌ 未创建 |
| `commercial_experiments` DB 表 | ❌ 未创建（Blueprint 建议） |
| 30 产品 Experiment Object 实例 | ❌ 0 / 30 |

## 实验资产数据流（目标）

```
Experiment Object Registry（登记规范 — EXPERIMENT_OBJECT_REGISTRY）
        ↓
Experiment Object 实例（JSON 台账 — 未来 commercial_experiments）
        ↓
3_DECISION → 11_CONTENT_FACTORY → 10_DEPLOY
        ↓
Feedback Object → metrics 回填
        ↓
result + learning_summary
        ↓
Database（generated_products / product_feedback — Pending）
        ↓
2_COGNITION Learning（Pending）
        ↓
7_MEMORY 摘要（单向 — 不替代 Registry）
```

## Current Runtime vs Future Commercial Validation System

| 维度 | Current Runtime | Future Commercial Validation System |
|------|-----------------|-------------------------------------|
| 实验登记 | 无标准 Registry | Experiment Object Registry v1 ✅ |
| 实验实例 | 无 | 30 × JSON / DB 台账 |
| 生命周期追踪 | 无 | feedback_status 9 状态 |
| 评价 | 无 | Success / Promising / Failed |
| Cognition 读取 | 无 | §7 AI Read Rules |

**层级关系：**

```
Commercial Validation Layer（MVP）
        ↓
Commercial Experiment Layer（System Blueprint）
        ↓
Commercial Experiment Asset Layer（Object Registry — 本次）
        ↓
Runtime Modules
```

---

# Opportunity Candidate Asset Layer（商业机会候选资产层）

**Registry：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md)

Opportunity Candidate Asset Layer（商业机会候选资产层）是 **Commercial Intelligence Asset（商业智能资产）** 的第一层池 — 管理 **Opportunity Candidate（商业机会候选）**，**不等于** Opportunity Object（商业机会对象）。

## 完整商业智能链（更新）

```
Market Intelligence（1_DATA / 2_COGNITION）
        ↓
Opportunity Candidate Pool（候选资产池 — OPPORTUNITY_CANDIDATE_REGISTRY）
        ↓
Opportunity Object（Contract v1 — 2_COGNITION 产出）
        ↓
Experiment Selection Layer（SELECTION_FRAMEWORK）
        ↓
Experiment Object（EXPERIMENT_OBJECT_REGISTRY）
        ↓
3_DECISION → 11_CONTENT_FACTORY → Feedback
```

## 当前状态

| 资产 | 状态 |
|------|------|
| Opportunity Candidate Registry v1 | ✅ Blueprint Completed |
| Candidate 实例 | ✅ 5 条 — opportunity_candidates_v1.json |
| Opportunity Object 自动产出 | ❌ 2_COGNITION Pending |
| DB `opportunity_candidates` | ❌ 未创建 |

---

# Commercial Asset Instance Layer Created（商业资产实例层已创建）

**Dataset：** [commercial_assets/opportunity_candidates/opportunity_candidates_v1.json](../commercial_assets/opportunity_candidates/opportunity_candidates_v1.json)

AI Factory OS **首次**创建真实 Commercial Intelligence Asset（商业智能资产）数据实例 — 非 docs 规范，非数据库，为 Project Intelligence 之外的**商业资产文件层**。

## 实例状态

| 项 | 值 |
|----|-----|
| **路径** | `commercial_assets/opportunity_candidates/opportunity_candidates_v1.json` |
| **schema_ref** | OPPORTUNITY_CANDIDATE_REGISTRY v1 |
| **batch** | category_a_batch_001 |
| **count** | 5 |
| **category** | 全部 A |
| **status** | 全部 `discovered` |
| **readiness_score 范围** | 78–86 / 100 |

## 与 Blueprint 层关系

```
docs/ Registry + Generation Rule（规范层）
        ↓
commercial_assets/（实例层 — 本次创建）
        ↓
未来 DB opportunity_candidates（Pending）
        ↓
2_COGNITION / Selection / Experiment（Pending）
```

## 当前 vs 目标

| 维度 | 创建前 | 创建后（Current） |
|------|--------|-------------------|
| Candidate JSON | ❌ | ✅ 5 条 |
| Opportunity Object JSON | ❌ | ✅ 5 条（human_assisted） |
| Experiment Object | ❌ | ❌ |
| 产品生产 | — | ❌ 未触发 |

---

# Opportunity Object Instance Layer Created（商业机会标准对象实例层已创建）

**Dataset：** [commercial_assets/opportunities/opportunities_v1.json](../commercial_assets/opportunities/opportunities_v1.json)

首批 **Opportunity Object（商业机会标准对象）** 实例 — 由 5 条 Candidate 人工辅助转换，对齐 Commercial Intelligence Contract v1。

| 项 | 值 |
|----|-----|
| **路径** | `commercial_assets/opportunities/opportunities_v1.json` |
| **count** | 5 |
| **conversion_method** | human_assisted |
| **score_method** | human_assisted_score（全部） |
| **recommendation** | produce: 4，watch: 1，skip: 0 |
| **2_COGNITION** | ❌ 未参与 — 非 Cognition Automation |

## 商业资产实例链（Current）

```
commercial_assets/opportunity_candidates/opportunity_candidates_v1.json（5 Candidate）
        ↓ human_assisted conversion
commercial_assets/opportunities/opportunities_v1.json（5 Opportunity Object）
        ↓ human_assisted selection
commercial_assets/experiment_selection/experiment_selection_records_v1.json（selected 4 / watch 1）
        ↓ human_assisted experiment design
commercial_assets/experiments/experiments_v1.json（4 Experiment Object — draft，未修改）
        ↓ human_assisted prepared review
commercial_assets/experiment_reviews/experiment_reviews_v1.json（4 Review — prepared 3 / rejected 1）
        ↓ human_assisted production request creation
commercial_assets/production_requests/production_requests_v1.json（3 Production Request — draft，未修改）
        ↓ human_assisted approval
commercial_assets/production_request_reviews/production_request_reviews_v1.json（3 Approval — approved）
        ↓ Integration Design ✅ + Adapter Plan ✅ — Code Pending
Content Factory Adapter → 11_CONTENT_FACTORY → Product Asset → Feedback
                                              ↑
                                    Product Asset Contract v1 已定义 — 实例未创建
```

**Selection 记录：** [commercial_assets/experiment_selection/experiment_selection_records_v1.json](../commercial_assets/experiment_selection/experiment_selection_records_v1.json)

| 项 | 值 |
|----|-----|
| **首次 Selection 执行** | ✅ 2026-07-08 |
| **selected** | 4 |
| **watch** | 1 |
| **rejected** | 0 |
| **pending_experiment** | 4（Selection 层状态，Experiment 已创建） |

**Experiment 实例：** [commercial_assets/experiments/experiments_v1.json](../commercial_assets/experiments/experiments_v1.json)

| 项 | 值 |
|----|-----|
| **首次 Experiment Object 创建** | ✅ 2026-07-08 |
| **count** | 4 |
| **category** | 全部 A |
| **status** | 全部 `draft` |
| **experiment_method** | human_assisted |
| **artifact / product** | ❌ 未创建 |

**Experiment Review 实例：** [commercial_assets/experiment_reviews/experiment_reviews_v1.json](../commercial_assets/experiment_reviews/experiment_reviews_v1.json)

| 项 | 值 |
|----|-----|
| **首次 Review 执行** | ✅ 2026-07-09 |
| **count** | 4 |
| **prepared** | 3 |
| **rejected** | 1 |
| **review_method** | human_assisted |
| **experiments_v1 修改** | ❌ 未修改 |

**约束：** Human Assisted ≠ Automation；Review Completed ≠ Production Started；Experiment 与 Review 为独立实体。

---

# Commercial Experiment Review Asset Instance（商业实验审核资产实例）

**Dataset：** [commercial_assets/experiment_reviews/experiment_reviews_v1.json](../commercial_assets/experiment_reviews/experiment_reviews_v1.json)

AI Factory OS **首次**创建 Experiment Review Object（实验审核对象）商业资产实例 — 对齐 Experiment Prepared Review Protocol v1。

| 项 | 值 |
|----|-----|
| **路径** | `commercial_assets/experiment_reviews/experiment_reviews_v1.json` |
| **schema_ref** | EXPERIMENT_PREPARED_REVIEW_PROTOCOL v1 |
| **count** | 4 |
| **prepared** | 3 |
| **rejected** | 1 |
| **review_method** | human_assisted |
| **experiments_v1** | 未修改 — 独立实体 |

**rejected 说明：** exp_20260708_002（Excel 家庭记账表）— 免费模板供给充足、commercial_pass=false、首批队列筛选。

---

# Production Request Asset Instance Layer（生产请求资产实例层）

**Dataset：** [commercial_assets/production_requests/production_requests_v1.json](../commercial_assets/production_requests/production_requests_v1.json)

AI Factory OS **首次**创建 Production Request Object（生产请求对象）商业资产实例 — 对齐 Production Request Contract v1。

| 项 | 值 |
|----|-----|
| **路径** | `commercial_assets/production_requests/production_requests_v1.json` |
| **schema_ref** | PRODUCTION_REQUEST_CONTRACT v1 |
| **count** | 3 |
| **status** | 全部 `draft` |
| **creation_method** | human_assisted |
| **priority** | P0: exp_005；P1: exp_001, exp_004 |
| **excluded** | exp_002（Review rejected） |
| **Content Factory** | ❌ 未调用 |

**约束：** Production Request Creation ≠ Content Factory Execution；Blueprint ≠ Implementation。

---

# Production Authorization Gate（生产授权门禁）

**Dataset：** [commercial_assets/production_request_reviews/production_request_reviews_v1.json](../commercial_assets/production_request_reviews/production_request_reviews_v1.json)

Production Authorization Gate（生产授权门禁）记录 Production Request 的人工审批结果 — **Approval 资产层，不触发 Runtime 生产**。

| 项 | 值 |
|----|-----|
| **路径** | `commercial_assets/production_request_reviews/production_request_reviews_v1.json` |
| **count** | 3 |
| **decision** | 全部 `approved` |
| **review_method** | human_assisted |
| **approved_by** | human |
| **production_requests_v1** | 未修改 — PR 仍为 draft（独立实体） |
| **Content Factory** | ❌ 未调用 |

**门禁：** Approval Completed ≠ Content Factory Execution；approved 仅表示人工授权记录，不等于生产已开始。

**映射：**

| approval_id | source_production_request_id | product | priority |
|-------------|------------------------------|---------|----------|
| appr_20260713_001 | preq_20260712_001 | 商业计划书 PPT 模板 | P1 |
| appr_20260713_004 | preq_20260712_004 | 工作总结 PPT 模板 | P1 |
| appr_20260713_005 | preq_20260712_005 | Excel 考勤记录表 | P0 |

---

# Production Pipeline Integration Layer（生产管线集成层）

**Design：** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md)

Production Pipeline Integration Layer 定义 Production Request 进入 `11_CONTENT_FACTORY` 的 Input/Output Contract 与 Agent 映射 — docs 认知集成层，**不参与运行**。

| 能力 | 状态 |
|------|------|
| Integration Design v1 | ✅ Design Completed |
| Input Contract v1 | ✅ 文档定义 |
| Agent Mapping（bypass MarketAgent） | ✅ 文档定义 |
| Product Asset Output Schema | ✅ 文档定义 |
| Feedback → Experiment Evaluation | ✅ 文档定义 |
| Runtime Protection Rules | ✅ 文档定义 |
| Integration Adapter 代码 | ❌ Code Implementation Pending |
| `11_CONTENT_FACTORY` 代码变更 | ❌ 未修改 |
| Pilot Production | ❌ 未执行 |

**当前 CF Runtime：** `content_pipeline.run(keyword)` — Legacy 路径；实验批次路径 **未接入**。

**明确：** Design Completed ≠ Runtime Connected；Blueprint ≠ Implementation。

---

# Adapter Layer Planning（Adapter 层规划）

**Plan：** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md)

Adapter Layer Planning 定义 Production Request 进入 Content Factory 的 **Adapter 实施方案** — docs 认知规划层，**不参与运行**。

| 能力 | 状态 |
|------|------|
| Adapter Implementation Plan v1 | ✅ Plan Completed |
| Legacy Flow 分析 | ✅ 文档定义 |
| Input / Output 映射 | ✅ 文档定义 |
| 未来文件结构（adapter/ contracts/ services/） | ✅ 仅设计 — 未创建 |
| Pilot 范围（preq_20260712_005 P0） | ✅ 文档定义 |
| 风险控制（Gate / Rollback / Legacy Protection） | ✅ 文档定义 |
| Adapter 代码 | ❌ Code Implementation Pending |
| Pilot 生产 | ❌ Pilot Execution Pending |

**Legacy 兼容：** 保留 `content_pipeline.run(keyword)`；Experiment 路径新增 `run_from_production_request()` — Implementation Pending。

**明确：** Plan Completed ≠ Code Implemented；Approval ≠ Production Started。

---

# Product Asset Layer（产品资产层）

**Contract：** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](../../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md)

Product Asset Layer 定义 Content Factory 生产完成后的 **Product Asset Object** 标准契约 — docs 认知契约层，**不参与运行**。

| 能力 | 状态 |
|------|------|
| Product Asset Contract v1 | ✅ Blueprint Completed |
| Object Schema（含 artifact_information） | ✅ 文档定义 |
| Lifecycle（8 状态） | ✅ 文档定义 |
| CF Output 映射 | ✅ 文档定义 |
| Feedback 四类连接 | ✅ 文档定义 |
| 未来 DB `product_assets` | ⏳ Blueprint — 未 CREATE TABLE |
| `commercial_assets/product_assets/` | ❌ 未创建 |
| 实际产品文件 | ❌ 未生成 |

**职责：** 记录实际生成资产 — 不是生产任务、不是实验定义、不是市场机会。

**明确：** Contract Completed ≠ Runtime Connected；Production Request Approved ≠ Product Created；Blueprint ≠ Implementation。

---

# Adapter Layer Planning（Adapter 层规划 — Runtime 审计）

**Audit：** [docs/07_AUDIT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md](../../07_AUDIT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md)

Content Factory Adapter Architecture Audit v1 — 只读 Runtime 审计，确认 Legacy 路径与 Adapter 插入点。

| 能力 | 状态 |
|------|------|
| Adapter Architecture Audit v1 | ✅ Audit Completed |
| Legacy Pipeline 分析 | ✅ run(keyword) → 7 步 Agent |
| 0_START / 3_DECISION CF 引用 | ❌ 无 — Adapter 无需改 Core OS |
| 推荐插入点 | `run_from_production_request()` + adapter/ |
| Adapter 代码 | ❌ Code Implementation Pending |
| Pilot 生产 | ❌ 未执行 |

**关键发现：** `validate_artifacts()` 要求 has_pdf — Excel Pilot 须在 Implementation 时处理。

**明确：** Audit Completed ≠ Code Implemented；Blueprint ≠ Runtime Connected。

---

# Adapter Runtime Layer Created（Adapter 运行时层已创建）

**Content Factory Adapter Code Implementation v1**

| 能力 | 状态 |
|------|------|
| `11_CONTENT_FACTORY/adapter/` | ✅ Created |
| `run_from_production_request()` | ✅ Added — MarketAgent bypass |
| `run(keyword)` Legacy | ✅ Unchanged |
| Approval Gate | ✅ Implemented |
| Pilot Whitelist | ✅ preq_20260712_005 only |
| Default dry_run | ✅ No commercial deliverable files |
| product_assets JSON | ❌ Not created |
| Pilot --execute | ❌ Not run |

**CLI（dry-run）：** `python 11_CONTENT_FACTORY/adapter/adapter_runner.py --preq preq_20260712_005`

**明确：** Adapter Completed ≠ Production Started；Code Completed ≠ Commercial Asset Created。

---

# Adapter Validation Layer（Adapter 验证层）

**Entry 032-C — Content Factory Adapter Regression Test v1**

| 测试 | 结果 |
|------|------|
| Test 1 Legacy Flow Regression | ✅ PASS — run(keyword) market→creator→generator（mock） |
| Test 2 Adapter Module Import | ✅ PASS |
| Test 3 Approval Gate Positive (preq_005) | ✅ PASS |
| Test 4 Pilot Whitelist Blocking (preq_001) | ✅ PASS — PILOT_NOT_ALLOWED |
| Test 5 Missing Approval Blocking | ✅ PASS — NO_APPROVAL |
| Test 6 Dry Run (preq_005) | ✅ PASS — Generator 未调用；0 商业文件 |

**脚本：** `11_CONTENT_FACTORY/adapter/regression_test_v1.py`

**明确：** Regression Completed ≠ Commercial Launch；Dry Run ≠ Production；Adapter Ready ≠ Product Created。

---

# Product Asset Validation Gate Layer（产品资产验收门禁层）

**Design：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PRODUCT_ASSET_VALIDATION_GATE.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_PRODUCT_ASSET_VALIDATION_GATE.md)

Product Asset Validation Gate v1 — CF Output 入库前验收设计；Validation Gate ≠ QualityAgent。

| 能力 | 状态 |
|------|------|
| Validation Gate Design v1 | ✅ Blueprint Completed |
| product_asset_validation Object | ✅ Schema 定义 |
| Validation Checklist（4 类） | ✅ 设计完成 |
| Validation Gate Runtime | ❌ 未实现 |
| product_assets JSON | ❌ 未创建 |
| Pilot Production | ❌ 未执行 |

**决策规则：** `passed` → 允许 product_assets；`failed` → 禁止；`pending_review` → 人工裁量。

**明确：** Validation Gate Completed ≠ Production Started；Design Completed ≠ Runtime Connected。

---

# Validation Runtime Layer Created（Validation Runtime 层已创建）

**Entry 033-A — Product Asset Validation Runtime Implementation v1**

| 能力 | 状态 |
|------|------|
| `11_CONTENT_FACTORY/validation/` | ✅ Created |
| `ProductAssetValidator` | ✅ Implemented |
| 四类 Checklist | ✅ artifact / contract / quality / commercial |
| validation_status | passed / failed / pending_review |
| Unit Tests | ✅ 5/5 PASS |
| product_assets 写入 | ❌ Runtime 不负责 |
| Pilot --execute | ❌ 未执行 |

**测试：** `python 11_CONTENT_FACTORY/validation/test_product_asset_validator.py`

**明确：** Validation Runtime Completed ≠ Production Started；Code Completed ≠ Product Created。

---

# First Commercial Production Loop（首次商业生产闭环）

**Entry 033-B1 — Pilot Production Controlled Execution v1**

| 步骤 | 结果 |
|------|------|
| Approval Gate | ✅ appr_20260713_005 |
| Adapter + CF `--execute` | ✅ pipeline status=ok |
| Artifact | ✅ `templates/8523329941d4.xlsx` + manual.pdf |
| Validation Gate | ✅ passed |
| product_assets | ✅ 1 条 registered |
| Pilot Lock | ✅ 仅 preq_20260712_005 |

**路径：** `commercial_assets/pilot_outputs/preq_20260712_005/`

**明确：** Production Completed ≠ Commercial Success；Validation Passed ≠ Market Validated。

---

# Feedback & Experiment Evaluation Layer（反馈与实验评估层）

**Entry 034 — Feedback & Experiment Evaluation Layer Design v1**

| 能力 | 状态 |
|------|------|
| Feedback Object Contract v1 | ✅ Blueprint Completed |
| Experiment Evaluation Framework v1 | ✅ Blueprint Completed |
| 五类 Feedback Type | ✅ 设计完成 |
| 四类 Score 隔离 | ✅ Readiness / Opportunity / Priority / Evaluation |
| feedback JSON 实例 | ❌ 未创建 |
| evaluation JSON 实例 | ❌ 未创建 |

**Design：** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md](../../04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md) | [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md)

**Pilot 锚点：** `8523329941d4` — exp_20260708_005 — Feedback Pending

**明确：** Feedback Design ≠ Market Validation；Blueprint ≠ Implementation。

---

# First Commercial Learning Loop Entry（首次商业学习闭环入口）

**Entry 035 — Pilot Feedback & Experiment Evaluation Instance Generation v1**

| 项 | 值 |
|----|-----|
| **Product Asset** | `8523329941d4` — Excel 考勤记录表 |
| **Experiment** | `exp_20260708_005` |
| **Feedback** | `fbk_20260713_001` — `pending` / `observation_period: not_started` |
| **Evaluation** | `eval_20260713_001` — `hypothesis_result: pending` / `recommendation: collect_feedback` |
| **市场数据** | 未填写 — actual 均为 null（生产 quality 0.89 除外） |

**链路：**
```
Product Asset → Feedback (pending) → Evaluation (pending) → Learning (未开始)
```

**明确：** Feedback Created ≠ Market Validation；Evaluation Created ≠ Experiment Success；Commercial Asset ≠ Commercial Result。

---

# Observation Governance Layer（观察治理层）

**Entry 036-A — Pilot Observation Protocol Design v1**

| 能力 | 状态 |
|------|------|
| Pilot Observation Protocol v1 | ✅ Blueprint Completed |
| Observation Metric Schema（4 类） | ✅ 设计完成 |
| observation_status | **planned** — 未开始 |
| Success / Failure Criteria | ✅ 设计完成 |
| Data Governance | ✅ 禁止伪造/预测 |
| Feedback / Evaluation JSON | ❌ 未修改 |
| 观察执行 | ❌ 未开始 |

**Protocol：** [docs/04_BLUEPRINT/protocol/AI_FACTORY_OS_PILOT_OBSERVATION_PROTOCOL.md](../../04_BLUEPRINT/protocol/AI_FACTORY_OS_PILOT_OBSERVATION_PROTOCOL.md)

**明确：** Observation Protocol Design ≠ Observation Started；Protocol Completed ≠ Market Validation。

---

# System Governance Layer（系统治理层）

**Entry 037 — AI_FACTORY_OS System Governance Layer v1**

**Purpose:** Maintain consistency between:

- Runtime
- Database
- Commercial Assets
- Documentation
- Memory

| 项 | 状态 |
|----|------|
| **Status** | Blueprint Completed |
| **Implementation** | Not Started |
| **Protocol** | [docs/99_ARCHIVE/AI_FACTORY_OS_SYSTEM_GOVERNANCE_PROTOCOL.md](../../99_ARCHIVE/AI_FACTORY_OS_SYSTEM_GOVERNANCE_PROTOCOL.md) |

**Scope:** Source of Truth、Entry Completion Governance、ZIP Audit Protocol、Module Boundary Protection。

**原则：** System Growth must not exceed Governance Capacity；Governance Before Expansion。

---

# Architecture Convergence（架构收敛）

**Entry 038-B — AI_FACTORY_OS Architecture Convergence Plan v1**

| 项 | 状态 |
|----|------|
| **Status** | Blueprint / Governance Completed |
| **Runtime Integration** | Not Started |
| **Unified Architecture** | [docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md](../../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) |
| **Full System Audit** | Entry 038-A — [docs/07_AUDIT/](../../07_AUDIT/) |
| **DB Alignment Report** | [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_ALIGNMENT_REPORT.md](../../07_AUDIT/database/AI_FACTORY_OS_DATABASE_ALIGNMENT_REPORT.md) |
| **Commercial State Report** | [docs/07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_ALIGNMENT_REPORT.md](../../07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_ALIGNMENT_REPORT.md) |
| **Validation Gate Plan** | [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_VALIDATION_GATE_INTEGRATION_PLAN.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_VALIDATION_GATE_INTEGRATION_PLAN.md) |
| **Broken Entry Report** | [docs/07_AUDIT/runtime/AI_FACTORY_OS_BROKEN_ENTRY_REPORT.md](../../07_AUDIT/runtime/AI_FACTORY_OS_BROKEN_ENTRY_REPORT.md) |

**模块状态校正：**

| 模块 | Status |
|------|--------|
| 2_COGNITION | Planned — Not Implemented |
| 4_PRODUCT | Planned — Not Implemented |
| 5_CONTENT | Planned — Not Implemented |
| 11_CONTENT_FACTORY | Active — Isolated（Execution Layer） |

**Pilot 可追溯：** preq_20260712_005 → Product Asset 8523329941d4 — **未修改**

**明确：** Documentation Update ≠ Runtime Integration；Design ≠ Production。

---

# Database Governance / State Authority（数据治理）

**Entry 039-A — Database Alignment & State Authority Design v1**

| 项 | 状态 |
|----|------|
| **Database Governance** | Blueprint Completed |
| **Implementation** | Not Started |
| **Inventory** | [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_INVENTORY_REPORT.md](../../07_AUDIT/database/AI_FACTORY_OS_DATABASE_INVENTORY_REPORT.md) |
| **Schema Drift** | [docs/07_AUDIT/database/AI_FACTORY_OS_SCHEMA_DRIFT_REPORT.md](../../07_AUDIT/database/AI_FACTORY_OS_SCHEMA_DRIFT_REPORT.md) |
| **Data Ownership** | [docs/02_ARCHITECTURE/AI_FACTORY_OS_DATA_OWNERSHIP_MODEL.md](../../02_ARCHITECTURE/AI_FACTORY_OS_DATA_OWNERSHIP_MODEL.md) |
| **JSON↔DB Boundary** | [docs/07_AUDIT/database/AI_FACTORY_OS_JSON_DATABASE_BOUNDARY_REPORT.md](../../07_AUDIT/database/AI_FACTORY_OS_JSON_DATABASE_BOUNDARY_REPORT.md) |
| **State Authority** | [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_STATE_AUTHORITY_PROTOCOL.md](../../04_BLUEPRINT/policy/AI_FACTORY_OS_STATE_AUTHORITY_PROTOCOL.md) |
| **Evolution Plan** | [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EVOLUTION_PLAN.md](../../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EVOLUTION_PLAN.md) |

**DB Reality（039-A 实测）：** `ai_factory.db` ~80KB；7 用户表；Commercial Objects **不在** SQLite。

**原则：** Database Reality ≠ Documentation Reality；JSON Asset ≠ Database Record；Design Schema ≠ Runtime Schema。

---

# Commercial Lifecycle Governance（商业生命周期治理）

**Entry 039-B — Commercial Lifecycle State Authority Design v1**

| 项 | 状态 |
|----|------|
| **Commercial Lifecycle Governance** | Blueprint Completed |
| **Implementation** | Not Started |
| **Inventory** | [docs/07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_OBJECT_INVENTORY.md](../../07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_OBJECT_INVENTORY.md) |
| **State Machine** | [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_LIFECYCLE_STATE_MACHINE.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_LIFECYCLE_STATE_MACHINE.md) |
| **Authority Model** | [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_COMMERCIAL_STATE_AUTHORITY_MODEL.md](../../04_BLUEPRINT/policy/AI_FACTORY_OS_COMMERCIAL_STATE_AUTHORITY_MODEL.md) |
| **Conflict Report** | [docs/07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_CONFLICT_REPORT.md](../../07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_CONFLICT_REPORT.md) — 8 actionable |
| **Human Assisted Boundary** | [docs/04_BLUEPRINT/protocol/AI_FACTORY_OS_HUMAN_ASSISTED_BOUNDARY_PROTOCOL.md](../../04_BLUEPRINT/protocol/AI_FACTORY_OS_HUMAN_ASSISTED_BOUNDARY_PROTOCOL.md) |

**历史 Reality：** Experiment/PR 多为 `draft`；Approval=`approved`；Product Asset `8523329941d4` completed/passed；Feedback/Evaluation pending。

**明确：** Historical Reality ≠ Target Lifecycle Design；JSON Sync Not Started。

---

# Commercial Field Normalization（商业字段规范化）

**Entry 039-C — Commercial Lifecycle Field Normalization Design v1**

| 项 | 状态 |
|----|------|
| **Commercial Field Normalization** | Blueprint Completed |
| **Implementation** | Not Started |
| **Inventory** | [docs/07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_CURRENT_INVENTORY.md](../../07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_CURRENT_INVENTORY.md) |
| **Standard** | [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_STANDARD.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_STANDARD.md) |
| **Mapping** | [docs/07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_MAPPING_MODEL.md](../../07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_MAPPING_MODEL.md) |
| **Compatibility** | [docs/07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_COMPATIBILITY_REPORT.md](../../07_AUDIT/commercial/AI_FACTORY_OS_COMMERCIAL_FIELD_COMPATIBILITY_REPORT.md) |
| **Transition Authority** | [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_STATE_TRANSITION_AUTHORITY_MATRIX.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_STATE_TRANSITION_AUTHORITY_MATRIX.md) |

**标准维：** lifecycle_status · execution_status · validation_status · release_status · evaluation_status · collection_status

**Reality：** Product Asset 有 generation_status + validation_status；**无**统一 release_status；Opportunity.status=`human_assisted` 为方法语义。

**明确：** Field Normalization ≠ JSON Migration。

---

# Commercial State Migration Strategy（商业状态迁移策略）

**Entry 039-D — Commercial State Migration Strategy v1**

| 项 | 状态 |
|----|------|
| **Migration Strategy** | Completed |
| **Implementation** | Not Started |
| **Historical Snapshot** | [docs/06_HISTORY/AI_FACTORY_OS_COMMERCIAL_STATE_HISTORICAL_SNAPSHOT.md](../../06_HISTORY/AI_FACTORY_OS_COMMERCIAL_STATE_HISTORICAL_SNAPSHOT.md) |
| **Migration Matrix** | [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_MIGRATION_MATRIX.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_STATE_MIGRATION_MATRIX.md) |
| **Pilot Analysis** | [docs/07_AUDIT/commercial/AI_FACTORY_OS_PILOT_STATE_MIGRATION_ANALYSIS.md](../../07_AUDIT/commercial/AI_FACTORY_OS_PILOT_STATE_MIGRATION_ANALYSIS.md) |
| **Permission Policy** | [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_STATE_MIGRATION_PERMISSION_POLICY.md](../../04_BLUEPRINT/policy/AI_FACTORY_OS_STATE_MIGRATION_PERMISSION_POLICY.md) |
| **Rollback Plan** | [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_STATE_MIGRATION_ROLLBACK_PLAN.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_STATE_MIGRATION_ROLLBACK_PLAN.md) |
| **Risk Report** | [docs/07_AUDIT/migration/AI_FACTORY_OS_STATE_MIGRATION_RISK_REPORT.md](../../07_AUDIT/migration/AI_FACTORY_OS_STATE_MIGRATION_RISK_REPORT.md) |

**Pilot 建议（未执行）：** exp_005→`running`；preq_005→`completed` + execution `succeeded`；PA→validated / unreleased。

**明确：** Strategy Completed ≠ Migration Executed；JSON 状态未改。

---

# Collaboration Control Architecture（协作控制架构）

**Core Governance Set v1（Entry 040-D1）**

```
CONTROL_CENTER (single entry + Core Governance Navigation)
  ├── PROJECT_CONSTITUTION
  ├── BUSINESS_STRATEGY                 ← 040-D1
  ├── CURRENT_STATE
  ├── DECISION_LOG（含 DEC-005..010）     ← 040-D1
  ├── EXECUTION_PROTOCOL
  │     ├── Human Readability Rule（040-A）
  │     └── AI Self Review Gate（040-A）
  ├── KNOWLEDGE_UPDATE_PROTOCOL         ← 040-D1
  ├── UNIFIED_ARCHITECTURE
  └── AUTHORITY_MODEL（强制卫星）
        └── Reference Layer（历史/蓝图/audit — 不删除）
```

| 项 | 状态 |
|----|------|
| **Core Governance Set v1** | Foundation Implemented（040-D1） |
| **Session Bootstrap Protocol** | ✅ Entry 040-A |
| **Human Readability Rule** | ✅ Entry 040-A |
| **AI Self Review Gate** | ✅ Entry 040-A |
| **Business Strategy file** | ✅ Entry 040-D1 |
| **Knowledge Update Protocol file** | ✅ Entry 040-D1 |
| **Runtime / commercial progress beyond docs** | Not claimed |
| **Validation** | [docs/07_AUDIT/validation/AI_FACTORY_OS_CORE_GOVERNANCE_FOUNDATION_VALIDATION_REPORT.md](../../99_ARCHIVE/audit_history/AI_FACTORY_OS_CORE_GOVERNANCE_FOUNDATION_VALIDATION_REPORT.md) |

**原则：** Reality > Documentation > Conversation；Required Reading 最小化；新会话必须先 Bootstrap + 核心导航。

---

**Rule：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_DATASET_GENERATION_RULE.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_DATASET_GENERATION_RULE.md)

定义 Candidate 数据**如何产生** — Data Sources、Quality Rules、Readiness Score、Creation Template、Human Assisted SOP。

| 能力 | 状态 |
|------|------|
| Dataset Generation Rule v1 | ✅ Blueprint Completed |
| Candidate 数据实例 | ✅ 5 条 — opportunity_candidates_v1.json |
| Human Assisted SOP | ✅ 文档定义 |
| Agent 自动生成 | ❌ Pending |

## 完整商业验证栈层级（更新）

```
Commercial Validation Layer（MVP）
        ↓
Opportunity Candidate Asset Layer（Candidate Pool — Registry）
        ↓
Opportunity Dataset Generation Layer（Generation Rule — 本次）
        ↓
Commercial Experiment Layer（System）
        ↓
Commercial Experiment Asset Layer（Experiment Registry）
        ↓
Commercial Experiment Selection Layer（Selection Framework）
        ↓
Runtime Modules
```

---

# Experiment Review Layer（实验审核层）

**Protocol：** [docs/04_BLUEPRINT/protocol/AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md](../../04_BLUEPRINT/protocol/AI_FACTORY_OS_EXPERIMENT_PREPARED_REVIEW_PROTOCOL.md)

Experiment Prepared Review Layer（实验准备审核层）在 **Experiment Object** 与 **Production Request** 之间建立人工审核门槛 — docs 认知协议层，**不参与运行**。

## 三层职责

| 层 | 职责 |
|----|------|
| Experiment Object | 商业实验设计 |
| Prepared Review | 生产前审核 — 五维确认 + 四层 Checklist |
| Production Request | 生产规格生成 |

## 当前状态

| 能力 | 状态 |
|------|------|
| Experiment Prepared Review Protocol v1 | ✅ Blueprint Completed |
| 四层 Checklist（Business/Product/Validation/Commercial） | ✅ 文档定义 |
| Experiment Review Object Schema v1 | ✅ 文档定义 |
| Review 生命周期（5 状态） | ✅ 文档定义 |
| 未来 DB `experiment_reviews` | ⏳ Blueprint — 未 CREATE TABLE |
| Review JSON 实例 | ✅ 4 条 — experiment_reviews_v1.json |
| 4 条 Experiment prepared 审核 | ✅ 已执行 — prepared 3 / rejected 1 |
| experiments_v1 写回 | ❌ 未修改 — 独立实体设计 |

**门禁：** prepared ≠ production；review approved ≠ Content Factory execution；Human Assisted ≠ Automation。

---

# Production Request Layer（生产请求协议层）

**Contract：** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md)

Production Request Layer（生产请求协议层）定义 **Experiment Object** 与 **Content Factory Runtime** 之间的标准生产请求协议 — docs 认知契约层，**不参与运行**。

## 三层职责

| 层 | Object | 职责 |
|----|--------|------|
| 商业验证 | Experiment Object | 商业验证目标 — hypothesis、success_metrics |
| 生产转换 | Production Request Object | 具体生产要求 — asset/quality requirements |
| 生产交付 | Generated Product Object | 实际生产资产 — artifact_path |

## 当前状态

| 能力 | 状态 |
|------|------|
| Production Request Contract v1 | ✅ Blueprint Completed |
| 生命周期设计（6 状态） | ✅ 文档定义 |
| 模块权限边界 | ✅ 3_DECISION 生成 / 11_CONTENT_FACTORY 只读执行 |
| 未来 DB `production_requests` | ⏳ Blueprint — 未 CREATE TABLE |
| Production Request JSON 实例 | ✅ 3 条 — production_requests_v1.json |
| Content Factory 唯一入口接入 | ❌ Runtime 未连接 |

**门禁：** 禁止 Experiment Object 直接调用 Content Factory；禁止 Content Factory 自行选品。

**明确：** Blueprint ≠ Implementation；Document Completed ≠ Runtime Connected。

---

# Commercial Experiment Selection Layer（商业实验选择层）

**Framework：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md](../../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md)

Experiment Selection Layer（实验选择层）连接 **Market Intelligence（市场智能）** → **Opportunity Object** → **Experiment Object** — docs 认知规则层，**不参与运行**。

## 商业智能链（Commercial Intelligence Chain）

```
1_DATA / 2_COGNITION
        ↓
Market Intelligence（市场智能）
        ↓
Opportunity Candidate Pool（商业机会候选 — Candidate Registry）
        ↓
Opportunity Object（商业机会对象）
        ↓
Experiment Selection Layer（实验选择层 — Selection Framework）
        ↓
Experiment Object（实验对象 — Object Registry）
        ↓
Experiment Prepared Review Layer（实验准备审核 — Prepared Review Protocol）
        ↓
Production Request Layer（生产请求协议 — Production Request Contract）
        ↓
3_DECISION → 11_CONTENT_FACTORY → Product Asset → Feedback
        ↓
Failure Learning → 回流 Candidate / Selection / Cognition
```

## 当前状态

| 能力 | 状态 |
|------|------|
| Selection Framework v1 | ✅ Blueprint Completed |
| Experiment Priority Score 公式 | ✅ 文档定义（与 Opportunity Score 隔离） |
| Category A/B/C 选择规则 | ✅ 文档定义 |
| 自动选择代码 | ❌ 未建 |
| 2_COGNITION Opportunity 产出 | ❌ 未建 |
| Experiment 实例 | ❌ 0 / 30 |

## 完整商业验证栈层级

```
Commercial Validation Layer（MVP Blueprint）
        ↓
Commercial Experiment Layer（System Blueprint）
        ↓
Commercial Experiment Asset Layer（Object Registry）
        ↓
Commercial Experiment Selection Layer（Selection Framework — 本次）
        ↓
Runtime Modules（1_DATA / 2_COGNITION / 3_DECISION / 11_CONTENT_FACTORY）
```

---

# Future Architecture Flow

目标架构（`2_COGNITION` Blueprint 已完成，待实现）：

```
1_DATA
        ↓
2_COGNITION
        ↓
3_DECISION
        ↓
11_CONTENT_FACTORY
        ↓
10_DEPLOY
        ↓
Feedback
        ↓
7_MEMORY
```

**Blueprint：** [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md)

**与 Current Data Flow Reality 的区别：** 未来链路在 `1_DATA` 与 `3_DECISION` 之间插入 `2_COGNITION`（Market Intelligence Layer）。

---

# Business Data Loop

商业数据资产闭环（Database Schema Blueprint v1）：

```
Market Data
        ↓
Database Asset（data/ai_factory.db）
        ↓
Cognition（2_COGNITION）
        ↓
Decision（3_DECISION）
        ↓
Production（11_CONTENT_FACTORY）
        ↓
Feedback（product_feedback）
        ↓
Database（数据沉淀）
        ↓
Memory（7_MEMORY — 单向同步）
```

**Schema Blueprint：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md)

**说明：** Database 为跨层商业资产；`7_MEMORY` 为 OS 运行记忆，二者物理隔离。

---

# Database Current Reality

**审计报告：** [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md](../../07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md)

| 项 | 现状 |
|----|------|
| **文件** | `data/ai_factory.db`（SQLite 3.45.1，~80 KB） |
| **用户表** | 7 张：`platforms`, `keywords`, `products`, `collection_log`, `scores`, `trends`, `audit_log` |
| **活跃使用** | `1_DATA`（采集）、`3_DECISION`（ScoringAgent 写 scores） |
| **未使用 DB** | `11_CONTENT_FACTORY`、`7_MEMORY`、`2_COGNITION` |
| **用途判断** | **混合数据库**（采集 + 商品评分 + 部分测试/遗留） |
| **Blueprint 对齐** | 7 张目标表均为 Missing 或 Partial；`opportunity_scores` 尚未存在 |
| **下一阶段** | Database Extension（Phase 2，须审批） |

---

# Data Contract Architecture

模块间数据交换**必须**经 Database Contract 或 OS 标准 JSON，禁止跨模块直读内部文件。

```
External Data
    → [Contract I1] 1_DATA → DB (Raw)
    → [Contract I2] DB → 2_COGNITION → opportunity_scores
    → [Contract I3] 2_COGNITION → 3_DECISION (Opportunity Object)
    → [OS Schedule] 3_DECISION → 11_CONTENT_FACTORY
    → [Contract I4] 11_CONTENT_FACTORY → generated_products
    → [Contract I5] Feedback → product_feedback → Cognition/Decision
```

**Integration Design：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](../../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md)

**Legacy 兼容：** `platforms` / `keywords` / `products` / `scores` / `collection_log` 保留，Additive 接入 Blueprint 表。

---

# Database Evolution Path

```
Current SQLite（Legacy Active Capability）
    platforms / keywords / products / scores / collection_log ...
        ↓
Extended Intelligence Schema（Additive — market_* + opportunity_scores）
        ↓
Market Intelligence Database（generated_products + product_feedback + 完整闭环）
```

**Migration Plan：** [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md](../../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md)

**策略：** Additive Evolution — 保留 Legacy 表，新增 Intelligence 表，禁止破坏 617 行历史数据。

---

# Database Evolution Status

| 维度 | 状态 |
|------|------|
| **Current** | Legacy SQLite Database（`platforms` / `keywords` / `products` / `scores` / `collection_log`） |
| **Target** | Market Intelligence Database（+ market_* / opportunity_scores / generated_products / product_feedback） |
| **演化方式** | **Additive Evolution** |
| **Implementation Plan** | ✅ Completed — [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md](../../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md) |
| **Implementation Execution** | ⏳ Pending |

---

## 5. 当前阶段

**Commercial Validation Preparation（商业验证准备阶段）**

- 四层核心架构已稳定（冻结）
- Content Factory 已建设（真实数字商品生产）
- Commercial MVP Blueprint v1 设计完成
- Commercial Experiment System Blueprint v1 设计完成
- Experiment Object Registry v1 登记规范完成
- Commercial Experiment Selection Framework v1 选择规则完成
- Opportunity Candidate Registry v1 候选资产池登记完成
- Opportunity Dataset Generation Rule v1 数据生成规范完成
- Opportunity Candidate Dataset v1 首批 5 条 Category A 实例创建
- Data Intelligence Layer 设计规划完成（未建代码）
- Content Factory Monetization 商业闭环设计完成
- 下一阶段：Commercial MVP Execution（30 产品实验）

---

## 6. 核心保护（禁止修改）

以下模块为系统核心，任何升级不得破坏：

| 模块 | 路径 |
|------|------|
| Controller | `0_START/controller.py` |
| Planner | `0_START/planner.py` |
| PolicyEngine | `0_START/policy_engine.py` |
| ExecutionRuntime | `0_START/execution_runtime.py` |
| DAG 执行结构 | 标准 `{nodes, edges}` 协议 |
| Agent 接口 | `BaseAgent.execute(input_data, context)` |
| API 接口 | `10_DEPLOY` 统一协议 |

---

## 7. 快速恢复检查清单

```powershell
# 1. 验证 CLI 入口
python 0_START/main.py

# 2. 验证 API 入口
cd 10_DEPLOY
python api.py

# 3. 检查 Memory 写入
#    7_MEMORY/event_log.jsonl 应有新事件
#    logs/execution_hash.log 应有新 hash

# 4. 检查 docs 认知层（建议先读 PROJECT_INTELLIGENCE_BLUEPRINT）
#    docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md
#    docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md
#    docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md
```

---

## 8. 目录边界总览

```
AI_FACTORY_OS/
├── docs/                  ← 系统认知层 + Project Context Layer
│   ├── AI_FACTORY_OS_WORK_PRINCIPLES.md
│   ├── AI_FACTORY_OS_BUSINESS_PLAN.md
│   ├── system_snapshot.md
│   ├── PROJECT_STATUS.md
│   ├── AI_FACTORY_OS_CONTENT_FACTORY_BLUEPRINT.md
│   ├── AI_FACTORY_OS_DATA_INTELLIGENCE_BLUEPRINT.md
│   ├── AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md
│   ├── AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md
│   ├── AI_FACTORY_OS_MODULE_REGISTRY.md
│   └── CURSOR_EXECUTION_HISTORY.md
├── commercial_assets/       ← 商业智能资产实例层（2026-07-08 创建）
│   ├── opportunity_candidates/
│   │   └── opportunity_candidates_v1.json
│   ├── opportunities/
│   │   └── opportunities_v1.json
│   ├── experiment_selection/
│   │   └── experiment_selection_records_v1.json
│   ├── experiments/
│   │   └── experiments_v1.json
│   ├── experiment_reviews/
│   │   └── experiment_reviews_v1.json
│   ├── production_requests/
│   │   └── production_requests_v1.json
│   └── production_request_reviews/
│       └── production_request_reviews_v1.json
├── 7_MEMORY/              ← 运行记忆层（event / pattern / strategy / policy）
│   ├── event_log.jsonl
│   ├── pattern_memory.json
│   ├── strategy_memory.json
│   ├── runtime_policy.json
│   └── PROJECT_CORE_MEMORY.md
├── 11_CONTENT_FACTORY/    ← 业务生产层（已建设）
├── 0_START/               ← 核心 OS（禁止修改）
├── 10_DEPLOY/             ← HTTP 部署层
└── 8_CONFIG/              ← 配置
```
