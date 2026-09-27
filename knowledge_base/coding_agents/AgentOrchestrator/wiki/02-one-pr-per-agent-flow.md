> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# One PR per Agent

**In one sentence:** Each AO session claims exactly one GitHub pull request, and every downstream fact — checks, review comments, mergeability — is attributed to that owner and routed back to that owner's session until the human merges.

## Key points

- Each session claims exactly one pull request: either the agent opens it and AO links it, or a human attaches an existing one with `ao session claim-pr <session> <pr>`.
- A takeover guard (`--no-takeover`) refuses PRs already owned by another active session, so two agents can never own the same PR.
- From inside a worker, `AO_SESSION_ID` supplies session context so the agent's own PR open can be auto-linked to the right owner.
- The GitHub SCM observer polls with lazy auth, ETag guards, semantic diffing, and rate-limit respect, then writes PR/check/review facts into SQLite.
- All lifecycle nudges route to the owning session only: failing checks, changes-requested reviews, and merge conflicts each have a defined owner-directed reaction.
- Merge is always explicit and human-gated: desktop merge button or `ao pr merge <n>`; the retired `auto-merge` YAML key is rejected by typed project config.
- Reviewer agents run as a second, separate loop (`ao review trigger/ls/cancel/submit`) whose findings are inspectable before anything is delivered to the worker.

---

## 1. Claiming model

There are two paths to ownership, and both end in the same invariant (Invariant — a rule that must always stay true): one session, one PR.

| Path | How it works |
|---|---|
| Agent opens | The worker opens a PR from its worktree branch; AO observes it and links it to the owning session |
| Human attaches | `ao session claim-pr <session> <pr>` links an existing PR to a session; `--no-takeover` refuses PRs already owned by another active session |

The claim-PR fallback closes the "orphan PR" gap: when auto-linking misses (the agent opened a PR outside the expected harness flow), the PR can still be brought under ownership from the CLI, or from inside the worker via the `AO_SESSION_ID` environment variable that identifies the current session.

## 2. The SCM observer

A daemon-owned GitHub observer polls each claimed PR and records facts — never display strings — into SQLite:

- PR state (open, merged, closed), head SHA, base branch.
- Check runs (names, conclusions, links, counts such as "8/44 passed" shown on board cards).
- Review comments, review decisions (approved, changes-requested), unresolved threads.
- Mergeability (clean, conflicted, blocked).

Polling is polite and cheap: lazy authentication (only when needed), ETag conditional requests, semantic diffing (unchanged payloads are not rewritten), and rate-limit respect. Tracker intake beyond GitHub issues and this GitHub PR observation path is incomplete — broader tracker/SCM integrations from older docs are not in the current rewrite.

## 3. Ownership routing

Every observed fact is attributed to the PR's owner, and every reaction goes to that owner's session:

- Failing checks → check names + links sent to the owner.
- Changes-requested or unresolved comments → focused feedback to the owner.
- Merge conflict → the eligible session is asked to rebase and resolve.
- Ready-to-merge → durable in-app notification plus Electron toast.
- Merged/closed → facts updated, notifications created or resolved.

Messages are signature-deduplicated: an unchanged failure set is not re-sent every poll; a changed set produces a fresh nudge. Delivery is mode-aware: TUI sessions receive nudges through their tmux/conpty runtime; Chat sessions receive a native provider turn persisted in the structured conversation. While a session is blocked on an approval prompt, lifecycle messages are withheld.

## 4. Merge flow, step by step

1. Worker finishes in its worktree; its PR is claimed.
2. Observer polls GitHub and writes PR facts.
3. Lifecycle logic reacts per the table above.
4. Owner fixes or rebases in its own worktree and pushes.
5. Observer sees green checks + approvals → ready-to-merge notification.
6. Human merges explicitly via desktop or `ao pr merge <n>` (plus `ao pr resolve-comments` for thread hygiene).
7. Facts update; session can be cleaned up; dirty worktrees are still never force-deleted.

There is no auto-merge configuration. The legacy `auto-merge` YAML key was deliberately retired and is rejected by the typed project config.

## 5. Reviewer agents: the second loop

Separately from lifecycle nudges, AO can run reviewer agents against a worker PR:

- `ao review trigger` starts a configured reviewer run against the PR.
- `ao review ls` / `cancel` / `submit` manage the run.
- Findings are inspectable before the send-to-worker step — review output is triaged (e.g. via `ao review` flows) rather than piped raw into the worker's context.

This keeps machine review advisory: the worker sees curated findings, and the human sees them first.

**Covers:** docs SCM observer + lifecycle-automation table, CLI claim-pr / pr merge / resolve-comments / review commands, architecture PR-facts section, typed project config merge policy.
