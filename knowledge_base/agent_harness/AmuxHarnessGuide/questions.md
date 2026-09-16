---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# AmuxHarnessGuide — Retrieval Practice

## Section 1: Concept — model+harness, guides vs sensors

### Q1 (core recall): State the Agent = Model + Harness formula and the two benchmark numbers that prove the harness is the moat, not the model.

<details>
<summary>Answer</summary>

An agent equals a commodity model (reasoning engine) plus an engineered harness (context pipelines, guides, sensors, tools, memory, orchestration, permissions, observability) — and harness design determines production performance.

Two numbers: on SWE-bench, swapping the harness moves scores by 22 points versus ~1 point for swapping the model; LangChain rose from 52.8% to 66.5% on Terminal Bench 2.0 (+13.7 points) with the same model by changing only the harness.

Vocabulary source: Birgitta Böckeler (Thoughtworks, on Martin Fowler's site) — guides are feedforward controls, sensors are feedback controls, borrowed from cybernetics.
</details>

### Q2 (core recall): Guides are followed ~70% of the time while sensors enforce at ~100% — what does each do, and what is the car analogy?

<details>
<summary>Answer</summary>

Guides steer before action (feedforward controls: instructions, context, prompts); sensors validate after action (feedback controls: tests, linters, hooks, type checkers).

Car analogy: guides without sensors are a car with a steering wheel but no brakes. Consequence: teams must invest in the "underdiscussed" sensors, not just guides — any must-hold rule moves into a hook/sensor that enforces at 100%.

Related absorption chain: prompt engineering (2022–2024) ⊂ context engineering (2025) ⊂ harness engineering (2026); 82% of IT leaders say prompting alone is insufficient.
</details>

### Q3 (elaboration): Why does investing mostly in guides (prompts, instructions) fail in production — what breaks if a team has no sensors?

<details>
<summary>Answer</summary>

Because guides are probabilistic (~70% compliance) — the model can ignore, forget, or misread them under long contexts or edge cases, with no corrective loop. Without sensors, mistakes pass silently into outputs, PRs, or pipelines: no brakes, no detection, no permanent fix.

The harness-engineering answer: route each must-hold property to a deterministic sensor (hook, test, linter, type checker, permissions) that enforces at ~100%, and keep fast feedback loops after every edit so violations are caught and ratcheted immediately.
</details>

## Section 2: Ratchet principle and first-harness steps

### Q4 (core recall): State the ratchet principle, Hashimoto's rule, the enforcement gap numbers, and the lean-start limits (CLAUDE.md lines, skill startup tokens).

<details>
<summary>Answer</summary>

- Ratchet principle (Addy Osmani): the harness only tightens, never loosens — fix the harness component, never the bad output.
- Hashimoto's rule: every line in AGENTS.md/CLAUDE.md must trace to a real agent failure; delete any rule you cannot tie to a specific mistake — zero aspirational rules.
- Enforcement gap: CLAUDE.md instructions are followed ~70% of the time, hooks enforce at 100% — so must-hold rules move into hooks.
- Lean start: CLAUDE.md under 500 lines with only non-inferable content (build/test commands, style rules, forbidden patterns, pointers); big references load on demand via skills (~200 tokens visible at startup); run tests/linters/typecheckers automatically after every edit.
</details>

### Q5 (elaboration): Why must every CLAUDE.md line trace to a real failure — what breaks if you allow aspirational rules?

<details>
<summary>Answer</summary>

Because uninferred-from-failure rules bloat context, dilute attention, and are still only followed ~70% of the time — they cost tokens on every run while adding unverified constraints that can conflict or go stale. Information parity cuts the other way: anything a human knows (docs, conventions, tribal knowledge) must be encoded, but only as proven-by-failure entries.

Failure-to-fix routing keeps this disciplined: unknown rule → CLAUDE.md, violated rule → hook, missing info → skill/MCP, dangerous tool → permissions, polluted context → subagent, silent crash → monitoring. Aspirational rules bypass this routing and rot.
</details>

## Section 3: Evidence, best practices, FAQ

### Q6 (transfer): Your agent must run unattended overnight generating PRs. Using the evidence and practices, which harness pieces do you put in place and why?

<details>
<summary>Answer</summary>

- Separate planning from execution (planner → generator → evaluator), because agents grade their own work too generously.
- Prefer fast deterministic/computational sensors (linters, tests, type checkers, hooks) over inferential LLM-based judgment; wire them to run after every edit.
- Add crash, context-exhaustion, and stuck-state recovery plus monitoring (silent crash → monitoring), with per-session token accounting and a self-healing watchdog — the amux-scale pattern proven at 1M LOC / 1B tokens per day (OpenAI Symphony) and 1,300 AI PRs/week (Stripe Minions).
- Supporting evidence for the investment: Atlan pipelines show 10–31% bare-schema accuracy versus 94–99% with governed context; Princeton reports +64% solve rates from harness configuration; model-driven sensors (e.g. Simple tab self-report cards) compound for free as models improve.
</details>

### Q7 (evaluation): This guide is published by amux.io and its FAQ maps every harness component onto amux's own product. Per [[critical_thinking|Critical Analysis]], which specific claims in this guide should you distrust more because of that, and which parts still hold up independent of the source?

<details>
<summary>Answer</summary>

Distrust more: the round, uncited statistics repeated as fact (~70% guide compliance, ~100% sensor enforcement, the Atlan 10-31% vs 94-99% figures, "82% of IT leaders") -- none is sourced to a checkable study in the extracted text -- and the claim that amux is "the complete harness" for multi-agent orchestration, which is the vendor's self-assessment of its own product.

Holds up independent of the source: the conceptual vocabulary (guides vs. sensors, the ratchet principle) is corroborated by an independent article, [[OsmaniHarness/summary]], which uses the same "Agent = Model + Harness" formula and ratchet discipline without citing amux -- so the framework itself is more trustworthy than any specific number or product claim in this particular guide.
</details>
