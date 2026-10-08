from pathlib import Path
import re

c = Path("1_DATA/_tests/xianyu_interactive_061/page_dump_pass1.html").read_text(
    encoding="utf-8"
)
out = Path("1_DATA/_tests/xianyu_interactive_061")
# find contexts around 想要
idxs = [m.start() for m in re.finditer("想要", c)]
print("want_count_occurrences", len(idxs))
snips = []
for i in idxs[:5]:
    snips.append(c[max(0, i - 400) : i + 200])
(out / "want_contexts.html").write_text("\n\n====\n\n".join(snips), encoding="utf-8")
# href patterns near cards
hrefs = re.findall(r'href="([^"]+)"', c)
interesting = [h for h in hrefs if any(x in h for x in ("item", "id=", "goods", "product", "idle"))]
(out / "interesting_hrefs.txt").write_text("\n".join(interesting[:80]), encoding="utf-8")
print("interesting_hrefs", len(interesting))
# class names containing card/feed/item
classes = set(re.findall(r'class="([^"]*(?:card|feed|item|goods|price|want)[^"]*)"', c, flags=re.I))
(out / "relevant_classes.txt").write_text("\n".join(sorted(classes)[:100]), encoding="utf-8")
print("classes", len(classes))
