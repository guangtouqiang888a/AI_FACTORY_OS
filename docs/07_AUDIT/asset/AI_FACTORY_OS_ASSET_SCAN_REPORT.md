# Asset Scan Report

> 项目资产扫描报告 | 扫描日期：2026-07-07  
> **范围：** 只读扫描，未修改、未删除任何文件

---

## Scan Summary

| 指标 | 数量 |
|------|------|
| 根级目录 | 18（含 `.cursor`） |
| 审计重点目录 | 6 |
| `output/` 文件 | 20 |
| `logs/` 文件 | 4 |
| `7_MEMORY/` 数据文件 | 9（含 1 个 .py） |
| `11_CONTENT_FACTORY/artifacts/products/` 产品批次 | 2 |
| `__pycache__/` 目录 | 11 |
| Reserved 空目录 | 3（`2_COGNITION`、`4_PRODUCT`、`5_CONTENT`） |

**根级 `artifacts/` 目录：** 不存在。产物目录为 `11_CONTENT_FACTORY/artifacts/`。

---

## Root Directory Structure

| Directory | Files (approx) | Default Status | Role |
|-----------|----------------|----------------|------|
| `0_START/` | 10 .py + cache | Active | Core OS |
| `1_DATA/` | 3 .py + cache | Active | Data Collection |
| `2_COGNITION/` | 0 | Reserved | Market Intelligence（空） |
| `3_DECISION/` | 5 .py + cache | Active | Decision Engine |
| `4_PRODUCT/` | 0 | Reserved | Product Definition（空） |
| `5_CONTENT/` | 0 | Reserved | Content Knowledge（空） |
| `6_EXECUTION/` | 2 .py + cache | Active | Execution / Publisher |
| `7_MEMORY/` | 9 files + cache | Active | System Memory |
| `8_CONFIG/` | 1 .py + cache | Active | Configuration |
| `9_PRODUCT/` | 5 .py | Experimental / Frozen | Early SaaS layer |
| `10_DEPLOY/` | 8+ files + cache | Active (Frozen) | Deployment |
| `11_CONTENT_FACTORY/` | 30+ .py + artifacts | Active | Digital Product Factory |
| `data/` | db + 1 sample xlsx | Active / Experimental | Database + raw sample |
| `docs/` | 9+ .md | Active | Project Context Layer |
| `logs/` | 4 | Temporary | Runtime logs |
| `output/` | 20 .json | Temporary | Publish simulation output |
| `.cursor/` | rules | Active | Cursor IDE config |

**根级文件：** `README.md`（0 bytes，空）、`requirements.txt`、`.gitignore`

---

# output/

## Directory

`output/` — 本地模拟发布输出目录

**Created By:** `6_EXECUTION/publisher.py`  
**Referenced By:** `8_CONFIG/config.py` → `OUTPUT_DIR`  
**Git Status:** `.gitignore` 已排除

## Files Found

| 文件模式 | 数量 | 大小约 |
|----------|------|--------|
| `publish_虚拟资料_*.json` | 17 | ~244 bytes each |
| `publish_test_*.json` | 1 | 236 bytes |
| `publish_virtual_*.json` | 1 | 239 bytes |
| `skip_虚拟资料_*.json` | 1 | 93 bytes |

**时间范围：** 2026-07-05 ~ 2026-07-07

## Possible Status

**Temporary**

## Recommendation

Review before deletion. 可保留最近 1–2 条用于调试对比；历史批次建议 **Archive** 至 `archive/output/`（未来清理阶段执行，本阶段不操作）。

---

# data/

## Directory

`data/` — 数据存储层

**Referenced By:** `8_CONFIG/config.py` → `DATA_DIR`, `DB_PATH`, `RAW_XIANYU_DIR`

## Files Found

| File Path | Size | Last Modified |
|-----------|------|---------------|
| `data/ai_factory.db` | 81,920 bytes | 2026-07-07 |
| `data/raw/xianyu/2026-07-04/虚拟资料_sample.xlsx` | 5,048 bytes | 2026-07-04 |

## Possible Status

| 文件 | Status |
|------|--------|
| `ai_factory.db` | **Active** — 生产 SQLite 数据库 |
| `raw/xianyu/.../虚拟资料_sample.xlsx` | **Experimental** — 早期采集样本 |

## Recommendation

**Keep** — 数据库为 Active 生产资产；raw 样本标记 Experimental，清理前须确认 `1_DATA/collector.py` 是否仍依赖。

---

# logs/

## Directory

`logs/` — 运行时日志

**Referenced By:** `8_CONFIG/config.py` → `LOGS_DIR`, `EXECUTION_HASH_LOG_PATH`  
**Git Status:** `.gitignore` 已排除

## Files Found

| File Path | Size | Purpose |
|-----------|------|---------|
| `logs/execution_hash.log` | 8,892 bytes | 执行 hash 审计链 |
| `logs/deploy/metrics.json` | 210 bytes | 部署 metrics 快照 |
| `logs/deploy/requests.log` | 465 bytes | HTTP 请求日志 |
| `logs/deploy/trace.jsonl` | 1,102 bytes | 部署 trace 链 |

## Possible Status

**Temporary**（可再生，但运行调试有价值）

## Recommendation

**Keep** 当前文件用于追溯；定期轮转可 **Archive** 旧日志。本阶段不删除。

---

# 11_CONTENT_FACTORY/artifacts/

## Directory

`11_CONTENT_FACTORY/artifacts/` — Content Factory 产物管理

**Code:** `artifact_manager.py`, `bundle_builder.py`  
**Products Root:** `artifacts/products/{product_id}/`

## Files Found

### 代码（Active）

| File | Status |
|------|--------|
| `artifact_manager.py` | Active |
| `bundle_builder.py` | Active |
| `__init__.py` | Active |

### 产品批次

#### Product `75f2feac9b04`（2026-07-07 14:16）

| 路径 | 类型 |
|------|------|
| `metadata.json` | 产品元数据 |
| `documents/使用说明.md` | 说明文档 |
| `templates/ppt_structure.json`, `slide_outline.md` | PPT 结构 |
| `package/publish_package/*` | 发布包装（title, description, pricing 等） |
| `package/publish_assistant/*` | 发布清单与平台指南 |

**Note:** 无 `final_product.zip`；可能为中间态或未完成 release_gate。

#### Product `e601c17c6977`（2026-07-07 14:40）

| 路径 | 类型 |
|------|------|
| `metadata.json` | 产品元数据 |
| `templates/e601c17c6977.pptx` | PPT 产物（34,707 bytes） |
| `documents/product_manual.pdf` | PDF 手册 |
| `images/cover_placeholder.txt` | 封面占位符 |
| `package/final_product.zip` | 最终交付包（30,980 bytes） |
| `package/publish_package/*` | 发布包装 |
| `package/publish_assistant/publish_checklist.md` | 发布清单 |

## Possible Status

| 类别 | Status |
|------|--------|
| 代码 | Active |
| `75f2feac9b04` | Experimental / Active — 未完成 zip 的实验批次 |
| `e601c17c6977` | Active — 完整生产交付示例 |
| `cover_placeholder.txt` | Temporary — 视觉占位，非最终封面 |
| `__pycache__/` | Temporary |

## Recommendation

**Keep** 两个 product_id 作为生产参考样本；`75f2feac9b04` 标记 Review（是否补跑 release_gate 或 Archive）。占位符文件保留至封面生成接入真实模型。

---

# 11_CONTENT_FACTORY/（非 artifacts）

## Directory

Content Factory 生产层代码与配置

## Key Assets

| Path | Status | Referenced By |
|------|--------|---------------|
| `agents/*.py` | Active | `content_pipeline.py` |
| `pipeline/content_pipeline.py` | Active | Content Factory 主链 |
| `storage/product_memory.json` | Active | `content_pipeline.py` → `STORAGE_PATH` |
| `templates/product_template.json` | Active | 产品模板 |
| `artifact_generators/*.py` | Active | PPT/XLSX/DOCX/PDF 生成 |
| `llm_adapter.py` | Active | LLM 适配 |
| `requirements.txt` | Active | 依赖 |
| `README.md` | Active | 模块说明 |
| 各子目录 `__pycache__/` | Temporary | Python 自动编译 |

## Possible Status

**Active**（代码与 storage）；**Temporary**（`__pycache__`）

## Recommendation

**Keep** — 核心生产资产，禁止误删。

---

# 7_MEMORY/

## Directory

`7_MEMORY/` — OS 运行时记忆层

**Referenced By:** `memory_core.py`, `8_CONFIG/config.py`, `0_START/policy_engine.py`, `0_START/self_evolution.py`

## Files Found

| File Path | Size | Referenced By Code | Status |
|-----------|------|-------------------|--------|
| `memory_core.py` | Active code | 全 OS Memory 链 | Active |
| `event_log.jsonl` | 35,889 bytes | `memory_core.py` | Active |
| `pattern_memory.json` | 5,992 bytes | `memory_core.py` | Active |
| `strategy_memory.json` | 1,343 bytes | `memory_core.py` | Active |
| `runtime_policy.json` | 522 bytes | `config.py`, `policy_engine.py` | Active |
| `policy_patch.json` | 130 bytes | `config.py`, `self_evolution.py` | Active |
| `runtime_policy_snapshot.json` | 621 bytes | `config.py` | Active |
| `PROJECT_CORE_MEMORY.md` | 4,005 bytes | `config.py` → `CORE_MEMORY_PATH` | Active |
| `core_state.json` | 242 bytes | **无引用** | **Deprecated** |
| `__pycache__/memory_core.cpython-311.pyc` | 19,478 bytes | — | Temporary |

## Possible Status

主 Memory 文件：**Active**  
`core_state.json`：**Deprecated**（疑似历史遗留）

## Recommendation

**Keep** 所有 Active Memory 文件。  
`core_state.json` → **Review before deletion**；建议标记 Deprecated，清理阶段可 Archive。

---

# 9_PRODUCT/（扩展扫描）

## Directory

`9_PRODUCT/` — 早期 SaaS/API 商业化层（Module Registry: Frozen）

## Files Found

| File | Status |
|------|--------|
| `api_server.py` | Experimental / Frozen |
| `auth.py` | Experimental / Frozen |
| `pricing_engine.py` | Experimental / Frozen |
| `schemas.py` | Experimental / Frozen |
| `service_layer.py` | Experimental / Frozen |

## Possible Status

**Experimental / Frozen** — 未在 `8_CONFIG/config.py` 的 `ACTIVE_MODULES` 中

## Recommendation

**Keep** — 历史设计参考；不删除，不接入主链直至 Phase 2 SaaS 规划确认。

---

# __pycache__ / Compiled Assets

## Files Found

11 个 `__pycache__/` 目录，分布于：

- `0_START/`（11 files）
- `10_DEPLOY/`（7 files）
- `1_DATA/`（3 files）
- `3_DECISION/`（5 files）
- `6_EXECUTION/`（2 files）
- `7_MEMORY/`（1 file）
- `8_CONFIG/`（1 file）
- `11_CONTENT_FACTORY/agents/`（8 files）
- `11_CONTENT_FACTORY/artifacts/`（2 files）
- `11_CONTENT_FACTORY/artifact_generators/`（4 files）
- `11_CONTENT_FACTORY/schemas/`（1 file）
- `11_CONTENT_FACTORY/visual/`（1 file）

## Possible Status

**Temporary**

## Recommendation

**Keep** 或忽略 — `.gitignore` 已排除；清理不影响源码，可安全删除但非本阶段任务。

---

# Suspected Legacy / Review Items

| File / Directory | Reason | Suggested Status | Action |
|------------------|--------|------------------|--------|
| `7_MEMORY/core_state.json` | 无 Python 代码引用 | Deprecated | Review → Archive |
| `output/*.json`（20 文件） | 模拟发布累积输出 | Temporary | Review → Archive 旧批次 |
| `data/raw/xianyu/.../虚拟资料_sample.xlsx` | 早期样本，2026-07-04 | Experimental | Keep / Review |
| `README.md`（根目录，0 bytes） | 空文件，无内容 | Deprecated | Review → 补写或 Remove |
| `9_PRODUCT/*.py` | Frozen 层，未接入 ACTIVE_MODULES | Experimental / Frozen | Keep |
| `2_COGNITION/`, `4_PRODUCT/`, `5_CONTENT/` | 空 Reserved 占位 | Reserved | Keep |
| `artifacts/products/75f2feac9b04/` | 无 final_product.zip | Experimental | Review |
| `cover_placeholder.txt` | 视觉占位非最终资产 | Temporary | Keep until cover gen |
| `logs/deploy/*` | 2026-07-06 单次部署快照 | Temporary | Archive when rotated |

---

# Overall Recommendations

1. **本阶段不执行任何删除** — 仅完成识别与分类
2. **优先 Review：** `7_MEMORY/core_state.json`、根目录空 `README.md`
3. **建立 archive 目录规范**（下一阶段）：`archive/output/`、`archive/logs/`、`archive/products/`
4. **更新 `.gitignore` 考虑项**（需单独审批）：`data/raw/`、`11_CONTENT_FACTORY/artifacts/products/` 是否纳入版本控制
5. **product_memory.json 与 7_MEMORY 边界** — Content Factory storage 与 OS Memory 物理分离，保持现状

---

## Related Documents

- [AI_FACTORY_OS_ASSET_AUDIT.md](AI_FACTORY_OS_ASSET_AUDIT.md)
- [AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md](AI_FACTORY_OS_ASSET_AUDIT_TEMPLATE.md)
- [AI_FACTORY_OS_MODULE_REGISTRY.md](../../01_CURRENT_STATE/AI_FACTORY_OS_MODULE_REGISTRY.md)
