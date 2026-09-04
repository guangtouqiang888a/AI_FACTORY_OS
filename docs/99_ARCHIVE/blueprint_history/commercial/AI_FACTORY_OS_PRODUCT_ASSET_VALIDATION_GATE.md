# AI_FACTORY_OS Product Asset Validation Gate v1

> Product Asset 验收门禁设计 | 最后更新：2026-07-13  
> **状态：Blueprint Completed — Project Intelligence Layer 设计规范，不参与运行计算**

**定位：** Product Asset Validation Gate Layer（产品资产验收门禁层）— 定义 **Content Factory Output（内容工厂产出）** 在进入 **`commercial_assets/product_assets/`** 登记之前，须通过的 **Product Asset Validation Gate（产品资产验收门禁）** 契约、检查清单、决策规则与模块边界。

**上级文档：**

- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](../contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md) — Product Asset Object Schema 与生命周期
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md) — CF 集成与 Output 映射
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md](../runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md) — Adapter 实施方案
- [docs/07_AUDIT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md](../../07_AUDIT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md) — Runtime 审计结论
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md](../contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md) — Production Request 规格与 quality_requirements

**当前状态（只读审计）：**

| 项 | 状态 |
|----|------|
| Adapter Code | ✅ Completed（Entry 032-B） |
| Adapter Regression | ✅ 6/6 PASS（Entry 032-C） |
| Validation Gate Runtime | ❌ **未实现** |
| `product_assets` JSON 实例 | ❌ **未创建** |
| Pilot Production（preq_005） | ❌ **未执行** |

**说明：** **Blueprint ≠ Implementation**。**Design Completed ≠ Runtime Connected**。**Validation Gate Completed ≠ Production Started**。本文档只定义验收门禁设计；不修改 Python、不调用 Content Factory、不生成 Product Asset、不创建 `commercial_assets/product_assets/`。

---

## 1. Validation Gate Position（门禁层定位）

### 1.1 在商业生产链中的位置

```
Production Request Object
        ↓
Production Request Approval（decision = approved）
        ↓
Content Factory Adapter（load → gate → map）
        ↓
Content Factory Pipeline（11_CONTENT_FACTORY — 生产执行）
        ↓
Product Asset Validation Gate              ← 本 Design 定义（资产准入层）
        ↓
Product Asset Object（commercial_assets/product_assets/）
        ↓
Feedback Object → Experiment Evaluation
```

### 1.2 Validation Gate ≠ QualityAgent

| 维度 | QualityAgent（11_CONTENT_FACTORY） | Product Asset Validation Gate |
|------|-----------------------------------|------------------------------|
| **阶段** | 生产过程内 | 生产完成后、资产入库前 |
| **输入** | `product` dict + `artifacts` | Product Asset 草稿 + PR 规格 + CF Output |
| **输出** | `quality_score`（0–100）、`commercial_score`、checklist | `validation_status`、`validation_result` |
| **目的** | 生产过程质量检查 — 是否继续 Packaging / ReleaseGate | **商业资产入库前验收** — 是否允许写入 `product_assets` |
| **失败后果** | Pipeline 中断或 `need_revision` | **禁止** Product Asset 持久化 |
| **商业裁决** | 不涉及 Experiment / PR 合规 | 对照 `validation_goal`、`asset_requirements` |

**规则：** QualityAgent 通过 **不等于** Product Asset 自动入库。Validation Gate 是 **独立准入层**，Pilot 阶段默认 **Human Assisted** 确认。

### 1.3 与 Adapter Approval Gate 的边界

| Gate | 时机 | 校验对象 |
|------|------|----------|
| **Adapter Approval Gate** | 生产**前** | Production Request + Approval 是否存在、`decision=approved`、Pilot whitelist |
| **Product Asset Validation Gate** | 生产**后** | CF Output → Product Asset 草稿是否符合 Contract + PR 规格 |

**顺序：** Approval Gate（授权生产）→ CF Pipeline（生成）→ **Validation Gate（验收入库）** → Product Asset Persistence。

### 1.4 核心原则

| 原则 | 说明 |
|------|------|
| **Validation Gate Completed ≠ Production Started** | 设计完成不等于 Runtime 已连接 |
| **QualityAgent Pass ≠ Asset Admitted** | 生产质检通过不等于商业资产已登记 |
| **passed → product_assets** | 仅 `validation_status=passed` 允许写入 `commercial_assets/product_assets/` |
| **Human Assisted ≠ Automation** | MVP Phase 1 验收默认人工辅助，非自动质量裁决 |

---

## 2. Validation Object Definition（验收对象定义）

### 2.1 product_asset_validation Object Schema v1

每条 Product Asset 入库验收须产生一条 **product_asset_validation** 记录（独立于 Product Asset Object）：

```json
{
  "validation_id": "pval_20260713_001",
  "object_type": "product_asset_validation",
  "contract_version": "1.0",
  "source_production_request_id": "preq_20260712_005",
  "source_product_asset_id": "passet_20260713_001",
  "source_experiment_id": "exp_20260708_005",
  "source_approval_id": "appr_20260713_005",
  "validation_method": "human_assisted",
  "validation_status": "passed",
  "validation_result": {},
  "review_items": [],
  "validated_by": "human",
  "created_at": "2026-07-13T18:30:00+08:00",
  "completed_at": "2026-07-13T18:35:00+08:00"
}
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 用途 |
|------|------|------|------|
| `validation_id` | TEXT | ✅ | 验收记录唯一 ID；格式建议 `pval_YYYYMMDD_NNN` |
| `object_type` | TEXT | ✅ | 固定 `"product_asset_validation"` |
| `contract_version` | TEXT | ✅ | 契约版本，当前 `"1.0"` |
| `source_production_request_id` | TEXT | ✅ | FK → Production Request |
| `source_product_asset_id` | TEXT | ✅ | FK → 待验收 Product Asset 草稿 / 实例 |
| `source_experiment_id` | TEXT | | 冗余 — Experiment 追溯 |
| `source_approval_id` | TEXT | | 冗余 — Approval 追溯 |
| `validation_method` | TEXT | ✅ | MVP Phase 1 固定 `"human_assisted"` |
| `validation_status` | TEXT | ✅ | `passed` / `failed` / `pending_review` — 见 §4 |
| `validation_result` | OBJECT | ✅ | 汇总结果 — 见 §2.3 |
| `review_items` | ARRAY | ✅ | 逐项检查明细 — 见 §3 |
| `validated_by` | TEXT | | `human` / `system`（未来） |
| `created_at` | TEXT | ✅ | ISO-8601 创建时间 |
| `completed_at` | TEXT | | 验收完成时间 |

### 2.3 validation_result 结构

```json
{
  "overall": "passed",
  "artifact_validation": { "passed": true, "failed_checks": [] },
  "contract_validation": { "passed": true, "failed_checks": [] },
  "quality_validation": { "passed": true, "failed_checks": [] },
  "commercial_validation": { "passed": true, "failed_checks": [] },
  "summary": "All checklist items passed; eligible for product_assets persistence",
  "blockers": [],
  "warnings": []
}
```

| 子字段 | 用途 |
|--------|------|
| `overall` | 与 `validation_status` 对齐的最终结论 |
| `artifact_validation` | §3.1 Artifact 检查结果汇总 |
| `contract_validation` | §3.2 Contract 检查结果汇总 |
| `quality_validation` | §3.3 Quality 检查结果汇总 |
| `commercial_validation` | §3.4 Commercial 检查结果汇总 |
| `blockers` | 导致 `failed` 的硬性阻断项 |
| `warnings` | 不阻断但需记录的软性提示 |

### 2.4 review_items 单项结构

```json
{
  "check_id": "artifact.file_exists",
  "category": "artifact_validation",
  "description": "Primary deliverable file exists on disk",
  "expected": "xlsx file present under artifact_path",
  "actual": "templates/xxx.xlsx",
  "passed": true,
  "severity": "blocker"
}
```

| 子字段 | 用途 |
|--------|------|
| `check_id` | 稳定检查项 ID — 便于回归与自动化 |
| `category` | `artifact_validation` / `contract_validation` / `quality_validation` / `commercial_validation` |
| `severity` | `blocker`（失败即 overall failed）/ `warning`（可 pending_review） |

---

## 3. Validation Checklist（验收检查清单）

Validation Gate 须按以下四类检查逐项执行，结果写入 `review_items`。

### 3.1 Artifact Validation（物理资产验收）

| check_id | 检查项 | 规则 | severity |
|----------|--------|------|----------|
| `artifact.file_exists` | 主交付文件是否存在 | `artifact_information.primary_file` 对应路径在磁盘存在 | blocker |
| `artifact.file_type_match` | 文件类型是否符合要求 | 后缀与 PR.`asset_requirements.deliverable_format` 一致（如 xlsx） | blocker |
| `artifact.file_openable` | 文件是否可打开 | xlsx/pptx/docx/pdf 可被标准库或工具解析（非空、非损坏） | blocker |
| `artifact.path_valid` | artifact_path 是否有效 | 路径存在、位于 `11_CONTENT_FACTORY/artifacts/products/{id}/` 下 | blocker |
| `artifact.deliverable_count` | 交付数量 | `artifact_files` 中主交付类型数量 ≥ PR.`deliverable_count` | blocker |
| `artifact.no_empty_primary` | 主文件非空 | 主文件 size > 0 bytes | blocker |

**Pilot preq_005 预期：** `file_type=xlsx`；`structure_outline` 对应 sheet 存在（考勤明细表、月度汇总、使用说明）— Commercial 层细检见 §3.4。

### 3.2 Contract Validation（契约字段验收）

| check_id | 检查项 | 规则 | severity |
|----------|--------|------|----------|
| `contract.product_asset_id` | product_asset_id 存在且非空 | 符合 `passet_*` 或 CF `product.id` 格式 | blocker |
| `contract.production_request_id` | source_production_request_id 匹配 | 与触发生产的 PR ID 一致 | blocker |
| `contract.experiment_id` | source_experiment_id 匹配 | 与 PR.`source_experiment_id` 一致 | blocker |
| `contract.approval_id` | approval_id 匹配 | 与 Approval 记录一致 | blocker |
| `contract.contract_version` | contract_version | 必须为 `"1.0"`（当前版本） | blocker |
| `contract.object_type` | object_type | 必须为 `"product_asset"` | blocker |
| `contract.creation_method` | creation_method | Pilot 允许 `adapter_generated` 或 `human_assisted` | warning |
| `contract.required_fields` | 必填字段完整 | Product Asset Contract §2.2 全部必填字段非空 | blocker |

### 3.3 Quality Validation（质量分验收）

| check_id | 检查项 | 规则 | severity |
|----------|--------|------|----------|
| `quality.score_present` | quality_score 存在 | 0.0–1.0 范围内（CF 0–100 须已归一化） | blocker |
| `quality.threshold_met` | 达到 PR 阈值 | `quality_score` ≥ PR.`quality_requirements.min_quality_score` | blocker |
| `quality.result_present` | quality_result 存在 | `artifact_information.quality_result` 非空 | blocker |
| `quality.first_pass` | 首次通过（若要求） | PR.`quality_requirements.first_pass_required=true` 时须 `first_pass=true` | blocker |
| `quality.checklist_items` | PR checklist 逐项 | PR.`quality_requirements.checklist[]` 每项在 quality_result 有对应 pass/fail | blocker |

**尺度对齐（Implementation 须处理）：**

| 来源 | 尺度 |
|------|------|
| QualityAgent 产出 | 0–100 |
| Product Asset Contract | 0.0–1.0 |
| PR min_quality_score（preq_005） | **0.85** |

**preq_005 checklist 参考：** `deliverable_format_correct`, `structure_complete`, `formulas_functional`, `attendance_stats_accurate`, `instructions_included`。

### 3.4 Commercial Validation（商业合规验收）

| check_id | 检查项 | 规则 | severity |
|----------|--------|------|----------|
| `commercial.validation_goal_readable` | validation_goal 只读对照 | Product Asset 可追溯至 Experiment validation_goal（不修改） | warning |
| `commercial.product_name_match` | 产品名一致 | Product Asset.`product_name` = PR.`product_name` | blocker |
| `commercial.product_type_match` | 产品类型一致 | Product Asset.`product_type` = PR.`product_type` | blocker |
| `commercial.structure_outline` | 结构大纲满足 | 交付内容覆盖 PR.`structure_outline[]` 主要章节/sheet | blocker |
| `commercial.content_constraints` | 内容约束 | language、max_pages_or_sheets、formulas_required 等满足 | blocker |
| `commercial.category_a_cost` | Category A 成本带 | 生产成本估算 ≤ PR.`category_a_threshold.production_cost_cny_max` | warning |
| `commercial.reject_conditions` | 拒绝条件未触发 | PR.`reject_conditions[]` 均未命中 | blocker |

**规则：** Commercial Validation **不重新执行** Opportunity 判断、Experiment Selection 或 Decision Scoring — 只对照 **已批准的 PR 规格** 与 **Experiment validation_goal** 只读上下文。

---

## 4. Validation Decision（验收决策）

### 4.1 validation_status 定义

| 状态 | 英文 | 含义 | 对 product_assets 的影响 |
|------|------|------|-------------------------|
| **Passed** | `passed` | 全部 blocker 检查通过 | ✅ **允许** 写入 `commercial_assets/product_assets/` |
| **Failed** | `failed` | 任一 blocker 检查失败 | ❌ **禁止** 写入 product_assets |
| **Pending Review** | `pending_review` | 存在 warning 或需人工裁量项 | ⏸ **等待** 人工判断后再定 passed/failed |

### 4.2 决策规则

```
IF any review_item.severity=blocker AND passed=false
    → validation_status = failed

ELSE IF any review_item requires human judgment OR warnings unresolved
    → validation_status = pending_review

ELSE IF all blocker checks passed
    → validation_status = passed
```

### 4.3 决策后果

| validation_status | Product Asset generation_status | product_assets 持久化 | 下一步 |
|-------------------|--------------------------------|----------------------|--------|
| `passed` | 可更新为 `completed` | ✅ 允许追加/更新 JSON | 进入 Feedback 链 |
| `failed` | 保持 `failed` 或 `generated` | ❌ 禁止 | 保留 trace；PR 保持 approved；可重试生产 |
| `pending_review` | 保持 `quality_checking` | ❌ 禁止 | 人工复核后重新提交验收 |

### 4.4 与 Product Asset Lifecycle 对齐

| Validation Gate 结果 | Product Asset Lifecycle 过渡 |
|---------------------|------------------------------|
| CF 产出草稿 | → `generated` |
| Validation Gate 执行中 | → `quality_checking` |
| `passed` | → `completed` |
| `failed` | → `failed`（含 `failure_reason`） |
| `pending_review` | 保持 `quality_checking` |

---

## 5. Relationship（对象关系）

### 5.1 关系链

```
Production Request（1）
    ↓ 授权
Production Request Approval（1）
    ↓ 触发
Content Factory Output（1 次 Pilot 生产）
    ↓ 映射
Product Asset Object 草稿（1）
    ↓ 验收
Product Asset Validation（1+ — 可重试验收）
    ↓ passed 后
Product Asset Object 持久化（commercial_assets/product_assets/）
    ↓
Feedback Object（market / customer / sales / quality）
    ↓
Experiment Evaluation（validation_goal 验证）
```

### 5.2 实体关系表

| 源 Object | 关系 | 目标 Object |  cardinality |
|-----------|------|-------------|--------------|
| Production Request | authorizes | Product Asset | 1 : 0..1（Pilot 单次） |
| Product Asset 草稿 | validated_by | product_asset_validation | 1 : 1..N |
| product_asset_validation | admits_to | product_assets JSON | passed → 1 |
| Product Asset | receives | Feedback | 1 : N |
| Experiment | context_for | Validation Gate | 只读 validation_goal |

### 5.3 未来 commercial_assets 目录扩展

```
commercial_assets/
├── production_requests/              ← 已有
├── production_request_reviews/       ← 已有
├── product_assets/                   ← 【未来】passed 后写入
│   └── product_assets_v1.json
└── product_asset_validations/        ← 【未来】验收记录
    └── product_asset_validations_v1.json
```

**规则：** `failed` / `pending_review` 的 Validation 记录**可**写入 validations 数据集，但 **不得** 写入 `product_assets`。

---

## 6. Module Responsibility（模块职责）

| 模块 | Validation Gate 相关职责 | 禁止 |
|------|-------------------------|------|
| **11_CONTENT_FACTORY** | 生成 artifact；产出 QualityAgent 结果；Pipeline trace | 决定 Product Asset 是否入库；修改 Experiment |
| **Adapter（output_mapper）** | 产出 Product Asset **草稿** dict | 绕过 Validation Gate 直接写 product_assets |
| **Product Asset Validation Gate** | 执行 §3 检查清单；产出 validation 对象；裁决 passed/failed | 重新生产；修改 PR；商业选品 |
| **3_DECISION** | **不参与** 文件验收 | 在 Validation Gate 阶段做 publish/skip 裁决 |
| **2_COGNITION** | **未来** 读取 validation 结果用于学习模式 | MVP Phase 1 不参与验收 |
| **7_MEMORY** | **未来** 保存验证结果摘要、event_log | MVP Phase 1 不强制 |
| **0_START** | **未来** Phase 5+ 可调度 Validation Gate Runtime | Pilot 阶段不参与 |

### 6.1 与 QualityAgent / ReleaseGateAgent 协作

| Agent / Gate | 阶段 | Validation Gate 消费其产出 |
|--------------|------|---------------------------|
| QualityAgent | 生产中 | `quality_score`, `quality_result`, checklist |
| ReleaseGateAgent | 生产中 | `release_status` — 参考项，非入库充分条件 |
| PackagingAgent | 生产中 | `bundle_path` — Artifact Validation 可选检查 |
| **Validation Gate** | 生产后 | 综合 CF Output + PR 规格 → 入库裁决 |

---

## 7. Future Runtime Connection（未来 Runtime 连接）

### 7.1 当前状态

| 项 | 状态 |
|----|------|
| Validation Gate Design | ✅ **Blueprint Completed（本任务）** |
| Validation Gate Runtime | ❌ 未实现 |
| product_assets 持久化 | ❌ 未实现 |
| product_asset_validations 数据集 | ❌ 未创建 |

### 7.2 目标 Runtime 流程（Entry 033+）

```
Content Factory Output（--execute 完成）
        ↓
Adapter output_mapper → Product Asset 草稿 dict
        ↓
Validation Gate Runtime（未来模块）
    ├── load PR.quality_requirements
    ├── run §3 checklist（artifact / contract / quality / commercial）
    ├── human_assisted confirm（Pilot）
    └── emit product_asset_validation Object
        ↓
IF validation_status == passed
    → append to commercial_assets/product_assets/product_assets_v1.json
ELSE
    → append to product_asset_validations only; block product_assets
        ↓
Feedback Layer（Entry 034+）
```

### 7.3 建议未来文件结构（Design Only — 不创建）

```
11_CONTENT_FACTORY/
├── adapter/
│   └── output_mapper.py          ← 已有 — 产出草稿
└── validation/                   ← 【未来】
    ├── __init__.py
    ├── validation_gate.py        # 主门禁逻辑
    ├── artifact_checks.py
    ├── contract_checks.py
    ├── quality_checks.py
    ├── commercial_checks.py
    └── validation_runner.py        # CLI / 编排
```

### 7.4 Entry 033 Pilot 衔接

| 步骤 | Entry | Validation Gate 角色 |
|------|-------|---------------------|
| `--execute` 生产 xlsx | 033 | CF 产出 → 草稿 Product Asset |
| 运行 Validation Gate | 033 | 对照 preq_005 checklist；`min_quality_score=0.85` |
| 人工确认 passed | 033 | `validation_method=human_assisted` |
| 写入 product_assets | 033 | **仅** validation_status=passed 后 |

---

## 8. Human Assisted Rules（人工辅助规则）

### 8.1 validation_method: human_assisted

| 含义 | 不代表 |
|------|--------|
| 人工触发验收流程 | 自动质量判断 |
| 人工确认 blocker 检查结果 | Cognition 自动裁决 |
| 人工将 pending_review → passed/failed | QualityAgent 结果自动等同入库 |

### 8.2 Pilot Phase 1 SOP（设计）

1. 执行 `adapter_runner --preq preq_20260712_005 --execute`（须单独授权）
2. 获取 Product Asset 草稿 + CF trace
3. 人工打开 xlsx，核对考勤 sheet 与公式
4. 运行 Validation Gate checklist（未来 CLI 或人工对照 §3）
5. 填写 `product_asset_validation` — `validated_by: human`
6. **仅** `passed` 时追加 `product_assets_v1.json`

### 8.3 未来自动化路径

| 阶段 | validation_method | 说明 |
|------|-------------------|------|
| MVP Phase 1 | `human_assisted` | 本 Design 默认 |
| Phase 2+ | `system_assisted` | 自动 artifact/contract/quality 检查 + 人工 spot check |
| Phase 3+ | `automated` | Cognition / Quality Agent 读取结果学习；仍保留 blocker 规则 |

---

## 9. Version Strategy（版本策略）

### 9.1 Validation Gate Version

| 版本 | 范围 | 当前 |
|------|------|------|
| **Validation Gate Version** | 检查清单、决策规则、validation object schema | **1.0** |
| **Product Asset Contract Version** | Product Asset Object schema | 1.0（独立） |
| **Database Version** | 未来 `product_assets` / `product_asset_validations` 表 | Pending（独立） |
| **Runtime Version** | 11_CONTENT_FACTORY / Adapter 代码 | 独立演进 |

### 9.2 版本独立原则

- Validation Gate **minor** 变更（新增 warning 级 check）**不强制** Product Asset Contract major 升级
- Product Asset Contract **major** 变更须同步更新 Contract Validation checklist
- Runtime 实现版本与 Gate Design 版本**解耦** — 文档先行

### 9.3 变更类型

| 变更 | 级别 | 示例 |
|------|------|------|
| 新增 blocker check | minor（1.x） | 增加 `artifact.virus_scan` |
| validation_status 枚举变更 | major（2.0） | 增加 `deferred` |
| review_items schema 变更 | minor + 文档 | 增加 `evidence_path` |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Product Asset Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md` |
| Content Factory Integration Design | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md` |
| Adapter Implementation Plan | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md` |
| Adapter Architecture Audit | `docs/07_AUDIT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_ARCHITECTURE_AUDIT.md` |
| Production Request Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCTION_REQUEST_CONTRACT.md` |

---

**Blueprint ≠ Implementation。** **Design Completed ≠ Runtime Connected。** **Validation Gate Completed ≠ Production Started。** 本文档完成 Product Asset Validation Gate v1 设计；Validation Gate Runtime、product_assets 实例、Pilot 生产均 **Pending**，须 Entry 033+ 单独授权后实施。
