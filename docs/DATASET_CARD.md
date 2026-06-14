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

## Non-Goals

This dataset is not:

- a live deployment trace;
- a broad general-purpose LLM benchmark;
- a benchmark for raw factuality or hallucination detection alone;
- a benchmark for token-efficient message compression alone;
- evidence that any policy dominates every baseline configuration under all
  possible regimes.

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
changing network pressure and verifier scarcity.  It enables controlled
same-information comparison, but it is not a substitute for live deployment
evidence.

## Construction Pipeline

The released records follow a fixed construction pipeline:

1. Generate controlled wireless/edge claims with hidden ground-truth labels.
2. Query role-conditioned LLM-agent prompts for planner, executor, verifier,
   and network-controller responses.
3. Parse each response into a structured role-response record.
4. Convert role responses into receiver action-state and commitment labels with
   a deterministic parser.
5. Generate delayed verifier outcomes and network-state traces.
6. Replay online policies using only observable features and delayed feedback
   that has already become available.
7. Accumulate offline realized FCE, true progress, resource waste, and terminal
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
- `label_confidence`, used as a parser confidence score rather than a human
  inter-annotator agreement statistic.

The transition labels are deterministic parser outputs.  They are intended to
make commitment-state replay auditable, not to replace a large human annotation
campaign.

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

## Known Limitations

- The release scale is modest: 576 claim records and 2,304 role-agent responses.
- The source responses are generated by one frozen model backend.
- The network regimes reuse the same semantic responses for controlled replay.
- The labels are deterministic schema/parser outputs rather than a large human
  annotation campaign.
- The benchmark is strongest for controlled mechanism evidence, not for claiming
  field deployment performance.

## Recommended Claims

Use this dataset to support claims about commitment-aware online replay,
same-information baseline comparison, delayed verification, and actionability
control under the recorded scale.  The strongest supported claims are those
that compare policies under the same frozen trace source, validation selection
protocol, and online-observation boundary.

Avoid claiming that the dataset is large-scale, live, or representative of all
LLM-agent deployments.
