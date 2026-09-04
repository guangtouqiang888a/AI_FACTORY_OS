# AI_FACTORY_OS Document Ownership Matrix

## 文件维护责任

| 文件 | 类型 | 更新条件 |
|-|-|-|
| CURRENT_STATE | Current Reality | 系统事实变化 |
| MODULE_REGISTRY | Module Status | 模块变化 |
| BUSINESS_STRATEGY | Business Direction | 商业方向变化 |
| DECISION_LOG | Decision Record | 新决策 |
| BLUEPRINT | Design Layer | 设计变化 |
| AUDIT | Evidence | 执行完成后生成 |
| HISTORY | Historical | 架构演进解释 |

原则：

没有维护责任的文档不得成为权威文件。
"



04_BLUEPRINT/README.md 03_BUSINESS/README.md 00_GOVERNANCE/README.md 01_CURRENT_STATE/README.md 05_EXECUTION/README.md 02_ARCHITECTURE/README.md 07_AUDIT/README.md 06_HISTORY/README.md 99_ARCHIVE/README.md.Add(
"05_EXECUTION/reference/AI_FACTORY_OS_DOCUMENT_OWNERSHIP_MATRIX.md"
)



# ============================
# 3. Update Governance Rules
# ============================


Update-File 
"00_GOVERNANCE/AI_FACTORY_OS_KNOWLEDGE_UPDATE_PROTOCOL.md" 
@"
# Documentation Integrity Hardening

所有 Markdown 必须属于：

A Core Authority
B Active Reference
C Historical
D Audit Evidence
E Archive


禁止：

- 创建重复权威文件
- 随意新增根目录 MD
- 创建无维护责任文件


所有新文件必须：
中文说明 + English Standard Name。


Folder ≠ Authority。

权威由文件职责决定。
"



Update-File 
"00_GOVERNANCE/AI_FACTORY_OS_EXECUTION_PROTOCOL.md" 
@"
# Cursor Execution Governance

所有 Cursor 修改必须：

执行前：
- 明确 Entry
- 明确范围
- 明确禁止修改范围


执行后：
必须生成报告。


报告位置：

07_AUDIT/{category}/


核心治理文件：
必须使用中文解释。


格式：

English Name（中文说明）
"



# ============================
# 4. Archive downgrade note
# ============================


Update-File 
"99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md" 
@"
# Historical Status

本文为历史工作原则参考。

当前执行规则：
请以：

00_GOVERNANCE/AI_FACTORY_OS_EXECUTION_PROTOCOL.md

为准。
"



# ============================
# 5. Generate Report
# ============================


 =
@"
# ENTRY 044-D Documentation Integrity Hardening Report

Date:
07/17/2026 00:53:45

## Created

04_BLUEPRINT/README.md
03_BUSINESS/README.md
00_GOVERNANCE/README.md
01_CURRENT_STATE/README.md
05_EXECUTION/README.md
02_ARCHITECTURE/README.md
07_AUDIT/README.md
06_HISTORY/README.md
99_ARCHIVE/README.md


## Updated




## Scope

docs only

NO:
- Runtime
- Python
- Database
- Assets
- commercial_assets


## Result

Documentation boundary hardened.