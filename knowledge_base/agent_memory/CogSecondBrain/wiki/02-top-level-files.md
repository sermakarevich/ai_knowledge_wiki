[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The repository root defines the agent-facing surfaces, framework instructions, vault layout, safe-update tooling, and versioned packaging for the COG second brain.
## Key points
- `AGENTS.md` is the universal agent command reference defining all invocable `/skills` for any markdown-reading agent (`AGENTS.md:3`, `AGENTS.md:11`).
- `CLAUDE.md` sets always-apply framework instructions for response style, opt-in verification, delegation caps, and Sonnet/Opus model routing (`CLAUDE.md:7`, `CLAUDE.md:22`, `CLAUDE.md:60`).
- `.cursorrules` is the Cursor-compatible mirror of `CLAUDE.md`, exposing 17 skills, 10 worker/verifier agents, the brain-first protocol, and the vault structure (`.cursorrules:8`, `.cursorrules:12`, `.cursorrules:23`, `.cursorrules:41`).
- `GEMINI.md` scopes Gemini CLI operation to the Obsidian vault layout, profile reads, 14 named skills, and Obsidian Tasks emoji format with 7-day news freshness (`GEMINI.md:3`, `GEMINI.md:11`, `GEMINI.md:30`).
- `cog-update.sh` updates only listed framework files file-by-file from the `cog-upstream` remote without touching personal content folders (`cog-update.sh:5`, `cog-update.sh:17`, `cog-update.sh:23`).
- `SETUP.md` prescribes a 2-step install (clone, run onboarding) and the multi-agent support matrix plus post-onboarding vault tree (`SETUP.md:21`, `SETUP.md:46`, `SETUP.md:129`).
- `WORKFLOW.md` governs harness runs only via an opt-in V-model with gated checkpoints CP-0–CP-7, risk lanes, and run artifacts under `04-projects/harness/` (`WORKFLOW.md:8`, `WORKFLOW.md:16`, `WORKFLOW.md:52`, `WORKFLOW.md:97`, `WORKFLOW.md:159`).
- `.gitignore`, `COG-VERSION`, `marketplace-entry.json`, and `plugin.json` pin runtime hygiene and packaging at version `3.13.0` (`.gitignore:2`, `.gitignore:46`, `COG-VERSION:1`, `marketplace-entry.json:10`, `plugin.json:4`).
---
## .cursorrules
Cursor entry point; explicitly "the Cursor-compatible version of CLAUDE.md" (`.cursorrules:1`).
Verbatim (`.cursorrules:8`):
```
COG exposes 17 skills via `.claude/skills/*/SKILL.md`. Each skill has a `name` and `description` in YAML frontmatter. Use AGENTS.md as the universal command reference.
```
Worker agents (`.cursorrules:12`): "10 agents live in `.claude/agents/`: 6 workers handle data-heavy tasks, 4 read-only verifiers check the result against acceptance criteria by observing the artifact."
Brain-first protocol (`.cursorrules:23`):
1. Read relevant notes from `05-knowledge/` first
2. If project-specific, read `04-projects/<project>/`
3. Then synthesize an answer
Daily journal (`.cursorrules:30`): after a meaningful unit of work, "append one entry to `01-daily/journal/YYYY-MM-DD.md` (`date +%F`)"; first entry of the day creates the file from `.claude/skills/daily-journal/SKILL.md`.
Vault structure (`.cursorrules:41`): `00-inbox/`, `01-daily/`, `02-personal/`, `03-professional/`, `04-projects/`, `05-knowledge/`, `06-templates/`.
Citation rule (`.cursorrules:53`): `[Source: [[path/to/note]] | YYYY-MM-DD | confidence: high|medium|low]`.

## .gitignore
Excludes Obsidian state, trash, OS files, IDE dirs, logs, harness runtime artifacts, backups, and private submission docs (`.gitignore:2`, `.gitignore:46`).
Verbatim (`.gitignore:46`):
```
.claude/logs/
04-projects/harness/runs/
```
Personal content (`00-inbox/*`, `01-daily/*`, `02-personal/*`, `03-professional/*`, `04-projects/*`, `05-knowledge/*`, `06-templates/*`) is commented out by default because `cog-update.sh` uses file-by-file extraction, not git merge (`.gitignore:16`).

## AGENTS.md
Universal surface: "This document defines the available commands/skills for AI agents interacting with COG (Cognition + Obsidian + Git)" (`AGENTS.md:3`); Claude Code should use `.claude/skills/` and Kiro `.kiro/powers/` natively (`AGENTS.md:8`).
Documented commands include `/onboarding` (creates `00-inbox/MY-PROFILE.md`, `MY-INTERESTS.md`, `MY-INTEGRATIONS.md`) (`AGENTS.md:11`), `/braindump` (domain-classified capture to `02-personal/braindumps/`, `03-professional/braindumps/`, `04-projects/[project-slug]/braindumps/`, or `00-inbox/`) (`AGENTS.md:50`), `/daily-brief` (7-day freshness, Tier 1/2/3 sources, output `01-daily/briefs/daily-brief-YYYY-MM-DD.md`) (`AGENTS.md:82`), `/weekly-checkin` (`01-daily/checkins/weekly-checkin-YYYY-MM-DD.md`), `/knowledge-consolidation` (frameworks to `05-knowledge/consolidated/`), `/url-dump` (booklets to `05-knowledge/booklets/[category]/`), `/loop-engineering`, `/team-brief` (Linear + GitHub/Slack/PostHog cross-reference with Linear sync-back to `03-professional/team-briefs/`) (`AGENTS.md:241`), `/meeting-transcript`, and `/comprehensive-analysis`.
Truncated in chunk: full `AGENTS.md` is 1082 lines; chunk notes "... (truncated, 38230 more characters)" after the comprehensive-analysis section (`AGENTS.md:304`), so remaining commands and references were not visible.

## CLAUDE.md
Framework instructions; response style is always-apply: optimize for information gain, start with the answer, never invent named frameworks, headings name subject matter (`CLAUDE.md:7`).
Verification harness is opt-in, off by default: "It does not run unless you ask for it" via skill (`/closed-loop`, `/ultragoal`, `/retro`, `/harvest`, `/review-cockpit`), phrasing, or `verification_harness: on` in `00-inbox/MY-PROFILE.md` (`CLAUDE.md:22`); two rules always apply — verify by observing the artifact and a worker never grades its own homework.
Model routing — always apply (`CLAUDE.md:60`):
| Task type | Model | Agent definition |
|-----------|-------|-----------------|
| Data collection (GitHub, Slack, Jira, Linear, file reads) | **Sonnet** | `worker-data-collector` |
| Web research (search, fetch URLs, extract facts) | **Sonnet** | `worker-researcher` |
| Publishing (Slack, Confluence, Notion, webhooks) | **Sonnet** | `worker-publisher` |
| File operations (vault reads/writes, metadata, profiles) | **Sonnet** | `worker-file-ops` |
| Pre-approved mutations (Jira transitions, Linear updates, API calls) | **Sonnet** | `worker-executor` |
| People profile updates from brief/meeting data | **Sonnet** | `brief-people-updater` |
| Read-only verification, harness runs only | **Sonnet** | `task-verifier` / `integration-verifier` |
| Reasoning, synthesis, editorial judgment | **Opus** | Lead session (no delegation) |
Worker output rule (`CLAUDE.md:81`): < 2K tokens inline, >= 2K tokens to `/tmp/{task-slug}-{context}.md`. Single-file deliverable rule (`CLAUDE.md:106`): one deliverable file per run; fan-out staging files are consolidated then deleted.
Truncated in chunk: full `CLAUDE.md` is 250 lines; chunk notes "... (truncated, 5247 more characters)" (`CLAUDE.md:163`), so engineering-discipline remainder was not visible.

## cog-update.sh
Bash updater: "Safely updates framework files (skills, docs, scripts) without touching your personal content" (`cog-update.sh:5`); config `REMOTE_NAME="cog-upstream"`, `REMOTE_URL="https://github.com/huytieu/COG-second-brain.git"`, `BRANCH="main"`, `VERSION_FILE="COG-VERSION"` (`cog-update.sh:17`); `FRAMEWORK_FILES=(...)` enumerates core docs, all `.claude/skills/`, references, role packs, worker agents, people CRM, Kiro powers, Antigravity `.agents/`, Gemini commands/skills, plugin manifests, and `.gitignore` (`cog-update.sh:23`).
Flags (`cog-update.sh:5`):
| Flag | Behavior |
|---|---|
| (none) | Interactive update, prompts per file |
| `--check` | Check for available updates, no changes |
| `--dry-run` | Show what would change, no changes |
| `--force` | Update all framework files without prompting |
| `--validate` | Run packaging validator only |
| `--help` | Show help message |
Mechanics: `ensure_remote()` adds/fetches `cog-upstream/main`; `file_has_changes()` diffs local vs `git show ${REMOTE_NAME}/${BRANCH}:${file}`; `update_file()` overwrites via `git show`; `backup_file()` copies to `${file}.backup-$(date +%Y%m%d-%H%M%S)`; warns if worktree is dirty (`cog-update.sh:228`).
Truncated in chunk: full script is 566 lines; chunk notes "... (truncated, 6451 more characters)" (`cog-update.sh:334`), so main-loop/validator tail was not visible.

## COG-VERSION, GEMINI.md, manifests
`COG-VERSION` content verbatim (`COG-VERSION:1`):
```
3.13.0
```
`GEMINI.md` role (`GEMINI.md:3`): "You are operating inside a **COG second brain** — a self-evolving knowledge management system built on Obsidian markdown files and Git." Vault map (`GEMINI.md:11`): `00-inbox/` profiles, `01-daily/` briefs/checkins, `02-personal/` braindumps, `03-professional/` braindumps + watchlist, `04-projects/[project-slug]/`, `05-knowledge/` consolidated/patterns/timeline/booklets, `06-templates/`. Skills (`GEMINI.md:30`): `/onboarding`, `/braindump`, `/daily-brief`, `/weekly-checkin`, `/knowledge-consolidation`, `/url-dump`, `/update-cog`, `/auto-research`, `/create-user-story`, `/generate-prd`, `/generate-release-notes`, `/export-open-issues`, `/publish-to-confluence`, `/update-knowledge-base`.
`marketplace-entry.json` (`marketplace-entry.json:2`): `name: cog-second-brain`, `version: 3.13.0` (`marketplace-entry.json:10`), category `productivity`. `plugin.json` (`plugin.json:2`): `name: cog-second-brain`, `version: 3.13.0` (`plugin.json:4`), license `MIT`.

## SETUP.md
Install is 2 steps (`SETUP.md:21`): `git clone https://github.com/huytieu/COG-second-brain.git`, then open the agent and run onboarding. Agent matrix (`SETUP.md:46`): `.claude/skills/` 33 skills, `.kiro/powers/` 7 powers, `.gemini/commands/` + `.gemini/skills/` 7 commands, `AGENTS.md` 33 commands; validator `./scripts/validate-agent-surface.sh`.
Onboarding creates `00-inbox/MY-PROFILE.md`, `MY-INTERESTS.md`, `MY-INTEGRATIONS.md`, `03-professional/COMPETITIVE-WATCHLIST.md`, project folders in `04-projects/`; role packs: Product Manager, Engineering Lead, Engineer, Designer, Founder, Marketer. Post-onboarding tree (`SETUP.md:129`) lists `AGENTS.md`, `.claude/agents|roles|skills`, `.kiro/powers`, `.gemini/commands|skills`, `CLAUDE.md`, and vault folders `00-inbox` through `06-templates` with `01-daily/briefs|checkins` and `05-knowledge/consolidated|patterns|people|booklets|timeline`.
Skill-sync rule: after modifying a skill update `.claude/skills/[name]/SKILL.md`, `AGENTS.md`, `.claude-plugin/plugin.json`, Kiro/Gemini surfaces if supported, support-matrix docs, then run `./scripts/validate-agent-surface.sh`.
Truncated in chunk: full `SETUP.md` is 533 lines; chunk notes "... (truncated, 4029 more characters)" (`SETUP.md:386`), so troubleshooting tail was not visible.

## WORKFLOW.md
Opt-in scope only: "This document governs harness runs, and nothing else" (`WORKFLOW.md:8`); in a run when `/closed-loop`, `/ultragoal`, `/retro`, `/harvest`, `/review-cockpit` was invoked, verification phrasing was used, or `verification_harness: on` is set. V-model (`WORKFLOW.md:16`): decompose left (CP-0 intake, CP-1 spec, CP-2 plan), build at apex (CP-3), verify right with `AC-n`-traced evidence (CP-3v, CP-4, CP-5), ship (CP-6), retro (CP-7).
Checkpoints (`WORKFLOW.md:52`):
| CP | Phase | Gate class | Evidence file |
|---|---|---|---|
| CP-0 | Intake / think | advisory | `evidence/CP-0-intake.md` |
| CP-1 | Spec | blocking (`normal`+) | spec + matrix |
| CP-2 | Plan | blocking (`normal`+) | `evidence/CP-2-plan.md` |
| CP-3v | Component verify | blocking | `evidence/CP-3v-component.md` |
| CP-4 | Integration verify | blocking (`full`+, multi-task) | `evidence/CP-4-integration.md` |
| CP-5 | Acceptance | blocking (mutations) | `evidence/CP-5-acceptance.md` |
| CP-6 | Ship | blocking (external) | `evidence/CP-6-ship.md` |
| CP-7 | Retro | advisory | `04-projects/harness/retro/YYYY-MM-DD-<slug>.md` |
Evidence row contract (`WORKFLOW.md:64`): `EVIDENCE <AC-id> | <checkpoint> | PASS|FAIL | <observation> | <artifact-path-or-command>`. Record via `bash .claude/lib/checkpoint.sh record <run-dir> <CP-id> PASS|FAIL|SKIP <note>`. Risk lanes (`WORKFLOW.md:97`): `tiny` CP-3→CP-5, `normal` CP-1→CP-2→CP-3→CP-3v→CP-5, `full` all through CP-4 + claim-verifier + CP-6 Review Gate, `bug` root-cause ledger path, `backfill` audit only. Classifier: `bash .claude/lib/lane-classify.sh classify "<task>"`.
File homes (`WORKFLOW.md:159`): specs `04-projects/<project>/specs/SPEC-NNN-<slug>.md`, runs `04-projects/harness/runs/<id>/evidence/`, retros `04-projects/harness/retro/`, backlog `04-projects/harness/BACKLOG.md`, logs `.claude/logs/checkpoint-ledger.tsv`, `loop-ledger.tsv`.

**Covers:** `.cursorrules`, `.gitignore`, `AGENTS.md`, `CLAUDE.md`, `cog-update.sh`, `COG-VERSION`, `GEMINI.md`, `marketplace-entry.json`, `plugin.json`, `SETUP.md`, `WORKFLOW.md`
