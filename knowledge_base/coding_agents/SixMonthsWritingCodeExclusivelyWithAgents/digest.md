> [[index|Wiki]] | [[summary|Summary]]

# Six Months of Writing Code Exclusively With Agents - exe.dev blog — Digest

## 1. [[wiki/01-the-system-lived-in-my-head|The system lived in my head]]

**In one sentence:** After models got good enough, the author stopped writing code by hand in February and scaled from one agent to ~20 parallel VMs managed by botd — which made shipping easy but made deciding what was worth shipping the hard part.

## Key points

- Before AI, the author's superpower was a hard-earned mental model of the whole system, especially interfaces between components, unwritten assumptions, and which line of code mattered — maintained by constantly reading others' changes.
- Hand-writing was the bottleneck: typing speed plus the fact that even small features spanned handlers, schema, tests, and docs with unequal blast radius (a bad handler reverts cleanly, a bad migration leaves a mess).
- The February rule — no code by hand for six months, broken once for three minutes — forced reps with agents: when an agent got stuck, fix what it was missing (prompts, tools, environment) instead of finishing the code.
- The trigger was Claude Code plus a step-change in models (GPT-5.3 and Opus 4.6 handling larger changes with less steering); earlier Copilot autocomplete and Cursor tab-complete only helped with first drafts.
- Parallelism grew accidentally from idle time between agent tasks (one agent became a dozen): sharing one dev box caused file/Git collisions, dependency/port/process fights, and waiting on the longest-running agent.
- Isolation evolved worktrees (fixed only Git) → AGENTS.md patches (random ports, ephemeral databases, burned context avoiding collisions) → containers (separate ports/processes/state but leaky boundary, laptop must stay awake) → one exe.dev Linux VM per task (SSH/HTTPS in seconds, work survives closing the laptop).
- Botd (three rules: off-laptop, mobile-first, preserve every conversation) provisioned/deprovisioned boxes, showed working/stuck/waiting status, and enabled phone/laptop inspection, follow-ups, and diff review; agents ran YOLO mode inside disposable VMs with credentials proxied (never in-VM) and write access limited to test environments.
- Validation at scale (~20 VMs peak, some abandoned for weeks) relied on agents running tests, full CI, browser-driven screenshots, and multi-agent code review — but the agent graded its own work, the author still had to load each full diff into his head, and good-looking passing changes were thrown away because tools can't say whether complexity is worth adding (Hyrum's Law makes unshipping harder than shipping).

## 2. [[wiki/02-not-all-agents-write-code|Not all agents write code]]

**In one sentence:** The most useful agents often don't write code at all — investigation, red-teaming, and deployment-watching agents plus up-front system engineering matter more than the code itself, as the vibe-coded collapse of botd proves.

## Key points

- An agent is just a model in a loop with tools, so the loop never changes and the tools decide what the agent can be — a dev agent needs a full computer (shell, compilers, browsers, install freedom).
- Tool risk comes from combinations, not single tools: private data + untrusted content + external communication together is Simon Willison's "lethal trifecta," so the author isolates environments and watches combinations rather than minimizing tools blindly.
- Investigation agents work from the customer's verbatim report queried against ClickHouse logs plus code reading, and the output is evidence for a human decision — sometimes the fix is a doc or email, not code.
- The red-team agent ("try to break into our systems") found open network paths thought to be restricted and showed exactly how they were reachable, so they were patched before outsiders noticed.
- The deploy-watcher Athena reads diff, metrics, and logs during wave rollouts and once correctly continued deploying to other machines after diagnosing a failure as infrastructure, not the new code.
- Agentic engineering means designing architecture, interfaces, constraints, and tradeoffs before accepting code, otherwise you inherit a brand-new legacy codebase — "that's vibe coding."
- Engineering hygiene amplifies under agents: behavior/contract/property tests beat implementation-mirroring unit tests, migrations/state handling is the hard part, tolerated bad patterns become templates, and cheap bespoke tools (e.g. a new linter) should encode lessons.

## The argument in five moves

1. The author's edge was a hard-won whole-system mental model, but hand-writing was the bottleneck — so the February no-code-by-hand rule forced reps with agents once Claude Code and stronger models made agent output buildable.
2. Idle time between agent tasks drove accidental parallelism from one agent to ~20 VMs, with isolation evolving from a shared box through worktrees, AGENTS.md patches, and containers to one disposable exe.dev VM per task managed by botd.
3. botd made off-laptop, mobile-first, conversation-preserving scale workable — YOLO inside disposable VMs, credentials proxied, writes limited — yet validation (agent-run tests, CI, screenshots, peer-agent review) still left the author responsible for every unfamiliar diff, and green builds still got discarded when the change wasn't worth shipping.
4. The highest-leverage agents don't write code at all: investigators reconstructing verbatim customer reports from logs, a red-team agent breaking assumed-closed network paths, and the Athena deploy-watcher continuing wave rollouts through infrastructure failures — all enabled by treating tools, not the loop, as what defines an agent and by watching lethal-trifecta combinations.
5. Code is cheap but systems carry state, so agentic engineering — architecture, interfaces, constraints, tradeoffs, behavior/contract/property tests, migrations, hygiene, bespoke linters — must precede the code, lest vibe coding produce a brand-new legacy codebase, as botd's own collapse proved.
6. The loop moved up a level: line-by-line familiarity was traded for queryable conversation history in SQLite, failures stayed cheap and numerous, and iteration shifted from code to prompts, designs, and whole features — he stopped writing code by hand without stopping engineering.
