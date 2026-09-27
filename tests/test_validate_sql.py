from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "sql-data-agent" / "scripts" / "validate_sql.py"
SPEC = importlib.util.spec_from_file_location("validate_sql", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ValidateSqlTests(unittest.TestCase):
    def codes(self, sql: str) -> set[str]:
        return {item.code for item in MODULE.validate(sql)}

    def test_allows_filtered_select(self) -> None:
        sql = "SELECT activity_date FROM metrics WHERE activity_date = DATE '2026-01-01' LIMIT 10;"
        self.assertEqual(self.codes(sql), set())

    def test_blocks_delete(self) -> None:
        self.assertIn("blocked_keyword", self.codes("DELETE FROM metrics WHERE id = 1"))

    def test_blocks_write_cte(self) -> None:
        sql = "WITH changed AS (UPDATE metrics SET value = 1 RETURNING *) SELECT * FROM changed"
        self.assertIn("blocked_keyword", self.codes(sql))

    def test_ignores_keywords_inside_literals_and_comments(self) -> None:
        sql = "SELECT 'drop table' AS text_value -- delete\nWHERE 1 = 1 LIMIT 1"
        self.assertNotIn("blocked_keyword", self.codes(sql))

    def test_blocks_multiple_statements(self) -> None:
        self.assertIn("multiple_statements", self.codes("SELECT 1; SELECT 2;"))

    def test_blocks_select_into(self) -> None:
        self.assertIn("blocked_keyword", self.codes("SELECT * INTO copied_table FROM source_table"))

    def test_blocks_locking_read(self) -> None:
        sql = "SELECT id FROM metrics WHERE id = 1 FOR UPDATE LIMIT 1"
        self.assertIn("locking_query", self.codes(sql))

    def test_blocks_side_effect_function(self) -> None:
        sql = "SELECT pg_read_file('/restricted/path') WHERE 1 = 1 LIMIT 1"
        self.assertIn("side_effect_function", self.codes(sql))

    def test_warns_on_unbounded_scan(self) -> None:
        codes = self.codes("SELECT event_name FROM product_events")
        self.assertIn("no_filter", codes)
        self.assertIn("no_limit", codes)


if __name__ == "__main__":
    unittest.main()
