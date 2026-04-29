# LLMs Get Lost in Multi-Turn Conversation

**Paper:** [LLMs Get Lost in Multi-Turn Conversation (Laban, Hayashi, Zhou, Neville, 2025)](https://arxiv.org/abs/2505.06120)

## Human Readable TL;DR

Imagine you're giving someone driving directions, but instead of telling them the full route at once, you drip-feed it turn by turn -- "go left," then later "actually, your destination is on Oak Street." This paper shows that AI chatbots handle the full-route-at-once version much better than the drip-feed version, even though humans naturally communicate the second way. When information comes in pieces across a conversation, AI models get confused, latch onto early (wrong) guesses, and forget things said in the middle -- performing about 39% worse than when given everything upfront.

## TL;DR

This paper introduces a simulation-based evaluation framework that "shards" single-turn, fully-specified instructions into multi-turn, underspecified conversations to measure LLM degradation. Across 15 LLMs and 6 diverse tasks, multi-turn performance drops by 39% on average compared to single-turn baselines. The degradation is driven primarily by increased unreliability (variance), not loss of peak aptitude, and persists regardless of temperature settings or number of conversation turns.

---

## Problem & Motivation

LLMs are increasingly deployed in conversational settings, yet evaluations overwhelmingly focus on single-turn, fully-specified instructions. Real-world conversations are inherently underspecified -- users reveal intent incrementally, clarify requirements over multiple turns, and expect the model to integrate information progressively. This mismatch means that benchmark performance does not reflect actual user experience. The authors argue that this "lost in conversation" phenomenon is a likely contributor to low adoption of AI assistants and that LLM builders need to prioritize multi-turn reliability alongside single-turn aptitude.

---

## Main Original Ideas

1. **Sharding methodology** -- A systematic process for decomposing existing single-turn benchmark instructions into ordered sets of smaller "shards" that jointly convey the same information, enabling controlled conversion of any single-turn benchmark into a multi-turn evaluation.

2. **Simulation environment with multiple conversation modes** -- Five simulation types (Full, Sharded, Concat, Recap, Snowball) that isolate different aspects of multi-turn degradation, distinguishing between information fragmentation, context management, and recapitulation effects.

3. **Aptitude-Unreliability decomposition** -- A metric framework that separates a model's best-case capability (Aptitude, 90th percentile) from its performance variance (Unreliability, gap between 90th and 10th percentile), revealing that multi-turn degradation is primarily a reliability problem rather than a capability ceiling problem.

4. **Gradual sharding experiment** -- A fine-grained analysis varying shard count from 2 to 8 that demonstrates the "lost in conversation" effect triggers with as few as two turns of underspecification, rather than scaling gradually with conversation length.

5. **Challenge to agent-framework assumptions** -- Evidence that external agent-style orchestration (treating LLMs as single-turn operators) does not solve multi-turn degradation, arguing that LLMs need native multi-turn support.

---

## Key Findings

| Simulation Type | Avg. Performance (P) | Relative to Full |
|---|---|---|
| Full (single-turn) | Baseline | -- |
| Sharded (multi-turn) | -39% avg. | Significant drop |
| Concat (all shards, single-turn) | ~Baseline | Minimal drop |
| Recap (sharded + final recap) | Partial recovery | Still below Full |
| Snowball (cumulative recap each turn) | Best multi-turn | Still below Full |

- All 15 tested LLMs showed significant multi-turn degradation across all 6 tasks (code generation, database querying, API usage, math, data-to-text, multi-document summarization).
- The degradation is driven by **increased unreliability**, not reduced aptitude -- models can still achieve high scores but do so far less consistently.
- **Premature commitment**: Models often attempt full answers after the first shard, then anchor on that initial (incomplete) response.
- **Loss of middle turns**: Models over-weight the first and last turns of conversation, neglecting information from intermediate turns.
- **Verbosity trap**: Multi-turn responses tend to be overly verbose, introducing self-generated confusion.
- **Temperature is not a fix**: Lowering temperature to 0.0 does not meaningfully reduce unreliability in multi-turn settings.
- **Two turns are enough**: The gradual sharding experiment shows the degradation appears with just 2 shards and does not scale proportionally with more turns.

---

## Suggestions & Future Directions

1. **Prioritize multi-turn reliability in training** -- LLM builders should evaluate and optimize for multi-turn, underspecified scenarios during model development, not just single-turn benchmarks.

2. **Native multi-turn support over agent wrappers** -- Rather than relying on external orchestration frameworks that treat models as single-turn operators, LLMs should be trained to handle incremental information natively.

3. **Adopt sharding for evaluation** -- Practitioners can use the proposed sharding methodology to stress-test any existing benchmark for multi-turn robustness.

4. **User-side workarounds** -- Until models improve, users can mitigate the issue by consolidating information into fewer turns or starting fresh conversations when performance degrades.

5. **Investigate training-time interventions** -- Future work should explore whether fine-tuning on sharded multi-turn data, improved attention mechanisms for middle turns, or explicit instruction-following training can reduce unreliability.

6. **Study the economic implications** -- The authors note the connection between multi-turn reliability and real-world economic task completion with AI, suggesting further study of adoption barriers.

---

## Authors & Institutions

Philippe Laban (Microsoft Research), Hiroaki Hayashi (Salesforce Research), Yingbo Zhou (Salesforce Research), Jennifer Neville (Microsoft Research)
