> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Non-interactive mode output formats
**In one sentence:** Use `claude -p` for non-interactive one-off queries, defaulting to plain text, using `--output-format json` for a single JSON object with a `result` field for scripts, and `--output-format stream-json --verbose` for line-delimited JSON starting with an `init` event for real-time processing.
## Key points
- Run one-off non-interactive queries with `claude -p` plus a quoted prompt, e.g. `claude -p "Explain what this project does"`.
- The default (first) command prints plain text with no output-format flag.
- Use structured output for scripts via `claude -p "List all API endpoints" --output-format json`.
- The `json` format returns a single JSON object with a `result` field.
- Use streaming for real-time processing via `claude -p "Analyze this log file" --output-format stream-json --verbose`.
- The `stream-json` format prints one JSON object per line, starting with an `init` event.
---
## One-off queries
**Covers:** Non-interactive `claude -p` one-off queries with text, JSON, and streaming JSON output

Verbatim command:

```
claude -p "Explain what this project does"
```

Claim from chunk: "The first command prints plain text."

## Structured output for scripts
Verbatim command:

```
claude -p "List all API endpoints" --output-format json
```

Claim from chunk: "The json format returns a single JSON object with a result field."

## Streaming for real-time processing
Verbatim command:

```
claude -p "Analyze this log file" --output-format stream-json --verbose
```

Claim from chunk: "The stream-json format prints one JSON object per line, starting with an init event."
