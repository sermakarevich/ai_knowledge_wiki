> [[index|Wiki]] | [[digest|Digest]] | [[summary|Summary]]

# The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement — In Plain Language

## What is this about?

Think of a cooking student who not only follows recipes but rewrites the cookbook itself: after every dish, the good tricks get written down permanently, and — crucially — the student also improves *how* they learn, so next week's learning goes faster. That is recursive self-improvement (RSI): an AI system that turns its own experience and feedback into lasting self-changes, and reuses those changes to get better at improving itself.

Right now, the bottleneck is not raw model size — models already reach trillions of parameters with million-token context windows. The bottleneck is the human-coordinated improvement pipeline: people still decide what to improve, build the training resources, and validate each change by hand. The paper surveyed here maps the whole field (491 papers plus 72 industrial systems) as a ladder of autonomy, from systems that merely retry an answer up to systems that rewrite their own improvement machinery and pass it on to successors.

A key piece of evidence is the Headroom-Closed Index (HCI): across 393 model-benchmark observations from 2023 to September 2026, advanced math (86.4) and graduate science (85.8) are far ahead, while interactive agentic domains lag — software engineering 52.6, search/terminal agents 56.8, tool agents 39.9. The biggest remaining headroom, and the biggest illustrative value of RSI, is in stateful tool-using workflows.

## Why does it matter?

- **Foundation training is enormously expensive.** One GPT-5.6 gain of just over 15% in token generation took hundreds of experiments; one benchmark (GDPval) cost about 9,240 expert-hours for 1,320 tasks; one exam dataset took 70,000 attempts to produce 3,000 questions. Anything that automates this pipeline saves real money and time.
- **Feedback environments cost a fortune too.** Post-training for DeepSeek-V3.2 exceeded 10% of pretraining cost; one competition effort used millions of solutions across 540,000 problems. RSI promises to generate and validate experience more autonomously.
- **Deployed agents keep needing adaptation.** Agentic workloads use about 4× the tokens (15× for multi-agent setups), and one industrial system sees thousands of regressions per week at roughly 10 engineer-hours each. Systems that distill deployment experience into lasting skills cut that recurring bill.
- **The gap is where it hurts most.** Math and science benchmarks are largely saturated; the interactive, tool-using agent work that businesses actually want to deploy is exactly where progress lags.

## How does it work?

The survey organizes every system on one ladder, from no persistence to full recursive inheritance:

1. **B0 — retry, then forget.** The system revises its answer (self-refine, self-critique, tree search over ideas) but nothing persists. Limits: experience never accumulates, the procedure stays human-defined, self-feedback can reinforce errors, and more retries under a fixed checker give limited gains.
2. **L1 — AI executes, humans define.** The loop is: receive objective → run the prescribed procedure → produce an improvement → save it → repeat. Example: an industrial system compressing hours of regression investigation into minutes with retained repair skills. Covers data, training methods, platforms, evaluation, deployment, and applications — but humans set the objective, procedure, and acceptance bar.
3. **L2 — AI picks the next move.** The loop is: observe performance → diagnose → choose how to change → test it → keep or revert → repeat. Organized by what is searched: prompts (e.g. GEPA, Promptbreeder), agent workflows (e.g. ADAS, AFlow, AgentSquare), or training rules and architectures (e.g. kernel profile–rewrite–benchmark loops). Watch out: extra search compute can masquerade as algorithmic genius, and AI judges may share the proposer's blind spots.
4. **L3 — AI chooses what to learn next.** The system aims its own curriculum at its weaknesses: challenger tasks tied to solver performance, self-play with learnability rewards, visual questions guided by uncertainty, and agents like VOYAGER that couple the curriculum to exploration history plus a reusable skill library.
5. **L4 — AI decides what deployment experience to keep.** Trajectories get distilled into text guides, structured knowledge, procedures, or executable skills; the agent system itself is iteratively revised; retention is selective, with validation, library upkeep, and governed release. Accepted changes can still fail by learning the wrong lesson, wrong scope, non-activation, or forgetting.
6. **L5 — the improver itself is inherited.** The AI persistently modifies the mechanism behind future improvements (search procedure, successor evaluator, research policy) and successors reuse it. Structural L5 means reuse was demonstrated; effective L5 means successors actually got better under matched budgets and independent assessment. End-to-end L5 exists only in bounded prototypes.
7. **Three credibility checks for any RSI claim.** Safe inheritance (some runs end up worse than they started — 14% in one 100-trial study), autonomy attribution (verify which parts the AI really controlled versus what stayed human-fixed), and reliable verification (guard against cherry-picked seeds, shortcut discovery, and test-label extraction; one approach freezes evaluators per round with a ground-truth anchor).

## Where can this be used?

- **Science (S1).** Evolving hypothesis modules, experimental agents (one system ran 1,590 tasks and evolved 925 tools), and reflection components. Strongest frontier: L2, with only aspects of L3 and almost no L4/L5.
- **Embodied intelligence (S2).** Co-evolving environments and curricula, reusable skill libraries, self-improving policies, and world models that double as evaluators. Reaches co-evolution in simulation and bounded L5 in one system (ENPIRE), but no safe autonomous real-world loop.
- **Software engineering (S3).** The natural home, since product and agent are both executable code: agents editing their own codebase under version control with rollback, shared skill libraries, and populations of agent variants competing under regression-aware selection. L2 established, L3 emerging, full L5 undemonstrated.
- **Healthcare (S4).** Evolving clinical memory, diagnostic reasoning strategies, and governed tool workflows under strict no-unrestricted-trial-and-error constraints, delayed and confounded feedback, and population-dependent validity. L2 is the frontier; L4/L5 largely unexplored.
- **Industry proofs.** Clean developer workspaces beat noisy ones by 21.7–51.6 percentage points; an enterprise knowledge pipeline lifted usability from 52% to 65%; a data-quality double loop cut defects from 9.0% to 3.7% and handling time from 48 to 27 minutes; automated AI engineering matched a major training framework in hours and raised hardware utilization several points; verifiable research infrastructure raised QA accuracy from 72.4% to 93.7%.

## Conclusions & takeaways

- RSI is a ladder, not a switch: persistence (B0→L1), strategy choice (L1→L2), control of the learning agenda (L2→L3), deployment adaptation (L3→L4), recursive inheritance (L4→L5). Higher rungs are more domain-dependent, and honest evidence thins out fast above L2.
- No system today achieves true end-to-end recursive self-improvement; the strongest results are bounded prototypes and L1–L2 persistent updates with fragments of L3–L5.
- The field's shared bar for the future: inherited changes must demonstrably help later rounds improve faster, under explicit resource and authority limits — spanning diagnosis, curriculum choice, memory management, governed adaptation, trustworthy meta-improvement, long-horizon evaluation, resource accounting, and reproducible infrastructure.
- Safety gates must stay outside the loop: while the improver becomes adaptive, the evaluators, constraints, and deployment approvals protecting it must remain externally guarded.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| RSI (recursive self-improvement) | An AI loop that turns its own experience into lasting self-changes and reuses them to improve future improving |
| Autonomy levels B0–L5 | The ladder from retry-and-forget (B0) up to inheriting a rewritten improver (L5) |
| HCI (Headroom-Closed Index) | A scoreboard of how much progress benchmarks show per domain; high means nearly solved |
| Persistent update | A change that sticks around for future tasks, not just the current answer |
| Verifier / evaluator | The checker that judges whether an improvement is real; its reliability is half the battle |
| Skill library | A saved collection of reusable abilities distilled from past runs |
| Experience Bank | A store of executable past traces (code, logs, scores, feedback) used to train successors |
| RAG (retrieval-augmented generation) | Answering by first looking facts up in a knowledge base, then generating |
| MFU (model FLOPs utilization) | Share of the chip's raw math power actually used in training; higher is more efficient |
| BPB (bits per byte) | A compression-style quality score for models; lower is better |
| SOL (speedup over baseline) | How much faster a solution is than the reference; higher is better |
| Regression-aware selection | Only keeping changes that pass old tests too, so nothing that used to work breaks |
