# Entry 080-C — correct historical observation engagement_signal 0.0 misread (NULL views)
# Does NOT mutate observations, selection_results, products, or a949.

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import data_foundation_080b as df  # noqa: E402


NOTE_SUFFIX = (
    " | Entry 080-C: engagement corrected — view_count all NULL so "
    "want_per_view is UNAVAILABLE (was 0.0 misread; NULL ≠ 0)"
)


def correct_observation_engagement_zero_misread() -> dict:
    before = df.snapshot_observation_integrity()
    updated = []
    with sqlite3.connect(config.DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT signal_id, value, unit, notes, source
            FROM market_signals
            WHERE signal_type='engagement_signal'
              AND unit='want_per_view'
              AND value = 0
              AND (notes LIKE '%observation_candidate_lineage%'
                   OR source='market_observation')
            """
        ).fetchall()
        for r in rows:
            notes = (r["notes"] or "") + NOTE_SUFFIX
            conn.execute(
                "UPDATE market_signals SET value=NULL, notes=? WHERE signal_id=?",
                (notes, r["signal_id"]),
            )
            updated.append(r["signal_id"])
        conn.commit()
    after = df.snapshot_observation_integrity()
    return {
        "entry": "080-C",
        "engagement_signals_corrected": updated,
        "observation_preservation_ok": before == after,
        "before": before,
        "after": after,
    }


if __name__ == "__main__":
    print(json.dumps(correct_observation_engagement_zero_misread(), ensure_ascii=False, indent=2))
