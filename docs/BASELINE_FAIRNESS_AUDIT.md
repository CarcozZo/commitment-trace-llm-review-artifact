# Baseline Fairness Audit

This audit describes the locked same-information replay used for the paper comparison. It records the comparison boundary, validation budget, online observation set, action set, and locked test tradeoff for each policy.

## Audit Contract

The comparison is a validation-locked replay audit rather than an adaptive
post-hoc sweep. Each policy is evaluated under the following contract:

- the same frozen claim, role-response, transition-label, verifier-outcome, and
  network-state records are used for every policy;
- hyperparameters are selected only on validation splits and then frozen before
  ID-test, OOD-template, and OOD-network replay;
- admission decisions can read online features, current queues, admissible
  action labels, and delayed feedback that has already become observable;
- online admission features exclude latent truth, future verifier outcomes,
  future downstream actions, realized FCE, and hindsight rollback cost;
- packet, verifier, actionability, and replay-budget accounting are computed
  from the same event table for all policies;
- summary metrics are computed after replay from the same hidden evaluation
  fields.

This contract makes the baselines comparable even when their action spaces are
different. Each policy uses its admissible interface, and all policies share the
same hidden-field exclusion rule. The fairness requirement is matched online
information at each policy interface, with policy-specific scoring rules left
intact.

## Verdict

- Same frozen trace records: yes.
- Validation-only configuration selection: yes.
- Hidden fields excluded from online features: yes.
- Forbidden online feature rows: `0`.
- Hidden flag errors: `0`.
- Dominance checks: `1/672` baseline rows core-dominate selected C-CPB+Prog. rows.

## Policy Interfaces

| Policy | Online objective | Online inputs | Labels | Validation configs | Selected configs | Locked test tradeoff |
|---|---|---|---:|---:|---:|---|
| Fastest broadcast | priority and packet pressure | priority, fanout, packet pressure | A/I | 24 | 4 | FCE/msg 0.607327; prog/msg 0.270678; debt 217.01113; D/R 0.0/0.0 |
| Semantic value | semantic utility minus estimated risk | utility, false-risk estimate, fanout | A/I/D | 24 | 3 | FCE/msg 0.867448; prog/msg 0.335545; debt 548.517115; D/R 0.049517/0.0 |
| State-aware AoII | deadline-weighted incorrect-state age | deadline, receiver state, false-risk estimate | A/V/D | 24 | 2 | FCE/msg 0.423037; prog/msg 0.27012; debt 303.193556; D/R 0.538345/0.0 |
| Action admission | receiver action risk gate | receiver state, action risk, utility | A/I/V/R | 24 | 3 | FCE/msg 0.42849; prog/msg 0.251386; debt 43.706691; D/R 0.100644/0.114936 |
| Pressure backpressure | debt/FCE backpressure | debt queue, FCE estimate, utility | A/D | 24 | 4 | FCE/msg 0.311238; prog/msg 0.176739; debt 18.403715; D/R 0.474336/0.0 |
| Static CPB | fixed commitment-pressure prices | receiver state, fixed prices, false-risk estimate | A/V/R | 24 | 4 | FCE/msg 0.293083; prog/msg 0.163072; debt 34.773152; D/R 0.135115/0.402929 |
| C-CPB | commitment authorization control | estimator, debt queue, verifier queue, feedback delay, receiver state | A/I/V/D/R | 24 | 4 | FCE/msg 0.43328; prog/msg 0.217093; debt 21.90804; D/R 0.22026/0.086353 |
| C-CPB+Prog. | progress-queued commitment authorization control | estimator, progress-deficit queue, debt queue, verifier queue, feedback delay, receiver state | A/I/V/D/R | 24 | 4 | FCE/msg 0.390827; prog/msg 0.222805; debt 21.145766; D/R 0.181159/0.090882 |

## Interpretation Boundary

The strongest baselines are meaningful operating points. Pressure backpressure lowers debt by deferring more events, and static CPB can lower realized FCE with a higher rejection ratio. C-CPB+Prog. is therefore evaluated as a receiver-state authorization controller that trades progress, false-commitment exposure, verifier load, and commitment debt under the same online observation boundary.

The main difference between Pressure BP and C-CPB+Prog. is the control surface: Pressure BP reacts to debt/FCE pressure with actionable-or-defer decisions, while C-CPB+Prog. can authorize informational-only, verify-first, defer, reject, or actionable receiver states and updates its estimates only after delayed feedback becomes observable.

## What Makes CLPD a Separate Algorithmic Interface

CLPD receives the same candidate event stream and solves a different online
admission interface:
for each message-receiver pair, it first evaluates feasible labels on the
authorization lattice and then selects the minimum sufficient label under
progress, commitment-debt, verifier-backlog, and exposure prices. This separates
three decisions that are collapsed in common baselines:

- packet admission: whether any delivery occurs in the current slot;
- receiver authorization: whether delivery may authorize information,
  verify-first handling, action preparation, propagation, or execution;
- delayed service update: how verifier and downstream feedback update queues
  after the original admission decision.

The audit therefore reports both conventional policy tradeoffs and whether a
policy can move along the receiver-state authorization boundary. The paper's
main comparison uses the validation-selected progress-queued C-CPB row because
it is the strongest non-CLPD operating point that exposes the same five-label
actionability interface while lacking CLPD's lattice minimum-sufficiency rule
and primal-dual price coupling.
