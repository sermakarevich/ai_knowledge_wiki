> [[index|Wiki]] | [[summary|Summary]]
# RRSI: Regularized Recursive Self-Improvement of Agent Harnesses — Digest

## 1. [[wiki/01-rrsi-regularized-recursive-self-improvement|RRSI: Regularized Recursive Self-Improvement of Agent Harnesses — Framing and Proposal]]
**In one sentence:** Iterative harness-level recursive self-improvement overfits its evolve set, so RRSI regularizes candidate proposal and selection to favor reusable mechanisms, gaining up to 14.1 points in-distribution and up to 4.7 points on five out-of-distribution benchmarks while using 30% fewer policy tokens.
## Key points
- An LLM agent's capability is largely magnified by its harness: the prompts, control flow, tooling, memory, and context management surrounding the frozen backbone model.
- Recent methods automate harness engineering by iteratively proposing and selecting component-wise edits, practically establishing recursive self-improvement (RSI) at the agent-system level.
- Such recursive evolution overfits by memorizing training tasks, showing large in-distribution gains that shrink or even vanish on out-of-distribution benchmarks.
- The RRSI proposer operates with a temporally annealed budget limiting how many edits a candidate can bundle, and encourages unexplored trajectories based on evolution history.
- The RRSI selector uses a critic that screens benchmark-specific proposals and a pruner that removes changes that are too small, too expensive, or no longer useful.
- Across eight benchmarks spanning coding, agentic workspace, and engineering design tasks, RRSI gains up to 14.1 points on the split it evolves against and up to 4.7 points on the five out-of-distribution benchmarks.
- The resulting harness runs on 30% fewer policy tokens than the unregularized evolution.
- Figure 1 shows prior methods retain little of their evolve-set gain on the agentic workspace benchmark and several end below H0, the initial harness, while RRSI generalizes the improvements.

## 2. [[wiki/02-test-time-computation-vs-reusable-mechanisms|Increased Test-Time Computation Rather Than Reusable Mechanisms]]
**In one sentence:** Recent harness-evolution methods gain from increased test-time computation rather than reusable mechanisms, so RRSI regularizes proposal and selection to close the evolve-to-transfer generalization gap.
## Key points
- Generalization is defined as an evolved harness transferring unchanged to unseen benchmarks with different task descriptions, tool interfaces, or verifiers.
- Recent works explicitly separate evolution and evaluation tasks to measure generalization (Huang et al., 2026d; Ke et al., 2026; Zhang et al., 2026d).
- Overfitting arises through three coupled behaviors: benchmark-specific fitting, noise chasing (candidates favored by evaluation noise), and complexity accumulation that improves evolve-set scores without improving the underlying mechanism.
- RRSI keeps the harness fully editable while constraining how finite evolve-set feedback guides search, regularizing both candidate proposal (simpler, reusable edits) and selection (robust criteria).
- RRSI is evaluated on eight benchmarks spanning three domains differing in task type, tooling, and verifier, evolving on one suite per domain and running unchanged on held-out benchmarks.
- RRSI gains up to 14.1 points on the evolving split and improves all six held-out splits by up to 4.7 points out of distribution, on fewer policy tokens than unregularized evolution.
- RRSI outperforms the average prior baseline by up to 22.9% across held-out environments, indicating broadly useful rather than environment-specific harness changes.
- Harness evolution is formalized as adaptive empirical optimization: propose candidates from `H_t` and feedback `F_t`, then select by empirical evolve-set score, reusing `D_evolve` adaptively across rounds.

## 3. [[wiki/03-regularization-view-of-harness-evolution|Regularization View of Harness Evolution]]
**In one sentence:** RRSI leaves the reachable harness set Ω(H) fully open to any source edit but regularizes the search trajectory through it, splitting regularization into proposal-side capacity control and selection-side survival criteria mapped to L0/L1/L2 analogies.
## Key points
- Let Ω(H) denote harnesses reachable from H by arbitrary source edits — prompts, control flow, configuration, context management, tools, skills, memory, and subagents may all be modified, added, or removed — and RRSI regularizes the trajectory, not the hypothesis space.
- At each round t the proposer generates candidate edits to Ht from finite evolve-set feedback and the selector decides which, if any, replaces the incumbent.
- Proposal regularization has three mechanisms: annealed update sparsity, evidence-aware credit assignment, and structured exploration during stalls.
- Annealed budget follows bt = bmin + (bmax − bmin) · ½(1 + cos(πt/T)) (Eq. 4), decreasing from bmax to bmin so early rounds combine coordinated changes and later rounds are sparse and attributable.
- Selection regularization is non-compensatory: a candidate must pass leakage screening, stability-aware acceptance Ŝ(H′) ≥ S★ − δ (Eq. 5), and complexity-aware acceptance before score justifies replacing the incumbent.
- Complexity-aware acceptance requires ΔC ≤ β0 + β1ΔS (Eq. 7) for gains ΔS > δ, where ΔS = Ŝ(H′) − Ŝ(Ht) and ΔC = (Ĉ(H′) − Ĉ(Ht))/Ĉ(Ht) (Eq. 6), using policy-token cost as footprint proxy with β0, β1 fixed from the evolve set.
- Structural pruning sparsifies the retained harness: components with no strictly positive measured gain over a fixed pruning window are reported as deletion targets, imitating Lasso/L1 sparsification.

## 4. [[wiki/04-environments-and-experimental-setup|Environments and Experimental Setup]]
**In one sentence:** RRSI is evolved in three domains — coding, agentic workspace, and engineering design — with frozen Claude Opus 4.8 policy and fixed evolve/held-out splits, and improves every held-out split while baselines overfit the evolve set.
## Key points
- Coding uses Terminal-Bench 2.1 (89 containerized terminal tasks, real shell, task-owned unit tests); agentic workspace uses Harvey LAB (25 practice areas; 120-task evolve set plus 40-task pristine in-distribution held-out); engineering design uses EngDesign (61 tasks, each graded by its own frozen simulator, not a judge model).
- Out-of-distribution generalization is tested on SWE-bench Verified (coding bug fixing), JobBench / GDPval / APEX-Agents (agentic workspace), and Frontier-Eng (engineering design).
- Baselines are the unevolved base harness H0 plus Meta-Harness, AHE, TTHE, and HarnessX, all starting from the same H0 with the same frozen policy, evolve set, and candidate budget.
- Policy, proposer, cross-round failure-feedback analyst, and leakage critic are all Claude Opus 4.8, frozen throughout; base harnesses are Terminus-2 (coding), a ReAct loop over an MCP tool gateway, a dynamic toolbelt, and ReSum-style context management (Harvey LAB and EngDesign).
- Evolve-set gains are +6.0 points (Terminal-Bench 2.1), +4.9 (EngDesign), +1.1 (Harvey LAB); held-out gains include +1.8 on never-scored SWE-bench Verified, +2.3 on Harvey LAB ID held-out, +3.5 to +4.7 (7.2%–13.1%) on the three OOD agentic benchmarks, and +4.3 Medal points (+24.3%) on Frontier-Eng, with no held-out split regressing.
- On agentic workspace tasks RRSI posts the smallest evolve-set gain of any evolved harness but the only OOD average clearing H0 by more than a point (43.6 vs 39.7), while Meta-Harness adds only 0.9 OOD, HarnessX lands on base, and AHE/TTHE finish below base (TTHE by 1.7).
- Ablation shows removing either regularizer group raises the evolve score and lowers transfer: without acceptance constraints evolve rises 90.5 to 91.5 while OOD average falls 43.6 to 41.0 and token cost rises by half.
- Transfer survives deterministic simulation/testbench grading on EngDesign and Frontier-Eng, ruling out judge-styling or shared-format artifacts, and replicates under a different frozen policy (Gemini 3.5 Flash: +14.1 evolve, +2.2 OOD on SWE-bench Verified).

## 5. [[wiki/05-ablation-proposal-vs-acceptance-regularizers|Ablation: Proposal vs Acceptance Regularizers, Transfer, Cost, and Conclusions]]
**In one sentence:** Removing proposal constraints costs little on the evolve split but 1.7 points out of distribution, removing both regularizers maximizes evolve score (92.8) while collapsing OOD transfer, and the full RRSI harness still transfers across policy families and to a weaker unseen backbone while remaining the lightest evolved harness.
## Key points
- Removing proposal constraints alone costs only 0.2 points on the evolve split but 1.7 points out of distribution, showing steering where search looks matters even when nothing is rejected.
- Removing both regularizers lifts the evolve-set score to 92.8 (highest of any arm) but leaves OOD average at 40.3, within a point of the unevolved harness, at 3.80M tokens per trial vs 2.42M for RRSI.
- Under Gemini 3.5 Flash, RRSI improves Terminal-Bench 2.1 from 64.6 to 78.7 (+14.1) and transfers +2.2 to SWE-bench Verified; under Claude Opus 4.8, Terminal-Bench 2.1 rises 74.2 to 80.2 and SWE-bench Verified 82.0 to 83.8.
- The Gemini 3.5 Flash–evolved coding harness run unchanged on unseen Gemini 3.1 Flash Lite rises 11.2 to 14.6 (+3.4, 30.4% relative) despite a base score less than a fifth of the search policy's.
- RRSI is the lightest evolved harness via two cost regularizers: an L1-style budget refusing unpaid growth at proposal time and a pruning rule removing growth that stopped paying since.
- AHE is the extreme cost case at 3.82M tokens per trial, 58% more than RRSI, for 4.4 points less OOD; RRSI runs 26.3 steps per trial vs 27.3–34.6 for prior methods, while unevolved H0 costs 1.56M tokens and 21.2 steps.
- RRSI regularizes search dynamics (full-history credit, task-specific-logic filtering, noise-adjusted acceptance) with an open edit space, and its conclusion holds that RSI requires controlling how feedback becomes persistent change, with limits around frozen backbones, finite evolve sets, and hyperparameters.

## 6. [[wiki/06-references|References (Anthropic Claude Opus 4.8 onward)]]
**In one sentence:** This chunk is the bibliography segment (pp. 11–14) listing cited model releases, harness-evolution methods, benchmarks, and background theory, beginning with Anthropic's Claude Opus 4.8 (2026a) and Sonnet 4.6 (2026b) announcements.
## Key points
- The chunk opens with two Anthropic model announcements: Claude Opus 4.8 (2026a) at `anthropic.com/news/claude-opus-4-8` and Claude Sonnet 4.6 (2026b) at `anthropic.com/news/claude-sonnet-4-6`.
- It cites two Google model references: Gemini 3.1 Pro (2026a) at `deepmind.google/models/gemini/pro/` and Gemini 3.5 (2026b) at the Google blog Gemini-models page.
- It lists harness foundry/adaptation works including HarnessX (arXiv:2606.14249), AutoHarness (arXiv:2603.03329), Meta-Harness (COLM 2026b), and Adaptive Auto-Harness (arXiv:2606.01770).
- It lists harness-evolution benchmarks and studies including Evo-Bench (arXiv:2608.09096), Evoharnessbench (arXiv:2609.04280), SWE-bench (ICLR 2024, pp. 54107–54157), and Terminal-bench (ICLR 2026, pp. 40903–40986).
- It cites recursive/self-improving agent works including Recursive Harness Self-Improvement (arXiv:2607.15524), Self-Harness (arXiv:2606.09498), Darwin Gödel Machine (ICLR 2026, pp. 104223–104294), and Huxley-Gödel Machine (arXiv:2510.21614).
- It cites memory/reasoning/RL works including EvolveMem (arXiv:2605.13941), ReasoningBank (ICLR 2026, pp. 94327–94354), SkillRL (arXiv:2602.08234), Agent0 (COLM 2026c), and R-Zero (ICLR 2026, pp. 130770–130790).
- It cites background theory and engineering commentary including Dwork et al. 2015 on adaptive data analysis (NeurIPS 28), Haarnoja et al. 2018 on Soft Actor-Critic (ICML pp. 1861–1870), Louizos et al. 2018 on L0 regularization (ICLR), Hastie et al. 2009 (Springer vol. 2), Goodfellow et al. 2016 (MIT Press vol. 1), plus blog posts by Weng (July 2026), Rajasekaran (2026), Lopopolo/OpenAI (2026), Zhang/Khattab (July 2026), Niklaus (2026), and Ding et al. (Aug 2026).

## 7. [[wiki/07-references-continued|References (continued) and Appendix: Evaluation, Baselines, Method Details]]
**In one sentence:** This chunk gives three continued bibliography entries and the appendix opening — a paired-window evaluation protocol across eight benchmark surfaces (Terminal-Bench 2.1, SWE-bench Verified, Harvey LAB, JobBench, GDPval, APEX-Agents, EngDesign, Frontier-Eng), summaries of four harness-evolution baselines, and the start of the round-level RRSI formulation.
## Key points
- Harness and baseline are always evaluated in the same window with the same tool environment, same judge, and same number of trials, with containers/environments reset so no state carries between arms.
- Terminal-Bench 2.1 reports fraction of 89 containerized shell tasks solved (hidden unit tests must pass); SWE-bench Verified reports resolve rate requiring both fail-to-pass and pass-to-pass tests to hold.
- Harvey LAB grades exact-filename deliverables from Word/Excel/PDF sources on 20–100 criteria per task (~14,000 verdicts per full evaluation) via isolated Gemini-3.5-Flash judgments, split once into 120 evolve / 40 held-out tasks.
- GDPval reports win rate vs. human expert over 185 tasks by majority vote of three judges (Qwen3.6-35B-A3B, Claude Sonnet 4.6, Gemini-3.1 Pro) with both presentation orders; APEX-Agents reports pass@1 over all 480 tasks with missing/failed rollouts counted as failures.
- Frontier-Eng is used only out-of-distribution with a Medal Score (1 / 0.67 / 0.33 for gold/silver/bronze thresholds from the frozen v1 snapshot, mean over 47 v1 tasks as a percentage), excluding its EngDesign domain and scoring only the 38 buildable tasks in both arms.
- The four baselines are Meta-Harness (outer-loop optimization over harness code from scores/traces), AHE (observability-driven component/experience/edit representations), TTHE (test-time multi-candidate evolution with fixed weights and agentic judge), and HarnessX (modular typed primitives with trace-driven adaptation).
- RRSI's method note states L0/Lasso-L1/Ridge-L2 language is analogy-only for complexity control: it does not optimize norm-penalized objectives and does not treat heterogeneous harness components as coordinates of a shared continuous vector.

## 8. [[wiki/08-selection-rule-and-appendix-details|Selection Rule and Appendix Bookkeeping Details]]
**In one sentence:** RRSI retains the incumbent (𝐻𝑡+1 = 𝐻𝑡) when no candidate is admissible, bounding each candidate by an annealed edit-cardinality budget and admitting winners only through a stability floor plus a gain-dependent cost rule or a shaped within-band rule with structural novelty and domain guards.
## Key points
- Incumbent retention is strict: Algorithm 2 sets 𝐻𝑡+1 ← arg max over admissible set A𝑡 of 𝑆ˆ′, or 𝐻𝑡 if A𝑡 = ∅, and updates 𝑆★ ← max(𝑆★, 𝑆ˆ𝑡+1).
- Each candidate applies a subset 𝑧𝑡 ∈ {0,1}^|𝐸𝑡| of a per-round redrawn atomic-edit pool 𝐸𝑡 from Ω(𝐻𝑡), constrained by ‖𝑧𝑡‖₀ ≤ 𝑏𝑡 (Eq. 9), a cardinality constraint on the update rather than an 𝐿₀ penalty.
- History is per-edit: L𝑡 = {(𝑡𝑖, ℓ𝑖, ℎ𝑖, 𝑑𝑖, Δ𝑆𝑖, Δ𝐶𝑖, 𝑎𝑖)}, 𝑎𝑖 ∈ {0,1}, where 𝑎𝑖 = 1 iff the carrying candidate won its round; admissible losers get 𝑎𝑖 = 0, and candidates failing before valid measurement are ignored.
- Exploration and pruning are explicit inputs: E𝑡 = (𝜎𝑡, U𝑡, 𝑚draft) with stall flag 𝜎𝑡 = 𝟙[𝑆ˆ𝑡 − 𝑆ˆ𝑡−𝑤 ≤ 𝛿] and unexplored set U𝑡 = K \ T𝑡, while B𝑡 = {ℓ ∈ T𝑡 : 𝑔𝑡(ℓ) ≤ 0} marks components with no strictly positive gain in the pruning window for Lasso/𝐿₁-style deletion.
- Selection first enforces the noise-adjusted floor 𝑆ˆ(𝐻′) ≥ 𝑆★ − 𝛿, which permits within-tolerance fluctuation while blocking accumulation of small regressions.
- The acceptance branch splits on measured gain: for Δ𝑆 > 𝛿 the gain-dependent cost rule Δ𝐶 ≤ 𝛽₀ + 𝛽₁Δ𝑆 applies (Ridge/𝐿₂-style analogy), and for Δ𝑆 ≤ 𝛿 the shaped rule 𝑤𝑠Δ𝑆 − 𝑤𝑐Δ𝐶 + 𝑤𝑛𝜈𝑡(𝐻′) > 0 applies, with the coding instance fixing 𝑤𝑠 = 0 so within-band score gain alone cannot admit a candidate.
- Structural novelty counts only new structural types: 𝜈𝑡(𝐻′) = Σ 𝟙[ℓ ∈ comp(𝐻′) ∧ 𝑁𝑡(ℓ) = 0] over Kstr = {client_tool, skill, memory, subagent}, excluding prompt, control-flow, config, output-plumbing, and context-management edits.
- Only the engineering-design instance adds domain guards (𝑔 = 1 for coding and agentic-workspace): reject if valid-output rate falls by more than 0.03 or no-submission rate rises by more than 0.02 relative to the incumbent.

## 9. [[wiki/09-final-round-selection|Final Round Selection]]
**In one sentence:** A final-round candidate is admissible only if it passes the noise-adjusted floor, the applicable complexity-aware branch, and all domain guards, with the highest-scoring admissible candidate selected (otherwise the incumbent is retained) and the running best updated as 𝑆★ ← max(𝑆★, 𝑆ˆ(𝐻𝑡+1)).
## Key points
- Admissibility requires all three conditions jointly: the noise-adjusted floor, the appropriate branch of the complexity-aware rule, and all active domain guards.
- Among admissible candidates the selector picks the one with the largest measured score; if none is admissible, the incumbent is retained.
- The running best score is updated as 𝑆★ ← max(𝑆★, 𝑆ˆ(𝐻𝑡+1)).
- Hyperparameters are selected using only the evolve environment and operational considerations; held-out and OOD benchmarks are not used for tuning, and the noise tolerance 𝛿 is calibrated from repeated evaluations of the unchanged base harness.
- Scores 𝑆ˆ are fractions in [0, 1] and Δ𝐶 is the relative change in policy tokens per trial: 𝛿 is 0.017 (coding, 3 passes out of 89 × 𝑘 = 178 trials), 0.004 (agentic workspace, 60 criteria out of ~14,100 verdicts), and 0.020 (engineering design, 5 passes out of 61 × 𝑘 = 244 trials).
- Cost trade-off parameters (𝛽0, 𝛽1) are (0.10, 44.5) coding, (0.10, 35.4) agentic workspace, (0.15, 24.4) engineering design, corresponding to a 25% token allowance per additional pass (coding), per 100 additional criteria (agentic workspace), and a 10% allowance per additional pass (engineering design).
- Case-study trajectories show selection is not score alone: Coding R0-A accepted (+3.93 points) while similar R0-B rejected by cost rule (+1.69 points, +26.1% cost); Coding R8-B rejected by floor (−2.81 points despite −13.6% cost); Engineering R2 accepted (122/244 → 128/244 passes, +1.6% tokens) as a small reusable control-flow fix.

## The argument in five moves
1. Iterative harness evolution over a finite evolve set overfits through benchmark-specific fitting, noise chasing, and complexity accumulation, so prior methods show large evolve-set gains that shrink, vanish, or invert out of distribution.
2. RRSI keeps the reachable harness set Ω(H) fully open but regularizes the search trajectory: proposal-side annealed edit budgets, full-history credit assignment, and stall-triggered exploration steer search toward simpler reusable edits.
3. Selection-side regularization then filters what survives via pre-evaluation leakage screening, a noise-adjusted floor Ŝ(H′) ≥ S★ − δ, a gain-dependent cost rule (plus a shaped within-band rule with structural novelty), and structural pruning of persistently unproductive components.
4. Across coding, agentic workspace, and engineering-design domains with frozen policies and paired-window evaluation, RRSI trades the smallest evolve-set gain for the only robust OOD transfer — up to +14.1 evolve, up to +4.7 OOD, no held-out regression — while ablations confirm removing either regularizer group raises evolve score but lowers transfer and raises token cost.
5. The resulting mechanisms transfer across policy families and to an unseen weaker backbone, survive deterministic simulator grading, and form the lightest evolved harness, supporting the conclusion that practical harness-level RSI requires controlling how finite feedback becomes persistent change.
