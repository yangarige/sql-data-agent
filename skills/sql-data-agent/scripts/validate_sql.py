#!/usr/bin/env python3
"""Conservative read-only SQL validator with no external dependencies."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


ALLOWED_STARTERS = {"select", "with", "show", "describe", "desc", "explain"}
BLOCKED_KEYWORDS = {
    "analyze",
    "alter",
    "attach",
    "call",
    "copy",
    "create",
    "delete",
    "drop",
    "detach",
    "execute",
    "export",
    "grant",
    "insert",
    "into",
    "load",
    "merge",
    "replace",
    "revoke",
    "truncate",
    "unload",
    "update",
    "upsert",
    "vacuum",
}

SIDE_EFFECT_FUNCTIONS = {
    "dblink",
    "http_get",
    "http_post",
    "load_file",
    "lo_export",
    "openrowset",
    "pg_ls_dir",
    "pg_read_file",
    "sys_eval",
    "xp_cmdshell",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str


def strip_comments_and_literals(sql: str) -> str:
    """Replace comments and quoted literals while preserving statement structure."""
    out: list[str] = []
    i = 0
    state = "code"
    quote = ""

    while i < len(sql):
        char = sql[i]
        nxt = sql[i + 1] if i + 1 < len(sql) else ""

        if state == "code":
            if char == "-" and nxt == "-":
                state = "line_comment"
                out.extend("  ")
                i += 2
                continue
            if char == "/" and nxt == "*":
                state = "block_comment"
                out.extend("  ")
                i += 2
                continue
            if char in {"'", '"', "`"}:
                state = "quoted"
                quote = char
                out.append(" ")
                i += 1
                continue
            out.append(char)
            i += 1
            continue

        if state == "line_comment":
            if char == "\n":
                state = "code"
                out.append("\n")
            else:
                out.append(" ")
            i += 1
            continue

        if state == "block_comment":
            if char == "*" and nxt == "/":
                state = "code"
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if char == "\n" else " ")
                i += 1
            continue

        if state == "quoted":
            if char == quote:
                if nxt == quote and quote in {"'", '"'}:
                    out.extend("  ")
                    i += 2
                    continue
                state = "code"
            out.append("\n" if char == "\n" else " ")
            i += 1

    return "".join(out)


def validate(sql: str) -> list[Finding]:
    cleaned = strip_comments_and_literals(sql)
    findings: list[Finding] = []
    words = re.findall(r"\b[a-z_]+\b", cleaned.lower())

    if not words:
        return [Finding("error", "empty_sql", "No SQL statement was found.")]

    if words[0] not in ALLOWED_STARTERS:
        findings.append(
            Finding(
                "error",
                "non_read_only_start",
                f"Statement starts with {words[0]!r}; only read-only statements are allowed.",
            )
        )

    blocked = sorted(set(words) & BLOCKED_KEYWORDS)
    if blocked:
        findings.append(
            Finding(
                "error",
                "blocked_keyword",
                "Blocked SQL keyword(s): " + ", ".join(blocked) + ".",
            )
        )

    functions = set(re.findall(r"\b([a-z_][a-z0-9_]*)\s*\(", cleaned.lower()))
    side_effects = sorted(functions & SIDE_EFFECT_FUNCTIONS)
    if side_effects:
        findings.append(
            Finding(
                "error",
                "side_effect_function",
                "Blocked side-effecting function(s): " + ", ".join(side_effects) + ".",
            )
        )

    if re.search(r"\bfor\s+update\b|\block\s+in\s+share\s+mode\b", cleaned.lower()):
        findings.append(
            Finding(
                "error",
                "locking_query",
                "Locking reads are not allowed in the read-only workflow.",
            )
        )

    statements = [part for part in cleaned.split(";") if part.strip()]
    if len(statements) != 1:
        findings.append(
            Finding("error", "multiple_statements", "Exactly one SQL statement is allowed.")
        )

    lowered = cleaned.lower()
    if re.search(r"\bselect\s+\*", lowered):
        findings.append(
            Finding("warning", "select_star", "Select only the columns needed for the analysis.")
        )

    if re.search(r"\bcross\s+join\b", lowered) or re.search(r"\bjoin\s+[^\n]+\s+on\s+1\s*=\s*1\b", lowered):
        findings.append(
            Finding("warning", "cartesian_join", "Review the Cartesian join and expected row count.")
        )

    if re.search(r"\bavg\s*\(\s*[a-z_][\w.]*?(?:rate|ratio|pct|percent)\s*\)", lowered):
        findings.append(
            Finding(
                "warning",
                "averaged_ratio",
                "Recompute the ratio from aggregated numerator and denominator.",
            )
        )

    if words[0] in {"select", "with"} and "from" in words:
        if "where" not in words:
            findings.append(
                Finding("warning", "no_filter", "The query has no WHERE clause; review scan scope.")
            )
        if "limit" not in words:
            findings.append(
                Finding("warning", "no_limit", "Exploratory queries should usually include LIMIT.")
            )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one read-only SQL statement.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("path", nargs="?", help="Path to a SQL file")
    source.add_argument("--sql", help="SQL text")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable findings")
    args = parser.parse_args()

    sql = args.sql if args.sql is not None else Path(args.path).read_text(encoding="utf-8")
    findings = validate(sql)

    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    elif findings:
        for item in findings:
            print(f"{item.severity.upper()} [{item.code}] {item.message}")
    else:
        print("OK: no issues found.")

    return 2 if any(item.severity == "error" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
