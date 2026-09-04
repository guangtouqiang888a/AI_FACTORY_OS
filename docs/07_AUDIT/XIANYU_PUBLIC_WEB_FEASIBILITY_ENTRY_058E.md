# XIANYU_PUBLIC_WEB_FEASIBILITY_ENTRY_058E.md

ENTRY ID: 058E  
DATE: 2026-08-30  
STATUS: PASS（principle + honest feasibility；HTML listing extract NOT_FEASIBLE）

## A. Test Goal

Anonymous, read-only, no-login, no-bypass public page feasibility for Xianyu listing fields.  
Not a production crawler. Not written to Current DB.

## B. Test Query

`虚拟资料`（digital/virtual materials market keyword）

## C. Access Mode

`PUBLIC_WEB_READ` — urllib HTTP GET, browser-like User-Agent, no cookies/login.

## D. Pages Tested

| Page | Result |
|------|--------|
| https://www.goofish.com/search?q=虚拟资料 | HTTP 200；CSR shell；2 re-reads |
| s.2.taobao.com legacy candidate | Earlier probe：punish/deny / short body |

Items extracted: **0**（cap was ≤10）

## E. Fields Available

| Field | Class |
|-------|--------|
| query | AVAILABLE（test-supplied） |
| observed_at | AVAILABLE（test-supplied） |

## F. Fields Unavailable

title, price, source_url, source_item_id, want_count, view_count, comment_count, share_count, seller_reference, published_at, category — all **UNAVAILABLE** from initial HTML.

## G. Login Requirement

No login wall for fetching search HTML. Sitemap contains a login link only. **login_used=false**.

## H. CAPTCHA

Not presented on goofish search HTML fetches. **No bypass attempted.**

## I. Access Control

Goofish search HTML: not blocked.  
Legacy URL probe: punish/deny observed earlier.  
Page scripts reference `mtop.taobao.idlemtopsearch` — **not called**.

## J. Stability

Two reads：status 200 both；sha256 equal；`#ice-container` empty both. Shell stable；listing payload absent.

## K–L. Source URLs / Item IDs

None extractable from initial HTML.

## M. Acquisition Risks

- Misreading CSR shell as “page works → fields available”
- Temptation to call hidden mtop / use browser automation without compliance review
- Treating test artifacts as Current DB market data

## N. Compliance Boundary

Stopped at HTML-only public read. No captcha bypass, no login automation, no anti-bot evasion, no hidden API.

## O. Data Origin

Artifacts marked `REAL_CANDIDATE_EXTERNAL` / technical — **not** imported as REAL observations.

## P. Current DB Impact

**0 rows added.** products=0, market_observations=0, market_signals=0, selection_results=0.

## Q. Recommended Next Step

Keep **EXTERNAL_IMPORT / USER_EXPORT**. Optional future: compliance-reviewed JS/browser path or official eligibility — not this Entry.

## Own Product（same Entry）

DEC-030 recorded. See Constitution #27 and `1_DATA/product_origin.py`.
