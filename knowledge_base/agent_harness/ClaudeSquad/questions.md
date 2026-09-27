---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Claude Squad

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. How does the Claude Squad binary enter, and what blocks startup outside a git repo?

> [!tip]- Answer
> Entry is cobra `rootCmd.RunE` in `main.go`, which initializes logging, branches on hidden `--daemon`, enforces a git-repo guard, resolves the agent program, then calls `app.Run`. Outside a repo, `filepath.Abs(".")` plus `git.IsGitRepo` rejects startup with an error naming the invoked binary. See [[wiki/01-architecture-and-entry|Architecture and Entry Points]].

### Q2. What are the two phases of session creation, and what happens if `Start(true)` fails?

> [!tip]- Answer
> `NewInstance` only builds an unstarted record with an absolute path and `Status: Ready`, without touching git or tmux. `Start(true)` then creates the worktree/branch and starts the tmux session, with deferred `Kill()` cleanup on setup failure so a failed create leaves no record. See [[wiki/02-session-lifecycle|Session Lifecycle and State]].

### Q3. Why does restart reconciliation park dead tmux sessions as `Paused` instead of returning an error?

> [!tip]- Answer
> `newHome` reloads every persisted row and `Start(false)` calls `tmuxSession.Restore()` to re-attach live sessions. Because `LoadInstances` aborts on the first bad row, reporting one dead session as an error would hide all other instances, so dead ones park as `Paused` with branch and worktree intact for later `Resume`. See [[wiki/02-session-lifecycle|Session Lifecycle and State]].

### Q4. How is a tmux session named and spawned per instance, and how is its output observed?

> [!tip]- Answer
> Each instance maps 1:1 to `claudesquad_` plus sanitized title with whitespace stripped and `.` replaced by `_`. Spawn is `tmux new-session -d -s <name> -c <workdir> <program>`, and observation is `tmux capture-pane -p -e -J -t <name>` with an `-S/-E` variant for scrollback ranges. See [[wiki/03-tmux-backend|Tmux Backend and Autoyes Daemon]].

### Q5. How does the autoyes daemon decide when to press Enter, and how does it avoid clashing with the TUI?

> [!tip]- Answer
> On each `DaemonPollInterval` tick it calls `HasUpdated()` on started, unpaused instances, which hashes pane content with SHA-256 and matches per-program prompt substrings, then calls `TapEnter()` plus `UpdateDiffStats()`. The foreground TUI stops any inherited daemon before starting and launches a fresh detached copy on exit only when autoyes is on, coordinated via a `daemon.pid` file. See [[wiki/03-tmux-backend|Tmux Backend and Autoyes Daemon]].

### Q6. Where does each instance's worktree live, and how are branch names made safe?

> [!tip]- Answer
> Each instance gets `<configDir>/worktrees/<sanitized-branch>_<hex-nanotime>`, created from pinned `HEAD` so agents never share a working tree or inherit uncommitted changes. Branch names default to `BranchPrefix` plus session name, then sanitize by lowercasing, space-to-dash, stripping outside `[a-z0-9-_/.]`, collapsing dashes, and trimming edges. See [[wiki/04-git-worktree-isolation|Git Worktree Isolation and Review]].

### Q7. How does the review Diff include untracked files, and how does remote publish handle a missing `gh` path?

> [!tip]- Answer
> `Diff()` runs `git add -N .` for intent-to-add so untracked files appear, then diffs against `baseCommitSHA` counting `+`/`-` lines excluding `+++`/`---` headers. `PushChanges` commits dirty state with `--no-verify`, then tries `gh repo sync --source -b <branch>`, falls back to `git push -u origin <branch>`, with every `gh` path gated by binary presence plus `gh auth status`. See [[wiki/04-git-worktree-isolation|Git Worktree Isolation and Review]].

### Q8. What is the TUI layout and which single keys drive create, kill, push, checkout, and resume?

> [!tip]- Answer
> The Bubble Tea `home` model pairs a left session list with a right tabbed pane for Preview, Diff, and Terminal tabs, plus modal overlays and a bottom menu. Dispatch maps `n` new, `N` new-with-prompt, `D` kill, `p` push, `c` checkout/pause, `r` resume, `enter`/`o` attach, `tab` cycle tab, with `ctrl-q` as tmux-detach only inside attached sessions. See [[wiki/05-tui-and-keybindings|TUI Views and Keybindings]].

### Q9. Why does the no-adapter multi-harness design work, and what breaks for an unknown CLI?

> [!tip]- Answer
> It works because `default_program` or a named profile's `program` string travels untouched into `tmux new-session` as the trailing command, so any CLI launches with zero adapter code. For unknown harnesses like codex or amp, launch succeeds but prompt and trust-screen substring matching silently misses, so autoyes and trust auto-accept do not trigger. See [[wiki/06-config-and-multi-harness|Config, Profiles, and Multi-Harness Support]].

### Q10. If Fleet adopts one Claude Squad idea for parallel coder workers, which pair eliminates both checkout conflicts and lost worker identity on restart?

> [!tip]- Answer
> Give each worker one worktree on its own branch under a controlled directory created from pinned `HEAD`, so no locking is needed. Persist started workers as JSON rows and reconcile on restart by re-attaching live tmux sessions and parking dead ones as resumable instead of replaying work. See [[wiki/targeted|Claude Squad for Fleet: Targeted Analysis]].

### Q11. What is the weakest engineering link in Claude Squad's design, and what would you probe first?

> [!tip]- Answer
> The strongest candidates are fail-fast state loading where one corrupt row hides all instances, substring-fragile prompt detection with no capability model, and shelling out to `tmux` and `gh` with no preflight guards. Probe blast radius first: corrupt-state recovery, unknown-harness autoyes misses, and stale-session name collisions after crashes. See [[critical_thinking|Critical Analysis]].
