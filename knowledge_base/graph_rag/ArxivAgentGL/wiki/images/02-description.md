**Figure summary (Ablation study — Figures 2a–d and 3a–b)**

**What it shows.** A set of training‑curve ablations for AgentGL(7B)‑GRPO on the NC benchmark, isolating the effect of each reward/strategy component: the coverage reward $r_{\text{cov}}(\tau)$ (2a–b), the CDR/RTT termination terms (2c–d), and Graph‑Conditioned Curriculum Learning (GCCL) in Stage 1 and Stage 2 (3a–b). Each subplot compares a full model against a version with one component removed.

**Axes.** All plots share a horizontal **Training Step** axis (roughly 0–80 for 2a, 2b, 3a and 0–60 for 2c, 2d, 3b). The vertical axes alternate between **search‑efficiency** metrics (#Valid GNS counts) and **quality** metrics (Training Reward / Train Reward). Figure 3 uses dual y‑axes, pairing Training Reward with #Valid GNS so convergence and search frequency can be read together.

**Trends.**
- *Without $r_{\text{cov}}$* (2a, 2b): valid‑GNS count collapses to near zero after a brief spike, and the reward plateaus at a suboptimal level — the agent stops searching. With $r_{\text{cov}}$, both metrics climb fast and stay high.
- *CDR/RTT* (2c, 2d): the model with both terms shows a steadily *decreasing* GNS count (i.e., fewer, more efficient searches) and a stable, higher reward; dropping either term (w/o CDR or w/o RTT) loses this efficiency gain and the curves become flatter or more oscillatory.
- *GCCL* (3a, 3b): with GCCL the reward curve rises smoothly and the GNS count settles at a low, stable value; without GCCL the reward oscillates and the GNS count stays higher/more erratic, i.e., slower and less stable convergence.

**Takeaway.** No single ablated component is sufficient: each reward term and the curriculum is needed to (i) keep the model searching productively rather than degenerating to zero searches, (ii) reduce the average number of search steps (≈20 %+ efficiency gain at the full method), and (iii) stabilize and speed up convergence. The full combination is what simultaneously preserves accuracy and improves search efficiency. (All numeric values read from the curves are approximate.)