# What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by Task-Completion Metrics

**Paper:** [What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by Task-Completion Metrics (Liu, 2026)](https://arxiv.org/abs/2608.16370)

## Human Readable TL;DR

When an AI agent's conversation history gets too long, systems trim it — dropping old turns or summarizing them — to save space. Everyone checks whether the agent still finishes its tasks afterward, and usually it does, so compression looks "free." This paper shows that check is misleading: the agent often pays a hidden bill in extra work — re-asking the environment for information it used to remember — that never shows up in the pass/fail score. In one case a model's success rate didn't move at all while it tripled how much it had to re-query just to recover what was thrown away.

## TL;DR

The paper formalizes task completion as a projection that discards interaction cost, proves this makes completion-only evaluation non-identifiable with respect to cost, and demonstrates the gap empirically in a controlled tool-using environment (IRBench). Across three models and two task regimes, compressing context via a sliding window increases retrieval tool calls (state reacquisition) in 6/6 comparisons — 5/6 significant after Holm correction — while completion changes are non-significant in all six (p ≥ .125). A causal oracle intervention shows restoring externally-queryable dropped state (D*) removes most of the added retrieval, while retention interventions show *which* real state is kept barely matters (random ≈ hindsight-optimal selection) but *whether* it is valid content matters a great deal (fabricated content raises retrieval 57% over real content). An ALFWorld probe shows the effect is environment-dependent, not intrinsic to shortening context.

---

## Problem & Motivation

Long-horizon agents outgrow any context window, so production systems compress trajectories via summarization, sliding windows, or retrieval filters. The standard justification for a compression method is "task completion doesn't drop" — but completion is bounded by a fixed interaction horizon and can stay flat while the agent quietly spends more of that horizon re-fetching state it used to have for free. No prior work measures this reacquisition cost directly or manipulates state availability to establish it causally — evaluations of compression ask *what to keep*, *whether information survives*, *whether it's used*, or *aggregate cost/completion trade-offs*, but none asks what the agent does, and what it costs, when needed state is genuinely gone.

---

## Main Original Ideas

1. **Non-identifiability of completion-only evaluation (Proposition 1).** The full evaluation outcome of a context strategy is a triple Y = (completion, retrieval calls, execution calls). The completion-only projection discards the cost dimensions, so two conditions with materially different interaction costs can map to indistinguishable completion values — formalized, then realized empirically under intervention.
2. **A recoverability decomposition of the hidden cost.** Dropped state splits into externally queryable task state (**D** — recoverable by re-querying) and history-dependent state (**R** — not recoverable from any single query). Losing R inflates defensive re-querying of D — a "re-query loop" — which is why the added interaction under compression is almost entirely retrieval, not execution.
3. **Retention interventions as causal probes.** By manipulating what a retained digest contains — how much, which atoms, whether it's genuine — the paper separates three effects: fine-grained *selection* among real atoms barely matters (random selection matches an offline hindsight oracle); *content validity* matters a lot (replacing real state with fabricated state increases retrieval 57% while completion stays flat); and the content effect only becomes visible when the digest occupies a substantial share of the compacted context (a content × budget interaction).

---

## Key Findings

| Comparison | Completion Δ (p) | Retrieval Δ (p) |
|---|---|---|
| DeepSeek, High-IR, Full→Sliding 5× | −11pp (.25, n.s.) | +32.9 (.002) |
| Qwen, High-IR, Full→Sliding 5× | −9pp (.13, n.s.) | +2.9 (.088) |
| GPT-5.5, High-IR, Full→Sliding 5× | +5pp (1.0, n.s.) | +42.9 (.002) |
| DeepSeek, Low-IR | 0pp (n.s.) | +22.6 (.004) |
| Qwen, Low-IR | −6pp (.25, n.s.) | +5.3 (.023) |
| GPT-5.5, Low-IR | 0pp (n.s.) | +22.4 (.002) |

- Retrieval increases in 6/6 model–regime cells, significant in 5/6 after Holm–Bonferroni; completion changes are non-significant in all six.
- DeepSeek's completion only degrades significantly at the most aggressive 10× compression (p = .016) — the cost signal (retrieval, significant at 5×) is the earlier, more sensitive indicator.
- Restoring the queryable task graph (oracle D*) cuts retrieval nearly in half (72.9 → 35.8 tool calls) and recovers most of the completion gap (66% → 80%); restoring history-only state (R*) helps completion (+12pp) but leaves retrieval almost unchanged.
- An extractive, fact-preserving summary operator is near-lossless at the same 5× budget where sliding-window deletion degrades completion and triples retrieval — *what* survives compression matters more than the ratio.
- Fabricating the retained D-state content (vs. real content) raises retrieval by 57% at a loose digest budget while completion is statistically unchanged (p = .41) — the content effect vanishes at a tight budget where the digest is a small fraction of the window.
- In ALFWorld, where dropped state can be re-observed directly through ordinary interaction, the same sliding operator produces no retrieval surge at all — the reacquisition signature is environment-dependent.

---

## Suggestions & Future Directions

- Report interaction cost (decomposed into retrieval vs. execution) alongside completion whenever evaluating a context-compression strategy, not completion alone.
- Where tool semantics allow, use oracle/causal restoration of specific dropped state as a diagnostic for which state is actually costly to lose.
- Extend the protocol beyond two bounded, synthetic-adjacent environments (IRBench, ALFWorld) to open-ended, partially-observable long-horizon settings (e.g. WebArena, SWE-bench).
- Test additional operators (abstractive LLM summarizers, token-level compressors) and a wider horizon sweep — the 24-turn horizon and two operators (sliding, extractive summary) are acknowledged as bounded choices.
- The authors explicitly do not claim compression is harmful in general — the message is that completion alone cannot certify a compression strategy safe with respect to interaction cost.

---

## Authors & Institutions

Shuyu Liu (single author; institutional affiliation not stated in the extracted wiki pages).
