> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Vibe Kanban

## Claims vs. evidence (2-4 central README/docs claims; assess strong/suggestive/weak + why)

**Claim 1: "Run many coding agents in parallel, each in its own isolated workspace." — suggestive, not strong.**
Isolation is real: one workspace row plus one container directory with one git worktree
(linked checkout sharing object store) per repo (`crates/workspace-manager/src/workspace_manager.rs:290-371`),
on one shared branch per workspace (`crates/services/src/services/container.rs:786-795`).
But "many in parallel" collides with a single SQLite (lightweight file database) file in `Delete`
journal mode, not WAL (write-ahead logging, a concurrency mode) (`crates/db/src/lib.rs:83`),
so concurrent agent writes serialize on one writer; every `status='running'` execution flips to
`failed` on reboot (`crates/services/src/services/container.rs:272-326`), with dev servers and PTY
(pseudo-terminal, an interactive shell session) terminals never restored.
Task farming that cannot survive a laptop sleep is not parallel infrastructure.

**Claim 2: "One board from issue to pull request (PR — a proposed change sent for review)." — weak.**
The board-to-Done path rests on exactly three narrow syncs (first workspace, open PR, all-merged)
in `crates/remote/src/db/issues.rs:523-691`, matched on literal status names
("In progress", "In review", "Done"): renaming "Done" silently disables merge-to-Done,
`completed_at` is never set, and one stale linked PR pins the card short of Done.
Review comments never reach the database: React (UI library) context cleared on send or workspace
switch (`ReviewProvider.tsx:44-46`; `SessionChatBoxContainer.tsx:514-516`).
A review loop that loses unsent feedback and disagrees with its own timestamps is a demo loop, not a pipeline.

**Claim 3: "Agent-agnostic: nine coding-agent CLIs (command-line tools) behind one trait." — suggestive, with a maintenance trap.**
The `StandardCodingAgentExecutor` trait plus `CodingAgent` dispatch enum
(`crates/executors/src/executors/mod.rs:220,109`) with per-adapter `normalize_logs()` into
`NormalizedEntry` patches on a `MsgStore` (`crates/services/src/services/container.rs:917`) is well-factored.
But there is no plugin registry: a new agent needs an enum variant, module, capability entries,
MCP (Model Context Protocol — standard for exposing tools to agents) shape match, and a `DEFAULT`
profile in `default_profiles.json:2`, against hard-coded npm (Node package manager) pins
(Claude `2.1.119`, Codex `0.124.0`, Copilot `0.0.403`).
Each upstream CLI (command-line interface) flag or JSON (data format) log change breaks spawn
or normalization until a human bumps the pin — breadth as liability, especially post-archival.

**Claim 4: "Local-first preview and privacy." — weak on robustness.**
Durable state is local (`db.v2.sqlite` + branches + worktree dirs), which is good;
but preview strips framing guardrails (`CSP`/`X-Frame-Options` in `crates/preview-proxy/src/lib.rs:77-86`),
loads the Eruda console from a public CDN (content delivery network), scrapes dev ports from logs
by regex (`usePreviewUrl.ts:151-220`), and kills all running dev servers on each start with no health
check (`execution.rs:37-137`). Local data with guessed ports and weakened browser isolation is fragile ops.

## Genuinely new vs. repackaged (name prior work: Copilot Workspaces, OpenHands, agent harnesses)

Almost everything is repackaging, competently combined. GitHub Copilot Workspaces already did
spec-to-plan-to-branch-to-PR, single-vendor and cloud-tied; Vibe Kanban copies the flow and swaps
in local worktrees plus model choice. OpenHands (ex-OpenDevin) *is* the agent runtime with its own
sandbox and action loop, while Vibe Kanban makes zero direct large language model (LLM — the AI that
writes code) calls and just shells to third-party CLIs. SWE-agent / SWE-bench harnesses already
normalized logs and scored patches in Docker (container tool) for benchmarking; Claude Code Task /
subagents already did prompt-level fan-out with no durable board. Only the combination is arguably
new: card-as-prompt (`IssueWorkspacesSectionContainer.tsx:131-156`), worktree-per-run with base-commit
diff streaming (`crates/git/src/lib.rs:327-353`), review-markdown prepended to the next prompt
(`promptMessage.ts:11-26`). Useful glue, not a new primitive.

## Weaknesses and blind spots (incl. Apr 2026 shutdown + community-maintained risk, relay/cloud vs local split, concurrency/scale limits)

- **Archived upstream is the headline risk.** BloopAI archived the repo in April 2026 (commit `4deb7eca`,
v0.1.44); builds come from community forks with no official relay backend, so every CLI pin, MCP shape,
and ACP (Agent Client Protocol — JSON message format for driving agents) harness assumption rots from that date.
- **Relay/cloud vs local split is unfinished.** `crates/remote` is excluded from the main Cargo (Rust build
tool) workspace (`Cargo.toml:35`) with its own server; `relay-*` crates tunnel to a local instance while
`VK_SHARED_API_BASE` still defaults to `https://api.vibekanban.com` — remote issues/PRs and local execution
drift with nobody to fix the seam.
- **Concurrency and scale ceiling is low.** Single-tenant app, one SQLite writer in Delete mode, 20+ services
with only `LocalDeployment` as production impl, 60s `pr_monitor` polling instead of webhooks (push
notifications from the host), 200 MB diff-stream cap with ~2 MB per-file omission. A handful of tasks, not a team.
- **Durability holes the docs underplay.** Restart kills running work; terminals are fresh PTY per WebSocket
(live two-way connection) with no reattach (`terminal.rs:165`; `pty.rs:36-39`); review drafts evaporate;
`completed_at` never set; sub-issue completion does not roll up. The board can lie after any disruption.
- **Hot-path fragility.** `unwrap` on executor-action/script `Option`s (`container.rs:216,420-431`),
poisoned `Mutex`/`RwLock` (thread locks) cascades, Windows-only migration-checksum auto-fix diverging by
platform (`crates/db/src/lib.rs:21-68`) — prototype-grade handling around destructive git (version-control tool) ops.

## Applicability (when it works, prerequisites, where it fails)

Works when: solo developer or pair runs 2-6 small independent tasks on local git repos, keeps default
status names, supervises each agent, and treats the board as scratch space rather than record.
Prerequisites: git plus `gh`/`az` hosting CLIs, logged-in agent CLIs matching pinned versions, free
localhost (local machine) ports, tolerance for re-running work after restarts, willingness to pin the fork commit.
Fails where: team-shared state, headless CI (continuous integration — automated build/test service),
long-running or many-parallel jobs, renamed workflows, audit needs (no durable review store), offline or
hardened browsers (CDN use, stripped headers), or anything needing multi-tenancy, auth (authentication),
or webhook-driven merge tracking.

**Relevance to my work** — for Sergii (AI/ML engineering, agentic fleet, Elisity data platform):

- **Fleet (agentic orchestration): borrow the pattern, ignore the binary.** Worktree-per-task plus
`NormalizedEntry` log normalization plus review-markdown-into-next-prompt is worth copying into fleet;
an archived single-SQLite desktop board is not a fleet runner.
- **AI/ML engineering: trial only for small parallel code spikes.** Fine for independent refactors across
agent vendors; useless for training, evaluation, or data pipelines needing lineage and restart-safe runs.
- **Elisity data platform: ignore for production paths.** No provenance, no multi-user story, one local
database file, community-fork maintenance — poor fit for shared data or lake-adjacent automation.

## What this changes (if claims hold)

If all claims held, review would move from chat transcripts to a durable board where each card owns its
branch, worktree, normalized log, diff, and next prompt — and model choice becomes a profile switch, not
a rewrite, making supervised parallelism the default. Since durability, concurrency, and maintenance do not
hold, the real change is narrower: Vibe Kanban validates the worktree-plus-normalized-log-plus-prompt-feedback
shape that a sturdier orchestrator should implement properly.

## Verdict (3-5 sentences ending with one-word adoption call: adopt / trial / watch / skip + strongest reason)

Vibe Kanban is a well-structured prototype whose best ideas — worktree isolation, one executor trait with log
normalization, review feedback folded into the next prompt — deserve reuse, but whose product cannot be trusted:
archived upstream, stale CLI pins, restart-amnesia, ephemeral reviews, literal-name automation.
It helps one supervised developer juggle a few local tasks and hurts everywhere scale, sharing, or auditability matter.
For Sergii's fleet and platform contexts the patterns merit a trial inside owned code, while the app itself
does not merit deployment, so the call is **skip**
