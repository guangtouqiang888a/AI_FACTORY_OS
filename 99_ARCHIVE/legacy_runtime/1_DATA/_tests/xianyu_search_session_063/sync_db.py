import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "1_DATA"), str(ROOT / "8_CONFIG")]
import acquisition_engine as e
import database
e.ensure_acquisition_engine_schema()
with database.get_connection() as c:
    print("obs", c.execute("select count(*) from market_observations").fetchone()[0])
    for r in c.execute(
        "select collector_id, status from collectors "
        "where collector_id in ('col_xianyu_search_session','col_xianyu_targeted_search')"
    ):
        print(dict(r))
