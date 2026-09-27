# Technical Analysis: open-code-review

**Repository:** https://github.com/alibaba/open-code-review
**Version analyzed:** v1.3.12
**Date:** 2026-06-16

---

## 1. Overview / What Problem It Solves

Code review is a bottleneck in high-velocity engineering teams: human reviewers miss subtle bugs under time pressure, review quality degrades across large diffs, and reviewers lack the context of the full codebase when reading an isolated diff. Generic LLM integrations attempt to close this gap but produce shallow, hallucinated, or mis-located comments because they only see the diff text, not the surrounding code.

Open Code Review is a CLI tool that runs LLM-assisted code review against a git diff with repository-level context. It was battle-tested as Alibaba's internal review assistant for tens of thousands of developers before being open-sourced. The tool gives the LLM a purpose-built toolset (file read, code search, diff inspection) so it can fetch full file contents and trace cross-file dependencies rather than guessing from diff context alone.

The primary users are: individual developers running pre-commit or pre-PR review locally, and CI/CD pipelines integrating automated review on pull requests. The tool is also installable as a Claude Code plugin or Codex skill, enabling it to run as a subagent inside an AI coding assistant.

---

## 2. High-Level Architecture

```
  Git Repository
       │
       ▼
  diff/parser.go ──► model.Diff (per-file)
       │
       ▼
  Preview / FileFilter
  (rules, extensions, excludes)
       │
       ▼
  agent/agent.go  ◄──────────────────────────────┐
       │                                          │
       ▼  (per-file concurrent)                   │
  Subtask Loop                                    │
  ┌──────────────────────────┐                    │
  │  Plan Phase (optional)   │                    │
  │  Main LLM Loop           │──► tool calls ─────┤
  │    FileRead              │         FileFind    │
  │    CodeSearch            │         FileReadDiff│
  │    CodeComment           │         CodeSearch  │
  │  Review Filter           │                    │
  │  RelocationRetry         │                    │
  └──────────────────────────┘                    │
       │                                          │
       ▼                                   llm/client.go
  model.LlmComment[]            (OpenAI or Anthropic SDK)
       │
       ▼
  Output (text / JSON)
  Session logged to ~/.opencodereview/sessions/
```

**Data flow for one review run:**

1. `review_cmd.go:runReview` parses CLI flags, resolves the git repo, loads config (template, rules, LLM endpoint).
2. `diff/parser.go:ParseDiffText` runs `git diff` and parses unified diff output into `[]model.Diff`, one per changed file.
3. `agent/preview.go:Preview` evaluates each diff against file filters and exclusion rules; files that fail are tagged with an exclusion reason.
4. `agent/agent.go:Run` dispatches one goroutine per reviewable file (bounded by `--concurrency`, default 8). Each goroutine runs a subtask: optionally a plan phase (extra LLM call to analyze large changes), then a main agentic loop (LLM call → tool execution → repeat until `task_done`).
5. When the LLM calls `code_comment`, the tool resolves the comment's line location using a sliding-window diff match; if matching fails, `diff/relocation.go:ReLocateComment` makes a second LLM call to regenerate the exact code snippet.
6. A post-processing review filter pass optionally calls the LLM again to cull false positives.
7. `session/persist.go` writes all LLM requests/responses/tool calls to a JSONL audit log at `~/.opencodereview/sessions/<repo>/<session-id>.jsonl`.

Persistent state lives in `~/.opencodereview/`: `config.json` for settings, `sessions/` for JSONL logs.

---

## 3. The Code Diff

The central domain object is `model.Diff` (defined in `internal/model/diff.go`), representing one changed file's diff data. The agent's entire context is built around slices of this type.

**Key fields:**

| Field | Type | Role |
|-------|------|------|
| `OldPath` / `NewPath` | string | File paths before/after rename |
| `Hunks` | `[]Hunk` | Parsed diff hunks with line ranges |
| `NewContent` | string | Full new file content (fetched by `finalizeDiff`) |
| `IsNew` / `IsDeleted` / `IsRenamed` / `IsBinary` | bool | Change classification |
| `Insertions` / `Deletions` | int | Line change counts |

The `diff/hunk.go` type captures individual change blocks with before/after line numbers. The `diff/resolver.go` implements the sliding-window line matching used by `code_comment` to pin a comment to the exact line range in the diff.

**Exclusion kinds** (in `agent/preview.go`):

- `ExcludeByUserRule` — matched by user/project rule's exclude patterns
- `ExcludeUnsupportedExt` — extension not in `config/allowlist/supported_file_types.json`
- `ExcludeDefaultPath` — matched by `config/allowlist/default_exclude_patterns.json`
- `ExcludeDeletedFile` — deleted files are skipped
- `ExcludeBinary` — binary diff detection

---

## 4. LLM / External Service Integration

Open Code Review calls LLMs itself — it is not an MCP server. The LLM is a required external dependency.

**Interface** (`internal/llm/client.go`):

```go
type LLMClient interface {
    CompletionsWithCtx(ctx context.Context, req ChatRequest) (*ChatResponse, error)
}
```

Two concrete implementations:

| Implementation | Protocol | SDK |
|----------------|----------|-----|
| `AnthropicClient` | Anthropic Messages API | `github.com/anthropics/anthropic-sdk-go v1.47.0` |
| `OpenAIClient` | OpenAI Chat Completions | `github.com/openai/openai-go/v3 v3.39.0` |

The `NewLLMClient` factory routes to the correct implementation based on `use_anthropic` config. Both support tool/function calling. Anthropic support includes `ReasoningContent` extraction for extended thinking outputs.

**Token counting** uses `github.com/pkoukk/tiktoken-go v0.1.8`: `cl100k_base` encoding by default, `o200k_base` for o1/o3/o4 model family names. Atomic counters accumulate input/output tokens and Anthropic cache metrics across all concurrent subtasks.

**Memory compression** triggers at 60% of `MaxTokens` (async background compression, non-blocking) and 80% (synchronous, blocking). Messages are partitioned into frozen (first 2), compressed (middle), and active (recent) zones.

**Env vars for auth:**

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | Anthropic auth (recommended path) |
| `OCR_LLM_URL` | Override LLM endpoint |
| `OCR_LLM_TOKEN` | Override auth token |
| `OCR_LLM_MODEL` | Override model |
| `OCR_USE_ANTHROPIC` | Force Anthropic protocol |

---

## 5. The Review Pipeline

The main user-facing workflow, orchestrated from `cmd/opencodereview/review_cmd.go:runReview`.

**Step 1 — Configuration load** (`review_cmd.go`):
- Load template from `internal/config/template/task_template.json` via `template.LoadDefault()`
- Resolve rules: CLI `--rule` flag → `<repo>/.opencodereview/rule.json` → `~/.opencodereview/rule.json` → embedded `system_rules.json`
- Build `tool.Registry` (frozen after population; panics on post-freeze mutation)
- Resolve `LLMClient` from provider config
- Apply `--language` to template via `template.ApplyLanguage()`

**Step 2 — Diff parsing** (`internal/diff/parser.go:ParseDiffText`):
- Runs `git diff` (or `git show` for `--commit`) with `-c core.quotepath=false`
- Parses unified diff lines via regex; `diffHeaderRe` matches `diff --git a/X b/X`
- `finalizeDiff` fetches full new file content via `git show <ref>:<path>` or reads from working directory
- 2-minute context timeout prevents blocking on large repos

**Step 3 — Preview filter** (`internal/agent/preview.go:Preview`):
- Evaluates each `model.Diff` against exclusion criteria in order: binary → deleted → unsupported ext → default path exclude → user rule exclude
- Returns `DiffPreview` with included/excluded counts

**Step 4 — Concurrent subtasks** (`internal/agent/agent.go:Run`):
- Semaphore-bounded goroutine pool (size = `--concurrency`)
- Per-file subtask: optional plan phase → main tool-use loop → optional review filter
- Plan phase: triggered when diff exceeds a token threshold; makes one LLM call to analyze the change and output a structured plan used to prime the main loop
- Main loop: sends LLM request, processes tool calls from response, repeats until `task_done` or `--max-tools` exhausted
- Tool calls execute synchronously except `code_comment`, which dispatches to `CommentWorkerPool` (bounded async semaphore) to decouple comment post-processing from the main loop

**Step 5 — Comment relocation** (`internal/diff/relocation.go:ReLocateComment`):
- When sliding-window matching fails to pin a comment's `ExistingCode` to a diff hunk, calls LLM again with `{diff}` + `{existing_code}` + `{suggestion_content}` substituted into the relocation template
- Extracts a revised code snippet from the fenced code block in the response
- Retries line resolution with the new snippet

**Step 6 — Review filter** (optional, in agent loop):
- Additional LLM pass that evaluates generated comments and prunes low-confidence or incorrect ones

**Step 7 — Output** (`cmd/opencodereview/output.go`):
- `--format text`: prints comments with file/line context and progress
- `--format json`: emits `CodeReviewResult[]` + token usage metrics + warnings
- `--audience agent`: suppresses progress output, emits summary only

---

## 6. Key Files

| File | Lines | What It Does |
|------|-------|-------------|
| `internal/agent/agent.go` | ~500 | Core review orchestrator: subtask dispatch, LLM loop, tool execution, memory compression |
| `cmd/opencodereview/review_cmd.go` | ~300 | CLI review entry point; wires config, diff, agent, output |
| `internal/llm/client.go` | ~400 | `LLMClient` interface + Anthropic/OpenAI implementations + token counting |
| `internal/diff/parser.go` | ~200 | Git diff text → `[]model.Diff` parsing |
| `internal/diff/resolver.go` | ~200 | Sliding-window line matching for comment anchoring |
| `internal/diff/relocation.go` | ~150 | LLM-based comment relocation retry |
| `internal/tool/definitions.go` | ~100 | Tool constants, `Provider` interface, `Registry` with freeze lifecycle |
| `internal/config/rules/system_rules.go` | ~250 | 4-layer rule hierarchy; glob resolution via `doublestar` |
| `internal/config/template/template.go` | ~150 | Task template loading, language injection, validation |
| `internal/session/persist.go` | ~200 | JSONL audit log writer with mutex, UUID chaining |
| `internal/agent/preview.go` | ~150 | Pre-review file filter with 5 exclusion categories |
| `cmd/opencodereview/main.go` | ~100 | CLI entry, subcommand dispatch, telemetry init |
| `internal/viewer/server.go` | ~100 | WebUI HTTP server for session replay |
| `internal/viewer/hostguard.go` | ~80 | Host-header allowlist for DNS-rebinding protection |
| `internal/llm/providers.go` | ~150 | Provider registry with presets for Anthropic, OpenAI, DashScope, DeepSeek, Z-AI |

---

## 7. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `github.com/anthropics/anthropic-sdk-go` | v1.47.0 | Anthropic Messages API client |
| `github.com/openai/openai-go/v3` | v3.39.0 | OpenAI Chat Completions client |
| `github.com/pkoukk/tiktoken-go` | v0.1.8 | Token counting (cl100k_base / o200k_base) |
| `charm.land/bubbles/v2` | v2.1.0 | TUI component library (provider selection UI) |
| `charm.land/bubbletea/v2` | v2.0.7 | TUI framework (interactive config flows) |
| `charm.land/lipgloss/v2` | v2.0.3 | TUI styling |
| `github.com/bmatcuk/doublestar/v4` | v4.10.0 | Glob matching with `**` and brace expansion for rule paths |
| `go.opentelemetry.io/otel` | v1.43.0 | OpenTelemetry tracing and metrics core |
| `go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc` | v1.43.0 | OTLP trace exporter (gRPC) |
| `go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc` | v1.43.0 | OTLP metric exporter (gRPC) |
| `go.opentelemetry.io/otel/sdk` | v1.43.0 | OTel SDK |

---

## 8. CLI / Usage Surface

**Entry points** (from `package.json` + Makefile):
- `ocr` — npm wrapper script at `bin/ocr.js` → invokes native `opencodereview` binary
- `opencodereview` — Go binary, built from `cmd/opencodereview/main.go`

**Commands:**

```bash
# Review commands
ocr review                                  # review unstaged changes
ocr review --from origin/main --to HEAD     # branch diff
ocr review --commit <sha>                   # single commit
ocr review --preview                        # dry-run: show which files qualify
ocr review --format json                    # machine-readable output
ocr review --audience agent                 # suppress progress for CI use
ocr review --concurrency 16 --timeout 20    # tuning knobs
ocr review --background "JIRA-123: ..."     # inject requirement context

# Configuration
ocr config provider                         # interactive provider picker (TUI)
ocr config model                            # interactive model picker (TUI)
ocr config set llm.url <endpoint>
ocr config set llm.model <model>
ocr config set llm.auth_token <key>
ocr config set llm.use_anthropic true

# Utilities
ocr llm test                                # verify LLM connectivity
ocr rules check <file>                      # show which rule applies to a file
ocr viewer                                  # launch WebUI session viewer
ocr version                                 # print build metadata
```

**Environment variables:**

| Variable | Default | Purpose |
|----------|---------|---------|
| `OCR_LLM_URL` | — | Override LLM endpoint URL |
| `OCR_LLM_TOKEN` | — | Override auth token |
| `OCR_LLM_MODEL` | — | Override model name |
| `OCR_USE_ANTHROPIC` | false | Force Anthropic protocol |
| `ANTHROPIC_API_KEY` | — | Anthropic auth (recommended) |

**Configuration files:**

| Path | Purpose |
|------|---------|
| `~/.opencodereview/config.json` | Global user config (provider, model, language, telemetry) |
| `<repo>/.opencodereview/rule.json` | Project-level rule overrides |
| `~/.opencodereview/rule.json` | User-level rule overrides |
| `~/.opencodereview/sessions/` | JSONL session audit logs |

---

## 9. Extensibility Points

- **New LLM provider**: implement the `LLMClient` interface in `internal/llm/client.go`; register a preset in `internal/llm/providers.go`. The factory at `llm.NewLLMClient` checks `use_anthropic` and falls back to OpenAI protocol — any OpenAI-compatible endpoint works without code changes, just config.

- **New review rule**: add an entry to `internal/config/rules/system_rules.json` with a glob pattern key and a rule struct value. Rules are matched in insertion order; the first match wins. Project and user overrides in `rule.json` sit above the system defaults automatically.

- **New file extension**: add the extension to `internal/config/allowlist/supported_file_types.json`. Language-specific rule documentation goes in `internal/config/rules/rule_docs/<lang>.md`.

- **New agent tool**: implement `tool.Provider` in a new file under `internal/tool/`, register it in the tool registry before `Freeze()` in `review_cmd.go`. Declare the tool schema in `internal/config/toolsconfig/tools.json` so the LLM knows it exists.

- **Custom tools at runtime**: pass `--tools <path/to/tools.json>` to `ocr review` to inject additional tool definitions without touching source.

- **Plugin / skill integration**: the `.claude-plugin/marketplace.json` and `skills/` directories define the interface for Claude Code and Codex marketplace discovery. New plugin manifests follow the same schema.

---

## 10. Limitations and Gotchas

- **Memory thresholds are hardcoded**: The 60%/80% compression thresholds in `agent/agent.go` are constants, not configurable. On models with very large context windows (e.g., 200k tokens), the agent compresses aggressively and may lose useful context from earlier tool results.

- **Test file exclusion patterns are hardcoded**: Built-in test excludes (`*_test.go`, `*Test.java`, `*.test.js`, etc.) are embedded in `config/allowlist/default_exclude_patterns.json`. While user rules can override with `include` patterns, the embedded patterns require a code change to modify globally.

- **Relocation adds LLM cost**: Comment relocation (`diff/relocation.go`) fires an extra LLM call when line matching fails. For large diffs with many comments, this can double LLM calls silently. There is no `--no-relocate` flag.

- **Viewer host-guard is allowlist-based**: `internal/viewer/hostguard.go` maintains an explicit allowlist; DNS rebinding is blocked but adding custom hostnames requires config. Loopback is always allowed.

- **Session logs grow unbounded**: JSONL files in `~/.opencodereview/sessions/` have no rotation or TTL policy. Long-running CI pipelines accumulate large log directories.

- **Concurrent git subprocesses are separate from file concurrency**: `--concurrency` bounds per-file LLM workers; `--max-git-procs` bounds parallel git calls. These defaults (8 and 16) are not automatically tuned to machine resources.

- **No incremental/cached review**: each `ocr review` run is stateless relative to prior runs. Re-reviewing the same diff always calls the LLM again; there is no diff fingerprint cache.

---

## 11. How It Compares to Alternatives

**CodeRabbit** (coderabbit.ai): SaaS product tightly integrated with GitHub/GitLab PR workflows, automatic triggering, persistent review memory across PRs, and team-wide configuration. Open Code Review is self-hosted and CLI-first — better for orgs with data residency requirements or custom LLM endpoints, but requires manual CI integration and has no PR persistence layer.

**Amazon CodeGuru Reviewer**: AWS-managed static analysis focused on Java and Python, using ML models trained on Amazon's codebase. Coverage is narrow by language but deep for security issues (credential exposure, resource leaks). Open Code Review supports any language via LLM generalization and custom rules, but quality on non-Java/non-Go code depends entirely on the configured LLM and rule docs.

**Sourcegraph Cody (Code Reviews)**: Integrates within the Sourcegraph platform with full repo graph context (symbol graphs, cross-repo search). Open Code Review's toolset (`code_search`, `file_read`) provides similar context retrieval at diff time but without a persistent symbol index. For repos already on Sourcegraph, Cody's pre-built graph is richer; for self-contained repos, Open Code Review requires no infrastructure beyond a git clone.

**GitHub Copilot Code Review** (pull_request_review agent): Native GitHub integration, no CLI, triggered automatically on PRs, uses GitHub's hosted models. Open Code Review gives full LLM choice (any OpenAI-compatible endpoint, Anthropic, DashScope, DeepSeek) and works outside GitHub. The tradeoff is manual integration effort vs. zero-config GitHub-native experience.

**Positioning**: Open Code Review occupies the "bring-your-own-LLM, local/CI-first, deep context retrieval" niche — the right choice when LLM choice and data sovereignty matter more than SaaS convenience.

---

## Appendix: Selected Code Snippets

**Agent subtask main loop** (`internal/agent/agent.go`)

```go
// Simplified from the actual loop
for {
    resp, err := a.args.LLMClient.CompletionsWithCtx(ctx, req)
    if err != nil {
        return err
    }
    if resp.StopReason == "end_turn" || len(resp.ToolCalls) == 0 {
        break
    }
    for _, tc := range resp.ToolCalls {
        result := a.executeToolCall(ctx, tc)
        req.Messages = append(req.Messages, llm.NewToolResultMessage(tc.ID, result))
    }
}
```

**Rule resolution hierarchy** (`internal/config/rules/system_rules.go`)

```go
// Returns the first matching rule across priority layers:
// CLI override → project rule → user rule → system default
func (r *Resolver) Resolve(path string) Rule {
    for _, layer := range r.layers {
        if rule, ok := layer.Match(path); ok {
            return rule
        }
    }
    return r.defaultRule
}
```

**Comment line anchoring** (`internal/diff/resolver.go`) — sliding-window match:

```go
// Scans diff hunks for a window of lines matching existingCode.
// Returns (startLine, endLine, ok). Falls back to relocation if ok=false.
func ResolveCommentPosition(diff *model.Diff, existingCode string) (int, int, bool) {
    lines := strings.Split(existingCode, "\n")
    for _, hunk := range diff.Hunks {
        if pos, ok := windowMatch(hunk.Lines, lines); ok {
            return hunk.NewStart + pos, hunk.NewStart + pos + len(lines) - 1, true
        }
    }
    return 0, 0, false
}
```

**Session JSONL record** (`internal/session/persist.go`) — audit chain entry:

```go
type sessionRecord struct {
    Type      string    `json:"type"`       // session_start | llm_request | tool_call | ...
    UUID      string    `json:"uuid"`
    ParentUUID string   `json:"parent_uuid"`
    Timestamp time.Time `json:"timestamp"`
    Payload   any       `json:"payload"`
}
```
