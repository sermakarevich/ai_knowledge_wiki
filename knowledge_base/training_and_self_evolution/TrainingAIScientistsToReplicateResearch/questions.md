---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Training AI Scientists to Replicate Research

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. The paper identifies three specific reasons LLM agents historically fail at paper replication. What are they?

> [!tip]- Answer
> (1) Replication is inherently underspecified — a paper is a lossy compression of the actual research, so details are always missing. (2) Existing agents are trained on well-specified, closed-ended problems, while replication needs open-ended exploration. (3) There's no definite, hill-climbable reward for a general replication task, so approaches like AlphaEvolve/autoresearch that need a scalar signal to climb don't apply directly. See [[wiki/01-introduction-motivation|Introduction & Motivation]].

### Q2. Why does the paper choose an LLM-judged reward over a verifiable benchmark-derived reward for training an "AI Scientist"?

> [!tip]- Answer
> Verifiable-benchmark rewards work well when hill-climbing produces genuinely novel insight (e.g. FunSearch, AlphaEvolve), but discoveries made against a fixed benchmark tend to be adaptations rather than exaptations (they don't generalize), there's a ceiling on attainable insight, and building enough benchmarks by hand doesn't scale. Qualitative LLM judgement of full rollouts avoids these limits, at the cost of needing a judge reliable enough to trust. See [[wiki/02-related-work|Related Work]].

### Q3. How does Replica automatically turn a paper into a task, and roughly how many tasks does the whole corpus yield?

> [!tip]- Answer
> A three-stage Gemini 2.5 Pro vision-language pipeline scans the paper, localizes a results figure's bounding box (with an LLM-verifier repair loop), then irreversibly redacts it — each redacted figure becomes one task. 100 papers (1990–2026) yield 310 tasks total: 242 training tasks from ML papers and 68 held-out test tasks from AI-for-science papers. See [[wiki/03-methods-replica-and-faraday|Methods: Replica & Faraday]].

### Q4. What keeps the rubric judge from just rewarding an agent that reproduces the exact pixels of the redacted figure rather than the underlying scientific claim?

> [!tip]- Answer
> Both the rubric-generating model (Claude Opus 4.7) and the policy being trained are kept blind to the "gold plot" when the rubric is written and when the agent acts — so the rubric is written to capture the paper's claim (visual match, claim support, implementation fidelity, compute-budget use, scientific integrity), not the specific pixels of one image, which prevents both rubric-authoring and the policy from gaming figure-level details. See [[wiki/03-methods-replica-and-faraday|Methods: Replica & Faraday]].

### Q5. How much better does the human-validated rubric judge agree with itself (across two independent draws) and with human raters, compared to a generic constant-prompt baseline judge?

> [!tip]- Answer
> Two rubric-judge draws agree at Kendall τ 0.66 vs. 0.46 for the baseline judge (and vs. 0.30 for two humans agreeing with each other); against humans, the rubric judge scores 0.19 vs. 0.15 for the baseline. Three rubric-judge samples match the noise-reduction of eight baseline-judge samples, making it a much cheaper, less noisy RL reward. See [[wiki/04-results|Results]].

### Q6. On what fraction of in-distribution (ML) and held-out (AI-for-science) tasks does Faraday beat both Claude Opus 4.8 and GPT-5.5/Codex, and what evidence rules out "the gap is just a prompting difference"?

> [!tip]- Answer
> Faraday wins 73% of in-distribution ML tasks and 60% of held-out AI-for-science tasks. The authors ran 24 generations of automatic prompt optimization on Codex's prompt and it did not meaningfully close the gap to Faraday, showing the advantage comes from the RL-trained weights, not a better prompt. See [[wiki/04-results|Results]].

### Q7. What is the "Coding Agent as a Tool" (CAT) paradigm, and what does the coder-tool ablation in the appendix suggest about why it works?

> [!tip]- Answer
> CAT means a smaller trained "researcher" model (Faraday) directs a much larger frontier coding agent (about two orders of magnitude bigger) by delegating implementation work to it as a tool, rather than doing the coding itself. The ablation ("Faraday Coder" — Qwen3.6-27B trained from scratch without the coding-agent tool) collapses in training after ~300 steps and stays weaker even with double the time budget, suggesting the ceiling on what a trained "researcher" role can reach exceeds what the same base model can reach if it also has to do all the coding itself. See [[wiki/06-appendix-task-and-judge-design|Appendix: Task & Judge Design]].

### Q8. What happens to training stability when turn-level credit assignment is removed from GRPO, and why does the paper consider this important for long-horizon, non-verifiable RL specifically?

> [!tip]- Answer
> Removing turn-level credit assignment from a late checkpoint causes rapid collapse: mean reward drops after about 50 steps, token entropy spikes and then collapses, and the Jensen–Shannon divergence between the generation and policy distributions grows by two orders of magnitude. This matters because long rollouts with only a single end-of-episode reward give very sparse, high-variance training signal; distributing credit across turns (weighted toward turns that delegate to the coding agent) keeps the reward informative enough to train on stably. See [[wiki/06-appendix-task-and-judge-design|Appendix: Task & Judge Design]].

### Q9. In the human agent-comparison study, how often did human experts prefer Faraday over Claude and over Codex, and under what selection condition were those rollouts chosen?

> [!tip]- Answer
> Humans preferred Faraday over Claude in 80% of rankings and over Codex in 88%, and preferred Faraday above both in 71% (p < 0.01, 41 rollouts, 11 participants). Crucially, these rollouts were pre-selected as ones where the rubric judge had already deemed Faraday "clearly ahead" — so this study validates the judge's calls on its most confident cases, not a random or adversarial sample of all rollouts. See [[wiki/06-appendix-task-and-judge-design|Appendix: Task & Judge Design]].

### Q10. What does the "Authenticity" rule in the agent's task prompt explicitly forbid, and what is still allowed as an honest fallback when full-scale replication isn't feasible?

> [!tip]- Answer
> It forbids simulating or fabricating experiments — hard-coding expected values or mocking runs scores 0. What's allowed instead is a clearly-documented, scaled-down version (smaller model, fewer training steps, fewer seeds) as long as it's disclosed; the optimized Codex prompt goes further, requiring at minimum the "smallest faithful real slice" (e.g., one model × one setting actually run) before any proxy numbers are permitted. See [[wiki/07-appendix-example-tasks-and-rubrics|Appendix: Example Tasks & Rubrics]].

### Q11. Faraday's held-out test split (AI-for-science papers) and its full-scale generalization tasks are both drawn from the same task-generation pipeline as its training data. Why does this matter when evaluating the "beats Claude Opus 4.8 and GPT-5.5" headline claim?

> [!tip]- Answer
> "Held-out" here means a different topical slice of papers processed by the identical redact-a-figure pipeline and graded by the identical rubric-judge design — not an independently constructed benchmark. This is a meaningfully weaker generalization test than transfer to a benchmark built by someone else with different task-construction assumptions, so the headline result is best read as "generalizes across topics within Replica's own construct," not as an unqualified claim about all scientific replication or research ability. See [[critical_thinking|Critical Analysis]].

### Q12. The paper reports Faraday winning 19 of 20 "imagined replication" tasks against Codex. Why does the paper itself flag this result as weaker evidence than the main replication results?

> [!tip]- Answer
> The rubric judge used to score these counterfactual (never-published) figure variants was never separately validated against human rankings the way it was for the main replication tasks — so while the score gap is large, there's no independent check that the judge's ordering on genuinely novel/counterfactual claims tracks human judgement as well as it does on real replication. See [[wiki/05-discussion|Discussion]].
