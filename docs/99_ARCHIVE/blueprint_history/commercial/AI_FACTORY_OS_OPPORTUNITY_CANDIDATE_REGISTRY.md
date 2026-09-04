# AI_FACTORY_OS Opportunity Candidate Registry v1

> 商业机会候选资产池登记规范 | 最后更新：2026-07-08  
> **状态：Blueprint Completed — Project Intelligence Layer 文档，不参与运行计算**

**定位：** Opportunity Candidate Registry（商业机会候选登记体系）— AI Factory OS **第一层商业机会资产池（Commercial Opportunity Asset Pool）**，连接 **Market Intelligence（市场智能）** → **Opportunity Candidate（商业机会候选）** → **Experiment Selection（实验选择）** → **Experiment Object（实验对象）**。

**相关文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — Opportunity Object 契约
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md) — Market Intelligence Layer（市场智能层）
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md](AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md) — Experiment Selection Layer（实验选择层）
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md) — Experiment Object Registry（实验对象登记）

**说明：** **Blueprint ≠ Implementation（蓝图不等于实施）**。本文档定义登记规范；不创建 Candidate 实例、不创建 JSON 数据、不创建数据库表、不修改运行代码。

---

## 1. Opportunity Candidate Definition（商业机会候选定义）

### 1.1 核心定义

**Opportunity Candidate（商业机会候选）** 是进入 Cognition 分析或 Experiment Selection 之前的**原始商业机会资产** — 由人工观察、外部输入或 Market Signal（市场信号）初步整理而成，**尚未**经过 `2_COGNITION` 标准化评分。

### 1.2 Opportunity Candidate ≠ Opportunity Object

| 维度 | Opportunity Candidate（候选） | Opportunity Object（标准对象） |
|------|----------------------------|--------------------------------|
| **性质** | 潜在机会 — 待验证假设 | 经 Cognition 分析后的标准商业机会 |
| **生产者** | 人工 / 外部 / Market Signal 整理 / 未来 Agent 草稿 | `2_COGNITION` OpportunityAgent |
| **评分** | 无 demand_score / opportunity_score | 含完整评分与 recommendation |
| **契约** | Registry Schema（本文档） | Commercial Intelligence Contract v1 |
| **消费者** | Cognition 输入 / 人工评估 / Selection 前置 | `3_DECISION` / Experiment Selection Layer |
| **持久化** | 未来 `opportunity_candidates` 表（未创建） | `opportunity_scores` 表（未创建） |
| **生命周期** | Discovered → … → Converted / Rejected | 运行时 Object — 无 Candidate 阶段 |

### 1.3 资产池定位

Opportunity Candidate Registry 是 **Commercial Intelligence Asset（商业智能资产）** 的**第一层池**：

```
Raw Market Signal（原始市场信号 — 1_DATA）
        ↓
Opportunity Candidate Pool（候选资产池 — 本文档）
        ↓
Opportunity Object（标准机会 — 2_COGNITION）
        ↓
Experiment Selection → Experiment Object
```

**目的：** 在「市场噪声」与「标准 Opportunity」之间保留**可审计、可积累、可拒绝**的中间资产层，避免未经验证的想法直接进入实验或生产。

---

## 2. Opportunity Candidate Schema（候选对象 Schema）

### 2.1 标准 JSON Schema v1

```json
{
  "opportunity_id": "",
  "source": "",
  "market": "",
  "keyword": "",
  "problem": "",
  "target_user": "",
  "demand_reason": "",
  "competition_status": "",
  "estimated_value": "",
  "recommended_category": "",
  "status": ""
}
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `opportunity_id` | TEXT | ✅ | 候选唯一 ID，建议 `cand_YYYYMMDD_NNN` |
| `source` | TEXT | ✅ | 来源：`manual` / `external` / `1_DATA` / `trend` / `feedback` / `agent_draft` |
| `market` | TEXT | ✅ | 目标市场 / 平台 / 地域，如「国内闲鱼虚拟商品」 |
| `keyword` | TEXT | ✅ | 核心关键词 |
| `problem` | TEXT | ✅ | 用户面临的问题 |
| `target_user` | TEXT | ✅ | 目标用户群 |
| `demand_reason` | TEXT | ✅ | 用户为何有需求 / 为何可能付费 |
| `competition_status` | TEXT | | 竞争概况：低 / 中 / 高；或文字描述 |
| `estimated_value` | TEXT / REAL | | 预估商业价值或定价带，如 `¥19.9` 或 `medium` |
| `recommended_category` | TEXT | | 建议实验品类：`A` / `B` / `C` / 空 |
| `status` | TEXT | ✅ | 生命周期状态 — 见 §3 |

### 2.3 扩展字段（Registry v1.0 可选 — 未来 minor 版本）

| 字段 | 说明 |
|------|------|
| `version` | Schema 版本，默认 `"1.0"` |
| `created_at` | ISO-8601 创建时间 |
| `updated_at` | 最后更新时间 |
| `linked_opportunity_object_id` | 转化后关联 Opportunity Object / opportunity_scores.id |
| `linked_experiment_id` | 若直达实验 — 关联 experiment_id |
| `reject_reason` | status = rejected 时必填 |
| `notes` | 人工备注 |

**MVP Phase 1：** 仅使用 §2.1 核心字段即可登记；扩展字段在 Implementation 时 Additive 增加。

### 2.4 与 Opportunity Object 字段映射（转化参考）

| Candidate 字段 | Opportunity Object 字段 |
|----------------|-------------------------|
| `keyword` | `keyword` |
| `problem` + `demand_reason` | `product_idea`（合成） |
| `target_user` | 写入 product_idea 上下文 |
| `competition_status` | 人工映射 → `competition_score`（Cognition 阶段） |
| `estimated_value` | 人工映射 → `profit_score` 参考 |
| `recommended_category` | Experiment Selection Category 参考 |
| — | `demand_score`, `trend_score`, `difficulty_score` — **仅 Cognition 产出** |

**禁止：** 在 Candidate 阶段填写 `opportunity_score` 或 `recommendation` — 该职责属 Opportunity Object / `2_COGNITION`。

---

## 3. Lifecycle（生命周期）

### 3.1 状态定义

| 状态 | 英文 | 含义 |
|------|------|------|
| **Discovered（已发现）** | discovered | 候选已登记，尚未评估 |
| **Evaluating（评估中）** | evaluating | 人工或 Cognition 正在分析 |
| **Selected（已选中）** | selected | 通过评估，可进入 Opportunity Object 转化或 Selection |
| **Rejected（已拒绝）** | rejected | 不进入下游；保留资产供学习 |
| **Converted_to_Experiment（已转化实验）** | converted_to_experiment | 已沿 Candidate → Object → Experiment 链路转化 |

### 3.2 状态流转

```
Discovered（已发现）
        ↓
Evaluating（评估中）
        ↓
    ┌───┴───┐
    ↓       ↓
Selected  Rejected
    ↓
（转化为 Opportunity Object — Cognition 或人工标准化）
    ↓
Experiment Selection Layer
    ↓
Experiment Object 创建
    ↓
Converted_to_Experiment（已转化实验）
```

### 3.3 转换条件

| 从 | 到 | 条件 |
|----|-----|------|
| discovered | evaluating | 核心五字段非空：keyword, problem, target_user, demand_reason, market |
| evaluating | selected | 通过 §5 Evaluation Rules |
| evaluating | rejected | 不满足评估规则；须填 reject_reason |
| selected | converted_to_experiment | Opportunity Object 已生成 + Selection 通过 + Experiment Object 已创建 |
| rejected | — | 终态；可 Archive，不 Delete |
| converted_to_experiment | — | 终态；保留 linked_experiment_id |

### 3.4 与 Experiment Object feedback_status 区别

| 层 | 状态字段 | 管辖对象 |
|----|----------|----------|
| Candidate Registry | `status` | Opportunity Candidate |
| Experiment Registry | `feedback_status` | Experiment Object |

二者**不得混用**同一字段名或同一状态机。

---

## 4. Relationship（层级关系）

### 4.1 完整商业智能链

```
Market Intelligence（市场智能）
    1_DATA Market Signal
    2_COGNITION Agents（未来）
        ↓
Opportunity Candidate（商业机会候选 — 本文档）
        ↓
Opportunity Object（商业机会对象 — Contract v1）
        ↓
Experiment Selection（实验选择 — Selection Framework）
        ↓
Experiment Object（实验对象 — Object Registry）
        ↓
3_DECISION → 11_CONTENT_FACTORY → Feedback
```

### 4.2 各层职责

| 层 | 输入 | 输出 | 文档 |
|----|------|------|------|
| **Market Intelligence** | External Data | Market Signal / Candidate 草稿 | COGNITION_BLUEPRINT |
| **Opportunity Candidate Pool** | Signal / 人工 / 外部 | 标准化 Candidate 登记 | **本文档** |
| **Cognition 标准化** | Candidate（selected） | Opportunity Object | COMMERCIAL_INTELLIGENCE_CONTRACT |
| **Experiment Selection** | Opportunity Object | Experiment 创建决策 | SELECTION_FRAMEWORK |
| **Experiment Registry** | Selection 批准 | Experiment Object | EXPERIMENT_OBJECT_REGISTRY |

### 4.3 MVP Phase 1 路径（无 Cognition 代码）

```
人工 / 1_DATA 观察
        ↓
Opportunity Candidate（status: discovered → evaluating → selected）
        ↓
人工映射为 Opportunity Object 字段（过渡 — 非标准 Cognition 产出）
        ↓
Experiment Selection Framework checklist
        ↓
Experiment Object（draft）
```

**说明：** MVP 允许人工跳过 Cognition **代码**，但**不可跳过** Candidate 登记与 Selection 规则。

### 4.4 未来路径（Cognition Active）

```
1_DATA → TrendAgent / DemandAgent / CompetitionAgent
        ↓
OpportunityAgent 生成 Candidate 草稿 或 直接 Opportunity Object
        ↓
Candidate Pool 积累（agent_draft 来源）
        ↓
人工或规则筛选 → selected
        ↓
Opportunity Object 写入 opportunity_scores
        ↓
Experiment Selection → Experiment Object
```

---

## 5. Evaluation Rules（评估规则）

### 5.1 进入 Experiment Selection 的前置条件

Opportunity Candidate 须 **status = selected**，且满足以下**全部**条件后，方可进入 Experiment Selection Layer（消费 Opportunity Object 或等效人工映射）：

| # | 条件 | 说明 |
|---|------|------|
| 1 | 核心字段完整 | keyword, problem, target_user, demand_reason, market, source 非空 |
| 2 | 无重复 active Candidate | 同 keyword 无其他 selected / evaluating 候选 |
| 3 | 竞争可接受 | competition_status ≠ 「极高饱和且无差异化」 |
| 4 | 预估价值合理 | estimated_value 非空或明确「待实验验证」 |
| 5 | Category 建议一致 | recommended_category 与 Selection Framework §5 不冲突 |
| 6 | 未在 Rejected 硬阻断列表 | 同 keyword 有 2+ rejected 且原因为「无需求」— 见 Selection Framework §7 |

### 5.2 Discovered → Evaluating 门禁

| 检查项 | 规则 |
|--------|------|
| 关键词质量 | keyword 长度 ≥ 2；非纯泛词（如「模板」 alone） |
| 问题描述 | problem 须描述具体场景，非空泛陈述 |
| 来源可追溯 | source 必填 |

### 5.3 Evaluating → Selected 评分（Candidate 层 — 非 Opportunity Score）

Candidate 层使用 **Candidate Readiness Score（候选就绪分）** — 与 opportunity_score **隔离**：

```
readiness_score =
      0.25 × completeness（字段完整度）
    + 0.25 × problem_clarity（问题清晰度 — 人工 0~1）
    + 0.20 × demand_plausibility（需求可信度 — 人工 0~1）
    + 0.15 × competition_acceptability（竞争可接受度）
    + 0.15 × category_fit（与 A/B/C 策略匹配度）
```

| readiness_score | 动作 |
|-----------------|------|
| ≥ 0.70 | selected |
| 0.50 – 0.69 | 保持 evaluating；补充信息 |
| < 0.50 | rejected |

### 5.4 Selected → Experiment Selection 交接

Selected Candidate 须先转化为 **Opportunity Object**（Cognition 或人工映射），再进入 [Selection Framework §6](AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md) 创建 Experiment。

**禁止：** status = selected 的 Candidate **直接**创建 Experiment Object，跳过 Opportunity Object 与 Selection Layer。

---

## 6. Future Cognition Connection（未来认知层连接）

### 6.1 Agent 与 Candidate 生成

未来 `2_COGNITION` 五 Agent 与 Candidate 池的关系：

| Agent | 对 Candidate Pool 的贡献 |
|-------|-------------------------|
| **TrendAgent（趋势 Agent）** | 从 `market_keywords` 识别上升趋势 → 自动生成 `source: trend` 的 Candidate 草稿 |
| **DemandAgent（需求 Agent）** | 从 `market_demands` 提取问题与 target_user → 填充 problem / demand_reason |
| **CompetitionAgent（竞争 Agent）** | 分析竞品密度 → 填充 competition_status |
| **OpportunityAgent（机会 Agent）** | 综合前三者 → 产出 **Opportunity Object**；可选同时写 Candidate `agent_draft` 供人工复核 |
| **InsightAgent（洞察 Agent）** | 从 Feedback / 实验 learning_summary 回流 → 生成 `source: feedback` 的新 Candidate |

### 6.2 自动生成流程（Blueprint）

```
1_DATA Collector
        ↓
Raw Tables（market_*）
        ↓
TrendAgent + DemandAgent + CompetitionAgent（并行）
        ↓
Candidate 草稿（status: discovered, source: agent_draft）
        ↓
人工复核 或 规则自动 evaluating
        ↓
OpportunityAgent → Opportunity Object + opportunity_scores
        ↓
Candidate status → selected
        ↓
Experiment Selection Layer
```

### 6.3 Agent 禁止项

| 禁止 | 原因 |
|------|------|
| Agent 直接创建 Experiment Object | 须过 Selection Layer |
| Agent 跳过 Candidate 直接 mass-produce | 资产池失去审计层 |
| OpportunityAgent 写 Candidate 为 selected 且无人工/规则门禁 | MVP 须 Human-in-the-loop |

### 6.4 与 Cognition Blueprint 对齐

详见 [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md) — OpportunityAgent **禁止**生产商品、修改 Content Factory、直接发布。

---

## 7. Asset Governance（资产治理）

### 7.1 资产分类

Opportunity Candidate Registry 属于 **Commercial Intelligence Asset（商业智能资产）** — 与 Database Raw Layer、Opportunity Scores、Experiment Registry 同级长期资产。

| 属性 | 说明 |
|------|------|
| **资产类型** | Commercial Intelligence Asset — Candidate Pool |
| **物理位置（当前）** | docs 登记规范 — 无运行文件 |
| **物理位置（未来）** | `opportunity_candidates` 表 或 `docs/candidates/` 台账 — **均未创建** |
| **生命周期** | Active（discovered ~ selected）→ Archive（rejected / converted） |
| **删除策略** | **禁止直接 Delete** — 须 Audit → Classify → Archive → Approval |

### 7.2 治理规则

| 规则 | 说明 |
|------|------|
| **可追溯** | 每条 Candidate 须含 source + created_at |
| **可拒绝** | rejected 候选保留 — 供 Failure Learning |
| **可转化** | converted_to_experiment 须链接 experiment_id |
| **与 Legacy 隔离** | Legacy `keywords` / `products` 不自动等于 Candidate — 须显式登记 |
| **与 7_MEMORY 隔离** | OS 运行记忆不替代 Candidate Pool |

### 7.3 权威治理文档

- [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](../policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)
- [docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md](../../99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md) — 历史资产保护原则

### 7.4 未来数据库映射（Blueprint — 未创建）

| Registry 字段 | 建议表 `opportunity_candidates` |
|---------------|--------------------------------|
| 全部 §2.1 字段 | 对应列 |
| `linked_opportunity_object_id` | FK → `opportunity_scores.id` |
| `linked_experiment_id` | FK → `commercial_experiments.experiment_id` |

**实施须：** Database Extension 审批 + Additive Evolution — 见 Implementation Plan。

---

## 8. Registry 使用说明

### 8.1 当前阶段（Blueprint Only）

| 项 | 状态 |
|----|------|
| 登记规范 | ✅ 本文档 |
| Candidate 实例 | ❌ 禁止在本阶段批量创建 |
| JSON 台账 | ❌ 未创建 |
| DB 表 | ❌ 未创建 |
| Cognition 自动写入 | ❌ 未建 |

### 8.2 登记检查清单

- [ ] `opportunity_id` 唯一（`cand_*` 前缀）
- [ ] `source` 可追溯
- [ ] 核心字段非空
- [ ] `status` 符合 §3 状态机
- [ ] 未填写 opportunity_score / recommendation
- [ ] selected 前通过 readiness_score 或人工等效评估
- [ ] 进入 Selection 前已转化为 Opportunity Object

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Cognition Blueprint | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| Experiment Selection Framework | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md` |
| Experiment Object Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Opportunity Candidate Registry 设计；Candidate 实例、JSON 台账、数据库表、Cognition 自动写入均 **Pending**。
