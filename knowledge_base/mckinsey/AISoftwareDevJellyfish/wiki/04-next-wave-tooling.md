> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The next wave of AI tooling

**In one sentence:** With integrated development environment (IDE) coding assistance largely won, Lau places the next innovation wave in code review and agentic systems spanning the life cycle, with testing as the hardest frontier because full automation requires formalizing intent and redefining correctness — an open question for regulated industries.

## Key points

- Most progress so far sits in IDE-based tools and experiences for individual developers writing code, which Lau treats as the completed first wave rather than the frontier.
- The next wave is code review plus agentic systems that coordinate work across stages of the PDLC, moving assistance from single-developer tasks to multi-stage coordination.
- Testing is singled out as a particularly interesting frontier because quality cannot be fully automated without defining truth, and many legacy systems lack that specification.
- The missing-specification problem is a blocker for full-scale AI transformation: organizations will need new ways to formalize intent, essentially redefining how correctness is expressed.
- Regulated industries sharpen the problem because they must prove independence and accuracy, raising the unresolved question of whether an agent can count as an independent validator — Lau's answer is that we are not there yet.
- Until validators exist, organizations must embed controls earlier in the process rather than relying on end-of-pipe checking.

---

## From IDE assistance to life-cycle coordination

Lau's wave structure mirrors the bottleneck argument: first-wave tools accelerated individual code-writing inside the IDE, which is exactly the local speedup that shifts pressure downstream. Second-wave value therefore lives where the new bottlenecks formed — code review throughput and agentic coordination across PDLC stages.

## Testing and the truth problem

The testing frontier is framed epistemically, not as a tooling gap: automating quality presupposes a definition of truth, and legacy systems frequently lack any specification to check against. Formalizing intent — writing down what the system should do in machine-checkable form — becomes prerequisite infrastructure, which is why Lau calls it a blocker for full-scale transformation rather than an incremental improvement.

## Correctness, independence, and regulated industries

Redefining how correctness is expressed collides with regulatory regimes built around independent human validation. The question "can an agent count as an independent validator" is left explicitly unanswered, and the interim prescription is architectural: embed controls earlier in the process so assurance does not depend on a validator role agents cannot yet fill.

**Covers:** the IDE-first-wave assessment, review and agentic coordination as the second wave, testing as the truth-definition frontier, the correctness-redefinition requirement, the independent-validator question in regulated industries, and the embed-controls-early interim prescription.
