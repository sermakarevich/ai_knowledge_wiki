> [[index|Wiki]] | [[summary|Summary]]

# Training AI Scientists to Replicate Research — In Plain Language

## What is this about?

Imagine giving a smart research assistant a scientific paper with one of the charts torn out, and asking them to run the experiment again from scratch and redraw that chart, given a strict time and equipment budget. That's the task at the heart of this paper. The twist is that the "assistant" here is an AI agent, and the researchers wanted to *train* it — not just prompt it — to get better at this specific kind of open-ended detective work.

The problem with training an AI on something like "redo this scientific experiment" is that there's no simple right-or-wrong answer to check against, the way there is for "did this code pass the unit test?" Scientific replication is messy: the paper never tells you every detail, there are many valid ways to approach it, and judging "did they do a good job" is itself a judgment call. So the authors built two things: a factory that mass-produces these replication challenges (called **Replica**), and a way to grade attempts at them that's almost as reliable as an expert human grader. With that grading system in hand, they could finally use reinforcement learning (RL) — a training method that needs a score to improve against — to train an AI model, which they named **Faraday**, to get better at this task over time.

## Why does it matter?

AI agents are already decent at things with a clear pass/fail test, like fixing a bug that makes a test suite go from red to green. But most of real scientific work — designing experiments, filling in gaps a paper doesn't spell out, deciding what to try next — doesn't come with a built-in scorecard. If AI is ever going to help meaningfully with science (not just coding), someone has to solve this "how do we grade open-ended work well enough to train on it" problem. This paper is a serious, carefully validated attempt at exactly that, using replication (redoing known experiments) as a stepping stone toward the harder goal of AI doing genuinely new research.

## How does it work?

Think of it as a four-step assembly line:

1. **Make the tests.** Take 100 well-known ML and AI-for-science papers. For each one, use an AI vision tool to find a results chart, black it out, and turn "recreate this chart" into a graded task. Do this automatically, and you get 310 tasks — far more than any team of humans could hand-craft.
2. **Make a fair grader.** For each task, have one AI (Claude) write a grading rubric — a checklist like "does the chart's shape match the claim in the paper? did they actually run real code, not fake numbers?" — without ever showing it the real answer chart. Then have a second AI (a coding-savvy judge) inspect an attempt's code, chart, and process, and score it against that rubric. The researchers checked this grader against real human PhD-level judges and found it agreed with them noticeably better than a generic "just look and rate it" AI judge would.
3. **Build a "researcher directs coder" agent.** Instead of building one giant AI that does everything, they trained a comparatively small model (27 billion parameters — think of parameter count loosely as "brain size") called Faraday to act like a lead scientist who plans the work and delegates the actual coding to a much bigger, more powerful coding AI (roughly 5 trillion parameters). Faraday decides what to investigate and how to scope it; the bigger coding AI does the typing.
4. **Train with reinforcement learning.** Faraday attempts many replication tasks, gets graded by the rubric judge, and its behavior is nudged — using a training method called GRPO — toward whatever it did on the highest-scoring attempts. A key engineering trick is scoring not just the final result but which specific *steps* in a long attempt deserved credit, which kept the training stable over very long, many-step tasks (something that normally breaks down).

## Where can this be used?

- **Any domain with expensive-to-check, hard-to-verify work** — legal drafting, technical writing review, engineering design reviews — where "was this done well" needs expert judgment rather than a pass/fail test, this rubric-judge recipe is a template for building a trainable reward signal.
- **"Small orchestrator + large tool" agent architectures** — instead of trying to build one enormous do-everything AI, train a smaller model to be a good project manager for an off-the-shelf powerful tool. This is directly applicable to building in-house agents that direct commercial coding assistants.
- **Auto-generating training/eval tasks at scale** from an existing corpus of documents (here, papers with figures) rather than hand-authoring benchmarks one at a time — relevant to any team building internal evals.

## Conclusions & takeaways

- A well-designed, human-validated LLM judge can be reliable enough to train on, even for genuinely open-ended, non-verifiable work — the key is keeping the rubric grounded in the specific case rather than generic.
- A small, specialized "director" model can out-perform much larger frontier models at a task by directing those same larger models as tools — capability doesn't only come from raw scale.
- The result generalizes: Faraday keeps winning when given more time/compute or a different (even stronger) coding tool than it trained with — a sign it learned durable skill, not a narrow trick.
- **Honest limitation:** "beats Claude Opus 4.8 and GPT-5.5" is measured on the paper's own judge and its own task distribution; the held-out set is still drawn from the same task-generation pipeline (redacted figures from papers), not an independently designed benchmark — worth remembering before treating the headline claim as settled science (see [[critical_thinking|Critical Analysis]]).

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| RL post-training | Extra training done *after* a model already works, using trial-and-error with a reward score, to sharpen a specific skill. |
| Rubric judge | An AI grader that scores an attempt against a written checklist tailored to that specific task, instead of just eyeballing it. |
| Coding-agent-as-tool (CAT) | An architecture where one AI (the "director") calls a separate, more powerful coding AI to do implementation work, like a manager assigning tasks to a specialist. |
| Rollout | One complete attempt by the AI agent at a task, from start to finish — the unit of experience used in RL training. |
| In-distribution vs. held-out | In-distribution = tasks similar to what the model trained on (here: ML papers); held-out = a different, unseen category (here: AI-for-science papers) used to test generalization. |
| GRPO | Group Relative Policy Optimization — an RL training method that compares several attempts at the same task to each other and reinforces the relatively better ones. |
| Turn-level credit assignment | Instead of grading only the final result of a long multi-step attempt, giving partial credit to individual steps along the way, so training knows which decisions actually helped. |
| Construct validity | Whether a test actually measures the thing it claims to measure (e.g., does a replication task really measure "scientific ability," or something narrower). |
| MIG slice | A carved-off fraction of a physical GPU (Multi-Instance GPU) — here, one-seventh of an Nvidia H200, the compute budget given per task. |
| Kendall τ | A statistic measuring how much two rankings (e.g., two judges' orderings of attempts) agree with each other. |

---

For the full picture, start at the [[index|wiki hub]].
