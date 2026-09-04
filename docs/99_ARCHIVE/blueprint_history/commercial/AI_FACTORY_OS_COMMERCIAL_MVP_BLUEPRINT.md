# AI_FACTORY_OS Commercial MVP Validation Blueprint v1

> 商业验证阶段设计蓝图 | Last updated: 2026-07-15（Entry **041-D** banner）

| Document Role | Architecture / Commercial Design Reference |
|---------------|---------------------------------------------|
| Reality Status | Design Reference |
| Runtime Status | Requires Reality Validation |

**状态：Blueprint Completed — 认知层设计，不参与运行计算。**  
**禁止：** Design = Runtime · Blueprint = Production · Blueprint Completed = 市场验证完成。

**定位：** Commercial Validation Layer（商业验证层）— 定义 AI Factory OS 从「能够生产」到「能够持续发现、生产并销售数字资产」的最小商业验证路径。

**相关文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — 商业智能 Object 契约 v1
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md](AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md) — 商业化战略设计
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md) — Market Intelligence Layer（市场智能层）设计
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md) — 反馈数据持久化 Schema
- [docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md](../../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md) — 模块注册表

**说明：** 本文档为 **Blueprint（设计蓝图）**，不代表代码或数据库已实施。Implementation（实施）须单独审批后执行。

---

## 1. Commercial MVP Definition（商业最小验证定义）

### 1.1 阶段目标

AI Factory OS 当前阶段目标**不是**最大化生产能力，而是验证：

> **「AI Factory 是否能够持续发现、生产并销售数字资产」**

即：系统能否形成可重复、可度量、可优化的商业闭环，而非单次演示性生产。

### 1.2 MVP（Minimum Viable Product，最小可行产品）边界

| 范围内 | 范围外 |
|--------|--------|
| 30 个数字产品商业实验 | 大规模自动化生产 |
| 半自动发布 + 人工确认上架 | 全自动平台发布 |
| 销售数据人工/半自动录入 | 高风险销售数据爬虫 |
| 验证品类 / 定价 / 转化率 | SaaS / API 商业化 |
| 反馈数据沉淀设计 | 完整 Cognition 代码实现 |

### 1.3 核心验证问题

| # | 验证问题 |
|---|----------|
| 1 | 哪类产品类型（办公 / AI 工具 / 行业）有真实市场需求？ |
| 2 | 什么定价区间能够产生购买转化？ |
| 3 | 单件数字商品的生产成本是否低于售价？ |
| 4 | 系统选品逻辑是否优于随机选品？ |
| 5 | 销售反馈能否反哺下一轮产品方向？ |

### 1.4 验证指标（MVP Success Metrics，最小验证成功指标）

| 指标类别 | 指标 | MVP 目标（Phase 1 参考） |
|----------|------|--------------------------|
| **市场验证** | 有效曝光产品数 | ≥ 30 个产品完成上架 |
| **互动验证** | 有点击产品占比 | ≥ 30% 产品获得 ≥ 1 次点击 |
| **转化验证** | 有销售产品数 | ≥ 3 个产品产生 ≥ 1 笔订单 |
| **盈利验证** | 盈利产品数 | ≥ 1 个产品 revenue > production_cost |
| **系统验证** | 反馈数据完整率 | ≥ 80% 产品具备完整 views/clicks/sales 记录 |
| **闭环验证** | 优化迭代次数 | ≥ 1 轮基于反馈的产品方向调整 |

**说明：** 以上为 Blueprint 参考阈值，实际执行时可据平台与品类微调，但须记录于实验台账。

---

## 2. MVP Business Loop（商业闭环）

### 2.1 完整流程

```
Market Signal（市场信号）
        ↓
Opportunity Object（商业机会对象）
        ↓
Production Request（生产请求）
        ↓
Content Factory（内容工厂）
        ↓
Product Asset（产品资产）
        ↓
Publish（发布）
        ↓
Customer Feedback（用户反馈）
        ↓
Database（数据库）
        ↓
Optimization（优化）
        ↓
（循环 → Market Signal / Cognition）
```

### 2.2 各阶段责任模块

| 阶段 | Object / 动作 | 责任模块 | 当前状态 |
|------|---------------|----------|----------|
| **Market Signal（市场信号）** | Market Signal Object | `1_DATA` | ✅ Active — collector / database |
| **Opportunity（商业机会）** | Opportunity Object | `2_COGNITION`（未来）/ 人工选品（MVP 过渡） | ⏳ Blueprint — 代码 Pending |
| **Production Request（生产请求）** | Production Request Object | `3_DECISION` | ✅ Active — 未完全标准化为本 Object |
| **Content Factory（内容工厂）** | 生产流水线 | `11_CONTENT_FACTORY` | ✅ Active — 真实 artifact 生产 |
| **Product Asset（产品资产）** | Product Asset Object | `11_CONTENT_FACTORY` | ✅ Active — artifacts + product_memory |
| **Publish（发布）** | 半自动发布辅助 | `11_CONTENT_FACTORY` PublishAssistant + 人工 | ✅ Active — 非自动发布 |
| **Customer Feedback（用户反馈）** | Feedback Object | 人工录入 / FeedbackAgent（未来） | ⏳ 设计完成 — DB 表 Pending |
| **Database（数据库）** | 持久化 | `1_DATA/database.py` → `ai_factory.db` | ✅ Legacy Active — Blueprint 表 Pending |
| **Optimization（优化）** | 权重 / 阈值调整 | `2_COGNITION` + `3_DECISION` + `7_MEMORY`（摘要） | ⏳ 未来 — MVP 阶段人工分析 |

### 2.3 OS 调度边界

所有运行时 Object 经 `0_START` → ExecutionRuntime（执行运行时）调度传递，禁止模块跨层直读内部文件。详见 [Commercial Intelligence Contract](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)。

### 2.4 MVP 过渡路径（Current → Target）

**当前真实运行流（无 Cognition）：**

```
1_DATA → 3_DECISION → 11_CONTENT_FACTORY → Publish（人工）→ Feedback（人工）→ product_memory.json
```

**目标商业闭环（Blueprint）：**

```
1_DATA → 2_COGNITION → 3_DECISION → 11_CONTENT_FACTORY → Publish → Feedback → Database → Optimization
```

MVP Phase 1 允许人工替代 `2_COGNITION` 选品环节，但**必须**按标准字段记录实验数据，为 Phase 3 评分优化预留训练样本。

---

## 3. First Commercial Experiment Design（第一批商业实验设计）

### 3.1 实验规模

| 项 | 值 |
|----|-----|
| **产品数量** | **30** |
| **实验周期** | 建议 8–12 周（含生产、上架、观察、复盘） |
| **实验类型** | 数字商品 A/B 品类 + 定价验证 |

### 3.2 产品分布

| 类别 | 数量 | 示例子类型 | 优先 artifact 类型 |
|------|------|------------|-------------------|
| **办公类（Office）** | 10 | PPT 模板、Excel 模板、Word 模板、简历模板 | ppt / excel / word |
| **AI 工具类（AI Tools）** | 10 | 提示词库、AI 工作流包、办公 AI 工具包 | pdf / ppt |
| **行业类（Industry）** | 10 | 电商运营资料、创业资料包、自媒体运营包 | pdf / word |

### 3.3 实验目的

验证以下维度：

| 维度 | 验证内容 |
|------|----------|
| **产品类型（Product Type）** | 哪类 artifact 更易获得曝光与转化 |
| **定价（Pricing）** | 低 / 中 / 高价位（如 ¥9.9 / ¥19.9 / ¥39.9）转化率差异 |
| **市场需求（Market Demand）** | 关键词 / 品类搜索热度与真实购买相关性 |
| **转化率（Conversion Rate）** | views → clicks → orders 漏斗 |
| **生产成本（Production Cost）** | 单件生产耗时、LLM 调用成本 vs 售价 |

### 3.4 单产品实验记录模板

| 字段 | 说明 |
|------|------|
| `experiment_id` | 实验批次 ID |
| `product_id` | 产品唯一 ID |
| `category` | office / ai_tools / industry |
| `keyword` | 关联市场关键词 |
| `product_type` | ppt / excel / word / pdf |
| `price` | 定价 |
| `platform` | 销售平台（闲鱼 / 淘宝 / Etsy / Gumroad 等） |
| `production_cost` | 生产成本（时间 + 算力估算） |
| `production_time_minutes` | 生产耗时（分钟） |
| `publish_date` | 上架日期 |
| `views` | 曝光 |
| `clicks` | 点击 |
| `favorites` | 收藏 |
| `orders` | 购买 / 订单数 |
| `revenue` | 收入 |
| `customer_feedback` | 用户评价 / 咨询摘要 |
| `profit` | revenue − production_cost |
| `conversion_rate` | orders / views（或 clicks） |
| `verdict` | continue / pivot / stop |

### 3.5 成功标准（Success Criteria，成功标准）

| 层级 | 指标 | 参考阈值 | 含义 |
|------|------|----------|------|
| **曝光（Views）** | 单产品 views | ≥ 50（平台可调） | 产品获得基础市场触达 |
| **点击（Clicks）** | 单产品 clicks | ≥ 5 | 标题 / 封面 / 定价有吸引力 |
| **收藏（Favorites）** | 单产品 favorites | ≥ 2 | 潜在购买意向 |
| **购买（Orders）** | 单产品 orders | ≥ 1 | 真实付费验证 |
| **利润（Profit）** | 单产品 profit | > 0 | 商业可持续 |
| **批次级** | 盈利产品占比 | ≥ 10%（≥ 3/30） | 品类方向有效 |
| **批次级** | 总 revenue | > 总 production_cost | 批次整体不亏损 |

**判定规则：**

- **continue（继续）** — orders ≥ 1 且 profit > 0
- **pivot（调整）** — clicks ≥ 5 但 orders = 0 → 调整定价 / 包装 / 描述
- **stop（停止）** — views < 20 且 clicks = 0 → 放弃该品类或关键词方向

---

## 4. Product Selection Strategy（产品选择策略）

### 4.1 评分维度

| 维度 | 英文 | 说明 | 数据来源 |
|------|------|------|----------|
| **市场需求** | Market Demand | 搜索量、想要数、问题描述强度 | `1_DATA` Market Signal |
| **趋势** | Trend | 上升 / 平稳 / 下降 | `2_COGNITION` TrendAgent（未来） |
| **竞争** | Competition | 同类商品数量、价格带、差异化空间 | `2_COGNITION` CompetitionAgent（未来） |
| **生产成本** | Production Cost | 生产耗时、算力、人工复核成本 | `11_CONTENT_FACTORY` 生产日志 |
| **利润潜力** | Profit Potential | 预期售价 − 生产成本 − 平台费用 | 人工估算 + 历史 Feedback |

### 4.2 Market Opportunity Score（市场机会评分）vs Product Quality Score（产品质量评分）

**必须分离 — 语义不可混用。**

| 评分 | 定义 | 产出模块 | 用途 |
|------|------|----------|------|
| **Market Opportunity Score（市场机会评分）** | 「是否值得生产」 | `2_COGNITION` → Opportunity Object | 选品、排产优先级 |
| **Product Quality Score（产品质量评分）** | 「生产质量是否达标」 | `11_CONTENT_FACTORY` QualityAgent | 发布门禁、质检 |

**禁止：**

- 用 Quality Score 替代 Opportunity Score 做选品
- 用 Legacy `scores.total_score`（商品表现分）替代 Opportunity Score
- 在 Opportunity Object 中混入 quality_score 字段

### 4.3 Opportunity Score 合成公式（Blueprint 参考）

```
opportunity_score = w1 × demand_score
                  + w2 × trend_score
                  + w3 × (1 − competition_score)
                  + w4 × profit_score
                  − w5 × difficulty_score
```

权重 `w1–w5` 在 MVP Phase 3 根据 Feedback 数据优化；Phase 1 可使用均等权重或人工 override。

### 4.4 MVP 选品流程（过渡）

```
1_DATA 采集 Market Signal
        ↓
人工 / 半自动筛选（MVP 过渡，替代 2_COGNITION）
        ↓
3_DECISION 阈值裁决 → Production Request
        ↓
11_CONTENT_FACTORY 生产
        ↓
Quality Score 门禁（独立于 Opportunity Score）
        ↓
发布
```

---

## 5. Feedback Data Architecture（反馈数据架构）

### 5.1 设计目的

沉淀商业反馈长期资产，用于：

1. 训练未来 `2_COGNITION` 评分权重
2. 调整 `3_DECISION` 生产阈值
3. 优化 Content Factory 品类与定价策略
4. 单向摘要同步至 `7_MEMORY` pattern（不反向混写 DB）

### 5.2 核心字段定义

#### 产品维度

| 字段 | 类型 | 说明 |
|------|------|------|
| `product_id` | TEXT | 产品唯一 ID，关联 Product Asset |
| `generated_product_id` | INTEGER | 未来 `generated_products` 表主键 |
| `production_request_id` | TEXT | 关联 Production Request |
| `opportunity_id` | INTEGER | 未来 `opportunity_scores` 表主键 |

#### 市场维度

| 字段 | 类型 | 说明 |
|------|------|------|
| `keyword` | TEXT | 关联市场关键词 |
| `keyword_id` | INTEGER | 未来 `market_keywords` 外键 |
| `category` | TEXT | office / ai_tools / industry |
| `platform` | TEXT | 销售平台 |

#### 销售维度

| 字段 | 类型 | 说明 |
|------|------|------|
| `views` | INTEGER | 曝光 |
| `clicks` | INTEGER | 点击 |
| `favorites` | INTEGER | 收藏 |
| `orders` | INTEGER | 订单 / 购买数 |
| `revenue` | REAL | 收入 |
| `conversion_rate` | REAL | 转化率（计算字段） |

#### 反馈维度

| 字段 | 类型 | 说明 |
|------|------|------|
| `customer_feedback` | TEXT | 用户评价、咨询、退货原因 |
| `feedback_sentiment` | TEXT | positive / neutral / negative（未来 NLP） |
| `recorded_at` | ISO-8601 | 记录时间 |

### 5.3 目标持久化位置

| 层级 | 位置 | 状态 |
|------|------|------|
| **Blueprint 目标表** | `product_feedback` | Missing — Implementation Pending |
| **Blueprint 目标表** | `generated_products` | Missing — Implementation Pending |
| **当前过渡** | `11_CONTENT_FACTORY/storage/product_memory.json` | Active — 非标准 Contract 格式 |
| **Legacy** | `scores` 表 | Active — Product Performance Score，非 Feedback |

### 5.4 Feedback Object 对齐

反馈录入须对齐 [Commercial Intelligence Contract §7 Feedback Object](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)：

```json
{
  "contract_version": "1.0",
  "object_type": "feedback",
  "product_id": "",
  "views": 0,
  "clicks": 0,
  "sales": 0,
  "revenue": 0.0,
  "conversion_rate": 0.0,
  "customer_feedback": "",
  "platform": "",
  "recorded_at": "ISO-8601"
}
```

MVP Phase 1 可人工维护 JSON / 表格；Phase 2 迁移至 Database Extension 后的 `product_feedback` 表。

### 5.5 训练 Cognition 的数据用途

| Feedback 字段 | Cognition 用途 |
|---------------|----------------|
| `views` / `clicks` | 校准 demand_score 权重 |
| `orders` / `revenue` | 校准 profit_score 权重 |
| `customer_feedback` | InsightAgent 主题提取 |
| `keyword` + 表现 | 关键词机会排名优化 |
| 品类聚合 | TrendAgent / CompetitionAgent 阈值调整 |

---

## 6. Content Factory Connection（内容工厂连接）

### 6.1 输入：Production Request Object（生产请求对象）

`11_CONTENT_FACTORY` 通过 OS 调度接收 Production Request，**禁止**自行读 `opportunity_scores` 或跨模块文件选品。

**Schema（v1 — 引用 Contract）：**

```json
{
  "contract_version": "1.0",
  "object_type": "production_request",
  "request_id": "req_20260707_001",
  "opportunity_id": null,
  "keyword": "PPT 商业计划书模板",
  "action": "publish",
  "priority": 1,
  "product_type": "ppt",
  "product_spec": {
    "title": "2026 商业计划书 PPT 模板",
    "category": "office",
    "target_platform": "xianyu",
    "notes": "MVP experiment batch 1"
  },
  "decision_reason": "opportunity_score >= 0.7",
  "threshold_met": true,
  "created_at": "2026-07-07T12:00:00+08:00"
}
```

### 6.2 Content Factory 内部流水线映射

| Production Request 字段 | Content Factory 组件 |
|-------------------------|----------------------|
| `product_spec.title` | CreatorAgent 输入 |
| `product_type` | ProductGenerator / artifact_generators |
| `keyword` | MarketAgent 上下文 |
| `product_spec.category` | 模板选择 / 包装策略 |
| `action: skip` | **不** 进入生产流水线 |

**当前实现（Reality）：** pipeline 接受 OS `input_data`，尚未完全标准化为 Production Request Object 字段校验。

### 6.3 输出：Product Asset Object（产品资产对象）

**Schema（v1 — 引用 Contract）：**

```json
{
  "contract_version": "1.0",
  "object_type": "product_asset",
  "product_id": "e601c17c6977",
  "opportunity_id": null,
  "production_request_id": "req_20260707_001",
  "product_name": "2026 商业计划书 PPT 模板",
  "product_type": "ppt",
  "artifact_path": "11_CONTENT_FACTORY/artifacts/products/e601c17c6977/",
  "bundle_path": "11_CONTENT_FACTORY/artifacts/products/e601c17c6977/final_product.zip",
  "quality_score": 0.85,
  "status": "released",
  "source": "experiment",
  "metadata_path": "11_CONTENT_FACTORY/artifacts/products/e601c17c6977/metadata.json",
  "created_at": "2026-07-07T12:30:00+08:00"
}
```

### 6.4 字段职责说明

| 字段 | 来源 Agent | 说明 |
|------|------------|------|
| `product_id` | ProductGenerator | 唯一 ID |
| `quality_score` | QualityAgent | **Product Quality Score** — 非 Opportunity Score |
| `artifact_path` | ArtifactManager | 产物目录指针 |
| `bundle_path` | BundleBuilder | final_product.zip |
| `status` | ReleaseGate | draft → released |
| `source` | MVP 实验标记 | `experiment` 用于 30 产品批次 |

### 6.5 发布辅助输出

ReleaseGate / PublishAssistant 额外产出（非 Product Asset Object 核心字段）：

- `publish_package/title.txt`
- `publish_package/description.txt`
- `publish_package/keywords.txt`
- `publish_package/pricing.json`
- `publish_assistant/publish_checklist.md`

人工确认后上架，销售数据回写 Feedback Object。

---

## 7. Cognition Connection（认知层连接）

### 7.1 未来 2_COGNITION 职责

| 方向 | 内容 |
|------|------|
| **输入** | Market Signal（via `1_DATA` → Database Raw Layer） |
| **输入（闭环）** | Feedback Object（via `product_feedback` 表） |
| **输出** | Opportunity Object → `3_DECISION` |
| **Agent 链** | TrendAgent → DemandAgent → CompetitionAgent → OpportunityAgent → InsightAgent |

详见 [Cognition Agent Architecture Blueprint](../runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md)。

### 7.2 Opportunity Object 输出示例

```json
{
  "contract_version": "1.0",
  "object_type": "opportunity",
  "keyword": "Excel 财务模板",
  "demand_score": 0.82,
  "trend_score": 0.75,
  "competition_score": 0.45,
  "profit_score": 0.70,
  "difficulty_score": 0.30,
  "opportunity_score": 0.78,
  "recommendation": "produce",
  "product_idea": "中小企业月度财务 Excel 模板包",
  "created_at": "ISO-8601"
}
```

### 7.3 为什么 Cognition 必须依赖商业反馈（Customer Feedback）

| 原因 | 说明 |
|------|------|
| **市场信号 ≠ 真实需求** | 采集到的搜索量、想要数可能不代表付费意愿 |
| **评分权重需校准** | demand / trend / competition 权重只有用真实 sales 数据验证才可靠 |
| **避免生产幻觉** | 无 Feedback 闭环时，系统可能持续生产「看起来有机会」但不赚钱的产品 |
| **竞争动态变化** | Feedback 揭示哪些品类已饱和、哪些定价带失效 |
| **长期资产积累** | Feedback 是 Database 层长期资产，Cognition 训练样本来源 |

**结论：** Cognition 不是一次性分析模块，而是 **Feedback-Driven Intelligence（反馈驱动智能）** — 没有 Customer Feedback → Database → Optimization 闭环，Market Intelligence Layer（市场智能层）无法持续进化。

### 7.4 MVP 阶段 Cognition 占位策略

| Phase | Cognition 状态 | 选品方式 |
|-------|----------------|----------|
| Phase 1 | 未实现 | 人工 + Market Signal 辅助 |
| Phase 2 | 未实现 | 结构化 Feedback 录入 |
| Phase 3 | 初始实现 | Opportunity Score v0 + 人工复核 |
| Phase 4+ | 完整 Agent 链 | 自动化选品 + Decision 阈值 |

---

## 8. MVP Timeline（最小验证时间线）

### Phase 1 — 30 产品实验（Product Experiment，产品实验）

| 项 | 内容 |
|----|------|
| **目标** | 生产并上架 30 个数字产品 |
| **周期** | 4–6 周 |
| **产出** | 30 × Product Asset + publish_package |
| **模块** | `11_CONTENT_FACTORY`（主）、`3_DECISION`（辅助）、人工发布 |
| **数据** | product_memory / 实验台账 |

### Phase 2 — 数据收集（Data Collection，数据收集）

| 项 | 内容 |
|----|------|
| **目标** | 完整记录 views / clicks / orders / revenue / feedback |
| **周期** | 4–6 周（与 Phase 1 重叠观察期） |
| **产出** | Feedback Object 批次数据集 |
| **模块** | 人工录入 → 未来 `product_feedback` 表 |
| **前置** | Database Extension 审批（可选，非阻塞 MVP 人工台账） |

### Phase 3 — 评分优化（Scoring Optimization，评分优化）

| 项 | 内容 |
|----|------|
| **目标** | 基于 Feedback 优化 Opportunity Score 权重与 Decision 阈值 |
| **周期** | 2–4 周 |
| **产出** | 品类 / 定价 / 关键词优先级列表 |
| **模块** | `2_COGNITION`（初始）、`3_DECISION` |
| **前置** | ≥ 30 产品完整 Feedback 样本 |

### Phase 4 — 自动化生产（Automated Production，自动化生产）

| 项 | 内容 |
|----|------|
| **目标** | Data → Cognition → Decision → Content Factory 链路接通 |
| **周期** | 4–8 周 |
| **产出** | 端到端 Object 流 + Database Contract 落地 |
| **模块** | `2_COGNITION` + Database Extension + OS 调度 |
| **前置** | Cognition Agent Implementation + DB Implementation |

### Phase 5 — 商业扩大（Commercial Scale，商业扩大）

| 项 | 内容 |
|----|------|
| **目标** | 扩大产品批次、验证可复制盈利模型 |
| **周期** | 持续 |
| **产出** | 第二批 50–100 产品、品类聚焦策略 |
| **模块** | 全链路 Active |
| **前置** | Phase 1–4 验证通过（≥ 1 可持续盈利品类） |

```
Phase 1 ──→ Phase 2
   │            │
   └──────┬─────┘
          ↓
      Phase 3（评分优化）
          ↓
      Phase 4（自动化生产）
          ↓
      Phase 5（商业扩大）
```

---

## 9. Commercial Metrics（商业指标）

### 9.1 生产指标（Production Metrics，生产指标）

| 指标 | 定义 | 采集来源 |
|------|------|----------|
| 产品数量 | 已生产并 release 的产品总数 | Product Asset 计数 |
| 生产时间 | 单件从 Production Request 到 Product Asset 耗时 | Content Factory 日志 |
| 一次通过率 | Quality Score ≥ 阈值无需返工占比 | QualityAgent |
| 单件生产成本 | LLM + 人工复核成本估算 | 实验台账 |

### 9.2 市场指标（Market Metrics，市场指标）

| 指标 | 定义 | 采集来源 |
|------|------|----------|
| 曝光（Views） | 产品展示次数 | 平台后台 / 人工录入 |
| 点击（Clicks） | 详情页访问次数 | 平台后台 / 人工录入 |
| 点击率（CTR） | clicks / views | 计算 |
| 收藏（Favorites） | 收藏 / 想要数 | 平台后台 |

### 9.3 商业指标（Business Metrics，商业指标）

| 指标 | 定义 | 采集来源 |
|------|------|----------|
| 销售（Orders / Sales） | 成交订单数 | Feedback Object |
| 收入（Revenue） | 总销售额 | Feedback Object |
| 利润（Profit） | revenue − production_cost − platform_fee | 计算 |
| 转化率（Conversion Rate） | orders / views 或 orders / clicks | 计算 |
| ROI（Return on Investment，投资回报率） | profit / production_cost | 计算 |

### 9.4 系统指标（System Metrics，系统指标）

| 指标 | 定义 | 目标方向 |
|------|------|----------|
| 自动化程度 | 无需人工介入的步骤占比 | Phase 1 低 → Phase 4 高 |
| Object 标准化率 | 符合 Commercial Intelligence Contract 的 Object 占比 | → 100% |
| 反馈数据完整率 | 具备完整 Feedback 字段的产品占比 | ≥ 80% |
| 闭环迭代周期 | 从 Feedback 到下一轮 Opportunity 调整的天数 | 缩短 |

### 9.5 指标看板（Blueprint 参考）

| 维度 | Phase 1 关注 | Phase 3+ 关注 |
|------|--------------|---------------|
| 生产 | 产品数量、生产时间 | 一次通过率、单件成本 |
| 市场 | 曝光、点击 | CTR、品类对比 |
| 商业 | 首单、首利 | ROI、品类利润排名 |
| 系统 | 数据完整率 | 自动化程度、闭环周期 |

---

## 10. Future Monetization Expansion（未来变现扩展）

### 10.1 扩展路径

| 路径 | 英文 | 说明 | 优先级 |
|------|------|------|--------|
| **数字产品销售** | Digital Product Sales | 自营虚拟商品 — 当前 MVP 核心 | **P0 — 当前** |
| **SaaS（软件即服务）** | Software as a Service | 开放 Content Factory 生产能力订阅 | P2 — Phase 5 后 |
| **Agent 服务** | Agent Services | 按任务计费的 AI 生产 Agent API | P2 — 需 Phase 4 稳定 |
| **数据服务** | Data Services | 市场机会报告、趋势 API | P3 — 需 Cognition + DB 成熟 |

### 10.2 当前优先：AI Factory 自营商业验证

**明确优先级：**

```
P0: AI Factory 自营数字商品销售验证（本文档 MVP）
        ↓
P1: Feedback 驱动 Cognition 优化
        ↓
P2: 对外 SaaS / Agent 服务
        ↓
P3: 数据服务 / API 经济
```

**禁止：** 在 MVP 未验证盈利前启动 SaaS 后台、多租户、API 商业平台。详见 [Monetization Blueprint §11](AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md)。

### 10.3 与 9_PRODUCT（Frozen）的关系

`9_PRODUCT` 目录保留早期 SaaS/API 实验代码，**Frozen（冻结）** 状态，不参与当前 MVP 主链。未来 SaaS 化须基于 MVP 验证数据重新设计，不得直接激活 Frozen 层。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Content Factory Monetization | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_CONTENT_FACTORY_MONETIZATION_BLUEPRINT.md` |
| Cognition Blueprint | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| Database Schema Blueprint | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
| Project Status | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` |

---

**Blueprint ≠ Implementation。** 本文档完成商业验证阶段设计；代码、数据库、运行逻辑变更须单独审批后执行。
