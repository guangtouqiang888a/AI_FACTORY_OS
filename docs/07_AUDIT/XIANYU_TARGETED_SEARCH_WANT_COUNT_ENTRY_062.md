# XIANYU_TARGETED_SEARCH_WANT_COUNT_ENTRY_062.md

ENTRY ID: 062  
DATE: 2026-08-30  
STATUS: **PASS / PARTIAL**  
FIRST_REAL_XIANYU_SEARCH_BATCH: **NO**  
DECISION: **DEC-032**

## A. Query

Attempted (among others): `Excel模板`, `PPT模板`, `简历模板`, `手机壳`, `电子书`, `蓝牙耳机`.  
Final pilot queries included UI-typed search. **None** produced primary SEARCH_RESULT in this anonymous interactive Chrome session.

## B. Search URL

e.g. `https://www.goofish.com/search?q=Excel%E6%A8%A1%E6%9D%BF`（and UI search from home）.

## C. Search Result Reality

Every tested query showed page text **「小闲鱼没有找到你想要的宝贝」** + **猜你喜欢** feed (~40 cards).  
**SEARCH_RESULT count = 0.** Recommendations **excluded** from target batch.

## D. Result Origin

Implemented: `SEARCH_RESULT` | `RECOMMENDED_RESULT` | `UNKNOWN`.  
061-style guess-you-like **not** counted as search evidence.

## E. Records

SEARCH_RESULT accepted: **0**  
RECOMMENDED excluded: **~40/query**（side observation only）

## F–G. Title / Price

On SEARCH_RESULT: N/A (0 records).  
On recommended side sample (not search batch): title/price readable when cards present.

## H–I. Want Count / Status

SEARCH_RESULT audit: empty (0 cards).  
**Side observation** (recommended cards, last dump, n=20):  
VISIBLE_ON_CARD=13, MISSING_ON_CARD=7.  
→ Anonymous session **can** show want_count on some cards ⇒  
**cannot conclude** missing want_count is caused by not being logged in (**NOT_PROVEN**).

Detail enrichment for SEARCH_RESULT: not applicable (no search cards).

## J–L. View / Comment / Share

UNAVAILABLE on sampled cards (not focus of this Entry).

## M. URL / Item ID

Pattern `/item?id=` confirmed on feed cards (recommended).

## N. Missing Field Analysis

| Rule | Applied |
|------|---------|
| NULL ≠ 0 | Yes |
| MISSING_ON_CARD keeps NULL | Yes |
| 0人想要 → value 0 | Yes (unit tested) |
| valid_without_want_count | Yes |
| Login causation | **NOT_PROVEN** |

## O. Stability

N/A for search batch (0 results). Classification tests cover stability helpers.

## P–R. Login / CAPTCHA / Access

login_used=false；no CAPTCHA；no ACCESS_DENIED（empty soft-state, not 非法访问）.

## S–T. Provenance / Origin

Artifacts: `1_DATA/_tests/xianyu_targeted_search_062/`  
candidate_class would be REAL_CANDIDATE_EXTERNAL **if** SEARCH_RESULT existed.

## U. Current DB Impact

observations/products/signals/selection **delta=0**.

## V. Legacy Isolation

No archive / sample / old 61 rows.

## W. Tests

`test_xianyu_targeted_search_062` — 8 OK.

## X. Recommendations

1. Human-controlled browser session may be required for primary SEARCH_RESULT in this environment.  
2. Keep IMPORT path as production until SEARCH_RESULT reproducible.  
3. Next Entry: human-verify path or controlled session — still no auto-login.
