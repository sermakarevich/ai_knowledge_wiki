**Figure 4 — "Harness Optimizer Search Progress."**

**What it shows.** The plot compares text-optimizer search algorithms on online text classification by tracking, over successive evaluations, the *best-so-far* search-set accuracy (step lines) together with the per-candidate accuracy of individual harnesses (scattered points). Two horizontal dotted lines mark the Few-shot and Zero-shot reference levels (roughly mid-30s %).

**Axes.** X-axis = number of Harness Evaluations (0–40); Y-axis = Best Performance (%), roughly 30–57%.

**Trends.**
- *Meta-Harness (red):* steepest early climb — to ~50% by ~5 evaluations and ~55% by ~8 — then a small late step to ~56–57% that holds to the end. It is the only curve that keeps rising after the initial jump and finishes highest.
- *TTT-Discover (cyan):* jumps early to ~42%, then a single step to ~45–46% near the 20th evaluation and plateaus.
- *Best-of-N (orange):* one early step to ~44% and then flat.
- *OpenEvolve (dark blue):* rises to ~40% early, with modest later steps to ~42–43% near 20 and ~40 evaluations.
- *ACE / GEPA (gray dashed):* essentially flat baselines in the ~40–41% band.
- The scattered candidate points span roughly 30–55%, with most mass in the 35–50% range, illustrating the variance around each method's best-so-far line.

**Takeaway.** Meta-Harness matches the *final* accuracy of OpenEvolve and TTT-Discover within the first ~4 evaluations and continues to improve thereafter, ultimately finishing more than ~10 points above every baseline — i.e., it both converges faster and reaches a higher ceiling.