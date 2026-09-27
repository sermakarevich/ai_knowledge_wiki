> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# What's in the prompt.md? Can I have it?
**In one sentence:** There is no perfect, copy-pasteable prompt — the CURSED prompt works only because it was continually tuned from watching Ralph, and its core mechanics are one item per loop, the same stack allocation every loop (fix plan + specs), and a scheduler-style primary context that fans out to subagents.
## Key points
- There is no perfect prompt, and copying the CURSED prompt verbatim will not reproduce its outcomes because it evolved through continual tuning based on observed LLM behaviour.
- Ralph is monolithic, not multi-agent: one repository, one single-process loop, performing one task per loop, instead of non-deterministic agent-to-agent multiplexing.
- Ralph is told to choose the most important thing itself and implement only one item per loop, relaxing that restriction only later and re-tightening if it goes off the rails.
- Every loop deterministically allocates the same items to context: the plan (`@fix_plan.md`) plus the specifications (`@specs/stdlib/*`).
- Specs are produced by a long requirements conversation with the agent first, then written out one file per spec into the specifications folder.
- The usable context budget is ~170k, so minimal primary-context allocation matters; the CURSED setup deliberately re-burns the specs allocation each loop rather than reusing it.
- The primary context must act as a scheduler that spawns subagents for expensive work (e.g. summarising test results), with parallelism controlled: many subagents for search/write but only 1 subagent for Rust build/tests, since fanning out hundreds of builders causes bad back pressure.
- Code search via ripgrep is non-deterministic, so a signature Ralph failure is wrongly concluding code is missing and duplicating implementations; the fix is an explicit "don't assume, search with subagents" sign, and duplicate implementation is called the Achilles' heel.
---
## No perfect prompt to copy
**Covers:** "what's in the prompt.md? can I have it?"

There is an obsession with the perfect prompt; there is no such thing. Taking the CURSED prompt verbatim will not make sense unless you know how to wield it, because it evolved through continual tuning based on observation of LLM behaviour — the author watches the stream, looks for patterns of bad behaviour, and tunes Ralph at each opportunity.

## First fundamentals: monolithic single loop
**Covers:** "first some fundamentals"

Multi-agent / agent-to-agent multiplexing is not needed at this stage; non-deterministic agents composed like microservices would be "a red hot mess". The opposite — a monolith — is the model: Ralph works autonomously in a single repository as a single process performing one task per loop.

To get good outcomes, ask Ralph to do one thing per loop and trust Ralph to decide what is most important to implement — described as full hands-off vibe coding. LLMs are surprisingly good at reasoning about what is important and what the next steps are.

Core prompt quoted verbatim:

> Your task is to implement missing stdlib (see @specs/stdlib/*) and compiler functionality and produce an compiled application in the cursed language via LLVM for that functionality using parrallel subagents. Follow the @fix_plan.md and choose the most important thing.

The other key mechanic is to deterministically allocate the stack the same way every loop: the plan (`@fix_plan.md`) and the specifications. Specs are formed through a conversation with the agent at the beginning of a project — not by asking for implementation immediately, but by a long conversation about requirements, then issuing a prompt to write specifications out, one per file, in the specifications folder.

## One item per loop
**Covers:** "one item per loop"

One item per loop — repeated for emphasis. The restriction may be relaxed as the project progresses, but if it goes off the rails, narrow back to one item. The game is a context budget of approximately 170k: use as little of it as possible, because the more is used, the worse the outcomes. This is wasteful in one sense, because the specifications allocation is effectively burned every loop instead of reused.

## Extend the context window via subagents as scheduler
**Covers:** "extend the context window"

Agentic loops work by executing a tool then evaluating the result, and that evaluation adds an allocation to the context window. Ralph requires the mindset of not allocating to the primary context window; instead the primary context operates as a scheduler, scheduling subagents to do expensive allocation-type work such as summarising whether the test suite worked.

On real vs advertised windows: Claude 3.7's advertised window is 200k, but observed output quality clips at the 147k–152k mark.

Parallelism is controllable. Quoted instruction variant:

> Your task is to implement missing stdlib (see @specs/stdlib/*) and compiler functionality and produce an compiled application in the cursed language via LLVM for that functionality using parrallel subagents. Follow the fix_plan.md and choose the most important thing. Before making changes search codebase (don't assume not implemented) using subagents. You may use up to parrallel subagents for all operations but only 1 subagent for build/tests of rust.

Fanning out to a couple of hundred subagents and telling them all to run build and test produces bad-form back pressure; hence only a single subagent for validation (Rust build/tests), while Ralph may use as many subagents as it likes for filesystem search and file writing.

## Don't assume it's not implemented
**Covers:** "don't assume it's not implemented"

All coding agents work via ripgrep, and code-based search can be non-deterministic. A common Ralph failure is running ripgrep and wrongly concluding code is not implemented; it is fixed by erecting a sign instructing Ralph not to assume. Quoted sign:

> Before making changes search codebase (don't assume an item is not implemented) using parrallel subagents. Think hard.

If Ralph wakes up doing multiple implementations, that step needs tuning; this nondeterminism is called the Achilles' heel of Ralph.
