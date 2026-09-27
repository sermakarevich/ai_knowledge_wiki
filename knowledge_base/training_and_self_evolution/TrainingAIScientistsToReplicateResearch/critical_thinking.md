> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Training AI Scientists to Replicate Research

## Claims vs. evidence

**Claim 1: "Faraday surpasses Claude Opus 4.8 and GPT-5.5 on replication tasks."**
Suggestive-to-strong within the paper's own construct, weaker as a general claim. The 73%/60% win rates are real and backed by a judge validated against 117 human PhD-rater rankings, plus a separate targeted human study (41 rollouts) confirming the judge's calls 80-88% of the time. But "held-out" only means a different topical slice (AI-for-science vs. ML papers) run through the *same* auto-generation pipeline and graded by the *same* rubric-judge design — not an independently constructed benchmark. A model can generalize well within one construct's assumptions while still overfitting to quirks of how that construct builds tasks (e.g. the specific redaction style, the specific rubric dimensions Claude 4.7 tends to write). This is a real result, but the generalization claim is narrower than the headline suggests.

**Claim 2: "The rubric judge is a reliable, low-noise reward signal."**
Well-supported. The comparison against a generic constant-prompt baseline judge is a real ablation (same underlying judge model, different prompting strategy), and the metrics (Kendall τ agreement, noise-vs-sample-count curves) are the right ones to check. The gap (0.66 vs 0.46 self-agreement; matching baseline's 8-sample noise floor with 3 samples) is large enough to be convincing, not a marginal improvement dressed up.

**Claim 3: "Faraday exhibits more scientific rigor, not just higher scores."**
Suggestive. The qualitative examples (faithful mechanism implementation, honest scaled-down experiments, avoiding shortcuts) and the sub-dimension breakdown (Figure C.2: Faraday ahead on experimental depth/claim reproduction, tied on integrity) support this, but "avoids shortcuts that would flatter its own result" is judged by the same rubric-judge family that graded the main task — a judge could plausibly reward surface behaviors that correlate with genuine rigor without perfectly discriminating rigor from rigor-flavored behavior. The four real-author interviews (Section 5) are a nice independent corroboration but are a sample of 4 papers' authors, not a systematic audit.

**Claim 4: "Training collapses without turn-level credit assignment / without the coding-agent tool."**
Strong. These are controlled ablations with clear, large, unambiguous training-dynamics signatures (reward collapse, entropy spikes, JS-divergence blowup) — the kind of result that's hard to fake or over-interpret.

## Genuinely new vs. repackaged

- **Genuinely new:** the specific combination of (a) auto-generated, redaction-based figure-replication tasks at this scale (310 tasks from 100 papers, fully automated pipeline) and (b) a rubric judge validated with a dedicated, well-powered human study (20 raters, 117 rankings) is a real contribution — most prior AI-Scientist/replication papers either hand-build far fewer tasks or skip rigorous judge validation.
- **Repackaged / building on prior work:** the reward-design dichotomy (verifiable benchmark reward vs. LLM-judged reward) is explicitly framed against FunSearch/AlphaEvolve and prior peer-review-style LLM judges (Lu et al. 2024, Weng et al. 2025). GRPO itself is Shao et al. 2024's method; the turn-level credit-assignment extension is the paper's own addition on top of it. The "small model directs large tool" (CAT) idea echoes broader agent-orchestration patterns already common in production agent harnesses, though applying it specifically as an RL-trained skill (rather than a hand-coded orchestration layer) is the paper's angle.

## Weaknesses and blind spots

- **No independently constructed held-out benchmark.** Every evaluation split — train, test, full-scale, counterfactual/imagined — comes from the same task-generation and grading pipeline. A benchmark built by a different team with different assumptions about what "replication" means would be a much stronger generalization test.
- **The "imagined replication" (innovation) result is explicitly under-validated by the authors' own admission** — the judge was never checked against humans specifically for counterfactual/novel claims, yet this result is used to gesture toward Faraday "innovating better," which is a bigger claim than the evidence supports.
- **The judge-vs-human agreement, while better than baseline, is still moderate in absolute terms** (Kendall τ 0.19 with humans). That's an improvement over a weaker judge, not evidence the judge is close to a ceiling of human-level discernment — training against it for many steps risks eventually optimizing into the judge's specific blind spots even if early gains are genuine.
- **Cost and infrastructure are barely discussed.** Running a Kubernetes/Ray/NeMo-RL stack with per-rollout fresh containers, MIG-sliced H200s, and a 5-stage training lineage to step 659 is a heavy, specialized infrastructure investment; the paper doesn't report compute cost, making "how reproducible/replicable is this training recipe itself" an open question (a pointed irony given the paper's subject).
- **Authors acknowledge:** the "tip of the iceberg" framing in the Discussion, and real-author feedback flagging poor simplifications, weak write-ups, and "code slop" in some Faraday rollouts — these are honestly reported, not hidden.
- **Authors are silent on:** failure-mode base rates (how often does Faraday clearly lose, and why), cost-per-rollout of the rubric judge itself (3 samples × a large coding-agent judge is not cheap), and whether the CAT paradigm's advantage would hold if the baseline agents (Claude, Codex) were themselves given an equivalent "plan first, delegate small scoped calls" system prompt rather than a generic one-liner.

## Applicability

This works when you can (a) auto-generate a large number of graded tasks from an existing corpus of documents with embedded "known answers" (here: papers with figures), and (b) afford the infrastructure to run many long, tool-using RL rollouts with a coding-agent-based judge. It would likely fail or not transfer to domains lacking a comparable ground-truth corpus (there's no equivalent of "the original figure" for genuinely novel research), or to teams without serious RL/agent-training infrastructure — this is not a lightweight recipe.

**Relevance to my work** (Sergii's contexts — AI/ML engineering, agentic systems, Elisity data platform):
- **Trial:** the CAT ("small orchestrator directs large tool") pattern is directly applicable to designing internal agent harnesses that direct commercial coding/data assistants rather than trying to replace them.
- **Trial:** the rubric-judge recipe (task-specific rubric generated blind to the answer, judge given full workspace context, multi-sample averaging) is a reusable template for building trainable or even just evaluation-only reward signals for open-ended internal tasks (e.g., data-pipeline debugging, device-classification quality review) where a simple pass/fail check doesn't exist.
- **Watch:** the RL post-training infrastructure (NeMo-RL, Ray, per-rollout containers) is heavyweight and probably overkill unless building an actual RL training loop; for most agentic-engineering work, the judge-design ideas transfer without needing the RL machinery.
- **Ignore:** the specific model choices (Qwen3.6-27B, Codex GPT-5.5) are implementation details tied to when this paper was written, not principles to adopt as-is.

## What this changes

If the claims hold as stated (within their own construct): it becomes more credible that "research taste" — deciding what to investigate, how to scope experiments, when a result is trustworthy — can be trained into a comparatively small model's weights and then reused across different, more powerful tools, rather than needing to be hard-coded into an ever-larger single model or an ever-more-elaborate harness. That's a meaningful architectural signal for anyone building agent systems: it favors investing in a trainable orchestration layer over building an all-in-one frontier model dependency. If the generalization claims turn out to be narrower than advertised (limited to Replica-like task constructions), the main surviving contribution is still the rubric-judge and CAT-architecture recipe, which is useful independent of the specific performance numbers.

## Verdict

This is a serious, methodologically careful piece of work — the human validation of the judge and the battery of ablations (credit assignment, coder-tool, full-scale, tool-swap) are exactly the checks a skeptical reader would ask for, and the authors are honest about caveats where evidence is thinner (imagined-replication judge validity, qualitative failure modes from real authors). The main thing to discount is the headline "surpasses frontier models" framing: it holds up well *within* the paper's own task construct but has not been tested against an independently built benchmark, so treat it as strong evidence for the training recipe and judge design, and only moderate evidence for a general claim about AI research capability. **Verdict: trial** — the rubric-judge and CAT-orchestration ideas are worth prototyping in agentic-engineering work now; the specific performance claims should not be over-cited without noting the construct-validity caveat.
