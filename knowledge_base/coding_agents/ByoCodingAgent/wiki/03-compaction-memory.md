> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Compaction strategies and session memory

**In one sentence:** Short-term context is truncated per-turn by a `CompactionStrategy` snapped to tool-pair-safe boundaries, while long-term context persists across sessions through a `memory.Store` whose default file-backed implementation writes one markdown file per session plus a JSON index.

## Key points

- Every strategy implements `Compact(ctx, messages)` and is invoked at the top of each agent-loop turn, returning input unchanged below its threshold (`internal/compact/strategy.go:14`).
- `SafeSplitPoint` walks backward from the desired index to the nearest plain-text user message, returning 0 ("do nothing") when no safe boundary exists so a `tool_use` is never split from its `tool_result` (`internal/compact/strategy.go:23`).
- `SlidingWindow{KeepLast}` keeps only the newest N messages and `Summarize{Threshold, KeepRecent}` replaces the dropped prefix with a single synthetic `[earlier conversation summary]` user message produced by one provider call (`internal/compact/slidingwindow.go:12`, `internal/compact/summarize.go:14`).
- `LoggingStrategy{Inner, FilePath}` wraps any strategy and appends a before/after transcript only when the message count changed, via `WithLogging(inner, path)` (`internal/compact/logging.go:15`, `internal/compact/logging.go:21`).
- `memory.Store` is a three-method interface — `Save`, `Recall`, `Preamble` — with a package-level `Default` that falls back to no-op `NoMemory` (`internal/memory/store.go:40`, `internal/memory/store.go:49`).
- `SessionFiles` is the default `Store`: `<root>/sessions/*.md` per session plus `<root>/index.json` as the lookup layer, with missing files pruned silently at open (`internal/memory/sessionfiles.go:24`, `internal/memory/sessionfiles.go:45`).
- `Save` only buffers into an in-memory draft (flushed by `Close`), `Recall` is a case-insensitive substring scan over summary/tags ordered most-recent-first, and `Preamble` injects at most the last 5 session summaries into the system prompt (`internal/memory/sessionfiles.go:100`, `internal/memory/sessionfiles.go:114`, `internal/memory/sessionfiles.go:162`).

---

## Compaction interface and invocation contract

All strategies live in `internal/compact/strategy.go:14` and share one interface:

```go
type CompactionStrategy interface {
	Compact(ctx context.Context, messages []api.Message) ([]api.Message, error)
}
```

Per the package doc (`internal/compact/strategy.go:1`), strategies run at the top of every agent loop turn; thresholded ones return the input unchanged when the threshold is not reached.

## SafeSplitPoint — the shared safety invariant

```go
func SafeSplitPoint(messages []api.Message, desired int) int
```

`internal/compact/strategy.go:23` walks backward from `desired` to find an index where the conversation is in a clean state: a `RoleUser` message with no tool result (`internal/compact/strategy.go:31`). Edge rules (`internal/compact/strategy.go:24`, `internal/compact/strategy.go:27`): `desired <= 0` returns 0; `desired >= len(messages)` returns `len(messages)`; no clean boundary returns 0, meaning "do nothing" rather than orphaning a `tool_use`.

## NoCompaction — the default passthrough

```go
type NoCompaction struct{}
func (NoCompaction) Compact(_ context.Context, messages []api.Message) ([]api.Message, error)
```

`internal/compact/nocompaction.go:10` never modifies messages; it is the default strategy.

## SlidingWindow — drop the prefix

```go
type SlidingWindow struct {
	KeepLast int
}
func (s *SlidingWindow) Compact(_ context.Context, messages []api.Message) ([]api.Message, error)
```

`internal/compact/slidingwindow.go:12` keeps the last `KeepLast` messages and drops everything older. Short history (`len(messages) <= s.KeepLast`) is a no-op (`internal/compact/slidingwindow.go:17`); otherwise it computes `SafeSplitPoint(messages, len(messages)-s.KeepLast)` and returns `messages[split:]` (`internal/compact/slidingwindow.go:20`), so the cut snaps to a safe boundary and never separates `tool_use` from `tool_result`.

## Summarize — LLM-compressed prefix

```go
type Summarize struct {
	Provider     provider.Provider
	Threshold    int    // compact once len(messages) >= Threshold
	KeepRecent   int    // most-recent N messages left untouched
	Instructions string // optional override for the summarization prompt
}
```

`internal/compact/summarize.go:14` compacts once `len(messages) >= Threshold` (`internal/compact/summarize.go:26`), splits at `SafeSplitPoint(messages, len(messages)-s.KeepRecent)` (`internal/compact/summarize.go:29`), and bails out unchanged when the split is 0 (`internal/compact/summarize.go:30`). The dropped prefix is rendered via `api.RenderTranscript(old)` and sent as a single user message with either the custom `Instructions` or the default prompt (`internal/compact/summarize.go:35`):

```go
const defaultSummarizeInstructions = `Summarize the following conversation concisely. ` +
	`Preserve facts, decisions, file paths, code identifiers, and anything else ` +
	`needed to continue the conversation. Output the summary directly with no preamble.`
```

`internal/compact/summarize.go:21` holds that default. The provider response's first text block becomes the summary; an empty response is an error (`internal/compact/summarize.go:56`). On success it prints `[compacted N messages → summary]` and prepends one synthetic message (`internal/compact/summarize.go:60`):

```go
Role:    api.RoleUser,
Content: []api.Block{{Type: api.BlockText, Text: "[earlier conversation summary]\n" + summary}},
```

followed by the untouched `recent` tail (`internal/compact/summarize.go:61`).

## LoggingStrategy — observable compaction

```go
type LoggingStrategy struct {
	Inner    CompactionStrategy
	FilePath string
}
func WithLogging(inner CompactionStrategy, path string) *LoggingStrategy
```

`internal/compact/logging.go:15` wraps another strategy; `internal/compact/logging.go:21` is the constructor sugar. `Compact` delegates to `Inner`, skips logging when the length is unchanged or `FilePath` is empty (`internal/compact/logging.go:31`, `internal/compact/logging.go:34`), and otherwise appends a timestamped `BEFORE (N)` / `AFTER (N)` transcript pair rendered with `api.RenderTranscript` (`internal/compact/logging.go:43`). The file is opened append-only with mode `0644` (`internal/compact/logging.go:44`); write failures print to stdout instead of failing the turn (`internal/compact/logging.go:38`).

## Memory Store interface

```go
type Entry struct {
	Time    time.Time
	Kind    string
	Content string
	Tags    []string
}
```

`internal/memory/store.go:19` defines one memory unit; `Kind` routes handling (e.g. `SessionFiles` treats `KindSessionSummary` as header/index material, per `internal/memory/store.go:15`). Recognised kinds (`internal/memory/store.go:28`):

```go
const (
	KindFact           = "fact"
	KindDecision       = "decision"
	KindSessionSummary = "session-summary"
	KindPreference     = "preference"
)
```

The persistence contract (`internal/memory/store.go:40`):

```go
type Store interface {
	Save(ctx context.Context, e Entry) error
	Recall(ctx context.Context, query string, limit int) ([]Entry, error)
	Preamble(ctx context.Context) (string, error)
}
```

`Save` writes, `Recall` searches, and `Preamble` returns the always-loaded preface for the system prompt at session start; lifecycle methods like `Close` stay on concrete types (`internal/memory/store.go:35`). Dispatch goes through the package-level `var Default Store = NoMemory{}` (`internal/memory/store.go:49`), and `NoMemory` succeeds on every method with empty output (`internal/memory/store.go:56`).

## SessionFiles — file-backed default store

```go
type SessionFiles struct {
	root         string
	mu           sync.Mutex
	index        []SessionRecord
	draft        []Entry // in-memory entries gathered this session, flushed at Close
	sessionStart time.Time
}
type SessionRecord struct {
	Path    string    `json:"path"`
	Date    time.Time `json:"date"`
	Summary string    `json:"summary"`
	Tags    []string  `json:"tags"`
}
```

`internal/memory/sessionfiles.go:24` stores one markdown file per session under `<root>/sessions/` with `<root>/index.json` as the fast-lookup layer (`internal/memory/sessionfiles.go:20`, `internal/memory/sessionfiles.go:32`). `NewSessionFiles(root)` creates `<root>/sessions`, loads the index, and silently prunes index entries whose files are gone (`internal/memory/sessionfiles.go:45`, `internal/memory/sessionfiles.go:76`). A missing `index.json` starts empty; a corrupt one returns an error (`internal/memory/sessionfiles.go:57`).

`Save` stamps a zero `Time` with `time.Now()` and appends to the in-memory draft — nothing reaches disk until `Close` (`internal/memory/sessionfiles.go:100`). `Recall(query, limit)` defaults non-positive limits to 5, sorts a copy of the index most-recent-first, and returns up to `limit` records whose summary or tags contain the query as a case-insensitive substring (`internal/memory/sessionfiles.go:114`, `internal/memory/sessionfiles.go:138`), each converted to `Entry{Kind: KindSessionSummary, Content: "[path] summary"}` (`internal/memory/sessionfiles.go:150`). An empty query matches everything, so it acts as "recent sessions" listing.

`Preamble` caps output at `const preambleSessionCount = 5` (`internal/memory/sessionfiles.go:18`), returning a `# Recent sessions (most recent first)` block of `- DATE (tags): summary` lines (`internal/memory/sessionfiles.go:162`); empty history returns `""`. `Close` is a no-op on an empty draft, otherwise writes `<root>/sessions/YYYY-MM-DD-HHhMM.md`, appends the record, flushes `index.json`, and clears the draft — safe to call repeatedly since only the first call has effect (`internal/memory/sessionfiles.go:196`). `assembleSession` promotes the `KindSessionSummary` entry to file header plus index record (default summary `(no summary)`), groups the rest under `Facts` / `Decisions` / `Preferences` sections, and puts unknown or empty kinds under `Notes` (`internal/memory/sessionfiles.go:225`).

**Covers:** component 03
