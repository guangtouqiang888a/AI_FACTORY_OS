# AI_FACTORY_OS Database Integration Design v1

> 架构设计文档 | 最后更新：2026-07-07  
> **状态：Interface Design Completed — 无代码修改，无数据库变更，无迁移执行**

**依据文档：**

- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md)
- [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md](../../07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md)
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md](AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md)
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md)

---

## 1. Purpose

### 定义

本文件定义 **Database Asset Layer**（`data/ai_factory.db`）与各业务模块之间的**数据交互规范**（Database Contract）。

### 目标

- 统一 `1_DATA`、`2_COGNITION`、`3_DECISION`、`11_CONTENT_FACTORY` 的读写边界
- 禁止模块间直接读取彼此内部文件
- 为 Phase 2–5 Implementation 提供接口契约，而非立即改代码

### 不在本文件范围

- SQL 建表语句执行
- Python 实现细节
- `7_MEMORY` 直接混写 DB（Memory 仅未来单向同步）

---

## 2. Architecture Position

### 数据流总览

```
1_DATA
    ↓  [Interface 1: Raw Data Write]
Database Asset Layer（data/ai_factory.db）
    ↓  [Interface 2: Raw Data Read → Opportunity Write]
2_COGNITION
    ↓  [Interface 3: Opportunity → Decision Input]
3_DECISION
    ↓  [Production Instruction — 经 OS 调度，非 DB 直写]
11_CONTENT_FACTORY
    ↓  [Interface 4: Production Result Write]
Database（generated_products）
    ↓  [Interface 5: Feedback Loop]
Feedback（product_feedback）
    ↓
2_COGNITION / 3_DECISION（未来改进）
    ↓
7_MEMORY（单向同步，物理隔离）
```

### Database Asset Layer 定位

| 属性 | 说明 |
|------|------|
| **物理路径** | `data/ai_factory.db` |
| **管理入口** | `1_DATA/database.py`（当前唯一 DB 访问层） |
| **性质** | Long Term Business Intelligence Asset |
| **原则** | 模块经 **Database Contract** 读写，不跨模块读文件 |

---

## 3. Interface 1 — 1_DATA → Database

### 职责

**Data Collection** — 采集外部数据，写入 Raw Data Layer。

### 输入

**External Data** — 搜索趋势、电商平台、内容平台、Excel 采集文件等。

### 输出

**Raw Data Tables**（目标态 + Legacy 并存）

| 目标表（Blueprint） | Legacy 表（当前 Active） | 写入方 |
|---------------------|------------------------|--------|
| `market_sources` | `platforms` | `1_DATA` |
| `market_keywords` | `keywords` | `1_DATA` |
| `market_products` | `products` | `1_DATA` |
| `market_demands` | —（待建） | `1_DATA` |
| — | `collection_log` | `1_DATA` |

### Market Data Object（1_DATA 内部标准化输出）

```json
{
  "keyword": "",
  "source": "",
  "platform_id": 1,
  "title": "",
  "price": 0.0,
  "want_count": 0,
  "view_count": 0,
  "collect_date": "YYYY-MM-DD",
  "raw_json": {}
}
```

### 原则

- **`1_DATA` 不负责决策** — 不写入 `opportunity_scores`、不调用 Decision 逻辑
- **只写事实** — 采集什么就存什么，不做商业判断
- **双写过渡期**（Implementation 阶段）：Legacy 表与 Blueprint 表可并行写入，见 Migration Plan §4

### 当前实现对照

| 函数 | 写入表 | 状态 |
|------|--------|------|
| `ensure_schema()` | Legacy 表初始化 | Active |
| `upsert_keyword()` | `keywords` | Active |
| `insert_product()` | `products` | Active |
| `start/finish_collection_log()` | `collection_log` | Active |

---

## 4. Interface 2 — Database → 2_COGNITION

### 职责

**Market Intelligence** — 读取 Raw Data，分析后输出 Opportunity Object。

### 输入

**Raw Data** — 自以下表读取（Implementation 后）：

- `market_keywords` / `keywords`
- `market_products` / `products`
- `market_demands`
- `market_sources` / `platforms`

### 输出

**Opportunity Object**（标准 JSON Contract）

```json
{
  "keyword": "",
  "demand_score": 0.0,
  "trend_score": 0.0,
  "competition_score": 0.0,
  "profit_score": 0.0,
  "opportunity_score": 0.0,
  "recommendation": "produce | watch | skip"
}
```

### 写入

**`opportunity_scores`** 表（待建）

| 字段 | 来源 |
|------|------|
| `keyword_id` | 关联 `market_keywords.id` |
| `demand_score` ~ `difficulty_score` | Cognition 分析 |
| `opportunity_score` | 加权综合 |
| `recommendation` | produce / watch / skip |
| `created_at` | 时间戳 |

### 原则

- **`2_COGNITION` 只读 Raw、只写 Analysis/Decision Layer** — 不生产数字文件
- **Market Opportunity Score** — 与 `scores`（product 级）语义隔离
- 经 OS 调度传递 JSON，不绕过 `controller.run()`

---

## 5. Interface 3 — 2_COGNITION → 3_DECISION

### 职责

```
Opportunity Discovery
        ↓
Production Decision
```

### 输入

**Opportunity Object**（来自 Interface 2 或 OS DAG 上游节点）

可选补充：**Legacy `scores`** — 已采集商品表现（product 级，非机会级）

### Decision 输出（Production Decision Object）

```json
{
  "keyword": "",
  "action": "publish | observe | skip",
  "priority": 1,
  "opportunity_id": null,
  "best_opportunity_score": 0.0,
  "reason": ""
}
```

### 明确边界

| 模块 | 负责 | 不负责 |
|------|------|--------|
| **`2_COGNITION`** | 机会发现、评分、recommendation | 不直接生产、不执行 publish |
| **`3_DECISION`** | **accept / reject / prioritize** | 不做市场原始分析、不采集数据 |

### Decision 规则（设计目标）

- `recommendation == "skip"` → Decision 默认 `action: skip`
- `recommendation == "produce"` + `opportunity_score >= threshold` → `action: publish` 或进入 Content Factory 队列
- `recommendation == "watch"` → `action: observe`
- **Cognition 不直接生产** — Content Factory 仅在 Decision 批准后触发

### 当前实现对照

| 现状 | 说明 |
|------|------|
| `ScoringAgent` 读 `products`、写 `scores` | Legacy product 评分链，保持至 Additive 接入完成 |
| `decide_scored()` | 基于 product scores 决策，未来扩展读取 `opportunity_scores` |

---

## 6. Interface 4 — 11_CONTENT_FACTORY → Database

### 职责

将 **Production Result** 持久化为 Database 资产。

### 输入

**Production Result** — Content Factory pipeline 完成产物后：

```json
{
  "opportunity_id": null,
  "product_name": "",
  "product_type": "ppt | excel | word | pdf",
  "artifact_path": "11_CONTENT_FACTORY/artifacts/products/{product_id}/",
  "quality_score": 0.0,
  "status": "draft | released | archived"
}
```

### 写入

**`generated_products`** 表（待建）

| 字段 | 说明 |
|------|------|
| `product_name` | 产品名称 |
| `artifact_path` | 产物目录或 `final_product.zip` 路径 |
| `quality_score` | **Product Quality Score**（QualityAgent） |
| `status` | draft / released / archived |
| `opportunity_id` | 关联 `opportunity_scores.id`（可追溯） |

### 原则

- **Quality Score 写入 `generated_products`** — 不写入 `opportunity_scores`
- **`artifact_path` 引用文件系统路径** — DB 存指针，文件存 `artifacts/products/`
- 当前 `storage/product_memory.json` 为过渡存储；Implementation 后双写或迁移至 DB

### 当前状态

`11_CONTENT_FACTORY` **尚未使用 DB** — 仅 `product_memory.json` + `artifacts/`。本 Interface 为 Implementation 目标。

---

## 7. Feedback Loop

### 闭环定义

```
Sales / User Feedback
        ↓
product_feedback（Database 写入）
        ↓
Cognition Improvement（2_COGNITION 读取反馈模式）
        ↓
Future Decision（3_DECISION 阈值/策略调整）
        ↓
7_MEMORY（单向同步 pattern，可选）
```

### Product Feedback Object

```json
{
  "product_id": 1,
  "views": 0,
  "clicks": 0,
  "sales": 0,
  "conversion_rate": 0.0,
  "customer_feedback": ""
}
```

### 写入

**`product_feedback`** 表 — 关联 `generated_products.id`

### 读取方

| 模块 | 用途 |
|------|------|
| `2_COGNITION` | 优化机会评分权重、品类偏好 |
| `3_DECISION` | 调整 publish 阈值 |
| `7_MEMORY` | 单向同步高阶 pattern（不反向写 DB） |

### 原则

- 反馈数据为 **Business Feedback Data Layer**
- 人工录入或半自动导入均可，禁止高风险自动爬取销售数据

---

## 8. Existing Compatibility

### Legacy Active 表 — 必须保留

| Legacy 表 | 当前用途 | Integration 策略 |
|-----------|----------|------------------|
| `platforms` | 平台注册 | 与 `market_sources` 双写或映射 |
| `keywords` | 关键词追踪 | 与 `market_keywords` 扩展并存 |
| `products` | 市场商品采集 | 与 `market_products` 映射 |
| `scores` | Product/Market Item Scoring | **保留**，与 `opportunity_scores` 隔离 |
| `collection_log` | 采集历史 | **保留**，作为 Data Collection History |

### Additive Evolution

```
Legacy 表（继续服务当前运行链）
        +
Blueprint 新表（market_*、opportunity_scores、generated_products、product_feedback）
        =
统一 Database Contract 查询层（未来 database.py 扩展）
```

### 禁止

- ❌ 停用 `collector.py` 对 `products`/`keywords` 的写入直至新表验证通过
- ❌ 将 `scores` 重命名为 `opportunity_scores`

---

## 9. Data Contract Rules

### 核心规则

| # | 规则 |
|---|------|
| 1 | 模块之间**禁止直接读取其他模块内部文件**（如 `11_CONTENT_FACTORY/storage/` 被 `2_COGNITION` 直接读） |
| 2 | 跨模块数据交换**必须通过 Database Contract** 或 **OS 标准 JSON 对象**（经 ExecutionRuntime 传递） |
| 3 | 所有 DB 访问**经 `1_DATA/database.py`**（或未来统一的 `database` 访问层），禁止各模块独立 `sqlite3.connect` |
| 4 | **评分语义隔离** — Opportunity Score ≠ Quality Score ≠ Legacy Product Score |
| 5 | **`7_MEMORY` 不直接写 DB** — 仅可选单向读取 feedback 摘要同步 pattern |

### Contract 层级

```
Layer A: OS Protocol JSON（DAG 节点间传递 — make_output / input_data）
Layer B: Database Contract（持久化 — 表 + 标准 Object）
Layer C: File Artifacts（artifact_path 指针 — 大文件不存 DB BLOB）
```

### 违规示例（禁止）

- `2_COGNITION` 直接读取 `11_CONTENT_FACTORY/artifacts/products/*/metadata.json`
- `3_DECISION` 直接解析 `product_memory.json` 做决策
- `11_CONTENT_FACTORY` 绕过 Decision 自行读 `opportunity_scores` 选品（应经 OS 调度）

---

## 10. Future Implementation Roadmap

| Phase | 名称 | 内容 | 状态 |
|-------|------|------|------|
| **Phase 1** | Interface Design | 本文档 — Database Integration Design v1 | **Completed** |
| **Phase 2** | Database Extension | 按 Migration Plan 执行 ADDITIVE 建表 | Pending |
| **Phase 3** | 1_DATA Integration | Legacy + Blueprint 双写 Raw Tables | Pending |
| **Phase 4** | 2_COGNITION Implementation | 读 Raw、写 `opportunity_scores` | Pending |
| **Phase 5** | Feedback Loop | `generated_products` + `product_feedback` + Cognition 回读 | Pending |

### Phase 1 完成检查清单

- [x] Interface 1–4 定义
- [x] Feedback Loop 定义
- [x] Legacy Compatibility 说明
- [x] Data Contract Rules
- [ ] Phase 2 SQL（须单独审批）
- [ ] Python 实现（须单独审批）

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Schema Blueprint | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md` |
| Reality Audit | `docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md` |
| Migration Plan | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md` |
| Cognition Blueprint | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| 模块注册表 | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
