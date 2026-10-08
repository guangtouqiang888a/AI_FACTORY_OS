"""V2 runtime/database baseline verification (stdlib unittest)."""

from __future__ import annotations

import ast
import importlib
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.main import OK_MESSAGE, healthcheck  # noqa: E402
from config.settings import SCHEMA_IDENTITY, SCHEMA_VERSION, Settings  # noqa: E402
from database.db import get_schema_info, initialize, reset, verify  # noqa: E402

LEGACY_IMPORT_MARKERS = (
    "0_START",
    "1_DATA",
    "3_DECISION",
    "6_EXECUTION",
    "7_MEMORY",
    "8_CONFIG",
    "9_PRODUCT",
    "10_DEPLOY",
    "11_CONTENT_FACTORY",
    "legacy_runtime",
    "commercial_assets",
)

V2_SOURCE_DIRS = (
    REPO_ROOT / "app",
    REPO_ROOT / "database",
    REPO_ROOT / "config",
    REPO_ROOT / "tests",
)


class TestV2Runtime(unittest.TestCase):
    def test_healthcheck_message(self) -> None:
        self.assertEqual(healthcheck(), OK_MESSAGE)
        self.assertEqual(healthcheck(), "AI_FACTORY_OS V2 runtime: OK")

    def test_main_module_entrypoint(self) -> None:
        mod = importlib.import_module("app.main")
        self.assertEqual(mod.main(), 0)


class TestV2Database(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(self._tmpdir.cleanup)
        self.db_path = Path(self._tmpdir.name) / "ai_factory_v2.db"
        self.settings = Settings(
            repo_root=REPO_ROOT,
            database_path=self.db_path,
            schema_identity=SCHEMA_IDENTITY,
            schema_version=SCHEMA_VERSION,
        )

    def test_initialize_and_schema(self) -> None:
        path = initialize(self.settings)
        self.assertTrue(path.exists())
        info = get_schema_info(self.settings)
        self.assertEqual(info["schema_identity"], SCHEMA_IDENTITY)
        self.assertEqual(info["schema_version"], SCHEMA_VERSION)
        self.assertEqual(info["initialization_status"], "initialized")
        verify(self.settings)

    def test_reset_reinitialize(self) -> None:
        initialize(self.settings)
        first = get_schema_info(self.settings)
        path = reset(self.settings)
        self.assertTrue(path.exists())
        second = verify(self.settings)
        self.assertEqual(second["schema_identity"], first["schema_identity"])
        self.assertEqual(second["schema_version"], SCHEMA_VERSION)
        self.assertEqual(second["initialization_status"], "initialized")


class TestLegacyIsolation(unittest.TestCase):
    def test_v2_sources_have_no_legacy_imports(self) -> None:
        offenders: list[str] = []
        for base in V2_SOURCE_DIRS:
            if not base.exists():
                continue
            for path in base.rglob("*.py"):
                source = path.read_text(encoding="utf-8")
                try:
                    tree = ast.parse(source, filename=str(path))
                except SyntaxError as exc:
                    offenders.append(f"{path}: syntax error {exc}")
                    continue
                for node in ast.walk(tree):
                    names: list[str] = []
                    if isinstance(node, ast.Import):
                        names = [alias.name for alias in node.names]
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        names = [node.module]
                    for name in names:
                        root = name.split(".")[0]
                        if root in LEGACY_IMPORT_MARKERS or any(
                            m in name for m in LEGACY_IMPORT_MARKERS
                        ):
                            offenders.append(f"{path}: import {name}")
        self.assertEqual(offenders, [], msg="\n".join(offenders))

    def test_legacy_runtime_archive_present(self) -> None:
        archive = REPO_ROOT / "99_ARCHIVE_RUNTIME" / "legacy_runtime"
        self.assertTrue(archive.is_dir())
        self.assertTrue((REPO_ROOT / "99_ARCHIVE_RUNTIME" / "database_history").is_dir())
        self.assertTrue((REPO_ROOT / "docs" / "99_ARCHIVE").is_dir())
        self.assertFalse(
            (REPO_ROOT / "99_ARCHIVE").exists(),
            msg="ambiguous root 99_ARCHIVE/ must not exist",
        )
        for name in (
            "0_START",
            "1_DATA",
            "3_DECISION",
            "6_EXECUTION",
            "7_MEMORY",
            "8_CONFIG",
            "9_PRODUCT",
            "10_DEPLOY",
            "11_CONTENT_FACTORY",
            "commercial_assets",
        ):
            self.assertTrue(
                (archive / name).exists(),
                msg=f"missing archived legacy path: {name}",
            )
            self.assertFalse(
                (REPO_ROOT / name).exists(),
                msg=f"legacy path still at Active Workspace root: {name}",
            )
        for name in ("2_COGNITION", "4_PRODUCT", "5_CONTENT", "data", "logs", "output"):
            self.assertFalse(
                (REPO_ROOT / name).exists(),
                msg=f"residual still at Active Workspace root: {name}",
            )


if __name__ == "__main__":
    unittest.main()
