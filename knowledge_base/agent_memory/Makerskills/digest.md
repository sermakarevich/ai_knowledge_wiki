> [[index|Wiki]] | [[summary|Summary]]
# coreyhaines31/makerskills — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** makerskills is a plugin of 21 documentation-first AI agent skills for founder/operator workflows (decisions, research, knowledge bases, content, CFO, domains) that run on Claude Code, Codex, Cursor, and other Agent Skills hosts.
## Key points
- The repo's job is "AI agent skills for the personal operator's craft" covering decisions, research, second-brain workflows, content rotation, scenario modeling, CFO cadence, domain hunts, and meta-skills for authoring more skills (README:11).
- It targets founders and indie operators and works with Claude Code, Codex, Cursor, and other Agent Skills hosts, with site maker-skills.com (README:13, README:15).
- Installation is via `/plugin marketplace add coreyhaines31/makerskills` + `/plugin install makerskills@makerskills`, or a symlink for local dev (`git clone ... ~/code/makerskills` + `ln -s ... ~/.claude/plugins/makerskills`), with env/personal-config details deferred to INSTALL.md (README:26-38).
- The first-touch pattern is structured input → structured output → written to disk, exemplified by `/decide` picking questions from the 37signals framework and archiving with a revisit date (README:56-62).
- Each skill is a workflow doc invocable as `/decide` or by reading `skills/decide/SKILL.md` and running steps by hand; "the plugin is documentation-first; the automation is a side effect" (README:64-70).
- A 21-row routing table maps operator intents ("I want to...") to skills, and each skill's SKILL.md description carries trigger phrases plus disambiguation from adjacent skills (README:88-114).
- Skills compose by calling each other by name instead of reimplementing, with central hubs `watch-video` (54 refs), `skillify` (51), `second-brain` (48), `slide-deck` (38), `company-brain` (33), `domain` (32) (README:173-186).
- The repo is "public + generic" with personal data kept out of the repo — but the Architecture section is truncated mid-sentence in this chunk so the full separation mechanism is not visible here (README:194-199).
## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** The repo root defines a public generic plugin layer plus a private on-disk config layer, with architecture, install, FAQ, examples, and backlog docs describing how the 20 skills install, configure, compose, and version.
## Key points
- The plugin is split into a public git repo (skills, references, docs; no personal data) and a private layer at `~/.config/makerskills/` located via `MAKERSKILLS_CONFIG`, so `git pull` never touches personal files (ARCHITECTURE.md:5-18, ARCHITECTURE.md:41-44).
- The 20 skills group into 6 families (meta `-ify` trifecta, decision & strategy, knowledge & content consumption, output & creative, operations & utilities, plus cross-family patterns), with the `-ify` family fixed at three members by the Rule of 3 (ARCHITECTURE.md:62-114).
- A `SKILL.md` file IS the skill — markdown workflow logic Claude executes at invocation time, so iterating means editing markdown with no build step (ARCHITECTURE.md:150-161).
- Skills compose by name with central hubs (`watch-video` 54 refs, `second-brain` 48, `skillify` 51, `slide-deck` 38), so adopters should set up central skills first (`watch-video` needs yt-dlp + ffmpeg + MLX-Whisper; `second-brain` needs a vault path) (ARCHITECTURE.md:128-146).
- Versioning is two-level semver: plugin release tag plus independent per-skill `metadata.version`, with PATCH/MINOR/MAJOR rules for each level (ARCHITECTURE.md:180-199).
- Install is plugin install (`/plugin marketplace add` + `/plugin install`, or git-clone symlink), env vars in `~/.zshenv`, personal configs under `$MAKERSKILLS_CONFIG/`, per-skill runtime deps, and optional API keys with free fallbacks (INSTALL.md:5-19, INSTALL.md:23-43, INSTALL.md:61-83, INSTALL.md:84-101).
- `.gitignore` guards the public/private boundary by ignoring secrets, overlays, and in-repo archives (`*.local.md`, `skills/*/references/*archive*/`, `skills/*/references/decks-archive.md`), while `FAQ.md`, `EXAMPLES.md`, and `BACKLOG.md` cover onboarding/debugging, one worked example per skill, and the shipped-vs-candidate roadmap (`.gitignore:6-24`, `FAQ.md:7-24`, `BACKLOG.md:7-15`).
## The system in five moves
1. Start with a documentation-first plugin of operator skills installed via marketplace or symlink, where each SKILL.md is executable workflow logic with no build step.
2. Route operator intent ("I want to...") to the right skill via the 21-row table and description trigger phrases, beginning with `/decide` since it needs no config.
3. Execute the structured input → structured output → archive-to-disk pattern across decision, knowledge, creative, and operations skill families.
4. Compose skills by name through central hubs (`watch-video`, `second-brain`, `skillify`, `slide-deck`) instead of reimplementing adjacent jobs.
5. Keep the repo public and generic behind `.gitignore` guards while personal configs, vaults, and archives live in the private `$MAKERSKILLS_CONFIG` layer, versioned by two-level semver and extended via the `-ify` meta-skills.
