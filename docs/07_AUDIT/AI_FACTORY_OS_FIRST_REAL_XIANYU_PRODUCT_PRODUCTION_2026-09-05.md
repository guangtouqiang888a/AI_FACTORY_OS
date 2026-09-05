# Formal Audit — First Real Xianyu Product Production

**Date:** 2026-09-05  
**Entry ID:** **077**  
**Result:** `PASS_WITH_FINDINGS`  
**Cursor PASS ≠ ChatGPT Closure Review**

---

## Objective

将已准备的 Production Request `preq_20260904_pmgantt`（商品假设：小微团队项目计划 + 任务进度 + 甘特图 Excel 模板）经合法授权路径生产为真实 Product Asset，达到 `SELLABLE_QUALITY_FLOOR`，并形成人工发布 Pack。**不**自动发布闲鱼。

---

## RESULT

**PASS_WITH_FINDINGS**

---

## Production Result

| Item | Value |
|------|-------|
| Product Definition | `prod_a0638789fc2b` |
| Opportunity | `aoc_19399677b7ba` |
| Selection (upstream) | `sel_53e7c414624f` |
| Hypothesis Selection | `sel_20260904_pmgantt` |
| Experiment | `exp_20260904_pmgantt` → `produced_awaiting_human_publish` |
| Production Request | `preq_20260904_pmgantt` → `PRODUCED` |
| Approval | `appr_20260904_pmgantt` → `approved`（CF production only） |
| Product Asset | **`a949d2e47cf1`** |
| Publish | **NOT_PUBLISHED** |
| Hypothesis | **HYPOTHESIS / DERIVED DESIGN**（≠ DIRECT_EVIDENCE） |

---

## Artifact Evidence

| Field | Value |
|-------|-------|
| Root | `11_CONTENT_FACTORY/artifacts/products/a949d2e47cf1/` |
| Primary | `templates/a949d2e47cf1.xlsx` |
| SHA256 | `07ae66a5f4981e79f0b519748e8a26a453fccbde3ac823e9465f26b85a44c566` |
| Sheets | 使用说明 / 任务明细 / 项目摘要 / 甘特图 |
| Manual | `documents/product_manual.pdf` |
| Zip | `package/final_product.zip` |
| Publish Pack | `package/publish_assistant/HUMAN_PUBLISH_PACK.md` |
| Registry | `commercial_assets/product_assets/product_assets_v1.json` |
| E2E mirror | `commercial_assets/e2e_outputs/a949d2e47cf1/` |

---

## Quality Evidence

`SELLABLE_QUALITY_FLOOR` = **PASS**

Evidence: `SELLABLE_QUALITY_FLOOR_VALIDATION.json` + regression Test 8.

Checks: file opens; sheets present; task headers; sample tasks; date fields; gantt formulas linked; summary formulas; instructions; input highlight; usable for ordinary user.

---

## Gate Evidence

**Before:** ApprovalGate pilot whitelist = `{preq_20260712_005}` only → `preq_20260904_pmgantt` blocked (`PILOT_NOT_ALLOWED`).

**After (minimal):** whitelist = `{preq_20260712_005, preq_20260904_pmgantt}` — deny-by-default retained; no wildcards; non-whitelisted PR still blocked (Test 4/7).

Authorization: ChatGPT Entry instruction + `appr_20260904_pmgantt.decision=approved` + PR `production_authorization` metadata. **Not** fabricated human UI click; **not** external publish authorization.

---

## Cost Evidence

| Cost | Value |
|------|-------|
| production_cost | `0.0`（≤ ¥3 ceiling） |
| ai_cost | `0.0`（deterministic openpyxl; no LLM） |
| packaging_cost | `0.0` |
| publish_cost | `NOT_STARTED` |
| price | ¥9.9 **PRICE_HYPOTHESIS only** |
| revenue | **NOT recorded**（none occurred） |

---

## Test Evidence

`11_CONTENT_FACTORY/adapter/regression_test_v1.py` → **8/8 PASS**

Including Test 7 (whitelist + deny-by-default) and Test 8 (PM/Gantt quality floor).

---

## External Action Status

**NONE.** No 闲鱼 login / listing / chat / payment. Human Final External Publish Gate **holds**.

---

## Reality Changes

| Layer | Change |
|-------|--------|
| Runtime | CF adapter execute path used once for authorized PR; no Core OS runtime change |
| Code | `approval_gate.py` whitelist; `excel_generator.py` Gantt generator; `product_generator.py` route; `regression_test_v1.py` Tests 7–8 |
| DB | **NONE**（no migration / SQLite product write） |
| Assets | Product Asset `a949d2e47cf1` + commercial JSON status updates + e2e mirror |
| Docs | Current State; Control Center; Execution History; this Audit |
| External | **NONE** |

---

## Git Evidence

Filled at commit closeout (see Execution History / Final Report).

---

## Unresolved Findings

1. Orphan local draft dir `11_CONTENT_FACTORY/artifacts/products/3d323bf0de83/` (attendance-titled metadata only; empty product) appeared during session — **not** registered as Product Asset; **excluded** from commit scope if still present.  
2. Product Definition `prod_a0638789fc2b` remains `draft` (by design); Asset ≠ market validation.  
3. Cover image is placeholder text — acceptable for quality floor; human may improve visuals at publish time.  
4. Cursor local PASS awaits **ChatGPT Closure Review**.

---

## Next Step

将真实 Product Asset `a949d2e47cf1` 交给人工完成闲鱼外部发布，并等待真实询盘/订单/成交证据。

**不得**把「已生产」写成「已盈利」。
