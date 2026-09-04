let currentData = [];

document.getElementById('startBtn').addEventListener('click', async () => {
    const minWant = parseInt(document.getElementById('minWant').value) || 0;
    const maxPages = parseInt(document.getElementById('maxPages').value) || 1;
    const status = document.getElementById('status');
    const startBtn = document.getElementById('startBtn');
    
    status.innerText = "🚀 正在全自动执行中，请勿关闭弹窗...";
    startBtn.disabled = true;

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, { 
        action: "start_auto_scrape", 
        minWant: minWant, 
        maxPages: maxPages 
    }, (response) => {
        startBtn.disabled = false;
        if (response && response.data) {
            currentData = response.data;
            status.innerText = `✅ 抓取完成！找到 ${currentData.length} 个商品`;
            renderTable(currentData);
            document.getElementById('downloadBtn').style.display = "block";
        } else {
            status.innerText = "❌ 抓取超时或页面已断开";
        }
    });
});

function renderTable(data) {
    const table = document.getElementById('resTable');
    const tbody = table.querySelector('tbody');
    table.style.display = "table";
    // 仅预览前 5 条
    tbody.innerHTML = data.slice(0, 5).map(i => `
        <tr>
            <td style="color:#ff5000;font-weight:bold;">${i.wantCount}</td>
            <td><img src="${i.imgUrl}" class="img-preview"></td>
            <td>${i.title.substring(0,8)}...</td>
            <td>${i.price}</td>
        </tr>
    `).join('') + (data.length > 5 ? `<tr><td colspan="4" style="text-align:center;">已记录全部 ${data.length} 条数据</td></tr>` : "");
}

document.getElementById('downloadBtn').addEventListener('click', () => {
    const headers = ["想要人数", "商品标题", "价格", "图片链接", "商品链接"];
    const formatCell = (str) => `"${String(str).replace(/"/g, '""').replace(/[\r\n\t]+/g, ' ')}"`;
    
    let csvContent = "\ufeff" + headers.join(',') + '\n';
    currentData.forEach(item => {
        csvContent += [
            item.wantCount, 
            formatCell(item.title), 
            formatCell(item.price), 
            formatCell(item.imgUrl), 
            item.link
        ].join(',') + '\n';
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `闲鱼采集数据_${new Date().getTime()}.csv`;
    link.click();
});