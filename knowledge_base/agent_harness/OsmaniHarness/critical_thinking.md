> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Agent Harness Engineering

## Claims vs. evidence

(1) "Harness dominates model choice — same model, wildly different scores across harnesses" — **suggestive, not rigorous**. The Terminal Bench 2.0 claim (Opus 4.6 scoring far lower in Claude Code than in a custom harness) and the "Top 30 to Top 5" jump are both attributed to Viv Trivedy's write-up and repeated, not independently re-measured or sourced with a benchmark table in this piece. No control for prompt differences, tool differences, or evaluation-run variance is shown; "far lower" and "Top 30 to Top 5" are qualitative, not quantified deltas.

(2) "Most agent failures are skill issues (configuration), not model-weight problems" — **anecdotal, not measured**. The four canonical examples (missing convention, destructive command, 40-step task, false "done") are illustrative case studies, not a failure-mode census. There's no denominator — no claim about what fraction of real-world agent failures are actually fixable by harness changes versus genuinely bounded by model capability, so the piece's framing could be surviorship bias toward the failures that happen to be harness-fixable.

(3) "The ratchet: constraints only after real failure, remove only when redundant" — **plausible design heuristic, unfalsifiable as stated**. No before/after measurement of AGENTS.md size, failure rate, or false-positive friction is offered; it's presented as good practice by authority (HumanLayer, Viv) rather than demonstrated with data from a specific team's failure log over time.

(4) "Self-grading skews positive, so split generator from evaluator" — **directionally well-supported by the broader field** (this is a widely replicated finding elsewhere — e.g. VerificationHorizon in this KB treats verification as the binding constraint precisely because naive self/proxy grading is gameable), but this article cites no original experiment of its own for the claim; it borrows Anthropic's stated position.

(5) "Scaffolding moves rather than shrinks as models improve (Opus 4.6 killed context-anxiety scaffolding, created need for multi-day memory)" — **single anecdote generalized**. One named behavioural change (premature "wrapping up" near context limits) is used to support a general law about how scaffolding evolves; it's a good illustration but not a pattern shown across multiple model generations in this piece.

## Genuinely new vs. repackaged

Almost nothing here is a novel technical contribution — the article is explicit about synthesizing Viv Trivedy's "Anatomy of an Agent Harness," HumanLayer's "skill issue" framing, Anthropic's long-running-work engineering post, Simon Willison's tools-in-a-loop definition, and Fareed Khan's Claude Code breakdown. The genuine value-add is the synthesis itself: naming and ordering the primitives (filesystem, bash, sandboxes, memory, context-rot defences, hooks, verification, HaaS) into one coherent, working-backwards-from-behaviour narrative that a practitioner can use as a checklist. It is a curation and framing exercise, not a research result.

## Weaknesses and blind spots

- No cost or failure-rate numbers anywhere: every claim about harnesses beating models is directional ("far lower," "Top 30 to Top 5," "wastes tokens") with no comparison table, unlike e.g. TheHarnessEffect in this KB, which quantifies the same underlying thesis (41% cost cut, 44% latency cut, 38% fewer tokens on 22 locked tasks across 6 models).
- The "ratchet" pattern has an unaddressed scaling failure mode: if every team's AGENTS.md only grows from accumulated failures and shrinks only "when a capable model makes a rule redundant" (a judgment call with no test proposed), the piece doesn't address how a team detects that a rule has become dead weight before it silently degrades performance — the 60-line HumanLayer heuristic is asserted, not derived.
- Security note (MCP tool descriptions are trusted, unvetted text injected into the prompt) is flagged but not explored — no mitigation beyond awareness is offered, despite the piece otherwise being thorough about enforcement mechanisms (hooks, permission gates).
- The Ralph Loop and generator/evaluator patterns are described at the level of "this pattern exists and works," with no discussion of failure modes specific to those patterns (e.g., a Ralph Loop that never converges, or an evaluator that itself hallucinates a false negative).
- The "moving, not shrinking" scaffolding claim, if true, implies no stable end-state for harness engineering — worth flagging as an assumption rather than a proven trend, since it is argued from one model transition (Opus 4.6).

## Applicability

Works: as an orientation checklist for a team building or auditing a coding-agent harness — the working-backwards-from-behaviour method, the ratchet discipline, and the primitive list (filesystem/Git, bash, sandboxes, memory, context-rot defences, hooks, verification splits) are concrete enough to apply directly to an existing agent stack.
Fails or untested: as a source of quantified guidance — none of the specific numbers (60-line AGENTS.md, ten tools) are derived from controlled experiments in this piece, so treat them as reasonable defaults to start from, not targets to hit precisely.
**Relevance to my own work** —
- Fleet (this user's orchestrator) already implements several named primitives here: beads as filesystem/Git-backed durable state, a Ralph-Loop-like re-injection pattern for long tasks, and hooks-shaped fleet task protocol rules (`STATE.md` rewrite, `RESULT.json` before exit) — this article is a useful cross-check list against fleet's own harness design, not new information about how to build one.
- The generator/evaluator split (finalize-synth writing content, finalize-verify checking it, as in this very OsmaniHarness pipeline) is a direct instantiation of the article's own core recommendation — worth noting as a live example of the pattern the article describes.

## What this changes

If the claims hold as stated: the practical takeaway is to treat every agent harness as a living, ratcheting system tied to observed failures rather than a one-time setup, to name a specific behaviour before adding any harness component, and to expect a shift toward configuring Harness-as-a-Service runtimes rather than hand-building loops.
If only partially true (likely, given the lack of quantification): the safe takeaway is narrower — adopt the checklist and the ratchet discipline as organizing habits, but do not treat the specific numbers (60 lines, ten tools, Top 30→Top 5) as targets; measure your own harness's cost/quality/failure rate the way TheHarnessEffect or VerificationHorizon do, rather than assuming Osmani's cited deltas transfer.

## Verdict

**Trial.** The synthesis is genuinely useful as a checklist and vocabulary for harness design — the working-backwards-from-behaviour method and the ratchet discipline are cheap to adopt today. But nearly every specific claim is borrowed and unquantified; treat the piece as a well-organized survey of other people's arguments and evidence, not as a primary source of new data, and go to the underlying sources (or to more rigorously measured papers like TheHarnessEffect and VerificationHorizon) before citing a specific number from it.
