/**
 * AI_FACTORY_OS Xianyu Collector — popup (Entry 065)
 */
const BRIDGE_URL = "http://127.0.0.1:8765/acquisition/v1/market-record-batch";

const els = {
  pageState: document.getElementById("pageState"),
  pageQuery: document.getElementById("pageQuery"),
  maxRecords: document.getElementById("maxRecords"),
  maxPages: document.getElementById("maxPages"),
  minWant: document.getElementById("minWant"),
  startBtn: document.getElementById("startBtn"),
  stopBtn: document.getElementById("stopBtn"),
  status: document.getElementById("status"),
  stats: document.getElementById("stats"),
  bridgeUrl: document.getElementById("bridgeUrl"),
};

els.bridgeUrl.textContent = BRIDGE_URL;

function parseOptionalInt(input) {
  const v = input.value.trim();
  if (!v) return null;
  const n = parseInt(v, 10);
  return Number.isFinite(n) ? n : null;
}

async function activeTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function refreshPageStatus() {
  try {
    const tab = await activeTab();
    if (!tab?.id || !tab.url?.includes("goofish.com")) {
      els.pageState.textContent = "NOT_XIANYU_PAGE";
      els.pageQuery.textContent = "—";
      return;
    }
    const resp = await chrome.tabs.sendMessage(tab.id, { action: "get_page_status" });
    els.pageState.textContent = resp?.page_state || "UNKNOWN";
    els.pageQuery.textContent = resp?.query || "UNKNOWN";
  } catch (e) {
    els.pageState.textContent = "CONTENT_SCRIPT_UNAVAILABLE";
    els.pageQuery.textContent = "—";
  }
}

async function postBatch(payload) {
  const res = await fetch(BRIDGE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-AIFO-Contract-Version": payload.contract_version || "064.1.0",
      "X-AIFO-Request-Id": payload.request_id || payload.run_id,
    },
    body: JSON.stringify(payload),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(body.error || `Bridge HTTP ${res.status}`);
  }
  return body;
}

els.startBtn.addEventListener("click", async () => {
  els.startBtn.disabled = true;
  els.stopBtn.disabled = false;
  els.status.textContent = "采集中…请勿关闭此页。";
  els.stats.textContent = "";

  try {
    const tab = await activeTab();
    if (!tab?.id) throw new Error("无活动标签页");

    const runId = `run_${Date.now()}`;
    const sessionId = `sess_${Date.now()}`;
    const minWantRaw = els.minWant.value.trim();
    const minWantCount = minWantRaw === "" ? null : parseInt(minWantRaw, 10);

    const collectResp = await chrome.tabs.sendMessage(tab.id, {
      action: "start_collect",
      runId,
      sessionId,
      maxRecords: parseInt(els.maxRecords.value, 10) || 20,
      maxPages: parseInt(els.maxPages.value, 10) || 1,
      minWantCount: Number.isFinite(minWantCount) ? minWantCount : null,
    });

    if (!collectResp) throw new Error("Content script 无响应");

    const batch = {
      contract_version: collectResp.contract_version || "064.1.0",
      message_type: "MARKET_RECORD_BATCH",
      request_id: runId,
      run_id: collectResp.run_id || runId,
      session_id: collectResp.session_id || sessionId,
      source: "xianyu",
      platform: "xianyu",
      query: collectResp.query,
      result_origin: collectResp.result_origin,
      page_state: collectResp.page_state,
      observed_at: collectResp.observed_at,
      collector_version: collectResp.collector_version,
      adapter_version: collectResp.adapter_version,
      status: collectResp.status,
      filter_metadata: collectResp.filter_metadata || { min_want_count: minWantCount },
      records: collectResp.records || [],
      stats: collectResp.stats || {},
    };

    const bridgeResp = await postBatch(batch);

    els.status.textContent =
      `完成: ${collectResp.status}\n` +
      `Bridge: ${bridgeResp.status || "OK"}\n` +
      `页面: ${collectResp.page_state}`;
    els.stats.textContent =
      `提取 ${batch.records.length} 条 | ` +
      `缺失想要 ${batch.stats.missing_want_count ?? 0} | ` +
      `Sink: ${bridgeResp.sink_path || "test sink"}`;
  } catch (err) {
    els.status.textContent = `失败: ${err.message || err}`;
  } finally {
    els.startBtn.disabled = false;
    els.stopBtn.disabled = true;
    refreshPageStatus();
  }
});

els.stopBtn.addEventListener("click", async () => {
  try {
    const tab = await activeTab();
    if (tab?.id) await chrome.tabs.sendMessage(tab.id, { action: "stop_collect" });
    els.status.textContent = "已请求停止…";
  } catch (e) {
    els.status.textContent = `Stop 失败: ${e.message}`;
  }
});

refreshPageStatus();
