---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Agent Orchestrator (AO)

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What does each AO worker session own, and why does that prevent file collisions?

> [!tip]- Answer
> Each session owns a fresh git worktree + branch (or an AO-managed Scratch directory), so two agents never share a checkout or a branch and cannot overwrite each other's files. See [[wiki/01-worktree-isolation|Worktree Isolation]].

### Q2. What happens when you kill a session with uncommitted work, and how do you preview cleanup safely?

> [!tip]- Answer
> `ao session kill` never force-deletes a dirty registered worktree — uncommitted work is preserved. `ao session cleanup --dry-run` previews reclaimable sessions before anything is removed. See [[wiki/01-worktree-isolation|Worktree Isolation]].

### Q3. State the one-session-one-PR invariant and the two paths to ownership.

> [!tip]- Answer
> One session owns exactly one PR: either the worker opens it from its branch and AO links it, or a human attaches an existing PR with `ao session claim-pr <session> <pr>` (`--no-takeover` refuses PRs owned by live sessions). See [[wiki/02-one-pr-per-agent-flow|One PR per Agent]].

### Q4. What does the SCM observer store, and what three polling courtesies does it extend to GitHub?

> [!tip]- Answer
> It stores PR/check/review/mergeability facts (never display strings) in SQLite. It uses lazy auth, ETag conditional requests, and semantic diffing with rate-limit respect. See [[wiki/02-one-pr-per-agent-flow|One PR per Agent]].

### Q5. Who owns all state and logic in AO's process layout, and what are the clients forbidden from doing?

> [!tip]- Answer
> One local Go daemon owns durable state (SQLite under `~/.ao`) and all domain logic; the desktop, `ao` CLI, and mobile clients are thin HTTP/SSE clients. The CLI never touches the database and never launches adapters. See [[wiki/03-control-surface|Control Surface]].

### Q6. Why does AO derive status at read time instead of storing it, and what is stored instead?

> [!tip]- Answer
> Stored status strings drift from reality under failures; derivation cannot drift. The daemon stores durable facts (activity, termination, controller generation, PR/check/review facts) and computes labels like "CI failed" or "ready to merge" on read. See [[wiki/03-control-surface|Control Surface]].

### Q7. How does signature deduplication stop CI-flap spam, and when is automation deliberately silenced?

> [!tip]- Answer
> Each lifecycle message is hashed by failure/comment set — an unchanged set is not re-sent, only a changed set produces a fresh nudge. While a session is blocked on an approval prompt, lifecycle messages are withheld entirely. See [[wiki/04-ci-review-feedback-routing|CI, Review, and Feedback Routing]].

### Q8. How many harnesses ship with AO, how many unlock Chat, and what is the onboarding consequence of the compiled-in adapter design?

> [!tip]- Answer
> 27 harnesses ship compiled into the binary (no plugin marketplace); only 4 (codex, claude-code, opencode, droid) unlock structured Chat, the rest are TUI-only. AO bundles no CLIs or credentials — it reuses the user's installed CLIs and auth. See [[wiki/05-harness-support-and-fleet-lessons|Harness Support and Fleet Lessons]].

### Q9. What is the weakest link in AO's evidence base, and why should fleet treat two of its claims with caution?

> [!tip]- Answer
> The source is vendor product docs, not an independent evaluation: throughput claims (2–3 → 5+ PRs/day) are testimonials without baselines, and orchestrator-to-orchestrator communication is anecdote with no documented protocol. Borrow the mechanisms, not the marketing numbers. See [[critical_thinking|Critical Analysis]].
