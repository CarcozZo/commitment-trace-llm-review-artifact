# Baseline and Replay Protocol

## Goal

The replay protocol tests whether commitment-aware admission changes the
FCE/progress/debt operating region under the same frozen role-response trace and
the same online observation boundary.

## Policy Interfaces

The released replay compares eight online policies:

| Policy | Online objective | Online inputs | Labels | Tuned and locked choices |
|---|---|---|---|---|
| Fastest broadcast | Admit high-priority traffic under packet budget. | Priority, fanout, packet pressure. | A/I | Priority threshold, packet budget. |
| Semantic value | Maximize semantic value minus estimated risk. | Semantic score, false-risk estimate, fanout. | A/I/D | Value/risk weights, defer threshold. |
| State-aware AoII | Reduce deadline-weighted incorrect-state age. | Deadline, receiver state, risk estimate. | A/V/D | Age/risk weights, verify threshold. |
| Action admission | Gate high-risk receiver actions using state utility. | Receiver state, action risk, utility. | A/I/V/R | Action-risk and utility thresholds. |
| Pressure backpressure | Backpressure on estimated FCE and debt. | Debt queue, FCE estimate, utility. | A/D | Debt and exposure prices. |
| Static CPB | Use fixed commitment-pressure prices without delayed updates. | Receiver state, labels, fixed prices. | A/V/R | Fixed debt/FCE prices, thresholds. |
| C-CPB | Closed-loop commitment authorization control. | Estimator, commitment debt, verifier queue, delay, receiver state. | A/I/V/D/R | Utility/FCE/debt prices, verifier price, estimator update. |
| PG-C-CPB | Progress-guarded C-CPB. | Estimator, progress-deficit queue, commitment debt, verifier queue, delay, receiver state. | A/I/V/D/R | Progress service target, debt/FCE prices, verifier price, estimator update. |

A, I, V, D, and R denote actionable, informational-only, verify-first, defer,
and reject.

The ablation replay further evaluates PG-C-CPB variants with the same selected
configurations while removing the progress guard, delayed feedback, commitment
debt, actionability downgrade, or verify-first admission.  These ablations isolate mechanism
contributions under the same trace and online observation boundary.

## Fairness Rules

All policies use:

- the same frozen claim, response, label, verifier, and network-state records;
- the same train/validation/test split definitions;
- the same hidden-label exclusion rule;
- the same configuration budget of 24 configurations per policy;
- validation-only selection before ID/OOD testing.

The comparison is not based on choosing the best hindsight test row for any
policy.  Policy configurations are selected from validation Pareto behavior and
then locked before test evaluation.

## Hidden-Field Exclusion

At admission time, policies cannot access:

- latent truth labels;
- future verifier outcomes;
- future downstream actions;
- hindsight false commitment exposure;
- future replay increments.

These fields are only used after replay completion to compute evaluation
metrics.

## Selection Protocol

For each policy, validation Pareto rows are screened by:

- low false commitment exposure;
- high true progress;
- low terminal commitment debt;
- a balanced normalized score over FCE, progress, rejection, deferral, debt, and
  resource waste.

Duplicate selections are removed.  The selected configurations are then
evaluated on locked ID, OOD-template, and OOD-network splits.

## Core Dominance Check

A selected baseline row core-dominates a selected PG-C-CPB row only if it is:

- no worse in false commitment exposure;
- no worse in rejection ratio;
- no worse in deferral ratio;
- no worse in terminal commitment debt;
- no worse in resource waste;
- no lower in true progress;
- strictly better in at least one of these dimensions.

The released run contains 672 dominance checks comparing selected PG-C-CPB
configurations with selected baseline configurations within the same regime and
split.

## Interpreting the Results

The strongest baselines occupy meaningful parts of the tradeoff surface.  Some
baselines reduce FCE by deferring or rejecting more aggressively, and a
one pressure-backpressure configuration core-dominates a selected PG-C-CPB point
in a verifier-stressed locked slice.  The intended claim is therefore not
unconditional single-metric dominance.  The supported claim is that C-CPB
exposes a practical low-debt operating region with explicit actionability and
delayed-feedback controls, and that the progress-guarded version improves
progress preservation without reverting to unbounded receiver-side commitments
under the locked same-information replay protocol.
