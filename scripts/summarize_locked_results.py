#!/usr/bin/env python3
"""Summarize locked test-set tradeoffs from released CommitmentTrace results."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Any


POLICY_LABEL = {
    "fastest_broadcast": "Fastest",
    "semantic_value": "Semantic",
    "state_aware_aoii": "State-AoII",
    "action_admission": "Action adm.",
    "pressure_backpressure": "Pressure BP",
    "static_cpb": "Static CPB",
    "closed_loop_cpb": "C-CPB",
    "progress_guarded_cpb": "PG-C-CPB",
}

POLICY_ORDER = [
    "fastest_broadcast",
    "semantic_value",
    "state_aware_aoii",
    "action_admission",
    "pressure_backpressure",
    "static_cpb",
    "closed_loop_cpb",
    "progress_guarded_cpb",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def f(row: dict[str, str], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="artifact root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    results_dir = root / "results"
    rows = read_csv(results_dir / "test_metrics.csv")

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["policy_name"]].append(row)

    print("Locked test-set numerical summary")
    print("Policy          Cfg  FCE/msg  Prog/msg  Debt   Def/Rej")
    for policy in POLICY_ORDER:
        items = grouped.get(policy, [])
        if not items:
            continue
        cfgs = len({row["policy_config_id"] for row in items})
        generated = sum(f(row, "generated") for row in items)
        fce = sum(f(row, "false_commitment_exposure") for row in items) / max(1.0, generated)
        progress = sum(f(row, "true_progress") for row in items) / max(1.0, generated)
        debt = sum(f(row, "commitment_debt_end") for row in items) / len(items)
        defer = 100.0 * sum(f(row, "deferred") for row in items) / max(1.0, generated)
        reject = 100.0 * sum(f(row, "rejected") for row in items) / max(1.0, generated)
        print(f"{POLICY_LABEL[policy]:<14} {cfgs:>3}  {fce:>7.3f}  {progress:>8.3f}  {debt:>5.1f}  {defer:>4.1f}/{reject:>4.1f}")

    dominance_rows = read_csv(results_dir / "dominance_checks.csv")
    total = len(dominance_rows)
    dominated = sum(int(float(row.get("baseline_core_dominates_ccpb", "0"))) for row in dominance_rows)
    print()
    print(f"Core dominance checks: {dominated}/{total} baseline rows dominate selected PG-C-CPB rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
