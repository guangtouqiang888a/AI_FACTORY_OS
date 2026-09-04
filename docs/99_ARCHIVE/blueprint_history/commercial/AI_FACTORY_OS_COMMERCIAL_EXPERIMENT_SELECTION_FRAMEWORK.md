# AI_FACTORY_OS Commercial Experiment Selection Framework v1

> 商业实验选择规则层设计 | 最后更新：2026-07-08  
> **状态：Blueprint Completed — Project Intelligence Layer 文档，不参与运行计算**

**定位：** Experiment Selection Layer（实验选择层）— 连接 **Market Intelligence（市场智能）** → **Opportunity Object（商业机会对象）** → **Experiment Object（实验对象）**，定义「哪些机会值得进入商业实验、以何种优先级、归入哪类实验」。

**上级文档：**

- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md](AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md)
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md)
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)

**说明：** **Blueprint ≠ Implementation（蓝图不等于实施）**。本文档完成选择规则设计；不创建实验实例、不创建产品、不修改代码或数据库。

---

## 1. Framework Definition（框架定义）

### 1.1 Experiment Selection Layer（实验选择层）

**Experiment Selection Layer（实验选择层）** 是 Commercial Validation Stack（商业验证栈）中位于 **Opportunity（机会）** 与 **Experiment（实验）** 之间的 **docs 认知规则层**。

```
Market Intelligence（市场智能 — 2_COGNITION / 1_DATA）
        ↓
Opportunity Object（商业机会对象）
        ↓
Experiment Selection Layer（实验选择层 — 本文档）
        ↓
Experiment Object（实验对象 — Registry v1）
        ↓
3_DECISION → 11_CONTENT_FACTORY → Feedback
```

### 1.2 核心职责

| 职责 | 说明 |
|------|------|
| **Opportunity → Experiment** | 判定 Opportunity 是否可转化为 Experiment Object |
| **Category Assignment（品类分配）** | 分配 Category A / B / C |
| **Priority Ranking（优先级排序）** | 计算 Experiment Priority Score，排序实验队列 |
| **Selection Gate（选择门禁）** | 拒绝不应进入实验的机会（skip / watch） |
| **Failure Feedback Loop（失败反馈）** | 历史失败实验影响未来选择权重 |

### 1.3 不是什么

| 层 | 区别 |
|----|------|
| **2_COGNITION** | 产出 Opportunity Score — **是否值得关注市场机会** |
| **Experiment Selection Layer** | 产出 Experiment Priority Score — **是否值得消耗实验配额做验证** |
| **3_DECISION** | 产出 Production Request — **是否批准生产** |
| **11_CONTENT_FACTORY** | 执行生产 — **如何生产** |

**关键隔离：** Experiment Priority Score（实验优先级评分）**不得**替代 Opportunity Score（市场机会评分）。二者语义、公式、消费者均不同。

### 1.4 在 Project Intelligence Layer 中的位置

```
Commercial Validation Layer（MVP Blueprint）
        ↓
Commercial Experiment Layer（System Blueprint）
        ↓
Commercial Experiment Asset Layer（Object Registry）
        ↓
Commercial Experiment Selection Framework（Selection Layer — 本文档）
        ↓
Runtime Modules
```

---

## 2. Selection Input（选择输入）

### 2.1 主输入：Opportunity Object（商业机会对象）

Experiment Selection Layer 的**主输入**为 [Commercial Intelligence Contract §4](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) 定义的 Opportunity Object：

```json
{
  "contract_version": "1.0",
  "object_type": "opportunity",
  "keyword": "",
  "keyword_id": null,
  "demand_score": 0.0,
  "trend_score": 0.0,
  "competition_score": 0.0,
  "profit_score": 0.0,
  "difficulty_score": 0.0,
  "opportunity_score": 0.0,
  "recommendation": "produce | watch | skip",
  "product_idea": "",
  "created_at": "ISO-8601"
}
```

### 2.2 输入字段与选择用途

| 字段 | 含义 | Selection 用途 |
|------|------|----------------|
| `keyword` | 市场关键词 | Experiment Object.keyword；去重检查 |
| `demand_score` | 需求分 | Market Potential 因子 |
| `trend_score` | 趋势分 | Market Potential 因子 |
| `competition_score` | 竞争分 | Competition Risk 因子 |
| `profit_score` | 利润分 | Expected Feedback Value 因子 |
| `difficulty_score` | 生产难度分 | Production Difficulty 因子 |
| `opportunity_score` | 市场机会综合分 | **只读参考 — 不直接进入 Priority 公式** |
| `recommendation` | produce / watch / skip | **首要门禁** — 见 §6 |
| `product_idea` | 产品构想 | 生成 hypothesis 草稿 |

### 2.3 辅助输入（MVP 过渡）

| 输入 | 来源 | 用途 |
|------|------|------|
| 人工 override | 操作者 | MVP Phase 1 无 Cognition 时替代 Opportunity |
| Legacy Market Signal | `1_DATA` | 人工构造 Opportunity 前的原始信号 |
| 历史 Experiment Registry | archived 实验 | Failure Learning — 见 §7 |
| 批次配额 | 30 产品计划 | Category A/B/C 各 10 剩余名额 |

### 2.4 MVP Phase 1 输入路径

```
路径 A（未来）：1_DATA → 2_COGNITION → Opportunity Object → Selection Layer
路径 B（当前）：1_DATA / 人工 → 半结构化机会描述 → 人工映射为 Opportunity 字段 → Selection Layer
```

**禁止：** 跳过 Selection Layer 直接从 Opportunity 创建 Experiment（即使人工操作也须过 Selection 规则 checklist）。

---

## 3. Selection Criteria（选择标准）

Experiment Selection 基于 **五维选择标准（Five Selection Dimensions）** 评估每个 Opportunity 是否值得进入实验队列。

### 3.1 Market Potential（市场潜力）

| 项 | 说明 |
|----|------|
| **定义** | 机会所在市场是否有足够需求与增长空间 |
| **主要输入** | `demand_score`, `trend_score`, `keyword` 搜索上下文 |
| **高潜力信号** | demand ≥ 0.7 且 trend ≥ 0.6 |
| **低潜力信号** | demand < 0.4 且 trend < 0.4 |
| **权重（Priority 公式）** | **w1 = 0.30** |

### 3.2 Validation Cost（验证成本）

| 项 | 说明 |
|----|------|
| **定义** | 完成一次商业实验所需的综合成本（生产 + 发布 + 观察人力） |
| **主要输入** | `difficulty_score`、Category 策略、预估 `production_cost` |
| **低成本信号** | Category A 适用；difficulty ≤ 0.4；单 artifact |
| **高成本信号** | 多 artifact 组合；需大量人工复核 |
| **权重** | **w2 = 0.20**（成本越低，得分越高 — 见 §4 反向归一化） |

### 3.3 Production Difficulty（生产难度）

| 项 | 说明 |
|----|------|
| **定义** | Content Factory 生产该机会的技术与质量难度 |
| **主要输入** | `difficulty_score`, `product_idea` 复杂度, `product_type` |
| **低难度** | ppt / excel 单模板 — Category A |
| **中难度** | AI 工具包、多页 pdf — Category B |
| **高难度** | 行业资料包、多 artifact  bundle — Category C |
| **权重** | **w3 = 0.15**（难度越低，得分越高） |

### 3.4 Competition Risk（竞争风险）

| 项 | 说明 |
|----|------|
| **定义** | 市场中同类产品的饱和程度与差异化空间 |
| **主要输入** | `competition_score`（越高 = 竞争越激烈） |
| **低风险** | competition ≤ 0.5 且有明确 product_idea 差异化 |
| **高风险** | competition ≥ 0.8 且 product_idea 同质化 |
| **权重** | **w4 = 0.20**（竞争越低，得分越高 — 使用 1 − competition_score） |

### 3.5 Expected Feedback Value（预期反馈价值）

| 项 | 说明 |
|----|------|
| **定义** | 该实验预期能沉淀多少可学习、可泛化的商业反馈 |
| **主要输入** | `profit_score`, Category 类型, 关键词代表性 |
| **高价值** | 代表新品类 / 新定价带；profit ≥ 0.6 |
| **低价值** | 与已有 5+ 成功实验高度重复；无新假设 |
| **权重** | **w5 = 0.15** |

### 3.5 五维与 Opportunity 字段映射

| Selection 维度 | Opportunity 字段 | 归一化方向 |
|----------------|------------------|------------|
| Market Potential | demand_score, trend_score | 越高越好 |
| Validation Cost | difficulty_score（代理） | 越低越好 |
| Production Difficulty | difficulty_score | 越低越好 |
| Competition Risk | competition_score | 越低越好 |
| Expected Feedback Value | profit_score | 越高越好 |

---

## 4. Experiment Priority Score（实验优先级评分）

### 4.1 定义与隔离原则

| 评分 | 英文 | 负责层 | 核心问题 |
|------|------|--------|----------|
| **Opportunity Score** | opportunity_score | `2_COGNITION` | 这个市场机会本身有多好？ |
| **Experiment Priority Score** | experiment_priority_score | Experiment Selection Layer | 这个机会是否值得**现在**消耗实验配额验证？ |

**必须隔离：**

- Experiment Priority Score **不得**等于或替代 opportunity_score
- Priority 公式 **不得**直接引用 opportunity_score 作为加权项（避免双重计数）
- Priority 使用 Opportunity 的**分解字段**（demand, trend, competition 等），而非综合分
- Registry / DB 须分别存储两个分数

### 4.2 计算公式（Blueprint v1）

```
market_potential     = 0.6 × demand_score + 0.4 × trend_score

validation_cost_inv  = 1.0 − norm(estimated_validation_cost)
                       ※ estimated_validation_cost 由 difficulty + category 估算

production_ease      = 1.0 − difficulty_score

competition_ease     = 1.0 − competition_score

feedback_value       = profit_score × category_feedback_multiplier

experiment_priority_score =
      0.30 × market_potential
    + 0.20 × validation_cost_inv
    + 0.15 × production_ease
    + 0.20 × competition_ease
    + 0.15 × feedback_value
```

### 4.3 category_feedback_multiplier（品类反馈乘数）

| Category | 乘数 | 说明 |
|----------|------|------|
| A | 0.8 | 反馈价值偏低 — 验证「有没有需求」 |
| B | 1.0 | 基准 — 验证「谁愿意付费」 |
| C | 1.2 | 反馈价值偏高 — 验证「高客单是否成立」 |

### 4.4 优先级排序规则

| priority_score | 优先级 | 动作 |
|----------------|--------|------|
| ≥ 0.75 | P0 — 立即实验 | 优先创建 Experiment Object |
| 0.55 – 0.74 | P1 — 排队实验 | 按 Category 配额排队 |
| 0.40 – 0.54 | P2 — 观察 | recommendation 可能为 watch；暂不创建 Experiment |
| < 0.40 | P3 — 拒绝 | 不进入实验；记录 skip 原因 |

### 4.5 与 Opportunity Score 对照示例

| 场景 | opportunity_score | experiment_priority_score | 解释 |
|------|-------------------|---------------------------|------|
| 高需求但高竞争 | 0.72 | 0.48 | 机会好但实验难出差异化 — 先 watch |
| 中需求低成本 | 0.55 | 0.78 | 机会一般但验证成本极低 — Category A 优先 |
| 高利润高难度 | 0.68 | 0.52 | 值得生产但实验反馈周期长 — 排队 Category C |

---

## 5. Category Selection Rules（品类选择规则）

### 5.1 总配额

| Category | 名称 | 数量 | 实验目的 |
|----------|------|------|----------|
| **A** | 低成本快速验证（Low-Cost Rapid Validation） | 10 | 用最低成本验证品类是否有基本市场需求 |
| **B** | 市场需求验证（Market Demand Validation） | 10 | 验证特定关键词 / 用户群是否有真实付费意愿 |
| **C** | 高潜力商业实验（High-Potential Commercial Experiment） | 10 | 验证高客单价、行业深度产品是否可持续盈利 |

### 5.2 Category A 选择规则

| 条件 | 规则 |
|------|------|
| **适用 Opportunity** | difficulty ≤ 0.5；product_type ∈ {ppt, excel, word} |
| **Priority 倾向** | validation_cost_inv 权重生效 — 低成本优先 |
| **定价带** | ¥9.9 – ¥19.9 |
| **recommendation** | produce 或 watch（非 skip） |
| **排除** | profit_score ≥ 0.8 且 difficulty ≥ 0.6 → 应归 Category C |

### 5.3 Category B 选择规则

| 条件 | 规则 |
|------|------|
| **适用 Opportunity** | demand ≥ 0.5；keyword 具有明确用户群 |
| **Priority 倾向** | market_potential 与 feedback_value 双高 |
| **定价带** | ¥19.9 – ¥49.9 |
| **典型 product_type** | pdf, ppt（AI 工具包、提示词库） |
| **排除** | 无明确 target_market 假设 → 不得归入 B |

### 5.4 Category C 选择规则

| 条件 | 规则 |
|------|------|
| **适用 Opportunity** | profit ≥ 0.6；product_idea 含行业垂直特征 |
| **Priority 倾向** | feedback_value × 1.2；可接受较高 difficulty |
| **定价带** | ¥29.9 – ¥99.9 |
| **典型 product_type** | pdf, word（行业资料包） |
| **门禁** | Category C 配额满 10 后 — 即使 Priority 高也须排队或降级 |

### 5.5 Category 分配决策树

```
Opportunity 进入 Selection
        ↓
recommendation = skip? ──Yes──→ 拒绝，不创建 Experiment
        ↓ No
difficulty ≤ 0.5 且 低成本? ──Yes──→ Category A（配额未满）
        ↓ No
profit ≥ 0.6 且 行业垂直? ──Yes──→ Category C（配额未满）
        ↓ No
demand ≥ 0.5 且 用户群明确? ──Yes──→ Category B（配额未满）
        ↓ No
recommendation = watch ──→ P2 观察，不立即创建
        ↓
人工 / 规则 override 或排队
```

---

## 6. Experiment Creation Rules（实验创建规则）

### 6.1 Opportunity → Experiment 转换条件

Opportunity Object **可以**生成 Experiment Object，当且仅当 **全部** 满足：

| # | 条件 | 说明 |
|---|------|------|
| 1 | `recommendation` ≠ `skip` | Cognition 或人工未否决 |
| 2 | `experiment_priority_score` ≥ 0.55 | 达到 P1 及以上 |
| 3 | 目标 Category 配额未满 | A/B/C 对应 < 10 |
| 4 | 同 keyword 无 active 实验 | 避免重复实验 |
| 5 | hypothesis 五问可填写 | 见 Registry §3 |
| 6 | 无 Failure Learning 硬阻断 | 见 §7.3 |

### 6.2 字段映射：Opportunity → Experiment Object

| Experiment Object 字段 | 来源 |
|------------------------|------|
| `experiment_id` | 新生成 `exp_YYYYMMDD_NNN` |
| `version` | `"1.0"` |
| `category` | Selection Layer Category 规则 §5 |
| `hypothesis` | 由 `product_idea` + 五问模板生成 |
| `target_market` | 从 product_idea / 人工补充 |
| `keyword` | Opportunity.keyword |
| `opportunity_source` | `2_COGNITION` 或 `manual` |
| `product_type` | 由 product_idea + Category 推断 |
| `feedback_status` | 初始 `draft` |
| `metrics` | 空结构 — 生产后填充 |

### 6.3 不得创建 Experiment 的情况

| 场景 | 动作 |
|------|------|
| `recommendation` = skip | 拒绝；记录 skip_reason |
| priority < 0.40 | 拒绝 |
| Category 配额已满 | 排队至 archived 释放名额或下一批次 |
| 同 keyword 已有 testing/published 实验 | 拒绝重复；可引用前实验 learning_summary |
| 无 hypothesis | 保持 Opportunity 在 watch 列表 |

### 6.4 创建后流程

```
Experiment Object 创建（feedback_status: draft）
        ↓
人工确认 hypothesis → prepared
        ↓
3_DECISION 产出 production_request
        ↓
（进入 Registry Lifecycle — 见 EXPERIMENT_OBJECT_REGISTRY §2）
```

**说明：** Selection Layer **只负责** Opportunity → Experiment 的创建决策；不触发 Production Request — 该职责属 `3_DECISION`。

---

## 7. Failure Learning Rules（失败学习规则）

### 7.1 失败实验定义

| result | 含义 |
|--------|------|
| `failed` | 假设否定 — 见 Registry §6.3 |
| `promising`（未二次实验） | 软失败 — 调整后可重试 |

### 7.2 对 Cognition（2_COGNITION）的影响

| 失败类型 | Cognition 动作 | 约束 |
|----------|----------------|------|
| keyword 级 failed | 降低该 keyword demand_score 权重参考 | 须 ≥ 3 次同 keyword 失败才调整 |
| Category 级 failed 聚集 | CompetitionAgent 提高该品类 competition 估计 | 批次聚合后调整 |
| promising 反复出现 | InsightAgent 标记「定价 / 包装」主题为高优先级 | 不直接改 opportunity_score |
| success 对照 | 正向校准 — 与 failed 对比提取差异因子 | 见 Registry §7 |

**禁止：** 单次 failed 实验直接 overwrite Opportunity Object。

### 7.3 对 Decision（3_DECISION）的影响

| 失败类型 | Decision 动作 |
|----------|---------------|
| keyword failed | 提高同 keyword Production Request 阈值 |
| Category A 批量 failed | 降低 Category A 自动批准率 |
| promising | 允许「调整重试」Production Request — 新 experiment_id |
| success | 降低阈值；提高 priority |

### 7.4 对 Future Selection（未来选择）的影响

| 规则 | 说明 |
|------|------|
| **Hard Block（硬阻断）** | 同 keyword 有 2+ failed 且 learning_summary 含「无需求」→ priority 上限 0.39 |
| **Soft Penalty（软惩罚）** | 同 Category 连续 3 failed → 该 Category 新实验 priority × 0.85 |
| **Promising 重试** | 允许 1 次同 keyword 新 Experiment — category 不变，hypothesis 须修订 |
| **Success _boost** | 同 keyword 有 success → 类似 keyword priority × 1.10（上限 1.0） |

### 7.5 学习数据流

```
Failed / Promising Experiment（archived）
        ↓
learning_summary + metrics
        ↓
Selection Layer 读取（Future — Registry / DB）
        ↓
调整 experiment_priority_score 权重 / 硬阻断规则
        ↓
2_COGNITION 批次权重校准（独立流程）
        ↓
3_DECISION 阈值更新（独立流程）
```

---

## 8. Future Automation（未来自动化）

### 8.1 目标架构

```
2_COGNITION（Opportunity Discovery — 机会发现）
        +
3_DECISION（Production Approval — 生产批准）
        +
Commercial Experiment System（Experiment Management — 实验管理）
        ↓
Opportunity Discovery（机会发现）
        ↓
Experiment Selection（实验选择 — 本文档）
        ↓
Production（生产 — Content Factory）
        ↓
Feedback → Evaluation → Learning
        ↓
（循环）
```

### 8.2 自动化阶段

| Phase | 名称 | Selection 能力 | 模块 |
|-------|------|----------------|------|
| **Phase 1** | 人工辅助（当前 Blueprint） | 人工 checklist + Priority 公式参考 | 人工 + docs |
| **Phase 2** | 半自动选择 | Priority 自动计算；人工确认 Category | Selection 脚本 + Registry |
| **Phase 3** | Cognition 驱动选择 | Opportunity 自动流入 Selection 队列 | `2_COGNITION` + Selection |
| **Phase 4** | 闭环自动运营 | 自动 Experiment 创建 + Decision 联动 | 全链路 + Human-in-the-loop |

### 8.3 模块协作（Future）

| 模块 | Selection 相关职责 |
|------|-------------------|
| **`2_COGNITION`** | 产出 Opportunity Object；**不**创建 Experiment |
| **Experiment Selection Layer** | 计算 priority；分配 Category；创建 Experiment 决策 |
| **`3_DECISION`** | 消费 Experiment（prepared）；产出 Production Request |
| **Experiment Registry** | 存储 Experiment Object 实例 |
| **`11_CONTENT_FACTORY`** | 执行生产 — Selection 不参与 |

### 8.4 Phase 1 MVP 人工 Checklist

- [ ] Opportunity 字段完整（或人工等效）
- [ ] recommendation ≠ skip
- [ ] 五维 Selection Criteria 人工评估
- [ ] experiment_priority_score 计算或估算
- [ ] Category A/B/C 配额检查
- [ ] Failure Learning 硬阻断检查
- [ ] 创建 Experiment Object（Registry Schema）
- [ ] **不**在本阶段自动生产

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Experiment Object Registry | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md` |
| Commercial Experiment System | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md` |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Cognition Blueprint | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Experiment Selection Framework 设计；Priority 计算代码、自动选择流程、Cognition 联动均 **Pending**。
