**Figure 4 — Accuracy vs. Cost trade‑off (Pareto comparison).**

- **What it shows:** A 2‑D scatter/curve plot comparing *GraphPlanner* against four baseline routers (GraphRouter‑Single, RouterDC‑Single, Router‑R1‑Multi, R2‑Reasoner‑Multi) on the routing task, where the goal is to maximize accuracy while minimizing token cost. GraphPlanner is drawn as a connected frontier; the baselines are single points.

- **Axes:** X‑axis = **Acc (%)**, roughly 50–64. Y‑axis = **Cost**, roughly 100–600 (driven by input‑token usage).

- **Trends:**
  - The GraphPlanner curve is monotonic and convex: moving from one operating point to the next raises accuracy from the low‑50s to the high‑60s while cost climbs from ~100 to ~600, with the slope steepening sharply at the high‑accuracy end (diminishing returns — extra accuracy costs disproportionately more tokens).
  - Each curve point is labeled with a hyperparameter α (0.9 → 0.5 → 0.3 → 0.1 → 0.0), which acts as a knob trading cost for accuracy: high α gives the cheapest, least‑accurate point; low α gives the most accurate, most expensive point.
  - The four baseline routers sit as discrete points clustered in the lower‑accuracy, mid‑cost region (acc ≈ 52–54, cost ≈ 100–180), i.e., they offer only a single operating point each and do not sweep the trade‑off.

- **Takeaway:** GraphPlanner traces out a Pareto frontier that lies to the upper‑right of (or dominates) the baseline operating points, meaning it achieves higher accuracy at comparable cost — or lower cost at comparable accuracy — than both single‑round and multi‑round baseline routers. In short, it provides *more efficient* accuracy‑vs‑cost trade‑offs across the whole range rather than a single fixed operating point.