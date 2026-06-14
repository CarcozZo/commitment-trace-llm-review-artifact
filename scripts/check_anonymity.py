#!/usr/bin/env python3
"""Scan the anonymous review artifact for common identity leaks."""

from __future__ import annotations

import argparse
import gzip
import re
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".csv",
    ".tsv",
    ".py",
    ".gz",
}

PATTERNS = {
    "windows_absolute_path": re.compile(r"[A-Za-z]:\\\\"),
    "unix_absolute_path": re.compile(r"(?<![A-Za-z0-9])/(home|root|Users|mnt|data|workspace|tmp)/[^\s\"']+", re.I),
    "local_project_path": re.compile(r"(my_SAGIN|auto_research_lab|Obsidian|Users\\\\|博士科研|格式的黄金甲)", re.I),
    "institution_marker": re.compile(r"(BUPT|Beijing University of Posts|北京邮电)", re.I),
    "private_server_marker": re.compile(r"(bupt_ANT|id_ed25519|root@|10\.112\.116\.151)", re.I),
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "ssh_key": re.compile(r"-----BEGIN (OPENSSH|RSA|DSA|EC) PRIVATE KEY-----"),
    "unresolved_public_doi": re.compile(r"\[repository name and DOI\]|\[version\]|\[data licence\]|\[software licence\]"),
}

ALLOWLIST_FILES = {
    "docs/DATA_AVAILABILITY.md",
    "docs/FAIR_CHECKLIST.md",
}


def read_text(path: Path) -> str:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as f:
            sample = f.read(2_000_000)
        return sample
    return path.read_text(encoding="utf-8", errors="replace")


def should_scan(path: Path) -> bool:
    if path.is_dir():
        return False
    if path.suffix in TEXT_SUFFIXES:
        return True
    if path.name in {"SHA256SUMS.txt", "RELEASE_MANIFEST.tsv"}:
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="artifact root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings: list[tuple[str, str]] = []

    for path in root.rglob("*"):
        if not should_scan(path):
            continue
        rel = path.relative_to(root).as_posix()
        if rel == "scripts/check_anonymity.py":
            continue
        text = read_text(path)
        for name, pattern in PATTERNS.items():
            if name == "unresolved_public_doi" and rel in ALLOWLIST_FILES:
                continue
            if pattern.search(text):
                findings.append((rel, name))

    if findings:
        print("verdict: FAIL")
        for rel, name in findings[:100]:
            print(f"- {rel}: {name}")
        if len(findings) > 100:
            print(f"- ... {len(findings) - 100} more")
        return 1
    print("verdict: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
