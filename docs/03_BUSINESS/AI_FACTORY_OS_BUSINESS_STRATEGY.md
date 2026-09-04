# AI_FACTORY_OS Business Strategy

> **Business Strategy（商业战略）** — 当前有效商业战略唯一入口  
> Core Governance Set v1（核心治理集 v1）  
> Last updated: 2026-08-29（Entry **049** / **DEC-020** — Phase 1 Scope ≠ 永久边界；**方向未改：仍数字商品验证准备**）  
> **Update frequency: MEDIUM（中等）** — 商业方向变化时必须经 Knowledge Update Protocol（知识更新协议）更新

**定位：** 本文定义「如何创造与验证商业价值」— **商业方向唯一文档归属**（DEC-016）。  
**不是：** Current State；**不是**模块 Status 表；**不是**历史演进主文；**不是**历史规划全文副本。早期长文见 `AI_FACTORY_OS_BUSINESS_PLAN.md`（Historical Reference）。

冲突时：以本文 + Current State（当前状态）+ Reality（运行现实）为准；不以旧 Business Plan 的「已完成」清单为准。

**Entry 040-D2-B 修改原因：** 按商业知识归位分析，补充「第一收入来源 / 盈利阶段 / 禁止误判 / 长期价值闭环」摘要；**不改变**既有商业方向（仍为商业验证准备 + 半自动 + 数字商品优先）。

---

## 1. 商业使命（Business Mission）

在**可控治理**下，建设可重复的商业验证能力：

- 发现可试验的产品机会（Opportunity，商业机会）
- 经 Content Factory（内容工厂）生产数字产品资产（Product Asset）
- 以 Human Assisted（人工辅助）方式发布与观测市场反馈
- 用真实反馈更新判断，而不是用假设或伪造指标宣称成功

近程目标不是「全自动赚钱机器」，而是：**可审计的商业验证准备与执行能力**。

### 1.1 Phase 1 Scope vs Permanent Boundary（DEC-020）

| | 内容 |
|--|------|
| **Current Product Scope（Phase 1）** | **只做虚拟资料类产品**（严格 Scope Control） |
| **Architecture / Long-term** | 多产品类型自主商业学习系统（Future-Extensible；**Not Built**） |
| **禁止误读** | 「当前只做虚拟资料」≠「系统永久只能虚拟资料」 |
| **Human Gate** | 管高风险外部行为（发布/付款/广告/账号），不是逐产品人工商业审批 |

长期方向见 Constitution **Autonomous Commercial Learning Principle**；当前 Reality 仍以 Pilot 人辅准备 + 观察未开始为准。

---

## 2. 商业价值创造方式（How Value Is Created）

价值来自闭环，而不是单次内容生成：

```
机会发现 → 实验设计 → 生产请求 → 内容/产品资产生产
  → 人工确认发布 → 观察与反馈 → 学习与下一轮选择
```

| 环节 | 作用 |
|------|------|
| 机会与实验 | 把「可能卖什么」变成可追踪实验对象 |
| Content Factory | 把请求变成可交付的产品资产 |
| 人工确认节点 | 控制平台风控与发布责任 |
| Feedback / Evaluation（反馈/评估） | 沉淀真实结果，供后续决策 |

长期可演进的收入设想（**愿景层**，非当前已验证收入）：

1. **能力调用** — AI 决策/分析能力按量或分层调用  
2. **模块化能力** — 选品、内容、决策等能力组合  
3. **企业级/部署型服务** — 更高隔离与定制（远期）

**当前阶段不以 SaaS 营收数字为完成标准。** 完成标准是验证栈可运行、可追溯、结论可信。

### 2.1 长期价值闭环（Long-Term Value Loop）

长期价值来自可重复闭环（与早期规划一致，**近程不要求全部自动化**）：

```
数据资产 → 市场洞察 → 商品生产 → 销售/发布反馈 → 系统优化 → 数据资产积累
```

---

## 3. 产品 / 资产价值路径（Product & Asset Value Path）

```
Opportunity Candidate（机会候选）
  → Opportunity（机会对象）
  → Experiment（商业实验）
  → Production Request / PR（生产请求）
  → Product Asset（产品资产）
  → Feedback / Observation（反馈/观察）
  → Experiment Evaluation（实验评估）
```

| 原则 | 说明 |
|------|------|
| 对象可追踪 | 关键 Pilot（试点）ID 必须可回溯，例如 `preq_20260712_005`、Product Asset `8523329941d4` |
| 契约优先 | 对象字段与生命周期以既有 Contract（契约）与 Field Standard（字段标准）为准 |
| 生产 ≠ 商业成功 | 资产生产完成只证明交付能力，不证明市场成功 |

详文保留在商业验证 Blueprint / Contract 层；本文只固定路径逻辑。

---

## 4. 市场验证原则（Market Validation Principles）

1. **先验证，后扩张** — 在治理与观察未就绪前，不放大自动化与投放规模。  
2. **真实数据优先** — 禁止伪造销量、收入、好评或「已验证成功」。  
3. **观察有协议** — Pilot Observation（试点观察）须按协议执行；未开始观察不得宣称实验结论。  
4. **状态诚实** — commercial_assets（商业资产）中的状态字段若与审批/生产现实不一致，以 Reality 为准，并用授权 Entry 同步；禁止用文档话术覆盖 JSON。  
5. **Isolated Active ≠ 全系统自动化** — Content Factory 可独立生产，不表示 Core OS（核心操作系统链）已与 CF Runtime 融合。

---

## 5. 人工参与边界（Human Assisted Boundary）

| 可为 AI / 系统辅助 | 必须 Human Assisted（人工确认） |
|--------------------|--------------------------------|
| 候选整理、草案生成、流水线生产辅助 | 商业成功 / 失败结论 |
| 技术验收（如 Validation Gate 技术通过） | 上架/发布最终确认（按风控策略） |
| 状态迁移**建议**与分析 | 商业 JSON 生命周期同步写入（须授权 Entry） |
| 风险与冲突记录 | 收入、市场验证成功字段的写入 |

**Human Assisted ≠ Automation（人工辅助 ≠ 自动化）：**  
自动化可提高生产效率，**不能**自动裁定商业结果（见 DEC-008）。

---

## 6. 商业决策原则（Commercial Decision Principles）

1. **盈利可行性优先于炫技自动化** — 稳定性与风控优先于「全自动发布」。  
2. **半自动发布** — AI 生成与筛选 → 人工确认 → 工具辅助发布 → 反馈学习。  
3. **禁止高风险绕过平台规则的行为设计。**  
4. **Blueprint ≠ Runtime（蓝图 ≠ 运行时）** — 战略/设计完成 ≠ 生产或市场完成。  
5. **Scope Control（范围控制）** — 商业相关 Reality 变更必须有明确 Entry 授权。  
6. **Governance Before Expansion（治理先于扩张）** — 文档与状态治理跟不上时，不扩大商业自动化面。

---

## 7. 当前商业方向（Current Business Direction）

| 项 | 内容 |
|----|------|
| **阶段** | Commercial Validation Preparation（商业验证准备）— **尚未**升格为 Ready for Observation（因人工未最终选定渠道/价格且未发布） |
| **主线** | Pilot 发布准备已完成 → **READY FOR HUMAN DECISION** → 人工决策后才可授权上架与观察 |
| **产能现实** | Content Factory = Isolated Active（隔离可用）；Core OS 与 CF **未** Runtime 连接 |
| **Pilot** | `preq_20260712_005` / `8523329941d4`；实验假设与 Minimum Publish Package **PREPARED**；Feedback/Evaluation **pending**；**观察未开始** |
| **分发** | Distribution：**NOT YET SELECTED**（AI 建议 taobao；备选 xianyu；≠ 已发布） |
| **价格** | 对账完成：12.9=HYPOTHESIS（建议首测）；19.9=CF CURRENT DEFAULT；9.9=对照带；**无 VALIDATED** |
| **迁移** | 商业状态迁移策略已就绪；**JSON 全量同步未执行**（RA-002） |
| **不做什么（当前）** | 不自动写商业成功；不擅自 Runtime 融合；不伪造市场数据；不把「发布准备完成」写成「已上架/已验证」 |

**下一商业动作（须人工决策 + 另开授权 Entry）：**  
确认 Decision Pack（渠道/价格/封面/发布授权）→ 人工上架并保存证据 → Observation Start。

---

## 7.1 第一收入来源与盈利阶段（Primary Revenue Focus）

| 优先级 | 盈利方向 | 状态 |
|--------|----------|------|
| **P0（当前）** | **自产数字商品销售验证**（Content Factory 可交付 PPTX/XLSX/DOCX/PDF 等） | 验证准备；观察未开始 |
| P1 | AI 生产服务（为他人提供产能） | 未来待验证 |
| P2 | 模块化 SaaS | 未来待验证 |
| P3 | API 经济 / 企业部署 | 远期愿景 |

**明确：** 当前第一收入来源设想是**数字商品**，不是已验证的 SaaS 订阅收入。历史报价表（如 $99/$499）**不作为**现行定价事实。

---

## 7.2 禁止误判事项（Anti-Misread Rules）

1. 禁止把 `BUSINESS_PLAN` §「已完成」清单当成 Current State。  
2. 禁止把 SaaS/API 愿景或历史定价当成已实现收入。  
3. 禁止把 Product Asset 生产完成当成市场/商业成功（见 DEC-008）。  
4. 禁止把 Content Factory Isolated Active 当成 Core OS Runtime 已融合。  
5. 禁止在无 Pilot Observation 数据时宣称实验成功/失败。  
6. 禁止用「提高自动化」压过盈利可行性与平台风控。

---

## 8. Modular Commercialization Strategy（模块化商业化策略）

> Entry **041-B-A** / **DEC-013**。长期产品方向：**模块化 AI 商业操作系统**。  
> 本条定义商业化路径原则；**不改变**当前阶段（仍为 Commercial Validation Preparation）；**不表示** Runtime 已融合。

未来商业化路径不仅包括完整系统服务，也包括：

* **单模块能力销售**
* **模块组合服务**
* **完整 AI_FACTORY_OS 服务**

### 示例能力线（愿景层示例，非当前已售 SKU）

**Content Factory：**

* 数字商品生产
* 短视频内容生产
* 小说内容生产
* 营销内容生产

**Data Intelligence：**

* 数据采集
* 趋势分析
* 市场洞察

**Decision Engine：**

* 商业机会筛选
* 实验评分

**Execution Module：**

* 多平台发布
* 流程执行

**边界：** 模块可独立演进与独立商业化；亦可通过治理与编排组合成完整系统。**Modular ≠ Fragmented（模块化 ≠ 碎片化）**；独立销售不等于放弃统一治理。

---

## 8.1 长期商业化方向清单（Strategic Directions — 非当前完成态）

> Entry **041-D-A**。以下为**战略方向 / 可能性**，**不是**当前完成状态，**不是**已验证收入。  
> 当前阶段仍为 **Commercial Validation Preparation**；P0 仍以数字商品验证准备为主（见 §7.1）。

AI_FACTORY_OS 未来商业化可能包括：

1. **自用 AI 商业操作系统**（内部经营与验证底座）
2. **数字产品生产**（可交付数字商品产能）
3. **内容生产体系**（可治理的内容流水线能力）
4. **短视频等内容平台商业化**（内容分发类商业化探索）
5. **企业解决方案**（组合能力包装为客户方案）
6. **SaaS 服务**（远期订阅/托管形态 — 未验证）
7. **独立能力模块商业化**（单模块或模块组合销售 — DEC-013）

**禁止：** 将本清单任何一项写成「已完成 / 已上线 / 已产生 SaaS 收入」。

---

## 8.2 Capability-based Commercialization Strategy（基于能力的商业化策略）

> Entry **041-B-B** / **DEC-014**。  
> **仅定义方向。不代表已经实现。** Blueprint ≠ Production · Design ≠ Runtime。  
> 当前阶段仍为 Commercial Validation Preparation；P0 仍见 §7.1。

未来商业化**不是单一路径**。可以包括：

### A. 完整 AI_FACTORY_OS 平台

整机/整平台服务（统一治理下的完整操作系统能力）。

### B. 能力组合产品

例如：

```
数据采集能力 + 数据库能力 + 分析能力
        ↓
    市场情报产品
```

### C. 内容商业化产品

例如：

```
数据能力 + 内容生产能力 + 执行能力
        ↓
小说生产系统 / 内容工厂类产品
```

### D. 企业解决方案

例如：

```
市场分析能力 + 决策能力
        ↓
企业 SaaS 类型服务
```

**边界：**

- Product = Capability Composition（能力组合可成产品；单能力亦可包装成产品）
- Folder ≠ 商业边界；不得把 `0`–`11` 目录名当成 SKU
- **Unified ≠ Forced Merge Runtime** — 商业组合不要求 Runtime 已融合
- 以上均为**战略方向**，禁止写成当前完成状态或已验证收入

---

## 9. 相关指针（Pointers）

| 文件 | 用途 |
|------|------|
| [PROJECT_CONSTITUTION](../00_GOVERNANCE/AI_FACTORY_OS_PROJECT_CONSTITUTION.md) | 项目使命与永久原则 |
| [CURRENT_STATE](../01_CURRENT_STATE/AI_FACTORY_OS_CURRENT_STATE.md) | 当前事实 |
| [DECISION_LOG](../00_GOVERNANCE/AI_FACTORY_OS_DECISION_LOG.md) | 正式决策 |
| [BUSINESS_PLAN](../99_ARCHIVE/AI_FACTORY_OS_BUSINESS_PLAN.md) | 历史规划参考（非默认战略入口） |
| [COMMERCIAL_MVP_BLUEPRINT](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md) | 验证蓝图详文 |
| [HUMAN_ASSISTED_BOUNDARY_PROTOCOL](../04_BLUEPRINT/protocol/AI_FACTORY_OS_HUMAN_ASSISTED_BOUNDARY_PROTOCOL.md) | 人辅边界详文 |
| [PILOT_OBSERVATION_PROTOCOL](../04_BLUEPRINT/protocol/AI_FACTORY_OS_PILOT_OBSERVATION_PROTOCOL.md) | 观察协议 |
| [BUSINESS_KNOWLEDGE_CONSOLIDATION_REPORT](../07_AUDIT/structure/AI_FACTORY_OS_BUSINESS_KNOWLEDGE_CONSOLIDATION_REPORT.md) | 040-D2-B 商业知识归位分析 |
| [ARCHITECTURE_EVOLUTION_CONTEXT_RECORD](../06_HISTORY/AI_FACTORY_OS_ARCHITECTURE_EVOLUTION_CONTEXT_RECORD.md) | 目录演进历史解释（非状态权威） |

---

**Entry 040-D1：** Business Strategy foundation created（商业战略基础已建立）。  
**Entry 040-D2-B：** 补充第一收入来源、盈利阶段、禁止误判、长期价值闭环（方向不变）。  
**Entry 041-B-A：** 新增 Modular Commercialization Strategy（模块化商业化策略）；长期方向更新为 Modular AI Business OS（现实 Runtime 不变）。  
**Entry 041-D-A：** 补充长期商业化方向清单（战略可能性；非完成态）。  
**Entry 041-B-B：** 新增 Capability-based Commercialization Strategy（§8.2）；DEC-014（方向 only；Runtime 不变）。
