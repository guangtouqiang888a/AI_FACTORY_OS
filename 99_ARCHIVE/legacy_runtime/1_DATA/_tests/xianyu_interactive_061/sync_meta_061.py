import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "8_CONFIG"), str(ROOT / "1_DATA")]
import acquisition_engine as eng
import database

eng.ensure_acquisition_engine_schema()
art = ROOT / "1_DATA" / "_tests" / "xianyu_interactive_061"
meta = json.loads((art / "run_metadata.json").read_text(encoding="utf-8"))
recs = json.loads((art / "extracted_records.json").read_text(encoding="utf-8"))
meta["search_primary_empty"] = bool(recs and recs[0].get("search_primary_empty"))
meta["page_section"] = recs[0].get("page_section") if recs else None
(art / "run_metadata.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
)
with database.get_connection() as conn:
    print("obs", conn.execute("select count(*) from market_observations").fetchone()[0])
    rows = conn.execute(
        "select collector_id, status, version from collectors "
        "where collector_id like '%browser%'"
    ).fetchall()
    for r in rows:
        print(dict(r))
