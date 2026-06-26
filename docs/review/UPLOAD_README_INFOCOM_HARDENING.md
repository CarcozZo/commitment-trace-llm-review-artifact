# 上传说明：INFOCOM hardening handoff package

本包包含两个面向 Codex 的文件：

1. `INFOCOM_ACCEPTANCE_HARDENING_PLAN_NO_HARDWARE.md`  
   接收导向改进方案。明确目标是 INFOCOM 接收，明确本轮不做真实硬件/大规模网络模拟，并给出六条 P0 根因修复路线：lattice、CLPD theory、software receiver intervention、verify/reject mechanism、matched/Pareto/CI、artifact reproducibility/anonymity。

2. `CODEX_REPLY_CHECKLIST.md`  
   Codex 完成任务后的强制回复清单。要求 Codex 每项工作绑定文件、命令、日志、指标、剩余风险，避免“已修复但不可审计”的交互。

推荐上传位置：

```text
docs/review/INFOCOM_ACCEPTANCE_HARDENING_PLAN_NO_HARDWARE.md
docs/review/CODEX_REPLY_CHECKLIST.md
```

推荐 Codex 任务标题：

```text
INFOCOM acceptance hardening without hardware testbed: theory, software intervention, matched baselines, CI, reproducibility
```

推荐 Codex 输出要求：

```text
Use docs/review/CODEX_REPLY_CHECKLIST.md as the mandatory completion-report template.
```
