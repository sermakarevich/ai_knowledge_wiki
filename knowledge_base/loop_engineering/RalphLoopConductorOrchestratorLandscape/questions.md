---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Ralph loop + Conductor + orchestrator landscape

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What are the three components of the Ralph loop plus its one rule?

> [!tip]- Answer
> A prompt file with goal + definition of done, a shell loop re-running the same agent, and a completion check (tests/COMPLETE tag/all PRD stories pass) — plus the one-item rule: one task per pass, then commit and exit. See [[wiki/01-ralph-loop-mechanics|Ralph loop mechanics]].

### Q2. Why does wiping the context window every pass *improve* results instead of hurting them?

> [!tip]- Answer
> Long sessions rot as the window fills with the agent's own chatter and early instructions are forgotten; refusing conversational memory and keeping truth in files + git avoids that decay. See [[wiki/01-ralph-loop-mechanics|Ralph loop mechanics]].

### Q3. What work is the Ralph loop fit for, and what must its success criteria look like?

> [!tip]- Answer
> Large, well-specified, mechanically verifiable work (migrations, coverage backfill, refactors) — and criteria must be numbers (tests, lint, types, coverage), not judgments. See [[wiki/01-ralph-loop-mechanics|Ralph loop mechanics]].

### Q4. What are Conductor's four design pillars, and who plays scheduler and merger?

> [!tip]- Answer
> One worktree per agent, diff-first review UI, human as scheduler/merger, multi-model compare — the human does the scheduling, merging, and quality gating (L0, "you are the loop"). See [[wiki/02-conductor-worktrees-review|Conductor: worktrees plus review dashboard]].

### Q5. The name "Conductor" covers three different tools — name them and say which is the long-term bet.

> [!tip]- Answer
> conductor.build (Melty, closed Mac review cockpit), Code Conductor (MIT, GitHub-issue queue), Microsoft Conductor (MIT, YAML workflows) — Microsoft Conductor is the most credible long-term bet. See [[wiki/02-conductor-worktrees-review|Conductor: worktrees plus review dashboard]].

### Q6. What does ralphy add over the bare Ralph one-liner, and what does it deliberately not add?

> [!tip]- Answer
> It adds a multi-harness backend menu (Claude Code, Codex, OpenCode, Cursor, Qwen, Droid) in one bash script; it keeps zero lock-in and adds no scheduler or verifier. See [[wiki/03-micro-patterns|Micro-patterns]].

### Q7. Contrast swarm-protocol and wit: what does each guard, and at what granularity?

> [!tip]- Answer
> swarm-protocol guards *who works on what* via MCP work-claim leases + heartbeats (work-item granularity); wit guards *what code gets touched* via declared intents + Tree-sitter function-level locks with pre-write warnings. See [[wiki/03-micro-patterns|Micro-patterns]].

### Q8. State fleet's loop-vs-goal gap in one sentence: what does fleet know that Ralph does not, and vice versa?

> [!tip]- Answer
> Fleet knows what "failed" means (typed outcomes → CLOSE/RELEASE/BLOCK with caps and backoff) but has no per-task executable done-predicate; Ralph knows what "done" means (a runnable check) but classifies no failures. See [[wiki/04-fleet-comparison|Fleet comparison]].

### Q9. Name three of the seven borrowable ideas and the single highest-value import.

> [!tip]- Answer
> Any three of: completion-check gates, Janitor reviewer, stuck-iteration kill + reassign, YAML workflow option, work-claim heartbeats, function-level conflict warnings, human-approved memory — with completion-checks-as-code the top import. See [[wiki/04-fleet-comparison|Fleet comparison]].

### Q10. What is the weakest link in this landscape's evidence, and how should it change your adoption decision?

> [!tip]- Answer
> Cost/win claims are advocate-supplied anecdotes (overnight $297–$800 runs, 30–50% routing savings) with no controlled benchmarks and survivor bias, plus a three-Conductor naming mess — so trial the cheap mechanical gates first and treat savings stories as hypotheses. See [[critical_thinking|Critical Analysis]].
