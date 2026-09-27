---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: itechmeat/open-second-brain

### Q1. What is Open Second Brain in one sentence, and where does it store its data?
> [!tip]- Answer
> Open Second Brain is an Obsidian-native memory layer for Hermes Agent that stores preferences, signals, evidence, and audit trails as plain Markdown under `Brain/` in the vault you already use. There is no daemon, no vector black box, and no hidden state outside the vault. See [[wiki/01-overview|Overview]].

### Q2. How does an agent read and write the second-brain vault, and what can the user do with the files by hand?
> [!tip]- Answer
> The agent reaches the vault only through deterministic CLI / MCP tools exposed as a Hermes memory layer. Because the records are real `.md` files, the user can grep them, version them with git, search them in Obsidian, and edit them by hand. See [[wiki/01-overview|Overview]].

### Q3. What provenance and reversibility guarantees did releases 1.55.0/1.54.0 and 1.43.0 add?
> [!tip]- Answer
> Every note write became an attributable, revertible event with a write record, before-image store, digest-sealed planned revert, fleet-freeze guard, and per-shard hash chain, while `visibility:` turned from a label into a boundary enforced at the three roots. Earlier, 1.43.0 quarantined agent-extracted entities from untrusted sources, gated caller-named writes by `_brain.yaml` path prefixes, and kept kernel on-disk evidence beside agent outcome claims. See [[wiki/01-overview|Overview]].

### Q4. How do the root `__init__.py` and `cli.py` expose the plugin to Hermes?
> [!tip]- Answer
> Root `__init__.py` re-exports `OpenSecondBrainMemoryProvider`, `check_health`, `health`, `register`, and `register_cli` from `.plugins.hermes`, since the Hermes gateway loads the repo root first. Root `cli.py` is a lightweight CLI-discovery shim re-exporting `register_cli` and `run` from `.plugins.hermes.cli` without executing root `__init__.py`. See [[wiki/02-top-level-files|Top-level-files]].

### Q5. What do `.mcp.json`, `plugin.yaml`, and `openclaw.plugin.json` each declare?
> [!tip]- Answer
> `.mcp.json` declares two stdio servers, `open-second-brain` (`o2b mcp`) and the always-loaded `open-second-brain-writer` (`o2b mcp --scope writer`). `plugin.yaml` declares `memory_provider: true` with seven lifecycle hooks from `system_prompt_block` to `shutdown`. `openclaw.plugin.json` declares plugin id `open-second-brain` v`1.58.2` with five contracted tools and a config schema of `vault`, `instanceName`, `agentName`, `timezone`, and `mcpEnabled`. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What are the versioning rule, the install/verify flow, and the shared hygiene defaults?
> [!tip]- Answer
> `package.json` `version` is the single source of truth propagated by `bun run scripts/sync-version.ts`, with Codex mirrors regenerated via `bun run sync-plugin-mirrors`. Installs route through `o2b install --target <name> --apply` per runtime, verified by `o2b init`, `o2b doctor`, and `o2b install --check` exit codes `0`/`3`/`5`. Hygiene pins LF checkouts with CRLF batch launchers, `printWidth: 100`, an oxlint `correctness:error` gate, strict `ES2022`/bundler TS config, and a hermetic Bun test preload. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. (Evaluation) Would you recommend Open Second Brain as a team's agent memory layer, and what should you check first?
> [!tip]- Answer
> Recommend it when the team already lives in Obsidian and wants ownable, auditable Markdown memory with attributable, revertible writes and enforced visibility boundaries rather than a black-box vector store. Before adopting, verify the `o2b install` path for your runtime, the `vault.include_paths` scoping, and the quarantine and `visibility:` enforcement fit your trust model. See [[wiki/01-overview|Overview]].
