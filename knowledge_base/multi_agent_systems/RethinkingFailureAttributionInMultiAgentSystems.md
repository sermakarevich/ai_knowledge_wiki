# Rethinking Failure Attribution in Multi-Agent Systems: A Multi-Perspective Benchmark and Evaluation

**Paper:** [Rethinking Failure Attribution in Multi-Agent Systems: A Multi-Perspective Benchmark and Evaluation (In et al., 2026)](https://arxiv.org/abs/2603.25001v1)

## Human Readable TL;DR

Imagine a team of workers fails to complete a project. When you ask different managers what went wrong, each one points to a different mistake -- and each explanation actually makes sense. Previous research tried to find "the one true cause" of failures in AI team systems, and concluded that AI was bad at diagnosing problems. This paper shows that failures usually have multiple legitimate explanations depending on your perspective, and once you evaluate AI fairly -- by accepting multiple valid answers instead of demanding one "correct" one -- it turns out AI is actually quite good at figuring out what went wrong.

## TL;DR

This paper challenges the prevailing assumption that failure attribution in LLM-based multi-agent systems (MAS) is deterministic. The authors propose multi-perspective failure attribution, introduce MP-Bench -- a 289-instance benchmark with triple expert annotations capturing diverse causal perspectives -- and design a ranking-based evaluation protocol using nDCG and LLM-as-a-Judge reasoning assessment. Their experiments demonstrate that LLMs perform substantially better than random at failure attribution when evaluated under this multi-perspective paradigm, reversing prior findings from deterministic benchmarks like Who&When.

---

## Problem & Motivation

Existing MAS failure attribution benchmarks (Who&When, TracerTraj, Aegis) assume a single deterministic root cause for each failure. In practice, expert annotators disagree on the failure-inducing step in up to 60% of cases, because complex inter-agent dependencies and ambiguous execution trajectories admit multiple plausible causal explanations. This mismatch between deterministic evaluation and inherently multi-perspective reality led prior work to incorrectly conclude that LLMs are near-random at step-level failure attribution -- a conclusion the authors argue stems from flawed benchmark design rather than model limitations.

---

## Main Original Ideas

1. **Multi-Perspective Failure Attribution Paradigm** -- Rather than identifying a single deterministic failure step, the task is reformulated as producing a set of plausible failure-inducing steps with explicit rationales. Each attribution reflects a distinct analytical perspective, and multiple attributions can be simultaneously valid.

2. **MP-Bench Benchmark** -- The first benchmark designed for multi-perspective failure attribution, comprising 289 execution logs from 121 distinct MAS configurations (MAgenticOne and CaptainAgent), annotated independently by three rigorously screened expert annotators (346 total expert-hours). Annotations include binary failure labels, failure reasons, and ideal actions per step.

3. **Ranking-Based Evaluation Protocol** -- A new evaluation framework using consensus-rate rankings and nDCG@K metrics that replaces rigid classification-based evaluation. Steps are ranked by the fraction of annotators who labeled them as failure-inducing, aligning evaluation with practical debugging prioritization.

4. **Attribution Reasoning Evaluation** -- An LLM-as-a-Judge framework that assesses whether model-generated failure reasons and ideal actions align with consolidated human expert reasoning across four dimensions: reasoning alignment, faithfulness, coverage, and plausibility.

5. **Multi-LLM Collaboration for Attribution** -- The finding that combining LLMs from different model families yields complementary attribution perspectives and consistently outperforms repeated sampling from a single model.

---

## Key Findings

| Model | nDCG@5 Exp (Hand-Crafted) | nDCG@5 Exp (Automatic) | LLM-Judge Score (Hand-Crafted) | LLM-Judge Score (Automatic) |
|---|---|---|---|---|
| Random | 0.1275 | 0.3147 | -- | -- |
| GPT-4.1 | 0.4313 | 0.6755 | 7.63 | 7.78 |
| GPT-5.1 | 0.3747 | 0.7844 | 7.62 | 8.25 |
| o3-mini | 0.4367 | 0.3944 | 7.48 | 7.37 |
| **Claude-Sonnet-4.5** | **0.4397** | **0.7894** | **7.95** | **8.23** |
| Qwen3-8B | 0.2944 | 0.6681 | 6.11 | 6.54 |
| GPT-oss-120B | 0.4245 | 0.7030 | 7.51 | 7.92 |

- Stochastic sampling of LLMs naturally produces diverse failure attributions that mirror human annotator disagreement patterns
- All models substantially outperform random baselines under multi-perspective evaluation, contradicting prior claims of near-random LLM performance
- Claude-Sonnet-4.5 achieves the best overall performance across both failure attribution and reasoning quality
- Stronger reasoning models do not necessarily guarantee superior performance
- Sampling temperature above zero is critical; fully deterministic decoding constrains attribution diversity
- Multi-LLM systems (combining models from different families) consistently outperform single-LLM systems, with cross-family diversity driving the largest gains
- Increasing the number of samples (N=3 to N=10) leads to consistent performance improvements
- LLM-Judge scores exceed 7.0 across all configurations, indicating reliable reasoning quality
- Only 16.2% of failure steps achieve full annotator consensus; 56.1% are labeled by only one annotator

---

## Suggestions & Future Directions

1. **Domain Extension** -- The benchmark currently covers general-purpose assistant tasks. Future work should extend to specialized domains such as scientific research, software engineering, and creative tasks.

2. **Scale and Framework Diversity** -- The quality-first annotation approach limits benchmark size. Hybrid expert-automated annotation pipelines could improve scalability while maintaining quality. Incorporating a wider range of MAS frameworks beyond MAgenticOne and CaptainAgent is also needed.

3. **Practical Guidance for Practitioners** -- (a) Always aggregate attributions from multiple perspectives rather than relying on a single deterministic result; (b) set sampling temperature above zero; (c) combine LLMs from different model families for complementary perspectives; (d) increase the number of samples when higher reliability is required.

4. **Benchmark as Foundation** -- MP-Bench is positioned as a gold-standard foundation for validating future automated annotation methods and advancing multi-perspective failure attribution research.

---

## Authors & Institutions

Yeonjun In (KAIST), Md Mehrab Tanjim (Adobe Research), Jayakumar Subramanian (Adobe Research), Sungchul Kim (Adobe Research), Uttaran Bhattacharya (Adobe Research), Wonjoong Kim (KAIST), Sangwu Park (KAIST), Somdeb Sarkhel (Adobe Research), Chanyoung Park (KAIST)
