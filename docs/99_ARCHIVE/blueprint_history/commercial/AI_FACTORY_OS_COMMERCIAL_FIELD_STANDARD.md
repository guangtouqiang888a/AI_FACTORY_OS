# AI_FACTORY_OS Commercial Field Standard v1

> Entry 039-C | Lifecycle Field Standard Design  
> **状态：Blueprint Completed — Implementation Not Started**

**原则：** 语义隔离 — 同一词 `completed` 不得跨维度复用而不带字段前缀

---

## 1. 标准维度

### lifecycle_status

**含义：** 对象在商业链上的生命周期位置。

| 例值 | 含义 |
|------|------|
| `draft` | 已创建，未批准进入下一阶段 |
| `approved` | 已批准（设计/生产/上架等，依对象契约） |
| `running` | 进行中（实验观察或活动窗） |
| `completed` | **生命周期完结**（可进入评估或归档） |
| `rejected` | 否决终态 |
| `archived` | 归档 |

**禁止：** 用 lifecycle_status 表达「文件生成成功」或「验收通过」。

---

### execution_status

**含义：** 执行过程（生产/调度）状态。

| 例值 | 含义 |
|------|------|
| `idle` | 未入队 |
| `queued` | 排队 |
| `executing` | 执行中 |
| `succeeded` | 执行成功（artifact 产出） |
| `failed` | 执行失败 |
| `cancelled` | 取消 |

**禁止：** 用 execution_status=`succeeded` 断言市场验证成功。

---

### validation_status

**含义：** 验收/门禁结果（契约与质量）。

| 例值 | 含义 |
|------|------|
| `pending` | 未验 |
| `passed` | 通过 |
| `failed` | 失败 |
| `waived` | 人工豁免 |

**范围：** Product Asset Validation Gate；非 Experiment.`validation_goal` 文本。

---

### release_status

**含义：** 发布/上架相关。

| 例值 | 含义 |
|------|------|
| `unreleased` | 未发布 |
| `approved_for_release` | 允许上架 |
| `released` | 已上架（观察） |
| `deprecated` | 下架/弃用 |

**禁止：** 与 generation/execution 混用。

---

### evaluation_status

**含义：** 实验评估过程状态。

| 例值 | 含义 |
|------|------|
| `pending` | 未开始评估 |
| `running` | 评估中 |
| `completed` | 评估流程完成（已有结论字段） |

**配套结论字段（非本维）：** `hypothesis_result` ∈ {pending, success, promising, failed, inconclusive}

---

### collection_status（Feedback 扩展维）

**含义：** 市场观测数据采集进度。

| 例值 | 含义 |
|------|------|
| `not_started` | 未开始 |
| `collecting` | 采集中 |
| `recorded` | 已录入真实指标 |
| `closed` | 观察窗关闭 |

---

### decision（决策维 — 保留）

**含义：** 独立审批/选择实体的决定，**不替代** lifecycle_status。

| 用于 | 例值 |
|------|------|
| Selection | selected, watch, rejected |
| Exp Review | prepared, rejected |
| Approval | approved, rejected, pending |

同步规则：decision 变更后，由 Human Assisted Entry 回写相关对象的 lifecycle_status（见 039-B）。

---

### creation_method / *_method（方法维 — 保留）

**含义：** human_assisted / adapter_generated 等 — **禁止写入 lifecycle_status**。

---

## 2. 对象 × 标准字段（哪些对象用哪些）

| 对象 | lifecycle_status | execution_status | validation_status | release_status | evaluation_status | collection_status | decision |
|------|------------------|------------------|-------------------|----------------|-------------------|-------------------|----------|
| Candidate | ✅ | — | — | — | — | — | — |
| Opportunity | ✅ | — | — | — | — | — | — |
| Selection | ✅* | — | — | — | — | — | ✅ 主 |
| Experiment | ✅ | — | —† | — | ✅ 可选镜像 | — | — |
| Exp Review | ✅* | — | — | — | — | — | ✅ 主 |
| Production Request | ✅ | ✅ | — | — | — | — | — |
| Approval | ✅* | — | — | — | — | — | ✅ 主 |
| Product Asset | ✅ | ✅‡ | ✅ | ✅ | — | — | — |
| Validation | — | — | ✅ | — | — | — | — |
| Feedback | ✅ | — | — | — | — | ✅ | — |
| Evaluation | ✅ | — | — | — | ✅ | —§ | — |

\* 可用 lifecycle_status 作镜像，或以 decision 为 SoT（契约选定其一）  
† Experiment 不设 Product 级 validation_status；文本用 validation_goal  
‡ 可由 generation→execution 映射  
§ observation 可用 collection 对齐 Feedback，或嵌套 observation_period  

---

## 3. `completed` 语义隔离

| 字段 | `completed` 表示 |
|------|------------------|
| lifecycle_status | 对象生命周期阶段结束 |
| execution_status | **不用** completed — 用 `succeeded` |
| evaluation_status | 评估流程结束 |
| generation_status（历史） | 应映射为 execution_status=`succeeded` |

---

## 4. 状态声明

| 项 | 状态 |
|----|------|
| Field Standard v1 | ✅ Blueprint Completed |
| JSON schema 迁移 | ❌ Not Started |
