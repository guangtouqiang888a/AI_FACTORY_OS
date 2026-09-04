# AI_FACTORY_OS Feedback Object Contract v1

> 反馈对象契约层 | 最后更新：2026-07-13  
> **状态：Blueprint Completed — Project Intelligence Layer 契约规范，不参与运行计算**

**定位：** Feedback Object Contract Layer（反馈对象契约层）— 定义 **Product Asset（产品资产）** 进入市场观察期后 **Feedback Object（反馈对象）** 的标准 Schema、五类反馈分类、生命周期、模块边界与未来数据库映射。

**上级文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md) — Product Asset 与 Feedback 连接 §8
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — 五类商业 Object 总契约 §7
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md](../commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md) — 实验评估框架
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md](../commercial/AI_FACTORY_OS_EXPERIMENT_OBJECT_REGISTRY.md) — Experiment success_metrics

**当前资产状态（只读审计）：**

| 资产 | 状态 |
|------|------|
| `product_assets_v1.json` | ✅ 1 条 — `8523329941d4`（preq_005 Pilot） |
| `commercial_assets/feedback/` | ❌ **未创建** |
| Feedback JSON 实例 | ❌ **未创建** |
| Feedback Runtime | ❌ **未实现** |

**说明：** **Blueprint ≠ Implementation**。**Feedback Design ≠ Market Validation**。**Human Assisted ≠ Automation**。**Production Completed ≠ Commercial Success**。本文档只定义 Feedback 契约；不创建 JSON 实例、不修改 Runtime、不伪造市场数据。

---

## §1 Feedback Layer Position（反馈层定位）

### 1.1 在商业生产链中的位置

```
Product Asset Object（completed / published / testing）
        ↓
Feedback Object                           ← 本 Contract 定义
        ↓
Experiment Evaluation
        ↓
Learning Signal
        ↓
Future Opportunity / Selection
```

### 1.2 Feedback 不是什么

| Feedback **是** | Feedback **不是** |
|-----------------|-------------------|
| 对市场/用户/销售/质量/运营的**观测记录** | **Market Success（市场成功）** 的裁决 |
| 实验假设验证的**输入信号** | **Revenue（收入）** 的权威账本 |
| 可审计、可回溯的单条指标或事件 | **Experiment Score（实验评分）** — 那是 Evaluation 层产出 |
| Human Assisted 阶段的真实录入载体 | Cognition 自动生成的 Opportunity Score |

**核心隔离：**

| 概念 | 说明 |
|------|------|
| **Feedback ≠ Market Success** | 一条 positive feedback 不等于实验成功 |
| **Feedback ≠ Revenue** | feedback 记录观测值，不替代财务系统 |
| **Feedback ≠ Experiment Score** | 评分由 Experiment Evaluation 层独立计算 |

### 1.3 与 Pilot Product Asset 的关系（preq_005 — 只读上下文）

| 项 | 值 |
|----|-----|
| `product_asset_id` | `8523329941d4` |
| `source_experiment_id` | `exp_20260708_005` |
| `generation_status` | completed |
| `validation_status` | passed |
| **Feedback 状态** | ⏳ **未录入** — 须 published/testing + 观察期后人工录入 |

**规则：** Product Asset 生产完成 **不等于** 可立即伪造 Feedback。须实际上架或进入 testing 观察期后，按 Human Assisted SOP 录入真实观测。

### 1.4 进入 Feedback 的门禁

| # | 条件 |
|---|------|
| 1 | Product Asset `generation_status` ≥ `completed` |
| 2 | Product Asset `validation_status` = `passed` |
| 3 | `source_experiment_id` 非空 |
| 4 | 人工确认进入 `published` 或 `testing` 观察期 |
| 5 | `feedback_method` = `human_assisted`（MVP Phase 1） |

**禁止：** Feedback 直接修改 Product Asset `quality_score`、Opportunity Score 或 Experiment Priority Score。

---

## §2 Feedback Object Schema v1

### 2.1 标准 Object

```json
{
  "feedback_id": "fbk_20260713_001",
  "object_type": "feedback",
  "contract_version": "1.0",
  "source_product_asset_id": "8523329941d4",
  "source_experiment_id": "exp_20260708_005",
  "source_production_request_id": "preq_20260712_005",
  "source_opportunity_id": "opp_20260708_005",
  "feedback_type": "market_feedback",
  "feedback_source": "human_assisted",
  "feedback_method": "human_assisted",
  "metric_name": "listing_views_7d",
  "metric_value": 0,
  "metric_unit": "count",
  "observation_period": {
    "start": "ISO-8601",
    "end": "ISO-8601"
  },
  "platform": "taobao",
  "feedback_status": "recorded",
  "notes": "",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 用途 |
|------|------|------|------|
| `feedback_id` | TEXT | ✅ | 唯一 ID；格式建议 `fbk_YYYYMMDD_NNN` |
| `object_type` | TEXT | ✅ | 固定 `"feedback"` |
| `contract_version` | TEXT | ✅ | 当前 `"1.0"` |
| `source_product_asset_id` | TEXT | ✅ | FK → Product Asset |
| `source_experiment_id` | TEXT | ✅ | FK → Experiment — 评估追溯 |
| `source_production_request_id` | TEXT | | 冗余 — PR 追溯 |
| `source_opportunity_id` | TEXT | | 冗余 — Opportunity 追溯 |
| `feedback_type` | TEXT | ✅ | 五类之一 — 见 §3 |
| `feedback_source` | TEXT | ✅ | 数据来源：`human_assisted` / `platform_import` / `agent_generated`（未来） |
| `feedback_method` | TEXT | ✅ | MVP Phase 1 固定 `human_assisted` |
| `metric_name` | TEXT | ✅ | 指标名 — 见 §3 各类型 metric 目录 |
| `metric_value` | NUMBER / TEXT / OBJECT | ✅ | 指标值 — 类型随 metric_name |
| `metric_unit` | TEXT | | count / rate / cny / text / boolean |
| `observation_period` | OBJECT | | 观察窗口 |
| `platform` | TEXT | | 渠道：taobao / xianyu / other |
| `feedback_status` | TEXT | ✅ | `draft` / `recorded` / `verified` / `archived` |
| `notes` | TEXT | | 人工备注 — 定性上下文 |
| `created_at` | TEXT | ✅ | ISO-8601 |
| `updated_at` | TEXT | | ISO-8601 |

### 2.3 与 Intelligence Contract §7 字段对齐

| Intelligence Contract v1 | 本 Contract v1 | 说明 |
|--------------------------|----------------|------|
| `product_id` | `source_product_asset_id` | 统一命名 |
| `views`, `clicks`, `sales`… | `metric_name` + `metric_value` | 本 Contract 更细粒度、可扩展 |
| `customer_feedback` | `feedback_type=customer_feedback` | 独立类型 |
| `recorded_at` | `created_at` | 一致 |

**规则：** Implementation 时 Intelligence Contract 扁平字段 **映射为** 多条 Feedback Object（按 metric 拆分）或聚合视图。

---

## §3 Feedback Type Classification（五类反馈）

### 3.1 类型总览

| feedback_type | 中文 | 核心问题 | 典型消费者 |
|---------------|------|----------|------------|
| `market_feedback` | 市场反馈 | 有没有曝光与兴趣？ | Experiment Evaluation |
| `customer_feedback` | 用户反馈 | 用户怎么说？ | Experiment Evaluation、生产改进 |
| `sales_feedback` | 销售反馈 | 有没有转化与收入？ | Experiment Evaluation |
| `quality_feedback` | 产品质量反馈 | 交付物质量够吗？ | Content Factory 改进 |
| `operational_feedback` | 生产运营反馈 | 生产成本/时效如何？ | Selection、Production Request |

### 3.2 market_feedback — 市场反馈

| metric_name | metric_unit | 说明 |
|-------------|-------------|------|
| `listing_views_7d` | count | 7 日 listing 浏览量 |
| `listing_clicks_7d` | count | 7 日点击 |
| `favorites_7d` | count | 收藏数 |
| `ctr_7d` | rate | 点击率 |
| `search_impressions_7d` | count | 搜索曝光 |

**禁止：** 无实际上架记录时录入非零 views/clicks。

### 3.3 customer_feedback — 用户反馈

| metric_name | metric_unit | 说明 |
|-------------|-------------|------|
| `inquiry_count_7d` | count | 咨询次数 |
| `review_count_7d` | count | 评论数 |
| `satisfaction_score` | rate | 满意度 0–1 |
| `qualitative_summary` | text | 定性摘要 |
| `complaint_count_7d` | count | 投诉数 |

### 3.4 sales_feedback — 销售反馈

| metric_name | metric_unit | 说明 |
|-------------|-------------|------|
| `orders_7d` | count | 7 日订单数 |
| `revenue_7d_cny` | cny | 7 日收入（人民币） |
| `conversion_rate_7d` | rate | 转化率 |
| `refund_count_7d` | count | 退款数 |
| `avg_order_value_cny` | cny | 客单价 |

**禁止：** 伪造 sales/revenue 以满足 success_metrics。

### 3.5 quality_feedback — 产品质量反馈

| metric_name | metric_unit | 说明 |
|-------------|-------------|------|
| `post_publish_quality_score` | rate | 上架后质量复评 0–1 |
| `formula_error_reported` | boolean | 是否报告公式错误 |
| `structure_issue_reported` | boolean | 结构/章节缺失报告 |
| `rework_required` | boolean | 是否需返工 |

**与 Product Asset quality_score 关系：** 可对比但不覆盖 CF 产出时的 `quality_score`。

### 3.6 operational_feedback — 生产运营反馈

| metric_name | metric_unit | 说明 |
|-------------|-------------|------|
| `production_time_minutes` | count | 实际生产耗时 |
| `production_cost_cny` | cny | 实际生产成本 |
| `first_pass_success` | boolean | 是否一次通过 Validation Gate |
| `pipeline_failure_step` | text | 若失败，失败步骤 |

**Pilot preq_005 参考：** production_time_minutes、production_cost_cny 可在 Pilot 后人工登记 operational_feedback。

---

## §4 Feedback Lifecycle（生命周期）

| 状态 | 含义 |
|------|------|
| `draft` | 草稿 — 未确认 |
| `recorded` | 已录入 — Human Assisted 确认 |
| `verified` | 已核实 — 二次核对（可选） |
| `archived` | 已归档 — 评估完成后只读 |

**流转：** draft → recorded →（verified）→ archived

---

## §5 Module Responsibility（模块职责）

| 模块 | Feedback 相关职责 | 禁止 |
|------|-------------------|------|
| **人工 / SOP** | MVP Phase 1 录入 Feedback JSON | 伪造数据 |
| **11_CONTENT_FACTORY** | 未来 FeedbackAgent 产出 quality/operational | 写入 Opportunity Score |
| **2_COGNITION** | **未来** 读取 Feedback 学习模式 | MVP Phase 1 自动裁决 |
| **3_DECISION** | **未来** 读取 Feedback 调整阈值 | 文件验收、Experiment Evaluation |
| **7_MEMORY** | **未来** 保存 Learning Signal 摘要 | 替代 Feedback JSON 权威源 |
| **Experiment Evaluation** | 消费 Feedback 计算 hypothesis_result | 产生 Feedback |

---

## §6 Human Assisted Phase（人工辅助阶段）

### 6.1 feedback_method: human_assisted

| 允许 | 禁止 |
|------|------|
| 人工录入真实平台截图/后台数据 | 伪造销售数据 |
| 观察期结束后批量录入 | 伪造用户反馈 |
| metric_value = 0 表示「无数据」 | 伪造市场结果以通过 Evaluation |
| notes 字段记录数据来源 | 自动生成「假阳性」Feedback |

### 6.2 Pilot 观察 SOP（设计 — 未执行）

1. Product Asset `8523329941d4` 上架 taobao（人工）
2. 设定观察期（如 7 / 14 天 — 来自 Experiment validation_period）
3. 按 metric 目录逐条录入 Feedback Object
4. 观察期结束 → 触发 Experiment Evaluation（单独任务）

---

## §7 Future Automation（未来自动化）

### 7.1 Agent 产出映射（Design Only）

| Agent | feedback_type | 说明 |
|-------|---------------|------|
| **MarketAgent（CF Legacy）** | 不直接写 Feedback | Legacy 选品 — 与 Experiment Feedback 隔离 |
| **CustomerAgent（未来）** | `customer_feedback` | 咨询/评论聚合 |
| **SalesAgent（未来）** | `sales_feedback` | 订单/收入导入 |
| **Market Intelligence Agent（未来）** | `market_feedback` | 曝光/点击（合规渠道） |
| **QualityAgent / FeedbackAgent（CF）** | `quality_feedback` | 返工/复评 |

### 7.2 2_COGNITION 消费路径（Future）

```
Feedback Objects（多条）
        ↓
2_COGNITION 聚合 / 模式提取
        ↓
Learning Signal（摘要 — 非 Feedback 替代）
        ↓
Future Opportunity Candidate 特征（不反向写 Feedback）
```

**规则：** Cognition **读取** Feedback，**不伪造** Feedback。

---

## §8 Database Mapping（数据库映射 — Blueprint Only）

### 8.1 表：`feedback`（预留 — 禁止 CREATE TABLE）

| 列 | 类型 | 映射字段 |
|----|------|----------|
| `id` | INTEGER PK | 内部 ID |
| `feedback_id` | TEXT UNIQUE | `feedback_id` |
| `product_asset_id` | TEXT | `source_product_asset_id` |
| `experiment_id` | TEXT | `source_experiment_id` |
| `production_request_id` | TEXT | `source_production_request_id` |
| `feedback_type` | TEXT | `feedback_type` |
| `feedback_source` | TEXT | `feedback_source` |
| `metric_name` | TEXT | `metric_name` |
| `metric_value_json` | TEXT / JSON | `metric_value` 序列化 |
| `metric_unit` | TEXT | `metric_unit` |
| `platform` | TEXT | `platform` |
| `feedback_status` | TEXT | `feedback_status` |
| `observation_start` | TEXT | `observation_period.start` |
| `observation_end` | TEXT | `observation_period.end` |
| `notes` | TEXT | `notes` |
| `created_at` | TEXT | `created_at` |
| `updated_at` | TEXT | `updated_at` |

**索引（设计）：** `(product_asset_id)`, `(experiment_id)`, `(feedback_type)`, `(metric_name)`

### 8.2 commercial_assets 扩展（Future）

```
commercial_assets/
├── product_assets/              ← 已有
└── feedback/                    ← 【未来】
    └── feedback_v1.json
```

**本任务：** ❌ 不创建 `commercial_assets/feedback/`

---

## §9 Version Strategy（版本策略）

| 版本体系 | 当前 | 独立原因 |
|----------|------|----------|
| **Feedback Object Contract** | 1.0 | 商业资产语义 |
| **Product Asset Contract** | 1.0 | 上游产物 |
| **Experiment Evaluation Framework** | 1.0 | 下游评估 |
| **Database Schema** | Pending | Implementation 层 |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Product Asset Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md` |
| Experiment Evaluation Framework | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_EXPERIMENT_EVALUATION_FRAMEWORK.md` |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Product Asset 实例 | `commercial_assets/product_assets/product_assets_v1.json` |

---

**Blueprint ≠ Implementation。** **Feedback Design ≠ Market Validation。** 本文档完成 Feedback Object Contract v1；Feedback JSON 实例、Runtime、DB 表均 **Pending**。
