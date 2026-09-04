# Documentation Conflict Report

> Entry 038-A | 文档声明 vs 代码/数据现实

---

## DC-001

**Document Claim:** PROJECT_STATUS —「系统生产能力 ✅ Content Factory Active」  
**Reality:** `11_CONTENT_FACTORY` 独立运行；`0_START` DAG **不调用** Content Factory；Commercial 链为 JSON + Adapter CLI  
**Conflict:** 「Active」未区分 **Isolated Active** vs **OS-Integrated Active**  
**Risk:** 读者假设全系统已端到端自动化生产  
**Severity:** P1

---

## DC-002

**Document Claim:** PROJECT_STATUS —「Production Request Approval ✅ approved 3」  
**Reality:** `production_requests_v1.json` 三条 PR **status 仍为 `"draft"`**  
**Conflict:** Approval 完成未回写 PR status 字段  
**Risk:** ZIP 审计仅读 PR JSON 会误判未批准  
**Severity:** P1

---

## DC-003

**Document Claim:** PROJECT_STATUS — Pilot Production Completed（preq_005）  
**Reality:** `experiments_v1.json` 中 exp_20260708_005 **status 仍为 `"draft"`**  
**Conflict:** 生产完成 vs Experiment 对象状态未更新  
**Risk:** Experiment Lifecycle 文档与 JSON 事实不一致  
**Severity:** P1

---

## DC-004

**Document Claim:** MODULE_REGISTRY §2_COGNITION —「Status: Reserved / Blueprint Completed」  
**Reality:** 目录 **0 文件**；市场分析由 `11_CONTENT_FACTORY/market_agent.py` 执行  
**Conflict:** Blueprint Completed 暗示设计就绪可对接；Runtime 为零，职责被 CF 侵占  
**Risk:** 架构恢复时跳过 2_COGNITION 实现  
**Severity:** P1

---

## DC-005

**Document Claim:** MODULE_REGISTRY §10_DEPLOY —「Status: Frozen」  
**Reality:** `10_DEPLOY/api.py` + `service.py` **完整可运行**；为唯一有效 HTTP 入口  
**Conflict:** Frozen vs Active 状态错误  
**Risk:** 维护者忽略 Deploy 层或重复建设 9_PRODUCT API  
**Severity:** P1

---

## DC-006

**Document Claim:** MODULE_REGISTRY §9_PRODUCT —「Frozen, 未接入主链」  
**Reality:** 准确；但 `api_server.py` 仍存在于 repo 且含 `"production_ready"` 字符串  
**Conflict:** 损坏代码未移除，与 Frozen 声明共存  
**Risk:** 误用无效 API 入口  
**Severity:** P2

---

## DC-007

**Document Claim:** AI_FACTORY_OS_DATABASE_SCHEMA_BLUEPRINT / DATABASE_REALITY_AUDIT（历史文档）  
**Reality:** DB 含 `trends`(0 rows), `audit_log`(1 row)；`database.py ensure_schema()` **未定义**  
**Conflict:** Blueprint/历史审计 vs 当前 database.py 源码不同步  
**Risk:** 新部署 schema 不完整；audit_log 来源不明  
**Severity:** P1

---

## DC-008

**Document Claim:** Governance Protocol §2 — commercial_assets 为 Commercial Object SoT  
**Reality:** `11_CONTENT_FACTORY/storage/product_memory.json` 含产品记录 **未全部** 进入 commercial_assets  
**Conflict:** 双 SoT（CF storage vs commercial_assets）  
**Risk:** 审计恢复时漏读 product_memory  
**Severity:** P1

---

## DC-009

**Document Claim:** PRODUCT_ASSET_VALIDATION_GATE — Validation Gate Runtime Implemented  
**Reality:** `ProductAssetValidator` 存在且测试通过；**adapter_runner 不调用 validator**  
**Conflict:** Implementation Completed ≠ Runtime Connected to Adapter  
**Risk:** 假设 Adapter 输出已自动验收  
**Severity:** P1

---

## DC-010

**Document Claim:** system_snapshot — System Governance Layer「Implementation: Not Started」  
**Reality:** 与 Entry 037 一致 ✅  
**Conflict:** 无  
**Risk:** 无  
**Severity:** —

---

## DC-011

**Document Claim:** PROJECT_STATUS Current Phase —「下一阶段重点 Commercial Experiment Execution」  
**Reality:** Current Development Focus 段为「System Governance Stabilization」；Observation **planned, not started**  
**Conflict:** Phase 表 vs Focus 段优先级表述不完全对齐  
**Risk:** 低 — 文档内两处 focus 历史段落并存  
**Severity:** P3

---

## DC-012

**Document Claim:** CURSOR_EXECUTION_HISTORY Entry 033-B1 — Pilot Production executed  
**Reality:** `commercial_assets/product_assets/product_assets_v1.json` 含 8523329941d4；CF artifacts 存在 xlsx  
**Conflict:** 无 — 文档与资产一致 ✅  
**Risk:** 无  
**Severity:** —

---

## DC-013

**Document Claim:** BUSINESS_PLAN / COMMERCIAL_MVP_BLUEPRINT — 商业验证路径  
**Reality:** Feedback pending, Evaluation pending, Observation not_started — **无真实市场数据**  
**Conflict:** 设计完成 vs 执行未开始（文档自身有说明，但 skimming 易忽略）  
**Risk:** 对外沟通时过度承诺验证进度  
**Severity:** P2

---

## DC-014

**Document Claim:** 1_DATA MODULE_REGISTRY —「已经具备数据采集与数据库基础能力」  
**Reality:** 仅 Excel 导入 + SQLite；`data/raw/xianyu` 文件不可见于工作区 glob  
**Conflict:** 「数据采集」暗示 live collection；实际为 **offline import**  
**Risk:** 部署时无 Excel 则 pipeline 空转或读历史 DB  
**Severity:** P2

---

## DC-015

**Document Claim:** core_state.json（7_MEMORY）— MODULE_REGISTRY 标注 Deprecated/Review  
**Reality:** **零 Python 引用**（grep 确认）  
**Conflict:** 文件仍存在且含 system_mode 字段，可能被人工误读为运行时状态  
**Risk:** 与 memory_core JSON 双轨系统状态  
**Severity:** P2

---

## Summary

| 严重度 | 数量 | 代表项 |
|--------|------|--------|
| P1 | 9 | DC-001~005, DC-007~009 |
| P2 | 4 | DC-006, DC-013~015 |
| P3 | 1 | DC-011 |
| 无冲突 | 2 | DC-010, DC-012 |

**总体：** 文档对 Entry 完成记录较准确；**主要冲突在 Runtime Connected 语义、JSON status 字段未同步、空模块状态声明**。
