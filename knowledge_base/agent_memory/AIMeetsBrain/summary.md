# AI Meets Brain: A Unified Survey on Memory Systems from Cognitive Neuroscience to Autonomous Agents

**Paper:** [AI Meets Brain: A Unified Survey on Memory Systems from Cognitive Neuroscience to Autonomous Agents (Liang et al., 2025)](https://arxiv.org/abs/2512.23343)

## Human Readable TL;DR

Think of how humans remember things: your brain has short-term memory (like a sticky note on your desk) and long-term memory (like a filing cabinet). AI systems like ChatGPT have a similar problem -- they forget everything after each conversation, like someone with severe amnesia. This survey compares how human brains manage memory with how AI systems try to do the same, and lays out a blueprint for building AI agents that can actually remember things across conversations, learn from past mistakes, and know who they are over time -- much like a person who accumulates wisdom with experience.

## TL;DR

This survey unifies memory research across cognitive neuroscience, LLMs, and autonomous agents. It proposes a shared taxonomy (episodic vs. semantic; inside-trail vs. cross-trail), systematically compares biological and artificial memory storage/management lifecycles, reviews benchmarks for agent memory evaluation, and addresses memory security threats. The work bridges the interdisciplinary gap between neuroscience and AI to guide the design of next-generation memory systems for autonomous agents.

---

## Problem & Motivation

LLMs are inherently stateless -- each inference is independent, preventing accumulation of experience, long-term context, or dynamic knowledge updates. Autonomous agents requiring long-horizon planning suffer particularly from this limitation. While cognitive neuroscience offers a rich theoretical basis for memory design, existing AI memory work is fragmented and siloed, failing to deeply integrate biological principles. This survey addresses the gap by providing a unified, cross-disciplinary framework.

---

## Main Original Ideas

1. **Progressive Memory Definition Trajectory** -- Memory is defined at three levels: cognitive neuroscience (dynamic neural process), LLMs (parametric / working / external), and agents (dynamic cognitive architecture enabling identity persistence and experiential accumulation). This progression builds a coherent conceptual bridge.

2. **Novel Agent Memory Taxonomy** -- Memory is classified along two orthogonal axes:
   - *Nature*: episodic (sequential interaction trajectories, "how-to") vs. semantic (factual knowledge, "what-is")
   - *Scope*: inside-trail (single trajectory, transient) vs. cross-trail (persistent across trajectories, generalizable)

3. **Comparative Storage Analysis** -- Biological storage (sensory-frontoparietal networks, hippocampus-neocortex) is mapped to artificial counterparts (context window for inside-trail, external memory banks for cross-trail). Formats range from natural language text and graphs to model parameters and latent vectors.

4. **Closed-Loop Memory Management Framework** -- A four-stage lifecycle (Extraction → Updating → Retrieval → Application) is analyzed in parallel for both biological systems and LLM agents, revealing structural analogies and gaps.

5. **Memory Security Analysis** -- First systematic treatment of agent memory security, covering extraction-based attacks (privacy leakage from RAG), poisoning-based attacks (backdoor injection), and a multi-layer defense taxonomy (retrieval-based, response-based, privacy-based).

6. **Agent Skills as Transferable Memory** -- Proposes composable, reusable "agent skills" (analogous to equipment in games) distilled from successful trajectories, enabling cross-agent knowledge transfer and reducing redundant learning.

---

## Key Findings

| Dimension | Cognitive Neuroscience | LLM Agents |
|-----------|----------------------|------------|
| Short-term storage | Sensory-frontoparietal network; persistent neural activity | Context window; dynamic context folding |
| Long-term storage | Hippocampus (index) + neocortex (storage) | External memory bank (vector DB, knowledge graph) |
| Memory format | Event-based units, cognitive maps | Text, graphs, parameters, latent vectors |
| Retrieval | Cue-triggered pattern completion + reconsolidation | Similarity-based (top-k) or multi-factor (recency, importance, reward) |
| Updating | Prediction-error-driven; differentiation + integration | Filter-based (inside-trail); selective merging + RL (cross-trail) |

- LLM parametric memory is static, prone to hallucination, costly to update.
- RAG (external memory) decouples computation from storage but introduces latency and retrieval noise.
- Experience-based reasoning (reflection, trajectory exemplars, skill libraries) significantly improves agent performance on complex tasks.
- Memory poisoning attacks via malicious RAG injection represent an under-studied but critical threat surface.
- Multimodal memory integration remains unsolved: semantic degradation, temporal alignment, and computational cost are open challenges.

---

## Suggestions & Future Directions

1. **Multimodal Memory Systems** -- Integrate text, image, audio, and video into coherent cross-modal memory representations; address semantic degradation and temporal alignment across modalities.
2. **Composable and Transferable Agent Skills** -- Build shared, domain-specific skill libraries that agents can acquire and compose, enabling generalization across heterogeneous architectures without relearning from scratch.
3. **Adaptive Memory Consolidation** -- Develop biologically-inspired consolidation mechanisms (analogous to hippocampal replay) that selectively strengthen important cross-trail memories over time.
4. **Memory Security Hardening** -- Advance detection of poisoned memory entries and design isolated private memory partitions for sensitive personal data in deployed agents.
5. **Unified Evaluation Benchmarks** -- Create benchmarks that jointly assess fidelity, dynamics, and generalization of both semantic and episodic agent memory in realistic long-horizon settings.

---

## Authors & Institutions

Jiafeng Liang, Hao Li, Chang Li, Jiaqi Zhou, Changkai Ji (Fudan University), Tao Ren (Peking University), Jinlan Fu, See-Kiong Ng (National University of Singapore), Xia Liang\*, Ming Liu\*, Bing Qin\* (Harbin Institute of Technology)

\* Corresponding authors
