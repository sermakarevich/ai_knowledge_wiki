**Figure 5 — ARC‑AGI‑3 test‑time scaling.** Two paired panels plot RHA E score (%) against two different "compute" axes, both on a log scale:

- **Panel A (left):** x‑axis = output tokens per game (roughly 10⁴ to 10⁶).
- **Panel B (right):** x‑axis = estimated API cost (roughly $10 to $10⁴).
- **y‑axis (both):** score %, linear from 0 to 100.

Each panel overlays five run‑curves (Prime Agent with Opus 5, GPT‑5.6 Sol, Terra, GLM 5.2, and Hermes Agent + GPT‑5.6 Sol) plus horizontal dashed reference lines marking the human baseline (~95%) and a few external ARC/Responses‑API baselines (roughly in the ~7–40% band).

**Trends.** The two strongest configurations (Opus 5, GPT‑5.6 Sol) climb steeply and roughly track each other, reaching the ~95% human‑baseline line on the order of a few hundred thousand output tokens / a few hundred dollars of cost. The mid‑tier model (Terra) gains a little and then plateaus around ~25% early. The two weakest (GLM 5.2, Hermes Agent) stay near the floor (single‑digit to low‑double‑digit percent). Cost scaling (right) mirrors token scaling (left), confirming the score gains are tied to spend rather than to a particular harness detail.

**Takeaway.** Additional output tokens and API cost are converted into score gains at sharply different rates per model: strong models keep improving across a long interaction horizon, while weak ones saturate quickly. This pattern is consistent with a model‑controlled interface that allows model‑dependent test‑time scaling instead of imposing one fixed workflow. The horizontal lines are external reference values (the authors' native‑harness reruns fell below published scores), so they situate the curves rather than isolate a causal harness effect.