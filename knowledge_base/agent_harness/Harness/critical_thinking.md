> [[index|Wiki]] | [[summary|Summary]]
# Critical Analysis: Harness
## Claims vs. evidence
- "Agents you can actually trust" (policy + sandbox + review make autonomy safe) — **weak**.
  All three trust layers default to pass: `SandboxMode` defaults to `DangerFullAccess`,
  a passthrough unless token paths or network policy narrow it (wiki/03:12).
  `RuleEngine::check_command_policy` has no per-tool-call gate — its only in-tree caller
  outside tests is the offline `execpolicy check` CLI (wiki/03:8).
  The hook enforcer fails open on disabled/`CI`/no-guards/no-files/scan-failure and returns
  `Warn`, never block, on violations (wiki/03:10), while the circuit breaker auto-passes
  for 300 s after 3 consecutive blocks (wiki/03:11).
  The source shows defense-in-depth paperwork, not an enforced perimeter.
- "Durable, crash-safe orchestration" — **suggestive**.
  The lease-claim SQL (pending or expired-`running`), `lease_generation` bump on claim,
  half-TTL renewal, and dead-letter-on-lease-loss path are concrete machinery (wiki/02:7-8).
  But the wiki admits there is no startup replay — only lease-expiry reclamation
  plus workspace/host restore (wiki/02:21) — so recovery latency equals lease TTL,
  and the dead-letter table presupposes a decider whose resolution logic is never described.
- "Independent cross-agent review catches what one model misses" — **weak**.
  The `CONFIRMED:`/`MISSED:` round protocol with `NotConverged`/`ProtocolFailure` outcomes
  and the `distinct_challenger` guard are real (wiki/06:5-6).
  Yet independence is enforced only by comparing backend `id()`/`name()` strings (wiki/06:17),
  so two adapters wrapping the same underlying model pass as "distinct".
  The `SingleModelDegraded` path legitimizes single-model operation, challenger context is a diff
  truncated at 4096 bytes (wiki/06), and no precision/recall evidence is cited anywhere.
  "Independent review" thus assumes model diversity and small diffs without demonstrating either.
- "Self-improving system via the GC loop" — **weak**.
  Six signal detectors plus staged `Pending`-draft persist-then-adopt is genuine (wiki/06:11-12),
  but signals are threshold aggregates over the event log (repeated warns, hot files, slow sessions),
  i.e. correlation counters, not causal defect attribution.
  Grading only a trailing 1-hour event window (wiki/06) is a recency heuristic,
  and `RulesOnly` auto-adoption can therefore codify spurious correlations into persistent rules.
## Genuinely new vs. repackaged
- Lease-claim with generation counters is Temporal/Cadence durability with the replay half removed:
  weaker semantics (reclaim, not deterministic replay), fairly priced as simpler to operate,
  but not an advance over either system.
- The Starlark exec policy is policy-as-code (OPA/Rego style) reduced to token-prefix matching
  over two builtins (`prefix_rule`, `host_executable`); strictly less expressive than Rego,
  and query-only at that rather than an admission-control gate.
- Seatbelt/Landlock/bwrap sandboxing, process-group-kill supervision (`ManagedChild`),
  and per-task git worktrees are repackaged OS/git primitives, not inventions.
  Erlang-OTP supervisor trees did liveness-plus-restart with stronger semantics decades ago.
- Primary-plus-challenger review is a two-LLM code-review bot with a line-tag wire protocol;
  the `CONFIRMED`/`MISSED`/`NotConverged` state machine is competent prompt engineering,
  not review theory, and no-self-review by name-string comparison is weaker than it looks.
- The one genuine contribution is compositional: leases plus two-stage permit scheduling
  plus the submissions/plan split plus review gates plus GC drafts in one Rust control plane.
  That integration is borrow-worthy; none of its parts is.
## Weaknesses and blind spots
- Cost multiplier is unacknowledged: every task can pay primary plus challenger rounds
  plus `MAX_FEEDBACK_REPAIR_ROUNDS = 3` plus quality-gate workflows, yet no cost ceiling,
  per-review token budget, or measured overhead appears anywhere in the wiki.
- Postgres is the single durable store with an 8-connection default pool, per-schema
  advisory-lock migrations, and in-memory scheduler state rebuilt at boot (wiki/01:14) —
  a throughput choke and a split-brain risk the design never load-tests or sizes.
- Lease tuning is all magic numbers with no sizing argument: renewal at `clamp(ttl/2, 1s, 30s)`,
  dispatch every 30 s batch 32, worker interval 5 s concurrency 8 with 600 s leases (wiki/05).
  Wrong TTLs mean duplicate execution or stalled reclaim, and nothing bounds that window's blast radius.
- The reconciler admits GitHub-only, non-destructive, anomaly-without-retry semantics (wiki/02:19),
  so silent drift on every non-GitHub trigger (Feishu, pollers) is by design, not accident.
- Retrieval quality is assumed, not earned: skill shadowing resolves by mechanical tier priority
  (wiki/07:10) and memory retrieval is lexical token-overlap with fixed weights (wiki/07:41),
  so both can silently promote stale or gaming content with no relevance evaluation.
- Observability is opt-in fragility: OTLP trajectory export defaults off, and endpoint resolution
  ends in a TCP probe that fails pipeline startup when unreachable (wiki/07:6).
## Applicability
- Works when a small team operates Postgres plus Docker plus a Rust binary,
  runs GitHub-centered file-scoped coding tasks, and accepts worktree-per-task
  plus `cargo fmt/check/test/clippy`-style gates — the `WORKFLOW.md` binding betrays a Rust-repo bias.
- Fails where there is no Docker/Postgres ops capacity, trackers other than GitHub,
  ambiguous long-horizon work that does not fit plan-then-implement turns,
  or high-throughput fleets where a two-stage permit queue with `MAX_PRIORITY_LEVEL = 2`
  and a single Axum server become the bottleneck.
  Note `CI`-set environments silently disable hook enforcement, so CI-run fleets get no hooks at all.
- **Relevance to my work**
  - Fleet (agentic orchestration): trial the patterns, ignore the server.
    Lease-owner/expiry/generation columns plus the submissions split (plan record vs attempt records)
    and two-stage permits port directly to the beads DB without adopting 13 crates of Rust.
  - Elisity data platform: watch only. The Postgres event log plus OTLP trajectory export
    is a reasonable audit pattern, but the GitHub-issue-to-merge runtime assumes code repos,
    not data pipelines, and transfers poorly to data-quality semantics.
  - AI/ML experimentation: ignore. Lexical skill scoring, 1-hour grading windows,
    and threshold GC signals are the wrong substrate for experiment tracking and model evaluation.
## What this changes
- If the trust and review claims held, Harness would obsolete hand-rolled supervisor scripts:
  leased jobs plus enforced distinct-model review plus staged rule adoption
  would be the default agent-fleet substrate. They do not hold as stated, so that substitution is unsafe.
- What partially holds — lease/generation reclaim, permit-queue scheduling,
  draft-staged self-modification — is still worth absorbing into Fleet:
  it converts crash recovery from watchdog heuristics into row-state mechanics,
  a durable improvement even if Harness itself is never deployed.
## Verdict
Harness is a well-instrumented composition of borrowed primitives whose best ideas survive
scrutiny while its headline promises rest on fail-open defaults and string-identity review checks.
For Sergii the rational move is extraction, not adoption: port the lease columns and submissions
split into Fleet, run one spike on distinct-backend review, and leave the server behind.
The Starlark policy theater and GC auto-adoption are liabilities dressed as safety features.
The single strongest reason to take anything at all is lease-generation reclaim as proven row-state mechanics: trial
