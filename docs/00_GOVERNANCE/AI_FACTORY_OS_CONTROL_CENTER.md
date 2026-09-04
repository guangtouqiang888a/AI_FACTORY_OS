# AI_FACTORY_OS Control Center

> **SINGLE ENTRY POINT for future AI sessions（未来 AI 会话唯一入口）**  
> Collaboration Control System v1（协作控制系统 v1）  
> Last updated: 2026-09-04（**Core Documentation Continuity Hardening** — NOT Entry 077）

**Read this file first.（任何新会话必须先读本文件。）** Then follow **New Session Recovery Protocol**（及下方 Bootstrap）。  
文档目录导航 SoT：[DOCUMENTATION_MAP](../AI_FACTORY_OS_DOCUMENTATION_MAP.md)。

### Navigation Authority ≠ Reality Authority（导航权威 ≠ Reality 权威）

本文件是新会话**入口、导航与 Recovery 控制层**。  
**不是** Runtime / Code / DB / Assets 的替代权威，也**不是** Current State 的替代品。

权威顺序仍以 [AUTHORITY_MODEL](AI_FACTORY_OS_AUTHORITY_MODEL.md) 为准：

`Reality > Current State > Decision Log > Documentation > Conversation Memory`

本文件中的 **Current Phase / Current Primary Goal / Current Development Focus / Active Risks** 属于**可过期状态投影**。  
若与 [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) 或 Reality 冲突 → **以 Current State / Reality 为准**，不得用本文件旧投影覆盖事实。

**Recovery 权威（唯一）：** 本文件内 **New Session Recovery Protocol（DEC-017）** + 上方 **AI Recovery Reading Boundary（044-A）** + Documentation Map 导航。  
**协作准则（现行对齐）：** [`AI_FACTORY_OS_WORK_PRINCIPLES.md`](../AI_FACTORY_OS_WORK_PRINCIPLES.md) — 冲突以本目录 Constitution / Protocol 为准。  
归档辅助文件 `99_ARCHIVE/execution_history/reference/AI_FACTORY_OS_RECOVERY_READ_ORDER.md` **不是**现行 Recovery 权威，默认不读取。

**长期商业方向指针（DEC-020…033）：** … + Browser Extension v1（065）；Import Gate（066）；Acquisition Policy + AI Cost Gate（067）— 成本控 estimated_cost 非 call_count；Model Router 未建；IMPORT 仍可用；Cursor ≠ 产品 AI；**DEC-033** 商业结果优先 / 最低成本含 AI / 用户发布与异常介入 / Commercialization Context 解耦 / 闲鱼 Pilot ≠ 永久边界。  
**基础设施指针：** GitHub `main` 已作为版本化 / 跨 Session 连续性载体（见下方 GitHub Continuity Note）；**GitHub ≠ Reality Authority**。

---

# AI Recovery Reading Boundary（AI 恢复阅读边界）

> Entry **044-A**。

AI 恢复上下文时，按层加载；**禁止**一次加载全部 `docs/`；**禁止**用 Archive / History 推断当前 Reality。

### 第一层（必须）

| 顺序 | 文件 | 路径提示 |
|------|------|----------|
| 0 | [DOCUMENTATION_MAP](../AI_FACTORY_OS_DOCUMENTATION_MAP.md) | `docs/AI_FACTORY_OS_DOCUMENTATION_MAP.md` |
| 1 | CONTROL_CENTER（本文件） | `docs/00_GOVERNANCE/` |
| 2 | [AUTHORITY_MODEL](AI_FACTORY_OS_AUTHORITY_MODEL.md) | `docs/00_GOVERNANCE/` |
| 3 | [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) | `docs/01_CURRENT_STATE/` |
| 4 | [MODULE_REGISTRY](../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) | `docs/01_CURRENT_STATE/` |

### 第二层（默认补齐）

| 文件 | 路径提示 |
|------|----------|
| [UNIFIED_ARCHITECTURE](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) | `docs/02_ARCHITECTURE/` |
| [BUSINESS_STRATEGY](../03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md) | `docs/03_BUSINESS/` |

### 按需读取

| 域 | 目录 |
|----|------|
| EXECUTION | `05_EXECUTION/`（执行台账；Entry 连续性） |
| HISTORY | `06_HISTORY/`（仅历史解释） |
| AUDIT | `07_AUDIT/` |
| BLUEPRINT（归档） | `99_ARCHIVE/blueprint_history/` — Design Reference only；≠ Production；**默认不作为 Current Reality** |

### 默认不读取

| 域 | 规则 |
|----|------|
| ARCHIVE | `99_ARCHIVE/` — **默认不读取**；不参与现行判断（含旧 Recovery Read Order、WORK_PRINCIPLES） |

完整目录职责与角色定义以 Documentation Map 为准。下方 **New Session Recovery Protocol（DEC-017）** 仍有效，并与本边界兼容。

---

# New Session Recovery Protocol（新会话恢复协议）

> Entry **041-G** / **DEC-017**。

解决：AI 重新进入项目时不知道读取顺序、权威关系、历史文件用途、当前 Reality。

**恢复顺序原则：** 先恢复规则 → 再恢复 Reality → 再读取设计 → 最后读取历史。  
**禁止：** 直接根据历史文件推断当前系统。

## 第一阶段：恢复系统基础认知（必须）

| 顺序 | 文件 | 用途 |
|------|------|------|
| 1 | [PROJECT_CONSTITUTION](AI_FACTORY_OS_PROJECT_CONSTITUTION.md) | 系统最高规则 |
| 2 | [AUTHORITY_MODEL](AI_FACTORY_OS_AUTHORITY_MODEL.md) | 确定信息权威关系 |
| 3 | [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) | 确定当前 Reality 状态（文档投影） |
| 4 | [MODULE_REGISTRY](../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) | 确定模块当前状态 |
| 5 | [DECISION_LOG](AI_FACTORY_OS_DECISION_LOG.md) | 确定历史重大决策 |

以上文件用于恢复系统**基础认知**。未完成第一阶段前，不得提出架构融合或 Reality 执行方案。

## 第二阶段：按任务类型追加读取

| 任务类型 | 读取 |
|----------|------|
| **架构问题** | [UNIFIED_ARCHITECTURE](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) |
| **商业问题** | [BUSINESS_STRATEGY](../03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md) |
| **商业方案 / 能力组合分析** | 见下方「分析商业方案」；**不得**按文件夹拆分能力 |
| **未来规划问题** | `../99_ARCHIVE/blueprint_history/` 相关 Blueprint（Design Reference only；≠ Production；非 Current Reality） |
| **历史来源问题** | [ARCHITECTURE_EVOLUTION_CONTEXT_RECORD](../06_HISTORY/AI_FACTORY_OS_ARCHITECTURE_EVOLUTION_CONTEXT_RECORD.md) |
| **执行问题** | [EXECUTION_PROTOCOL](AI_FACTORY_OS_EXECUTION_PROTOCOL.md)、[KNOWLEDGE_UPDATE_PROTOCOL](AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md) |

仍禁止一次加载全部 `docs/`。第二阶段仅追加与 Scope 相关的文件。

### 分析商业方案时（041-H / DEC-018）

**不得**直接按照文件夹（`0`–`11`）拆分能力。

**必须参考：**

- Constitution：**Folder Capability Separation** / **Capability Composition Principle**
- [UNIFIED_ARCHITECTURE](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) — Capability Architecture Model
- DEC-013 / DEC-014 / **DEC-018**

**公式提醒：** Folder Structure ≠ Capability Architecture ≠ Product Architecture。

---

# Document Reading Principle（文档读取原则）

> Entry **041-F** / **DEC-016**。

读取文件时：**首先判断信息类型**，再选择归属文件。

| 需要的信息 | 读取 |
|------------|------|
| **当前事实** | [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) |
| **模块 Status（Active/Frozen/Planned）** | [MODULE_REGISTRY](../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) |
| **历史原因** | [ARCHITECTURE_EVOLUTION_CONTEXT_RECORD](../06_HISTORY/AI_FACTORY_OS_ARCHITECTURE_EVOLUTION_CONTEXT_RECORD.md) |
| **设计 / 目标架构** | [UNIFIED_ARCHITECTURE](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) |
| **商业方向** | [BUSINESS_STRATEGY](../03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md) |
| **系统规则** | [PROJECT_CONSTITUTION](AI_FACTORY_OS_PROJECT_CONSTITUTION.md) |

**不得**因为历史文件、Blueprint 或审计内容覆盖 Reality。  
信息归属总表见 Constitution **Information Ownership Principle**（DEC-016）。

---

# Session Bootstrap Required Reading Order（会话启动必读顺序 — 扩展）

> 与 **New Session Recovery Protocol** 第一阶段兼容。完整运营会话可在第一阶段后按本表补齐 Business Strategy / UA / Protocols。  
> **权威恢复顺序以 New Session Recovery Protocol + DEC-017 为准。**

新会话必须先完成 **New Session Recovery Protocol 第一阶段**，**不得跳过认知步骤、不得只用聊天记忆**。

| 顺序 | 文件 | 为什么读取（中文） |
|------|------|-------------------|
| 1 | [AUTHORITY_MODEL](AI_FACTORY_OS_AUTHORITY_MODEL.md) | 先理解**什么最高权威**：用户决策权、Reality、以及文档之间谁优先；防止把聊天或历史报告当事实。 |
| 2 | [PROJECT_CONSTITUTION](AI_FACTORY_OS_PROJECT_CONSTITUTION.md) | 理解**长期使命和不可改变原则**（如 Blueprint≠Runtime、Human Assisted、Scope 控制）。 |
| 3 | [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) | 理解**当前真实阶段**、已完成/阻塞/已知问题；禁止用愿景代替现状。 |
| 4 | [BUSINESS_STRATEGY](../03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md) | 理解**商业目标**、第一收入来源优先级、禁止误判事项。 |
| 5 | [UNIFIED_ARCHITECTURE](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) | 理解**架构目标与边界**（双轨、Not Started、数据所有权摘要）；目标≠已融合 Runtime。 |
| 5b（按需） | [MODULE_REGISTRY](../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) | 模块 **Current Status** 以 Registry Reality 为准（041-D：`10_DEPLOY`=Active HTTP；Current Flow=双轨）。 |
| 6 | [EXECUTION_PROTOCOL](AI_FACTORY_OS_EXECUTION_PROTOCOL.md) | 理解**执行规则**（Scope、可读性、自检门、认知完整性检查）。 |
| 7 | [KNOWLEDGE_UPDATE_PROTOCOL](AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md) | 理解变化发生后**如何分级更新**核心文件、是否需用户确认与 DEC。 |
| 8 | [DECISION_LOG](AI_FACTORY_OS_DECISION_LOG.md) | 理解**历史关键裁决**（含 DEC-011..**018** 等）；禁止重复否决过的方向。 |
| 9 | — | **进入任务执行**（仍须遵守本文件 Forbidden 与任务 Scope）。 |

仍禁止一次加载全部 `docs/`。任务相关详文仅在 Scope 需要时追加。

### 按需：模块历史来源（Historical Explanation）

当需要分析模块**历史形成原因**时（例如理解 `2_COGNITION`、`4_PRODUCT`、`9_PRODUCT`、`10_DEPLOY`、`11_CONTENT_FACTORY` 为何如此），读取：

[ARCHITECTURE_EVOLUTION_CONTEXT_RECORD](../06_HISTORY/AI_FACTORY_OS_ARCHITECTURE_EVOLUTION_CONTEXT_RECORD.md)

**说明：** 该文件仅用于历史解释。

**不得覆盖：**

- Reality（Code / DB / commercial_assets / Runtime）
- Current State
- Authority Model

文档角色分层策略（不移动文件）：[DOCUMENTATION_ARCHITECTURE_GOVERNANCE_STRATEGY](../99_ARCHIVE/audit_history/AI_FACTORY_OS_DOCUMENTATION_ARCHITECTURE_GOVERNANCE_STRATEGY.md)（DEC-015）。

---

# Core Governance Navigation（核心治理导航）

### Current Core Continuity Domain（当前核心连续性文档域 · DEC-019）

当前 **`docs/00_GOVERNANCE` → `docs/06_HISTORY`（`docs/0–6`）** 构成 AI_FACTORY_OS **当前核心连续性文档域**。  
新会话应能从该域恢复：规则、权威、当前状态、商业/架构认知、执行进度、重大决策与长期演进背景。

**含：** Governance · Current State（含 Module Registry）· Architecture · Business · Execution History · History。  
**Audit（`07_AUDIT`）** = 证据 / 验证记录，**不是** Current State 替代品。

### Historical: Core Governance Set v1（历史结构版本 · DEC-009）

**Core Governance Set v1 = 8 核心文件 + AUTHORITY_MODEL（强制卫星）** 是**历史治理结构版本**（Entry 040-D1 / DEC-009）。  
它仍是「核心认知文件检查清单」的有用导航，**不得**再被解释为「当前完整核心文件集合 = 仅此 8+1」。

文件清单（速查 / Impact 评估常用）：

| # | 文件 | 角色 |
|---|------|------|
| — | [CONTROL_CENTER](AI_FACTORY_OS_CONTROL_CENTER.md)（本文件） | 启动入口与导航（**非 Reality SoT**） |
| 1 | [AUTHORITY_MODEL](AI_FACTORY_OS_AUTHORITY_MODEL.md) | 权威模型（强制卫星） |
| 2 | [PROJECT_CONSTITUTION](AI_FACTORY_OS_PROJECT_CONSTITUTION.md) | 项目宪法 |
| 3 | [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) | 当前事实状态投影 |
| 4 | [BUSINESS_STRATEGY](../03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md) | 当前商业战略唯一入口 |
| 5 | [UNIFIED_ARCHITECTURE](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) | 统一架构（目标层） |
| 6 | [EXECUTION_PROTOCOL](AI_FACTORY_OS_EXECUTION_PROTOCOL.md) | AI 执行协议 |
| 7 | [KNOWLEDGE_UPDATE_PROTOCOL](AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md) | 知识更新协议 |
| 8 | [DECISION_LOG](AI_FACTORY_OS_DECISION_LOG.md) | 正式决策 |

另属 `docs/0–6` 连续性域、须按影响同步：`MODULE_REGISTRY`、`CURSOR_EXECUTION_HISTORY`、`ARCHITECTURE_EVOLUTION_CONTEXT_RECORD`（历史解释 only）。

Entry 037–040 治理类继承关系见：[KNOWLEDGE_CONSOLIDATION_MAP_A](../99_ARCHIVE/audit_history/AI_FACTORY_OS_KNOWLEDGE_CONSOLIDATION_MAP_A.md)（映射，非默认全文必读）。

---

# Session Bootstrap Protocol（会话启动协议）

任何**新的 AI 工作会话**开始时，必须按下列顺序执行，**不得跳过**。

### 第一步

必须读取：

`docs/00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md`（本文件）

并执行上方 **New Session Recovery Protocol** 第一阶段（DEC-017）；再按任务需要进入第二阶段。  
扩展阅读仍可参考 Session Bootstrap Required Reading Order。

### 第二步

阅读下方 **Current Phase**（状态投影），然后**必须**与 [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md)（及 Scope 所需 Reality）交叉核验。  
**禁止**仅凭本文件旧投影宣布 Current Reality。

### 第三步

阅读下方 **Current Primary Goal**（状态投影），同样以 Current State / 用户授权 Scope 为准核验。

### 第四步

确认：**当前禁止事项（Forbidden Actions）**  
（见下方「Forbidden Actions」章节）

### 第五步

**只有**完成以上确认后，才可以：

- 提出方案  
- 生成执行任务 / Cursor 指令  

### 无法确认时

若无法确认当前阶段、最高优先级目标或禁止事项：

- **禁止**直接提出架构方案  
- **必须**先恢复项目状态（读取 Current State、Authority Model，必要时核对 Reality）  
- 恢复完成前，不得扩大任务范围  

---

## Current Phase

> **State projection（可过期）。** 权威事实投影 → [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md)。Audit ≠ Current State。

### Strategic orientation（慢变标签）

**Commercial Validation Preparation（商业验证准备）** — 长期战略取向标签；**不等于**「下一动作已授权」或「Runtime/商业已验证成功」。

### Operational snapshot（2026-09-04 · 须与 Current State / Reality 核验）

| 项 | 投影（须核验） |
|----|----------------|
| Latest completed product-path Entry | **076** = `PASS_WITH_FINDINGS` |
| Product Definition | `prod_a0638789fc2b`（`draft`）← Opportunity `aoc_19399677b7ba` |
| Product Definition ≠ | Product Asset / Commercial Product / Listing / Published / Market Validated |
| Entry **077** | **NOT_STARTED** — 不得擅自启动 |
| Development posture | 商业/产品推进**暂停**，等待另开授权 Entry |
| GitHub | `main` 已建立为版本化 / 协作连续载体；**同步本身未改变**产品/商业/架构方向 |
| Pilot Observation | 仍 **NOT_STARTED**（见 Current State；非本投影发明） |
| Commercial JSON full migration / Pilot sync | 历史 open item（RA-002 等）— **不得**因本文件旧文自动当作当前唯一焦点 |

### Governance foundation history（已完成 · 非 Current Reality 清单）

Collaboration Control System v1 Foundation: **Implemented (docs/control layer)**  
Entry 040-A … 041-H 治理基础（DEC-013…018 等）— **Completed**（详文保留于历史 Entry / Audit；此处不重复当作「今天刚发生」）。

---

## Current Primary Goal

1. **正确 Recovery：** 先规则与权威 → 再 Current State / Reality → 再按 Scope 读设计 / 商业 / 历史（DEC-017）。  
2. **防止认知错误：** 不以 Control Center 旧投影、Audit  alone、或 GitHub 文档状态覆盖 Reality。  
3. **范围纪律：** Entry **077** = **NOT_STARTED**；未授权不得推进 Product content / Publish / CF–Core 合并 / DB 迁移。  
4. **连续性：** 有意义推进写入 `docs/0–6`（DEC-019）；长期协作规则不得只留在 Conversation Memory。

**重大判断必须回溯 Core Governance（DEC-012）与 `docs/0–6`，** 不得只靠聊天改方向。  
Governance / Recovery hardening 可在授权下进行；**Reality Execution（产品内容、发布、观察、迁移）须另开授权 Entry。**

---

## Current Development Focus

1. Control Center + **New Session Recovery Protocol**（DEC-017）启动；状态投影须对照 Current State / Reality  
2. DEC-011 / DEC-012：Scope 控制 + 防聊天认知漂移  
3. Trust **CURRENT_STATE + MODULE_REGISTRY + Reality**；Blueprint / Audit / GitHub docs ≠ Production / Runtime complete  
4. Entry **076** 已完成（Definition draft）；**等待授权**再开 Product content / Commercial / Publish Entry  
5. Entry **077**：**NOT_STARTED** — 禁止抢跑  
6. Do **not** expand into Core OS ↔ CF Runtime merge unless explicitly tasked  
7. DEC-015…018：文档角色 / Ownership / Recovery / Folder≠Capability≠Product  
8. Open historical commercial items（Pilot Observation、RA-002 migration 等）— **先读 Current State**，不得因本文件旧 bullet 自动执行  
9. GitHub = 版本化 / 跨工具运输 / 可追溯恢复；**≠ Reality Authority**

---

## Active Risks

| ID | Risk（风险） |
|----|------|
| R1 | Documentation volume high → context overflow if all docs loaded |
| R2 | Control Center / 其他导航文件中的**状态投影过期**，被误当作 Current Reality（Recovery Drift） |
| R3 | Dual-track: Core OS pipeline ≠ Content Factory Adapter（双轨未统一 Runtime） |
| R4 | Schema drift: `database.py` vs `ai_factory.db`（已知；未执行迁移） |
| R5 | Conversation memory / GitHub docs / Audit  alone 被当成 Reality 或 Current State |
| R6 | Product Definition（如 `prod_a0638789fc2b`）被误升格为 Asset / Listing / Published / Market Validated |
| R7 | Commercial JSON lifecycle / Pilot 字段与已完成生产不一致（RA-002 等仍可能 open — 以 Current State 为准） |

---

## Required Reading

**Minimum（与 Bootstrap 必读顺序一致，摘要）：**

1. 本文件（Control Center）  
2. Authority Model → Constitution → Current State → Business Strategy → Unified Architecture → Execution Protocol → Knowledge Update Protocol → Decision Log  

**If changing commercial status / Pilot（改商业状态 / Pilot 时）：**

- `docs/06_HISTORY/AI_FACTORY_OS_COMMERCIAL_STATE_HISTORICAL_SNAPSHOT.md`
- `docs/07_AUDIT/commercial/AI_FACTORY_OS_PILOT_STATE_MIGRATION_ANALYSIS.md`

**Do NOT** load every file under `docs/` at session start.（启动时禁止加载全部 markdown。）

---

## Forbidden Actions (session default)（会话默认禁止）

- Modify Python / Runtime / DB / commercial_assets unless the **current task explicitly authorizes** it  
- Expand scope beyond stated Goal / Out of Scope  
- Auto-fill market success, revenue, or fake feedback  
- Claim Blueprint/Strategy as Production/Runtime complete  
- Delete or bulk-move historical docs  
- Merge Core OS and Content Factory without explicit architecture Entry  
- “Fix” unrelated issues discovered mid-task (record only)  
- Skip Session Bootstrap Protocol / **New Session Recovery Protocol** / Required Reading Order（跳过会话启动必读；违反 DEC-017）  
- Infer current system from Evolution Context / Blueprint / audit alone（用历史文件推断当前系统；违反 DEC-017）  
- Split commercial capabilities by folder name alone（按目录名拆商业能力；违反 DEC-018）  
- Change project direction from **chat context alone** without Core Governance 回溯（违反 DEC-012）  
- Treat Control Center **state projections** as Reality SoT when they conflict with Current State / Reality  
- Treat **Audit** as Current State substitute  
- Treat **GitHub** Documentation / Commit / Audit as Runtime Reality Authority  
- Start **Entry 077** or Product content / Publish without explicit authorization  
- Elevate Product Definition to Product Asset / Commercial Product / Listing / Published / Market Validated without Reality  

---

## Quick Links (control layer)（控制层快捷链接）

| File | Purpose（用途） | 权限 |
|------|---------|------|
| [AUTHORITY_MODEL](AI_FACTORY_OS_AUTHORITY_MODEL.md) | Truth order（权威顺序） | 核心卫星 |
| [PROJECT_CONSTITUTION](AI_FACTORY_OS_PROJECT_CONSTITUTION.md) | Why / permanent principles（使命与永久原则） | 核心 |
| [BUSINESS_STRATEGY](../03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md) | Current business strategy（当前商业战略） | 核心 |
| [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) | Facts now（当前事实） | 核心 |
| [DECISION_LOG](AI_FACTORY_OS_DECISION_LOG.md) | Decisions（决策） | 核心 |
| [EXECUTION_PROTOCOL](AI_FACTORY_OS_EXECUTION_PROTOCOL.md) | How to execute（如何执行） | 核心 |
| [KNOWLEDGE_UPDATE_PROTOCOL](AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md) | Knowledge update rules（知识更新规则） | 核心 |
| [UNIFIED_ARCHITECTURE](../02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) | Target architecture（目标架构） | 核心 |
| [DOCUMENTATION_MAP](../AI_FACTORY_OS_DOCUMENTATION_MAP.md) | 文档唯一导航入口（044-A / 044-K） | 参考（导航 SoT） |
| [DOCUMENTATION_MAP Reference History](../99_ARCHIVE/AI_FACTORY_OS_DOCUMENTATION_MAP_REFERENCE_HISTORY.md) | 旧 L2 索引（已归档） | Archive |
| [治理系统使用手册](../05_EXECUTION/guides/AI_FACTORY_OS治理系统使用手册.md) | **用户操作指南**（如何指挥 AI / 新会话怎么做） | **参考文件（非核心权威）** |



## Documentation Governance Entry

Documentation Map 是文档结构唯一导航入口。

所有人员与 AI：

首先通过 Documentation Map 判断：

- 哪些文件属于 Core
- 哪些文件属于 Current Reality
- 哪些文件属于 Blueprint
- 哪些文件属于 History
- 哪些文件属于 Audit

目录名称不是权威依据。

文件角色声明与 Authority Model 优先。


---


# 044-H / 046 Recovery Entry


新 AI 会话恢复入口：

1. 本文件 **AI Recovery Reading Boundary**
2. 本文件 **New Session Recovery Protocol（DEC-017）**
3. 导航 SoT：[DOCUMENTATION_MAP](../AI_FACTORY_OS_DOCUMENTATION_MAP.md)

以上共同构成**唯一正式 Recovery 定义**。其他文件只做引用与导航，不得平行定义冲突的恢复顺序。

归档文件 `AI_FACTORY_OS_RECOVERY_READ_ORDER.md`（现位于 `99_ARCHIVE/execution_history/reference/`）**不是**现行权威来源。

---

# Core Documentation Continuity（核心文档连续性 · DEC-019）

项目连续性**不依赖** Conversation Memory。  
**当前核心连续性文档域 = `docs/0–6`**（Governance → History）。  
历史 **Core Governance Set v1（8+1）** = 结构版本 / 检查清单，≠ 当前完整连续性域。

正式 Cursor Entry（及同类正式治理任务）完成后，必须执行 **Post-Execution Core Documentation Sync**（见 [EXECUTION_PROTOCOL](AI_FACTORY_OS_EXECUTION_PROTOCOL.md)）：

- **Core Documentation Impact Check** — 判断哪些核心文件受事实变化影响  
- **禁止**机械更新全部核心文件；**禁止**仅因日期旧而强制刷新；**禁止**用 Audit 覆盖他处 Information Ownership  
- **Audit ≠ Current State** — Audit 事实须经正确 Sync 后才进入状态投影  
- 长期协作规则必须进入 Governance（Persistent Collaboration Rule）

### GitHub Continuity Note（基础设施 · 非 Reality 权威）

GitHub（当前 `main`）承担：版本化、协作连续性、跨 Session / 跨工具运输、可追溯恢复。  
**不得**：以 GitHub 文档 / Commit / Audit **凌驾** Runtime / Code / DB / Assets Reality。  
**GitHub sync ≠** Runtime 完成 ≠ Production ≠ 商业成功。

### Collaboration Continuity Pointer（协作连续性指针）

长期协作闭环 + **Task Intent Continuity** 的正式规则位于：

[EXECUTION_PROTOCOL — Collaboration Continuity Workflow + Task Intent Continuity Model](AI_FACTORY_OS_EXECUTION_PROTOCOL.md)

关键约束（已硬化，勿重复发明）：

```text
Conversation Idea ≠ Execution Authorization
Cursor reports PASS ≠ Project Task Closed
Finding ≠ Objective
Audit ≠ Current State
Process Output ≠ Formal Audit
GitHub ≠ Reality Authority
Local Reality ≠ Git Commit ≠ GitHub main
PHASE_N PASS ≠ PROJECT TASK CLOSED
```

需要用户确认的重大任务：ChatGPT 形成 Cursor-ready instruction 后，须经用户确认再执行。  
多步骤任务进入下一 Step 前：须过 **Intent Continuity Gate**。  
Cursor 返回后：须经 **ChatGPT Closure Review** 才可宣布 Project Task Closed。

### Active Task Anchor（当前正式任务锚点）

> **指针层，不是 SoT。** Active Task Anchor ≠ Current State ≠ Reality ≠ Primary Goal ≠ Task Content SoT。

用于告诉未来 AI：是否存在正式进行中的多步骤任务；Original Objective / Phase / Step / Completion Criteria **指针**在哪里。

| Field | Value |
|-------|-------|
| **ACTIVE_TASK** | **`NONE`** |
| **STATUS** | 无正在进行的正式多步骤治理任务 |
| **NOTE** | 商业最高原则硬化（DEC-033）已落盘；First Xianyu Experiment Preparation 已完成对象准备（NOT_PRODUCED）；不得当作正在执行的 CF/发布任务 |
| **LAST GOVERNANCE / COMMERCIAL PREP（证据指针，非当前任务）** | Continuity → PHASE 1/2 → Closure → DEC-033 → **exp_20260904_pmgantt / preq_20260904_pmgantt preparation** |
| **EVIDENCE POINTERS** | `docs/07_AUDIT/AI_FACTORY_OS_COMMERCIAL_PRINCIPLES_HARDENING_2026-09-04.md`；`docs/07_AUDIT/AI_FACTORY_OS_FIRST_XIANYU_PRODUCT_EXPERIMENT_PREPARATION_2026-09-04.md`；DEC-033 |
| **INTENT / PROTOCOL POINTER** | [EXECUTION_PROTOCOL — Task Intent Continuity Model](AI_FACTORY_OS_EXECUTION_PROTOCOL.md) |
| **ENTRY_077** | **NOT_STARTED** |
| **PROJECT_DEVELOPMENT** | **PAUSED** |

若当前无正式多步骤任务，应写：`ACTIVE_TASK = NONE`。

详见 Constitution **Core Documentation Continuity Rule** 与 **DEC-019**。


