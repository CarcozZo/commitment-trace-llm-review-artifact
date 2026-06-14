# Representative Trace Examples

This file provides compact, anonymized examples from CommitmentTrace-LLM. The goal is to show how a received message can authorize different receiver-side commitments even when every role responds locally and constructively. Full raw responses are stored in `data/raw_agent_responses.jsonl.gz`; this document only reports short summaries and parsed transition fields.

## Example 1: Edge Reservation Token Demand

- `claim_id`: `high_fanout_feasible::edge_reservation-0-006`
- `template_id`: `edge_reservation`
- `claim_type`: `token_demand`
- `message`: The prompt budget is below 256 tokens.
- `truth_label`: `false`
- `total_commitment_pressure`: `19.046`

| Role | Parsed action state | Commitment type | Verification queued | Commitment pressure | Local response summary |
|---|---|---|---:|---:|---|
| planner | `TENTATIVE_PLAN` | `plan` | yes | 4.244 | The message may affect LLM resource allocation, so the planner prepares a tentative allocation plan. |
| executor | `PREPARED_ACTION` | `action` | yes | 5.559 | The executor prepares for resource allocation while requesting verification. |
| verifier | `VERIFICATION_QUEUED` | `verification_queue` | yes | 2.569 | The verifier queues validation because the token-demand state is uncertain. |
| network_controller | `RESOURCE_RESERVED` | `resource_reservation` | yes | 6.675 | The controller reserves capacity to keep the inference service ready. |

Interpretation: the claim is false, but each role's response is locally reasonable. The system-level cost appears because the message authorizes a plan, an action preparation, a verifier queue entry, and a resource reservation before feedback arrives.

## Example 2: LEO Contact Handover

- `claim_id`: `high_fanout_feasible::leo_contact_handover-0-000`
- `template_id`: `leo_contact_handover`
- `claim_type`: `contact_window`
- `message`: Satellite S4 will remain in view for the next three slots.
- `truth_label`: `false`
- `total_commitment_pressure`: `17.371`

| Role | Parsed action state | Commitment type | Verification queued | Commitment pressure | Local response summary |
|---|---|---|---:|---:|---|
| planner | `TENTATIVE_PLAN` | `plan` | yes | 3.618 | The planner prepares migration planning around the claimed contact window. |
| executor | `PREPARED_ACTION` | `action` | no | 4.945 | The executor prepares handover-related action because the claimed utility is high. |
| verifier | `VERIFICATION_QUEUED` | `verification_queue` | yes | 2.393 | The verifier queues a check on the satellite visibility duration. |
| network_controller | `RESOURCE_RESERVED` | `resource_reservation` | yes | 6.414 | The controller reserves resources for the contact window while verification remains pending. |

Interpretation: the controller and executor do not act maliciously; they prepare for a plausible high-utility contact opportunity. The false message nevertheless creates commitment debt through reserved resources and prepared execution.

## Example 3: Distributed Verifier Compute Demand

- `claim_id`: `high_fanout_feasible::distributed_verifier_safety-0-009`
- `template_id`: `distributed_verifier_safety`
- `claim_type`: `resource_demand`
- `message`: The verification request needs minimal compute.
- `truth_label`: `false`
- `total_commitment_pressure`: `16.158`

| Role | Parsed action state | Commitment type | Verification queued | Commitment pressure | Local response summary |
|---|---|---|---:|---:|---|
| planner | `TENTATIVE_PLAN` | `plan` | yes | 3.370 | The planner treats the request as feasible and prepares a validation plan. |
| executor | `PREPARED_ACTION` | `action` | yes | 4.486 | The executor prepares because the request appears resource-efficient. |
| verifier | `VERIFICATION_QUEUED` | `verification_queue` | yes | 2.328 | The verifier queues the request under moderate false-risk estimates. |
| network_controller | `RESOURCE_RESERVED` | `resource_reservation` | yes | 5.975 | The controller reserves compute to keep the verification path ready. |

Interpretation: verifier capacity is exactly the scarce network service in this scenario. A false low-cost claim can increase verifier backlog and reserved compute even before the actual verifier outcome is observed.

## Example 4: Multi-Edge Wireless Capacity

- `claim_id`: `high_fanout_feasible::multi_edge_model_cache-0-005`
- `template_id`: `multi_edge_model_cache`
- `claim_type`: `wireless_capacity`
- `message`: The uplink can carry the prompt without retransmissions.
- `truth_label`: `false`
- `total_commitment_pressure`: `16.140`

| Role | Parsed action state | Commitment type | Verification queued | Commitment pressure | Local response summary |
|---|---|---|---:|---:|---|
| planner | `VERIFICATION_QUEUED` | `verification_queue` | yes | 2.560 | The planner asks for validation because uplink capacity is uncertain. |
| executor | `PREPARED_ACTION` | `action` | yes | 4.792 | The executor prepares because the potential utility of prompt transmission is high. |
| verifier | `VERIFICATION_QUEUED` | `verification_queue` | yes | 2.399 | The verifier queues a check on the wireless-capacity claim. |
| network_controller | `RESOURCE_RESERVED` | `resource_reservation` | yes | 6.389 | The controller reserves uplink resources for prompt transmission. |

Interpretation: this example separates information from actionability. Sending the message as actionable can trigger resource reservation; sending it as informational-only would preserve awareness with lower downstream commitment.

## Example 5: UAV Rerouting Edge Capacity

- `claim_id`: `high_fanout_feasible::uav_rerouting-0-002`
- `template_id`: `uav_rerouting`
- `claim_type`: `edge_capacity`
- `message`: Edge node E4 can accept the high-priority inference job.
- `truth_label`: `false`
- `total_commitment_pressure`: `16.085`

| Role | Parsed action state | Commitment type | Verification queued | Commitment pressure | Local response summary |
|---|---|---|---:|---:|---|
| planner | `VERIFICATION_QUEUED` | `verification_queue` | yes | 2.933 | The planner requests verification before committing to the high-priority job. |
| executor | `PREPARED_ACTION` | `action` | yes | 5.165 | The executor prepares because the inference job is important but capacity is uncertain. |
| verifier | `VERIFICATION_QUEUED` | `verification_queue` | yes | 2.822 | The verifier queues validation of edge-node capacity. |
| network_controller | `PREPARED_ACTION` | `action` | yes | 5.165 | The controller prepares capacity-related action while requesting verification. |

Interpretation: high priority and uncertainty coexist. A send/drop controller treats delivery as the main decision, while commitment authorization distinguishes verification-only, informational, prepared-action, and resource-reservation states.

## Field Traceability

The examples above can be reproduced from the following files:

- `data/claims.jsonl.gz`: `message`, `template_id`, `claim_type`, and `truth_label`.
- `data/raw_agent_responses.jsonl.gz`: role-conditioned JSON responses.
- `data/transition_labels.jsonl.gz`: parsed `intended_action_state`, `commitment_type`, `verification_queued`, and `commitment_pressure`.
- `data/policy_replay_events.jsonl.gz`: online replay action, hidden-field exclusion flag, feedback delay, FCE increment, progress increment, commitment debt, and verifier queue.

The label audit is a deterministic parser audit. It checks traceability and schema consistency; it is not presented as a human inter-annotator agreement study.

