# The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement

**Paper:** [The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement](https://arxiv.org/abs/2609.11873)

## Human Readable TL;DR

Right now, humans are still the ones deciding what to fix in an AI system, building the tools to fix it, and checking whether the fix worked. This survey asks: what would it take for the AI itself to take over that whole loop — not just get a better answer, but get better at getting better? It maps 491 papers and 72 industrial systems onto a five-rung ladder of autonomy, shows a scoreboard (the Headroom-Closed Index) proving that interactive, tool-using agent work is the frontier's weakest spot, and concludes that nobody has built a system that closes the loop end to end yet — the best examples are still bounded prototypes with humans holding the safety switch.

## TL;DR

The paper defines recursive self-improvement (RSI) as an autonomous, closed loop in which an AI system identifies its own limitations, develops and validates improvements, and reuses the resulting capabilities to improve the improvement process itself — distinct from one-off optimization or ordinary continual learning. It organizes RSI into five autonomy levels (L1 execution → L2 strategy selection → L3 experience acquisition → L4 environment adaptation → L5 recursive inheritance) above a non-RSI baseline (B0: retry-and-forget), surveys these levels across four feedback regimes (science, embodied intelligence, software engineering, healthcare) plus six industrial case studies, and motivates the whole exercise with the Headroom-Closed Index (HCI): across 393 model-benchmark observations, advanced math (86.4) and graduate science (85.8) are nearly saturated while software engineering (52.6) and tool agents (39.9) still have the most room to grow. The verdict: L2 is the broadly demonstrated frontier, L3/L4 evidence is thin and domain-dependent, and end-to-end L5 — an AI-revised improver whose successors are verifiably better under matched, independently assessed budgets — exists only in bounded prototypes, guarded by three unresolved credibility checks (safe inheritance, autonomy attribution, reliable verification).

---

This is a rung-1, shallow read (~2 min). For the medium-depth pass (~10 min), see [[digest|the digest]]; for the plain-language version, see [[explainer]]; for a claims-vs-evidence critique, see [[critical_thinking]].
