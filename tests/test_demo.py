from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BUILDER = load_module("demo_builder", ROOT / "examples" / "demo" / "build_demo_db.py")
RUNNER = load_module("demo_query_runner", ROOT / "examples" / "demo" / "query_demo.py")


class DemoTests(unittest.TestCase):
    def test_all_demo_queries_execute_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "demo.sqlite"
            BUILDER.build_database(database)
            query_paths = sorted((ROOT / "examples" / "demo" / "queries").glob("*.sql"))
            self.assertGreaterEqual(len(query_paths), 4)
            for query_path in query_paths:
                with self.subTest(query=query_path.name):
                    result = RUNNER.execute_read_only(
                        database,
                        query_path.read_text(encoding="utf-8"),
                        max_rows=100,
                    )
                    self.assertTrue(result.get("ok"), result)
                    self.assertGreater(result.get("row_count", 0), 0)
                    self.assertFalse(result.get("truncated"))

    def test_demo_runner_refuses_write_sql(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "demo.sqlite"
            BUILDER.build_database(database)
            result = RUNNER.execute_read_only(
                database,
                "DELETE FROM example_analytics.daily_activity",
                max_rows=100,
            )
            self.assertFalse(result.get("ok"))
            self.assertTrue(result.get("errors"))


if __name__ == "__main__":
    unittest.main()
