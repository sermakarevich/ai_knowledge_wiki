> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents — In Plain Language

## What is this about?
This paper asks a simple question: when should an AI agent decide what to remember?

Most agent memory systems do it at "write time." After finishing a task,
they distill what happened into a fixed note — a reflection, a workflow,
a skill — and file it away for later. The problem: at that moment,
the agent does not know what future task that note will serve.

Just-in-Time Memory (JITMEM) flips this around. It keeps the raw record
of each completed task — the full trajectory of observations and actions —
and only distills it at "read time," when the new task is already known.
A curator model looks at the new task plus a few relevant past episodes
and writes a short, task-specific briefing that the agent (executor) uses
right away.

In short: don't summarize before you know the question. Keep the raw tape,
then cut a custom briefing for each new job.

## Why does it matter?
Three reasons this timing shift is a big deal:

1. **Deciding early destroys information.** A single episode holds many
   possible lessons, but a write-time summary keeps only one fixed version.
   Whatever is discarded is gone forever, even if a later task needed it.

2. **Learning what to store is hard when the payoff is far away.**
   A write-time storage decision may only prove useful many tasks later,
   which makes training the curator a difficult long-horizon guessing game.

3. **Curating late is easier to learn and works better.**
   Because the briefing is used on the current task immediately,
   the curator gets instant feedback: did this briefing help or not?
   No waiting, no artificial grouping of "related" tasks.

The results back this up. Across three benchmarks — ALFWorld (household tasks),
WebShop (online shopping), and τ2-bench (customer service) — JITMEM beats
the strongest write-time methods by 16.2, 16.3, and 3.9 success-rate points.
Strikingly, even the *untrained* curator already matches or beats strong
baselines; training on task success compounds the gain. It also uses roughly
half the input tokens and ~30% fewer steps than write-time methods.

## How does it work?
JITMEM runs a four-step loop on every task: retrieve, curate, execute, update.

**1. Retrieve.** Given the new task, a simple BM25 search over task
descriptions pulls the top-3 relevant raw trajectories from the memory bank.
Retrieval is fixed and untrained — it matches on the task text only.

**2. Curate.** The curator (a Qwen3-8B model) reads the new task plus the
retrieved episodes and writes a compact natural-language briefing:
which past experiences matter, what strategies they suggest, and what
concrete guidance applies right now. The same stored episode can produce
a different briefing for a different task — e.g., one past kitchen episode
yields "how to heat and cool" for a potato task but "where to place things"
for a newspaper task.

**3. Execute.** A frozen executor model (Qwen3-8B, Gemini-2.5-Pro, or GPT-5.4
in the experiments) acts on the task with the briefing prepended to its prompt.
The briefing is ephemeral — it is used once and never stored.

**4. Update.** After the task, the executor itself acts as judge: was this
a success? Only successful trajectories are appended to the bank as raw,
unsummarized records, keeping the bank stocked with positive examples.

**Training.** Only the curator is trained, using GRPO reinforcement learning
without a value network. For each training task it generates a group of
candidate briefings, the frozen executor tries each, and rewards (binary
success on ALFWorld/τ2-bench, continuous score on WebShop) produce advantages
relative to the group mean. Because feedback is immediate, training is a
simple single-step objective — no task grouping or reward shaping needed.
Training runs up to 100 steps on a fixed bank of successful base-executor runs;
evaluation starts each test sequence from an empty bank (cold start).

Ablations confirm each piece matters: replacing raw storage with write-time
distillation costs 2–8 points; removing retrieved trajectories costs up to
~15 points; staged bank refreshes and warm-starting the test bank barely help.

## Where can this be used?
Anywhere an LLM agent repeats related tasks and can learn from its own history:

- **Household / robotics simulators (ALFWorld):** cleaning, heating, placing
  objects — the curator assembles procedures from partially relevant episodes
  (e.g., "locate plate → clean in sink → place on countertop").
- **Web shopping agents (WebShop):** phrasing searches, picking products,
  setting color/size options, checking price limits before buying.
- **Customer-service agents (τ2-bench):** diagnosing issues step by step
  (e.g., MMS failures: check device state first, account blockers later),
  with explicit user confirmation before mutating actions like `refuel_data`.
- **General pattern:** any agent with an episodic log — coding assistants,
  support copilots, workflow automation — can keep raw traces and brief
  itself per task instead of maintaining hand-written playbooks.

A practical bonus: one trained curator transfers across executors without
retraining (a Qwen3-8B curator serving GPT-5.4 lands within 1.4 points of
a GPT-5.4-trained one), and the extra cost is just one curator call per task.

## Conclusions & takeaways
- **When you curate matters as much as what you store.** Deferring
  distillation until the task is known beats fixed write-time summaries.
- **Raw retention wins.** Keeping full trajectories preserves options;
  write-time distillation loses 2–8 points in ablations.
- **Immediate feedback simplifies learning.** Read-time curation turns
  memory training into a single-step task-success objective.
- **The untrained version is already strong** — task-adaptive briefing
  itself is a major source of gain; RL training adds large wins on top.
- **Efficient and portable:** ~50% fewer input tokens, ~30% fewer steps,
  and cross-executor transfer without retraining.
- **Limits:** the retriever is plain BM25, each task costs one extra LLM call,
  and briefing formats are hand-designed — all future-work directions.

## Jargon decoder
| Term | Plain definition |
|------|------------------|
| Write-time curation | Summarizing an episode into a fixed note right after it finishes, before future tasks are known. |
| Read-time (just-in-time) curation | Waiting until a new task arrives, then writing a custom briefing from past episodes for that task. |
| Trajectory | The full raw record of one task: the request plus every observation and action. |
| Memory bank | The stored collection of past successful raw trajectories. |
| Curator | The model that reads retrieved episodes and writes the short task-specific briefing. |
| Executor | The (frozen) agent model that performs the task using the briefing. |
| Payload / briefing | The short ephemeral guidance note the curator writes per task; used once, never stored. |
| BM25 retrieval | A simple keyword-based search used here to find relevant past tasks by description. |
| LLM-as-judge | Using the executor model itself to decide whether a finished trajectory counts as success. |
| GRPO | The reinforcement-learning algorithm used to train the curator from grouped task-success rewards. |
