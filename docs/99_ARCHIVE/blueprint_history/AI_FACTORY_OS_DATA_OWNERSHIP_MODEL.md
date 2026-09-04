# AI_FACTORY_OS Data Ownership Model v1

> Entry 039-A — Database Alignment & State Authority Design  
> **状态：Blueprint Completed — Implementation Not Started**

**原则：** JSON Asset ≠ Database Record · 每类数据一个 Owner · Documentation 不拥有业务事实

---

## 1. 目的

定义 AI_FACTORY_OS 五类数据所有权，避免：

- docs 覆盖 Runtime 事实
- commercial_assets 与 SQLite 混写
- Memory 与 Commercial Feedback 语义混淆

---

## 2. 数据分类

### System State

**示例：**

- 当前 Entry / Phase（工程阶段）
- 模块 Status（Active / Planned / Frozen）
- 架构状态（Blueprint Completed / Runtime Connected）
- Governance Layer 状态

**Owner：** System Governance

**存储现实：**

| 介质 | 路径 | 角色 |
|------|------|------|
| 权威描述 | `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md`, `docs/01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md`, `docs/01_CURRENT_STATE/reference/system_snapshot.md` | 展示与恢复 |
| 执行轨迹 | `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` | Entry 审计 |
| 孤儿 JSON | `7_MEMORY/core_state.json` | **非 SoT**（无代码引用） |

**规则：** System State 的变更必须经 Entry + 三文件同步；不得仅改 Memory JSON。

---

### Operational Data

**示例：**

- 市场 listing 采集结果（products）
- 采集日志（collection_log）
- OS 商品评分（scores）
- Runtime 执行事件 / execution_hash
- Deploy metrics / traces（若启用）

**Owner：** Execution Runtime（经 `1_DATA` + `0_START` + `3_DECISION`）

**存储现实：**

| 介质 | 路径 |
|------|------|
| SQLite Operational DB | `data/ai_factory.db` |
| Event / Hash | `7_MEMORY/event_log.jsonl`, `logs/execution_hash.log` |
| Local publish simulation | `output/*.json` |

**规则：** Operational Data **不**存放 Commercial Product Asset / Experiment Object。

---

### Commercial Asset Data

**示例：**

- Opportunity / Candidate
- Experiment / Experiment Review
- Production Request / Approval
- Product Asset / Validation
- Feedback / Evaluation
- Pilot execution snapshots

**Owner：** Commercial Asset Layer

**存储现实：**

| 介质 | 路径 |
|------|------|
| **SoT** | `commercial_assets/**/*.json` |
| Artifact 文件 | `11_CONTENT_FACTORY/artifacts/products/{id}/`（物理交付物） |
| CF cache | `11_CONTENT_FACTORY/storage/product_memory.json`（**非 SoT**） |

**规则：**

- Python **不得**默认自动写入 commercial_assets（当前 Adapter/Validator 注释已约束）
- SQLite **不含** Commercial Object 表（039 实测）
- Artifact 路径可引用；登记身份以 Product Asset JSON 为准

---

### Memory Data

**示例：**

- pattern_memory（执行模式）
- strategy_memory（决策规则学习）
- runtime_policy（运行策略参数）
- policy snapshot / patch
- learning signals from OS runs

**Owner：** Memory System（`7_MEMORY` / `memory_core.py`）

**存储现实：**

| 文件 | 用途 |
|------|------|
| pattern_memory.json | 模式 |
| strategy_memory.json | 策略规则 |
| runtime_policy.json | 策略参数 |
| event_log.jsonl | 事件 |

**规则：**

- Memory ≠ Commercial Feedback
- Memory ≠ Product Asset
- Experiment Evaluation（commercial_assets）属 Commercial，不属 Memory Owner

---

### Documentation

**示例：**

- Markdown Blueprints / Protocols / Audit reports
- Business Plan / Work Principles

**Owner：** Governance Layer（docs）

**规则：**

- Documentation **只展示与设计**，**不作为** Operational / Commercial 事实来源
- 文档声称与代码/JSON/DB 冲突时，以事实源为准（State Authority Protocol）

---

## 3. Owner 对照矩阵

| 分类 | Owner | Primary Store | Secondary / Cache |
|------|-------|---------------|-------------------|
| System State | System Governance | docs/（PROJECT_STATUS, MODULE_REGISTRY, snapshot） | — |
| Operational Data | Execution Runtime | data/ai_factory.db | event_log, output/ |
| Commercial Asset Data | Commercial Asset Layer | commercial_assets/ | CF artifacts, product_memory |
| Memory Data | Memory System | 7_MEMORY/*.json(l) | — |
| Documentation | Governance Layer | docs/*.md | — |

---

## 4. 禁止交叉写入

| 禁止 | 原因 |
|------|------|
| docs 写入冒充 Commercial status SoT | docs 展示层 |
| Memory 写入 Product Asset | 域隔离 |
| SQLite 静默覆盖 commercial_assets ID | 双轨冲突 |
| CF product_memory 冒充 Commercial SoT | cache ≠ registry |

---

## 5. 状态声明

| 项 | 状态 |
|----|------|
| Data Ownership Model v1 | ✅ Blueprint Completed |
| Enforcement Runtime | ❌ Not Started |
| ORM / Unified Data Layer | ❌ Not Started（见 Evolution Plan） |

**Design ≠ Production.**
