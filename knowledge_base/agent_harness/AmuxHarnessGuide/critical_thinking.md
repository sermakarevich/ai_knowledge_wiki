> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Harness Engineering: The Complete Guide

## Claims vs. evidence

(1) "Harness swaps move scores far more than model swaps" — **moderate**. The two headline numbers (SWE-bench: harness ±22 points vs. model ±1 point; LangChain +13.7 points on Terminal Bench 2.0 with the same model) are cited as facts but the guide gives no link to the underlying benchmark run, no methodology, and no confidence interval — they read as third-hand claims repackaged from other harness-engineering writing (the same Terminal Bench figure appears in Osmani's independent piece, which is reassuring corroboration, but the guide itself does not show its work).

(2) "Guides ~70% compliance, sensors ~100% enforcement" — **weak**. These two round numbers recur throughout every section as if measured, but no experiment, dataset, or citation backs either figure. They function as a rhetorical anchor (memorable, precise-sounding) rather than a reported result — treat them as illustrative approximations, not measured constants.

(3) "Atlan pipelines: 10–31% bare-schema vs 94–99% governed-context accuracy" and "82% of IT leaders say prompting is insufficient" — **unverifiable from this source**. Both are named without a link, sample size, or methodology in the extracted text; they may trace to real Atlan/survey publications, but the guide does not make that traceable, so they should be treated as pointers to check independently, not settled evidence.

(4) "amux implements the complete harness architecture" — **self-interested, not independently verified**. The source is amux's own marketing guide (amux.io), and Section "How does amux implement harness engineering?" directly maps every framework component (guides, sensors, orchestration, self-healing) onto amux's own product features. The scale claims attributed to others (OpenAI Symphony 1M LOC/day, Stripe Minions 1,300 PRs/week) are real-sounding case studies but are used here to justify buying into the vendor's specific orchestration design, not just the general principle that orchestration helps at scale.

## Genuinely new vs. repackaged

Almost nothing here is original to this guide. The core formula (Agent = Model + Harness), the guides/sensors cybernetics framing (credited to Böckeler), and the ratchet principle (credited to Osmani) are explicitly attributed to other authors within the guide's own text — this is a synthesis/vocabulary-standardization piece, not a novel contribution. Its actual original content is narrow: the specific six failure-to-fix routing table, the "lean CLAUDE.md" numeric thresholds (500 lines, ~200 tokens for skills), and the case for amux as the reference multi-agent implementation of the same ideas. The value is compilation and productization, not new evidence.

## Weaknesses and blind spots

- Vendor content presented as neutral guidance: the guide's own FAQ ("How does amux implement harness engineering?", "Do I need amux?") shows this is marketing collateral for amux's orchestration product, wrapped in general-purpose framework language. Readers should discount the framing wherever amux is the example, not just where it's explicitly named.
- No falsification anywhere: every cited number moves in the direction the guide's thesis predicts; there is no discussion of when harness investment fails, plateaus, or is not worth the engineering cost (contrast with papers like Self-Refine or The Harness Effect, which report null/negative results in some conditions).
- Numbers without provenance: the ~70%/~100% guide-vs-sensor compliance figures and the Atlan/IT-leader survey stats are repeated as load-bearing evidence across all three wiki sections but none is sourced to a checkable study within the extracted text.
- Survivorship in the scale examples: OpenAI's 3-engineers/1,500-PRs case study and the 1M-LOC/day, 1,300-PRs/week figures are impressive outliers presented without failure-rate, rework-rate, or defect-rate context — a reader cannot tell whether "PRs shipped" corresponds to durable, correct software.

## Applicability

Works: as a vocabulary and mental model for organizing agent-reliability engineering work — the guides-vs-sensors distinction and the ratchet principle are genuinely useful framing tools regardless of their source, and the six failure-to-fix routing table is a concrete, applicable checklist for any team building CLAUDE.md/AGENTS.md-style harnesses today.
Fails or untested: as a source of quantitative benchmarks to cite in a decision memo — the headline numbers lack the provenance needed to defend them under scrutiny, and the amux-specific claims should be treated as a vendor's self-assessment until verified against independent multi-agent orchestration comparisons (e.g. [[TheHarnessEffect/summary]]'s controlled harness-swap study is a stronger evidentiary source for the same underlying thesis).
**Relevance to my work** —
- Use the guides/sensors framing and the six-routing table as a design checklist for CLAUDE.md and hooks, but verify the compliance/enforcement percentages against my own team's observed behavior rather than citing them as fixed constants.
- Before adopting amux or any specific orchestration tool because "this guide says it implements harness engineering completely," treat that as a vendor claim requiring the same evaluation rigor as any other tool purchase — cross-check against papers with controlled comparisons.

## What this changes

If the claims hold as stated: the guides/sensors/ratchet vocabulary is a useful shared language for structuring agent-reliability work, and the specific numeric thresholds (500-line CLAUDE.md, ~200-token skill previews) are reasonable starting defaults for teams with no better data of their own.
If only partially true (the likely case, given the unsourced statistics and vendor framing): the safe takeaway is to adopt the conceptual vocabulary and the ratchet discipline (both corroborated independently by Osmani's article) while treating every specific number and every amux-as-reference-implementation claim as needing independent verification before being repeated as fact.

## Verdict

A useful synthesis and vocabulary standardization of ideas developed elsewhere (Böckeler's guides/sensors, Osmani's ratchet), packaged as marketing content for amux's orchestration product. The framework concepts are sound and corroborated by an independent source ([[OsmaniHarness/summary]]), but nearly every specific number in this guide is unsourced within the extracted text, and the multi-agent-scaling section doubles as a product pitch. **Trial** — adopt the vocabulary and the failure-to-fix routing checklist, but do not cite this guide's statistics or its amux endorsement as independent evidence; go to [[TheHarnessEffect/summary]] or [[OsmaniHarness/summary]] for claims that carry their own methodology.
