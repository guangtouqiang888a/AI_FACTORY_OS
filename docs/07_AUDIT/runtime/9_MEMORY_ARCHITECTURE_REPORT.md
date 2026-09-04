# Memory Architecture Report

> Entry 038-A | 7_MEMORY 与记忆系统设计审计

---

## 存储位置总览

| 域 | 路径 | Python 模块 | 用途 |
|----|------|-------------|------|
| OS 运行时记忆 | `7_MEMORY/` | `memory_core.py` | pattern, strategy, policy, events |
| OS 执行审计 | `logs/execution_hash.log` | memory_core.log_execution_hash | DAG node hash |
| CF 产品记忆 | `11_CONTENT_FACTORY/storage/product_memory.json` | ContentPipeline._save_product | 产品生产历史 |
| 商业资产 | `commercial_assets/` | 无 Python 写入 | Product Asset, Feedback 等 |
| Operational DB | `data/ai_factory.db` | 1_DATA/database | 市场商品与评分 |
| 核心文档记忆 | `7_MEMORY/PROJECT_CORE_MEMORY.md` | 无代码读写 | 人工/Agent 可读项目摘要 |

---

## 7_MEMORY 文件清单

| 文件 | 类型 | 代码 API | 内容摘要 |
|------|------|----------|----------|
| `memory_core.py` | Python | — | 唯一记忆逻辑模块 |
| `pattern_memory.json` | JSON | load/save via extract_pattern | 运行模式学习 |
| `strategy_memory.json` | JSON | load/update_strategy | 决策规则 |
| `runtime_policy.json` | JSON | load/save_runtime_policy | 阈值/权重/mode |
| `policy_patch.json` | JSON | save_policy_patch | 演化补丁记录 |
| `runtime_policy_snapshot.json` | JSON | save/rollback_policy_snapshot | 策略回滚 |
| `event_log.jsonl` | JSONL | write_event, get_recent_events | boot/dag/complete 事件 |
| `core_state.json` | JSON | **无引用** | LIGHTWEIGHT_RUNTIME 静态字段 |
| `PROJECT_CORE_MEMORY.md` | Markdown | config.CORE_MEMORY_PATH | 项目核心说明 |

---

## 四类概念回答

### 什么是长期记忆？

**代码事实：**

| 类型 | 位置 | 机制 |
|------|------|------|
| **OS 学习记忆** | `pattern_memory.json` + `strategy_memory.json` | 每次 `SystemController.run()` 后 extract_pattern → update_strategy |
| **策略记忆** | `runtime_policy.json` | Self-Evolution 可修改 allowed keys；immutable keys 锁定 |
| **CF 产品记忆** | `product_memory.json` | 每次 CF pipeline 成功 _save_product |
| **商业知识** | `commercial_assets/` JSON | 人工 assisted 登记 — **非 memory_core 管理** |
| **文档记忆** | `PROJECT_CORE_MEMORY.md`, `docs/` | 描述性，非 Runtime 读写 |

**结论：** 「长期记忆」在代码中 **分裂为三轨**：7_MEMORY（OS 学习）、CF storage（产品历史）、commercial_assets（商业对象）。

---

### 什么是系统状态？

| 来源 | 字段示例 | 是否 Runtime 读 |
|------|----------|-----------------|
| `core_state.json` | system_mode, active_module | ❌ 无代码引用 |
| `runtime_policy.json` | mode, threshold, evolution_step | ✅ decision/scorer/policy |
| `SystemController.last_run` | 内存 | ✅ 当次 session |
| `10_DEPLOY/service.py` | _boot_info | ✅ API status |
| `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` | Phase, Entry 状态 | 人工/Agent 读 |

**结论：** 无单一系统状态 SoT；`core_state.json` **已 orphaned**。

---

### 什么是运行数据？

| 数据 | 位置 | 生命周期 |
|------|------|----------|
| SQLite products/scores | data/ai_factory.db | 持久，采集/评分累积 |
| collection_log | DB | 每次采集 |
| event_log.jsonl | 7_MEMORY | append-only |
| execution_hash.log | logs/ | append-only |
| session_llm_cost | runtime_policy 内存字段 | 单次 run |
| CF pipeline_trace | pipeline result dict | 单次 run，部分写入 generation_log |

---

### 什么是商业资产？

**Governance Protocol 定义：** `commercial_assets/` 为 Commercial Object SoT。

**代码事实：**
- Python **不自动写入** commercial_assets（adapter output_mapper、validator 注释确认）
- Product Asset 物理文件在 `11_CONTENT_FACTORY/artifacts/` + JSON 登记在 `product_assets_v1.json`
- Pilot 副本在 `commercial_assets/pilot_outputs/`

**与 7_MEMORY 边界：** ✅ 隔离 — memory_core 不读写 commercial_assets

---

## 是否存在重复记录？

| 重复对 | 详情 | 严重度 |
|--------|------|--------|
| product_memory.json ↔ product_assets_v1.json | 同 product_id 8523329941d4 两处 | P1 |
| product_memory.json ↔ CF artifacts/ | 物理路径交叉引用 | 预期 |
| pattern_memory ↔ event_log | 不同粒度，非重复 | — |
| core_state.json ↔ runtime_policy | 语义重叠（系统 mode）但无代码同步 | P2 |
| PROJECT_CORE_MEMORY.md ↔ docs/PROJECT_STATUS | 文档层重复 | P3 预期 |

---

## memory_core API 完整性

| 函数 | 调用者 |
|------|--------|
| init_memory | SystemController.boot |
| write_event / get_recent_events | controller, policy, evolution |
| extract_pattern / update_strategy | controller.run |
| load/save_runtime_policy | policy_engine, decision, scorer |
| save_policy_patch / rollback_policy_snapshot | self_evolution |
| log_execution_hash | execution_runtime |
| enforce_immutable_policy | 内部 |

**不存在：** `write_memory()` — `self_healing_engine.py` 错误引用

---

## CF FeedbackAgent vs commercial_assets Feedback

| 项 | CF FeedbackAgent | commercial_assets/feedback |
|----|------------------|----------------------------|
| 文件 | `agents/feedback_agent.py` | `feedback_v1.json` |
| Pipeline 接入 | ❌ | N/A |
| 内容 | stub — 销售反馈分析预留 | fbk_20260713_001 pending |
| 关系 | **无连接** | 独立商业对象 |

---

## 设计文档 vs 实现

| 设计（docs） | 实现 |
|--------------|------|
| COGNITION Agent Architecture | 2_COGNITION 空 |
| DATA_INTELLIGENCE_BLUEPRINT | 1_DATA + 3_DECISION 部分实现 |
| MEMORY in Governance Protocol | 7_MEMORY 仅 OS 域 |
| Feedback Object Contract | JSON 实例，无 Runtime writer |

---

## 结论

1. **7_MEMORY 对 Core OS 有效且被积极使用**
2. **Commercial / CF 记忆不在 7_MEMORY 治理范围内** — 符合 Protocol 意图，但 product 重复需治理
3. **core_state.json 应归档或删除**（需 Entry 授权，本次审计不修改）
4. **长期记忆无统一抽象** — 三轨并行
