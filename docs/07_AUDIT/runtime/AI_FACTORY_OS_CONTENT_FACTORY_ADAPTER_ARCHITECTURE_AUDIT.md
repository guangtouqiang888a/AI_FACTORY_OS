# AI_FACTORY_OS Content Factory Adapter Architecture Audit v1

> Content Factory Adapter 架构审计 | 最后更新：2026-07-13  
> **状态：Audit Completed — 只读分析报告，未修改任何代码**

**定位：** 在 Content Factory Adapter Code Implementation 之前，对 **`11_CONTENT_FACTORY` Runtime**、**`0_START`**、**`3_DECISION`** 及设计文档进行只读审计，确认 Legacy 路径、Adapter 插入点、Output 映射与风险。

**审计依据：**

- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md)
- [docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md](../../04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md)
- [docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md](../../04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md)

**说明：** **Audit Completed ≠ Code Implemented**。**Blueprint ≠ Runtime Connected**。本报告不修改 Python、不创建 adapter、不调用 Content Factory。

---

## Executive Summary（审计结论）

| 项 | 结论 |
|----|------|
| **CF Runtime 入口** | `ContentPipeline.run(keyword, platform)` — `pipeline/content_pipeline.py` |
| **0_START 与 CF 连接** | ❌ **无直接引用** — CF 独立于 Core OS DAG |
| **3_DECISION 与 CF 连接** | ❌ **无直接引用** — Decision 基于 keyword + Legacy scores |
| **Adapter 推荐插入点** | `ContentPipeline` 新增 `run_from_production_request()`；Adapter 为独立 `adapter/` 包 |
| **Legacy 保护** | 保留 `run(keyword)` 不变；Experiment 路径 bypass MarketAgent |
| **可否进入 Adapter Code** | ✅ **可以** — 有条件；须先解决 Excel Pilot 的 artifact_validation PDF 硬门禁 |
| **关键风险** | `validate_artifacts()` 要求 `has_pdf`；QualityAgent 使用 0–100 分制 vs Contract 0–1 |

---

## §1 当前 Content Factory Runtime 入口

### 1.1 Main Pipeline

| 项 | 值 |
|----|-----|
| **主类** | `ContentPipeline` |
| **文件** | `11_CONTENT_FACTORY/pipeline/content_pipeline.py` |
| **CLI 入口** | `main()` — `python content_pipeline.py [keyword]` |
| **默认 keyword** | `"办公PPT模板"` |

### 1.2 `run()` 方法签名与行为

```python
def run(self, keyword: str, platform: str = "xianyu") -> dict
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `keyword` | str | 唯一必填业务输入 — 驱动 MarketAgent 与 Creator |
| `platform` | str | 默认 `"xianyu"` — 传入 Creator context |

**初始化 Agent（`__init__`）：**

| Agent | 类 | role |
|-------|-----|------|
| `self.market` | MarketAgent | market_analyst |
| `self.creator` | CreatorAgent | product_creator |
| `self.generator` | ProductGeneratorAgent | product_generator |
| `self.quality` | QualityAgent | quality_inspector |
| `self.packaging` | PackagingAgent | packaging_designer |
| `self.release_gate` | ReleaseGateAgent | release_gate |

### 1.3 Agent 调用顺序（Legacy）

```
1. MarketAgent.execute({"keyword": keyword}, context)
2. CreatorAgent.execute({keyword, market, platform, market_requirement}, context)
3. ProductGeneratorAgent.execute({product, keyword, product_type}, context)
4. validate_artifacts() — 模块级函数，非 Agent
5. QualityAgent.execute({product, artifacts}, context)
6. PackagingAgent.execute({keyword, product, quality}, context)
7. ReleaseGateAgent.execute({product, quality, packaging, artifacts}, context)
8. _save_product() → storage/product_memory.json
```

### 1.4 成功输出结构（`status: "ok"`）

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | str | `"ok"` |
| `product_id` | str | DigitalProduct.id（12 位 hex） |
| `artifact_path` | str | 绝对路径 `artifacts/products/{id}/` |
| `artifact_files` | list[str] | 相对路径列表 |
| `quality_score` | float | 0–100（QualityAgent） |
| `commercial_score` | float | 0–100 |
| `release_status` | str | ReleaseGate 产出 |
| `zip_path` | str | Packaging 产出 |
| `product` | dict | DigitalProduct.to_dict() |
| `artifacts` | dict | path + files + product_type |
| `quality` | dict | 完整 quality 结果 |
| `packaging` | dict | 发布包信息 |
| `release_gate` | dict | 门禁检查结果 |
| `pipeline_trace` | list[dict] | 逐步 trace |

### 1.5 失败输出结构（`status: "error"`）

```python
{"status": "error", "failed_step": str, "error": dict, "pipeline_trace": list}
```

---

## §2 Legacy Flow 分析

### 2.1 keyword 如何进入各 Agent

```
keyword (CLI / run 参数)
    ↓
MarketAgent
    input: {"keyword": keyword}
    output: {keyword, category, market_score, competition, recommendation}
    ↓
CreatorAgent
    input: {keyword, market, platform, market_requirement=recommendation}
    output: {product: DigitalProduct dict, artifacts: {artifact_path, ...}}
    ↓
ProductGeneratorAgent
    input: {product, keyword, product_type}
    product_type: 来自 product dict 或 keyword 启发式 (_detect_type)
    ↓
QualityAgent
    input: {product, artifacts}
    market_score: 来自 product（Creator 从 market 写入）
    ↓
PackagingAgent
    input: {keyword, product, quality}
    门禁: commercial_score >= 80
    ↓
ReleaseGateAgent
    input: {product, quality, packaging, artifacts}
```

### 2.2 MarketAgent 行为（选品层 — Experiment 路径须 bypass）

- 基于 keyword 启发式分类（ppt/excel/word 等 hint）
- 产出 `market_score`（0–100）、`recommendation` 文本
- **与商业链冲突：** 自行做市场分析，等价于选品

### 2.3 CreatorAgent 关键输入

| 字段 | Legacy 来源 | PR 路径应对 |
|------|-------------|-------------|
| `keyword` | CLI keyword | → `product_name` |
| `market` | MarketAgent 结果 | **跳过** — 人工构造 stub 或直传 PR 字段 |
| `product_type` | 可选 input | → PR `product_type` 映射为 `"Excel模板"` 等 |
| `target_customer` | 可选 input | → PR `target_customer` |
| `platform` | run 参数 | → PR `publish_channel_planned` |

**Creator 内部类型映射：** `"Excel模板"` / `"PPT模板"` 等中文 category — PR `product_type: excel` 须映射。

### 2.4 ProductGeneratorAgent 文件产出

| product_type | 主文件 | 附加 |
|--------------|--------|------|
| PPT模板 | `templates/{id}.pptx` | product_manual.pdf |
| Excel模板 | `templates/{id}.xlsx` | product_manual.pdf |
| Word模板 | `templates/{id}.docx` | product_manual.pdf |
| PDF资料 | `documents/{id}.pdf` | — |

**目录结构：** `artifacts/products/{product_id}/` — source, documents, templates, images, package

### 2.5 持久化 — Legacy 输出落点

| 存储 | 路径 | 内容 |
|------|------|------|
| product_memory.json | `11_CONTENT_FACTORY/storage/product_memory.json` | products[] + history[] |
| metadata.json | `artifacts/products/{id}/metadata.json` | 产品元数据 |

**无** `production_request_id` / `source_experiment_id` 追溯字段。

---

## §3 Adapter 插入点分析

### 3.1 推荐架构

```
commercial_assets/production_requests_v1.json
commercial_assets/production_request_reviews_v1.json
        ↓
adapter/production_request_loader.py
        ↓
adapter/approval_gate.py
        ↓
adapter/input_mapper.py → Integration Input Package
        ↓
ContentPipeline.run_from_production_request(input_package)  ← 新增方法
        ↓
adapter/output_mapper.py → Product Asset Object
        ↓
commercial_assets/product_assets/product_assets_v1.json（未来）
```

### 3.2 推荐插入点：`ContentPipeline` 新 метод

**位置：** `11_CONTENT_FACTORY/pipeline/content_pipeline.py` — **新增** `run_from_production_request()`

**理由：**

| 理由 | 说明 |
|------|------|
| 最小侵入 | 复用现有 Agent 实例与 `_fail` / `_save_product` |
| Legacy 隔离 | `run(keyword)` **不修改** |
| 单类入口 | Adapter 只调 Pipeline，不直接调各 Agent |
| 与 Plan 一致 | Adapter Plan §4.1 设计 |

### 3.3 `run_from_production_request()` 伪代码结构（设计 — 未实现）

```python
def run_from_production_request(self, input_package: dict) -> dict:
    context = {
        "production_request_id": input_package["production_request_id"],
        "source_experiment_id": input_package["source_experiment_id"],
        "approval_id": input_package["approval_id"],
        "platform": ...,
        "validation_goal": input_package["validation_goal"],  # 只读
    }
    trace = []
    # SKIP MarketAgent
    creator_out = self.creator.execute(mapped_creator_input, context)
    # ... generator → validation → quality → packaging → release_gate
    # context 附带 PR 字段；_save_product 可扩展或 bypass
    return result  # 同 run() 结构 + PR 追溯字段
```

### 3.4 0_START / 3_DECISION 影响

| 模块 | 审计结果 | Adapter 阶段影响 |
|------|----------|------------------|
| **0_START** | `controller.run(task)` 走 Planner → ExecutionRuntime DAG；**无 CF import** | **无影响** — Pilot 不经过 0_START |
| **3_DECISION** | `decide_scored(keyword, products)` — Legacy 评分决策；**无 CF import** | **无影响** — PR 已在 commercial_assets 批准 |
| **7_MEMORY** | event_log 可记录 boot/dag；CF 独立 | Pilot 可选写 event — 非必须 |

**结论：** Adapter Code Implementation **Phase 2 不需要修改 0_START 或 3_DECISION**。

### 3.5 Legacy 不受影响证明

| 检查项 | 状态 |
|--------|------|
| `run(keyword)` 方法体保留 | 设计约束 |
| `main()` CLI 仍调 `run(keyword)` | 不变 |
| MarketAgent 仍仅在 Legacy 路径调用 | Experiment 路径 skip |
| `product_memory.json` 格式不变 | Legacy 条目无 PR 字段 |
| 0_START / 3_DECISION 零变更 | 已确认无引用 |

---

## §4 Output Mapping 分析

### 4.1 CF 当前输出 → Product Asset Object

| CF Output 字段 | Product Asset Contract 字段 | 映射注意 |
|---------------|---------------------------|----------|
| `product_id` | `product_asset_id` | 可直接复用或加 `passet_` 前缀 |
| PR.`production_request_id` | `source_production_request_id` | 来自 input_package |
| PR.`source_experiment_id` | `source_experiment_id` | 来自 input_package |
| Review.`approval_id` | `approval_id` | 来自 input_package |
| `product.title` | `product_name` | |
| PR.`product_type` | `product_type` | ppt/excel/word/pdf |
| 推导 | `asset_category` | office_template |
| `artifact_path` | `artifact_information.artifact_path` | |
| 主文件 | `artifact_information.primary_file` | 从 artifact_files 解析 |
| 后缀 | `artifact_information.file_type` | xlsx/pptx/... |
| `artifact_files` | `artifact_information.artifact_files` | |
| `pipeline_trace` | `artifact_information.generation_log_ref` | 或内嵌 summary |
| `quality.quality_score` | `quality_score` | **须归一化 0–1**（CF 为 0–100） |
| `quality` 全对象 | `artifact_information.quality_result` | |
| 成功/失败 | `generation_status` | completed / failed |
| 时间 | `created_at`, `updated_at` | |

### 4.2 quality_score 尺度差异（Implementation 须处理）

| 层 | 尺度 |
|----|------|
| QualityAgent 产出 | **0–100** |
| Product Asset Contract | **0.0–1.0** |
| PR quality_requirements.min_quality_score | **0.85**（0–1 语义） |

**建议：** Adapter output_mapper 做 `quality_score / 100.0`；Quality 门禁比较时统一尺度。

### 4.3 metadata.json 与 Product Asset 关系

`ArtifactManager.generate_metadata()` 写入：

```json
{
  "product_id", "title", "category", "product_type",
  "target_customer", "status", "artifact_path", "created_at", "directories"
}
```

**缺口：** 无 `production_request_id` — Implementation 时扩展 metadata 或仅写 commercial_assets Product Asset JSON。

---

## §5 风险分析

### 5.1 Controller 调度影响

| 风险 | 级别 | 说明 |
|------|------|------|
| 0_START 调度冲突 | **低** | CF 与 Core OS 物理隔离；Pilot CLI 独立运行 |
| 未来 0_START 接入 | **中** | Phase 5 须新 DAG 节点 — 非本次范围 |

### 5.2 Agent 调用风险

| 风险 | 级别 | 说明 | 缓解 |
|------|------|------|------|
| **artifact_validation 要求 PDF** | **高** | `passed = len(real) > 0 and has_pdf` — Excel 主交付为 xlsx，虽 Generator 会产 manual pdf，但逻辑耦合 PPT 场景 | Pilot 前评估：确认 xlsx+manual.pdf 能否通过；或 Experiment 路径使用独立 validation |
| MarketAgent bypass 后 market_score=0 | **中** | QualityAgent 公式含 market_score 权重 30% | Experiment 路径注入 PR derived stub score 或调权重 |
| product_type 映射错误 | **中** | PR `excel` → 须映射 `"Excel模板"` | input_mapper 显式映射表 |
| Packaging commercial_score < 80 | **中** | 阻断 packaging | Pilot 可能需调阈值或 PR quality_requirements 对齐 |
| Creator content outline 通用 | **低** | PR structure_outline 未传入 Generator | Phase 2 扩展 `_ppt_sections` / Excel sheets 映射 |

### 5.3 Legacy 回归风险

| 风险 | 级别 | 缓解 |
|------|------|------|
| 修改 `run()` 破坏 CLI | **高** if 改 | **禁止修改 run() 签名与 Market 步骤** |
| 共享 Agent 行为变更 | **中** | Creator/Generator 增 optional 参数，默认值保持 Legacy |
| product_memory.json 污染 | **低** | Experiment 路径可选 separate save 或带 PR 标记 |

**回归测试命令（Implementation 后）：**

```powershell
python 11_CONTENT_FACTORY/pipeline/content_pipeline.py "办公PPT模板"
```

### 5.4 文件结构风险

| 风险 | 级别 | 说明 |
|------|------|------|
| 新增 adapter/ 目录 | **低** | Additive — Plan 已设计 |
| artifacts/products/ 写入 | **低** | 现有机制复用 |
| commercial_assets 写回 | **低** | 新 JSON 文件，不改 PR 源 |

### 5.5 Pilot preq_20260712_005 专项风险

| 项 | 风险 |
|----|------|
| product_type excel → Excel模板 | 映射须 explicit |
| structure_outline 考勤明细/汇总/说明 | Generator 当前用固定 sheets 模板 — **产出可能与 PR spec 不完全一致** |
| formulas_required | Excel generator 当前仅简单 SUM — **考勤公式可能不满足 PR** |
| quality min 0.85 | 归一化后对比 |
| Pilot whitelist | Adapter 硬编码仅 preq_005 |

---

## §6 Adapter 推荐插入点（汇总）

| 层级 | 推荐位置 | 操作 |
|------|----------|------|
| **Adapter 包** | `11_CONTENT_FACTORY/adapter/` | 新建 — loader, gate, mappers, runner |
| **Pipeline 扩展** | `ContentPipeline.run_from_production_request()` | 新增 method — bypass MarketAgent |
| **CLI 扩展** | `adapter_runner.py` 或 pipeline `main` 增 flag | `--preq preq_20260712_005` |
| **不修改** | `run(keyword)`, `0_START/`, `3_DECISION/` | Legacy 保护 |

---

## §7 Legacy 保护方案

| # | 规则 |
|---|------|
| 1 | `ContentPipeline.run(keyword, platform)` **方法体不变** |
| 2 | Experiment 路径 **仅** 通过新 method 进入 |
| 3 | MarketAgent **仅** Legacy 调用 |
| 4 | Legacy 产物 **不强制** 写 Product Asset commercial_assets |
| 5 | Implementation 后 **必须** 跑 Legacy CLI 回归 |
| 6 | Adapter additive — 不删除/重命名现有 Agent |
| 7 | Pilot whitelist — 仅 preq_20260712_005 |

---

## §8 是否可以进入 Adapter Code Implementation

### 8.1 结论：**可以进入 — 有条件**

| 条件 | 优先级 | 说明 |
|------|--------|------|
| 解决 artifact_validation PDF 门禁 | **P0** | Excel Pilot 可能被现有 validation 误伤 — Implementation 时 Experiment 路径须独立 validation 或放宽 has_pdf 规则（仅 Experiment 路径） |
| 明确 product_type 映射表 | P0 | excel→Excel模板, ppt→PPT模板 |
| quality_score 归一化 | P1 | 0–100 → 0–1 |
| structure_outline → Generator | P2 | Pilot 可先用默认 Excel 结构，后续迭代 |
| 不修改 0_START / 3_DECISION | P0 | 已确认可行 |

### 8.2 建议 Implementation 顺序

1. `adapter/approval_gate.py` + `input_mapper.py`（纯读取 commercial_assets）
2. `ContentPipeline.run_from_production_request()` — skip Market，Experiment validation
3. `adapter/output_mapper.py` — Product Asset dict
4. `adapter_runner.py` — CLI + Pilot whitelist
5. Legacy 回归测试
6. Pilot 执行 preq_005（**单独授权**）
7. `commercial_assets/product_assets/product_assets_v1.json`

---

## §9 审计文件清单

| 路径 | 审计范围 |
|------|----------|
| `11_CONTENT_FACTORY/pipeline/content_pipeline.py` | ✅ 主 Pipeline |
| `11_CONTENT_FACTORY/agents/*.py` | ✅ 全部 Agent |
| `11_CONTENT_FACTORY/schemas/product_schema.py` | ✅ DigitalProduct |
| `11_CONTENT_FACTORY/artifacts/artifact_manager.py` | ✅ 产物路径 |
| `11_CONTENT_FACTORY/storage/product_memory.json` | ✅ Legacy 存储 |
| `0_START/controller.py` | ✅ 无 CF 引用 |
| `3_DECISION/decision_engine.py` | ✅ 无 CF 引用 |

---

## 相关文档

| 文档 | 路径 |
|------|------|
| Integration Design | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_INTEGRATION_DESIGN.md` |
| Adapter Plan | `docs/04_BLUEPRINT/runtime/AI_FACTORY_OS_CONTENT_FACTORY_ADAPTER_IMPLEMENTATION_PLAN.md` |
| Product Asset Contract | `docs/04_BLUEPRINT/contract/AI_FACTORY_OS_PRODUCT_ASSET_CONTRACT.md` |

---

**Audit Completed ≠ Code Implemented.** **Blueprint ≠ Runtime Connected.** 本审计完成；Adapter 代码、Pilot 生产均未执行。
