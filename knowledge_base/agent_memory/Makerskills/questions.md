---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: coreyhaines31/makerskills

### Q1. What is makerskills, who is it for, and which agent hosts does it run on?

> [!tip]- Answer
> makerskills is a plugin of 21 documentation-first AI agent skills for founder/operator workflows such as decisions, research, knowledge bases, content, CFO cadence, and domain hunts. It targets founders and indie operators and runs on Claude Code, Codex, Cursor, and other Agent Skills hosts, with companion site maker-skills.com. See [[wiki/01-overview|Overview]].

### Q2. What is the structured input → structured output → archive-to-disk pattern, and how does `/decide` exemplify it?

> [!tip]- Answer
> Every skill takes structured input, produces structured output, and writes the result to disk for later revisit. `/decide` exemplifies this by triaging 6–8 questions from the 37signals framework (38 questions plus house additions like opportunity cost) and archiving the decision with a revisit date. It needs no config, which is why it is the recommended first skill to try. See [[wiki/01-overview|Overview]].

### Q3. How do the 21-row routing table and skill composition keep 21 skills from overlapping?

> [!tip]- Answer
> The routing table maps each operator intent ("I want to...") to exactly one skill, and each SKILL.md description carries trigger phrases plus disambiguation from adjacent skills. Skills then compose by calling each other by name instead of reimplementing, with central hubs `watch-video` (54 refs), `skillify` (51), `second-brain` (48), and `slide-deck` (38) absorbing the shared jobs. See [[wiki/01-overview|Overview]].

### Q4. How does the public/private two-layer split work, and what guards it?

> [!tip]- Answer
> The public layer is the git repo (skills, references, docs with no personal data) while the private layer at `~/.config/makerskills/`, located via `MAKERSKILLS_CONFIG`, holds per-skill YAML, overlays, and archives — so `git pull` never touches personal files. `.gitignore` guards the boundary by ignoring secrets, `*.local.*` overlays, and in-repo archives, with generated outputs living under the config dir or `~/Documents/`. See [[wiki/02-top-level-files|Top-level files]].

### Q5. What does "a SKILL.md file IS the skill" mean, and how does two-level semver version it?

> [!tip]- Answer
> Each skill is markdown workflow logic Claude executes at invocation time, so iterating means editing markdown with no build step, and the `description` field's precision matters most for routing. Versioning is two-level: the plugin release tag versions the collection while each skill's `metadata.version` evolves independently, with PATCH for docs/typos, MINOR for new modes or composition, and MAJOR for breaking invocation or schema changes. See [[wiki/02-top-level-files|Top-level files]].

### Q6. What is the install-and-configure sequence, and how do the `-ify` trifecta and personal/team siblings differ?

> [!tip]- Answer
> Install via `/plugin marketplace add` + `/plugin install` (or git-clone symlink), set `MAKERSKILLS_CONFIG` plus per-skill vault paths in `~/.zshenv`, copy per-skill configs under `$MAKERSKILLS_CONFIG/`, then add only the runtime deps and optional API keys for skills you use. `skillify` creates skills, `toolify` wires integrations, and `loopify` schedules recurring work; `second-brain`/`personal-cfo` are personal-scope while `company-brain`/`company-cfo` add team scope with multi-author attribution, sensitivity tagging, and review passes. See [[wiki/02-top-level-files|Top-level files]].

### Q7. A solo founder with no vault, no API keys, and one afternoon wants the most durable value from makerskills — what should they adopt first and why?

> [!tip]- Answer
> They should run `/decide` first since it needs no config or dependencies, then read one SKILL.md to internalize the documentation-first pattern, and next set up a central hub (`second-brain` vault path or `watch-video` deps) before spreading outward. This order is best because it delivers an archived decision on day one, teaches the composable workflow cheaply, and only then pays the setup cost where downstream skills reuse it most. See [[wiki/01-overview|Overview]] and [[wiki/02-top-level-files|Top-level files]].
