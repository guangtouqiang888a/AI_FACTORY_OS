# Entry 080-B — Data Foundation automated tests (temp DB; never pollutes Current with fixtures)

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "8_CONFIG"))
sys.path.insert(0, str(ROOT / "1_DATA"))

import config  # noqa: E402
import database  # noqa: E402
import market_source_core as msc  # noqa: E402
import data_foundation_080b as df  # noqa: E402


class Entry080BDataFoundationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        base = Path(self._tmpdir.name)
        self.db_path = base / "test_080b.db"
        self._patches = [
            mock.patch.object(config, "DB_PATH", self.db_path),
            mock.patch.object(config, "DATA_DIR", base),
        ]
        for p in self._patches:
            p.start()
        msc.ensure_market_source_schema()
        df.ensure_data_foundation_schema()

    def tearDown(self) -> None:
        for p in self._patches:
            p.stop()
        self._tmpdir.cleanup()

    def _insert_obs(self, **over) -> tuple[bool, str]:
        base = {
            "source_id": "src_xianyu_marketplace",
            "source": "xianyu",
            "platform": "xianyu",
            "source_item_id": over.pop("source_item_id", "item_1001"),
            "source_url": over.pop(
                "source_url", "https://www.goofish.com/item?id=item_1001"
            ),
            "title": over.pop("title", "Excel模板测试"),
            "price": over.pop("price", 9.9),
            "want_count": over.pop("want_count", None),
            "view_count": over.pop("view_count", None),
            "data_origin": over.pop("data_origin", msc.ORIGIN_REAL),
            "verification_status": over.pop(
                "verification_status", msc.VERIF_MANUAL
            ),
            "observed_at": over.pop("observed_at", "2026-09-03T15:20:02+08:00"),
            "collection_query": over.pop("collection_query", "Excel模板"),
            "want_count_status": over.pop("want_count_status", "MISSING_ON_CARD"),
            "run_id": over.pop("run_id", None),
        }
        base.update(over)
        return msc.insert_market_observation(base)

    def test_01_schema_additive_columns(self) -> None:
        with database.get_connection() as conn:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(market_observations)")}
            for c in (
                "collection_query",
                "keyword_id",
                "want_count_status",
                "image_url",
                "result_position",
                "product_identity_id",
                "evidence_level",
            ):
                self.assertIn(c, cols)
            tables = {
                r[0]
                for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            }
            self.assertIn("market_product_identities", tables)

    def test_02_want_and_view_null_preserved(self) -> None:
        ok, oid = self._insert_obs(want_count=None, view_count=None)
        self.assertTrue(ok)
        with database.get_connection() as conn:
            row = dict(
                conn.execute(
                    "SELECT want_count, view_count FROM market_observations WHERE observation_id=?",
                    (oid,),
                ).fetchone()
            )
        self.assertIsNone(row["want_count"])
        self.assertIsNone(row["view_count"])

    def test_03_keyword_create_retrieve_dedupe(self) -> None:
        a = df.upsert_keyword_foundation(
            "Excel模板",
            keyword_source=df.KEYWORD_SOURCE_SEED,
            discovery_class=df.DISCOVERY_SEED,
            evidence_status=df.EVIDENCE_STATUS_HYPOTHESIS,
        )
        b = df.upsert_keyword_foundation(
            "Excel模板",
            evidence_status=df.EVIDENCE_STATUS_EVIDENCE_BACKED,
        )
        self.assertEqual(a["id"], b["id"])
        self.assertEqual(b["keyword"], "Excel模板")
        self.assertEqual(b["discovery_class"], df.DISCOVERY_SEED)
        self.assertEqual(b["evidence_status"], df.EVIDENCE_STATUS_EVIDENCE_BACKED)
        got = df.get_keyword_by_text("Excel模板")
        self.assertIsNotNone(got)
        self.assertEqual(got["id"], a["id"])
        with database.get_connection() as conn:
            n = conn.execute("SELECT COUNT(*) FROM keywords WHERE keyword=?", ("Excel模板",)).fetchone()[0]
        self.assertEqual(n, 1)

    def test_04_run_observation_keyword_linkage(self) -> None:
        run_id = msc.start_collection_run(
            source_id="src_xianyu_marketplace",
            source="xianyu",
            platform="xianyu",
            collection_mode=msc.MODE_IMPORT,
            collection_query="Excel模板",
            acquisition_mode="BROWSER_EXTENSION",
        )
        ok, oid = self._insert_obs(run_id=run_id, collection_query="Excel模板", want_count=50)
        self.assertTrue(ok)
        msc.finish_collection_run(
            run_id,
            {
                "raw_count": 1,
                "accepted_count": 1,
                "duplicate_count": 0,
                "requested_depth": 1,
                "actual_depth": 1,
                "stop_reason": "max_records",
            },
        )
        with database.get_connection() as conn:
            obs = dict(
                conn.execute(
                    "SELECT * FROM market_observations WHERE observation_id=?", (oid,)
                ).fetchone()
            )
            run = dict(
                conn.execute(
                    "SELECT * FROM collection_runs WHERE run_id=?", (run_id,)
                ).fetchone()
            )
            kw = dict(conn.execute("SELECT * FROM keywords WHERE keyword=?", ("Excel模板",)).fetchone())
        self.assertEqual(obs["run_id"], run_id)
        self.assertEqual(obs["collection_query"], "Excel模板")
        self.assertEqual(obs["keyword_id"], kw["id"])
        self.assertEqual(obs["evidence_level"], df.EVIDENCE_REAL_OBSERVATION)
        self.assertEqual(run["actual_depth"], 1)
        self.assertEqual(run["stop_reason"], "max_records")

    def test_05_product_identity_across_timestamps(self) -> None:
        ok1, oid1 = self._insert_obs(
            source_item_id="same_item",
            source_url="https://www.goofish.com/item?id=same_item",
            observed_at="2026-09-03T10:00:00+08:00",
            want_count=10,
        )
        ok2, oid2 = self._insert_obs(
            source_item_id="same_item",
            source_url="https://www.goofish.com/item?id=same_item",
            observed_at="2026-09-04T10:00:00+08:00",
            want_count=12,
        )
        self.assertTrue(ok1)
        self.assertTrue(ok2)
        self.assertNotEqual(oid1, oid2)
        with database.get_connection() as conn:
            rows = [
                dict(r)
                for r in conn.execute(
                    "SELECT observation_id, product_identity_id, observed_at "
                    "FROM market_observations WHERE source_item_id='same_item' "
                    "ORDER BY observed_at"
                )
            ]
            pids = {
                r[0]
                for r in conn.execute(
                    "SELECT product_identity_id FROM market_product_identities "
                    "WHERE source_item_id='same_item'"
                )
            }
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["product_identity_id"], rows[1]["product_identity_id"])
        self.assertEqual(len(pids), 1)
        # Same observed_at = duplicate protection
        ok3, reason = self._insert_obs(
            source_item_id="same_item",
            source_url="https://www.goofish.com/item?id=same_item",
            observed_at="2026-09-03T10:00:00+08:00",
        )
        self.assertFalse(ok3)
        self.assertEqual(reason, "duplicate")

    def test_06_provenance_mapping(self) -> None:
        self.assertEqual(df.map_evidence_level("REAL"), df.EVIDENCE_REAL_OBSERVATION)
        self.assertEqual(df.map_evidence_level("SAMPLE"), df.EVIDENCE_SAMPLE)
        self.assertEqual(df.map_evidence_level("TEST_FIXTURE"), df.EVIDENCE_TEST)
        self.assertEqual(df.map_evidence_level("SIMULATION"), df.EVIDENCE_SIMULATION)
        self.assertEqual(df.map_evidence_level("HYPOTHESIS"), df.EVIDENCE_HYPOTHESIS)
        self.assertNotEqual(df.EVIDENCE_HYPOTHESIS, df.EVIDENCE_REAL_OBSERVATION)
        self.assertNotEqual(df.EVIDENCE_TEST, df.EVIDENCE_REAL_OBSERVATION)

    def test_07_backfill_preserves_nulls(self) -> None:
        # Seed two rows with notes/query then backfill
        run_id = msc.start_collection_run(
            source_id="src_xianyu_marketplace",
            source="xianyu",
            platform="xianyu",
            collection_mode=msc.MODE_IMPORT,
            collection_query="Excel模板",
        )
        notes = json.dumps(
            {"query": "Excel模板", "want_count_status": "MISSING_ON_CARD"},
            ensure_ascii=False,
        )
        ok, oid = self._insert_obs(
            run_id=run_id,
            want_count=None,
            view_count=None,
            notes=notes,
            collection_query=None,
            want_count_status=None,
        )
        self.assertTrue(ok)
        # Clear additive fields to simulate pre-080b row shape for backfill path
        with database.get_connection() as conn:
            conn.execute(
                """
                UPDATE market_observations SET
                    collection_query=NULL, keyword_id=NULL, want_count_status=NULL,
                    product_identity_id=NULL, evidence_level=NULL
                WHERE observation_id=?
                """,
                (oid,),
            )
            conn.commit()
        report = df.backfill_existing_observations()
        self.assertTrue(report["preservation_ok"])
        with database.get_connection() as conn:
            row = dict(
                conn.execute(
                    "SELECT want_count, view_count, collection_query, keyword_id, "
                    "want_count_status, evidence_level, product_identity_id "
                    "FROM market_observations WHERE observation_id=?",
                    (oid,),
                ).fetchone()
            )
        self.assertIsNone(row["want_count"])
        self.assertIsNone(row["view_count"])
        self.assertEqual(row["collection_query"], "Excel模板")
        self.assertIsNotNone(row["keyword_id"])
        self.assertEqual(row["want_count_status"], "MISSING_ON_CARD")
        self.assertEqual(row["evidence_level"], df.EVIDENCE_REAL_OBSERVATION)
        self.assertIsNotNone(row["product_identity_id"])


if __name__ == "__main__":
    unittest.main()
