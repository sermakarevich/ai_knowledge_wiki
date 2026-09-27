> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# CI, Review, and Feedback Routing

**In one sentence:** A daemon-owned GitHub observer records CI, review, and mergeability facts into SQLite, and a built-in lifecycle engine routes signature-deduplicated, mode-aware nudges to the owning session while a separate reviewer-agent loop keeps machine review advisory and human-triaged.

## Key points

- The SCM observer polls GitHub with lazy auth, ETag guards, semantic diffing, and rate-limit respect, then writes PR, check, review, and mergeability facts — never display strings — into SQLite.
- Every observed fact is attributed to the PR's owning session: failing checks, changes-requested reviews, and merge conflicts each trigger a defined owner-directed reaction.
- Lifecycle messages are signature-deduplicated: an unchanged failure set is never re-sent; only a changed set produces a fresh nudge, which prevents CI-flap spam.
- Delivery is mode-aware: TUI sessions get nudges through their tmux/conpty runtime, Chat sessions get a native provider turn persisted in the structured conversation.
- While a session is blocked on an approval or permission prompt, lifecycle messages are deliberately withheld — automation never talks over a permission gate.
- Reviewer agents run as a second, separate loop (`ao review trigger/ls/cancel/submit`) whose findings are inspectable before anything is delivered to the worker.
- Merge is always explicit and human-gated (desktop button or `ao pr merge`); the legacy `auto-merge` YAML key was retired and is rejected by typed project config.

---

## 1. The observation layer

The GitHub SCM observer is the only component that talks to GitHub, and it only writes facts:

| Fact family | Examples |
|---|---|
| PR state | open / merged / closed, head SHA, base branch |
| Check runs | names, conclusions, links, counts ("8/44 passed" on board cards) |
| Reviews | comments, decisions (approved / changes-requested), unresolved threads |
| Mergeability | clean, conflicted, blocked |

Polling is polite and cheap: authentication happens lazily (only when a request needs it), ETag conditional requests avoid re-downloading unchanged payloads, semantic diffing means unchanged payloads are not rewritten to SQLite, and rate limits are respected. Tracker intake beyond GitHub issues and this GitHub PR observation path is incomplete — broader tracker/SCM integrations from older docs are not in the current rewrite.

## 2. The lifecycle reaction table

Observed facts drive a fixed, daemon-owned reaction table — built in, not user-scripted:

| Observation | Reaction |
|---|---|
| Failing CI checks | Send check names + links to the owning session |
| Changes-requested review / unresolved comments | Send focused feedback to the owner |
| Merge conflict (unmergeable) | Ask the eligible session to rebase and resolve |
| PR ready to merge | Durable in-app notification + Electron toast to the human |
| Merged / closed | Update facts; create or resolve notifications |
| Session needs input | Notify the human |

There is deliberately no user-facing reactions DSL (Domain-Specific Language — a mini-language for one job). The retired `reactions:` / `retries:` / `auto-merge` YAML schema was removed in the Go rewrite: `ao import` reports those legacy fields as dropped, and typed project config rejects unknown fields.

## 3. Signature deduplication

Every lifecycle message carries a signature derived from the failure or comment set. An unchanged set is not re-sent on the next poll; a changed set produces a fresh nudge. This is the anti-spam mechanism: flaky CI that fails identically for ten polls produces one nudge, not ten. The fleet equivalent is hashing the CI/beads failure set before re-pinging a worker.

## 4. Mode-aware delivery and the blocked-session rule

Delivery follows the session's live interface:

- **TUI sessions** receive nudges injected through their tmux (macOS/Linux) or ConPTY (Windows) runtime.
- **Chat sessions** receive a native provider turn persisted in the structured conversation (turns, approvals, usage), so the nudge is part of the durable history, not an ephemeral injection.

One hard rule overrides both paths: while a session is blocked on an approval or permission prompt, lifecycle messages are withheld. The human must answer the gate first; automation resumes after.

## 5. Reviewer agents: the second loop

Separately from lifecycle nudges, AO can run reviewer agents against a worker PR:

- `ao review trigger` starts a configured reviewer run against the PR.
- `ao review ls` / `cancel` / `submit` manage the run.
- Findings are inspectable before the send-to-worker step — review output is triaged rather than piped raw into the worker's context.

This keeps machine review advisory: the worker sees curated findings, and the human sees them first. Related hygiene commands: `ao pr resolve-comments` for thread cleanup after the fix lands.

## 6. Explicit merge

Merge itself is always a human action: the desktop merge button or `ao pr merge <n>` through AO's GitHub action engine. There is no auto-merge configuration by design — throughput comes from routing fixes to owners automatically, while the merge decision stays with the operator.

**Covers:** docs lifecycle-automation page (reaction table, dedup, delivery), SCM observer polling behavior, CLI review/pr commands, retired reactions schema, blocked-session rule.
