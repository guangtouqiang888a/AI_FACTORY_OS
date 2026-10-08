# quick Current DB snapshot for Entry 060
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "8_CONFIG"), str(ROOT / "1_DATA")]
import database
import acquisition_engine as eng

eng.ensure_acquisition_engine_schema()
with database.get_connection() as conn:
    print("obs", conn.execute("select count(*) from market_observations").fetchone()[0])
    print("runs", list(conn.execute(
        "select run_id, status, acquisition_mode from collection_runs"
    )))
    print("collectors", list(conn.execute(
        "select collector_id, status from collectors "
        "where collector_id like '%xianyu%browser%' or collector_id like '%public_web%'"
    )))
