# Technical Analysis: coreyhaines31/makerskills

**Repository:** https://github.com/coreyhaines31/makerskills
**Version analyzed:** unknown
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview

Problem space: founders and indie operators repeat the same judgment-heavy workflows — triaging decisions, pressure-testing ideas, researching with citations, maintaining personal and team knowledge bases, producing content and decks, running CFO cadence, hunting domains — across disconnected tools and chat threads with no durable output. The repo addresses it with a plugin of 20–21 documentation-first AI agent skills covering decisions, research, second-brain workflows, content rotation, scenario modeling, CFO cadence, domain hunts, and meta-skills for authoring more skills (README:11; ARCHITECTURE.md:62-114). Each skill is invoked as a slash command (e.g. `/decide`) or by reading `skills/<name>/SKILL.md` and executing the steps by hand; the first-touch pattern is structured input → structured output → written to disk, exemplified by `/decide` triaging 37signals-framework questions and archiving with a revisit date (README:56-62, README:64-70). The primary user is the founder/operator running Claude Code, Codex, Cursor, or another Agent Skills host, with companion site maker-skills.com (README:13, README:15).

## 2. High-Level Architecture

The system is a two-layer markdown plugin with no runtime server: a public generic repo layer executed by the host agent, and a private on-disk config/archive layer holding personal data (ARCHITECTURE.md:5-36).

```
                    ┌─────────────────────────────────┐
                    │ Agent Skills host               │
                    │ Claude Code │ Codex │ Cursor    │  (README:13)
                    └───────────────│─────────────────┘
                                    ▼
                    ┌─────────────────────────────────┐
                    │ skills/<name>/SKILL.md           │
                    │ + references/*.md               │  public repo layer
                    │ + README / INSTALL / FAQ        │  (ARCHITECTURE.md:5-36)
                    └───────────────│─────────────────┘
                                    ▼
                    ┌─────────────────────────────────┐
                    │ skill composition by name       │
                    │ watch-video ► skillify          │
                    │             ► second-brain ─►   │
                    │               company-brain ►   │
                    │               domain            │  (ARCHITECTURE.md:128-144)
                    └───────────────│─────────────────┘
                                    ▼
                    ┌─────────────────────────────────┐
                    │ $MAKERSKILLS_CONFIG/<skill>/    │
                    │ ~/.config/makerskills (default) │  private layer
                    │ vaults │ archives │ overlays    │  (ARCHITECTURE.md:46-54)
                    └─────────────────────────────────┘
```

Data flow:

1. User invokes a slash command (e.g. `/decide`, `/paste twitter`) or opens the corresponding `skills/<name>/SKILL.md`; the host agent loads the markdown workflow logic (README:64-70, ARCHITECTURE.md:150-161).
2. The skill collects structured input through scripted questions (e.g. 6–8 triaged from 38 in `decide`; 9 structural questions in `toolify`; 5 questions in `loopify`) (EXAMPLES.md:63-84, EXAMPLES.md:28-41, EXAMPLES.md:45-59).
3. The agent executes the workflow, calling sibling skills by name rather than reimplementing adjacent jobs (e.g. `business-brainstorm` composes with `deep-research` + `domain`; `skillify from-video` drives `watch-video`) (README:175-186).
4. External tools and APIs are called directly from the user's machine with graceful degradation to free fallbacks when keys are absent (INSTALL.md:84-101, FAQ.md:93-108).
5. Structured output (decision record, research brief, deck, kanban update, CFO snapshot) is written to disk under the private config dir or vault, with archives indexed (e.g. `decide/archive/` + `INDEX.md`) (EXAMPLES.md:63-84, INSTALL.md:122-131).
6. Cadence skills (`company-cfo`, `company-brain` auto-sync via `loopify`) re-read the archived state on schedule; cross-skill propagation and semver bumps carry improvements forward (ARCHITECTURE.md:188-199).

Persistent state lives outside the repo: per-skill YAML, voice overlays, board configs, and `archive/` directories under `$MAKERSKILLS_CONFIG` (default `~/.config/makerskills`), plus vault paths (`SECOND_BRAIN_VAULT`, `COMPANY_BRAIN_VAULT`), financial roots (`COMPANY_CFO_ROOT`), deck repos (`SLIDE_DECK_REPO`), and generated outputs under `~/Documents/<skill>/` (ARCHITECTURE.md:5-36, ARCHITECTURE.md:46-54, INSTALL.md:122-131). The repo itself stores no personal data, keys, or portfolio names, and `git pull` never touches personal files (ARCHITECTURE.md:38-44).

## 3. The Skill (SKILL.md as Executable Documentation)

Representation: a skill is a directory `skills/<name>/` whose `SKILL.md` file is the executable artifact — markdown workflow logic the host agent executes at invocation time, with supporting `references/*.md` files. Consequences stated verbatim in the wiki: every SKILL.md is human-readable; iterating is markdown editing; debugging is reading; the `description` field's precision matters most for routing (ARCHITECTURE.md:150-159). There is no build step.

Named kinds/types (6 families, 20 skills per ARCHITECTURE.md:62-114; the README routing table lists 21 intents at README:90-112):

- Meta `-ify` trifecta (fixed at three by the Rule of 3): `skillify`, `toolify`, `loopify` (ARCHITECTURE.md:64-70). `skillify` has CREATE (from-chat / from-video / from-dump / from-scratch), ADAPT (port external skill with license check + attribution), UPDATE (cross-skill propagation + semver discipline) modes; `toolify` wires integrations/APIs/MCP into Next.js or Rails projects; `loopify` is the judgment layer over `ScheduleWakeup` / `CronCreate` / `/loop` (README:122-125).
- Decision and strategy: `decide`, `business-brainstorm`, `deep-research`, `domain`, `unstuck`, `maker-council`; thread: structured input → structured output → archived (ARCHITECTURE.md:72-83). `decide` uses the 37signals framework (38 questions + house additions such as Q39 opportunity cost, triaged to 6–8 per decision) (README:132-137).
- Knowledge and content consumption: `second-brain`, `company-brain`, `read-book`, `watch-video`; thread: compile raw → wiki → outputs (ARCHITECTURE.md:87-94). `second-brain` implements the Karpathy LLM Wiki workflow (capture / compile / query / lint / connect / search); `company-brain` is its team-scope sibling with structured raw dirs and sensitivity tagging (README:144-148).
- Output and creative: `jab-hook`, `slide-deck`; thread: strong voice + brand-perfect output (ARCHITECTURE.md:98-103).
- Operations and utilities: `pm`, `personal-cfo`, `company-cfo`, `paste`, `social-fetch`; thread: cadence + discipline (ARCHITECTURE.md:107-114).
- Cross-family patterns: personal ↔ team siblings (`second-brain` ↔ `company-brain`, `personal-cfo` ↔ `company-cfo`) and the `-ify` extension trifecta (ARCHITECTURE.md:118-122).

Key queries: routing is by intent-to-skill description match at invocation time, with no manifest linking, including cross-plugin refs such as `makerskills:paste` (ARCHITECTURE.md:173-174, FAQ.md:75-79). The 21-row routing table maps statements like "Think through a decision with a real fork" → `decide`, "Break through a wall" → `unstuck`, "Find an available `.com`" → `domain`, "Create, adapt, or update a skill" → `skillify` (README:90-112). Each skill's SKILL.md `description` carries trigger phrases plus disambiguation from adjacent skills (README:88-114). Verbatim composition example:

```
**`watch-video`** (54 refs) | `second-brain` (capture summary), `skillify from-video`, `social-fetch` (X/IG/TikTok metadata), `pm` (action items), `decide` (flagged decisions)
```

(README:175-186).

## 4. LLM / External Service Integration

The repo calls no LLM or API itself. It is prompt-and-workflow content executed by the host agent (Claude Code, Codex, Cursor, other Agent Skills hosts per README:13); all model calls belong to the host. External services are invoked by the agent following skill instructions, and every API key is optional with a free fallback (INSTALL.md:84-101, FAQ.md:93-108). External calls originate directly from the user's machine; there is no telemetry (FAQ.md:93-108).

| Provider / tool | Required vs optional | Used by | Env var |
|---|---|---|---|
| Host LLM (Claude Code / Codex / Cursor / Agent Skills host) | Required (execution substrate, not a repo dependency) | all skills | none |
| Vercel CLI (domain dry-run) | Optional (ensemble member) | `domain` | none |
| whois per-TLD + `rdap.org` (modern TLDs) | Optional (ensemble member) | `domain` | none |
| Domainr API | Optional | `domain` | `DOMAINR_API_KEY` |
| Namecheap API | Optional | `domain` | `NAMECHEAP_API_USER`, `NAMECHEAP_API_KEY`, whitelisted `NAMECHEAP_CLIENT_IP` |
| USPTO trademark screening via `agent-browser` | Optional | `domain` | none |
| Aftermarket click-throughs (HugeDomains / Afternic / Sedo / Dan) | Optional | `domain` | none |
| WebSearch / WebFetch / `agent-browser` / `/last30days` / memory | Optional (research chain) | `deep-research` | none |
| Brave API | Optional | `deep-research` (fallback chain) | `BRAVE_API_KEY` |
| Gemini-native multimodal | Optional | `watch-video` | `GEMINI_API_KEY` |
| ScrapeCreators API | Optional | `social-fetch` | `SCRAPECREATORS_API_KEY` |
| Typefully API | Optional | `jab-hook` | `TYPEFULLY_API_KEY` |
| Notion API | Optional | `pm` (adapter) | `NOTION_API_KEY` |
| Plane API | Optional | `pm` (adapter) | `PLANE_API_KEY` |
| Linear API | Optional | `pm` (adapter) | `LINEAR_API_KEY` |
| GitHub / Obsidian / manual adapters | Optional | `pm` | none stated |
| Bank + payment processor + payroll + expense-mgmt via `toolify`-wired integrations | Optional | `company-cfo` | per-integration (e.g. `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` in the worked example) |
| Fathom / Gong / Granola / CRM auto-sync | Optional | `company-brain`, `ingest` | none stated |
| Grain / Zoom / Granola / Fathom transcripts | Optional (input) | `ingest` | none stated |
| YouTube / Loom / Vimeo / Riverside / Zoom / MP4 tooling | Optional (input) | `watch-video` | none |

Path configuration env vars (INSTALL.md:23-43, ARCHITECTURE.md:46-54): `MAKERSKILLS_CONFIG` (only required var, defaults to `~/.config/makerskills`), `SECOND_BRAIN_VAULT`, `COMPANY_BRAIN_VAULT`, `COMPANY_CFO_ROOT`, `SLIDE_DECK_REPO`, `SLIDE_DECK_DEV_HOST`. Keys are stored in `~/.zshenv`/`~/.bashrc`, never in the repo or config dir (FAQ.md:28-47).

## 5. The Invocation Pipeline (Structured Input → Structured Output → Archived)

The primary workflow is shared across families with per-skill parameters: collect structured input, execute with composition, write the artifact to disk (ARCHITECTURE.md:203-212 principle 3; decision-thread ARCHITECTURE.md:72-83; knowledge-thread ARCHITECTURE.md:87-94). There are no Python functions; every step below is a skill-doc procedure cited to its wiki location.

1. Install and configure (`INSTALL.md:5-19`, `INSTALL.md:23-43`): add and install the plugin (`/plugin marketplace add` + `/plugin install`, or git-clone symlink), export `MAKERSKILLS_CONFIG` in `~/.zshenv`, copy per-skill example configs (e.g. `skills/jab-hook/references/typefully-config.example.yaml` → `~/.config/makerskills/jab-hook/typefully.yaml`) (`INSTALL.md:45-60`), install only the runtime deps for skills used (`INSTALL.md:62-83`), verify with `ls ~/code/makerskills/skills/` and a no-config skill such as `/decide` or `/paste` (`INSTALL.md:103-116`, `FAQ.md:7-24`).
2. Route intent to skill (`README:90-112`, `FAQ.md:112-130`): match the operator's "I want to..." statement against the routing table and each SKILL.md `description` trigger; on ambiguity invoke `/skill-name` explicitly rather than relying on description match.
3. Answer the skill's structural questions (`EXAMPLES.md:28-41`, `EXAMPLES.md:45-59`, `EXAMPLES.md:63-84`): e.g. `decide` triages 6 of 38 37signals questions for a hire-vs-freelance fork; `toolify` asks 9 integration questions before reading `context7` docs; `loopify` asks 5 scheduling questions and selects cron vs dynamic vs one-shot.
4. Run the domain procedure with composition (`README:175-186`, `ARCHITECTURE.md:128-144`): `domain` brainstorms ~30 candidates then buckets AVAILABLE/AFTERMARKET/TAKEN via Vercel dry-run + whois + Domainr + Namecheap, with USPTO screening via `agent-browser` and social-handle checks on the top 3 (`EXAMPLES.md:228-251`); `deep-research` chains WebSearch → `/last30days` → WebFetch → agent-browser into TL;DR + Findings + Sources + Adjacent + Not-found (`EXAMPLES.md:120-149`); `unstuck` classifies the wall type, applies lateral-thinking techniques with a 10-angle minimum, then hands off to `/decide` (`EXAMPLES.md:154-182`).
5. Capture and compile side effects (`EXAMPLES.md:255-270`, `EXAMPLES.md:274-290`): `second-brain` capture writes fetch results to `<vault>/raw/*.md` with `source:` + `captured:` front-matter, then compiles by grepping `## Sources` and merging into `[[...]]` pages with `wiki/INDEX.md` updates; `company-brain` capture adds multi-author front-matter (`source:`, `author:`, `captured:`, `sensitivity:`, `attendees:`, `company:`, `duration_min:`, `recording_url:`).
6. Archive with revisit metadata and index (`EXAMPLES.md:63-84`, `EXAMPLES.md:88-115`): `decide` writes a Decision/Why/Revisit doc to `~/.config/makerskills/decide/archive/` + `INDEX.md`; `business-brainstorm` records 9-dimension ✓/⚠/❌ scores with a Build/Sleep/Kill verdict and stealable angle; `maker-council` maps disagreements across seated members (e.g. Jensen Huang + Jason Fried with Naval Ravikant dissenter) and synthesizes a call before `/decide` handoff (`EXAMPLES.md:186-224`).
7. Schedule or wire follow-ups where applicable (`EXAMPLES.md:45-59`, `README:122-125`): `loopify` emits `CronCreate({ schedule: "0 6 * * *", timezone: "America/Los_Angeles", ... })` with `cron_id` + `CronDelete`, idempotent dedupe, and a 3-failure bailout; `toolify` emits client wrappers, webhook/example routes, `.env.local.example`, pinned SDK versions, and smoke-test curl commands.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | refed as README:11–199 | Plugin overview: tagline, hosts, install, 5-minute path, 21-skill routing table, `-ify`/decision/knowledge/output/ops category tables, compose graph, truncated Architecture lead-in |
| `ARCHITECTURE.md` | refed as ARCHITECTURE.md:5–212 | Mental model: public/private two-layer split, env-var contract, 6 skill families, composition map, SKILL.md-as-executable-doc, sibling ecosystem, two-level semver, 8 design principles |
| `INSTALL.md` | refed as INSTALL.md:5–131 | Install and configure: plugin install, env-var table, personal-config copies, per-skill runtime deps, optional API keys, verify steps, data locations and migration |
| `FAQ.md` | refed as FAQ.md:7–144 | Onboarding, config, routing, debugging: first-run path, key storage, `-ify` disambiguation, personal-vs-team siblings, cross-ref resolution, versioning, host compatibility, contributing |
| `EXAMPLES.md` | refed as EXAMPLES.md:3–290 (truncated) | One worked example per skill: `skillify`/`toolify`/`loopify`/`decide`/`business-brainstorm`/`deep-research`/`unstuck`/`maker-council`/`domain`/`second-brain`/`company-brain` (capture + compile); remainder cut in chunk |
| `BACKLOG.md` | refed as BACKLOG.md:7–33 | Shipped log (v0.2.0–v1.5.0) and candidate skills (`weekly-review`, `intro-broker`, `thanks-no`, `daily-startup`, `swipe-save`, `new-project`, `gh-triage`, `bjj-log`) plus a productized-service brainstorm |
| `CHANGELOG.md` | referenced, not excerpted | Plugin-level release history backing the collection-version half of two-level semver (ARCHITECTURE.md:180-186, FAQ.md:83-89) |
| `.gitignore` | `.gitignore:1-24` | Public/private boundary guard: ignores secrets, `*.local.*` overlays, migration working files, and in-repo archive paths |
| `skills/decide/SKILL.md` | referenced via README:56-68, EXAMPLES.md:63-84 | 37signals decision workflow; zero-config entry point; archives Decision/Why/Revisit docs |
| `skills/second-brain/SKILL.md` | referenced via README:144-148, EXAMPLES.md:255-270 | Personal markdown-vault workflow (Karpathy LLM Wiki): capture / compile / query / lint / connect / search |
| `skills/company-brain/SKILL.md` | referenced via README:144-148, EXAMPLES.md:274-290 | Team-scope sibling of second-brain with structured raw dirs, multi-author attribution, sensitivity tagging, trust levels |
| `skills/watch-video/SKILL.md` | referenced via README:175-186 (54 refs) | Central ingestion hub: transcript / visual / multimodal extraction for YouTube, Loom, Vimeo, Riverside, Zoom, MP4 |
| `skills/skillify/SKILL.md` | referenced via README:122-125, EXAMPLES.md:9-24 | Meta-skill for CREATE/ADAPT/UPDATE of skills in any sibling repo |
| `skills/domain/SKILL.md` | referenced via README:132-137, EXAMPLES.md:228-251 | 11-step availability-first `.com` hunt (Vercel + whois + Domainr + Namecheap + rdap.org + agent-browser USPTO) |
| `skills/jab-hook/references/typefully-config.example.yaml` | referenced via INSTALL.md:45-60 | Example personal config copied to `$MAKERSKILLS_CONFIG/jab-hook/typefully.yaml`; pattern reused for `properties.yaml` |
| `${MAKERSKILLS_CONFIG:-$HOME/.config/makerskills}/skillify/repos.yaml` | referenced via ARCHITECTURE.md:173-174 | Private registry of sibling/private plugin repos that `skillify` reads; cross-plugin refs resolve at invocation time |

## 7. Dependencies

No library manifest is described in the wiki excerpts; constraints below are the exact install strings given in `INSTALL.md:62-83`. All entries are unpinned (no version constraint string appears in the wiki).

| Package | Version constraint | Purpose |
|---|---|---|
| `yt-dlp` (brew) | (none stated) | `watch-video` transcript extraction |
| `ffmpeg` (brew) | (none stated) | `watch-video` media handling |
| `mlx-whisper` via `uv tool install` (after `brew install uv`) | (none stated) | `watch-video` local transcription |
| `pandoc` (brew) | (none stated) | Document conversion (deck/content flows) |
| `git-filter-repo` (brew) | (none stated) | Repo history operations (used in the 2026-06-28 public flip per ARCHITECTURE.md:38-44) |
| `basictex` + fonts (optional) | (none stated) | PDF/TeX output path |
| `calibre` for `ebook-convert` (optional) | (none stated) | `read-book` EPUB/MOBI handling |
| Agent Skills host: Claude Code / Codex / Cursor | (none stated) | Execution substrate for all SKILL.md workflows |
| `pbcopy` / `pbpaste` (macOS default) | (none stated) | `paste` clipboard round-trip; needs swaps on Linux/Windows (FAQ.md:93-108) |
| Next.js / Rails project target | (none stated) | `toolify` integration target; `slide-deck` branded React decks (Next.js) |
| Playwright | (none stated) | `slide-deck` export path |
| `agent-browser` | (none stated) | `deep-research` retrieval; `domain` USPTO screening |
| Vercel CLI | (none stated) | `domain` availability dry-run ensemble member |
| `ScheduleWakeup` / `CronCreate` / `/loop` primitives | (none stated) | `loopify` scheduling substrate |

## 8. CLI / Usage Surface

Entry points: there is no binary or package CLI. Installation uses the host's plugin commands, and usage is slash commands plus direct SKILL.md reads (README:26-38, README:64-70, INSTALL.md:5-19).

| Command | Effect |
|---|---|
| `/plugin marketplace add coreyhaines31/makerskills` | Register the marketplace in Claude Code |
| `/plugin install makerskills@makerskills` | Install the plugin collection |
| `git clone https://github.com/coreyhaines31/makerskills ~/code/makerskills` + `ln -s ~/code/makerskills ~/.claude/plugins/makerskills` | Local-dev alternative (symlinked plugin picks up edits immediately) |
| `/plugin update makerskills` | Update a marketplace install (symlinked dev needs no update step) |
| `/decide`, `/unstuck`, `/maker-council`, `/business-brainstorm`, `/deep-research`, `/domain` | Decision and strategy invocations (README:90-112) |
| `/second-brain`, `/company-brain`, `/read-book`, `/watch-video`, `/ingest` | Knowledge and content-consumption invocations |
| `/jab-hook`, `/slide-deck` | Output and creative invocations |
| `/pm`, `/personal-cfo`, `/company-cfo`, `/paste`, `/social-fetch` | Operations and utilities invocations |
| `/skillify`, `/toolify`, `/loopify` (incl. `/skillify`, `from-video <url>`, `from-scratch`, URL-adapt, `update` shapes) | Meta `-ify` invocations (EXAMPLES.md:9-24) |
| `open ~/code/makerskills/skills/decide/SKILL.md` | Manual read-through of the canonical skill pattern (README:64-68) |
| `/paste twitter` | Clipboard utility: reads clipboard, strips formatting, warns over 280 chars, copies back cleaned output (README:72-78) |
| `/cb review` | Culling pass so unreviewed or deprecated `company-brain` info never poisons answers (README:163-167) |
| `source ~/.zshenv` | Reload env vars after setting them (FAQ.md:112-130) |
| `ls ~/code/makerskills/skills/` | Verify install (expect 20 skill dirs per INSTALL.md:103-116) |

Env-var table (INSTALL.md:23-43, ARCHITECTURE.md:46-54):

| Variable | Purpose | Default |
|---|---|---|
| `MAKERSKILLS_CONFIG` | Personal config / archives root (only required var) | `$HOME/.config/makerskills` |
| `SECOND_BRAIN_VAULT` | `second-brain` personal wiki vault | `$HOME/Documents/SecondBrain` |
| `COMPANY_BRAIN_VAULT` | `company-brain` team vault | `$HOME/Documents/CompanyBrain` |
| `COMPANY_CFO_ROOT` | `company-cfo` financial workflow root | `$HOME/code/company-cfo` |
| `SLIDE_DECK_REPO` | Where `slide-deck` writes branded React decks | `$HOME/code/your-personal-site-repo` |
| `SLIDE_DECK_DEV_HOST` | `slide-deck` preview URL pattern | `localhost:3000` |

Optional API-key vars (INSTALL.md:84-101): `NOTION_API_KEY`, `TYPEFULLY_API_KEY`, `GEMINI_API_KEY`, `SCRAPECREATORS_API_KEY`, `BRAVE_API_KEY`, `PLANE_API_KEY`, `LINEAR_API_KEY`, `DOMAINR_API_KEY`, `NAMECHEAP_API_USER`, `NAMECHEAP_API_KEY`, `NAMECHEAP_CLIENT_IP` (whitelisted). Per-skill personal configs live under `$MAKERSKILLS_CONFIG/<skill>/` (e.g. `jab-hook/typefully.yaml`, `properties.yaml`, `people.yaml` for `ingest` person→project routing, `skillify/repos.yaml`); generated outputs under `~/Documents/<skill>/` (INSTALL.md:45-60, INSTALL.md:122-131).

## 9. Extensibility Points

- New skill → `skillify` CREATE modes (`from-chat` / `from-video` / `from-dump` / `from-scratch`): authors a new `skills/<name>/SKILL.md` plus `references/*.md`, following the SKILL.md-as-executable-doc pattern (README:122-125, EXAMPLES.md:9-24, ARCHITECTURE.md:150-161).
- Port external skill → `skillify` ADAPT mode: license check + attribution, then rewrite into a sibling repo (README:122-125).
- Improve existing skill → `skillify` UPDATE mode: edit the markdown directly (no build step) with cross-skill propagation and PATCH/MINOR/MAJOR discipline at the per-skill `metadata.version` level (README:122-125, ARCHITECTURE.md:188-192).
- New integration/API/MCP → `toolify` wizard: adds auth handling, env vars, client wrapper (e.g. `src/lib/stripe.ts`), webhook/example routes, `.env.local.example`, pinned SDK, and smoke-test curl in a Next.js or Rails target (README:122-125, EXAMPLES.md:28-41).
- Recurring workflow → `loopify`: selects dynamic / cron / one-shot pattern over `ScheduleWakeup` / `CronCreate` / `/loop`, with idempotency and bail-out conditions; `company-brain` auto-sync is the canonical consumer via `toolify`-wired sources (README:122-125, README:163-167, EXAMPLES.md:45-59).
- Personal behavior without forking → `*.local.md` / `*.local.yaml` / `*.local.json` overlays and voice overlays, board-member configs (`maker-council` custom members via config dir), and `people.yaml` routing for `ingest`; all are gitignored and live under `$MAKERSKILLS_CONFIG` (`.gitignore:6-24`, INSTALL.md:45-60).
- Cross-plugin composition → reference sibling skills by name (`makerskills:paste` style); add private plugin paths in `skillify/repos.yaml`; no manifest linking is required because resolution happens at invocation time by description match (ARCHITECTURE.md:173-174, FAQ.md:75-79).
- New skill family → constrained by the Rule of 3 for the `-ify` trifecta (stays at three members) and the personal↔team sibling pattern; backlog candidates (`weekly-review`, `intro-broker`, `thanks-no`, `daily-startup`, `swipe-save`, `new-project`, `gh-triage`, `bjj-log`) show the expected granularity (ARCHITECTURE.md:64-70, BACKLOG.md:19-27).

## 10. Limitations and Gotchas

- **Mac-default tooling breaks on Linux/Windows.** `watch-video` assumes MLX-Whisper and `paste` assumes `pbcopy`/`pbpaste`; both need platform swaps outside macOS, and Agent Skills spec support is still early in Codex/Cursor (FAQ.md:93-108).
- **Marketplace installs go stale silently.** A marketplace install requires an explicit `/plugin update makerskills`, while only the git-clone symlink picks up edits immediately — debugging a "fixed" skill against a stale install wastes a cycle (FAQ.md:112-130).
- **Losing `$MAKERSKILLS_CONFIG` resets personalization.** First-run prompts return for every skill; the mitigation is keeping the config dir in a private git repo or cloud-synced symlink, since the public repo intentionally contains none of it (FAQ.md:28-47, ARCHITECTURE.md:38-44).
- **Routing depends on `description` precision.** Overlapping trigger phrases across adjacent skills misroute invocations; the fix is invoking `/skill-name` explicitly and checking competing descriptions, not rephrasing the request (FAQ.md:112-130, ARCHITECTURE.md:150-159).
- **Missing siblings degrade but also silently narrow results.** Cross-refs resolve at invocation time with no manifest linking, so an absent `deep-research`, `domain`, or `toolify`-wired source produces a thinner answer rather than an error (FAQ.md:75-79, FAQ.md:112-130).
- **Coverage in this analysis is bounded by the wiki excerpts.** The Architecture section in the overview chunk ends mid-sentence at README:194-195 and the EXAMPLES.md chunk truncates mid-`company-brain` compile mode, so the remaining `company-brain` modes and any further skill examples are not grounded here (README:194-199, EXAMPLES.md:274-290).

## 11. How It Compares to Alternatives

- `marketingskills` (sibling repo, 46 marketing skills covering CRO, copywriting, SEO, ads): same SKILL.md-as-executable-doc and invocation-time cross-plugin referencing, but scoped to the marketing craft while `makerskills` covers the personal operator's craft (ARCHITECTURE.md:165-171).
- Anthropic `compound-engineering:*` skill-authoring set: the officially-blessed methodology `skillify` composes with rather than replaces — `skillify` adds CREATE/ADAPT/UPDATE routing, license-check porting, and cross-skill propagation with semver discipline on top (README:175-186).
- Agent Skills ecosystem (`agentskills.io`) and community plugin collections for Claude Code / Codex / Cursor: the portable spec `makerskills` targets, with the caveat that non-Claude hosts are early and Mac-default dependencies need swaps (FAQ.md:93-108).
- Karpathy LLM Wiki workflow over a markdown vault: the explicit basis for `second-brain` (capture / compile / query / lint / connect / search), extended here with a team-scope sibling (`company-brain` with sensitivity tagging, trust levels, and `/cb review`), CFO siblings, and archive-with-revisit-date discipline (README:144-148, README:163-167).

Positioning: `makerskills` is the operator-craft complement to marketing-specific and vendor-official skill sets — differentiated by documentation-first composable skills, a strict public/private data split, and structured-input-to-archived-output cadence rather than one-off prompting.

## Appendix: Selected Code Snippets

1. Plugin install and local-dev alternative (`INSTALL.md:5-19`, `README:26-38`):

```bash
/plugin marketplace add coreyhaines31/makerskills
/plugin install makerskills@makerskills
```

```bash
git clone https://github.com/coreyhaines31/makerskills ~/code/makerskills
ln -s ~/code/makerskills ~/.claude/plugins/makerskills
```

2. Env-var contract (`ARCHITECTURE.md:46-54`):

```bash
export MAKERSKILLS_CONFIG="$HOME/.config/makerskills"
```

3. Public/private boundary guard (`.gitignore:1-24`):

```gitignore
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

4. Composition map (`ARCHITECTURE.md:128-144`):

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
