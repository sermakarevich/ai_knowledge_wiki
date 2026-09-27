---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: GasTown

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. How does GasTown store polecat identity, and how is that different from its live session?
> [!tip]- Answer
> Polecat identity is persistent and lives in the beads database as an agent bead ID plus an assignee string, derived at query time by cross-checking hooked beads against tmux liveness. The live tmux session is ephemeral: it is killed on clean completion while identity, branch, and work history survive. There is no per-polecat state file. See [[wiki/01-orchestrator-town-rig-polecat|Orchestrator Core]].

### Q2. What is stored in `.polecat-checkpoint.json`, and what happens to it when a worker crashes?
> [!tip]- Answer
> The checkpoint stores the git-observable half of state: molecule, step, hooked bead, modified files, branch, last commit, timestamp, and session ID. Nobody detects the crash eagerly; the next session's startup hook re-reads the file and re-displays it as advisory context when it is parseable and under 24 hours old. Nothing is auto-applied, so commits and files survive while in-memory reasoning is lost. See [[wiki/02-worktrees-hooks-persistence|Worktrees and Persistence]].

### Q3. How does Mountain stall detection decide to skip a stuck issue in a convoy?
> [!tip]- Answer
> A mountain is a convoy bead carrying the `mountain` label, and each polecat failure on its hooked bead increments a failure-count label. At three failures the issue is set to blocked with a skipped label, which drops it from the ready front so the convoy feeder grinds around it. Recovery is manual by reopening the issue and removing the skipped label. See [[wiki/03-beads-ledger-convoy|Beads and Convoys]].

### Q4. How does GasTown add support for a new coder harness without writing a new adapter class?
> [!tip]- Answer
> Each harness is one data row in the agent registry: a preset entry declaring the CLI binary, autonomous-mode flags, resume style, hooks provider, and prompt mode, merged from built-ins with town or rig JSON overrides. Launch isargv construction from that row, not a plugin call, so thirteen coders ship as table entries. Adding one means adding a JSON preset plus a hooks template, not a Go package. See [[wiki/04-harness-adapters|Harness Adapters]].

### Q5. What survives a daemon-driven worker restart, and what does the restart re-provision?
> [!tip]- Answer
> Restart is kill-then-recreate of the tmux pane under exponential backoff with a crash-loop budget, while beads rows and git worktrees survive untouched. Re-provisioned are the session itself, the startup command rebuilt from role config, the identity environment, theme, and respawn hooks. Lost are the in-flight conversation context and any un-checkpointed edits. See [[wiki/05-daemon-scheduler-sessions|Runtime Supervision]].

### Q6. Why is mail durable while `mq` is not transport, and how do handoffs reuse mail?
> [!tip]- Answer
> Mail is durable beads issues with delivery tracking, routing, fan-out, and tmux nudges, while the merge queue only generates merge-request identifiers. Handoffs are self-addressed mail flipped to hooked status so the successor session auto-loads them, with stale hooked beads closed first. Handoff mail is never ephemeral so hook queries can find it. See [[wiki/06-messaging-coordination|Messaging]].

### Q7. Why do `gt sling`, `gt hook`, and `gt handoff` exist as three commands, and when is each correct?
> [!tip]- Answer
> Hook attaches work to an agent hook without starting it, sling attaches plus starts now with auto-spawn and convoy tracking, and handoff attaches plus restarts into a fresh session carrying context forward. The split separates queuing work, dispatching work, and cycling sessions without losing the hook pointer. Using sling for queued future work would spawn capacity too early. See [[wiki/07-cli-tui-web-config|CLI and Config]].

### Q8. Why does the refinery abort on merge conflict instead of auto-merging, and where does the conflict go?
> [!tip]- Answer
> The refinery rehearses each polecat branch merge and aborts immediately so the repository never stays in a conflicted state, preserving the branch and merge-request bead. It files a conflict-resolution task and returns structured rebase instructions to the worker through protocol mail. The worker rebases, force-pushes, and resubmits rather than any automation editing conflicted files. See [[wiki/08-safety-workflow-plugins|Safety and Workflow]].

### Q9. Which five GasTown patterns does the targeted analysis mark as directly transferable to fleet?
> [!tip]- Answer
> The analysis names the harness registry, the checkpoint plus lazy-recovery pair, the restart backoff budget, the worktree-per-worker plus rehearsal-abort merge rule, and the file-based nudge queue. Each maps to a small fleet change because fleet already mirrors the town, rig, and isolated-worker shape. The common thread is durable state outside the agent process with advisory recovery inside it. See [[wiki/targeted|Fleet Transfer]].

### Q10. Why do concurrent polecat spawns use nested file locks plus atomic temp-and-rename writes?
> [!tip]- Answer
> Every CLI invocation is a separate process, so in-process mutexes cannot serialize allocation; the pool lock is held across name allocation plus directory creation to close the double-allocate race, with the per-worker lock nested inside. Atomic temp-plus-rename writes guarantee readers of shared settings files always see one complete writer even under parallel spawns. The checkpoint writer is the known exception that still uses direct writes. See [[wiki/02-worktrees-hooks-persistence|Worktrees and Persistence]].

### Q11. How would you apply the GasTown harness registry to fleet's Python orchestrator for a new coder?
> [!tip]- Answer
> Replace per-coder spawn code with one Python dict row per harness holding command, args, env, resume flag and style, and hooks path, merged from built-ins with per-project JSON overrides. Add a single command-builder function that renders argv and resume commands from the row, plus a wrapper that prints role context before exec for weak-hooks harnesses. A new coder then ships as config, with no orchestrator code change. See [[wiki/04-harness-adapters|Harness Adapters]].

### Q12. Is GasTown's lazy crash recovery plus refinery-gated merging the right tradeoff for fleet's Python orchestrator?
> [!tip]- Answer
> Judge it against failure cost: lazy recovery is cheap and correct when beads plus git already persist work, but it loses in-memory reasoning and leans on fresh checkpoints and WIP commits. Refinery gating keeps shared branches green at the price of merge latency and rework loops for conflicted workers. Recommend where fleet should copy, adapt, or reject each half given its scale and conflict rate. See [[critical_thinking]].
