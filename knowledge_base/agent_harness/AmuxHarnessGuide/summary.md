# Harness Engineering: The Complete Guide

**Article:** [Harness Engineering: The Complete Guide](https://amux.io/guides/harness-engineering/) — amux.io, 2026

## Human Readable TL;DR

Think of a powerful racehorse and its tack — the saddle, bridle, and reins that channel all that strength in a useful direction. This guide argues an AI (Artificial Intelligence) agent works the same way: the model is the horse, and everything built around it — instructions, tools, checks, memory, permissions — is the tack, called the harness. The pitch: the model is now a commodity, and the harness is where all the competitive advantage lives, so every mistake an agent makes should be fixed once, permanently, in the harness — never patched in the output.

## TL;DR

Agent = Model + Harness: the harness (context pipelines, guides, sensors, tools, memory, orchestration, permissions, observability) determines production performance more than model choice, evidenced by SWE-bench harness swaps moving scores 22 points versus ~1 point for model swaps, and LangChain gaining 13.7 points on Terminal Bench 2.0 (52.8%→66.5%) with the same model. Harness components split into guides (feedforward, ~70% compliance) and sensors (feedback, ~100% enforcement) — the guide argues teams over-invest in guides and under-invest in the "underdiscussed" sensors. The ratchet principle (Osmani) says every agent mistake gets fixed permanently in the harness via six failure-to-fix routings (unknown rule→CLAUDE.md, violated rule→hook, missing info→skill/MCP, dangerous tool→permissions, polluted context→subagent, silent crash→monitoring), with Hashimoto's rule that every CLAUDE.md line must trace to a real failure. Practice starts lean (CLAUDE.md under 500 lines, skills on demand) and scales to multi-agent orchestration platforms like amux (Kanban task claiming, per-agent worktrees, watchdogs, token accounting), proven at scales like 1M LOC/day (OpenAI Symphony) and 1,300 AI PRs/week (Stripe Minions).

---

## Problem & Motivation

Prompt engineering alone (shaping a single model call, 2022–2024 era) is insufficient for production agents — 82% of IT leaders say so — because a bare model has no state, no tool execution, no feedback loops, and no enforceable constraints. Context engineering (2025) improved reasoning by architecting the information environment, but still did not solve execution reliability: agents repeat mistakes, violate rules they "know", crash silently, and pollute context. The guide addresses this gap with harness engineering (2026): the discipline of designing the entire operational environment around the model so mistakes get engineered away permanently. It matters because the model is increasingly a commodity while the harness is the competitive moat — benchmark data shows harness changes move scores 13–64 points while model swaps move ~1 point, so return on investment is dramatically higher in harness work.

---

## Main Original Ideas

1. **Agent = Model + Harness** — A model alone (GPT-4o, Claude, Gemini) is only a reasoning engine; it becomes an agent when the harness supplies state, tool execution, feedback loops, and enforceable constraints. Like horse tack channeling a powerful animal, the harness (context pipelines, guides, sensors, tools, memory, orchestration, hooks, permissions, sandboxes, observability) is what makes the model useful.
2. **Guides vs sensors (feedforward vs feedback)** — Borrowed from cybernetics via Birgitta Böckeler (Thoughtworks): guides steer before action (CLAUDE.md, system prompts, skills, tool definitions, task specs) and are followed ~70% of the time, while sensors validate after action (linters, tests, hooks, evals) and enforce at ~100%. A harness with only guides is a car with a steering wheel but no brakes; sensors are the "powerful and underdiscussed" half most teams neglect.
3. **The ratchet principle** — Coined by Addy Osmani: every agent mistake becomes a permanent harness fix, never an output patch; the harness only tightens, never loosens. Six failure-to-fix routings diagnose the broken component: unknown rule→CLAUDE.md, violated rule→hook, missing info→skill/MCP server, dangerous tool→permissions, polluted context→subagent isolation, silent crash→monitoring.
4. **Hashimoto's rule and information parity** — From Mitchell Hashimoto: every line in AGENTS.md/CLAUDE.md must trace to a real agent failure; delete anything aspirational. Complemented by information parity: anything a human knows (docs, conventions, tribal knowledge) must be encoded in the harness, or agents will make mistakes humans never would.
5. **Lean-first harness build** — Start with tools you have: a lean CLAUDE.md under 500 lines with only non-inferable content (build/test commands, style rules, forbidden patterns, pointers), skills that expose ~200 tokens at startup and load on demand, hooks that promote must-hold rules to 100% enforcement, fast feedback loops (tests/linters/typecheckers after every edit), and MEMORY.md for cross-session knowledge.
6. **Multi-agent harness as orchestration platform** — One agent needs configuration; ten agents need a platform like amux: Kanban board with atomic task claiming via REST API, one worktree per agent, self-healing watchdog (auto-restart, compaction, stuck-prompt resolution), inter-session messaging, SSE (Server-Sent Events) dashboard, and per-session token accounting for unattended overnight operation.
7. **Model-compounding sensors** — August 2026 pattern: model-driven sensors (Simple tab plain-English self-report cards, voice fleet-orchestrator dispatch, event-driven subagent lifecycle counts) improve for free as models improve, unlike static sensors. Design sensors that compound with model capability rather than merely constraining it.

---

## Key Findings

| Benchmark / source | Harness change | Model change / baseline result |
|---|---|---|
| SWE-bench | Swapping the harness moves scores by 22 points | Swapping the model moves scores by ~1 point |
| Terminal Bench 2.0 (LangChain) | Redesigned harness alone: 52.8% → 66.5% (+13.7 points), same model | — |
| Atlan data pipelines | With governed harness context: 94–99% accuracy | Bare schema without governed context: 10–31% |
| Princeton research | Harness configurations improve solve rates by 64% vs basic setups | — |
| OpenAI Symphony (Codex case study) | 1M lines generated, 1B tokens/day, 1,500 PRs by 3 engineers (3.5 PRs/engineer/day), zero hand-written code | — |
| Stripe "Minions" | 1,300 AI-generated PRs/week via deterministic/agentic node separation | — |

- Guides are followed ~70% of the time; hooks/sensors enforce at ~100% — so must-hold rules belong in hooks, not markdown.
- Prompt engineering (2022–2024) was absorbed, not replaced: prompt ⊂ context engineering (2025) ⊂ harness engineering (2026).
- Computational (deterministic) sensors — linters, type checkers, tests, hooks — beat inferential (LLM-based) sensors on speed, cost, and reliability; use deterministic first, LLM judgment where determinism cannot reach.
- Agents grade their own work too generously, so planning must be separated from execution (planner → generator → evaluator).
- Context structure beats prompt wording; most practitioners invest backwards (hours on wording, minutes on structure).
- Proven multi-agent pattern: deterministic nodes (lint, push, commit) separated from agentic nodes (implement feature, fix CI).
- Term origins: February 2026 Hashimoto ("engineer a solution such that the agent never makes that mistake again"), six days later Lopopolo's OpenAI case study, then Böckeler's canonical guides-vs-sensors framework.

---

## Suggestions & Future Directions

1. **Start simple, ratchet up.** A good CLAUDE.md plus pre-commit hooks beats complex middleware; add complexity only when simple controls fail, and convert every failure into a permanent fix.
2. **Enforce zero aspirational rules.** Audit CLAUDE.md regularly: every line must trace to a specific observed failure; delete the rest to keep the file lean and load-bearing.
3. **Invest in sensors over guides.** Shift effort from more markdown to automated checks — hooks, evals, UI (User Interface) automation verification — and wire fast feedback loops after every edit.
4. **Separate planning from execution.** Use planner → generator → evaluator roles so grading stays honest; never let the generator grade itself.
5. **Close the information-parity gap.** Systematically encode docs, conventions, and tribal knowledge into guides, skills, or MCP (Model Context Protocol) servers.
6. **Prefer computational sensors first.** Deploy linters, type checkers, and deterministic hooks before LLM-based reviewers; reserve inferential sensors for semantic judgment determinism cannot cover.
7. **Design for overnight operation.** Build crash recovery, context-exhaustion handling, and stuck-state resolution so agents run unattended; if you cannot walk away, the harness has gaps.
8. **Scale to orchestration deliberately.** Move to a multi-agent platform (amux-style: Kanban claiming, worktree isolation, watchdog, token accounting) at ~3+ parallel agents, not before.
9. **Build model-compounding sensors.** Invest in sensors whose signal improves with the model (self-report cards, event-driven lifecycle metrics) rather than static parsers like raw terminal scraping.
10. **Open questions.** How to measure harness coverage (which failures still escape all sensors)? What is the minimal sensor set per project type? How do subagent-spawn policies generalize? The guide acknowledges these as ongoing practice, not solved problems — harness engineering is a practice, not a product.

---

## Authors & Institutions

amux.io (guide publisher, 2026), synthesizing Mitchell Hashimoto, Ryan Lopopolo (OpenAI), Birgitta Böckeler (Thoughtworks), Addy Osmani, LangChain, Red Hat, Atlan, Princeton research, Stripe, Augment Code
