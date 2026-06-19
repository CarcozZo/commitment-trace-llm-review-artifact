# Progress-Guard Audit

This audit documents the progress-deficit queue added to the progress-queued
C-CPB replay.  It uses the same frozen trace records, validation-locked
configuration selection, hidden-field exclusion rule, and locked test splits as
the main artifact.

## Replay Boundary

C-CPB+Prog. adds an online progress-deficit queue to the prior C-CPB controller.
The queue is updated from observable priority and estimated utility/service, not
from latent truth labels, future verifier outcomes, hindsight FCE, or realized
true progress at admission time.

Released source data:

- `results/round5_progress_guard_policy_summary.csv`
- `results/round5_progress_guard_operating_points.csv`
- `results/round5_progress_guard_stress_bins.csv`
- `results/round5_progress_guard_figure_qa.json`
- `results/round5_online_ablation_curve_source.csv`
- `results/round5_online_ablation_tradeoff_source.csv`
- `results/round5_role_actionability_source.csv`
- `results/round5_role_summary_source.csv`

## Locked Test Summary

| Policy | FCE/msg | Progress/msg | Terminal debt | Withheld action | Waste/msg |
|---|---:|---:|---:|---:|---:|
| Pressure BP | 0.311238 | 0.176739 | 18.403715 | 47.4336% | 0.008885 |
| Static CPB | 0.293083 | 0.163072 | 34.773152 | 53.8043% | 0.009632 |
| C-CPB | 0.433280 | 0.217093 | 21.908040 | 30.6612% | 0.018535 |
| C-CPB+Prog. | 0.390827 | 0.222805 | 21.145766 | 27.2041% | 0.012471 |
| Action admission | 0.428490 | 0.251386 | 43.706691 | 21.5580% | 0.016822 |

Compared with C-CPB, C-CPB+Prog. reduces FCE/msg by 9.80%, increases
progress/msg by 2.63%, lowers terminal debt by 3.48%, lowers withheld-action
cost by 11.28%, and lowers resource waste/msg by 32.72%.

Compared with Pressure BP and Static CPB, C-CPB+Prog. preserves higher progress
while avoiding the high withheld-action operating region.  The supported claim
is therefore not that C-CPB+Prog. minimizes every scalar metric, but that the
progress-deficit queue improves the progress-preserving commitment-control
operating region under delayed verification.

## Mechanism Interpretation

The progress-deficit queue addresses a specific failure mode: low-FCE policies
can appear safe by suppressing receiver-side action.  C-CPB+Prog. prices this
suppression as an online service deficit.  When delayed feedback and verifier
pressure accumulate, the controller still prices commitment debt and verifier
scarcity, but it also increases the weight of estimated useful progress so that
the system does not drift into a low-action, low-progress corner.

This mechanism is evaluated as an online controller: the progress-deficit
feature appears in released `online_features_json` only for C-CPB+Prog. rows and is
computed before hidden evaluation fields are used.

The online-ablation and role-actionability source files support the main-paper
figures that compare C-CPB+Prog. against same-control-surface ablations and audit
how receiver roles move through actionable, informational-only, verify-first,
defer, and reject labels.
