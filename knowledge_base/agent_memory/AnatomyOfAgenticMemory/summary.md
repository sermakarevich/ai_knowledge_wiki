# Anatomy of Agentic Memory: Taxonomy and Empirical Analysis of Evaluation and System Limitations

**Paper:** [Anatomy of Agentic Memory: Taxonomy and Empirical Analysis of Evaluation and System Limitations (Jiang et al., 2026)](https://arxiv.org/abs/2602.19320)

## Human Readable TL;DR

Imagine you're testing a new filing cabinet (the AI's memory system) to see if it helps workers find documents faster. But the test keeps giving workers filing cabinets full of only 50 documents -- when the workers already have a desk big enough to hold 500 documents in front of them. Of course the cabinet doesn't help! This paper exposes that most current tests for AI memory systems are exactly this broken: the tests are too small, the scoring methods punish correct answers that use slightly different words, and the hidden costs of maintaining the memory (time, compute) are almost never measured. The paper maps out all the different types of AI memory systems that exist and then runs experiments to show where the whole field is going wrong in how it evaluates them.

## TL;DR

This survey introduces a structure-oriented taxonomy of Memory-Augmented Generation (MAG) systems for LLM agents, classifying them into four categories based on how memory is organized and manipulated. It then empirically exposes four critical bottlenecks undermining the field: (1) existing benchmarks are underscaled relative to modern context windows, causing "saturation" where external memory is structurally unnecessary; (2) lexical metrics (F1, BLEU) systematically diverge from semantic correctness; (3) performance is highly backbone-dependent, with open-weight models producing alarming format error rates; and (4) memory maintenance introduces substantial hidden latency and cost ("agency tax") that is rarely reported.

---

## Problem & Motivation

LLM agents are increasingly expected to operate across long time horizons, but fixed context windows prevent persistent state maintenance. Memory-Augmented Generation (MAG) systems emerged to address this, yet despite rapid architectural development -- from lightweight semantic stores to complex hierarchical graph memory -- the empirical foundations remain fragile:

- **Underscaled benchmarks:** Many widely-used benchmarks fit within modern context windows (128k+), meaning a brute-force full-context baseline beats or matches complex memory systems, obscuring any real benefit.
- **Metric misalignment:** F1 and BLEU reward verbatim overlap, penalizing abstractive or paraphrased but semantically correct answers.
- **Backbone dependence:** Reported gains depend heavily on which LLM is used as the backbone, with weaker open-weight models frequently producing malformed structured outputs that silently corrupt memory.
- **Ignored system costs:** Retrieval latency, memory update overhead, and throughput degradation are rarely measured, leaving an incomplete picture of practical viability.

---

## Main Original Ideas

1. **Structure-Oriented MAG Taxonomy.** A four-category classification of all major agentic memory architectures based on *how memory is organized*, not just what it stores. Categories: Lightweight Semantic, Entity-Centric and Personalized, Episodic and Reflective, and Structured and Hierarchical. Each has sub-types with representative systems mapped to them.

2. **Context Saturation Gap (Delta).** A formal metric defined as `Delta = Score_MAG - Score_FullContext`. A benchmark is only meaningful for evaluating agentic memory when Delta >> 0 -- i.e., when external memory provides a structural advantage the full-context baseline cannot replicate. This exposes whether a benchmark actually requires external memory or is trivially solvable without it.

3. **Saturation Risk Analysis of Existing Benchmarks.** Benchmarks are analyzed along three structural axes -- Volume (total token load), Interaction Depth (temporal structure), and Entity Diversity (relational complexity) -- to assign a theoretical saturation risk. Most popular benchmarks (HotpotQA, LoCoMo, LongMemEval-S, MemBench) score as high or moderate risk. Only LongMemEval-M (>1M tokens) is consistently low-risk.

4. **LLM-as-a-Judge Robustness Validation.** The paper shows that LLM-based semantic judges (gpt-4o-mini) produce stable system rankings across diverse grading rubrics, whereas F1-based rankings are unreliable and systematically wrong. This empirically validates LLM-as-a-judge as the preferred evaluation approach for MAG systems.

5. **Backbone Sensitivity and Silent Failure Characterization.** Open-weight models (e.g., Qwen-2.5-3B) exhibit dramatically higher format error rates during structured memory operations compared to API models, with some architectures jumping from ~18% errors (gpt-4o-mini) to ~30% (Qwen-2.5-3B). These "silent failures" corrupt long-term memory without raising exceptions.

6. **Agency Tax Measurement.** A decomposed latency model (T_read + T_gen + T_write) is applied across six representative MAG systems to quantify user-facing latency and offline construction cost. This makes visible the practical overhead that complex memory systems impose.

---

## Key Findings

### Benchmark Saturation Risk Summary

| Benchmark | Avg. Volume | Interaction Depth | Entity Diversity | Saturation Risk |
|---|---|---|---|---|
| HotpotQA | ~1k tokens | Single turn | Low | **High** (trivial for context window) |
| LoCoMo | ~20k tokens | 35 sessions | High | Moderate (requires reasoning) |
| LongMemEval-S | 103k tokens | 5 core abilities | High | Moderate (borderline) |
| **LongMemEval-M** | **>1M tokens** | 5 core abilities | High | **Low** (requires external memory) |
| MemBench | ~100k tokens | Fact/Reflection | Medium | **High** (fits in 128k window) |

### Metric Misalignment

- Abstractive systems like A-MEM rank highly under semantic judge (Rank 4) but poorly under F1 (0.116, Rank 5) because they do not reproduce verbatim content.
- SimpleMem achieves F1 of 0.268 despite semantic score <0.30 -- F1 rewards surface memorization, not reasoning.
- Two named failure modes: **Paraphrase Penalty** (correct but rephrased answers punished) and **Negation Trap** (high token overlap despite factual incorrectness).

### Backbone Sensitivity

- Nemori format error rate: 17.91% with gpt-4o-mini vs. 30.38% with Qwen-2.5-3B.
- Complex architectures (graph-based, episodic) are most vulnerable; append-only systems are relatively more robust.
- Malformed JSON during memory updates causes silent corruption of long-term state.

### System Latency (Agency Tax)

- SimpleMem and LOCOMO: sub-second user-facing latency.
- MAGMA: ~1.46 seconds per turn (balanced).
- MemoryOS: >32 seconds per turn -- impractical for interactive use.
- A-MEM offline construction: ~15 hours; Nemori: >7.04M tokens consumed for index construction.

---

## Suggestions & Future Directions

1. **Design saturation-aware benchmarks.** Future benchmarks must exceed modern context window limits (>1M tokens) and report the Context Saturation Gap (Delta) to confirm external memory is structurally necessary.

2. **Adopt LLM-as-a-judge as the primary metric.** Replace or supplement F1/BLEU with semantic judges validated for rubric robustness. Standardize grading protocols across the community to enable fair comparison.

3. **Build backbone-aware memory systems.** Integrate constrained decoding or validation layers for structured memory operations to prevent format-induced silent failures, especially when targeting open-weight models.

4. **Report system costs as first-class metrics.** Latency decomposition (T_read, T_gen, T_write), throughput under load, and offline construction cost should be mandatory in evaluation protocols.

5. **Develop adaptive memory schemas.** Static memory schemas degrade as domains evolve; future systems should support schema evolution to maintain long-term memory integrity without full reconstruction.

6. **Model maintenance throughput explicitly.** Asynchronous write pipelines and efficient consolidation mechanisms should be designed to prevent throughput collapse under sustained interaction load.

---

## Authors & Institutions

Dongming Jiang, Yi Li, Songtao Wei, Jinxin Yang, Dingyi Kang, Xu Hu, Feng Chen, Bingzhe Li (University of Texas at Dallas); Ayushi Kishore, Qiannan Li (University of California, Davis); Alysa Zhao (Texas A&M University). Corresponding author: Bingzhe Li.
