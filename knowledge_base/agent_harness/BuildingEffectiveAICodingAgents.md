# Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

**Paper:** [Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned (Nghi D. Q. Bui, 2025)](https://arxiv.org/abs/2603.05344)

## Human Readable TL;DR

Imagine you hire a brilliant assistant to help you write software, but they can only remember the last few pages of your conversation and have a tendency to accidentally delete important files. This paper is like a detailed instruction manual for building that assistant so it stays on track during long work sessions, doesn't break anything, and knows when to ask for help. The authors share practical recipes -- like giving the assistant a notepad for important reminders, teaching it to compress old conversation notes, and setting up safety guardrails -- all so it can work reliably inside the same text-based terminal window that programmers already use every day.

## TL;DR

This paper presents OPENDEV, an open-source, Rust-based, terminal-native AI coding agent, and provides a comprehensive technical report on its architecture. The system introduces a compound AI architecture with workload-optimized multi-model routing across five specialized roles (action, thinking, critique, vision, compaction), a five-layer defense-in-depth safety framework, and an Adaptive Context Compaction pipeline that reduces peak observation token consumption by ~54%. The paper's primary contribution is not a novel algorithm but a detailed, transparent engineering blueprint for building production-grade agentic coding systems, covering scaffolding, harness design, context engineering, and persistence.

---

## Problem & Motivation

Terminal-native AI coding agents face three fundamental engineering challenges that this paper addresses:

1. **Context window exhaustion:** Long-running coding sessions quickly consume finite LLM context budgets with conversation history and tool outputs, causing the agent to "forget" earlier instructions and goals.
2. **Safety of arbitrary execution:** Agents that can run shell commands and modify files risk destructive operations (deleting repositories, overwriting production configs) without robust guardrails.
3. **Extensibility vs. efficiency tradeoff:** Adding new tools and capabilities (e.g., via MCP servers) inflates prompt size, degrading performance and increasing cost.

Existing production-grade systems (e.g., Claude Code) are closed-source with undocumented architectures, while open-source alternatives often prioritize benchmark scores over interactive daily usability and lack comprehensive technical documentation. OPENDEV fills this gap by providing a transparent, well-documented reference implementation.

---

## Main Original Ideas

1. **Workload-Optimized Multi-Model Architecture** -- Five distinct model roles (Action, Thinking, Critique, Vision, Compact) are defined, each independently configurable with its own LLM binding and fallback chain. This allows routing cheap models to simple tasks and powerful models to complex reasoning, optimizing cost-latency-capability tradeoffs within a single agent session.

2. **Extended ReAct Loop with Thinking and Self-Critique Phases** -- The standard ReAct loop is augmented with a dedicated tool-free thinking phase and an optional self-critique phase before the action step. This separation prevents the model from being pressured to act prematurely, producing more deliberate reasoning traces.

3. **Five-Layer Defense-in-Depth Safety Architecture** -- Safety is enforced through prompt-level guardrails, schema-level tool restrictions (making dangerous tools structurally invisible in safe modes), runtime approval with persistent rules, tool-level validation with dangerous pattern blocklists, and user-defined lifecycle hooks. Schema gating is emphasized as more robust than runtime permission checks alone.

4. **Adaptive Context Compaction (ACC)** -- A five-stage pipeline monitors token utilization and applies progressively aggressive reduction: warning injection, observation masking, fast pruning, aggressive masking, and full LLM-based summarization. This achieves ~54% reduction in peak observation context, often eliminating the need for expensive summarization in typical 30-turn sessions.

5. **Dual-Memory Architecture for Thinking** -- Episodic memory (periodically regenerated LLM summaries of full history) is combined with working memory (verbatim recent messages) to bound context while preserving both strategic goals and operational details during the thinking phase.

6. **Context-Aware System Reminders** -- Event-driven, targeted messages injected as `role: user` at critical decision points counteract instruction fade-out in long sessions, yielding measurably higher compliance rates beyond 15 tool calls compared to relying on the initial system prompt alone.

7. **Adaptive Memory (ACE) Pipeline** -- An experience-driven memory system captures learned strategies as a scored "playbook" of natural-language bullets, injected into the system prompt based on relevance. This enables the agent to accumulate project-specific knowledge across sessions.

8. **9-Pass Fuzzy Matching for File Edits** -- The `edit_file` tool employs a 9-pass fuzzy matching chain to handle LLM-generated content that subtly differs from actual file content, converting near-misses into successful edits and significantly reducing "content not found" errors.

---

## Key Findings

### Context Efficiency

| Strategy | Impact |
|---|---|
| **Adaptive Context Compaction (ACC)** | **~54% reduction** in peak observation token consumption |
| Tool Result Optimization (summarization + scratch offload) | Large outputs (>8K chars) offloaded, keeping context focused |
| Lazy MCP/Skill Discovery | Baseline context overhead reduced to **<5%** |
| Dual-Memory Architecture | Bounded thinking context while preserving strategic + operational detail |

### Behavioral Steering and Reliability

- Context-aware system reminders proved more effective than initial system prompts alone for maintaining instruction compliance in sessions exceeding 15 tool calls
- Separating thinking from action phases consistently produced higher-quality reasoning traces
- The 9-pass fuzzy matching chain for `edit_file` significantly reduced file edit failures caused by LLM imprecision

### Safety and Control

- Schema-level tool restriction (making write tools invisible to the Planner subagent) was more robust than runtime permission checks, making dangerous actions structurally impossible
- Persistent approval rules stored on disk reduced "approval fatigue," preventing users from resorting to blanket auto-approval
- Shadow Git snapshots provided per-step rollback for all filesystem changes

### Operational Lessons

- Explicit resource caps (undo history, nudge attempts, iteration limits) were essential for preventing unbounded growth in long sessions
- Deterministic REPL command dispatch for non-LLM operations (session management, model selection) kept interactions fast, predictable, and token-free
- Doom-loop detection via tool-call fingerprinting identified and intervened on repetitive agent actions

---

## Suggestions & Future Directions

1. **Quantitative benchmarking** -- The authors acknowledge the need for rigorous evaluation against established benchmarks such as SWE-bench and Terminal-Bench to validate OPENDEV's effectiveness with quantitative metrics.

2. **Adaptive resource allocation** -- Future work should explore dynamically adjusting resources (iteration budgets, context allocation) based on inferred task complexity rather than using fixed caps.

3. **Cross-project memory scaling** -- The memory pipeline (ACE) should be extended to support knowledge transfer across projects, enabling the agent to leverage patterns learned in one codebase when working in another.

4. **Richer code representations** -- Moving beyond text-based context retrieval to incorporate AST-level and semantic code representations could improve the agent's understanding of code structure.

5. **Advanced multi-agent coordination** -- More sophisticated patterns for coordinating concurrent subagents, including shared state management and conflict resolution, are identified as an open research direction.

6. **Human-agent collaboration improvements** -- The authors highlight that research (e.g., LongCLI-Bench) shows human-agent collaboration significantly improves task completion rates, suggesting further investment in interaction design and feedback mechanisms.

---

## Authors & Institutions

Nghi D. Q. Bui -- OpenDev (open-source project)
