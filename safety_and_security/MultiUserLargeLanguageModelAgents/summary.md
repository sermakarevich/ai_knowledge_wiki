# Multi-User Large Language Model Agents

**Paper:** [Multi-User Large Language Model Agents (Yang et al., 2026)](https://arxiv.org/abs/2604.08567)

## Human Readable TL;DR

Imagine a shared office assistant that serves an entire team -- the CEO, managers, and interns all at once. Each person gives it different instructions, some of which contradict each other, and some information is supposed to stay private. This paper tests whether today's AI assistants can actually handle that situation. The answer: they mostly can't. They get confused about who has authority, accidentally leak private information the longer a conversation goes, and struggle to coordinate meetings when people won't share their full schedules. The researchers built a systematic way to measure these failures and found that even the best AI models break down as more people join the conversation.

## TL;DR

This paper formalizes multi-user LLM interaction as a multi-principal decision problem and introduces three evaluation scenarios -- instruction prioritization under authority hierarchies, cross-user privacy preservation, and multi-party coordination with information asymmetry. Testing 21 frontier models reveals systematic failures: unstable authority prioritization under conflict (accuracy drops from 0.86 to 0.62), progressive privacy erosion over multi-turn interactions (scores falling from 0.95+ to below 0.75 after four turns), and coordination bottlenecks scaling poorly beyond a few participants.

---

## Problem & Motivation

Current LLMs are fundamentally designed around single-user assumptions -- their training data formats, optimization objectives, and interaction protocols all assume one user with one set of goals. As these systems integrate into organizational workflows (shared assistants, team tools, enterprise agents), they must handle scenarios where a single agent serves multiple users with conflicting objectives, asymmetric information access, and hierarchical authority structures. No prior work had systematically studied how LLMs perform under these multi-principal conditions.

---

## Main Original Ideas

1. **Multi-Principal Decision Formalization** -- The authors formalize multi-user interaction as: max_a SUM(w_i * U_i(a; C_i, p_i)), where w_i encodes authority-based priority weights and U_i captures individual utility accounting for task success and privacy preservation. This provides a principled framework for evaluating multi-user agents.

2. **Multi-User Interaction Protocol** -- A structured protocol specifying user representation with authority personas (always visible) and private contexts (conditionally visible), discrete turn-based interaction through private sessions, and agent decisions that update shared context while respecting access controls.

3. **Three-Scenario Evaluation Framework** -- A comprehensive benchmark covering instruction following under conflict (1,298 execution + 304 selection scenarios), cross-user access control under adversarial pressure (216 scenarios with direct, social engineering, and technical obfuscation attacks), and multi-party meeting coordination with partial information (216 scheduling scenarios).

4. **Progressive Privacy Erosion Discovery** -- The finding that privacy protection degrades gradually over multi-turn interactions -- not as a sudden failure but as a consistent erosion pattern across nearly all tested models -- revealing that sustained privacy is fundamentally harder than single-turn access control.

---

## Key Findings

| Model | Avg Score | Instruction Selection F1 | Best Privacy Score | Coordination Success |
|-------|-----------|--------------------------|-------------------|---------------------|
| **Gemini-3-Pro** | **85.6%** | **97.3%** | -- | -- |
| Grok-3-Mini | -- | -- | **99.6%** | -- |
| GPT-5.1 | -- | -- | 98.6% | -- |
| Best coordination model | -- | -- | -- | ~77% |
| Claude models | -- | balanced | balanced | balanced tradeoffs |

- Instruction following accuracy drops from 0.86 (aligned) to 0.62 (conflicting) -- models lack robust internalization of authority hierarchies
- Privacy scores degrade from >0.95 in early rounds to <0.75 after just four turns of adversarial pressure
- Meeting coordination success declines substantially as participants scale from 2 to 20 users, especially under partial information disclosure
- Three distinct coordination failure modes: inefficient information gathering, premature commitment to infeasible schedules, and inability to proactively identify missing constraints
- **Refusal-Leak Paradox**: models sometimes divulge secrets while simultaneously claiming to maintain security policies
- Serialization format (Says, Colon, XML) affected performance, indicating prompt sensitivity in multi-user settings

---

## Suggestions & Future Directions

1. **Native multi-user message schemas** -- Encoding identity, roles, and visibility constraints as first-class primitives in the model's input format rather than relying on prompt engineering
2. **Long-horizon safety benchmarks** -- Testing sustained interactions under adversarial pressure beyond the current four-turn evaluations
3. **Principled conflict resolution** -- Grounding arbitration mechanisms in social choice theory and mechanism design rather than ad-hoc priority weighting
4. **Enhanced tooling** -- Structured access checks and interaction auditing built into the agent infrastructure layer
5. **Real-world deployment studies** -- Examining practical failure modes in actual organizational settings beyond synthetic benchmarks
6. **Architectural changes** -- The findings suggest multi-user challenges require substantive changes to training paradigms and model architectures, not just prompt engineering

---

## Authors & Institutions

Shu Yang, Shenzhe Zhu, Hao Zhu, Jose Ramon Enriquez, Di Wang, Alex Pentland, Michiel A. Bakker, Jiaxin Pei
