# Baseline Fairness Check

Status: `SAME_INFORMATION_REPLAY_CHECK`

- Policies: `['fastest_broadcast', 'semantic_value', 'state_aware_aoii', 'action_admission', 'pressure_backpressure', 'static_cpb', 'closed_loop_cpb', 'progress_guarded_cpb']`
- Regimes: `['feasible', 'high_fanout_feasible', 'network_delay_high', 'verifier_scarce']`
- All policies are replayed over the same frozen transition labels.
- Online features are serialized in `online_features_json`.
- Hidden ground-truth labels, future verifier results, future downstream actions, and hindsight FCE are excluded from online features.
- Fixed-threshold smoke runs and same-budget tuned Pareto runs share this hidden-label exclusion rule.
- Test splits are evaluated after policy configuration lock.
