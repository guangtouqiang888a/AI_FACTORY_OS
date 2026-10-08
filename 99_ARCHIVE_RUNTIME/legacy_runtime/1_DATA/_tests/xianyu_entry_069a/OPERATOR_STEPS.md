# Entry 069-A — Operator Steps（人工必做）

Bridge 已在本机运行：

```
python 1_DATA/connectors/xianyu_extension_bridge_065.py --port 8765 --test-mode
```

地址：`http://127.0.0.1:8765/acquisition/v1/market-record-batch`  
模式：`test_mode=true`（只写 Test Sink，不写 Current DB）

## Chrome

1. `chrome://extensions` → Developer mode → **Load unpacked**
2. 选择目录：`D:\AI_FACTORY_OS\1_DATA\browser_extension\xianyu`
3. 打开真实闲鱼（goofish.com），**手工**搜索（例：`Excel模板`）
4. 确认页面是真实 **搜索结果**，不是仅「猜你喜欢」
5. 打开 Extension Popup → **Start**
6. 把 Popup 显示的 `page_state` / Bridge 结果 / 新 sink 文件名发回 Cursor

## 成功时你会看到

- Popup：`页面: SEARCH_RESULT`，提取 N 条（N≥1）
- `1_DATA/_tests/xianyu_extension_065/raw/` 出现新的 `run_*.json`（时间戳接近现在）
- `validation_report.json` 中 `ok: true`（或等价成功）

## 失败但诚实

- 只有推荐 → 记 `EMPTY_SEARCH_RESULT` / `NO_RESULTS`，**不要**标 PASS
- Bridge 连不上 → 先确认 8765 仍在监听
- Content script 不可用 → 刷新闲鱼页后重试

## 禁止

- 不要把历史 `batch.json` / 「测试搜索商品」当成本次 REAL
- 不要跑 Import Gate / 写 Current DB（那是 069-B）
