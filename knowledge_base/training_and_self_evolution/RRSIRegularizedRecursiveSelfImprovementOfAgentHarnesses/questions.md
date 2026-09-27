---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: RRSI: Regularized Recursive Self-Improvement of Agent Harnesses

### Q1. What is the harness in RRSI, and why is harness-level evolution a practical form of recursive self-improvement?

> [!tip]- Answer
> The harness is everything around the frozen backbone weights: prompts, control flow, tool interfaces, memory, skills, and context management. It decides whether the same model reads the right file, recovers from failures, and writes deliverables, so much agent progress comes from harness engineering. Automating that loop with LLMs that propose and select edits from task feedback creates RSI at the agent-system level, where current-system feedback reshapes subsequent behavior. See [[wiki/01-rrsi-regularized-recursive-self-improvement|RRSI: Regularized Recursive Self-Improvement of Agent Harnesses — Framing and Proposal]].

### Q2. What does Figure 1 show about prior harness-evolution methods versus RRSI on the agentic workspace benchmark?

> [!tip]- Answer
> Prior methods retain little of their evolve-set gain out of distribution, with several finishing below H0, the unevolved initial harness. Their large in-distribution improvements shrink, vanish, or invert on unseen benchmarks, the signature of memorization. RRSI instead generalizes its improvements, trading a smaller evolve-set gain for robust OOD transfer. See [[wiki/01-rrsi-regularized-recursive-self-improvement|RRSI: Regularized Recursive Self-Improvement of Agent Harnesses — Framing and Proposal]].

### Q3. What are the three coupled overfitting behaviors that widen the evolve-to-transfer gap?

> [!tip]- Answer
> The three behaviors are benchmark-specific fitting (encoding task-specific patterns), noise chasing (promoting candidates favored by evaluation noise), and complexity accumulation (adding machinery that lifts evolve scores without improving the mechanism). All three raise evolve-set performance without corresponding unseen-task gains. RRSI regularizes both proposal and selection to suppress exactly these paths. See [[wiki/02-test-time-computation-vs-reusable-mechanisms|Increased Test-Time Computation Rather Than Reusable Mechanisms]].

### Q4. How is the harness-evolution loop formalized, and what are the score and cost objectives?

> [!tip]- Answer
> An agent A = (π, H) combines frozen policy π with harness H, scored by verifier r(x,τ) ∈ [0,1] with S(H;D) as expected score and C(H;D) as expected policy-token cost. Each round executes Ht on Devolve, summarizes trajectories into feedback Ft, samples candidates from a proposer, and keeps the best by empirical evolve-set score Ŝ. Because candidates depend on earlier measurements on the same tasks, reuse of Devolve is adaptive empirical optimization over an expressive space. See [[wiki/02-test-time-computation-vs-reusable-mechanisms|Increased Test-Time Computation Rather Than Reusable Mechanisms]].

### Q5. What are the three proposal-side regularizers, and what is the annealed budget schedule?

> [!tip]- Answer
> Proposal regularization uses annealed update sparsity, evidence-aware credit assignment over full run history, and structured exploration during stalls. The budget follows bt = bmin + (bmax − bmin)·½(1 + cos(πt/T)) (Eq. 4), starting broad for coordinated changes and annealing sparse for attributable late edits. Evidence-aware credit keeps rejected mechanisms as negative evidence, while stalls (progress within noise band δ over w rounds) reserve capacity for unexplored components. See [[wiki/03-regularization-view-of-harness-evolution|Regularization View of Harness Evolution]].

### Q6. What are the four selection-side regularizers, and what is the complexity-aware acceptance rule?

> [!tip]- Answer
> Selection requires leakage screening (critic rejects task-name, entity, answer, or benchmark-specific logic before scoring), stability-aware acceptance Ŝ(H′) ≥ S★ − δ (Eq. 5), complexity-aware acceptance, and Lasso-style structural pruning of components with no strictly positive gain in the pruning window. For gains ΔS > δ the gain-dependent cost rule ΔC ≤ β0 + β1ΔS (Eq. 7) applies, where ΔS and ΔC are score and relative token-cost changes and β0, β1 are fixed from the evolve set. The criteria are non-compensatory: a candidate must pass all of them. See [[wiki/03-regularization-view-of-harness-evolution|Regularization View of Harness Evolution]].

### Q7. What are the three evolve domains, their OOD counterparts, and the shared experimental protocol?

> [!tip]- Answer
> Coding evolves on Terminal-Bench 2.1 (89 containerized shell tasks) with OOD SWE-bench Verified; agentic workspace evolves on Harvey LAB (120 evolve / 40 pristine ID held-out) with OOD JobBench, GDPval, and APEX-Agents; engineering design evolves on EngDesign (61 simulator-graded tasks) with OOD Frontier-Eng. All baselines (H0 plus Meta-Harness, AHE, TTHE, HarnessX) start from the same H0 with the same frozen Claude Opus 4.8 policy, evolve set, and candidate budget. Harness and baseline are always evaluated in the same window with identical tools, judges, and trial counts. See [[wiki/04-environments-and-experimental-setup|Environments and Experimental Setup]].

### Q8. What are the headline main results, and how does Table 1 invert the evolve-vs-OOD ranking?

> [!tip]- Answer
> Evolve-set gains are +6.0 (Terminal-Bench 2.1), +4.9 (EngDesign), +1.1 (Harvey LAB), while every held-out split improves: +1.8 SWE-bench Verified, +2.3 Harvey LAB ID held-out, +3.5 to +4.7 on OOD agentic benchmarks, +4.3 Medal points on Frontier-Eng. Table 1 shows RRSI posts the smallest evolve gain (90.5) yet the only OOD average clearing H0 by over a point (43.6 vs 39.7), while Meta-Harness adds only 0.9 OOD and AHE/TTHE finish below base. No held-out split regresses anywhere. See [[wiki/04-environments-and-experimental-setup|Environments and Experimental Setup]].

### Q9. What does the Table 2 ablation show about removing proposal versus acceptance regularizers?

> [!tip]- Answer
> Removing proposal constraints costs only 0.2 points on evolve but 1.7 points OOD, showing steering where search looks matters even when nothing is rejected. Removing acceptance constraints lifts evolve 90.5 to 91.5 while OOD falls 43.6 to 41.0 and token cost rises by half. Removing both maximizes evolve score (92.8) while collapsing OOD to 40.3 near the unevolved harness at 3.80M versus 2.42M tokens per trial. See [[wiki/05-ablation-proposal-vs-acceptance-regularizers|Ablation: Proposal vs Acceptance Regularizers, Transfer, Cost, and Conclusions]].

### Q10. How does RRSI transfer across policy families and to a weaker unseen backbone, and what does it cost?

> [!tip]- Answer
> Under Gemini 3.5 Flash, Terminal-Bench 2.1 rises 64.6 to 78.7 (+14.1) with +2.2 transfer to SWE-bench Verified; under Claude Opus 4.8 the gains are +6.0 evolve and +1.8 OOD. The Gemini-evolved harness run unchanged on unseen Gemini 3.1 Flash Lite rises 11.2 to 14.6 (+3.4, 30.4% relative), proving the mechanism is a reusable program, not a policy artifact. RRSI is the lightest evolved harness (26.3 steps, 2.42M tokens) versus AHE at 3.82M tokens for 4.4 points less OOD. See [[wiki/05-ablation-proposal-vs-acceptance-regularizers|Ablation: Proposal vs Acceptance Regularizers, Transfer, Cost, and Conclusions]].

### Q11. What does the 06-references bibliography segment cover, and which entries anchor the method?

> [!tip]- Answer
> The segment (pp. 11–14) lists model releases (Claude Opus 4.8, Sonnet 4.6, Gemini 3.1 Pro/3.5, Qwen3.6), harness foundry and evolution methods (HarnessX, AutoHarness, Meta-Harness, AHE, TTHE, Recursive Harness Self-Improvement, Self-Harness), benchmarks (SWE-bench, Terminal-Bench, Evo-Bench, Evoharnessbench), and memory/reasoning works (EvolveMem, ReasoningBank, SkillRL, Agent0, Darwin Gödel Machine). The load-bearing theory anchors are Dwork et al. 2015 on adaptive data analysis, Haarnoja et al. 2018 on entropy regularization, Louizos et al. 2018 on L0, and Hastie et al. 2009 on sparsification. See [[wiki/06-references|References (Anthropic Claude Opus 4.8 onward)]].

### Q12. How do the appendix evaluation protocol and the four baselines work?

> [!tip]- Answer
> Every harness-baseline pair is evaluated in the same window with the same tools, judges, and trial counts, with containers reset between arms so no state carries over. Scoring ranges from Terminal-Bench accuracy over 89 tasks and SWE-bench resolve rate (fail-to-pass plus pass-to-pass), through Harvey LAB criterion fractions (~14,000 verdicts), GDPval expert win rate by three-judge majority, APEX-Agents pass@1 over 480 tasks, to Frontier-Eng Medal Score (1/0.67/0.33 over 38 buildable tasks). The four baselines are Meta-Harness (outer-loop harness-code optimization), AHE (observability-driven evolution), TTHE (test-time multi-candidate evolution with agentic judge), and HarnessX (modular typed primitives with trace-driven adaptation). See [[wiki/07-references-continued|References (continued) and Appendix: Evaluation, Baselines, Method Details]].

### Q13. What is the appendix selection rule: retention, edit budget, novelty, and domain guards?

> [!tip]- Answer
> Algorithm 2 retains the incumbent (Ht+1 = Ht) when the admissible set At is empty, otherwise picks its highest-scoring member and updates S★ ← max(S★, Ŝt+1). Each candidate applies a subset zt of a per-round redrawn atomic-edit pool Et with ‖zt‖₀ ≤ bt (Eq. 9), and history Lt records per-edit component, hypothesis, diff, ΔS, ΔC, and win flag. Within-noise-band candidates (ΔS ≤ δ) pass only via the shaped rule wsΔS − wcΔC + wnνt(H′) > 0, where novelty νt counts new structural types over {client_tool, skill, memory, subagent} and coding fixes ws = 0; only engineering design adds guards (valid-output drop > 0.03 or no-submission rise > 0.02 rejects). See [[wiki/08-selection-rule-and-appendix-details|Selection Rule and Appendix Bookkeeping Details]].

### Q14. What are the per-domain hyperparameters and case-study outcomes for final-round selection?

> [!tip]- Answer
> Noise tolerance δ is 0.017 coding, 0.004 agentic workspace, 0.020 engineering design, calibrated from repeated base-harness evaluations, with (β0, β1) at (0.10, 44.5), (0.10, 35.4), (0.15, 24.4); all hyperparameters use only evolve environments, never held-out or OOD. Admissibility is conjunctive (floor plus applicable cost branch plus guards), highest admissible score wins, else the incumbent stays. Case studies confirm selection is not score alone: Coding R0-A accepted (+3.93) while similar R0-B was cost-rejected (+1.69, +26.1% cost), R8-B was floor-rejected (−2.81 despite −13.6% cost), and Engineering R2 accepted a small reusable control-flow fix (+6 passes, +1.6% tokens). See [[wiki/09-final-round-selection|Final Round Selection]].

### Q15. (Evaluation) Your team wants to adopt RRSI-style evolution for an internal coding agent with a small, noisy eval set and a strict inference budget — should you, and which regularizers matter most?

> [!tip]- Answer
> Yes, but only with the full regularizer stack, since a small noisy eval set is exactly where unregularized evolution memorizes and the ablation shows removing either group raises evolve score while lowering transfer and inflating tokens. Prioritize the noise-adjusted floor calibrated from repeated base runs, the gain-dependent cost rule with tight β0/β1, and the annealed edit budget plus pruning to keep the harness light. Treat the reported 30%-lighter, OOD-transferring harness as conditional on frozen-policy, fixed-budget evolution rather than a guarantee under longer runs or new tool ecosystems. See [[wiki/09-final-round-selection|Final Round Selection]].
