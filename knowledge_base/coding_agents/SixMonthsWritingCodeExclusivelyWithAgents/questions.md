---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Six Months of Writing Code Exclusively With Agents - exe.dev blog

### Q1. What was the February rule, and what were you supposed to do when an agent got stuck instead of finishing the code yourself?
> [!tip]- Answer
> The rule was no code by hand for six months, broken only once for three minutes. When an agent got stuck, the discipline was to fix what it was missing — the prompts, tools, or environment — instead of typing the fix. The logic mirrors learning to code: reps of real work, failure, and iteration build understanding of agents. See [[wiki/01-the-system-lived-in-my-head|The system lived in my head]].

### Q2. How did agent isolation evolve from one shared dev box to per-task VMs, and what did each step fix?
> [!tip]- Answer
> Sharing one box caused file/Git collisions plus dependency, port, and process fights. Worktrees fixed only Git collisions, AGENTS.md patches (random ports, ephemeral databases) burned context on collision-avoidance, and containers separated ports and state but leaked to whatever the laptop could reach while requiring the laptop to stay awake. The endpoint was one exe.dev Linux VM per task over SSH/HTTPS, so work survived closing the laptop. See [[wiki/01-the-system-lived-in-my-head|The system lived in my head]].

### Q3. What are botd's three design rules and its safety model for running agents in YOLO mode?
> [!tip]- Answer
> Botd's rules are run off-laptop, mobile-first with no terminal required, and preserve every conversation for later analysis. YOLO mode (unrestricted bash, installs, services) was acceptable because each agent sat in an isolated disposable VM where a trashed environment cost nothing but the VM. External risk was contained by proxying credentials so secrets never lived in the VM and limiting writes to test environments. See [[wiki/01-the-system-lived-in-my-head|The system lived in my head]].

### Q4. Why did passing tests, screenshots, and peer-agent reviews still lead to discarding changes, and what closed the loop on shipping?
> [!tip]- Answer
> The agent graded its own work and could confidently build the wrong thing, so the author still had to load each unfamiliar diff into his head before merging. Even green, good-looking changes were thrown away when nobody needed them, they duplicated an existing path, or a small convenience added years of complexity. The closing claim is that tools say whether a change works, never whether it is worth adding — shipping got easy, deciding what to ship got important. See [[wiki/01-the-system-lived-in-my-head|The system lived in my head]].

### Q5. What are the three non-coding agent roles, and what did each one concretely achieve?
> [!tip]- Answer
> Investigation agents reconstruct incidents from the customer's verbatim report queried against ClickHouse logs plus code reading, with the human deciding the fix (sometimes a doc or email, not code). The red-team agent, told only to break in, found open network paths believed restricted and showed exactly how they were reachable, so they were patched first. The Athena deploy-watcher reads diff, metrics, and logs during wave rollouts and once correctly continued deploying through a failure it diagnosed as infrastructure rather than bad code. See [[wiki/02-not-all-agents-write-code|Not all agents write code]].

### Q6. What distinguishes agentic engineering from vibe coding, and which engineering lessons amplify under agents?
> [!tip]- Answer
> Agentic engineering means working with the agent on architecture, interfaces, constraints, and tradeoffs before accepting code so you understand what you own; accepting a blind whole-system design inherits a brand-new legacy codebase, which is vibe coding. Testing shifts to behavior, contract, and property tests that survive rewrites instead of implementation-mirroring unit tests. Tolerated bad patterns become templates for the next hundred changes, migrations and state handling stay the hard part, and cheap bespoke tools like a new linter should encode each lesson. See [[wiki/02-not-all-agents-write-code|Not all agents write code]].

### Q7. Your team proposes vibe-coding an internal orchestration tool with agents and skipping design review to ship faster — should you approve it?
> [!tip]- Answer
> Reject the skip: botd's collapse shows exactly this failure, as an entirely vibe-coded harness with an unread architecture crumbled under its own weight when its genuinely hard core (driving every model family through native harnesses) needed changes. Recommend agentic engineering instead — agree on architecture, interfaces, and contracts up front, preserve full conversation history in queryable storage, and let agents iterate within those constraints. The data outlived the tool, but only the design discipline would have kept the tool alive. See [[wiki/02-not-all-agents-write-code|Not all agents write code]].
