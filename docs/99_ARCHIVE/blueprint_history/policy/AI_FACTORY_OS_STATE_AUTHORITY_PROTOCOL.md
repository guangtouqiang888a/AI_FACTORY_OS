# AI_FACTORY_OS State Authority Protocol v1

> Entry 039-A — State Authority Design  
> **状态：Blueprint Completed — Enforcement Not Started**

**原则：**

- 每类状态 **唯一事实来源（Single Source of Truth）**
- Documentation **只展示，不作为事实来源**
- Database Reality ≠ Documentation Reality
- JSON Asset ≠ Database Record

**对齐：** Governance Protocol §2 Source of Truth；Data Ownership Model v1

---

## 1. 权威总表

| 状态域 | Source of Truth（权威） | 允许的展示/副本 | 禁止 |
|--------|-------------------------|-----------------|------|
| **Runtime Behavior** | Python 代码 | docs 说明 | docs 改行为预期不改代码 |
| **Operational Market Data** | `data/ai_factory.db` | docs inventory | commercial JSON 冒充 listing |
| **Commercial Objects** | `commercial_assets/` | docs、pilot_outputs 快照 | product_memory 冒充登记 |
| **OS Learning Memory** | `7_MEMORY/`（memory_core 管理文件） | PROJECT_CORE_MEMORY.md 摘要 | core_state.json 作 SoT |
| **System Description / Phase** | docs（Registry + PROJECT_STATUS + snapshot）经 Entry 同步 | — | 仅改一处不同步 |
| **Execution Trace（Entry）** | `docs/05_EXECUTION/CURSOR_EXECUTION_HISTORY.md` | — | 口头完成无台账 |

---

## 2. Commercial Object 分项权威

### Product Asset

| 项 | 定义 |
|----|------|
| **Source of Truth** | `commercial_assets/product_assets/product_assets_v1.json` |
| **Physical deliverable** | `11_CONTENT_FACTORY/artifacts/products/{product_asset_id}/` |
| **Cache（非权威）** | `11_CONTENT_FACTORY/storage/product_memory.json` |
| **Snapshot（非权威）** | `commercial_assets/pilot_outputs/**` |
| **Docs** | 仅引用 ID / 状态摘要 |

**Pilot 权威实例：** `8523329941d4` ↔ `preq_20260712_005`

---

### Experiment

| 项 | 定义 |
|----|------|
| **Source of Truth** | `commercial_assets/experiments/experiments_v1.json` |
| **关联 Review** | `commercial_assets/experiment_reviews/`（独立实体；decision 字段） |
| **待确认事项** | Experiment.`status` 与 Review.`decision` / Product Asset 完成态 **字段冲突已记录**（CSA-001）；**权威仍是 JSON 原文** — 在同步 Entry 执行前，**不得**用 docs「Pilot Completed」覆盖 Experiment.status=`draft` 的对象事实 |

**说明：** 「待确认」指 **lifecycle 字段应取何值** 需人工 Entry 决策；**文件位置权威已确认**为 experiments JSON。

---

### Production Request

| 项 | 定义 |
|----|------|
| **Source of Truth** | `commercial_assets/production_requests/production_requests_v1.json` |
| **Approval SoT** | `commercial_assets/production_request_reviews/`（`decision`） |
| **Runtime gate** | `ApprovalGate` 读 Approval JSON；Pilot whitelist 另属 **策略代码**（非 PR.status 字段） |

**字段冲突：** PR.status 常为 `draft` 而 Approval=`approved` — 权威各自为自身文件；交叉解释必须显式标注两边字段。

---

### Approval

| 项 | 定义 |
|----|------|
| **Source of Truth** | `commercial_assets/production_request_reviews/production_request_reviews_v1.json` |

---

### Validation

| 项 | 定义 |
|----|------|
| **Source of Truth** | `commercial_assets/product_asset_validations/product_asset_validations_v1.json` |
| **Runtime check** | `ProductAssetValidator` 结果对象 — **写入登记**才成为商业事实 |

---

### Feedback

| 项 | 定义 |
|----|------|
| **Source of Truth** | `commercial_assets/feedback/feedback_v1.json` |
| **Not SoT** | CF FeedbackAgent stub；docs Observation Protocol（协议 ≠ 数据） |

---

### Evaluation

| 项 | 定义 |
|----|------|
| **Source of Truth** | `commercial_assets/experiment_evaluations/experiment_evaluations_v1.json` |

---

### Opportunity / Candidate / Selection

| 对象 | Source of Truth |
|------|-----------------|
| Candidate | `commercial_assets/opportunity_candidates/` |
| Opportunity | `commercial_assets/opportunities/` |
| Selection | `commercial_assets/experiment_selection/` |

---

## 3. Execution / Operational 权威

| 状态 | Source of Truth |
|------|-----------------|
| 采集商品与评分 | `data/ai_factory.db`（products / scores） |
| DAG 执行结果 | Runtime 返回值 + `7_MEMORY/event_log.jsonl` + `logs/execution_hash.log` |
| 本地 publish 模拟 | `output/*.json` |
| CF pipeline 某次运行 | 当次返回 dict；持久化以 _save_product / pilot_outputs 为准（非 DB） |

---

## 4. Documentation 角色

```
Code / DB / JSON  = 事实
docs              = 投影（Projection）
```

当冲突时：

1. 以 **代码** 判定 Runtime 行为  
2. 以 **DB 文件** 判定 Operational 行存  
3. 以 **commercial_assets JSON** 判定商业对象字段  
4. **更新 docs** 对齐事实；禁止「文档覆盖事实」

---

## 5. 冲突处理流程（设计）

```
发现冲突
  → 记录于 Schema Drift / Commercial State Alignment / Known Issues
  → 人工确认权威字段
  → 单独 Entry 同步（改 JSON 或改代码或改 docs）
  → 禁止静默迁移到另一存储域
```

---

## 6. 状态声明

| 项 | 状态 |
|----|------|
| State Authority Protocol v1 | ✅ Blueprint Completed |
| Automated authority checks | ❌ Not Started |
| Commercial status field sync | ❌ Not Started（须授权） |

**Blueprint ≠ Runtime.**
