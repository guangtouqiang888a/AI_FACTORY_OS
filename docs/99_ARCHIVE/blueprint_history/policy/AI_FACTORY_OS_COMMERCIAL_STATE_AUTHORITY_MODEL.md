# AI_FACTORY_OS Commercial State Authority Model v1

> Entry 039-B | 商业状态权威与权限  
> **状态：Blueprint Completed — Enforcement Not Started**

**对齐：** `STATE_AUTHORITY_PROTOCOL.md` · `DATA_OWNERSHIP_MODEL.md` · Lifecycle State Machine

---

## 1. 总则

| 规则 | 说明 |
|------|------|
| Single Writer | 每个对象字段的状态更新只能由 **Owner Layer** 或经其授权的 Human Assisted Entry |
| Read-wide | 下游模块可读上游 SoT；默认 **不可写** |
| Docs Projection | docs 只展示；不能单独改 Lifecycle 事实 |
| No Silent Auto-Success | 销售/收入/市场验证成功禁止无人确认写入 |

---

## 2. 对象 Owner 与权限

### Opportunity / Candidate / Selection

| 项 | 定义 |
|----|------|
| **Owner** | Experiment / Opportunity Layer（Commercial Intelligence） |
| **SoT** | `commercial_assets/opportunity_candidates/` · `opportunities/` · `experiment_selection/` |
| **可修改** | Human Assisted Entry；未来 2_COGNITION（只提案，默认不直接写 SoT） |
| **可读** | 3_DECISION（设计）；docs；Selection Framework |
| **不可写** | 11_CONTENT_FACTORY；1_DATA SQLite；7_MEMORY |

---

### Experiment

| 项 | 定义 |
|----|------|
| **Owner** | Experiment Layer |
| **SoT** | `commercial_assets/experiments/experiments_v1.json` |
| **可修改** | Human Assisted Entry（lifecycle 同步）；Exp Review 流程（经 Entry） |
| **可读** | PR 创建者；Evaluation；docs；CF Adapter（经 PR 间接） |
| **不可写** | CF Pipeline；SQLite；Memory |

---

### Experiment Review

| 项 | 定义 |
|----|------|
| **Owner** | Experiment Layer（Prepared Review） |
| **SoT** | `commercial_assets/experiment_reviews/` |
| **可修改** | Human only（prepared/rejected） |
| **可读** | Production Request 创建流程 |

---

### Production Request

| 项 | 定义 |
|----|------|
| **Owner** | Production Management Layer |
| **SoT** | `commercial_assets/production_requests/` |
| **可修改** | Human Assisted Entry；目标上 Approval 同步可写 status（须 Entry） |
| **可读** | CF Adapter（只读加载）；ApprovalGate；docs |
| **不可写** | ContentPipeline；MarketAgent；1_DATA |

---

### Approval

| 项 | 定义 |
|----|------|
| **Owner** | Production Management Layer（审批） |
| **SoT** | `commercial_assets/production_request_reviews/` |
| **可修改** | Human only |
| **可读** | `ApprovalGate`（Python 只读） |
| **不可写** | Runtime 自动 approve |

---

### Product Asset

| 项 | 定义 |
|----|------|
| **Owner** | Commercial Asset Layer |
| **SoT** | `commercial_assets/product_assets/` |
| **可修改** | Human Assisted Entry（登记）；未来授权的 Adapter 写入器 |
| **可读** | Validation；Feedback；Evaluation；docs |
| **不可写冒充 SoT** | `product_memory.json`；`pilot_outputs`（快照） |

**物理 artifacts：** CF 可写文件目录；**登记身份**仍归 Commercial Asset Layer。

---

### Validation

| 项 | 定义 |
|----|------|
| **Owner** | Commercial Asset Layer（验收登记） |
| **Runtime check** | `ProductAssetValidator`（可计算，默认不写 SoT） |
| **SoT** | `commercial_assets/product_asset_validations/` |
| **可修改 JSON** | Human / 授权 Entry；未来 Adapter 集成后可写 validation 记录 |
| **不可** | 无人确认标记市场成功 |

---

### Feedback

| 项 | 定义 |
|----|------|
| **Owner** | Commercial Asset Layer（观察反馈） |
| **SoT** | `commercial_assets/feedback/` |
| **可修改** | Human Assisted 观测录入（强制） |
| **可读** | Evaluation；Memory（只读学习信号，未来） |
| **不可写** | CF FeedbackAgent stub；自动伪造 metric |

---

### Evaluation

| 项 | 定义 |
|----|------|
| **Owner** | Experiment Layer（评估结论） |
| **SoT** | `commercial_assets/experiment_evaluations/` |
| **可修改** | Human Assisted 判定 hypothesis_result |
| **可读** | Selection Failure Learning；docs；未来 Cognition |
| **门禁** | 无真实 Feedback recorded 不得 completed（除非 waiver） |

---

## 3. 模块读写矩阵（目标）

| 模块 | Candidate/Opp | Experiment | PR | Approval | Product Asset | Feedback | Evaluation |
|------|---------------|------------|-----|----------|---------------|----------|------------|
| docs / Governance | R | R | R | R | R | R | R |
| Human Assisted Entry | RW* | RW* | RW* | RW* | RW* | RW* | RW* |
| CF Adapter | — | R(indir) | R | R | W† | — | — |
| CF Pipeline | — | — | — | — | artifact W | — | — |
| ProductAssetValidator | — | — | R | — | R | — | — |
| 0_START / 1_DATA / 3_DECISION | —‡ | — | — | — | — | — | — |
| 7_MEMORY | — | — | — | — | — | R† | R† |

\* 仅经授权 Entry  
† 仅未来授权  
‡ 现状无连接；未来 Cognition 提案不直接写 Commercial SoT  

---

## 4. 与 System State Authority 边界

| 域 | 权威 |
|----|------|
| Commercial lifecycle 字段 | 本模型 + commercial_assets JSON |
| Operational scores/products | SQLite |
| Entry / Phase 工程状态 | docs PROJECT_STATUS 等 |

---

## 5. 状态声明

| 项 | 状态 |
|----|------|
| Commercial State Authority Model | ✅ Blueprint Completed |
| Permission enforcement in code | ❌ Not Started |
