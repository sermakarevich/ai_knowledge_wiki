# Codex Memories

**Source:** [Codex Memories -- OpenAI Developers Documentation](https://developers.openai.com/codex/memories)

## Human Readable TL;DR

Imagine if every time you started a new conversation with a helpful assistant, you had to re-explain your tech stack, your preferences, and which mistakes to avoid. Codex Memories is a small notebook the assistant keeps on your computer, where it jots down useful patterns from past conversations so it remembers them next time. You can turn it on or off per conversation, and the notebook never leaves your machine.

## TL;DR

Codex Memories is an opt-in local recall layer that persists durable context (preferences, workflows, tech stacks, project conventions, known pitfalls) across threads without forcing users to repeat themselves. Memory files live under `~/.codex/memories/` and are generated asynchronously from eligible idle threads using configurable extraction and consolidation models. The feature is off by default, currently unavailable in EEA/UK/Switzerland, and is positioned as a supplement to -- not a replacement for -- `AGENTS.md` and checked-in documentation.

---

## Problem & Motivation

Users starting a new Codex thread previously had to re-establish context from scratch: which stack they use, what conventions the project follows, which pitfalls have already been learned, and what personal workflow preferences matter. Pasting the same boilerplate into every session is friction and pollutes the context window. Codex Memories addresses this by persisting stable, recurring context locally so future threads can pull it in automatically, while keeping the user in control of when memories are read or written.

---

## Main Original Ideas

1. **Local-only recall layer.** Memories live entirely under `~/.codex/memories/` on the user's machine. They are not a cloud feature -- no server-side storage of conversation summaries is implied -- which keeps data residency simple and makes the EEA/UK/Switzerland exclusion a launch-phase policy choice rather than an architectural constraint.

2. **Asynchronous, idle-gated generation.** Rather than summarizing at end-of-thread (which would capture work-in-progress), Codex waits for threads to be idle long enough to be considered complete before generating memory artifacts. This avoids polluting long-term memory with half-finished reasoning.

3. **Per-thread governance via `/memories`.** A dedicated slash command (available in both app and TUI) lets the user decide, per session, whether to read from existing memories and whether to contribute to future memory generation -- a four-quadrant control surface (read/no-read crossed with write/no-write).

4. **Separate extract and consolidate models.** The pipeline exposes two distinct model choices: `memories.extract_model` for per-thread extraction and `memories.consolidation_model` for global consolidation across threads. This lets users tune cost/quality at each stage independently.

5. **Layered memory artifacts.** A memory file is not a single blob; it includes summaries, durable entries, recent inputs, and supporting evidence from prior threads -- so the system preserves provenance alongside the distilled content.

6. **Explicit guidance split from memories.** Team-wide rules belong in `AGENTS.md` or checked-in docs; memories are explicitly framed as local, personal recall, not a shared source of truth.

---

## Key Findings

This is a product documentation page rather than a research paper, so there are no experimental results. Structural features worth tracking:

| Aspect | Detail |
|--------|--------|
| Default state | **Off** |
| Storage location | `~/.codex/memories/` |
| Config file | `~/.codex/config.toml`, `[features]` table |
| Activation key | `memories = true` |
| Per-thread control | `/memories` slash command (app + TUI) |
| Launch regions excluded | EEA, UK, Switzerland |
| Secret handling | Auto-redaction with user review recommended |
| Manual editing | Discouraged -- treated as generated state |
| Related feature | Chronicle (screen-based recent-context recovery) |

Configuration knobs exposed:

- `memories.generate_memories` -- whether new threads contribute
- `memories.use_memories` -- whether existing memories inject into new sessions
- `memories.extract_model` -- per-thread extraction model
- `memories.consolidation_model` -- global consolidation model

---

## Suggestions & Future Directions

1. **Chronicle integration.** The docs point to Chronicle as a companion feature that "helps Codex recover recent working context from your screen to build up memory" -- suggesting a roadmap where on-disk memories are augmented by on-screen signals.

2. **Regional rollout.** The EEA/UK/Switzerland exclusion is flagged as "at launch," implying later availability pending (presumably) privacy/compliance review.

3. **Explicit split with `AGENTS.md`.** The guidance to keep required team rules in `AGENTS.md` signals that memories are deliberately scoped as personal, not team, context -- future team-level sharing would need a different mechanism.

4. **Secret-handling maturity.** Current redaction is automatic but the docs advise human review before sharing the Codex home directory, indicating room for stronger guarantees.

---

## Authors & Institutions

OpenAI (Codex product team). Published on the OpenAI Developers documentation site.
