# AI_FACTORY_OS Unified Architecture Definition v1

> Entry 038-B — Architecture Convergence Plan  
> Last updated: 2026-08-30（Entry **063**）

| Document Role | Architecture Reference — **架构设计唯一文档归属**（DEC-016） |
|---------------|------------------------|
| Reality Status | Design Reference（目标/分层原则）— **不是**已部署统一 Runtime；**不是** Current State |
| Runtime Status | Requires Reality Validation — see CURRENT_STATE / MODULE_REGISTRY / Entry 041-A |

**状态标签：** Blueprint Completed · Runtime Integration **Not Started** · Dual Track **Confirmed（Case B）**

**原则：** Architecture Alignment ≠ Full Refactor · Documentation Update ≠ Runtime Integration · Design ≠ Production · Blueprint ≠ Production  
**DEC-013：** Unified governance ≠ Forced merge · Modular ≠ Fragmented  
**DEC-014：** Capability Composition — Folder ≠ commercial boundary · Product = Capability Composition · Unified ≠ Forced Merge Runtime  
**DEC-016：** 模块 Status → MODULE_REGISTRY；事实投影 → CURRENT_STATE；历史原因 → Evolution Context（勿在本文件重复定义）  
**DEC-018：** Folder Structure ≠ Capability Architecture ≠ Product Architecture

**依据：** Entry 038-A；041-A；041-D；041-D-A；041-B-B；041-H  
**历史解释（非本文件权威）：** [ARCHITECTURE_EVOLUTION_CONTEXT_RECORD](../06_HISTORY/AI_FACTORY_OS_ARCHITECTURE_EVOLUTION_CONTEXT_RECORD.md)

---

## Runtime Reality Snapshot（当前真实 — 非目标）

```
Track A — Core OS Runtime
  0_START / 10_DEPLOY → 1_DATA → 3_DECISION → 6_EXECUTION → 7_MEMORY
  （Governance + Operational Runtime）

Track B — Content Factory / Commercial Capability
  adapter_runner → 11_CONTENT_FACTORY + commercial_assets
  （Reusable Commercial Capability；Independent Runtime Track）

Runtime Integration: Not Started
性质: Intentional Isolation + Unfinished Convergence
Future Direction: Composable Capability（不强制立即融合）
```

禁止把下文「统一分层模型」读成「已融合生产」或「已经融合」。

---

## Architecture Lexicon（目录 / 模块 / 产品 — 041-D-A）

| 原则 | 含义 |
|------|------|
| **目录 ≠ 模块** | 磁盘目录是组织载体；能力模块是可治理的能力边界，不必 1:1 |
| **模块 ≠ 产品** | 模块是可复用能力；商业产品是包装与交付结果 |
| **能力可跨目录实现** | 同一能力可分布在多个目录/服务中 |
| **多模块 → 解决方案 → 商业产品** | Capability Composition：组合形成方案，再包装成产品 |

```
Capability Modules  →  Solution  →  Commercial Product
```

**Core OS 与 Content Factory：** 当前保持**模块化隔离**（Independent Runtime Tracks）。  
**未来是否 Runtime 桥接：** 须独立 Decision（如建议 Entry 041-G / DEC Candidate）— **本文件禁止写成已融合。**

---

## Capability Composition Note（认知说明 — 非 DEC）

**Module is reusable capability, not necessarily final product.**

```
Multiple capabilities → Solution → Commercial Product
```

**Module ≠ Product。** 本说明不单独构成新 DEC（原则锚定 DEC-013 / DEC-014）。

---

## Capability Composition Architecture Principle

> Entry **041-B-B** / **DEC-014**。  
> **Architecture Principle Only** — 不修改 Runtime 架构；**不声明**下列 Layer 已实现。

### 当前工程组织（Reality）

目录结构 `0`–`11` 属于**工程组织**，不是商业边界，也不是已实现的「产品分层」。

### 未来架构理解（原则层 — Design Reference）

架构理解可划分为：

```
Infrastructure Layer（基础设施）
        ↓
Capability Layer（能力层）
        ↓
Solution Layer（解决方案层）
        ↓
Business Product Layer（商业产品层）
```

| 层 | 含义（原则） | 禁止误读 |
|----|--------------|----------|
| Infrastructure | 工程与运行底座组织 | ≠ 已统一 Runtime |
| Capability | 可独立运行/演进/商业化的能力 | ≠ 某个文件夹 = 能力完成 |
| Solution | 多 Capability 组合 | ≠ 已交付企业方案 |
| Business Product | 包装后的可售产品 | ≠ 已验证收入 / Production Complete |

**必须标注：** Architecture Principle Only · Blueprint ≠ Production · Design ≠ Runtime。  
**Runtime Reality：** Core OS 与 Content Factory 仍双轨；Integration **Not Started**。禁止写成「已经融合」。

### 统一治理下的能力组合系统（041-E）

AI_FACTORY_OS 未来**不是**：

- 一个巨大不可拆分系统；
- 多个互相无关项目。

而是：

**统一治理下的能力组合系统。**

```
基础能力
    ↓
能力组合
    ↓
解决方案
    ↓
商业产品
```

**Architecture Principle Only** — 不表示上述链路已在 Runtime 打通。  
文档角色分层见 [DOCUMENTATION_ARCHITECTURE_GOVERNANCE_STRATEGY](../99_ARCHIVE/audit_history/AI_FACTORY_OS_DOCUMENTATION_ARCHITECTURE_GOVERNANCE_STRATEGY.md)（DEC-015）。

---

## Capability Architecture Model

> Entry **041-H** / **DEC-018**。  
> **Architecture Principle Only** — 不修改 Runtime；**不声明**已实现。

AI_FACTORY_OS 采用：

- **统一治理**
- **能力组合**
- **解决方案生成**

模型：

```
Infrastructure Capability（基础设施能力）
        ↓
Reusable Capability（可复用能力）
        ↓
Solution Composition（解决方案组合）
        ↓
Commercial Product（商业产品）
```

**说明：**

- 能力可以**跨目录**组合。
- **目录不是商业边界。**
- Folder Structure ≠ Capability Architecture ≠ Product Architecture。

**禁止：** 按 `0`–`11` 文件夹名拆分商业方案；须参考 Capability Composition Principle（DEC-014）。

---

## Modular Capability Architecture

> Entry **041-B-A**。长期产品方向：**模块化 AI 商业操作系统**。  
> 本条更新**目标架构原则**；**不改变** Current Reality（双轨 Runtime 仍成立）；**不执行** Runtime 融合。

### 目标架构层级

```
Governance Layer（统一治理）
        ↓
Orchestration Layer（编排 / 契约组合）
        ↓
Independent Capability Modules（独立能力模块）
```

### 模块包括但不限于

* Data Intelligence Module
* Content Factory Module
* Decision Module
* Execution Module
* Memory/Learning Module

### 模块协作方式

模块之间通过以下机制协作（可独立运行，亦可组合）：

* **Data Contract**（数据契约 / 数据边界）
* **Module Contract**（模块接口契约）
* **Authority Rules**（权威与权限规则）

### 原则辨析（必须保留）

| 说法 | 正确理解 | 禁止误解 |
|------|----------|----------|
| **Modular（模块化）** | 独立价值、独立演进、独立商业化可能 | ≠ Fragmented（碎片化、无治理散装） |
| **Unified（统一）** | 统一治理、边界、契约与编排 | ≠ Forced Merge（强制代码融合 / 单一 Runtime） |

**结论：** 独立模块运行与整体协同**同时成立**。CF 保持 Isolated Active **符合**本原则，不自动等于「必须立即 Runtime 合并」。

---

## 1. 架构收敛目标

AI_FACTORY_OS 当前存在 **Core OS 链** 与 **Content Factory + Commercial Assets 链** 双轨并行。本定义描述 **统一目标架构（治理与契约层统一）**，指导后续 Entry 逐步收敛，**不要求**把所有能力强制并入单一 Runtime，**也不要求**消除独立模块。

---

## 2. 统一分层模型（流水线视角；与模块化原则并存）

> **Design Reference only.** 下图为**目标**端到端流水线视角；**当前 Reality 为双轨**（见上文 Runtime Reality Snapshot）。不得读作已连通生产。

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer（1_DATA）                      │
│         外部数据采集 · SQLite Operational Data               │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              Cognition Layer（2_COGNITION）                  │
│    市场理解 · 趋势 · 机会发现 · 认知评分输入                  │
│              【Planned — Not Implemented】                    │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              Decision Layer（3_DECISION）                      │
│    评分 · 风险 · 生产/发布决策（OS + Commercial 决策语义）    │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│         Execution Runtime（0_START + 6_EXECUTION）           │
│    Planner · PolicyEngine · ExecutionRuntime · DAG 编排      │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│      Content Factory（11_CONTENT_FACTORY）                   │
│    数字商品生产 · Artifact · 包装 · 质量 · 发布辅助           │
│    ★ Reusable Commercial Capability（目标可组合；现为 Track B）★ │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│         Commercial Asset Layer（commercial_assets/）         │
│  Opportunity → Experiment → PR → Approval → Product Asset    │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│              Feedback（commercial_assets/feedback）          │
│    市场观察 · 指标 · 人工 assisted 反馈                        │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│         Memory Learning（7_MEMORY + Evaluation）             │
│    OS pattern/strategy · 实验评估 · 策略演化                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 11_CONTENT_FACTORY 定位

### 3.1 架构归属

| 项 | 定义 |
|----|------|
| **层级（目标）** | Execution / Commercial Capability 可组合模块 |
| **当前 Reality** | Independent Runtime Track（Isolated Active） |
| **角色** | Reusable Commercial Capability — 数字商品生产 |
| **不是** | 失败复制项目；Commercial Object SoT；必须立即并入单一 Runtime 的废件 |
| **目录** | `11_CONTENT_FACTORY/` — 实现载体 |
| **编排入口（当前）** | Adapter CLI、`ContentPipeline` — **未**纳入 `0_START` DAG |

---

### 3.2 与 Core OS 关系（目标 vs 现状）

| 维度 | 目标架构（Design） | 当前现实（041-A / 041-D） |
|------|---------------------|--------------------------|
| 调度 | Orchestration 可选调用 CF | ❌ 无 import 连接；**Not Started** |
| 输入 | Decision / commercial_assets PR | Adapter 读 JSON（Track B） |
| 输出 | Product Asset → Validation → assets | 人辅登记 / Adapter 草案 |
| Legacy `run(keyword)` | 开发/测试路径 | ✅ 独立 CLI，保持 |

**禁止：**「CF 必须立即融合」「已统一 Runtime」「失败的第二条产品线」。  
**允许：** 独立运行 + 未来可组合（DEC-013）。

### 3.3 明确边界

- **CF 负责：** 产品文件生成、artifact、quality scoring（生产域）、packaging、release gate
- **CF 不负责：** Opportunity 发现、Experiment 设计、Approval 决策、Feedback 采集、Commercial Object 持久化（SoT = commercial_assets）
- **CF MarketAgent（Legacy）：** 临时 keyword 启发式 — 未来应迁移至 2_COGNITION 或显式标注为 Legacy stub

---

## 4. 模块映射表

| 统一层 | 目录模块 | 当前状态 |
|--------|----------|----------|
| Data Layer | `1_DATA` | Active |
| Cognition Layer | `2_COGNITION` | Planned — Not Implemented |
| Decision Layer | `3_DECISION` | Active（OS 域） |
| Execution Runtime | `0_START`, `6_EXECUTION` | Active |
| Content Factory | `11_CONTENT_FACTORY` | Active（Isolated） |
| Commercial Asset Layer | `commercial_assets/` | JSON SoT — human_assisted |
| Feedback | `commercial_assets/feedback/` | Instance Created — pending |
| Memory Learning | `7_MEMORY`, `commercial_assets/experiment_evaluations/` | Active / pending |
| Configuration | `8_CONFIG` | Active |
| Deployment | `10_DEPLOY` | **Active — HTTP Runtime Entry**（非 Production Ready；041-D 校正） |
| Product Definition（规划） | `4_PRODUCT` | Planned — Not Implemented |
| Content Knowledge（规划） | `5_CONTENT` | Planned — Not Implemented |
| Legacy SaaS stub | `9_PRODUCT` | Frozen — Broken entry |

---

## 5. 双轨收敛路径（设计 — 非本 Entry 实施）

### Phase A — 治理对齐（038-B 范围）

- 统一架构文档 ✅
- 模块状态校正 ✅
- DB / Commercial 状态对齐报告 ✅
- Validation Gate 接入计划 ✅
- Broken Entry 评估 ✅

### Phase B — 状态同步（未来 Entry）

- commercial_assets JSON status 字段与下游一致
- database.py 与 ai_factory.db schema 对齐
- MODULE_REGISTRY / PROJECT_STATUS 持续同步

### Phase C — Runtime 融合（未来 Entry，须单独授权）

- Execution Runtime 注册 CF Adapter 为可选 DAG node
- ProductAssetValidator 接入 Adapter 链
- 2_COGNITION 实现，接管 CF MarketAgent 职责
- **禁止** 破坏 Legacy `run(keyword)` 与 Pilot `preq_20260712_005` 可追溯性

---

## 6. Pilot 可追溯性约束

以下对象在架构收敛过程中 **必须保持 ID 与文件可追踪**：

| 对象 | ID | 路径 |
|------|-----|------|
| Production Request | `preq_20260712_005` | `commercial_assets/production_requests/` |
| Approval | `appr_20260713_005` | `commercial_assets/production_request_reviews/` |
| Product Asset | `8523329941d4` | `commercial_assets/product_assets/product_assets_v1.json` |
| CF Artifacts | `8523329941d4` | `11_CONTENT_FACTORY/artifacts/products/8523329941d4/` |
| Validation | `pval_20260713_ac223d` | `commercial_assets/product_asset_validations/` |
| Feedback | `fbk_20260713_001` | `commercial_assets/feedback/feedback_v1.json` |
| Evaluation | `eval_20260713_001` | `commercial_assets/experiment_evaluations/` |

---

## 7. Source of Truth（与 Governance Protocol 一致）

| 域 | SoT |
|----|-----|
| Runtime Behavior | Python 代码 |
| Operational Data | `data/ai_factory.db`（**Current SoT** · Entry 058A clean） |
| Legacy DB Archive | `99_ARCHIVE/database_history/`（not_current_sot） |
| Commercial Object | `commercial_assets/` |
| Learning Knowledge | `7_MEMORY/` |
| System Description | `docs/` |
| **目标架构** | **本文档 + MODULE_REGISTRY** |

---

## 7.1 Data Ownership Boundary Summary（数据与认知所有权边界摘要）

> Entry **040-D2-B** 增补。**不改变**上文架构设计与分层，仅澄清「谁拥有哪类唯一职责」。

| 对象 | 唯一职责（Unique Responsibility） | 不是什么 |
|------|----------------------------------|----------|
| **Business Strategy**（`AI_FACTORY_OS_BUSINESS_STRATEGY.md`） | 当前有效**商业方向、价值路径、盈利优先级、人辅商业边界**的文档入口 | 不是 Runtime；不是 JSON/DB 状态；不是 Entry 流水账 |
| **Current State**（`AI_FACTORY_OS_CURRENT_STATE.md`） | 面向会话的**事实摘要投影**（完成/阻塞/已知问题）；须可追溯到 Reality | 不是愿景书；不能覆盖 Code/DB/Assets 现实 |
| **Decision Log**（`AI_FACTORY_OS_DECISION_LOG.md`） | **正式战略决策与否决记录**（含不可重复错误裁决） | 不是日常 commit 日志；不是商业资产 SoT |
| **Runtime**（可调用的 Python / 服务入口） | **实际行为**：被调用时真正执行什么 | 不是文档声明的「应当」；文档不能改 Runtime 除非改代码 |
| **Database**（`data/ai_factory.db` + `database.py` 相关） | **Operational Data（运行/市场操作数据）** 的权威存储 | 不是 Commercial Object 生命周期 SoT；不是 Memory 学习结论的唯一源 |
| **commercial_assets** | **Commercial Object（商业对象）** JSON SoT：机会/实验/PR/资产/反馈等 | 不是 Core OS SQLite 操作表；写入须授权/人辅规则 |
| **Documentation**（`docs/` 含本架构文） | **系统描述、蓝图、治理与恢复**；解释如何理解系统 | 默认**不是** Reality；目标架构文 ≠ 已融合 Runtime |

**冲突速记：** Reality（Runtime / Code / DB / Assets）> Current State > Decision Log > 其他 Documentation > Conversation Memory（见 AUTHORITY_MODEL）。

---

## 8. 状态声明

| 项 | 状态 |
|----|------|
| Unified Architecture Definition | ✅ Blueprint Completed |
| Runtime Integration | ❌ Not Started |
| Core OS ↔ CF 连接 | ❌ Not Started |
| 2_COGNITION Implementation | ❌ Not Started |

**Blueprint ≠ Runtime。** 本文档完成架构收敛 **设计基础**；任意 Runtime 桥接须后续 Entry 授权。  
**041-B-A：** 目标架构已明确为 Modular Capability Architecture；**Runtime Integration 仍为 Not Started**。  
**041-D：** Documentation Alignment — Runtime Reality Snapshot / Document Role banners 已与 041-A Reality 对齐；**未改 Runtime**。  
**041-D-A：** Architecture Lexicon（目录≠模块≠产品）；Evolution Context 指针；**仍禁止写成已融合**。  
**041-B-B：** Capability Composition Architecture Principle（Architecture Principle Only）；**DEC-014**；Runtime 未改。  
**041-E：** 统一治理下的能力组合系统公式；文档分层策略指针（DEC-015）；**未改 Runtime / 未移文件**。  
**041-H：** Capability Architecture Model；Folder ≠ Capability ≠ Product（DEC-018）；**未改 Runtime**。

---

## 9. Autonomous Commercial Learning Loop（Design Reference · DEC-020）

> Entry **049**。**Architecture Principle / Target Loop** — **Not Implemented as closed Runtime**。

```text
1_DATA / Market Collection
        ↓
Opportunity Discovery（目标；当前人辅 JSON）
        ↓
3_DECISION Scoring / Risk / Rank（Track A 对 listing 有 Reality；商业 Opportunity 未接入）
        ↓
Experiment Selection（当前 human_assisted）
        ↓
11_CONTENT_FACTORY Production
        ↓
Quality / Commercial Heuristics
        ↓
Risk Gate / Approval
        ↓
Publish Queue（当前 MISSING）
        ↓
External Publish（当前人工；NOT STARTED for Pilot）
        ↓
Market Observation / Feedback
        ↓
Evaluation
        ↓
7_MEMORY / Learning（Track A = Execution Learning；Commercial Learning = Guardrail Interface only）
        ↓
Strategy Update → 下一轮 Opportunity
```

| 区分（强制） | 含义 | 代码状态（050） |
|--------------|------|-----------------|
| EXECUTION_OUTCOME | 流水线/本地发布发生了什么（含 `published_local`） | **Implemented** |
| PRODUCTION_OUTCOME | 产品生产是否完成 | Ontology reserved；非商业成功 |
| QUALITY_OUTCOME | 质量是否达标 | Ontology reserved；非商业成功 |
| COMMERCIAL_OUTCOME | 真实商业结果（purchase/revenue/…） | Guardrail **Implemented**；真实事件源 **Not Built** |
| MARKET_OUTCOME | 市场行为（views/clicks/…） | Reserved；须 REAL 或显式 SIMULATION |

**FORMER GAP CLOSED（050 / DEC-021）：** `extract_pattern` 不再把 `published_local` 解释为 Commercial Success。`outcome=success` 仅表示 **Execution Learning**；`commercial_success=False`；`data_origin=SIMULATION`。SelfEvolution 标注 `strategy_domain=EXECUTION`。

**Implemented（050）：** `is_commercial_learning_eligible` / `ingest_commercial_learning_event` — Real Commercial Learning 最低门。  
**Implemented（051 · Partial）：** Market Event ontology + SQLite `market_events` + Observation fact store + route→ingest bridge（`1_DATA/market_event_core.py`）。  
**Implemented（052 · Partial）：** Publish Queue + Human External Action Gate（`6_EXECUTION/publish_queue.py`）；最小 Candidate Selector（`3_DECISION/candidate_selector.py`）。  
**Implemented（053 · Partial）：** Commercial Product / Listing handoff（`6_EXECUTION/commercial_handoff.py`）+ JSON registries。  
**Implemented（054 · Partial）：** Market Signals + Opportunity Discovery + Selection（`market_signal_core` / `opportunity_discovery`）。  
**Proposed / Not Built：** 2_COGNITION · live connectors · auto Experiment/PR · advanced ML scoring · auto external publish（**Forbidden**）。

---

## 9.1 Outcome Ontology & Learning Lanes（Entry 050 · Partially Implemented）

> **Implemented：** 代码层语义与 guardrail。**Not Implemented：** 完整商业事件系统 / DB schema。

```text
learning_lane: EXECUTION | COMMERCIAL | SIMULATION
data_origin:   REAL | SIMULATION | SYNTHETIC | UNKNOWN
pattern_origin: EXECUTION | SIMULATION | REAL_MARKET
```

| Rule | Enforcement |
|------|-------------|
| Execution Success ≠ Commercial Success | `commercial_success` 永不由 `published_local` 单独置 True |
| REAL only → Real Commercial Learning | `data_origin!=REAL` → reject |
| SIMULATION / SYNTHETIC / UNKNOWN | reject from Real Commercial Learning |
| quality / production alone | reject |

---

## 9.2 Market Event → Observation → Learning（Entry 051 · Partially Implemented）

> **Implemented：** 最小事件持久化与回流护栏。**Not Started：** Pilot 真实 Observation（仍 NOT_STARTED）。

```text
Raw Market Event
      ↓ validate / dedupe
Normalized MarketEvent  (SQLite market_events)
      ↓
Observation Record     (facts only · commercial_assets/observations)
      ↓
Evaluation Input        (facts summary · not auto decision)
      ↓
Commercial Learning     (PURCHASE/REVENUE/REFUND + REAL + verified only)
```

| Boundary | Rule |
|----------|------|
| Market Event ≠ Observation Conclusion | 只存事实计数/金额 |
| Observation ≠ Commercial Success | VIEW 可观察，不自动学习成功 |
| verification_status | UNVERIFIED / VERIFIED / MANUAL_VERIFIED |
| Platform expansion | `platform` 文本字段；无平台专用产品表 |
| Product expansion | `product_type` 文本（document/video/…）；不改核心表 |

---

## 9.3 Publish Queue & Human External Action（Entry 052 · Partially Implemented）

> **Implemented：** Queue schema + gates + evidence + Pilot `AWAITING_HUMAN_ACTION`。  
> **Forbidden / Not Built：** Auto external publish · Observation Start · Commercial Success from PUBLISHED。

```text
Production Candidate
      ↓
Quality / Commercial Score / Risk / Package Gate
      ↓
Publish Queue  (platform-agnostic)
      ↓
READY | BLOCKED | AWAITING_HUMAN_ACTION
      ↓ (human only)
Publish Evidence (VERIFIED / MANUAL_VERIFIED)
      ↓
PUBLISHED + observation_eligible
      ↓ (next Entry)
Observation Start
```

| Rule | Enforcement |
|------|-------------|
| Human Gate ≠ Product Approval | System may enqueue; human does external click |
| READY ≠ PUBLISHED | No auto transition |
| PUBLISHED ≠ Commercial Success | Evidence path sets commercial_success=False |
| Observation Eligible ≠ Started | `observation_eligible=1` only; experiment JSON untouched |
| Platform expansion | `platform` text field — no TaobaoPublishQueue table |

---

## 9.4 Product → Commercial Product → Listing（Entry 053 · Partially Implemented）

> **Implemented：** Handoff model + readiness gates + Pilot materialization。  
> **Not：** Published Listing · Observation Started · CF generator refactor。

```text
Product (logical)
  → Product Version
  → Product Asset (files; asset_type)
  → Commercial Product (COMMERCIAL_READY / QUEUED / …)
  → Listing Package (platform presentation)
  → Listing (platform instance)
  → Publish Queue / Human External Action
  → Publish Evidence
  → Published Listing
  → Observation (next Entry)
```

| Separation | Rule |
|------------|------|
| Asset ≠ Commercial Product | Asset-only → NOT READY |
| Commercial Ready ≠ Published | status never auto-PUBLISHED |
| Package ≠ Marketing Ready | placeholder cover → PREPARED_WITH_PLACEHOLDER |
| Listing ≠ Published Listing | requires verified Publish Evidence |
| product_type ≠ asset_type | e.g. digital_template + xlsx/pdf/zip |
| Platform ∉ Product Core | Listing.platform only |

**Future Expansion Risk（documented, not fixed here）：** CF `product_generator` hardcodes PPT/Excel/Word/PDF as product types.

---

## 9.5 Opportunity Discovery & Selection（Entry 054 · Partially Implemented）

> **Implemented：** Signal derivation from SQLite listings → candidate → score → risk → selection with evidence。  
> **Partial：** Score = listing proxy model（not final intelligence）。  
> **Missing：** Cognition agents；auto Experiment；true time-series trend/growth。

```text
MarketSource → Connector → Raw → Normalizer → market_observations
      ↓ (PARTIAL bridge)
market_signals (derived; does not overwrite raw)
      ↓
Opportunity Candidate (autonomous_discovery_v1.json)
      ↓
Score / Risk / Selection → Experiment Candidate（NOT auto Production）
```

> **058B：** Prefer `market_observations` over legacy `products` for new market facts. `products` remains compatibility store.

| Rule | Enforcement |
|------|-------------|
| Raw ≠ Signal ≠ Score | separate tables/objects |
| No evidence → no silent opp | INSUFFICIENT_DATA / refuse_empty |
| Hot ≠ Opportunity alone | multi-dimension score |
| Selection ≠ Production | auto_production_forbidden |
| No future leakage | observation_timestamp ≤ score_time |
| Platform/source extensible | text fields |

Human-assisted `opportunities_v1.json` remains separate SoT for legacy manual objects.

---

## 9.6 End-to-End Autonomous Product Generation Loop（Entry 055 · Partially Implemented）

> **DEC-026.** Vertical pilot proving modules can be chained. Stops at Publish Queue.

| Segment | Status |
|---------|--------|
| Data → Signal → Opportunity → Selection | **Implemented**（054） |
| Selection → Experiment Candidate → Experiment | **Partial Implemented**（055 bridge；≠ Cognition） |
| Experiment → Production Request | **Partial Implemented**（055 append；human_assisted retained） |
| Production Request → Content Factory | **Implemented**（Adapter reuse；pilot_only=false for approved E2E） |
| CF → Product Asset（physical file） | **Implemented**（Pilot `f2f8bab97df8.xlsx`） |
| Product Asset → Quality | **Implemented**（QualityAgent inside CF） |
| Quality → Commercial Product | **Partial Implemented**（generic handoff via E2E；pilot builders remain） |
| Commercial Product → Listing Package | **Partial Implemented**（CF package + minimal faq/delivery/version adapter） |
| Listing → Publish Queue → AWAITING_HUMAN | **Implemented**（`pq_auto_f2f8bab97df8`） |
| External Publish / Observation / Learning | **Missing**（by design for 055） |

```text
aoc_919c62520b98 → exp_auto_* → preq_auto_* → f2f8bab97df8
  → cp_auto_f2f8bab97df8 → lst_auto_f2f8bab97df8 → pq_auto_f2f8bab97df8
  → AWAITING_HUMAN_ACTION
```

**Rules：** Production Success ≠ Commercial Success；no fake Market Events；Legacy Pilot `8523329941d4` = HISTORICAL.

**Future expansion risk（document only）：** CF generators still hardcode PPT/Excel/Word/PDF； Listing/Queue/Commercial core remain product_type-agnostic strings.

### Human Publish Pack（Entry 056 · Implemented）

> Operational handoff before Human External Action. Does not create Publish Evidence.

| Artifact | Path / Status |
|----------|----------------|
| HUMAN_PUBLISH_PACK | `commercial_assets/e2e_outputs/f2f8bab97df8/HUMAN_PUBLISH_PACK.md` |
| Evidence template | `PUBLISH_EVIDENCE_TEMPLATE.json`（TEMPLATE_ONLY） |
| Builder | `6_EXECUTION/human_publish_pack.py` |
| Queue | still `AWAITING_HUMAN_ACTION` |
| Publish Evidence | MISSING |
| Observation | NOT_STARTED |

```text
Human Publish Pack READY
  → Human External Publish
  → record_publish_evidence (VERIFIED / MANUAL_VERIFIED)
  → Queue PUBLISHED + observation_eligible
  → Observation Start (NEXT Entry)
```

### Price Intelligence（Entry 057 · Partially Implemented · DEC-027）

```text
Market Evidence (listing asking prices)
      ↓
Price Recommendation (explainable; confidence = evidence confidence)
      ↓
Listing Price (Human External Action confirms)
      ↓
Paid Price (REAL market events only)
      ↓
Price Learning (Future — currently NONE)
```

| Layer | Status |
|-------|--------|
| Ontology / roles | **Implemented** |
| Provenance audit (99.9 / 19.9) | **Implemented** |
| Recommendation v0.1 (hybrid rule) | **Implemented**（LOW confidence） |
| Listing Price confirm | **Human Gate**（not auto） |
| Paid / Validated / Learning | **Missing**（by design；Paid=null） |

**Reality on `f2f8bab97df8`：** 99.9=SAMPLE listing avg→HYPOTHESIS（058A）；19.9=CF_PIPELINE_DEFAULT；recommended_experimental=19.9 range 12.9–29.9.

### Data Provenance Boundary（Entry 058A · Implemented · DEC-028）

```text
External Source (must prove REAL)
      ↓
Raw (preserved; may be SAMPLE)
      ↓
Current DB (operational SoT — clean after 058A)
      ↓
Signals → Opportunity → …
```

| Store | Role |
|-------|------|
| `data/ai_factory.db` | Current Operational DB |
| `99_ARCHIVE/database_history/*.db` | Legacy / SAMPLE archive only |
| `data/raw/xianyu/` | Raw evidence（incl. `*_sample.xlsx`） |
| `commercial_assets/` | Commercial lifecycle SoT |

**Rule：** DB has rows ≠ REAL market data.

### Market Source Architecture（Entry 058B · Partial Implemented · DEC-029）

```text
External Source
      ↓
Connector (XianyuImportConnector · EXTERNAL_IMPORT)
      ↓
Raw (data/raw/<source>/…)
      ↓
Normalizer
      ↓
MarketObservation (Current DB)
      ↓
MarketSignal → Opportunity → Product → Listing(sales_platform)
      ↓
MarketEvent → Evaluation → Commercial Learning
```

| Rule | Enforcement |
|------|-------------|
| Discovery Source ≠ Sales Platform | `sales_platform` never auto-bound from source |
| LIVE ≠ IMPORT ≠ FIXTURE | modes explicit；LIVE_COLLECTION = **NOT AVAILABLE** |
| Observation ≠ Event | separate tables/semantics |
| No platform-core tables | no `xianyu_products` / `taobao_products` |
| Provenance + data_origin | required on observations / runs |
| One Product → many Listings | Listing.platform independent |
| SAMPLE ≠ REAL | import rejects sample markers |

**Xianyu Reality：** Recommended **USER_EXPORT / MANUAL_IMPORT**；LIVE_API = **NOT_AVAILABLE_CURRENTLY**（open.goofish invitation-only；project ineligible）。Collector abstraction：**Source → Adapter → Raw → Observation**。WAITING_FOR_REAL_SOURCE（drop zone empty）。

### Acquisition Modes（Entry 058D）

| Mode | Status |
|------|--------|
| USER_EXPORT / MANUAL_IMPORT | **IMPLEMENTED**（recommended） |
| LIVE_API / PARTNER_API | **NOT_AVAILABLE_CURRENTLY** |
| SCRAPE_BYPASS / LOGIN_AUTOMATION_BYPASS / ANTI_BOT_BYPASS | **FORBIDDEN** |

`collection_query` (e.g. Excel模板) ≠ `source` (xianyu).

### Own Product & Commercial Dimensions（Entry 058E · DEC-030）

```text
Market Intelligence ≠ Product Copying
MARKET_INSPIRED ≠ auto infringement
Product Type (digital_template/…) ≠ Business Model (DIRECT_SALE/…)
```

| Concern | Status |
|---------|--------|
| Own Product Principle | **Recorded**（Constitution #27） |
| product_origin / rights / provenance / risk | **Minimal model** Implemented |
| business_models (multi-tag) | **Minimal model** Implemented |
| market_region CN/GLOBAL | Designed；overseas Not Built |
| Public Web HTML listing extract | **NOT_FEASIBLE**（CSR shell · 058E） |
| Browser PUBLIC_WEB_READ（060） | **LIMITED** — headless = ACCESS_DENIED |
| Interactive Browser（061） | **LIMITED** — visible Chrome+CDP；title/price/url OK；want PARTIAL；candidates in test-dir |
| Targeted SEARCH_RESULT（062） | **LIMITED** — origin classification Implemented；anonymous session = empty primary search |
| Search Session（063） | **PARTIAL** — Control NOT_FEASIBLE；Collect FEASIBLE when SEARCH_RESULT DOM present |
| Xianyu Extension Forensics（064） | **Blueprint** — reference plugin analyzed；Browser Extension + Local Bridge **Designed, Not Built** |
| Xianyu Browser Extension v1（065） | **IMPLEMENTED / LIMITED** — MV3 + localhost bridge + test sink；live SEARCH_RESULT **NOT_CONFIRMED** |
| Production first REAL batch in Current DB | **NO** |

### Search Session Architecture（Entry 063）

```text
Acquisition Engine
      ↓
Search Controller  (PARTIAL / NOT_FEASIBLE in anon automation)
      ↓
Browser Session (SearchSession)
      ↓
Page State: SEARCH_RESULT | EMPTY | RECOMMENDED | BLOCKED
      ↓
Xianyu Browser Collector  (FEASIBLE when SEARCH_RESULT DOM present)
      ↓
Raw → Candidate (test-dir) → later MarketObservation
```

### Browser Extension Acquisition Path（Entry 064 · Blueprint · Not Built）

```text
User Policy
      ↓
Acquisition Engine
      ↓
AcquisitionTask { source, query, scope, filters }
      ↓
Query Strategy (UserConfigured; future AIQueryPlanner)
      ↓
Search Controller (PARTIAL — 063)
      ↓
AI_FACTORY_OS Browser Extension (Entry 065)
      ↓
Xianyu Adapter (DOM selectors, want regex — adapter-only)
      ↓
MarketRecord batch
      ↓
Localhost Bridge (recommended: HTTP POST)
      ↓
Raw → Normalizer → MarketObservation
      ↓
Filter (min_want_count; NULL → UNKNOWN)
      ↓
Signal → Opportunity → Product (future)
```

| Piece | Status |
|-------|--------|
| Reference plugin forensics | **Done**（064） |
| Own Extension | **Implemented**（065 · LIMITED） |
| Local Bridge | **Implemented**（065 · localhost HTTP） |
| Collector-side want filter | **Rejected** — Filter layer only |
| CSV/Excel as SoT | **Rejected** — debug export only |

### Autonomous Market Acquisition Engine（Entry 059 · DEC-031 · Partial）

```text
User Policy / Acquisition Policy (goal — Entry 067)
      ↓
Acquisition Engine (tasks — no platform DOM)
      ↓
AcquisitionTask { policy_id?, source, query, scope, filters }
      ↓
Source Adapter (Import ACTIVE; Browser LIMITED; Live NOT_AVAILABLE)
      ↓
Raw → Normalizer → market_observations
      ↓
Filter Layer (optional; NULL want → UNKNOWN — Entry 067)
```

### AI Cost Gate（Entry 067 · Partial）

```text
Product / Analysis Task
      ↓
Product Creation Capability (boundary only)
      ↓
AI Cost Gate (estimated_cost vs allowed_cost)
      ↓
PASS | BLOCKED / REDESIGN_REQUIRED | UNKNOWN
      ↓
(Future) ModelSelector / Cost-aware Router — NOT_BUILT
```

| Piece | Status |
|-------|--------|
| AcquisitionTask / Policy | **Implemented** |
| Market Acquisition Policy (goal) | **PARTIAL**（067） |
| Filter Layer | **PARTIAL**（067） |
| Filter → Observation wiring | **PARTIAL**（068；live SEARCH=0） |
| KEYWORD_SEARCH + MANUAL | **Implemented** |
| Other scan strategies / schedules | **Designed**（DRAFT / not auto-run） |
| AI Query Planner | **PROPOSED** |
| AI Cost Gate | **PARTIAL**（067；no paid calls） |
| Model Router / Cursor≠Product AI | **Documented**；Router Not Built |
| Learning→Acquisition | **RESERVED** |
| Software UI | **Settings shape only** |

---

## 10. Future Extensibility Architecture Notes（Design Reference · DEC-020）

> **Reserve Abstraction ≠ Implement Future Capability.**

| Concern | Preferred direction（Proposed） | Current Reality risk |
|---------|--------------------------------|----------------------|
| Product model | `Product` + `Product Type` + `Asset` + `Asset Type` | **053：** handoff model Implemented；CF generators 仍硬编码 PDF/PPT/Excel/Word |
| Collector | Source / Connector / Raw / Normalizer / Observation / Signal | **058B：** layer Implemented；LIVE Xianyu Missing（compliance） |
| Quality | Unified Quality Framework + type-specific dimensions | 固定启发式分数字段 |
| Feedback | Market Event（type/source/product/listing/time） | **051：** `market_events` Implemented；live connectors Not Built |
| Distribution | Channel adapter ≠ Product core model | **052：** Publish Queue Implemented；live publish Missing |
| Learning | Real market outcomes ≠ simulated publish | **050+051：** Integrity + Event bridge；真实 Pilot 事件仍 0 |

**Phase 1 Scope：** Digital / Virtual Materials only.  
**Future types（Not Built）：** video / drama / novel / audio / image / course / software …

---

## 11. Commercial Loop Reality Snapshot（Entry 049 Audit · 050 Learning Integrity Update）

| Layer | Capability | Reality | Expansion Risk | Action |
|-------|------------|---------|----------------|--------|
| Data | Collection | **058B：** EXTERNAL_IMPORT REALITY；LIVE Missing | MEDIUM residual | Live only if compliant |
| Data | Opportunity Discovery | **054：** Partial Implemented（listing→signals→candidates） | MEDIUM | Expand sources later |
| Decision | Listing scoring | REALITY（Track A） | MEDIUM | NO ACTION now |
| Decision | Commercial Opportunity | **054+055：** Partial autonomous + E2E bridge；human JSON 并存 | HIGH residual | Expand intelligence |
| Experiment | Selection / E2E bridge | **055：** Partial autonomous Experiment/PR bridge | MEDIUM | Harden later |
| Production | CF generation | **055：** E2E Adapter real asset + Legacy Pilot | MEDIUM（类型硬编码） | LATER abstract |
| Quality | Validation | PARTIAL fixed scores（CF QualityAgent） | MEDIUM | LATER |
| Distribution | Publish Queue | **052+055：** Implemented（Legacy + E2E AWAITING_HUMAN） | MEDIUM | Human publish next |
| Market | Observation | MISSING（not started）；pipeline Ready | CRITICAL | After evidence |
| Feedback | Market Events | **051：** empty table + ingest API | MEDIUM residual | Wire connectors later |
| Learning | Memory Integrity | **050+051：** guardrail + event bridge | MEDIUM residual | Needs real events |
| Storage | SQLite commercial entities | MISSING | HIGH | LATER |
| Governance | Continuity | REALITY（DEC-019…026） | LOW | NO ACTION |

**Blueprint ≠ Runtime。** E2E Loop to Queue = **Partial Implemented（055）**；完整自主商业学习闭环仍 **Not Implemented**。
