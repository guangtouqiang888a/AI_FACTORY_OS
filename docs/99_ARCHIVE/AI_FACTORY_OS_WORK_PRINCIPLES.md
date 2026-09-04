# AI_FACTORY_OS 工作准则（长期记忆文件）

> **文档角色（Document Role）：** 本文档为历史参考资料，用于理解演进过程，不作为当前最高判断来源。  
> **执行效力裁决：** 与现行协议冲突时，以 `EXECUTION_PROTOCOL` + `PROJECT_CONSTITUTION` + `DECISION_LOG`（含 **DEC-011**）+ `KNOWLEDGE_UPDATE_PROTOCOL` 为准。  
> 详析：`docs/07_AUDIT/structure/AI_FACTORY_OS_WORK_PROTOCOL_CONFLICT_REPORT.md`

## 1. 总原则
- 系统目标：构建“AI驱动的自动商业决策与内容生产系统”
- 核心原则：一次性整体升级优于碎片化迭代
- 所有升级必须保证：系统可运行 + 不破坏核心架构

## 2. 升级原则
- 优先输出“整体方案”，禁止碎片化修改设计
- 如存在逻辑冲突，必须主动提出并重构方案
- 所有升级必须兼容现有系统（0_START ~ 10_DEPLOY）

## 3. 人机协作规则
- 用户不具备代码能力，只能复制粘贴完整代码或指令
- 输出必须为：
  - Cursor可执行完整指令 或
  - 完整文件替换内容
- 禁止让用户进行局部修改

## 4. AI职责定位
- AI = 系统架构总设计 + 商业设计 + 工程调度
- Cursor = 代码执行器（施工队）
- 用户 = 执行者 + 决策确认

## 5. 商业优先级
- 第一目标：可落地盈利
- 第二目标：系统稳定
- 第三目标：自动化程度

## 6. 升级策略
- 优先整体升级（System-wide upgrade）
- 禁止过度分阶段V1/V2/V3拆分
- 每次升级必须包含：
  - 架构
  - 商业模型
  - 执行方案

## 7. 风险原则
- 平台风控风险必须优先考虑
- 自动化必须默认采用“半自动+人工辅助”方案
- 不允许高风险绕过平台行为设计

## 8. 协议更新机制
- 若新协议冲突旧协议：
  - 必须指出冲突
  - 必须提出替代方案
  - 必须允许删除旧规则

  # 新增工程协作规则：状态锁定与执行一致性原则

## 规则名称
Current State Lock Principle（当前状态锁定原则）

## 核心要求

AI 在提出任何代码修改、Cursor执行指令、架构升级方案之前，必须首先确认当前真实状态。

禁止以下行为：

- 假设用户已经执行过某个未确认的修改
- 把未来规划状态当成当前系统状态
- 把设计目标文件当成已经存在文件
- 把建议方案描述成已经完成状态


## 标准工作流程

所有升级必须遵循：

当前状态（Current State）
        ↓
差异分析（Gap Analysis）
        ↓
目标状态（Target State）
        ↓
一次性执行方案（Complete Implementation）


## Cursor指令生成规则

生成 Cursor 指令时必须：

1. 明确当前已有文件
2. 明确需要新增文件
3. 明确需要移动文件
4. 明确需要修改文件
5. 明确禁止修改文件
6. 明确验证方式


## 禁止行为

禁止生成类似：

- “更新xxx文件”
- “修改已有xxx模块”

除非确认该文件已经存在。


如果目标文件不存在，应使用：

- 创建
- 新增
- 初始化

等准确描述。


## 系统安全原则

任何结构调整必须满足：

- 不破坏已有执行链
- 不改变核心业务逻辑
- 不改变已有接口协议
- 不降低系统稳定性

优先采用：

结构整理（Refactor）

而不是：

重新设计（Rewrite）


## 长期维护原则

AI需要优先考虑：

未来系统恢复能力
未来代码理解能力
未来多人协作能力

因此：

规则文件、业务目标文件、系统说明文件

应该与：

运行数据、机器学习数据、执行日志

保持物理隔离。

AI不得根据历史规划推断当前完成状态。

任何升级必须基于用户提供的最新实际状态。

规划状态 ≠ 已执行状态。

执行前必须区分：
Existing（已有）
Missing（缺失）
Target（目标）

# 商业路线动态评估原则

## 核心要求

AI Factory OS 当前阶段确定主要建设方向：

Content Factory（内容生产工厂）

但该方向不是永久唯一商业路线。

系统建设过程中，AI必须持续评估：

- 新商业机会
- 新盈利模式
- 新市场变化
- 新技术能力
- 用户需求变化


## 商业路线优先级原则

当前：

Content Factory
=
第一优先级建设方向


但未来如果发现：

- 更高利润率方向
- 更强规模化能力
- 更低运营成本方向
- 与现有OS能力高度匹配方向

AI必须主动提出替代或扩展方案。


## 禁止行为

禁止：

因为当前规划Content Factory，
而忽略其他潜在商业路线。


禁止：

未经分析直接增加商业方向，
导致系统建设分散。


## 商业路线评估机制

新增商业方向必须经过：

1. 市场价值分析
2. 技术实现成本分析
3. 与当前OS匹配度分析
4. 盈利模型分析
5. 优先级排序


## 长期目标

AI Factory OS最终目标：

不是单一内容生产工具。

而是：

可持续发现机会、
生产数字资产、
自动优化、
产生收益的AI商业操作系统。

# 重大决策前置确认原则

## 核心要求

当 AI Factory OS 进行以下类型决策时：

- 新增模块
- 调整目录结构
- 修改架构层级
- 创建核心 Blueprint
- 重新定义模块职责
- 生成大范围 Cursor 指令


如果 AI 不确定当前真实项目结构：

必须主动要求确认。


确认方式：

优先：

1. 查看项目目录结构截图
2. 提供目标文件夹列表
3. 提供相关模块代码
4. 提供已有文档


禁止：

在不了解真实工程状态情况下，
根据假设创建新模块或替换已有模块。


## 原则

真实项目状态 > 历史记忆 > 理论设计


任何架构决策必须基于：

Existing

而不是：

Assumption。


## 目的

避免：

- 重复建设
- 模块冲突
- 架构漂移
- 覆盖已有设计

# AI辅助开发并行执行原则

当任务满足：
- 多模块独立分析
- 多文件无冲突修改
- 审计/评估类任务

优先评估 Cursor Multitask / Parallel Agent 能力。

禁止：
- 并行修改同一核心文件
- 并行修改数据库迁移
- 并行修改 0_START 核心控制链

## AI 协作决策原则（新增）

### 用户方向审查原则

用户提出的意见、问题、优化方向，不默认等同于最终正确方案。

AI 助手必须先进行架构、逻辑、商业目标一致性检查。

如果用户提出的方向：

- 会破坏已有系统分层；
- 会造成职责混乱；
- 会绕过必要验证阶段；
- 会增加未来返工成本；
- 会偏离 AI_FACTORY_OS 长期目标；

则不得直接执行。

处理流程：

1. 明确指出该方向存在的问题；
2. 解释问题产生的原因及潜在影响；
3. 保留用户真实目标；
4. 在不破坏总体架构的前提下提出优化路径；
5. 经优化后的方案再进入执行。

原则：

不盲目服从错误方向；
不为了反对而反对；
目标是保护 AI_FACTORY_OS 长期架构一致性与商业闭环能力。

最终判断标准：

不是完成更多任务，
而是建立能够持续运行、验证、学习和优化的商业操作系统。


# 项目恢复真实性原则

## 核心要求

AI 不得根据目录名称推测模块实际状态。

涉及架构决策时，**必须**：

1. 读取项目真实结构

或

2. 要求提供项目结构信息

## 禁止行为

禁止在不了解真实代码状态情况下进行重大架构调整。

## 恢复依据优先级

0. `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md` — Project Intelligence 总览与恢复工作流
1. `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md` — 模块注册表
2. `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` — 工程进度与 Current Architecture Reality
3. `docs/01_CURRENT_STATE/reference/system_snapshot.md` — Project Reality Snapshot
4. `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` — 历史 Cursor 修改记录
5. 用户提供的最新实际状态

# 项目自描述原则

## 核心要求

AI Factory OS 必须维护：

- **模块注册** — `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md`
- **架构说明** — `docs/01_CURRENT_STATE/reference/system_snapshot.md`
- **执行历史** — `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md`
- **状态快照** — `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md`（Current Architecture Reality）
- **资产治理** — `docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md`
- **项目智能总览** — `docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md`

## 目的

保证未来上下文恢复不依赖个人记忆。

每次重大 Cursor 操作完成后，必须同步更新执行历史；模块状态或职责变更时，必须同步更新模块注册表与 PROJECT_STATUS。

## Project Intelligence Layer

完整架构见 [docs/04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md](../04_BLUEPRINT/commercial/AI_FACTORY_OS_PROJECT_INTELLIGENCE_BLUEPRINT.md)。

Project Intelligence 是 **docs 认知体系**，与 `7_MEMORY` 运行记忆、`2_COGNITION` 市场智能运行时模块三者物理与职责隔离。

# 商业智能契约原则

## 核心要求

商业智能模块（`1_DATA` → `2_COGNITION` → `3_DECISION` → `11_CONTENT_FACTORY`）之间交换数据时，**必须使用标准 Commercial Intelligence Object**，不得传递未文档化的 ad-hoc 结构。

## 权威契约

[docs/04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md](../04_BLUEPRINT/contract/AI_FACTORY_OS_COMMERCIAL_INTELLIGENCE_CONTRACT.md)

## 五类 Object（v1.0）

Market Signal → Opportunity → Production Request → Product Asset → Feedback

## 规则

- 遵守 Module Permission Boundary — 禁止越权读写
- Opportunity Score ≠ Quality Score ≠ Legacy Product Score
- 运行时经 OS 调度；持久化经 Database Contract
- `contract_version` 字段必填；major 变更须更新契约文档

## Cognition Agent 架构原则

2_COGNITION 内 Agent 须遵守 [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_AGENT_ARCHITECTURE_BLUEPRINT.md)：

- 五 Agent 职责不重叠：Trend / Demand / Competition / Opportunity / Insight
- OpportunityAgent **禁止**生产商品、修改 Content Factory、直接发布
- 输出 Opportunity Object 须符合 Commercial Intelligence Contract
- 所有 Agent 经 ExecutionRuntime 调度，实现 `BaseAgent.execute()`

# 项目资产生命周期管理原则

## 核心要求

AI Factory OS 所有文件必须具有明确生命周期状态。

**状态：**

- **Active** — 当前系统正在使用
- **Experimental** — 实验阶段文件
- **Temporary** — 临时生成文件
- **Deprecated** — 已废弃但保留历史价值
- **Archive** — 归档保存

## 原则

1. 不确定用途的文件禁止直接删除。
2. 删除前必须完成资产审计（见 `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md`）。
3. 历史实验文件必须标记来源（Created By / Referenced By）。
4. 正式资产与测试资产必须分离（生产代码 vs `output/` / `logs/` / 实验批次 artifact）。

## 审计文档

- **审计规范** — `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md`
- **登记模板** — `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md`
- **扫描报告** — `docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_SCAN_REPORT.md`

## 与项目自描述体系的关系

资产生命周期管理是 Project Intelligence Layer 的组成部分，与模块注册、执行历史、状态快照共同保证未来 AI 不被历史文件误导。

**完整治理规范：** [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](../04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)

# 资产生命周期管理原则

## 核心

AI_FACTORY_OS 中的**数据、代码、产品、模型输出**均属于**长期资产**。

任何资产删除必须经过：

1. **审计** — Asset Audit + Scan Report 对照
2. **分类** — Active / Experimental / Archive / Temporary
3. **归档** — Archive 先于 Delete
4. **确认** — 用户 Approval

## 禁止

- 未经审计直接删除
- Deprecated 资产直接删除
- 数据库表或历史行无 backup 变更

## 权威文档

- [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](../04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)

# 数据资产优先原则

## 核心要求

AI Factory OS 的长期资产包括：

- **软件代码资产** — 核心 OS、Agent、生产流水线
- **自动化流程资产** — DAG 执行链、Content Factory pipeline
- **数据资产** — `data/ai_factory.db`、采集样本、市场数据
- **市场分析资产** — 机会评分、趋势洞察（未来 `2_COGNITION` 产出）
- **用户反馈资产** — 销售数据、用户评价、product_memory

数据采集、分析结果、商业反馈必须被视为**长期资产**。

## 建设优先级

系统建设过程中，应优先考虑：

**数据积累能力**

而不仅是功能增加。

## 与架构的关系

- `1_DATA` 负责事实数据采集与存储
- `2_COGNITION`（下一阶段）负责市场分析资产沉淀
- `7_MEMORY` 负责 OS 运行时学习
- `11_CONTENT_FACTORY/storage/` 负责产品级记忆

各层数据物理隔离，未来通过标准接口单向同步，不得混写或覆盖。

# 架构先行原则

## 核心要求

任何核心模块新增前，**必须先完成**：

1. **模块定位** — 在整体架构中的位置与名称
2. **职责边界** — 负责什么、不负责什么
3. **输入输出定义** — 标准数据对象与接口协议
4. **上下游关系** — 与相邻模块的连接方式
5. **实施路线** — 分阶段 Roadmap

**再进入代码开发。**

## 目的

避免模块重复建设和架构漂移。

## 实践参考

- `2_COGNITION` — [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md)（Blueprint v1 已完成，代码未建）
- 新增模块须同步更新：`AI_FACTORY_OS_MODULE_REGISTRY.md`、`PROJECT_STATUS.md`、`CURSOR_EXECUTION_HISTORY.md`

# 数据库资产原则

## 核心要求

数据库**不是临时存储**。

AI Factory OS 应持续积累：

- **市场数据** — 关键词、趋势、竞争、需求信号
- **产品数据** — 已生成产品与 artifact 关联
- **用户反馈数据** — views / clicks / sales / customer_feedback
- **商业结果数据** — 转化率、收入相关指标

## 原则

数据资产必须具备**长期价值**。

- 与 `7_MEMORY` 运行时记忆物理隔离
- 与 `output/`、`logs/` 等 Temporary 资产区分
- Schema 变更须先完成 Blueprint / Migration Plan，再执行代码

## 参考文档

- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT.md)
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md](../04_BLUEPRINT/runtime/AI_FACTORY_OS_COGNITION_BLUEPRINT.md)
- [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md](../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md)
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md)

# 历史能力保护原则

## 核心要求

AI Factory OS 升级**必须基于已有能力演化**。

```
Existing Capability
        +
New Architecture
```

## 原则

- **禁止**因为新设计而删除历史有效模块
- **禁止**因 Blueprint 目标态而废弃正在运行的 Legacy Active 表（如 `products`、`scores`）
- 数据库演化采用 **Additive Evolution Strategy**（见 Migration Plan v1）
- 代码层：`0_START` ~ `11_CONTENT_FACTORY` 已有运行链在未评估影响前不得破坏

## 参考

- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md)
- [docs/07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md](../07_AUDIT/database/AI_FACTORY_OS_DATABASE_REALITY_AUDIT.md)

# 数据接口契约原则

## 核心要求

模块之间**必须通过明确接口通信**。

## 允许的方式

| 方式 | 用途 |
|------|------|
| **Database Contract** | 跨模块持久化数据 — 见 Integration Design |
| **OS Protocol JSON** | DAG 节点间运行时传递 — `input_data` / `make_output` |
| **artifact_path 指针** | 大文件产物 — DB 存路径，不存 BLOB |

## 禁止行为

- **禁止**模块直接依赖其他模块内部实现
- **禁止**跨模块直接读取 `storage/`、`artifacts/`、`*_memory.json` 等内部文件
- **禁止**各模块独立 `sqlite3.connect` — 统一经 `1_DATA/database.py`

## 参考

- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_INTEGRATION_DESIGN.md) — Interface 1–5 与 Data Contract Rules

# 数据库实施生命周期原则

## 核心要求

AI_FACTORY_OS 数据库属于**长期商业资产**。

任何数据库实施**必须遵守**：

1. **设计优先** — Schema Blueprint / Integration Design 先于 SQL
2. **审计优先** — Reality Audit 对照现有 `ai_factory.db` 再行动
3. **迁移计划优先** — Migration Plan + Implementation Plan 审批后执行
4. **数据保留优先** — Legacy 表与历史行禁止删除
5. **可回滚原则** — backup + migration_history + rollback 预案

## 禁止

- **禁止**未经审计直接修改数据库
- **禁止**跳过 backup 执行 DDL
- **禁止**一次性重构数据库

## 实施规范

- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_EXTENSION_IMPLEMENTATION_PLAN.md)
- [docs/04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md](../04_BLUEPRINT/database/AI_FACTORY_OS_DATABASE_MIGRATION_PLAN.md)

# 中文可理解原则

## 核心要求

Project Intelligence Layer（项目智能层）及所有面向人类与 AI 协作者的 **docs 文档** 中，英文技术名称**必须**提供中文解释，确保非英语读者可准确理解架构与职责。

## 格式规范

```
English Name（中文说明）
```

**示例：**

- Market Intelligence Layer（市场智能层）
- Commercial Validation Layer（商业验证层）
- Production Request Object（生产请求对象）
- Feedback-Driven Intelligence（反馈驱动智能）

## 适用范围

| 适用 | 不适用 |
|------|--------|
| 文档标题、章节名、架构术语 | 代码变量名、函数名、文件名 |
| 模块职责描述、Blueprint 正文 | JSON Schema 字段名（可附中文列说明） |
| 执行报告、恢复说明 | import 路径、CLI 命令 |

## 目的

保证未来 AI 与用户恢复项目上下文时，不因纯英文术语产生理解偏差；与 [Commercial MVP Blueprint](../04_BLUEPRINT/commercial/AI_FACTORY_OS_COMMERCIAL_MVP_BLUEPRINT.md) 等文档的中英对照风格保持一致。

# 历史资产保护原则

## 核心要求

AI Factory OS 中的**旧文档、旧代码、旧数据库结构**属于长期资产，**不得直接删除**。

任何废弃或清理操作**必须**经过完整治理流程：

```
Audit（审计）
        ↓
Classify（分类）
        ↓
Archive（归档）
        ↓
Approval（用户确认）
        ↓
Delete（删除 — 仅最后一步，且非默认）
```

## 分类参考

| 状态 | 说明 | 默认动作 |
|------|------|----------|
| **Active** | 当前使用中 | 保留 |
| **Experimental** | 实验文件 | 保留或 Archive |
| **Deprecated** | 已废弃但有历史价值 | Archive，不 Delete |
| **Temporary** | 临时输出 | 按 Policy 清理周期 |
| **Archive** | 已归档 | 保留只读 |

## 特别保护项

| 资产类型 | 保护规则 |
|----------|----------|
| Legacy DB 表（`products`, `scores` 等） | Additive Evolution，禁止 DROP |
| Frozen 模块（`9_PRODUCT`, `10_DEPLOY`） | 禁止未经评估修改或删除 |
| docs 历史 Blueprint | 版本演进，不覆盖删除 |
| `7_MEMORY/*.json(l)` | 运行资产，禁止无审计清理 |

## 权威文档

- [docs/04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md](../04_BLUEPRINT/policy/AI_FACTORY_OS_ASSET_LIFECYCLE_POLICY.md)
- [docs/07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md](../07_AUDIT/asset/AI_FACTORY_OS_ASSET_AUDIT.md)

## 与 Current State Lock Principle 的关系

历史资产保护是 **Current State Lock Principle（当前状态锁定原则）** 在资产治理维度的具体化：Existing（已有）资产默认保留，Delete 不是演化手段。



---

# Historical Status

本文为历史工作原则参考。

当前执行规则：
请以：

00_GOVERNANCE/AI_FACTORY_OS_EXECUTION_PROTOCOL.md

为准。

---

# ARCHIVED_HISTORICAL_STATUS

状态：

历史参考文件。

禁止：

作为当前执行规则。

当前规则唯一来源：

00_GOVERNANCE/AI_FACTORY_OS_EXECUTION_PROTOCOL.md
