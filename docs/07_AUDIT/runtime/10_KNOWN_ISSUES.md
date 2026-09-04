# AI_FACTORY_OS Known Issues

> Entry 038-A | 问题清单（代码/数据/文档证据）

---

## P0 — 严重架构风险

### ISSUE-P0-001

**ID:** ISSUE-P0-001  
**问题:** Core OS 与 Content Factory / Commercial 链 **Runtime 零连接**  
**证据:**
- 全 repo grep：`0_START` 无 `11_CONTENT_FACTORY`、`commercial_assets` import
- `config.ACTIVE_MODULES` 不含 11_CONTENT_FACTORY  
**影响:** 两套独立系统；文档「全链路生产」易误解；Commercial 实验无法触发 OS 或 CF 自动执行  
**建议方向:** Entry 授权设计 Integration Runtime 或明确永久双轨架构并更新所有 Phase 文档

---

### ISSUE-P0-002

**ID:** ISSUE-P0-002  
**问题:** 双决策 / 双数据 / 双产品语义无 Runtime 汇聚  
**证据:**
- OS: SQLite products → ScoringAgent → DecisionAgent
- Commercial: JSON Opportunity → Experiment → PR → Adapter
- `3_DECISION/decision_engine.py` 不读 commercial_assets  
**影响:** 无法从 Opportunity 自动驱动生产；市场 DB 数据不影响 Pilot 产品  
**建议方向:** 定义 Commercial Orchestrator（Blueprint）或保持人工 assisted 并在 MODULE_REGISTRY 显式标注

---

### ISSUE-P0-003

**ID:** ISSUE-P0-003  
**问题:** Database schema 与 `database.py ensure_schema()` 漂移  
**证据:**
- DB 存在 `trends`, `audit_log` 表；database.py 未创建
- `platforms` 表实际列 base_url/status vs 代码定义 id/name only
- grep：无 Python 写 trends/audit_log  
**影响:** 新环境 bootstrap  schema 不完整；audit_log 1 行来源不可追溯  
**建议方向:** Database Reality Entry — 对齐 ensure_schema 或 migration 脚本

---

## P1 — 需要整改

### ISSUE-P1-001

**ID:** ISSUE-P1-001  
**问题:** `9_PRODUCT/api_server.py` 语法无效  
**证据:** `from 0_START.controller import SystemController` — Python 非法模块名  
**影响:** 无法作为 API 入口；与 10_DEPLOY 混淆  
**建议方向:** 删除或移入 archive/；文档标注 Deprecated

---

### ISSUE-P1-002

**ID:** ISSUE-P1-002  
**问题:** `0_START/self_healing_engine.py` 不可运行  
**证据:** `from 7_MEMORY.memory_core import write_memory` — 语法错误 + API 不存在（应为 write_event）  
**影响:** 自愈演示入口损坏  
**建议方向:** 修复 import 或移出 ACTIVE 入口列表

---

### ISSUE-P1-003

**ID:** ISSUE-P1-003  
**问题:** 2_COGNITION 空目录 vs CF MarketAgent 职责重叠  
**证据:** `2_COGNITION/` 0 files；`market_agent.py` 实现 market analysis  
**影响:** 模块边界冲突 MB-001  
**建议方向:** 明确 MarketAgent 定位；更新 MODULE_REGISTRY 职责矩阵

---

### ISSUE-P1-004

**ID:** ISSUE-P1-004  
**问题:** commercial_assets JSON status 字段与下游不同步  
**证据:**
- PR 三条 `status: draft`；Approval 三条 approved
- Experiment exp_005 `status: draft`；Product Asset 已 completed  
**影响:** ZIP 审计误判；Governance State Review 失败  
**建议方向:** Entry 授权 JSON status 同步（非本次范围）

---

### ISSUE-P1-005

**ID:** ISSUE-P1-005  
**问题:** ProductAssetValidator 未接入 Adapter 主链  
**证据:** `adapter_runner.py` 无 validator import；output_mapper 注释不写 commercial_assets  
**影响:** Validation Gate Implementation ≠ Adapter Runtime Connected  
**建议方向:** Adapter v2 集成 validate 步骤或文档明确人工 validation 流程

---

### ISSUE-P1-006

**ID:** ISSUE-P1-006  
**问题:** product 记忆三处存储  
**证据:** `product_memory.json` + `product_assets_v1.json` + `artifacts/products/`  
**影响:** Source of Truth 模糊（Governance Protocol §2 冲突）  
**建议方向:** 定义 canonical 层级：artifacts=文件, product_assets=商业登记, product_memory=cache

---

### ISSUE-P1-007

**ID:** ISSUE-P1-007  
**问题:** MODULE_REGISTRY 10_DEPLOY 标 Frozen，代码 Active  
**证据:** `api.py` 完整 FastAPI；`service.py` Service Lock 实现  
**影响:** 文档冲突 DC-005  
**建议方向:** 更新 MODULE_REGISTRY status → Active

---

### ISSUE-P1-008

**ID:** ISSUE-P1-008  
**问题:** Pilot 白名单阻塞已批准 PR  
**证据:** `approval_gate.py` PILOT_WHITELIST 仅 preq_20260712_005；001/004 approved 但 Adapter 拒绝  
**影响:** 与 Approval JSON 语义冲突（approved 但不可执行）  
**建议方向:** 文档明确 Pilot Policy；或扩展 whitelist Entry

---

## P2 — 优化建议

### ISSUE-P2-001

**ID:** ISSUE-P2-001  
**问题:** `7_MEMORY/core_state.json` orphaned  
**证据:** grep 零 Python 引用；MODULE_REGISTRY Deprecated/Review  
**影响:** 误导系统状态读取  
**建议方向:** 归档删除或接入 boot 写入

---

### ISSUE-P2-002

**ID:** ISSUE-P2-002  
**问题:** CF FeedbackAgent / PublishAssistantAgent 未接入 pipeline  
**证据:** `content_pipeline.py` 不 import；agents/__init__ 仅 export  
**影响:** Agent 清单膨胀但未使用  
**建议方向:** 接入 release 后步骤或移入 experimental/

---

### ISSUE-P2-003

**ID:** ISSUE-P2-003  
**问题:** CF llm_adapter stub；cover_generator 占位  
**证据:** `llm_adapter.py` NotImplementedError；cover_placeholder.txt  
**影响:** 封面/LLM 增强未实现  
**建议方向:** 保持 stub 或文档标注 Non-Goal

---

### ISSUE-P2-004

**ID:** ISSUE-P2-004  
**问题:** 1_DATA 采集依赖本地 Excel，无 live fetch  
**证据:** `collector.py` _find_excel_files(); 无 HTTP crawler  
**影响:** 空 Excel 目录时 pipeline 依赖历史 DB  
**建议方向:** 文档明确 Data Input 前提；或实现采集 Entry

---

### ISSUE-P2-005

**ID:** ISSUE-P2-005  
**问题:** 4_PRODUCT / 5_CONTENT 空目录占编号  
**证据:** 0 files；实际职能在 9/11  
**影响:** 导航混淆 MB-003/MB-004  
**建议方向:** MODULE_REGISTRY 合并说明或 README placeholder

---

### ISSUE-P2-006

**ID:** ISSUE-P2-006  
**问题:** 两套 Agent 基类无共享  
**证据:** `0_START/agent_runtime.BaseAgent` vs `11_CONTENT_FACTORY/agents/base_agent.ContentAgent`  
**影响:** 无法统一 Agent Registry  
**建议方向:** 长期统一 Protocol 或保持隔离并文档化

---

## P3 — 未来建设

### ISSUE-P3-001

**ID:** ISSUE-P3-001  
**问题:** Governance Runtime 自动化未实现  
**证据:** Governance Protocol §3 Entry Completion State Review — 无 tooling  
**建议方向:** Entry 039+ Governance Runtime

---

### ISSUE-P3-002

**ID:** ISSUE-P3-002  
**问题:** ZIP Full Audit 工具化未实现  
**证据:** Governance Protocol §5 — 本次 038-A 为首轮人工审计  
**建议方向:** audit/ 报告模板 + 自动化 scanner

---

### ISSUE-P3-003

**ID:** ISSUE-P3-003  
**问题:** 2_COGNITION Blueprint 未落地  
**证据:** 空目录；COGNITION_BLUEPRINT.md 存在  
**建议方向:** Cognition Implementation Entry

---

### ISSUE-P3-004

**ID:** ISSUE-P3-004  
**问题:** Observation Period / Feedback 采集 Runtime 未实现  
**证据:** feedback_v1.json pending；PILOT_OBSERVATION_PROTOCOL planned  
**建议方向:** Entry 036-B 人工观察 + 可选 Feedback writer

---

### ISSUE-P3-005

**ID:** ISSUE-P3-005  
**问题:** Experiment 台账 DB 扩展未实现  
**证据:** PROJECT_STATUS「实验台账 / DB 实施 ⏳ Pending」  
**建议方向:** Database Extension Entry（须单独授权）

---

## 统计

| 级别 | 数量 |
|------|------|
| P0 | 3 |
| P1 | 8 |
| P2 | 6 |
| P3 | 5 |
| **合计** | **22** |
