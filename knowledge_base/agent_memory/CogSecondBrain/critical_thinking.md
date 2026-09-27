> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: huytieu/COG-second-brain
## Claims vs. evidence
- Claim: "no database, no vendor lock-in — just `.md` files that think" (`README.md:9`).
  Evidence for intent is strong: vault layout (`00-inbox` through `06-templates`),
  Git/iCloud sync, and file-by-file framework updates via `cog-update.sh`.
  Evidence for scalability is absent: no query, indexing, or concurrent-write story.
- Claim: 2-minute onboarding (clone → "Run onboarding" → personalized vault).
  Evidence is plausible: per-agent command table, `SETUP.md` 2-step install,
  plus `npx skills add` alternative. No failure-mode or timing data is cited,
  so the "2 minutes" figure is marketing, not measurement.
- Claim: 33 skills + 6 workers + 4 verifiers across 6+ agent surfaces.
  Partially verified: full Claude Code surface, full Antigravity pointer-stub surface,
  `AGENTS.md` universal fallback, and 7-skill Kiro/Gemini subsets are all documented.
  Gap: `AGENTS.md` (1082 lines), `CLAUDE.md`, and `cog-update.sh` chunks all truncate,
  so full-catalog parity is asserted rather than shown.
- Claim: cheap-worker / smart-lead routing (Sonnet collects, Opus reasons).
  This is the best-evidenced claim: explicit model table (`CLAUDE.md:60`),
  <2K-inline / ≥2K-to-`/tmp/`-file rule, single-deliverable consolidation rule.
  Missing: any cost, latency, or quality numbers proving the split pays off.
- Claim: opt-in V-model harness (CP-0–CP-7, risk lanes, evidence ledgers).
  Well-specified on paper: checkpoint table, `EVIDENCE <AC-id> | … | PASS|FAIL`
  contract, run dirs under `04-projects/harness/`. But opt-in means the headline
  rigor covers the least-used path; ordinary work carries no checkpoints by design.
- Claim: evidence-based People CRM with tiered enrichment.
  Weakest claim: Tier 2 truncates mid-word ("stren"), higher tiers undescribed.
  Cannot be evaluated from the digest at all.
## Genuinely new vs. repackaged
- Genuinely new as a package (not as inventions): the combination of brain-first
  protocol (read `05-knowledge/` before answering) with a citation rule,
  `/tmp/` path-only handoffs plus "a worker never grades its own homework",
  rigor-off-by-default with a `verification_harness: on` escape hatch,
  and pointer-stub multi-surface strategy (authoritative `.claude/`, thin delegates).
- Supporting hygiene is also thoughtful: `validate-agent-surface.sh` plus an explicit
  skill-sync checklist (edit skill → update `AGENTS.md`, manifests, Kiro/Gemini
  surfaces → run validator) treats prompt drift as a build problem.
- Most original single ideas: the `memory-hygiene` trust sweep (`last_verified` +
  confidence re-check against the live environment) and the `harvest` / `retro` /
  `review-cockpit` learning loop, which stages session learnings for approval
  instead of silently mutating durable memory.
- Repackaged: Obsidian vault conventions (inbox/daily/braindump/knowledge folders),
  GTD capture → consolidate → review loop, PM lifecycle
  (Research → PRD → Stories → Release Notes → KB), V-model checkpoints,
  and anti-slop taste guidance — all competent curation, openly inspired
  by `garrytan/gstack` and `garrytan/gbrain`, not novel research.
## Weaknesses and blind spots
- Truncation everywhere: `AGENTS.md`, `CLAUDE.md`, `cog-update.sh`, `SETUP.md`
  troubleshooting, and People CRM tiers are all cut short in the digest.
  Every judgment here is therefore provisional, not a full audit.
- Single-user PKM core wearing team-intelligence clothes: `team-brief`
  cross-references GitHub/Linear/Slack/PostHog, but the digest shows no auth,
  permissions, conflict-resolution, or multi-writer story for shared vaults.
- No-database is a trade-off, not a pure win: no schema, no queries, no migrations.
  Fine for notes; weak for the structured team/product data the PM skills produce.
- 33 skills × 6 surfaces is a real maintenance liability: the sync rule names
  the cost without removing it, and drift between Claude/Codex/Cursor/Kiro/Gemini
  surfaces is likely over time (current version `3.13.0` already shows churn).
- `/tmp/` handoffs and Sonnet/Opus routing assume Claude pricing and ephemeral
  filesystems; portability to other model families and sandboxed agents is unproven.
- No evaluation of any kind: no accuracy, cost, latency, or adoption metrics,
  and no security/privacy treatment of meeting transcripts, people profiles,
  or the API tokens the integrations necessarily hold.
## Applicability
- Good fit: solo technical leads wanting markdown-native memory plus PM glue
  (briefs, braindumps, release notes, Confluence publishing) inside their editor.
- Poor fit: teams needing shared ground truth, access control, auditability,
  or structured analytics over the same data the vault stores as prose.
- **Relevance to my work**
  - AI/ML engineering: borrow `memory-hygiene` (scheduled claim re-verification
    with confidence stamps) for experiment notes and eval ledgers; the
    `EVIDENCE <AC-id> | checkpoint | PASS|FAIL | observation | artifact` row
    transfers directly to model eval and data-quality runs.
  - Agentic systems: borrow the worker/verifier split with path-only handoffs,
    the <2K-inline file-spill rule, and the single-deliverable consolidation rule
    to cut narrativisation and context bloat in multi-agent pipelines.
  - Elisity data platform: borrow the `team-brief` / `comprehensive-analysis`
    shapes (cross-source daily brief, Linear sync-back, weekly board-prep rollup)
    as reporting patterns — but keep platform telemetry in a schema-backed store
    with access control, not in a prose vault Git cannot query.
## What this changes
- It reframes personal knowledge as agent runtime state: the vault is not
  documentation of work but the medium agents must read before reasoning.
- It makes rigor a dial rather than a default: ship fast with verification off,
  turn the V-model on per request, per project, or via profile flag.
- It treats skill maintenance as a build problem: pointer stubs plus validator
  plus sync checklist, instead of copy-pasted prompts rotting per IDE.
- If the handoff discipline (files over pasted context, verifiers observing
  artifacts rather than summaries) holds up empirically, it is worth copying
  even for teams that reject everything else in the repo.
## Verdict
- COG is a well-packaged, honestly-documented PKM-plus-PM agent harness whose
  best ideas are operational (handoff discipline, opt-in verification, memory
  hygiene, skill-sync hygiene) rather than architectural, and whose team,
  scale, and evaluation stories are thin or missing.
- For my context the transferable patterns outweigh the system: trial the
  worker/verifier handoff, evidence-row ledgers, and memory-hygiene sweep inside
  existing agentic workflows before considering any vault migration.
- **trial**
