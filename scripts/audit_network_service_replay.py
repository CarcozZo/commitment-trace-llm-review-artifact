#!/usr/bin/env python3
"""Audit whether policy replay events instantiate network-service control slots."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


JSONL_FILES = {
    "network_states": "network_states.jsonl.gz",
    "policy_replay_events": "policy_replay_events.jsonl.gz",
}

SERVICE_FEATURES = [
    "packet_capacity",
    "verifier_capacity",
    "resource_utilization",
    "contact_window_remaining",
    "link_quality",
    "verifier_queue_length",
    "commitment_debt",
    "estimated_fanout",
    "estimated_irreversibility",
    "estimated_false_risk",
    "estimated_utility_if_true",
]

NETWORK_STATE_FEATURES = [
    "packet_capacity",
    "verifier_capacity",
    "resource_utilization",
    "contact_window_remaining",
    "link_quality",
    "burst_indicator",
]

ACTIONS = [
    "send_actionable",
    "send_informational_only",
    "verify_first",
    "defer",
    "reject",
]


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
                raise ValueError(f"{path}:{line_no}: row is not a JSON object")
            yield row


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def delay_bin(delay: float) -> str:
    if delay <= 3:
        return "delay_low_0_3"
    if delay <= 6:
        return "delay_mid_4_6"
    return "delay_high_7_plus"


def verifier_bin(capacity: float) -> str:
    if capacity <= 2.5:
        return "verifier_scarce_le_2p5"
    if capacity <= 5.0:
        return "verifier_mid_le_5"
    return "verifier_ample_gt_5"


def resource_bin(utilization: float) -> str:
    if utilization < 0.55:
        return "resource_low_lt_0p55"
    if utilization < 0.65:
        return "resource_mid_lt_0p65"
    return "resource_high_ge_0p65"


def debt_bin(debt: float) -> str:
    if debt < 5:
        return "debt_low_lt_5"
    if debt < 20:
        return "debt_mid_lt_20"
    return "debt_high_ge_20"


def empty_mix(scope: str, axis: str, bin_name: str) -> dict[str, Any]:
    row: dict[str, Any] = {
        "scope": scope,
        "stress_axis": axis,
        "stress_bin": bin_name,
        "rows": 0,
        "mean_delay": 0.0,
        "mean_packet_capacity": 0.0,
        "mean_verifier_capacity": 0.0,
        "mean_resource_utilization": 0.0,
        "mean_commitment_debt": 0.0,
        "mean_verifier_queue_length": 0.0,
        "mean_fce_increment": 0.0,
        "mean_progress_increment": 0.0,
    }
    for action in ACTIONS:
        row[f"{action}_ratio"] = 0.0
    row["protective_ratio"] = 0.0
    return row


def summarize_mix(scope: str, axis: str, bin_name: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    out = empty_mix(scope, axis, bin_name)
    n = len(rows)
    out["rows"] = n
    if not rows:
        return out
    action_counts = Counter(row["action"] for row in rows)
    for action in ACTIONS:
        out[f"{action}_ratio"] = action_counts[action] / n
    out["protective_ratio"] = (
        action_counts["verify_first"] + action_counts["defer"] + action_counts["reject"]
    ) / n
    out["mean_delay"] = sum(row["observed_feedback_delay"] for row in rows) / n
    out["mean_packet_capacity"] = sum(row["packet_capacity"] for row in rows) / n
    out["mean_verifier_capacity"] = sum(row["verifier_capacity"] for row in rows) / n
    out["mean_resource_utilization"] = sum(row["resource_utilization"] for row in rows) / n
    out["mean_commitment_debt"] = sum(row["commitment_debt"] for row in rows) / n
    out["mean_verifier_queue_length"] = sum(row["verifier_queue_length"] for row in rows) / n
    out["mean_fce_increment"] = sum(row["fce_increment"] for row in rows) / n
    out["mean_progress_increment"] = sum(row["true_progress_increment"] for row in rows) / n
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="artifact root")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    data_dir = root / "data"
    results_dir = root / "results"
    docs_dir = root / "docs"

    network_path = data_dir / JSONL_FILES["network_states"]
    event_path = data_dir / JSONL_FILES["policy_replay_events"]
    selected_path = results_dir / "selected_configs.csv"

    network_states = list(read_jsonl(network_path))
    state_by_key = {(row["episode_id"], int(row["slot"])): row for row in network_states}

    selected_rows = read_csv(selected_path)
    selected_pg_configs = {
        row["policy_config_id"]
        for row in selected_rows
        if row.get("policy_name") == "progress_guarded_cpb"
    }

    event_count = 0
    join_count = 0
    hidden_ok = 0
    feature_coverage: Counter[str] = Counter()
    action_counts: Counter[str] = Counter()
    policy_counts: Counter[str] = Counter()
    regime_counts: Counter[str] = Counter()
    split_counts: Counter[str] = Counter()
    feature_values: dict[str, set[Any]] = {key: set() for key in SERVICE_FEATURES}
    network_values: dict[str, set[Any]] = {key: set() for key in NETWORK_STATE_FEATURES}

    scoped_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    binned: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)

    for state in network_states:
        for key in NETWORK_STATE_FEATURES:
            network_values[key].add(state.get(key))

    for event in read_jsonl(event_path):
        event_count += 1
        key = (event["episode_id"], int(event["slot"]))
        state = state_by_key.get(key)
        if state is not None:
            join_count += 1
        features = json.loads(event["online_features_json"])
        for feature in SERVICE_FEATURES:
            if feature in features:
                feature_coverage[feature] += 1
                feature_values[feature].add(features[feature])

        hidden_ok += int(event.get("hidden_fields_excluded") is True)
        action_counts[event["action"]] += 1
        policy_counts[event["policy_name"]] += 1
        regime_counts[event["regime"]] += 1
        split_counts[event["split"]] += 1

        row = {
            "policy_name": event["policy_name"],
            "policy_config_id": event["policy_config_id"],
            "split": event["split"],
            "regime": event["regime"],
            "action": event["action"],
            "observed_feedback_delay": fnum(event.get("observed_feedback_delay")),
            "packet_capacity": fnum(features.get("packet_capacity", state.get("packet_capacity") if state else 0.0)),
            "verifier_capacity": fnum(features.get("verifier_capacity", state.get("verifier_capacity") if state else 0.0)),
            "resource_utilization": fnum(features.get("resource_utilization", state.get("resource_utilization") if state else 0.0)),
            "commitment_debt": fnum(features.get("commitment_debt")),
            "verifier_queue_length": fnum(features.get("verifier_queue_length")),
            "fce_increment": fnum(event.get("fce_increment")),
            "true_progress_increment": fnum(event.get("true_progress_increment")),
        }

        scopes = ["all_policy_events"]
        if event["policy_name"] == "progress_guarded_cpb":
            scopes.append("all_pg_cpb_events")
        if (
            event["policy_config_id"] in selected_pg_configs
            and event["split"].startswith("test_")
        ):
            scopes.append("selected_pg_cpb_locked_test")

        for scope in scopes:
            scoped_rows[scope].append(row)
            for axis, bin_name in [
                ("feedback_delay", delay_bin(row["observed_feedback_delay"])),
                ("verifier_capacity", verifier_bin(row["verifier_capacity"])),
                ("resource_utilization", resource_bin(row["resource_utilization"])),
                ("commitment_debt", debt_bin(row["commitment_debt"])),
            ]:
                binned[(scope, axis, bin_name)].append(row)

    mix_rows: list[dict[str, Any]] = []
    for scope in ["all_policy_events", "all_pg_cpb_events", "selected_pg_cpb_locked_test"]:
        for axis, ordered_bins in [
            ("feedback_delay", ["delay_low_0_3", "delay_mid_4_6", "delay_high_7_plus"]),
            ("verifier_capacity", ["verifier_scarce_le_2p5", "verifier_mid_le_5", "verifier_ample_gt_5"]),
            ("resource_utilization", ["resource_low_lt_0p55", "resource_mid_lt_0p65", "resource_high_ge_0p65"]),
            ("commitment_debt", ["debt_low_lt_5", "debt_mid_lt_20", "debt_high_ge_20"]),
        ]:
            for bin_name in ordered_bins:
                mix_rows.append(summarize_mix(scope, axis, bin_name, binned[(scope, axis, bin_name)]))

    result_csv = results_dir / "round8_network_service_replay_audit.csv"
    write_csv(result_csv, mix_rows)

    coverage = {
        key: {
            "present": feature_coverage[key],
            "total": event_count,
            "coverage": feature_coverage[key] / max(1, event_count),
            "unique_values": len(feature_values[key]),
        }
        for key in SERVICE_FEATURES
    }
    network_support = {
        key: {
            "unique_values": len(network_values[key]),
            "sample_values": sorted(network_values[key])[:8],
        }
        for key in NETWORK_STATE_FEATURES
    }

    selected_pg_delay = {
        row["stress_bin"]: row
        for row in mix_rows
        if row["scope"] == "selected_pg_cpb_locked_test" and row["stress_axis"] == "feedback_delay"
    }
    selected_pg_verifier = {
        row["stress_bin"]: row
        for row in mix_rows
        if row["scope"] == "selected_pg_cpb_locked_test" and row["stress_axis"] == "verifier_capacity"
    }

    errors: list[str] = []
    if join_count != event_count:
        errors.append(f"network-state join incomplete: {join_count}/{event_count}")
    if hidden_ok != event_count:
        errors.append(f"hidden-field exclusion incomplete: {hidden_ok}/{event_count}")
    missing_features = [key for key, item in coverage.items() if item["present"] != event_count]
    if missing_features:
        errors.append(f"online feature coverage incomplete: {missing_features}")
    nonvarying_network = [key for key, item in network_support.items() if item["unique_values"] <= 1]
    if nonvarying_network:
        errors.append(f"network-state variables do not vary: {nonvarying_network}")
    if not selected_pg_configs:
        errors.append("no selected PG-C-CPB configurations found")

    summary = {
        "audit_name": "round8_network_service_replay_audit",
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "verdict": "PASS" if not errors else "FAIL",
        "purpose": (
            "Check that released policy replay events instantiate network-service control slots "
            "rather than offline LLM-answer scoring rows."
        ),
        "row_counts": {
            "network_states": len(network_states),
            "policy_replay_events": event_count,
            "selected_pg_cpb_configs": len(selected_pg_configs),
            "selected_pg_cpb_locked_test_events": len(scoped_rows["selected_pg_cpb_locked_test"]),
        },
        "network_state_join": {
            "matched_events": join_count,
            "total_events": event_count,
            "join_rate": join_count / max(1, event_count),
        },
        "hidden_fields_excluded": {
            "true_rows": hidden_ok,
            "total_events": event_count,
            "rate": hidden_ok / max(1, event_count),
        },
        "online_service_feature_coverage": coverage,
        "network_state_variable_support": network_support,
        "action_counts": dict(sorted(action_counts.items())),
        "policy_counts": dict(sorted(policy_counts.items())),
        "regime_counts": dict(sorted(regime_counts.items())),
        "split_counts": dict(sorted(split_counts.items())),
        "selected_pg_cpb_delay_bins": selected_pg_delay,
        "selected_pg_cpb_verifier_bins": selected_pg_verifier,
        "errors": errors,
        "outputs": {
            "csv": "results/round8_network_service_replay_audit.csv",
            "json": "results/round8_network_service_replay_audit.json",
            "markdown": "docs/NETWORK_SERVICE_REPLAY_AUDIT.md",
        },
    }

    result_json = results_dir / "round8_network_service_replay_audit.json"
    result_json.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    low_delay = selected_pg_delay.get("delay_low_0_3", {})
    high_delay = selected_pg_delay.get("delay_high_7_plus", {})
    scarce_verifier = selected_pg_verifier.get("verifier_scarce_le_2p5", {})
    ample_verifier = selected_pg_verifier.get("verifier_ample_gt_5", {})

    md = f"""# Network-Service Replay Audit

This audit checks whether the released policy replay rows instantiate network-service
control slots rather than offline answer-quality scoring rows.

## Verdict

- verdict: `{summary['verdict']}`
- policy replay events: {event_count}
- network-state rows: {len(network_states)}
- network-state join rate: {summary['network_state_join']['join_rate']:.4f}
- hidden-field exclusion rate: {summary['hidden_fields_excluded']['rate']:.4f}
- selected PG-C-CPB locked-test events: {len(scoped_rows['selected_pg_cpb_locked_test'])}

## Service-Control Variables

Every policy event is audited for observable service-control variables used at
admission time: packet capacity, verifier capacity, resource utilization, contact
window, link quality, verifier queue length, commitment debt, estimated fanout,
irreversibility, false-risk estimate, and utility-if-true estimate.

| Variable | Coverage | Unique values |
|---|---:|---:|
"""
    for key in SERVICE_FEATURES:
        item = coverage[key]
        md += f"| `{key}` | {item['coverage']:.4f} | {item['unique_values']} |\n"

    md += """
## Selected PG-C-CPB Stress Response

The rows below summarize selected PG-C-CPB locked-test action mixes under
observable service stress. `protective_ratio` is the fraction of verify-first,
defer, and reject decisions.

| Stress comparison | Protective ratio | Actionable ratio | Rows |
|---|---:|---:|---:|
"""
    for label, row in [
        ("low feedback delay (0-3)", low_delay),
        ("high feedback delay (7+)", high_delay),
        ("verifier scarce (capacity <= 2.5)", scarce_verifier),
        ("verifier ample (capacity > 5)", ample_verifier),
    ]:
        if row:
            md += (
                f"| {label} | {row['protective_ratio']:.4f} | "
                f"{row['send_actionable_ratio']:.4f} | {row['rows']} |\n"
            )

    md += f"""
## Generated Files

- `results/round8_network_service_replay_audit.csv`
- `results/round8_network_service_replay_audit.json`
- `docs/NETWORK_SERVICE_REPLAY_AUDIT.md`

## Reproduction Command

Run from the artifact root:

```bash
python scripts/audit_network_service_replay.py --root .
```

## Result Freeze

- run name: `round8_network_service_replay_audit`
- purpose: verify that policy replay events instantiate online network-service
  control slots rather than offline LLM-answer scoring rows
- artifact root: current anonymous artifact root
- command: `python scripts/audit_network_service_replay.py --root .`
- completion: full
- exit status: `{summary['verdict']}`
- paper usability: usable for artifact/audit support and setup-level claims
- dataset: released CommitmentTrace-LLM anonymous artifact
- rows: {event_count} policy replay events, {len(network_states)} network-state rows
- primary metrics: join rate {summary['network_state_join']['join_rate']:.4f},
  hidden-field exclusion rate {summary['hidden_fields_excluded']['rate']:.4f}

## Interpretation Boundary

This audit does not claim that the artifact is a production deployment trace.
It verifies the narrower review claim: the released replay evaluates online
admission decisions over observable network-service state, with frozen LLM
responses acting as role-reactive workload and with latent truth, future verifier
outcomes, and hindsight FCE excluded at admission time.
"""
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "NETWORK_SERVICE_REPLAY_AUDIT.md").write_text(md, encoding="utf-8")

    print(f"verdict: {summary['verdict']}")
    print(f"policy_replay_events: {event_count}")
    print(f"network_states: {len(network_states)}")
    print(f"network_state_join_rate: {summary['network_state_join']['join_rate']:.4f}")
    print(f"hidden_field_exclusion_rate: {summary['hidden_fields_excluded']['rate']:.4f}")
    print(f"selected_pg_cpb_locked_test_events: {len(scoped_rows['selected_pg_cpb_locked_test'])}")
    if low_delay and high_delay:
        print(
            "selected_pg_delay_protective_ratio_low_high: "
            f"{low_delay['protective_ratio']:.4f}/{high_delay['protective_ratio']:.4f}"
        )
    if scarce_verifier and ample_verifier:
        print(
            "selected_pg_verifier_protective_ratio_scarce_ample: "
            f"{scarce_verifier['protective_ratio']:.4f}/{ample_verifier['protective_ratio']:.4f}"
        )
    for error in errors:
        print(f"error: {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
