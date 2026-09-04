const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 智能翻页逻辑 (针对 div 结构的页码框)
async function goToNextPage() {
    const allPageBoxes = Array.from(document.querySelectorAll('[class*="search-pagination-page-box"]'));
    if (allPageBoxes.length === 0) return false;

    // 找到 active 的 div
    const activeIndex = allPageBoxes.findIndex(el => el.className.includes('active'));

    if (activeIndex !== -1 && activeIndex < allPageBoxes.length - 1) {
        const nextBtn = allPageBoxes[activeIndex + 1];
        const nextText = nextBtn.innerText.trim();

        if (!isNaN(nextText) || nextText === '>' || nextText.includes('下一页')) {
            nextBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
            await sleep(600); 
            nextBtn.click();
            return true;
        }
    }
    return false;
}

// 自动滚动 (触发懒加载图片)
async function autoScrollToBottom() {
    let totalHeight = 0;
    const distance = 400;
    while (totalHeight < document.body.scrollHeight - 1000) {
        window.scrollBy(0, distance);
        totalHeight += distance;
        await sleep(300);
    }
    window.scrollTo(0, document.body.scrollHeight);
    await sleep(2000); // 等待最后的数据加载
}

// 抓取当前页数据
async function scrapeCurrentPage(minWant) {
    const results = [];
    const seenTitles = new Set();
    const cards = document.querySelectorAll('[class*="item"], [class*="card"]');

    cards.forEach(card => {
        const text = card.innerText || "";
        const match = text.match(/(\d+)\s*人想要/);
        
        if (match) {
            const wantCount = parseInt(match[1]);
            if (wantCount >= minWant) {
                const titleEl = card.querySelector('[class*="title"]');
                const title = titleEl ? titleEl.innerText.trim() : "未知标题";
                const priceEl = card.querySelector('[class*="price"]');
                const price = priceEl ? priceEl.innerText.trim() : "面议";
                const linkEl = card.querySelector('a') || card.closest('a');
                const link = linkEl ? linkEl.href : window.location.href;

                // 提取商品主图
                const imgEl = card.querySelector('img');
                let imgUrl = imgEl ? (imgEl.src || imgEl.dataset.src || "") : "";
                if (imgUrl.startsWith('//')) imgUrl = 'https:' + imgUrl;

                if (!seenTitles.has(title)) {
                    results.push({ wantCount, title, price, link, imgUrl });
                    seenTitles.add(title);
                }
            }
        }
    });
    return results;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "start_auto_scrape") {
        (async () => {
            let finalResults = [];
            for (let i = 0; i < request.maxPages; i++) {
                console.log(`正在处理第 ${i+1} 页...`);
                await autoScrollToBottom();
                const data = await scrapeCurrentPage(request.minWant);
                finalResults = finalResults.concat(data);
                
                if (i < request.maxPages - 1) {
                    const hasNext = await goToNextPage();
                    if (!hasNext) break;
                    await sleep(5000); // 等待翻页渲染
                }
            }
            sendResponse({ data: finalResults });
        })();
        return true;
    }
});