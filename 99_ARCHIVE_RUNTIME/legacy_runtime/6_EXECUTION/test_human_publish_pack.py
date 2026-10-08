# Entry 056 — Human Publish Pack + Publish Evidence Preparation tests

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "6_EXECUTION"))
sys.path.insert(0, str(ROOT / "8_CONFIG"))

import human_publish_pack as hpp  # noqa: E402
import publish_queue as pq  # noqa: E402


ASSET = "f2f8bab97df8"
LEGACY = "8523329941d4"
QUEUE = "pq_auto_f2f8bab97df8"


class Entry056HumanPublishPackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = hpp.materialize_human_publish_pack(ASSET)

    def test_01_autonomous_product_not_legacy(self) -> None:
        self.assertNotEqual(ASSET, LEGACY)
        snap = hpp.build_reality_snapshot(ASSET)
        self.assertTrue(snap["ok"])
        self.assertIn("AUTONOMOUSLY", snap["selection_origin"])
        self.assertFalse(snap["commercially_validated"])
        self.assertTrue(snap["legacy_pilot_isolated"])

    def test_02_legacy_isolated(self) -> None:
        bad = hpp.build_reality_snapshot(LEGACY)
        self.assertFalse(bad["ok"])
        self.assertEqual(bad["reason"], "legacy_pilot_isolated")

    def test_03_asset_integrity(self) -> None:
        integ = hpp.verify_asset_integrity(ASSET)
        self.assertTrue(integ["ok"], integ.get("blockers"))
        self.assertFalse(integ["publish_readiness_blocked"])
        types = {a["type"] for a in integ["assets"]}
        self.assertTrue("xlsx" in types or any(a.get("openable_ooxml_zip") for a in integ["assets"]))

    def test_04_listing_package(self) -> None:
        listing = hpp.find_listing(ASSET)
        self.assertIsNotNone(listing)
        pkg = hpp.package_dir_from_listing(listing, ASSET)
        ev = hpp.verify_listing_package(pkg)
        self.assertTrue(ev["ok"], ev.get("missing"))

    def test_05_queue_awaiting_human(self) -> None:
        entry = pq.get_queue_entry(QUEUE)
        self.assertIsNotNone(entry)
        self.assertEqual(entry["queue_status"], pq.QUEUE_AWAITING_HUMAN)

    def test_06_no_publish_evidence(self) -> None:
        self.assertEqual(hpp.count_publish_evidence(QUEUE), 0)

    def test_07_pack_files_exist(self) -> None:
        self.assertTrue(self.result["ok"])
        paths = self.result["paths"]
        self.assertTrue(Path(paths["human_publish_pack"]).exists())
        self.assertTrue(Path(paths["decision_pack_alias"]).exists())
        self.assertTrue(Path(paths["evidence_template"]).exists())
        tpl = json.loads(Path(paths["evidence_template"]).read_text(encoding="utf-8"))
        self.assertEqual(tpl["status"], "TEMPLATE_ONLY_NOT_RECORDED")
        self.assertEqual(tpl["fields_to_fill"]["listing_reference"], "")

    def test_08_price_boundary_labels(self) -> None:
        snap = hpp.build_reality_snapshot(ASSET)
        self.assertTrue(snap["price"]["ai_recommendation_only"])
        self.assertIsNone(snap["price"]["actual_paid_price"])
        self.assertEqual(snap["price"]["price_hypothesis"], 99.9)

    def test_09_platform_reported_from_reality(self) -> None:
        snap = hpp.build_reality_snapshot(ASSET)
        self.assertEqual(snap["platform"]["system_recorded_platform"], "xianyu")
        self.assertIsNone(snap["platform"]["human_confirmed_platform"])

    def test_10_observation_not_started(self) -> None:
        snap = hpp.build_reality_snapshot(ASSET)
        self.assertEqual(snap["observation"]["observation_status"], "NOT_STARTED")
        self.assertFalse(snap["observation"]["observation_may_start"])
        self.assertEqual(snap["commercial_learning"], "NONE")

    def test_11_evidence_api_rejects_empty_reference(self) -> None:
        r = pq.record_publish_evidence({
            "queue_id": QUEUE,
            "listing_reference": "",
            "verification_status": "MANUAL_VERIFIED",
        })
        self.assertFalse(r["accepted"])
        self.assertEqual(pq.get_queue_entry(QUEUE)["queue_status"], pq.QUEUE_AWAITING_HUMAN)

    def test_12_evidence_api_rejects_unverified(self) -> None:
        r = pq.record_publish_evidence({
            "queue_id": QUEUE,
            "listing_reference": "https://example.invalid/fake",
            "verification_status": "UNVERIFIED",
        })
        self.assertFalse(r["accepted"])
        self.assertEqual(r["reason"], "unverified_evidence_rejected")
        # still no evidence row accepted; queue unchanged
        self.assertEqual(hpp.count_publish_evidence(QUEUE), 0)
        self.assertEqual(pq.get_queue_entry(QUEUE)["queue_status"], pq.QUEUE_AWAITING_HUMAN)

    def test_13_future_product_type_struct(self) -> None:
        # Pack identity uses string product_type — video would not break field shape
        snap = hpp.build_reality_snapshot(ASSET)
        self.assertIsInstance(snap["product_identity"]["product_type"], str)
        template = hpp.build_publish_evidence_template(
            QUEUE, {"platform": "future_platform", "listing_id": "x"}, {"commercial_product_id": "y", "product_asset_id": ASSET}
        )
        self.assertEqual(template["fields_to_fill"]["platform"], "future_platform")

    def test_14_ready_for_human_external_action(self) -> None:
        self.assertEqual(self.result["publish_readiness"], "READY FOR HUMAN EXTERNAL ACTION")
        self.assertFalse(self.result["published"])


if __name__ == "__main__":
    unittest.main()
