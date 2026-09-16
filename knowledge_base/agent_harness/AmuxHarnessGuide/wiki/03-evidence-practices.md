> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evidence, best practices, FAQ

**In one sentence:** The harness matters more than the model — benchmarks show harness changes move scores by 13–64 points while model swaps move ~1 point — so winning practice is to ratchet every agent mistake into guides and sensors, keep rules tied to real failures, separate planning from execution, and design for unattended overnight operation.

## Key points

- On SWE-bench, swapping the harness changes scores by 22 points while swapping the model changes scores by only 1 point, making harness engineering the higher-return investment.
- LangChain gained 13.7 points on Terminal Bench 2.0 (52.8% → 66.5%) by redesigning only the harness with the same model, and Princeton research reports harness configurations improving solve rates by 64% over basic setups.
- Atlan's data pipelines show bare-schema accuracy of 10–31% without governed context versus 94–99% with a proper harness, confirming context structure beats prompt wording.
- The ratchet principle (Osmani): every agent mistake becomes a permanent harness fix — the harness only tightens, never loosens — and every CLAUDE.md line must trace to a real failure (Hashimoto's zero-aspirational-rules rule).
- Invest in sensors over guides: use fast deterministic/computational sensors (linters, tests, type checkers, hooks) before inferential LLM-based judgment, and wire fast feedback loops after every edit.
- Separate planning from execution (planner → generator → evaluator) because agents grade their own work too generously; design for overnight operation with crash, context-exhaustion, and stuck-state recovery.
- August 2026 additions show the compounding pattern: model-driven sensors such as the Simple tab (plain-English self-report cards), voice fleet-orchestrator dispatch, and event-driven subagent lifecycle counts improve for free as models improve.

---

## The evidence: harness > model

The most surprising finding of 2026 is that the harness matters more than the model. The data is consistent across benchmarks:

| Benchmark / source | Harness change | Model change / result |
|---|---|---|
| SWE-bench | Swapping the harness changes scores by 22 points | Swapping the model changes scores by 1 point |
| Terminal Bench 2.0 (LangChain) | Redesigned harness alone: 52.8% → 66.5% (+13.7 points), same model | — |
| Atlan data pipelines | With proper harness: 94–99% accuracy | Bare schema without governed context: 10–31% |
| Princeton research | Harness configurations improve solve rates by 64% vs basic setups | — |

This is why Augment Code, Red Hat, and SIG are all investing in harness engineering as a discipline — the returns are dramatically higher than chasing the latest model.

## 10 best practices

1. **Start simple.** A good CLAUDE.md and pre-commit hooks are more impactful than complex middleware. Add complexity only when simple controls fail.
2. **Apply the ratchet.** Every agent mistake becomes a permanent harness fix. The harness only tightens, never loosens. (Osmani)
3. **Zero aspirational rules.** Every line in CLAUDE.md should trace to a real agent failure. If you can't point to the mistake, delete the line. (Hashimoto)
4. **Invest in sensors, not just guides.** Most teams over-invest in markdown files and under-invest in automated checks. Sensors are the underdiscussed component.
5. **Separate planning from execution.** A planner agent expands prompts into specs. A generator implements. An evaluator tests and grades. Agents rate their own work too generously — separation creates honest feedback.
6. **Context structure > prompt wording.** Most practitioners spend hours on prompt wording and minutes on context structure. This is backwards.
7. **Achieve information parity.** If it's available to humans but not agents, the harness has a hole. Encode every convention, shortcut, and tribal knowledge.
8. **Wire fast feedback loops.** Tests, linters, type checkers running after every edit. The faster the feedback, the fewer cascading failures.
9. **Use computational sensors before inferential ones.** A linter is faster, cheaper, and more reliable than an LLM-based code reviewer. Use deterministic tools first; add LLM-based judgment where deterministic tools can't reach. (Böckeler)
10. **Design for overnight operation.** The harness should handle crashes, context exhaustion, and stuck states without human intervention. If you can't walk away from your agents, your harness has gaps.

## Tools and resources

### Agent platforms and orchestrators

- **amux** — open-source multi-agent orchestration for Claude Code. Session management, kanban board, self-healing watchdog, REST API. The complete harness for parallel agents.
- **Claude Code** — terminal-native coding agent by Anthropic. Built-in harness primitives: CLAUDE.md, hooks, skills, subagents, MCP.
- **OpenAI Codex** — cloud-sandboxed coding agent. AGENTS.md for guides, containerized execution for isolation.
- **Cursor** — AI-native IDE. .cursorrules for guides, built-in linting for sensors.

### Harness components

- CLAUDE.md templates — starter configs for different project types
- Hooks cookbook — 20 production-ready sensor recipes
- MCP servers — tool interfaces for agents
- Sandboxing guide — Docker, E2B, Firecracker, gVisor compared
- Config files compared — CLAUDE.md vs .cursorrules vs AGENTS.md

### Further reading

- Mitchell Hashimoto: My AI Adoption Journey — the origin of Agent = Model + Harness
- OpenAI: Harness Engineering — the Codex case study (0% human code)
- Thoughtworks / Martin Fowler: Harness Engineering — the guides-and-sensors framework
- Thoughtworks: Exploring AI Coding Sensors — the case for investing in sensors
- Addy Osmani: Agent Harness Engineering — the ratchet principle and harness primitives
- LangChain: The Anatomy of an Agent Harness — components defined by working backwards from behaviors
- Red Hat: Harness Engineering for AI-Assisted Development — structured workflows, symbol analysis
- Latent Space: Extreme Harness Engineering — 1M LOC, 1B tokens/day, 0% human code
- Awesome Harness Engineering — curated list of tools, patterns, and resources
- HumanLayer: Skill Issue — Harness Engineering for Coding Agents

## FAQ

### What is harness engineering?

Harness engineering is the discipline of designing everything around an AI model that makes it a useful agent — context pipelines, guides, sensors, tools, memory, orchestration, permissions, and observability. The formula is Agent = Model + Harness. The term was coined by Mitchell Hashimoto in February 2026 and formalized by OpenAI, Thoughtworks, and others.

### How is harness engineering different from prompt engineering?

Prompt engineering shapes behavior within a single interaction. Context engineering shapes reasoning by architecting the complete information environment. Harness engineering shapes execution by designing the entire operational environment — it contains both prompt and context engineering alongside tool interfaces, sensors, memory, orchestration, and permissions. Prompt engineering didn't die; it was reclassified as one component inside the harness.

### What are guides and sensors?

Guides are feedforward controls that constrain the agent before it acts — CLAUDE.md, system prompts, tool definitions. Sensors are feedback controls that validate the agent after it acts — linters, tests, hooks, evals. Together they form a control system. Framework by Birgitta Böckeler at Thoughtworks.

### What is the ratchet principle?

Coined by Addy Osmani: every agent mistake should become a permanent fix in the harness. The harness only tightens, never loosens. This means every line in your CLAUDE.md traces to a real failure, every hook traces to a real violation, and the harness accumulates institutional knowledge about what goes wrong.

### Why does the harness matter more than the model?

On SWE-bench, swapping the harness changes scores by 22 points; swapping the model changes scores by 1 point. LangChain improved 13.7 points on Terminal Bench 2.0 by changing only the harness. The model is increasingly a commodity; the harness is the competitive moat.

### How does amux implement harness engineering?

amux is a harness for multi-agent systems. It provides orchestration (parallel session management, atomic task claiming via kanban board, voice-driven fleet commands from your phone), sensors (health monitoring, crash detection, context exhaustion detection, Simple tab plain-English status summaries, event-driven subagent lifecycle count), context pipelines (CLAUDE.md, session memory, MCP servers), tool interfaces (REST API, browser automation), and self-healing (automatic crash recovery, context compaction, stuck-prompt resolution).

### What is the Simple tab in harness engineering?

The Simple tab is a sensor component that queries each worker for a plain-English status summary and displays it as a human-readable card. It turns raw terminal output (an unreliable signal) into a model-generated status the operator can act on without reading logs. As models improve, the summaries improve: the sensor compounds with model capability. amux ships it as a first-class harness component alongside health monitoring and context-exhaustion detection.

### Do I need amux to practice harness engineering?

No. Harness engineering starts with a CLAUDE.md file and a pre-commit hook — tools you already have. amux becomes valuable when you scale to 3+ parallel agents and need orchestration, monitoring, and self-healing that a single terminal session can't provide. Start simple, scale when the single-agent harness isn't enough.

## The harness in August 2026

Harness engineering is a practice, not a product. Its components evolve as the agents they wrap become more capable. Three additions in August 2026 illustrate this: the harness gets better as the models get better only if the harness compounds with model capability. A static sensor gives you the same information at GPT-3 quality as at GPT-6 quality. A model-driven sensor gives you richer signal every time the underlying model improves. The Simple tab is a concrete example of this design pattern.

### New sensor: Simple tab

A per-worker sensor that asks the model what it is doing and renders the answer as a plain-English card. Instead of parsing terminal output (brittle, ANSI-polluted, truncated at arbitrary widths), the operator reads a three-sentence summary the model generated about its own state. The summary is configurable: a standing prompt like "one sentence, present tense" gives you a consistent format across 20 workers. Read-aloud support ships the summary through the iOS audio player so you can monitor a fleet without looking at a screen.

Why this matters for the harness: as models improve, their self-reports improve. A sensor wired to a better model becomes a better sensor for free.

### New orchestration interface: voice fleet-orchestrator

A new guide delivery mechanism: dispatch a task to your entire agent fleet by speaking into your phone. The voice input is transcribed and sent as a steering message to all active workers. The harness receives a natural-language instruction and distributes it as structured work. Practical application: standing in your kitchen at 8am, you say "focus on the checkout flow today" and every coding agent receives the priority. No keyboard, no SSH session.

### New observability sensor: event-driven subagent lifecycle count

The harness now tracks subagents spawned by each worker as a first-class metric. When Claude Code launches a subagent (for isolation, for a parallel task, for a risky operation), the event propagates to the dashboard in real time. The ratchet principle applied to observability: once you can see subagent spawning, you can set policy on it. A worker that spawns 40 subagents in an hour is doing something very different from one that spawns 2.

The pattern in all three: close the gap between what the model is doing and what the operator can see. A harness that cannot express a discriminator cannot enforce policy on it. These additions are sensors and observability improvements, not configuration additions. They compound with model capability rather than constraining it.

**Covers:** chunk 03
