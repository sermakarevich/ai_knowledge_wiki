> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Table 4: Recovering the reasoning gap
**In one sentence:** A no-think policy plus the distilled skill recovers most or all of the no-think→think accuracy gap with zero reasoning tokens, and failure-rich no-think rollouts alone suffice as the distillation corpus.
## Key points
- On ALFWorld, no-think + CASD skill reaches 83.3 vs 71.3±1.2 for think mode, recovering >100% of the no-think→think gap from a 56.7 baseline.
- On τ-2 retail, no-think + skill reaches 40.0 vs 35.0±6.6 for think mode, recovering >100% of the gap from a 32.5 baseline.
- On τ-2 telecom, no-think + skill reaches 39.2 vs 45.0±2.5 for think mode, recovering 78% of the gap from a 19.2 baseline.
- On SSB-Verified, no-think + skill reaches 51.3 vs 61.3±1.2 for think mode, recovering 55% of the gap from a 39.3 baseline.
- Per-episode output stays at or below the no-think budget (0.6–0.8k tokens) with zero reasoning tokens, where thinking costs 2.9–4.5× more (think → skill: 3.7k→0.8k, 1.6k→0.6k, 2.1k→0.6k, 3.3k→0.8k).
- Distilling from think rollouts vs no-think rollouts lands within a few points with no consistent winner (ALFWorld 81.3 vs 78.7; retail 45.8 vs 40.8; telecom 32.5 vs 33.3; SSB reversed, 46.0 vs 56.0), so expensive reasoning traces are optional corpus enrichment needed at most once at corpus-construction time.
- Residual gaps on telecom and SSB suggest a portion of thinking — instance-specific deduction rather than reusable policy — that no static prompt recovers; closing it is future work.
- Limits: skill-to-skill variance (3 independently distilled skills) vs seed variance of a single prompt, one target model (GPT-5.4-mini no-think) and one coding agent (Claude Sonnet 5 / Claude Code) with untested distiller-capability sensitivity, and CASD inherits the corpus so it cannot discover behaviors absent from logged rollouts.
---
## Table 4: no-think + skill vs think (GPT-5.4-mini)
"Rec." = fraction of the no-think→think accuracy gap recovered by the skill; tok = mean output tokens per episode (think → skill).

| Benchmark | no-think | +CASD skill | think | Rec. | tok (↓) |
|---|---|---|---|---|---|
| ALFWorld | 56.7 | 83.3 | 71.3±1.2 | >100% | 3.7k→0.8k |
| τ-2 retail | 32.5 | 40.0 | 35.0±6.6 | >100% | 1.6k→0.6k |
| τ-2 telecom | 19.2 | 39.2 | 45.0±2.5 | 78% | 2.1k→0.6k |
| SSB-Verified | 39.3 | 51.3 | 61.3±1.2 | 55% | 3.3k→0.8k |

The chunk states the skill "ceeds the think mode outright (83.3 vs. 71.3; 40.0 vs. 35.0); on telecom and SSB it recovers 78% and 55% of the no-think→think gap" while "emitting zero reasoning tokens: per-episode output stays at or below the no-think budget (0.6–0.8k tokens), where thinking costs 2.9–4.5× more."
## Interpretation
- Much of what reasoning re-derives episode after episode — "which diagnostic to run next, when a lookup argument is unjustified, when not to give up" — is policy-like and "can be crystallized once, offline, into explicit rules."
- "The distillation corpus need not contain thinking": think-distilled vs no-think-distilled skills land "within a few points of each other with no consistent winner (e.g., ALFWorld 81.3 think-distilled vs. 78.7 no-think-distilled; retail 45.8 vs. 40.8; telecom 32.5 vs. 33.3; SSB reversed, 46.0 vs. 56.0)."
- "Failure-rich no-think rollouts alone carry enough signal; expensive reasoning traces are optional corpus enrichment, needed at most once at corpus-construction time."
## Limitations
- "Our SD for CASD measures skill-to-skill variance (3 independently distilled skills, one evaluation each) while baselines report seed variance of a single prompt; the quantities are close but not identical."
- "All results use one target model (GPT-5.4-mini no-think) and one coding agent (Claude Sonnet 5/Claude Code); the recipe's sensitivity to distiller capability is untested."
- "CASD inherits the corpus: it cannot discover behaviors absent from the logged rollouts and very small or failure-free corpora may leave nothing to distill."
## Conclusion
- "A stock coding agent, pointed at a directory of frozen rollouts with a one-paragraph instruction, is a strong prompt optimizer: it beats state-of-the-art reflective search under matched data access on 3 of 4 agentic benchmarks, never touches the environment, and costs about $1.60 per prompt."
- "The key difference is reflection scope—executing analysis code over the entire rollout corpus instead of relying on minibatch reflection and validation gating."
- "As coding agents improve, offline corpus-scale reflection may become the default first step of prompt optimization, with search reserved for the final gains when additional interaction is inexpensive."

**Covers:** Table 4 think-vs-skill ablation, Sections 7 (Limitations) and 8 (Conclusion), references tail
