> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Methods: Replica Task Space & the Faraday Post-Training Recipe

**In one sentence:** The method turns a corpus of ~100 well-known papers into a scalable, auto-generated *Replica* task space in which an agent must replicate one results figure within a 60-minute budget on one-seventh of an H200, scores the inherently non-verifiable rollouts with a low-variance, rubric-based LLM judge (Codex GPT-5.5) validated against expert human rankings inside a deliberately minimal and maximally permissive agent harness that treats a frontier coding agent as a tool, and stably post-trains Qwen3.6-27B into *Faraday* with a modified GRPO recipe (LoRA, turn-level credit assignment) suited to long-horizon RL in a non-verifiable domain.

## Key points

- The **Replica** task space comprises **242 training tasks** (ML papers from 1990–2026) and **68 test tasks** (AI-for-science papers from 2012–2026) drawn from **100 well-known papers**; each task asks an agent to replicate one results figure from the paper given the original with the figure redacted, a **60-minute** limit, and a **single one-seventh MIG slice of an H200 GPU**.
- Tasks are **automatically generated** by three **Gemini 2.5 Pro** vision-language stages (scan → bounding-box localisation in an LLM-verifier repair loop → irreversible redaction), yielding a **scalable** task space; each paper contributes **1–13 tasks (median 2)** and every task is hand-checked and filtered for low quality (under-redaction, non-results plot, misidentified caption).
- Reward is **rubric-based**: **Claude Opus 4.7** auto-generates per-task rubrics over **five dimensions** (visual match, support for the scientific claim, implementation fidelity, compute-budget use, scientific integrity/no cheating); both the rubric generator **and** the policy are kept blind to the **"gold plot"** so the rubric captures claims (not figure details) and the model cannot game the criteria.
- Judging uses **Codex GPT-5.5 as a coding agent** given the same workspace, tools, git history (final plot), rollout trace and the gold plot, with **10 minutes** to explore and optionally **re-execute** the agent's code; each criterion is scored **0–1** and averaged, with **three judge samples** per rollout to cut variance.
- The rubric judge is **less noisy and more human-aligned** than a non-task-specific baseline: two rubric-judge draws agree at **Kendall τ 0.66** vs **0.46** (baseline) and **0.30** (two humans); it agrees with humans at **0.19** vs **0.15** (baseline); and **3 rubric-judge samples** match the noise-reduction of **8 baseline samples**.
- Human validation recruits **20 PhD-level participants** (preferring ICML/ICLR/NeurIPS main-conference publishers) who produced **117 rankings** of 3 or 6 rollouts each, paid **£150/task** with **£125 bonuses** at tasks 5 and 8, instructed to follow their own best judgement to capture tacit knowledge.
- The harness is **minimal and maximally permissive**: five function-calling tools (**apply_patch, read_file, list_dir, grep_files, shell**) — a Python re-implementation of a **Codex CLI** schema subset — with a **linear, append-only, un-compacted** history; a frontier coding agent (**GPT-5.4 mini** for most training, **GPT-5.5** for the final stage/eval) is used **as-a-tool (CAT)** via a Codex-CLI wrapper run through the shell tool, with a per-request configurable deadline.
- *Faraday* is obtained by **post-training Qwen3.6-27B** with **modified GRPO** using **LoRA (rank 128, α=128)** on all linear projections, a **128K-token** context and a **constant LR of 6e-6**; each Adam step draws a **batch of 10 tasks × 8 rollouts** sampled evenly over the corpus' year range so every epoch visits each task once and no single era dominates an update.
- **Long-horizon stability** in this non-verifiable RL setting is achieved by (a) using the **mean of three independent judge draws** as the rollout reward and (b) having the judge emit **turn-level credit weights u_k normalised so Σ u_k n_k = Σ n_k** (preserving reward scale), averaged over the three draws, to **scale per-token advantage** in GRPO — redistributing credit within a rollout without changing the update magnitude.

---

## The post-training pipeline (Figure 1)

![Pipeline for post-training Faraday on the Replica task space: ~100 source papers are converted into ~310 replicate-one-figure tasks by redacting a results figure; the policy runs rollouts in a container using Codex as a coding-agent tool; a per-task rubric generator and a rubric-based judge emit a reward plus per-turn credit weights, which drive a modified-GRPO update fed back into the policy.](images/fig1.png)

Figure 1 depicts the closed-loop, rubric-based RL recipe as a pipeline: a corpus of roughly 100 source papers is turned into ~310 *Replica* tasks, *Faraday* produces rollouts in a provisioned container while using Codex as a coding-agent tool, and a rubric generator + rubric-based judge supply a low-noise reward and per-turn credit weights that drive the GRPO update. The rest of this section unpacks each block: the task space (§3.1), the reward function (§3.2), the human studies that validate the judge (§3.3), the harness the agent acts in (§3.4), and the post-training recipe (§3.5).

## 3.1 Task space

The *Replica* task space comprises **242 training tasks and 68 test tasks drawn from 100 well-known ML and AI-for-science papers**. Each task requires an agent to replicate **one results figure** from a paper, given:

- the original paper **with the figure redacted**;
- a **60-minute time limit**;
- a **single one-seventh MIG slice of an H200 GPU** (a containerd container with helpful research libraries pre-installed);
- access to the internet, a **system prompt**, and a **task prompt** (Appendix G).

Where a paper's experiment cannot be completed within the budget, the prompt asks for the **most faithful scaled-down version** of the underlying experiment. Training tasks come from **ML papers (1990–2026)**; test tasks from **AI-for-science papers (2012–2026)**. Well-known papers are chosen "for ease of human rating" (Section 3.3).

### Automatic generation → a scalable task space

Tasks are automatically generated, so the task space is **scalable**. Given a paper, **three vision-language stages powered by Gemini 2.5 Pro** convert it into a task:

1. a **scan** that finds every main-text results plot and its caption;
2. a **localisation** stage that draws its bounding box inside an **LLM-verifier repair loop**;
3. **irreversible redaction** of the figure from the PDF.

A task is a **triple** of (caption, extracted figure — the "gold plot", and the paper with the figure redacted). Every task is inspected **by hand** and filtered if low quality — e.g. the figure is insufficiently redacted, it is not a results plot, or the caption is misidentified. Each paper contributes **1–13 tasks (median 2)**. Pre-training contamination is addressed in Appendix D.1.

## 3.2 Reward function

Paper replication is **inherently non-verifiable**, especially when scaling down experiments to fit resource constraints while remaining true to the core claim. In *Replica* tasks the "gold plot" (redacted figure from the original paper) helps judge replication attempts, but **perfectly reproducing the plot is not the same as a successful replication**: a good replication should also demonstrate strong experimental design, good scientific practice, faithfulness to the original paper, and strategic use of available resources. Designing a reward signal to train against is therefore a key challenge, and the **long-horizon** nature of the tasks demands that the signal be **low-variance across judge samples** and **consistent across similar rollouts**.

### Judge rubric generation

The judge is based on a **rubric** — a scoring guide giving specific criteria for assessing performance. Starting from a short, hand-designed meta-prompt, **Claude Opus 4.7** auto-generates **task-specific rubrics**. The "gold plot" is **hidden** from the rubric generator so the rubric captures the paper's **claims** without over-indexing on figure details (axis ranges, formatting, exact numerical values). The rubric is **also hidden from the policy** during training, encouraging broadly effective replications rather than gaming of the criteria.

The rubric covers **five dimensions**:

1. how closely the replicated figure **visually matches** the paper's;
2. how well the replication **supports the paper's scientific claim**;
3. whether the underlying experiment **actually implements and tests** what the paper describes;
4. whether the agent makes **good use of the compute budget**;
5. whether the agent acted with **scientific integrity** — adhering to its instructions and not cheating.

Because the time/resource limit often prevents full-scale replication, the rubric generator is instructed to **reward agents for producing a faithful scaled-down version**. This is a key feature of the task space: it introduces further **underspecification**, teaching decision-making skills characteristic of open-ended research.

### Coding agent as a judge

Rollouts are assessed using **Codex GPT-5.5 as a judge**, prompted with the appropriate per-task rubric. The judge is given the **same workspace and compute resources as the agent**, including the redacted paper, all the agent's tools, the replication codebase, and git history (containing the final plot), the **full interaction trace** of the rollout, and the ground-truth "gold plot". The judge is given **10 minutes** to explore these materials and form a judgement on each rubric dimension. Each criterion receives a **continuous score between 0 and 1**, and these per-dimension scores are **averaged** to give an overall score. Crucially, this lets the judge **fully examine and potentially re-execute** the agent's code to understand its process and check the robustness of its claims. During training the judge is **sampled three times per rollout** to reduce variance, and is additionally instructed to produce **credit-assignment weights** for each agent turn (see Section 3.5).

### Judge quality (Figure 3)

The paper reports (Figure 3) that this per-task rubric judge **achieves higher human agreement and lower noise** than a simpler baseline prompt that does not vary across tasks. On tasks selected to maximise disagreement between the two judges, **Kendall τ** (a rank correlation between two orderings; +1 = identical, −1 = reversed) measurements are: two **independent rubric-judge draws** agree at **0.66**, vs two **baseline judge draws at 0.46** and **two humans at 0.30**; the **rubric judge agrees with humans (0.19)** more closely than the baseline judge (**0.15**). For within-group noise (16 GRPO groups of 8 rollouts sampled uniformly across training steps 430–461, each rollout scored eight times per judge), the rubric judge is **less noisy at every sample count m** — in particular **eight baseline judge samples** are required to reduce the noise share to the level obtained with **three rubric-judge samples**.

## 3.3 Human studies

Human rankings of agent rollouts are collected to assess how well the rubric-based judge captures **human research taste**. For each rollout the human expert is given: the relevant paper with the figure redacted, the "gold plot" and its caption, a transcript of the rollout, and the git repository the agent generated (including agent instructions, code, outputs, and the resulting plot(s)).

The design choices are:

- Humans **rank either three or six rollouts** from best to worst, following simple instructions (Appendix G.4).
- They are instructed to **follow their own best judgement** about what a faithful replication should look like, to capture **human tacit knowledge**.
- They **justify their ranking** to encourage a principled, consistent approach (McDonnell et al., 2016).
- They **explain what effect the "gold plot" shows** and **suggest a correct methodology** to reproduce it.

Given the task's complexity, participants are drawn from a pool of **ongoing or completed PhDs from top research universities**, preferring those who have **published at least one paper in the main conference track of ICML, ICLR, or NeurIPS**. Pay is **£150 per task**, with **bonuses of £125** on completing the fifth and eighth tasks. In total, **117 rankings from 20 participants** are collected (Appendix F describes how the tasks and rollouts were chosen).

## 3.4 Simple harness

An agent harness is an interface between an LLM (tokens-in/tokens-out) and an environment (action-in/state-out); here the environment is an interface to a container. The *Faraday* harness is designed around **three principles**: it should be **simple and interpretable**; **maximally permissive**, giving the agent the same context and affordances a human has when doing AI research; and its **tool set should be minimal, deliberate, and legible** to contemporary models. *Faraday*'s scientific capability is improved by **changing its policy weights, not by complexifying its harness**. The harness system prompt is in Appendix G.1.

### Affordances and context

The agent acts via **five function-calling tools**: `apply_patch`, `read_file`, `list_dir`, `grep_files`, and `shell`. *Faraday* can detach background processes with the `shell` tool, taking many turns while running several commands in parallel. The tool interface is a **subset of the Codex CLI schema (OpenAI, 2025), re-implemented in Python**. The conversation is a **linear, append-only history with no compaction**; a turn's tool calls execute **concurrently** and their results are appended **in call order**. **Context overflow (exceeding the per-turn 16K-token limit)** and inference **end the rollout**, and the partial rollout is **judged like any other**. A rollout otherwise ends when *Faraday* replies **without tool calls** or when its **wall-clock time is exhausted**.

### Coding agent as a tool (CAT)

*Faraday* is given a **frontier coding agent to use as a tool**: a wrapper script runs the **Codex CLI non-interactively**. *Faraday* invokes it through the `shell` tool and receives a **rendered transcript** of the coding agent's commands, outputs, and messages with **per-step timings**. **Successive invocations resume the coding agent's previous session by default**, though *Faraday* can reset context or run multiple coding agents in parallel. The wrapper enforces a **deadline configurable by *Faraday* per-request**; if exceeded, a **partial transcript** is returned. The coding-agent model is a **runtime parameter**: **GPT-5.4 mini** for most of the training, and **GPT-5.5** in the final stage and for evaluation.

## 3.5 Post-training recipe

To obtain *Faraday*, the team **post-trains Qwen3.6-27B in the Faraday harness on the Replica task space**, using a **modified version of GRPO (Shao et al., 2024)**. Hyperparameters:

- **LoRA fine-tuning** (Hu et al., 2022), **rank 128, α = 128**, with adapters on **all linear projections**;
- a **128K-token context window** (sufficient for *Replica* tasks given the 1-hour training time limit);
- a **constant learning rate of 6×10⁻⁶**;
- **Adam** (Kingma & Ba, 2014); each optimiser step draws a **batch of 10 tasks with eight rollouts apiece** from the 242-task train split;
- tasks are sampled so **every batch spans the corpus' year range evenly**, and **each epoch visits every task exactly once**, so no single era of science dominates any update.

Appendix D.2 has further training details; Appendix H describes the infrastructure.

### Long-horizon stability

Post-training requires **long-horizon RL in a non-verifiable domain**, a setting known to be prone to **instability and collapse**. Two sources of instability are the **high variance of the reward signal** and **uniform credit assignment**. Two train-time judge modifications address this:

1. **Rollout-level reward** uses the **mean of three independent judge evaluations**.
2. The judge is instructed to produce **turn-level weights** attributing credit over the rollout's turns. It emits a weight distribution **u_k over turns k**, normalised so that **Σ u_k n_k = Σ n_k** (where **n_k** is the number of tokens in turn k), so the overall reward scale is **unchanged**. The normalised weights are **averaged turn-wise over the three judge draws** (preserving the normalisation), and the resulting turn weight is used to **scale the per-token advantage during GRPO**. This **redistributes credit within a rollout without changing the overall magnitude of the update**.

Figure C.1 explores empirically how the method assigns credit within each rollout; these techniques helped achieve **stable training** (ablations in Appendix B).

**Covers:** Section 3 Methods — 3.1 Task space, 3.2 Reward function, 3.3 Human studies, 3.4 Simple harness, 3.5 Post-training recipe (incl. Figure 1 pipeline schematic and the Figure 3 judge-agreement/noise results); source pages of `source/chunks/03.txt`.
