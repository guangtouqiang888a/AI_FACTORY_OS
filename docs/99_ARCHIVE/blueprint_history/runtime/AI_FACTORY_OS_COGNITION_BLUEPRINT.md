# AI_FACTORY_OS Cognition Layer Blueprint v1

> 设计层文档 | 最后更新：2026-07-07  
> **状态：Blueprint Completed — 仅架构设计，无运行代码，不参与当前执行**

---

## 1. Module Definition

### 模块

**`2_COGNITION`**

### 名称

**Market Intelligence Layer**（市场智能层）

### 定位

AI Factory OS 的**市场认知系统**。

### 核心目标

让系统从：

**「能够生产数字产品」**

升级为：

**「知道应该生产什么数字产品」**

### 职责边界说明

**2_COGNITION 不负责：**

- 产品生产
- 产品发布
- 最终决策执行

**2_COGNITION 负责：**

- 市场理解
- 机会发现
- 趋势分析
- 商业信息整理

---

# 2. Architecture Position

## 系统位置

```
External Market Data
        ↓
1_DATA
        ↓
2_COGNITION
        ↓
3_DECISION
        ↓
11_CONTENT_FACTORY
        ↓
10_DEPLOY
        ↓
Feedback
        ↓
7_MEMORY
```

## 说明

**2_COGNITION** 是 **Data 与 Decision 之间的智能转换层**。

- 上游：`1_DATA` 提供事实数据与市场原始信号
- 下游：`3_DECISION` 接收 Opportunity Intelligence，决定是否生产、优先级与风险控制
- 不绕过核心 OS：所有执行任务仍经 `0_START` → Planner → PolicyEngine → ExecutionRuntime 调度

**当前状态：** 目录 `2_COGNITION/` 为空，Blueprint 已完成，等待 Phase 2 实现。

---

# 3. Responsibility Boundary

明确各模块边界，禁止职责重叠。

## 1_DATA

**负责：**

- 数据采集
- 数据清洗
- 数据存储

**不负责：**

- 商业判断

---

## 2_COGNITION

**负责：**

- 市场理解
- 趋势识别
- 机会发现

**输出：**

**Opportunity Intelligence**（机会情报对象）

**不负责：**

- 是否生产的最终裁决（交给 `3_DECISION`）
- 数字资产生成（交给 `11_CONTENT_FACTORY`）

---

## 3_DECISION

**负责：**

根据机会结果决定：

- 是否生产
- 优先级
- 风险控制

**输入：** `2_COGNITION` 输出的 Opportunity Object

**不负责：**

- 市场数据采集
- 趋势原始分析

---

## 11_CONTENT_FACTORY

**负责：**

生产数字资产（PPT / Excel / Word / PDF 等）。

**不负责：**

- 自行判断市场方向（应由 `2_COGNITION` + `3_DECISION` 输入生产指令）

---

# 4. Intelligence Pipeline

## 未来流程设计

```
External Data Sources
        ↓
Data Storage
        ↓
Cognition Analysis
        ↓
Opportunity Discovery
        ↓
Decision Input
```

## External Data Sources

包括：

- 搜索趋势
- 电商平台
- 内容平台
- 用户反馈
- 销售数据

## 各阶段说明

| 阶段 | 负责层 | 产出 |
|------|--------|------|
| External Data Sources | 外部 + `1_DATA` 采集 | 原始市场信号 |
| Data Storage | `1_DATA` / `data/ai_factory.db` | 结构化事实数据 |
| Cognition Analysis | `2_COGNITION` | 趋势报告、需求分析、竞争图谱 |
| Opportunity Discovery | `2_COGNITION` | Product Opportunity Candidate |
| Decision Input | → `3_DECISION` | 生产/观望/放弃建议 |

---

# 5. Core Intelligence Components

> 以下组件**仅设计，不实现**。未来建设时每个组件职责单一，禁止重叠。

## Trend Intelligence

**职责：** 发现增长趋势、新需求、热点变化。

| 项 | 说明 |
|----|------|
| **输入** | market data |
| **输出** | trend report |

---

## Demand Intelligence

**职责：** 分析用户需求强度。

**指标：**

- search volume
- engagement
- problem frequency

---

## Competition Intelligence

**职责：** 分析市场竞争。

**指标：**

- competitor count
- pricing
- saturation

---

## Opportunity Discovery Engine

**职责：** 综合需求、趋势、竞争、利润，生成 **Product Opportunity Candidate**。

**输入：** Trend Intelligence + Demand Intelligence + Competition Intelligence

**输出：** 带评分的 Opportunity Object → `3_DECISION`

---

# 6. Opportunity Scoring Model

## 重要区分

| 类型 | 用途 | 负责层 |
|------|------|--------|
| **市场机会评分** | 是否进入生产流程 | `2_COGNITION` |
| **产品质量评分** | 已生产内容是否合格 | `11_CONTENT_FACTORY` / QualityAgent |

二者不得混用。

## 市场机会评分维度

- **Demand Score** — 需求强度
- **Trend Score** — 趋势方向
- **Competition Score** — 竞争程度（越低越好则取反或单独加权）
- **Profit Score** — 利润空间
- **Difficulty Score** — 生产难度（辅助参考，可选纳入）

## 示例公式

```
Opportunity Score =
    Demand   × 30%
  + Trend    × 25%
  + Profit   × 25%
  + Competition × 20%
```

**说明：** 该评分用于判断是否进入生产流程，由 `3_DECISION` 消费并做最终裁决。

---

# 7. Database Relationship

## 未来数据库关系

基于现有 **`data/ai_factory.db`**，未来可能扩展以下表（设计目标，当前未建）：

| 表名 | 用途 |
|------|------|
| `market_keywords` | 保存关键词趋势 |
| `market_products` | 保存市场产品样本 |
| `market_competition` | 保存竞争信息 |
| `opportunity_scores` | 保存机会评分历史 |
| `product_feedback` | 保存销售反馈 |

## 原则

- 数据库是**长期市场资产**，与 `7_MEMORY` 运行记忆层物理隔离
- `1_DATA` 负责写入事实层
- `2_COGNITION` 负责读取分析并写入 opportunity 相关表
- 销售反馈经 Feedback 闭环回写 `product_feedback`，反哺下一轮 Cognition

---

# 8. Interface With Existing Modules

## 1_DATA 输出：Market Data Object

```json
{
  "keyword": "",
  "source": "",
  "trend": "",
  "timestamp": ""
}
```

**消费方：** `2_COGNITION`

---

## 2_COGNITION 输出：Opportunity Object

```json
{
  "product_idea": "",
  "demand_score": "",
  "competition_score": "",
  "opportunity_score": "",
  "recommendation": ""
}
```

**消费方：** `3_DECISION`

---

## 接口原则

- 标准 JSON 对象，经 OS 协议传递
- 不直接跨层调用 Python 模块内部函数
- 经 `controller.run()` 与 DAG 节点调度

---

# 9. Future Agent Design

> 只定义职责，**禁止 Agent 职责重叠**。

| Agent | 职责 | 禁止 |
|-------|------|------|
| **Market Analyst Agent** | 综合市场数据解读 | 不生成产品文件 |
| **Trend Analyst Agent** | 趋势识别与报告 | 不做最终生产决策 |
| **Competition Analyst Agent** | 竞争格局分析 | 不采集原始数据 |
| **Opportunity Research Agent** | 机会候选生成与初评 | 不执行 Content Factory 生产 |
| **Report Generator Agent** | 输出可读市场分析报告 | 不写入 Decision 策略 |

所有 Agent 实现标准 `BaseAgent.execute(input_data, context)`，由 ExecutionRuntime 统一调度。

---

# 10. Commercial Value

## 2_COGNITION 未来价值

### 内部价值

提升产品成功率 — 在投入 Content Factory 生产前，先验证市场机会。

### 外部价值（未来可能商业化）

- Market Intelligence API
- AI 选品服务
- 行业分析报告
- SaaS 市场洞察模块

**当前阶段：** 仅 Blueprint，不启动外部商业化。

---

# 11. Implementation Roadmap

| Phase | 名称 | 内容 | 状态 |
|-------|------|------|------|
| **Phase 1** | Blueprint | 架构设计、职责边界、接口定义 | **Completed** |
| **Phase 2** | Database Enhancement | 扩展 `ai_factory.db` 市场相关表 | Pending |
| **Phase 3** | Data Collection Expansion | 扩展 `1_DATA` 数据源与清洗 | Pending |
| **Phase 4** | Intelligence Engine | 实现 Trend / Demand / Competition / Opportunity 组件 | Pending |
| **Phase 5** | Connection With Content Factory | 接通 Data → Cognition → Decision → Content Factory 闭环 | Pending |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| 模块注册表 | `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` |
| Data Intelligence 蓝图 | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_DATA_INTELLIGENCE_BLUEPRINT.md` |
| 工程进度 | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` |
| 系统快照 | `docs/01_CURRENT_STATE/reference/system_snapshot.md` |
| 工作准则 | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` |
