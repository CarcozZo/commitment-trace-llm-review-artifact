#!/usr/bin/env python3
"""Audit dataset traceability and online-observation boundaries."""

from __future__ import annotations

import argparse
import gzip
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


JSONL_FILES = {
    "claims": "claims.jsonl.gz",
    "raw_agent_responses": "raw_agent_responses.jsonl.gz",
    "transition_labels": "transition_labels.jsonl.gz",
    "verifier_outcomes": "verifier_outcomes.jsonl.gz",
    "network_states": "network_states.jsonl.gz",
    "policy_replay_events": "policy_replay_events.jsonl.gz",
}

FORBIDDEN_ONLINE_FEATURE_KEYS = {
    "truth_label",
    "truth_source",
    "truth_label_after_verification",
    "verifier_result",
    "future_verifier_outcome",
    "future_downstream_action",
    "hindsight_fce",
    "fce_increment",
    "true_progress_increment",
}

REQUIRED_STRESS_FEATURES = {
    "verifier_capacity",
    "packet_capacity",
    "estimated_fanout",
    "resource_utilization",
    "verifier_queue_length",
    "commitment_debt",
}

ROLES = {"planner", "executor", "verifier", "network_controller"}


def open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with open_text(path) as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: record is not an object")
            yield row


def load_rows(data_dir: Path, logical_name: str) -> list[dict[str, Any]]:
    return list(read_jsonl(data_dir / JSONL_FILES[logical_name]))


def split_audit(data_dir: Path, claim_ids: set[str]) -> tuple[dict[str, int], list[str]]:
    errors: list[str] = []
    splits = json.loads((data_dir / "splits.json").read_text(encoding="utf-8"))
    split_counts = {name: len(items) for name, items in splits.items()}
    owner: dict[str, str] = {}
    for split_name, items in splits.items():
        for claim_id in items:
            if claim_id in owner:
                errors.append(f"claim {claim_id} appears in both {owner[claim_id]} and {split_name}")
            owner[claim_id] = split_name
            if claim_id not in claim_ids:
                errors.append(f"split {split_name} references unknown claim {claim_id}")
    missing = claim_ids.difference(owner)
    if missing:
        errors.append(f"{len(missing)} claims are not assigned to any split")
    return split_counts, errors


def online_feature_audit(events: list[dict[str, Any]]) -> tuple[Counter[str], int, int]:
    stress_coverage: Counter[str] = Counter()
    forbidden_rows = 0
    hidden_flag_errors = 0
    for row in events:
        if row.get("hidden_fields_excluded") is not True:
            hidden_flag_errors += 1
        features = json.loads(row["online_features_json"])
        if FORBIDDEN_ONLINE_FEATURE_KEYS.intersection(features.keys()):
            forbidden_rows += 1
        for key in REQUIRED_STRESS_FEATURES:
            if key in features:
                stress_coverage[key] += 1
    return stress_coverage, forbidden_rows, hidden_flag_errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="artifact root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data_dir = root / "data"

    claims = load_rows(data_dir, "claims")
    raw = load_rows(data_dir, "raw_agent_responses")
    transitions = load_rows(data_dir, "transition_labels")
    outcomes = load_rows(data_dir, "verifier_outcomes")
    events = load_rows(data_dir, "policy_replay_events")
    network_states = load_rows(data_dir, "network_states")

    errors: list[str] = []
    claim_ids = {row["claim_id"] for row in claims}

    split_counts, split_errors = split_audit(data_dir, claim_ids)
    errors.extend(split_errors)

    for name, rows in [
        ("transition_labels", transitions),
        ("verifier_outcomes", outcomes),
        ("policy_replay_events", events),
    ]:
        unknown = sum(1 for row in rows if row["claim_id"] not in claim_ids)
        if unknown:
            errors.append(f"{name}: {unknown} rows reference unknown claims")

    transition_roles: dict[str, set[str]] = defaultdict(set)
    raw_roles: dict[str, set[str]] = defaultdict(set)
    for row in transitions:
        transition_roles[row["claim_id"]].add(row["role"])
    for row in raw:
        raw_roles[row["claim_id"]].add(row["role"])

    complete_transition_claims = sum(1 for roles in transition_roles.values() if roles == ROLES)
    complete_raw_claims = sum(1 for roles in raw_roles.values() if roles == ROLES)
    if complete_transition_claims != len(claim_ids):
        errors.append("not every claim has four transition-label roles")
    if complete_raw_claims != len(claim_ids):
        errors.append("not every claim has four raw-response roles")

    stress_coverage, forbidden_rows, hidden_flag_errors = online_feature_audit(events)
    if forbidden_rows:
        errors.append(f"{forbidden_rows} policy events expose forbidden online feature keys")
    if hidden_flag_errors:
        errors.append(f"{hidden_flag_errors} policy events have hidden_fields_excluded != true")
    missing_stress = {
        key: len(events) - stress_coverage[key]
        for key in REQUIRED_STRESS_FEATURES
        if stress_coverage[key] != len(events)
    }
    if missing_stress:
        errors.append(f"stress feature coverage is incomplete: {missing_stress}")

    confidence = [float(row["label_confidence"]) for row in transitions]
    state_counts = Counter(row["intended_action_state"] for row in transitions)
    type_counts = Counter(row["commitment_type"] for row in transitions)
    role_counts = Counter(row["role"] for row in transitions)
    regime_counts = Counter(row["regime"] for row in events)
    split_event_counts = Counter(row["split"] for row in events)

    print(f"verdict: {'PASS' if not errors else 'FAIL'}")
    print(f"claims: {len(claims)}")
    print(f"raw_agent_responses: {len(raw)}")
    print(f"transition_labels: {len(transitions)}")
    print(f"verifier_outcomes: {len(outcomes)}")
    print(f"network_states: {len(network_states)}")
    print(f"policy_replay_events: {len(events)}")
    print(f"splits: {json.dumps(split_counts, sort_keys=True)}")
    print(f"transition_claims_with_four_roles: {complete_transition_claims}/{len(claim_ids)}")
    print(f"raw_claims_with_four_roles: {complete_raw_claims}/{len(claim_ids)}")
    print(f"transition_role_counts: {json.dumps(dict(sorted(role_counts.items())), sort_keys=True)}")
    print(f"state_counts: {json.dumps(dict(sorted(state_counts.items())), sort_keys=True)}")
    print(f"commitment_type_counts: {json.dumps(dict(sorted(type_counts.items())), sort_keys=True)}")
    print(
        "label_confidence_min_mean_max: "
        f"{min(confidence):.4f}/{statistics.mean(confidence):.4f}/{max(confidence):.4f}"
    )
    print(f"hidden_feature_forbidden_rows: {forbidden_rows}")
    print(f"hidden_flag_errors: {hidden_flag_errors}")
    print(f"stress_feature_coverage: {json.dumps(dict(sorted(stress_coverage.items())), sort_keys=True)}")
    print(f"event_regime_counts: {json.dumps(dict(sorted(regime_counts.items())), sort_keys=True)}")
    print(f"event_split_counts: {json.dumps(dict(sorted(split_event_counts.items())), sort_keys=True)}")
    if errors:
        print("\nerrors:")
        for error in errors[:50]:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
