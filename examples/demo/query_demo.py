#!/usr/bin/env python3
"""Execute one validated read-only query against the fictional demo database."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sqlite3
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "skills" / "sql-data-agent" / "scripts" / "validate_sql.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("sql_data_agent_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load SQL validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def execute_read_only(database: Path, sql: str, max_rows: int) -> dict:
    validator = load_validator()
    findings = validator.validate(sql)
    errors = [item for item in findings if item.severity == "error"]
    if errors:
        return {
            "ok": False,
            "errors": [item.message for item in errors],
            "warnings": [item.message for item in findings if item.severity == "warning"],
        }

    if not database.is_file():
        return {"ok": False, "errors": [f"Database does not exist: {database}"]}

    started = time.perf_counter()
    connection = sqlite3.connect(":memory:", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        database_uri = f"file:{database.resolve().as_posix()}?mode=ro"
        connection.execute("ATTACH DATABASE ? AS example_analytics", (database_uri,))
        cursor = connection.execute(sql)
        fetched = cursor.fetchmany(max_rows + 1)
        truncated = len(fetched) > max_rows
        rows = fetched[:max_rows]
        columns = [item[0] for item in cursor.description or []]
    except sqlite3.Error as exc:
        return {"ok": False, "errors": [str(exc)]}
    finally:
        connection.close()

    return {
        "ok": True,
        "columns": columns,
        "rows": [dict(row) for row in rows],
        "row_count": len(rows),
        "truncated": truncated,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "warnings": [item.message for item in findings if item.severity == "warning"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("query", type=Path)
    parser.add_argument("--max-rows", type=int, default=100)
    args = parser.parse_args()
    if args.max_rows < 1 or args.max_rows > 1000:
        parser.error("--max-rows must be between 1 and 1000")

    sql = args.query.read_text(encoding="utf-8")
    result = execute_read_only(args.database.resolve(), sql, args.max_rows)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
