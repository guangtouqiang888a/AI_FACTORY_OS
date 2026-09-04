# AI Factory OS — Content Factory Blueprint

> 设计层文档 | 最后更新：2026-07-07  
> **状态：设计阶段 — 未创建代码，未创建 Agent**

---

# 1. Content Factory 战略定位

AI Factory OS 未来不是单纯自动生成内容的工具。

**目标：建立 AI 数字资产生产系统。**

Content Factory 是 AI Factory OS 之上的**生产制造层**，负责将市场信号转化为可销售的数字产品，并在销售反馈中持续优化。

## 完整商业闭环

```
市场发现
    ↓
需求分析
    ↓
产品规划
    ↓
内容生产
    ↓
质量检测
    ↓
商品包装
    ↓
发布辅助
    ↓
销售反馈
    ↓
Memory 学习优化
```

## 战略边界

- Content Factory **不替代** AI Factory OS 核心决策与执行控制
- Content Factory **不直接** 修改 Planner / PolicyEngine / ExecutionRuntime
- 所有生产任务必须经核心 OS 调度，经 Memory 闭环学习

---

# 2. 商业目标

## 当前第一阶段：Content Factory

第一阶段聚焦：**数字虚拟产品的自动化生产与半自动销售辅助**。

Content Factory 不是 AI Factory OS 的唯一盈利方向，而是当前最高优先级的产品化路径。

## 未来可能扩展方向

| 方向 | 说明 |
|------|------|
| SaaS 服务 | 模块化订阅，按功能/用量收费 |
| API 服务 | 对外提供决策、选品、内容生成能力 |
| Agent 服务 | 独立 Agent 能力打包出售 |
| 企业 AI 解决方案 | 私有部署 + 定制策略 |
| 数字资产交易 | 自产数字产品直接销售 |

## 商业路线动态评估原则

1. **可落地优先** — 优先选择 30 天内可验证盈利的方向
2. **风险可控** — 平台规则、合规、成本必须在设计阶段评估
3. **与 OS 能力对齐** — 新商业方向必须能接入现有 Planner → Execution → Memory 链
4. **定期复盘** — 每完成一个阶段，对照 `docs/99_ARCHIVE/AI_FACTORY_OS_BUSINESS_PLAN.md` 重新评估优先级
5. **不绑定单一模式** — Content Factory 是起点，不是终点；架构需预留扩展至 SaaS / API / 企业版的空间

---

# 3. 第一阶段产品方向

## 优先级分级

### A 级：数字模板产品（最高优先级）

| 类型 | 示例 |
|------|------|
| PPT 模板 | 商务汇报、行业专题、数据可视化 |
| Excel 模板 | 财务模型、项目管理、数据分析 |
| Notion 模板 | 知识库、任务管理、CRM |
| 工作流模板 | 自动化流程、SOP 文档 |

**选择理由：**

| 维度 | 评估 |
|------|------|
| 生产成本 | 低 — AI 可批量生成结构化模板，人工微调即可 |
| 销售难度 | 中低 — 闲鱼、小红书、独立站均有成熟市场 |
| 利润空间 | 中高 — 单价 9–99 元，边际成本趋近于零 |
| AI 适配程度 | 高 — 结构化输出，质量可量化检测 |

### B 级：AI 效率产品

| 类型 | 示例 |
|------|------|
| Prompt 合集 | 行业专用 Prompt 包 |
| AI 工作流 | 可复用的 AI 自动化流程 |
| AI 工具包 | 脚本 + 模板 + 使用说明组合 |

**选择理由：**

| 维度 | 评估 |
|------|------|
| 生产成本 | 低 — 以文本和配置为主 |
| 销售难度 | 中 — 需教育市场，竞争较 A 级更激烈 |
| 利润空间 | 中 — 单价偏低，靠量取胜 |
| AI 适配程度 | 极高 — 原生 AI 产物 |

### C 级：知识产品

| 类型 | 示例 |
|------|------|
| 教程 | 工具使用、行业入门 |
| 行业指南 | 垂直领域方法论 |

**选择理由：**

| 维度 | 评估 |
|------|------|
| 生产成本 | 中高 — 需深度内容，质量要求高 |
| 销售难度 | 高 — 信任建立周期长 |
| 利润空间 | 中高 — 单价可更高，但转化慢 |
| AI 适配程度 | 中 — AI 可辅助，但需大量人工审核 |

## 第一阶段建议

**从 A 级数字模板产品切入**，以 PPT / Excel 模板验证完整生产闭环，再扩展至 B、C 级。

---

# 4. Content Factory 未来架构设计

## 未来目录（当前不创建）

```
11_CONTENT_FACTORY/          ← 生产制造层（设计目标，未建设）
├── market_agent/            ← 需求发现
├── product_agent/           ← 产品设计
├── creator_agent/           ← 内容生产
├── quality_agent/           ← 质量检测
├── packaging_agent/         ← 商品包装
├── publish_agent/           ← 发布辅助
└── feedback_agent/          ← 反馈分析
```

## Agent 职责定义

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| `market_agent` | 需求发现 | 关键词、平台数据、趋势信号 | 机会清单、需求评分 |
| `product_agent` | 产品设计 | 机会清单 | 产品规格、内容大纲 |
| `creator_agent` | 内容生产 | 产品规格 | 原始内容资产（文件/文本） |
| `quality_agent` | 质量检测 | 原始内容 | 质量评分、修改建议 |
| `packaging_agent` | 商品包装 | 合格内容 | 标题、描述、封面、定价建议 |
| `publish_agent` | 发布辅助 | 包装完成商品 | 发布清单、平台适配说明 |
| `feedback_agent` | 反馈分析 | 销售数据、用户评价 | 优化建议、模式提取 |

## 设计原则

- 每个 Agent 实现标准 `BaseAgent.execute(input_data, context)` 接口
- 由 ExecutionRuntime 统一调度，不独立运行
- 当前阶段**仅文档设计**，不创建任何代码或目录

---

# 5. 与 AI Factory OS 核心连接方式

Content Factory **不直接控制核心 OS**。

## 执行链

```
Planner
    ↓
PolicyEngine
    ↓
ExecutionRuntime
    ↓
Content Agent（11_CONTENT_FACTORY 内 Agent）
    ↓
Memory
```

## 连接规则

| 规则 | 说明 |
|------|------|
| 统一入口 | 所有 Content Factory 任务经 `controller.run()` 触发 |
| DAG 扩展 | Planner 将 Content 任务拆解为标准 DAG 节点 |
| 策略管控 | PolicyEngine 决定使用哪个 LLM、成本上限、是否批准执行 |
| 执行隔离 | ExecutionRuntime 调用 Content Agent，Agent 不绕过 Runtime |
| 记忆闭环 | 执行结果写入 Memory，驱动 pattern / strategy 更新 |

## 禁止行为

- Content Agent 直接调用 `policy_engine` 或 `execution_runtime`
- Content Factory 模块独立启动，绕过 Controller
- 在 Content Factory 内重复实现 Planner / Router / Governor 逻辑

---

# 6. Memory 闭环设计

## 未来数据流

```
产品（生产结果）
    ↓
销售结果（反馈数据）
    ↓
成功模式（pattern 提取）
    ↓
策略优化（strategy 更新）
```

## 现有 Memory 层级扩展

```
event_log.jsonl        ← 事实层（生产事件、发布事件、销售事件）
    ↓
pattern_memory.json    ← 模式层（成功产品特征、高转化模式）
    ↓
strategy_memory.json   ← 策略层（选品权重、定价策略、内容风格偏好）
```

## 未来扩展：`product_pattern`

| 字段 | 说明 |
|------|------|
| `product_type` | 模板类型（PPT / Excel / Notion 等） |
| `keyword` | 关联关键词 |
| `quality_score` | 质量评分 |
| `sales_count` | 销售数量 |
| `conversion_rate` | 转化率 |
| `profit_margin` | 利润率 |
| `confidence` | 模式置信度 |

**设计原则：** `product_pattern` 作为 `pattern_memory.json` 的扩展类型，不新建独立 Memory 文件，保持 Memory 架构简洁。

---

# 7. 发布策略设计

## 核心原则：半自动发布辅助模式

**禁止设计高风险自动化刷平台行为。**

| 禁止 | 允许 |
|------|------|
| 批量无行为模拟登录 | AI 生成发布内容 |
| 绕过平台验证码 / 风控 | 人工确认后辅助发布 |
| 多账号轮换自动上架 | 发布清单 + 步骤说明生成 |
| 伪造用户行为轨迹 | 影刀 / RPA 辅助（人工监督） |

## 标准发布流程

```
AI 生成内容与包装
    ↓
quality_agent 质量检测
    ↓
人工确认节点（Human-in-the-loop）
    ↓
publish_agent 生成发布清单
    ↓
工具辅助发布（影刀 / RPA / 手动）
    ↓
feedback_agent 收集销售反馈
    ↓
Memory 学习优化
```

## 未来可研究方向

- 平台官方 API（合规接口）
- 平台合作接口（企业级）
- 合规自动化（需法务与平台规则双重评估）

**当前阶段：** 仅记录设计原则，不实现任何发布自动化代码。

---

# 8. AI 模型和工具规划

## LLM 接入规划

| 模型 | 成本 | 优势 | 适用场景 |
|------|------|------|----------|
| **DeepSeek** | 低 | 中文理解好、响应快、成本低 | 内容生成、模板填充、批量文本 |
| **OpenAI (GPT)** | 高 | 推理强、规划能力好、工具调用成熟 | 产品规划、复杂决策、质量评估 |
| **Claude** | 中高 | 长文本、安全对齐好 | 教程撰写、行业指南 |
| **Gemini** | 中 | 多模态、视觉理解 | 封面设计辅助、视觉模板 |

## 任务 — 模型映射（设计目标）

| 任务类型 | 推荐模型 | 原因 |
|----------|----------|------|
| 市场关键词分析 | DeepSeek | 低成本高频调用 |
| 产品规格规划 | GPT | 需要复杂推理 |
| 模板内容生成 | DeepSeek | 结构化输出，成本敏感 |
| 质量评分 | GPT / DeepSeek | 规则 + LLM 混合 |
| 封面 / 视觉 | Gemini / DALL·E | 视觉任务专用 |
| 销售反馈分析 | DeepSeek | 批量文本分析 |

## 成本控制原则

- 所有 LLM 调用经 `ModelBridge`，caller 必须为 `ExecutionRuntime`
- PolicyEngine 控制单次 session 成本上限（`llm_cost_budget`）
- 低成本任务默认 DeepSeek，高复杂度任务升级 GPT
- Content Factory 不得绕过 PolicyEngine 直接调用 LLM

---

# 9. 与 9_PRODUCT 和 10_DEPLOY 关系

## 三层架构关系

```
Content Factory（11_CONTENT_FACTORY）
    ↓  生产数字产品 / 提供 Agent 能力
9_PRODUCT
    ↓  商业产品化（用户 / 权限 / 计费 / 套餐）
10_DEPLOY
    ↓  部署访问（API / 服务 / 监控）
外部用户 / 客户
```

## 各层职责

| 层 | 目录 | 职责 |
|----|------|------|
| **Content Factory** | `11_CONTENT_FACTORY/`（未来） | 生产制造 — Agent 执行内容生产全流程 |
| **9_PRODUCT** | `9_PRODUCT/` | 商业产品化 — 用户管理、权限、计费、套餐 |
| **10_DEPLOY** | `10_DEPLOY/` | 部署访问 — FastAPI、HTTP 服务、Docker、监控 |

## 数据流向

```
用户请求
    → 10_DEPLOY（API 接入 + 鉴权）
    → 9_PRODUCT（套餐校验 + 计费）
    → controller.run()（核心 OS）
    → 11_CONTENT_FACTORY Agent（生产执行）
    → Memory（学习闭环）
    → 10_DEPLOY（统一响应返回）
```

**当前状态：** 9_PRODUCT 与 10_DEPLOY 已有基础结构；11_CONTENT_FACTORY 仅为设计目标，未创建。

---

# 10. 当前建设阶段

| 项目 | 状态 |
|------|------|
| **Current Stage** | Content Factory Blueprint Design |
| **阶段性质** | 设计阶段 |
| **代码状态** | 未创建代码 |
| **Agent 状态** | 未创建 Agent |
| **核心 OS** | 冻结 — 0_START ~ 10_DEPLOY 保持不变 |

## 下一阶段

**11_CONTENT_FACTORY Construction**

建设顺序建议：

1. `creator_agent` — 验证最小生产闭环（A 级模板）
2. `quality_agent` — 建立质量检测标准
3. `packaging_agent` — 商品包装自动化
4. `market_agent` + `product_agent` — 需求发现与产品设计
5. `publish_agent` + `feedback_agent` — 发布辅助与反馈闭环

## 相关文档

| 文档 | 路径 |
|------|------|
| 商业规划 | `docs/99_ARCHIVE/AI_FACTORY_OS_BUSINESS_PLAN.md` |
| 工作准则 | `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` |
| 工程进度 | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` |
| 系统快照 | `docs/01_CURRENT_STATE/reference/system_snapshot.md` |
| 本文档 | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_BLUEPRINT.md` |
