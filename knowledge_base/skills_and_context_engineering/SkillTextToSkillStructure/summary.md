# From Skill Text to Skill Structure: The Scheduling-Structural-Logical Representation for Agent Skills

**Paper:** [From Skill Text to Skill Structure: The Scheduling-Structural-Logical Representation for Agent Skills (Liang et al., 2026)](https://arxiv.org/abs/2604.24026)

## Human Readable TL;DR

Imagine a librarian who stores all recipes as freeform prose. Finding the right one, or checking if it's safe, is slow and error-prone. This paper is like redesigning that library so every recipe is stored with a clear index card: when to use it, what steps depend on what, and what ingredients (resources) it needs. AI assistants that can perform tasks ("skills") currently store those skills as plain text, which makes searching and safety-checking them hard. The authors propose a smarter three-part card system that makes skills much easier to find and audit -- and show it measurably improves both.

## TL;DR

The paper introduces the **Scheduling-Structural-Logical (SSL) representation**, a structured three-layer encoding for LLM agent skills that separates scheduling signals, scene-level execution structure, and logic-level action/resource evidence. Grounded in classical knowledge-representation theory (Memory Organization Packets, Script Theory, Conceptual Dependency), the authors build an LLM-based normalizer that converts free-text skill documents into SSL format. Evaluated on Skill Discovery and Risk Assessment tasks, SSL improves MRR from 0.573 → 0.707 and macro F1 from 0.744 → 0.787 respectively.

---

## Problem & Motivation

Current LLM agent frameworks store reusable skills as unstructured or lightly structured text documents. This creates two practical problems:

1. **Retrieval gap** -- embedding-based search over raw text conflates surface language with structural intent, degrading skill discovery.
2. **Safety gap** -- risk assessors cannot reliably extract what a skill does, what resources it touches, or when it triggers from prose alone.

Classical AI had formal representations (frames, scripts, conceptual dependency) but these were brittle and hand-crafted. The paper argues that LLMs can now automate the normalization step, making structured representations practical at scale.

---

## Main Original Ideas

1. **Scheduling-Structural-Logical (SSL) representation** -- A three-layer decomposition of a skill document: (i) scheduling signals that encode when/why the skill should be invoked, (ii) a scene-level structural graph of execution steps and their dependencies, and (iii) logic-level evidence capturing concrete actions, tool calls, and resource-use constraints.

2. **LLM-based normalizer** -- An LLM pipeline that reads a free-text skill document and outputs an SSL-structured object. This removes the need for manual curation and generalizes across skill knowledge bases.

3. **Grounding in classical knowledge-representation theory** -- The SSL layers are explicitly mapped to Memory Organization Packets (scheduling), Script Theory (structural scenes), and Conceptual Dependency (logical actions/resources), providing theoretical justification for the decomposition.

4. **Dual-task evaluation protocol** -- SSL is validated on two downstream tasks -- Skill Discovery (retrieval quality) and Risk Assessment (classification quality) -- showing that structure helps both finding and auditing skills.

---

## Key Findings

| Task | Metric | Baseline (text) | SSL | Delta |
|------|--------|-----------------|-----|-------|
| Skill Discovery | MRR | 0.573 | **0.707** | +0.134 |
| Risk Assessment | Macro F1 | 0.744 | **0.787** | +0.043 |

- Structured representations consistently outperform raw text on both retrieval and classification, confirming that structure captures signal that embeddings over prose miss.
- The LLM normalizer generalizes across skill types without task-specific fine-tuning.
- The three-layer decomposition is individually motivated by distinct cognitive/linguistic theories, each contributing to the final representation.

---

## Suggestions & Future Directions

1. **Security hardening** -- The authors call for enhanced mechanisms to prevent adversarial skill documents from bypassing the normalizer or risk assessor.
2. **Skill routing algorithms** -- Better selection among competing skills when multiple SSL entries match a query.
3. **Reasoning-model integration** -- Extending SSL compatibility with chain-of-thought and multi-step decomposition architectures.
4. **Cross-framework standardization** -- Unifying SSL with emerging skill knowledge bases (SkillNet, Skill-X, etc.) toward an interoperability standard.
5. **Scalability at corpus size** -- Evaluating normalizer quality and downstream gains on very large skill libraries.

---

## Authors & Institutions

Qiliang Liang, Hansi Wang, Zhong Liang, Yang Liu (affiliations not listed in preprint)
