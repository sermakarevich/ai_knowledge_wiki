---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]]
# Retrieval Practice: Agentic ML Exploration (A-MLE) for Ads Ranking
Answer each question from memory, then expand the tip to check.
### Q1. Why does a portfolio of dozens of differentiated ranking models combined with a days-to-weeks cost per single-model iteration leave the long tail of model-by-technique pairs unexplored, and what are the six manual phases?
> [!tip]- Answer
> Each model has its own objective, surface, data, features, architecture, and infra limits, so porting an idea costs a full try-train-evaluate cycle of days to weeks of senior attention. A finite team can therefore test only a small fraction of pairs, leaving long-tail models underexplored even when a technique works nearby. The six phases are ideation, prioritization, implementation, training and failure recovery, evaluation triage, and proposal preparation. See [[wiki/01-manual-iteration-bottleneck|Manual Iteration Bottleneck]].
### Q2. What parameterizes a single A-MLE session, what are its five stages, and what are its two terminal outputs?
> [!tip]- Answer
> Each session is fixed by a (model, objective, compute) triple that sets the target, the success goal, and the budget. One tool-using agent then walks hypothesis generation, exploration strategy, experiment execution, and result analysis over a shared substrate of skill library plus sandbox. Every stage boundary is a human checkpoint, and the session ends in either a launch proposal or a documented null result. See [[wiki/02-five-stage-system|Five-Stage System]].
### Q3. Why does the paper conclude that chaining phases without engineer handoffs is the main lever, rather than automating any single phase?
> [!tip]- Answer
> The semi-automated baseline kept engineer hypotheses but scripted launches and evaluations, yet gained only a smaller throughput bump with weaker offline impact and slower convergence. A-MLE instead chains planning, execution, and analysis without waiting on handoffs, multiplying completed iterations per engineer-week. The lesson is that handoff delay, not single-step speed, is the binding constraint. See [[wiki/03-tiered-evaluation|Tiered Evaluation]].
### Q4. On the L1 tool-availability bench on M*, what were the overall scores for the domain-equipped agent, the generic ML agent, and the generic LLM, and where was the gap largest?
> [!tip]- Answer
> The domain-equipped A-MLE agent reached 68% overall versus 16% for the generic ML agent with cross-portfolio tools and 8% for the generic LLM with no tooling. The largest gap was job-config modification, solved fully at 100% by the domain setup while both generic setups scored below 40%. The paper reads this as proof that domain skills dominate at L1. See [[wiki/03-tiered-evaluation|Tiered Evaluation]].
### Q5. What were the three headline L3 open-ended exploration results on M*, and why does multi-source exploration stand out?
> [!tip]- Answer
> Single-hypothesis arch scale-up gave +0.44% relative regression-error reduction with neutral training QPS, and multi-round arch exploration gave +0.58% with neutral QPS. Multi-source exploration combining model-state and training-efficiency generators gave +2.56% (reported as +2.557%) with +0.42% QPS. It stands out because combining hypothesis sources substantially beats pushing architecture alone. See [[wiki/03-tiered-evaluation|Tiered Evaluation]].
### Q6. In the cross-LLM study with loop, skills, and prompts fixed, what were the L2 completeness scores and how did stressful prompts flip L3 behavior by family?
> [!tip]- Answer
> L2 split into a capable cluster -- Gemini 2.5 at 100, Sonnet 4.0 at 96.7, Sonnet 3.5 and 3.7 at 93.3 each, GPT-5 at 66.7 -- versus GPT-4 at 13.3, with weak models hallucinating workflow IDs or failing to wait on async jobs. Under the basic prompt Gemini 2.5 and GPT-5 led near 116.04 x1e-4 rMSE gain, but under stress Sonnet 4.0 jumped to 255.87 x1e-4 while GPT-5 retreated to 68.05 x1e-4. Stress therefore favors Sonnet-style conservatism-turned-aggression and punishes GPT-5 exploration. See [[wiki/04-cross-llm-study|Cross-LLM Study]].
### Q7. How does A-MLE map onto Meta's production REA system, and what production impact does the companion article report?
> [!tip]- Answer
> A-MLE's sandboxed loop plus waiting operator maps to the REA Executor plus hibernate-and-wake over multiweek spans, its substrate with eligibility and Track Record maps to the Historical Insights Database plus experiment logger, and its hypothesis generators map to the dual-source engine of history plus research agent. Strategy maps from explore-then-exploit to REA's Validation, Combination, then Exploitation within approved budgets. Reported impact is 2x average accuracy across six models and 5x engineering output, with three engineers shipping proposals for eight models versus two engineers per model historically. See [[wiki/targeted|REA Mapping]].
### Q8. What is the weakest evidence link behind A-MLE's reported wins, and why does baseline drift force recalibration before any launch claim?
> [!tip]- Answer
> Throughput, training-success, and proposal-acceptance gains are reported only qualitatively because exact numbers are undisclosed, so they cannot be independently sized. Baseline drift then weakens even the quantified offline wins, since a concurrent refresh can erase a measured gain because hypotheses were tuned to the older reference. Treat every win as provisional until rechecked against a fresh rolling baseline with multi-seed reruns and segment breakdowns. See [[wiki/05-failure-modes-and-outlook|Failure Modes and Outlook]].
