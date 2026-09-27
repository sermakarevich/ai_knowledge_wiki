[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level files
**In one sentence:** The repo root defines a public generic plugin layer plus a private on-disk config layer, with architecture, install, FAQ, examples, and backlog docs describing how the 20 skills install, configure, compose, and version.
## Key points
- The plugin is split into a public git repo (skills, references, docs; no personal data) and a private layer at `~/.config/makerskills/` located via `MAKERSKILLS_CONFIG`, so `git pull` never touches personal files (ARCHITECTURE.md:5-18, ARCHITECTURE.md:41-44).
- The 20 skills group into 6 families (meta `-ify` trifecta, decision & strategy, knowledge & content consumption, output & creative, operations & utilities, plus cross-family patterns), with the `-ify` family fixed at three members by the Rule of 3 (ARCHITECTURE.md:62-114).
- A `SKILL.md` file IS the skill — markdown workflow logic Claude executes at invocation time, so iterating means editing markdown with no build step (ARCHITECTURE.md:150-161).
- Skills compose by name with central hubs (`watch-video` 54 refs, `second-brain` 48, `skillify` 51, `slide-deck` 38), so adopters should set up central skills first (`watch-video` needs yt-dlp + ffmpeg + MLX-Whisper; `second-brain` needs a vault path) (ARCHITECTURE.md:128-146).
- Versioning is two-level semver: plugin release tag plus independent per-skill `metadata.version`, with PATCH/MINOR/MAJOR rules for each level (ARCHITECTURE.md:180-199).
- Install is plugin install (`/plugin marketplace add` + `/plugin install`, or git-clone symlink), env vars in `~/.zshenv`, personal configs under `$MAKERSKILLS_CONFIG/`, per-skill runtime deps, and optional API keys with free fallbacks (INSTALL.md:5-19, INSTALL.md:23-43, INSTALL.md:61-83, INSTALL.md:84-101).
- `.gitignore` guards the public/private boundary by ignoring secrets, overlays, and in-repo archives (`*.local.md`, `skills/*/references/*archive*/`, `skills/*/references/decks-archive.md`), while `FAQ.md`, `EXAMPLES.md`, and `BACKLOG.md` cover onboarding/debugging, one worked example per skill, and the shipped-vs-candidate roadmap (`.gitignore:6-24`, `FAQ.md:7-24`, `BACKLOG.md:7-15`).
---
## .gitignore — public/private boundary guard
Keeps personal data, secrets, and working files out of the public repo (`.gitignore:1-24`):

```gitignore
.DS_Store
*.swp
*.swo
.idea/
.vscode/
node_modules/
.env
.env.local

# Personal overlays — never commit
*.local.md
*.local.yaml
*.local.json
*-local.md

# Migration working files — not for public repo
MIGRATION-TO-PUBLIC.md
*-local-backup.md

# Personal archives live in $MAKERSKILLS_CONFIG (~/.config/makerskills), never in-repo.
# Guard against skills accidentally writing old-style in-repo archives:
skills/*/references/*archive*/
skills/*/references/decks-archive.md
```

## ARCHITECTURE.md — mental model
### Two-layer split
Public layer holds `skills/*/SKILL.md`, `skills/*/references/*.md`, README/INSTALL docs with no personal data, keys, or portfolio names; private layer holds per-skill YAML, voice overlays, board configs, and `archive/` dirs under `~/.config/makerskills/` (ARCHITECTURE.md:5-36). Why it matters: repo is safe to share/fork (public flip via `git filter-repo` on 2026-06-28), data migrates by copying the config dir, and updates don't break config (ARCHITECTURE.md:38-44).

Env var contract (ARCHITECTURE.md:46-54):

```bash
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
```

Additional per-skill vars only for paths outside the config dir: `SECOND_BRAIN_VAULT`, `COMPANY_BRAIN_VAULT`, `COMPANY_CFO_ROOT`, `SLIDE_DECK_REPO` (ARCHITECTURE.md:52).

### Skill families (20 skills, 6 families)
- Meta `-ify` trifecta: `skillify`, `toolify`, `loopify`; Rule of 3 — stays at three (ARCHITECTURE.md:64-70).
- Decision & strategy: `decide`, `business-brainstorm`, `deep-research`, `domain`, `unstuck`, `maker-council`; thread: structured input → structured output → archived (ARCHITECTURE.md:72-83).
- Knowledge & content consumption: `second-brain`, `company-brain`, `read-book`, `watch-video`; thread: compile raw → wiki → outputs (ARCHITECTURE.md:87-94).
- Output & creative: `jab-hook`, `slide-deck`; thread: strong voice + brand-perfect output (ARCHITECTURE.md:98-103).
- Operations & utilities: `pm`, `personal-cfo`, `company-cfo`, `paste`, `social-fetch`; thread: cadence + discipline (ARCHITECTURE.md:107-114).
- Cross-family patterns: personal ↔ team siblings (`second-brain` ↔ `company-brain`, `personal-cfo` ↔ `company-cfo`) and the `-ify` extension trifecta (ARCHITECTURE.md:118-122).

### Composition map
```
                      watch-video (54 refs)
                          ↓
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
     skillify (51)   second-brain (48)   slide-deck (38)
          ↓               ↓
     (record → skill)  company-brain (33)
                          ↓
                      domain (32)
```
(ARCHITECTURE.md:128-144). `skillify from-video`, `slide-deck` talk-recordings, and capture/query flows drive the counts; central skills carry more downstream load (ARCHITECTURE.md:142-146).

### SKILL.md as executable documentation
Consequences verbatim: every SKILL.md is human-readable; iterating is markdown editing; debugging is reading; the `description` field's precision matters most for routing (ARCHITECTURE.md:150-159).

### Sibling ecosystem
| Repo | Scope |
|---|---|
| `makerskills` | Personal operator's craft — this repo |
| `marketingskills` | 46 marketing skills (CRO, copywriting, SEO, ads) |

(ARCHITECTURE.md:165-171). Cross-plugin refs (e.g. `makerskills:paste`) resolve at invocation time with no manifest linking; `skillify` reads `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/skillify/repos.yaml` for private plugins (ARCHITECTURE.md:173-174).

### Versioning policy
Plugin tag = collection version (see `CHANGELOG.md`); per-skill `metadata.version` evolves independently, so `v0.5.0` may contain `0.1.0`–`0.3.1` skills simultaneously (ARCHITECTURE.md:180-186). Skill bump: PATCH = docs/typo/non-behavioral; MINOR = new mode/sub-workflow/composition/references file; MAJOR = breaking invocation/mode/schema change (ARCHITECTURE.md:188-192). Plugin bump: MINOR = net-new skill or coordinated update; PATCH = docs/infra polish; MAJOR = reserved stable milestone, not yet reached (ARCHITECTURE.md:194-199).

### Design principles
1. Documentation-first, automation-second. 2. Composability over completeness. 3. Structured input, structured output, archived to disk. 4. Voice matters. 5. Graceful degradation. 6. Personal data stays private. 7. Cite everything. 8. Cadence + rituals over one-off invocations (ARCHITECTURE.md:203-212).

## INSTALL.md — install and configure
Step 1 — install the plugin (INSTALL.md:5-19):

```
/plugin marketplace add coreyhaines31/makerskills
/plugin install makerskills@makerskills
```

```bash
git clone https://github.com/coreyhaines31/makerskills ~/code/makerskills
ln -s ~/code/makerskills ~/.claude/plugins/makerskills
```

Step 2 — environment (`~/.zshenv` or `~/.bashrc`) (INSTALL.md:23-43):

| Variable | Purpose | Default |
|---|---|---|
| `MAKERSKILLS_CONFIG` | Personal config / archives root | `$HOME/.config/makerskills` |
| `SLIDE_DECK_REPO` | Where slide-deck writes branded React decks | `$HOME/code/your-personal-site-repo` |
| `SECOND_BRAIN_VAULT` | second-brain personal wiki vault | `$HOME/Documents/SecondBrain` |
| `COMPANY_BRAIN_VAULT` | company-brain team vault | `$HOME/Documents/CompanyBrain` |
| `COMPANY_CFO_ROOT` | company-cfo financial workflow root | `$HOME/code/company-cfo` |
| `SLIDE_DECK_DEV_HOST` | slide-deck preview URL pattern | `localhost:3000` |

Step 3 — personal configs under `$MAKERSKILLS_CONFIG/` (gitignored), e.g. copy `skills/jab-hook/references/typefully-config.example.yaml` → `~/.config/makerskills/jab-hook/typefully.yaml` and `properties.example.yaml` → `properties.yaml` (INSTALL.md:45-60). Step 4 — runtime deps, only what you use: `brew install yt-dlp ffmpeg pandoc git-filter-repo`, `brew install uv` + `uv tool install mlx-whisper`, optional `basictex` + fonts and `calibre` for `ebook-convert` (INSTALL.md:62-83). Step 5 — API keys (all optional, free fallbacks): `NOTION_API_KEY`, `TYPEFULLY_API_KEY`, `GEMINI_API_KEY`, `SCRAPECREATORS_API_KEY`, `BRAVE_API_KEY`, `PLANE_API_KEY`, `LINEAR_API_KEY`, `DOMAINR_API_KEY`, `NAMECHEAP_API_USER`, `NAMECHEAP_API_KEY`, `NAMECHEAP_API_KEY` + whitelisted `NAMECHEAP_CLIENT_IP` (INSTALL.md:84-101). Step 6 — verify: `ls ~/code/makerskills/skills/` shows 20 skills; try `/skillify`, `/decide`, `/paste`, `/company-brain`, `/company-cfo`, `/domain` (INSTALL.md:103-116). Data locations: `~/.config/makerskills/<skill>/` for config, `~/Documents/<skill>/` for generated outputs; migrate by copying config dir + env vars (INSTALL.md:122-131).

## FAQ.md — onboarding, config, routing, debugging
Getting started: run `/decide` first (no config/deps), then read `skills/decide/SKILL.md`; only `MAKERSKILLS_CONFIG` is required (defaults to `~/.config/makerskills`); install only the runtime deps for skills you use — `decide`, `paste`, `pm`, `personal-cfo` need none (FAQ.md:7-24). Keys go in `~/.zshenv`/`~/.bashrc`, never in repo or config dir; losing the config dir means first-run prompts again — keep it in a private git repo or cloud-synced symlink (FAQ.md:28-47). `skillify` = new SKILL.md (what Claude knows), `toolify` = integration/API/MCP (what Claude can talk to), `loopify` = loop/schedule (what Claude does on cadence) (FAQ.md:53-59). `second-brain` is personal-scope, `company-brain` team-scope with `people/` `companies/` `meetings/` `sops/` `decisions/` + sensitivity tagging; same pattern for `personal-cfo` vs `company-cfo` (FAQ.md:61-67). Cross-refs resolve at invocation time by description match, cross-plugin included, no manifest linking (FAQ.md:75-79). Versioning/plugin-vs-skill split and `CHANGELOG.md` + GitHub Releases pointers (FAQ.md:83-89). Compatibility: Agent Skills spec (`agentskills.io`) early in Codex/Cursor; Mac-default tools (`watch-video` MLX-Whisper, `paste` `pbcopy`/`pbpaste`) need swaps on Linux/Windows; no telemetry — external APIs called directly from your machine (FAQ.md:93-108). Debugging: check SKILL.md `description` triggers and competing adjacent skills (invoke `/skill-name` explicitly); missing siblings degrade gracefully; `source ~/.zshenv` after setting vars; marketplace installs need `/plugin update makerskills`, symlinked dev picks up edits immediately (FAQ.md:112-130). Contributing: fork/branch/PR, MIT rebrand allowed; questions via GitHub Discussions, Issues, `maker-skills.com` (FAQ.md:134-144).

## EXAMPLES.md — one worked example per skill (truncated in chunk)
Hand-authored illustrations, not literal captures; real invocations are longer (EXAMPLES.md:3-5). Covered in full: `skillify` (extract-from-chat; CREATE/ADAPT/UPDATE routing with `/skillify`, `from-video <url>`, `from-scratch`, URL-adapt, `update` shapes) (EXAMPLES.md:9-24); `toolify` (Stripe: 9 structural questions, `context7` docs, `src/lib/stripe.ts` + webhook/example routes + `.env.local.example`, `STRIPE_SECRET_KEY` + `STRIPE_WEBHOOK_SECRET`, pinned SDK, smoke-test curl) (EXAMPLES.md:28-41); `loopify` (Fathom nightly pull; 5 questions; cron vs predictable-timing detection; `CronCreate({ schedule: "0 6 * * *", timezone: "America/Los_Angeles", ... })`; `cron_id` + `CronDelete`; idempotent dedupe; 3-failure bailout) (EXAMPLES.md:45-59); `decide` (hire-vs-freelance; 6 of 38 37signals questions; Decision/Why/Revisit doc archived to `~/.config/makerskills/decide/archive/` + `INDEX.md`) (EXAMPLES.md:63-84); `business-brainstorm` (9 dimensions scored ✓/⚠/❌, Build/Sleep/Kill verdict, stealable angle, archive) (EXAMPLES.md:88-115); `deep-research` (strategy chain WebSearch → `/last30days` → WebFetch → agent-browser; TL;DR + Findings + Sources + Adjacent + Not-found; archive) (EXAMPLES.md:120-149); `unstuck` (gatekeeper-wall capture; T1+T10+T6; 12 angles; `/decide` handoff; archive) (EXAMPLES.md:154-182); `maker-council` (question-type seating, e.g. Jensen Huang + Jason Fried with Naval Ravikant dissenter; disagreement map; chair synthesis → `/decide`; archive) (EXAMPLES.md:186-224); `domain` (budget ask; 30 candidates; Vercel dry-run + whois + Domainr + Namecheap; AVAILABLE/AFTERMARKET/TAKEN buckets; USPTO via `agent-browser` + social checks for top 3) (EXAMPLES.md:228-251); `second-brain` capture (fetch → `<vault>/raw/*.md` with `source:` + `captured:` front-matter) and compile (`## Sources` grep, merge into `[[...]]` page, update `wiki/INDEX.md`) (EXAMPLES.md:255-270); `company-brain` capture (meetings dir detection; multi-author front-matter `source:` `author:` `captured:` `sensitivity:` `attendees:` `company:` `duration_min:` `recording_url:`) (EXAMPLES.md:274-290). Chunk truncates mid-`company-brain` compile mode at "If j" — the remaining ~8355 characters (rest of `company-brain` plus any further skills) were cut, so they are not covered here.

## BACKLOG.md — shipped log and candidates
Shipped (BACKLOG.md:7-15): v1.5.0 `maker-council` (8-member bench, dissenter, dossier + live-research pass, disagreement map, `/decide` handoff; issue #1); v1.3.0 `unstuck` (6-type wall taxonomy, 10-technique inventory, 10-angle gate, honest-exit guardrail; issue #9); v0.5.0 `domain` (11-step availability-first hunt: Vercel CLI + whois + Domainr + Namecheap + rdap.org + agent-browser USPTO); v0.4.0 `company-cfo` (team-scope `personal-cfo` sibling; snapshots + cash pulse + projector; `toolify` sources + `loopify` schedule); v0.3.0 `company-brain` (team-scope `second-brain` sibling; structured raw dirs + multi-author + auto-sync; Company Brain Setup backbone); v0.2.0 `-ify` trifecta (`skillify`/`toolify`/`loopify`; Rule of 3). Candidates: `weekly-review`, `intro-broker`, `thanks-no`, `daily-startup`, `swipe-save`, `new-project`, `gh-triage`, `bjj-log` (BACKLOG.md:19-27); brainstorm (non-skill, via `/business-brainstorm`): Company Brain Setup productized service ~$2–5K + retention (BACKLOG.md:29-33).

**Covers:** `.gitignore`, `ARCHITECTURE.md`, `BACKLOG.md`, `EXAMPLES.md` (truncated — see note above), `FAQ.md`, `INSTALL.md`
