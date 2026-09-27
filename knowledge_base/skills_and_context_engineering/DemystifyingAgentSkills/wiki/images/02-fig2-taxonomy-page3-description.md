**Figure 2 — Technical summary**

**What it shows.** A three‑panel stacked‑bar chart comparing the *composition* of trajectory‑level failure/success labels (a 3‑category, 12‑mode taxonomy) across three experimental arms — **Raw**, **Workflow Memory**, and **Skill** — for each of six source‑trajectory mixtures (5s0f → 0s5f, i.e. varying success/failure ratio summing to 5).

**Axes.**
- *Y:* Number of trajectories (0–100; each bar ≈ 100).
- *X:* Trajectory mixture (the six s/f blends), repeated within each arm panel.
- *Stack segments (color groups):* **SC1 Guided success** (greens: skill‑, workflow‑, autonomous‑guided), **SC2 Execution & verification** (blues: logic, verify‑only, format/schema, infra, background‑service, shell corruption), **SC3 Invocation & budget** (red/orange: timeout/budget, misapplied guidance, capability/safety).

**Trends / composition by arm.**
- **Raw:** roughly half the bar is success (green), with a thick blue execution/verification band and a thin red top — i.e. many execution‑layer failures.
- **Workflow Memory:** success share drops somewhat, the blue band stays large, and the **red top (timeout/budget) is visibly thicker** than in Raw, reflecting retained verbose exploration / drift.
- **Skill:** the green (skill‑guided success) base is the most prominent, the blue execution‑failure band is comparatively thinner, and red is moderate — i.e. fewer execution‑layer failures and more guided successes.
- Across the six mixtures, bar heights stay ~constant (≈100), so the differences are in *composition*, not total counts.

**Takeaway.** Skills primarily *reduce execution‑layer (blue) failures* and shift outcomes toward *guided success*, whereas workflow memory preserves useful procedural evidence but at the cost of extra process noise and more timeout/budget (red) failures. The label mix is therefore arm‑dependent, not just a function of the underlying success/failure mixture of the source trajectories. (Exact per‑mode percentages are in Appendix Table 11.)