# AI_FACTORY_OS Experiment Object Registry v1

> 商业实验对象登记体系 | 最后更新：2026-07-08  
> **状态：Blueprint Completed — Project Intelligence Layer 登记规范，不参与运行计算**

**定位：** Commercial Experiment Object Registry（商业实验对象登记体系）— 为 30 产品实验、Feedback Loop（反馈闭环）、Database Extension（数据库扩展）、2_COGNITION Learning（认知学习）提供**标准化实验资产登记规范**。

**上级文档：**

- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md](AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md) — 实验管理体系
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md](AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md) — MVP 验证目标
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — Object 契约 v1

**说明：** **Blueprint ≠ Implementation（蓝图不等于实施）**。本文档定义登记规范与 Schema；不创建代码、不创建数据库表、不写入运行层。

---

## 1. Experiment Object Definition（实验对象定义）

### 1.1 标准 JSON Schema v1

每条商业实验须登记为一条 **Experiment Object（实验对象）**。以下为 Registry v1 权威 Schema：

```json
{
  "experiment_id": "",
  "version": "1.0",
  "category": "",
  "hypothesis": "",
  "target_market": "",
  "keyword": "",
  "opportunity_source": "",
  "product_type": "",
  "production_request": "",
  "content_asset": "",
  "publish_channel": "",
  "test_period": "",
  "metrics": {
    "production": "",
    "market": "",
    "commercial": "",
    "system": ""
  },
  "feedback_status": "",
  "result": "",
  "learning_summary": ""
}
```

### 1.2 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `experiment_id` | TEXT | ✅ | 实验唯一 ID，格式建议 `exp_YYYYMMDD_NNN` |
| `version` | TEXT | ✅ | Schema 版本，当前固定 `"1.0"` |
| `category` | TEXT | ✅ | `A` / `B` / `C` — 见 §3 |
| `hypothesis` | TEXT | ✅ | 实验假设 — 用户是谁、解决什么问题、为何购买 |
| `target_market` | TEXT | ✅ | 目标市场 / 目标用户群 |
| `keyword` | TEXT | ✅ | 关联市场关键词 |
| `opportunity_source` | TEXT | | 机会来源：`manual` / `1_DATA` / `2_COGNITION` / `legacy_scoring` |
| `product_type` | TEXT | ✅ | `ppt` / `excel` / `word` / `pdf` |
| `production_request` | TEXT / OBJECT | | Production Request ID 或 JSON 指针 — 关联 `3_DECISION` 产出 |
| `content_asset` | TEXT | | Product Asset 路径或 `product_id` — 关联 `11_CONTENT_FACTORY` 产出 |
| `publish_channel` | TEXT | | 发布渠道：闲鱼 / 淘宝 / Etsy / Gumroad 等 |
| `test_period` | TEXT | | 测试观察期，如 `2026-07-08 ~ 2026-07-22` |
| `metrics` | OBJECT | | 四类指标 — 见 §1.3 |
| `feedback_status` | TEXT | | 生命周期状态 — 见 §2 |
| `result` | TEXT | | 评估结果：`success` / `promising` / `failed` / `incomplete` / `cancelled` |
| `learning_summary` | TEXT | | 实验复盘摘要 — 供 Cognition 与人类阅读 |

### 1.3 metrics 四类指标结构（Registry v1）

`metrics` 各子字段为 **OBJECT 或 JSON 字符串**，须包含以下键（可为空，Testing 阶段后补全）：

#### metrics.production（生产指标 — Production Metrics）

```json
{
  "production_time_minutes": 0,
  "ai_cost": 0.0,
  "human_cost": 0.0,
  "production_cost": 0.0,
  "first_pass": true,
  "quality_score": 0.0
}
```

#### metrics.market（市场指标 — Market Metrics）

```json
{
  "views": 0,
  "visits": 0,
  "clicks": 0,
  "favorites": 0,
  "ctr": 0.0
}
```

#### metrics.commercial（商业指标 — Commercial Metrics）

```json
{
  "orders": 0,
  "revenue": 0.0,
  "profit": 0.0,
  "conversion_rate": 0.0,
  "roi": 0.0,
  "expected_price": 0.0
}
```

#### metrics.system（系统指标 — System Metrics）

```json
{
  "automation_rate": 0.0,
  "agent_involvement_rate": 0.0,
  "error_rate": 0.0,
  "data_completeness": 0.0
}
```

### 1.4 完整登记示例

```json
{
  "experiment_id": "exp_20260708_001",
  "version": "1.0",
  "category": "A",
  "hypothesis": "中小企业主需要快速可用的商业计划书 PPT 模板，愿为省时间付费",
  "target_market": "中小企业主、创业初期团队",
  "keyword": "商业计划书 PPT 模板",
  "opportunity_source": "manual",
  "product_type": "ppt",
  "production_request": "req_20260708_001",
  "content_asset": "11_CONTENT_FACTORY/artifacts/products/e601c17c6977/",
  "publish_channel": "xianyu",
  "test_period": "2026-07-08 ~ 2026-07-22",
  "metrics": {
    "production": {
      "production_time_minutes": 25,
      "ai_cost": 0.5,
      "human_cost": 2.0,
      "production_cost": 2.5,
      "first_pass": true,
      "quality_score": 0.85
    },
    "market": {
      "views": 0,
      "visits": 0,
      "clicks": 0,
      "favorites": 0,
      "ctr": 0.0
    },
    "commercial": {
      "orders": 0,
      "revenue": 0.0,
      "profit": 0.0,
      "conversion_rate": 0.0,
      "roi": 0.0,
      "expected_price": 19.9
    },
    "system": {
      "automation_rate": 0.7,
      "agent_involvement_rate": 0.8,
      "error_rate": 0.0,
      "data_completeness": 0.5
    }
  },
  "feedback_status": "published",
  "result": "",
  "learning_summary": ""
}
```

### 1.5 与 Commercial Experiment System Blueprint 对齐

| Registry 字段 | Experiment System Blueprint 字段 |
|---------------|----------------------------------|
| `hypothesis` + `target_market` | `hypothesis` 五问对象 |
| `feedback_status` | Experiment Lifecycle `status` |
| `result` | Evaluation `final_result` |
| `metrics.*` | Experiment Metrics System 四类指标 |

---

## 2. Experiment Lifecycle（实验生命周期）

### 2.1 状态定义

| 状态 | 英文 | 含义 |
|------|------|------|
| **Draft（草案）** | draft | 实验构思，字段未完整 |
| **Prepared（准备完成）** | prepared | 假设与品类已定，可进入生产 |
| **Production（生产中）** | production | Content Factory 正在生产 |
| **Published（已发布）** | published | 已人工确认上架 |
| **Testing（测试阶段）** | testing | 观察期，收集 metrics |
| **Validated（验证成功）** | validated | 评估为 Success，假设成立 |
| **Promising（有潜力）** | promising | 有互动未达 Success，值得优化 |
| **Failed（失败）** | failed | 假设否定，停止同方向实验 |
| **Archived（归档）** | archived | 实验关闭，资产保留 |

**登记字段：** 当前状态写入 `feedback_status`；终态评估写入 `result`。

### 2.2 状态流转

```
Draft
    ↓  hypothesis + category + target_market 完整
Prepared
    ↓  production_request 下发
Production
    ↓  content_asset 产出 + 上架
Published
    ↓  test_period 开始
Testing
    ↓  metrics 录入 + 评估
    ├──→ Validated（result: success）──→ Archived
    ├──→ Promising（result: promising）──→ Archived
    └──→ Failed（result: failed）──→ Archived
```

### 2.3 转换条件

| 从 | 到 | 条件 |
|----|-----|------|
| draft | prepared | `hypothesis`、`category`、`target_market`、`keyword`、`product_type` 非空 |
| prepared | production | `production_request` 已关联 |
| production | published | `content_asset` 非空；`publish_channel` 已指定 |
| published | testing | `test_period` 开始；上架完成 |
| testing | validated | `result` = success；metrics.commercial 完整 |
| testing | promising | `result` = promising；metrics.market 有 clicks 无 orders |
| testing | failed | `result` = failed；观察期满且无转化 |
| validated / promising / failed | archived | `learning_summary` 已填写 |

### 2.4 feedback_status 与 result 关系

| feedback_status | result（可选） | 说明 |
|-----------------|----------------|------|
| draft ~ testing | 空 | 进行中 |
| validated | success | 终态 — 成功 |
| promising | promising | 终态 — 有潜力 |
| failed | failed | 终态 — 失败 |
| archived | 任意终态 | 已归档 |

---

## 3. 30 产品实验管理规则（Product Experiment Management Rules）

### 3.1 批次总览

| 项 | 值 |
|----|-----|
| **总实验数** | 30 |
| **登记要求** | 每个产品 1 条 Experiment Object |
| **存储（MVP 过渡）** | docs 台账 JSON 文件或 spreadsheet — **非运行代码** |
| **未来存储** | `commercial_experiments` 表 — **未创建** |

### 3.2 Category A — 低成本快速验证（Low-Cost Rapid Validation）

| 项 | 内容 |
|----|------|
| **数量** | 10 |
| **category 值** | `A` |
| **实验目的** | 用最低生产成本快速验证品类是否有基本市场需求 |
| **典型 product_type** | ppt / excel / word |
| **定价带** | ¥9.9 – ¥19.9 |
| **生产策略** | 最短 pipeline；最少 LLM 调用 |
| **成功参考** | views ≥ 50 或 clicks ≥ 5 |
| **登记重点** | `metrics.production.production_cost` 必须精确记录 |

### 3.3 Category B — 市场需求验证（Market Demand Validation）

| 项 | 内容 |
|----|------|
| **数量** | 10 |
| **category 值** | `B` |
| **实验目的** | 验证特定关键词 / 用户群是否有真实付费需求 |
| **典型 product_type** | pdf / ppt（AI 工具包、提示词库） |
| **定价带** | ¥19.9 – ¥49.9 |
| **生产策略** | 完整 Creator + Quality；强调需求匹配 |
| **成功参考** | conversion_rate 高于 Category A 批次均值 |
| **登记重点** | `keyword`、`target_market`、`hypothesis` 必须详细 |

### 3.4 Category C — 高潜力商业实验（High-Potential Commercial Experiment）

| 项 | 内容 |
|----|------|
| **数量** | 10 |
| **category 值** | `C` |
| **实验目的** | 验证高客单价、行业深度产品是否可持续盈利 |
| **典型 product_type** | pdf / word（行业资料包、解决方案包） |
| **定价带** | ¥29.9 – ¥99.9 |
| **生产策略** | 多 artifact 组合；行业关键词精准定位 |
| **成功参考** | profit > 0 且 customer_feedback 正向 |
| **登记重点** | `metrics.commercial.roi`、`learning_summary` 必须完整 |

### 3.5 登记门禁规则

| 规则 | 说明 |
|------|------|
| 无 experiment_id 的生产 | 不纳入 30 批次统计 |
| 无 hypothesis 的实验 | 不得从 draft 进入 prepared |
| 同 keyword 重复实验 | 须新 experiment_id，并在 learning_summary 引用前次结果 |
| 数据缺失 | feedback_status 不得进入 validated / promising / failed |

---

## 4. 实验与现有模块关系（Module Integration）

### 4.1 运行时数据流

```
Experiment Object（登记 — docs / 未来 DB）
        ↓
3_DECISION（Decision Layer — 决策层）
    产出 Production Request；阈值裁决
        ↓
11_CONTENT_FACTORY（Content Factory — 内容工厂）
    产出 Product Asset；回填 content_asset
        ↓
10_DEPLOY（Deployment Layer — 部署层）
    可选 API 接入；非商业 Object 持久化
        ↓
Feedback Object（反馈对象 — 人工 / 未来 FeedbackAgent）
    回填 metrics.market / metrics.commercial
        ↓
7_MEMORY（Memory Layer — 运行记忆层）
    单向摘要同步 pattern — 不替代 Experiment Registry
```

### 4.2 各模块职责

| 模块 | 与 Experiment Object 关系 | 读/写 |
|------|---------------------------|-------|
| **Experiment Registry（本文档体系）** | 权威登记源 | 写：实验全字段 |
| **`3_DECISION`** | 消费 opportunity / 人工选品；产出 `production_request` | 读：Prepared 实验；写：production_request 指针 |
| **`11_CONTENT_FACTORY`** | 执行生产；产出 `content_asset` | 读：Production Request；写：content_asset |
| **`10_DEPLOY`** | HTTP 服务；不参与实验登记 | 无 Experiment 读写 |
| **Feedback 流程** | 更新 metrics；驱动 result 评估 | 写：metrics / result |
| **`7_MEMORY`** | 吸收 learning_summary 摘要 | 只读摘要；禁止覆盖 Registry |

### 4.3 与 Commercial Intelligence Contract 映射

| Contract Object | Registry 字段 |
|-----------------|---------------|
| Production Request Object | `production_request` |
| Product Asset Object | `content_asset` |
| Feedback Object | `metrics` + `result` |
| Opportunity Object | `opportunity_source` + `keyword` |

---

## 5. 与未来数据库映射（Future Database Mapping）

### 5.1 预留表关系

**以下表均为 Blueprint 设计 — 当前未创建。**

```
commercial_experiments（建议新增 — 实验登记）
        ↓ experiment_id
generated_products（Blueprint Table 6）
        ↓ product_id
product_feedback（Blueprint Table 7）
        ↓ 聚合
opportunity_scores（Blueprint Table 5 — Cognition 学习）
```

### 5.2 commercial_experiments（建议表 — Missing）

| Registry 字段 | 建议 DB 列 |
|---------------|------------|
| `experiment_id` | `experiment_id` TEXT UNIQUE |
| `version` | `schema_version` TEXT |
| `category` | `category` TEXT |
| `hypothesis` | `hypothesis` TEXT |
| `target_market` | `target_market` TEXT |
| `keyword` | `keyword` TEXT |
| `opportunity_source` | `opportunity_source` TEXT |
| `product_type` | `product_type` TEXT |
| `production_request` | `production_request_id` TEXT |
| `content_asset` | `content_asset_path` TEXT |
| `publish_channel` | `publish_channel` TEXT |
| `test_period` | `test_period` TEXT |
| `metrics` | `metrics_json` TEXT / JSON |
| `feedback_status` | `status` TEXT |
| `result` | `result` TEXT |
| `learning_summary` | `learning_summary` TEXT |

### 5.3 generated_products 关联

| 关联 | 说明 |
|------|------|
| `content_asset` → `artifact_path` | Product Asset 物理路径 |
| `experiment_id` → 扩展 FK | Database Extension 时 Additive 增加 |
| `quality_score` | 来自 `metrics.production.quality_score` |

### 5.4 product_feedback 关联

| 关联 | 说明 |
|------|------|
| `experiment_id` | 扩展列 — 关联实验 |
| `metrics.market.*` | 映射 `views`, `clicks` 等 |
| `metrics.commercial.*` | 映射 `sales`, `revenue`, `conversion_rate` |
| `result` | 扩展列 `evaluation_result` |

**实施须走：** [Database Extension Implementation Plan](../database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md) — 须单独审批。

---

## 6. 实验评价规则（Experiment Evaluation Rules）

### 6.1 Success（成功）

| 项 | 定义 |
|----|------|
| **result 值** | `success` |
| **feedback_status** | `validated` → `archived` |
| **条件** | `metrics.commercial.orders` ≥ 1 **且** `metrics.commercial.profit` > 0 |
| **Decision 影响** | 降低同 category / keyword 生产阈值；提高 priority |
| **Cognition 影响** | 正向样本 — 提高类似 keyword 的 opportunity_score 权重 |
| **learning_summary 须含** | 成功因素、可复制要素、建议扩大方向 |

### 6.2 Promising（有潜力）

| 项 | 定义 |
|----|------|
| **result 值** | `promising` |
| **feedback_status** | `promising` → `archived` |
| **条件** | `metrics.market.clicks` ≥ 5 **且** `metrics.commercial.orders` = 0；或有点击但 profit ≤ 0 |
| **Decision 影响** | 保持 observe；建议 pivot（调价 / 换 publish_channel / 改包装） |
| **Cognition 影响** | 边界样本 — 竞争 / 定价因子校准 |
| **learning_summary 须含** | 卡点分析、建议调整项、是否值得二次实验 |

### 6.3 Failed（失败）

| 项 | 定义 |
|----|------|
| **result 值** | `failed` |
| **feedback_status** | `failed` → `archived` |
| **条件** | `metrics.market.views` < 20 **且** `metrics.market.clicks` = 0；或观察期满且 orders = 0 |
| **Decision 影响** | 提高 skip 权重；同 hypothesis 类型降权 |
| **Cognition 影响** | 负向样本 — 降低类似 keyword opportunity_score |
| **learning_summary 须含** | 失败原因、不可复制因素、停止方向 |

### 6.4 评价流程

```
Testing 期满
    ↓
metrics 四类完整性检查（data_completeness ≥ 0.8）
    ↓
按 §6.1–6.3 规则判定 result
    ↓
填写 learning_summary
    ↓
feedback_status → validated / promising / failed
    ↓
归档 → archived
```

---

## 7. AI 后续读取规则（AI Read Rules for Cognition）

### 7.1 适用范围

未来 `2_COGNITION` Market Intelligence Layer（市场智能层）及 AI 协作者读取 Experiment Object Registry 时，须遵守以下规则。

### 7.2 可读取数据

| 数据类型 | 用途 | 读取条件 |
|----------|------|----------|
| **成功实验（Success Experiments）** | 正向训练样本；提高 opportunity_score | `result` = success 且 `feedback_status` = archived |
| **失败实验（Failed Experiments）** | 负向样本；降低无效 keyword 权重 | `result` = failed 且 learning_summary 非空 |
| **市场反馈（Market Feedback）** | 校准 demand / trend 因子 | `metrics.market` 完整 |
| **产品类型（Product Types）** | 品类优先级排序 | 按 category + product_type 聚合 |
| **用户需求变化（User Demand Shifts）** | InsightAgent 主题提取 | `learning_summary` + customer_feedback 摘要 |

### 7.3 禁止读取 / 使用方式

| 禁止 | 原因 |
|------|------|
| 用单次实验 overwrite Opportunity Score | 须批次聚合 |
| 读取 draft / prepared 未完成实验作训练 | 数据不完整 |
| 直接写回 Experiment Registry | Cognition 只消费，不修改登记源 |
| 混用 Quality Score 与 Opportunity Score | 语义隔离 — 见 Contract |

### 7.4 读取优先级

```
1. archived + result 非空（终态实验）
2. metrics.commercial 完整（有商业结果）
3. learning_summary 非空（有人类复盘）
4. category 内样本 ≥ 3 再调整权重（避免过拟合）
```

### 7.5 与 7_MEMORY 边界

| 层 | 职责 |
|----|------|
| **Experiment Object Registry** | 商业实验长期登记 — 权威源 |
| **`7_MEMORY`** | OS 运行时 pattern — 可吸收 learning_summary **摘要** |
| **Database** | 未来持久化 — Implementation Pending |

**规则：** Memory 摘要不得替代 Registry 完整记录；Cognition 学习优先读 Registry / DB，非 Memory。

---

## 8. Registry 使用说明

### 8.1 MVP Phase 1 登记方式

| 方式 | 说明 | 状态 |
|------|------|------|
| JSON 台账文件 | 每实验一条 JSON 或数组文件 | 推荐 — 人工维护 |
| spreadsheet | 字段列与 Schema 对齐 | 可选 |
| `commercial_experiments` 表 | DB 持久化 | **Pending — 未创建** |

### 8.2 登记检查清单

- [ ] `experiment_id` 唯一
- [ ] `version` = `"1.0"`
- [ ] `category` ∈ {A, B, C}
- [ ] `hypothesis` + `target_market` + `keyword` 非空
- [ ] 状态变更时更新 `feedback_status`
- [ ] Testing 结束后填写 `metrics` 四类
- [ ] 评估后填写 `result` + `learning_summary`
- [ ] 终态后 `feedback_status` → archived

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Commercial Experiment System Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_EXPERIMENT_SYSTEM_BLUEPRINT.md` |
| Commercial MVP Blueprint | `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md` |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Database Schema Blueprint | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |

---

**Blueprint ≠ Implementation。** 本文档完成 Experiment Object Registry 登记规范；实验台账文件、数据库表、Cognition 读取代码均 **Pending**，须单独审批后实施。
