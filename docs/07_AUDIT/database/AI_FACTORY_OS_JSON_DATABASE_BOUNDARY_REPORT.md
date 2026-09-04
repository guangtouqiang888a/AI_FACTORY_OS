# AI_FACTORY_OS JSON vs Database Boundary Report

> Entry 039-A | JSON ↔ Database 边界分析 | 2026-07-14  
> **方法：** commercial_assets/ + data/ai_factory.db 事实对照  
> **禁止：** 未迁移、未改 JSON、未改 DB

**原则：** JSON Asset ≠ Database Record

---

## 1. 双轨现实（实测）

| 轨 | 存储 | 内容 |
|----|------|------|
| **A — Operational** | `data/ai_factory.db` | 市场 listing、采集日志、OS 评分 |
| **B — Commercial** | `commercial_assets/**/*.json` | 机会→实验→生产→资产→反馈→评估 |

**Python 连接：** Core OS 读 SQLite；Adapter **只读** PR/Approval JSON；**无** Commercial→SQLite 写入代码。

---

## 2. 对象级决策

### Opportunity / Candidate

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/opportunity_candidates/`, `opportunities/` |
| **In Database?** | ❌ 无表 |
| **Should stay JSON (near-term)** | ✅ Yes — 人机 assisted、schema 仍在演化、低频变更 |
| **Should enter Database (future)** | ⚠️ Optional — 仅当 Cognition 自动大批量机会评分且需查询索引时 |

---

### Experiment

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/experiments/experiments_v1.json` |
| **In Database?** | ❌ |
| **Should stay JSON (near-term)** | ✅ Yes — lifecycle draft/prepared 人工治理；状态冲突已记录于 Commercial State Alignment |
| **Should enter Database (future)** | ⚠️ Phase 后期 — 实验台账规模化（30+）且需聚合分析时；须单独 Entry |

---

### Production Request

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/production_requests/production_requests_v1.json` |
| **In Database?** | ❌ |
| **Should stay JSON (near-term)** | ✅ Yes — Adapter 输入 SoT；人类审批绑定 |
| **Should enter Database (future)** | ⚠️ 若 Runtime 自动出队调度 — 可镜像 `production_requests` 表；JSON 仍可作 import source |

---

### Approval（PR Review）

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/production_request_reviews/` |
| **In Database?** | ❌ |
| **Should stay JSON** | ✅ — 审批凭证；低频；审计可读 |
| **Should enter Database** | 低优先级 — 除非合规要求 append-only table |

---

### Product Asset

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/product_assets/product_assets_v1.json` |
| **Artifacts** | `11_CONTENT_FACTORY/artifacts/products/{id}/` |
| **In Database?** | ❌（Blueprint 曾规划 generated_products — **未实现**） |
| **Should stay JSON (near-term)** | ✅ **强制** — Pilot 8523329941d4 可追溯 SoT |
| **Should enter Database (future)** | 可选镜像：id、path、quality_score、source_preq — **不得**删除 JSON SoT 除非迁移 Entry 完成双写验证 |

---

### Validation

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/product_asset_validations/` |
| **Runtime** | `ProductAssetValidator`（不写 DB） |
| **Should stay JSON** | ✅ |
| **Should enter Database** | 低 — 验收结果作为 Commercial 附属记录即可 |

---

### Feedback

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/feedback/feedback_v1.json` |
| **In Database?** | ❌（Blueprint product_feedback — **未实现**） |
| **Should stay JSON (near-term)** | ✅ — observation pending；无虚假市场数据 |
| **Should enter Database (future)** | ✅ **优先候选**（当观察期开始、指标时间序列需要查询时）— 仍可 JSON 双写过渡 |

---

### Evaluation

| 项 | 事实 |
|----|------|
| **Current store** | `commercial_assets/experiment_evaluations/` |
| **Should stay JSON** | ✅ near-term |
| **Should enter Database** | 与 Feedback 同期；聚合报表需求出现后再迁 |

---

## 3. 应保留在 Database 的数据

| 数据 | 原因 |
|------|------|
| products / keywords / collection_log | OS DataAgent 运行时路径 |
| scores | ScoringAgent 批量 INSERT |
| platforms | 平台注册 |

**不应**把 Opportunity/Product Asset 塞入现有 `products` 表（语义冲突：市场 listing ≠ 自产数字商品）。

---

## 4. 应保持 JSON 的数据（当前阶段结论）

| 对象 | 决策 | 理由 |
|------|------|------|
| Opportunity / Candidate | **Keep JSON** | 人工 assisted；无 DB writer；演化中 |
| Experiment | **Keep JSON** | SoT；状态治理先修字段再考虑迁移 |
| Production Request | **Keep JSON** | Adapter 输入 SoT |
| Approval | **Keep JSON** | 审批凭证 |
| Product Asset | **Keep JSON** | Pilot 追溯；Commercial SoT |
| Validation | **Keep JSON** | 附属验收 |
| Feedback | **Keep JSON now**；**Future DB candidate** | 观察时序 |
| Evaluation | **Keep JSON now** | 绑定 Experiment |

---

## 5. 禁止事项（边界保护）

1. 禁止把 CF `product_memory.json` 当作 Product Asset DB  
2. 禁止未授权 CREATE Commercial 表（须 Entry）  
3. 禁止假设 Blueprint 表已存在  
4. 禁止用 SQLite products 行冒充 `8523329941d4` Product Asset  

---

## 6. 与 Ownership / Authority 关系

- Commercial → JSON（Owner: Commercial Asset Layer）  
- Operational → SQLite（Owner: Execution Runtime）  
- 边界见 `AI_FACTORY_OS_STATE_AUTHORITY_PROTOCOL.md`

---

## 本 Entry 操作

- ✅ 边界分析完成  
- ❌ 无迁移、无双写、无 JSON/DB 修改  
