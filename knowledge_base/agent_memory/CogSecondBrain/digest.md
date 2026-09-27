> [[index|Wiki]] | [[summary|Summary]]
# huytieu/COG-second-brain — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** COG is a self-evolving second brain built on Cognition + Obsidian + Git — AI agents, markdown files, and version control with no database and no vendor lock-in.
## Key points
- COG is defined as **Cognition + Obsidian + Git**, a self-evolving second brain where `.md` files do the thinking, with no database and no vendor lock-in (`README.md:9`).
- The runtime flow is You → AI Agent → 33 Skills → 6 Workers plus 4 read-only Verifiers → `.md` files → Git/iCloud, with external sync to GitHub / Linear / Slack / PostHog (`README.md:17-29`).
- Onboarding takes ~2 minutes: clone the repo, run onboarding in your agent (per-agent command table), optionally via `npx skills add huytieu/COG-second-brain` (`README.md:35-58`).
- COG ships a full Claude Code surface (33 skills + 10 agents) and a full Antigravity surface (pointer stubs delegating to authoritative `.claude/` playbooks), plus an Agent Plugins standard surface, Cursor plugin + rules, 7 Kiro powers, 7 Gemini CLI commands, and `AGENTS.md` as universal fallback (`README.md:64-74`).
- The skill catalog spans personal knowledge (8 skills), team intelligence (3), PM workflows (6 forming a Research → PRD → Stories → Release Notes → Knowledge Base lifecycle), strategic research, content factory, an opt-in verification harness (5 skills), craft skills (7), and a paired anti-slop design set (`README.md:80-172`).
- Workers run data-heavy tasks cheaply on Sonnet while the lead session reasons on Opus; workers write results to `/tmp/` files and return status + path, and verifiers receive paths only to avoid narrativisation (`README.md:177-199`).
- People CRM keeps evidence-based team profiles in `05-knowledge/people/` with tiered enrichment (Stub at 1 mention, Moderate at 3+ mentions); the chunk truncates the Tier 2 description mid-word so further tiers are not described here (`README.md:203-208`).
## 2. [[wiki/02-top-level-files|top-level-files]]
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
## The system in five moves
1. You clone the repo and run onboarding (~2 minutes), personalizing profiles and vault folders for your agent surface.
2. You speak in natural language to any supported agent (Claude Code, Antigravity, Cursor, Kiro, Gemini CLI, Codex, or any markdown reader via `AGENTS.md`), invoking one of 33 skills.
3. Skills decompose work across cheap Sonnet workers (collect, research, file-ops, execute, publish, people-update) while the Opus lead reasons and synthesizes via `/tmp/` file handoffs.
4. Everything lands as `.md` files in the vault (`00-inbox` through `06-templates`), synced by Git/iCloud and pushed outward to GitHub / Linear / Slack / PostHog / Confluence.
5. Opt-in rigor is available but never default: the V-model harness (CP-0–CP-7, risk lanes) and read-only verifiers check artifacts with traced evidence only when asked.
6. Framework evolution stays safe via `cog-update.sh` file-by-file updates from `cog-upstream` and the agent-surface validator, never touching personal content.
