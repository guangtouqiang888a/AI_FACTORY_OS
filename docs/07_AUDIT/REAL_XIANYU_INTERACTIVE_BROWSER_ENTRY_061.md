# REAL_XIANYU_INTERACTIVE_BROWSER_ENTRY_061.md

ENTRY ID: 061  
DATE: 2026-08-30  
STATUS: **PASS / PARTIAL**  
FIRST_REAL_XIANYU_CANDIDATE_BATCH: **YES**（test-dir only；未写 Current DB）

## A. Browser Mode

`INTERACTIVE_VISIBLE` — System Chrome + isolated profile + CDP（`websockets`）。**非 headless**。

## B. Query

`虚拟资料`（单 query）。

## C. Page Access

打开成功：`https://www.goofish.com/search?q=虚拟资料`，title=`虚拟资料_闲鱼`。  
**无** 非法访问 / CAPTCHA / LOGIN wall。  
主搜索结果：**空**（「小闲鱼没有找到你想要的宝贝」）→ 页面展示 **猜你喜欢** 推荐流。

## D. Product Cards

可见 `feeds-item-wrap` 卡片；抽取 **20** 条（≤20 上限）。  
`page_section=guess_you_like_after_empty_search`（诚实标注，非伪造成搜索命中）。

## E–J. Fields

| Field | Status | Rate |
|-------|--------|------|
| title | AVAILABLE | 1.0 |
| price | AVAILABLE | 1.0 |
| want_count | PARTIAL | 0.4 |
| source_url | AVAILABLE | 1.0 |
| source_item_id | AVAILABLE | 1.0（`/item?id=`） |
| view / comment / share / published_at | UNAVAILABLE | 0 |

## K. Stability

同页二次读取：comparable=10，match_rate=1.0，**stable=true**。

## L. Access Control

未触发（interactive 与 060 headless ACCESS_DENIED 对比鲜明）。

## M–O. Provenance / Origin / Test Output

Artifacts：`1_DATA/_tests/xianyu_interactive_061/`  
（run_metadata / extracted_records.json+csv / field_availability / page dumps / error.log）  
Candidate class：`REAL_CANDIDATE_EXTERNAL`。若日后入库：`data_origin=REAL`，`verification=MANUAL_VERIFIED`。

## P. Current DB Impact

market_observations / products / signals / selection **delta = 0**。

## Q. Collector Status

`col_xianyu_browser_interactive` = **LIMITED**（want_count 未达 AVAILABLE；主搜空）。  
`col_xianyu_browser` headless 仍 LIMITED/blocked path。

## R. Future Path

下一 Entry：人工核对 test 输出 → 决定是否正式写入 `market_observations`。  
可另测有主搜命中的 query（如 Excel模板）。

## S. Risks

猜你喜欢 ≠ 关键词命中；want_count 仅部分卡片展示；勿当爆款判断。

## T. Tests

`test_xianyu_interactive_061`（10）+ 060 regression — OK。
