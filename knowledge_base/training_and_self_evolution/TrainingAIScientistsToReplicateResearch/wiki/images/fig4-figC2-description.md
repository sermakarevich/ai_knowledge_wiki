**Figure 4 — "Frontier coding agents do not saturate Replica"** (two panels).

**What it shows.** The figure has two complementary views of how five agents (Qwen3.6‑27B, GLM‑5.2, Codex, Claude, and Faraday) perform on paper‑replication tasks. The left panel relates performance to the age of the paper being replicated; the right panel breaks performance down by research topic.

**Left panel (scatter + fit lines).**
- **X‑axis:** Publication year (≈1990–2025). **Y‑axis:** mean rubric score (≈0.3–1.0).
- Each point is the mean score for one paper in the train split, with point size encoding the number of tasks that paper yields; straight lines are least‑squares fits per agent.
- **Trend:** Every agent's fit line slopes downward — score falls as publication year increases, i.e. more recent papers are harder to replicate. An inset lists the per‑decade decline for each agent (all negative, on the order of a few points per decade), with Faraday's slope being the shallowest (smallest magnitude), so it degrades least with recency. The agents also start at different heights: Claude/Codex sit highest among the baselines, while Qwen's line is steepest.

**Right panel (categorical dot plot).**
- **Y‑axis:** research topics, grouped into a *Train* block (RL/Agents/Games, Automated AI Research, Sequence models, NLP & LLMs, Vision, Meta‑Learning, Optimisation & Training, Classic ML/Stats) and a *Test* block (Protein & Structural Bio, Climate/Weather/Earth, Materials & Chemistry).
- **X‑axis:** mean rubric score (≈0.3–0.95).
- **Trend:** Scores are spread across the range (some topics easier, e.g. classic ML/stats, some harder, e.g. NLP/LLMs), and the *Test* (AI‑for‑science) topics cluster at lower scores than most *Train* topics. Crucially, the green‑star marker (Faraday) is rightmost — highest score — on essentially every topic in both blocks.

**Takeaway.** Frontier coding agents do not saturate the Replica task space: performance is far from perfect and degrades with paper recency for all of them, with difficulty varying by domain and AI‑for‑science tasks being harder than ML tasks. Despite these difficulties, Faraday consistently outperforms the Claude and Codex baselines across topics and is the most robust to the recency effect.