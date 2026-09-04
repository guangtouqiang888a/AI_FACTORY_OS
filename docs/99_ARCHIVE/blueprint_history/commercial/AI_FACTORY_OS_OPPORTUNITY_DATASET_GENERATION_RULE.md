# AI_FACTORY_OS Opportunity Dataset Generation Rule v1

> 商业机会候选数据资产生成规范 | 最后更新：2026-07-08  
> **状态：Blueprint Completed — Project Intelligence Layer 文档，不参与运行计算**

**定位：** Opportunity Dataset Generation Rule（商业机会数据集生成规则）— 定义 **Opportunity Candidate（商业机会候选）** 数据资产**如何产生、如何质检、如何登记**的标准流程，为后续创建 Candidate 实例提供操作规范。

**上级文档：**

- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md](AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md) — Candidate Schema 与生命周期
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md](AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md) — Experiment Selection Layer（实验选择层）
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — Opportunity Object 契约
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md) — Cognition Agent 架构

**说明：** **Blueprint ≠ Implementation（蓝图不等于实施）**。本文档定义生成**规范**；不创建 Candidate 实例、不创建 JSON 数据、不写入数据库、不修改运行代码。

---

## 1. Purpose（目的）

### 1.1 规范定义

**Opportunity Candidate Dataset Generation Rule（商业机会候选数据生成规则）** 是 Commercial Intelligence Asset（商业智能资产）的**数据生产 SOP（标准操作流程）** — 回答：

> **「一条 Opportunity Candidate 数据资产，从哪来、凭什么进入 Candidate Pool、按什么格式登记？」**

### 1.2 与 Registry 的分工

| 文档 | 职责 |
|------|------|
| **OPPORTUNITY_CANDIDATE_REGISTRY** | **是什么** — Schema、生命周期、关系链 |
| **OPPORTUNITY_DATASET_GENERATION_RULE（本文档）** | **怎么来** — 来源、质检、评分、创建模板、治理 |

### 1.3 目标

| 目标 | 说明 |
|------|------|
| **标准化首批资产** | 为 30 产品 MVP 实验提供 Candidate 输入规范 |
| **防止低质量入库** | 无 Demand / Market / Competition 证据的不进入 Pool |
| **评分隔离** | Candidate Readiness ≠ Opportunity Score ≠ Experiment Priority |
| **人机过渡** | 当前人工辅助；未来 Agent 自动 — 同一规范 |

### 1.4 资产流位置

```
Data Sources（数据来源 — §2）
        ↓
Quality Rules + Readiness Score（质检 — §3–§4）
        ↓
Creation Template（创建模板 — §5）
        ↓
Candidate Pool（Registry 登记 — status: discovered）
        ↓
Lifecycle（evaluating → selected / rejected）
        ↓
Opportunity Object → Experiment Selection → Experiment Object
```

---

## 2. Data Sources（数据来源）

### 2.1 未来与当前数据来源总览

| 来源 | 英文 | 说明 | 当前可用 | 未来模块 |
|------|------|------|----------|----------|
| **1_DATA 采集** | `1_DATA` collection | Legacy / Blueprint Raw 表采集的市场信号 | ✅ Partial | `1_DATA` collector |
| **人工市场研究** | manual research | 操作者观察平台、竞品、用户咨询 | ✅ MVP 主路径 | 人工 |
| **用户反馈** | user feedback | 销售/咨询/差评回流的新机会线索 | ⚠️ Partial | Feedback → Candidate |
| **平台信号** | platform signal | 闲鱼/淘宝/Etsy 等曝光、搜索、想要数 | ✅ 人工录入 | `1_DATA` + 平台 |
| **竞争分析** | competition analysis | 同类商品数量、价格带、差异化空间 | ✅ 人工 | CompetitionAgent |

### 2.2 1_DATA 采集（Data Collection — 数据采集）

| 项 | 内容 |
|----|------|
| **输入** | `1_DATA` collector / Legacy `keywords`, `products`, `platforms` |
| **产出** | Market Signal（市场信号）— 非 Candidate |
| **转化步骤** | 人工或规则从 Signal 提取 keyword + problem → 填 Creation Template |
| **source 字段值** | `1_DATA` |
| **禁止** | 直接将 Legacy `products` 行当作 Candidate — 须显式填 Template |

### 2.3 人工市场研究（Manual Market Research — 人工市场研究）

| 项 | 内容 |
|----|------|
| **输入** | 平台浏览、行业报告、社群观察、自身商业经验 |
| **产出** | 完整 Creation Template 字段 |
| **source 字段值** | `manual` |
| **MVP Phase 1** | **主要数据来源** — Cognition 未实现 |

### 2.4 用户反馈（User Feedback — 用户反馈）

| 项 | 内容 |
|----|------|
| **输入** | customer_feedback、咨询记录、未成交原因、复购需求 |
| **产出** | 新 keyword / 新 problem 的 Candidate |
| **source 字段值** | `feedback` |
| **规则** | 须链接原 product_id 或 experiment_id（扩展 notes） |
| **禁止** | 单次负面反馈自动生成 Candidate — 须人工确认需求真实性 |

### 2.5 平台信号（Platform Signal — 平台信号）

| 项 | 内容 |
|----|------|
| **输入** | 平台后台 views/clicks/想要/搜索建议 |
| **产出** | demand_reason、competition_status 证据 |
| **source 字段值** | `external` 或 `1_DATA`（若经采集） |
| **风控** | 禁止高风险自动爬取 — 半自动 + 人工 |

### 2.6 竞争分析（Competition Analysis — 竞争分析）

| 项 | 内容 |
|----|------|
| **输入** | 同类商品列表、价格分布、评分分布 |
| **产出** | `competition_status` 字段 |
| **source 字段值** | `external` 或 `agent_draft`（未来） |
| **未来** | CompetitionAgent 自动填充 |

### 2.7 来源优先级（MVP 推荐）

```
1. 人工市场研究（manual）— 当前主路径
2. 1_DATA 采集 + 人工整理（1_DATA）
3. 用户反馈（feedback）— 有实验基础后
4. 平台信号 + 竞争分析（external）— 辅助证据
5. Agent 草稿（agent_draft）— 未来
```

---

## 3. Candidate Quality Rules（候选质量规则）

### 3.1 进入 Candidate Pool 的最低标准

Opportunity Candidate **可以**进入 Candidate Pool（status: discovered），当且仅当满足 **四类证据（Four Evidence Types）** 中 **至少三类** 有实质内容：

| 证据类型 | 英文 | 必填字段 / 内容 | 最低标准 |
|----------|------|-----------------|----------|
| **需求证据** | Demand Evidence | problem, demand_reason, target_user | 能回答「谁、什么问题、为何付费」 |
| **市场证据** | Market Evidence | market, keyword | 明确目标市场与可搜索关键词 |
| **竞争证据** | Competition Evidence | competition_status | 非空 — 低/中/高或文字描述 |
| **验证潜力** | Validation Potential | estimated_value, recommended_category | 有定价带或「待实验验证」+ Category 建议 |

### 3.2 Demand Evidence（需求证据）细则

| 检查项 | 通过 | 拒绝 |
|--------|------|------|
| target_user | 具体人群（如「自媒体新手」） | 「所有人」 |
| problem | 具体场景（如「不会做 PPT 封面」） | 「需要模板」 alone |
| demand_reason | 付费动机（省时/省钱/专业） | 空或「可能有人买」 |

### 3.3 Market Evidence（市场证据）细则

| 检查项 | 通过 | 拒绝 |
|--------|------|------|
| market | 明确平台或地域 | 空 |
| keyword | ≥ 2 字；可搜索 | 纯泛词「模板」「资料」 |
| 可观察性 | 能在目标平台搜到同类 | 完全无参照 |

### 3.4 Competition Evidence（竞争证据）细则

| competition_status | 含义 | 是否可入库 |
|--------------------|------|------------|
| 低 / 蓝海 | 同类少、差异化易 | ✅ |
| 中 | 有竞争但可差异化 | ✅ |
| 高 | 饱和但可细分 | ✅ — 须 problem 差异化 |
| 极高饱和且无差异化 | 完全同质化 | ❌ 拒绝进入 Pool |

### 3.5 Validation Potential（验证潜力）细则

| 检查项 | 说明 |
|--------|------|
| estimated_value | 有具体定价带（如 ¥19.9）或标注 `TBD_experiment` |
| recommended_category | A / B / C 之一 — 对齐 Selection Framework |
| 实验可执行 | Content Factory 能生产对应 product_type |
| 成本可接受 | Category A 优先 — 未知高成本机会延后 |

### 3.6 拒绝入库（Hard Reject）

以下情况 **不得** 创建 Candidate（即使人工想登记）：

| # | 条件 |
|---|------|
| 1 | 四类证据满足 < 3 类 |
| 2 | keyword 与已有 rejected Candidate 相同且 reject_reason = 无需求 |
| 3 | 违反平台风控 — 违规虚拟商品方向 |
| 4 | 无法对应任何 product_type（ppt/excel/word/pdf） |
| 5 | 纯 speculative — 无任何 market 或 demand 观察 |

---

## 4. Candidate Scoring（候选评分）

### 4.1 三种评分体系 — 必须隔离

| 评分 | 英文 | 层级 | 核心问题 | 产出阶段 |
|------|------|------|----------|----------|
| **Candidate Readiness Score** | readiness_score | Candidate Pool | 这条候选**数据是否足够好**可进入 evaluating/selected？ | **本文档 / Registry** |
| **Opportunity Score** | opportunity_score | Cognition | 这个市场机会**本身**有多好？ | **2_COGNITION / Contract** |
| **Experiment Priority Score** | experiment_priority_score | Selection | 是否值得**现在**做实验验证？ | **Selection Framework** |

**禁止：**

- 用 readiness_score 替代 opportunity_score
- 用 opportunity_score 替代 experiment_priority_score
- 在 Candidate 创建时填写 opportunity_score 或 recommendation
- 在 Candidate 阶段计算 experiment_priority_score

### 4.2 Candidate Readiness Score 公式（权威 — 与 Registry §5.3 一致）

```
readiness_score =
      0.25 × completeness（字段完整度 — 0~1）
    + 0.25 × problem_clarity（问题清晰度 — 人工 0~1）
    + 0.20 × demand_plausibility（需求可信度 — 人工 0~1）
    + 0.15 × competition_acceptability（竞争可接受度 — 0~1）
    + 0.15 × category_fit（与 A/B/C 策略匹配度 — 0~1）
```

### 4.3 子因子计算参考

| 因子 | 计算参考 |
|------|----------|
| **completeness** | 必填字段非空数 / 必填字段总数（§5 Template） |
| **problem_clarity** | 人工 0~1 — problem 是否具体、可验证 |
| **demand_plausibility** | 人工 0~1 — demand_reason 是否有真实观察支撑 |
| **competition_acceptability** | 低=1.0, 中=0.7, 高=0.4, 极高无差异=0.0 |
| **category_fit** | recommended_category 与 Selection Framework §5 规则一致=1.0，冲突=0.3 |

### 4.4 分数 → 动作映射

| readiness_score | status 动作 |
|-----------------|-------------|
| ≥ 0.70 | evaluating → **selected**（可进入 Opportunity 转化） |
| 0.50 – 0.69 | **evaluating** — 补充证据 |
| < 0.50 | **rejected** — 填 reject_reason |

### 4.5 评分记录（治理 — 见 §8）

创建实例时须在扩展字段或 notes 记录：

- `readiness_score` 数值
- 各子因子人工评分
- 评分人与评分时间

**不写入** opportunity_score 或 experiment_priority_score 字段。

---

## 5. Candidate Creation Template（候选创建模板）

### 5.1 创建实例时必须填写字段

创建 Opportunity Candidate 实例时（**未来执行** — 本任务不创建），须按以下模板填写：

#### 必填字段（Required）

| 字段 | 填写说明 | 示例 |
|------|----------|------|
| `opportunity_id` | `cand_YYYYMMDD_NNN` | `cand_20260708_001` |
| `source` | §2 数据来源枚举 | `manual` |
| `market` | 目标市场/平台 | `国内闲鱼虚拟商品` |
| `keyword` | 核心关键词 | `商业计划书 PPT 模板` |
| `problem` | 用户具体问题 | `创业团队缺少专业 PPT 模板，制作耗时` |
| `target_user` | 目标用户 | `创业初期中小企业主` |
| `demand_reason` | 付费动机 | `比自己做省 4 小时，比请人便宜` |
| `status` | 初始 `discovered` | `discovered` |

#### 强烈建议（Strongly Recommended）

| 字段 | 填写说明 |
|------|----------|
| `competition_status` | 低/中/高 + 一句说明 |
| `estimated_value` | `¥19.9` 或 `TBD_experiment` |
| `recommended_category` | `A` / `B` / `C` |

#### 治理扩展（Governance — 创建时一并记录）

| 字段 | 填写说明 |
|------|----------|
| `version` | `"1.0"` |
| `created_at` | ISO-8601 |
| `evidence_summary` | 四类证据摘要（notes 或扩展 JSON） |
| `readiness_score` | §4 计算结果 |
| `validator` | 登记人 / 审核人 |

### 5.2 空白创建模板（Copy-Paste 参考 — 不生成实例）

```
opportunity_id:     cand___________
source:             manual | 1_DATA | feedback | external | agent_draft
market:
keyword:
problem:
target_user:
demand_reason:
competition_status:
estimated_value:
recommended_category:   A | B | C
status:             discovered

--- 治理 ---
version:            1.0
created_at:
readiness_score:
evidence_demand:    [ ]
evidence_market:    [ ]
evidence_competition: [ ]
evidence_validation: [ ]
validator:
```

### 5.3 创建后流程

```
填写 Template → Quality Rules 检查（§3）
        ↓
计算 readiness_score（§4）
        ↓
status: discovered → evaluating
        ↓
readiness ≥ 0.70 → selected
readiness < 0.50 → rejected
        ↓
selected → 转化为 Opportunity Object（人工或 Cognition）
        ↓
Experiment Selection Framework
```

---

## 6. Human Assisted Phase（人工辅助阶段）

### 6.1 当前阶段定义

| 项 | 状态 |
|----|------|
| **阶段名称** | Human Assisted Candidate Generation（人工辅助候选生成） |
| **2_COGNITION** | ❌ 未实现 — 目录为空 |
| **Agent 自动写入** | ❌ 未实现 |
| **DB `opportunity_candidates`** | ❌ 未创建 |
| **主操作者** | 人工 + docs 规范 |

### 6.2 人工辅助 SOP（标准操作流程）

| 步骤 | 动作 | 产出 |
|------|------|------|
| 1 | 从 §2 数据来源收集观察 | 原始笔记 |
| 2 | 填写 §5 Creation Template | Candidate 草稿 |
| 3 | §3 Quality Rules 四类证据检查 | 通过 / 拒绝 |
| 4 | §4 计算 readiness_score | 分数 + 子因子 |
| 5 | 更新 status → evaluating | Registry 合规记录 |
| 6 | readiness ≥ 0.70 → selected | 可进入下游 |
| 7 | 人工映射 Opportunity Object 字段 | 过渡 — 非 Cognition 代码 |
| 8 | Selection Framework checklist | Experiment 创建决策 |

### 6.3 人工阶段禁止项

| 禁止 | 原因 |
|------|------|
| 跳过 Template 直接做实验 | 无 Candidate 资产积累 |
| 在 Candidate 填 opportunity_score | 语义越权 |
| 批量创建无证据 Candidate | 污染资产池 |
| 删除 rejected Candidate | 须 Archive — 资产治理 |

### 6.4 首批数据集规模建议（规范 — 非本任务执行）

| 批次 | 数量 | Category 倾向 |
|------|------|---------------|
| 第一批 | 5–10 条 | Category A 为主 |
| 第二批 | 10–15 条 | A + B |
| 第三批 | 补至 30+ 候选 | A + B + C |

**说明：** 本规范为**生成规则**；实际实例创建须**单独任务授权**。

---

## 7. Future Automation（未来自动化）

### 7.1 Agent 自动生成路径

```
1_DATA Raw Tables
        ↓
TrendAgent ──────────→ trend 类 Candidate 草稿
DemandAgent ─────────→ demand 证据填充
CompetitionAgent ────→ competition_status 填充
        ↓
OpportunityAgent ────→ 综合 → Opportunity Object
                      └→ 可选 Candidate agent_draft
        ↓
Quality Rules 自动校验 + readiness 预计算
        ↓
人工复核（Human-in-the-loop — MVP 保留）
        ↓
selected → opportunity_scores → Selection
```

### 7.2 各 Agent 职责

| Agent | 自动生成内容 | source 值 |
|-------|--------------|-----------|
| **TrendAgent（趋势 Agent）** | 上升趋势 keyword → keyword, market | `trend` / `agent_draft` |
| **DemandAgent（需求 Agent）** | problem, demand_reason, target_user | `agent_draft` |
| **CompetitionAgent（竞争 Agent）** | competition_status | `agent_draft` |
| **OpportunityAgent（机会 Agent）** | Opportunity Object + 可选 Candidate 链接 | `agent_draft` → selected |

### 7.3 自动化门禁

| 规则 | 说明 |
|------|------|
| agent_draft 默认 status | `discovered` — 非 selected |
| 自动 readiness ≥ 0.70 | 仍须人工或规则复核后 → selected |
| OpportunityAgent 禁止 | 直接创建 Experiment — 见 Agent Architecture |
| 批量生成上限 | 防止 Candidate Pool 污染 — 批次审批 |

### 7.4 自动化阶段

| Phase | Candidate 生成方式 |
|-------|-------------------|
| Phase 1（当前） | 100% 人工 — §6 |
| Phase 2 | Agent 草稿 + 100% 人工复核 |
| Phase 3 | Agent 草稿 + 规则自动 evaluating + 抽样人工 |
| Phase 4 | 全自动 Candidate + Human-in-the-loop 仅 selected 复核 |

---

## 8. Data Governance（数据治理）

### 8.1 治理维度

每条 Opportunity Candidate 数据资产须具备：

| 维度 | 英文 | 要求 |
|------|------|------|
| **版本** | version | Schema `1.0`；major 变更须更新本文档 |
| **来源** | source | §2 枚举之一；可追溯 |
| **时间** | created_at / updated_at | ISO-8601；状态变更须更新 updated_at |
| **验证状态** | status + readiness_score | 生命周期 + 就绪分 |

### 8.2 验证状态与资产生命周期

| status | 资产治理分类 |
|--------|--------------|
| discovered / evaluating | **Active — Experimental** |
| selected | **Active** |
| rejected | **Deprecated — 保留学习** |
| converted_to_experiment | **Archive — 链接下游** |

### 8.3 治理规则

| 规则 | 说明 |
|------|------|
| **禁止 Delete** | rejected 须保留 — 见 WORK_PRINCIPLES 历史资产保护 |
| **Audit Trail（审计轨迹）** | 状态变更须可重建 — notes / updated_at |
| **来源不可篡改** | source 创建后不改；修正须新 Candidate |
| **与 DB 隔离** | 当前无 DB — 未来 Additive 迁移须保留 JSON 历史 |
| **与 7_MEMORY 隔离** | OS Memory 不替代 Candidate 权威记录 |

### 8.4 权威治理文档

- [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](../policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md](AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md) §7

### 8.5 未来持久化

| 存储 | 状态 | 说明 |
|------|------|------|
| docs 台账 JSON | Pending — 单独任务 | MVP 过渡 |
| `opportunity_candidates` 表 | Pending — DB Extension | Blueprint 建议 |
| `opportunity_scores` 表 | Pending | Opportunity Object 持久化 |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Opportunity Candidate Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_OPPORTUNITY_CANDIDATE_REGISTRY.md` |
| Experiment Selection Framework | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SELECTION_FRAMEWORK.md` |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Cognition Agent Architecture | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Dataset Generation Rule 设计；Candidate 实例、JSON 台账、数据库、Agent 自动写入均 **Pending**。
