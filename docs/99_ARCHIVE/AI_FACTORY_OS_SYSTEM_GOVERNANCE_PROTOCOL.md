# AI_FACTORY_OS System Governance Protocol v1

> **文档角色（Document Role）：** 本文档为历史参考资料，用于理解演进过程，不作为当前最高判断来源。  
> Current highest judgment（当前最高判断）：Core Governance Set v1 + Reality + AUTHORITY_MODEL。

> 系统治理协议层 | 最后更新：2026-07-13  
> **状态：Blueprint Completed — Project Intelligence Layer 治理规范，不参与运行计算**

**定位：** System Governance Layer（系统治理层）— AI_FACTORY_OS 的**横向治理层**，覆盖 Runtime、Database、Commercial Assets、Documentation、Memory，保证系统长期演化过程中**状态一致、边界清晰、审计可恢复**。

**说明：** **Blueprint ≠ Runtime**。**Design ≠ Production**。**Documentation First**。**Governance Before Expansion**。本文档为治理协议设计；不修改 Python、Database、commercial_assets 或 Runtime。

---

## 1. Governance Layer Position（治理层定位）

### 1.1 横向治理层

System Governance Layer 是 AI_FACTORY_OS **横向治理层（Cross-Cutting Governance Layer）**，不替代任何业务模块，而是约束各层如何协作、如何声明状态、如何同步事实。

**覆盖范围：**

| 域 | 路径 / 模块 | 治理关注点 |
|----|-------------|------------|
| **Runtime** | `0_START/`, `11_CONTENT_FACTORY/`, Agents | 行为是否与文档声明一致 |
| **Database** | `data/ai_factory.db`, `1_DATA/` | Schema 与 Blueprint 是否对齐 |
| **Commercial Assets** | `commercial_assets/` | Object 生命周期与 Contract 一致性 |
| **Documentation** | `docs/` | 状态描述是否与事实源同步 |
| **Memory** | `7_MEMORY/` | 学习知识是否与 Operational Data 隔离 |

### 1.2 治理目标

| # | 长期风险 | 治理目标 |
|---|----------|----------|
| 1 | Runtime 状态与文档状态不同步 | 单一事实来源 + Entry 完成后 State Review |
| 2 | Blueprint / Design / Implementation / Production 混淆 | 统一状态词汇表（§4） |
| 3 | DB、commercial_assets、Memory、Documentation 边界不清 | Source of Truth 定义（§2） |
| 4 | ZIP 审计无法恢复真实状态 | ZIP Full Audit Protocol（§5） |
| 5 | 扩展超过治理能力 | Governance Principle（§8） |

### 1.3 架构关系

```
System Governance Layer（横向 — 本 Protocol）
        │
        ├── Runtime（0_START / 11_CONTENT_FACTORY / Agents）
        ├── Database（data/ai_factory.db / 1_DATA）
        ├── Commercial Assets（commercial_assets/）
        ├── Documentation（docs/）
        └── Memory（7_MEMORY/）
```

**规则：** 业务功能在各模块内实现；**状态声明、边界、审计、Entry 闭环**在 Governance Layer 统一约束。

---

## 2. Source of Truth Definition（唯一事实来源）

同一个状态**只能存在一个主要事实来源（Primary Source of Truth）**。其他位置**只能同步描述**，不得独立定义冲突状态。

| 域 | 事实来源 | 说明 |
|----|----------|------|
| **Runtime Behavior** | **Python 代码** | 实际可执行行为以代码为准；文档描述须可对照代码验证 |
| **Operational Data** | **`data/ai_factory.db`** | 运行时操作数据、Legacy 表数据 |
| **Commercial Object** | **`commercial_assets/`** | Production Request、Product Asset、Feedback、Evaluation 等商业 Object JSON |
| **Learning Knowledge** | **`7_MEMORY/`** | 经验沉淀、pattern、策略摘要 — **非** Commercial Object 权威源 |
| **System Description** | **`docs/`** | 设计、契约、状态说明、Entry 历史 — **描述层**，须与事实源定期对齐 |

### 2.1 同步规则

| 规则 | 说明 |
|------|------|
| **代码优先** | Runtime 行为争议时，以 Python 为准，文档跟进修正 |
| **JSON 优先** | Commercial Object 是否存在、字段值，以 `commercial_assets/` 为准 |
| **DB 优先** | Operational 数据是否存在，以 `ai_factory.db` 为准 |
| **docs 不创造事实** | `docs/` 不得单独声明「已生产」「已连接」而无对应代码/JSON/DB 支撑 |
| **Memory 不替代 JSON** | `7_MEMORY` 摘要不得覆盖 `commercial_assets` 权威登记 |

### 2.2 常见混淆（禁止）

| 混淆 | 正确做法 |
|------|----------|
| PROJECT_STATUS 写 Production Completed 但无 product_assets JSON | State Review 阻断或标注 Blueprint only |
| MODULE_REGISTRY 写 Runtime Connected 但无 Pipeline 调用链 | 以代码审计为准修正文档 |
| product_memory.json 当作 Product Asset 权威源 | Commercial 权威源为 `commercial_assets/product_assets/` |

---

## 3. Entry Completion Governance（Entry 完成治理）

### 3.1 Entry 闭环流程

以后所有 Entry 完成**必须**执行：

```
Implementation（或 Documentation Implementation）
        ↓
State Review（状态审查）
        ↓
检查五项：
  1. Python 变化
  2. Database 变化
  3. JSON Asset 变化
  4. Documentation 变化
  5. Snapshot 变化（system_snapshot / PROJECT_STATUS / MODULE_REGISTRY）
        ↓
Execution History 更新（CURSOR_EXECUTION_HISTORY.md）
        ↓
Entry Complete
```

### 3.2 State Review 检查清单

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | **Python 变化** | git diff 确认；CURSOR_EXECUTION_HISTORY 如实记录 Yes/No |
| 2 | **Database 变化** | 无未授权 CREATE TABLE / schema 变更 |
| 3 | **JSON Asset 变化** | commercial_assets 变更与 Entry 授权范围一致 |
| 4 | **Documentation 变化** | PROJECT_STATUS、MODULE_REGISTRY、相关 Contract 已同步 |
| 5 | **Snapshot 变化** | system_snapshot 反映当前链路与状态词汇一致 |

### 3.3 Entry 完成定义

**Entry 完成 ≠ 仅代码完成。**

Entry Complete 表示：**Implementation + State Review + Execution History + 文档同步** 均已闭环，系统描述与事实源**一致或可解释的差异已标注**。

---

## 4. Blueprint and Runtime Separation（Blueprint 与 Runtime 分离）

### 4.1 统一状态定义

| 状态 | 英文 | 含义 |
|------|------|------|
| **Blueprint Completed** | blueprint_completed | 设计/契约/协议文档完成 — **无代码或无运行连接** |
| **Design Completed** | design_completed | 架构设计、集成设计、审计报告完成 |
| **Implementation Completed** | implementation_completed | 代码/模块已实现（如 Adapter、Validation Runtime） |
| **Runtime Connected** | runtime_connected | 已接入真实运行流程（如 PR → CF Pipeline 可执行） |
| **Production Verified** | production_verified | 真实生产/试点已执行并验证（如 Pilot preq_005） |

### 4.2 状态层级（示意）

```
Blueprint Completed
        ↓（可选）
Design Completed
        ↓（Implementation 授权）
Implementation Completed
        ↓（集成 + 调用链验证）
Runtime Connected
        ↓（真实执行 + 验收）
Production Verified
```

### 4.3 禁止混淆

| 禁止 | 说明 |
|------|------|
| **Blueprint Completed 等同 Runtime Ready** | 设计完成不等于可运行 |
| **Design Completed 等同 Production Started** | 集成设计不等于已生产 |
| **Implementation Completed 等同 Commercial Success** | 代码完成不等于市场验证 |
| **Audit Completed 等同 Code Implemented** | 只读审计不等于已写代码 |

**文档须显式标注**当前处于哪一状态层级。

---

## 5. ZIP Full Audit Protocol（ZIP 全量审计协议）

### 5.1 审计范围

以后审计 AI_FACTORY_OS ZIP（或完整工作区快照）**必须完整读取**：

| 类别 | 内容 |
|------|------|
| **文件结构** | 目录树、模块边界、新增/缺失路径 |
| **Python 代码** | 入口、调用链、Agent 顺序、Adapter 路径 |
| **Markdown 文档** | Contract、PROJECT_STATUS、MODULE_REGISTRY、Execution History |
| **JSON 文件** | commercial_assets 全链、storage JSON |
| **配置文件** | `8_CONFIG/`, requirements, rules |
| **Database** | `data/ai_factory.db` schema 与样本（若可读） |

### 5.2 禁止

| 禁止 | 原因 |
|------|------|
| **只读目录结构推断系统能力** | 目录存在 ≠ 功能已实现 |
| **假设代替代码事实** | 须读 `content_pipeline.py` 等确认行为 |
| **忽略 commercial_assets 内容** | 商业链状态以 JSON 为准 |
| **忽略 Execution History** | Entry 序列是演化事实 |

### 5.3 审计必须包含

| # | 内容 |
|---|------|
| 1 | **文件确认** — 关键路径是否存在、版本 |
| 2 | **代码调用关系确认** — Legacy vs Experiment 路径、MarketAgent bypass |
| 3 | **数据流确认** — PR → Adapter → CF → Validation → Product Asset |
| 4 | **状态流确认** — 文档状态 vs 代码/JSON 实际 |

### 5.4 审计输出格式

最终输出**必须区分**：

| 分类 | 说明 |
|------|------|
| **已确认内容** | 基于代码/JSON/DB 直接读取 |
| **未确认内容** | 文档声明但未验证 |
| **无法读取内容** | 二进制、权限、缺失文件 |

**禁止使用假设代替代码事实。**

---

## 6. User Direction Optimization Rule（用户方向优化规则）

### 6.1 架构方向判断

当用户提出架构方向时，执行 Agent **必须先进行判断**，再执行。

### 6.2 方向正确

若方向与 Work Principles、Module Boundary、Source of Truth 一致：

→ **执行优化**，并在文档/Entry 中记录决策。

### 6.3 方向存在重大缺陷

若方向存在重大缺陷（如混淆 Blueprint 与 Runtime、越界修改禁止模块、伪造商业数据）：

**必须：**

1. **指出问题** — 具体违反哪条治理/契约规则
2. **说明风险** — 长期一致性、审计、回归风险
3. **提供优化方案** — 可执行的替代路径
4. **保留总体战略目标** — 不否定用户商业目标，修正实现路径

### 6.4 禁止

| 禁止 | 说明 |
|------|------|
| **为服从用户直接执行错误架构** | 如未授权修改 Legacy `run(keyword)`、伪造 Feedback |
| **跳过 State Review 宣称 Entry Complete** | 须闭环 §3 |
| **静默扩大 Entry 范围** | 超出任务授权的 Python/DB/JSON 变更 |

---

## 7. Module Boundary Protection（模块边界保护）

### 7.1 模块职责

| 模块 | 职责 | 禁止无限扩张 |
|------|------|--------------|
| **0_START** | 系统启动、Planner、Execution Runtime | 不承担 Content Factory 生产、Commercial Object 登记 |
| **1_DATA** | 数据采集、数据管理 | 不承担 Opportunity 裁决、Product 生产 |
| **2_COGNITION** | 数据理解、分析、机会认知 | 不承担 Production Request 审批、CF 执行 |
| **3_DECISION** | 评分、选择、决策 | 不承担文件验收、Feedback 录入、CF 调度（Pilot 阶段） |
| **11_CONTENT_FACTORY** | 内容生产、商业资产生成（artifact） | 不承担选品（Experiment 路径 bypass Market）、Commercial JSON 权威写回 |
| **7_MEMORY** | 经验沉淀、学习存储 | 不替代 commercial_assets、不直接写 DB 商业表 |

### 7.2 协作原则

| 原则 | 说明 |
|------|------|
| **模块允许协作** | 通过 Contract、Adapter、明确 API 协作 |
| **禁止无限扩张职责** | 新职责须新 Layer/Contract/Entry 授权 |
| **Commercial 链在 commercial_assets** | 不由单模块私有 JSON 定义全链 |
| **Governance 不替代业务** | 本 Layer 约束边界，不实现业务逻辑 |

### 7.3 Adapter / Validation 边界（当前实践）

| 组件 | 位置 | 边界 |
|------|------|------|
| Approval Gate | `11_CONTENT_FACTORY/adapter/` | 生产**前** — 只读 commercial_assets |
| Validation Gate | `11_CONTENT_FACTORY/validation/` | 生产**后** — check only，不写 product_assets（除非单独 Entry 授权） |
| Observation Protocol | `docs/` | 规则层 — 不修改 Feedback JSON（除非 Entry 授权） |

---

## 8. Governance Principle（治理原则）

### 8.1 核心原则

> **System Growth must not exceed Governance Capacity.**  
> 系统复杂度增加时，**优先**增加状态治理、数据治理、文档同步、生命周期管理——**再**扩展功能。

### 8.2 扩展优先级

当系统能力扩展时，优先顺序：

1. **状态治理** — 词汇表、Source of Truth、Entry 闭环
2. **数据治理** — Commercial Object Contract、禁止伪造
3. **文档同步** — PROJECT_STATUS、MODULE_REGISTRY、system_snapshot、Execution History
4. **生命周期管理** — Object 状态机（draft → prepared → … → validated）
5. **功能实现** — Python、Runtime、新 Agent

### 8.3 与 AI_FACTORY_OS 当前阶段对齐（只读快照 — 2026-07-13）

| 能力 | 状态层级 |
|------|----------|
| Commercial 链 Blueprint | Blueprint / Design Completed |
| Adapter + Validation Runtime | Implementation Completed |
| Pilot Production preq_005 | Production Verified（单 Pilot） |
| Feedback / Evaluation 实例 | Implementation（JSON）— 观察 pending |
| Observation Protocol | Blueprint Completed |
| System Governance Protocol | **Blueprint Completed（本 Protocol）** |
| Full Runtime Connected（0_START → CF） | **未连接** |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Work Principles | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
| Project Status | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` |
| System Snapshot | `docs/01_CURRENT_STATE/reference/system_snapshot.md` |
| Execution History | `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` |

---

**Blueprint ≠ Runtime。** **Design ≠ Production。** **Governance Before Expansion.** 本文档完成 System Governance Protocol v1；Governance Runtime 自动化、ZIP 审计工具化均 **Pending**，须后续 Entry 单独授权。


---

# ARCHIVED_HISTORICAL_STATUS

状态：

历史治理参考。

不是当前系统控制文件。

当前治理入口：

00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md
