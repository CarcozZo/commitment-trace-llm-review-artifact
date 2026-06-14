# Network-Service Replay Audit

This audit checks whether the released policy replay rows instantiate network-service
control slots rather than offline answer-quality scoring rows.

## Verdict

- verdict: `PASS`
- policy replay events: 442368
- network-state rows: 2208
- network-state join rate: 1.0000
- hidden-field exclusion rate: 1.0000
- selected PG-C-CPB locked-test events: 6624

## Service-Control Variables

Every policy event is audited for observable service-control variables used at
admission time: packet capacity, verifier capacity, resource utilization, contact
window, link quality, verifier queue length, commitment debt, estimated fanout,
irreversibility, false-risk estimate, and utility-if-true estimate.

| Variable | Coverage | Unique values |
|---|---:|---:|
| `packet_capacity` | 1.0000 | 3 |
| `verifier_capacity` | 1.0000 | 4 |
| `resource_utilization` | 1.0000 | 4 |
| `contact_window_remaining` | 1.0000 | 4 |
| `link_quality` | 1.0000 | 4 |
| `verifier_queue_length` | 1.0000 | 377 |
| `commitment_debt` | 1.0000 | 255880 |
| `estimated_fanout` | 1.0000 | 432 |
| `estimated_irreversibility` | 1.0000 | 112 |
| `estimated_false_risk` | 1.0000 | 143 |
| `estimated_utility_if_true` | 1.0000 | 576 |

## Selected PG-C-CPB Stress Response

The rows below summarize selected PG-C-CPB locked-test action mixes under
observable service stress. `protective_ratio` is the fraction of verify-first,
defer, and reject decisions.

| Stress comparison | Protective ratio | Actionable ratio | Rows |
|---|---:|---:|---:|
| low feedback delay (0-3) | 0.2047 | 0.4356 | 2096 |
| high feedback delay (7+) | 0.3202 | 0.2567 | 2080 |
| verifier scarce (capacity <= 2.5) | 0.3581 | 0.0998 | 2304 |
| verifier ample (capacity > 5) | 0.2010 | 0.4135 | 2880 |

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
- exit status: `PASS`
- paper usability: usable for artifact/audit support and setup-level claims
- dataset: released CommitmentTrace-LLM anonymous artifact
- rows: 442368 policy replay events, 2208 network-state rows
- primary metrics: join rate 1.0000,
  hidden-field exclusion rate 1.0000

## Interpretation Boundary

This audit does not claim that the artifact is a production deployment trace.
It verifies the narrower review claim: the released replay evaluates online
admission decisions over observable network-service state, with frozen LLM
responses acting as role-reactive workload and with latent truth, future verifier
outcomes, and hindsight FCE excluded at admission time.
