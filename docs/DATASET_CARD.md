# CommitmentTrace-LLM Dataset Card

## Dataset Name

CommitmentTrace-LLM

## Status

Anonymous review artifact for double-blind submission.

## Intended Use

CommitmentTrace-LLM is designed for evaluating online communication-admission
and actionability-control policies in role-reactive LLM-agent services.  It is
especially intended for studying when message delivery authorizes receiver-side
commitments such as planning, action preparation, resource reservation,
verification enqueueing, propagation, or execution.

## Review-Relevant Design Points

The dataset is built to support three mechanism checks:

- **same semantic content, different network pressure:** the same frozen role
  responses are replayed under feasible, high-fanout, high-delay, and
  verifier-scarce regimes;
- **same online observation, hidden evaluation labels:** policy events expose
  only online features, current queues, admissible labels, and feedback that has
  already arrived; hidden truth and realized FCE are evaluation-only fields;
- **receiver-state authorization rather than send/drop only:** each event
  records admissible actionability labels and the receiver state induced by the
  selected label, allowing policies to differ in the commitment they authorize
  even when semantic content is unchanged.

## Scope

CommitmentTrace-LLM targets mechanism-level evaluation for receiver-state
authorization in distributed LLM-agent services. The released records support
audits of admission control, actionability labels, delayed verifier feedback,
commitment debt, and same-information baseline replay under controlled
wireless/edge service regimes.

## Data Generation

The source responses are frozen controlled role-conditioned LLM-agent responses.
Each claim is presented to four role prompts:

- planner;
- executor;
- verifier;
- network controller.

The released trace uses six wireless and edge collaboration templates:

- UAV rerouting;
- edge reservation;
- LEO contact handover;
- vehicular edge handoff;
- multi-edge model cache;
- distributed verifier safety.

The source responses are replayed across four network regimes:

- feasible;
- high-fanout feasible;
- high-delay network;
- verifier-scarce network.

This repeated-regime design intentionally keeps semantic content fixed while
changing network pressure and verifier scarcity, enabling controlled
same-information comparison of how policies authorize receiver-side
commitments.

The six templates are chosen to cover distributed LLM-agent services where
communication has immediate service consequences: mobility planning, edge
capacity reservation, satellite/LEO contact preparation, vehicular handoff,
distributed model-cache updates, and verifier-service scheduling. In all cases,
the benchmark records both the message-level evidence and the receiver-side
commitment that delivery is allowed to trigger.

## Construction Pipeline

The released records follow a fixed construction pipeline:

1. Generate controlled wireless/edge source claims with hidden ground-truth
   labels.
2. Instantiate each source claim into one of the six service templates, which
   defines the communication context, receiver role set, verifier-delay handle,
   and network-service variables used during replay.
3. Query role-conditioned LLM-agent prompts for planner, executor, verifier,
   and network-controller responses.
4. Parse each response into a structured role-response record.
5. Convert role responses into receiver action-state and commitment labels with
   a deterministic parser.
6. Join each claim--role transition with delayed verifier outcomes and
   per-slot network-state traces.
7. Replay online policies using only observable features and delayed feedback
   that has already become available.
8. Accumulate offline realized FCE, true progress, resource waste, and terminal
   debt after replay.

## Record Types

| File | Description |
|---|---|
| `claims.jsonl.gz` | Claim records, context, estimated online features, hidden truth label for evaluation. |
| `raw_agent_responses.jsonl.gz` | Frozen role-conditioned LLM responses and parsed JSON. |
| `transition_labels.jsonl.gz` | Receiver action-state and commitment labels derived from role responses. |
| `verifier_outcomes.jsonl.gz` | Delayed verifier outcomes and verification delay. |
| `network_states.jsonl.gz` | Per-slot network and verifier-service state. |
| `policy_replay_events.jsonl.gz` | Online policy decisions and resulting replay increments. |
| `schema.json` | Machine-readable schema and quality gates. |
| `splits.json` | Train, validation, ID test, OOD-template test, and OOD-network test splits. |

## Transition Label Schema

Each transition label connects one claim and one receiver role to an intended
receiver action state.  The main fields are:

- `intended_action_state`: one of the recorded receiver states, such as
  `TENTATIVE_PLAN`, `PREPARED_ACTION`, `RESOURCE_RESERVED`, or
  `VERIFICATION_QUEUED`;
- `commitment_type`: commitment family, such as plan, action,
  resource-reservation, or verification-queue workload;
- boolean state indicators including `plan_created`, `action_prepared`,
  `resource_reserved`, `verification_queued`, `tool_invoked`, and `propagated`;
- `commitment_pressure`, `false_commitment_exposure`, and
  `true_progress_if_delivered`;
- `label_confidence`, recorded as the deterministic parser confidence score.

The transition labels are deterministic parser outputs that make
commitment-state replay auditable and reproducible.

## Hidden Labels and Online Observation Boundary

Truth labels and post-hoc verifier outcomes are hidden from online policy
decisions.  They are used only for offline evaluation after replay.  Policy
events include `hidden_fields_excluded=true`, and `online_features_json` excludes
latent truth, future verifier outcomes, future downstream actions, and hindsight
false commitment exposure.

## Quality Checks

The released validation gate checks:

- parse success rate;
- row counts;
- split consistency;
- nonzero false-transition roles;
- hidden-field exclusion in policy events;
- absence of schema errors and warnings.

The current release passes the validation gate; `parse_success_rate` is recorded
as 1.0000 in the validation summary.

The additional dataset audit script checks traceability and network-control
feature coverage:

```bash
python scripts/audit_commitmenttrace_dataset.py --root .
```

The current audit reports:

- `transition_claims_with_four_roles: 576/576`;
- `raw_claims_with_four_roles: 576/576`;
- `hidden_feature_forbidden_rows: 0`;
- `hidden_flag_errors: 0`;
- full coverage of online network-control features in all 442,368 replay
  events: verifier capacity, packet capacity, estimated fanout, resource
  utilization, verifier queue length, and current commitment debt.

See `docs/LABEL_AUDIT.md` for the label audit protocol and the distinction
between deterministic parser checks and optional manual review.

The release also includes representative trace examples in `docs/EXAMPLES.md`,
an examples-to-metrics audit in `docs/TRACE_TO_METRICS.md`, and a
reproducibility checklist in `docs/REPRODUCIBILITY.md`.

Baseline fairness is audited separately in `docs/BASELINE_FAIRNESS_AUDIT.md`.
That audit records validation-grid size, selected configurations, online
features, action sets, and locked test tradeoffs for every compared policy.

Robustness checks in `docs/ROBUSTNESS_AUDIT.md` report split/regime stability,
label-confidence threshold sensitivity, and subset dominance rates over locked
test events.

Verifier-delay and verifier-budget checks in
`docs/VERIFIER_DELAY_BUDGET_AUDIT.md` report how observable feedback delay and
verifier capacity affect progress, FCE/progress, commitment debt, and receiver
authorization states.

## Release Profile

- Scale: 576 claim records and 2,304 role-agent responses.
- Source responses: one frozen role-conditioned model backend.
- Regime design: fixed semantic responses replayed across four network-pressure
  regimes.
- Labels: deterministic schema/parser outputs with parser confidence scores.
- Evaluation target: controlled mechanism evidence for commitment-aware online
  replay, delayed verification, and actionability control.

## Supported Use

Use this dataset to support claims about commitment-aware online replay,
same-information baseline comparison, delayed verification, and actionability
control under the recorded scale, frozen trace source, validation selection
protocol, and online-observation boundary.
