#!/usr/bin/env python3
"""Validate the CommitmentTrace-LLM anonymous review artifact."""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


EXPECTED_COUNTS = {
    "claims": 576,
    "raw_agent_responses": 2304,
    "transition_labels": 2304,
    "verifier_outcomes": 576,
    "network_states": 2208,
    "policy_replay_events": 442368,
}

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


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_splits(data_dir: Path, errors: list[str]) -> None:
    splits_path = data_dir / "splits.json"
    require(splits_path.exists(), "missing splits.json", errors)
    if not splits_path.exists():
        return
    splits = json.loads(splits_path.read_text(encoding="utf-8"))
    required = {"train", "validation", "test_id", "test_ood_template", "test_ood_network"}
    require(required.issubset(splits.keys()), "splits.json missing required split keys", errors)
    seen: dict[str, str] = {}
    for split_name, items in splits.items():
        if not isinstance(items, list):
            errors.append(f"split {split_name} is not a list")
            continue
        for item in items:
            if item in seen:
                errors.append(f"claim {item} appears in both {seen[item]} and {split_name}")
            seen[item] = split_name


def validate_schema(data_dir: Path, errors: list[str]) -> None:
    schema_path = data_dir / "schema.json"
    require(schema_path.exists(), "missing schema.json", errors)
    if not schema_path.exists():
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    require(schema.get("schema_version") == "commitment_trace_llm_v1", "unexpected schema version", errors)
    records = schema.get("records", {})
    for name in ["claim", "network_state", "raw_agent_response", "transition_label", "verifier_outcome", "policy_replay_event"]:
        require(name in records, f"schema missing record definition: {name}", errors)


def validate_online_features(row: dict[str, Any], errors: list[str], line_no: int) -> None:
    features_raw = row.get("online_features_json")
    if not isinstance(features_raw, str):
        errors.append(f"policy_replay_events:{line_no}: online_features_json is missing or not a string")
        return
    try:
        features = json.loads(features_raw)
    except json.JSONDecodeError as exc:
        errors.append(f"policy_replay_events:{line_no}: invalid online_features_json: {exc}")
        return
    forbidden = sorted(FORBIDDEN_ONLINE_FEATURE_KEYS.intersection(features.keys()))
    if forbidden:
        errors.append(f"policy_replay_events:{line_no}: forbidden online feature keys: {forbidden}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="artifact root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data_dir = root / "data"
    errors: list[str] = []
    stats: dict[str, Any] = {}

    validate_schema(data_dir, errors)
    validate_splits(data_dir, errors)

    for logical_name, filename in JSONL_FILES.items():
        path = data_dir / filename
        require(path.exists(), f"missing {filename}", errors)
        if not path.exists():
            continue
        count = 0
        truth_counter: Counter[str] = Counter()
        parse_counter: Counter[str] = Counter()
        hidden_counter: Counter[str] = Counter()
        for count, row in enumerate(read_jsonl(path), 1):
            if logical_name == "claims":
                truth_counter[str(row.get("truth_label"))] += 1
            elif logical_name == "raw_agent_responses":
                parse_counter[str(row.get("parse_status"))] += 1
            elif logical_name == "policy_replay_events":
                hidden_counter[str(row.get("hidden_fields_excluded"))] += 1
                if row.get("hidden_fields_excluded") is not True:
                    errors.append(f"policy_replay_events:{count}: hidden_fields_excluded is not true")
                validate_online_features(row, errors, count)
        stats[logical_name] = count
        expected = EXPECTED_COUNTS[logical_name]
        require(count == expected, f"{logical_name}: expected {expected}, observed {count}", errors)
        if truth_counter:
            stats["claim_truth_labels"] = dict(truth_counter)
        if parse_counter:
            stats["raw_parse_status"] = dict(parse_counter)
            ok = parse_counter.get("ok", 0)
            stats["parse_success_rate"] = ok / max(1, sum(parse_counter.values()))
            require(ok == sum(parse_counter.values()), "not all raw responses parsed successfully", errors)
        if hidden_counter:
            stats["hidden_fields_excluded"] = dict(hidden_counter)
            require(set(hidden_counter.keys()) == {"True"}, "not all policy events exclude hidden fields", errors)

    verdict = "PASS" if not errors else "FAIL"
    print(f"verdict: {verdict}")
    for key in EXPECTED_COUNTS:
        print(f"{key}: {stats.get(key, 0)}")
    if "parse_success_rate" in stats:
        print(f"parse_success_rate: {stats['parse_success_rate']:.4f}")
    if errors:
        print("\nerrors:")
        for error in errors[:50]:
            print(f"- {error}")
        if len(errors) > 50:
            print(f"- ... {len(errors) - 50} more")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
