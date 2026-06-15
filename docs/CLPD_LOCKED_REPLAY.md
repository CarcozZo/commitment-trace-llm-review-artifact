# CLPD Locked Replay

This note maps the manuscript's CLPD claims to released result files. CLPD is
evaluated as the framework-specific online controller over the same frozen
trace records, validation splits, online observation boundary, verifier
budgets, and hidden-field exclusion rule used by the baseline audit.

## Released Files

| File | Purpose |
|---|---|
| `results/clpd_policy_configs.csv` | CLPD validation configuration grid |
| `results/clpd_validation_config_metrics.csv` | validation metrics for 24 CLPD configurations |
| `results/clpd_selected_configs.csv` | validation-selected CLPD operating points |
| `results/clpd_test_metrics.csv` | locked test metrics for selected CLPD configurations |
| `results/clpd_comparison_summary.csv` | aggregate comparison against strong baselines |
| `results/clpd_anchor_gate_summary.csv` | validation-locked anchor comparison used in the abstract and RQ1 |
| `results/clpd_pareto_points.csv` | CLPD validation Pareto context |
| `results/fig3_oldstyle_clpd_operating_source_v1.csv` | source data for Fig. 3 |
| `results/fig4_oldstyle_clpd_displacement_source_v1.csv` | source data for Fig. 4 |
| `results/fig5_oldstyle_clpd_phase_source_v1.csv` | source data for Fig. 5 |
| `results/fig6_oldstyle_clpd_role_action_source_v1.csv` | source data for Fig. 6 |

## Replay Scope

- CLPD configurations: `24`, matching the per-policy validation budget used for
  the baseline suite.
- CLPD policy event rows: `55,296`.
- CLPD aggregated rows: `312`.
- CLPD validation rows: `24`.
- CLPD validation Pareto rows: `17`.
- Selected CLPD configs: `clpd_cfg005`, `clpd_cfg018`, `clpd_cfg016`,
  `clpd_cfg003`, and `clpd_cfg013`.
- Manuscript anchor: `clpd_cfg016`.

## Anchor Metrics

The manuscript uses `clpd_cfg016` as the validation-locked anchor. In
`results/clpd_anchor_gate_summary.csv`, the anchor has:

| Metric | Value |
|---|---:|
| FCE/message | `0.330245` |
| Progress/message | `0.231742` |
| Mean commitment debt | `17.388952` |
| Withheld ratio | `0.059783` |
| Progress ratio vs selected PG-C-CPB | `1.040109` |
| FCE ratio vs selected PG-C-CPB | `0.844992` |
| Debt ratio vs selected PG-C-CPB | `0.822337` |
| Withheld-ratio delta vs selected PG-C-CPB | `-0.212258` |
| Replacement gate | `1` |

These values correspond to the manuscript statement that the locked CLPD anchor
improves progress/message by about `4.0%`, reduces FCE/message by about
`15.5%`, lowers debt by about `17.8%`, and reduces withheld-action cost by about
`21.2` percentage points relative to the selected progress-queued C-CPB
operating region.

## Baseline Boundary

The original baseline result files remain in `results/` because they document
the same-information replay suite, selected PG-C-CPB operating region, dominance
checks, verifier-delay audit, and robustness checks. CLPD result files are the
main files for the manuscript's proposed controller; the progress-guarded files
support the strong-baseline comparison.
