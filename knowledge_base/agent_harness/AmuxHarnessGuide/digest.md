> [[index|Wiki]] | [[summary|Summary]]

# AmuxHarnessGuide — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-concept-formula|Concept: model+harness, guides vs sensors]]

**In one sentence:** An AI agent equals a commodity model plus an engineered harness of feedforward guides and feedback sensors, and harness design — not the model choice — is what determines production performance.

- Harness engineering is the discipline of designing everything around a model (context pipelines, guides, sensors, tools, memory, orchestration, permissions, observability) so mistakes get engineered away permanently.
- The term emerged in February 2026 from Mitchell Hashimoto ("engineer a solution such that the agent never makes that mistake again") and, six days later, Ryan Lopopolo's OpenAI case study of 3 engineers shipping 1M generated lines across 1,500 PRs (3.5 PRs/engineer/day) with zero hand-written code.
- The canonical vocabulary comes from Birgitta Böckeler (Thoughtworks, on Martin Fowler's site): guides are feedforward controls, sensors are feedback controls, borrowed from cybernetics.
- Agent = Model + Harness: the model alone is only a reasoning engine; state, tool execution, feedback loops, and enforceable constraints come from the harness, like tack that channels a powerful horse.
- The model is a commodity and the harness is the moat: on SWE-bench swapping the harness moves scores by 22 points versus 1 point for swapping the model, and LangChain rose from 52.8% to 66.5% on Terminal Bench 2.0 with the same model by changing only the harness (+13.7 points).
- Guides (followed ~70% of the time) steer before action while sensors (enforcing at ~100%) validate after action — guides without sensors are a car with a steering wheel but no brakes, so teams must invest in the "underdiscussed" sensors, not just guides.
- Prompt engineering (2022–2024) was absorbed, not replaced: prompt ⊂ context engineering (2025) ⊂ harness engineering (2026), and 82% of IT leaders say prompting alone is insufficient for production agents.

## 2. [[wiki/02-ratchet-build|Ratchet principle and first-harness steps]]

**In one sentence:** Every agent mistake is fixed permanently in the harness — never in the output — starting from a lean CLAUDE.md and tightening via hooks, skills, feedback loops, and memory until the same architecture scales to multi-agent orchestration with amux.

- The ratchet principle (Addy Osmani): the harness only tightens, never loosens — fix the harness component, not the bad output.
- Six failure-to-fix mappings route each mistake to a component: unknown rule → CLAUDE.md, violated rule → hook, missing info → skill/MCP, dangerous tool → permissions, polluted context → subagent, silent crash → monitoring.
- Hashimoto's rule: every line in AGENTS.md must trace to a real agent failure; delete any rule you cannot tie to a specific mistake — zero aspirational rules.
- Information parity: anything a human knows (docs, conventions, tribal knowledge) must be encoded in the harness or agents will make mistakes humans never would.
- Enforcement gap: CLAUDE.md instructions are followed ~70% of the time, while hooks enforce at 100% — so any must-hold rule moves into a hook.
- Lean start: keep CLAUDE.md under 500 lines with only non-inferable content (build/test commands, style rules, forbidden patterns, pointers), load big references on demand via skills (~200 tokens visible at startup), and run tests/linters/typecheckers automatically after every edit.
- Scaling to 10+ agents turns configuration into an orchestration platform (amux): Kanban task claiming via REST API, one worktree per agent, self-healing watchdog, inter-session messaging, SSE web dashboard, per-session token accounting — proven at scales like 1M LOC / 1B tokens per day (OpenAI Symphony) and 1,300 AI PRs per week (Stripe Minions).

## 3. [[wiki/03-evidence-practices|Evidence, best practices, FAQ]]

**In one sentence:** The harness matters more than the model — benchmarks show harness changes move scores by 13–64 points while model swaps move ~1 point — so winning practice is to ratchet every agent mistake into guides and sensors, keep rules tied to real failures, separate planning from execution, and design for unattended overnight operation.

- On SWE-bench, swapping the harness changes scores by 22 points while swapping the model changes scores by only 1 point, making harness engineering the higher-return investment.
- LangChain gained 13.7 points on Terminal Bench 2.0 (52.8% → 66.5%) by redesigning only the harness with the same model, and Princeton research reports harness configurations improving solve rates by 64% over basic setups.
- Atlan's data pipelines show bare-schema accuracy of 10–31% without governed context versus 94–99% with a proper harness, confirming context structure beats prompt wording.
- The ratchet principle (Osmani): every agent mistake becomes a permanent harness fix — the harness only tightens, never loosens — and every CLAUDE.md line must trace to a real failure (Hashimoto's zero-aspirational-rules rule).
- Invest in sensors over guides: use fast deterministic/computational sensors (linters, tests, type checkers, hooks) before inferential LLM-based judgment, and wire fast feedback loops after every edit.
- Separate planning from execution (planner → generator → evaluator) because agents grade their own work too generously; design for overnight operation with crash, context-exhaustion, and stuck-state recovery.
- August 2026 additions show the compounding pattern: model-driven sensors such as the Simple tab (plain-English self-report cards), voice fleet-orchestrator dispatch, and event-driven subagent lifecycle counts improve for free as models improve.

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. An agent is a commodity model plus an engineered harness of guides and sensors, and harness design determines production performance.
2. Benchmarks prove the harness is the moat: harness swaps move scores 13–64 points while model swaps move ~1 point.
3. Guides steer before action (~70% compliance) while sensors enforce after action (~100%), so teams must invest in underdiscussed sensors.
4. Every agent mistake ratchets permanently into the harness — never into the output — with each failure mapped to a harness fix.
5. Start lean from a sub-500-line CLAUDE.md of non-inferable rules, then tighten via hooks, skills, feedback loops, and memory.
6. The same architecture scales to multi-agent orchestration with amux: worktrees, Kanban claiming, watchdogs, and token accounting.
7. Winning practice compounds: sensors over guides, planning separated from execution, and design for unattended overnight operation.
<!-- FIVE_MOVES_END -->
