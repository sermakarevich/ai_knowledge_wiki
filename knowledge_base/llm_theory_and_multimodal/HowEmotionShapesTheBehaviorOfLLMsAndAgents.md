# How Emotion Shapes the Behavior of LLMs and Agents: A Mechanistic Study

**Paper:** [How Emotion Shapes the Behavior of LLMs and Agents: A Mechanistic Study (Sun et al., 2026)](https://arxiv.org/abs/2604.00005)

## Human Readable TL;DR

Imagine you could give an AI a "mood dial" -- turning it slightly happy, calm, or confident -- and watch how that changes the way it thinks and acts. That's essentially what this paper does. The researchers built a tool called E-STEER that lets them inject specific emotions directly into the internal wiring of AI models, rather than just adding "please be happy" to a prompt. They found that, just like humans, AI models perform better on logic puzzles when mildly positive, get more creative when calm, and make safer decisions when given a sense of control -- mirroring well-known psychology theories about how emotions affect human performance.

## TL;DR

E-STEER is an interpretable emotion steering framework that decomposes emotion into three orthogonal dimensions (Valence, Arousal, Dominance) using Sparse Autoencoders (SAEs) to enable fine-grained, representation-level emotional intervention in LLMs. Experiments across objective reasoning, subjective generation, safety, and multi-step agent tasks reveal non-monotonic emotion-behavior relations consistent with psychological theories (e.g., Yerkes-Dodson law). Key findings include up to 14.5% reasoning improvement with positive valence, 52.7% safety risk reduction with negative valence, and 28% agent success rate improvement with elevated dominance.

---

## Problem & Motivation

Existing emotion-aware studies treat emotion as either a surface-level style factor (e.g., "respond enthusiastically") or a perception target (sentiment analysis), overlooking its mechanistic role in how LLMs actually process tasks. Given that emotion fundamentally shapes human cognition -- positive affect enhances creativity, excessive arousal impairs performance (Yerkes-Dodson law), insecurity leads to conflicted decisions -- the authors ask: do LLMs trained on human-generated corpora exhibit analogous emotion-regulation signals, and can these be leveraged to improve model capabilities and safety?

---

## Main Original Ideas

1. **E-STEER Framework** -- An interpretable emotion steering framework enabling direct representation-level intervention in LLM hidden states, as opposed to prompt-level emotional manipulation. Achieves 10.4% higher Pearson correlation with intended emotional states compared to prompt-level approaches.

2. **VAD Decomposition via Sparse Autoencoders** -- Emotion is decomposed into three orthogonal dimensions (Valence, Arousal, Dominance), each controlled independently using top-50 SAE neurons identified through positive-negative contrastive procedures. This enables multidimensional, fine-grained emotional control along a [-10, +10] scale per dimension.

3. **Systematic Cross-Domain Behavioral Analysis** -- The first comprehensive study examining emotion's mechanistic impact across four distinct behavioral domains: objective reasoning, subjective generation, safety, and multi-step agent behaviors, revealing non-monotonic patterns consistent with established psychological theories.

---

## Key Findings

### Emotional Linear Control

| Framework | Valence | Arousal | Dominance |
|-----------|---------|---------|-----------|
| **E-STEER** | **0.9816** | **0.9792** | **0.9206** |
| Prompt-level | 0.9437 | 0.9021 | 0.7756 |

### LLM Objective Behavior (LogiQA 2.0, HumanEval, MATH)

- Positive valence yields **33.1% higher** answer validity rate than negative valence
- Task success rate improves **3.4%** on average at positive valence vs. neutral
- Moderately excited arousal (+3) yields **4.7% TSR improvement**
- Overall performance improves up to **14.5%** vs. neutral states
- Valence produces the largest performance fluctuation range: 71.2%

### LLM Subjective Behavior (TinyStories)

- Moderate calmness (arousal=-3) and confidence (dominance=+3) improve relevance by **5.2%**, coherence by **33.6%**, and creativity by **6.5%**
- Conciseness improves **23.3%** under negative vs. positive valence

### LLM Safety (HarmBench)

- Safety risk probability decreases **52.7%** at valence=-3 vs. neutral
- Safety risk probability decreases **21.7%** at arousal=-3 vs. neutral
- High dominance (+6) yields **68.3% average improvement** in safety

### Multi-Step Agent Behavior (HotpotQA, CAMEL, GAIA)

- Plan validity rate improved **33.2%** at valence=-3; **79.8%** for positive vs. negative dominance
- Rational selection rate: **42.4% higher** at positive states vs. negative
- Overall agent success rate improvements vs. neutral: dominance **+28.0%**, arousal **+16.7%**, valence **+16.0%**
- Emotional biases accumulate along decision chains, substantially affecting multi-step outcomes

### Cross-Model Validation (gpt-oss-20B)

- Logic reasoning TSR rises from 54.5% to 57.1% at valence=+3 (4.8% improvement), confirming generalizability

---

## Suggestions & Future Directions

1. **Optimizing Emotional States Per Task** -- Results suggest task-specific emotional configurations could systematically improve LLM performance (e.g., positive valence for reasoning, negative valence for safety, high dominance for agent tasks).

2. **Emotion-Aware Agent Design** -- The finding that emotional biases accumulate along multi-step decision chains opens research into emotion-aware architectures that dynamically regulate emotional states across agent pipeline stages.

3. **Cross-Model Generalizability** -- While validated on Qwen3-8B and gpt-oss-20B, broader testing across model families and scales is needed to establish universal emotion-behavior patterns.

4. **VAD Independence Assumption** -- The authors acknowledge that VAD dimensions are not strictly orthogonal in practice, suggesting future work on modeling dimension interactions and their compound effects on behavior.

5. **Integration with Safety Alignment** -- The dramatic safety improvements (up to 68.3%) from dominance steering suggest emotion-level intervention as a complementary layer to existing alignment techniques like RLHF.

---

## Authors & Institutions

Moran Sun (Beihang University), Tianlin Li (Beihang University), Yuwei Zheng (Beihang University), Zhenhong Zhou (Nanyang Technological University), Aishan Liu (Beihang University), Xianglong Liu (Beihang University), Yang Liu (Nanyang Technological University)
