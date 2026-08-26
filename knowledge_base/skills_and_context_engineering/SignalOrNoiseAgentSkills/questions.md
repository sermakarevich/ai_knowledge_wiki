---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Signal or Noise? A Benchmark Study of Agent Skills in Web Development

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. What is the range of the mean ∆Pass@2 (target Skill vs no Skill) across the four models tested, and what direction is it in?

> [!tip]- Answer
> All four models show a **negative** mean ∆Pass@2, ranging from −1.3 pp (GPT-5.1) to −4.2 pp (Claude Sonnet 4), with Qwen3 Coder at −2.3 pp and DeepSeek-V4-flash at −2.0 pp. Token cost rises 72–394% at the same time, so injection is both less reliable and more expensive on average. See [[wiki/01-introduction-and-benchmark-design|Introduction and Benchmark Design]].

### Q2. What does the C2 (length-matched irrelevant Skill) condition let the researchers separate, and why couldn't C1 vs C0 alone do this?

> [!tip]- Answer
> C2 injects an irrelevant Skill of matched byte length, letting the researchers split the C1−C0 gross effect into a length artifact (C2−C0) and a content effect (C1−C2). C1 vs C0 alone conflates "the prompt got longer" with "the specific content was good or bad" — a model could get worse purely because any equally long text distracts it, which C1 vs C0 cannot distinguish from genuine content harm. See [[wiki/01-introduction-and-benchmark-design|Introduction and Benchmark Design]].

### Q3. Why does Skill-induced degradation concentrate on easy tasks rather than hard ones, and what mechanism does the paper propose?

> [!tip]- Answer
> The proposed mechanism is "retry lock-in": on easy early tasks, models usually recover from a first-attempt mistake by varying a superficial structural choice (e.g. relabeling a button) on the second attempt. An injected Skill that prescribes that exact structural choice removes this self-repair flexibility — if the prescribed choice still collides with the test (as in the zustand × react-expert trace, Appendix A), the model repeats the same mistake on retry and the task chain terminates. Hard tasks aren't dominated by this simple retry dynamic, so the effect doesn't show up there. See [[wiki/02-results-and-mechanisms|Results and Mechanisms]].

### Q4. Two pairs of models show opposite root causes for the same average performance drop. Name the two mechanisms and which models exhibit each.

> [!tip]- Answer
> **Length distraction** (Claude Sonnet 4 and Qwen3 Coder): an equally-long irrelevant Skill reproduces most of the loss, so the harm is mostly about prompt length, not content. **Content misalignment** (GPT-5.1 and DeepSeek-V4-flash): length alone is neutral, but the specific target Skill content still lowers Pass@2 by 1.1–1.4 pp. See [[wiki/02-results-and-mechanisms|Results and Mechanisms]].

### Q5. In the C3 slice ablation, which SKILL.md component is the only one with a statistically reliable positive effect, and which component is both the most expensive and the most model-dependent?

> [!tip]- Answer
> Anti-pattern ("don't") rules (Rn) are the only slice with a directionally reliable effect (Wilcoxon p=0.008, +3.1 pp pooled). Example code (X) is null on average (−0.7 pp pooled) yet costs ~22.7% of the SKILL.md token budget, and it is highly model-dependent — it helps DeepSeek (+8.3 pp) and Qwen (+3.7 pp) but hurts Sonnet (−15.3 pp), the strongest model in the panel. See [[wiki/02-results-and-mechanisms|Results and Mechanisms]].

### Q6. What practical routing heuristic does the paper recommend based on the finding that Skill harm concentrates on easy, early-chain tasks?

> [!tip]- Answer
> Rather than attaching a Skill before any task begins (the common practice), the paper recommends skipping the Skill on early tasks and injecting it only once error rates rise as the task chain progresses — evaluating and deploying Skills by chain position, not just by tech stack. See [[wiki/03-implications-and-conclusion|Implications and Conclusion]].

### Q7. On the lowdb × database-optimizer pair, describe the cross-model outcome and explain why it undermines the idea of a single marketplace ranking for a Skill.

> [!tip]- Answer
> The identical Skill content produces a +33 pp gain on Sonnet 4, a −22 pp loss on both DeepSeek and Qwen, and roughly no change on GPT-5.1 — a 55 pp spread on one pair, not explained by baseline task difficulty (DeepSeek had the strongest C0 baseline yet dropped the most). Since per-pair effects are nearly uncorrelated across models generally (Pearson |r| ≤ 0.12), a single "this Skill is good" rating validated on one model gives essentially no signal about whether it should be deployed with a different model. See [[wiki/04-appendices-worked-examples|Appendices: Worked Examples and Protocol Detail]].

### Q8. The paper's own Limitations section notes that seed spread across Sonnet's three replicates is "comparable to the headline effect size." What does this mean for how confidently a reader should treat any single (Skill, project) pair's reported ∆Pass@2, and is this a weakness the authors disclose or one a critical reader must infer?

> [!tip]- Answer
> The 4.4 pp (C0) / 3.6 pp (C1) spread across just three random seeds is roughly the same magnitude as the paper's headline model-level effects (−1.3 to −4.2 pp), meaning a single pair-level ∆Pass@2 estimate could easily be noise rather than signal at N=3 seeds — even though the aggregated 117-pair, N=3 model-level means are described as stable. This is a limitation the authors explicitly disclose themselves in the paper's own Limitations section, not one a reader must infer — but it is still a caution readers should weigh before treating any individual reported pair effect (e.g. the 55 pp lowdb swing) as fully precise. See [[critical_thinking|Critical Analysis]] and [[wiki/03-implications-and-conclusion|Implications and Conclusion]].
