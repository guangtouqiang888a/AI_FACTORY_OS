# AI_FACTORY_OS Cognition Agent Architecture Blueprint v1

> 2_COGNITION Agent 架构设计 | 最后更新：2026-07-07  
> **状态：Blueprint Completed — 无运行代码，无数据库变更**

**上级文档：**

- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](AI_FACTORY_OS_COGNITION_BLUEPRINT.md) — Market Intelligence Layer 模块定义
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md) — 商业 Object 契约
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md) — 表结构

**当前状态：** `2_COGNITION/` 目录为空；本 Blueprint 仅定义 Agent 架构，不创建代码。

---

## 1. Module Position

### 2_COGNITION 在 AI_FACTORY_OS 中的位置

```
1_DATA
    ↓
Database（data/ai_factory.db）
    ↓
2_COGNITION          ← 本 Blueprint
    ↓
3_DECISION
    ↓
11_CONTENT_FACTORY
```

### 定位

**Market Intelligence Layer** — 将市场**事实**转化为**机会情报**，供 Decision 消费。

### 明确边界

| Cognition | 说明 |
|-----------|------|
| **不生产产品** | 不调用 Content Factory、不生成 PPT/PDF/artifact |
| **不执行发布** | 不写入 `output/` 模拟发布、不触发 publish |
| **不替代 Decision** | 不输出 `action: publish/skip` 最终裁决；仅输出 `recommendation` 建议 |

### 与核心 OS 关系

所有 Cognition Agent 经 `0_START` → Planner → PolicyEngine → **ExecutionRuntime** 调度，实现 `BaseAgent.execute(input_data, context)`，**不绕过 Controller**。

---

## 2. Agent Architecture

### 流水线总览

```
Market Signal Object（来自 1_DATA / DB）
        ↓
    ┌───┴───┐
    ↓       ↓       ↓
TrendAgent  DemandAgent  CompetitionAgent
    ↓       ↓       ↓
    └───┬───┘
        ↓
OpportunityAgent
        ↓
InsightAgent
        ↓
Opportunity Object → 3_DECISION
Business Insight Object → 报告 / DB（可选）
```

### TrendAgent

| 项 | 说明 |
|----|------|
| **职责** | 趋势发现 — 识别增长、热点、方向变化 |
| **输入** | Market Signal Object |
| **输出** | Trend Insight Object |

---

### DemandAgent

| 项 | 说明 |
|----|------|
| **职责** | 分析用户需求强度 |
| **输入** | keywords、products、market signals（经 DB / Object） |
| **输出** | Demand Object |

---

### CompetitionAgent

| 项 | 说明 |
|----|------|
| **职责** | 竞争环境分析 |
| **输入** | market_products（及 Legacy `products` 过渡期） |
| **输出** | Competition Object |

---

### OpportunityAgent

| 项 | 说明 |
|----|------|
| **职责** | 综合机会评分 |
| **输入** | Trend Insight + Demand + Competition |
| **输出** | **Opportunity Object**（Commercial Intelligence Contract v1） |

---

### InsightAgent

| 项 | 说明 |
|----|------|
| **职责** | 生成商业洞察报告（人类可读摘要） |
| **输入** | Opportunity Object |
| **输出** | Business Insight Object |

---

## 3. Agent Responsibility Boundary

| Agent | 负责 | 不负责 |
|-------|------|--------|
| **TrendAgent** | 趋势指数、growth 方向、热点识别 | 需求语义、竞争定价、机会综合分 |
| **DemandAgent** | 需求强度、问题频次、search 信号解读 | 趋势预测、竞品数量统计 |
| **CompetitionAgent** | 竞品密度、价格带、饱和度 | 需求理解、最终机会分 |
| **OpportunityAgent** | 机会评分、`recommendation`、写 `opportunity_scores` | 生成商品、修改 Content Factory、直接发布 |
| **InsightAgent** | 可读报告、洞察摘要 | 改变 Opportunity 分数、触发 Decision |

### OpportunityAgent 禁止项（重点）

- ❌ 生成商品（Product Asset）
- ❌ 修改 Content Factory
- ❌ 直接发布
- ❌ 写入 `generated_products` / `product_feedback`
- ❌ 替代 `3_DECISION` 的 accept/reject/prioritize

---

## 4. Input / Output Contract

**权威引用：** [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)

所有 Agent I/O 须携带 `contract_version: "1.0"`。

### TrendAgent

**Input:** Market Signal Object（Contract §3）

**Output — Trend Insight Object（v1）:**

```json
{
  "contract_version": "1.0",
  "object_type": "trend_insight",
  "keyword": "",
  "trend_score": 0.0,
  "growth_rate": 0.0,
  "direction": "rising | stable | falling",
  "hotspot_flags": [],
  "analysis_method": "rule | llm | hybrid",
  "timestamp": "ISO-8601"
}
```

---

### DemandAgent

**Input:** Market Signal Object、DB keywords/products 聚合

**Output — Demand Object（v1）:**

```json
{
  "contract_version": "1.0",
  "object_type": "demand",
  "keyword": "",
  "demand_score": 0.0,
  "search_volume": 0,
  "problem_frequency": 0,
  "engagement_proxy": 0.0,
  "problem_summary": "",
  "timestamp": "ISO-8601"
}
```

---

### CompetitionAgent

**Input:** market_products / products 样本集

**Output — Competition Object（v1）:**

```json
{
  "contract_version": "1.0",
  "object_type": "competition",
  "keyword": "",
  "competition_score": 0.0,
  "competitor_count": 0,
  "price_range": { "min": 0.0, "max": 0.0, "median": 0.0 },
  "saturation_level": "low | medium | high",
  "timestamp": "ISO-8601"
}
```

---

### OpportunityAgent

**Input:** Trend Insight Object + Demand Object + Competition Object

**Output:** **Opportunity Object**（Contract §4 — 标准字段，不得扩展为 Production Request）

---

### InsightAgent

**Input:** Opportunity Object

**Output — Business Insight Object（v1）:**

```json
{
  "contract_version": "1.0",
  "object_type": "business_insight",
  "keyword": "",
  "opportunity_id": null,
  "executive_summary": "",
  "key_findings": [],
  "risks": [],
  "recommended_next_step": "produce | watch | skip",
  "report_markdown": "",
  "timestamp": "ISO-8601"
}
```

**说明：** `recommended_next_step` 为洞察建议，**不等于** Decision 的 `action` 裁决。

---

## 5. Database Mapping

> 读取/写入经 `1_DATA/database.py`；Legacy 表在过渡期可读。Analysis 表为 Blueprint 扩展（Additive，当前未建）。

| Agent | 读取表 | 写入表 |
|-------|--------|--------|
| **TrendAgent** | `market_keywords`（Legacy: `keywords`） | `trend_analysis`（未来 Analysis 表） |
| **DemandAgent** | `market_keywords`, `market_demands`, `market_products`（Legacy: `keywords`, `products`） | `market_demands`（补写分析字段） |
| **CompetitionAgent** | `market_products`（Legacy: `products`） | —（或 `competition_snapshots` 未来扩展表） |
| **OpportunityAgent** | `market_demands`, `market_products`, `trend_analysis` | **`opportunity_scores`** |
| **InsightAgent** | `opportunity_scores` | `business_insights`（未来可选报告表） |

### 未来 Analysis 表（设计目标）

| 表名 | 用途 | 写入 Agent |
|------|------|------------|
| `trend_analysis` | 趋势分析结果持久化 | TrendAgent |
| `business_insights` | 洞察报告存档 | InsightAgent |

**禁止：** Agent 直接 `sqlite3.connect`；禁止写入 Legacy `scores`（Product Performance Score）。

---

## 6. LLM Usage Strategy

| 任务类型 | 示例 | LLM 需求 | 推荐 |
|----------|------|----------|------|
| **规则计算** | 趋势指数、growth_rate 数值聚合 | 不一定需要 LLM | 规则 + SQL 聚合 |
| **统计竞争** | competitor_count、price median | 不需要 LLM | 规则 |
| **语义分析** | 需求理解、problem_summary | **需要 LLM** | DeepSeek（批量）/ GPT（复杂） |
| **机会综合** | opportunity_score 加权 | 可选 LLM 辅助 | 规则为主，LLM 解释 |
| **洞察报告** | executive_summary、report_markdown | **需要 LLM** | GPT / Claude |

### 成本控制

- 所有 LLM 调用经 **ModelBridge**，由 **PolicyEngine** 控制 `llm_cost_budget`
- 默认低成本：DeepSeek；高复杂度：GPT
- Cognition Agent **不得**绕过 PolicyEngine 直接调用 LLM

---

## 7. Memory Interaction

### 2_COGNITION 与 `7_MEMORY` 边界

| 允许 | 禁止 |
|------|------|
| **读取** 历史分析结果（经 DB `opportunity_scores` / `trend_analysis`） | 直接读写 `7_MEMORY/*.json(l)` |
| **写入** analysis feedback 至 DB（非 Memory 文件） | 直接控制 Memory 系统、更新 `runtime_policy` |
| 未来：高阶 pattern **单向**摘要同步至 Memory（经 OS 事件，非 Agent 直写） | 混写 `pattern_memory.json` |

**原则：** Cognition 商业分析资产存 **Database**；OS 运行时学习存 **7_MEMORY** — 物理隔离。

---

## 8. Future Implementation Roadmap

| Phase | 名称 | 内容 | 状态 |
|-------|------|------|------|
| **Phase 1** | Blueprint | COGNITION_BLUEPRINT + **Agent Architecture Blueprint（本文档）** | **Completed** |
| **Phase 2** | Database Connection | Analysis 表 + `opportunity_scores` Additive 建表 | Pending |
| **Phase 3** | Agent Implementation | `2_COGNITION/agents/` 五 Agent + pipeline | Pending |
| **Phase 4** | Decision Integration | Opportunity Object → `3_DECISION` | Pending |
| **Phase 5** | Feedback Learning | Feedback Object → Cognition 权重优化 | Pending |

---

## 9. Relationship With Existing Modules

| 模块 | 角色 | 一句话 |
|------|------|--------|
| **`1_DATA`** | 提供事实 | 采集 Raw → Market Signal → DB |
| **`2_COGNITION`** | 解释事实 | 分析 → Opportunity + Insight |
| **`3_DECISION`** | 做商业决策 | accept / reject / prioritize → Production Request |
| **`11_CONTENT_FACTORY`** | 执行生产 | Product Asset → artifact |
| **`7_MEMORY`** | OS 运行学习 | 与 Cognition DB 隔离 |
| **`0_START`** | 调度控制 | 统一入口，Cognition 不自治 |

```
事实（1_DATA）→ 解释（2_COGNITION）→ 决策（3_DECISION）→ 生产（11_CONTENT_FACTORY）
```

---

## 10. Agent Directory Design（未来，当前不创建）

```
2_COGNITION/                    ← 未来建设
├── agents/
│   ├── trend_agent.py
│   ├── demand_agent.py
│   ├── competition_agent.py
│   ├── opportunity_agent.py
│   └── insight_agent.py
├── pipeline/
│   └── cognition_pipeline.py
└── __init__.py
```

**接口：** 均实现 `BaseAgent.execute(input_data, context)`，由 ExecutionRuntime 注册调度。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Cognition 模块 Blueprint | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md` |
| Commercial Intelligence Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md` |
| Database Integration | `docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md` |
| Module Registry | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
