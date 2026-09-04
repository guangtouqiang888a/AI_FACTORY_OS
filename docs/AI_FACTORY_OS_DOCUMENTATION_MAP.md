# AI_FACTORY_OS Documentation Map

> **文档唯一导航入口（Documentation Navigation SoT）**  
> Entry **044-A** · Hardening · Entry **044-B** · Physical Consolidation · Entry **045** Minimal Core · Entry **046** Continuity  
> Last updated: 2026-09-03（Entry **067**）

**本文件职责：** AI_FACTORY_OS 文档结构与阅读边界的**唯一导航入口**。  
**不替代：** Reality（Code / DB / Assets / Runtime）· Current State · Authority Model · Control Center 会话协议细节。

**关联：** 会话入口仍为 [CONTROL_CENTER](./00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md)。  
**Recovery 权威（唯一）：** Control Center 内 **New Session Recovery Protocol（DEC-017）** + **AI Recovery Reading Boundary**；本 Map 只做导航。  
旧索引（已归档）：[Documentation Map Reference History](./99_ARCHIVE/AI_FACTORY_OS_DOCUMENTATION_MAP_REFERENCE_HISTORY.md)。

---

## 1. 文档目录职责说明

| 目录 | 唯一职责 |
|------|----------|
| `00_GOVERNANCE/` | 核心治理 only（Control Center / Authority / Constitution / Decision / Execution Protocol / Knowledge Update） |
| `01_CURRENT_STATE/` | **仅** Current State + Module Registry（现行 Reality 文档投影） |
| `02_ARCHITECTURE/` | 架构入口 UNIFIED_ARCHITECTURE；Supporting detail 见 §1.3 |
| `03_BUSINESS/` | **仅** BUSINESS_STRATEGY（现行商业方向） |
| `05_EXECUTION/` | **仅** CURSOR_EXECUTION_HISTORY（执行连续性台账）；**不是**系统状态来源 |
| `06_HISTORY/` | 历史解释 only（不得覆盖 Current State） |
| `07_AUDIT/` | 验证证据；子类见下 |
| `99_ARCHIVE/` | 冻结历史参考（默认不参与判断）；含 `blueprint_history/`（原 04_BLUEPRINT）、execution/old_history/legacy 等 |

> **注（045/046）：** 现行最小核心不再保留活动态 `04_BLUEPRINT/`。Blueprint 设计文位于 `99_ARCHIVE/blueprint_history/`（≠ Production）。

### 1.1 Blueprint 归档位置（原 04_BLUEPRINT）

| 子目录（在 archive 下） | 内容 |
|------|------|
| `99_ARCHIVE/blueprint_history/commercial/` | 商业验证 / Experiment / Opportunity / Monetization 设计 |
| `99_ARCHIVE/blueprint_history/runtime/` | Content Factory / Cognition / Integration / Validation Gate 设计 |
| `99_ARCHIVE/blueprint_history/database/` | Schema / DB 演进与迁移设计 |
| `99_ARCHIVE/blueprint_history/contract/` | 商业对象契约 |
| `99_ARCHIVE/blueprint_history/protocol/` | 观察 / 人辅 / Review 协议 |
| `99_ARCHIVE/blueprint_history/policy/` | 生命周期 / 状态权限策略 |

### 1.2 `07_AUDIT/` 子类

| 子目录 | 内容 |
|------|------|
| `structure/` | 文档结构 / 知识治理审计 |
| `runtime/` | Reality / Runtime / 模块审计 |
| `database/` | DB / Schema 审计 |
| `migration/` | 迁移计划与执行证据 |
| `commercial/` | 商业状态 / 字段对齐报告 |
| `validation/` | 验证与验收报告 |
| `asset/` | 资产审计 |

### 1.3 `02_ARCHITECTURE/` Supporting Detail（Entry 066）

| 文件 | 角色 |
|------|------|
| [UNIFIED_ARCHITECTURE](./02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) | **Core** — 架构总入口 |
| [XIANYU_BROWSER_EXTENSION_BLUEPRINT_064](./02_ARCHITECTURE/XIANYU_BROWSER_EXTENSION_BLUEPRINT_064.md) | **Supporting Architecture Detail** — Xianyu Extension + Bridge 长期设计；Recovery 按需读取；非重复 UA |

### 1.4 根目录协作准则

| 文件 | 角色 |
|------|------|
| [WORK_PRINCIPLES](./AI_FACTORY_OS_WORK_PRINCIPLES.md) | **Reference（现行对齐）** — 协作方法；含 Browser-Native Acquisition、Acquisition Policy、AI Cost 原则；冲突以 `00_GOVERNANCE` 为准；Archive 版见 `99_ARCHIVE/` |

**Acquisition Policy / AI Cost Gate（Entry 067）：** 实现于 `1_DATA/acquisition_engine.py` + `1_DATA/ai_cost_gate.py`；架构说明见 Unified Architecture；详细证据见 `07_AUDIT/ENTRY_067_...md`。

---

## 2. 默认 AI Recovery Reading Order

### 优先读取（默认恢复）

| 目录 | 文件 |
|------|------|
| `00_GOVERNANCE/` | [CONTROL_CENTER](./00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md) |
| `00_GOVERNANCE/` | [AUTHORITY_MODEL](./00_GOVERNANCE/AI_FACTORY_OS_AUTHORITY_MODEL.md) |
| `01_CURRENT_STATE/` | [CURRENT_STATE](./01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) |
| `01_CURRENT_STATE/` | [MODULE_REGISTRY](./01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) |
| `02_ARCHITECTURE/` | [UNIFIED_ARCHITECTURE](./02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md) |
| `03_BUSINESS/` | [BUSINESS_STRATEGY](./03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md) |

建议先读本 Map，再进入 Control Center Recovery（DEC-017）与 AI Recovery Reading Boundary（044-A）。连续性要求见 **DEC-019**。

按需补齐：`05_EXECUTION/CURSOR_EXECUTION_HISTORY.md`（最近做到哪里）、`00_GOVERNANCE` 内 Decision / Execution / Knowledge Update Protocols、`06_HISTORY` Evolution Context。

### 条件读取（按任务 Scope）

| 目录 | 何时读取 |
|------|----------|
| `99_ARCHIVE/blueprint_history/` | 未来规划 / 契约 / 协议设计（≠ Production） |
| `05_EXECUTION/` | 执行台账与推进连续性 |
| `06_HISTORY/` | **仅**历史形成原因 |
| `07_AUDIT/` | 验证证据 |

### 默认不参与判断

| 目录 | 规则 |
|------|------|
| `99_ARCHIVE/` | **默认不读取**（含旧 WORK_PRINCIPLES、旧 Recovery Read Order） |

---

## 3. 文件角色定义

| 角色 | 含义 |
|------|------|
| **Core** | 核心权威 |
| **Reference** | 辅助说明 / 非权威快照 |
| **Blueprint** | 设计规划（≠ Production；现多位于 Archive） |
| **History** | 历史解释 |
| **Audit** | 验证证据 |
| **Archive** | 冻结历史 |

---

## 4. 结构治理指针

[KNOWLEDGE_UPDATE_PROTOCOL — Documentation Structure Governance Rules](./00_GOVERNANCE/AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md)  
[CONTROL_CENTER — AI Recovery Reading Boundary + New Session Recovery Protocol](./00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md)  
[044-B Consolidation Report](./07_AUDIT/migration/ENTRY_044_B_DOCUMENTATION_PHYSICAL_CONSOLIDATION_REPORT.md)  
[045-A Minimal Core Consolidation](./07_AUDIT/migration/ENTRY_045_A_DOCUMENTATION_MINIMAL_CORE_CONSOLIDATION_REPORT.md)

---

**Entry 044-A：** Documentation Map established.  
**Entry 044-B：** Physical Consolidation — Blueprint/Audit 子类与 Business/Architecture 边界硬化。  
**Entry 045：** Minimal Core — Blueprint / 辅助 Execution / 旧 reference 归档。  
**Entry 046：** Core Documentation Continuity Rule（DEC-019）。



## AI Reading Boundary（AI读取边界）

AI_FACTORY_OS 文档读取必须遵循以下顺序：

1. 00_GOVERNANCE
   - 系统规则
   - 权威模型
   - 决策与执行规则

2. 01_CURRENT_STATE
   - 当前 Reality 文档入口
   - 模块实际状态

3. 02_ARCHITECTURE
   - 当前架构原则

4. 03_BUSINESS
   - 当前商业方向

5. 05_EXECUTION
   - 执行记录与推进连续性

6. 06_HISTORY
   - 历史背景解释

7. Blueprint（归档）
   - `99_ARCHIVE/blueprint_history/` 设计与规划参考

禁止默认使用：

- 07_AUDIT 作为系统事实来源
- 99_ARCHIVE 作为当前规则来源

原则：

Reality > Current State > Core Governance > Blueprint > History > Archive

---

## Document Maintenance Rule

任何具有持续价值的 Markdown 文件必须满足：

1. 有明确职责
2. 有唯一归属目录
3. 有维护责任
4. 状态变化时同步更新

禁止：

- 创建无归属 Markdown
- 创建重复权威入口
- 创建长期无人维护的状态文件

## Continuity Rule Pointer（DEC-019）

项目连续性不依赖 Conversation Memory。正式 Entry 必须完成 Post-Execution Core Documentation Sync（见 Execution Protocol）。
