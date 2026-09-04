# AI_FACTORY_OS Database Schema Blueprint v1

> 设计层文档 | 最后更新：2026-07-07  
> **状态：Schema Blueprint Completed — 无真实表创建，无数据库迁移，不参与当前运行**

---

## 1. Database Position

### 定义

AI_FACTORY_OS 数据库**不是普通存储**。

### 定位

**Long Term Business Intelligence Asset**（长期商业智能资产）

### 作用

保存：

- 市场数据
- 产品数据
- 机会分析数据
- 生产反馈数据
- 销售反馈数据

### 架构连接

```
1_DATA
    ↓
Database（data/ai_factory.db）
    ↓
2_COGNITION
    ↓
3_DECISION
    ↓
11_CONTENT_FACTORY
```

**说明：**

- 物理路径：`data/ai_factory.db`（当前已存在，由 `1_DATA/database.py` 管理）
- 逻辑定位：跨层商业数据资产，非 OS 运行时 Memory（`7_MEMORY/` 与之物理隔离）
- 本 Blueprint **不修改**现有数据库文件，仅定义目标 Schema

---

# 2. Database Architecture

## 设计逻辑（四层数据架构）

```
Raw Data Layer
    保存原始采集数据
        ↓
Analysis Layer
    保存 AI 分析结果
        ↓
Decision Layer
    保存机会评分
        ↓
Feedback Layer
    保存商业结果
```

| 层级 | 代表表 | 写入方 | 读取方 |
|------|--------|--------|--------|
| Raw Data Layer | `market_sources`, `market_keywords`, `market_products`, `market_demands` | `1_DATA` | `2_COGNITION` |
| Analysis Layer | （分析中间结果可存于 opportunity 前置字段或扩展表） | `2_COGNITION` | `2_COGNITION`, `3_DECISION` |
| Decision Layer | `opportunity_scores` | `2_COGNITION` | `3_DECISION` |
| Feedback Layer | `generated_products`, `product_feedback` | `11_CONTENT_FACTORY` | `2_COGNITION`, `7_MEMORY`（单向同步） |

---

# 3. Core Tables Design

> 以下为核心表**设计目标**。Phase 1 仅文档定义，**不创建真实表**。

---

## Table 1: `market_sources`

**用途：** 记录数据来源。

| 字段 | 类型（建议） | 说明 |
|------|--------------|------|
| `id` | INTEGER PK | 主键 |
| `source_name` | TEXT | 来源名称 |
| `platform` | TEXT | 平台标识 |
| `api_or_method` | TEXT | API 或采集方式 |
| `status` | TEXT | active / inactive / experimental |
| `created_at` | TIMESTAMP | 创建时间 |

**示例来源：**

- Google Trends
- Etsy
- Gumroad
- 淘宝
- 小红书

---

## Table 2: `market_keywords`

**用途：** 保存市场关键词趋势。

| 字段 | 类型（建议） | 说明 |
|------|--------------|------|
| `id` | INTEGER PK | 主键 |
| `keyword` | TEXT | 关键词 |
| `source_id` | INTEGER FK → `market_sources.id` | 数据来源 |
| `search_volume` | INTEGER | 搜索量 |
| `trend_score` | REAL | 趋势分数 |
| `growth_rate` | REAL | 增长率 |
| `competition_level` | REAL | 竞争程度 |
| `timestamp` | TIMESTAMP | 采集时间 |

**用于：** Trend Intelligence

---

## Table 3: `market_products`

**用途：** 保存市场已有产品。

| 字段 | 类型（建议） | 说明 |
|------|--------------|------|
| `id` | INTEGER PK | 主键 |
| `product_name` | TEXT | 产品名称 |
| `category` | TEXT | 品类 |
| `platform` | TEXT | 所在平台 |
| `price` | REAL | 价格 |
| `rating` | REAL | 评分 |
| `review_count` | INTEGER | 评论数 |
| `competition_level` | REAL | 竞争程度 |
| `created_at` | TIMESTAMP | 记录时间 |

**用于：** Competition Intelligence

---

## Table 4: `market_demands`

**用途：** 保存用户需求信号。

| 字段 | 类型（建议） | 说明 |
|------|--------------|------|
| `id` | INTEGER PK | 主键 |
| `keyword` | TEXT | 关联关键词 |
| `problem_description` | TEXT | 问题描述 |
| `demand_score` | REAL | 需求强度分 |
| `frequency` | INTEGER | 出现频次 |
| `source` | TEXT | 信号来源 |
| `timestamp` | TIMESTAMP | 记录时间 |

**用于：** Demand Intelligence

---

## Table 5: `opportunity_scores`

**用途：** 保存 `2_COGNITION` 输出。

| 字段 | 类型（建议） | 说明 |
|------|--------------|------|
| `id` | INTEGER PK | 主键 |
| `keyword_id` | INTEGER FK → `market_keywords.id` | 关联关键词 |
| `demand_score` | REAL | 需求分 |
| `trend_score` | REAL | 趋势分 |
| `competition_score` | REAL | 竞争分 |
| `profit_score` | REAL | 利润分 |
| `difficulty_score` | REAL | 生产难度分 |
| `opportunity_score` | REAL | 综合机会分 |
| `recommendation` | TEXT | produce / watch / skip |
| `created_at` | TIMESTAMP | 评分时间 |

**说明：**

- 这是 **Market Opportunity Score**
- **不是** Product Quality Score

---

## Table 6: `generated_products`

**用途：** 连接 `11_CONTENT_FACTORY`。

| 字段 | 类型（建议） | 说明 |
|------|--------------|------|
| `id` | INTEGER PK | 主键 |
| `opportunity_id` | INTEGER FK → `opportunity_scores.id` | 关联机会 |
| `product_name` | TEXT | 产品名称 |
| `product_type` | TEXT | PPT / Excel / Word / PDF 等 |
| `artifact_path` | TEXT | 产物路径（如 `artifacts/products/{id}/`） |
| `quality_score` | REAL | 产品质量分（QualityAgent） |
| `status` | TEXT | draft / released / archived |
| `created_at` | TIMESTAMP | 生产时间 |

---

## Table 7: `product_feedback`

**用途：** 保存商业反馈。

| 字段 | 类型（建议） | 说明 |
|------|--------------|------|
| `id` | INTEGER PK | 主键 |
| `product_id` | INTEGER FK → `generated_products.id` | 关联产品 |
| `views` | INTEGER | 曝光 |
| `clicks` | INTEGER | 点击 |
| `sales` | INTEGER | 销量 |
| `conversion_rate` | REAL | 转化率 |
| `customer_feedback` | TEXT | 用户反馈文本 |
| `created_at` | TIMESTAMP | 记录时间 |

**用于：** Memory 学习（未来单向同步至 `7_MEMORY` pattern 层）

---

# 4. Data Flow

```
External Data
        ↓
1_DATA Collector
        ↓
Raw Tables（market_sources / market_keywords / market_products / market_demands）
        ↓
2_COGNITION
        ↓
Opportunity Scores（opportunity_scores）
        ↓
3_DECISION
        ↓
11_CONTENT_FACTORY
        ↓
Product Feedback（generated_products / product_feedback）
        ↓
Database（数据资产沉淀）
        ↓
Memory（7_MEMORY — OS 运行时学习，物理隔离）
```

---

# 5. Relationship Design

```
market_sources
        ↓
market_keywords
        ↓
opportunity_scores
        ↓
generated_products
        ↓
product_feedback
```

**辅助关系：**

- `market_demands` — 可独立关联 `keyword`，供 Demand Intelligence 输入
- `market_products` — 按 `category` / `platform` 供 Competition Intelligence 聚合
- `opportunity_scores.keyword_id` → `market_keywords.id` → `market_sources.id`（可追溯数据来源）

---

# 6. Scoring System Separation

**必须明确：两个评分体系，禁止混合。**

## Market Opportunity Score

| 项 | 说明 |
|----|------|
| **负责** | 是否值得生产 |
| **来源** | `2_COGNITION` |
| **存储** | `opportunity_scores` 表 |
| **消费** | `3_DECISION` |

---

## Product Quality Score

| 项 | 说明 |
|----|------|
| **负责** | 产品质量 |
| **来源** | `11_CONTENT_FACTORY` QualityAgent |
| **存储** | `generated_products.quality_score` |
| **消费** | release_gate、包装与发布决策 |

**禁止：** 将 Quality Score 写入 `opportunity_scores`；将 Opportunity Score 作为产品质量依据。

---

# 7. Data Asset Strategy

## 数据库长期价值

| 阶段 | 价值 |
|------|------|
| **短期** | 辅助选品 |
| **中期** | 提升生产成功率 |
| **长期** | 形成 **Market Intelligence Asset** |

## 未来商业化可能

- 数据分析服务
- AI 选品 API
- SaaS 市场洞察

**当前阶段：** Schema Blueprint 已完成，不启动外部商业化。

---

# 8. Data Lifecycle Management

```
Raw Data
    ↓
Processed Data
    ↓
Intelligence Data
    ↓
Business Feedback Data
```

## 原则

数据必须：

- **可追踪** — 每条 opportunity 可追溯到 source 与 keyword
- **可复用** — 历史评分与反馈可供下一轮 Cognition 分析
- **可分析** — 时间序列字段支持趋势复盘

## 与文件资产的关系

| 资产类型 | 位置 | 关系 |
|----------|------|------|
| 数据库商业资产 | `data/ai_factory.db` | 本 Blueprint |
| Content Factory 产物 | `11_CONTENT_FACTORY/artifacts/` | `generated_products.artifact_path` 引用 |
| OS 运行记忆 | `7_MEMORY/` | 单向同步，不混写 |
| JSON 产品记忆 | `11_CONTENT_FACTORY/storage/product_memory.json` | 未来可同步至 `generated_products` |

---

# 9. Future Implementation Roadmap

| Phase | 名称 | 内容 | 状态 |
|-------|------|------|------|
| **Phase 1** | Schema Blueprint | 表结构、关系、数据流设计 | **Completed** |
| **Phase 2** | Review existing ai_factory.db | 审计现有表结构与 Blueprint 差异 | Pending |
| **Phase 3** | Database migration plan | 迁移脚本设计（仍须审批后执行） | Pending |
| **Phase 4** | 1_DATA integration | Collector 写入 Raw Tables | Pending |
| **Phase 5** | 2_COGNITION integration | 读取 Raw、写入 opportunity_scores | Pending |

---

# 10. Security and Maintenance

## 未来考虑（设计预留）

- **数据备份** — 定期备份 `ai_factory.db`
- **数据版本** — Schema 版本号与 migration 历史
- **数据来源记录** — `market_sources` 全链路追溯
- **时间序列保存** — `timestamp` / `created_at` 字段标准化，支持历史对比

## 与现有资产审计的关系

见 [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md](../../07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md) — `data/ai_factory.db` 当前为 **Active** 生产数据库。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Cognition 蓝图 | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| Data Intelligence 蓝图 | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_DATA_INTELLIGENCE_BLUEPRINT.md` |
| 模块注册表 | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
| 资产审计 | `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md` |
| 工程进度 | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` |
