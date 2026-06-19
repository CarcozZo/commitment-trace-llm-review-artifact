# Robustness Audit

This audit uses validation-selected configurations and locked test events only. It does not retune policies or change the replay protocol.

## Checks

- Split/regime stability over ID, OOD-template, and OOD-network tests.
- Deterministic parser label-confidence threshold sensitivity.
- Subset dominance rates against selected C-CPB+Prog. rows under the same threshold, split, and regime.

## Threshold Summary

| Threshold | C-CPB+Prog. events | C-CPB+Prog. FCE/prog | Pressure BP FCE/prog | Static CPB FCE/prog | Dominance rate |
|---:|---:|---:|---:|---:|---:|
| 0.35 | 6620 | 1.7534 | 1.7598 | 1.7923 | 0.30% |
| 0.45 | 6556 | 1.7472 | 1.7493 | 1.7828 | 0.30% |
| 0.55 | 5776 | 1.6309 | 1.5741 | 1.5671 | 0.15% |
| 0.65 | 5288 | 1.4447 | 1.4216 | 1.4048 | 0.45% |

## Interpretation

The robustness audit is intended as a paper-supporting check, not as a new main claim. It verifies that the reported operating-region comparison is not created by a single parser-confidence slice or a single ID/OOD block.

- Minimum label-threshold event count for C-CPB+Prog.: `5288`.
- Maximum subset dominance rate across tested thresholds: `0.45%`.
- Figure package: reproduced from the released result tables under `results/`.
