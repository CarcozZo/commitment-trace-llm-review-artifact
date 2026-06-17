# CommitmentTrace-LLM Anonymous Review Artifact

This repository contains an anonymized review artifact for CommitmentTrace-LLM,
a controlled trace-replay benchmark for commitment-aware communication in
role-reactive LLM-agent services.

## Reviewer Quick Map

This artifact is organized to let reviewers audit three claims from the paper:

1. **Dataset and service boundary.** The released records connect wireless/edge
   claims, frozen role-conditioned LLM-agent responses, receiver commitment
   labels, delayed verifier outcomes, network states, and policy replay events.
   The key control object is the receiver action state authorized by message
   delivery, not only whether a packet is delivered.
2. **Same-information baseline comparison.** All compared policies are replayed
   on the same locked events, selected on validation only, and evaluated on
   hidden fields only after admission decisions have been made.
3. **Figure and metric regeneration.** The released scripts validate the schema,
   check hidden-field exclusion, audit network-service replay, and summarize the
   CLPD locked replay and baseline tradeoffs used by the manuscript.

The artifact is intended for double-blind peer review.  It avoids author names,
institution names, grant identifiers, local absolute paths, and non-anonymous
repository identifiers.  If the paper is accepted, the anonymous placeholders
should be replaced by a public archival record and a persistent DOI.

## What This Artifact Contains

CommitmentTrace-LLM links six types of records:

- candidate claims in wireless and edge collaboration scenarios;
- frozen role-conditioned LLM responses;
- receiver action-state and commitment labels;
- delayed verifier outcomes;
- network-state traces;
- online policy replay events.

The trace construction is explicit. Balanced source claims are instantiated into
six wireless/edge service templates, queried once against four role prompts
(planner, executor, verifier, and network controller), parsed into receiver
action-state labels, joined with delayed verifier outcomes and network-state
tuples, and then expanded into locked policy replay events. Thus every figure
point can be traced from a source claim to a scenario tuple, a role response, an
authorized receiver state, and a policy decision under the recorded online
state.

The released scale is:

| Record type | Count |
|---|---:|
| Trace claim records | 576 |
| Raw role-agent responses | 2,304 |
| Transition labels | 2,304 |
| Verifier outcomes | 576 |
| Network-state rows | 2,208 |
| Policy replay events | 442,368 |

The benchmark is designed for controlled mechanism evidence. Frozen role
responses are replayed across feasible, high-fanout, high-delay, and
verifier-scarce regimes while preserving the same semantic content. This makes
it possible to isolate whether an admission controller changes the receiver
state authorized by delivery under the same online observation set.

## Directory Layout

```text
data/
  claims.jsonl.gz
  raw_agent_responses.jsonl.gz
  transition_labels.jsonl.gz
  verifier_outcomes.jsonl.gz
  network_states.jsonl.gz
  policy_replay_events.jsonl.gz
  schema.json
  splits.json
  validation_report.json
  validation_report.md
  audit_report.md

results/
  clpd_comparison_summary.csv
  clpd_anchor_gate_summary.csv
  clpd_test_metrics.csv
  clpd_validation_config_metrics.csv
  clpd_selected_configs.csv
  clpd_pareto_points.csv
  clpd_aggregated_metrics.csv
  clpd_policy_configs.csv
  fig3_oldstyle_clpd_operating_source_v1.csv
  fig4_oldstyle_clpd_displacement_source_v1.csv
  fig5_oldstyle_clpd_phase_source_v1.csv
  fig6_oldstyle_clpd_role_action_source_v1.csv
  figure_package_v1_oldstyle_clpd_qa.json
  selected_configs.csv
  validation_config_metrics.csv
  pareto_points.csv
  test_metrics.csv
  dominance_checks.csv
  practical_regime_summary.csv
  aggregated_metrics.csv
  summary.json
  baseline_fairness_check.md
  round2_baseline_fairness_audit.csv
  round2_baseline_fairness_audit.json
  round3_robustness_audit.csv
  round3_robustness_audit.json
  round3_trace_to_metrics.csv
  round3_trace_to_metrics.json
  round4_verifier_delay_budget_audit.csv
  round4_verifier_delay_budget_audit.json
  round5_progress_guard_policy_summary.csv
  round5_progress_guard_operating_points.csv
  round5_progress_guard_stress_bins.csv
  round5_progress_guard_figure_qa.json
  round5_online_ablation_curve_source.csv
  round5_online_ablation_tradeoff_source.csv
  round5_role_actionability_source.csv
  round5_role_summary_source.csv
  round6_fig3_pg_operating_points_v22.csv
  round6_fig3_pg_action_mix_v22.csv
  round6_fig4_pg_mechanism_displacement_v22.csv
  round6_fig5_pg_feedback_phase_trace_v22.csv
  round7_fig3_oldstyle_pg_operating_source_v23.csv
  round7_fig4_oldstyle_pg_mechanism_source_v23.csv
  round7_fig5_oldstyle_pg_phase_source_v23.csv
  round7_fig6_oldstyle_pg_role_action_source_v23.csv
  round8_network_service_replay_audit.csv
  round8_network_service_replay_audit.json

scripts/
  validate_commitmenttrace.py
  audit_commitmenttrace_dataset.py
  audit_network_service_replay.py
  summarize_locked_results.py
  check_anonymity.py

docs/
  DATASET_CARD.md
  LABEL_AUDIT.md
  BASELINE_PROTOCOL.md
  BASELINE_FAIRNESS_AUDIT.md
  EXAMPLES.md
  TRACE_TO_METRICS.md
  CLPD_LOCKED_REPLAY.md
  ROBUSTNESS_AUDIT.md
  VERIFIER_DELAY_BUDGET_AUDIT.md
  PROGRESS_GUARD_AUDIT.md
  NETWORK_SERVICE_REPLAY_AUDIT.md
  REPRODUCIBILITY.md
  ANONYMIZATION.md
  DATA_AVAILABILITY.md
  FAIR_CHECKLIST.md
  RELEASE_MANIFEST.tsv
  SHA256SUMS.txt
```

## Quickstart

Use Python 3.10 or later.  The validation and summary scripts use only the
Python standard library.

```bash
python scripts/validate_commitmenttrace.py --root .
python scripts/audit_commitmenttrace_dataset.py --root .
python scripts/audit_network_service_replay.py --root .
python scripts/summarize_locked_results.py --root .
python scripts/check_anonymity.py --root .
```

See `docs/REPRODUCIBILITY.md` for the full artifact audit sequence, including
baseline-fairness checks and release-manifest refresh.

The quickstart covers the main review checks:

| Check | Script | What it verifies |
|---|---|---|
| Schema and row counts | `validate_commitmenttrace.py` | record counts, splits, parse success, hidden-field flags |
| Dataset traceability | `audit_commitmenttrace_dataset.py` | four-role coverage, transition labels, online feature exclusion |
| Network-service replay | `audit_network_service_replay.py` | packet/verifier/feedback/service variables join every replay event |
| Locked result summary | `summarize_locked_results.py` | validation-selected CLPD operating point and baseline tradeoffs |
| Anonymous release check | `check_anonymity.py` | absence of known author, institution, path, and credential patterns |

Expected validation summary:

```text
verdict: PASS
claims: 576
raw_agent_responses: 2304
transition_labels: 2304
verifier_outcomes: 576
network_states: 2208
policy_replay_events: 442368
hidden_fields_excluded: true
parse_success_rate: 1.0000
```

Expected dataset audit summary includes:

```text
verdict: PASS
transition_claims_with_four_roles: 576/576
raw_claims_with_four_roles: 576/576
hidden_feature_forbidden_rows: 0
hidden_flag_errors: 0
```

Expected network-service replay audit summary includes:

```text
verdict: PASS
policy_replay_events: 442368
network_states: 2208
network_state_join_rate: 1.0000
hidden_field_exclusion_rate: 1.0000
```

Expected CLPD locked replay summary includes:

```text
CLPD anchor clpd_cfg016: FCE/msg 0.330; progress/msg 0.232; debt 17.4; withheld 6.0%
CLPD vs selected PG-C-CPB: progress ratio 1.040; FCE ratio 0.845; debt ratio 0.822; withheld delta -21.2 pp
```

## Main Review Boundary

The artifact supports claims about validation-locked trace replay under the
recorded scale and splits. It is intended to test mechanism-level questions:
whether actionability labels, delayed verifier feedback, and queue prices change
the commitments that communication is allowed to induce.

The key experimental boundary is same-information online replay: policy
decisions use online features, queue states, delayed feedback that has already
become observable, and configured actionability labels. The online feature set
excludes latent truth, future verifier outcomes, future downstream actions, and
hindsight false commitment exposure at admission time.

Baseline fairness is documented in `docs/BASELINE_FAIRNESS_AUDIT.md`. In brief,
each policy receives the same frozen trace events, the same observable online
features available to its interface, the same validation-only selection rule,
and the same locked test replay. Strong baselines are treated as meaningful
operating points rather than strawmen; several reduce exposure or debt by
withholding more service, while CLPD targets a progress-preserving low-exposure
frontier by controlling the receiver-state authorization label.

## Citation Placeholder

For double-blind review:

```text
Anonymous Authors (2026). CommitmentTrace-LLM: An anonymized controlled
trace-replay benchmark for commitment-aware LLM-agent communication.
Anonymous review artifact.
```

For camera-ready release, replace this placeholder with a public repository
record and DOI.
