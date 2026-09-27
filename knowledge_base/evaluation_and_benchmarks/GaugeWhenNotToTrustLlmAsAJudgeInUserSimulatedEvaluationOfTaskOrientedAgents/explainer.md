> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents — In Plain Language

## What is this about?

Many teams that build customer-service agents face the same problem: there is no clean test set for real conversations, and asking humans to rate every new version is slow and expensive.

So the industry settled on a cheap automatic gate with two parts. First, a fake user — a persona-driven simulator, which is an LLM (Large Language Model, an AI system trained on text) role-playing a shopper — chats with each candidate agent. Second, an LLM-as-a-judge — another AI model acting as a grader — reads the chat transcript and gives a score. The higher-scoring agent ships.

This paper asks a simple question nobody had measured properly: does that cheap gate pick the same winners as a grounded check of whether the task actually got done?

GAUGE — short for Grounded Audit of User-simulator-and-judge Gate Evaluation — is the authors' audit toolkit for answering that. It separates two ideas teams often mix up: ranking validity (does the gate order agents the same way as ground truth?) and construct validity (does a "satisfied user" score actually mean the task succeeded?).

The audit covers 25 agent versions from six providers, four judge models, two task worlds (shop and airline support in τ2-bench, plus math tutoring in SimulatorArena), and about 3,700 transcripts. A blind 3-person human panel also rated a stratified sample of 150 chats.

Think of it like a driving test. The simulator is the practice road, the judge is the examiner, and the verifiable reward is the hidden answer key — did the car actually park in the right spot? GAUGE checks whether the examiner's marks match the answer key.

A key design choice: the paper tests two different graders, not one. The policy-aware gate sees everything, including tool calls and the goal. The satisfaction proxy sees only the visible chat words, like a real customer would. Only the first one proves useful, which turns out to be the whole point.

## Why does it matter?

Because the gate can look human-approved and still point at the wrong thing. Two headline results show this.

First, satisfaction tells you almost nothing about success. Among chats the human panel rated satisfied (5 or more on a 1–7 scale), 57.5% had actually failed the customer's task. That is no better than the sample's own failure rate of 57.3% — knowing the user sounded happy did not lower the chance of failure at all. The correlation is flat and slightly negative (ρ = −0.147), and the ability to tell success from failure is worse than a coin flip (AUC, Area Under the Curve, a 0–1 accuracy score where 0.5 is random, is 0.44).

This is not just one wording or one rater. All five rated feelings — satisfaction, respect, clarity, helpfulness, would-return — are disconnected from success. It holds across five rater groups, both task worlds, and even when any single annotator is dropped.

Second, the ranking works in general but breaks exactly where shipping decisions live. Overall the gate's ordering matches the verifiable reward (a non-AI oracle check of database state and correct actions) very well (ρ = 0.94). But on near-equal pairs — agents whose true success rates differ by less than 10 points — the gate promotes the worse agent 31.0% of the time, versus only 0.9% on clearly separated pairs. Averaging four judges or trying 21 cheaper signals does not fix it.

In short: trust the gate for rough sorting, not for photo finishes or for proving users' tasks succeeded.

There are two extra dangers. One is the optimization trap: if you tune your agent to maximize satisfaction, you push on a dial that is already disconnected from the goal, so scores can climb while real success stalls or drops. The other is the absolute bar: if you set a pass/fail cutoff based on satisfaction, you will ship agents that fail roughly half the time (48–60% in the paper's test). A gate can therefore pass human review — the judge agrees with people — and still be anchored to the wrong target.

## How does it work?

GAUGE runs the cheap gate and the grounded truth side by side, then compares them at the level of whole agents.

Each agent converses with persona simulators — for example cooperative, impatient, distracted, anxious, terse, or skeptical characters — while keeping the task facts identical. Each chat transcript gets four scores: a policy-aware gate score (an operations-supervisor rubric that sees tool calls and the goal, and checks policy adherence first, then task resolution), a process-blind proxy score (a first-person shopper rating of how the chat felt, with tools and goal hidden), a blind human-panel score, and a verifiable non-AI reward (1 for task done, 0 for failed).

Three concrete cases make the gap vivid. A retail chat scores 7/7 from gate and proxy and 5.5/7 from humans, yet reward 0.0, because one pending T-shirt order was never changed. An airline chat feels perfect (proxy 7/7, "thank you so much!") yet reward 0.0, because the rebooking missed the required end state. A math-tutoring chat earns a human 10/10 yet is verifiably wrong: its own working implies 330 passes, but the tutor declares 165.

The paper then stress-tests every result. Same-family favoritism exists — a Claude judge inflates Claude agents by about +0.75 on the 7-point scale — but the ranking survives. A controlled simulator swap (same tasks, different fake-user provider) preserves both the gap and the ranking. A deliberately crippled-agent set confirms the tools can detect real breakage, including a sharp inversion where a step-starved agent scores 0.00 on truth but 4.64/7 on human satisfaction because it sounds helpful turn by turn before being cut off.

How is "better" measured? Mostly at agent level, not chat level. For each agent the team averages its gate scores and its grounded success rate, then checks whether the two orderings agree (Spearman ρ, rank correlation). They also count decision disagreements: for every pair of agents, did the gate promote the one with the lower true success rate? That pair-counting is what exposes the 31% close-pair problem that a single average correlation hides.

The crippled-agent check deserves a note because it is clever and cheap. The team took one good model and only tightened inference-time limits — fewer output tokens, fewer conversation steps, lower error tolerance — with no prompt or code changes. True success collapsed (degraded-tier average 0.05 versus 0.65 for healthy configs), yet satisfaction stayed mid-scale. Any valid gate must rank these broken configs last, and the policy-aware gate does.

## Where can this be used?

Anywhere a team uses fake users plus an AI grader as a release gate in CI (Continuous Integration, the automatic check that runs on every code change) — customer-support bots, tool-using assistants, tutors — this audit pattern applies directly.

The recommended cadence is calibrate-then-trust: run the expensive grounded audit once on a representative benchmark to learn where the cheap gate is trustworthy, then run the cheap gate in daily CI (Continuous Integration) only inside that trusted region. Re-audit whenever the model, prompt, policy, tools, or user mix changes — not on a fixed calendar.

Two practical tricks fall out. A judge-free completion bit — did the agent finish without truncation or crash? — is a free tripwire for truncation regressions (ρ = 0.87 on broken-vs-working). But out-of-sample score recalibration does not transfer, so do not expect one calibration curve to hold on new tasks.

What should a team do on Monday morning? Keep the cheap gate for fast everyday checks, but stop using satisfaction as the definition of done. Add at least one grounded check — database end-state, action log, or human-graded correctness — for release candidates. Flag any launch decision between two close-scoring agents for extra review, because that is where the gate is weakest. And treat a new model, prompt, tool, or user population as a reason to re-run the grounded audit.

## Conclusions & takeaways

- A polite chat is not a completed task. Satisfaction, respect, clarity, helpfulness, and likelihood to return all miss task success, so never use them as an accept/reject bar — such a bar admits agents that fail 48–60% of the time.
- What the grader can see matters more than how smart it is. The policy-aware gate that checks tools and outcomes halves failure risk (20.0% failures among accepted chats versus a 40.2% base rate, AUC 0.73); the process-blind proxy behaves like raw satisfaction (AUC 0.49). The weakest model-as-agent was tied-best as a grader.
- Aggregate correlation hides decision risk. A ρ of 0.94 sounds safe, but the 31% wrong-promotion rate on close pairs is the number that governs real launches.
- Favoritism is real but not the main story. Same-family judges boost their own models without changing the order; judge reruns are stable (ICC, Intraclass Correlation, a repeatability score, of 0.87).
- Calibrate scope, then trust cheaply. Map the gate's trusted operating region once against grounded truth, monitor truncation with a free completion check, and re-audit on configuration change.
- Close pairs need human-grade evidence. When two agents differ by a small margin, demand tool logs or end-state checks before declaring a winner.
- Do not grade with the same lens you train on. Optimizing for satisfaction alone is a classic Goodhart trap: the number improves while the real outcome does not.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| LLM (Large Language Model) | An AI system trained on large amounts of text that can chat, answer, and grade writing. |
| LLM-as-a-judge | Using one AI model as an automatic grader of chat transcripts. |
| User simulator | A fake customer played by an AI model, given a persona such as impatient or cooperative. |
| Task-oriented agent | A bot that must do real actions (look up orders, rebook flights), not just chat. |
| Verifiable reward / oracle | A non-AI rule check of the final state (was the database actually updated correctly?). |
| Ranking validity | Whether the cheap gate orders agents the same way as the grounded truth. |
| Construct validity | Whether a score (like satisfaction) really measures what it claims (task success). |
| Satisfied-but-failed | A chat the rater calls satisfying even though the task objectively failed. |
| Spearman ρ (rank correlation) | A −1 to +1 score for how similarly two methods rank items; near +1 means same order. |
| AUC (Area Under the Curve) | A 0–1 score for telling success from failure; 0.5 is random guessing, higher is better. |
| CI (Continuous Integration) | Automatic tests that run every time code changes, before shipping. |
| Self-preference | A grader AI giving slightly higher scores to agents from its own model family. |
