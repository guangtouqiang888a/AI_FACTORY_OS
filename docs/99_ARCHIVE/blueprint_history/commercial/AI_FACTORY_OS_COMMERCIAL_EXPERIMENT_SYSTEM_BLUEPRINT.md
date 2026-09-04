# AI_FACTORY_OS Commercial Experiment System Blueprint v1

> 商业实验管理体系设计蓝图 | 最后更新：2026-07-07  
> **状态：Blueprint Completed — Project Intelligence Layer 文档，不参与运行计算**

**定位：** Commercial Experiment Layer（商业实验层）— 管理 30 产品商业验证实验的**设计、记录、评估与数据沉淀**，为 Database Extension（数据库扩展）、Product Feedback Loop（产品反馈闭环）、2_COGNITION Market Intelligence（市场智能）提供数据结构基础。

**上级 Blueprint：** [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md](AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md) — 定义 MVP 目标与商业闭环；本文档定义**实验管理体系**。

**相关文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — Object 契约 v1
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md) — 目标表结构
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](../database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md) — Database Contract（数据库契约）

**说明：** **Blueprint ≠ Implementation（蓝图不等于实施）**。本文档完成设计；文档完成 ≠ 功能完成。代码、数据库、运行逻辑变更须单独审批。

---

## 1. Commercial Experiment System Definition（商业实验系统定义）

### 1.1 系统定位

Commercial Experiment System（商业实验系统）**不是** Content Factory（内容工厂）生产系统。

| 对比 | Content Factory | Commercial Experiment System |
|------|-----------------|------------------------------|
| **核心问题** | 如何生产数字资产？ | 数字资产是否有商业价值？ |
| **输出** | Product Asset（产品资产） | Experiment Result（实验结果）+ Feedback Data（反馈数据） |
| **运行层** | `11_CONTENT_FACTORY` 代码 | docs 认知层 + 未来 DB 台账 |
| **成功标准** | quality_score ≥ 阈值 | Success / Promising / Failed 评估 |

### 1.2 系统职责

Commercial Experiment System（商业实验系统）负责：

| 职责 | 说明 |
|------|------|
| **设计实验（Experiment Design）** | 定义假设、品类、目标用户、预期价值 |
| **记录实验（Experiment Recording）** | 追踪生命周期状态与指标 |
| **评估结果（Result Evaluation）** | Success / Promising / Failed 判定 |
| **沉淀商业数据（Data Accumulation）** | 为 DB 与 Cognition 提供结构化样本 |

### 1.3 阶段升级目标

```
当前：生产数字资产（Production）
        ↓
目标：验证数字资产商业价值（Validation）
        ↓
未来：Feedback-Driven Intelligence（反馈驱动智能）
```

AI Factory OS 通过本系统，从 **「能够生产」** 升级为 **「能够验证并优化商业方向」**。

### 1.4 与 Project Intelligence Layer 的关系

本系统属于 **Project Intelligence Layer（项目智能层）** — 物理位于 `docs/`，不参与 ExecutionRuntime（执行运行时）调度，不写入 `7_MEMORY` pattern。

---

## 2. Experiment Lifecycle（实验生命周期）

### 2.1 状态流转图

```
Draft（草案）
        ↓
Prepared（准备完成）
        ↓
Production（生产中）
        ↓
Published（已发布）
        ↓
Testing（测试阶段）
        ↓
Validated（验证成功）  ──→  Archived（归档）
        ↓
   [Promising / Failed 分支同样 → Archived]
```

### 2.2 各状态定义与转换条件

| 状态 | 英文 | 含义 | 进入条件 | 退出条件 |
|------|------|------|----------|----------|
| **Draft（草案）** | draft | 实验构思阶段 | 创建 Experiment Object | hypothesis 五问填完 + category 指定 → Prepared |
| **Prepared（准备完成）** | prepared | 可进入生产 | hypothesis 完整；expected_value / production_cost 已估算 | Production Request 下发 → Production |
| **Production（生产中）** | production | Content Factory 正在生产 | `11_CONTENT_FACTORY` 接收 Production Request | Product Asset released → Published |
| **Published（已发布）** | published | 已人工确认上架 | publish_date 记录；platform 指定 | 观察期开始（≥ 7 天）→ Testing |
| **Testing（测试阶段）** | testing | 收集市场与销售数据 | 产品已上架 | 指标录入完整 + Evaluation 完成 → Validated 或直 Archive |
| **Validated（验证成功）** | validated | 实验假设得到验证 | Evaluation = Success 或 Promising（经复核） | 复盘完成 → Archived |
| **Archived（归档）** | archived | 实验关闭，数据保留 | 任何终态评估完成 | 不可回退（新实验用新 experiment_id） |

### 2.3 异常与回退规则

| 场景 | 处理 |
|------|------|
| Production 失败（quality 未过） | 保持 `production`，修正后重试；不进入 Published |
| Published 后零曝光 | Testing 期满 → Evaluation = Failed → Archived |
| 数据缺失 | 不可进入 Validated；保持 Testing 直至补录或标记 incomplete |
| 实验中途取消 | status → archived；`final_result` = cancelled |

### 2.4 与 generated_products.status 映射（未来）

| Experiment Status | generated_products.status（Blueprint） |
|-------------------|----------------------------------------|
| production | draft |
| published / testing / validated | released |
| archived | archived |

---

## 3. Experiment Object Definition（实验对象定义）

### 3.1 Experiment Object（实验对象）Schema v1

Experiment Object（实验对象）是商业实验系统的**核心数据结构**，未来映射 Database Extension 中的实验台账表（Blueprint 建议表名：`commercial_experiments` — **当前未创建**）。

```json
{
  "contract_version": "1.0",
  "object_type": "experiment",
  "experiment_id": "exp_20260707_001",
  "product_id": "",
  "category": "A | B | C",
  "hypothesis": {
    "target_customer": "",
    "problem_solved": "",
    "purchase_reason": "",
    "expected_price": 0.0,
    "competition_summary": ""
  },
  "production_cost": 0.0,
  "expected_value": 0.0,
  "status": "draft",
  "created_time": "ISO-8601",
  "updated_time": "ISO-8601",
  "opportunity_id": null,
  "production_request_id": null,
  "evaluation": null
}
```

### 3.2 字段说明

| 字段 | 类型 | 说明 | 未来 DB 映射 |
|------|------|------|--------------|
| `experiment_id` | TEXT | 实验唯一 ID | `commercial_experiments.id` 或 business key |
| `product_id` | TEXT | 关联 Product Asset | FK → `generated_products` 业务 ID |
| `category` | TEXT | A / B / C 实验分类 | `category` |
| `hypothesis` | OBJECT | 实验假设五问（见 §5） | JSON 列或关联表 |
| `production_cost` | REAL | 预估 / 实际生产成本 | `production_cost` |
| `expected_value` | REAL | 预期收入或商业价值 | `expected_value` |
| `status` | TEXT | 生命周期状态（§2） | `status` |
| `created_time` | TIMESTAMP | 创建时间 | `created_at` |
| `updated_time` | TIMESTAMP | 最后更新时间 | `updated_at` |
| `opportunity_id` | INTEGER | 关联 Opportunity（未来） | FK → `opportunity_scores.id` |
| `production_request_id` | TEXT | 关联 Production Request | 运行时 audit |
| `evaluation` | OBJECT | 评估结果（§8） | JSON 或关联 evaluation 表 |

### 3.3 与 Commercial Intelligence Contract 的关系

| Contract Object | Experiment Object 关系 |
|-----------------|------------------------|
| Opportunity Object | 实验设计输入 — `opportunity_id` 关联 |
| Production Request Object | Prepared → Production 触发 |
| Product Asset Object | Production 产出 — `product_id` 回填 |
| Feedback Object | Testing 阶段录入 — 见 §7 |

**说明：** Experiment Object 是 **Commercial Validation Layer（商业验证层）** 特有对象，扩展 Contract v1，不替代现有五类 Object。

---

## 4. Product Experiment Categories（产品实验分类）

### 4.1 30 产品实验总览

| 分类 | 英文代号 | 数量 | 策略定位 |
|------|----------|------|----------|
| **Category A** | low_cost_rapid | **10** | 低成本快速验证（Low-Cost Rapid Validation） |
| **Category B** | ai_enhanced | **10** | AI 增强型产品（AI-Enhanced Product） |
| **Category C** | industry_vertical | **10** | 行业垂直产品（Industry Vertical Product） |

**与 Commercial MVP Blueprint 品类对照：**

| MVP 品类 | 实验分类映射 |
|----------|--------------|
| 办公类（Office） | 主要 → Category A |
| AI 工具类（AI Tools） | 主要 → Category B |
| 行业类（Industry） | 主要 → Category C |

### 4.2 Category A — 低成本快速验证（10 个）

| 项 | 内容 |
|----|------|
| **实验目的** | 用最低生产成本验证「是否有基本市场需求」 |
| **典型产品** | 单页 PPT 模板、简单 Excel 表格、Word 简历模板 |
| **定价带** | ¥9.9 – ¥19.9 |
| **生产策略** | 最短 pipeline；最少 LLM 调用 |
| **成功信号** | views ≥ 50 或 clicks ≥ 5 |
| **失败信号** | 14 天内 views < 20 且 clicks = 0 |

### 4.3 Category B — AI 增强型产品（10 个）

| 项 | 内容 |
|----|------|
| **实验目的** | 验证「AI 差异化内容」是否带来更高转化或溢价 |
| **典型产品** | AI 提示词库、AI 工作流包、智能办公工具包 |
| **定价带** | ¥19.9 – ¥49.9 |
| **生产策略** | 完整 Creator + Quality 链；强调 AI 价值主张 |
| **成功信号** | conversion_rate 高于 Category A 均值 |
| **失败信号** | 溢价无转化 — AI 差异化未感知 |

### 4.4 Category C — 行业垂直产品（10 个）

| 项 | 内容 |
|----|------|
| **实验目的** | 验证「行业深度」是否带来更高客单价与复购 |
| **典型产品** | 电商运营资料包、创业工具包、自媒体 SOP 包 |
| **定价带** | ¥29.9 – ¥99.9 |
| **生产策略** | 多 artifact 组合；行业关键词精准定位 |
| **成功信号** | profit > 0 且 customer_feedback 正向 |
| **失败信号** | 高生产成本 + 零订单 |

---

## 5. Experiment Hypothesis System（实验假设系统）

### 5.1 五问框架（每个产品必须定义）

| # | 问题 | 字段 | 示例 |
|---|------|------|------|
| 1 | **用户是谁？** | `target_customer` | 中小企业主、自媒体新手 |
| 2 | **解决什么问题？** | `problem_solved` | 缺少专业 PPT 模板，制作耗时 |
| 3 | **为什么用户购买？** | `purchase_reason` | 比自己做便宜，比请人做快 |
| 4 | **预计价格？** | `expected_price` | ¥19.9 |
| 5 | **竞争情况？** | `competition_summary` | 闲鱼同类 50+，均价 ¥15，差异化在 AI 定制 |

### 5.2 Hypothesis → Test → Result 循环

```
Hypothesis（假设）
    │  Experiment Object 创建（Draft → Prepared）
    ↓
Test（测试）
    │  Production → Published → Testing
    │  采集 Production / Market / Commercial / System Metrics
    ↓
Result（结果）
    │  Evaluation Model（§8）→ Success / Promising / Failed
    ↓
Learning（学习）
    │  Feedback Object → Database → Cognition
    ↓
（下一轮 Hypothesis 优化）
```

### 5.3 假设质量门禁

| 条件 | 规则 |
|------|------|
| Draft → Prepared | 五问全部非空 |
| Prepared → Production | `expected_value` > `production_cost`（预期盈利） |
| 无假设的生产 | **禁止** — 视为非实验产品，不纳入 30 批次统计 |

---

## 6. Experiment Metrics System（实验指标体系）

### 6.1 四类指标总览

| 类别 | 英文 | 采集阶段 | 主要用途 |
|------|------|----------|----------|
| **生产指标** | Production Metrics | Production | 成本控制、效率优化 |
| **市场指标** | Market Metrics | Testing | 需求验证、包装优化 |
| **商业指标** | Commercial Metrics | Testing | 盈利验证、选品决策 |
| **系统指标** | System Metrics | Production + Testing | 自动化演进评估 |

---

### 6.2 Production Metrics（生产指标）

| 指标 | 字段建议 | 说明 | 采集来源 |
|------|----------|------|----------|
| 生产时间 | `production_time_minutes` | Request → Asset 耗时 | Content Factory 日志 |
| AI 调用成本 | `ai_cost` | LLM token / 调用费用估算 | llm_adapter 统计 |
| 人工成本 | `human_cost` | 人工复核、发布确认耗时折算 | 实验台账 |
| 总生产成本 | `production_cost` | ai_cost + human_cost + 分摊 | Experiment Object |
| 一次通过率 | `first_pass_rate` | 无需返工占比 | QualityAgent |

---

### 6.3 Market Metrics（市场指标）

| 指标 | 字段建议 | 说明 | 采集来源 |
|------|----------|------|----------|
| 曝光 | `views` | 展示次数 | 平台后台 |
| 访问 | `visits` | 详情页访问（可与 views 合并或拆分） | 平台后台 |
| 点击 | `clicks` | 点击进入详情 | 平台后台 |
| 收藏 | `favorites` | 收藏 / 想要 | 平台后台 |
| 点击率 | `ctr` | clicks / views | 计算 |

---

### 6.4 Commercial Metrics（商业指标）

| 指标 | 字段建议 | 说明 | 采集来源 |
|------|----------|------|----------|
| 订单 | `orders` | 成交笔数 | Feedback Object |
| 收入 | `revenue` | 总销售额 | Feedback Object |
| 利润 | `profit` | revenue − production_cost − platform_fee | 计算 |
| 转化率 | `conversion_rate` | orders / views 或 orders / clicks | 计算 |
| ROI | `roi` | profit / production_cost | 计算 |

---

### 6.5 System Metrics（系统指标）

| 指标 | 字段建议 | 说明 | 目标方向 |
|------|----------|------|----------|
| 自动化程度 | `automation_rate` | 无人工步骤占比 | Phase 1 低 → Phase 4 高 |
| Agent 参与比例 | `agent_involvement_rate` | Agent 完成任务 / 总任务 | 随自动化上升 |
| 错误率 | `error_rate` | 生产失败或返工次数 / 总次数 | 下降 |
| 数据完整率 | `data_completeness` | 必填指标填全比例 | ≥ 80% |

---

## 7. Feedback Object Design（反馈对象设计）

### 7.1 Feedback Object v1（扩展版）

在 [Commercial Intelligence Contract §7](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) 基础上，Commercial Experiment System 采用**结构化分组**的 Feedback Object v1，未来写入 `product_feedback` 表。

```json
{
  "contract_version": "1.0",
  "object_type": "feedback",
  "feedback_id": "fb_20260707_001",
  "experiment_id": "exp_20260707_001",
  "product_id": "e601c17c6977",
  "market_data": {
    "keyword": "",
    "category": "A",
    "platform": "",
    "competitor_price_range": ""
  },
  "traffic_data": {
    "views": 0,
    "visits": 0,
    "clicks": 0,
    "favorites": 0,
    "ctr": 0.0
  },
  "sales_data": {
    "orders": 0,
    "revenue": 0.0,
    "production_cost": 0.0,
    "platform_fee": 0.0,
    "profit": 0.0,
    "conversion_rate": 0.0
  },
  "customer_feedback": "",
  "final_result": "success | promising | failed | incomplete | cancelled",
  "recorded_at": "ISO-8601"
}
```

### 7.2 字段与数据库映射（未来 product_feedback）

| Feedback Object 字段 | product_feedback 列（Blueprint） | 说明 |
|----------------------|----------------------------------|------|
| `feedback_id` | 业务 ID 或 `id` | 主键 |
| `experiment_id` | 扩展列 `experiment_id`（Blueprint 建议新增） | 关联实验 |
| `product_id` | `product_id` FK → `generated_products.id` | 关联产品 |
| `traffic_data.views` | `views` | 已有 Blueprint 字段 |
| `traffic_data.clicks` | `clicks` | 已有 Blueprint 字段 |
| `sales_data.orders` | `sales` | Contract 用 sales |
| `sales_data.conversion_rate` | `conversion_rate` | 已有 |
| `customer_feedback` | `customer_feedback` | 已有 |
| `market_data.keyword` | 扩展列或 JSON | 关联 market_keywords |
| `final_result` | 扩展列 `evaluation_result` | 实验终态 |

**说明：** Database Extension 实施时，须在 Migration Plan 中 **Additive** 增加 `experiment_id`、`evaluation_result` 等列，禁止删除现有 Blueprint 字段。

### 7.3 MVP 过渡存储

| 阶段 | 存储方式 |
|------|----------|
| Phase 1（当前） | JSON 实验台账文件 /  spreadsheet — docs 或 `11_CONTENT_FACTORY/storage/` 过渡 |
| Phase 2 | Database Extension — `generated_products` + `product_feedback` |
| Phase 3 | 与 `opportunity_scores` 闭环 |

---

## 8. Experiment Evaluation Model（实验评估模型）

### 8.1 三级结果定义

| 结果 | 英文 | 定义 | 典型条件 |
|------|------|------|----------|
| **Success（成功）** | success | 假设验证，可扩大生产 | profit > 0 且 orders ≥ 1 |
| **Promising（有潜力）** | promising | 有互动未盈利，值得优化 | clicks ≥ 5 且 orders = 0，或 profit ≤ 0 但 conversion 高于品类均值 |
| **Failed（失败）** | failed | 假设否定，归档停止 | views < 20 且 clicks = 0；或 30 天零订单 |

### 8.2 评分维度

| 维度 | 英文 | 权重参考 | 数据来源 |
|------|------|----------|----------|
| **需求** | Demand | 30% | views, favorites, clicks |
| **转化** | Conversion | 30% | orders, conversion_rate |
| **利润** | Profit | 25% | profit, roi |
| **可扩展性** | Scalability | 15% | production_cost, automation_rate, 品类可复制性 |

### 8.3 综合评估公式（Blueprint 参考）

```
experiment_score = 0.30 × norm(demand)
                 + 0.30 × norm(conversion)
                 + 0.25 × norm(profit)
                 + 0.15 × norm(scalability)
```

| experiment_score | 映射 final_result |
|------------------|-------------------|
| ≥ 0.70 | success |
| 0.40 – 0.69 | promising |
| < 0.40 | failed |

**norm()** 为品类内归一化；MVP Phase 1 可人工判定 override。

### 8.4 实验结果对 Decision（决策层）的影响

| final_result | 3_DECISION 动作 |
|--------------|-----------------|
| success | 降低同品类 / 同 keyword 生产阈值；提高 priority |
| promising | 保持 observe；建议 pivot（调价 / 换平台 / 改包装） |
| failed | 提高 skip 权重；同 hypothesis 类型降权 |

### 8.5 实验结果对 Cognition（认知层）的影响

| final_result | 2_COGNITION 学习 |
|--------------|------------------|
| success | 正向样本 — 提高 demand_score / profit_score 权重 |
| promising | 边界样本 — 竞争 / 定价因子校准 |
| failed | 负向样本 — 降低类似 keyword opportunity_score |

**禁止：** 用单次实验结果直接 overwrite Opportunity Score；须批次聚合后调整权重。

---

## 9. Database Relationship（数据库关系）

### 9.1 商业实验数据链

```
Experiment（commercial_experiments — Blueprint 建议，未创建）
        ↓
Product（generated_products）
        ↓
Feedback（product_feedback）
        ↓
Opportunity Learning（opportunity_scores 权重优化）
```

### 9.2 表关系映射

| 层级 | Blueprint 表 | Experiment System 对象 | 状态 |
|------|--------------|------------------------|------|
| 实验台账 | `commercial_experiments`（建议新增） | Experiment Object | Missing — 随 Extension 审批 |
| 决策层 | `opportunity_scores` | opportunity_id 关联 | Missing |
| 产品层 | `generated_products` | product_id / Product Asset | Missing |
| 反馈层 | `product_feedback` | Feedback Object v1 | Missing |

### 9.3 ER 关系（Blueprint）

```
market_keywords
        ↓
opportunity_scores ←── Experiment.opportunity_id
        ↓
generated_products ←── Experiment.product_id
        ↓
product_feedback ←── Feedback.experiment_id
        ↓
（聚合分析 → Cognition 权重更新）
```

### 9.4 与 Legacy 表隔离

| Legacy 表 | 关系 |
|-----------|------|
| `scores` | Product Performance Score — **不**替代 experiment evaluation |
| `products` | Market Signal Legacy — 可辅助 market_data |
| `platforms` / `keywords` | 采集 Legacy — Additive 保留 |

详见 [Database Integration Design](../database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md) Interface 1–5。

---

## 10. Cognition Learning Connection（认知学习连接）

### 10.1 2_COGNITION 如何利用实验数据

| 数据类型 | Cognition Agent | 学习用途 |
|----------|-----------------|----------|
| **成功实验** | OpportunityAgent | 提高相似 keyword / category 的 opportunity_score |
| **失败实验** | CompetitionAgent / DemandAgent | 识别饱和品类、无效需求信号 |
| **市场反馈** | InsightAgent | 提取 customer_feedback 主题 → 产品方向 |
| **traffic_data** | DemandAgent | 校准 demand_score 与真实 CTR 相关性 |
| **sales_data** | OpportunityAgent | 校准 profit_score 权重 |

### 10.2 Opportunity Score 优化闭环

```
Experiment Feedback（product_feedback）
        ↓
批次聚合（按 category / keyword / price_band）
        ↓
Cognition 权重调整（w1–w5）
        ↓
opportunity_scores 重新计算
        ↓
3_DECISION 阈值更新
        ↓
下一轮 Experiment Design
```

### 10.3 为什么 Cognition 必须依赖实验反馈

| 原因 | 说明 |
|------|------|
| **Ground Truth（真实标签）** | 市场信号是输入；实验结果是标签 |
| **避免过拟合采集数据** | 高搜索量 ≠ 高购买意愿 |
| **品类差异** | Category A/B/C 需不同权重 — 仅实验可发现 |
| **长期资产** | 30+ 实验构成 Market Intelligence 训练集 |

**当前状态：** `2_COGNITION/` 目录为空；学习闭环为 Blueprint，待 Implementation。

---

## 11. Commercial Experiment Workflow（商业实验工作流）

### 11.1 完整流程

```
Market Signal（市场信号 — 1_DATA）
        ↓
Opportunity（商业机会 — 2_COGNITION / 人工 MVP）
        ↓
Experiment Design（实验设计 — Experiment Object Draft → Prepared）
        ↓
Content Factory（内容工厂 — 11_CONTENT_FACTORY）
        ↓
Publish（发布 — 半自动 + 人工）
        ↓
Feedback（反馈 — Feedback Object v1）
        ↓
Evaluation（评估 — Success / Promising / Failed）
        ↓
Database（数据库 — generated_products / product_feedback）
        ↓
Cognition（认知 — 2_COGNITION 权重优化）
        ↓
（循环 → 下一轮 Experiment Design）
```

### 11.2 各步骤责任

| 步骤 | 责任模块 | MVP Phase 1 实现 |
|------|----------|------------------|
| Market Signal | `1_DATA` | ✅ Legacy 采集 |
| Opportunity | `2_COGNITION` | 人工选品 |
| Experiment Design | Commercial Experiment Layer（docs） | 人工 + 台账 |
| Content Factory | `11_CONTENT_FACTORY` | ✅ Active |
| Publish | PublishAssistant + 人工 | ✅ 半自动 |
| Feedback | 人工录入 | JSON 台账 |
| Evaluation | Commercial Experiment Layer | 人工 + 公式参考 |
| Database | `1_DATA/database.py` | ⏳ Extension Pending |
| Cognition | `2_COGNITION` | ⏳ Pending |

---

## 12. Future Automation Roadmap（未来自动化路线）

| Phase | 名称 | 实验系统能力 | 人的角色 |
|-------|------|--------------|----------|
| **Phase 1** | 人工辅助实验（Manual-Assisted Experiment） | JSON 台账 + 标准 Object；Content Factory 生产 | 假设、发布、录入、评估 |
| **Phase 2** | 半自动实验（Semi-Automated Experiment） | DB 持久化；FeedbackAgent 辅助录入；Dashboard 指标 | 确认发布、复核评估 |
| **Phase 3** | AI 自动发现机会（AI Opportunity Discovery） | `2_COGNITION` 自动 Opportunity → Experiment 建议 | 审批实验批次 |
| **Phase 4** | AI 自动运营（AI-Assisted Operations） | 自动 Production Request；动态定价建议；权重自优化 | 风控确认、平台合规 |

```
Phase 1（当前 Blueprint）
    人工 Hypothesis + 人工 Feedback
        ↓
Phase 2
    Database Extension + 半自动录入
        ↓
Phase 3
    Cognition 驱动 Experiment 建议
        ↓
Phase 4
    闭环自动化（Human-in-the-loop 保留）
```

**禁止：** 跳过 Phase 1–2 数据积累，直接进入 Phase 4 全自动运营。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Commercial MVP Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md` |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Database Schema Blueprint | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` |
| Database Integration Design | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Commercial Experiment System 设计；实验台账、数据库表、Cognition 学习代码均 **Pending**，须单独审批后实施。
