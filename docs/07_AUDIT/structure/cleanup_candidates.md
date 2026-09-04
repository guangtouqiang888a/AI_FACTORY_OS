# Cleanup Candidates（待删除候选 · 未执行删除）

> Entry **044-B** · Documentation Physical Consolidation  
> **Date:** 2026-07-17  
> **规则：** 本 Entry **不删除**高风险文件；仅登记，等待后续授权 Entry。

---

## 1. 空目录（无文件）

| 路径 | 说明 | 建议 |
|------|------|------|
| `docs/audit/` | 042-C 迁移后空壳；易与 `07_AUDIT/` 混淆 | 授权后移除空目录 |
| `docs/03_BUSINESS/reports/` | 商业报告已迁入 `07_AUDIT/commercial/` | 授权后移除空目录 |
| `docs/05_EXECUTION/reports/` | Broken Entry 报告已迁入 `07_AUDIT/runtime/` | 授权后移除空目录 |

---

## 2. 重复 / 降级后的平行入口（保留，不删）

| 文件 | 状态 | 说明 |
|------|------|------|
| `docs/05_EXECUTION/AI_FACTORY_OS_DOCUMENTATION_MAP.md` | Reference（044-A） | 唯一入口为根目录 Documentation Map；勿再当 SoT |
| `docs/99_ARCHIVE/AI_FACTORY_OS_SYSTEM_GOVERNANCE_PROTOCOL.md` | Archive（044-B） | 文首已声明历史参考；现行执行以 `00_GOVERNANCE/EXECUTION_PROTOCOL` 为准 |
| `docs/99_ARCHIVE/AI_FACTORY_OS_WORK_PRINCIPLES.md` | Archive | 勿覆盖 Constitution / Execution Protocol |
| `docs/99_ARCHIVE/AI_FACTORY_OS_BUSINESS_PLAN.md` | Archive | 勿覆盖 Business Strategy |
| `docs/01_CURRENT_STATE/reference/PROJECT_STATUS.md` | Reference | 勿覆盖 Current State |
| `docs/01_CURRENT_STATE/reference/system_snapshot.md` | Reference | 勿覆盖 Current State |

---

## 3. 无明显临时废弃副本

未发现未引用的临时 Markdown 副本需要立即删除。  
全库仍保留证据链；清理以空目录与认知降权为主。

---

## 4. 禁止本清单自动执行

- **禁止**无授权删除上表任何路径或文件  
- 删除须新开 Entry，并遵守 File Migration Rule（修链 + 更新 Map + Audit Report）

**Entry 044-B：** Cleanup candidates recorded only.
