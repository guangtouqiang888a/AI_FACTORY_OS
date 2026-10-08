/**
 * AI_FACTORY_OS Xianyu Collector — content script (Entry 065)
 * DOM-only acquisition. Collector records facts — no business filter in scrape loop.
 */
(() => {
  const ADAPTER_VERSION = "065.1.0";
  const COLLECTOR_VERSION = "065.1.0";
  const CONTRACT_VERSION = "064.1.0";
  const SOURCE = "xianyu";
  const PLATFORM = "xianyu";

  const DEFAULTS = {
    scrollStep: 400,
    scrollInterval: 300,
    maxScrollRounds: 30,
    readinessWait: 2000,
    pageReadyTimeout: 8000,
    cardStableChecks: 3,
    cardStableInterval: 500,
  };

  let stopRequested = false;

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  function nowIso() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    const off = -d.getTimezoneOffset();
    const sign = off >= 0 ? "+" : "-";
    const hh = pad(Math.floor(Math.abs(off) / 60));
    const mm = pad(Math.abs(off) % 60);
    return (
      `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` +
      `T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}${sign}${hh}:${mm}`
    );
  }

  function detectAccessBlocked() {
    const text = document.body?.innerText || "";
    return /非法访问|ACCESS_DENIED|访问受限|请使用正常浏览器|安全验证|验证码|captcha/i.test(text);
  }

  function detectLoginRequired() {
    const text = document.body?.innerText || "";
    return /请登录|登录后查看|LOGIN_REQUIRED/i.test(text) && !!document.querySelector('input[type="password"]');
  }

  function readQueryFromPage() {
    try {
      const u = new URL(location.href);
      for (const key of ["q", "keyword", "searchWord"]) {
        const v = u.searchParams.get(key);
        if (v && v.trim()) return v.trim();
      }
    } catch (_) {
      /* ignore */
    }
    const input = document.querySelector('input[type="search"], input[placeholder*="搜索"]');
    if (input && input.value && input.value.trim()) return input.value.trim();
    return null;
  }

  function classifyPageState() {
    if (detectAccessBlocked()) {
      return {
        page_state: "ACCESS_BLOCKED",
        result_origin_default: "UNKNOWN",
        search_primary_empty: false,
      };
    }
    if (detectLoginRequired()) {
      return {
        page_state: "LOGIN_REQUIRED",
        result_origin_default: "UNKNOWN",
        search_primary_empty: false,
      };
    }

    const bodyText = document.body?.innerText || "";
    const empty =
      bodyText.includes("没有找到你想要的宝贝") ||
      !!document.querySelector('[class*="empty-text-notfound"]');
    const guess =
      bodyText.includes("猜你喜欢") || !!document.querySelector('[class*="empty-feed-title"]');
    const cards = document.querySelectorAll('a[class*="feeds-item-wrap"]');

    if (empty && guess) {
      return {
        page_state: "RECOMMENDED_FEED",
        result_origin_default: "RECOMMENDED_RESULT",
        search_primary_empty: true,
      };
    }
    if (empty && cards.length === 0) {
      return {
        page_state: "EMPTY_SEARCH_RESULT",
        result_origin_default: "UNKNOWN",
        search_primary_empty: true,
      };
    }
    if (location.pathname.includes("/search") && cards.length > 0 && !empty) {
      return {
        page_state: "SEARCH_RESULT",
        result_origin_default: "SEARCH_RESULT",
        search_primary_empty: false,
      };
    }
    if (cards.length > 0 && guess && !location.pathname.includes("/search")) {
      return {
        page_state: "RECOMMENDED_FEED",
        result_origin_default: "RECOMMENDED_RESULT",
        search_primary_empty: false,
      };
    }
    return {
      page_state: "UNKNOWN",
      result_origin_default: "UNKNOWN",
      search_primary_empty: empty,
    };
  }

  function parseItemId(url) {
    if (!url) return null;
    try {
      const u = new URL(url, location.origin);
      const id = u.searchParams.get("id");
      if (id && id.trim()) return id.trim();
      const m = u.pathname.match(/\/item\/([^/?]+)/i);
      return m ? m[1] : null;
    } catch (_) {
      return null;
    }
  }

  function parseTitle(card) {
    const titled = card.querySelector('[class*="row1-wrap-title--"]');
    if (titled) {
      const t = titled.getAttribute("title");
      if (t && t.trim()) return t.trim();
    }
    const main = card.querySelector('[class*="main-title--"]');
    if (main) {
      const t = main.innerText?.trim();
      if (t) return t;
    }
    return null;
  }

  function parsePrice(card) {
    const num = card.querySelector('[class*="number--"]');
    if (!num) return null;
    const dec = card.querySelector('[class*="decimal--"]');
    const raw = `${num.innerText || ""}${dec ? dec.innerText || "" : ""}`.replace(/[^\d.]/g, "");
    if (!raw) return null;
    const p = parseFloat(raw);
    return Number.isFinite(p) ? p : null;
  }

  function parseWant(card) {
    const text = card.innerText || "";
    const m = text.match(/(\d+)\s*人想要/);
    if (m) {
      return { want_count: parseInt(m[1], 10), want_count_status: "VISIBLE_ON_CARD" };
    }
    return { want_count: null, want_count_status: "MISSING_ON_CARD" };
  }

  function parseImageUrl(card) {
    const img = card.querySelector("img");
    if (!img) return null;
    let src = img.src || img.getAttribute("data-src") || "";
    if (src.startsWith("//")) src = `https:${src}`;
    return src || null;
  }

  function cardResultOrigin(card, pageState) {
    if (pageState.page_state === "RECOMMENDED_FEED" || pageState.search_primary_empty) {
      return "RECOMMENDED_RESULT";
    }
    if (card.closest('[class*="empty-feed-container"]')) return "RECOMMENDED_RESULT";
    if (card.closest('[class*="empty-feed-title"]')) return "RECOMMENDED_RESULT";
    return pageState.result_origin_default || "UNKNOWN";
  }

  function recordDedupeKey(rec) {
    if (rec.source_item_id) return `id:${rec.source_item_id}`;
    if (rec.source_url) return `url:${rec.source_url}`;
    return `hash:${rec.title || ""}|${rec.price ?? ""}`;
  }

  function extractCards(pageState, query, sessionId, globalSeen) {
    const cards = document.querySelectorAll('a[class*="feeds-item-wrap"]');
    const out = [];
    let position = 0;

    for (const card of cards) {
      if (stopRequested) break;

      const hrefEl = card.matches("a") ? card : card.querySelector("a");
      let sourceUrl = hrefEl?.href || null;
      if (sourceUrl?.startsWith("//")) sourceUrl = `https:${sourceUrl}`;
      if (!sourceUrl || sourceUrl === location.href) continue;

      const title = parseTitle(card);
      if (!title) continue;

      position += 1;
      const price = parsePrice(card);
      const want = parseWant(card);
      const sourceItemId = parseItemId(sourceUrl);
      const resultOrigin = cardResultOrigin(card, pageState);
      const imageUrl = parseImageUrl(card);

      const rec = {
        source: SOURCE,
        platform: PLATFORM,
        source_item_id: sourceItemId,
        source_url: sourceUrl.split("#")[0],
        title,
        price,
        currency: "CNY",
        want_count: want.want_count,
        want_count_status: want.want_count_status,
        result_origin: resultOrigin,
        observed_at: nowIso(),
        query: query || null,
        session_id: sessionId,
        collector_version: COLLECTOR_VERSION,
        result_position: position,
        image_url: imageUrl,
        sales_platform: null,
      };

      const key = recordDedupeKey(rec);
      if (globalSeen.has(key)) continue;
      globalSeen.add(key);
      out.push(rec);
    }
    return out;
  }

  async function boundedScroll(cfg) {
    let rounds = 0;
    let total = 0;
    while (!stopRequested && rounds < cfg.maxScrollRounds) {
      const before = document.body.scrollHeight;
      window.scrollBy(0, cfg.scrollStep);
      total += cfg.scrollStep;
      rounds += 1;
      await sleep(cfg.scrollInterval);
      if (total >= before - 1000 || window.innerHeight + window.scrollY >= before - 200) {
        break;
      }
    }
    window.scrollTo(0, document.body.scrollHeight);
    await sleep(cfg.readinessWait);
  }

  async function waitForCardStability(cfg) {
    let last = -1;
    let stable = 0;
    const deadline = Date.now() + cfg.pageReadyTimeout;
    while (Date.now() < deadline && !stopRequested) {
      const n = document.querySelectorAll('a[class*="feeds-item-wrap"]').length;
      if (n === last && n > 0) {
        stable += 1;
        if (stable >= cfg.cardStableChecks) return n;
      } else {
        stable = 0;
        last = n;
      }
      await sleep(cfg.cardStableInterval);
    }
    return document.querySelectorAll('a[class*="feeds-item-wrap"]').length;
  }

  async function goToNextPage() {
    const boxes = Array.from(document.querySelectorAll('[class*="search-pagination-page-box"]'));
    if (!boxes.length) return false;
    const activeIdx = boxes.findIndex((el) => (el.className || "").includes("active"));
    if (activeIdx === -1 || activeIdx >= boxes.length - 1) return false;
    const next = boxes[activeIdx + 1];
    const label = (next.innerText || "").trim();
    if (!( /^\d+$/.test(label) || label === ">" || label.includes("下一页") )) return false;
    next.scrollIntoView({ behavior: "smooth", block: "center" });
    await sleep(600);
    next.click();
    await waitForCardStability(DEFAULTS);
    return true;
  }

  async function collectRun(request) {
    stopRequested = false;
    const cfg = { ...DEFAULTS, ...(request.scrollConfig || {}) };
    const maxRecords = Math.min(Math.max(parseInt(request.maxRecords, 10) || 20, 1), 50);
    const maxPages = Math.min(Math.max(parseInt(request.maxPages, 10) || 1, 1), 5);
    const sessionId = request.sessionId || `sess_${Date.now()}`;
    const runId = request.runId || `run_${Date.now()}`;
    const query = request.query || readQueryFromPage();

    const pageState = classifyPageState();
    if (pageState.page_state === "ACCESS_BLOCKED") {
      return {
        status: "ACCESS_BLOCKED",
        run_id: runId,
        session_id: sessionId,
        page_state: pageState.page_state,
        records: [],
        stats: { records_seen: 0, records_extracted: 0 },
      };
    }
    if (pageState.page_state === "LOGIN_REQUIRED") {
      return {
        status: "ACCESS_BLOCKED",
        run_id: runId,
        session_id: sessionId,
        page_state: "LOGIN_REQUIRED",
        records: [],
        stats: { records_seen: 0, records_extracted: 0 },
      };
    }

    const globalSeen = new Set();
    const all = [];
    let pagesProcessed = 0;
    let structureError = false;

    for (let p = 0; p < maxPages && !stopRequested; p += 1) {
      pagesProcessed += 1;
      await boundedScroll(cfg);
      const cardCount = await waitForCardStability(cfg);
      if (cardCount === 0 && p === 0) {
        if (document.querySelectorAll('[class*="feeds-item-wrap"]').length === 0) {
          structureError = !pageState.search_primary_empty;
        }
      }

      const batch = extractCards(pageState, query, sessionId, globalSeen);
      for (const rec of batch) {
        if (all.length >= maxRecords) break;
        all.push(rec);
      }
      if (all.length >= maxRecords) break;
      if (p < maxPages - 1) {
        const moved = await goToNextPage();
        if (!moved) break;
      }
    }

    let status = "SUCCESS";
    if (stopRequested && all.length) status = "PARTIAL";
    else if (stopRequested) status = "PARTIAL";
    else if (structureError) status = "PAGE_STRUCTURE_CHANGED";
    else if (!all.length) status = pageState.page_state === "EMPTY_SEARCH_RESULT" ? "NO_RESULTS" : "NO_RESULTS";
    else if (all.length < maxRecords && pagesProcessed > 0) status = "SUCCESS";

    const missingWant = all.filter((r) => r.want_count_status === "MISSING_ON_CARD").length;

    return {
      status,
      run_id: runId,
      session_id: sessionId,
      contract_version: CONTRACT_VERSION,
      message_type: "MARKET_RECORD_BATCH",
      source: SOURCE,
      platform: PLATFORM,
      query,
      result_origin: pageState.result_origin_default,
      page_state: pageState.page_state,
      observed_at: nowIso(),
      collector_version: COLLECTOR_VERSION,
      adapter_version: ADAPTER_VERSION,
      filter_metadata: {
        min_want_count: request.minWantCount ?? null,
        min_price: request.minPrice ?? null,
        max_price: request.maxPrice ?? null,
      },
      records: all,
      stats: {
        records_seen: document.querySelectorAll('a[class*="feeds-item-wrap"]').length,
        records_extracted: all.length,
        missing_want_count: missingWant,
        pages_processed: pagesProcessed,
        duplicates_skipped: globalSeen.size - all.length,
      },
    };
  }

  chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
    if (request.action === "get_page_status") {
      const ps = classifyPageState();
      sendResponse({
        page_state: ps.page_state,
        result_origin: ps.result_origin_default,
        query: readQueryFromPage(),
        url: location.href,
        adapter_version: ADAPTER_VERSION,
      });
      return false;
    }
    if (request.action === "stop_collect") {
      stopRequested = true;
      sendResponse({ ok: true });
      return false;
    }
    if (request.action === "start_collect") {
      collectRun(request).then(sendResponse).catch((err) => {
        sendResponse({
          status: "UNKNOWN",
          error: String(err?.message || err),
          records: [],
        });
      });
      return true;
    }
    return false;
  });
})();
