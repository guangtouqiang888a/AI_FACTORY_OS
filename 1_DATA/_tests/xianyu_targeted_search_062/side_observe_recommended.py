# Post-process last page dump: recommended-only want_count side observation
# NOT counted as SEARCH_RESULT / FIRST_REAL_SEARCH_BATCH.

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "1_DATA"), str(ROOT / "8_CONFIG")]

from connectors.xianyu_targeted_search_062 import (  # noqa: E402
    ARTIFACT_DIR,
    ORIGIN_RECOMMENDED,
    ORIGIN_SEARCH,
    extract_classified_cards,
    field_availability_search,
    filter_search_results,
    want_count_audit,
)

dumps = sorted(ARTIFACT_DIR.glob("page_dump_*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
if not dumps:
    print("no dumps")
    raise SystemExit(1)
html = dumps[0].read_text(encoding="utf-8")
all_cards = extract_classified_cards(html, max_records=50)
search = filter_search_results(all_cards, 20)
rec = [c for c in all_cards if c.get("result_origin") == ORIGIN_RECOMMENDED][:20]
# Side observation only
side = {
    "purpose": "want_count_visibility_on_visible_cards_when_primary_search_empty",
    "dump_file": dumps[0].name,
    "search_result_count": len(search),
    "recommended_sampled": len(rec),
    "recommended_want_audit": want_count_audit(
        [
            {
                **r,
                # treat recommended as pseudo for status distribution only
                "result_origin": ORIGIN_SEARCH,
            }
            for r in rec
        ]
    )
    if rec
    else None,
    "recommended_field_availability": field_availability_search(rec) if rec else None,
    "warning": (
        "RECOMMENDED_RESULT only. Must NOT be used as query-specific SEARCH_RESULT "
        "evidence or FIRST_REAL_XIANYU_SEARCH_BATCH."
    ),
    "login_causation": "NOT_PROVEN",
}
(ARTIFACT_DIR / "recommended_want_side_observation.json").write_text(
    json.dumps(side, ensure_ascii=False, indent=2), encoding="utf-8"
)
# Ensure search want audit exists even when empty
empty_audit = want_count_audit([])
empty_avail = field_availability_search([])
meta_path = ARTIFACT_DIR / "run_metadata.json"
meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
meta["want_count_audit"] = empty_audit
meta["field_availability"] = empty_avail
meta["recommended_side_observation_file"] = "recommended_want_side_observation.json"
meta["attempt_note"] = (
    "Multiple queries (digital templates + high-volume) returned primary empty + 猜你喜欢 "
    "in anonymous interactive Chrome. SEARCH_RESULT batch not obtained. "
    "Recommendations excluded from target batch."
)
meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
(ARTIFACT_DIR / "want_count_audit.json").write_text(
    json.dumps(empty_audit, ensure_ascii=False, indent=2), encoding="utf-8"
)
(ARTIFACT_DIR / "field_availability.json").write_text(
    json.dumps(empty_avail, ensure_ascii=False, indent=2), encoding="utf-8"
)
(ARTIFACT_DIR / "extracted_records.json").write_text("[]\n", encoding="utf-8")
print(json.dumps({
    "dump": dumps[0].name,
    "search": len(search),
    "recommended": len(rec),
    "rec_want_visible": (side.get("recommended_want_audit") or {}).get("status_distribution"),
}, ensure_ascii=False, indent=2))
