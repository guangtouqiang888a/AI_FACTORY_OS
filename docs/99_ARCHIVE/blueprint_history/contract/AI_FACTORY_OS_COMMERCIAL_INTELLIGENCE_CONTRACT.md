# AI_FACTORY_OS Commercial Intelligence Contract v1

> 商业智能数据契约 | 最后更新：2026-07-07  
> **状态：Contract Completed — 文档层契约，无代码/DB 变更**

**定位：** Commercial Intelligence Contract Layer — 定义商业智能模块之间传递的**标准对象**、**权限边界**与**数据库映射**。

**相关文档：**

- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](../database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md) — Database 层接口
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md) — 2_COGNITION 架构
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md) — 表结构
- [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md](../commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md) — 项目认知总览

---

## 1. Purpose

本契约统一 AI_FACTORY_OS **商业智能链路**中各模块交换的数据对象：

```
Market Signal → Opportunity → Production Request → Product Asset → Feedback
```

**原则：**

- 模块经 **标准 Object + Database Contract** 通信
- 禁止跨模块直接读内部文件
- 经 `0_START` → ExecutionRuntime 调度传递运行时对象
- 持久化经 `1_DATA/database.py` 统一访问

---

## 2. Commercial Intelligence Flow

```
External Market
    ↓
1_DATA          → Market Signal Object
    ↓
2_COGNITION     → Opportunity Object
    ↓
3_DECISION      → Production Request Object
    ↓
11_CONTENT_FACTORY → Product Asset Object
    ↓
Feedback        → Feedback Object
    ↓
2_COGNITION / 3_DECISION / Database（闭环）
```

---

## 3. Market Signal Object

### 定义

**市场原始信号** — `1_DATA` 采集输出，不含商业裁决。

### Schema（v1）

```json
{
  "contract_version": "1.0",
  "object_type": "market_signal",
  "keyword": "",
  "source": "",
  "platform_id": 1,
  "signal_type": "keyword | product | demand | trend",
  "payload": {
    "title": "",
    "price": 0.0,
    "want_count": 0,
    "view_count": 0,
    "problem_description": "",
    "raw_json": {}
  },
  "collect_date": "YYYY-MM-DD",
  "timestamp": "ISO-8601"
}
```

### 生产者 / 消费者

| 角色 | 模块 |
|------|------|
| **Producer** | `1_DATA`（collector / sources） |
| **Consumer** | `2_COGNITION`（未来）、Database Raw Layer |

### 规则

- 禁止包含 `opportunity_score`、`action`、`recommendation`
- 当前 Legacy 等价：`products` 行 + `keywords` upsert

---

## 4. Opportunity Object

### 定义

**市场机会情报** — `2_COGNITION` 输出，`3_DECISION` 输入。

### Schema（v1）

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

### 生产者 / 消费者

| 角色 | 模块 |
|------|------|
| **Producer** | `2_COGNITION` |
| **Consumer** | `3_DECISION` |

### 规则

- **Market Opportunity Score** — 与 Product Quality Score、Legacy `scores.total_score` **语义隔离**
- Cognition **不**附带 Production Request，不触发 Content Factory

---

## 5. Production Request Object

### 定义

**生产指令** — `3_DECISION` 批准后，经 OS 调度至 Content Factory。

### Schema（v1）

```json
{
  "contract_version": "1.0",
  "object_type": "production_request",
  "request_id": "",
  "opportunity_id": null,
  "keyword": "",
  "action": "publish | observe | skip",
  "priority": 1,
  "product_type": "ppt | excel | word | pdf",
  "product_spec": {
    "title": "",
    "category": "",
    "target_platform": "",
    "notes": ""
  },
  "decision_reason": "",
  "threshold_met": true,
  "created_at": "ISO-8601"
}
```

### 生产者 / 消费者

| 角色 | 模块 |
|------|------|
| **Producer** | `3_DECISION`（decision_engine / decision_agent） |
| **Consumer** | `11_CONTENT_FACTORY`（pipeline / agents） |

### 规则

- `action: skip` 时 **不得** 生成 Production Request 下游任务
- 当前 Legacy：`ScoringAgent` + `decide_scored()` 产出类似语义，未标准化为本 Object
- 须经 `controller.run()` / DAG 传递，Content Factory 不自行读 `opportunity_scores`

---

## 6. Product Asset Object

### 定义

**已生产数字产品资产** — Content Factory 交付结果。

### Schema（v1）

```json
{
  "contract_version": "1.0",
  "object_type": "product_asset",
  "product_id": "",
  "opportunity_id": null,
  "production_request_id": "",
  "product_name": "",
  "product_type": "ppt | excel | word | pdf",
  "artifact_path": "11_CONTENT_FACTORY/artifacts/products/{product_id}/",
  "bundle_path": "",
  "quality_score": 0.0,
  "status": "draft | released | archived",
  "source": "opportunity | manual | experiment",
  "metadata_path": "",
  "created_at": "ISO-8601"
}
```

### 生产者 / 消费者

| 角色 | 模块 |
|------|------|
| **Producer** | `11_CONTENT_FACTORY` |
| **Consumer** | Database（`generated_products`）、Feedback 流程、人工发布 |

### 规则

- `quality_score` 来自 QualityAgent — **Product Quality Score**
- 文件存 `artifacts/`；DB 存指针（`artifact_path`），不存 BLOB
- 当前过渡：`storage/product_memory.json` + `metadata.json`（Implementation 后映射至本 Object）

---

## 7. Feedback Object

### 定义

**商业反馈** — 销售/用户/平台表现数据。

### Schema（v1）

```json
{
  "contract_version": "1.0",
  "object_type": "feedback",
  "product_id": "",
  "generated_product_id": null,
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

### 生产者 / 消费者

| 角色 | 模块 |
|------|------|
| **Producer** | 人工录入 / 半自动导入 / `11_CONTENT_FACTORY` FeedbackAgent（未来） |
| **Consumer** | `2_COGNITION`（权重优化）、`3_DECISION`（阈值调整）、Database |

### 规则

- 反馈写入 `product_feedback`（未来表）
- 可单向摘要同步至 `7_MEMORY` pattern — **不**反向混写 DB
- 禁止高风险自动爬取销售数据

---

## 8. Module Permission Boundary

| 模块 | 可读 | 可写 | 禁止 |
|------|------|------|------|
| **`1_DATA`** | External Data | Market Signal → DB Raw | Opportunity、Decision、Production |
| **`2_COGNITION`** | Raw DB、Feedback（读） | Opportunity → DB | Production Request、Product Asset、直接生产 |
| **`3_DECISION`** | Opportunity、Legacy scores、Feedback（读） | Production Request（OS 传递） | Raw 采集、Cognition 分析、Artifact 文件 |
| **`11_CONTENT_FACTORY`** | Production Request（OS 输入） | Product Asset、Feedback | 自行选品、读 opportunity 内部文件 |
| **`7_MEMORY`** | Feedback 摘要（单向，未来） | OS 运行 pattern | 直接写 DB、替代 Cognition |
| **`0_START`** | 调度全链 Object | 无 DB 直写 | 绕过 Contract 的跨层读写 |
| **`10_DEPLOY`** | API 请求/响应 | deploy logs | 商业 Object 持久化 |

---

## 9. Database Mapping

| Object | 目标表（Blueprint） | Legacy 表（当前） | 状态 |
|--------|---------------------|-------------------|------|
| Market Signal | `market_keywords`, `market_products`, `market_demands`, `market_sources` | `keywords`, `products`, `platforms`, `collection_log` | Partial — Legacy Active |
| Opportunity | `opportunity_scores` | — | Missing |
| Production Request | —（OS 运行时传递，可选 audit 表未来扩展） | `output/*.json`（模拟） | Partial |
| Product Asset | `generated_products` | —（文件：`artifacts/products/`） | Missing DB |
| Feedback | `product_feedback` | — | Missing |

### Legacy `scores` 映射说明

| 项 | 说明 |
|----|------|
| **不属于 Opportunity Object** | `scores` = Product Performance Score |
| **保留** | Additive Evolution，见 Migration Plan |

---

## 10. Version Strategy

### 契约版本

| 字段 | 说明 |
|------|------|
| `contract_version` | semver 字符串，当前 **`"1.0"`** |
| 所有 Object 必须携带 | 消费者须校验 major 版本兼容 |

### 版本演进规则

| 变更类型 | 版本 bump | 示例 |
|----------|-----------|------|
| 新增可选字段 | minor（1.0 → 1.1） | 增加 `feedback.platform` |
| 必填字段变更 / 语义变更 | major（1.x → 2.0） | `recommendation` 枚举扩展须文档化 |
| 新 Object 类型 | 新 object_type | 不影响现有 v1 消费者 |

### 与 Database Schema 版本

- Database `schema_version`（未来）独立于 `contract_version`
- Contract 变更不自动 imply DB migration — 须走 Implementation Plan

---

## 11. Agent Contract Rules

### 通用规则

1. 所有 Agent 实现 `BaseAgent.execute(input_data, context)`
2. Agent **只**消费/生产本模块 Permission 内 Object
3. 运行时 Object 经 OS `input_data["data"]` 传递，形状须符合本契约
4. 持久化 Object 经 `database.py` 读写，禁止 Agent 内 `sqlite3.connect`

### 模块 Agent 契约

| 模块 | Agent（现有/规划） | 输入 Object | 输出 Object |
|------|-------------------|-------------|-------------|
| `1_DATA` | DataAgent / XianyuCollector | External | Market Signal（implicit） |
| `2_COGNITION` | Market/Trend/Competition/Opportunity Analyst（规划） | Market Signal（via DB） | Opportunity |
| `3_DECISION` | ScoringAgent、DecisionAgent | Market Signal / scores（Legacy）、Opportunity（未来） | Production Request（implicit） |
| `11_CONTENT_FACTORY` | Creator/Quality/Packaging/Feedback Agent | Production Request | Product Asset、Feedback |

### 禁止

- Agent 职责重叠（Cognition 不生产文件；Quality 不输出 Opportunity）
- Agent 绕过 ExecutionRuntime 独立启动
- Agent 直接读 `artifacts/`、`product_memory.json` 做跨模块决策

---

## 12. Object Flow Summary

```
Market Signal Object     ← 1_DATA
        ↓
Opportunity Object       ← 2_COGNITION
        ↓
Production Request Object ← 3_DECISION
        ↓
Product Asset Object     ← 11_CONTENT_FACTORY
        ↓
Feedback Object        ← Feedback / FeedbackAgent
        ↓
（闭环 → Cognition / Decision / DB）
```

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Database Integration | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
| Work Principles | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` |
