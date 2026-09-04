# AI_FACTORY_OS Execution Protocol

> Collaboration Control — ChatGPT + Cursor task execution rules（协作控制 — 执行规则）  
> Last updated: 2026-09-04（**PHASE 2 / GOVERNANCE IMPLEMENTATION** — Intent Continuity + Collaboration Model — NOT Entry 077）

Applies to every Entry / implementation task unless the task document overrides with **explicit** authorization（除非任务明确授权覆盖）。

**Document Role（041-F）：** AI 如何执行任务（Scope、门禁）。**不是** Reality 状态 SoT；**不是**架构目标定义正文。  
重要 Reality 变更后须按 Constitution **Architecture State Change Synchronization** 同步 MODULE_REGISTRY / CURRENT_STATE（DEC-016）。

Session start must follow **Session Bootstrap Protocol（会话启动协议）** and **Session Bootstrap Required Reading Order** in Control Center before proposing architecture or execution tasks.

---

# Collaboration Continuity Workflow（协作连续性工作流）

> **NOT Entry 077.** 本节目的：ChatGPT ↔ 用户确认 ↔ Cursor ↔ GitHub ↔ ChatGPT Closure Review 闭环 + **Task Intent Continuity**（DEC-016 / 017 / 019）。  
> **不是**新架构层；**不是**新 Core 文件；**不是**新 DEC。

## Workflow（协作闭环）

```text
ChatGPT
↓ Governance / Reality / Original Objective Recovery
↓ Intent Continuity Gate（多步骤任务）
↓ Task Analysis / Scope Definition
↓ AI Self Review / Cognitive Integrity Check
↓ 用户确认（需要确认的任务）
↓ Cursor（Local Reality Execution Agent）
↓ Reality Verification → Execution → Validation
↓ Core Documentation Impact Check
↓ Formal Audit（docs/07_AUDIT）+ Execution History
↓ Git Commit → GitHub Push → Remote Verification（若任务要求）
↓ ChatGPT Closure Review（独立）
↓ Project Task Closed / PASS_WITH_FINDINGS / RETRY_REQUIRED
```

## Four-Layer Responsibility Model（四层职责模型）

```text
Layer 1 — Human Intent
  用户：目标 / 方向 / 授权 / 重大决策

Layer 2 — Cognitive Governance
  ChatGPT：理解 / 恢复 / 分析 / Scope / 编排 / Intent Continuity / Closure Review

Layer 3 — Local Reality Execution
  Cursor：本地 Reality / 修改 / 测试 / Git / 持久化证据

Layer 4 — Shared Version Continuity
  GitHub：版本 / 跨 Session / 共享证据
```

不得将四层混成一个角色。

## Responsibility Boundary（责任边界）

### ChatGPT — Cognitive / Governance / Orchestration

负责：Governance Recovery；Reality / Current State Recovery；**Original Objective Recovery**；**Task Intent Continuity**；任务分析；Scope / Out of Scope；AI Self Review；AI Cognitive Integrity Check；Cursor-ready instruction；GitHub 文档审计 / 治理一致性 / 历史链分析（ChatGPT 能经 GitHub 完成的，**不得机械委托 Cursor 重复**）；收到执行结果后的**独立 Closure Review**。

```text
Conversation Idea ≠ Execution Authorization
```

**硬规则：** ChatGPT 不得把 GitHub 文档状态误认为本地 Runtime Reality；需要本地 Reality 的检查仍必须交给 Cursor。

### 用户（User Gate）— Human Decision / Authorization

负责：原始目标；项目/商业方向；重大决策；必要授权；高风险外部不可逆行为确认。

**明确：** 用户**不承担**技术 Reality 核验、Runtime 验证、Git diff 判断、Commit 技术审查、Audit 编写、Cursor 输出整理等技术执行职责。  
用户确认 **≠** 免除 ChatGPT / Cursor 的 Governance / Reality 检查。

### Cursor — Local Reality Execution Agent

负责：本地文件 / Runtime / Code / DB / Assets Reality 检查；按 Scope 修改；本地测试与验证；Git 操作；Formal Audit 落盘；Execution History；Core Documentation Impact Check；按任务要求 Commit / Push / Remote Verification。

**不承担：** 项目最终治理裁决；Original Objective 最终解释权；商业方向决定；用 PASS 直接宣布 Project Task Closed；替代 ChatGPT Closure Review。

```text
Cursor = Execution Agent
Cursor ≠ Project Brain
Cursor reports PASS ≠ Project Task Closed
```

### GitHub — Shared Continuity Infrastructure

负责：Versioning；跨 Session 连续性；共享 baseline；Commit history；Remote evidence；ChatGPT 可读取的连续性载体。

```text
GitHub ≠ Runtime Reality
GitHub ≠ DB Reality
GitHub ≠ Commercial Success
GitHub ≠ Reality Authority
Local Reality ≠ Git Commit ≠ GitHub main
```

若任务要求 **Git-versioned closure**：`Local Validation → Commit → Push → Remote Verification`。  
全部完成前不得声称 Git-versioned closure = PASS。失败 → `REMOTE_VERIFICATION = DEGRADED / RETRY_REQUIRED`。

## Audit Role + Process Output Separation（审计与过程输出分层）

### Formal Audit

Audit = Execution Evidence。必须落盘：`docs/07_AUDIT/*.md`。  
记录：做了什么 / 没做什么 / Scope / Reality Changes / Validation / Core Documentation Impact / Git 状态 / 风险 / 未完成事项。

```text
Audit ≠ Current State
Formal Audit ≠ ChatGPT Closure Review
```

Audit 事实须经 Core Documentation Impact Check 后，按 Information Ownership（DEC-016）同步。

### Cursor Process Output（执行过程输出）

Agent 窗口中的搜索结果、中间分析、命令输出、重复扫描、阶段性判断、Debug、临时总结 = **PROCESS OUTPUT**。

```text
Cursor Process Output ≠ Formal Audit
Process Output ≠ Current State
Process Output ≠ Execution History
Process Output ≠ Project Task Closed 唯一证据
```

**不要求**用户把全部过程输出转发给 ChatGPT。  
**Audit 最小化：** 正式交付 = 必要执行/测试结果 + Formal Audit + Execution History +（若要求）Git evidence；ChatGPT 能经 GitHub 自查的内容，不要求 Cursor 再复制成长报告。

## Task State Model（状态不得混用）

```text
Execution Started
Execution Completed
Local Validation Passed
Audit Generated
Core Documentation Synced
Git Commit Created
GitHub Push Succeeded
Remote Verification Passed
ChatGPT Closure Reviewed
Project Task Closed
```

以下**单独任一**均 ≠ 任务完成：Cursor PASS · Execution Completed · Local Validation · Audit Generated · Git Commit · GitHub Push。  
**Project Task Closed** = 任务规定的全部闭环条件已满足，并经 **ChatGPT Closure Review**。

```text
PHASE_N PASS ≠ PROJECT TASK CLOSED
```

## ChatGPT Closure Review（最终闭环审查）

Cursor 返回后，ChatGPT **不得**仅凭 `STATUS: PASS` 宣布任务完成。至少检查：

1. Scope 是否遵守；是否 Scope Creep  
2. **Original Objective / Current Objective 是否仍对齐**  
3. Reality 是否发生预期变化；不允许修改的文件是否未改  
4. Current State / Module Registry / Decision Log / Architecture / Business Strategy 是否需要/已同步  
5. Execution History 是否更新（含 Intent Continuity 字段，若适用）  
6. Formal Audit 是否存在且内部一致  
7. Git commit / push / remote verification（若要求）  
8. 是否错误启动 Entry 077 / 越权开发  
9. 是否出现新的 Governance Drift / Intent Drift  

通过后才可给出：`PROJECT TASK CLOSED` / `PASS_WITH_FINDINGS` / `RETRY_REQUIRED`。

---

# Task Intent Continuity Model（任务意图连续性模型）

> PHASE 2。每一个跨多个 Step / Phase 的正式任务必须具备可恢复意图状态链。  
> Intent Continuity **不改变** Authority hierarchy：Reality > Current State > Decision Log > Documentation > Conversation Memory。

## Required Fields

```text
ORIGINAL OBJECTIVE
CURRENT OBJECTIVE
SCOPE
OUT OF SCOPE
CURRENT PHASE
CURRENT STEP
COMPLETED
FINDINGS
DECISIONS
PENDING
NEXT STEP
STOP CONDITIONS
FINAL COMPLETION CRITERIA
EVIDENCE
```

### ORIGINAL OBJECTIVE

任务最初为什么开始。必须在任务开始时确定。  
多步骤期间 **不得**被 Finding / Next Step / Entry 自动覆盖。  
仅当用户明确改变任务目的时才可改变，并记录 `Original Objective Changed` + 原因。  
ChatGPT 在每一后续 Step 进入前必须检查当前工作是否仍服务于 Original Objective。

### CURRENT OBJECTIVE

当前 Phase / Step 正在解决什么。允许变化，但必须证明：

```text
CURRENT OBJECTIVE → 服务于 → ORIGINAL OBJECTIVE
```

无法证明 → **STOP**。不得因“Finding 看起来更重要”自动改变总任务。

### CURRENT PHASE / CURRENT STEP

必须说明任务链位置。禁止只写 `Next: xxx` 而不说明：为什么现在做、属于哪个 Phase、如何服务 Original Objective。

### COMPLETED / PENDING / NEXT STEP

描述**任务链**，不是只描述最后一次 Cursor 操作。

### STOP CONDITIONS

明确：何时停止；何时不能继续；何时需用户重新授权；何为 Scope Creep；何种 Finding 应只记录不处理。

### FINAL COMPLETION CRITERIA

真正任务完成条件。不得把 Cursor PASS / Audit / Commit / Push 单独当作完成。

### EVIDENCE

每个重要状态由 Reality / Audit / Commit / History 等证据支持。

## Intent Continuity Gate（意图连续性门）

重大多步骤任务进入下一 Step / Phase 前，ChatGPT 必须执行：

```text
Original Objective Check
→ Current Objective Check
→ Scope Check
→ Current Step Check
→ Next Step Alignment Check
→ Final Completion Path Check
```

必须回答：Original / Current Objective；Current Step；为何仍属 Original；Next Step 及为何仍属 Original；Finding 是否仅为 Finding；是否 Scope Creep；是否朝 Final Completion Criteria 前进。

```text
PASS → Continue
FAIL → Stop / Re-scope
UNCERTAIN → Recover Governance / User Clarification
```

## Finding ≠ Objective（发现 ≠ 目标）

```text
Finding ≠ Objective
Finding ≠ Authorization
Finding ≠ Scope Expansion
Finding ≠ New Entry
Finding ≠ New Phase
```

发现新问题：

```text
Finding → Impact Assessment → 是否阻碍 Original Objective？
  YES（且在当前授权 Scope 内）→ 可处理
  NO → 记录 Finding / Pending，不自动处理
  OUTSIDE SCOPE → 等待用户授权
```

禁止：`Finding → 自动改变任务方向`。

## Binding（绑定）

多步骤正式任务的 Intent 字段必须出现在：

1. Cursor-ready Instruction（开始时）  
2. Formal Audit（`docs/07_AUDIT/*.md`）  
3. `CURSOR_EXECUTION_HISTORY` 新记录（见模板）  
4. Control Center **Active Task Anchor**（指针，非正文 SoT）

不得只留在 Conversation Memory（DEC-019）。

---

## Before Execution（执行前检查）

Define and confirm:

| Item | 中文 | Requirement |
|------|------|-------------|
| **Goal** | 任务目标 | One clear outcome（单一清晰结果） |
| **Scope** | 范围 | Allowed files / domains（允许的文件/域） |
| **Out of Scope** | 范围外 | Explicit exclusions（明确排除） |
| **Expected Result** | 预期结果 | Artifacts / state changes expected |
| **Validation** | 验证 | How success is checked |
| **Rollback** | 回滚 | How to undo or freeze if wrong |

Read minimum:

1. Control Center（控制中心）  
2. Current State（当前状态）  
3. This Protocol（本协议）  
4. Task brief（任务说明）  

If Scope conflicts with Forbidden Actions in Control Center → **stop and ask（停止并询问）**.

Before producing a major plan for user review → pass **AI Self Review Gate（AI自检门）**.  
Before **entering major execution** → pass **AI Cognitive Integrity Check（AI认知完整性检查）**.  
User-facing text → follow **Human Readability Rule（人类可读规则）**.

---

# Human Readability Rule（人类可读规则）

所有提供给**用户审核**的内容，包括：

- Cursor 执行指令  
- 架构方案  
- 项目规则  
- 重要决策  

必须满足：

### 1. 中文为主要表达语言

正文、结论、理由以中文为主；必要时保留规范英文技术词，但须附中文。

### 2. 英文技术词必须附中文解释

**错误：** Task Goal  

**正确：** Task Goal（任务目标）

**错误：** SoT  

**正确：** SoT（Source of Truth，事实唯一来源）

### 3. 禁止用户无法理解的缩写

首次出现须写出全称 + 中文；后续可用简称。  
例：CF → Content Factory（内容工厂）；PR → Production Request（生产请求）

### 4. 用户必须能理解四件事

| 问题 | 要求 |
|------|------|
| **为什么做** | 与当前阶段 / Primary Goal（最高优先级目标）对齐 |
| **做什么** | 范围清晰 |
| **不做什么** | Out of Scope（范围外）写明 |
| **完成标准** | Validation（验证）可检查 |

不满足本规则的用户审核材料 → **不得提交审核**，须改写后再出。

---

# AI Self Review Gate（AI自检门）

任何**重大方案**输出前（架构方案、大范围 Entry 计划、迁移执行方案等），必须自检：

| # | 检查 | 问题 |
|---|------|------|
| 1 | **目标检查** | 是否符合当前阶段目标（Current Phase / Primary Goal）？ |
| 2 | **范围检查** | 是否扩大任务范围（Scope creep）？ |
| 3 | **必要性检查** | 是否现在必须做？ |
| 4 | **理解检查** | 用户是否能够理解方案（符合人类可读规则）？ |
| 5 | **风险检查** | 是否可能产生新的长期维护问题？ |
| 6 | **连续性检查** | 是否符合已有 Decision Log（决策日志）？ |

### 失败处理

若**任意一项**检查失败：

- **禁止**直接输出该重大方案给用户拍板执行  
- **必须**重新调整方案后再次通过本门  

### 通过记录（建议）

重大方案可在报告中声明：`AI Self Review Gate: PASSED`（六项检查通过）。

---

# AI Cognitive Integrity Check（AI认知完整性检查）

**重大方案进入执行前**必须回答下列问题。任一项无法回答或答案不合格 → **禁止进入执行**。

| # | 检查 | 要求 |
|---|------|------|
| 1 | **我的判断来自哪里？** | 必须标明来自 **Core**（核心治理）/ **State**（Current State）/ **History**（历史证据）中的哪一类；**禁止**仅写「来自本聊天」。 |
| 2 | **是否违反 Decision Log？** | 对照 DEC（尤其 DEC-006/007/008/011/012）；冲突则停止或提请用户新 DEC。 |
| 3 | **是否扩大 Scope？** | 相对任务授权范围；扩大必须用户显式批准。 |
| 4 | **是否改变商业目标？** | 若会改变 → 至少 **Change Level 3**，须更新 Business Strategy + DEC，并经用户确认。 |
| 5 | **是否需要更新知识治理文件？** | 按 Knowledge Update Protocol 的 Change Level 与四问判断；该更不更则不得结案。 |

### 失败处理

- **禁止进入执行**  
- 回到 Bootstrap 必读顺序或请用户澄清后再检  

### 通过记录（建议）

`AI Cognitive Integrity Check: PASSED`

---

## During Execution（执行中）

1. **Do not expand scope（禁止扩范围）** without user authorization in the same task.
2. Prefer Reality (code/DB/assets) over prior summary（现实优先于旧摘要）.
3. If unrelated problems appear（发现无关问题）:
   - **Do not fix（不修复）**
   - Record in `docs/audit/` or `docs/known_issues/` only（仅记录）
4. Do not modify Python / DB / commercial_assets unless Scope lists them.
5. Keep Pilot IDs and product assets intact unless Scope lists migration.
6. Prefer additive documentation over deletion.
7. Do not change project direction from chat alone（DEC-012）.

---

## After Execution（执行后）

1. Produce **Entry / Execution Report（执行报告）** with:
   - New files（新增文件）
   - Modified files（修改文件）
   - Python Yes/No
   - Database Yes/No
   - Commercial assets Yes/No
   - Validation（验证）
   - Risks（风险）
   - Next step（下一步）
2. **必须**完成下方 **Post-Execution Core Documentation Sync**（文档同步是 Entry 完成条件的一部分，不是可选收尾）。
3. Update **Current State** if factual status changed.
4. Update **CURSOR_EXECUTION_HISTORY** when Entry-level work completes（`PROJECT_STATUS` / `system_snapshot` 若仍存在仅为辅助；不得替代 Current State）。
5. Add **Decision Log** entry only if a durable decision was made.
6. Do not mark Implementation Completed when only Blueprint/Strategy was produced.
7. Apply Knowledge Update Protocol Change Level if cognition/state changed.
8. 若任务要求 Git-versioned closure：完成 Commit → Push → Remote Verification（见上方 Collaboration Continuity Workflow）。
9. Cursor 报告完成后，仍须等待 **ChatGPT Closure Review**；不得自称 Project Task Closed。

用户可见报告须遵守 **Human Readability Rule（人类可读规则）**.

---

# Post-Execution Core Documentation Sync
# 执行后核心文档同步

> Entry **046** / **DEC-019**。  
> **Documentation Sync 是 Entry 完成条件的一部分。不得作为「可选收尾」。**

每一个正式 Cursor Entry 完成以后，必须：

```text
Reality Verification
↓
Reality Change Detection
↓
Core Documentation Impact Analysis
↓
Update Required Core Files
↓
Update Execution History
↓
Check Current State
↓
Check Module Registry
↓
Check Decision Log
↓
Check Architecture
↓
Check Business Strategy
↓
Check Governance / Protocol
↓
Final Core File Impact Report
```

## Core Documentation Continuity Check（每次 Cursor Entry 必须包含）

以后所有 AI_FACTORY_OS Cursor Entry（及正式治理硬化任务），都必须包含本检查。Cursor 至少须：

1. 判断本次工作影响哪些 `docs/0–6` 文件（**Core Documentation Impact Check**）  
2. 更新必要核心文件（**仅受影响者**）  
3. 更新 `CURSOR_EXECUTION_HISTORY`  
4. 若 Current State 变化 → 更新 Current State  
5. 若模块 Reality 变化 → 更新 Module Registry  
6. 若发生重大决策 → 更新 Decision Log  
7. 若架构认知变化 → 更新 Unified Architecture  
8. 若商业战略/阶段变化 → 更新 Business Strategy  
9. 若工作协议 / Recovery / Continuity 规则变化 → 更新相关 Governance  
10. 最后列出：

```text
Modified Core Files
Reviewed but Not Modified Core Files
Reason for Each
```

### Impact Check 强制纪律

- **禁止**机械更新全部核心文件  
- **禁止**仅因文件日期旧而强制刷新  
- **禁止**用单个 Audit 覆盖其他文件的 Information Ownership  
- **Audit ≠ Current State** — Audit 事实须经 Sync 后才进入状态投影  
- **GitHub ≠ Reality Authority** — sync / commit 不等于 Runtime 完成或商业成功  
- Control Center 状态投影若需更新，仍须与 Current State 对齐，不得让投影成为独立 SoT  

### Modified Core Files（强制格式）

```text
文件：
修改原因：
```

### Reviewed but Not Modified Core Files（强制格式）

```text
文件：
未修改原因：
```

**禁止**只输出「文档已同步。」

### 反膨胀（Impact-Based Updates Only）

「`docs/0–6` 是核心连续性记录域」≠「每一个 Entry 都要修改 0–6 的全部文件」。

| Entry 类型（示例） | 通常需要 |
|--------------------|----------|
| 普通技术 Entry | Current State · Module Registry · Execution History |
| 商业实验 Entry | Current State · Business Strategy · Execution History ·（重大决策时）Decision Log |
| Governance Entry | Execution Protocol · Knowledge Update Protocol · Decision Log · Execution History |
| Architecture Entry | Unified Architecture · Current State · Decision Log · Execution History |

无影响则**不修改**；但必须在「Reviewed but Not Modified」中说明原因。

### Daily / Timely Progress Recording

有意义的工作单元完成后，应及时同步受影响的核心记录，不得故意积压数天后再集中补写。  
**不等于**每改一行代码都改文档。

### Persistent Collaboration Rule

长期有效的协作规则不得只存在 Conversation Memory；必须进入对应 Governance 文件（见 Constitution DEC-019）。

### Human Gate（商业执行中的人工闸门 · DEC-020）

正式 Cursor Entry 涉及商业闭环时：

- **必须 Human Gate：** 真实发布、付款、广告、平台账号不可逆操作。  
- **不得默认要求：** 每个产品/每个 Production 都人工商业审批。  
- **禁止：** 把 Track A `published_local` 或仅技术 Validation 写成 Market Validation / Commercial Success。  
- **DEC-021：** Real Commercial Learning 仅可消费已验证真实商业证据；Execution Learning 与 Commercial Learning 必须隔离（代码护栏）。  
- **DEC-022：** 真实市场数据须经 Market Event ingest；不得伪造 Observation；VIEW ≠ Commercial Success。  
- **DEC-023：** Publish Queue 入队可由系统完成；外部发布必须人工；READY ≠ PUBLISHED；Publish Evidence → Observation Eligible（不自动 Start）；禁止自动登录/发布/付款/广告。

### Publish Queue / External Action（DEC-023）

正式 Cursor Entry 涉及发布准备时：

1. 经 Quality / Commercial Score / Risk / Package 门控后可入 `publish_queue`  
2. 合格条目 → `READY` 或 `AWAITING_HUMAN_ACTION`  
3. 人工完成平台侧发布后，录入 **Publish Evidence**（VERIFIED / MANUAL_VERIFIED）  
4. 仅此之后 `observation_eligible=1`；**Observation Start 留给后续 Entry**  
5. 不得把 `published_local` 或 Queue 状态写成市场成功

### Product Handoff / Listing Readiness（DEC-024）

1. Product Asset validation ≠ Commercial Product Ready（须 Version + Metadata + Delivery + Quality + Risk）  
2. Listing Package = 平台呈现层；不得反向定义 Product Core  
3. COMMERCIAL_READY / QUEUED ≠ PUBLISHED  
4. PREPARED_WITH_PLACEHOLDER ≠ Marketing Ready  
5. Published Listing 仅可在 verified Publish Evidence 之后创建  
6. Price：Hypothesis ≠ Listing Price ≠ Paid ≠ CF Default

### Opportunity Discovery / Selection（DEC-025）

1. Opportunity 须有 discovery_method + evidence_refs（或明确 INSUFFICIENT_DATA）  
2. Raw Data ≠ Signal ≠ Score；不得覆盖原始采集字段  
3. Risk unknown/failed → 不得 Selected  
4. Selection Result ≠ 跳过门控的自动发布  
5. 禁止用未来时间戳观察数据污染当前评分（no leakage）  
6. human_assisted opportunities 与 autonomous_discovery 分流，不得混称为同一 SoT

### End-to-End Product Generation Loop（DEC-026）

1. 优先复用既有 Discovery / CF Adapter / Quality / Handoff / Queue — 最小桥接，不做平行系统  
2. 候选必须来自真实 Market Data 的 Selection Result（或诚实 INSUFFICIENT DATA）  
3. Experiment Candidate ≠ Experiment completed；未验证判断标记 HYPOTHESIS  
4. Production Request 必须引用 experiment_id / opportunity / constraints — 禁止孤立 keyword 直喂 CF  
5. Quality Pass + Risk Pass + Commercial Readiness 才可 Commercial Product → Listing → Queue  
6. 止于 `AWAITING_HUMAN_ACTION`；禁止自动外部发布；禁止伪造 Market Event / Commercial Learning  
7. Legacy Pilot（如 `8523329941d4`）可并存，但不得冒充本循环的自主发现证明  
8. Trace：opportunity → experiment → preq → product_asset → commercial_product → listing → publish_queue

### Human Publish Pack / Evidence Prep（Entry 056）

1. Queue=`AWAITING_HUMAN_ACTION` 的产品须有可执行 Human Publish Pack（标题/描述/资产路径/价格边界/平台边界/清单）  
2. Human Gate 仅确认外部动作（平台/价格/封面/授权发布）；**不**重新选品或重写生产价值判断  
3. Publish Evidence 仅接受真实 listing_reference + VERIFIED/MANUAL_VERIFIED；禁止 AI 伪造 URL/ID  
4. 无 verified evidence 不得 Queue→PUBLISHED；PUBLISHED ≠ Commercial Success；Observation Start 另 Entry  
5. Legacy Pilot 与自主产品 Pack / Evidence 必须隔离

### Price Intelligence（DEC-027 / Entry 057）

1. 任何价格输出必须带 role：MARKET_REFERENCE / CF_DEFAULT / HYPOTHESIS / AI_RECOMMENDED / LISTING / PAID  
2. Default 与 AI Recommendation **不得**标为 VALIDATED 或 Paid  
3. commercial_score / production_cost **不得**直接映射为售价  
4. Product 层不绑定单渠道价格；Listing Price 由 Human External Action 确认  
5. Paid=null 且无 REAL commercial events → Price Learning Data = NONE  
6. Legacy Pilot 价格仅 HISTORICAL，不得污染自主产品证据

### Database Provenance / Current SoT（DEC-028 / Entry 058A）

1. Current Operational DB = `data/ai_factory.db` only  
2. Legacy / SAMPLE DBs → `99_ARCHIVE/database_history/` 且 `not_current_sot=true`  
3. 入库前须 provenance；sample/test/fixture URL 或文件名不得标 REAL  
4. 「有行」≠「真实市场数据」；Collector 成功 ≠ 真实平台采集已证明  
5. 初始化 Current DB 必须走现有 `ensure_schema` / additive ensure_* — 禁止手搓不一致空库  
6. SAMPLE/SIMULATION 不得进入 Real Commercial Learning

### Market Source / Collection（DEC-029 / Entry 058B–058C）

1. Modes 必须标明：LIVE_COLLECTION / EXTERNAL_IMPORT / TEST_FIXTURE  
2. Xianyu 当前默认 EXTERNAL_IMPORT；LIVE 不可用时不得伪造  
3. Raw 与 Normalized 分离；Collection Run 记录 raw/accepted/rejected/duplicate  
4. Discovery Source ≠ Sales Platform；Opportunity/Product 不得因 source 名自动绑定销售渠道  
5. 禁止验证码/登录/风控绕过；失败标 FAILED/PARTIAL，不补假数据  
6. 历史 Observation 按 observed_at 追加，不覆盖  
7. **无真实源文件时：** 标 IMPORT_READY / WAITING_FOR_REAL_SOURCE — **禁止**制造 REAL 数据或复制 sample  
8. Market Observation ≠ Product ≠ Our Listing ≠ Market Event；缺失计数字段 = NULL（≠ 0）  
9. REAL 导入 verification = MANUAL_VERIFIED（不得伪造平台官方验证）  
10. **Acquisition（058D）：** 优先 USER_EXPORT/MANUAL_IMPORT；LIVE_API 仅在资格满足后；官方有 API ≠ 本项目可用；禁止 SCRAPE/LOGIN/ANTI_BOT bypass；`collection_query` ≠ source platform  
11. **Own Product（058E / DEC-030）：** 市场学习 ≠ 搬运第三方商品；商业资产默认 SELF_PRODUCED / LAWFULLY_USED；MARKET_INSPIRED 允许但 ≠ 自动侵权；无 originality 硬门  
12. **Public Web Test（058E）：** 仅独立测试目录；禁止写入 Current DB；遇验证码/登录墙立即停止且不绕过；HTML-only 不可行时保持 EXTERNAL_IMPORT  
13. **Acquisition Engine（059 / DEC-031）：** 经 `acquisition_tasks` 执行；Engine 不含平台 DOM；仅 MANUAL+KEYWORD_SEARCH v1；无文件→WAITING_FOR_REAL_SOURCE；禁止假数据与 Archive 作 Current 源  
14. **Browser Collector（060）：** PUBLIC_WEB_READ 经 `XianyuBrowserCollector`；遇 非法访问/验证码/登录墙 → BLOCKED，不绕过；headless ACCESS_DENIED 时保持 LIMITED，生产仍走 EXTERNAL_IMPORT  
15. **Interactive Browser（061）：** 有界面独立 Profile + CDP；第一轮结果只写 `_tests/xianyu_interactive_061/`；禁止自动写 Current DB；猜你喜欢须标注 `page_section`；want_count 不得估算  
16. **Search Origin / Missing Fields（062 / DEC-032）：** 仅 SEARCH_RESULT 作 query 证据；禁止用猜你喜欢填充搜索批次；NULL≠0；缺失≠未登录（无证据时写 NOT_PROVEN）；允许 valid_without_want_count  
17. **Search Session（063）：** Search Control ≠ Page Collection 分别报告；URL=/search 不足以认定 SEARCH_RESULT；允许 attach 现有调试会话（不读 cookie）；minimum_want 对 NULL 进 unknown bucket  
18. **Extension Forensics / Blueprint（064）：** 参考插件仅作 forensics；自有 Extension 不得 Collector 内硬过滤 want_count；输出 MarketRecord→Bridge→Raw，禁止 Extension 直写 SQLite；CSV/Excel=debug export；复用现有 acquisition_engine / market_source_core / xianyu_search_session_063  
19. **Browser Extension v1（065）：** Extension+Bridge 为正式采集路径（LIMITED）；默认 TEST sink `xianyu_extension_065/`；max_records≤50；localhost bridge only；Current DB import 需 Entry 066+人工验证  
20. **Import Gate（066）：** test sink → verification_report → 仅 `--human-verified` 可写 `market_observations`；SEARCH_RESULT only；禁止 sample/推荐充数；Core File 新增须显式报告

低风险、规则内的选品评分/质量启发式/文档同步，可在 Scope 授权下自动继续。

### 必须检查 docs/0–6 的事件类型（触发清单）

项目阶段 / Primary Goal / 商业方向或实验状态 / 产品方向 / Runtime·模块·Database·commercial asset Reality / 架构或模块边界 / 重大技术方案接受或否决 / 重大问题发现或关闭 / 新增长期或修改已有工作协议 / Governance 或 Recovery 规则变化 / 用户与 AI 形成新的长期协作约束 / 任何新 AI 必须知道否则可能误判项目状态的事项。

---

## Report Minimum Format（报告最低格式）

```
1. New files（新增文件）
2. Modified files（修改文件）
3. Python changes: No|Yes
4. Database changes: No|Yes
5. Commercial assets changes: No|Yes
6. Validation result（验证结果）
7. Remaining risks（剩余风险）
8. Recommended next step（建议下一步）
```

---

## Rollback Defaults（回滚默认）

| Change type | Default rollback |
|-------------|------------------|
| Docs only | Revert files / restore from git if available |
| commercial_assets | Follow State Migration Rollback Plan (backup first — future Entries) |
| DB | No silent ALTER; authorized Entry + backup only |
| Python | Authorized Entry + tests; out of scope for control-only tasks |


---

# Cursor Execution Governance

所有 Cursor 修改必须：

执行前：
- 明确 Entry
- 明确范围
- 明确禁止修改范围


执行后：
必须生成报告。


报告位置：

07_AUDIT/{category}/


核心治理文件：
必须使用中文解释。


格式：

English Name（中文说明）

---


# Cursor Report Language Standard
# Cursor执行报告语言标准


所有 Cursor 执行报告必须包含中文摘要。


固定结构：


## 执行摘要

说明：

- 做了什么
- 为什么做
- 修改哪些文件
- 是否影响 Runtime


## Technical Details

技术细节可以使用英文。


禁止：

只输出英文执行报告。



---


# Cursor Command Language Standard
# Cursor命令语言标准


所有交给 Cursor 执行的命令必须满足：

## 1. 中文说明要求

必须说明：

- 本次任务目的
- 修改范围
- 禁止修改范围
- 风险说明


## 2. 输出要求

Cursor 执行报告必须：

中文摘要优先。

必须包含：

- 完成了什么
- 创建了什么
- 修改了什么
- 未修改什么


## 3. 保留英文的位置

允许：

- 文件名
- 类名
- API名称
- 技术关键词


禁止：

- 整个执行过程只有英文
- 用户无法理解执行目的


原则：

机器使用英文标准。

人使用中文理解。


---


# 044-H Cursor 输出语言规则


## Cursor 指令要求


所有执行指令必须包含：

中文目的说明。

例如：

# 目的：
# 整理文档目录边界



英文名称只用于：

文件名
模块名
代码引用


---

## Cursor 执行报告要求


报告必须包含：


## 中文执行摘要


说明：

做了什么。

为什么做。

影响什么。


## 文件变化


创建：

修改：

移动：

删除：


## 风险检查


说明：

是否影响 Runtime。

是否影响 Database。

是否影响商业资产。


原则：

机器可读 + 人类可理解。



---

# Cursor中文执行规则

所有 Cursor 执行任务必须：

1. 指令包含中文注释。

2. 执行目的必须中文说明。

3. 风险范围必须中文说明。

4. 执行报告必须包含中文摘要。

5. 文件名保持 English Standard Name。

6. 不允许只输出英文执行结果导致人工无法判断。

原则：

机器需要结构化，
人需要可理解。
