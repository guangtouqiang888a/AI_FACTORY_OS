# AI_FACTORY_OS Core Governance Materialization Design Report

> **核心治理结构落地设计报告** | Core Governance Materialization Design（只设计验证，不落地实施）  
> **Date:** 2026-07-15  
> **Scope:** 最终候选治理结构（8 核心 + 1 强制卫星）对 `docs/` 重要知识的承载能力  
> **前置输入：**  
> - `docs/07_AUDIT/structure/AI_FACTORY_OS_KNOWLEDGE_GOVERNANCE_AUDIT_REPORT.md`  
> - `docs/07_AUDIT/structure/AI_FACTORY_OS_KNOWLEDGE_MIGRATION_MAP_REPORT.md`  
> - `docs/07_AUDIT/structure/AI_FACTORY_OS_CORE_STRUCTURE_VALIDATION_REPORT.md`  
> **Constraint：** 本任务**只分析设计**。未修改任何既有 Markdown / Python / Database / commercial_assets / Runtime；未创建核心治理文件；未删/移/改名；未做架构调整。  
> **唯一产出：** 本报告（`docs/audit/`，**非**核心治理文件）。

---

## 0. 执行摘要

| 问题 | 结论 |
|------|------|
| **候选结构（8+1）是否可作为最终治理结构？** | **是（设计批准）** |
| **能否覆盖商业 / 架构 / 决策 / 协作 / 状态 / 更新？** | **能覆盖（角色齐全）**；实施前仍须创建 2 个空槽并充实 Decision Log |
| **是否允许进入实施阶段？** | **条件允许（Conditional GO）** — 仅 Docs-only Materialization Entry；禁止借机改 Reality |
| **本任务是否已落地文件？** | **否** — 仅设计 |

**推荐对外称呼：**

```
Core Governance Set v1（核心治理集 v1）=
  8 Cognitive Core Files + AUTHORITY_MODEL（Mandatory Satellite）
```

---

## 1. 最终治理结构建议

### 1.1 批准结构

```
┌──────────────────────────────────────────────────────────────┐
│ Level 0  用户决策权（User Decision Authority）                 │
└──────────────────────────────────────────────────────────────┘
┌──────────────────────────────────────────────────────────────┐
│ Reality（非 docs）：Runtime / Code / DB / commercial_assets   │
│ （由 AUTHORITY_MODEL 声明优先于一切文档）                      │
└──────────────────────────────────────────────────────────────┘
┌─ Core Cognitive Layer（核心认知层 · 8）───────────────────────┐
│ 1 PROJECT_CONSTITUTION                                        │
│ 2 BUSINESS_STRATEGY          ← 待创建                          │
│ 3 CONTROL_CENTER                                              │
│ 4 CURRENT_STATE                                               │
│ 5 DECISION_LOG               ← 待充实                         │
│ 6 EXECUTION_PROTOCOL                                          │
│ 7 KNOWLEDGE_UPDATE_PROTOCOL  ← 待创建                          │
│ 8 UNIFIED_ARCHITECTURE                                        │
├─ Mandatory Satellite（强制卫星 · 1）──────────────────────────┤
│ ★ AUTHORITY_MODEL            ← 已存在；保持独立文件            │
└──────────────────────────────────────────────────────────────┘
┌─ Reference Layer（参考层 · 不升核心）─────────────────────────┐
│ MODULE_REGISTRY · SYSTEM_GOVERNANCE · Ownership/Lifecycle     │
│ Contracts/Blueprints · audit/* · PROJECT_STATUS / HISTORY …   │
│ BUSINESS_PLAN（历史）· WORK_PRINCIPLES（待裁决后降级）         │
│ DOCUMENTATION_MAP → 实施时吸收进 KNOWLEDGE_UPDATE 或降为索引   │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 落地文件命名约定（实施时用，本任务不创建）

| 槽位 | 建议路径 |
|------|----------|
| PROJECT_CONSTITUTION | `docs/00_GOVERNANCE/AI_FACTORY_OS_PROJECT_CONSTITUTION.md`（已有） |
| BUSINESS_STRATEGY | `docs/03_BUSINESS/AI_FACTORY_OS_BUSINESS_STRATEGY.md`（**新建**；PLAN 保留为历史） |
| CONTROL_CENTER | `docs/00_GOVERNANCE/AI_FACTORY_OS_CONTROL_CENTER.md`（已有） |
| CURRENT_STATE | `docs/01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md`（已有） |
| DECISION_LOG | `docs/00_GOVERNANCE/AI_FACTORY_OS_DECISION_LOG.md`（已有） |
| EXECUTION_PROTOCOL | `docs/00_GOVERNANCE/AI_FACTORY_OS_EXECUTION_PROTOCOL.md`（已有） |
| KNOWLEDGE_UPDATE_PROTOCOL | `docs/00_GOVERNANCE/AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md`（**新建**） |
| UNIFIED_ARCHITECTURE | `docs/02_ARCHITECTURE/AI_FACTORY_OS_UNIFIED_ARCHITECTURE.md`（已有） |
| AUTHORITY_MODEL | `docs/00_GOVERNANCE/AI_FACTORY_OS_AUTHORITY_MODEL.md`（已有 · 强制卫星） |

### 1.3 第一部分：覆盖验证

| 知识域 | 主承载 | 辅承载 | 覆盖判定 |
|--------|--------|--------|----------|
| **商业知识** | BUSINESS_STRATEGY | CONSTITUTION（使命级）；Control（阶段导航） | **设计覆盖完整** |
| **架构知识** | UNIFIED_ARCHITECTURE | CURRENT_STATE（Runtime 现实）；MODULE_REGISTRY（L2） | **设计覆盖完整** |
| **历史决策** | DECISION_LOG | — | **槽位完整；存货不足（实施必补）** |
| **AI 协作规则** | EXECUTION_PROTOCOL | CONTROL_CENTER（Bootstrap） | **已较强** |
| **当前状态** | CURRENT_STATE | Control（导航摘要）；Reality | **设计正确**（唯一文档现实投影） |
| **更新机制** | KNOWLEDGE_UPDATE_PROTOCOL | Execution After；AUTHORITY | **设计覆盖；文件待建** |

**结论：** 候选 **8+1 足以覆盖全部重要知识类别**；不需要为本报告新增第 10 类「核心叙事文件」（详见 §6）。

---

## 2. 文件职责矩阵

### 2.1 应保存 / 禁止保存

| 文件 | 应该保存什么 | 禁止保存什么 |
|------|--------------|--------------|
| **PROJECT_CONSTITUTION** | 使命；长期方向；永久原则；永久禁止；Pilot 锚点；三条口令（Blueprint≠Runtime 等） | Entry 流水；字段清单；市场指标；临时阶段细节；可频繁改的战术 |
| **BUSINESS_STRATEGY** | 商业模式；价值路径；收入逻辑；市场验证方法；Human-in-the-loop 商业理由；验证路线图（指针） | Runtime 完成假象；JSON 状态细表；「已完成系统状态」类过时清单；代码路径细节 |
| **CONTROL_CENTER** | Session Bootstrap；Current Phase；Primary Goal；Forbidden；Required Reading；风险短表；核心指针 | 长篇推导；契约全文；审计正文；第二套宪法 |
| **CURRENT_STATE** | Completed / In Progress / Blocked；Known Issues 摘要；Pilot IDs；「实施未开始」诚实标记 | 愿景辩论；否决方案长文；未来蓝图当已完成；未核对 Reality 的 Status 文案 |
| **DECISION_LOG** | DEC-ID；决策；理由；**Rejected Alternatives**；Review Condition；不可重复错误（可附录） | 日常 commit 日志；未战略化的 Entry 完成记录（→ HISTORY）；删除旧 DEC |
| **EXECUTION_PROTOCOL** | Before/During/After；Human Readability；Self Review Gate；Scope；输出形态；回滚默认 | 商业状态机全文；架构分层重述；DB schema |
| **KNOWLEDGE_UPDATE_PROTOCOL** | 触发类型；必须更新文件列表；更新顺序；谁可改核心文件；禁止动作；与 Reality 同步规则 | 具体商业策略正文；模块实现细节 |
| **UNIFIED_ARCHITECTURE** | 目标分层；Core OS / CF / Commercial 关系；技术与数据边界摘要；Not Started 声明 | 「已 Runtime 融合」虚假声明；协作礼仪；DEC 全文 |
| **AUTHORITY_MODEL**（卫星） | 权威序；冲突决议伪代码；Domain SoT 提醒 | 阶段目标；商业模式；长蓝图 |

### 2.2 职责边界简图

```
CONSTITUTION     「为什么 / 不可破」
BUSINESS_STRATEGY「如何赚钱与如何验证」
CONTROL_CENTER   「此刻读什么 / 禁什么」
CURRENT_STATE    「此刻事实是什么」
DECISION_LOG     「为何选了这条路 / 否决了什么」
EXECUTION_PROTOCOL「本任务如何做」
KNOWLEDGE_UPDATE 「事实或规则变了更新谁」
UNIFIED_ARCHITECTURE「系统长什么样（目标）」
AUTHORITY_MODEL  「吵架时听谁的」
```

---

## 3. 权威模型建议

### 3.1 设计目标

在现有 `AUTHORITY_MODEL`（Reality 优先）之上，增加 **文档间**层级，并单独设立 **Level 0 用户决策权**。

### 3.2 层级定义（Level 0 + Level 1–5）

| Level | 名称 | 含义 | 冲突时 |
|-------|------|------|--------|
| **0** | **用户决策权（User Decision Authority）** | 用户在当次任务中的明确授权、否决与范围裁定 | **高于一切文档解释**；不可被 AI 用旧文档绕过；但仍**不能伪造 Reality**（不能口头宣布 DB 已迁移若磁盘未变） |
| **1** | **Reality（运行现实）** | Runtime / Code / Database / commercial_assets | 文档与 Reality 冲突 → **改文档**；不改 Reality（除非用户授权 Entry） |
| **2** | **导航与裁决控制集** | AUTHORITY_MODEL + CONTROL_CENTER（入口/禁止/必读）+ CURRENT_STATE（事实投影） | 控制会话行为；State 落后于 Reality → 先恢复 State |
| **3** | **战略承诺集** | PROJECT_CONSTITUTION + DECISION_LOG + BUSINESS_STRATEGY | 宪法最稳；DEC 可被新 DEC 取代（不删旧）；STRATEGY 可变但须走 Update Protocol |
| **4** | **作业与结构集** | EXECUTION_PROTOCOL + KNOWLEDGE_UPDATE_PROTOCOL + UNIFIED_ARCHITECTURE | 协议冲突以新 DEC / 用户裁定为准；UA 服从「Blueprint≠Runtime」 |
| **5** | **参考与台账集** | MODULE_REGISTRY、Contracts、audit、PROJECT_STATUS、snapshot、HISTORY、BUSINESS_PLAN、WORK_PRINCIPLES… | **最低文档层**；冲突时不得覆盖 Level 2–4；聊天记忆低于本层 |

### 3.3 文件冲突速查

| 冲突对 | 优先 |
|--------|------|
| Chat vs 任意核心文件 | 核心文件（再核 Reality） |
| PROJECT_STATUS vs CURRENT_STATE | **CURRENT_STATE**（再核 Reality） |
| BUSINESS_PLAN vs BUSINESS_STRATEGY | **BUSINESS_STRATEGY**（PLAN 历史） |
| WORK_PRINCIPLES vs EXECUTION_PROTOCOL | **EXECUTION_PROTOCOL**（除非新 DEC 裁决旧条仍有效） |
| UNIFIED_ARCHITECTURE（目标）vs CURRENT_STATE（双轨现实） | **CURRENT_STATE + Reality** 描述「现在」；UA 描述「目标」——**类型不同，禁止互相覆盖** |
| 两份 DEC 矛盾 | **较新 DEC** 取代；旧条保留标注 Superseded |
| 用户本任务范围 vs Control Center 默认禁止 | **用户 Level 0**（须在任务中**显式**授权）；未授权则禁止仍有效 |

### 3.4 与现网 AUTHORITY_MODEL 的关系

- **保留独立卫星文件**（推荐），实施时更新其「文档子层级」指向本 §3.2。  
- **不建议**把 Level 0–5 拆成第二个平行权威文件。  
- Reality 四级（Runtime/Code/DB/Assets）继续位于 Level 1 内部细节。

---

## 4. 历史知识归属规则（只映射，不迁移）

| 来源文件 | 应该继承的内容 | 未来归属目标 |
|----------|----------------|--------------|
| `BUSINESS_PLAN.md` | 愿景；半自动策略；盈利优先；收入结构 | **BUSINESS_STRATEGY**；过时「已完成」**不继承** |
| `WORK_PRINCIPLES.md` | 完整指令输出；人机分工；Current State Lock；风控半自动 | **EXECUTION_PROTOCOL**；与 Scope 冲突条 → **DECISION_LOG** 裁决后淘汰执行效力 |
| `SYSTEM_GOVERNANCE_PROTOCOL.md` | SoT；状态词汇；Governance Before Expansion | **CONSTITUTION**（原则摘要）；**DECISION_LOG**（治理层为何出现）；详文留 L2 |
| `HUMAN_ASSISTED_BOUNDARY_PROTOCOL.md` | 商业结论人辅 | **CONSTITUTION** + **DECISION_LOG** + **BUSINESS_STRATEGY**（理由） |
| `STATE_MIGRATION_PERMISSION_POLICY.md` | 禁自动商业成功 / 迁移人工边界 | **DECISION_LOG** + CURRENT_STATE Blocked |
| `UNIFIED_ARCHITECTURE.md` | 自身已是目标；补边界摘要 | **UNIFIED_ARCHITECTURE**（充实，非另起炉灶） |
| `MODULE_REGISTRY.md` | 模块职责（纠正后） | L2 保留；摘要 → **UA** + **CURRENT_STATE** |
| `DATA_OWNERSHIP` / `JSON_DATABASE_BOUNDARY` / `SCHEMA_DRIFT` | 数据边界与漂移 | **UA** 边界章 + **CURRENT_STATE** + 必要 **DEC** |
| Commercial MVP / Experiment / Contracts / Pilot Observation | 验证逻辑与栈 | **BUSINESS_STRATEGY**（逻辑+指针）；专文留 L2 |
| 039 Lifecycle / Field / Migration / Snapshot | 状态权威与迁移策略 | **DEC** + **CURRENT_STATE**；快照永不覆写 |
| `audit/10_KNOWN_ISSUES.md` / `audit/8` / Broken Entry | 错误与文档冲突 | **CURRENT_STATE** + **DECISION_LOG**（避坑） |
| `audit/2` / `audit/3` | 边界与 Runtime 流 | **UA** 前提 + **CURRENT_STATE** |
| Control / Constitution / State / Decision / Execution / Authority | 已是核心 | 就地强化；补缺槽 |
| `DOCUMENTATION_MAP.md` | 控 vs 参、反爆炸 | **KNOWLEDGE_UPDATE_PROTOCOL** |
| Migration/Governance/Structure 审计报告 | 缺口与路线元知识 | **KNOWLEDGE_UPDATE**（引用）；audit 自留痕 |
| `PROJECT_STATUS` / `system_snapshot` / `CURSOR_EXECUTION_HISTORY` | Entry 台账与投影 | **不进核心全文**；由 Update Protocol 规定同步 |

---

## 5. 更新机制设计（KNOWLEDGE_UPDATE_PROTOCOL 内容纲要）

### 5.1 强制更新顺序

```
1) 核对 Reality（若涉及）
2) Level 0 用户确认（战略级）
3) DECISION_LOG（若战略 / 否决 / 永久规则变化）
4) CURRENT_STATE
5) CONTROL_CENTER（阶段 / 目标 / 禁止 / 必读）
6) 受影响的 CONSTITUTION / BUSINESS_STRATEGY / UA / EXECUTION
7) PROJECT_STATUS / system_snapshot / CURSOR_EXECUTION_HISTORY（Entry 收尾）
8) L2 专文（仅当设计真正变化）
```

### 5.2 触发规则表

| # | 变化类型 | 必须更新 | 应当更新 | 通常新建 DEC？ |
|---|----------|----------|----------|----------------|
| 1 | **商业方向变化** | BUSINESS_STRATEGY；CONTROL_CENTER Primary Goal；CURRENT_STATE | CONSTITUTION（仅使命级变更时） | **是** |
| 2 | **架构变化** | UNIFIED_ARCHITECTURE；CURRENT_STATE；CONTROL_CENTER Focus/Forbidden | MODULE_REGISTRY；system_snapshot | **是** |
| 3 | **模块变化** | MODULE_REGISTRY；CURRENT_STATE | UNIFIED_ARCHITECTURE 边界；Broken Entry（若损坏） | 边界冲突时 **是** |
| 4 | **项目阶段变化** | CONTROL_CENTER Phase；CURRENT_STATE | BUSINESS_STRATEGY 验证段；PROJECT_STATUS | 阶段跃迁 **是** |
| 5 | **AI 工作协议变化** | EXECUTION_PROTOCOL；必要时 CONTROL_CENTER Bootstrap | WORK_PRINCIPLES 效力标注 | **是** |
| 6 | **重大错误修正** | CURRENT_STATE Known Issues；audit/10 或新 audit 条 | DECISION_LOG（避坑）；CONTROL_CENTER Risks | 改规则时 **是** |
| — | 商业 JSON / Pilot 同步 | CURRENT_STATE；迁移报告；Snapshot 只读引用 | STATUS/HISTORY | **是（授权 Entry）** |
| — | 知识治理规则本身变化 | **KNOWLEDGE_UPDATE_PROTOCOL**；DOCUMENTATION_MAP（若仍保留） | CONTROL_CENTER 指针 | **是** |

### 5.3 禁止动作（更新协议内写死）

- 无 Entry 创建第 2 个 Control Center / 第 2 部宪法  
- 用 PROJECT_STATUS 覆盖 CURRENT_STATE  
- 将 Blueprint 标记为 Runtime Completed  
- 删除历史 DEC 或 audit  
- 在未授权任务中「顺手」改 Python / DB / commercial_assets  

---

## 6. 遗漏检视：是否需要新的核心类别？

| 候选新类别 | 是否需要升为核心？ | 原因 |
|------------|-------------------|------|
| MODULE_REGISTRY Core | **否** | 详细地图属 L2；核心只需 UA + State 摘要 |
| ERROR_REGISTER 独立文件 | **否（暂）** | 由 DECISION_LOG 附录 + CURRENT_STATE + audit/10 足够；若 ISSUE>50 再评估 |
| DOMAIN_SOT_REGISTER | **否** | 放入 AUTHORITY_MODEL Domain SoT 即可 |
| PILOT_DOSSIER | **否** | Pilot 锚点在 Constitution；细节在 039-D / Observation |
| DOCUMENTATION_MAP 永久核心 | **否** | 功能并入 KNOWLEDGE_UPDATE；可降为可选索引 |
| **第 10 叙事核心** | **不需要** | 8+1 已覆盖六大知识域 |

**唯一保持「非 8 内、但强制」的类别：** `AUTHORITY_MODEL`（已在候选结构中）。

---

## 7. 风险分析

| ID | 风险 | 等级 | 缓解（实施阶段） |
|----|------|------|------------------|
| R1 | BUSINESS_STRATEGY / UPDATE 空槽导致迁移无家可归 | P0 | Materialization Entry **先建二文件骨架**再灌内容 |
| R2 | DECISION_LOG 仍空心 → 「为什么」丢失 | P0 | Wave-1 必写 Human Assisted / 禁自动成功 / Scope vs 旧整体升级等 DEC |
| R3 | UA 被误读为 Runtime SoT | P1 | 文首固定「Target Architecture ≠ Runtime Reality」 |
| R4 | BUSINESS_PLAN 与 STRATEGY 双源 | P1 | PLAN 顶栏标明 Historical；策略只认 STRATEGY |
| R5 | Update Protocol 不执行 → 巨册再漂 | P1 | Control Center Required Reading 纳入 UPDATE；Entry 收尾 Checklist |
| R6 | 实施时越权改 Reality | P0 | Entry Scope 白名单仅 docs；Python/DB/Assets = 0 |
| R7 | 8+1 与旧 CCS「7 文件」叙述并存混淆 | P2 | CONTROL_CENTER 更新「Core Governance Set v1」指针表 |

---

## 8. 是否允许进入实施阶段？

### 8.1 裁决

| 项 | 结果 |
|----|------|
| **设计是否批准？** | **YES — Core Governance Set v1（8+1）批准作为最终结构** |
| **是否允许进入实施？** | **CONDITIONAL GO** |
| **实施范围** | **仅文档：** 创建 STRATEGY + UPDATE 骨架；充实 DEC；对齐 Control/State；按归属规则摘要继承 |
| **实施禁止** | Python / DB / commercial_assets / Runtime / 删历史文件 / 架构重构 |

### 8.2 实施入口门禁（全部满足才开写）

1. 用户确认采用 **8+1**（含 AUTHORITY 卫星独立保留）。  
2. 用户确认 BUSINESS_STRATEGY = **新建文件**（推荐），BUSINESS_PLAN 降历史。  
3. 用户确认 KNOWLEDGE_UPDATE_PROTOCOL = **新建文件**。  
4. 单 Entry Scope 列出**允许修改的路径白名单**。  
5. 验收标准含：Python=0、DB=0、Assets=0；两新文件存在；DEC 至少补齐关键人辅/反自动成功类。

### 8.3 建议实施分波（供下一 Entry，非本任务）

| Wave | 内容 |
|------|------|
| **M0** | 建 STRATEGY / UPDATE 空骨架 + 职责声明 + 权威层级写入 AUTHORITY/CONTROL |
| **M1** | DEC 升格 + State/Control 同步 |
| **M2** | 商业/架构摘要继承（非删源） |
| **M3** | WORK_PRINCIPLES / PLAN 降级标注；Update 触发自检 |

---

## 9. 报告必备清单回执

| 要求章节 | 本报告位置 |
|----------|------------|
| 1. 最终治理结构建议 | §1 |
| 2. 文件职责矩阵 | §2 |
| 3. 权威模型建议 | §3 |
| 4. 历史知识归属规则 | §4 |
| 5. 更新机制设计 | §5 |
| 6. 风险分析 | §7 |
| 7. 是否允许进入实施阶段 | §8 |

---

## 10. 约束核对

| 约束 | 结果 |
|------|------|
| 只设计验证 | **Yes** |
| 修改既有 Markdown | **No** |
| 创建核心治理文件 | **No** |
| 删/移/改名 | **No** |
| Python / DB / Assets / Runtime / 架构调整 | **No** |
| 产出本设计报告 | **Yes** |

---

## 11. 结论

**Core Governance Set v1 = 8 核心认知文件 + AUTHORITY_MODEL 强制卫星** 通过最终设计验证：职责可分、权威可判、历史可归、更新可触发、重要知识可覆盖。

进入实施的条件是清晰的：**先骨架与 DEC，后摘要继承；始终 Docs-only。**  
本任务至此结束——**结构已设计完成，文件尚未物化。**

---

**Report status:** Completed — Core Governance Materialization Design（Analysis Only）  
**Design verdict:** **APPROVED (8+1)**  
**Implementation verdict:** **CONDITIONAL GO**
