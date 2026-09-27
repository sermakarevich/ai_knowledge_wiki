> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Claude Squad

## Claims vs. evidence
- "No conflicts between parallel agents" — **strong**. Each instance gets its own git worktree path plus its own branch from pinned `HEAD` (`session/git/worktree_ops.go:101-112`), so two agents never share a working tree, index, or `HEAD`.
- The only shared state is the branch namespace, partitioned by per-session branch name plus hex timestamp-suffixed directory (`session/git/worktree.go:66-68`).
- Fresh sessions additionally start from the pinned commit hash rather than inheriting uncommitted changes from another worktree (`session/git/worktree_ops.go:104-107`).
- Pre-existing-branch sessions set `isExistingBranch=true` so cleanup keeps the branch (`session/git/worktree.go:95-108`).
- "Multi-harness support (Claude, Codex, Aider, Gemini, Amp)" — **weak**. The program is a plain shell string passed verbatim into `tmux new-session` (`session/tmux/tmux.go:93-102`).
- Only three constants exist (`ProgramClaude/Aider/Gemini` at `session/tmux/tmux.go:22-25`) and only for substring prompt/trust matching (`session/tmux/tmux.go:253-260`, `session/tmux/tmux.go:161-184`).
- Codex/Amp launch but get generic trust handling and no autoyes prompt detection, so the claim overstates the code.
- "Background tasks / autoyes daemon" — **weak**. The daemon is a same-binary `--daemon` poll loop calling `HasUpdated()` then `TapEnter()` (`daemon/daemon.go:48-60`).
- It is stopped whenever the foreground TUI starts (`main.go:72-74`) and re-launched on exit (`main.go:64-69`), coordinated only by a `daemon.pid` file (`daemon/daemon.go:115-167`).
- It injects Enter on fragile substrings with no capability model, so it is assisted foreground work, not autonomous background execution.
- "Easy restore after restart" — **suggestive**. Live sessions re-attach via `Restore()` and dead ones park as `Paused` (`session/instance.go:248-263`), which is good design.
- But one corrupt JSON row aborts the whole load (`session/storage.go:76-83`) and `newHome` exits the process (`app/app.go:135-150`), so a single bad row defeats the feature.

## Genuinely new vs. repackaged
- Novel composition: one tmux session plus one git worktree plus one branch per agent, managed from a single Bubble Tea TUI with single-key ops (`keys/keys.go:38-58`, `app/app.go:609-814`).
- No prior tool packaged exactly that loop for agent CLIs; the finalizer-plus-background-`Start` creation path (`app/app.go:923`) keeps the event loop responsive during slow setup.
- Novel use of `capture-pane` as attention polling: `tmux capture-pane -p -e -J` plus SHA-256 hash-compare in `HasUpdated()` (`session/tmux/tmux.go:246-267`) gives agent-agnostic progress detection.
- This needs zero worker cooperation — no hooks, no wrappers — which is the key insight worth copying.
- Repackaged: tmux session managers and tools like tmuxp already did named-session create/attach/kill; git-worktree CLI flows already did per-branch isolation.
- Repackaged: `CleanupSessions` via `tmux ls` regex (`session/tmux/tmux.go:499-526`) is a standard pattern, and even its comment still says the stale `session-` prefix (`session/tmux/tmux.go:498`).
- Repackaged: trust-prompt auto-answer (`session/tmux/tmux.go:161-184`) and profile selection from config (`config/config.go:61-82`) are thin string maps, not a harness abstraction.

## Weaknesses and blind spots
- `LoadInstances` aborts on the first bad row (`session/storage.go:76-83`) and `newHome` calls `os.Exit(1)` on load failure (`app/app.go:135-150`): one corrupt row hides all instances.
- Config/state load failures instead degrade silently to defaults plus a log line (`config/config.go:155-185`), so the system is strict where it should be lenient and lenient where it should warn.
- No `tmux` binary guard: every primitive calls `exec.Command("tmux", ...)` directly (`session/tmux/tmux.go:102`) with no `LookPath` check.
- Missing tmux therefore surfaces as a confusing 2 s timeout (`session/tmux/tmux.go:117-133`), not a clear prerequisite error.
- Unstarted draft rows are never persisted (`session/storage.go:57-64`); a crash or quit during naming loses the row silently (`app/app.go:468`).
- Hard cap `GlobalInstanceLimit = 10` (`app/app.go:24`), enforced at both creation sites (`app/app.go:613-644`); no queue or overflow handling.
- Autoyes matching is substring-fragile: `"No, and tell Claude what to do differently"`, `"(Y)es/(N)o"`, `"Yes, allow once"` (`session/tmux/tmux.go:253-260`) break on any CLI version or locale change.
- Unknown harnesses silently get no detection at all, and a false-positive substring means an unintended Enter injection.
- Push hard-requires `gh` plus `gh auth status` (`session/git/util.go:36-49`); without it, `PushChanges` fails even though plain `git push` would work (`session/git/worktree_git.go:71-126`).
- Windows support is second-class: size polling every 250 ms (`session/tmux/tmux_windows.go:30-56`) vs Unix SIGWINCH signal debounce (`session/tmux/tmux_unix.go:16-64`); `Detach` panics on failure (`session/tmux/tmux.go:401-416`).
- Test coverage is thin on orchestration: sanitization, diff parsing, and tmux CLI strings are pinned (`session/tmux/tmux_test.go:52-88`), but `app.go` dispatch, pause/resume races, and daemon polling have no equivalent harness.

## Applicability
- Works: solo developer, git repositories, tmux-friendly terminal, running 2-8 long-lived agent CLIs with manual review before push.
- The diff-against-pinned-base tab (`session/git/diff.go:26-52`) plus confirmation-gated push (`app/app.go:716-738`) fits that review loop well.
- Fails: non-git projects (hard `IsGitRepo` guard in `main.go:42-50`), headless/CI use (TUI-first, daemon is an appendage), teams needing audit trails, permissions, or reproducible runs.
- Also fails beyond 10 workers, on machines without tmux/gh, and anywhere Enter-injection auto-approval is unacceptable policy.
- **Relevance to my work**
  - Agentic systems / Fleet execution floor — **trial**: borrow worktree-per-worker, capture-pane polling, and reconcile-on-restart (`session/instance.go:248-263`) directly.
  - AI/ML (artificial intelligence / machine learning) engineering with notebooks or non-git data dirs — **ignore**: git-repo requirement plus `gh` auth gate add friction with no benefit.
  - Elisity data platform work needing auditability — **ignore**: `commit --no-verify` pushes with timestamped `[claudesquad]` messages (`app/app.go:716-738`) leave no review record or policy hook.
  - Multi-model routing experiments — **trial**: `{name, program}` profiles (`config/config.go:61-82`) give one-line harness swaps, good enough for quick comparison runs.

## What this changes
- If the claims hold, parallel agent work stops needing manual branch/worktree bookkeeping: isolation becomes the default, and `reset` (`main.go:80-115`) bounds the cost of stuck agents.
- Passive `capture-pane` observability makes progress monitoring harness-agnostic; per-harness plugins become unnecessary for basic supervision.
- Pinned-base diffs with intent-to-add (`session/git/diff.go:26-52`) make review-before-push cheap enough to enforce on every worker branch.
- Second-order effect: orchestration moves up a layer — Fleet-style systems keep scheduling, messaging, and evaluation, while spawn/isolate/observe/push collapses into commodity plumbing.
- The risk is normalizing Enter-injection auto-approval as "autonomy": cheap yes-saying scales accidents as fast as output.

## Verdict
Claude Squad is well-built plumbing, not a platform: its worktree-plus-tmux isolation is structurally sound, but config, daemon, and multi-harness claims are thin string passthrough with fragile failure modes. It earns its place as a solo operator console and as a source of proven patterns for Fleet, including worktree-per-worker, capture-pane polling, and reconcile-on-restart. The fatal-load and substring-matching weaknesses rule out team or headless use without fixes. For now the right move is **trial** — worktree-per-worker plus capture-pane reconciliation is worth borrowing.
