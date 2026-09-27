# Is Grep All You Need? How Agent Harnesses Reshape Agentic Search

**Paper:** [Is Grep All You Need? How Agent Harnesses Reshape Agentic Search (Sen et al., 2026)](https://arxiv.org/abs/2605.15184)

## Human Readable TL;DR

Imagine you're hiring two assistants to find facts in a pile of old chat logs: one uses a highlighter to find exact words, the other reads for meaning. You'd assume the meaning-reader wins -- but it turns out the winner depends more on *how the office is organized* than on which assistant you hired. This paper shows that the framework wrapping an AI search tool (how results are handed back, how the AI is prompted) often matters more than whether you chose "exact-word search" vs. "smart semantic search."

## TL;DR

This paper conducts an empirical study comparing lexical (grep) and vector (semantic) retrieval across four agent harnesses (Chronos, Claude Code, Codex, Gemini CLI) on a 116-question LongMemEval subset. Grep consistently outperforms vector retrieval under inline tool delivery, but the gap reverses with file-based delivery on some harnesses. The key finding is that harness choice introduces accuracy variance comparable to swapping the retrieval method entirely -- the same Claude Opus 4.6 model reaches 93.1% under Chronos but only 76.7% under Claude Code.

---

## Problem & Motivation

LLM-based agentic systems increasingly rely on retrieval for long-context memory tasks, yet benchmarks typically evaluate retrieval in isolation. Three under-studied dimensions are: (1) how retrieval strategy interacts with agent orchestration, (2) how performance degrades as irrelevant context scales up, and (3) whether findings hold across heterogeneous harness architectures. The authors argue that treating retrieval and orchestration as independent design choices underestimates real-world variance.

---

## Main Original Ideas

1. **Retrieval-Harness Coupling** -- Accuracy is determined by the joint system of retrieval method + harness, not either in isolation. System prompts, tool descriptions, and result formatting all shape how the agent uses retrieved content.

2. **Inline vs. File-Based Tool Delivery** -- Inline delivery (results injected into context) favors grep; file-based delivery (results written to disk, agent reads them) eliminates grep's advantage on some harnesses and creates a brittle read-integrate-retry cycle that can collapse performance (e.g., Codex/GPT-5.4 grep drops from 93.1% to 55.2%).

3. **Non-Monotonic Noise Scaling** -- Accuracy does not decrease monotonically as irrelevant sessions are added; it peaks and dips at different session counts per harness, revealing harness-specific inductive biases rather than a universal retrieval property.

4. **Lexical Advantage on Verbatim-Span Tasks** -- LongMemEval rewards recovery of exact strings (dates, counts, preferences). Grep surfaces these without embedding bottlenecks, explaining its inline advantage -- but this advantage may not transfer to synthesis-heavy tasks.

---

## Key Findings

### Experiment 1: Inline Delivery (Retrieval × Harness)

| Harness | Model | Grep | Vector | Delta |
|---------|-------|------|--------|-------|
| Chronos | Gemini Flash-Lite | **86.2%** | 62.9% | +23.3 |
| Chronos | Opus 4.6 | **93.1%** | 83.6% | +9.5 |
| Claude Code | Opus 4.6 | **76.7%** | 75.0% | +1.7 |
| Claude Code | Haiku 4.5 | **55.2%** | 44.0% | +11.2 |

- Grep outperforms vector on **all** inline harness-model pairs.
- Chronos (custom, LangChain-based) achieves 83.6--93.1% with grep; provider CLIs peak lower.

### Experiment 1: File-Based Delivery

- Vector exceeds grep on **5 of 10** harness-model pairs -- inline advantage vanishes or reverses.
- Codex/GPT-5.4 programmatic grep collapses: 93.1% → 55.2%.

### Experiment 2: Context Scaling (Noise Sessions)

- **Chronos Opus**: accuracy peaks at s20 (90.5%), dips at s30 (85.3%), recovers at full haystack (89.7%) -- non-monotonic.
- **Claude Code**: consistently favors grep for both Opus and Haiku across all session counts.
- **Gemini CLI Pro**: consistently favors vector throughout -- a stable harness-level bias.
- Retriever ordering reverses as sessions scale for some harnesses, indicating no universal scale advantage for dense retrieval.

### Cross-Cutting Observations

- Weaker models (Haiku) show larger inline grep-vector gaps, suggesting they are less consistent at iterative query refinement.
- "Dense retrieval explores neighborhoods in embedding space; lexical retrieval exploits surface cues" -- neither dominates universally.

---

## Suggestions & Future Directions

1. **Joint optimization** -- Researchers and practitioners should treat retrieval method, harness, tool-calling architecture, and task type as jointly optimized dimensions rather than independent module choices.
2. **Benchmark reform** -- Reporting isolated retrieval metrics understates the variance introduced by agent scaffolding; benchmarks should report full harness configurations.
3. **Vendor migration caution** -- CLI stacks are not retrieval-interchangeable even with identical corpora; switching providers requires re-evaluating retrieval choices.
4. **Synthesis-heavy domains** -- Future work should test whether the inline grep advantage holds for tasks requiring paraphrase matching or semantic reasoning rather than verbatim span recovery.
5. **Context engineering as first-class concern** -- Tool result presentation (inline vs. file, formatting, prompt design) is itself a stress test of agent competence and should be treated as a tunable hyperparameter.

---

## Authors & Institutions

Sahil Sen, Akhil Kasturi, Elias Lumer, Anmol Gulati, Vamse Kumar Subbiah -- PricewaterhouseCoopers
