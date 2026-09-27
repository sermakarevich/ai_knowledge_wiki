---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: huytieu/COG-second-brain

### Q1. What is COG in one sentence, and what does its runtime flow look like?
> [!tip]- Answer
> COG is a self-evolving second brain built on Cognition + Obsidian + Git, where AI agents, markdown files, and version control replace any database with zero vendor lock-in. The flow runs You → AI Agent → 33 Skills → 6 Workers plus 4 read-only Verifiers → `.md` files → Git/iCloud, with outward sync to GitHub, Linear, Slack, and PostHog. See [[wiki/01-overview|Overview]].

### Q2. What does the skill catalog cover, and what order does the PM lifecycle follow?
> [!tip]- Answer
> The catalog spans 8 personal-knowledge skills, 3 team-intelligence skills, 6 PM workflow skills, strategic research, a content factory, an opt-in 5-skill verification harness, 7 craft skills, and a paired anti-slop design set. The PM lifecycle runs Research (`/auto-research`) → PRD (`/generate-prd`) → Stories (`/create-user-story`) → Development → Release Notes (`/generate-release-notes`) → Knowledge Base (`/update-knowledge-base`), with audits and Confluence publishing alongside. See [[wiki/01-overview|Overview]].

### Q3. How do workers, verifiers, and the People CRM divide labor?
> [!tip]- Answer
> Six Sonnet workers handle data-heavy tasks (collection, research, file-ops, execution, publishing, people updates) while the Opus lead session does reasoning and synthesis, with workers writing results to `/tmp/` files and returning only status plus path. Read-only verifiers observe artifacts against acceptance criteria without ever seeing worker output, since pasted context induces narrativisation, and a worker never grades its own homework. People profiles live in `05-knowledge/people/` with tiered enrichment starting at Stub on 1 mention and Moderate on 3+ mentions. See [[wiki/01-overview|Overview]].

### Q4. What do the agent-facing surfaces (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`) each define?
> [!tip]- Answer
> `AGENTS.md` is the universal command reference defining all invocable `/skills` for any markdown-reading agent, while `CLAUDE.md` sets always-apply framework instructions for response style, opt-in verification, delegation caps, and Sonnet/Opus model routing. `.cursorrules` is the Cursor-compatible mirror of `CLAUDE.md` exposing skills, worker/verifier agents, the brain-first protocol, and the vault structure, and `GEMINI.md` scopes Gemini CLI to the vault layout, profile reads, named skills, and Obsidian Tasks emoji format with 7-day news freshness. See [[wiki/02-top-level-files|Top-level-files]].

### Q5. How do `cog-update.sh`, `SETUP.md`, and the version manifests keep framework evolution safe?
> [!tip]- Answer
> `cog-update.sh` updates only listed framework files file-by-file from the `cog-upstream` remote without touching personal content folders, with `--check`, `--dry-run`, `--force`, and `--validate` flags plus timestamped backups. `SETUP.md` prescribes the 2-step install (clone, run onboarding) with the multi-agent support matrix and a skill-sync rule enforced by `./scripts/validate-agent-surface.sh`. `COG-VERSION`, `marketplace-entry.json`, and `plugin.json` pin packaging at version `3.13.0`. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. When does `WORKFLOW.md` apply, and what are its checkpoints, risk lanes, and evidence rules?
> [!tip]- Answer
> `WORKFLOW.md` governs harness runs only and nothing else, applying solely when a `/closed-loop`-family skill was invoked, verification phrasing was used, or `verification_harness: on` is set. It walks an opt-in V-model through gated checkpoints CP-0 to CP-7 with risk lanes (`tiny`, `normal`, `full`, `bug`, `backfill`) and stores run artifacts under `04-projects/harness/`. Every evidence row must trace `EVIDENCE <AC-id> | <checkpoint> | PASS|FAIL | <observation> | <artifact-path-or-command>`. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. (Evaluation) Should you adopt COG as your second brain, and what must you accept first?
> [!tip]- Answer
> Recommend COG when you want a markdown-and-Git second brain with a broad 33-skill catalog, multi-agent surfaces, and opt-in verification rigor that stays off by default. Before adopting, verify you accept the ~2-minute clone-and-onboard setup, per-agent skill surfaces that must be re-validated after edits, and the discipline of file-based handoffs plus opt-in harness overhead for high-stakes work. See [[wiki/01-overview|Overview]].
