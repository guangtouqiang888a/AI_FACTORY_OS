# AI_FACTORY_OS Validation Gate Integration Plan v1

> Entry 038-B | Validation Gate Architecture Alignment | 2026-07-13  
> **状态：Blueprint Completed — 接入计划，非 Runtime 修改**

**原则：** Design ≠ Production · 本 Entry **不修改** Adapter Pipeline

---

## 1. 当前状态确认（代码事实）

### 1.1 ProductAssetValidator 实现

| 项 | 状态 |
|----|------|
| 文件 | `11_CONTENT_FACTORY/validation/product_asset_validator.py` |
| 类 | `ProductAssetValidator.validate()` |
| 行为 | 只 check，不写 commercial_assets |
| 测试 | `validation/test_product_asset_validator.py` — 历史 Entry 5/5 PASS |

### 1.2 Adapter 调用链

**文件：** `11_CONTENT_FACTORY/adapter/adapter_runner.py`

```
ProductionRequestLoader.load_input_package()
  → ApprovalGate.validate()
  → input_mapper.map_production_request_to_input()
  → ContentPipeline.run_from_production_request()
  → output_mapper.map_pipeline_result_to_product_asset()
```

**确认：** `adapter_runner.py` **无** `ProductAssetValidator` import 或调用。

### 1.3 Pilot 实际 Validation 路径

| 步骤 | 方式 |
|------|------|
| Entry 033-B1 生产 | Adapter `--execute` |
| Validation 记录 | **人工/Entry** 写入 `product_asset_validations_v1.json` |
| Validator Runtime | 可独立调用，**非 Adapter 强制步骤** |

**结论：** Validation Gate **Implementation Completed** ≠ **Adapter Runtime Connected**

---

## 2. 目标接入架构

```
Adapter.run_adapter()
  ↓
ApprovalGate.validate()
  ↓
ContentPipeline.run_from_production_request()
  ↓
output_mapper.map_pipeline_result_to_product_asset()  → product_asset_draft
  ↓
【未来接入点 A】ProductAssetValidator.validate(product_asset_draft)
  ↓
  ├─ passed → 返回 draft + validation_result（仍不写 commercial_assets，除非 Entry 授权）
  └─ failed → adapter_status=error, 阻断后续人工登记
```

---

## 3. 推荐接入位置

### 接入点 A（推荐）— Adapter Runner 层

**文件：** `adapter_runner.py` — `run_adapter()` 内，`map_pipeline_result_to_product_asset()` 之后

**理由：**
- 单一编排入口；与 Approval Gate 对称
- 不修改 `ContentPipeline.run()` / `run_from_production_request()` 行为
- 不破坏 Legacy keyword 路径
- dry_run 时可 skip validation 或仅做 contract check

**伪代码（设计 only）：**

```python
product_asset_draft = map_pipeline_result_to_product_asset(...)
validation_result = None
if not dry_run and pipeline_result.get("status") == "ok":
    validator = ProductAssetValidator(min_quality_score=...)
    validation_result = validator.validate(product_asset_draft)
    if validation_result.get("validation_status") != "passed":
        return {"adapter_status": "validation_failed", ...}
```

---

### 接入点 B — Output Mapper 层

**文件：** `output_mapper.py`

**理由：** 映射后立即校验字段完整性  
**风险：** 混合 map + validate 职责；output_mapper 注释强调「不写 commercial_assets」，扩展需谨慎

**结论：** 次选；优先 Adapter Runner

---

### 接入点 C — Content Pipeline 内 release_gate 之后

**文件：** `content_pipeline.py`

**理由：** 生产质量与 validation 同一事务  
**风险：** **违反 Entry 约束** — 修改 pipeline 行为；影响 Legacy 与 experiment path  
**结论：** **不推荐** 在收敛 Phase C 之前实施

---

## 4. 接入条件与门禁

| 条件 | 说明 |
|------|------|
| Pilot 保护 | preq_20260712_005 回归测试必须通过 |
| dry_run | 默认不跑 full artifact validation |
| commercial_assets 写入 | 仍须单独 Entry 授权 — Validator 不自动写 JSON |
| 阈值 | 从 PR `quality_requirements.min_quality_score` 传入 |
| validation_context | output_mapper 已提供 — Validator 可消费 |

---

## 5. 测试计划（未来 Entry）

1. 扩展 `adapter/regression_test_v1.py` — mock validator pass/fail  
2. Pilot preq_005 dry_run + execute 对比  
3. 确认 8523329941d4 历史记录不受影响  

---

## 6. 与 Unified Architecture 关系

Validation Gate 位于 **Content Factory → Commercial Asset Layer** 之间：

```
Content Factory (artifact 生产)
  ↓
Validation Gate（质量/契约验收）
  ↓
Commercial Asset Layer（Product Asset 登记 — human_assisted / Entry 授权）
```

---

## 7. 本 Entry 操作

- ✅ 确认 Adapter **未** 强制调用 Validator  
- ❌ **未修改** adapter_runner / validator / pipeline  
- ✅ 输出接入计划供 Phase C 使用
