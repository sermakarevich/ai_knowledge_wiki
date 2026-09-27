> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# CLAUDE.md Code Style and Workflow

**In one sentence:** Put broadly-applicable code-style rules (ES modules with destructured imports) and workflow rules (typecheck after a series of changes, run single tests for performance) in a concise CLAUDE.md, cutting anything that fails the "would removing this cause mistakes?" test.

## Key points

- Use ES modules (`import`/`export`) syntax, not CommonJS (`require`), as a CLAUDE.md code-style rule.
- Destructure imports when possible, e.g. `import { foo } from 'bar'`.
- Typecheck when done making a series of code changes.
- Prefer running single tests rather than the whole test suite, for performance.
- CLAUDE.md is loaded every session, so include only broadly-applicable rules; put sometimes-relevant domain knowledge or workflows in skills that Claude loads on demand.
- Keep CLAUDE.md concise with the cut test: "Would removing this cause Claude to make mistakes?" — if not, cut it, because bloated files cause Claude to ignore actual instructions.
- Run `/context` to confirm Claude loaded the file; check CLAUDE.md into git so the team can contribute and value compounds; import additional files with `@path/to/import` syntax.

---

## Code style

Per the chunk heading, the prescribed CLAUDE.md code-style rules are:

- Use ES modules (`import`/`export`) syntax, not CommonJS (`require`).
- Destructure imports when possible (e.g. `import { foo } from 'bar'`).

The chunk body provides no further elaboration, examples, or rationale beyond these two lines.

## Workflow

Per the chunk heading, the prescribed workflow rules are:

- Be sure to typecheck when you're done making a series of code changes.
- Prefer running single tests, and not the whole test suite, for performance.

The chunk body provides no test-runner names, typecheck commands, or timing numbers beyond this.

## Keeping CLAUDE.md concise

- `CLAUDE.md` is loaded every session, so "only include things that apply broadly"; for domain knowledge or workflows that are only relevant sometimes, "use skills instead" since "Claude loads them on demand without bloating every conversation."
- Verbatim rule: "Keep it concise. For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it."
- Verbatim warning: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

## What to include vs exclude

The chunk gives this include/exclude table (verbatum):

| ✅ Include | ❌ Exclude |
|---|---|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

## Maintaining CLAUDE.md

- "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."
- "If Claude asks you questions that are answered in CLAUDE.md, the phrasing might be ambiguous."
- "Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts."
- For a checked-in file, "run /doctor and Claude proposes cuts for content it can derive from the codebase."
- "If Claude keeps skipping one instruction, add emphasis such as 'IMPORTANT' to that line alone. If you emphasize many lines, none of them stands out."
- "Check CLAUDE.md into git so your team can contribute. The file compounds in value over time."
- "CLAUDE.md files can import additional files using @path/to/import syntax."

**Covers:** CLAUDE.md code-style rules and workflow conventions (typecheck, focused test runs)
