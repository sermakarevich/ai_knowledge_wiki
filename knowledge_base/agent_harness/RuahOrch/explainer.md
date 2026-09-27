> [[index|Wiki]] | [[summary|Summary]]

# ruah-orch — In Plain Language

## What is this about?

Imagine hiring five builders to renovate one house at the same time. If everyone just walks in and starts hammering, they will trip over each other: two people paint the same wall different colors, someone tears out wiring someone else just installed. The usual fix is taking turns — slow — or cleaning up the mess afterward — painful.

Ruah is the foreman with a simple rule: **before you start, write down exactly which rooms are yours.** One builder owns the kitchen (nobody else may touch it). Two builders share the hallway, but only to add things at the end, never to rip out what is there. Everyone may look at the blueprints (read-only) but not redraw them. The foreman checks these notes for conflicts before anyone picks up a tool, gives each builder a separate copy of the house to work in, inspects the finished work against the notes, and then combines everything back in the right order.

In software terms: each AI coding agent declares which files it will touch (a "claim"), works isolated in its own copy of the code (a git worktree), and the orchestrator validates the result and merges it back.

## Why does it matter?

AI coding assistants are becoming good enough that running several at once is tempting — one writes the web pages, another the server code, a third the tests. But they all share one pitfall: they overwrite each other's work, and a human spends the saved time untangling merge conflicts instead. Ruah's answer is prevention plus proof: prevent conflicts with declared boundaries, and keep a receipt (an "artifact": exactly what changed, plus whether it passed inspection) so nothing merges silently. It also avoids vendor lock-in — the same foreman can supervise builders from different companies (Claude Code, Aider, Codex, OpenCode, or a plain script).

## How does it work?

1. **Declare.** Each job lists its files: "I own these, I append to those, I only read these."
2. **Check.** The foreman compares all notes. Two owners for one room? A helper working outside its supervisor's rooms? Rejected before anyone starts.
3. **Separate.** Each job gets a private copy of the house (an isolated workspace branched from the main code).
4. **Supervise.** The chosen worker (whichever AI tool the job names) is started inside that copy, with a note on the door stating its name, its rooms, and who its supervisor is (environment variables like `RUAH_TASK`).
5. **Inspect.** When the worker finishes, the foreman diffs the copy against the original: owned changes pass, read-only edits fail, shared files must be additions-only, anything undeclared fails.
6. **Combine.** Approved copies are merged back in dependency order (foundations before walls), with policy checks (governance gates) for top-level jobs. A single notebook (one state file, carefully locked so concurrent foremen do not scribble over each other) tracks everything, and survives restarts.

## Where can this be used?

- Any team running parallel AI coders on one repository (the direct use case).
- Human teams that want lightweight file-ownership contracts without adopting a monorepo permission system.
- Continuous-integration pipelines that need a receipt of exactly what an automated change touched and whether it respected its scope.
- Outside software: any parallel-work setup where participants declare resource boundaries up front (think lab equipment schedules or shared documents with append-only sections).

## Conclusions & takeaways

What to remember a month from now: boundaries declared up front beat conflicts cleaned up later; a stored receipt (diff plus verdict) makes automated work auditable; and you do not need heavy infrastructure for any of this — ruah does it with plain git worktrees, one JSON file with careful locking, and no install-time dependencies. Honest limitations: the boundaries are file globs (it cannot tell two agents apart inside the same file), and the single state file can become a bottleneck with dozens of simultaneous workers.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Claim | A job's written note saying which files it owns, shares, or only reads |
| Artifact | The receipt kept after a job: what changed, plus pass/fail verdicts |
| Worktree | A private copy of the code for one job to work in |
| DAG workflow | A to-do list with arrows showing which jobs must finish first (no loops allowed) |
| Executor | Which AI tool (or script) actually does a job |
| Contract validation | Inspecting finished work against the declared claim |
| Append-only | Allowed to add at the end, forbidden to change or delete what exists |
| Governance gate | A policy check (e.g. tests, approvals) that must pass before merging |
| State file | The foreman's notebook tracking every job's status |
| Revision guard | A counter that rejects stale notebook updates so nothing is silently overwritten |
