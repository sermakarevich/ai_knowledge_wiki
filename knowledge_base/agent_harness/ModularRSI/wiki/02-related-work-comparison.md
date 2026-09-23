[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Related Work and Comparison of Representative Self-Evolving Frameworks
**In one sentence:** Prior harness-evolution work adapts weights, skills, prompts, or whole harnesses but often relies on benchmark-derived data and treats the harness monolithically, so the authors propose benchmark-disjoint evolution plus ModularRSI's fine-grained modular self-evolution via contrastive trajectory analysis.
## Key points
- Prior work reuses execution experience to adapt model weights (Wang et al., 2026c; Zweiger et al., 2026; Luo et al., 2026b).
- Other prior work accumulates reusable skills or context artifacts, or optimizes prompts and external agent mechanisms through trajectory feedback.
- Some approaches use execution traces to diagnose failures and localize editable components, while recent work directly evolves agent implementations or synthesizes harness code.
- TACO specializes harness evolution to observation compression for terminal agents (Ren et al., 2026).
- A central self-improvement challenge is separating transferable improvements from adaptation to development data, making data selection (source-aware rubrics, shortcut filtering) important.
- Existing evaluations cover repository repair, terminal interaction, and online workflows, with HarnessDev, Aspire, and S3 Gym studying harness evolution, feedback budgets, held-out generalization, and hidden evaluation.
- The chunk states that existing harness-evolution methods often rely on evaluation-benchmark data and treat the harness as a monolithic whole, leaving generalizable fine-grained harness improvement underexplored.
- The proposed response is a benchmark-disjoint evolution dataset plus ModularRSI, which decomposes the harness into functional modules and evolves them via contrastive trajectory analysis.
---
## Table 1: comparison of representative self-evolving frameworks
**Covers:** Table 1 caption plus Sections 2–3.1/3.2 as present in this chunk

The chunk contains only the Table 1 caption, not the table rows:

> "Table 1: Comparison of representative self-evolving agent and harness frameworks. Do Not Use Benchmark Data indicates whether benchmark instances, trajectories, or benchmark-derived rewards are excluded from harness evolution."

No per-method table entries or numbers are present in the chunk body, so they are not reproduced here.

## Prior work on experience-driven improvement
**Covers:** Section 2 text preceding Section 2.2

Per the chunk, prior work uses execution experience to:
- adapt model weights (Wang et al., 2026c; Zweiger et al., 2026; Luo et al., 2026b);
- accumulate reusable skills or context artifacts (Zhang et al., 2026c; Yan et al., 2026);
- optimize prompts or external agent mechanisms through trajectory feedback (Agrawal et al., 2026; Zhang et al., 2026d; Fan et al., 2026);
- use execution traces to diagnose failures and localize editable components (Lin et al., 2026; Chen et al., 2026a);
- directly evolve agent implementations or synthesize harness code (Zhang et al., 2026b; Lou et al., 2026a; Lee et al., 2026).

Verbatim note on TACO:

> "TACO further specializes harness evolution to observation compression for terminal agents (Ren et al., 2026)."

## Generalization in self-improvement
**Covers:** Section 2.2

Key claims stated in the chunk:
- "A central challenge in self-improvement is distinguishing transferable improvements from adaptation to the development data."
- "Data selection therefore matters: source-aware rubrics and shortcut filtering help ensure that learning signals reflect the intended capability (Wang et al., 2026a; Zhang et al., 2026e)."
- Existing evaluations cover repository repair, terminal interaction, and online workflows (Deng et al., 2025; Merrill et al., 2026a; Zhang et al., 2026f).
- HarnessDev and broader studies examine harness evolution, feedback budgets, and held-out generalization (Wu et al., 2026b; Wang et al., 2026b).
- Aspire studies weight and harness evolution under hidden evaluation (Wu et al., 2026c).
- S3 Gym separates self-testing, self-judging, and improvement through history, memory, or parameter updates (Shi et al., 2026).
- Gap statement (verbatim in substance): "Despite these advances, existing harness-evolution methods often rely on data drawn from evaluation benchmarks or treat the harness as a monolithic whole, leaving broadly generalizable, fine-grained harness improvement underexplored."
- Response: "To address these limitations, we construct a benchmark-disjoint evolution dataset and propose ModularRSI, which decomposes the harness into functional modules and performs self-evolution through contrastive trajectory analysis."

## Method preview included in this chunk: credit assignment and ModularRSI overview
**Covers:** Section 3 through Section 3.2 as present in this chunk

- Stated problem: "Existing harness self-evolution methods face a fundamental credit-assignment problem: task-level rewards indicate whether an execution succeeds or fails, but provide limited guidance on which harness mechanisms are responsible and how they should be improved."
- ModularRSI response: decompose behavioral components into independently evolvable modules and use contrastive trajectory analysis to turn task-level outcomes into localized function-level evolution signals.
- Three stages named in the chunk: (i) Contrastive Trajectory Sampling and Analysis; (ii) Module-wise Harness Evolution; (iii) Validation Gates (program checks, generalization-oriented diff review, execution validation).
- Five functional modules named: Agent Loop; Observation Management; Tool Use; Context Management; Task Completion Detection.
- Initial harness named in the chunk: Terminus-2 from Harbor (Merrill et al., 2026b), reorganized into these five modules as the shared starting point.
