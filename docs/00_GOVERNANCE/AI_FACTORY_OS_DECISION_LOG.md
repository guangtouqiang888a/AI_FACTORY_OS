# AI_FACTORY_OS Decision Log

> Collaboration Control — important decisions only（重要决策专用）  
> Last updated: 2026-08-30（Entry **062** / **DEC-032**）

**Document Role（041-F）：** 正式战略裁决与否决记录。**不是** Current State；**不是**模块 Status 表；**不是**日常 commit 日志。

Append new decisions; do not rewrite history. Supersede via new Decision ID + Review Condition.  
新增决策只追加；禁止改写历史。取代须新编号并保留旧条。

---

### Decision ID: DEC-20260715-001

| Field | Content |
|-------|---------|
| **Date** | 2026-07-15 |
| **Decision** | Create Collaboration Control System v1 as documentation control layer |
| **Reason** | Multi-session work shows context loss, unclear authority, outdated “memory”, uncontrolled scope, missing decision history |
| **Rejected Alternatives** | (A) Continue relying only on PROJECT_STATUS/snapshot size growth; (B) Rebuild entire Project Intelligence from scratch; (C) Encode control only in chat memory |
| **Review Condition** | After 3+ controlled Entries using Control Center — review whether Current State stays accurate |

---

### Decision ID: DEC-20260715-002

| Field | Content |
|-------|---------|
| **Date** | 2026-07-15 |
| **Decision** | Prevent documentation explosion via Control Center Required Reading (minimum set) |
| **Reason** | docs/ already contains large governance/blueprint surface; loading all md into every session fails |
| **Rejected Alternatives** | (A) Delete old docs now; (B) Merge all docs into one file; (C) Require every agent to read MODULE_REGISTRY end-to-end each time |
| **Review Condition** | If agents still load 20+ files by default — tighten Required Reading further |

---

### Decision ID: DEC-20260715-003

| Field | Content |
|-------|---------|
| **Date** | 2026-07-15 |
| **Decision** | Authority order: Reality (Runtime/Code/DB/Assets) > Current State > Decision Log > Documentation > Conversation Memory |
| **Reason** | Past conflicts show docs and chat summarizing ahead of JSON/code/DB facts |
| **Rejected Alternatives** | (A) Treat latest chat as SoT; (B) Treat PROJECT_STATUS alone as SoT; (C) Equal weight to all markdown files |
| **Review Condition** | On next Reality vs Doc conflict — log Decision and update Current State from Reality |

---

### Decision ID: DEC-20260715-004

| Field | Content |
|-------|---------|
| **Date** | 2026-07-15 |
| **Decision** | Control files have authority over documentation interpretation; existing docs remain knowledge/reference |
| **Reason** | Need stable entry without deleting historical designs/audits |
| **Rejected Alternatives** | (A) Delete pre-control governance docs; (B) Replace PROJECT_STATUS with Control Center only |
| **Review Condition** | If control and PROJECT_STATUS diverge >7 days without Entry — treat as control-process failure |

---

### Decision ID: DEC-20260715-005（DEC-005）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-005 / DEC-20260715-005 |
| **标题** | Governance Layer Establishment（治理层建立） |
| **日期 / Entry 来源** | 2026-07-15 · Entry 037（System Governance）动机确认；Entry 040-D1 正式入库 |
| **背景** | 项目文档与双轨系统快速膨胀后，出现文档与 Reality 不一致、Blueprint 被当成已完成、上下文丢失、Scope 失控等问题。 |
| **决策** | 建立并持续维护系统治理层与协作控制层：用核心治理文件解释文档、约束扩展，使增长不超过治理能力。 |
| **原因** | 没有治理层，AI 会话会重复发明规则、误判完成态，并可能越权修改 Runtime / 商业资产。 |
| **影响** | 后续扩展须 Governance Before Expansion（治理先于扩张）；重大规则变化须进 Decision Log；详情见 System Governance Protocol（L2 参考）。 |
| **Rejected Alternatives** | (A) 仅靠聊天约定；(B) 删除旧文档「从零开始」；(C) 无控制地继续堆 PROJECT_STATUS |
| **Review Condition** | 若连续出现未走控制层的大范围改造 — 升级强制门禁 |

---

### Decision ID: DEC-20260715-006（DEC-006）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-006 / DEC-20260715-006 |
| **标题** | Blueprint ≠ Runtime（蓝图 ≠ 运行时） |
| **日期 / Entry 来源** | 2026-07-15 · Entry 037/038 原则；040-D1 正式入库 |
| **背景** | 多份 Blueprint / Plan 被进度叙事写成「已完成」，易被解读为 Runtime 已具备同等能力。 |
| **决策** | **设计/蓝图完成不得自动等于 Runtime 完成。** 声称 Runtime 能力必须有代码调用链或可运行入口证据。 |
| **原因** | 混淆会导致错误排期、错误集成假设，以及虚假的「系统已端到端」。 |
| **影响** | Unified Architecture、各类 Blueprint 均视为目标或设计；Current State 与 Reality 描述「现在」。 |
| **Rejected Alternatives** | (A) 以文档标题 Completed 推断 Runtime；(B) 用计划文案覆盖 Isolated Active 等现实标签 |
| **Review Condition** | 下一次有人把 Blueprint 当成已上线能力时 — 强制回写 Current State 并记冲突 |

---

### Decision ID: DEC-20260715-007（DEC-007）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-007 / DEC-20260715-007 |
| **标题** | Design ≠ Production（设计 ≠ 生产） |
| **日期 / Entry 来源** | 2026-07-15 · Governance / Commercial 验证链；040-D1 正式入库 |
| **背景** | Contract、Gate、Migration Strategy 等「设计完成」常与 Production Request 执行、资产落盘、观察完成混为一谈。 |
| **决策** | **文档设计完成不能代表实际生产完成。** Production（生产）以资产、流水线执行记录与授权结果为准。 |
| **原因** | 设计态过早宣称为生产态，会破坏 Pilot 可追溯性与商业验证诚实性。 |
| **影响** | Entry 报告必须区分 Design / Implementation / Production；禁止用设计文档代替交付证明。 |
| **Rejected Alternatives** | (A) 「Plan Completed = 已生产」；(B) 无资产 ID 宣称 Pilot 完成 |
| **Review Condition** | 商业验证下一阶段启动前复查 Status 用语 |

---

### Decision ID: DEC-20260715-008（DEC-008）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-008 / DEC-20260715-008 |
| **标题** | Human Assisted Commercial Judgment（商业判断必须人工辅助确认） |
| **日期 / Entry 来源** | 2026-07-15 · Human Assisted Boundary / 039-D Permission；040-D1 正式入库 |
| **背景** | 存在将技术验收通过、生产完成或自动指标，直接写成「市场成功/商业成功」的风险。 |
| **决策** | **商业成功或失败结论必须有人参与确认（Human Assisted）。** 禁止系统在无授权情况下自动写入商业成功/收入类结论。 |
| **原因** | 平台风控、责任归属与数据真实性要求；自动化可辅助生产，不可替代商业判定。 |
| **影响** | commercial_assets 成功类字段、Evaluation 结论写入须人工确认流程；Migration 自动边界受此约束。 |
| **Rejected Alternatives** | (A) Adapter/Validator 通过即自动 market success；(B) 用预测模型静默写成功 |
| **Review Condition** | 任何自动写商业结论的提案 — 默认否决，除非新 DEC 明确授权极窄范围 |

---

### Decision ID: DEC-20260715-009（DEC-009）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-009 / DEC-20260715-009 |
| **标题** | Core Governance Set v1（核心治理集 v1） |
| **日期 / Entry 来源** | 2026-07-15 · Materialization Design 批准；**Entry 040-D1** 落地 |
| **背景** | 知识治理审计显示控制层可启动但商业战略槽与更新协议槽缺失，决策日志过薄。 |
| **决策** | 采用 **8 核心文件 + AUTHORITY_MODEL 强制卫星** 作为 Core Governance Set v1：Constitution、Business Strategy、Control Center、Current State、Decision Log、Execution Protocol、Knowledge Update Protocol、Unified Architecture + Authority Model。 |
| **原因** | 该结构经设计验证可覆盖商业/架构/决策/协作/状态/更新；避免再建平行宪法。 |
| **影响** | 新会话按 Control Center 核心导航读取；历史详文降为参考层；更新走 Knowledge Update Protocol。 |
| **Rejected Alternatives** | (A) 仅 5 文件硬塞全部知识；(B) 把 MODULE_REGISTRY 升为第 9 宪法；(C) 删除历史文档 |
| **Review Condition** | 使用 3+ Entry 后评估是否仍出现无家可归的核心知识 |

---

### Decision ID: DEC-20260715-010（DEC-010）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-010 / DEC-20260715-010 |
| **标题** | Historical Document Role（历史文档角色） |
| **日期 / Entry 来源** | 2026-07-15 · DEC-002/004 延伸；**Entry 040-D1** |
| **背景** | docs/ 存在大量 Blueprint、审计、旧 BUSINESS_PLAN、WORK_PRINCIPLES 等；若与核心文件同等默认采信，会再次上下文爆炸与冲突。 |
| **决策** | **历史与参考文件作为证据与详文，不作为会话默认判断来源。** 默认判断来自 Reality + Core Governance Set + Authority Model。 |
| **原因** | 保留历史可追溯，同时防止过时叙事（如旧 Plan「已完成」）覆盖当前战略与状态。 |
| **影响** | BUSINESS_PLAN 等保留但不作战略入口；审计报告按需引用；禁止为「清理」删除治理历史。 |
| **Rejected Alternatives** | (A) 每会话加载全部 md；(B) 立即删除旧治理文档；(C) PROJECT_STATUS 单独作为 SoT |
| **Review Condition** | 若代理默认仍整库朗读 docs/ — 收紧 Control Center 必读并记一次失效 |

---

### Decision ID: DEC-20260715-011（DEC-011）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-011 / DEC-20260715-011 |
| **标题** | Scope-Controlled Execution Supersedes Bulk Upgrade Mandate（范围受控执行优先于「必须整体一次升级」） |
| **日期 / Entry 来源** | 2026-07-15 · **Entry 040-D2-B**；依据 `AI_FACTORY_OS_WORK_PROTOCOL_CONFLICT_REPORT.md` |
| **背景** | `WORK_PRINCIPLES` 要求「一次性整体升级」「禁止过度分阶段」「每次升级捆绑架构+商业+执行」，与现行 Scope Control、Entry 管理、阶段验证、Human Assisted、Governance Before Expansion 冲突（见 WP-C-001..005）。 |
| **决策** | **执行层最终裁决：**（1）**Scope-controlled Entries 优先**——单次任务不得以「整体升级」为由越权；（2）仍鼓励向用户提供**完整可理解的整体方案**，但**落地必须按授权 Scope 分 Entry**；（3）「Complete Implementation」仅覆盖已授权范围；（4）不追求自动化所有流程；商业结论遵循 DEC-008；（5）`WORK_PRINCIPLES` 降为历史协作参考，**执行效力低于** EXECUTION_PROTOCOL、PROJECT_CONSTITUTION、DECISION_LOG、KNOWLEDGE_UPDATE_PROTOCOL。 |
| **原因** | 旧「整包升级」在文档爆炸与双轨现实下会导致 Scope 失控、误改 Reality、把 Blueprint 当 Production；现行治理已证明分 Entry + 门禁更安全。 |
| **影响** | AI 遇到旧条文与新协议冲突时，以本 DEC + Execution/Update Protocol 为准；不删除 WORK_PRINCIPLES 文件。 |
| **Rejected Alternatives** | (A) 恢复强制 system-wide 单次改造；(B) 删除 WORK_PRINCIPLES；(C) 每次任务强制同时改架构+商业+代码 |
| **Review Condition** | 若连续出现以「整体升级」越权的失败 Entry — 在 Control Center Forbidden 中显式点名本 DEC |

---

### Decision ID: DEC-20260715-012（DEC-012）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-012 / DEC-20260715-012 |
| **标题** | Governance Hardening Principle（治理硬化原则） |
| **日期 / Entry 来源** | 2026-07-15 · **Entry 040-F-A** |
| **背景** | 长对话中 AI 易仅依据当前聊天上下文形成「新共识」，绕过 Authority、Current State、Decision Log，造成认知漂移与方向漂移。 |
| **决策** | **AI 不得只依据当前聊天上下文改变项目方向。** 重大判断必须回溯 Core Governance Set，并检查：**Authority Model**、**Current State**、**Decision Log**（及任务相关的 Business Strategy / Constitution）。无法完成回溯则禁止提出改方向方案。 |
| **原因** | 防止长会话记忆覆盖 Reality 与已批准裁决；巩固 Session Bootstrap 必读顺序与认知完整性检查。 |
| **影响** | Control Center Forbidden 增加「禁止仅靠聊天改方向」；Execution Protocol 增加 AI Cognitive Integrity Check；与 DEC-003/010/011 一致加强。 |
| **Rejected Alternatives** | (A) 以最新长聊天摘要为 SoT；(B) 允许方案阶段跳过 Core 回溯；(C) 用 PROJECT_STATUS  alone 证明方向变更合法 |
| **Review Condition** | 若出现未回溯 Core 即改商业/架构方向的失败案例 — 升级 Bootstrap 为硬门禁清单勾选 |

---

### Decision ID: DEC-20260715-013（DEC-013）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-013 / DEC-20260715-013 |
| **标题** | Modular Capability Principle（模块化能力原则） |
| **日期 / Entry 来源** | 2026-07-15 · **Entry 041-B-A** |
| **背景** | Entry 041-A 确认 Core OS 与 Content Factory 仍为双轨（情况 B）。若把「统一系统」误读为强制代码融合 / 单一 Runtime / 消除独立模块，将牺牲模块独立价值与独立商业化可能。 |
| **决策** | **AI_FACTORY_OS adopts modular capability architecture.** 长期产品方向为 **Modular AI Business Operating System**。各能力模块应保持独立功能价值、独立演进路径、独立商业化可能；可通过统一治理、数据边界、接口契约与编排组合成完整系统。 |
| **原因** | 避免未来为了「系统统一」而牺牲模块独立价值；允许独立运行与整体协同同时成立。 |
| **Decision Boundary** | **统一治理 ≠ 强制融合。** Modular ≠ Fragmented；Unified ≠ Forced Merge。 |
| **影响** | Constitution / Business Strategy / Unified Architecture 同步本原则；后续 Entry 不得以「必须合并 Runtime」为默认前提；Runtime 现状不变，融合须另开授权。 |
| **Rejected Alternatives** | (A) 强制把 CF 并入 OS 单一 Runtime；(B) 以统一为由消除模块独立性；(C) 将双轨现实直接等同于永久无治理碎片化 |
| **Review Condition** | 若出现「为统一而强融」且破坏 Pilot/模块独立性的提案 — 以本 DEC + Constitution Modular Capability Principle 否决 |

---

### Decision ID: DEC-20260716-014（DEC-014）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-014 / DEC-20260716-014 |
| **标题** | Capability Composition Principle（能力组合原则） |
| **日期 / Entry 来源** | 2026-07-16 · **Entry 041-B-B** |
| **背景** | 目录 `0`–`11` 易被误读为商业模块边界；「统一 OS」易被误读为强制单一 Runtime。需在 DEC-013 模块化原则之上，明确能力组合与产品形成方式。 |
| **决策** | **统一 AI_FACTORY_OS 的目标不是强制所有能力进入单一 Runtime。** 目标是形成**可治理、可组合、可商业化的能力体系**。商业边界以 Capability 为准，不以 Folder 为准。**Module ≠ Folder**；**Capability ≠ Implementation**；**Product = Capability Composition**。 |
| **原因** | 保护独立能力价值与多路径商业化；避免为「统一」牺牲组合弹性；与 Reality（双轨）及 DEC-013 一致。 |
| **Decision Boundary** | Unified ≠ Forced Merge Runtime · Modular ≠ Fragmented · Folder ≠ commercial boundary · Blueprint ≠ Production |
| **影响** | Constitution / Business Strategy / Unified Architecture 写入能力组合原则；未来商业化可走平台 / 能力组合产品 / 内容产品 / 企业方案等路径（战略方向 only）；Runtime 现状不变。 |
| **Rejected Alternatives** | (A) 以目录名定义 SKU/商业模块；(B) 以统一为由强制 Runtime 融合；(C) 将能力组合愿景写成已实现产品 |
| **Review Condition** | 若出现「文件夹=产品」或「未授权强融 Runtime」提案 — 以本 DEC + Constitution Capability Composition Principle 否决 |

---

### Decision ID: DEC-20260716-015（DEC-015）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-015 / DEC-20260716-015 |
| **标题** | Documentation Architecture Governance Principle（文档架构治理原则） |
| **日期 / Entry 来源** | 2026-07-16 · **Entry 041-E** |
| **背景** | `docs/` 文件量大；新会话易混淆当前事实、架构设计、商业战略、历史解释、审计与执行记录，导致 Blueprint/历史覆盖 Reality。 |
| **决策** | **文档角色必须分离。** 历史解释不得覆盖现实状态。未来规划不得被读取为已实现。治理通过角色分层与读取顺序实现；**默认不移动/不重命名文件。** |
| **原因** | 降低文档爆炸下的认知漂移；保护 Reality > Documentation；与 DEC-012/013/014 一致。 |
| **Decision Boundary** | Audit/History/Evolution Context ≠ Current State · Blueprint ≠ Production · Design ≠ Runtime |
| **影响** | Control Center 增加历史解释按需读取提示；策略见 `docs/07_AUDIT/structure/AI_FACTORY_OS_DOCUMENTATION_ARCHITECTURE_GOVERNANCE_STRATEGY.md`；Constitution 增补 Capability ≠ Folder Mapping；物理整理须另开授权 Entry。 |
| **Rejected Alternatives** | (A) 立即大规模移动/重命名 docs；(B) 用单一「总文档」吞并分层；(C) 允许历史/Blueprint 覆盖 Current State |
| **Review Condition** | 若出现未分层即把审计/Blueprint 当 Reality 的失败会话 — 强化 Bootstrap 角色检查 |

---

### Decision ID: DEC-20260716-016（DEC-016）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-016 / DEC-20260716-016 |
| **标题** | Information Ownership Governance Principle（信息归属治理原则） |
| **日期 / Entry 来源** | 2026-07-16 · **Entry 041-F** |
| **背景** | 治理文件增加后，同类信息在多处重复定义，易导致 AI 误判权威来源；且 Reality 变更后易漏同步 Registry / Current State。 |
| **决策** | **信息必须有唯一权威归属。** 他处可引用，不得重复定义。重要 Reality 变化必须同步 MODULE_REGISTRY、CURRENT_STATE（必要时 Evolution Context）。**禁止只改代码不更新治理。** |
| **原因** | 建立长期稳定的信息归属规则；降低文档重复与认知漂移；与 DEC-015 文档角色分层互补。 |
| **Decision Boundary** | Constitution=规则 · Current State=事实投影 · Registry=模块 Status · UA=设计 · Business Strategy=商业方向 · Evolution Context=历史原因 |
| **影响** | Constitution 写入 Information Ownership + State Sync；Control Center 增加 Document Reading Principle；8+1 核心文件仅做职责说明校准。 |
| **Rejected Alternatives** | (A) 允许多文件并列定义同一事实；(B) 只改代码不同步治理；(C) 大规模重写/移动核心文件 |
| **Review Condition** | 若出现「聊天或 Blueprint 覆盖 Current State」或「代码变更无 Registry/State 同步」— 升级 Entry 收尾检查清单 |

---

### Decision ID: DEC-20260716-017（DEC-017）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-017 / DEC-20260716-017 |
| **标题** | New Session Recovery Protocol Principle（新会话恢复协议原则） |
| **日期 / Entry 来源** | 2026-07-16 · **Entry 041-G** |
| **背景** | AI 重新进入项目时易不知读取顺序、权威关系、历史文件用途与当前 Reality，易用历史/Blueprint 推断现状。 |
| **决策** | AI 恢复项目上下文必须：**先恢复规则 → 再恢复 Reality → 再读取设计 → 最后读取历史。** 第一阶段必读 Constitution、Authority Model、Current State、Module Registry、Decision Log。**禁止直接根据历史文件推断当前系统。** |
| **原因** | 保证新会话认知可恢复、可审计；与 DEC-015/016 分层与归属原则一致。 |
| **Decision Boundary** | Evolution Context / Blueprint / audit ≠ Current Reality · Control Center New Session Recovery Protocol 为会话恢复入口 |
| **影响** | Control Center 增加 New Session Recovery Protocol；Current State 增加 Reality Change Synchronization；Evolution Context 明确「先 State/Registry，后历史」 |
| **Rejected Alternatives** | (A) 先读全部历史/Blueprint 再猜现状；(B) 跳过 Current State / Registry；(C) 用聊天记忆替代第一阶段 |
| **Review Condition** | 若出现未跑第一阶段即提出融合/执行 Reality 的失败会话 — 将 Recovery Protocol 升为硬门禁勾选 |

---

### Decision ID: DEC-20260716-018（DEC-018）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-018 / DEC-20260716-018 |
| **标题** | Folder Structure and Capability Architecture Separation（目录结构与能力架构分离） |
| **日期 / Entry 来源** | 2026-07-16 · **Entry 041-H** |
| **背景** | `0`–`11` 目录编号易被读成「目录 = 能力 = 商业产品」，导致错误拆分商业方案与错误推断能力边界。 |
| **决策** | **确认：目录结构、能力结构、商业产品结构三者分离。** Folder Structure ≠ Capability Architecture ≠ Product Architecture。遵循 Modular Capability（DEC-013）与 Capability Composition（DEC-014）。禁止按文件夹名直接推断商业能力边界。 |
| **原因** | 保护可复用能力与跨目录组合；降低工程编号对商业认知的污染。 |
| **Decision Boundary** | Module Registry = 工程模块 Status ≠ Product/Solution 定义 · Evolution Context ≠ Current Reality |
| **影响** | Constitution / UA / Module Registry / Evolution Context / Control Center 同步澄清；分析商业方案须参考 Capability Composition，不得按目录拆能力。 |
| **Rejected Alternatives** | (A) 目录名 = SKU/能力边界；(B) Module Registry 定义全部商业能力；(C) 用历史目录叙事覆盖 Current State |
| **Review Condition** | 若出现「按 0–11 拆商业方案」的失败提案 — 以本 DEC + Folder Capability Separation Principle 否决 |

---

### Decision ID: DEC-20260829-019（DEC-019）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-019 / DEC-20260829-019 |
| **标题** | Establish Core Documentation Continuity Rule（建立核心文档连续性规则） |
| **日期 / Entry 来源** | 2026-08-29 · **Entry 046** |
| **背景 / Problem** | 长期项目的跨会话 / ZIP 恢复存在风险：关键协作规则与推进进度易只留在 Conversation Memory；新 AI 无法可靠恢复「做到哪里」。 |
| **决策 / Decision** | 建立 **Core Documentation Continuity Rule**：`docs/0–6` 为项目核心连续性记录域。配套建立 Daily/Timely Progress Recording、Persistent Collaboration Rule、Post-Execution Core Documentation Sync，以及每次 Entry 强制的 Core Documentation Continuity Check（含 Modified / Reviewed-but-Not-Modified 报告）。 |
| **Scope** | Governance · Current State · Architecture · Business · Execution · History（`docs/0–6`） |
| **Effect** | 所有正式 Cursor Entry 必须进行核心文件影响判断与必要同步；Documentation Sync 是完成条件的一部分。 |
| **Non-Goals** | 不要求每行代码都写文档；不要求所有核心文件每次都修改；不建立新的平行治理体系；不新建额外核心治理文件。 |
| **Compatibility** | **不改变** User authority · Reality-first · Authority Model 层级 · Current State SoT · Information Ownership · Blueprint ≠ Runtime · Design ≠ Production · Conversation ≠ Authority。Archive `WORK_PRINCIPLES` 不得自动成为现行规则；其中仍有效协作精神已由现行治理吸收，冲突项（如强制一次性整体升级）以本 DEC 与既有 DEC-011 等为准。 |
| **原因** | 保证未来仅凭最新 ZIP + `docs/0–6` 即可恢复规则、状态、商业、架构、执行进度与重大决策，而不依赖本聊天记录。 |
| **Decision Boundary** | Recovery 权威仍为 Control Center New Session Recovery Protocol（DEC-017）+ AI Recovery Reading Boundary；归档 Recovery Read Order ≠ 现行权威 |
| **影响** | Constitution / Authority Model / Control Center / Execution Protocol / Knowledge Update Protocol / Decision Log / Documentation Map / Execution History 同步 |
| **Rejected Alternatives** | (A) 继续依赖聊天记忆恢复；(B) 每个 Entry 强制改写全部 0–6 文件；(C) 新建平行「连续性」治理树绕过 Authority Model；(D) 把 Archive WORK_PRINCIPLES 直接升格为现行最高规则 |
| **Review Condition** | 若出现「正式 Entry 完成后无 Continuity Check / 无 Execution History / 长期规则仅在聊天」— 视为未完成 Entry，须补同步后再关闭 |

---

### Decision ID: DEC-20260829-020（DEC-020）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-020 / DEC-20260829-020 |
| **标题** | Establish Autonomous Commercial Learning & Future Extensibility Principles（自主商业学习与未来扩展性原则） |
| **日期 / Entry 来源** | 2026-08-29 · **Entry 049** |
| **背景 / Problem** | （1）系统若停留在「人工逐产品审批」或「仅本地模拟发布学习」，无法形成真实商业学习能力；（2）若把 Phase 1 虚拟资料硬编码为永久架构边界，未来扩展短视频/小说/音频等将被迫推翻。 |
| **决策 / Decision** | 正式建立 **Autonomous Commercial Learning Principle** 与 **Future Extensibility Principle**。长期商业主线为可审计自主商业学习闭环；真实市场反馈为学习主依据；Human Gate 控制高风险外部行为，不替代全部商业判断。Current Scope（Phase 1=虚拟资料）与 Architecture Boundary 分离；Future-Extensible ≠ Future-Built。 |
| **Scope** | Governance · Architecture Design Reference · Business Scope discipline · Learning integrity |
| **Effect** | Constitution / UA / Business Strategy / Decision Log / Control Center 对齐；后续实施 Entry 须按 P0/P1 优先补「最小关键连接」，禁止借扩展之名提前建设未来产品 Runtime。 |
| **Human Gate Boundary** | 人工负责：平台账号、不可逆外部操作、付款、广告、（当前）真实发布。人工不负责：每个产品必须手工商业审批。 |
| **Current Scope vs Future Architecture** | Phase 1 严格只做虚拟资料；架构须保留 Product/Asset/Collector/Market Event/Quality 等可扩展抽象空间，但不得现在实现全部未来类型。 |
| **Non-Goals** | 不在本 DEC 实施 Database Migration；不新建短视频/短剧/小说/音频 Runtime；不自动发布；不伪造市场数据；不强制 Core OS↔CF Runtime 合并。 |
| **Compatibility** | **不改变** User authority · Reality-first · Authority Model · Current State SoT · Information Ownership · Blueprint ≠ Runtime · Design ≠ Production · Conversation ≠ Authority · DEC-013/014/018 Modular/Composition · DEC-019 Continuity |
| **原因** | Entry 049 Reality Audit：双轨未融合；商业机会/实验仍人辅；Observation 未开始；Track A 以 `published_local` 为 success — 必须先立原则再择最小连接。 |
| **影响** | 永久原则 #16/#17；UA 增加学习闭环与扩展性 Design Reference；P0 优先修复「模拟成功冒充商业成功」与真实观察缺失。 |
| **Rejected Alternatives** | (A) 永久人工逐产品审批；(B) 现在一次性开发全部未来媒体类型；(C) 继续用 `published_local` 驱动商业策略；(D) 把 Phase 1 Scope 写成永久架构边界 |
| **Review Condition** | 若出现「用模拟发布结果更新商业战略」或「为未来类型提前大规模开发」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260829-021（DEC-021）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-021 / DEC-20260829-021 |
| **标题** | Commercial Learning Integrity Hardening（商业学习完整性硬规则） |
| **日期 / Entry 来源** | 2026-08-29 · **Entry 050** |
| **背景 / Problem** | Track A `extract_pattern` 将 `action==publish` 且 `exec_status==published_local` 记为 `outcome=success`，SelfEvolution 据此调 threshold/weights — 把执行模拟成功污染为可驱动策略的「成功」信号；真实商业证据尚未进入学习。 |
| **决策 / Decision** | 正式建立 **Commercial Learning Integrity Principle**。Execution Success ≠ Commercial Success。Real Commercial Learning 仅可消费 `commercial_outcome` + `data_origin=REAL` + `verified_source`。`published_local` / quality / production / SIMULATION / SYNTHETIC / UNKNOWN 一律不得进入 Real Commercial Learning。SelfEvolution 明确为 **Execution Strategy** 域。 |
| **Scope** | `7_MEMORY/memory_core.py` · `0_START/self_evolution.py` · Outcome Ontology（代码层）· Constitution · UA · tests |
| **Effect** | 永久原则 #18；Commercial Learning ingest guardrail 接口；Execution Learning 保持可用；不宣称商业闭环已完成。 |
| **Non-Goals** | Database Migration；完整 Market Event 系统；商业平台发布；修改 Pilot Observation/Revenue；大规模 Memory/SelfEvolution 重构。 |
| **Compatibility** | 强化 DEC-020 Learning Integrity；不改变 User authority · Reality-first · DEC-019 Continuity · Pilot 商业状态。 |
| **原因** | Entry 049 P0：模拟发布成功被当作学习 success — 必须先「不学错」再谈「学会赚钱」。 |
| **影响** | `outcome` 在 Track A 仅表示 EXECUTION；`commercial_success` 默认 False；`ingest_commercial_learning_event` 为未来真实商业摄入边界。 |
| **Rejected Alternatives** | (A) 继续用 published_local 驱动商业策略；(B) 为 PASS 伪造真实商业数据；(C) 大规模 Schema/DB Migration；(D) 停用 Execution Learning |
| **Review Condition** | 若出现「仅凭 published_local / quality_pass / simulation 写入 commercial_success 或更新 Commercial Strategy」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260829-022（DEC-022）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-022 / DEC-20260829-022 |
| **标题** | Market Event as Commercial Learning Data Foundation（市场事件作为商业学习数据基础） |
| **日期 / Entry 来源** | 2026-08-29 · **Entry 051** |
| **背景 / Problem** | Entry 050 已建立 Commercial Learning 安全门，但系统无法持久化真实市场事件；Feedback/Evaluation 仅为 pending 占位；Collector 仅 Xianyu Excel 竞品抓取，与 Pilot 产品资产无关。 |
| **决策 / Decision** | 正式建立 **Market Event Data Foundation Principle**。统一 `MarketEvent` ontology（平台无关、产品类型无关）；Raw→Normalized→Observation→Evaluation→Learning 分层；REAL+verified 的 PURCHASE/REVENUE/REFUND 等可经 bridge 进入 `ingest_commercial_learning_event()`；VIEW 等仅 Observation。 |
| **Scope** | `1_DATA/market_event_core.py` · additive SQLite `market_events` · `commercial_assets/observations/` · memory evidence fields · Constitution · UA |
| **Effect** | 永久原则 #19；接收真实观察数据的能力落地；**不**启动 Pilot Observation；**不**伪造市场数据。 |
| **Non-Goals** | 大 Migration；全平台 Connector；发布；伪造 Observation；未来媒体 Runtime；Core OS↔CF 强制合并。 |
| **Compatibility** | 强化 DEC-020/021；Platform 仅作 Source/Connector 层扩展点。 |
| **原因** | 无标准事件入口则无法诚实学习；必须先把入口设计正确。 |
| **Rejected Alternatives** | (A) 把 metrics 直接写进 Feedback 结论；(B) 建 taobao_product/xianyu_product 永久表；(C) 伪造 Pilot 事件以「启动」学习；(D) 大规模 Schema 重构 |
| **Review Condition** | 若出现「无 Market Event 证据却宣称 Commercial Success」或「平台硬编码进核心产品模型」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260829-023（DEC-023）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-023 / DEC-20260829-023 |
| **标题** | Publish Queue + Human External Action Gate（发布队列与人工外部动作闸门） |
| **日期 / Entry 来源** | 2026-08-29 · **Entry 052** |
| **背景 / Problem** | 系统缺少正式 Publish Queue；Human Gate 易被误解为「每个产品人工商业审批」；`published_local` 与真实发布混淆；无 Publish Evidence 回流。 |
| **决策 / Decision** | 正式建立 **Human External Action Gate Principle**。系统可自主完成候选排序与 Publish Queue 入队（经 Quality/Commercial Score/Risk/Package 门控）。人工仅负责不可逆外部动作。Human Gate ≠ Product Approval Gate。READY ≠ PUBLISHED。PUBLISHED ≠ Commercial Success。Publish Evidence 仅使 Observation Eligible，不自动 Start Observation。 |
| **Scope** | `6_EXECUTION/publish_queue.py` · `3_DECISION/candidate_selector.py` · SQLite publish_queue/publish_evidence · Constitution · Authority · Execution Protocol · UA |
| **Effect** | 永久原则 #20；Pilot 入队 `AWAITING_HUMAN_ACTION`；禁止自动外部发布。 |
| **Non-Goals** | 自动登录/发商品/付款/广告；启动 Observation；伪造 Publish Evidence；大 Migration；未来媒体 Runtime。 |
| **Compatibility** | 强化 DEC-020 Human Gate；DEC-021 Integrity；DEC-022 Market Event。 |
| **Rejected Alternatives** | (A) 每产品人工商业审批；(B) READY 自动 PUBLISHED；(C) TaobaoPublishQueue 平台绑定表；(D) 无证据启动 Observation |
| **Review Condition** | 若出现「自动平台发布」或「把 Queue PUBLISHED 写成 Commercial Success / Observation Started」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260829-024（DEC-024）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-024 / DEC-20260829-024 |
| **标题** | Product / Commercial Product / Listing Separation（产品·商业产品·上架分离） |
| **日期 / Entry 来源** | 2026-08-29 · **Entry 053** |
| **背景 / Problem** | Product Asset 易被当成可售 Commercial Product；Listing Package 易被当成已发布；价格 Hypothesis/CF Default/Listing/Paid 混淆；CF 将文件扩展名硬编码为 product_type，威胁未来扩展。 |
| **决策 / Decision** | 正式分离 **Product → Product Version → Product Asset → Commercial Product → Listing Package → Listing → Published Listing**。Commercial Ready ≠ Published。Listing Package 为平台呈现层，不得污染 Product Core。禁止 TaobaoProduct/XianyuProduct 核心模型。`product_type` 与 `asset_type` 分离。价格角色分离。 |
| **Scope** | `6_EXECUTION/commercial_handoff.py` · commercial_products/listings JSON · Constitution · UA · Execution Protocol |
| **Effect** | 永久原则 #21；Pilot Commercial Product=`QUEUED`；Listing=`AWAITING_HUMAN_ACTION`；Package=`PREPARED_WITH_PLACEHOLDER` |
| **Non-Goals** | 真实发布；Observation Start；伪造市场数据；CF 大规模重构；未来媒体 Runtime |
| **Rejected Alternatives** | (A) Asset ID = Product 本体；(B) Package PREPARED = PUBLISHED；(C) 平台专用产品表；(D) 把 19.9 CF default 写成 VALIDATED 售价 |
| **Review Condition** | 若出现「Asset validation = Published」或「Platform 进入 Product Core」或「未证据宣称 Published Listing」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260829-025（DEC-025）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-025 / DEC-20260829-025 |
| **标题** | Data-Driven Opportunity Discovery & Selection（数据驱动机会发现与选择） |
| **日期 / Entry 来源** | 2026-08-29 · **Entry 054** |
| **背景 / Problem** | Collector→SQLite products 已存在，但 Opportunity JSON 仍为 human_assisted；与市场数据断连；candidate_selector 仅 Pool Sorting。人工成为永久选品瓶颈。 |
| **决策 / Decision** | 正式建立 **Data-Driven Opportunity Discovery & Selection Principle**。链路：Market Data → Signals → Opportunity Candidate → Score → Risk → Selection（含 reason/evidence）。Selection ≠ Experiment ≠ Production。无证据 → INSUFFICIENT DATA / 拒绝静默创建。评分模型标明当前 proxy，非最终商业智慧。 |
| **Scope** | `1_DATA/market_signal_core.py` · `3_DECISION/opportunity_discovery.py` · additive SQLite tables · autonomous_discovery_v1.json · Constitution · UA |
| **Effect** | 永久原则 #22；最小自主发现能力落地；不自动生产/发布；不修改 Pilot Observation |
| **Non-Goals** | 2_COGNITION；自动 Experiment；伪造商业结果；大 Migration；未来媒体 Runtime |
| **Rejected Alternatives** | (A) 永久仅人工写 Opportunity；(B) views 高=机会；(C) Selection 直接 Production；(D) 无数据伪造候选 |
| **Review Condition** | 若出现「无 market evidence 写入 Opportunity」或「Selection 自动触发 Production」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260830-026（DEC-026）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-026 / DEC-20260830-026 |
| **标题** | End-to-End Autonomous Product Generation Loop（端到端自主产品生成闭环） |
| **日期 / Entry 来源** | 2026-08-30 · **Entry 055** |
| **背景 / Problem** | 050–054 已横向建立 Integrity / Event / Queue / Handoff / Discovery，但缺少一条可追踪的纵向闭环证明：真实市场数据能否走到 Publish Queue。 |
| **决策 / Decision** | 正式建立 **E2E Autonomous Product Generation Loop** 为长期执行原则：Real Market Data → Opportunity → Selection → Experiment → Production → Quality → Commercial Product → Listing → Publish Queue（止于 AWAITING_HUMAN_ACTION）。优先复用既有模块，仅做最小桥接。Production Success ≠ Commercial Success；不得伪造市场结果。 |
| **Scope** | `6_EXECUTION/e2e_autonomous_pilot.py` · CF Adapter reuse · commercial_handoff · publish_queue · commercial_assets append · Constitution · UA |
| **Effect** | 永久原则 #23；首个自主发现产品入队；Legacy Pilot 保留为 HISTORICAL |
| **Non-Goals** | 真实平台发布；Observation；Real Commercial Learning；CF 重写；大规模 DB migration；未来媒体 Runtime |
| **Rejected Alternatives** | (A) 人工指定新产品冒充自主发现；(B) 复用 8523329941d4 作为 055 证明；(C) 为 PASS 伪造 Market Event；(D) Selection 跳过 Quality 直接 Queue |
| **Review Condition** | 若出现「E2E Production Success = Commercial Success」或「Queue 自动 PUBLISHED」或「无证据伪造机会」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260830-027（DEC-027）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-027 / DEC-20260830-027 |
| **标题** | Evidence-Based Price Intelligence Boundary（证据型价格智能边界） |
| **日期 / Entry 来源** | 2026-08-30 · **Entry 057** |
| **背景 / Problem** | 自主产品出现 99.9 vs 19.9；若把 listing 均价或 CF 默认当成 Validated / Paid，将污染定价与未来学习。 |
| **决策 / Decision** | 正式建立 **Price Intelligence Boundary**：Market Evidence ≠ Recommendation ≠ Listing Price ≠ Paid Price ≠ Validated。Default/Heuristic ≠ Market Fact；Score/Cost 不得直接映射为售价。无真实成交则 Price Learning=NONE。多产品类型/多渠道价格挂在 Listing，不覆盖 Product Core。 |
| **Scope** | `3_DECISION/price_intelligence.py` · price_recommendations JSON · Constitution · UA · Execution Protocol |
| **Effect** | 永久原则 #24；99.9 归类 MARKET_REFERENCE→HYPOTHESIS；实验推荐 19.9（LOW confidence）；Queue 不变 |
| **Non-Goals** | 真实发布；Paid 写入；Price Learning 开启；ML 定价；平台专用价格表 |
| **Rejected Alternatives** | (A) 99.9 自动当 Listing Price；(B) 19.9 当 Market Evidence；(C) commercial_score→price；(D) 成本加成=市价；(E) 伪造 Paid |
| **Review Condition** | 若出现「Default=Validated」或「无 Paid 开启 Real Price Learning」或「Product Core 被单平台价覆盖」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260830-028（DEC-028）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-028 / DEC-20260830-028 |
| **标题** | Current vs Legacy Database Boundary（当前库 vs 历史库边界） |
| **日期 / Entry 来源** | 2026-08-30 · **Entry 058A** |
| **背景 / Problem** | `data/ai_factory.db` 被证实为早期评分练习/样例库（sample/test URL、测试标题、`*_sample.xlsx`），却被当作 Real Market Data 驱动 054–057。 |
| **决策 / Decision** | 正式分离 **Legacy Archive DB** 与 **Current Operational DB**。Current SoT=`data/ai_factory.db`（干净 schema）。Legacy 整库归档且 `not_current_sot=true`。Provenance 不足不得标 REAL。SAMPLE/SIMULATION 不得进入 Real Commercial Learning。 |
| **Scope** | `1_DATA/db_legacy_reset_058a.py` · `99_ARCHIVE/database_history/` · Constitution · UA · Current State |
| **Effect** | 永久原则 #25；Current products=0；054–057 上游声明重分类；商业资产文件保留 |
| **Non-Goals** | 删除 raw 证据；删除 f2f8 商业资产；伪造 REAL；开启 Observation/Learning |
| **Rejected Alternatives** | (A) 继续把样例库当 Current SoT；(B) 无归档直接删除；(C) 清空后假装从未有过历史库；(D) 把 SAMPLE 标 REAL |
| **Review Condition** | 若出现「Archive 被当 Current」或「无 provenance 的行进入 Real Learning」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260830-029（DEC-029）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-029 / DEC-20260830-029 |
| **标题** | Discovery Source / Product / Sales Channel / Feedback Source Separation |
| **日期 / Entry 来源** | 2026-08-30 · **Entry 058B** |
| **背景 / Problem** | XianyuCollector 实为 Excel 导入却易被当成实时采集；且 source 平台名易与销售平台自动绑定，破坏多渠道结构。 |
| **决策 / Decision** | 正式分离 Discovery Source、Product、Sales Channel、Feedback Source。第一阶段 Xianyu 以 **EXTERNAL_IMPORT** 进入 `market_observations`；LIVE_COLLECTION 在无合规适配器前标 NOT AVAILABLE。禁止绕过验证码/风控。禁止平台专用核心表。SAMPLE 不得标 REAL。 |
| **Scope** | `market_source_core.py` · `connectors/xianyu_import_connector.py` · collector facade · Constitution · UA |
| **Effect** | 永久原则 #26；Source Registry + Collection Run + Observation；sales_platform 不自动绑定 |
| **Non-Goals** | 淘宝/社交实时抓取；绕过风控；伪造 REAL 批次；自动发布 |
| **Rejected Alternatives** | (A) 把 Excel Collector 标 LIVE；(B) source=xianyu⇒sales=xianyu；(C) xianyu_products 核心表；(D) 用 sample.xlsx 冒充真实批次 |
| **Review Condition** | 若出现「无合规 LIVE 却宣称 LIVE」或「Source 强制 Sales」或「SAMPLE=REAL」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260830-030（DEC-030）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-030 / DEC-20260830-030 |
| **标题** | Own Product Principle / Market Learning Boundary |
| **日期 / Entry 来源** | 2026-08-30 · **Entry 058E** |
| **背景 / Problem** | 市场学习易被误解为可直接搬运第三方商品；同时「必须 100% 独创」僵化门也会误伤合法同类/竞品生产。 |
| **决策 / Decision** | 正式确立 Own Product Principle：可研究市场并生产同类竞品；商业资产默认须自我生产或合法可用；禁止未经授权搬运/简单重包装作为常规路线。`MARKET_INSPIRED` ≠ 自动侵权。用 `product_origin` / `rights_status` / `provenance_status` / `risk_status` 表达边界，**不**建立 originality_score 硬门。Product Type ≠ Business Model。 |
| **Scope** | Constitution #27 · `1_DATA/product_origin.py` · UA · Commercial / Quality 未来闸门语义 |
| **Effect** | 市场情报 → 自有产品概念 → 生成 → Rights/Risk → 商业发布 |
| **Non-Goals** | 复杂版权 AI；海外市场实现；把公开网页测试结果写入 Current DB；生产级 Web Collector |
| **Rejected Alternatives** | (A) 允许默认搬运第三方数字商品；(B) originality_score\<X→BLOCK；(C) 把 MARKET_INSPIRED 当侵权；(D) 混用 Product Type 与 Business Model 字段 |
| **Review Condition** | 若出现「第三方受保护内容未经授权进入 Publish Queue」或「用 originality 硬分误杀合法竞品」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260830-031（DEC-031）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-031 / DEC-20260830-031 |
| **标题** | Establish Autonomous Market Acquisition Engine Boundary |
| **日期 / Entry 来源** | 2026-08-30 · **Entry 059** |
| **背景 / Problem** | 需要可持续市场数据入口，但不能把系统做成「闲鱼爬虫」、不能把 Cursor 当产品 AI、不能把 source 绑死为销售平台。 |
| **决策 / Decision** | 建立 Acquisition Engine：User Policy 设边界；Engine 编排任务；Source Adapter 承载平台细节。Xianyu 当前仅 USER_EXPORT/MANUAL_IMPORT 为 AVAILABLE；PUBLIC_WEB_READ=NOT_FEASIBLE；LIVE_API=NOT_AVAILABLE_CURRENTLY。Query 为任务参数。禁止造假数据与 Archive 回流。不实现 Learning→Acquisition 闭环与完整 Model Router。 |
| **Scope** | `acquisition_engine.py` · adapters · Constitution #28 · UA · Current State |
| **Effect** | acquisition_tasks / acquisition_policy；Engine v0 MANUAL+KEYWORD_SEARCH |
| **Non-Goals** | 生产级爬虫；绕过风控；AI Query Planner 完整实现；UI；Learning 驱动采集 |
| **Rejected Alternatives** | (A) Engine 内嵌闲鱼 HTML；(B) 宣称 LIVE 可用；(C) query 写死虚拟资料；(D) sample 补 Current DB；(E) Cursor=产品生产 AI |
| **Review Condition** | 若出现「无资格宣称 LIVE」或「Engine 含平台 DOM 细节」或「造假补数」— 以本 DEC 否决 |

---

### Decision ID: DEC-20260830-032（DEC-032）

| 字段 | 内容 |
|------|------|
| **编号** | DEC-032 / DEC-20260830-032 |
| **标题** | Search Result Origin & Missing Field Integrity |
| **日期 / Entry 来源** | 2026-08-30 · **Entry 062** |
| **背景 / Problem** | 061 将空搜后的「猜你喜欢」混入候选；want_count 缺失易被误写成 0 或归因「未登录」。 |
| **决策 / Decision** | (1) `result_origin` 必须区分 `SEARCH_RESULT` / `RECOMMENDED_RESULT` / `UNKNOWN`；仅 SEARCH_RESULT 可作为 query-specific market evidence。(2) 字段缺失状态：`VISIBLE_ON_CARD` / `MISSING_ON_CARD` / `AVAILABLE_ON_DETAIL` / `UNAVAILABLE` / `UNKNOWN`。(3) `NULL ≠ 0`；`MISSING ≠ ZERO`。(4) 匿名测试无法获取 ≠ 证明「因未登录」。(5) Observation 允许 `valid_without_want_count=true`。 |
| **Scope** | Browser/Import collectors · Observation candidates · Future Signal weighting · Constitution · UA · KUP |
| **Effect** | Entry 062 tooling + audits；Signal 层日后对 missing 降权而非造假 |
| **Non-Goals** | 登录对比实验；强制 want_count；把推荐当搜索命中 |
| **Rejected Alternatives** | (A) 猜你喜欢填充搜索批次；(B) NULL→0；(C) 缺失即丢弃整条；(D) 未登录=缺失根因（无证据） |
| **Review Condition** | 若出现「推荐当搜索证据」或「NULL 写成 0」或「无证据宣称登录导致缺失」— 以本 DEC 否决 |

---

## Template

```
### Decision ID: DEC-YYYYMMDD-NNN（DEC-NNN）

| 字段 | 内容 |
|------|------|
| **编号** | |
| **标题** | |
| **日期 / Entry 来源** | |
| **背景** | |
| **决策** | |
| **原因** | |
| **影响** | |
| **Rejected Alternatives** | |
| **Review Condition** | |
```
