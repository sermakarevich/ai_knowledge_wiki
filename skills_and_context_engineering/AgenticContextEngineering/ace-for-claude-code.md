# Implementing ACE for Claude Code

**Source:** [[summary]] | Analysis of how ACE's self-improving playbook mechanism maps onto Claude Code's existing architecture.

---

## The Core Mapping

ACE has three components: **Generator** (executes tasks using a playbook), **Reflector** (extracts lessons from execution traces), **Curator** (produces structured delta updates). Claude Code already has partial analogs for each -- the gap is closing the loop automatically.

| ACE Component | Claude Code Analog | Gap |
|---|---|---|
| Generator | Claude Code session (reads CLAUDE.md + skills) | Already exists |
| Playbook (bullet list) | CLAUDE.md + claude-mem observations | Unstructured; no helpful/harmful counters |
| Reflector | `self-review` skill (manual) | Not automatic; doesn't run on every task |
| Curator | Manual CLAUDE.md edits | No delta-update logic; no dedup |
| Execution feedback | Hook system (`PostToolUse`, `Stop`) | Logs activity but doesn't feed back into context |
| Multi-epoch refinement | `self-review-improve` skill (manual) | Not automated; no convergence tracking |

---

## What To Build (5 components)

### 1. Structured Playbook Format

**Replace** free-form CLAUDE.md sections with a structured bullet store (JSON or YAML).

```jsonl
{"id": "b-001", "content": "When editing files >300 LOC, re-read the file first -- stale context causes silent Edit failures", "domain": "editing", "helpful": 12, "harmful": 1, "epoch": 3}
{"id": "b-002", "content": "For arxiv papers, always try arxiv.org URL if alphaxiv.org fails", "domain": "research", "helpful": 5, "harmful": 0, "epoch": 1}
```

**Where it lives:** `~/.claude/playbook.jsonl` -- loaded into system prompt the same way CLAUDE.md is today. Each bullet is a self-contained, actionable instruction with metadata.

**Integration:** A `SessionStart` hook injects relevant bullets (filtered by domain/project) into the prompt prefix. This replaces the monolithic CLAUDE.md approach for machine-generated knowledge while keeping human-authored CLAUDE.md for explicit user preferences.

### 2. Automatic Reflector (Post-Session Hook)

**New hook:** `Stop` event triggers a reflector script that:

1. Reads the session's `activity-log.jsonl` entries (already being logged)
2. Reads any error outputs, test failures, or user corrections from the session
3. Calls Claude (via `mcp__ask-claude__ask_claude` or a lightweight API call) with: the activity log + outcome signals + current playbook bullets used
4. Asks: "What concrete lessons should be added/updated/removed from the playbook? Output as JSON deltas."

**Key design:** The Reflector runs as a **background subagent** (not in the main session), so it doesn't contaminate the user's context window. It writes deltas to `~/.claude/playbook-deltas/pending.jsonl`.

### 3. Deterministic Curator (No LLM Needed)

A simple Node.js/Python script (triggered by hook or cron) that:

1. Reads `pending.jsonl` deltas
2. Merges into `playbook.jsonl`:
   - **New ID** -> append bullet
   - **Existing ID** -> update content in place, increment counters
   - **Delete signal** -> remove bullet
3. Runs semantic dedup: embed all bullets (via local model or API), cosine similarity > 0.92 -> merge the pair, keeping higher helpful/harmful ratio
4. Prunes bullets where `harmful / (helpful + harmful) > 0.6` (consistently misleading)
5. Writes cleaned `playbook.jsonl`

**No LLM call.** Pure data manipulation. This is ACE's key efficiency insight -- the merge logic is deterministic.

### 4. Execution Feedback Capture

Extend the existing `activity-logger.js` hook to capture outcome signals:

| Signal | Source | How to Capture |
|---|---|---|
| Tool errors | `PostToolUse` hook | Already logged; tag with `outcome: "error"` |
| User corrections | "no", "that's wrong", "try again" | Sentiment heuristic in `UserPromptSubmit` hook |
| Test pass/fail | `Bash` tool running tests | Parse exit code in `PostToolUse` |
| Task completion | User says "done", "thanks", moves on | `Stop` hook + session length heuristic |
| Explicit feedback | User runs `/self-review` | Skill output piped to reflector |

This turns every session into a training signal without requiring labeled data -- exactly ACE's self-supervision mode.

### 5. Multi-Epoch Refinement (Periodic Consolidation)

A **scheduled trigger** (via `/schedule` or cron) that runs weekly:

1. Reviews the full `playbook.jsonl`
2. Re-embeds all bullets and runs aggressive dedup (lower threshold, ~0.85)
3. Removes bullets with 0 helpful hits after 2+ weeks (never used)
4. Calls Claude to refine surviving bullets: "Given these 5 bullets about 'editing', consolidate into the fewest, most precise instructions"
5. Resets epoch counters

This is ACE's "lazy refine" mode -- lets the playbook grow daily, consolidates periodically.

---

## Implementation Priority

| Phase | What | Effort | Impact |
|---|---|---|---|
| **Phase 1** | Structured playbook format + `SessionStart` loader | 1 day | Foundation -- everything depends on this |
| **Phase 2** | Execution feedback tagging in existing hooks | 1 day | Enables self-supervision |
| **Phase 3** | Reflector as `Stop` hook subagent | 2 days | The core learning loop |
| **Phase 4** | Deterministic curator script | 1 day | Closes the loop |
| **Phase 5** | Semantic dedup + periodic consolidation | 2 days | Prevents playbook bloat |

---

## What Already Works (No Changes Needed)

- **claude-mem MCP** already stores observations with searchable metadata -- could serve as the bullet store instead of a flat file
- **Hooks infrastructure** already captures tool usage, errors, and session lifecycle events
- **Skills system** already provides the "inject specialized knowledge into prompt" pattern
- **`self-review` / `self-review-improve` skills** are manual versions of the Reflector -- they just need to be automated and output structured deltas instead of prose

## Key Risks

- **Playbook pollution:** Without good dedup, the playbook grows endlessly and drowns signal in noise. ACE mitigates this with counters + embedding dedup -- both are essential.
- **Reflector quality:** If the background reflector extracts bad lessons, they compound. Mitigation: harmful counters + periodic human review of `playbook.jsonl`.
- **Context budget:** A 200-bullet playbook at ~100 tokens/bullet = 20K tokens of system prompt. Need to filter by domain/project relevance at load time, not inject everything.
- **Privacy:** The reflector sees session traces. If sessions contain sensitive data, the playbook inherits it. Need a scrubbing step.
