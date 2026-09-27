# Demystifying Evals for AI Agents

**Paper:** [Demystifying Evals for AI Agents (Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe, 2026)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

## Human Readable TL;DR

Imagine releasing a new feature in your app without any automated tests -- you'd only find bugs when real users complain. AI agents have the same problem, but worse, because they can do so many different things. This article is a practical guide for building a "safety net" of automated checks for AI agents, covering what those checks should look like, how to score them, and how to go from zero tests to a full system. The punchline: teams that invest early in this testing infrastructure ship better agents faster, because every user-reported bug becomes a permanent automated check.

## TL;DR

This Anthropic engineering guide defines evaluation (eval) infrastructure for AI agents -- from terminology to a concrete 8-step roadmap. It classifies graders (code-based, model-based, human), agent types (coding, conversational, research, computer-use), and evaluation metrics (pass@k vs. pass^k). The core argument is that evaluation investment pays dividends immediately by converting failures into test cases, preventing regressions, and replacing guesswork with metrics. Practical advice: start with 20-50 tasks from real failures, prefer deterministic graders where possible, and always read transcripts to verify graders measure what you intend.

---

## Problem & Motivation

AI agents are harder to evaluate than classic LLM prompts because they take multi-step actions, use tools, modify state, and must adapt to dynamic environments. Without structured evals, teams operate reactively -- catching regressions only after users report them. Manual testing does not scale, and intuition breaks down as agents grow more complex. The article addresses how to build systematic, automated evaluation infrastructure from scratch.

---

## Main Original Ideas

1. **Eval taxonomy** -- A precise vocabulary for agent evaluation: task, trial, grader, transcript/trace, outcome, evaluation harness, agent scaffold, and evaluation suite. This shared language reduces ambiguity when teams reason about quality.

2. **Three grader tiers** -- Code-based graders (fast, deterministic, brittle), model-based graders (flexible, non-deterministic, expensive), and human graders (gold-standard, slow, costly). Each tier fills gaps the others cannot, and mixing them is the recommended pattern.

3. **Capability vs. regression evals** -- Capability evals start at low pass rates and target areas needing improvement; regression evals stay near 100% and guard against backsliding. Graduating a capability eval to regression status is a concrete milestone marking agent maturity.

4. **pass@k vs. pass^k** -- Two metrics that capture different quality dimensions. pass@k (probability at least one of k trials succeeds) rewards any-success; pass^k (probability all k trials succeed) rewards consistency. Tracking both exposes agents that can solve a task occasionally but not reliably.

5. **Agent-type-specific patterns** -- Coding agents favor deterministic graders (run tests, inspect state); conversational agents require multi-dimensional rubrics (state, turn count, tone); research agents need groundedness + coverage + source quality checks; computer-use agents must inspect UI state, file systems, and app configs.

6. **8-step roadmap: zero to one** -- A sequenced process: start early with real failures → manual-first → unambiguous tasks → balanced problem sets → isolated harness → thoughtful grader design → transcript review → saturation monitoring.

---

## Key Findings

| Metric | Value |
|---|---|
| SWE-Bench Verified pass rate (1 year) | 40% → >80% |
| Opus 4.5 CORE-Bench before/after fixes | 42% → 95% |
| Eval saturation threshold (SWE-Bench) | ~80% pass rate |

- Eval investment accelerates development rather than slowing it -- converted failures become permanent regression guards.
- No single method is sufficient: automated evals, production monitoring, A/B testing, user feedback, and manual review each catch different failure modes.
- Transcript review is essential for distinguishing genuine failures from grader misconfiguration.
- Shared state between trials introduces correlated failures unrelated to agent performance -- trial isolation is a hard requirement.
- Eval saturation (agent passes all solvable tasks) is a real risk; monitor for it and retire or extend the benchmark before it stops providing signal.

---

## Suggestions & Future Directions

1. **Multi-agent evals** -- As agents collaborate in networks, evaluation must capture inter-agent interactions, not just individual performance.
2. **Longer-horizon tasks** -- Current benchmarks are limited; the field needs evals for tasks spanning hours or days of autonomous work.
3. **Subjective quality** -- Research and creative agents produce outputs where ground truth is contested; better rubrics and multi-judge consensus are open research problems.
4. **Dedicated eval teams** -- Mature orgs should staff teams that own eval infrastructure while domain experts contribute tasks, mirroring how platform teams support unit test infrastructure.
5. **Benchmark retirement** -- Fields should actively retire saturated benchmarks (e.g., SWE-Bench Verified at >80%) and develop harder successors before the signal disappears.

---

## Authors & Institutions

Mikaela Grace (Anthropic), Jeremy Hadfield (Anthropic), Rodrigo Olivares (Anthropic), Jiri De Jonghe (Anthropic)
