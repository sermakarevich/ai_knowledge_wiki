> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# You will wake up to a broken code base
**In one sentence:** You will wake up to a non-compiling codebase Ralph cannot always fix himself, so you must judge between `git reset --hard` and rescue prompts, keep `fix_plan.md`/commit/tag discipline, and treat Ralph as a Greenfield-only bootstrapper that gets ~90% done under senior guidance because any AI-created problem is solvable with a different series of prompts and more loops.
## Key points
- Expect a broken, non-compiling codebase on some mornings that Ralph cannot fix himself; the operator judgment call is `git reset --hard` and restart Ralph versus crafting another series of rescue prompts.
- The commit discipline is: when tests pass update `@fix_plan.md`, then `git add -A` changed code plus `@fix_plan.md`, `git commit` with a descriptive message, then `git push`; when there are no build or test errors create a git tag starting at `0.0.0` and incrementing patch by 1 (e.g. `0.0.1`).
- Compilation-error volume once filled Claude's context window, and the workaround was throwing the error file into Gemini and asking Gemini to create a plan for Ralph.
- The maintainability objection is answered with "by whom?", rejecting humans as the frame and arguing for post-AI loops that resolve/adapt when needed.
- The core claim is that all Ralph-created issues "can be resolved by crafting a different series of prompts and running more loops with Ralph"; Ralph has three states — under baked, baked, or baked with unspecified latent behaviours (sometimes quite nice).
- Ralph is Greenfield-only: verbatim "There's no way in heck would I use Ralph in an existing code base", with expectation of 90% done via bootstrapping; senior expertise is still required, denials of that are "peddling horseshit", yet the technique can displace a large majority of SWEs as they currently are on Greenfield projects.
- Scale numbers in the CURSED prompts are explicit: up to 500 parallel subagents for build-prompt operations (only 1 subagent for Rust build/tests), up to 500 subagents for each plan-prompt study task, and up to 1000 parallel subagents for authoring multiple stdlib libraries at once.
---
## You will wake up to a broken code base
**Covers:** "you will wake up to a broken code base"

Verbatim: "Yep, it's true, you'll wake up to a broken codebase that doesn't compile from time to time, and you'll have situations where Ralph can't fix it himself."

Operator rule: "This is where you need to put your brain on. You need to make a judgment call. Is it easier to do a git reset --hard and to kick Ralph back off again? Or do you need to come up with another series of prompts to be able to rescue Ralph?"

Discipline quoted from the chunk:

> When the tests pass update the @fix_plan.md`, then add changed code and @fix_plan.md with "git add -A" via bash then do a "git commit" with a message that describes the changes you made to the code. After the commit do a "git push" to push the changes to the remote repository.

> As soon as there are no build or test errors create a git tag. If there are no git tags start at 0.0.0 and increment patch by 1 for example 0.0.1 if 0.0.0 does not exist.

Scale anecdote: "when I was first getting this compiler up and running, and the number of compilation errors was so large that it filled Claude's context window. So, at that point, I took the file of compilation errors and threw it into Gemini, asking Gemini to create a plan for Ralph."

## But maintainability?
**Covers:** "but maintainability?"

Verbatim exchange:

> When I hear that argument, I question "by whom"? By humans? Why are humans the frame for maintainability? Aren't we in the post-AI phase where you can just run loops to resolve/adapt when needed? 😎

## Any problem created by AI can be resolved through a different series of prompts
**Covers:** "any problem created by AI can be resolved through a different series of prompts"

Claims and verbatim quotes:

- "What I'd like people to understand is that all these issues, created by Ralph, can be resolved by crafting a different series of prompts and running more loops with Ralph."
- CURSED is expected to "have some significant gaps, just like Ralph Wiggum"; it is easy to poke holes in CURSED right now, which is why publication was held back; "The repository is full of garbage, temporary files, and binaries."
- Request to refrain from finding the CURSED codebase on GitHub and sharing it on social media because "it's not yet ready for launch"; the goal is "indisputable proof that AI can build a brand new programming language and program a programming language where it has no training data in its training set is possible."
- "Ralph has three states. Under baked, baked, or baked with unspecified latent behaviours (which are sometimes quite nice!)"
- Technique claim: "When CURSED ships, understand that Ralph built it. What comes next, technique-wise, won't be Ralph. I firmly maintain that if models and tools remain as they are now, we are in post-AGI territory. All you need are tokens; these models yearn for tokens, so throw them at them, and you have primitives to automate software development if you take the right approaches."
- Staffing claim: "Having said all of that, engineers are still needed. There is no way this is possible without senior expertise guiding Ralph. Anyone claiming that engineers are no longer required and a tool can do 100% of the work without an engineer is peddling horseshit."
- Displacement claim: "the Ralph technique is surprisingly effective enough to displace a large majority of SWEs as they are currently for Greenfield projects."
- Scope limit, verbatim: "There's no way in heck would I use Ralph in an existing code base" — with invitation to report outcomes if tried; "This works best as a technique for bootstrapping Greenfield, with the expectation you'll get 90% done with it."

| Number in chunk | Meaning |
|---|---|
| 90% | expected completion via Greenfield bootstrapping |
| 100% | rejected claim that a tool does this without an engineer |
| three states | under baked / baked / baked with unspecified latent behaviours |

## Current prompt used to build CURSED
**Covers:** "current prompt used to build cursed"

Preamble quoted verbatim:

> 0a. study specs/* to learn about the compiler specifications
> 0b. The source code of the compiler is in src/
> 0c. study fix_plan.md.

Build-prompt mechanics (spelling as in source, e.g. "parrallel"):

| # | Instruction |
|---|---|
| 1 | Implement missing stdlib (see `@specs/stdlib/*`) and compiler functionality and produce a compiled application in the cursed language via LLVM using parallel subagents; follow `fix_plan.md` and choose the most important 10 things; before making changes search codebase (don't assume not implemented) using subagents; up to 500 parallel subagents for all operations but only 1 subagent for build/tests of rust. |
| 2 | After implementing or resolving problems, run the tests for that unit of improved code; if functionality is missing add it per application specifications; "Think hard." |
| 2 (parser/LLVM) | On discovering a parser, lexer, control flow or LLVM issue, immediately update `@fix_plan.md` with findings using a subagent; when resolved, update `@fix_plan.md` and remove the item using a subagent. |
| 3 | When tests pass update `@fix_plan.md`, then `git add -A`, `git commit` with descriptive message, then `git push`. |
| 999–99999999999 | Authoring docs must capture why tests and backing implementation matter; single sources of truth, no migrations/adapters; unrelated failing tests must be resolved as part of the increment; tag when no build/test errors (`0.0.0` → `0.0.1` pattern); may add extra logging; ALWAYS keep `@fix_plan.md` up to date with learnings via subagent especially after turn; update brief `@AGENT.md` on compiler/example commands via subagent; stdlib in cursed itself with tests — delete/migrate rust implementations; resolve/document bugs via subagents even if unrelated; start cursed stdlib with testing primitives; stdlib tests next to source plus per-folder `README.md`; keep `AGENT.md` build/test-loop learnings current; resolve or document noticed bugs in `@fix_plan.md`; up to 1000 parallel subagents for multiple stdlibs; periodically clean completed items from large `@fix_plan.md`; fix `specs/*` inconsistencies (types, lexical tokens) via oracle then update specs. |
| 9999999999999999999999999999 | Verbatim: "DO NOT IMPLEMENT PLACEHOLDER OR SIMPLE IMPLEMENTATIONS. WE WANT FULL IMPLEMENTATIONS. DO IT OR I WILL YELL AT YOU" |
| 9999999999999999999999999999999 | Verbatim: "SUPER IMPORTANT DO NOT IGNORE. DO NOT PLACE STATUS REPORT UPDATES INTO @AGENT.md" |

## Current prompt used to plan CURSED
**Covers:** "current prompt used to plan cursed"

Inputs quoted verbatim:

> study specs/* to learn about the compiler specifications and fix_plan.md to understand plan so far.
> The source code of the compiler is in src/*
> The source code of the examples is in examples/* and the source code of the tree-sitter is in tree-sitter/*. Study them.
> The source code of the stdlib is in src/stdlib/*. Study them.

| Task | Instruction |
|---|---|
| First task | Study `@fix_plan.md` (may be incorrect) and use up to 500 subagents to study `src/` versus compiler specifications; create/update `@fix_plan.md` as a priority-sorted bullet list of unimplemented items; "Think extra hard and use the oracle to plan"; search TODOs, minimal implementations, placeholders; keep `@fix_plan.md` complete/incomplete status current using subagents. |
| Second task | Use up to 500 subagents to study `examples/` versus compiler specifications; create/update `fix_plan.md` the same way (priority-sorted, oracle, TODOs/minimal/placeholders, subagent-kept status). |
| Stdlib rule | Verbatim: "The standard library in src/stdlib should be built in cursed itself, not rust. If you find stdlib authored in rust then it must be noted that it needs to be migrated." |
| Ultimate goal | Self-hosting compiler release with full stdlib; plan missing stdlib modules; if stdlib missing, author spec at `specs/stdlib/FILENAME.md` (search before creating, do NOT assume non-existence); module naming "should be GenZ named and not conflict with another stdlib module name"; new modules get an implementation plan in `@fix_plan.md`. |
