from pathlib import Path
import re

c = Path("1_DATA/_tests/xianyu_interactive_061/page_dump_pass1.html").read_text(
    encoding="utf-8"
)
out = Path("1_DATA/_tests/xianyu_interactive_061")
# one feeds-item-wrap block
m = re.search(r'feeds-item-wrap--[^"]*"[\s\S]{0,2500}', c)
(out / "one_card.html").write_text(m.group(0) if m else "NONE", encoding="utf-8")
print("card_found", bool(m))
print("feeds_item_wrap", len(re.findall(r"feeds-item-wrap--", c)))
print("item_qid", len(re.findall(r"/item\?id=\d+", c)))
