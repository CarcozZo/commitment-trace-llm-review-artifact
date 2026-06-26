# INFOCOM 接收导向改进包（无真实硬件模拟版）

日期：2026-06-26  
目标：将 CommitmentTrace-LLM 从“可审计 replay artifact”推进到“具备 INFOCOM 接收竞争力的网络系统/在线控制论文”。  
硬约束：当前时间不足以支持真实硬件部署、真实硬件模拟、大规模 ns-3/Mininet/Kubernetes testbed。不要把精力投入硬件环境搭建。  
非妥协原则：不靠降级措辞掩盖根因；能直接修复的问题直接修复，不能做硬件验证的部分用严格的软件级干预、trace-driven service simulation、统计审计和理论闭环替代。

---

## 0. 当前判断

当前版本的 artifact 工程明显进步：数据、结果、脚本、baseline audit、network-service replay audit、manifest 已基本齐备。但若以 INFOCOM 接收为目标，当前主要风险仍集中在：

1. authorization lattice / CLPD 理论链条未完全闭合；
2. frozen replay 尚未验证不同 authorization label 真实改变 receiver 行为；
3. baseline 口径需要从“平均 selected operating region”升级为 matched / Pareto / closest-strong-baseline 比较；
4. CLPD anchor 未激活 verify-first / reject，五类动作机制说服力不足；
5. 统计上缺 source-claim clustered CI；
6. artifact 的 full reproducibility guide 与实际发布脚本仍需完全对齐；
7. 双盲发布必须使用匿名 ZIP 或匿名 mirror，不能直接使用个人 GitHub public repo 链接。

由于硬件模拟时间不足，本轮不要求真实硬件/网络 testbed。应集中补齐以下六条 P0 根因修复。

---

## 1. P0-A：重建 authorization lattice，使其数学上闭合

### 目标

不要把 `defer` / `reject` 强行放进 authorization lattice。将 receiver authorization 定义为 capability-set lattice，将 admission/scheduling outcome 与 authorization state 分开。

### 要求

定义 receiver capability set：

```text
C = {
  observe,
  plan,
  verify_enqueue,
  reserve,
  prepare_action,
  execute,
  propagate
}
```

authorization element 是 `2^C` 的子集。偏序：

```text
a1 <= a2 iff a1 subset-of a2
meet(a1, a2) = intersection
join(a1, a2) = union
```

将当前动作语义拆分为两层：

| 层 | 元素 | 说明 |
|---|---|---|
| admission/scheduling | reject | terminal discard，不进入 authorization lattice |
| admission/scheduling | defer | 保留未来服务机会，不进入 authorization lattice |
| authorization | informational-only | `{observe}` |
| authorization | verify-first | `{observe, verify_enqueue}`，结果到达前不释放执行/预留/传播权限 |
| authorization | actionable variants | `{observe, plan, reserve, prepare_action, execute, propagate}` 的若干可行子集 |

### Codex 需交付文件

- `docs/AUTHORIZATION_LATTICE.md`
- `scripts/check_authorization_lattice.py`
- `results/authorization_lattice_check.json`
- 如果论文源文件在仓库中存在：同步修改 method/theory 相关段落与图注。

### 验收标准

- 自动枚举 lattice elements，验证任意两个 authorization elements 有唯一 meet/join；
- 文档明确说明 `defer` 和 `reject` 是 admission/scheduling outcomes，不是 authorization lattice elements；
- “minimum sufficient authorization”定义为 capability-set 中满足 receiver progress constraint 的最小元素，并说明不可唯一时的 tie-break rule；
- 所有正文/README/docs 中不再混用 “five-label lattice” 这种数学上危险的表述；
- 若仍保留 “lattice” 术语，必须有 Hasse diagram 或等价清晰图示。

---

## 2. P0-B：把 CLPD score 与 drift-plus-penalty 推导逐项闭合

### 目标

将 CLPD 从“受 primal-dual 启发的 heuristic score”改成可以逐项追溯到 Lyapunov drift-plus-penalty 的在线控制器。若某些项不能从推导产生，必须明确为 engineering tie-breaker，并在理论保证中排除或有界处理。

### 要求

重新整理单时隙问题：

```text
max over x[i,a,t] in {0,1}:
  sum_i,a x[i,a,t] * [
    V * utility_hat[i,a,t]
    - Q_F(t) * fce_hat[i,a,t]
    - Q_D(t) * debt_hat[i,a,t]
    + Q_P(t) * progress_hat[i,a,t]
    - Q_V(t) * verifier_cost_hat[i,a,t]
    - Q_B(t) * packet_or_resource_cost_hat[i,a,t]
  ]
```

约束至少包括：

- 每个 message-receiver pair 至多选一个 action；
- packet budget；
- verifier budget；
- resource/actionability budget；
- defer/reject 的 queue/backlog 或 terminal 语义。

### Codex 需交付文件

- `docs/CLPD_DPP_DERIVATION.md`
- `docs/CLPD_SCORE_MAPPING_TABLE.md`
- `scripts/audit_clpd_score_mapping.py`
- `results/clpd_score_mapping_audit.json`
- 如能实现 exact per-slot solver：`scripts/solve_clpd_slot_exact.py`
- 如继续使用 greedy：`docs/CLPD_GREEDY_GAP_BOUND.md`

### 验收标准

- P1 中每个权重、约束、queue 与 CLPD 实现中的每个 score 项都有一对一映射；
- 明确 bounded increment、外生网络状态、内生 queue state、Slater/feasibility 条件；
- 给出标准 tradeoff：`O(1/V)` objective gap 与 `O(V)` queue/backlog，或明确说明当前只给经验控制器、不声称完整理论保证；
- 多维预算 admission 的解法不能再只用未受控的 `Gamma` 吸收误差；
- 若用 greedy，必须报告 empirical oracle gap，最好在小 slot 上用 exact solver 对照；
- projection error 若按 pair 累积，必须写成 `K * epsilon` 或说明归一化条件。

---

## 3. P0-C：新增软件级 receiver authorization intervention，不做硬件模拟

### 目标

在无需真实硬件或复杂网络 testbed 的前提下，直接验证不同 authorization labels 是否改变真实 receiver-agent 行为。这个实验是替代硬件模拟的关键根因修复。

### 实验范围

使用 held-out claims，优先覆盖：

- high false risk；
- high fanout；
- high irreversibility；
- high utility-if-true；
- verifier-scarce / delay-high regimes；
- planner / executor / verifier / network-controller 四类 role。

### 干预条件

同一 claim-role pair 至少运行：

- informational-only；
- verify-first；
- actionable；
- defer；
- reject。

### 软件环境

不要求真实硬件。使用 deterministic tool stubs 或 lightweight service stubs：

- reservation API stub；
- route planner stub；
- handover scheduler stub；
- cache update stub；
- verifier queue stub；
- downstream message stub；
- execution attempt stub。

### 必须记录的真实 outcome

- tool calls；
- plan changes；
- resource reservations；
- downstream messages；
- verifier enqueue；
- verification completion；
- propagation；
- execution attempt；
- wrong execution；
- wasted reservation；
- true task progress；
- rollback/repair cost；
- deadline miss。

### Codex 需交付文件

- `experiments/intervention/run_receiver_intervention.py`
- `experiments/intervention/tool_stubs.py`
- `experiments/intervention/intervention_config.yaml`
- `data/intervention_logs.jsonl.gz`
- `results/intervention_effects.csv`
- `results/intervention_state_confusion_matrix.csv`
- `results/replay_validity_calibration.csv`
- `docs/AUTHORIZATION_INTERVENTION_AUDIT.md`

### 验收标准

- 同一 held-out item 在不同 authorization labels 下重新运行 receiver agent 或 receiver policy，不只是读取已有 replay event；
- 每个 condition 有固定 seed，顺序随机化，state 隔离；
- 报告 ATE：`actionable - informational`、`verify-first - informational`、`defer - actionable`；
- 报告 95% CI，cluster 单位为 source claim；
- 报告 replay predictor 对真实 transition 的 precision / recall / calibration / Brier score / confusion matrix；
- 若 intervention 结果不支持当前 replay dynamics，必须指出需要改 replay model，而不是只改措辞。

---

## 4. P0-D：让 verify-first / reject 成为可观测机制

### 目标

当前 CLPD anchor 没有激活 verify-first / reject。必须修复机制或诚实收缩贡献。优先选择修复机制。

### 机制要求

#### verify-first

verify-first 应定义为 delayed conditional authorization：

1. 当前 slot 允许 `{observe, verify_enqueue}`；
2. 不释放 reserve/execute/propagate；
3. verifier queue 增加；
4. verifier result 到达后：true 则 release 到 informational/actionable；false 则 terminal reject；
5. progress reward 延迟计入，FCE 显著削减，queue cost 显式体现。

#### reject

reject 应定义为 terminal budget-saving action：

- 不进入未来 backlog；
- 节省未来 packet/verifier/resource；
- 承担 missed-opportunity cost；
- 与 defer 明确区分：defer 保留未来服务机会，reject 终止服务。

### Codex 需交付文件

- `docs/VERIFY_FIRST_REJECT_MECHANISM.md`
- `results/action_activation_by_stress.csv`
- `results/verify_first_release_trace.csv`
- `results/reject_vs_defer_tradeoff.csv`
- `docs/VERIFY_REJECT_ACTIVATION_AUDIT.md`
- 对应图源文件：`results/fig_verify_reject_activation_source.csv`

### 验收标准

- verify-first 和 reject 在合理 stress/risk/utility 区间中非零激活；
- 按 estimated false risk、utility-if-true、feedback delay、verifier capacity、fanout 分桶报告激活率；
- 至少给出若干 case studies，说明 verify-first 避免了高 FCE 或 reject 节省了无效服务；
- 若合理调参后仍不激活，必须把主文中的五类动作贡献降级为 extensible action interface，而不是继续宣称主机制已验证。

---

## 5. P0-E：重做 baseline、Pareto 与 clustered statistics

### 目标

摘要和主结果不再依赖“对多个 selected baseline configs 求平均”作为唯一胜利口径。要让强审稿人看到 CLPD 相对 closest / best / Pareto baselines 的真实位置。

### Codex 需交付文件

- `scripts/bootstrap_by_source_claim.py`
- `scripts/build_matched_baseline_table.py`
- `scripts/build_pareto_frontier.py`
- `results/matched_baseline_table.csv`
- `results/pareto_frontier.csv`
- `results/clustered_bootstrap_ci.csv`
- `docs/STATISTICAL_AUDIT.md`

### 主表必须包含

- CLPD anchor；
- closest matched C-CPB+Prog；
- mean selected C-CPB+Prog operating region；
- best-FCE baseline；
- best-progress baseline；
- best-debt baseline；
- Pareto frontier membership；
- relative differences；
- source-claim clustered 95% CI；
- p 值可选，但 effect size 与 CI 必须有。

### 验收标准

- bootstrap cluster 单位必须是 source claim，而不是 replay event；
- 报告 ID / OOD-template / OOD-network 分层结果；
- 摘要数字必须能从 `matched_baseline_table.csv` 或 `clustered_bootstrap_ci.csv` 直接追溯；
- 不再使用 “strongest baseline” 除非确实在 matched/Pareto 口径下成立；
- 若 CLPD 主要优势是 withheld ratio，而不是 FCE/progress/debt，也必须诚实写出。

---

## 6. P0-F：artifact 一键复现与双盲发布规范

### 目标

将 artifact 从“文档可追溯”提升为“fresh clone 后一条命令复现主表/主图/审计结果”。

### Codex 需交付文件

- `Makefile` 或 `scripts/run_all_audits.py`
- `environment.yml` 或 `requirements.txt`
- `docs/REPRODUCIBILITY.md` 更新版
- `docs/RELEASE_MANIFEST.tsv` 更新版
- `docs/SHA256SUMS.txt` 更新版
- `docs/ANONYMITY_EXTERNAL_RELEASE_CHECK.md`

### 一键命令要求

至少支持：

```bash
python scripts/run_all_audits.py --root . --out results_reproduced
```

或：

```bash
make reproduce-all
```

该命令应顺序执行：

1. schema validation；
2. dataset audit；
3. network-service replay audit；
4. CLPD score mapping audit；
5. authorization lattice check；
6. intervention audit；
7. verify/reject activation audit；
8. baseline/Pareto/statistical audit；
9. figure/table regeneration；
10. anonymity check；
11. manifest/SHA check。

### 验收标准

- `docs/REPRODUCIBILITY.md` 中引用的每个脚本都真实存在；
- 不再出现“文档要求运行但 release 不包含脚本”的情况；
- 所有主结果 CSV/JSON 都能由一键命令再生，或明确标注为 frozen precomputed external output；
- 匿名提交不得直接使用个人 GitHub public repo 链接；
- 需要生成 anonymous ZIP 或匿名 mirror，并附外部匿名检查清单。

---

## 7. 不要求本轮完成的事项

由于时间不足，本轮不要求：

- 真实硬件部署；
- 真实硬件模拟；
- 大规模 Mininet/ns-3/Kubernetes testbed；
- 真实 WAN/edge cloud trace 采集；
- 新的大规模人工标注活动。

但不做硬件并不意味着放弃网络性。必须通过以下替代方式补强：

1. trace-driven service queue simulation；
2. verifier backlog / delay / capacity stress analysis；
3. receiver intervention with tool stubs；
4. source-claim clustered statistics；
5. exact or auditable online solver comparison；
6. artifact 一键复现。

---

## 8. 论文措辞原则

修复前不得继续使用以下高风险表达：

- “strongest baseline”；
- “validates five-label lattice”；
- “deployment trace”；
- “real distributed service”；
- “complete proof of CLPD”；
- “directly proves receiver behavior changes”。

推荐表达：

- “validation-selected C-CPB+Prog operating region”；
- “capability-set authorization lattice”；
- “controlled trace-replay benchmark”；
- “software-level receiver intervention with tool stubs”；
- “trace-driven network-service replay”；
- “empirical oracle-gap audit”；
- “source-claim clustered confidence intervals”。

---

## 9. 最小可接收完成标准

若时间有限，至少完成以下最小集：

1. `AUTHORIZATION_LATTICE.md` + lattice check；
2. `CLPD_SCORE_MAPPING_TABLE.md` + score mapping audit；
3. software receiver intervention 小样本实验；
4. verify-first/reject activation audit；
5. matched baseline + Pareto + clustered CI；
6. `run_all_audits.py`；
7. 匿名 ZIP/mirror 检查。

达到这七项后，论文才有机会从当前 Weak Reject / Borderline Reject 推进到 Borderline Accept 竞争区间。
