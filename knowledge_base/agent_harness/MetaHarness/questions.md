---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Meta-Harness

Answer from memory before opening any answer. Run sessions with `kb show summary/quiz`.

### Q1. Why does the paper claim that prior text optimizers (OPRO, TextGrad, AlphaEvolve, GEPA, Feedback Descent, TTT-Discover) are poorly matched to harness engineering, specifically?

> [!tip]- Answer
> They compress feedback too aggressively for a task where it matters: some condition only on the current candidate, some rely mainly on scalar scores, and others restrict feedback to short templates or LLM-generated summaries. Harnesses act over long horizons — an early design choice can cause a failure many steps later — and compressed feedback strips out the information needed to trace that failure back to its cause. Quantitatively, these optimizers work with only 100–30,000 tokens of context per step, vs. up to 10,000,000 tokens Meta-Harness can produce per evaluation. See [[wiki/01-motivation-and-related-work|Motivation and Related Work]].

### Q2. In the Meta-Harness outer loop (Algorithm 1), what decides which prior harness a new candidate is based on, and why does the paper consider this a deliberate design choice rather than an oversight?

> [!tip]- Answer
> Nothing decides it explicitly — there is no parent-selection rule and no predefined mutation operator. The proposer can inspect *any* prior harness and its execution trace and choose anything from a small tweak to a full rewrite. The paper frames "starting from a strong prior harness" as an emergent strategy the proposer adopts on its own, not a hard-coded mechanism — leaving diagnosis and edit decisions entirely to the coding agent lets the system improve automatically as coding agents get more capable. See [[wiki/02-method|The Meta-Harness Method]].

### Q3. On text classification, the "proposer-interface ablation" tested giving the proposer only scores, only scores+summary, or the full raw-trace interface. What did this ablation isolate, and what was the result?

> [!tip]- Answer
> It isolated whether raw execution traces (vs. compressed scores/summaries) are actually the source of Meta-Harness's advantage. Scores-only reached 34.6 median / 41.3 best accuracy; scores+summary reached 34.9/38.7 (summaries did not help, and even slightly hurt the best case); the full interface with raw traces reached 50.0 median / 56.7 best — and its *median* candidate beat either ablation's *best* candidate. This shows raw trace access, not just more search iterations, is the key ingredient. See [[wiki/03-classification-and-reasoning-experiments|Classification and Reasoning Experiments]].

### Q4. On TerminalBench-2, Meta-Harness ranked #2 on Claude Opus 4.6 (behind ForgeCode at 81.8%) but #1 on Claude Haiku 4.5. What does the paper say about the ForgeCode result, and why might the gain be larger on the weaker model?

> [!tip]- Answer
> The authors state they could not reproduce ForgeCode's 81.8% result from its publicly available code alone, suggesting its leaderboard score depends on components beyond the published repository — implying the "true" #1 comparison is uncertain. The paper doesn't give a formal explanation for the larger Haiku gain, but the general pattern (discovered harnesses helping more on weaker models) is consistent with the harness compensating for capability gaps that a stronger model already covers on its own. See [[wiki/04-coding-experiments-and-discussion|Agentic Coding Experiments and Discussion]].

### Q5. Describe the TerminalBench-2 search trajectory case study in Appendix A: what confound did the proposer identify by iteration 3, and how did it verify that diagnosis?

> [!tip]- Answer
> Iterations 1 and 2 each bundled a plausible structural bugfix together with a prompt-template rewrite, and both regressed sharply from the 64.4% Terminus-KIRA baseline — two different structural changes, one shared prompt intervention. By iteration 3 the proposer inferred the common factor (the cleanup-heavy prompt rewrite) was the real cause, reverted the prompt, and tested only the structural fix (marker stripping + loop breaker) in isolation. That candidate still underperformed slightly (63.3%, −1.1pp) but lost far less than the earlier versions, supporting the confound diagnosis — the authors call this "the key causal step in the trajectory." See [[wiki/05-appendix-case-studies|Appendix: Case Studies and Discovered Harnesses]].

### Q6. What is the "Draft Verification" classification harness, and why does its second retrieval step matter more than a standard nearest-neighbor lookup?

> [!tip]- Answer
> It's a two-call procedure: first, retrieve 5 nearest labeled examples and produce a draft label D; then retrieve 5 "confirmers" (same label as D) and 5 "challengers" (different label) — conditioned on D, not just the raw query — and use those to keep or revise the draft. Because the second retrieval depends on both the query *and* the draft prediction, it surfaces counterexamples specifically targeted at the model's current guess, rather than only generic nearby examples — a form of targeted, hypothesis-driven verification a fixed nearest-neighbor lookup wouldn't produce. See [[wiki/05-appendix-case-studies|Appendix: Case Studies and Discovered Harnesses]].

### Q7. Suppose you wanted to apply the Meta-Harness recipe to a new domain, say a customer-support triage agent. Based on the paper's practical implementation tips, what two things would matter most for getting the search loop to actually work, and why?

> [!tip]- Answer
> (1) Writing a good "skill" for the proposer — the primary steering interface — that constrains *what's forbidden and what to produce* (safety-relevant behavior) without constraining *how* the proposer diagnoses problems; iterating on this skill text had a bigger effect than changing iteration count or population size, and the authors recommend a few short 3-5 iteration debug runs to refine it first. (2) Choosing a baseline harness and a search set that is genuinely *hard* for that baseline — if the baseline already saturates the eval, there's little for the search to optimize — kept small enough for roughly 50 full evaluations per run so search stays fast and discriminative. See [[wiki/05-appendix-case-studies|Appendix: Case Studies and Discovered Harnesses]].

### Q8. The paper's TerminalBench-2 evaluation used no held-out split — search and final evaluation ran on the same 89-task benchmark. Given the critical analysis of this paper, is this a serious threat to the coding-agent result, and how did the authors try to mitigate it?

> [!tip]- Answer
> It's a real limitation the authors acknowledge rather than hide: because the benchmark is small and expensive, a separate holdout split would have materially weakened the search signal, so they accepted the overfitting risk and instead relied on manual inspection plus regex-based audits for task-specific string leakage into the evolved harness. This is weaker evidence than the classification and math results, which do use genuine held-out datasets/models (9 unseen datasets, 5 unseen models) and show real transfer. The TerminalBench-2 number should be read as "best harness found for this specific contested benchmark," not proof of clean generalization to arbitrary new coding tasks. See [[critical_thinking|Critical Analysis]] and [[wiki/04-coding-experiments-and-discussion|Agentic Coding Experiments and Discussion]].
