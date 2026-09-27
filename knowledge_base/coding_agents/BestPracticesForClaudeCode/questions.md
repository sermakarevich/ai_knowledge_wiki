---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Best practices for Claude Code - Claude Code Docs

### Q1. Why is the context window the most important resource to manage in Claude Code, and what fills it?

> [!tip]- Answer
> > The window holds every message, file read, and command output, so a single debugging session or exploration can consume tens of thousands of tokens. As it fills, Claude starts "forgetting" earlier instructions and making more mistakes. See [[wiki/01-documentation-index|Documentation Index]].

### Q2. What kind of verification check should you give Claude, and why does it matter?

> [!tip]- Answer
> > Give Claude a runnable signal it can read in-conversation: a test suite, build exit code, linter, output-diff script, or screenshot comparison. Without one, "looks done" is the only signal and you become the verification loop; with one, Claude iterates itself. See [[wiki/01-documentation-index|Documentation Index]].

### Q3. What are the four phases of the Explore → Plan → Implement → Commit workflow, and how do you enter plan mode?

> [!tip]- Answer
> > Explore read-only in plan mode, then ask for a detailed plan, then approve/leave plan mode and implement with verification, then commit with a descriptive message and PR. Enter plan mode with Shift+Tab until `⏸ plan mode on`, or `claude --permission-mode plan`. See [[wiki/01-documentation-index|Documentation Index]].

### Q4. How do you make prompts specific and supply rich content to Claude Code?

> [!tip]- Answer
> > Scope the file/scenario/test preferences, point to sources like git history, reference existing codebase patterns, and describe the symptom plus what "fixed" looks like. Supply content directly via `@`-referenced files, pasted images, documentation URLs (allowlist via `/permissions`), or piped data like `cat error.log | claude`. See [[wiki/01-documentation-index|Documentation Index]].

### Q5. What belongs in CLAUDE.md, and what is the cut test for keeping it concise?

> [!tip]- Answer
> > Include only broadly-applicable rules — Bash commands Claude can't guess, non-default style, test runners, repo etiquette, architecture decisions — and put sometimes-relevant knowledge in skills loaded on demand. For each line ask "Would removing this cause Claude to make mistakes?"; if not, cut it, since bloated files make Claude ignore real instructions. See [[wiki/02-claude-md-code-style-and-workflow|CLAUDE.md Code Style and Workflow]].

### Q6. When do you use plain text, `json`, and `stream-json` output with `claude -p`?

> [!tip]- Answer
> > `claude -p "prompt"` prints plain text by default for one-off queries. Add `--output-format json` for scripts — it returns a single JSON object with a `result` field. Use `--output-format stream-json --verbose` for real-time processing, which prints one JSON object per line starting with an `init` event. See [[wiki/03-non-interactive-mode-output-formats|Non-interactive mode output formats]].

### Q7. A teammate wants to paste the full API reference and a long tutorial into CLAUDE.md so Claude "knows everything" — what do you recommend and why?

> [!tip]- Answer
> > Recommend against it: exclude detailed API docs (link instead) and long tutorials, since CLAUDE.md loads every session and bloat buries real instructions. Keep only the broadly-applicable rules that pass the cut test and check the file into git for team compounding. See [[wiki/02-claude-md-code-style-and-workflow|CLAUDE.md Code Style and Workflow]].
