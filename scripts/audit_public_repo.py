#!/usr/bin/env python3
"""Fail on common secrets, private paths, generated data, and local deny terms."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SKIP_DIRECTORIES = {".git", ".venv", "__pycache__", "node_modules"}
BLOCKED_SUFFIXES = {
    ".db",
    ".key",
    ".parquet",
    ".pem",
    ".sqlite",
    ".sqlite3",
    ".xlsx",
}
SECRET_PATTERNS = {
    "aws_access_key": re.compile(rb"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "github_token": re.compile(rb"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "openai_key": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "private_key": re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "database_url": re.compile(rb"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|snowflake)://[^\s]+", re.I),
    "home_path": re.compile(
        rb"(?:/" + rb"Users/[^/\s]+|/" + rb"home/[^/\s]+|[A-Za-z]:\\" + rb"Users\\[^\\\s]+)"
    ),
    "private_ipv4": re.compile(rb"\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3})\b"),
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRECTORIES for part in path.parts):
            continue
        if path.is_file():
            yield path


def load_local_deny_terms(root: Path) -> list[bytes]:
    path = root / "audit-denylist.local.txt"
    if not path.exists():
        return []
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            terms.append(value.casefold().encode("utf-8"))
    return terms


def audit(root: Path) -> list[str]:
    findings: list[str] = []
    deny_terms = load_local_deny_terms(root)

    for path in iter_files(root):
        relative = path.relative_to(root)
        if path.name == ".env":
            findings.append(f"blocked environment file: {relative}")
        if path.suffix.lower() in BLOCKED_SUFFIXES:
            findings.append(f"blocked generated or sensitive file type: {relative}")
        if path.stat().st_size > 1_000_000:
            findings.append(f"file exceeds 1 MB review threshold: {relative}")

        data = path.read_bytes()
        if b"\x00" in data:
            findings.append(f"binary file requires manual review: {relative}")
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                findings.append(f"{name} pattern: {relative}")
        folded = data.lower()
        for term in deny_terms:
            if term in folded:
                findings.append(f"local deny term found: {relative}")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    findings = audit(root)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}")
        return 1
    print("OK: no blocked files, secret patterns, private paths, or local deny terms found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
