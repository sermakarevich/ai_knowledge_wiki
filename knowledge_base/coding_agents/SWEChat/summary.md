# SWE-chat: Coding Agent Interactions From Real Users in the Wild

**Paper:** [SWE-chat: Coding Agent Interactions From Real Users in the Wild (Baumann et al., 2026)](https://arxiv.org/abs/2604.20779)

## Human Readable TL;DR

Imagine you hired an assistant to help you write documents, but instead of watching them work, you only see the final result -- and half of what they wrote still needs to be thrown away or rewritten. This study is the first large-scale look at how real programmers actually use AI coding helpers day-to-day, not in lab tests. It finds that when people let the AI do nearly everything ("vibe coding"), it produces buggier, more expensive code than when human and AI collaborate closely. The research is a wake-up call: AI coding agents are getting more autonomous faster than they're getting safer.

## TL;DR

SWE-chat is the first large-scale dataset of real-world AI coding agent sessions, containing 6,000 sessions, 63,000+ user prompts, and 355,000+ tool calls collected from open-source developers. The study finds a bimodal usage pattern -- 41% full agent autonomy ("vibe coding") vs. 23% human-only -- and quantifies that only 44.3% of agent-produced code survives into commits. Critically, vibe coding introduces ~9× more security vulnerabilities per 1K lines than human-authored code, while users push back or interrupt agents in 44% of turns, revealing a dangerous autonomy-oversight gap.

---

## Problem & Motivation

Existing coding agent benchmarks (SWE-bench, etc.) evaluate agents on curated, single-turn tasks with clean ground truth. This misses the messy reality: developers use agents in iterative multi-turn sessions, frequently redirect them, and often discard their output. There is no large-scale empirical study of how agents are actually used in the wild -- what users ask for, how often agents fail, how much of their code is kept, and what security risks they introduce.

---

## Main Original Ideas

1. **SWE-chat Dataset** -- First dataset combining complete agent interaction traces with line-level human vs. agent code attribution. 6,000 sessions across 200+ repos, 2.7M logged events from 5 agents (Claude Code ~85%, OpenCode, Gemini CLI, Cursor, Factory AI Droid). Continuously growing via an automated pipeline.

2. **Bimodal Coding Taxonomy** -- Three empirically derived usage modes: *vibe coding* (40.8%, agent writes >99% of committed code), *collaborative* (36.5%, mixed authorship), *human-only* (22.7%, agent assists without writing code). Vibe coding share doubled from 20% to 40%+ during the 3-month observation window.

3. **Code Survival Rate as Efficiency Metric** -- Introduces the fraction of agent-produced code that survives into user commits as a ground-truth efficiency signal. Overall: 44.3%; collaborative: 38.2%; vibe coding: 59.0% (higher acceptance but at 3× the token cost).

4. **Autonomy-Oversight Asymmetry** -- Quantifies the mismatch: agents ask clarifying questions in only 1.1--2.6% of turns, yet users push back or interrupt in 44% of turns. Users are actively compensating for agents that never ask for guidance.

5. **Security Vulnerability Quantification** -- Uses Semgrep to measure introduced vulnerabilities per 1,000 committed lines across coding modes. Vibe coding: 0.76 (path traversal, SQL injection, command injection); human-only: 0.08 -- a ~9.5× gap.

6. **LLM-Annotated Behavioral Taxonomy** -- Five annotation tasks applied at scale with human-validated LLM judges: session success (0-100), user persona (expert nitpicker, vague requester, mind changer), prompt intent, pushback type, and repository classification.

---

## Key Findings

| Metric | Vibe Coding | Collaborative | Human-Only |
|--------|------------|---------------|------------|
| Share of sessions | 40.8% | 36.5% | 22.7% |
| Code survival rate | 59.0% | 38.2% | -- |
| Tokens per 100 committed lines | 204K | ~68K | -- |
| Cost per 100 committed lines | $0.13 | $0.05 | $0.07 |
| Time per 100 committed lines | 12.6 min | 4.8 min | 8.6 min |
| Vulns per 1K committed lines | **0.76** | 0.14 | 0.08 |

- Most common user intent: understanding existing code (19%), not generating new code (13.4%)
- One-third of all agent tool calls are bash commands (primarily git operations)
- Expert nitpicker persona dominates -- users meticulously correct output while maintaining stable goals
- 90% of sessions score 50+/100 on success; most failures are early user interruptions
- 99.9th percentile turn duration exceeds 100 minutes -- agents run unsupervised for very long stretches
- Collaborative coding is the most cost- and time-efficient mode, despite the trend toward full autonomy

---

## Suggestions & Future Directions

1. **Realistic benchmarks** -- Shift evaluation from curated single-turn patches to multi-turn iterative tasks grounded in actual developer workflows, including agent-user correction cycles.
2. **Adaptive interaction design** -- Study pushback patterns at scale to redesign agent interfaces that solicit clarification and reduce user oversight burden.
3. **User simulators** -- Use complete interaction traces (prompts, corrections, persona labels) to train simulators for cheap offline evaluation, replacing costly human studies.
4. **Security interventions** -- SWE-chat provides a realistic testbed for evaluating secure fine-tuning, system-prompt hardening, and vulnerability-aware code generation.
5. **Longitudinal tracking** -- Continue data collection as agents improve to track whether efficiency gaps and security risks narrow or widen over time.
6. **Expand agent coverage** -- Current dataset is ~85% Claude Code; broader coverage of Cursor, Gemini CLI, and others would enable cross-agent comparisons.

---

## Authors & Institutions

Joachim Baumann, Vishakh Padmakumar, Xiang Li, John Yang, Diyi Yang, Sanmi Koyejo -- Stanford University (SALT-NLP Lab)
