> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Micro-patterns: ralphy, subtask, swarm-protocol, wit

**In one sentence:** Four tiny open tools each solve one chore the bare Ralph loop leaves out — ralphy (run the loop on any CLI), subtask (fan work out into worktrees), swarm-protocol (claim work and prove liveness), and wit (lock single functions before writing).

## Key points

- ralphy (michaelshimeles) is the multi-harness Ralph: one bash script looping Claude Code, Codex, OpenCode, Cursor, Qwen, or Droid until done — the "runs anywhere" Ralph.
- subtask is a Claude Skill that runs tasks through subagents in git worktrees with the workflow "one parent, N file-owned children": cost-neutral fan-out where the human still coordinates.
- swarm-protocol is a coordination protocol over MCP (Model Context Protocol — a standard way for agents to call tools): claim work, detect file conflicts, heartbeat, hand off across sessions, so the workflow is a lease on a work item, not a graph.
- wit is an intent-plus-lock protocol: agents declare intents and acquire symbol-level locks (parsed via Tree-sitter, a code-parser library) before writing, warning about conflicts before they happen instead of at merge.
- Together they form a conflict-granularity ladder: worktrees (file-set isolation, conflicts at merge) → work-claim leases with heartbeats (who works on what) → symbol-level locks (warn before two agents touch the same function).
- Multi-harness breadth leaders (Emdash 34 CLIs, Orca 25+, Bernstein 49 adapters) vs narrow-but-polished (Conductor) vs harness-agnostic-by-construction (bare Ralph bash, ralphy's 6-harness loop).
- Mature setups route by cost: plan expensive, execute cheap, verify independently (OMC claims 30–50% savings from smart routing; OmO routes chores to local Ollama models).

---

## 1. ralphy — the Ralph that runs anywhere

ralphy (michaelshimeles) is the multi-harness Ralph: one bash script looping Claude Code, Codex, OpenCode, Cursor, Qwen, or Droid until done. Alongside snarktank/ralph (~21k stars) and vercel-labs/ralph-loop-agent it is the most starred packaging of the pattern. The Ralph core stays harness-agnostic by construction — bash around *any* headless CLI — so thinness is the feature: zero harness lock-in, but also zero harness help (you wire flags like `--dangerously-skip-permissions` yourself). ralphy keeps the thinness and adds the backend menu.

## 2. subtask — worktree fan-out as a Skill

subtask is a Claude Skill that runs tasks through subagents in git worktrees — the workflow is "one parent, N file-owned children", cost-neutral, human-coordinated. It adds no scheduler and no verifier: isolation comes from worktrees (same primitive as Conductor), decomposition comes from the human's file-ownership mapping, and review comes from the human too. Its value is packaging: fan-out without new infrastructure.

## 3. swarm-protocol — leases and heartbeats over MCP

swarm-protocol is a coordination protocol over MCP: claim work, detect file conflicts, heartbeat, hand off across sessions. The workflow is a *lease on a work item*, not a graph. It solves *who works on what* (atomic claims on work items, heartbeats proving liveness, hand-off across sessions) but says nothing about *what files they touch* — pair it with worktree isolation for files and wit-style locks for symbols.

## 4. wit — function-level locks before writing

wit is an intent + lock protocol: agents declare intents and acquire symbol-level locks (parsed via Tree-sitter, the code-grammar parser) before writing — the workflow is defined by what is *locked*, not by a plan. Tree-sitter AST (abstract syntax tree — the code's grammatical structure) parsing lets agents lock individual *functions*, declaring intent and getting conflict warnings *before* writing. It is the finest granularity in the landscape and the only pattern that prevents same-file collisions rather than detecting them at merge.

## 5. Reading them together

Conflict handling across the four is a three-rung ladder, finest last: (1) worktree/branch isolation — free during work, conflicts at merge; (2) work-claim + heartbeat leases — who works on what; (3) symbol-level locks — what functions are touched. Multi-harness support follows the same thin-to-wide arc: Ralph/ralphy thin and agnostic, Conductor narrow and polished, orchestrator tier (Emdash/Orca/Superset) widest. And nobody runs *one* harness everywhere: the mature setups route by cost — plan expensive, execute cheap, verify independently (DEV piece's "route by cost" rule; OMC's 30–50% savings claim from smart routing).

**Covers:** ralphy multi-harness loop, subtask worktree fan-out Skill, swarm-protocol MCP leases and heartbeats, wit Tree-sitter function locks, conflict-granularity ladder, multi-harness breadth and cost routing; sources: awesome-agent-orchestrators list, Augment Code roundup, OpenAlternative and DEV comparisons.
