from pathlib import Path
import re

c = Path("1_DATA/_tests/xianyu_interactive_061/page_dump_pass1.html").read_text(
    encoding="utf-8"
)
out = Path("1_DATA/_tests/xianyu_interactive_061")
print("len", len(c))
m = re.search(r'id="ice-container"([\s\S]{0,50000})', c)
inner = m.group(1) if m else ""
print("ice_snip_len", len(inner))
(out / "ice_inner_snip.txt").write_text(inner[:4000], encoding="utf-8")
for pat in [
    r"goofish\.com/item",
    r"/item/",
    r"itemId",
    r"wantNum",
    r"want",
    r"¥",
    r"￥",
    r"aria-label",
    r"feeds",
    r"Card",
    r"非法访问",
    r"登录",
]:
    print(pat, len(re.findall(pat, c, flags=re.I)))
t = re.sub(r"<script[\s\S]*?</script>", " ", c, flags=re.I)
t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
t = re.sub(r"<[^>]+>", " ", t)
t = re.sub(r"\s+", " ", t)
(out / "visible_text.txt").write_text(t[:5000], encoding="utf-8")
print("visible_head:", t[:400])
