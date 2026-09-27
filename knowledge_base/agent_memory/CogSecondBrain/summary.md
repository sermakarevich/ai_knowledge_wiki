# Technical Analysis: huytieu/COG-second-brain

**Repository:** https://github.com/huytieu/COG-second-brain
**Version analyzed:** 3.13.0
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview

COG (Cognition + Obsidian + Git) addresses the problem of fragmented personal and team knowledge: notes scattered across apps, meeting transcripts that never become decisions, and team signals split across GitHub, Linear, Slack, and PostHog with no synthesis layer (`README.md:9`, `README.md:17-29`). The repo addresses it by defining a convention-based second brain: a versioned Obsidian markdown vault (`00-inbox/` through `06-templates/`) operated on by a catalog of 33 agent skills, 6 data-heavy worker agents, and 4 read-only verifiers, with Git as the persistence and sync layer and no database (`README.md:9`, `README.md:17-29`, `README.md:177-199`, `.cursorrules:41`). The primary user is an individual knowledge worker (engineer, product manager, founder) who works inside an AI coding agent daily, with a secondary user in the product/engineering lead who needs cross-source team intelligence (`README.md:80-92`, `README.md:95-101`).

## 2. High-Level Architecture

```
You (natural language)
  │
  ▼
AI Agent (Claude Code / Antigravity / Cursor / Kiro / Gemini CLI / Codex)
  │
  ▼
33 Skills (.claude/skills/*/SKILL.md, AGENTS.md:3) ──► .md Files (vault 00-06)
  │          │                                            ▲      │
  │          ├─ delegates to ─► 6 Workers (Sonnet) ───────┘      │
  │          ├─ verified by ──► 4 Read-Only Verifiers ── observes ┘
  │          └─ syncs with ───► GitHub / Linear / Slack / PostHog / Confluence / Notion
  │
  ▼
.md Files ──► Git (versioning) ──► GitHub remote
.md Files ──► iCloud (mirror)
```

Data-flow narrative:

1. The user issues a natural-language request ("Run onboarding", "Team brief", "Weekly analysis"); the host agent resolves it to one of 33 skills via its native surface (`.claude/skills/`, `.agents/skills/`, `.kiro/powers/`, `.gemini/commands/`, or `AGENTS.md` fallback) (`README.md:35-58`, `README.md:64-74`).
2. The skill playbook applies the brain-first protocol: read `05-knowledge/` first, then `04-projects/<project>/` if project-specific, then synthesize (`.cursorrules:23`).
3. Data-heavy sub-tasks fan out to Sonnet workers (collection, research, file ops, execution, publishing, people-profile updates) while the lead session retains reasoning/synthesis on Opus (`CLAUDE.md:60`, `README.md:177-186`).
4. Workers return status + `/tmp/` file path rather than pasted output; the lead reads the file for synthesis. Verifiers receive paths only and check the artifact against acceptance criteria, never the worker's summary (`README.md:197-199`, `CLAUDE.md:81`).
5. Results land as markdown in fixed vault locations (briefs to `01-daily/briefs/`, braindumps to domain folders, frameworks to `05-knowledge/consolidated/`, people updates to `05-knowledge/people/`) (`AGENTS.md:50`, `AGENTS.md:82`, `AGENTS.md:241`).
6. When requested, results sync outward (Linear sync-back, Slack/Confluence/Notion publishing); the vault itself persists via Git commits and optionally iCloud, with harness evidence under `04-projects/harness/` and checkpoint ledgers in `.claude/logs/` (`README.md:17-29`, `WORKFLOW.md:159`).

Persistent state lives in markdown files in the vault, Git history, `/tmp/` handoff files (ephemeral), and harness run artifacts (`04-projects/harness/runs/<id>/evidence/`, `.claude/logs/checkpoint-ledger.tsv`, `loop-ledger.tsv`) (`WORKFLOW.md:159`, `CLAUDE.md:81`, `.gitignore:46`).

## 3. The Vault as Database: Markdown Files That Think

The central concept is the vault: numbered markdown directories replace a database, and skills are the stored procedures (`README.md:9`, `.cursorrules:41`). Representation is plain Obsidian markdown with YAML-frontmatter skill descriptors (`name`, `description` per `.claude/skills/*/SKILL.md`) and a citation convention `[Source: [[path/to/note]] | YYYY-MM-DD | confidence: high|medium|low]` (`.cursorrules:53`).

Named vault kinds with locations (`.cursorrules:41`, `GEMINI.md:11`, `SETUP.md:129`):

- `00-inbox/` — profiles (`MY-PROFILE.md`, `MY-INTERESTS.md`, `MY-INTEGRATIONS.md`) created by `/onboarding` (`AGENTS.md:11`)
- `01-daily/` — `briefs/daily-brief-YYYY-MM-DD.md`, `checkins/weekly-checkin-YYYY-MM-DD.md`, `journal/YYYY-MM-DD.md` (`AGENTS.md:82`, `.cursorrules:30`)
- `02-personal/` / `03-professional/` — domain-classified braindumps; `03-professional/` also holds `team-briefs/` and `COMPETITIVE-WATCHLIST.md` (`AGENTS.md:50`, `AGENTS.md:241`, `SETUP.md:129`)
- `04-projects/<project-slug>/` — per-project braindumps, `specs/SPEC-NNN-<slug>.md`, harness `runs/`, `retro/`, `BACKLOG.md` (`AGENTS.md:50`, `WORKFLOW.md:159`)
- `05-knowledge/` — `consolidated/`, `patterns/`, `timeline/`, `booklets/[category]/`, `people/` (`GEMINI.md:11`, `SETUP.md:129`)
- `06-templates/` — reusable note templates (`SETUP.md:129`)

Named executable kinds: 33 skills (8 personal-knowledge, 3 team-intelligence, 6 PM-workflow, research/content/verification/craft/design sets) (`README.md:80-172`); 6 workers (`worker-data-collector`, `worker-researcher`, `worker-file-ops`, `worker-executor`, `worker-publisher`, `brief-people-updater`) (`README.md:180-186`); 4 verifiers (`task-verifier` at CP-3v, `integration-verifier` at CP-4, `fix-agent` on `FAIL:fixable` with max 2 retries, `harvest-curator` propose-only at CP-7) (`README.md:188-195`).

Key query pattern: the brain-first protocol is a read rule, not a query language (`.cursorrules:23`):

```
1. Read relevant notes from `05-knowledge/` first
2. If project-specific, read `04-projects/<project>/`
3. Then synthesize an answer
```

People CRM is the closest thing to indexed state: profiles in `05-knowledge/people/` auto-escalate by mention count — Tier 3 (Stub) at 1 mention holds name, role, one-line context; Tier 2 (Moderate) at 3+ mentions holds executive snapshot and working style (`README.md:203-208`).

## 4. LLM / External Service Integration

The repo calls no LLM API itself. There is no model client, key, or inference call in the covered pages; the LLM is the host (Claude Code, Antigravity, Cursor, Kiro, Gemini CLI, Codex), and the repo supplies the instructions, skills, and routing policy the host executes (`README.md:13`, `README.md:64-74`). Model routing is a cost policy, not an API integration: Sonnet for all worker/verifier data tasks, Opus reserved for lead-session reasoning, synthesis, and editorial judgment (`CLAUDE.md:60`).

External services are integration targets reached through worker-executed actions and publishing skills, not vendored SDKs:

- Required for base use: none. The vault, skills, and Git versioning function without any external service (`README.md:9`, `SETUP.md:21`).
- Optional per skill: GitHub + Linear + Slack + PostHog (`team-brief`, `comprehensive-analysis`), Linear/GitHub Issues/Jira (`create-user-story`), GitHub milestones/Linear cycles (`generate-release-notes`), Confluence/Notion (`generate-prd` approval gate, `publish-to-confluence`, `update-knowledge-base`), web search/fetch (`worker-researcher`, `auto-research`, `daily-brief`) (`README.md:95-132`, `AGENTS.md:241`).
- No environment variables are documented in the covered pages. Integration configuration is file-based (`00-inbox/MY-INTEGRATIONS.md` created at onboarding) rather than env-based (`AGENTS.md:11`). `verification_harness: on` in `00-inbox/MY-PROFILE.md` is the one documented behavioral toggle (`CLAUDE.md:22`).

## 5. The Second-Brain Loop: Capture → Synthesize → Verify → Sync

The primary workflow is the capture-to-knowledge loop executed by skills, with the PM lifecycle (Research → PRD → Stories → Release Notes → Knowledge Base) as its most structured instantiation (`README.md:116`) and the opt-in V-model harness as its gated variant (`WORKFLOW.md:8`, `WORKFLOW.md:16`).

Step by step (each step cites the skill or agent definition location):

1. Onboard once — `/onboarding` creates `00-inbox/MY-PROFILE.md`, `MY-INTERESTS.md`, `MY-INTEGRATIONS.md`, `03-professional/COMPETITIVE-WATCHLIST.md`, and project folders in `04-projects/`; role packs (Product Manager, Engineering Lead, Engineer, Designer, Founder, Marketer) specialize the vault (`AGENTS.md:11`, `SETUP.md:129`).
2. Capture — `/braindump` classifies raw input into `02-personal/braindumps/`, `03-professional/braindumps/`, `04-projects/[project-slug]/braindumps/`, or `00-inbox/`; `/url-dump` saves URLs with extracted insights to `05-knowledge/booklets/[category]/`; `/meeting-transcript` structures recordings into decisions, actions, and team dynamics (`AGENTS.md:50`, `README.md:80-101`).
3. Research — `/auto-research` decomposes questions into parallel research threads across worker agents; `/daily-brief` produces freshness-gated (7-day) news intelligence to `01-daily/briefs/daily-brief-YYYY-MM-DD.md` (`README.md:120-124`, `AGENTS.md:82`).
4. Plan and specify (PM track) — `/generate-prd` drafts PRDs with an approval gate before Confluence/Notion publish; `/create-user-story` checks duplicates across Linear, GitHub Issues, or Jira first (`README.md:105-114`).
5. Execute and release (PM track) — development happens outside the vault; `/export-open-issues` audits tracker state into a vault summary; `/generate-release-notes` builds notes from GitHub milestones, Linear cycles, or manual input; `/update-knowledge-base` folds release changes into the product knowledge base (`README.md:105-116`).
6. Consolidate — `/knowledge-consolidation` builds frameworks from scattered notes into `05-knowledge/consolidated/`; `/weekly-checkin` runs cross-domain pattern analysis to `01-daily/checkins/`; `/harvest` stages session learnings for approval and proposes skill patches without writing durable knowledge unapproved (`AGENTS.md:82`, `README.md:140-146`).
7. Verify (opt-in only) — when a `V` skill (`/closed-loop`, `/ultragoal`), verification phrasing, or `verification_harness: on` triggers a harness run, work walks CP-0 intake → CP-1 spec → CP-2 plan → CP-3 build → CP-3v component verify → CP-4 integration verify → CP-5 acceptance → CP-6 ship → CP-7 retro, with `AC-n`-traced evidence rows and risk lanes (`tiny`, `normal`, `full`, `bug`, `backfill`) selecting which gates block (`WORKFLOW.md:8`, `WORKFLOW.md:16`, `WORKFLOW.md:52`, `WORKFLOW.md:97`).
8. Sync outward — `/team-brief` cross-references GitHub + Linear + Slack + PostHog with two-way Linear sync-back to `03-professional/team-briefs/`; `/publish-to-confluence` publishes any vault file; `worker-publisher` handles Slack/Confluence/Notion/webhook delivery (`AGENTS.md:241`, `CLAUDE.md:60`).
9. Maintain — `/update-cog` and `cog-update.sh` refresh framework files without touching personal content; `/memory-hygiene` re-verifies persistent-memory claims against the live environment and stamps `last_verified` + confidence (`README.md:80-92`, `cog-update.sh:5`).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | ~208+ | Repo concept, mermaid data flow, quick start, agent matrix, full skill catalog, worker/verifier architecture, People CRM |
| `AGENTS.md` | 1082 | Universal command reference: all 33 `/skills`, inputs, vault destinations, tracker integrations |
| `CLAUDE.md` | 250 | Always-apply framework instructions: response style, opt-in verification, Sonnet/Opus routing, worker output and single-deliverable rules |
| `WORKFLOW.md` | ~159+ | Harness-only V-model: checkpoints CP-0–CP-7, evidence-row contract, risk lanes, classifier, file homes |
| `SETUP.md` | 533 | 2-step install, agent support matrix, post-onboarding vault tree, skill-sync contributor rule |
| `cog-update.sh` | 566 | Safe updater: file-by-file framework refresh from `cog-upstream/main` with backup, dry-run, check, force, validate modes |
| `.cursorrules` | ~53+ | Cursor-compatible mirror of `CLAUDE.md`: skill count, agents, brain-first protocol, journal and citation rules |
| `GEMINI.md` | ~30+ | Gemini CLI scope: vault map, profile reads, 14 named skills, Obsidian Tasks emoji format, 7-day freshness |
| `plugin.json` | short | Agent Plugins standard manifest (spec 1.0.0): name, version, license |
| `marketplace-entry.json` | short | Marketplace packaging metadata: name, version, category |
| `COG-VERSION` | 1 | Single-line version source of truth (`3.13.0`) |
| `.gitignore` | ~46+ | Excludes Obsidian state, logs, harness runtime artifacts, backups; personal-content lines commented out by design |
| `scripts/validate-agent-surface.sh` | — | Packaging validator run before publishing/updating framework files |
| `docs/AGENT-SUPPORT.md` | — | Detailed agent-support matrix and contributor rules |

## 7. Dependencies

No runtime package dependencies are documented in the covered pages. The repo is markdown instructions, skill playbooks, agent definitions, and shell scripts executed by the host agent; there is no `package.json`, `requirements.txt`, or equivalent. The only versioned references are packaging and platform-conformance pins:

| Package | Version constraint | Purpose |
|---|---|---|
| *(none — no runtime packages)* | n/a | Vault, skills, and Git versioning run without installed dependencies |
| Agent Plugins standard (spec, via `plugin.json` + `skills/`) | `1.0.0` | Lets any standard-aware client load COG as a plugin |
| `cog-second-brain` (`COG-VERSION`, `marketplace-entry.json:10`, `plugin.json:4`) | `3.13.0` | Self-version pin for framework files and marketplace publishing |
| `npx skills` (installer shorthand) | unpinned | Alternative install path: `npx skills add huytieu/COG-second-brain` |

## 8. CLI / Usage Surface

Entry points: clone the repo and speak to the host agent; or install via the skills CLI. No compiled binary or served port exists.

| Entry point | Command | Effect |
|---|---|---|
| Clone | `git clone https://github.com/huytieu/COG-second-brain.git && cd COG-second-brain` | Local copy of vault + framework (`README.md:35-41`) |
| Onboarding (Claude Code) | `code .` → `Run onboarding` | Personalizes vault via `.claude/skills/` (`README.md:43-51`) |
| Onboarding (Antigravity / Cursor / Kiro / Codex / other) | Open folder → `Run onboarding` / `setup COG` / `/onboarding` / point at `AGENTS.md` | Same via `.agents/`, `.cursor-plugin/`, `.kiro/powers/`, `.gemini/commands/`, `AGENTS.md` (`README.md:43-51`) |
| Skills CLI | `npx skills add huytieu/COG-second-brain` | Alternative install (`README.md:53-56`) |
| Updater | `./cog-update.sh [--check \| --dry-run \| --force \| --validate \| --help]` | Safe framework refresh without touching personal content (`cog-update.sh:5`) |
| Validator | `./scripts/validate-agent-surface.sh` | Required before publishing/updating framework files (`README.md:76`) |
| Lane classifier | `bash .claude/lib/lane-classify.sh classify "<task>"` | Selects harness risk lane (`WORKFLOW.md:97`) |
| Checkpoint recorder | `bash .claude/lib/checkpoint.sh record <run-dir> <CP-id> PASS\|FAIL\|SKIP <note>` | Appends evidence-row to run ledger (`WORKFLOW.md:64`) |

Representative skill commands (full list of 33 in `AGENTS.md:11-304`): `/onboarding`, `/braindump`, `/daily-brief`, `/weekly-checkin`, `/knowledge-consolidation`, `/url-dump`, `/update-cog`, `/memory-hygiene`, `/team-brief`, `/meeting-transcript`, `/comprehensive-analysis`, `/auto-research`, `/create-user-story`, `/generate-prd`, `/generate-release-notes`, `/export-open-issues`, `/publish-to-confluence`, `/update-knowledge-base`, `/closed-loop`, `/ultragoal`, `/harvest`, `/retro`, `/review-cockpit`, plus craft/design skills (`no-ai-slop`, `slop-gate`, `voice-baseline`, `editorial-illustrations`, `data-forms`, `museum-art`, `daily-journal`, `taste-skill`, `product-ui-taste`).

| Env var | Required? | Purpose |
|---|---|---|
| *(none documented)* | — | Integration config is file-based (`00-inbox/MY-INTEGRATIONS.md`); no env vars appear in covered pages |

| Config file | Purpose |
|---|---|
| `00-inbox/MY-PROFILE.md` | Identity, preferences, `verification_harness: on` toggle (`CLAUDE.md:22`) |
| `00-inbox/MY-INTERESTS.md`, `MY-INTEGRATIONS.md` | Interest profile and service connections (`AGENTS.md:11`) |
| `03-professional/COMPETITIVE-WATCHLIST.md` | Tracked competitors/topics (`SETUP.md:129`) |
| `COG-VERSION` | Framework version pin (`COG-VERSION:1`) |
| `plugin.json` / `marketplace-entry.json` | Plugin-standard and marketplace packaging (`plugin.json:4`, `marketplace-entry.json:10`) |

## 9. Extensibility Points

- New skill: add `.claude/skills/[name]/SKILL.md` with `name`/`description` frontmatter, then mirror to `AGENTS.md`, `.claude-plugin/plugin.json`, and Kiro/Gemini surfaces if supported, then run `./scripts/validate-agent-surface.sh` (`SETUP.md:129`, `.cursorrules:8`).
- New agent surface (new editor/agent): add pointer stubs delegating to the authoritative `.claude/` playbooks, following the Antigravity `.agents/` precedent — stubs stay thin, `.claude/` stays canonical (`README.md:66-74`).
- New worker or verifier: add definition under `.claude/agents/` and extend the routing table in `CLAUDE.md:60` plus the matrix in `.cursorrules:12`; verifiers must remain read-only (observe artifact, no edits, no mutations) (`README.md:188-195`).
- New harness gate or lane: extend `WORKFLOW.md` checkpoints (`WORKFLOW.md:52`), the evidence-row contract (`WORKFLOW.md:64`), and the classifier (`lane-classify.sh`) plus recorder (`checkpoint.sh`) helpers (`WORKFLOW.md:97`).
- New vault domain: add a numbered folder alongside `00-inbox`–`06-templates` and document it in `.cursorrules:41`, `GEMINI.md:11`, and `SETUP.md:129` so all surfaces agree.
- New external integration: extend the relevant worker (`worker-data-collector` for reads, `worker-executor` for mutations, `worker-publisher` for outbound) and record credentials in `00-inbox/MY-INTEGRATIONS.md` rather than code (`CLAUDE.md:60`, `AGENTS.md:11`).
- Safe upstream evolution: extend `FRAMEWORK_FILES` in `cog-update.sh:23` so new framework files participate in file-by-file updates without endangering personal content (`cog-update.sh:5`).

## 10. Limitations and Gotchas

- **Verification is off by default and easy to skip.** Ordinary work carries no checkpoints or evidence ledger unless a `V` skill, verification phrasing, or `verification_harness: on` is set — quality gates only exist when explicitly invoked (`CLAUDE.md:22`, `WORKFLOW.md:8`).
- **Workers are cheap by design, and handoffs are lossy by rule.** Sonnet workers return status + `/tmp/` path, verifiers see paths only; anything that does not survive file serialization (nuance, rationale, negative results) is dropped unless the lead explicitly reads for it (`README.md:197-199`, `CLAUDE.md:81`).
- **Multi-surface parity is manual.** Every skill change must be mirrored across `.claude/skills/`, `AGENTS.md`, plugin manifests, and Kiro/Gemini surfaces, enforced only by remembering to run `./scripts/validate-agent-surface.sh` — drift between the 33-skill canonical set and the 7-power/7-command/14-skill subsets is the default failure mode (`SETUP.md:46`, `SETUP.md:129`, `GEMINI.md:30`).
- **`.gitignore` does not protect personal content.** Vault folders are commented out because `cog-update.sh` uses file-by-file extraction rather than merge; anyone running a naive `git clean`/`checkout` or a `--force` update without reading the backup behavior risks personal notes, with only timestamped `${file}.backup-*` copies as recourse (`cog-update.sh:228`, `.gitignore:16`).
- **Single-deliverable rule constrains harness runs.** One deliverable file per run; fan-out staging files must be consolidated then deleted — multi-artifact builds need explicit consolidation steps or they violate the framework rule (`CLAUDE.md:106`).
- **People CRM tiers above Moderate are undocumented in the covered pages.** The Tier 2 line truncates mid-word and no higher tiers or fields are described, so escalation behavior past 3+ mentions cannot be relied on from these sources (`README.md:207-208`).
- **Design skill pairing is exclusive.** `taste-skill` (first-impression surfaces, states a Design Read first) and `product-ui-taste` (everyday surfaces, budgets the frame in px first) must never both run on the same component; invoking both yields conflicting direction (`README.md:164-171`).

## 11. How It Compares to Alternatives

- **garrytan/gstack** — cited inspiration for the specialist-session worker pattern (`README.md:177`); gstack is a task-delegation harness, while COG adds the persistent markdown vault, skill catalog, and verification V-model around the same fan-out idea.
- **garrytan/gbrain** — cited inspiration for knowledge-pattern handling (`README.md:177`); gbrain focuses on knowledge representation, while COG couples that with PM workflows, team-intelligence integrations, and safe-update tooling.
- **Obsidian (plain vault + community plugins)** — same storage substrate (local markdown, no lock-in) but no agent skill layer, no worker/verifier routing, and no cross-tracker synthesis; COG is an opinionated agent-operated layer on top of an Obsidian-compatible tree.
- **Notion / Confluence (hosted knowledge bases)** — database-backed, permissioned, vendor-hosted collaboration; COG inverts the tradeoff (local files, Git history, no database) and treats Notion/Confluence as publish targets (`publish-to-confluence`, `update-knowledge-base`) rather than the system of record.

Positioning: COG is the agent-native, file-first option — it assumes the LLM host is the application server and the vault is the database, which minimizes lock-in and maximizes hackability at the cost of manual multi-surface maintenance and opt-in (rather than enforced) quality gates.

## Appendix: Selected Code Snippets

Version source of truth (`COG-VERSION:1`):

```
3.13.0
```

Skill exposure contract (`.cursorrules:8`):

```
COG exposes 17 skills via `.claude/skills/*/SKILL.md`. Each skill has a `name` and `description` in YAML frontmatter. Use AGENTS.md as the universal command reference.
```

Harness-ignored runtime artifacts (`.gitignore:46`):

```
.claude/logs/
04-projects/harness/runs/
```

Harness scope gate (`WORKFLOW.md:8`):

```
This document governs harness runs, and nothing else
```
