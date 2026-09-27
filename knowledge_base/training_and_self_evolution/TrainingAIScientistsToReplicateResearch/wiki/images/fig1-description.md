This is **Figure 1**, a schematic of a training pipeline rather than a data plot — there are no axes or trends; it depicts the components and data flow used to post‑train the agent *Faraday* on a task space called *Replica*. Approximate figures in the diagram: ~100 source papers (1990–2026) and ~310 generated tasks.

**Pipeline (the four numbered blocks + feedback loop):**

1. **Task construction (Replica task space).** A corpus of ~100 ML / AI‑for‑science papers is fed to Gemini, which redacts a results figure and its caption. Each redacted figure defines one replication task; together this yields ~310 tasks. Each task pairs a *task prompt* ("replicate this plot by running real experiments…") with the *original figure*, which is shown only to the judge.
2. **Agent rollout (Faraday with Codex as a tool).** The policy π_θ (Faraday) acts inside a container provisioned with the task, the paper PDF, useful libraries (Python, PyTorch, pdftotext), a Codex terminal, a GPU MIG slice (~1/7 of an H200), and internet access. Codex is used as a code‑writing tool.
3. **Per‑task rubric generator.** A Claude‑based model (Claude Code) writes a task‑specific grading rubric from a meta‑rubric.
4. **Rubric‑based judge.** A Codex‑based judge, given access to the rollout's container (generated figure, code, agent trace, and the gold plot), emits an overall reward *r* plus per‑turn credit weights.

**Feedback loop:** the reward and per‑turn weights drive a modified **GRPO** update, feeding back into the policy (block 2).

**Takeaway.** The figure illustrates a closed‑loop, rubric‑based RL recipe for long‑horizon, non‑verifiable tasks: auto‑generated per‑task rubrics + multi‑sample judge aggregation + turn‑level credit assignment supply a low‑noise reward signal, enabling stable GRPO post‑training of a ~27B coding‑agent‑as‑a‑tool (CAT) model that outperforms frontier models on figure‑replication tasks.