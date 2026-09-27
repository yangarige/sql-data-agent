#!/usr/bin/env python3
"""Build a deterministic SQLite database containing fictional analytics data."""

from __future__ import annotations

import argparse
import sqlite3
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "demo.sqlite"
SCHEMA_PATH = ROOT / "examples" / "example_schema.sql"


def build_database(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    schema = SCHEMA_PATH.read_text(encoding="utf-8").replace("example_analytics.", "")
    connection = sqlite3.connect(output)
    try:
        connection.executescript(schema)

        activity_rows = []
        segments = {
            "free": (1000, 7),
            "pro": (420, 4),
            "team": (180, 2),
        }
        start = date(2026, 1, 1)
        for offset in range(28):
            current = start + timedelta(days=offset)
            for segment, (base, growth) in segments.items():
                active = base + growth * offset
                if current == date(2026, 1, 28) and segment == "free":
                    active -= 180
                sessions = int(active * (1.35 if segment == "free" else 1.65))
                activity_rows.append((current.isoformat(), segment, active, sessions))
        connection.executemany(
            "INSERT INTO daily_activity VALUES (?, ?, ?, ?)", activity_rows
        )

        acquisition_rows = []
        channel_rules = {
            "organic": (520, 3, 0.24, 0.62),
            "search": (340, 2, 0.19, 0.57),
            "partner": (160, 1, 0.13, 0.49),
        }
        for offset in range(31):
            current = start + timedelta(days=offset)
            for channel, (base, growth, signup_rate, activation_rate) in channel_rules.items():
                visitors = base + growth * offset
                signups = int(visitors * signup_rate)
                activated = int(signups * activation_rate)
                acquisition_rows.append(
                    (current.isoformat(), channel, visitors, signups, activated)
                )
        connection.executemany(
            "INSERT INTO acquisition_funnel VALUES (?, ?, ?, ?, ?)",
            acquisition_rows,
        )

        retention_rows = []
        cohort_dates = [date(2026, 1, day) for day in (1, 8, 15, 22)]
        retention_rules = {
            "free": (800, 0.42, 0.21),
            "pro": (260, 0.58, 0.37),
            "team": (110, 0.67, 0.49),
        }
        for cohort_index, cohort_date in enumerate(cohort_dates):
            for segment, (base_size, day_1_rate, day_7_rate) in retention_rules.items():
                cohort_users = base_size + cohort_index * 20
                retention_rows.extend(
                    [
                        (
                            cohort_date.isoformat(),
                            1,
                            segment,
                            cohort_users,
                            int(cohort_users * day_1_rate),
                        ),
                        (
                            cohort_date.isoformat(),
                            7,
                            segment,
                            cohort_users,
                            int(cohort_users * day_7_rate),
                        ),
                    ]
                )
        connection.executemany(
            "INSERT INTO retention_cohorts VALUES (?, ?, ?, ?, ?)",
            retention_rows,
        )
        connection.commit()
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    build_database(output)
    print(f"Created fictional demo database: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
