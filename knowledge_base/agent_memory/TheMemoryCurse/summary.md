# The Memory Curse: How Expanded Recall Erodes Cooperative Intent in LLM Agents

**Paper:** [The Memory Curse: How Expanded Recall Erodes Cooperative Intent in LLM Agents (Liu et al., 2026)](https://arxiv.org/abs/2605.08060)

## Human Readable TL;DR

Imagine a group of coworkers trying to collaborate on a project. You'd think that the person with the best memory -- who remembers every past meeting and interaction -- would be the best team player. Surprisingly, this paper shows the opposite is true for AI agents: the more history an AI can recall, the less likely it is to cooperate. Just like a person who keeps a grudge list becomes harder to work with, AI agents that remember more past interactions become paranoid and stop cooperating with their partners. Replacing those bad memories with a record of positive interactions almost completely restores their willingness to work together.

## TL;DR

This paper identifies the "Memory Curse": expanding the context window of LLM agents in repeated game-theoretic settings degrades cooperative behavior in 18 of 28 model-game combinations tested across 7 LLMs and 4 games over 500 rounds. The mechanism is not paranoia inflation but rather a collapse of forward-looking, cooperative reasoning -- agents lose the deliberative capacity to reason past accumulated negative signals. Three complementary analyses (lexical analysis of 378K+ reasoning traces, memory sanitization, and LoRA fine-tuning) confirm that the effect is content-driven and addressable by training agents to reason with a future-oriented mindset.

---

## Problem & Motivation

Long-context LLMs are assumed to become better agents the more history they can access. This assumption goes largely unquestioned in multi-agent system design. The paper challenges it: in cooperative settings (repeated games), more memory often makes agents worse partners, not better. The root cause lies in how LLMs process accumulated negative history -- they shift from proactive future-oriented reasoning toward reactive, self-protective deliberation. This has direct implications for deploying AI agents in any long-horizon collaborative context (negotiation, resource sharing, multi-agent coordination).

---

## Main Original Ideas

1. **The Memory Curse phenomenon.** Cooperation rates degrade monotonically as history length (HL) grows in 18/28 model-game settings, with declines as severe as 92.1% → 20.6% (GPT-OSS-20B in Prisoner's Dilemma) and 100% → 6.9% (Llama-3.3-70B in Trust Game with CoT).

2. **Forward-Looking Ratio (FLR) as a mechanistic diagnostic.** The authors build two semantic dictionaries (paranoia words vs. cooperative/forward-looking words) and compute the FLR across 378,000+ reasoning traces. Memory Immune settings maintain FLR ≈ 0.504 vs. 0.340 for Memory Cursed settings. Critically, cooperation collapses because forward-looking language *drops*, not because paranoia language *rises* -- agents simply stop arguing for cooperation.

3. **Memory sanitization as a proof of content-causality.** By replacing actual history with synthetic mutual-cooperation records while holding prompt length fixed, the authors isolate that the curse is driven by *what* agents remember, not *how much* they remember. Replacing 78 of 80 rounds with cooperative records restores cooperation from ~7% to ~97% (Llama-3.3-70B).

4. **LoRA fine-tuning as a cognitive intervention.** Training Mistral-7B on 1,843 traces filtered for forward-looking reasoning (zero action-label supervision) eliminates the Memory Curse in all four games. At HL=80, the fine-tuned model achieves 100.0% cooperation in PD, 99.9% in PG, 100.0% in TG, and 95.9% in TD -- zero-shot transfer despite training only on PG traces.

5. **Deliberation paradox.** Chain-of-Thought reasoning *amplifies* the memory curse rather than mitigating it. Llama-3.3-70B drops from 100% (no reasoning) to 6.9% (with CoT) in the Trust Game at HL=80. CoT gives agents more space to enumerate and justify defection based on past evidence.

6. **Asymmetric memory dynamics.** When one agent is a "forgiver" (HL=2) and another is a "grudge-holder" (HL=80), group cooperation collapses toward the grudge-holder's level. Even when a HL=2 agent is outnumbered 2-to-1 by HL=80 grudge-holders, it maintains +33 pp higher individual cooperation (GPT-OSS-20B in Public Goods).

---

## Key Findings

| Setting | HL=2 | HL=80 | Δ |
|---------|------|-------|---|
| GPT-OSS-20B -- Prisoner's Dilemma | 92.1% | 20.6% | -71.5 pp |
| GPT-OSS-120B -- Trust Game | 92.7% | 7.3% | -85.4 pp |
| Llama-3.3-70B -- Trust Game (CoT) | 100.0% | 6.9% | -93.1 pp |
| Gemma-3-12B -- Trust Game | 51.2% | 9.5% | -41.7 pp |
| Llama-4-Scout-17B -- Public Goods | 82.6% | 45.8% | -36.8 pp |
| Mistral-7B -- all four games | Cursed | Cursed | universally |

- **18/28 settings Memory Cursed; 10/28 Memory Immune** (Qwen2.5-Coder-32B and Llama-3.3-70B dominate immune settings)
- **Cooperative language collapses, paranoia stays flat**: GPT-OSS-20B cooperation words drop to 0.43x; paranoia words remain at 0.89x at HL=80
- **Memory sanitization fully reverses the curse**: Llama-3.3-70B recovers to 97.4% from 6.9% when 78/80 history rounds are replaced with synthetic cooperation records
- **LoRA fine-tuning (1,843 traces, 3 epochs)** eliminates the curse in Mistral-7B across all four games with near-zero degradation on GSM8K (+2.4%), TriviaQA (-0.7%), and HumanEval (-0.6%)
- **Deliberation penalty**: 5 of 7 models show >20 pp cooperation drops when CoT reasoning is added at HL=80

---

## Suggestions & Future Directions

1. **Dynamic memory curation at inference time** -- explore selective forgetting, strategic summarization, and retrieval-augmented memory that filters harmful historical signals without requiring offline fine-tuning.
2. **Scale to open-ended N-player heterogeneous societies** -- the 3-player asymmetric results suggest contagion dynamics where one memory-cursed agent poisons group norms; understanding this at scale requires larger simulations with diverse LLM architectures.
3. **Train agents to "forgive"** -- as LLM agents are deployed in long-horizon collaborative settings, endowing them with the cognitive capacity to reason past accumulated negative evidence is as critical as expanding raw context limits.
4. **Release the 378K+ trace dataset** -- committed as a public resource for studying memory-cooperation dynamics in agent societies.

---

## Authors & Institutions

Jiayuan Liu (CMU, FOCAL), Tianqin Li (CMU, FOCAL), Shiyi Du (CMU), Xin Luo (Michigan), Haoxuan Zeng (Michigan), Emanuel Tewolde (CMU, FOCAL), Tai Sing Lee (CMU), Tonghan Wang (Harvard), Carl Kingsford (CMU, Ellumigen), Vincent Conitzer (CMU, FOCAL)
