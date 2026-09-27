> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Motivation: Why Performance-Modeling Software Rots, and the Regeneration Answer

**In one sentence:** ML performance-modeling frameworks decay because model architectures and hardware churn invalidates their abstractions from both directions, while incremental patching (by humans or context-starved agents) compounds technical debt — so SMART makes natural-language design docs the durable artifact and regenerates all code from scratch on every version update.

## Key points

- Performance-modeling frameworks sit between the two fastest-moving parts of the stack (model architectures above, accelerators/interconnects below) and absorb churn from both sides, e.g. the once-safe assumption "every transformer layer looks the same" is now false under mixture-of-experts routing, latent attention, and heterogeneous inference phases.
- Failure mode 1, incremental generation debt: with spec St at time t and generator G, greenfield builds Ct = G(St) but practice computes Ct+1 = G(St+1, Ct); the debt Dt+1 = G(St+1, Ct) - G(St+1) (Equation 1) compounds because humans find deleting all their code mentally hard and time-consuming.
- Failure mode 2, context-window myopia: agents cannot fit a mature codebase in one prompt, so developers feed fragmented snippets; the agent misses global invariants and cross-module dependencies and produces locally plausible but globally sub-optimal code that degrades structural coherence over time.
- The SMART response: the main branch holds almost no code — only a DAG of self-contained natural-language design docs; coding subagents regenerate the implementation from the docs alone on every version update, and every human change is a natural-language doc edit (self-documenting by construction).
- Figure 1 workflow: design-doc DAG (checked into master) → subagents regenerate the library in topological order (one sub-agent per doc) → symbolic cost model build product → validation (reference-model reconciliation, parameter guards, unit tests) → repair loop; humans only ever edit docs.
- Because Ct = G(St) is recomputed from scratch on a regular cadence, Equation (1) debt is driven to zero by construction, and vague intent surfaces early since a guess must be written into a doc to survive.

---

## The churn problem in detail

The paper opens by characterizing ML performance modeling as "a uniquely hostile terrain for long-lived software." The mechanism is specific: a performance model must mirror both the workload (model architecture) and the machine (accelerator, memory hierarchy, interconnect). Both change fast. An abstraction that seemed reasonable a year ago — every transformer layer looks the same — breaks simultaneously from above (MoE routing makes layers heterogeneous; MLA changes the attention cost shape; prefill vs. decode splits inference into two regimes) and from below (new TPU generations, new interconnect topologies). Each change arrives as a refactoring or hack layered onto an aging framework.

## Two compounding failure modes

**1. Incremental generation debt (predates AI).** Formalized with Equation (1): Dt+1 = G(St+1, Ct) - G(St+1). The "distance" is between the patched system and the system that would have been built from the current spec alone. The paper stresses the psychological root: starting over is mentally challenging for humans, so debt is in practice much larger than zero and compromises compound with every spec revision.

**2. Context-window myopia (AI-era).** Finite context windows force developers to feed agents fragmented, localized snippets when requesting revisions. Missing global invariants, cross-module dependencies, and broader architectural intent, the agent generates code that is locally plausible but globally sub-optimal; piecemeal context-blind updates degrade structural coherence over time.

## The regeneration workflow (Figure 1)

The answer to both failure modes is one workflow with a strict division of labor:

- **Humans edit:** natural language only, in the doc files of the design-doc DAG checked into master.
- **Agents do:** agentic regeneration — one sub-agent per doc, executed in topological order — producing the generated library (the symbolic cost model build product).
- **Gate:** validation via reference-model reconciliation, parameter guards, and unit tests, with a repair path back into regeneration before the new build replaces the previous one.

Section pointers: how docs must be written to make this reliable is Section 2 (see [[wiki/02-design-docs-as-source-of-truth|Design Docs as Source of Truth]]); how the modeled system is factored so docs stay stable under churn is Section 3 (see [[wiki/03-symbolic-ir-and-builder-dsl|Symbolic IR and Builder DSL]] and [[wiki/04-rollup-modes-validation-conclusion|Roll-up Modes and Validation]]).

**Covers:** Abstract, Section 1 (Introduction), Figure 1, Equation (1).
