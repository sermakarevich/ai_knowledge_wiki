# Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets

**Paper:** [Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets (Tran & Kiela, 2025)](https://arxiv.org/abs/2604.02460)

## Human Readable TL;DR

Imagine you have a tough puzzle to solve. You could either give it to one smart person with a time limit, or split it among a team of people with the same total time. Many recent studies claimed the team approach works better -- but this paper shows the team only *seemed* better because they were secretly given more total time. When you give both approaches the exact same amount of "thinking time," the single smart person consistently does just as well or better. The team approach only starts winning when the single person is deliberately confused or distracted.

## TL;DR

This paper presents an information-theoretic argument (via the Data Processing Inequality) and controlled experiments showing that single-agent LLM systems (SAS) consistently match or outperform multi-agent systems (MAS) on multi-hop reasoning when thinking-token budgets are equalized. Across three model families (Qwen3, DeepSeek-R1-Distill-Llama, Gemini 2.5) and two benchmarks (FRAMES, MuSiQue), SAS is more information-efficient. The authors also identify significant measurement artifacts in API-based budget control and standard benchmarks that inflate MAS gains.

---

## Problem & Motivation

Multi-agent LLM architectures (debate, role-playing, planner-executor, tool-specialized swarms) report strong performance but typically consume far more tokens than single-agent baselines. Prior comparisons rarely normalize for this extra compute, making it impossible to tell whether MAS wins come from architectural advantages or simply from spending more reasoning tokens. This paper asks: *when computation is held constant, do multi-agent systems still outperform a single agent?* The answer matters because it determines whether the field should invest in complex multi-agent orchestration or focus on scaling single-agent reasoning.

---

## Main Original Ideas

1. **Information-Theoretic Framing via Data Processing Inequality (DPI)** -- The authors formalize the SAS-vs-MAS comparison using the DPI, arguing that splitting context across agents and communicating via generated text introduces a lossy bottleneck. Under a fixed token budget and perfect context utilization, a single agent with full context access is provably more information-efficient.

2. **Thinking-Token Budget Normalization** -- A controlled experimental framework that matches total reasoning tokens between SAS and MAS variants (Sequential, Subtask-Parallel, Parallel-Roles, Debate, Ensemble). This eliminates the confound of unequal compute that plagues prior MAS evaluations.

3. **Identification of Evaluation Artifacts** -- The paper uncovers two systematic artifacts that inflate MAS performance: (a) API-based budget control in Gemini 2.5 does not reliably cap internal thinking tokens, and (b) standard benchmarks are vulnerable to memorization, as shown by accuracy drops under deep semantic paraphrasing.

4. **Context Degradation Predictions** -- From the DPI framework, the authors derive a testable prediction: MAS should become competitive when a single agent's effective context utilization is impaired. They confirm this via masking, substitution, deletion, and distractor experiments.

---

## Key Findings

### Main Results (Table 1 averages across FRAMES & MuSiQue)

| Thinking Tokens | SAS   | SAS-L | Sequential | Subtask-Par. | Par.-Roles | Debate | Ensemble |
|-----------------|-------|-------|------------|--------------|------------|--------|----------|
| 100             | 0.290 | 0.337 | 0.364      | 0.322        | 0.363      | 0.370  | 0.280    |
| 500             | 0.390 | 0.366 | 0.376      | 0.342        | 0.365      | 0.380  | 0.310    |
| 1000            | **0.418** | 0.397 | 0.379  | 0.369        | 0.381      | 0.388  | 0.333    |
| 2000            | **0.421** | 0.420 | 0.389  | 0.383        | 0.398      | 0.403  | 0.372    |
| 5000            | **0.427** | 0.425 | 0.386  | 0.396        | 0.417      | 0.420  | 0.411    |
| 10000           | **0.426** | 0.424 | 0.387  | 0.399        | 0.423      | 0.420  | 0.420    |

- At very low budgets (100 tokens), MAS variants (Debate, Sequential) can outperform SAS because reasoning is ineffective and broader exploration helps
- From 1000+ tokens onward, SAS consistently leads or ties across all model families
- SAS is more token-efficient -- achieves comparable accuracy while consuming fewer thinking tokens
- Gemini-2.5-Pro is the strongest overall model; MuSiQue is the harder benchmark
- Performance saturates around 2000-5000 tokens with diminishing returns beyond
- SAS-L (longer thinking prompt) primarily benefits Gemini models, suggesting their thinking channel is underutilized with standard prompts
- Context degradation experiments confirm the DPI prediction: under masking (alpha=0.7) and substitution (alpha=0.7), MAS becomes competitive or surpasses SAS
- Deep semantic paraphrasing reduces accuracy for both SAS and MAS, exposing benchmark memorization vulnerabilities
- Error analysis shows SAS succeeds by staying anchored to the question, while Sequential MAS succeeds through broader exploration combined with late constraint checking

---

## Suggestions & Future Directions

1. **Focus on genuine MAS advantages** -- Future research should identify specific scenarios where multi-agent structures provide real architectural benefits beyond extra compute, such as tasks requiring genuine specialization or adversarial robustness.

2. **Control compute-context-coordination tradeoffs** -- The community needs standardized evaluation protocols that explicitly account for thinking tokens, visible context, and coordination overhead when comparing agent architectures.

3. **Improve benchmark robustness** -- Deep semantically-equivalent paraphrasing should be adopted to force models into genuine reasoning rather than exploiting memorized patterns from pretraining data.

4. **Investigate context utilization** -- Since MAS gains emerge primarily when context utilization is degraded, understanding and improving how single agents utilize long contexts could be more productive than adding multi-agent complexity.

5. **Standardize API budget control** -- The Gemini thinking-token distortions highlight the need for transparent and reliable compute metering in LLM APIs used for research.

---

## Authors & Institutions

Dat Tran (Stanford University), Douwe Kiela (Stanford University)
