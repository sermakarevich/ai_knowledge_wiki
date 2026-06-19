# Technical Analysis: caveman

**Repository:** https://github.com/juliusbrussee/caveman
**Version analyzed:** 0.1.0 (package.json)
**Date:** 2026-06-18

---

## 1. Overview / What Problem It Solves

LLM coding agents are verbose by default. A single explanation of a React bug can consume 1,180 output tokens; the same answer in "caveman mode" takes 159. At $15/M output tokens (Sonnet 4), sessions that run for hours accumulate significant cost and context pressure. Claude Code in particular serializes its full conversation history into each new request, so shorter turns compound into smaller context windows and faster throughput.

`caveman` attacks this at the prompt layer. The primary user is a developer running Claude Code (or Cursor, Windsurf, Cline, Copilot, and 30+ other agents) who wants output tokens cut with no change to technical correctness. The project installs hooks that inject a compressed-communication style guide into the agent's system context at session start, then maintain it across turns via a flag file. Secondary users are the 65% of devs who never touch system prompts but will run a one-line `curl | bash` installer.

The project is MIT-licensed and maintained by Julius Brussee. It includes a benchmark harness, a memory-file compression script that calls the Anthropic API directly, and an MCP middleware proxy that compresses tool descriptions before they reach the model.

---

## 2. High-Level Architecture

```
                         Developer terminal
                               │
                     npx caveman (install)
                               │
              bin/install.js — PROVIDERS matrix (30+ agents)
                               │
               ┌───────────────┴──────────────────┐
          hooks/                               plugin CLI
     (Claude Code)                    (claude plugin install / npx-skills)
               │                                   │
 ┌─────────────▼──────────────────┐        plugins/caveman/
 │ ~/.claude/settings.json        │        (auto-synced mirror)
 │   hooks.SessionStart           │
 │   hooks.PreToolUse             │
 └─────────────┬──────────────────┘
               │  fires on each session
               ▼
      caveman-activate.js
        └── loads skills/caveman/SKILL.md
        └── injects rules into Claude context
        └── writes ~/.claude/.caveman-active flag
               │
               ▼
      caveman-mode-tracker.js  (PreToolUse hook)
        └── intercepts slash commands (/caveman, /caveman-stats …)
        └── detects natural-language triggers
        └── writes/deletes flag file
               │
               ▼
      Claude model — compressed output
               │
               ▼
      caveman-stats.js (reads JSONL transcript, derives savings)
```

**Data flow for a typical session (Claude Code):**

1. Developer opens a new session; `SessionStart` hook fires `caveman-activate.js`.
2. Script reads `SKILL.md`, resolves active mode (env var → repo `.caveman/config.json` → user config → default `'full'`), and filters the ruleset to that level.
3. Rules are injected as hook output text into Claude's context before the first user message.
4. Flag file `~/.claude/.caveman-active` is written with the current mode string.
5. `PreToolUse` hook fires `caveman-mode-tracker.js` on each subsequent turn, re-emitting the active mode reminder and intercepting `/caveman*` commands.
6. Model produces compressed output per the injected rules.
7. `/caveman-stats` invokes `caveman-stats.js`, which reads the session's JSONL transcript directly, sums `usage.output_tokens`, and estimates savings based on a stored 0.65 compression ratio.

Persistent state: `~/.claude/.caveman-active` (current mode), `~/.claude/.caveman-history.jsonl` (per-session snapshots for lifetime totals).

---

## 3. The Skill System

Skills are the central abstraction — Markdown files (`SKILL.md`) that contain rules injected into the model's context. They are not code; they are structured natural-language prompt fragments consumed by `caveman-activate.js` at session start.

**Skill files and their modes:**

| Skill | Path | Mode value | Purpose |
|-------|------|------------|---------|
| caveman | `skills/caveman/SKILL.md` | `lite`, `full`, `ultra`, `wenyan*` | Core output compression |
| caveman-compress | `skills/caveman-compress/SKILL.md` | `compress` | Memory file compression |
| caveman-stats | `skills/caveman-stats/SKILL.md` | `stats` | Token savings display |
| caveman-review | `skills/caveman-review/SKILL.md` | `review` | Terse PR feedback format |
| caveman-commit | `skills/caveman-commit/SKILL.md` | `commit` | Compressed commit messages |
| cavecrew | `skills/cavecrew/SKILL.md` | `cavecrew` | Subagent delegation format |
| caveman-help | `skills/caveman-help/SKILL.md` | `help` | Usage guide |

`caveman-activate.js` loads `SKILL.md` line-by-line and filters sections by a comment tag matching the active mode, so the `full` ruleset is never injected into a `lite` session. Each `SKILL.md` pairs with a human-facing `README.md` — the two files serve different audiences and must stay separate.

Thirteen valid mode strings are recognized (`src/hooks/caveman-config.js`): `off`, `lite`, `full`, `ultra`, `wenyan-lite`, `wenyan`, `wenyan-full`, `wenyan-ultra`, `commit`, `review`, `compress`, `cavecrew`, `stats`. `wenyan` aliases to `wenyan-full`.

**Key knobs:**
- `CAVEMAN_DEFAULT_MODE` env var (highest priority)
- `.caveman/config.json` or `.caveman.json` in any ancestor directory (repo-local)
- `$XDG_CONFIG_HOME/caveman/config.json` (user-global)
- Hardcoded fallback: `'full'`

---

## 4. LLM / External Service Integration

Most of the system — hooks, installer, mode tracking — makes no LLM calls. The model is the client, consuming injected rules as context.

Two components do call external services:

**caveman-compress** (`skills/caveman-compress/scripts/compress.py`): Calls the Anthropic API to rewrite `.md`/`.txt`/`.typ`/`.tex` files in compressed form. Prefers `ANTHROPIC_API_KEY` + Anthropic Python SDK; falls back to the `claude` CLI for desktop authentication. The file's prose is sent to the API; code blocks, YAML frontmatter, and fenced segments are extracted first and reinserted verbatim afterward to prevent model drift. Validation runs post-compression, with up to two fix cycles where the model receives the error list and original text. The CLAUDE.md explicitly warns: "Compressing ships the raw bytes to the Anthropic API — a third-party data boundary that developers on sensitive codebases cannot cross."

**caveman-shrink** MCP server (`src/mcp-servers/caveman-shrink/`): A stdio JSON-RPC proxy wrapping an upstream MCP server. Compresses `description` fields in `tools/list`, `prompts/list`, and `resources/list` responses using a regex-based algorithm (no LLM call). Tool call responses are passed through unchanged. Configured via `CAVEMAN_SHRINK_FIELDS` (comma-separated field names) and `CAVEMAN_SHRINK_DEBUG=1`.

---

## 5. The Activation Pipeline

The core user-facing workflow is: install → activate → stay active.

**Install** (`bin/install.js`):
- Reads `PROVIDERS` array containing 30+ agent entries, each with a `detect` key using one of six strategies: `command:<bin>`, `vscode-ext:<needle>`, `cursor-ext:<needle>`, `jetbrains-plugin:<needle>`, `dir:<path>`, `file:<path>`, `macapp:<name>`.
- Detects which agents are present on the machine.
- For Claude Code: writes hooks entries to `~/.claude/settings.json` via `readSettings()` / `validateHookFields()`. Downloads hook scripts from the pinned release tag, verifies SHA-256 checksums before writing.
- For plugin-native agents (Gemini, OpenClaw): runs the agent's own CLI (`claude plugin install`, `gemini extensions install`).
- For npx-skills agents: runs `npx skills add <repo> --skill '*'`.
- For opencode: copies files directly to `~/.config/opencode/` (or `$XDG_CONFIG_HOME/opencode`).

**Activate** (`src/hooks/caveman-activate.js`, fires on SessionStart):
- Resolves config hierarchy to determine the current mode.
- Loads `SKILL.md` and filters to mode-relevant sections.
- Emits rules as hook output text — this is the mechanism by which rules enter Claude's context.
- Writes `~/.claude/.caveman-active` flag.
- On first run without statusline config, suggests the settings.json snippet.

**Persist** (`src/hooks/caveman-mode-tracker.js`, fires on PreToolUse):
- Each user turn re-reads the flag file and re-emits a one-line mode reminder.
- Intercepts `/caveman*` slash commands and natural-language triggers ("activate caveman", "be brief"), updating the flag file via `safeWriteFlag()`.
- `'off'` mode triggers `fs.unlinkSync()` on the flag file.

**caveman-init** (`src/tools/caveman-init.js`, `src/rules/caveman-activate.md`):
- `npx caveman --with-init` writes auto-activation rules from `src/rules/caveman-activate.md` into the project `.mcp.json` or `.claude/settings.json`, so caveman enables itself whenever the model detects a matching trigger phrase.

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|-------------|
| `skills/caveman/SKILL.md` | ~80 | Master rule document for caveman mode (all intensity levels) |
| `src/hooks/caveman-activate.js` | ~150 | SessionStart hook: loads SKILL.md, injects rules, writes flag |
| `src/hooks/caveman-mode-tracker.js` | ~200 | PreToolUse hook: persists mode, intercepts commands |
| `src/hooks/caveman-config.js` | ~250 | Shared config resolver, security-hardened flag I/O |
| `src/hooks/caveman-stats.js` | ~180 | Reads JSONL transcript, computes token savings, formats output |
| `bin/install.js` | ~600 | Multi-agent installer: detection, file placement, checksum verification |
| `bin/lib/settings.js` | ~100 | settings.json JSONC reader/writer with validation |
| `skills/caveman-compress/scripts/compress.py` | ~300 | Anthropic API orchestrator for memory file compression |
| `skills/caveman-compress/scripts/validate.py` | ~150 | Post-compression structural validator (headings, code blocks, URLs) |
| `skills/caveman-compress/scripts/detect.py` | ~80 | Classifies files as natural language vs. code/config |
| `src/mcp-servers/caveman-shrink/index.js` | ~200 | JSON-RPC proxy that compresses MCP tool descriptions |
| `src/mcp-servers/caveman-shrink/compress.js` | ~120 | Regex-based prose compressor with protected-segment isolation |
| `src/hooks/caveman-statusline.sh` | ~50 | Shell fragment: reads flag file, outputs mode to status bar |
| `agents/cavecrew-builder.md` | ~40 | Subagent definition for surgical multi-file edits |
| `agents/cavecrew-investigator.md` | ~40 | Subagent definition for code location/definition lookup |
| `evals/llm_run.py` | ~150 | Multi-arm eval runner (baseline vs. terse vs. caveman) |
| `evals/measure.py` | ~80 | Statistical analysis of token compression results |
| `.github/workflows/sync-skill.yml` | ~60 | CI: mirrors skills/ → plugins/, rebuilds dist/caveman.skill |

---

## 7. Dependencies

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| node | `>=18` | Runtime for all hooks, installer, MCP server |
| (no npm runtime deps) | — | Core hooks use Node.js stdlib only |
| anthropic (Python) | unspecified | caveman-compress: API calls for prose rewriting |
| tiktoken (Python) | unspecified | evals/measure.py: token counting approximation |
| openai o200k_base | (via tiktoken) | Token count approximation (not exact Claude tokenization) |

The root `package.json` lists no `dependencies` — only the installer entry point. The MCP server (`src/mcp-servers/caveman-shrink/package.json`) has its own manifest with stdio JSON-RPC handling via Node stdlib. Python dependencies for `caveman-compress` are not pinned in a `requirements.txt` or `pyproject.toml` within the skills directory.

---

## 8. CLI / Usage Surface

**Entry point:** `caveman` command, defined in `package.json` as `./bin/install.js`

**Installer:**
```bash
npx caveman                 # detect agents, install for all found
npx caveman --with-init     # also write auto-activation rules
curl -fsSL https://.../install.sh | bash   # shell shim → delegates to npx
```

**In-session slash commands** (intercepted by `caveman-mode-tracker.js`):
```
/caveman [lite|full|ultra|wenyan]   # set compression mode
/caveman-commit                     # activate commit message mode
/caveman-review                     # activate PR review mode
/caveman-compress <filepath>        # compress a memory file
/caveman-stats [--share]            # display token savings
/caveman-help                       # usage guide
```

**Environment variables:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `CAVEMAN_DEFAULT_MODE` | `'full'` | Override default intensity level |
| `CLAUDE_CONFIG_DIR` | `~/.claude` | Flag file and settings location |
| `CAVEMAN_SHRINK_FIELDS` | `description` | Fields compressed by caveman-shrink MCP proxy |
| `CAVEMAN_SHRINK_DEBUG` | unset | Set to `1` for compression stats on stderr |
| `ANTHROPIC_API_KEY` | unset | Enables SDK path in caveman-compress |
| `XDG_CONFIG_HOME` | OS default | User config base dir |
| `OPENCLAW_WORKSPACE` | `~/.openclaw/workspace` | OpenClaw agent workspace |

**Configuration files:**

| Path | Purpose |
|------|---------|
| `~/.claude/settings.json` | Hook registration (SessionStart, PreToolUse entries) |
| `~/.claude/.caveman-active` | Current mode flag (64-byte max, symlink-safe) |
| `~/.claude/.caveman-history.jsonl` | Per-session token savings history |
| `.caveman/config.json` or `.caveman.json` | Repo-local mode override (walked up 64 dirs) |
| `$XDG_CONFIG_HOME/caveman/config.json` | User-global mode override |

---

## 9. Extensibility Points

- **Add a new agent:** Append an entry to the `PROVIDERS` array in `bin/install.js`. Each entry needs an `id`, a `detect` expression using one of the six strategy prefixes, and a `type` indicating how to install (`hook`, `plugin-cli`, `npx-skills`, `native-config`). Verify that the upstream [vercel-labs/skills](https://github.com/vercel-labs/skills) profile slug exists before adding.

- **Add a new compression level:** Add the mode string to `VALID_MODES` in `src/hooks/caveman-config.js`. Add a tagged section to `skills/caveman/SKILL.md` matching the new mode string so `caveman-activate.js` can filter to it. Update the mode resolution fallback table as needed.

- **Add a new skill:** Create `skills/<name>/SKILL.md` (LLM-facing rules) and `skills/<name>/README.md` (human-facing docs). Add a mode constant for it. The CI workflow (`sync-skill.yml`) will mirror it into `plugins/caveman/skills/<name>/` automatically on merge to main. Never edit `plugins/` manually.

- **Extend caveman-compress to new file types:** Edit the `COMPRESSIBLE_EXTENSIONS` set in `skills/caveman-compress/scripts/detect.py` and add any required validation rules to `validate.py`. The backup and retry logic in `compress.py` applies automatically.

- **Extend caveman-shrink to compress additional MCP fields:** Set `CAVEMAN_SHRINK_FIELDS` env var or edit `compress.js` to handle new JSON shapes. The protected-segment isolation logic in `withProtectedSegments()` handles code blocks and URLs automatically.

---

## 10. Limitations and Gotchas

- **Savings estimates, not measurements.** `caveman-stats.js` computes "estimated savings" from a single hardcoded ratio (0.65 for `'full'` mode). No other modes have stored ratios. The eval harness uses the `o200k_base` (OpenAI) tokenizer as a proxy — the script itself notes "approximate output-length reduction, not exact Claude tokens."

- **caveman-compress sends file contents to Anthropic.** The CLAUDE.md and compress.py both flag this explicitly: prose bytes are transmitted to a third-party API. Teams on sensitive codebases or with data-residency requirements cannot use this feature.

- **Skill files are not versioned by mode.** All intensity levels live in one `SKILL.md` file, filtered by comment tags at activation time. A parsing bug in `caveman-activate.js` would silently inject wrong-level rules with no visible error.

- **`plugins/` is auto-generated but present in the tree.** CI syncs `skills/` → `plugins/caveman/skills/` on every main push. Until CI runs, `plugins/` can be stale, causing confusion when reading the repo locally. CLAUDE.md warns never to edit `plugins/` directly, but there is no lint/diff guard enforcing this.

- **No Python dependency pinning for caveman-compress.** The `scripts/` directory has `__init__.py` and `__main__.py` but no `pyproject.toml` or `requirements.txt`. The `anthropic` SDK version is unspecified; a breaking SDK release would silently break the compress pipeline.

- **SHA-256 hook verification is self-referential.** The installer downloads checksums from the same release artifact it is installing. A compromised release would pass its own checksum, giving integrity checking against tampering in transit but not against a malicious release publisher.

- **Flag file size cap is a behavior-silencing mechanism.** `readFlag()` caps reads at 64 bytes to prevent exfiltration if the flag path is replaced with a symlink. Any mode string longer than 64 bytes is silently ignored, returning `null` as if no flag exists. Currently all mode strings are well under this limit, but the behavior is invisible to users.

- **`dist/caveman.skill` is gitignored.** CI rebuilds it on push; local contributors cannot run or test the built artifact without triggering the CI workflow or running the build step manually. The README does not document a local build command.

---

## 11. How It Compares to Alternatives

**Generic conciseness system prompts** ("Answer concisely." / "Be terse.") are the zero-install baseline. The eval harness explicitly measures against this as the "terse" arm — caveman claims ~65% reduction vs. ~45–55% for a generic instruction. The difference is the structured rule set (fragment grammar, article dropping, synonym substitution) rather than a vague directive. Caveman also persists across turns and survives model drift via per-turn reinforcement; a system-prompt instruction does not have a persistence mechanism.

**LLMLingua / LLMLingua-2** are token-budget compression tools that operate on the *input* side — they shorten prompts fed to the model, not the model's outputs. They require a separate LLM inference pass for compression and produce outputs opaque to the human reading them. Caveman compresses the *output* side, is human-readable, and needs no additional model call for the core mode.

**Claude Code's built-in `/compact` command** compresses conversation history on demand but does not change output style going forward. It operates on already-generated tokens. Caveman operates preemptively — it prevents verbose output from being generated in the first place. The two are complementary.

**TokenLens / Claude Code token counters** are observability tools, not reduction tools. They show you where tokens are spent but do not change output behavior. Caveman's `caveman-stats` overlaps in the monitoring dimension but primarily exists to quantify the savings of the compression layer itself.

Positioning: caveman is the only tool in this space that installs into 30+ agents via a single command, operates purely on the output side via injected rules, and requires no API key or extra model call for its core functionality. The tradeoff is that compression quality is instruction-following dependent — a model that drifts from the injected rules produces inconsistent results, and there is no programmatic enforcement beyond per-turn reminders.

---

## Appendix: Selected Code Snippets

**Mode resolution chain** (`src/hooks/caveman-config.js`, ~line 40–80)

```javascript
function resolveDefaultMode() {
  // 1. Env var takes priority
  if (process.env.CAVEMAN_DEFAULT_MODE) {
    const m = process.env.CAVEMAN_DEFAULT_MODE.trim().toLowerCase();
    if (VALID_MODES.has(m)) return m;
  }
  // 2. Walk up directories looking for .caveman/config.json
  let dir = process.cwd();
  for (let i = 0; i < 64; i++) {
    for (const name of ['.caveman/config.json', '.caveman.json']) {
      const p = path.join(dir, name);
      try {
        const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
        if (cfg.mode && VALID_MODES.has(cfg.mode)) return cfg.mode;
      } catch {}
    }
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  // 3. User config
  // ... XDG_CONFIG_HOME lookup ...
  // 4. Fallback
  return 'full';
}
```

**Protected-segment compression pattern** (`src/mcp-servers/caveman-shrink/compress.js`, ~line 20–60)

```javascript
function withProtectedSegments(text, fn) {
  const protected_ = [];
  const placeholder = (i) => `\x00CAVEMAN${i}\x00`;

  // Extract code fences, inline code, URLs, paths, technical identifiers
  const result = text
    .replace(/```[\s\S]*?```/g, (m) => { protected_.push(m); return placeholder(protected_.length - 1); })
    .replace(/`[^`]+`/g, (m) => { protected_.push(m); return placeholder(protected_.length - 1); })
    .replace(/https?:\/\/\S+/g, (m) => { protected_.push(m); return placeholder(protected_.length - 1); });

  // Apply compression to unprotected text
  const compressed = fn(result);

  // Restore protected segments
  return compressed.replace(/\x00CAVEMAN(\d+)\x00/g, (_, i) => protected_[+i]);
}
```

**YAML frontmatter surgical extraction** (`skills/caveman-compress/scripts/compress.py`, ~line 60–90)

```python
def extract_frontmatter(text):
    """Remove YAML frontmatter before compression; reinsert verbatim after.
    The compression LLM has a habit of stripping or rewriting these despite
    preserve-structure rules.
    """
    if not text.startswith('---'):
        return '', text
    end = text.find('\n---', 3)
    if end == -1:
        return '', text
    frontmatter = text[:end + 4]
    body = text[end + 4:].lstrip('\n')
    return frontmatter, body
```

**Caveman mode core rules** (`skills/caveman/SKILL.md`, representative excerpt)

```markdown
## Full Mode Rules
- Drop: articles (a, an, the), filler (just, really, basically, essentially),
  hedging (perhaps, might, could potentially), pleasantries
- Use fragments: "Run tests first." not "You should run the tests first."
- Short synonyms: use → run, implement → add, utilize → use
- Pattern: [thing] [action] [reason]. [next step].
- All technical substance stay. Only fluff die.
- NEVER invent abbreviations. Keep code, API names, error strings verbatim.
- Auto-disable for: security warnings, irreversible action confirmations.
```
