# Codex 回复内容清单与交互规范

用途：每次 Codex 完成任务后，必须按本清单回复，便于人工审计、复现和继续迭代。  
原则：不接受“已修复”“已完善”“已验证”这类无证据结论。每个结论都必须绑定文件、命令、指标、日志或剩余风险。

---

## 1. 顶部摘要

Codex 回复开头必须包含：

```text
Target: INFOCOM acceptance hardening
Branch/commit:
Scope completed:
Scope not completed:
Recommendation for next audit:
```

要求：

- 写出准确 commit SHA；
- 写出修改文件数量；
- 写出新增/更新/删除文件路径；
- 写出本轮没有完成的内容，不得省略；
- 若存在失败命令，必须置顶说明。

---

## 2. 逐项任务状态表

必须使用如下表格：

| Workstream | Required deliverables | Status | Evidence files | Validation command | Result | Remaining risk |
|---|---|---:|---|---|---|---|
| A. Authorization lattice | ... | done/partial/not done | ... | ... | PASS/FAIL/N/A | ... |
| B. CLPD theory mapping | ... | done/partial/not done | ... | ... | PASS/FAIL/N/A | ... |
| C. Receiver intervention | ... | done/partial/not done | ... | ... | PASS/FAIL/N/A | ... |
| D. Verify/reject mechanism | ... | done/partial/not done | ... | ... | PASS/FAIL/N/A | ... |
| E. Baseline/statistics | ... | done/partial/not done | ... | ... | PASS/FAIL/N/A | ... |
| F. Reproducibility/anonymity | ... | done/partial/not done | ... | ... | PASS/FAIL/N/A | ... |

状态定义：

- `done`：交付文件存在，命令可运行，结果通过，主文/文档同步更新；
- `partial`：有交付但缺命令、缺结果、缺文档同步、或结果不完全支持主张；
- `not done`：没有实质交付；
- 不允许用 `mostly done`、`should be okay`、`looks good` 等模糊状态。

---

## 3. 文件级变更清单

必须列出所有新增和修改文件：

```text
Added:
- path: purpose

Modified:
- path: change summary

Deleted:
- path: reason
```

每个文件都必须说明用途。例如：

```text
Added:
- docs/AUTHORIZATION_LATTICE.md: Defines capability-set lattice and separates admission outcomes from authorization elements.
- scripts/check_authorization_lattice.py: Enumerates elements and verifies meet/join uniqueness.
- results/authorization_lattice_check.json: Machine-readable PASS/FAIL output from the checker.
```

---

## 4. 命令与日志

必须提供实际运行过的命令，不得只写“tests passed”。

格式：

```bash
python scripts/check_authorization_lattice.py --root .
python scripts/audit_clpd_score_mapping.py --root .
python scripts/run_receiver_intervention.py --root . --config experiments/intervention/intervention_config.yaml
python scripts/bootstrap_by_source_claim.py --root .
python scripts/run_all_audits.py --root . --out results_reproduced
python scripts/check_anonymity.py --root .
```

每条命令后必须写：

```text
exit status:
runtime:
output artifact:
important stdout summary:
```

如果命令未运行，必须写：

```text
Not run. Reason: ...
```

不允许把未运行的命令写成 expected command。

---

## 5. 核心数值变化表

凡涉及实验或指标，必须提供 before/after 表。至少包括：

| Metric | Previous value | New value | Source file | Interpretation |
|---|---:|---:|---|---|
| CLPD FCE/msg | ... | ... | ... | ... |
| CLPD progress/msg | ... | ... | ... | ... |
| closest C-CPB+Prog FCE/msg | ... | ... | ... | ... |
| closest C-CPB+Prog progress/msg | ... | ... | ... | ... |
| withheld delta | ... | ... | ... | ... |
| verify-first activation | ... | ... | ... | ... |
| reject activation | ... | ... | ... | ... |
| source-claim clustered CI | absent/present | ... | ... | ... |
| parser/intervention calibration | absent/present | ... | ... | ... |

要求：

- 所有数字必须能追溯到 CSV/JSON；
- 不允许只在 prose 中写百分比；
- 如果发现旧摘要数字不再成立，必须明确指出。

---

## 6. 理论修复回复格式

若修改了 lattice / CLPD theory，必须回答：

```text
1. What is the formal authorization set?
2. What is the partial order?
3. What are meet and join?
4. Are defer and reject inside or outside the lattice?
5. What is the exact definition of minimum sufficient authorization?
6. What is the per-slot objective?
7. Which queue produces each score term?
8. Which terms are theoretical and which are engineering tie-breakers?
9. What solver is used for the per-slot budgeted decision?
10. If greedy is used, what is the approximation/gap evidence?
11. What theorem changed?
12. What assumptions are required?
```

必须附：

- proof file path；
- mapping table path；
- checker script path；
- checker output path。

---

## 7. Receiver intervention 回复格式

若做了软件级 receiver intervention，必须回答：

```text
1. How many source claims?
2. How many claim-role pairs?
3. Which authorization labels were intervened?
4. Which receiver roles?
5. Which tool stubs?
6. How was state isolated?
7. Which seeds?
8. What outcomes were logged?
9. What are ATE(actionable - info), ATE(verify - info), ATE(defer - actionable)?
10. What are precision/recall/calibration/Brier/confusion matrix results?
11. Which claims failed or were ambiguous?
12. What changes to replay dynamics are recommended by the intervention?
```

必须附：

- raw logs path；
- summary CSV path；
- calibration CSV path；
- audit markdown path。

---

## 8. Verify-first / reject 回复格式

必须回答：

```text
1. Did verify-first activate?
2. Did reject activate?
3. In which stress/risk/utility bins?
4. Did verify-first use delayed release?
5. How does reject differ from defer in queue semantics?
6. What FCE/progress/debt effect did these actions have?
7. Are there case studies?
8. If either action remains zero, what is the root cause?
```

若 verify-first/reject 仍为零，必须明确建议：

- 修改机制；
- 修改配置；
- 或收缩论文贡献。

不允许只写“action space supports them”。

---

## 9. Baseline/statistics 回复格式

必须回答：

```text
1. What is the closest matched C-CPB+Prog baseline?
2. What is the best-FCE baseline?
3. What is the best-progress baseline?
4. Is CLPD on the Pareto frontier?
5. What is the source-claim clustered 95% CI?
6. Does the old abstract comparison still hold?
7. Which claims/regimes drive the gains?
8. Are results stable across ID/OOD-template/OOD-network?
```

必须附：

- `results/matched_baseline_table.csv`
- `results/pareto_frontier.csv`
- `results/clustered_bootstrap_ci.csv`
- `docs/STATISTICAL_AUDIT.md`

---

## 10. Reproducibility/anonymity 回复格式

必须回答：

```text
1. Does a fresh clone run one command to regenerate all main tables?
2. What is that one command?
3. Which scripts are referenced by docs but absent from release?
4. Were manifest and SHA256 refreshed?
5. Did anonymity check pass?
6. Does the external release path avoid personal GitHub identity?
7. What files are intentionally precomputed rather than regenerated?
```

必须附：

- command output summary；
- manifest diff；
- SHA diff；
- anonymity check output。

---

## 11. 不接受的回复类型

以下回复视为不合格：

```text
- "All requested changes are complete."  # 没有证据
- "The theory is now rigorous."          # 没有定理、假设、映射、命令
- "Intervention experiment added."       # 没有 raw logs 和 ATE/CI
- "Baselines are fair."                  # 没有 matched/Pareto/CI 表
- "Anonymity passed."                    # 没有命令输出和外部发布路径说明
- "Could not do X due to time."          # 没有 partial fallback 和剩余风险
```

---

## 12. Codex 最终回复模板

Codex 可以直接复制以下模板填写：

```markdown
# Codex Completion Report

Target: INFOCOM acceptance hardening
Branch/commit:
Date:
Scope completed:
Scope not completed:
Recommended next audit focus:

## 1. Workstream Status

| Workstream | Status | Evidence files | Validation command | Result | Remaining risk |
|---|---|---|---|---|---|
| A. Authorization lattice |  |  |  |  |  |
| B. CLPD theory mapping |  |  |  |  |  |
| C. Receiver intervention |  |  |  |  |  |
| D. Verify/reject mechanism |  |  |  |  |  |
| E. Baseline/statistics |  |  |  |  |  |
| F. Reproducibility/anonymity |  |  |  |  |  |

## 2. Files Changed

### Added
-

### Modified
-

### Deleted
-

## 3. Commands Run

```bash
# command
```

exit status:
runtime:
output artifact:
stdout summary:

## 4. Key Numerical Changes

| Metric | Previous | New | Source file | Interpretation |
|---|---:|---:|---|---|
|  |  |  |  |  |

## 5. Theory Answers

1. Formal authorization set:
2. Partial order:
3. Meet/join:
4. Defer/reject placement:
5. Minimum sufficient authorization:
6. Per-slot objective:
7. Queue-to-score mapping:
8. Engineering tie-breakers:
9. Solver:
10. Greedy/approximation evidence:
11. Theorem changes:
12. Assumptions:

## 6. Intervention Answers

1. Source claims:
2. Claim-role pairs:
3. Labels:
4. Roles:
5. Tool stubs:
6. State isolation:
7. Seeds:
8. Outcomes:
9. ATE/CI:
10. Calibration/confusion matrix:
11. Ambiguous/failure cases:
12. Replay model changes:

## 7. Verify/Reject Answers

1. Verify-first activation:
2. Reject activation:
3. Stress bins:
4. Delayed release:
5. Reject vs defer:
6. Metric effect:
7. Case studies:
8. Remaining zero-action root cause:

## 8. Baseline/Statistics Answers

1. Closest matched baseline:
2. Best-FCE baseline:
3. Best-progress baseline:
4. Pareto status:
5. Clustered 95% CI:
6. Abstract comparison validity:
7. Gain drivers:
8. ID/OOD stability:

## 9. Reproducibility/Anonymity Answers

1. One-command reproduction:
2. Command:
3. Missing referenced scripts:
4. Manifest/SHA:
5. Anonymity:
6. External release path:
7. Precomputed outputs:

## 10. Remaining Risks

- P0:
- P1:
- P2:
```
