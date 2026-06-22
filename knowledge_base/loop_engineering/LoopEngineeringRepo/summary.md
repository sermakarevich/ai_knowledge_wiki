# Technical Analysis: loop-engineering

**Repository:** https://github.com/cobusgreyling/loop-engineering
**Version analyzed:** tools at loop-audit@1.4.1 / loop-init@1.2.1 / loop-cost@1.0.2 (repo has no single root version)
**Date:** 2026-06-22

---

## 1. Overview / What Problem It Solves

AI coding agents -- Grok, Claude Code, Codex, Cursor, Windsurf -- are today typically driven turn-by-turn by a human who manually crafts each prompt. This model caps throughput at the human's attention. The loop-engineering repository addresses the next step: replacing the human prompter with a system that discovers work, delegates it to agents, verifies results, and persists state -- continuously and on a schedule.

The repo serves two audiences simultaneously. For individual engineers it is a pattern library and quick-start scaffold: clone a starter, audit readiness, and run a report-only loop by day one. For teams it is an opinionated reference architecture that codifies what "production-ready autonomous loops" requires in terms of safety gates, state management, verification splits, and observability.

Primary users are developers already running AI coding agents who want to graduate from one-off sessions to scheduled, durable, self-maintaining automation pipelines.

---

## 2. High-Level Architecture

```
  Human Engineer
        |  defines patterns, skills, safety gates
        v
  loop-engineering repo
  +-----------------------------------------------------+
  |  patterns/         docs/           starters/        |
  |  (7 YAML/MD)       (15 MD files)   (9 tool kits)   |
  |       |                                 |           |
  |       v                                 v           |
  |  registry.yaml     primitives.md    minimal-loop/   |
  |  (machine index)   concepts.md      pr-babysitter/  |
  |       |            safety.md        ci-sweeper/...  |
  |       v                                 |           |
  |  tools/                                 |           |
  |  +-- loop-audit   (TS -> npm)           |           |
  |  +-- loop-init    (TS -> npm)  <--------+           |
  |  +-- loop-cost    (TS -> npm)                       |
  |       |                                             |
  +-------+---------------------------------------------+
          |  npx / local build
          v
  Developer's project repo
  +-- STATE.md          <- loop state spine
  +-- skills/           <- triage, fix, verifier SKILLs
  +-- .github/          <- Actions-based scheduling
  +-- loop-budget.md    <- token cap config
```

Data flow for a new project adopting the Daily Triage pattern:

1. Developer runs `npx @cobusgreyling/loop-init . --pattern daily-triage --tool claude-code`, which copies starter files from `starters/minimal-loop-claude/` into the project.
2. `npx @cobusgreyling/loop-cost --pattern daily-triage` reads `patterns/registry.yaml` and outputs estimated daily token spend.
3. `npx @cobusgreyling/loop-audit . --suggest` scores the project (L0--L3) and lists missing artifacts.
4. The agent runtime (Claude Code, Grok, etc.) runs on a schedule; it reads `STATE.md`, invokes the `loop-triage` skill, and appends findings.
5. A verifier sub-agent (separate model/instructions) checks the implementer's output before any changes are staged.
6. Output is written back to `STATE.md`; human reviews the "High Priority (waiting on human)" section.

Persistent state lives in `STATE.md` at the project root (or pattern-specific files like `pr-babysitter-state.md`). There is no database -- all state is markdown on disk, readable and writable by both agents and humans.

---

## 3. The Loop Pattern Registry

The central domain abstraction is the **pattern** -- a machine-readable and human-readable specification of one repeating engineering loop. Each pattern defines a stable identity that tools and starters reference.

`patterns/registry.yaml` is the single authoritative index. Every pattern entry contains:

- `id`, `name`, `file` -- identity and documentation link
- `goal` -- one-line plain-English objective
- `cadence` -- scheduling interval range (e.g. `5m-15m`, `1d-2h`)
- `risk` -- `low` / `medium`
- `tools` -- which agent environments support this pattern
- `skills` -- array of required skill module names
- `state` -- the expected state file name in the consumer project
- `phases` -- ordered execution phases (e.g. `[discover, triage, fix, verify, notify]`)
- `human_gates` -- conditions that must escalate to a human (e.g. `security`, `max-fix-attempts`)
- `starter` -- pointer to the matching starter kit in `starters/`
- `week_one_mode` -- recommended initial level (`L1` or `L2`)
- `token_cost` -- qualitative estimate (`low` / `medium` / `high` / `very-high`)
- `cost` -- quantitative token estimates: `tokens_noop`, `tokens_report`, `tokens_action`, `suggested_daily_cap`, `early_exit_required`

Example entry (pr-babysitter):

```yaml
- id: pr-babysitter
  cadence: 5m-15m
  risk: medium
  phases: [discover, triage, fix, verify, notify]
  human_gates: [security, payments, auth, max-fix-attempts]
  cost:
    tokens_noop: 3000
    tokens_action: 250000
    suggested_daily_cap: 2000000
    early_exit_required: true
```

The schema is validated by `scripts/validate-registry.mjs` against `patterns/registry.schema.json`, enforced in CI via the `validate:registry` npm script.

---

## 4. LLM / External Service Integration

This repo does **not** call LLMs directly. It is pure scaffolding and tooling. The repo's intended position in the stack:

```
  This repo (patterns + starters + CLI tools)
        |  provides skills, state templates, audit scoring
        v
  Agent runtime (Claude Code / Grok / Codex / Cursor / Windsurf)
        |  calls LLMs, reads STATE.md, runs skills
        v
  LLM API (Anthropic, OpenAI, xAI, etc.)
```

The three npm CLI tools (`loop-audit`, `loop-init`, `loop-cost`) are pure Node.js utilities: filesystem reads, YAML parsing, score computation, and console output. They have no LLM dependencies.

MCP (Model Context Protocol) connectors are referenced in documentation and example directories (`examples/mcp/`) as the integration pattern for reaching GitHub, Linear, Slack, or databases from within the agent runtime. The repo provides recipes and scope recommendations but does not implement MCP servers.

Environment variables: none required to run the CLI tools. Individual project starters inherit their env requirements from the target agent runtime.

---

## 5. The Loop Readiness Assessment Pipeline

The `loop-audit` tool implements the primary user-facing analytical workflow: given a project directory, score its readiness to run production loops.

**Phase 1 -- Filesystem scan (`auditor.ts`):**
Scans the target directory for presence and content of loop artifacts:
- `STATE.md` -- loop state spine (required for L1+)
- `LOOP.md` -- self-describing loop documentation
- `AGENTS.md` -- agent instructions file
- `safety.md` -- safety policy document
- `loop-budget.md` -- token cap configuration
- `loop-run-log.md` -- historical run record
- Skill directories matching known skill names (`loop-triage`, `minimal-fix`, `loop-verifier`)
- Worktree usage evidence (git config, isolation flags in skills)
- Activity signals (recent commits, updated STATE.md timestamps)

**Phase 2 -- Scoring (`auditor.ts`):**
Assigns weighted points per artifact and sums to a 0--100 Loop Readiness Score. Maps score to maturity level:
- L0 (0--24): Draft -- document intent
- L1 (25--49): Report-only -- safe to run, report only
- L2 (50--74): Assisted -- loop can suggest fixes, human reviews
- L3 (75--100): Unattended-capable with human gates

**Phase 3 -- Suggestion generation (`auditor.ts`, `reporter.ts`):**
For each missing artifact, generates a copy-paste command or file-creation snippet.

**Phase 4 -- Output formatting (`reporter.ts`, `cli.ts`):**
Renders results in human-readable terminal output, `--json` for machine consumption, or `--markdown` for CI comments. The `cli.ts` entry point parses arguments (`--suggest`, `--json`, `--markdown`, `--verbose`) and routes to reporter.

Entry point: `tools/loop-audit/dist/cli.js` (compiled from `tools/loop-audit/src/cli.ts`).
Source files: `tools/loop-audit/src/auditor.ts`, `tools/loop-audit/src/cli.ts`, `tools/loop-audit/src/reporter.ts`.

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|-------------|
| `README.md` | ~120 | Primary entry point; quick-start, primitives table, patterns table, caveats |
| `LOOP.md` | ~80 | Self-describing operational doc; lists which loops run on this repo itself |
| `patterns/registry.yaml` | ~120 | Machine-readable index of all 7 patterns with cost and phase data |
| `patterns/registry.schema.json` | ~40 | JSON Schema validating registry.yaml entries |
| `docs/primitives.md` | ~90 | Detailed explanation of all 6 loop primitives |
| `docs/primitives-matrix.md` | ~130 | Cross-tool mapping table: Grok, Claude Code, Codex, Cursor, Windsurf |
| `docs/concepts.md` | ~80 | Vocabulary: intent debt, comprehension debt, cognitive surrender, harness vs loop |
| `docs/safety.md` | ~60 | Protected paths, merge controls, access limits, human gate requirements |
| `docs/anti-patterns.md` | ~80 | 10 design mistakes with mitigations |
| `docs/failure-modes.md` | ~140 | Incident-style catalog of 11 failure modes with severity classifications |
| `patterns/daily-triage.md` | ~50 | Full spec for daily triage loop pattern |
| `patterns/pr-babysitter.md` | ~50 | Full spec for PR monitoring pattern |
| `tools/loop-audit/src/auditor.ts` | ~200 | Scoring logic, artifact detection, suggestion generation |
| `tools/loop-audit/src/cli.ts` | ~60 | CLI argument parsing, entry point |
| `tools/loop-audit/src/reporter.ts` | ~80 | Output formatting (terminal, JSON, markdown) |
| `tools/loop-init/src/index.ts` | ~200 | Scaffolding logic; copies starters, validates inputs |
| `tools/loop-cost/src/index.ts` | ~100 | Token estimation from registry.yaml data |
| `starters/minimal-loop/` | ~30/file | Grok-flavored daily triage starter (STATE.md + triage skill) |
| `starters/minimal-loop-claude/` | ~30/file | Claude Code variant of minimal loop |
| `starters/pr-babysitter/` | ~50/file | PR Babysitter starter with verifier skill |
| `package.json` | 20 | Root monorepo manifest; no runtime deps; dev: ajv, yaml |

---

## 7. Dependencies

### Root monorepo (`package.json`)

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `ajv` | `^8.17.1` | JSON Schema validation for `scripts/validate-registry.mjs` |
| `yaml` | `^2.8.0` | YAML parsing for pattern registry validation scripts |

### `tools/loop-audit`

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `typescript` | `^5.0.0` | Compile TS to JS; dev only |
| `@types/node` | `^25.9.3` | Node.js type definitions; dev only |

No runtime npm dependencies -- loop-audit is stdlib + built-in Node.js modules only.

### `tools/loop-cost`

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `yaml` | `^2.8.0` | Read `patterns/registry.yaml` for token estimates |
| `typescript` | `^5.0.0` | Dev only |

### `tools/loop-init`

| Package | Version constraint | Purpose |
|---------|-------------------|---------|
| `typescript` | `^5.0.0` | Dev only |

Runtime deps: stdlib only (file copying, path resolution).

---

## 8. CLI / Usage Surface

### Entry points (from `bin` fields in each tool's `package.json`)

| Binary | Compiled source | npm package |
|--------|----------------|-------------|
| `loop-audit` | `tools/loop-audit/dist/cli.js` | `@cobusgreyling/loop-audit@1.4.1` |
| `loop-init` | `tools/loop-init/dist/` | `@cobusgreyling/loop-init@1.2.1` |
| `loop-cost` | `tools/loop-cost/dist/` | `@cobusgreyling/loop-cost@1.0.2` |

### Commands

```bash
# Score a project's loop readiness (L0-L3)
npx @cobusgreyling/loop-audit .
npx @cobusgreyling/loop-audit . --suggest     # copy-paste fix commands
npx @cobusgreyling/loop-audit . --json        # machine-readable JSON
npx @cobusgreyling/loop-audit . --markdown    # for CI PR comments
npx @cobusgreyling/loop-audit . --verbose     # per-signal breakdown

# Scaffold a starter into the current project
npx @cobusgreyling/loop-init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop-init . --pattern pr-babysitter --tool claude-code
npx @cobusgreyling/loop-init . --pattern ci-sweeper --tool codex

# Estimate token spend for a pattern
npx @cobusgreyling/loop-cost --pattern daily-triage
npx @cobusgreyling/loop-cost --pattern pr-babysitter --level L2

# Root monorepo scripts
npm run validate:registry   # validate patterns/registry.yaml
npm run build:tools         # build all three CLI tools
npm run test:tools          # run all tool test suites
bash scripts/before-after-demo.sh
```

### Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| None required | -- | All CLI tools run without env vars; token estimates read from registry.yaml |

### Configuration files

| Path | Purpose |
|------|---------|
| `patterns/registry.yaml` | Pattern definitions consumed by loop-cost and loop-audit |
| `patterns/registry.schema.json` | Validation schema for registry.yaml |
| `starters/*/` | Template directories copied by loop-init into target projects |
| `STATE.md` (target project) | Loop state spine; read and written by the agent runtime |
| `loop-budget.md` (target project) | Token cap configuration (created by loop-init) |

---

## 9. Extensibility Points

- **Adding a new loop pattern:** Create `patterns/<id>.md` and add an entry to `patterns/registry.yaml` following the schema. Immediately available to `loop-cost` and `loop-audit`. Add a matching starter in `starters/<id>/`.

- **Adding a new starter kit:** Create a directory under `starters/` with at minimum `STATE.md.example` and required skill SKILL.md files. Reference it from the pattern's `starter` field in `registry.yaml`. The `loop-init` tool copies this directory wholesale.

- **Adding a new skill module:** Create `skills/<skill-name>/SKILL.md` following the templates (`loop-triage`, `minimal-fix`, `loop-verifier`, `loop-budget`). Skills are tool-agnostic -- the same SKILL.md works in Grok, Claude Code, and Codex.

- **Supporting a new agent tool:** Add a column to `docs/primitives-matrix.md`. Update the `tools` array on relevant pattern entries in `registry.yaml`. Create tool-specific starters under `starters/<pattern>-<toolname>/`.

- **Extending loop-audit scoring:** Add detection logic in `tools/loop-audit/src/auditor.ts` for new artifacts. Add suggestion generation and update the scoring table. Output format is extensible through `reporter.ts`.

- **Adding an MCP connector recipe:** Add a directory under `examples/mcp/` with a README and configuration snippet. Documentation-only; no code changes to CLI tools needed.

---

## 10. Limitations and Gotchas

- **No runtime enforcement of safety gates.** The `safety.md` denylist and human gate requirements are documentation and convention only -- the repo cannot enforce them in the agent runtime. A misconfigured loop will override them without any error from this tooling.

- **State file is unstructured markdown.** Multiple loops appending to a single `STATE.md` without a schema can corrupt state. The repo warns against this in `docs/anti-patterns.md` and recommends pattern-specific state files, but provides no parsing library or schema enforcement.

- **loop-audit scoring is heuristic and file-name-dependent.** The L0--L3 scoring detects named files and patterns by convention. A project using non-standard naming (e.g. `loop_state.md` instead of `STATE.md`) scores lower than its actual readiness, with no way to configure expected filenames.

- **No GitHub Actions scaffolding in loop-init.** Despite the repo hosting its own Actions workflows, `loop-init` does not generate `.github/workflows/*.yml` files -- these must be written manually or sourced from `examples/github-actions/`.

- **Minimal monorepo tooling.** The root `package.json` has no workspaces config and no cross-tool dependency management. Building each tool requires entering its subdirectory; `npm run build:tools` chains them but does not parallelize.

- **Starter kits are not integration-tested.** The `test:tools` suite covers CLI logic but not whether scaffolded starter files produce valid loop behavior in a real agent runtime.

- **No versioning of pattern files.** `registry.yaml` has no `version` or `since` field per pattern, making it impossible to detect breaking changes when upgrading `loop-init` after initial scaffolding.

- **Token cost estimates are static.** The `loop-cost` tool reads fixed ranges from `registry.yaml`. Actual costs vary by model, context length, and whether sub-agents fire -- estimates can be off by an order of magnitude for atypical workloads.

---

## 11. How It Compares to Alternatives

**GitHub Actions + custom YAML workflows** is the incumbent alternative for scheduled automation. Actions offers mature scheduling, secrets management, and native GitHub API access, but requires writing imperative shell/YAML rather than declarative agent instructions. loop-engineering is designed as a layer on top of Actions (it references Actions for scheduling) rather than a replacement -- but for teams already fluent in Actions, the added abstraction layer may feel redundant.

**AutoGPT / AgentGPT / open-source agent frameworks** focus on autonomous task execution but treat the "loop" as an internal model concern rather than an engineering discipline. They provide no pattern library, no safety gate conventions, and no readiness scoring. loop-engineering's value is the institutional knowledge encoded in `patterns/`, `docs/`, and `skills/` -- not a novel execution engine.

**LangGraph / CrewAI / similar multi-agent orchestration frameworks** operate at the agent graph layer: they wire LLM calls, tools, and conditional edges in code. loop-engineering sits a level above, orchestrating full agent runtime sessions (not individual LLM calls) and treating the agent's entire session as the unit of work. There is no implementation overlap -- a LangGraph pipeline could be invoked from inside a loop-engineering loop.

**Sweep.dev / Devin / autonomous coding agents as a product** handle the full vertical as SaaS. loop-engineering targets teams that want to own the automation layer inside their existing agent tool, not outsource it. The tradeoff is setup overhead vs. vendor lock-in.

loop-engineering's positioning: a vendor-agnostic, copy-and-own scaffold for teams graduating from manual AI prompting to scheduled autonomous loops, emphasizing pattern reuse, safety conventions, and incremental autonomy levels over novel automation technology.

---

## Appendix: Selected Code Snippets

**Pattern definition with token cost data (`patterns/registry.yaml`)**

```yaml
- id: pr-babysitter
  name: PR Babysitter
  goal: Shepherd PRs through review, CI, rebase, and merge
  cadence: 5m-15m
  risk: medium
  phases: [discover, triage, fix, verify, notify]
  human_gates: [security, payments, auth, max-fix-attempts]
  cost:
    tokens_noop: 3000
    tokens_report: 80000
    tokens_action: 250000
    suggested_daily_cap: 2000000
    early_exit_required: true
```

**Cross-tool primitive mapping excerpt (`docs/primitives-matrix.md`)**

```markdown
| Primitive        | Grok                          | Claude Code                        | Codex                     |
|------------------|-------------------------------|-------------------------------------|---------------------------|
| Automations      | /loop [interval] <prompt>     | /loop, scheduled tasks, cron, hooks | Automations tab, cadence  |
| Worktrees        | isolation: "worktree"         | git worktree, --worktree            | Built-in per thread       |
| Skills           | SKILL.md in .grok/skills/     | SKILL.md in .claude/skills/         | $name or implicit match   |
| Sub-agents       | Task tool, subagent_type      | .claude/agents/, agent teams        | TOML in .codex/agents/    |
```

**Failure mode with severity and mitigations (`docs/failure-modes.md`)**

```markdown
## Infinite Fix Loop
Severity: S2 -- Wrong code merged, bad tickets, alert fatigue
Mitigations:
- Hard cap on attempts (e.g. 3) -> escalate to human
- Separate verifier model / higher reasoning effort
- Classify flakes in triage; quarantine instead of code change
- Record attempt count in state file
```

**Getting started sequence (`README.md`)**

```bash
npx @cobusgreyling/loop-init . --pattern daily-triage --tool grok
npx @cobusgreyling/loop-cost --pattern daily-triage
npx @cobusgreyling/loop-audit . --suggest
# then in agent runtime:
/loop 1d Run loop-triage. Update STATE.md. No auto-fix in week one.
```
