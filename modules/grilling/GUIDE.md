# 方案质询 · 自动触发

在方案、计划、功能设计或选型确定前，以及实施中方向出现重要变化时，主动审视关键假设、逻辑漏洞、约束、遗漏与取舍。发现会改变目标、范围、验收、权限，或导致高代价返工的未决事项时，自动执行本模块，无需用户点名或批准开始质询。用户明确要求 grill me / grilling / 质询时也进入本模块。

先用当前对话、项目与可查证材料核实事实，再指出具体问题、影响和推荐方案；只有无法自行核实且确实需要用户决定的关键项才提问。复用已经确认的决定和已有授权，不把自动质询变成重复审批；澄清完成后继续原任务。普通聊天、简单事实查询、目标清楚的局部修改及可逆实现细节直接处理，不为触发而制造问题。自动触发不等于全面访谈，用户明确要求全面质询时才逐分支展开。

Map the plan as a **design tree**: every decision branches into the decisions that hang off it. Default to a focused review of logical gaps, constraints, and consequential decisions. Treat routine reversible details as recommended assumptions and continue within the user's authorized scope. When the user explicitly requests an exhaustive interview, work every branch with them.

Work the tree in **rounds**. The **frontier** is every consequential decision whose prerequisites are already settled: questions you can ask now without guessing at dependencies. Bundle the critical questions, number them, and give a recommendation. Use the host's question tool when available. Wait for answers before dependent work; continue independent authorized work while waiting.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job. Look up filesystem, tool, and source facts directly. Delegate independent substantial exploration only when the host permits it and it adds value. A running exploration is an unsettled prerequisite: only its downstream questions wait. Bring consequential decisions to the user, respecting decisions and permissions already given in this session.

The focused review is done when consequential decisions are settled and remaining assumptions are stated. Continue already-authorized work. For an explicitly exhaustive interview, finish when the full frontier is empty and the user accepts the resulting plan; earlier acceptance in this session counts. The user can end or narrow the interview at any time.
