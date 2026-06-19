# Agentic Code Reasoning

**Paper:** [Agentic Code Reasoning (Ugare & Chandra, 2026)](https://arxiv.org/abs/2603.01896)

## Human Readable TL;DR

Imagine you hire a detective to investigate whether two crime scene reports are actually describing the same event -- but the detective isn't allowed to visit the scene, only read documents. This paper teaches AI coding assistants to act like that detective: carefully reading code files, tracing through what would happen step-by-step, and reaching reliable conclusions *without ever running the code*. The trick is forcing the AI to write down every clue it finds and every reasoning step it takes, like filling out a formal case report, rather than just guessing. This structured approach makes the AI significantly more accurate at spotting bugs, comparing code changes, and answering tricky questions about how code behaves.

## TL;DR

The paper introduces **semi-formal reasoning**, a structured prompting methodology for LLM agents that requires explicit premise construction, execution path tracing, and formal conclusion derivation -- acting as a "certificate" that prevents unsubstantiated claims. Evaluated on patch equivalence verification, fault localization (Defects4J), and code Q&A (RubberDuckBench), semi-formal reasoning consistently outperforms unstructured chain-of-thought by 5--12 percentage points across all tasks, reaching 93% accuracy on real-world patch verification without any code execution.

---

## Problem & Motivation

LLM-based software engineering agents (SWE-agent, OpenHands, Agentless) rely heavily on *test execution* to validate code changes -- which requires expensive sandbox environments, dependency installation, and computational resources. For tasks like bug detection, code review, and patch verification, relevant context spans multiple files and intricate dependencies, yet fully formal verification (Lean, Coq) is impractical for arbitrary multi-language repositories.

Existing execution-free approaches (SWE-RM, CodeJudge, Agentic Rubrics) use *unstructured reasoning*, letting models make claims without explicit justification -- leading to unreliable conclusions. The gap: a method that is more rigorous than free-form chain-of-thought but far less overhead than full formal verification.

---

## Main Original Ideas

1. **Semi-formal Reasoning** -- A structured prompting technique that requires agents to (a) state explicit premises from gathered evidence, (b) trace execution paths interprocedurally, and (c) derive formal conclusions. The template acts as a certificate: every claim must be backed by a specific code location or evidence, preventing case-skipping or unsupported guesses.

2. **Agentic Code Reasoning as a Capability** -- Formalizes the notion that LLM agents can navigate repositories, trace dependencies, and perform deep semantic analysis without execution. Evaluated rigorously across three distinct tasks to demonstrate this is a general, transferable capability.

3. **Task-Specific Semi-formal Templates** -- Three tailored templates (patch equivalence, fault localization, code Q&A) sharing the same core principle but adapted to each domain. The fault localization template uses a four-phase PREMISE → CLAIM → PREDICTION chain; the Q&A template requires a Function Trace Table, Data Flow Analysis, and Alternative Hypothesis Check.

4. **Execution-Free RL Reward Signal** -- Demonstrates that 93% verification accuracy on real-world patches is achievable without code execution, opening the door to drastically cheaper RL training pipelines for software engineering agents (no sandbox spin-up, no dependency installation).

---

## Key Findings

| Task | Metric | Standard Reasoning | Semi-formal Reasoning | Gain |
|------|--------|-------------------|----------------------|------|
| Patch equivalence (curated, 170 examples) | Accuracy | 78.2% | **88.8%** | +10.6 pp |
| Patch equivalence (LLM patches, Opus-4.5) | Accuracy | 87.0% | **93.0%** | +6.0 pp |
| Patch equivalence (LLM patches, Sonnet-4.5) | Accuracy | 84.5% | **91.5%** | +7.0 pp |
| Fault localization Top-5 "All" (43 bugs) | Accuracy | 60.1% | **72.1%** | +12.0 pp |
| Fault localization Top-5 "Any" (43 bugs) | Accuracy | 81.4% | **88.4%** | +7.0 pp |
| Fault localization Top-5 "All" (90 bugs) | Accuracy | 43.3% | **47.8%** | +4.5 pp |
| Code Q&A / RubberDuckBench (Opus-4.5) | Accuracy | 78.3% | **87.0%** | +8.7 pp |

- Semi-formal reasoning uses ~2.8x more agent steps (28 vs. 10 for patch equivalence) -- a deliberate trade-off for higher accuracy.
- Single-shot (no agentic exploration) modes consistently underperform agentic modes, confirming that codebase navigation is critical.
- A `difflib` text similarity baseline achieves only 73% on patch equivalence, showing surface similarity is insufficient.
- Primary failure modes: incomplete execution tracing, incorrect assumptions about third-party library semantics, and multi-file/indirection bugs.

---

## Suggestions & Future Directions

1. **Fine-tuning LLMs on semi-formal templates** -- Internalizing the structure through training could reduce prompt overhead and further improve accuracy.
2. **Broader static analysis applications** -- Security vulnerability detection, code smell identification, API misuse detection are directly addressable with the same template approach.
3. **Hybrid verification** -- Combining LLM-based semi-formal reasoning with lightweight formal methods or symbolic execution for stronger correctness guarantees.
4. **RL pipeline integration** -- Using the 93% accurate execution-free verifier as a reward model in SWE-RL / R2E-Gym style training to cut sandbox costs.
5. **Cross-language generalization** -- Templates demonstrated on Python, Java, and C++; future work could systematically evaluate on more languages and frameworks.

---

## Authors & Institutions

Shubham Ugare (Meta, USA), Satish Chandra (Meta, USA)
