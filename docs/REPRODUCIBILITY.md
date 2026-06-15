# Reproducibility Guide

This guide records the command chain for checking the released CommitmentTrace-LLM artifact and reproducing the numerical summaries used by the manuscript. Run commands from the artifact root unless a command explicitly points to the repository-level scripts directory.

## Reviewer Checklist

The recommended review sequence is:

1. run the five artifact-root commands in the quickstart;
2. inspect `docs/DATASET_CARD.md` for the template, split, and online-observation
   boundary;
3. inspect `docs/BASELINE_FAIRNESS_AUDIT.md` for validation-only selection and
   same-information replay;
4. inspect `docs/NETWORK_SERVICE_REPLAY_AUDIT.md` for packet capacity, verifier
   capacity, feedback delay, resource utilization, verifier queue, and
   commitment-debt coverage;
5. inspect the released `results/round7_*` CSV files for the source data used
   by the manuscript figures.

All checks are deterministic on the released files and run as CPU-only artifact
audits with no LLM API calls.

## 1. Validate Dataset Structure

```powershell
python scripts\validate_commitmenttrace.py --root .
```

Expected result:

- `verdict: PASS`
- 576 claims
- 2,304 raw role-agent responses
- 2,304 transition labels
- 576 verifier outcomes
- 2,208 network-state rows
- 442,368 policy replay events

## 2. Audit Traceability and Online Observation Boundary

```powershell
python scripts\audit_commitmenttrace_dataset.py --root .
```

Expected checks:

- every claim has four role responses and four parsed transition labels;
- hidden labels and hindsight metrics are excluded from online policy features;
- all policy events carry stress features for commitment debt, estimated fanout, packet capacity, resource utilization, verifier capacity, and verifier queue length;
- train/validation/ID/OOD splits match the released split file.

## 3. Summarize Locked Test Results

```powershell
python scripts\summarize_locked_results.py --root .
```

Expected high-level result:

- seven policies are summarized from validation-selected configurations;
- the locked dominance audit reports `1/672` baseline rows core-dominate selected PG-C-CPB rows.

## 4. Audit Network-Service Replay Boundary

```powershell
python scripts\audit_network_service_replay.py --root .
```

Expected checks:

- every released policy replay event joins to an observable network-state row;
- every released policy replay event includes observable service-control
  variables such as packet capacity, verifier capacity, feedback delay,
  resource utilization, verifier queue, commitment debt, fanout, and utility;
- selected PG-C-CPB locked-test action mixes are summarized across feedback
  delay and verifier-capacity stress bins.

Expected high-level result:

- `verdict: PASS`
- network-state join rate `1.0000`
- hidden-field exclusion rate `1.0000`
- 6,624 selected PG-C-CPB locked-test events

Generated outputs:

- `docs/NETWORK_SERVICE_REPLAY_AUDIT.md`
- `results/round8_network_service_replay_audit.csv`
- `results/round8_network_service_replay_audit.json`

## 5. Check Anonymity

```powershell
python scripts\check_anonymity.py --root .
```

Expected result:

- `verdict: PASS`

The check scans released text and metadata for known author, institution, local-path, and credential patterns used during artifact preparation.

## 6. Reproduce Round-2 Baseline Fairness Audit

From the repository root:

```powershell
python scripts\audit_round2_baseline_fairness.py --root artifact_release\commitmenttrace_llm_anonymous_v1
```

Generated outputs:

- `results/round2_baseline_fairness_audit.csv`
- `results/round2_baseline_fairness_audit.json`
- `docs/BASELINE_FAIRNESS_AUDIT.md`

The audit reports validation budget, selected configurations, observed action sets, online feature keys, hidden-field exclusion, and locked test tradeoffs for each policy.

## 7. Reproduce Round-2 Stress-Response Figure

From the repository root:

```powershell
python scripts\build_round2_stress_response_v14.py --artifact-root artifact_release\commitmenttrace_llm_anonymous_v1
```

Generated outputs:

- released stress-response source tables under `results/`

The script uses validation-selected configurations and locked test events only. It constructs an event-level online stress index from observable delay, fanout, resource utilization, verifier backlog, verifier capacity, and packet capacity.

## 8. Reproduce Round-3 Robustness Audit

From the repository root:

```powershell
python scripts\build_round3_robustness_v15.py --artifact-root artifact_release\commitmenttrace_llm_anonymous_v1
```

Generated outputs:

- `docs/ROBUSTNESS_AUDIT.md`
- `results/round3_robustness_audit.csv`
- `results/round3_robustness_audit.json`
- `results/round3_robustness_audit.csv`

The audit uses validation-selected configurations and locked test events only.
It checks split/regime stability, deterministic parser label-confidence
thresholds, and subset dominance rates against selected PG-C-CPB rows.

## 9. Reproduce Examples-to-Metrics Trace

From the repository root:

```powershell
python scripts\build_examples_to_metrics_trace.py --root artifact_release\commitmenttrace_llm_anonymous_v1
```

Generated outputs:

- `docs/TRACE_TO_METRICS.md`
- `results/round3_trace_to_metrics.csv`
- `results/round3_trace_to_metrics.json`

The trace links the five representative examples to claim records, transition
labels, delayed verifier outcomes, and selected-policy replay increments.

## 10. Reproduce Verifier Delay/Budget Audit

From the repository root:

```powershell
python scripts\build_round4_verifier_delay_budget_audit.py --artifact-root artifact_release\commitmenttrace_llm_anonymous_v1
```

Generated outputs:

- `docs/VERIFIER_DELAY_BUDGET_AUDIT.md`
- `results/round4_verifier_delay_budget_audit.csv`
- `results/round4_verifier_delay_budget_audit.json`
- `results/round4_verifier_delay_budget_audit.csv`

The audit groups locked test events by observable feedback delay and verifier
capacity. It is a direct RQ3 support check using the locked policy
configurations.

## 11. Recompute Release Manifest

If any released file changes, regenerate the manifest and SHA list from the repository root:

```powershell
python scripts\refresh_commitmenttrace_manifest.py --root artifact_release\commitmenttrace_llm_anonymous_v1
```

If that helper is unavailable, recompute SHA256 values for all files except `docs/RELEASE_MANIFEST.tsv` and `docs/SHA256SUMS.txt`, preserving the existing two-space `SHA  path` format in `SHA256SUMS.txt`.

## Interpretation Boundary

The released artifact supports same-information, validation-locked trace replay.
Metrics are computed after replay from frozen transition labels and hidden
evaluation labels. Policy inputs exclude latent truth, future verifier outcomes,
future downstream actions, and realized FCE at decision time.
