# AI_FACTORY_OS Pilot Observation Protocol v1

> Pilot 商业观察协议层 | 最后更新：2026-07-13  
> **状态：Blueprint Completed — Project Intelligence Layer 观察规范，不参与运行计算**

**定位：** Pilot Observation Protocol Layer（Pilot 商业观察协议层）— 为首个 Product Asset Pilot **Excel 考勤记录表**（`8523329941d4`）定义 **Observation Protocol（观察协议）** — 观察什么、如何采集、观察期规则、成功/失败判据、数据治理与 Feedback / Evaluation 映射。**不执行观察、不上架、不修改现有商业资产实例。**

**上级文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md](../contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md) — Feedback Object Schema
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md](../commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md) — Experiment Evaluation Framework
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](../contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md) — Product Asset 生命周期

**Pilot 锚点资产（只读 — 本任务不修改）：**

| 资产 | 值 | 当前状态 |
|------|-----|----------|
| Product Asset | `8523329941d4` — Excel 考勤记录表 | `generation_status: completed`, `validation_status: passed` |
| Production Request | `preq_20260712_005` | approved / 已生产 |
| Experiment | `exp_20260708_005` | validation_goal 已定义 |
| Feedback | `fbk_20260713_001` | **`pending`** — `observation_period: not_started` |
| Evaluation | `eval_20260713_001` | **`pending`** — `hypothesis_result: pending` |

**说明：** **Blueprint ≠ Implementation**。**Observation Protocol Design ≠ Observation Started**。**Protocol Completed ≠ Market Validation**。**Human Assisted ≠ Automation**。本文档只定义观察协议；不开始市场观察、不上架、不修改 Feedback / Evaluation JSON、不生成虚假市场数据。

---

## §1 Observation Layer Position（观察层定位）

### 1.1 在商业学习链中的位置

```
Product Asset Object（completed / passed）
        ↓
Observation Protocol                    ← 本 Protocol 定义（规则层）
        ↓
Feedback Collection（Feedback Object — 事实层）
        ↓
Experiment Evaluation
        ↓
Learning Signal
        ↓
Future Opportunity / Selection
```

### 1.2 Observation Protocol ≠ Feedback Object

| 维度 | Observation Protocol | Feedback Object |
|------|---------------------|-----------------|
| **性质** | 规则 / SOP / 指标目录 | 单条观测事实记录 |
| **内容** | 观察什么、何时采、如何判 | `metric_name` + `metric_value` + 时间戳 |
| **状态** | `observation_status: planned` | `feedback_status: pending` |
| **变更** | 设计文档版本演进 | 观察发生后逐条追加/更新 |
| **伪造** | 协议禁止预测写入 | 实例禁止 null 冒充真实值 |

**规则：** Protocol 定义 **如何观察**；Feedback 保存 **观察到什么**。Evaluation 消费 Feedback 做 **假设裁决** — 三者不可混用。

### 1.3 与现有 Layer 边界

| Layer | 关系 |
|-------|------|
| **Product Asset Validation Gate** | 生产入库验收 — 已完成；**不等于**商业观察 |
| **Observation Protocol** | 上架后观察规则 — **本 Protocol** |
| **Feedback Object** | 观察事实 — Entry 035 已建 pending 占位 |
| **Experiment Evaluation** | 观察期结束后裁决 — Entry 035 pending |

---

## §2 Observation Objective（观察目标）

### 2.1 Pilot 对象

| 项 | 值 |
|----|-----|
| **product_asset_id** | `8523329941d4` |
| **product_name** | Excel 考勤记录表 |
| **source_experiment_id** | `exp_20260708_005` |
| **source_production_request_id** | `preq_20260712_005` |
| **platform_planned** | taobao |
| **expected_price_cny** | ¥12.9 |

### 2.2 validation_goal（来自 Experiment — 只读）

> 验证低竞争细分「小团队考勤 Excel」是否有稳定长尾需求与首单转化；本批次 selection_score 最高（69）优先实验候选。

### 2.3 观察目标（Observation Objectives）

| # | 目标 | 说明 |
|---|------|------|
| 1 | **需求存在性** | 小团队考勤 Excel 细分是否存在真实浏览/兴趣信号 |
| 2 | **首单转化** | 14 天观察期内是否出现 ≥1 笔真实付费订单（对照 Experiment `target_orders: 1`） |
| 3 | **假设验证** | 用户是否愿为「自动统计 + 月度汇总」支付 ¥12.9 量级 |
| 4 | **定性洞察** | 咨询/评论是否反映「省时、公式、小团队适用」假设 |
| 5 | **失败信号识别** | 有曝光无转化、需求不匹配等 — 见 §6 |

**明确：** 观察目标是 **验证假设**，不是 **宣布成功**。Production Completed ≠ Commercial Success。

---

## §3 Observation Metric Schema（观察指标 Schema）

所有指标字段 **必须允许 `null`** — 观察尚未开始时全部为 null；**禁止**用 0 冒充「无数据」与「观测为零」混淆。

### 3.1 Acquisition Metrics（获客 / 曝光）

| metric_key | 类型 | 说明 | 初始值 |
|------------|------|------|--------|
| `exposure` | count \| null | 搜索/推荐曝光次数 | null |
| `views` | count \| null | Listing 浏览量 | null |
| `clicks` | count \| null | 点击进入详情 | null |
| `ctr` | rate \| null | clicks / views | null |

**Experiment 对照目标（只读）：** `target_views: 50`, `target_clicks: 5`, `target_ctr: 0.05`

### 3.2 Engagement Metrics（互动）

| metric_key | 类型 | 说明 | 初始值 |
|------------|------|------|--------|
| `favorites` | count \| null | 收藏数 | null |
| `inquiries` | count \| null | 咨询次数 | null |
| `downloads` | count \| null | 若平台可统计下载/领取 | null |

**Experiment 对照目标：** `target_favorites: 2`

### 3.3 Conversion Metrics（转化）

| metric_key | 类型 | 说明 | 初始值 |
|------------|------|------|--------|
| `orders` | count \| null | 订单数 | null |
| `paid_orders` | count \| null | 已付款订单 | null |
| `revenue_cny` | cny \| null | 实际收入（人民币） | null |
| `conversion_rate` | rate \| null | paid_orders / views（有足够样本时） | null |

**Experiment 对照目标：** `target_orders: 1`, `target_conversion_rate: 0.025`, `expected_price_cny: 12.9`

**禁止：** 在未上架、未观察时填写任何非 null 转化数据。

### 3.4 Product Feedback Metrics（产品反馈）

| metric_key | 类型 | 说明 | 初始值 |
|------------|------|------|--------|
| `customer_questions` | text \| null | 用户咨询摘要（定性） | null |
| `improvement_requests` | text \| null | 改进建议 | null |
| `complaints` | text \| null | 投诉/负面反馈 | null |
| `formula_questions` | count \| null | 公式/功能相关咨询数 | null |

### 3.5 聚合 Schema 示例（Protocol 层 — 非实例）

```json
{
  "observation_metrics": {
    "acquisition": {
      "exposure": null,
      "views": null,
      "clicks": null,
      "ctr": null
    },
    "engagement": {
      "favorites": null,
      "inquiries": null,
      "downloads": null
    },
    "conversion": {
      "orders": null,
      "paid_orders": null,
      "revenue_cny": null,
      "conversion_rate": null
    },
    "product_feedback": {
      "customer_questions": null,
      "improvement_requests": null,
      "complaints": null,
      "formula_questions": null
    }
  }
}
```

---

## §4 Observation Period（观察期）

### 4.1 observation_status 枚举

| 状态 | 含义 | Pilot 当前 |
|------|------|------------|
| `planned` | 协议已定义，尚未上架/未开始计时 | **✅ 当前** |
| `running` | 已上架，观察期进行中 | ⏳ 未开始 |
| `completed` | 观察期结束，可触发 Evaluation | ⏳ 未开始 |

### 4.2 观察期字段

| 字段 | 类型 | 说明 | Pilot 当前 |
|------|------|------|------------|
| `observation_status` | TEXT | planned / running / completed | **`planned`** |
| `start_date` | ISO-8601 \| null | 上架日或观察起始日 | **null** |
| `end_date` | ISO-8601 \| null | start + duration | **null** |
| `duration_days` | INTEGER | 观察窗口长度 | **14**（来自 Experiment `expected_cycle`） |
| `platform` | TEXT | taobao | taobao |

### 4.3 状态流转（Design）

```
planned（当前）
    ↓  人工确认上架 + 填写 start_date
running
    ↓  duration_days 届满或人工提前结束
completed
    ↓  触发 Evaluation 更新（单独任务 — Entry 036-B+）
hypothesis_result 裁决
```

**规则：** `planned → running` 须 **人工确认上架** — 本任务 **不执行** 该转换。

---

## §5 Success Criteria（成功判据）

### 5.1 原则

成功判据描述 **何种信号组合** 支持假设成立 — **不预设具体数字达成**。实际对照 Experiment `success_metrics` 在 Evaluation 阶段填写 `actual` / `met`。

### 5.2 成功信号（须真实 Feedback 支撑）

| # | 判据 | 所需 Feedback 类型 |
|---|------|-------------------|
| 1 | **有真实用户兴趣信号** | Acquisition：`views`/`clicks` > 0；或 Engagement：`favorites`/`inquiries` > 0 |
| 2 | **有咨询或购买行为** | Engagement：`inquiries` ≥ 1；和/或 Conversion：`paid_orders` ≥ 1 |
| 3 | **用户反馈支持需求存在** | Product Feedback：咨询内容与小团队考勤/公式/省时假设一致 |
| 4 | **达到 Experiment 最低目标（对照）** | `views` ≥ 50 或 `paid_orders` ≥ 1（以 Experiment 定义为准） |

### 5.3 hypothesis_result 映射（Evaluation 阶段）

| 条件 | 建议 hypothesis_result |
|------|------------------------|
| 核心 commercial + market 指标 met | `success` |
| 有兴趣信号但未达订单目标 | `promising` |
| 数据不足 | `inconclusive` |

**禁止：** 在 Observation 未 running 时将 Evaluation 改为 `success`。

---

## §6 Failure Criteria（失败判据）

### 6.1 失败也是资产

失败信号须完整记录于 Feedback + Evaluation `failure_metrics` — 供 Selection 学习。**Failure 不可隐藏。**

### 6.2 失败信号定义

| # | 失败模式 | 信号描述 | failure_metric_key（建议） |
|---|----------|----------|---------------------------|
| 1 | **有曝光无点击** | exposure/views > 0 且 clicks = 0 或 ctr 极低 | `exposure_no_click` |
| 2 | **有点击无咨询** | clicks > 0 且 inquiries = 0 且 paid_orders = 0 | `click_no_inquiry` |
| 3 | **有咨询无购买** | inquiries > 0 且 paid_orders = 0（观察期结束） | `inquiry_no_purchase` |
| 4 | **需求与假设不匹配** | 咨询/反馈指向非考勤场景或拒绝付费 | `hypothesis_mismatch` |
| 5 | **零曝光** | 观察期结束 views = 0 或 null（上架异常） | `zero_exposure` |

### 6.3 hypothesis_result 映射

| 条件 | 建议 hypothesis_result |
|------|------------------------|
| 明确失败信号触发且无转化 | `failed` |
| 部分负面 + 少量正面 | `promising` 或 `failed`（人工裁量） |

---

## §7 Data Governance（数据治理）

### 7.1 禁止

| 禁止项 | 原因 |
|--------|------|
| **预测数据写入 Feedback** | 预测 ≠ 观测 |
| **AI 生成市场结果** | Human Assisted 阶段须真实来源 |
| **用 Quality Score 替代商业验证** | `quality_score: 0.89` 是生产质量，不是市场成功 |
| **用 0 代替 null** | 0 表示「观测为零」；未开始须 null |
| **伪造订单/收入/转化率** | 违反 Work Principles |
| **Observation 未 running 时更新 Evaluation 为 success** | 时序违规 |

### 7.2 允许

| 允许项 | 说明 |
|--------|------|
| **人工录入真实观察结果** | 平台后台截图/导出为据 |
| **逐日/逐周追加 Feedback 条** | 每条 metric 独立 Object |
| **observation_status 人工推进** | planned → running → completed |
| **Evaluation 在观察 completed 后更新** | 单独授权任务 |

### 7.3 数据来源优先级

1. 平台官方后台（taobao 卖家中心）
2. 人工记录咨询截图/文本
3. 第三方工具（须注明 source，未来扩展）

**禁止：** 无来源的「估计值」。

---

## §8 Experiment Evaluation Mapping（观察 → Feedback → Evaluation 映射）

### 8.1 映射总览

```
Observation Metric（Protocol §3）
        ↓  人工录入
Feedback Object（metric_name + metric_value）
        ↓  观察期 completed 后聚合
Experiment Evaluation（success_metrics.actual / failure_metrics）
        ↓
hypothesis_result + learning_summary
```

### 8.2 字段映射表

| Observation Metric | Feedback feedback_type | Feedback metric_name | Evaluation 字段 |
|-------------------|---------------------|-------------------|-----------------|
| `views` | market_feedback | `listing_views_7d` | success_metrics.market_metric.actual_views |
| `clicks` | market_feedback | `listing_clicks_7d` | actual_clicks |
| `ctr` | market_feedback | `ctr_7d` | actual_ctr |
| `favorites` | market_feedback | `favorites_7d` | actual_favorites |
| `inquiries` | customer_feedback | `inquiry_count_7d` | （Engagement 扩展） |
| `orders` | sales_feedback | `orders_7d` | actual_orders |
| `paid_orders` | sales_feedback | `orders_7d` | actual_orders |
| `revenue_cny` | sales_feedback | `revenue_7d_cny` | actual_revenue_cny |
| `conversion_rate` | sales_feedback | `conversion_rate_7d` | actual_conversion_rate |
| `customer_questions` | customer_feedback | `qualitative_summary` | feedback_summary |
| `complaints` | customer_feedback | `complaint_count_7d` | failure_metrics |
| `formula_questions` | quality_feedback | 自定义 | quality 扩展 |

### 8.3 Pilot 实例锚点（只读 — 不修改）

| 对象 | ID | 当前 |
|------|-----|------|
| Feedback | `fbk_20260713_001` | pending — 待 running 后追加 metric 条 |
| Evaluation | `eval_20260713_001` | pending — 待 completed 后更新 actual |

---

## §9 Human Assisted Operation SOP（人工辅助操作 SOP）

### 9.1 当前阶段：human_assisted

| 步骤 | 操作 | 负责 | 产出 |
|------|------|------|------|
| 0 | 确认 Observation Protocol（本文档） | 人工 | Protocol v1 ✅ |
| 1 | Product Asset 上架 taobao | 人工 | listing URL（不写入本任务） |
| 2 | 更新 observation：`planned → running`，填 `start_date` | 人工 | Entry 036-B+ |
| 3 | 按 §3 指标定期录入 Feedback Object | 人工 | 追加 feedback 条或更新 metric_value |
| 4 | 观察期第 14 天：标记 `observation_status: completed` | 人工 | 填 `end_date` |
| 5 | 聚合 Feedback → 更新 Evaluation | 人工 | hypothesis_result 裁决 |
| 6 | 撰写 learning_summary | 人工 | Selection 输入 |

### 9.2 录入频率建议

| 频率 | 指标 |
|------|------|
| 每日 | views, clicks, inquiries（若 running） |
| 每周 | favorites, orders, revenue 汇总 |
| 事件驱动 | customer_questions, complaints |

### 9.3 未来自动化（Design Only — 禁止提前实施）

| 未来 Agent | 角色 | 当前 |
|------------|------|------|
| **Observation Agent** | 调度观察期、提醒录入 | ❌ 未实现 |
| **Market Agent（Intelligence）** | 合规渠道曝光数据 | ❌ 与 CF Legacy MarketAgent 隔离 |
| **CustomerAgent / SalesAgent** | 咨询/订单导入 | ❌ Phase 2+ |
| **2_COGNITION** | 读取 Evaluation 学习 | ❌ 不替代人工录入 |

**规则：** MVP Phase 1 **禁止** 自动化替代人工观察录入。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Feedback Object Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_FEEDBACK_OBJECT_CONTRACT.md` |
| Experiment Evaluation Framework | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md` |
| Product Asset 实例 | `commercial_assets/product_assets/product_assets_v1.json` |
| Feedback 实例 | `commercial_assets/feedback/feedback_v1.json` |
| Evaluation 实例 | `commercial_assets/experiment_evaluations/experiment_evaluations_v1.json` |

---

**Blueprint ≠ Implementation。** **Observation Protocol Design ≠ Observation Started。** **Protocol Completed ≠ Market Validation。** 本文档完成 Pilot Observation Protocol v1；观察执行、上架、Feedback/Evaluation 实例更新均 **Pending**，须 Entry 036-B+ 单独授权。
