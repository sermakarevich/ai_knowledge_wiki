# Loop Engineering

**Paper:** [Loop Engineering (Cobus Greyling, 2026)](https://cobusgreyling.medium.com/loop-engineering-62926dd6991c)

## Human Readable TL;DR

Instead of typing instructions to an AI assistant and waiting for a response, loop engineering means you build a small automated system that does the typing for you -- finding tasks, handing them to the AI, checking the results, and deciding what to do next, all on its own. It's the difference between being the person who operates a machine and being the person who builds the machine. The core insight: your job as a developer shifts from writing prompts to designing systems that write prompts.

## TL;DR

Loop engineering is an architectural pattern for AI-assisted development in which developers replace manual prompt-response cycles with autonomous control loops. These loops discover work, delegate to coding agents, verify outputs, maintain durable state, and determine next steps -- running on schedules or until goal conditions are satisfied. The author frames it as a shift in leverage: from individual prompt quality to system design.

---

## Problem & Motivation

Traditional AI-assisted development requires a human in the loop at every step: write prompt, read output, write next prompt. This sequential model limits throughput, does not scale to parallel workstreams, and loses context across sessions. Loop engineering addresses this by removing the human from the inner loop while preserving human oversight at the outer loop (verification, approval gates, state review).

---

## Main Original Ideas

1. **The Loop Replaces the Prompter** -- The practitioner's role shifts from crafting individual prompts to designing autonomous systems. As Peter Steinberger (OpenClaw) puts it: "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." Boris Cherny (Head of Claude Code, Anthropic) echoes: "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."

2. **Five Building Blocks + Memory** -- The author identifies six composable primitives that underpin all loop architectures:
   - **Automations/Scheduling (The Heartbeat):** Cadenced discovery and triage replace manual checks; ad-hoc tasks become reliable, unattended processes.
   - **Worktrees for Safe Parallel Execution:** Agents are isolated in separate git worktrees to prevent merge conflicts and enable concurrent work.
   - **Skills & Persistent Project Knowledge:** External knowledge files (e.g., CLAUDE.md) preserve conventions, build commands, and institutional context across runs, eliminating re-derivation overhead.
   - **Plugins & Connectors (MCP):** MCP-based connectors let loops act on external systems -- opening PRs, updating tickets, posting to Slack, querying databases.
   - **Sub-agents (Maker/Checker Split):** Implementation and verification are separated, optionally using different models or instruction sets to verify against specifications.
   - **Memory as the Spine:** Durable state files track current work, previous attempts, and items awaiting human input -- essential for multi-day or multi-run loops.

3. **Tooling Convergence** -- Both Claude Code and OpenAI Codex support the same set of primitives, making loop patterns largely tool-agnostic. The Grok TUI is cited as directly mapping to this architectural stack, suggesting the pattern is stabilising across vendors.

---

## Key Findings

- The leverage point in AI-assisted development has shifted from individual prompt quality to system design.
- Loops are early-stage technology; the author explicitly cautions against treating current tooling as mature.
- Token costs scale non-linearly: sub-agents and frequent cadences multiply consumption significantly.
- Unattended loops produce unattended mistakes -- verification gates remain non-negotiable.
- "Comprehension debt" accumulates when speed masks gaps in the developer's own understanding of the system.
- "Cognitive surrender" is identified as a failure mode: builders must remain engineers, not just loop operators.

---

## Suggestions & Future Directions

1. Treat loop engineering as systems design work, not prompt engineering -- apply the same discipline to loop architecture as to any software system.
2. Build in verification checkpoints from the start; do not bolt them on after unattended runs produce errors.
3. Monitor token costs proactively -- cadence and sub-agent depth are the primary cost drivers.
4. Maintain deep comprehension of what the loop is doing; resist the temptation to treat the loop as a black box.
5. The author implies that as tooling matures, the primitives (scheduling, worktrees, skills, plugins, sub-agents, memory) will become standard infrastructure -- invest in understanding them now.

---

## Authors & Institutions

Cobus Greyling (independent author/practitioner, Medium); quotes from Peter Steinberger (OpenClaw) and Boris Cherny (Anthropic, Head of Claude Code).
