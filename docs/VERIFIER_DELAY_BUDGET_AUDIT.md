# Verifier Delay/Budget Audit

This audit directly supports RQ3 using validation-selected configurations and locked test events only. It groups events by observable verifier-feedback delay and verifier capacity; it does not retune policies.

## High-Stress Summary

High stress means feedback delay >= 6 slots or verifier capacity <= 2.

| Policy | Events | FCE/prog | Progress/event | Mean debt | Verify-first | Inform | Defer |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pressure BP | 3088 | 2.2635 | 0.1135 | 15.3169 | 0.0000 | 0.0000 | 0.5427 |
| Static CPB | 3088 | 2.6362 | 0.0972 | 38.4942 | 0.1856 | 0.0000 | 0.1856 |
| C-CPB | 3088 | 2.6157 | 0.1490 | 32.9398 | 0.1736 | 0.3970 | 0.2989 |
| PG-C-CPB | 3088 | 2.4200 | 0.1535 | 34.6038 | 0.1694 | 0.4521 | 0.2503 |

## Interpretation

The audit shows how verifier delay and verifier budget enter the replay as observable network-control states. C-CPB reacts by changing receiver authorization states instead of using only a send/drop response.

- Event rows used: `26496`.
- Figure package: reproduced from the released result tables under `results/`.
- Source data: released CSV/JSON summaries under `results/`.
