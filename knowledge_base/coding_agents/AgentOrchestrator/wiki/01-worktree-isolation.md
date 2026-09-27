> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Worktree Isolation

**In one sentence:** Every AO worker session gets its own isolated git worktree plus branch (or a managed Scratch directory), so parallel agents never share a checkout and conflicts are prevented by construction rather than resolved after the fact.

## Key points

- Each worker session in a Git project owns a fresh git worktree + branch, so two agents can never overwrite each other's files.
- Multi-repo workspace projects materialize one root worktree plus registered child worktrees, keeping cross-repo tasks isolated as a unit.
- Scratch sessions use an AO-managed directory with no branch or PR operations, for work that is not yet tied to a repository.
- Cleanup is conservative by design: `ao session kill` never force-deletes a dirty registered worktree, and `ao session cleanup --dry-run` previews reclaimable sessions first.
- Restart reuses the same record and the same worktree: `ao session restore` relaunches a terminated session in place whenever the adapter supports recovery.
- The mental model is explicit in testimonials: agents' work lives in separate worktrees, so the human always keeps the merge decision.
- Only one agent interface is live per session at a time (tmux/conpty terminal or runtime-less Chat controller), with drained handoffs between them.

---

## 1. The isolation model

AO defines three workspace kinds, chosen automatically from the project type:

| Project kind | What the session gets | Branch / PR ops |
|---|---|---|
| Git repo | Fresh git worktree + new branch | Yes |
| Multi-repo workspace | Root worktree + registered child worktrees | Yes, per repo |
| Scratch | AO-managed directory | No — plain files only |

A worktree here means a separate working copy of the repository (Git feature: one repo, several checked-out directories, each on its own branch). The worker agent runs only inside its own directory. There is no shared checkout, no shared branch, and no shared file lock to get wrong.

## 2. Why this is the primary safety mechanism

Running several coding agents in one checkout produces the failure modes the fleet track knows well: mixed files and branches, lost track of who does what, review comments landing in the wrong conversation, merge conflicts discovered late. AO pushes all of that out of the shared space:

1. File writes cannot collide — different directories.
2. Branch state cannot collide — different branches.
3. Attribution cannot blur — every worktree belongs to exactly one session, and every session owns exactly one PR (see `02-one-pr-per-agent-flow`).

The testimonial quoted in the docs states the mental model directly: thinking of the agents' work as separate git worktrees keeps the operator calm, because the decision to merge a branch stays with the human.

## 3. Lifecycle of a worktree

- **Create:** `ao spawn` (or the desktop start-session action) creates the worktree + branch from the project's base branch and records it against the session.
- **Work:** the agent edits only inside its worktree; setup commands, symlinks, and env vars from typed project config are applied at creation.
- **Kill:** `ao session kill` terminates the agent but preserves a dirty worktree — uncommitted work is never silently discarded.
- **Reclaim:** `ao session cleanup [--dry-run]` lists or removes only eligible terminated sessions; `--dry-run` previews first.
- **Restore:** `ao session restore <id>` relaunches a terminated session reusing the same session record and the same worktree, provided the harness CLI is still installed and authenticated and the adapter supports recovery.

## 4. Scratch sessions

Scratch projects skip version control entirely: the session gets an AO-managed directory with no branch and no PR operations. This covers spikes, explorations, and orchestrator planning notes that should not create branches. A Scratch session can still be promoted by starting a real session from its output, but nothing about Scratch auto-creates Git state.

## 5. One live interface per session

Isolation is not only files — it is also control. A session has exactly one live agent interface at a time:

- **TUI (Terminal UI):** the harness's native terminal screen, run through tmux (macOS/Linux) or ConPTY (Windows).
- **Chat:** a structured, runtime-less controller with durable provider-identified conversations (turns, approvals, usage, compaction, rollback) — available only for the four Chat-capable harnesses.

Compatible Claude Code and Codex sessions can switch Chat ↔ TUI without changing session or worktree. AO drains or interrupts the old controller before committing the replacement (generation counter + checkpoints + queued messages), so two controllers are never live at once and cannot issue conflicting tool calls.

## 6. What isolation does not cover

- Two sessions can still edit the same logical file on different branches — the merge conflict surfaces later, at PR time, where the SCM observer detects unmergeable state and routes a rebase request (see `04-ci-review-feedback-routing`).
- Isolation says nothing about in-flight tool-call durability: there is no documented checkpoint-resume of individual agent steps; durability is at the session/worktree/conversation level.
- Blocked sessions (waiting on an approval or permission prompt) hold their worktree until a human answers; lifecycle automation is deliberately withheld while blocked.

**Covers:** docs workspaces page, architecture sessions-and-worktrees section, CLI session kill/restore/cleanup, troubleshooting recovery, Chat-vs-TUI interface model.
