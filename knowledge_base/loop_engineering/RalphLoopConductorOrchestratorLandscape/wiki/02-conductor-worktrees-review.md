> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Conductor: worktrees plus review dashboard

**In one sentence:** Conductor (Melty Labs, closed-source Mac app) runs 3–8 parallel agents in isolated git worktrees behind a diff-first review UI where the human is the scheduler, merger, and quality gate.

## Key points

- Conductor (Melty Labs, YC S24, closed-source Mac app) = one isolated git worktree per agent plus visual dashboard plus diff-first review UI plus checkpoints and rollback; the human is the scheduler, merger, and quality gate.
- One isolated git worktree per agent means each agent owns its own working directory on its own branch, so there are no merge conflicts during parallel work; worktrees with no changes auto-clean and ones with changes persist for review.
- The dashboard answers "who is working on what", but the product is the review flow: file-by-file diffs, checkpoints, rollback, PR creation — review throughput is the whole product.
- In supervision-ladder terms (L0–L4) Conductor is L0, "you are the loop": no programmatic surface, no API, macOS only, closed source, and it does not decompose work, assign tasks, or verify quality itself.
- Multi-model compare runs parallel attempts (including different models) and keeps the best.
- The Conductor name covers three different tools: conductor.build (Melty, closed Mac app, diff-first L0 review cockpit), Code Conductor (MIT, GitHub-issue queue), and Microsoft Conductor (MIT, YAML workflows with parallel groups — strongest long-term bet).
- Worktrees give isolation for free but not decomposition: two agents editing the same file in different worktrees still conflict at merge, so human file-ownership mapping ("no two agents own the same file") is the manual fix.

---

## 1. Four pillars

Conductor (by Melty Labs, YC S24) is the polished Tier-2 "local orchestrator": your machine spawns 3–8 parallel agents, you stay in the loop with dashboards, diff review, and merge control. Its design has four pillars:

1. **One isolated git worktree per agent.** Each agent gets its own working directory on its own branch — no merge conflicts *during* parallel work. (Since Claude Code v2.1.49 this is vendor-native: `claude --worktree feature-auth`.) Worktrees with no changes auto-clean; ones with changes persist for review.
2. **Diff-first review UI.** The dashboard answers "who is working on what", but the product is the review flow: file-by-file diffs, checkpoints, rollback, PR creation. Review throughput is the whole product.
3. **Human as scheduler and merger.** Conductor does not decompose work, assign tasks, or verify quality itself — you do. In supervision-ladder terms (L0–L4, from the DEV comparison): Conductor is L0, "you are the loop". No programmatic surface, no API, macOS only, closed source.
4. **Multi-model compare:** run parallel attempts (including different models) and keep the best.

## 2. The three Conductors — do not confuse them

Per the Augment Code roundup: **conductor.build** (Melty, closed, Mac desktop, reviewed here) vs **Code Conductor** (MIT, GitHub-native CLI where agents claim `conductor:task`-labeled issues) vs **Microsoft Conductor** (MIT, YAML-defined multi-agent workflows with static/dynamic parallel groups, sub-workflows, conditional routing, web dashboard — the most credible long-term bet of the three). Only the first is the "review cockpit"; the other two are workflow systems covered on the fleet-comparison page.

## 3. Worktrees: what isolation buys and what it does not

Worktree/branch isolation (Conductor, subtask, Claude Squad, fleet) gives each agent a directory plus branch: free isolation during work, with conflicts surfacing only at merge. Limitation, per Osmani: worktrees give isolation for free but *not* decomposition — two agents editing the same file in different worktrees still conflict at merge. Human file-ownership mapping ("no two agents own the same file") is the manual fix. No restarts either: a dead agent is a dead pane and the human respawns it — at L0 the human is the watchdog.

## 4. Fleet parallel

Fleet *is* a Tier-2 local orchestrator in the same sense — per-task worktrees on `fleet/<task_id>` branches, merge validation, GC (garbage collection) of stale worktrees — but headless and queue-driven rather than dashboard-driven: beads (tasks) are claimed by workers instead of agents being watched by a human. Fleet automated the dispatch; Conductor perfected the review.

**Covers:** Conductor four pillars (worktrees, diff-first review, human-as-scheduler, multi-model compare), three-Conductor disambiguation, worktree isolation limits and manual decomposition fix, fleet headless parallel; sources: htdocs.dev primary, Augment Code roundup, DEV supervision ladder, fleet worktree sources.
