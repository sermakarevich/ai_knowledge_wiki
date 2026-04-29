# Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering

**Paper:** [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering (Li & Storhaug, 2026)](https://arxiv.org/abs/2604.01437)

## Human Readable TL;DR

Imagine reviewing chefs by only tasting their final dish -- you know who made something tasty, but you have no idea *why* one cook succeeded and another failed. That's how researchers currently judge AI "agents" (AI programs that think, act, and use tools on their own) that help with software engineering. This paper says we should record and share the agents' full cooking journey -- every thought, every action, every result -- so other researchers can learn from the process, reproduce the work cheaply, and understand what actually made an agent good or bad at its job.

## TL;DR

The authors surveyed 18 recent software engineering papers using Agentic AI and found widespread problems with reproducibility (missing LLM versions, temperatures, prompts), explainability (black-box outputs), and cost (expensive to re-run). They propose sharing agents' **Thought-Action-Result (TAR) trajectories** publicly, together with an LLM-based pipeline to automatically summarize and compare them. A proof-of-concept on CVE vulnerability-fix detection across three LLMs (Qwen3-235B, Llama-3.3-70B, Gemma-3-27B) shows this approach surfaces concrete behavioral differences -- e.g., Llama's advantage came from "analytical discipline," not deeper reasoning.

---

## Problem & Motivation

Agentic AI is exploding in software engineering research (ICSE papers with "agent" in the title jumped from 7 in 2025 to 30 in 2026), but evaluation practice has not kept up:

- **Black-box behavior:** LLM-powered agents produce results that are hard to justify or interpret.
- **Reproducibility gaps:** Papers frequently omit LLM versions, temperature, and prompt templates; LLM randomness compounds the issue.
- **Cost barriers:** Re-running commercial LLM-based evaluations to reproduce baselines is expensive.
- **Weak baselines:** Only 1 of 18 surveyed papers compared against an existing Agentic AI approach; most compare against classical techniques or naive prompting.
- **No systematic understanding:** Aggregate metrics hide *why* one agent succeeds where another fails.

As Agentic AI methods become default baselines for future studies, the field needs standardized evaluation practices that are reproducible, explainable, and efficient.

---

## Main Original Ideas

1. **Literature-grounded diagnosis of evaluation gaps.** A structured survey of 18 Agentic AI papers from ICSE 2025/2026, FSE 2025, ASE 2025, and ISSTA 2025 categorizes what is (and isn't) reported about approaches, baselines, ablations, explainability, reproducibility, and efficiency.

2. **TAR trajectory sharing as a first-class research artifact.** The authors argue that agents' Thought-Action-Result trajectories (or summarized versions) should be publicly released alongside code, enabling post-hoc analysis without re-running expensive LLM agents.

3. **Automated multi-step TAR analysis pipeline.** A three-stage LLM-based summarization workflow: (Step 1) summarize each run per agent, (Step 2) compare agents on the same run, (Step 3) aggregate comparisons across runs to extract recurring behavioral patterns. This turns qualitative behavior into structured, comparable findings.

4. **Concrete reproducibility checklist.** Standardize reporting of prompt templates, exact LLM versions, temperature settings, repetition counts, and cost/time metrics; use shared TAR trajectories of baselines instead of re-running them.

5. **Behavioral-pattern evaluation beyond accuracy.** Demonstrates that agent comparison can surface distinguishing traits like epistemic humility, tool-use discipline, and failure modes -- richer signal than a single accuracy number.

---

## Key Findings

### Literature survey (18 papers)

| Dimension | Finding |
|-----------|---------|
| Agent architecture | **11/18 multi-agent**, 7/18 single-agent |
| Baselines (Agentic AI vs. ...) | Classical methods: 6, Naive LLM prompting: several, Deep learning: 1, **Existing Agentic AI: only 1** |
| Ablation studies | 13/18 |
| Failure analyses | 6/18 |
| Case studies | 4/18 |
| Cost / efficiency analyses | 4/18 |
| Precise LLM versions reported | Few |
| Temperature sensitivity analyses | Some |

### Proof-of-concept case study (CVE vulnerability-fix detection)

Compared Qwen3-235B, Llama-3.3-70B-Instruct, and Gemma-3-27B on 10 runs where Qwen3 failed. Automated TAR analysis (via Kimi K2.5 Instant) surfaced:

- **What works consistently:** Llama-3.3-70B's "verify then analyze" discipline (check dates, versions, CVE metadata before code analysis); Gemma's structured tool use; Llama's error recovery.
- **What fails consistently:** Pattern matching on keyword overlap without functional validation (Qwen3 and Gemma); tool abandonment or hallucination on tool errors; Qwen3 getting stuck in infinite examination loops.
- **Behavioral patterns:** Llama shows epistemic humility and cross-checks evidence; Qwen/Gemma overconfident; all three struggle with architectural/data-flow reasoning and are misled by commit messages over actual code diffs.
- **Key differentiator:** "Analytical discipline over reasoning sophistication" -- Llama wins via strict verification protocols, not deeper chains of thought.

---

## Suggestions & Future Directions

1. **Publicly release TAR trajectories** (raw or summarized) as a standard research artifact for every Agentic AI paper.
2. **Standardize reporting** of LLM version, temperature, prompts, repetitions, and token/API costs.
3. **Use existing Agentic AI methods as baselines**, not only classical or naive-LLM baselines, to measure progress within the paradigm.
4. **Develop automated TAR-analysis tools** that scale qualitative comparison across many runs and agents.
5. **Adopt summarized trajectories as cheap proxies** for re-running baselines, lowering the cost of replication.
6. **Extend the literature analysis** beyond the 18-paper sample and beyond "agent"-in-title filtering for a more complete picture.

---

## Authors & Institutions

Jingyue Li, André Storhaug -- Norwegian University of Science and Technology, Trondheim, Norway.
