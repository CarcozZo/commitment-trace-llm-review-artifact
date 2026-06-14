# CommitmentTrace-LLM Label and Traceability Audit

This document records the label-audit boundary for the anonymous review
artifact.  The current release uses deterministic parser labels rather than a
large human annotation campaign.  The audit therefore verifies schema
consistency, traceability, online-observation isolation, and stratified manual
review readiness.  It does not claim human inter-annotator agreement.

## Audit Command

Run from the artifact root:

```bash
python scripts/audit_commitmenttrace_dataset.py --root .
```

Current output:

```text
verdict: PASS
claims: 576
raw_agent_responses: 2304
transition_labels: 2304
verifier_outcomes: 576
network_states: 2208
policy_replay_events: 442368
splits: {"test_id": 54, "test_ood_network": 144, "test_ood_template": 216, "train": 126, "validation": 36}
transition_claims_with_four_roles: 576/576
raw_claims_with_four_roles: 576/576
transition_role_counts: {"executor": 576, "network_controller": 576, "planner": 576, "verifier": 576}
state_counts: {"PREPARED_ACTION": 524, "RESOURCE_RESERVED": 320, "TENTATIVE_PLAN": 600, "VERIFICATION_QUEUED": 860}
commitment_type_counts: {"action": 488, "plan": 620, "resource_reservation": 324, "verification_queue": 872}
label_confidence_min_mean_max: 0.3468/0.6658/0.8924
hidden_feature_forbidden_rows: 0
hidden_flag_errors: 0
stress_feature_coverage: {"commitment_debt": 442368, "estimated_fanout": 442368, "packet_capacity": 442368, "resource_utilization": 442368, "verifier_capacity": 442368, "verifier_queue_length": 442368}
event_regime_counts: {"feasible": 96768, "high_fanout_feasible": 96768, "network_delay_high": 96768, "verifier_scarce": 96768}
event_split_counts: {"test_id": 36288, "test_ood_network": 96768, "test_ood_template": 145152, "train": 84672, "validation": 24192}
```

## What Is Checked

The audit checks:

- every claim has one raw response for each of the four receiver roles;
- every claim has one transition label for each of the four receiver roles;
- transition labels, verifier outcomes, and replay events reference known
  claims;
- train, validation, ID-test, OOD-template, and OOD-network splits are disjoint
  and cover the released claims;
- all replay events set `hidden_fields_excluded=true`;
- online features do not expose hidden truth labels, future verifier outcomes,
  future downstream actions, realized FCE, or true progress;
- all replay events include the online network-control features needed for
  stress analysis: verifier capacity, packet capacity, fanout estimate,
  resource utilization, verifier queue length, and commitment debt.

## Stratified Manual Review Protocol

For optional manual review, sample transition labels by the Cartesian product
of:

- role: planner, executor, verifier, network controller;
- receiver state: tentative plan, prepared action, resource reserved,
  verification queued;
- split: validation, ID test, OOD-template test, OOD-network test;
- network regime: feasible, high-fanout feasible, high-delay network,
  verifier-scarce network.

For each sampled item, compare the raw role response with:

- intended action state;
- commitment type;
- commitment pressure;
- action-preparation / resource-reservation / verification-queued flags;
- whether the label would be visible to an online policy at admission time.

Disagreements should be recorded as one of:

- parser missed a commitment cue;
- parser over-assigned a commitment state;
- role response was ambiguous;
- commitment pressure was directionally correct but magnitude questionable;
- online/offline field boundary was unclear.

The current anonymous release includes the protocol and automatic traceability
checks.  It does not report a human agreement rate.
