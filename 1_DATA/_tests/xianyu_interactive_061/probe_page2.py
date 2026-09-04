from pathlib import Path
import re

c = Path("1_DATA/_tests/xianyu_interactive_061/page_dump_pass1.html").read_text(
    encoding="utf-8"
)
out = Path("1_DATA/_tests/xianyu_interactive_061")
# find content region signals
keys = [
    "feedsList",
    "feed",
    "searchList",
    "empty",
    "loading",
    "骨架",
    "暂无",
    "没有找到",
    "content-container",
    "want",
    "想要",
    "price",
    "元",
]
lines = []
for k in keys:
    lines.append(f"{k}\t{c.count(k)}")
# extract last part of ice-container-ish content area
idx = c.find('id="content"')
snip = c[idx : idx + 8000] if idx >= 0 else ""
(out / "content_snip.txt").write_text(snip, encoding="utf-8")
t = re.sub(r"<script[\s\S]*?</script>", " ", c, flags=re.I)
t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
t = re.sub(r"<[^>]+>", " ", t)
t = re.sub(r"\s+", " ", t)
(out / "visible_text.txt").write_text(t[:6000], encoding="utf-8")
(out / "probe_counts.txt").write_text("\n".join(lines), encoding="utf-8")
print("wrote")
