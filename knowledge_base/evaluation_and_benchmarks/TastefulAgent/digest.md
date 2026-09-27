> [[index|Wiki]] | [[summary|Summary]]
# The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks — Digest

## 1. [[wiki/01-introduction-and-taste-definition|Introduction and Taste Definition]]
**In one sentence:** The paper defines agent "taste" as the ability to make good long-horizon decisions (e.g. which hypothesis to test or implementation to build on) and introduces Taste-Bench, a 502-question benchmark mined automatically from agent trajectories that freezes trajectories at decision forks and asks models to choose the better direction without seeing the outcome.
## Key points
- Taste is defined as the ability to make good long-horizon decisions whose influence extends beyond the current step, such as which hypothesis to test, which implementation to build on, or which experiment to run next.
- Existing benchmarks measure only end-to-end task success and provide no measure of decision quality along the way; none measures agent taste.
- Each Taste-Bench question presents a decision fork — a point where multiple directions were available and one leads to a better outcome — with all later work hidden at evaluation time.
- Forks are mined automatically without human annotation from parallel attempts at the same task and from detours (self-corrections) inside a single trajectory.
- Taste-Bench contains 502 taste questions drawn from software-engineering and machine-learning research trajectories.
- The best frontier model answers only 59.7% of Taste-Bench questions correctly.
- Forks whose deciding evidence appears later in the trajectory are much harder for every model, and a larger reasoning budget does not improve accuracy.
- Taste is trainable: distilling the judgment of a teacher that has seen the outcome into a student improves decisions on unseen tasks and end-to-end success on held-out SWE-bench Pro tasks.

## 2. [[wiki/02-measuring-taste-via-hindsight|Measuring Taste via Hindsight: Decision Forks and Taste-Bench Construction]]
**In one sentence:** Taste is measured in hindsight by finding decision forks where attempts share an equivalent prefix then diverge into different judgments, labeling the fork with whichever branch has the better realized outcome, and testing whether a model picks that supported candidate without seeing the future.
## Key points
- A single trajectory outcome cannot directly score a judgment because execution quality and environment also shape the outcome, so the method isolates judgment by comparing branches that share an equivalent prefix before a decision fork and differ mainly in the judgment at the fork.
- Formally each fork defines one taste question x = (q, ht, c1, c2) with prefix ht = (o0, a0, …, ot), and the label is the supported candidate y = arg max_i U(Ei) where Ei is branch evidence (e.g. test results, research scores) mapped to a scalar by U; taste Tb(π) is the fraction of questions where π(x) = y.
- Taste-Bench applies this to real trajectories with 502 questions built by two complementary constructions: parallel trajectories (wrong judgments the agent never notices, run to completion) and detour trajectories (wrong directions the agent takes then corrects inside one run).
- Mining starts from an engineering pool of 2,677 graded rollouts on 517 SWE-bench Pro tasks (GPT-5.4/5.5 agents) and a research pool of 1,132 runs on 47 AI R&D tasks (RE-Bench + HCAST research subset, MALT/METR transcripts); a generator proposes 4,657 candidate forks and 10.8% pass all filters to give 390 engineering + 112 research questions.
- Filtering removes two failure modes with judge models excluding the generator: trivial questions (every judge answers correctly from candidates alone, no trajectory) are dropped, and a question is released only when every judge agrees with its label given the full task record, trajectory, and outcome.
- Human review of 100 sampled questions gives 170/172 explicit A/B judgments agreeing with mined labels (98.8%), and on the 74 questions where both reviewers chose A or B they agree with each other on 98.6% with Cohen's κ = 0.973.
- Evaluation counters position bias by asking each question twice (deterministic seeded order plus exact reverse); headline accuracy counts a question correct only when both orders are correct (random guessing = 25%, always-picking-one-position = 0%), with mean-over-orders also reported and the Average headline defined as the 1:1 mean of research and engineering subset accuracies.

## 3. [[wiki/03-model-accuracy-results|Accuracy of Current Models on Taste-Bench]]
**In one sentence:** Frontier models score poorly on Taste-Bench (best 59.7% on binary choices), errors concentrate on forks whose deciding evidence appears late, and extra reasoning budget does not fix this.
## Key points
- Best model GPT-5.6 Sol reaches only 59.7% Average accuracy, with GPT-5.5 close behind at 59.5%, and all remaining models dispersed below them — none close to solving Taste-Bench despite every question being a binary choice.
- Research and engineering subsets diverge per model: e.g. Claude Opus 5 scores 64.3% on research but 46.7% on engineering, while GPT-5.6 Sol scores 62.5% research / 56.9% engineering.
- Mean accuracy over 14 models falls from 62.3% at the in-prefix horizon to 21.0% at the more-work horizon, near the 25% score of random guessing on the both-orders-correct metric.
- Detour forks are harder than parallel forks in both domains, and this gap exceeds the gap between the two domains (Appendix D.1).
- Moving from lowest to highest reasoning-effort setting changes accuracy by −0.2 points (GPT-5.6 Sol) and +2.2 points (GPT-5.6 Luna), with settings overlapping at every time horizon — larger reasoning budget does not improve taste.
- Models produce the most reasoning tokens at the more-work level, the level with the lowest accuracy, suggesting they recognize the hard forks but the deciding evidence appears only in the later work.
- Solid bars report accuracy when both candidate orders are answered correctly; dotted extension shows mean over the two orders; whiskers show 95% item-bootstrap intervals; unparseable responses count as incorrect.

## 4. [[wiki/04-taste-bench-vs-end-to-end-benchmarks|Taste-Bench Average vs End-to-End Benchmarks]]
**In one sentence:** Taste-Bench Average is useful only when it is not a restatement of end-to-end ability, and the chunk argues it passes this test because it is only partly correlated with SWE-bench Verified while separating top models that SWE-bench compresses, then shows taste can be distilled into Qwen3.6-27B to improve unseen-task judgment and end-to-end success.
## Key points
- Comparison uses each model's Taste-Bench Average against its public SWE-bench Verified score from the Vals AI leaderboard under one shared harness, with 11 models remaining after excluding 3 models unparsable on more than 9% of presentations.
- Pearson correlation between Average and SWE-bench Verified is r = +0.63, so SWE-bench Verified explains R² = 0.39 of variance between models; on the engineering subset mined from SWE-bench Pro tasks the correlation is only r = +0.37.
- The four highest models on SWE-bench Verified sit within 4.0 points of each other there but 10.7 points apart on Taste-Bench Average, showing Taste-Bench separates models at the top of SWE-bench.
- Distillation uses Qwen3.6-27B as base with LoRA-adapter updates, training on 390 engineering questions split into two task-disjoint folds so no student sees the source task of any evaluation question.
- Recipe distills reasoning rather than fitting binary labels: a privileged teacher seeing question plus supported-candidate description generates reasoning, and the student seeing only task, trajectory prefix, and two shuffled candidates is aligned via SDPO-style token-level distillation with forward KL over reasoning tokens and final choice, computed on teacher-sampled continuations.
- On the held-out fold the student reaches 47.9% accuracy vs 30.0% for the base model under the Section 3.4 protocol, with mean accuracy over two orders rising from 42.7% to 62.4% (+17.9 percentage points); on the training fold single-order accuracy rises from 48.6% to 92.9%.
- On 41 held-out SWE-bench Pro tasks with a fixed Qwen3.6-27B executor, success rises from 14.6% (no advice) to 39.0% (correct advice, +24.4 pp upper bound) and to 33.7% with student advice (+19.1 pp).

## 5. [[wiki/05-related-work|Related Work: Long-Horizon Agents, Pre-Outcome Judgment, Process Evaluation, and Distillation]]
**In one sentence:** The paper positions Taste-Bench against four literatures — long-horizon agent benchmarks that test task completion rather than direction choice, pre-outcome idea judgment on standalone ideas rather than in-trajectory forks, process/step-level evaluation that scores steps or whole trajectories rather than outcome-labeled direction choice made blind, and distillation methods whose recipe it adapts — and concludes that taste is measurable from existing trajectories (502 questions), distillable into weights, and transferable to end-to-end success.
## Key points
- Long-horizon benchmarks (AgentBench [9]; SWE-bench and SWE-bench Pro [10, 11]; MLAgentBench and RE-Bench [12, 13]) test whether an agent completes a long task, whereas Taste-Bench tests whether the agent chooses the better direction inside the task.
- Prior work on judging research directions before outcomes — predicting which of two ideas performs better [33], preferring one of two ML solutions before executing them [34], choosing the better of two AI-safety proposals against expert ratings [35] — judges standalone ideas or solutions, whereas Taste-Bench judges forks inside executed trajectories carrying the agent's situation and recorded outcome labels.
- Judgments of ideas before execution often flip after execution [36], which motivates Taste-Bench's use of recorded trajectory outcomes as labels.
- Process supervision scores steps with human labels [37] or rollout outcomes from each step [38]; agent work has trained policies from explored-vs-expert trajectory preferences [39] and verified alternatives at critical steps [40], plus test-time process reward models scoring candidate actions [41] — while Taste-Bench instead labels the better direction with the outcome the trajectory later records and evaluates the model choosing before seeing it.
- Whole-trajectory judges (Agent-as-a-Judge, AgentRewardBench [42, 43]) and failure-attribution methods (Who&When, AgenTracer [44, 45], which models localize poorly) differ from Taste-Bench's blind, outcome-labeled direction choice.
- The distillation recipe follows SDPO [32] but replaces environment feedback with a demonstration of the supported candidate and samples targets from the teacher rather than the student [51], transferring in-context judgment into weights; advisor models similarly steer an executor with advice from a small trained model [52].
- The paper's conclusion restates the arc: taste (choosing the better direction before the outcome is visible) is measurable from existing trajectories; Taste-Bench has 502 outcome-labeled questions; distilling teacher reasoning given the supported candidate transfers to unseen tasks; injecting the student's judgment as advice improves end-to-end success.

## 6. [[wiki/06-references-and-appendix-opening|References and Appendix Opening: Benchmark Construction Details]]
**In one sentence:** This chunk lists references [38]–[52] and opens Appendix A with the source trajectory pools, mined-fork statistics and validation rules, and the generator prompts used to build the benchmark.
## Key points
- Engineering trajectories come from 2,677 graded rollouts on 517 tasks from 11 repositories, produced by GPT-5.4 and GPT-5.5 agents in 31 runs between April and July 2026 on SWE-bench Pro.
- Research trajectories come from MALT/METR with 1,132 runs on 47 tasks from RE-Bench and HCAST, produced by Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude Sonnet 4, Claude Opus 4, and DeepSeek V3 agents.
- Detour construction input was 896 trajectories in a first pass plus 437 further trajectories in a second pass; parallel construction input was 600 pairs of opposite-outcome attempts, retained from 905 candidate pairs after exclusions.
- Released parallel engineering cell has 111 of 124 pairs contrasting same-model attempts and 13 contrasting GPT-5.5 vs GPT-5.4; all 48 research parallel pairs contrast same-model attempts.
- Detour forks require four verbatim excerpts in order (abandoned-direction commit, observed failure, recovery commit, recovery success) plus a failure signal such as non-zero exit code or error message, with mechanical discarding on any failed check.
- Parallel pairs are formed within a task between one passing and one failing attempt with at most eight pairs per task, pairing same-model/same-reasoning-setting attempts first.
- The generator is GPT-5.6 Sol at high reasoning effort, returning one JSON object per candidate fork, with separate parallel and detour prompts ending in the rubric requirements.

## 7. [[wiki/07-appendix-goal-spec|Appendix Goal Spec]]
**In one sentence:** The "Goal" appendix section specifies acceptance/rejection filters for judgment-benchmark samples plus the detour-generator prompts that ask for one genuine detour (poor approach pursued, wall hit, recovery) written as two neutral parallel next steps.
## Key points
- If the better option is already identifiable from pre-decision differences, the sample must be rejected.
- The prefix from the good trajectory before the start step must contain enough task context, and important task constraints must be preserved in the query even if they appear early in a transcript.
- Choices must describe the actual branch decisions at the same specificity and tone, must not mention scores, pass/fail, grader results, branch names, or hindsight, and must not use praise, blame, confidence, caution, or other wording that makes one option an obvious strawman — rejecting the sample if neutral parallel wording is not possible.
- A choice must not carry a branch's self-reported or predicted target metric when its direction makes that choice mechanically preferable (e.g. merely claiming a lower predicted loss); the decision procedure or controllable action must be described instead.
- The reason must identify post-decision trajectory evidence connecting the decision to the native outcome, and the timeline must be reconstructed before accepting: a score or artifact already existing before the proposed cut cannot be credited to the proposed next step.
- The proposed action must be new at the cut — reject if the same action was already executed before the cut or if cited post-decision evidence repeats pre-cut evidence — and only completed experiment outputs count as evidence, not scripts followed by timeout, OOM, interruption, or missing output.
- Claims or predictions written into an answer are not observed outcomes, validators prove only format/budget/schema constraints rather than task performance, actual implemented actions (not plans or filenames) must be compared with rejection when both branches implement the same approach, and failures rooted in submission/finalization protocol, timeout, crash, missing dependency, hard-coded answer, task-version mismatch, or instruction noncompliance must be rejected.
- Every evidence quote must be a literal excerpt from the cited trajectory step and is checked mechanically after generation, while the detour generator treats rejection as correct and preferred whenever a clean detour cannot be demonstrated or the better approach is only nameable with hindsight.

## 8. [[wiki/08-appendix-required-json-format|Required JSON Format]]
**In one sentence:** The appendix specifies the exact JSON schema miners must return for each taste fork, with mechanical ordering and evidence rules, plus the shared four-judge panel and both filter prompts, and reports the per-stage filtering yield.
## Key points
- Miners must return exactly one object with `is_good_sample`, `reason`, `query`, `breakpoint_step`, `good_choice`, `bad_choice`, and `evidence` containing `bad_action`, `wall`, `recovery_action`, and `success` steps with literal quotes.
- Ordering is checked mechanically: `breakpoint_step <= bad_action.step <= wall.step < recovery_action.step <= success[*].step`, with `bad_action` and `wall` allowed to cite the same step when one message contains both commitment and failure.
- The wall must be an observed failure (non-zero exit, error, traceback, "not found", failing assertion, explicitly reported failing result); a remark that something could improve, clean diff, or successful command is not a wall, and fabricated walls are discarded.
- Forks are rejected when the recovery is only nameable after seeing the failure (hindsight lookup, e.g. "revert the file the traceback names"), with preference for rejection when unsure; mid-rollout discoveries (missing tool/dependency/broken toolchain) require relocating the fork to mine the second cycle instead.
- Both options must be live candidates a competent engineer could plausibly pick from the prefix alone — no strawmen (e.g. repeating an action the prefix already shows failing), no different subproblems, no mere execution ordering — phrased in strictly parallel form with no evaluative/leaking words, grades, step numbers, or wall error text.
- Both Section 3 filters use the same four-judge panel (Kimi K2.5, GPT-4.1, Llama 4 Maverick, Mistral Large 3, excluding the generator) with one shared system message and per-question shuffling of candidate order.
- Of 4,657 mined candidate forks, 1,809 pass the generator rubric, 729 survive the trivial filter, and 502 questions remain in the release (10.8%); detour-research questions come from two passes (40 from 896 trajectories, then 24 from 437 further trajectories).

## 9. [[wiki/09-filtering-undecidable-examples|Filtering Undecidable Examples]]
**In one sentence:** One sparse-adversarial-attack fork was removed as undecidable because the prefix favored the multi-strategy ensemble (80% success with 3 pixels vs 43% for one-pixel) while the label rested only on a later full-scale timeout with no stated time budget, followed by released per-cell example questions and the exact evaluation prompt.
## Key points
- A ResNet18 CIFAR-10 sparse-attack task over 1000 images was removed as undecidable: Candidate A runs a single one-pixel attack with batched incremental saving, Candidate B scales a multi-strategy ensemble.
- At the fork, the record supports Candidate B: the ensemble reached 0.80 attack success with 3.00 average pixels changed on the sample set, versus 0.43 success for the one-pixel attack.
- The removal reason is that the label is determined only by a later timeout of the ensemble at full scale, and no time budget is stated in the task, so judges do not confirm the label from the full record.
- Appendix B releases one question per cell with task, shortened prefix, both candidates in release order, supported candidate, and hindsight evidence, with `[i]` marking trajectory-step index.
- Parallel engineering (Element Web homeserver discovery): supported Candidate A selects the five delegated-auth fields (`authorizationEndpoint, registrationEndpoint, tokenEndpoint, issuer, account`) because assigning the whole discovery block fails hidden deep-equality tests via extra state-marker and error fields.
- Parallel research (GPT-2 embedding repair, loss 2.55 → 10.5): supported Candidate A fine-tunes only the tied embedding for 200 iterations (`loss_validation`: 7.3821) over Candidate B's global-rescaling sweep (best std 0.032, `loss_validation`: 10.1482).
- Detour engineering (ansible-doc role summaries): supported Candidate A puts the missing-metadata placeholder on the production call path (28 passed) rather than extending `_build_summary()`/`_build_doc()` defaults (3 failed, 25 passed).
- Detour research (expression discovery, ≤5 operators, 1e-6 tolerance): supported Candidate A finds `add(inverse(X4), cosine(X3))` with max error 5.13e-10 and all 1000 rows in tolerance, after Candidate B's linear fit `Y − 1/X4 = −0.46926192 * X3 + 1.07467532` leaves error 5.4016000766e-01.

## 10. [[wiki/10-evaluation-prefix-rendering|Evaluation Prefix Rendering]]
**In one sentence:** Evaluation prefixes are rendered one line per trajectory step before the fork (with truncation rules for long outputs and a 65,536-token cap), answers are parsed from a final ANSWER line, and accuracy requires both seeded and reversed presentations to be correct.
## Key points
- Agent messages render as `[i] AGENT:` plus text, commands as `[i] $` plus command, exit code, and indented output, and file edits as `[i] EDIT:` plus edited paths.
- Command outputs longer than 700 characters keep head and tail with the omitted character count marked in between.
- Complete prompts are limited to 65,536 tokens; over-limit prompts keep the first 25 prefix lines (task setup) plus the longest fitting tail, marking omitted steps.
- In the main evaluation the token limit is reached by one question for two models (Claude Opus 5 and Claude Sonnet 5) and by no question for the other models.
- Responses are parsed from the final `ANSWER: X` line, with a single-letter response also accepted; unparseable responses score as incorrect and Table 4 reports counts per model.
- Each question is presented twice (seeded candidate order, fixed per question and shared by all models, and reversed); cell accuracy is the fraction correct in both presentations, mean accuracy is the fraction of correct presentations.
- Engineering accuracy pools the two engineering cells, research accuracy pools the two research cells, and Average is the mean of the two; Figure 3 95% intervals are percentile intervals from 4,000 bootstrap resamples drawn within each domain.
- Every model gets the same prompt and the same 65,536-token output budget with default sampling unless stated; Table 3 lists per-model reasoning settings.

## 11. [[wiki/11-time-horizon-annotation-levels|Time-Horizon Annotation Levels]]
**In one sentence:** Accuracy falls steeply from In-prefix to More-work decisions (mean 62.3% → 21.0%), extra reasoning budget does not rescue far-horizon choices, judge agreement on released parallel-engineering items is only 51.7% while human reviewers support the mined labels at 98.8%, and taste is distilled from a Qwen3.6-27B teacher into the same frozen student via forward KL plus calibration.
## Key points
- Accuracy declines with horizon distance: mean over models is 62.3% In-prefix (n=158), 42.9% Inferable (n=219), 31.5% Next-step (n=56), and 21.0% More-work (n=69), with GPT-5.6 Sol best In-prefix at 79.7% and Grok 4.20 Reasoning worst at 32.3% / 16.4% / 14.3% / 4.3%.
- Reasoning effort does not fix the horizon gap: GPT-5.6 Sol scores 56.2% (low), 55.6% (xhigh), 56.0% (max) and Luna 43.4% (none), 45.8% (high), 45.6% (max); a logistic budget×horizon interaction is null (p = 0.80 Sol, p = 0.82 Luna) over 10,000 joint bootstrap resamples.
- Models spend the most reasoning tokens at the More-work level yet score lowest there (13.0%–23.2% over six conditions); across 6,024 responses no response reaches the token limit and one is unparsable.
- Only Luna on the research subset improves with budget (43.8% → 54.5%); its engineering subset and both Sol subsets are unchanged.
- Judge agreement is weak on released parallel-engineering items (pairwise 51.7%; e.g. GPT-4.1 85.8% proposed → 63.7% released, Llama 4 Maverick 75.6% → 34.7%), while the undecidable filter keeps a question only under unanimous agreement so every judge selects the labeled candidate there by construction.
- Human review (100 questions: 70 released plus 15 trivial-removed plus 15 non-unanimous-removed, two-stage A/B then post-outcome judgment) supports the mined label on 170/172 retained judgments (98.8%), with reviewers agreeing on 73/74 jointly-retained questions (Cohen's κ = 0.973).
- Distillation uses the same frozen Qwen3.6-27B as teacher and student with different contexts (two views per question, both candidate orders); teacher traces at temperature 1.0 with 3,072-token budget keep 328/390 and 311/390 traces → 156 and 142 questions (312 and 284 views), selecting the supported candidate in 328/328 and 310/311 kept traces; loss is forward KL over top-100 student tokens plus remainder mass (≤512 reasoning positions) plus forward KL on the two answer tokens, trained on teacher-sampled continuations, then calibrated with cross-entropy on the student's own traces (306 and 320 views); LoRA rank 16, α = 32, 79.7M parameters, ~2 h per fold on one A100 80GB.

## 12. [[wiki/12-distillation-fold-splits|Fold Splits, Transfer Results, and End-to-End Experiment Details]]
**In one sentence:** Task-disjoint Fold 1 / Fold 2 splits (195 questions each) support distillation transfer evaluation where the student beats the base model (187 vs 117 both-presentations-correct of 390) and selects the supported fork candidate on 77 of 98 end-to-end forks across 41 held-out SWE-bench Pro tasks.
## Key points
- Each fold has 195 questions with identical parallel/detour splits (62/133), but different task counts (86 in Fold 1, 72 in Fold 2) and different per-repo mixes (e.g. ansible 29 vs 43, tutanota 21 vs 7).
- Transfer scoring presents each of the 390 questions in both orders and counts a question correct only when both presentations are answered correctly, with unparseable answers counted wrong.
- The student answers both presentations correctly on 187 questions vs 117 for the base model: +104 gained where the base is wrong, −34 lost where the base is right.
- On the training fold the gain from 48.6% to 92.9% has p ≈ 8 × 10−9, and Figure 7 intervals use item bootstrap with 4,000 draws as in Figure 3.
- Under the same scoring the student ranks below GPT-5.6 Sol (56.9%) and GPT-5.6 Terra (50.0%), equal to GLM-5.2 (47.9%), above Claude Opus 5 (46.7%), while the base model sits just below GPT-5.4 Nano (32.1%).
- For advice (one decision per question), summing log-odds over both presentations selects the supported candidate on 287/390 (student) vs 207/390 (base) — higher than accuracy because only the combined decision must be right.
- The end-to-end test uses 41 held-out SWE-bench Pro tasks (98 forks, 11 repos) with advice from the fold not containing the task; the executor is SWE-agent 1.1.0 with Qwen3.6-27B, and correct-advice gain over no advice has exact McNemar p ≤ 0.004.
- With student advice (supported candidate on 77/98 forks) the executor reaches 33.7% success, with per-task results in Table 12 (e.g. all 8 ansible tasks mostly correct; navidrome 8383527 0/2; element-web 494d9de 0/1).

## 13. [[wiki/13-trailing-fragment|Trailing Fragment (Chunk 33)]]
**In one sentence:** Chunk 13/13 ("33") contains no substantive content — only the two characters "33".
## Key points
- The chunk body consists solely of the heading `# 33` and the text `33`.
- No claims, numbers, mechanisms, tables, or quotes are present to summarise.
- There is nothing to mirror in subsections because the source has no sections.
- This page exists only as a placeholder so the 13/13 wiki set is complete.

## The argument in five moves
1. Taste is the ability to make good long-horizon decisions whose payoff appears only later, and existing end-to-end benchmarks do not measure decision quality along the way.
2. Later trajectory outcomes provide hindsight labels for earlier forks, so mining parallel attempts and in-run detours yields 502 outcome-labeled Taste-Bench questions with all future work hidden at test time.
3. Frontier models show limited taste (best 59.7%), with errors concentrating on forks whose deciding evidence appears far in the future and no rescue from larger reasoning budgets.
4. Taste-Bench is not a restatement of end-to-end ability (r = +0.63 vs SWE-bench Verified, wider spread at the top), and taste distills: a Qwen3.6-27B student trained on teacher reasoning improves on held-out folds (47.9% vs 30.0%).
5. Better judgment transfers end to end — student advice lifts a fixed executor from 14.6% to 33.7% on held-out SWE-bench Pro tasks — so taste is measurable from trajectories, trainable, and practically useful.
