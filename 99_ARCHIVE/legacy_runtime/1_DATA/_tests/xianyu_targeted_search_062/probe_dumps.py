from pathlib import Path
import re

art = Path("1_DATA/_tests/xianyu_targeted_search_062")
for p in sorted(art.glob("page_dump_*.html")):
    c = p.read_text(encoding="utf-8")
    m = re.search(r'class="search-input[^"]*"[^>]*value="([^"]*)"', c)
    empty = "没有找到你想要的宝贝" in c
    feeds = len(re.findall(r"feeds-item-wrap--", c))
    empty_feed = "empty-feed-container" in c
    t = re.search(r"<title[^>]*>([^<]+)", c)
    # look for result count UI
    count_hints = re.findall(r".{0,20}结果.{0,20}", c[:50000])
    text = (
        f"file={p.name}\n"
        f"input={m.group(1) if m else None}\n"
        f"title={t.group(1) if t else None}\n"
        f"empty={empty}\n"
        f"empty_feed={empty_feed}\n"
        f"feeds={feeds}\n"
        f"len={len(c)}\n"
        f"hints={count_hints[:5]}\n"
    )
    (art / f"{p.stem}_probe.txt").write_text(text, encoding="utf-8")
    print(text)
