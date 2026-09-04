# Content Factory Reality Report

> Entry 038-A | 11_CONTENT_FACTORY 专项审计

---

## 1. Legacy Pipeline（keyword 入口）

### 入口确认

| 项 | 事实 |
|----|------|
| 文件 | `11_CONTENT_FACTORY/pipeline/content_pipeline.py` |
| 方法 | `ContentPipeline.run(keyword, platform="xianyu")` |
| CLI | `python content_pipeline.py [keyword]`，默认 keyword=`办公PPT模板` |

### 调用顺序（代码 line 106–201）

```
market.execute({"keyword"})
  ↓ status != ok → _fail return
creator.execute({keyword, market, platform, market_requirement})
  ↓
product_generator.execute({product, keyword, product_type})
  ↓
validate_artifacts(product_id, artifact_files, artifact_path)
  ↓ passed=false → error return
quality.execute({product, artifacts})
  ↓
packaging.execute({keyword, product, quality})
  ↓
release_gate.execute({product, quality, packaging, artifacts})
  ↓
_save_product(result) → storage/product_memory.json
```

### MarketAgent 实际行为

- **非真实市场 API** — 基于 keyword 字符串匹配 `_CATEGORY_HINTS` 启发式
- 输出：category, market_score (0–100), competition, recommendation
- **证据：** `market_agent.py` 无 HTTP/DB 调用

### Legacy 产物

- 目录：`11_CONTENT_FACTORY/artifacts/products/{product_id}/`
- 内存：`11_CONTENT_FACTORY/storage/product_memory.json`
- 历史记录确认：至少 2 个产品（`e601c17c6977` PPT、`8523329941d4` Excel 等）

---

## 2. Adapter Pipeline（production_request 入口）

### 入口确认

| 项 | 事实 |
|----|------|
| 文件 | `11_CONTENT_FACTORY/adapter/adapter_runner.py` |
| CLI | `--preq <production_request_id>` + optional `--execute` |
| 默认 | `dry_run=True`（无 `--execute` 时不生成交付文件） |

### 组件链

| 组件 | 文件 | 功能 | 状态 |
|------|------|------|------|
| Loader | `production_request_loader.py` | 读 commercial_assets JSON | ✅ 实现 |
| Approval Gate | `approval_gate.py` | decision=approved + pilot whitelist | ✅ 实现 |
| Input Mapper | `input_mapper.py` | PR → pipeline input_package | ✅ 实现 |
| Pipeline | `run_from_production_request()` | 跳过 MarketAgent | ✅ 实现 |
| Output Mapper | `output_mapper.py` | pipeline → product_asset draft | ✅ 实现 |
| Validation Gate | `validation/product_asset_validator.py` | Product Asset 验收 | ✅ 实现，**未接入 adapter_runner** |

### Pilot 白名单

```python
PILOT_WHITELIST = frozenset({"preq_20260712_005"})
```

- `preq_20260712_001`、`preq_20260712_004` 虽有 Approval JSON，**Adapter 默认拒绝**

### Experiment Path 差异

| 步骤 | Legacy | Adapter |
|------|--------|---------|
| MarketAgent | ✅ 执行 | ❌ skipped |
| validate_artifacts | 标准（需 pdf） | experiment 模式（excel+xlsx 规则） |
| dry_run | 不支持 | ✅ 仅 Creator |
| production_request_id | 无 | 写入 product dict |

---

## 3. Commercial Chain 连接真实性

### 链路图（代码 + JSON 交叉验证）

```
Opportunity (commercial_assets/opportunities/opportunities_v1.json)
  ↓ ID 引用（JSON only）
Experiment (experiments_v1.json) — 4 条，status=draft
  ↓ ID 引用
Production Request (production_requests_v1.json) — 3 条，status=draft
  ↓ ID 引用
Approval (production_request_reviews_v1.json) — 3 approved
  ↓ Python 读取（adapter only）
Content Factory Adapter (--preq preq_20260712_005 --execute)
  ↓
CF Artifacts (11_CONTENT_FACTORY/artifacts/products/8523329941d4/)
  ↓ 人工/Entry 写入（非 adapter 自动）
Product Asset (commercial_assets/product_assets/product_assets_v1.json) — 1 条
  ↓ ID 引用（JSON only）
Validation (product_asset_validations_v1.json) — 1 passed
  ↓ ID 引用（JSON only）
Feedback (feedback_v1.json) — 1 pending, observation_period=not_started
  ↓ ID 引用（JSON only）
Evaluation (experiment_evaluations_v1.json) — 1 pending, hypothesis_result=pending
```

### 连接状态表

| 环节 | Python 自动连接 | JSON 手动连接 | 运行时验证 |
|------|-----------------|---------------|------------|
| Opportunity → Experiment | ❌ | ✅ ID refs | JSON only |
| Experiment → PR | ❌ | ✅ ID refs | JSON only |
| PR → Approval | ❌ | ✅ ID refs | JSON only |
| Approval → CF Adapter | ✅ | ✅ | Pilot 005 only |
| CF → Product Asset JSON | ❌ | ✅ 人工登记 | 1 asset |
| Product Asset → Validation | ❌ | ✅ 人工登记 | Validator 可独立运行 |
| Product Asset → Feedback | ❌ | ✅ 人工登记 | pending |
| Feedback → Evaluation | ❌ | ✅ 人工登记 | pending |

---

## 4. Validation Gate 实际状态

- **实现：** `ProductAssetValidator.validate()` — artifact/contract/quality/commercial checks
- **测试：** `validation/test_product_asset_validator.py` — 5/5 PASS（历史 Entry 记录）
- **接入 adapter_runner：** ❌ **未调用**
- **Pilot 验证记录：** `commercial_assets/product_asset_validations/product_asset_validations_v1.json` — 1 passed

---

## 5. Agent 实现 vs Pipeline 接入

| Agent | 文件存在 | 在 run()/run_from_production_request 中 |
|-------|----------|----------------------------------------|
| MarketAgent | ✅ | Legacy only |
| CreatorAgent | ✅ | ✅ |
| ProductGeneratorAgent | ✅ | ✅ (non-dry_run) |
| QualityAgent | ✅ | ✅ |
| PackagingAgent | ✅ | ✅ |
| ReleaseGateAgent | ✅ | ✅ |
| FeedbackAgent | ✅ stub | ❌ |
| PublishAssistantAgent | ✅ | ❌ |

---

## 6. LLM 状态

- `11_CONTENT_FACTORY/llm_adapter.py`：**stub**，`NotImplementedError`
- CF 全流程 **不调用 LLM** — 规则/模板生成

---

## 7. 关键结论

1. **Content Factory 生产能力真实存在** — 可生成 xlsx/pptx/docx/pdf artifacts
2. **Commercial 链为 JSON 编排 + 人工辅助** — 非端到端 Runtime 自动化
3. **唯一 Runtime 连接的环节：** Adapter 读取 PR + Approval → 执行 Pipeline
4. **Product Asset / Validation / Feedback / Evaluation 写入** — 不在 Python 主链，为 Entry 人工资产登记
5. **Legacy `run(keyword)` 与 Commercial 链无关联**
