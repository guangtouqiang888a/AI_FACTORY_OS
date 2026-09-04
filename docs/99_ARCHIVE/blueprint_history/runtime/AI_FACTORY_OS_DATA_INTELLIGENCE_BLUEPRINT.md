# AI Factory OS Data Intelligence Blueprint

> 项目战略设计层 | 最后更新：2026-07-07  
> **状态：设计规划阶段 — 未开始代码建设，不参与任何运行逻辑**

---

## 1. 战略定位

AI Factory OS 未来不是单纯内容生成系统。

**战略定位：数据资产驱动的 AI 商业生产系统。**

系统价值不在于「生成一份内容」，而在于：**用数据驱动选品、生产、销售与优化的完整商业闭环**。

### 核心闭环

```
市场数据
    ↓
数据资产
    ↓
AI 市场分析
    ↓
产品机会评分
    ↓
Content Factory 生产
    ↓
销售反馈
    ↓
数据沉淀
    ↓
（持续优化循环）
```

每一次销售结果都会反哺数据资产，使下一次选品与生产决策更准确。

---

## 2. Data Intelligence Layer 定位

**Data Intelligence Layer（数据智能层）** 由以下能力组成：

- 数据采集
- 数据存储
- 市场分析
- 产品机会判断

### 架构位置

```
1_DATA（事实数据层）
    ↓
Data Intelligence Layer（智能分析层）  ← 未来建设
    ↓
11_CONTENT_FACTORY（商品生产层）
```

### 逻辑链路

```
事实数据
    ↓
智能分析
    ↓
生产决策
    ↓
商品生产
```

**边界：** Data Intelligence Layer 负责「该不该做、做什么」，Content Factory 负责「怎么做、交付什么」。

---

## 3. 模块职责划分

### Data Collector

**职责：** 采集市场事实数据。

**例如：**

- 搜索趋势
- 平台热度
- 用户需求信号
- 竞争信息

**禁止：** 直接生产商品。

---

### Database

**职责：** 长期保存数据资产。

**例如：**

- 关键词数据
- 市场趋势
- 产品历史
- 销售反馈

**禁止：** 参与执行决策。

---

### Market Intelligence Engine

**职责：** 分析数据，输出洞察。

**输出：**

- 市场机会
- 用户需求画像
- 产品方向建议

**禁止：** 直接生成商品。

---

### Opportunity Scoring

**职责：** 评估是否值得生产。

**参考维度：**

| 维度 | 说明 |
|------|------|
| 需求强度 | 搜索量、讨论热度、购买意愿 |
| 竞争程度 | 同类商品数量、差异化空间 |
| 利润空间 | 定价区间、边际成本 |
| 生产成本 | AI 生产复杂度、人工介入比例 |
| 趋势变化 | 上升/平稳/下降 |

**输出：** 机会评分 + 生产建议（生产 / 观望 / 放弃）

---

### Content Factory

**职责：** 根据已确定的机会生产商品。

**当前状态：** `11_CONTENT_FACTORY/` 已建设，可生成真实 PPTX / XLSX / DOCX / PDF 及 `final_product.zip`。

**禁止：** 自行判断市场方向（应由 Data Intelligence Layer 输入机会评分）。

---

## 4. 与现有架构关系

### 当前 AI Factory OS

**核心 OS（冻结）：**

```
Planner
    ↓
PolicyEngine
    ↓
ExecutionRuntime
    ↓
Memory
```

**业务生产层（已建设）：**

```
11_CONTENT_FACTORY
```

### 未来完整架构

```
Data Intelligence Layer
    ↓  （机会评分 + 生产指令）
Content Factory
    ↓  （真实数字商品）
9_PRODUCT → 10_DEPLOY
    ↓
销售反馈 → 数据沉淀 → Data Intelligence Layer
```

**原则：** Data Intelligence 不替代核心 OS；核心 OS 仍负责 Planner → Execution → Memory 的执行控制。

---

## 5. 数据资产战略

长期积累的数据可能成为 AI Factory OS 的**核心竞争资产**。

### 数据资产价值

| 价值 | 说明 |
|------|------|
| 提高选品准确率 | 历史成功模式指导新品类选择 |
| 优化生产方向 | 高转化产品特征驱动 Content Factory 模板策略 |
| 形成行业知识库 | 垂直领域需求、定价、竞争图谱 |
| 支持 SaaS/API 商业化 | 市场洞察、选品评分作为独立产品出售 |

### 与 7_MEMORY 的关系

| 层 | 职责 |
|----|------|
| `7_MEMORY/` | OS 运行时学习（event → pattern → strategy） |
| Data Intelligence Database | 商业数据资产（市场、销售、反馈） |

两者物理隔离，未来可单向同步（销售反馈 → Memory + Data Intelligence）。

---

## 6. 未来商业路线

### 当前主路线

**数字商品生产与销售验证** — 以 Content Factory 真实交付闭环为主。

### 未来扩展路线（当前阶段不扩展）

| 路线 | 说明 |
|------|------|
| 路线 1 | AI 自动商品生产（Content Factory 全自动化） |
| 路线 2 | 市场分析服务（Data Intelligence 独立产品） |
| 路线 3 | 选品智能 API（Opportunity Scoring 对外输出） |
| 路线 4 | SaaS 化 AI 商业工具（9_PRODUCT 模块化订阅） |

**当前优先级：** 数字商品生产闭环验证 > 数据智能增强 > 服务化/SaaS/API。

---

## 7. 当前阶段

| 项目 | 状态 |
|------|------|
| **Data Intelligence Layer** | 设计规划阶段 |
| **代码建设** | 未开始 |
| **Content Factory** | 已建设（真实文件生产） |
| **核心 OS** | 冻结（0_START ~ 10_DEPLOY） |

---

## 8. 架构原则

必须保留以下边界：

| 原则 | 说明 |
|------|------|
| 数据层 ≠ 生产层 | Database 存事实，Content Factory 产商品 |
| 分析层 ≠ 执行层 | Market Intelligence 出洞察，ExecutionRuntime 做执行 |
| Content Factory ≠ Market Intelligence | 生产不自行判断市场方向 |

**模块职责单一** — 每层只做一件事，通过标准接口衔接。

---

## 相关文档

| 文档 | 路径 |
|------|------|
| 商业规划 | `docs/99_ARCHIVE/AI_FACTORY_OS_BUSINESS_PLAN.md` |
| Content Factory 蓝图 | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_BLUEPRINT.md` |
| 工程进度 | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` |
| 系统快照 | `docs/01_CURRENT_STATE/reference/system_snapshot.md` |
