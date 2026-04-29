# TRIZ Agents: A Multi-Agent LLM Approach for TRIZ-Based Innovation

**Paper:** [TRIZ Agents: A Multi-Agent LLM Approach for TRIZ-Based Innovation (Szczepanik & Chudziak, 2025)](https://arxiv.org/abs/2506.18783)

## Human Readable TL;DR

Imagine you need a team of specialists to solve a tricky engineering problem -- a mechanical engineer, an electrical engineer, a safety officer -- but you can't afford to hire them all. This paper builds that team out of AI chatbots, each playing one expert role, and has them collaborate using a tried-and-true invention recipe called TRIZ. The AI team was given a real problem (improving a gantry crane) and came up with solutions that matched what human engineers independently proposed, including the exact same "move fast but don't swing" dilemma and a matching control-system fix.

## TL;DR

The paper proposes "TRIZ Agents," a supervised multi-agent LLM system built with LangGraph and GPT-4o that automates the TRIZ (Theory of Inventive Problem Solving) methodology. A Project Manager agent orchestrates a team of specialized domain experts (mechanical, electrical, control systems, safety, operations engineers) plus a TRIZ Specialist equipped with RAG tools and a Contradiction Matrix lookup. Evaluated against a gantry crane case study, the system reproduced key intermediate TRIZ steps and converged on several solutions identical to those derived by human researchers, including the physical contradictions and a Sliding Mode Control solution.

---

## Problem & Motivation

TRIZ is a powerful structured innovation methodology but is rarely used outside specialist R&D labs because it demands deep interdisciplinary expertise, significant time, and experienced facilitators. Single LLMs applied to TRIZ struggle with the full complexity of multi-step workflows. The authors address this by distributing the problem across specialized collaborating agents, lowering the human-resource barrier to structured invention.

---

## Main Original Ideas

1. **Multi-Agent TRIZ Simulation** -- A supervised team of LLM agents, each profiled as a domain expert (or methodology specialist), collectively navigates all six TRIZ workflow steps. No prior system modeled a full end-to-end TRIZ process with an agent team.

2. **Supervised Agent Architecture via LangGraph** -- A Project Manager agent acts as orchestrator, dynamically deciding which specialist to invoke next and when to move to the next TRIZ step. Agents communicate entirely in natural language; AI messages are re-typed as "human" messages to simulate real conversation flow.

3. **TRIZ-Specific Tool Integration** -- The TRIZ Specialist agent is uniquely equipped with four tools: a 39-parameter feature list, a Contradiction Matrix lookup, an Inventive Principles reference, and a RAG tool over curated TRIZ literature -- grounding it beyond the LLM's parametric knowledge.

4. **Step-Level Documentation for Context Management** -- Instead of relying on a growing conversation history (which exceeds context windows), the Documentation Specialist agent writes a summary at the end of each step that is injected as context for the next step, enabling long workflows without context overflow.

---

## Key Findings

| TRIZ Step | Human Case Study | TRIZ Agents Output | Match Level |
|---|---|---|---|
| Engineering System | 8 components + supersystems | Most components, weak on supersystems | Partial |
| Function Analysis | Useful + harmful connections | Several overlapping connections | Partial |
| CECA (root causes) | "Excessive weight", "Fast speed" | "Overloading", "Rapid Movements" | Strong conceptual match |
| Engineering Contradiction | Object-generated harm vs. weight | Speed vs. Stability; Load vs. Safety | Conceptually close |
| Physical Contradiction | Move fast / slow; lift heavy / light | **Exact same two contradictions** | Exact match |
| Solutions | SMC antiswing + intelligent breaker | SMC antiswing + thermal management | Partial (missed breaker) |

- The TRIZ Specialist underutilized the RAG tool despite explicit prompting -- agents defaulted to web search or internal knowledge instead.
- The Project Manager selectively engaged multiple agents for creative steps (Function Analysis, Solutions) but single agents for formal/deterministic steps (Engineering Contradiction, Physical Contradiction).
- All six TRIZ workflow steps completed successfully across multiple non-deterministic runs.

---

## Suggestions & Future Directions

1. **Feedback loops** -- The current system is strictly sequential; adding iterative refinement (ability for the PM to send the team back to rethink a step) would better model real TRIZ practice.
2. **Long-term memory** -- For larger problems, explicit external memory stores beyond step-level summaries are needed to avoid context loss.
3. **Better RAG utilization** -- Prompt engineering needs refinement to reliably trigger specialized tools over general web search.
4. **Hierarchical agent teams** -- Organizing sub-teams (e.g., a hardware sub-team) under the main PM could improve specialization and scalability.
5. **Extend to other innovation methodologies** -- The same architecture could wrap Design Thinking, Lean Innovation, or DFSS workflows.
6. **Cognitive architecture augmentation** -- Integrating explicit reasoning flows and external grounding could yield more human-like decision-making.

---

## Authors & Institutions

Kamil Szczepanik, Jarosław A. Chudziak -- Institute of Computer Science, Warsaw University of Technology, Poland. Published at ICAART 2025 (17th International Conference on Agents and Artificial Intelligence).
