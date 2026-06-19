# Examples-to-Metrics Trace

This file links the representative examples to the exact replay metrics used by the paper. It is designed for artifact inspection: a reviewer can trace a claim from message text to parsed commitment state, delayed verifier outcome, and selected-policy replay increments.

## Scope

- Examples are the five high-commitment cases listed in `docs/EXAMPLES.md`.
- Policy rows use validation-selected configurations only.
- Metrics are replay increments for the listed claim/role under Pressure BP, Static CPB, and C-CPB.
- These single-claim traces are inspection anchors, not dominance tests. Aggregate claims are evaluated by the locked operating-region and dominance audits.

## high_fanout_feasible::edge_reservation-0-006

- Template: `edge_reservation`
- Claim type: `token_demand`
- Truth label: `false`
- Verification result: `false` after `5` slots
- Message: The prompt budget is below 256 tokens.

| Role | Parsed state | Pressure | Policy | Action counts | FCE/event | Progress/event | Mean debt | D/R |
|---|---|---:|---|---|---:|---:|---:|---:|
| planner | `TENTATIVE_PLAN` | 4.244 | Pressure BP | `send_actionable:4` | 1.980651 | 0.0 | 8.043134 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 4.244 | Static CPB | `send_actionable:4` | 2.296407 | 0.0 | 19.454249 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 4.244 | C-CPB | `send_actionable:4` | 2.296407 | 0.0 | 18.289431 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 4.244 | C-CPB+Prog. | `send_actionable:4` | 2.296407 | 0.0 | 14.713195 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 5.559 | Pressure BP | `defer:4` | 0.0 | 0.0 | 8.043134 | 1.0/0.0 |
| executor | `PREPARED_ACTION` | 5.559 | Static CPB | `verify_first:4` | 0.0 | 0.0 | 20.010144 | 1.0/0.0 |
| executor | `PREPARED_ACTION` | 5.559 | C-CPB | `send_informational_only:4` | 1.573434 | 0.0 | 19.679168 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 5.559 | C-CPB+Prog. | `send_informational_only:4` | 1.573434 | 0.0 | 16.102932 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.569 | Pressure BP | `defer:1;send_actionable:3` | 0.333082 | 0.0 | 9.969523 | 0.25/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.569 | Static CPB | `send_actionable:4` | 0.444109 | 0.0 | 22.578663 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.569 | C-CPB | `send_actionable:1;send_informational_only:3` | 0.177644 | 0.0 | 20.802895 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.569 | C-CPB+Prog. | `send_actionable:2;send_informational_only:1;verify_first:1` | 0.24426 | 0.0 | 17.611937 | 0.25/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.675 | Pressure BP | `defer:4` | 0.0 | 0.0 | 9.969523 | 1.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.675 | Static CPB | `verify_first:4` | 0.0 | 0.0 | 23.246141 | 1.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.675 | C-CPB | `send_informational_only:4` | 1.5003 | 0.0 | 22.47159 | 0.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.675 | C-CPB+Prog. | `send_informational_only:4` | 1.5003 | 0.0 | 19.280631 | 0.0/0.0 |

## high_fanout_feasible::leo_contact_handover-0-000

- Template: `leo_contact_handover`
- Claim type: `contact_window`
- Truth label: `false`
- Verification result: `false` after `4` slots
- Message: Satellite S4 will remain in view for the next three slots.

| Role | Parsed state | Pressure | Policy | Action counts | FCE/event | Progress/event | Mean debt | D/R |
|---|---|---:|---|---|---:|---:|---:|---:|
| planner | `TENTATIVE_PLAN` | 3.618 | Pressure BP | `send_actionable:4` | 1.369664 | 0.0 | 11.775214 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 3.618 | Static CPB | `send_actionable:4` | 1.588017 | 0.0 | 28.271497 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 3.618 | C-CPB | `send_actionable:4` | 1.588017 | 0.0 | 19.379705 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 3.618 | C-CPB+Prog. | `send_actionable:4` | 1.588017 | 0.0 | 16.260349 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 4.945 | Pressure BP | `defer:3;send_actionable:1` | 0.736813 | 0.0 | 12.331539 | 0.75/0.0 |
| executor | `PREPARED_ACTION` | 4.945 | Static CPB | `reject:4` | 0.0 | 0.0 | 28.271497 | 0.0/1.0 |
| executor | `PREPARED_ACTION` | 4.945 | C-CPB | `send_informational_only:4` | 1.30989 | 0.0 | 20.615984 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 4.945 | C-CPB+Prog. | `send_informational_only:4` | 1.30989 | 0.0 | 17.496628 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.393 | Pressure BP | `defer:3;send_actionable:1` | 0.093229 | 0.0 | 12.929873 | 0.75/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.393 | Static CPB | `reject:4` | 0.0 | 0.0 | 28.271497 | 0.0/1.0 |
| verifier | `VERIFICATION_QUEUED` | 2.393 | C-CPB | `reject:1;send_actionable:1;send_informational_only:2` | 0.13052 | 0.0 | 21.513484 | 0.0/0.25 |
| verifier | `VERIFICATION_QUEUED` | 2.393 | C-CPB+Prog. | `send_actionable:2;verify_first:2` | 0.186457 | 0.0 | 18.812961 | 0.5/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.414 | Pressure BP | `defer:2;send_actionable:2` | 1.632857 | 0.0 | 15.254875 | 0.5/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.414 | Static CPB | `reject:2;send_actionable:2` | 2.252217 | 0.0 | 31.478396 | 0.0/0.5 |
| network_controller | `RESOURCE_RESERVED` | 6.414 | C-CPB | `send_actionable:4` | 4.504434 | 0.0 | 27.927282 | 0.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.414 | C-CPB+Prog. | `send_actionable:4` | 4.504434 | 0.0 | 25.226759 | 0.0/0.0 |

## high_fanout_feasible::distributed_verifier_safety-0-009

- Template: `distributed_verifier_safety`
- Claim type: `resource_demand`
- Truth label: `false`
- Verification result: `false` after `4` slots
- Message: The verification request needs minimal compute.

| Role | Parsed state | Pressure | Policy | Action counts | FCE/event | Progress/event | Mean debt | D/R |
|---|---|---:|---|---|---:|---:|---:|---:|
| planner | `TENTATIVE_PLAN` | 3.370 | Pressure BP | `send_actionable:4` | 1.37824 | 0.0 | 7.245006 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 3.370 | Static CPB | `send_actionable:4` | 1.597959 | 0.0 | 7.604953 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 3.370 | C-CPB | `send_actionable:4` | 1.597959 | 0.0 | 5.656255 | 0.0/0.0 |
| planner | `TENTATIVE_PLAN` | 3.370 | C-CPB+Prog. | `send_actionable:4` | 1.597959 | 0.0 | 3.36981 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 4.486 | Pressure BP | `defer:1;send_actionable:3` | 3.407356 | 0.0 | 9.992462 | 0.25/0.0 |
| executor | `PREPARED_ACTION` | 4.486 | Static CPB | `send_actionable:3;verify_first:1` | 4.172273 | 0.0 | 11.081325 | 0.25/0.0 |
| executor | `PREPARED_ACTION` | 4.486 | C-CPB | `send_actionable:2;send_informational_only:2` | 3.337818 | 0.0 | 8.459781 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 4.486 | C-CPB+Prog. | `send_actionable:2;send_informational_only:2` | 3.337818 | 0.0 | 6.173336 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.328 | Pressure BP | `defer:2;send_actionable:2` | 0.254706 | 0.0 | 11.156212 | 0.5/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.328 | Static CPB | `send_actionable:4` | 0.509413 | 0.0 | 13.408825 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.328 | C-CPB | `verify_first:4` | 0.0 | 0.0 | 8.692531 | 1.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.328 | C-CPB+Prog. | `send_actionable:2;verify_first:2` | 0.254706 | 0.0 | 7.453461 | 0.5/0.0 |
| network_controller | `RESOURCE_RESERVED` | 5.975 | Pressure BP | `defer:3;send_actionable:1` | 0.662008 | 0.0 | 11.828402 | 0.75/0.0 |
| network_controller | `RESOURCE_RESERVED` | 5.975 | Static CPB | `send_actionable:2;verify_first:2` | 2.942256 | 0.0 | 16.695091 | 0.5/0.0 |
| network_controller | `RESOURCE_RESERVED` | 5.975 | C-CPB | `send_informational_only:4` | 1.176902 | 0.0 | 10.186288 | 0.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 5.975 | C-CPB+Prog. | `send_informational_only:4` | 1.176902 | 0.0 | 8.947218 | 0.0/0.0 |

## high_fanout_feasible::multi_edge_model_cache-0-005

- Template: `multi_edge_model_cache`
- Claim type: `wireless_capacity`
- Truth label: `false`
- Verification result: `false` after `4` slots
- Message: The uplink can carry the prompt without retransmissions.

| Role | Parsed state | Pressure | Policy | Action counts | FCE/event | Progress/event | Mean debt | D/R |
|---|---|---:|---|---|---:|---:|---:|---:|
| planner | `VERIFICATION_QUEUED` | 2.560 | Pressure BP | `send_actionable:4` | 1.026428 | 0.0 | 8.791317 | 0.0/0.0 |
| planner | `VERIFICATION_QUEUED` | 2.560 | Static CPB | `send_actionable:4` | 1.190061 | 0.0 | 18.118537 | 0.0/0.0 |
| planner | `VERIFICATION_QUEUED` | 2.560 | C-CPB | `send_actionable:4` | 1.190061 | 0.0 | 14.555208 | 0.0/0.0 |
| planner | `VERIFICATION_QUEUED` | 2.560 | C-CPB+Prog. | `send_actionable:4` | 1.190061 | 0.0 | 9.392423 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 4.792 | Pressure BP | `defer:3;send_actionable:1` | 0.655352 | 0.0 | 9.330403 | 0.75/0.0 |
| executor | `PREPARED_ACTION` | 4.792 | Static CPB | `verify_first:4` | 0.0 | 0.0 | 18.597725 | 1.0/0.0 |
| executor | `PREPARED_ACTION` | 4.792 | C-CPB | `send_actionable:1;send_informational_only:3` | 2.330139 | 0.0 | 16.651653 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 4.792 | C-CPB+Prog. | `send_informational_only:4` | 1.165069 | 0.0 | 10.590391 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.399 | Pressure BP | `send_actionable:4` | 0.356343 | 0.0 | 11.72944 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.399 | Static CPB | `send_actionable:4` | 0.356343 | 0.0 | 20.996762 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.399 | C-CPB | `send_actionable:2;send_informational_only:2` | 0.213806 | 0.0 | 18.151051 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.399 | C-CPB+Prog. | `send_actionable:4` | 0.356343 | 0.0 | 12.989429 | 0.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.389 | Pressure BP | `defer:3;send_actionable:1` | 0.678413 | 0.0 | 12.448202 | 0.75/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.389 | Static CPB | `verify_first:4` | 0.0 | 0.0 | 21.635662 | 1.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.389 | C-CPB | `send_actionable:3;send_informational_only:1` | 4.824271 | 0.0 | 23.342115 | 0.0/0.0 |
| network_controller | `RESOURCE_RESERVED` | 6.389 | C-CPB+Prog. | `send_informational_only:4` | 1.206068 | 0.0 | 14.586679 | 0.0/0.0 |

## high_fanout_feasible::uav_rerouting-0-002

- Template: `uav_rerouting`
- Claim type: `edge_capacity`
- Truth label: `false`
- Verification result: `false` after `4` slots
- Message: Edge node E4 can accept the high-priority inference job.

| Role | Parsed state | Pressure | Policy | Action counts | FCE/event | Progress/event | Mean debt | D/R |
|---|---|---:|---|---|---:|---:|---:|---:|
| planner | `VERIFICATION_QUEUED` | 2.933 | Pressure BP | `send_actionable:4` | 0.969725 | 0.0 | 5.719229 | 0.0/0.0 |
| planner | `VERIFICATION_QUEUED` | 2.933 | Static CPB | `send_actionable:4` | 0.969725 | 0.0 | 7.742001 | 0.0/0.0 |
| planner | `VERIFICATION_QUEUED` | 2.933 | C-CPB | `send_actionable:4` | 0.969725 | 0.0 | 8.920481 | 0.0/0.0 |
| planner | `VERIFICATION_QUEUED` | 2.933 | C-CPB+Prog. | `send_actionable:4` | 0.969725 | 0.0 | 6.742953 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 5.165 | Pressure BP | `defer:1;send_actionable:3` | 4.330436 | 0.0 | 9.593024 | 0.25/0.0 |
| executor | `PREPARED_ACTION` | 5.165 | Static CPB | `reject:2;send_actionable:2` | 2.886957 | 0.0 | 10.324531 | 0.0/0.5 |
| executor | `PREPARED_ACTION` | 5.165 | C-CPB | `send_actionable:2;send_informational_only:2` | 3.464349 | 0.0 | 12.148643 | 0.0/0.0 |
| executor | `PREPARED_ACTION` | 5.165 | C-CPB+Prog. | `send_informational_only:4` | 1.154783 | 0.0 | 8.034218 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.822 | Pressure BP | `defer:1;send_actionable:3` | 0.322863 | 0.0 | 11.70929 | 0.25/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.822 | Static CPB | `send_actionable:4` | 0.430484 | 0.0 | 13.14622 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.822 | C-CPB | `send_actionable:2;send_informational_only:2` | 0.258291 | 0.0 | 13.912199 | 0.0/0.0 |
| verifier | `VERIFICATION_QUEUED` | 2.822 | C-CPB+Prog. | `send_actionable:3;send_informational_only:1` | 0.344387 | 0.0 | 10.32684 | 0.0/0.0 |
| network_controller | `PREPARED_ACTION` | 5.165 | Pressure BP | `defer:3;send_actionable:1` | 0.515835 | 0.0 | 12.29036 | 0.75/0.0 |
| network_controller | `PREPARED_ACTION` | 5.165 | Static CPB | `reject:3;send_actionable:1` | 1.146301 | 0.0 | 14.437485 | 0.0/0.75 |
| network_controller | `PREPARED_ACTION` | 5.165 | C-CPB | `send_actionable:3;send_informational_only:1` | 3.668163 | 0.0 | 18.108809 | 0.0/0.0 |
| network_controller | `PREPARED_ACTION` | 5.165 | C-CPB+Prog. | `send_actionable:2;send_informational_only:2` | 2.751122 | 0.0 | 13.555002 | 0.0/0.0 |

## Audit Outputs

- CSV: `results/round3_trace_to_metrics.csv`
- JSON QA: `results/round3_trace_to_metrics.json`
- Trace rows: `80`
