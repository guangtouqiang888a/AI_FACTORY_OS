# AI_FACTORY_OS Knowledge Update Protocol

> **Knowledge Update Protocol（知识更新协议）**  
> Last updated: 2026-09-04（**Collaboration Continuity Hardening** — NOT Entry 077）

**目的：** 当项目发生重大变化时，规定必须检查与更新哪些核心文件，防止文档再次爆炸或与 Reality（运行现实）漂移。

**Document Role（041-F）：** 变化如何分级更新核心认知。**不是** Current State；更新时须遵守 Constitution **Information Ownership**（DEC-016）— 不在错误文件重复定义。

**适用：** 所有影响认知、状态、架构解释或协作规则的 Entry。  
**不适用：** 未经授权的 Reality 修改（Python / Database / commercial_assets）——此类必须先有明确 Scope（范围）。

**连续性（DEC-019）：** `docs/0–6` 是**当前**核心连续性记录域。历史 Core Governance Set v1（8+1）是结构版本 / 检查清单，≠「完整连续性域仅此 8+1」。变化发生后须与 Execution Protocol 的 **Post-Execution Core Documentation Sync** 配合；长期规则不得只留在聊天中。  
**GitHub：** 版本化 / 协作连续基础设施；**不得**当作 Reality Authority。  
**协作闭环：** 长期协作规则见 Execution Protocol **Collaboration Continuity Workflow**；`Conversation Idea ≠ Execution Authorization`；Cursor PASS 后须 ChatGPT Closure Review 才可 Project Task Closed。
---

## Change Level（变化等级）

每次拟议变化须先判定等级，再决定更新深度。

| Level | 含义 | 通常需要更新 | 用户确认 | DEC |
|-------|------|--------------|----------|-----|
| **Level 0** | 普通文字调整（措辞、错别字、格式） | **无需**核心战略更新 | 一般否 | 否 |
| **Level 1** | 局部功能或流程变化（不改商业方向/原则） | **Current State**（及必要台账） | 任务级 | 通常否 |
| **Level 2** | 系统能力变化（架构能力描述或模块边界变更） | **Unified Architecture** + **Current State** | 是（战略级） | 边界冲突时是 |
| **Level 3** | 商业方向变化 | **Business Strategy** + **Decision Log**（及 Control Center / State） | **必须** | **必须** |
| **Level 4** | 核心原则变化 | **重新审核 Constitution** + **Decision Log**（及受影响协议） | **必须** | **必须** |

### 每次变化必须回答（四问）

1. **改变了什么？**（一句话）  
2. **影响哪些核心文件？**（列出；对照 Core 清单）  
3. **是否需要用户确认？**（Level ≥2 默认是；Level 3–4 强制是）  
4. **是否生成 DEC？**（Level 3–4 强制；战略否决/原则变更强制）  

无法回答四问 → **禁止**擅自改核心认知文件。

---

## 一、触发条件（Trigger Conditions）

以下任一发生，即触发本协议：

| # | 触发类型 | 示例 |
|---|----------|------|
| 1 | **商业方向变化** | 使命级价值路径调整；半自动策略变更；验证主线改变 |
| 2 | **产品方向变化** | 主推资产类型变化；Pilot 策略转向；新产品线立项 |
| 3 | **架构变化** | 分层调整；Core OS ↔ Content Factory 关系变化；融合授权 |
| 4 | **模块变化** | 新模块落盘；职责迁移；入口启用/废弃登记 |
| 5 | **数据结构变化** | Schema / Ownership / commercial_assets 字段或权威域变化 |
| 6 | **AI 工作协议变化** | Bootstrap、可读性、自检、Scope 规则变化；**长期协作规则变化（DEC-019）**；Collaboration Continuity Workflow / Closure Review 规则变化 |
| 7 | **重大错误修正** | P0/P1 问题关闭策略；发现新的系统性错误与避坑规则 |
| 8 | **项目阶段变化** | Current Phase / Primary Goal 跃迁（须更新 Control Center + Current State） |
| 9 | **连续性 / Recovery 规则变化** | Core Documentation Continuity、Recovery 权威路径、Post-Execution Sync 要求变化 |
| 10 | **商业学习 / 发布 / 产品 / 选品 / 价格 / 数据源原则变化** | DEC-020…028：含 Price Intelligence + **Current vs Legacy DB Boundary** |
| 11 | **Git-versioned closure 要求变化** | 任务是否要求 Commit / Push / Remote Verification；失败不得标 PASS |

另外：任何拟修改 **核心认知文件**（见下文核心清单）的行为，默认触发本协议。

### 1.1 必须检查 docs/0–6 的重要变化（DEC-019）

以下事件发生时，必须做 Core Documentation Impact Analysis（不一定改全部文件）：

- 项目阶段 / Primary Goal 变化  
- 商业方向、商业实验状态、产品方向变化  
- Runtime / 模块 / Database / commercial asset Reality 变化  
- 架构边界或模块边界变化  
- 重大技术方案接受/否决；重大问题发现/关闭  
- 新增长期工作协议或修改已有工作协议  
- Governance / Recovery 规则变化  
- 用户与 AI 之间形成新的长期协作约束  
- 任何以后新 AI 必须知道、否则可能错误判断项目状态的重要事项  

**反膨胀：** 只更新受影响文件；未改文件须在 Entry 报告中写明「未修改原因」。

---

## 二、影响分析流程（Impact Analysis Flow）

```
变化提出
    ↓
影响范围判断（哪些域：商业 / 架构 / 状态 / 协议 / 数据）
    ↓
检查核心文件（`docs/0–6` Continuity Domain；可用历史 Core Governance Set v1 清单作评估起点，但须另评估 Module Registry / Execution History / Evolution Context 等受影响文件）
    ↓
生成更新建议（逐文件：改 / 不改 / 仅指针）
    ↓
用户确认（Level 0 用户决策权）
    ↓
Cursor 按 Scope 执行
    ↓
验证（文件存在性、范围未越权、Current State 对齐；**禁止机械全量刷新**）
    ↓
Decision Log 记录（战略级必须写 DEC；仅明确化既有 DEC 时通常不新增 DEC）
```

### 2.1 影响范围判断检查单

- [ ] 是否改变「为什么存在 / 永久原则」？ → Constitution  
- [ ] 是否改变「如何赚钱与如何验证」？ → Business Strategy  
- [ ] 是否改变阶段 / 目标 / 禁止 / 必读 / Recovery 导航？ → Control Center（状态投影须对照 Current State）  
- [ ] 是否改变事实摘要？ → Current State  
- [ ] 是否战略选择或否决？ → Decision Log  
- [ ] 是否改变协作做法？ → Execution Protocol  
- [ ] 是否改变更新规则本身？ → 本文件  
- [ ] 是否改变目标架构描述？ → Unified Architecture  
- [ ] 是否改变裁决顺序？ → Authority Model  
- [ ] 是否仅台账？ → PROJECT_STATUS / snapshot / HISTORY  
- [ ] 是否仅解释「目录为何如此」的历史背景？ → Architecture Evolution Context（**非核心**；不得当 Current State）
- [ ] 是否仅 Audit 证据？ → `07_AUDIT`（**不得**替代 Current State）
- [ ] 是否仅 GitHub 同步？ → 通常不改商业/架构；记录 Execution History；**不得**把 sync 写成 Runtime 完成

### 2.2 核心文件检查清单（必须打开评估）

> 下列 8+1 源自历史 **Core Governance Set v1**（DEC-009），用作 Impact **评估清单**。  
> **当前连续性域仍是整个 `docs/0–6`。** 评估后按影响更新；无影响则 Reviewed-but-Not-Modified。

1. `AI_FACTORY_OS_CONTROL_CENTER.md`  
2. `AI_FACTORY_OS_PROJECT_CONSTITUTION.md`  
3. `AI_FACTORY_OS_CURRENT_STATE.md`  
4. `AI_FACTORY_OS_DECISION_LOG.md`  
5. `AI_FACTORY_OS_BUSINESS_STRATEGY.md`  
6. `AI_FACTORY_OS_EXECUTION_PROTOCOL.md`  
7. `AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md`（本文件）  
8. `AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md`  
9. `AI_FACTORY_OS_AUTHORITY_MODEL.md`（强制卫星）  

**同属 `docs/0–6`、须按影响评估：** `AI_FACTORY_OS_MODULE_REGISTRY.md` · `CURSOR_EXECUTION_HISTORY.md` · `AI_FACTORY_OS_ARCHITECTURE_EVOLUTION_CONTEXT_RECORD.md`（历史解释 only）。

**非 Continuity 权威：** `docs/07_AUDIT`（证据）；GitHub remote 本身（运输层）。

**非核心（可选同步）：** `AI_FACTORY_OS_ARCHITECTURE_EVOLUTION_CONTEXT_RECORD.md` — 仅历史解释；**不得**升格为核心治理文件。

---

## 2.3 文档生命周期意识（Document Lifecycle Awareness）

> Entry **041-D-A**。长期信息变化时，必须先分层，再选择更新对象，避免旧文档覆盖 Reality。

任何长期信息变化，需判断：

1. **变化属于什么层？**  
   - 商业（Business）  
   - 架构（Architecture）  
   - 状态（State / Reality projection）  
   - 规则（Rules / Protocol / Authority）  
   - 历史（Historical explanation）

2. **应该更新哪个核心文件？**（见 §2.2；历史解释 → Evolution Context，非核心）

3. **旧文件是否应该降级为历史参考？**  
   - 若已被 Core / Current State 替代 → 加 Historical Reference 标识  
   - 不得继续用旧 Blueprint「已完成」话术覆盖 Reality

| 层 | 典型写入位置 | 禁止 |
|----|--------------|------|
| 商业 | BUSINESS_STRATEGY（± DEC） | 把愿景写成已完成收入 |
| 架构 | UNIFIED_ARCHITECTURE（± DEC） | Design = Runtime |
| 状态 | CURRENT_STATE（对齐 Reality） | 聊天记忆覆盖状态 |
| 规则 | EXECUTION / KNOWLEDGE_UPDATE / AUTHORITY | 静默改核心规则 |
| 历史 | EVOLUTION_CONTEXT / audit / 旧 Blueprint | 用历史文件覆盖 Reality / Current State |

**避免：** 旧文档覆盖 Reality。

---

## 三、推荐更新顺序（Update Order）

```
1) 核对 Reality（若涉及代码/DB/资产）
2) 用户确认（战略级）
3) Decision Log（若战略 / 永久规则 / 否决）
4) Current State
5) Control Center（阶段 / 目标 / 禁止 / 导航）
6) 受影响的 Constitution / Business Strategy / Unified Architecture / Execution Protocol
7) 本协议（若规则自身变更）
8) PROJECT_STATUS / system_snapshot / CURSOR_EXECUTION_HISTORY（Entry 收尾）
9) L2 参考详文（仅当设计真正变化）
```

---

## 四、触发类型 → 必更映射

| 触发 | 必须检查并通常更新 | 条件写 DEC |
|------|-------------------|------------|
| 商业方向 | Business Strategy；Control Center；Current State | **是** |
| 产品方向 | Business Strategy；Current State；相关 Contract 指针 | 战略级 **是** |
| 架构变化 | Unified Architecture；Current State；Control Center | **是** |
| 模块变化 | Current State；MODULE_REGISTRY（L2）；Unified Architecture 摘要 | 边界冲突时 **是** |
| 数据结构 | Current State；Authority / State Authority 指针；相关 Blueprint | **是**（若改权威域） |
| AI 工作协议 | Execution Protocol；Control Center（若 Bootstrap/禁止变） | **是** |
| 重大错误修正 | Current State；audit/已知问题；必要时 Decision Log 避坑 | 改规则时 **是** |
| 项目阶段变化 | Control Center Phase；Current State；必要时 Business Strategy | 阶段跃迁 **是** |

---

## Documentation Structure Governance Rules

> Entry **044-A** · Documentation Governance Hardening v1  
> 导航入口：[DOCUMENTATION_MAP](../AI_FACTORY_OS_DOCUMENTATION_MAP.md)

### Directory Responsibility Rule

一级目录代表**唯一职责**（见 Documentation Map）。

**禁止：**

- 一个文件承担多个权威职责（例如同一文件既当 Current State 又当 History）
- 一个领域存在多个 Source of Truth（SoT）
- 历史文件（History / Archive / 过时参考）覆盖当前状态（Current State / Reality）

**冲突时：** Reality > Current State > Authority / Core Governance > Blueprint / History / Audit / Archive。

### New File Rule

任何新增 Markdown，创建前必须确认：

1. **文件职责**（Core / Reference / Blueprint / History / Audit / Archive）
2. **所属目录**（对应唯一职责的一级目录）
3. **是否已有同职责文件**（有则优先更新既有文件，禁止平行权威）
4. **是否产生新的权威入口**（禁止第二个 Control Center / 第二部平行宪法 / 平行 Current State）

无法回答上述四点 → **禁止**新建。

### File Migration Rule

任何**移动 / 重命名 / 删除** Markdown，必须同时完成：

1. 修复 Markdown 引用（相对路径与 `docs/...` 字符串）
2. 更新 [DOCUMENTATION_MAP](../AI_FACTORY_OS_DOCUMENTATION_MAP.md)
3. 更新相关索引（Control Center Quick Links、Recovery 路径等）
4. 生成 Audit Report（写入 `docs/07_AUDIT/`，建议 `migration/`）

未完成以上四项 → **禁止**执行迁移。

---

## 五、禁止事项（Forbidden）

1. **AI 未经用户确认修改核心认知**（上列 8+1 文件的原则性/战略性内容）。  
2. 用聊天记忆覆盖 Current State 或 Reality。  
3. 用 PROJECT_STATUS 覆盖 Current State。  
4. 将 Blueprint / Strategy 标记为 Runtime / Production Completed（除非 Reality 证实且用户授权）。  
5. 用 Architecture Evolution Context / 历史 Blueprint **覆盖** Current State 或 Reality。  
6. 把 Evolution Context 新增或改写当成「核心治理升级」而不走分层判断。  
7. 删除历史 Decision 或 audit 证据。  
8. 无 Scope 修改 Python / Database / commercial_assets。  
9. 同任务「顺手」扩大到未授权域。  
10. 新建第二个 Control Center 或第二部平行宪法。

---

## 六、与执行协议的关系

- 日常任务执行：遵守 `AI_FACTORY_OS_EXECUTION_PROTOCOL.md`（含 Human Readability、Self Review Gate）。  
- 认知/状态同步：遵守**本协议**。  
- 两者冲突时：先停，交用户确认；默认不得静默改核心认知。

---

## 七、验证最低标准（Entry 收尾）

- [ ] 声明的触发类型已覆盖  
- [ ] 核心清单已逐项判断  
- [ ] 用户确认记录（任务说明或 DEC）  
- [ ] Python / Database / Commercial Assets 变更符合 Scope（040-D1 类 Docs-only 必须为 0）  
- [ ] Current State 与 Reality 无已知矛盾被故意忽略  
- [ ] 战略变更已写入 Decision Log  

---

**Entry 040-D1：** Knowledge Update Protocol foundation created（知识更新协议基础已建立）。  
**Entry 040-F-A：** Change Level（变化等级）与四问检查已加入。  
**Entry 041-D-A：** 文档生命周期意识（§2.3）；Evolution Context 标为非核心历史层。  
**Entry 044-A：** Documentation Structure Governance Rules（目录职责 / 新建 / 迁移）。



## Documentation Structure Governance v2

### New File Placement Rule

创建新的 Markdown 文件前必须判断：

1. 文件角色
2. 权威等级
3. 生命周期

必须进入对应目录。

禁止：

- 默认放入 docs 根目录
- 在已有职责文件外创建平行权威文件
- 用新文件替代旧权威文件而不迁移

---

### Change Synchronization Rule

当 Reality、Runtime、商业方向、架构能力发生变化：

必须同步更新：

1. Current State
2. Module Registry（如涉及模块）
3. 对应 Architecture / Business / Blueprint 文件

**Collection / Provenance 同步（Entry 058B / DEC-029）：**

当 Source Registry、Collection Mode（LIVE / IMPORT / FIXTURE）、第一批真实 Observation、或 LIVE 可用性变化时：

必须同步 Current State + Module Registry + Unified Architecture + Execution History；必要时 Decision Log / Constitution。

**Own Product / Rights 同步（Entry 058E / DEC-030）：**

当 `product_origin` / `rights_status` / Business Model 维度或 Own Product 边界变化时：

必须同步 Constitution / Decision Log / Current State / UA（如适用）。

**Acquisition Engine 同步（Entry 059 / DEC-031）：**

当 Engine 状态、Xianyu mode 可用性、第一批 REAL 采集、或 Policy 边界变化时：

必须同步 Current State / Module Registry / UA / Execution History。

**Browser Collector 同步（Entry 060）：**

当 PUBLIC_WEB_READ 从 NOT_FEASIBLE → LIMITED / BLOCKED / ACTIVE 变化时：同步 Current State + Module Registry + UA + Execution History。不得把 ACCESS_DENIED 记成 FIRST_REAL 成功批次。

**Interactive Browser 同步（Entry 061）：**

有界面采集候选批次出现或 collector status 变化时：同步 Current State / Module Registry / UA / Execution History。test-dir candidates ≠ Current DB observations。

**Search Origin / Missing Fields 同步（Entry 062 / DEC-032）：**

当 SEARCH_RESULT 可用性、want_count 状态模型、或「推荐误作搜索」边界变化时：同步 Constitution / Decision Log / Current State / UA / Execution History。

**Search Session 同步（Entry 063）：**

Search Control 与 Collector 可行性分别变化时：同步 Current State / Module Registry / UA / Execution History。不得把 EMPTY+推荐写成 SEARCH_RESULT 成功。

**Extension Forensics / Blueprint 同步（Entry 064）：**

参考插件分析、MarketRecord contract、Bridge 方案、KEEP/REWRITE/REMOVE 决策变化时：同步 UA / Current State / Module Registry / Execution Protocol / Execution History。Extension contract version 与 collector_version 须与 KUP 对齐。

**Browser Extension v1 同步（Entry 065）：**

Extension/Bridge 实现状态、collector `col_xianyu_browser_extension`、test sink 路径变化时：同步 Current State / Module Registry / UA / Execution Protocol / Execution History。test sink ≠ Current DB observations。

**Import Gate / WORK_PRINCIPLES 同步（Entry 066）：**

Import gate、`AI_FACTORY_OS_WORK_PRINCIPLES.md`、Core File Creation 规则变化时：同步 Documentation Map / Control Center / Execution Protocol / Execution History。

禁止：

文档长期停留在旧状态；把 EXTERNAL_IMPORT 写成 LIVE_COLLECTION；把 SAMPLE 写成 REAL；把公开网页可行性测试写入 Current DB 当正式市场数据。

---

### Chinese Annotation Rule

面向人类维护的核心 Markdown：

必须包含必要中文说明。

英文名称用于：

- 模块名
- 标准名
- 技术术语

中文说明用于：

- 文件职责
- 状态解释
- 使用边界

目标：

Human + AI 均可正确理解。


---

# Documentation Integrity Hardening

所有 Markdown 必须属于：

A Core Authority
B Active Reference
C Historical
D Audit Evidence
E Archive


禁止：

- 创建重复权威文件
- 随意新增根目录 MD
- 创建无维护责任文件


所有新文件必须：
中文说明 + English Standard Name。


Folder ≠ Authority。

权威由文件职责决定。

---


# Human-Machine Readability Standard
# 人机共同阅读标准


AI_FACTORY_OS 文档必须同时满足：

1. Machine Readable
机器可识别

2. Human Readable
人类可理解


## File Naming Rule
文件命名规则


保持：

English Standard Name

原因：

- 工程搜索
- Cursor识别
- 自动化处理


## Content Language Rule
内容语言规则


所有新增或修改文档：

必须：

- 中文解释优先
- 英文术语保留
- 禁止纯英文治理说明


标准格式：

English Title
（中文说明）


Purpose
用途说明


Rules
规则说明



---


# Document Update Propagation Rule
# 文档变化传播规则


任何以下变化发生：

- 商业方向变化
- 架构变化
- 模块状态变化
- Blueprint进入实现阶段
- Runtime状态变化
- 模块冻结或废弃


必须检查以下文件是否需要同步：


1. CURRENT_STATE
（当前事实）


2. MODULE_REGISTRY
（模块状态）


3. UNIFIED_ARCHITECTURE
（架构影响）


4. BUSINESS_STRATEGY
（商业影响）


5. DECISION_LOG
（决策记录）


6. AUDIT
（变化证据）


禁止：

只修改单个文件，
导致系统知识分裂。



---


# 044-H 文档更新传播规则


## 核心原则

任何重要变化必须同步对应权威文件。

不能只修改一个说明文件。


---

## 商业变化


商业方向变化：

必须更新：

1.
BUSINESS_STRATEGY


2.
CURRENT_STATE


3.
MODULE_REGISTRY


4.
生成对应 AUDIT 记录



---

## 架构变化


架构变化：

必须更新：

1.
UNIFIED_ARCHITECTURE


2.
相关 BLUEPRINT


3.
MODULE_REGISTRY


4.
生成 AUDIT 记录



---

## 模块状态变化


模块：

Created / Active / Frozen / Deprecated


必须更新：

MODULE_REGISTRY


不得只修改 Blueprint 或 History。



---

## 新增 Markdown 文件规则


任何新增文件必须：

1.
明确所属目录


2.
说明维护责任


3.
说明更新条件


4.
中文解释 + English Standard Name


禁止：

创建无维护责任文件。

