# A Brief History of Ralph

**Article:** [A Brief History of Ralph (Dex Horthy, 2026)](https://www.humanlayer.dev/blog/brief-history-of-ralph)

## Human Readable TL;DR

Imagine you had a diligent intern who would keep re-reading a to-do list and chipping away at tasks, one small chunk at a time, without ever needing a coffee break. The "Ralph Wiggum Technique" is essentially that: a simple loop that feeds a set of written instructions to an AI coding assistant over and over until the work is done. It sounds almost too dumb to work -- and yet it does, often surprisingly well. This article is the story of how that idea emerged, spread, and eventually got an official plugin (which turned out to miss the whole point).

## TL;DR

The Ralph Wiggum Technique, created by Geoff Huntley, runs an AI coding agent in a continuous bash loop against declarative specification documents. First shown in June 2025, it proved effective for refactoring and standardisation tasks by keeping each iteration scoped to a small, independent context window. The official Anthropic plugin released in December 2025 disappointed by requiring `--dangerously-skip-permissions` and failing to replicate the core principle of isolated context chunks.

---

## Problem & Motivation

Modern LLM-based coding agents are powerful but struggle with large, sprawling tasks: context windows fill up, instructions get stale, and massive changesets create rebase nightmares. The question driving ralph was: what if you kept tasks tiny and declarative, and simply looped the agent until it converged? The answer was a surprisingly effective workflow that also clarified what "context engineering" really means in practice.

---

## Main Original Ideas

1. **The Bash Loop as an Agent Runtime** -- The simplest possible continuous agent: `while :; do cat PROMPT.md | npx --yes @sourcegraph/amp; done`. The insight is that the loop is not the point -- the declarative specification inside `PROMPT.md` is. Telling the agent *what* to achieve rather than *how* to do it produces more durable results than imperative step-by-step prompts.

2. **Context Window Carving** -- Each iteration of the loop gets its own fresh, isolated context window. This prevents context pollution across tasks and makes failures cheap: if a run goes wrong, discard it and start again rather than rebasing a large diff. The author notes: "code is cheap" -- re-running ralph on fresh code beats resolving merge conflicts.

3. **Specification Quality as the Bottleneck** -- The GTD productivity experiment failed not because of the loop, but because the spec documents were poorly written. A high-quality, tested workflow understanding is a prerequisite; ralph cannot substitute for knowing what you actually want.

4. **Cursed Lang as Proof of Concept** -- Geoff Huntley used ralph to build a programming language (cursed lang) sequentially in C, Rust, and Zig, then wrote a stage-2 self-hosting compiler in cursed lang itself -- a credible demo that the technique scales beyond trivial tasks.

---

## Key Findings

| Finding | Context |
|---|---|
| React codebase refactored in ~6 hours | Agent developed refactor plan and executed standards changes autonomously |
| 6 repos shipped overnight | "Repomirror" HN post documented via ralph loop |
| Official plugin rated disappointing | Requires `--dangerously-skip-permissions`, misses isolated-context-window principle |
| Declarative > imperative | Consistent lesson across all experiments |

- Best use cases: refactoring, enforcing coding standards, project setup, spec generation.
- Poor use cases: exploratory work where the desired end state is unknown.
- Semantic diffusion risk: widespread YouTube coverage and the official plugin risk diluting the specific concept into generic "AI agent in a loop" noise.

---

## Suggestions & Future Directions

1. The bash loop is a floor, not a ceiling -- smarter loop implementations (better state management, smarter task decomposition) could amplify results further.
2. Kanban-style task tracking (as shown by Matt Poccock) grounds ralph in practical team workflows and reduces ambiguity.
3. Improving spec-writing practices is the highest-leverage activity for teams adopting the technique -- more so than tuning the loop itself.
4. The January 2026 "Ralph Showdown" video comparing the raw bash loop vs. the official plugin is an open comparison whose winner is not stated in this post.

---

## Authors & Institutions

Dex Horthy (HumanLayer / Codelayer) -- article author and practitioner.
Geoff Huntley -- creator of the Ralph Wiggum Technique and cursed lang.
Vaibhav -- co-guest on the "AI That Works" podcast episode covering ralph.
