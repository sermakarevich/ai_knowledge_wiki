[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Judge robustness and self-preference
**In one sentence:** The judge's agent ranking is robust — it holds with an out-of-family judge and is not a capability artifact — but same-family judges inflate their own provider's agents by about 0.7/7 without changing the ranking.
## Key points
- Opus-4.8 and GPT-5.5 agree at ρ=0.92, so the ordering is "not a single-provider artifact."
- All four judges recover the verifiable-reward ordering (ρ=0.84–0.94) and agree with one another (ρ=0.90–0.98).
- GPT-5.5 grades ≈0.8/7 lower in absolute level, even though its ranking agrees.
- The ordering is not a capability artifact: as agents on the same τ 2 pool, Opus-4.8 scores 0.82 and GPT-5.5 scores 0.84 versus pool-best Opus-4.6 (t.7) at 0.87, with overlapping 95% CIs.
- The weakest judge-as-agent, GPT-5.4 (0.77), is tied-best as a ranker (ρ=0.94), so ranking ability does not require outclassing the agents.
- The near-equal limit holds for every judge (top-11 ρ=0.25–0.51, all n.s.), confirming "genuine agent near-equality rather than mis-ranking by a weak judge."
- Same-family self-preference is isolated by a scale-invariant diff-in-diff of +0.75/7 for the Opus-4.8 judge inflating Claude agents over GPT-5.5 (Sonnet-4.5 shows +0.67/7 against GPT-5.4), and it "leaves the ranking intact."
- Ranking is stable against judge noise across two reruns: test–retest ICC=0.87 and rank stability ρ=0.92.
---
## Out-of-family judge check
Because "the Anthropic judge and the agents share a provider, 'validity' could reflect self-recognition (Panickssery et al., 2024), so we re-score the grid with an out-of-family judge." Opus-4.8 and GPT-5.5 agree at ρ=0.92; all four judges recover the verifiable-reward ordering (ρ=0.84–0.94) and agree with one another (ρ=0.90–0.98). The ordering is thus "not a single-provider artifact, though GPT-5.5 grades ≈0.8/7 lower."
## Not a capability artifact
"The ordering is also not a capability artifact. Run as agents on the same τ 2 pool, both frontier judges are statistical peers of the strongest agent (Opus-4.8 0.82, GPT-5.5 0.84, vs. pool-best Opus-4.6 (t.7) at 0.87; overlapping 95% CIs); they recover the ordering without outclassing it, while the weakest judge-as-agent (GPT-5.4, 0.77) is tied-best as a ranker (ρ=0.94)." The near-equal limit holds for every judge: "top-11 ρ=0.25–0.51, all n.s.; Appendix F.1", "confirming genuine agent near-equality rather than mis-ranking by a weak judge."
## Same-family self-preference
"The two-provider design also isolates same-family self-preference: the Opus-4.8 judge inflates Claude agents over GPT-5.5 more than non-Claude agents, a scale-invariant diff-in-diff of +0.75/7 (Sonnet-4.5 shows +0.67/7 against GPT-5.4; Appendix F.2), so it reflects self-preference and leaves the ranking intact."
## Stability against judge noise
"Two reruns confirm the ranking is stable against judge noise (test–retest ICC=0.87, rank stability ρ=0.92; Appendix F.3)."
**Covers:** Section 4.3 Judge robustness and self-preference
