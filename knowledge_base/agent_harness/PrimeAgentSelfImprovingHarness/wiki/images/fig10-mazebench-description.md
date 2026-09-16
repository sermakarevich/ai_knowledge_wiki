**Figure 10 — MazeBench exploration vs. estimated token cost.**

*What it shows.* A set of three line plots (Unique States, Room Count, Gem Count) comparing how much of the maze environment each model explores as a function of the total token cost of the run. Each model is drawn twice: a **solid line with filled markers** for the *Prime Agent* harness and a **dotted line with open markers** for a *comparison* harness, with color/shape encoding the model (GLM‑5.2, Opus 5, GPT‑5.6 SOL).

*Axes.* Common x‑axis = estimated token cost in USD, roughly 0–45. y‑axes are the benchmark metrics: unique states (≈0–2500), room count (≈0–25), and gem count (≈0–5).

*Trends.*
- **Unique states:** exploration grows monotonically with cost. The GLM‑5.2 (green) Prime‑Agent curve rises steadily to the highest solid‑line value (~1500–2000 near 40–45 USD); GPT‑5.6 SOL (orange) Prime Agent is comparable or slightly lower, while the orange comparison (dotted) lags below it. Opus 5 (purple) stays flat for most of the budget then climbs sharply near the top.
- **Room count:** GPT‑5.6 SOL reaches the most rooms; its dotted comparison curve climbs to the ceiling (~25) by the high‑cost end, while its solid Prime‑Agent curve plateaus earlier at a mid value. GLM‑5.2 solid rises to a moderate count; Opus 5 solid jumps near the right edge.
- **Gem count:** all curves stay near zero until roughly 25–30 USD, then step up (gems are found late in exploration); Opus 5 solid and GPT‑5.6 SOL both reach the top (~4–5) at high cost.

*Takeaway.* For a given token budget the solid (Prime Agent) curves are at least as good as, and in several cases better than, the dotted comparison‑harness curves — i.e., Prime Agent yields comparable or greater exploration (states/rooms/gems) at lower or equal cost, demonstrating better cost‑efficiency of the self‑improving harness across models. Exact values should be read as approximate.