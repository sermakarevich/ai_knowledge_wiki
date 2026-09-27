> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix Worked Examples: Prompts, Task, Rater Guide, Optimized Prompt & Rubrics

**In one sentence:** The appendix reproduces the full artifact set used to run and grade rollouts — the agent's system prompt (a researcher delegate-coding paradigm), the per-task "plot replication" prompt, the human rater guide, an optimized Codex prompt distilled from failure modes, and three randomly drawn per-paper grading rubrics — plus a description of the Kubernetes/Ray/NeMo-RL infrastructure running it all.

## Key points

- The agent system prompt casts the model as "a researcher, not a coder": it must plan, then delegate ALL implementation to a `coding_agent.py` subagent via `python coding_agent.py "<prompt>"` (with `--fresh` to reset the session and `--budget` to check tokens), and must make many small, scoped calls rather than one giant prompt, since course-correcting a giant call means cancelling and restarting (wasted budget).
- An "Authenticity" rule is central: "Never simulate or fabricate experiments" — fabricating results, hard-coding expected values, or mocking runs "will score 0"; a clearly-documented scaled-down version (smaller model, fewer steps, fewer seeds) is acceptable, fabrication is not.
- The task prompt (Appendix G.3) hands the agent a `paper.pdf` with one plot removed, a `caption.md`, and a 1-hour wall-clock budget checked via `./check_time.sh`; required outputs are `plot.png` and a graded `writeup.md` (explicitly "REQUIRED. This is graded and easy to forget"), with the whole git commit history assessed, not just the final artifacts.
- The task forbids downloading the original paper, using paper-specific code found online, hard-coding data deduced from elsewhere in the paper, and guessing; it rewards "best-effort within constraints over fabrication," and penalizes *unnecessary* scaling-down when the original scale is feasible. Available env credentials: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `HF_TOKEN`; GPUs may be NVIDIA MIG slices (read the "MIG devices" section since `memory.total` renders `[Insufficient Permissions]`).
- Claude Opus 4.8 and GPT-5.5 baselines (Appendix G.2) use Claude Code's and Codex's built-in system prompts plus a one-line user prompt: "Read prompt.md to understand your task, then complete it."; in the CAT paradigm Codex's initial prompt is decided by the calling agent.
- The optimized Codex prompt (G.5) encodes observed failure modes: agents "submit at minute –1220 with 40+ min unused" (i.e., far too early); it demands training the real mechanism (never proxy/oracle/tuned prior; if infeasible, still run the "SMALLEST FAITHFUL REAL SLICE" — one model × one cell — before allowing proxy), reproducing the difference in direction AND magnitude, ≥3 seeds averaged with real error bars, and a write-up where every quantitative claim is "READ OFF the final artifacts" — a contradicting number "halves the write-up score."
- Rubrics (G.6) are generated per task, each specific to the figure graded; each scores four dimensions — visual fidelity, claim reproduction, implementation fidelity, experimental effort — with concrete 0.0 / 0.5 / 1.0 worked examples. Three rubrics are shown, drawn "uniformly at random": Zucchet et al. 2025 (hallucinations/knowledge co-emergence, Fig. 5), Friedman et al. 2000 (LogitBoost additive coordinate functions, Fig. 5), and Gers et al. 2002 (peephole vs traditional LSTM on NMSD timing, Fig. 4).
- Infrastructure (Appendix H): Kubernetes clusters of Hopper and Blackwell GPUs with Kueue managing whole-GPU, MIG-slice, and CPU-only quotas; each training run is a Ray job with its own RayCluster across trainer and generation node pools; RL framework is a fork of NeMo-RL with Megatron-Core (tensor + context parallelism over the full 128K-token context) and vLLM serving, with policy weights refit in place so in-flight rollouts continue on newer weights; Qwen3.6's hybrid gated-delta-net layers get custom sequence-packing + context-parallelism support; rollouts flow through a NeMo-Gym fork decomposed into model/agent/resources HTTP services; every rollout gets a fresh container pod (CUDA, Python, ML stack, coding-agent CLI), the resource server enforces wall-clock deadlines and runs the judge inside the container at evaluation time.

---

## G.2 Claude and Codex baselines (system prompt + initial user prompt)

The baselines are run with the harnesses' own built-in system prompts (Claude Code for Claude Opus 4.8; Codex for GPT-5.5). The only added text is the initial user prompt (with `prompt.md` = the task prompt of Appendix G.3):

> Read prompt.md to understand your task, then complete it.

When used in the CAT (calling agent) paradigm, Codex's initial user prompt is instead decided by the agent calling it.

## G.1 (implicit) Agent system prompt (CAT paradigm)

The main system prompt given to the trained agent (pages 37–38 of the paper) has the following sections:

### Role

> "You are a researcher, not a coder. Your job is to plan experiments, analyze results, and iterate toward the goal described in your prompt. You have a coding agent available for all implementation work — delegate coding tasks to it rather than writing code yourself."

Tools: `shell` (also used to invoke `coding_agent.py`), `apply_patch` (`* Add File:` to create/overwrite, e.g. `writeup.md`; `* Update File:` for surgical edits), `read_file`, `list_dir`, `grep_files`.

### Coding Agent

The subagent has its own shell, reads/writes files in the working directory, but does NOT share conversation context and does NOT see the task or system prompt — "any context it'll need — available GPU resources, time guidance, API keys in the env, etc. — must be threaded through in the prompt you pass it."

Invocations:
- `python coding_agent.py "<detailed prompt>"` — resumes the previous coding-agent session by default (first call starts fresh).
- `python coding_agent.py --fresh "<detailed prompt>"` — new session.
- `python coding_agent.py --budget` — check remaining token budget.

Prompts containing shell-significant characters must go via a quoted heredoc with `-` as the argument:

```
python coding_agent.py - <<'EOF'
Implement foo. Use this snippet as reference:
```python
def bar(): ...
```
EOF
```

(The single quotes around `'EOF'` make bash pass the body through literally.) No timeout is required, but the agent may instruct how long to run. Output token budget: `{coding_agent_budget}` tokens (a template variable).

> "**Make many small calls, not one big one.** Each call should have one clear deliverable. Scoped calls give short feedback loops. One giant all-in-one prompt is an anti-pattern — course-correcting means cancelling the whole call and restarting, which wastes a lot of budget."

### Workflow

1. **Plan first.** Read the prompt and AGENTS.md, then make a plan.
2. **Execute iteratively.** Delegate coding; run experiments; evaluate; adapt.
3. **Persist.** Keep going autonomously until fully resolved — don't ask for clarification, make reasonable decisions; pivot quickly.
4. **Monitor your time budget.** Wrap up with enough time for final deliverables.

### Authenticity

> "**Never simulate or fabricate experiments.** Always run experiments for real. Fabricating results, hard-coding expected values, generating fake data, mocking experiment runs, or producing predetermined outputs that did not come from actual execution will score 0. If the original scale of an experiment is infeasible within the available compute and time, run a clearly-documented scaled-down version (smaller model, fewer steps, fewer seeds) — that is acceptable; fabrication or simulation is not."

### Finishing / Rules

When done: respond with a brief summary and no tool calls (ends the rollout). Rules: use `apply_patch` for all file writes (never rewrite whole files via shell; `* Update File:` is for targeted edits located by `@@` context, 3 lines of context above/below each change); explore with `read_file`/`list_dir`/`grep_files`; long-running work (training, builds, `coding_agent.py` delegations) should run with `background: true`, polled via `job_output("<job_id>")` and stopped via `kill_job("<job_id>")` (do not set `timeout_ms` together with `background: true`); never expose secrets/API keys.

### Hardware

If the task implies a GPU, **assume a CUDA GPU is available and use it** — CPU training "will time out and score zero." Check with `nvidia-smi`. Move HuggingFace models to CUDA explicitly (`.to("cuda")` or `device_map="cuda")` — default `.from_pretrained()` leaves the model on CPU. When delegating, include GPU info and API-key availability in the prompt, since the inner agent does not inherit it.

### Runtime Paths

Working directory: `/home/agent/task`. Write exactly two files: `plot.png` and `writeup.md`.

## G.3 Task prompt

### Objective

> "You have been given a research paper (paper.pdf) from which one experimental plot has been removed. Your goal is to replicate the missing plot by reproducing the experiments described in the paper. The caption for the missing plot is provided in caption.md. Your replicated plot MUST be the result of running real experiments. You must also produce a write-up (`writeup.md`) that clearly documents your approach, any scaling or simplification choices you made, and what your results show."

### Reading the paper

`pymupdf` is pre-installed; a suggested dump:

```python
import pymupdf
doc = pymupdf.open("paper.pdf")
text = "\n".join(page.get_text() for page in doc)
```

"it's there so you don't need to spend turns installing a PDF library."

### Time budget

"You have 1 hour(s) to complete this task. Check how much time is left with `./check_time.sh`." Extra time refining the plot, running more seeds, or sanity-checking "may well improve the result," but don't pad with busywork; "do not return to the user mid-task to ask for clarification — make reasonable decisions and keep going autonomously."

### Available compute

GPUs may be NVIDIA MIG slices abstracted away — "any GPUs you see are yours alone." Run `nvidia-smi` first; on a MIG slice read the "MIG devices" section for actual memory and avoid `nvidia-smi --query-gpu=memory.total` (rendered `[Insufficient Permissions]` on MIG slices).

Env credentials: `OPENAI_API_KEY` (OpenAI), `ANTHROPIC_API_KEY` (Anthropic), `GEMINI_API_KEY` (Google Gemini), `HF_TOKEN` (Hugging Face — `huggingface_hub`/`transformers`/`datasets` pick it up automatically, so gated models like Llama or Gemma "will just work").

On infeasible experiments: "do the most faithful scaled-down version you can: smaller model, fewer steps, fewer seeds, etc… The judge has been told to reward best-effort within constraints over fabrication, so a clearly-documented scaled-down implementation is better than a fake-but-pretty plot." But if the original scale IS feasible: "you should do that, and you will be penalized for unnecessarily scaling down or simplifying/modifying experiments."

### Rules

- MUST NOT look up or download the original paper PDF from the internet.
- MUST NOT use existing implementations found online that are specifically related to or derived from this paper; other online resources (ML frameworks, code from cited papers) are OK.
- MUST NOT guess or fabricate the plot; MUST NOT hard-code the plot by deducing data from elsewhere in the paper.
- MAY use the rest of the paper to cross-check the generated plot, so long as it came from real implemented experiments.
- Otherwise free to use the internet, write/execute code, install packages — ethically.
- NEVER delete or modify `/home/agent/task/logs` (written automatically for future human inspection).
- Abide by the spirit of the rules: "You must not cheat."

### What is a good replication?

Faithful code implementing the methodology (accounting for compute/time); principled, accurate reproduction of the removed plot — "It is more important to reproduce the scientific claim and overall trend than it is to get an exact match on specific datapoints." If a method is the core novelty, reimplement it fully; rely on libraries for non-core aspects.

### Output

- `git init` at start; commit provided files (PDF, caption, prompt) with a descriptive message.
- Save the replicated plot as `plot.png`; commit plot and code on every save/modify.
- "You will be assessed on the whole commit history, not just the final plot."
- **Write-up — REQUIRED. "This is graded and easy to forget, so do not skip it."** `writeup.md` covering (1) what was implemented, how, and why, and (2) observations on the results. Create it EARLY and keep updating it. "The judge can only credit work it can see: if `plot.png` or `writeup.md` is missing when the time expires, you will be scored as if that part of the work was never done."

## G.4 Human prompt (rater guide)

> "We're evaluating how well AI agents can replicate results from research papers, a test of whether they can do genuine scientific work on underspecified problems."

Each agent got a paper with one figure removed and tried to regenerate it by coding from scratch and running experiments; raters compare and rank several attempts at the same figure. Exact formatting/axes/layout match is **not** required — "A good replication is about the science and not just the final plot. The transcript and write-up are the main evidence for the process behind it."

**What you must look at:** the agents' instructions (the exact prompt every agent received); the materials PDF (paper, original "gold" figure + caption, and each rollout's figure and writeup); the trajectory viewer (transcript per rollout); the GitHub repo (workspace per rollout).

**How to rank:** first answer "Summarize the task" questions; then drag rollouts into order (best at top), giving a per-rollout rationale citing something specific; finally describe the overall decision process. "Trust your judgment — there's no answer key beyond the gold figure and the paper." (Beta note: on bugs, hard-refresh, else email [redacted] for support.)

## G.5 Optimised Codex prompt

> "You have 60 minutes and a GPU (an H200 slice) to reproduce ONE figure from a paper. Scored on: (1) figure format, (2) the plot reproduces the paper's qualitative trend, (3) you implement the paper's ACTUAL mechanism, (4) effort/rigor, plus integrity and write-up accuracy. Integrity, disclosure, and figure honesty are largely solved; remaining losses are on fidelity, trend/magnitude, misread constants, and stopping early / skipping the real anchor on hard tasks."

### 1. Read the goal first — restate the spec in writing

Before coding, write down (and put in `writeup.md`): exact panels/axes/legend/units; the ONE qualitative claim; the EXACT quantity each axis names; the FULL list of conditions/curves/model-arms/classes; the EXACT task setup (positive class, subset, split, metric, precise equation/algorithm); and every load-bearing CONSTANT (sizes, counts, |H|, step budgets). Match values in/around the TARGET figure itself — "when a constant differs between the target figure and the paper's body text (e.g. |H|=10^5 vs 10^6), follow the TARGET FIGURE." Cited misread failures: "class-4-vs-rest done as class-3-vs-4; a chi-square boundary instead of the additive one; omitting model arms the figure includes." Before submitting, DIFF the figure against the list: every arm/panel present, right construction and constants, no extra/missing panels.

### 2. Implement and TRAIN the real mechanism — never a proxy, oracle, or tuned prior

"Fidelity is graded on whether the real mechanism actually ran — disclosure earns NO credit."

- Build the real architecture/algorithm and TRAIN it from standard init with a real LR; when it doesn't converge, ITERATE on the training (LR search, better init/curriculum, more steps, larger batch on GPU) — "never pivot to hand engineering the answer."
- For LLM/agentic mechanisms, CHECK FEASIBILITY: if the real pipeline runs in-budget, use it; if it genuinely cannot, "you MUST STILL run the SMALLEST FAITHFUL REAL SLICE (one model × one cell, a few real ideas/samples per arm) to anchor the result, then clearly label the rest as proxy." Only if even a 1×1 real cell is truly impossible may you go full proxy — and log the specific reason.
- NEVER feed the gold answer (oracle), hand-tune per-arm priors/profiles, add off-paper objectives, or retune a proxy to the paper's magnitude after seeing results.
- If scaling down, PRESERVE the property the figure tests (async parallelism, the learned component, pixel inputs, enough steps to plateau) and trade BREADTH (fewer games/points/examples/seeds); still reproduce all panels/sweep points.
- Never fit/select params on the eval stream, run a ≈lr0 pass, or select a data window/split/seed after seeing the trend; every plotted number comes from post-training weights and completed measurements, rendered directly from the results CSV. Use the real dataset/environment (verify by importing/installing), on GPU.

### 3. Reproduce the DIFFERENCE — direction AND magnitude, honestly

The plot must exhibit both the ordering AND the magnitude. "If your arms look identical when the paper's differ, the setup is wrong (too small/short, wrong regime, or a proxy/oracle/tuned prior masking it) — fix the SETUP." But if the magnitude is genuinely unreachable at your scale, "REPORT the honest value and say so — never select a training horizon, budget, stopping point, or seed that recovers the paper's expected direction. An honest miss scores far better than a manufactured match."

### 4. Use the full budget on the right things

> "The most-ignored rule: agents submit at minute –1220 with 40+ min unused."

Do NOT submit with more than ~5 min of budget remaining (unless the minimal real anchor was run or its impossibility logged). "A plausible-looking figure is NOT done." With time left, in priority order: run the minimal real slice skipped; complete missing arms/panels/sweep points; harden the weakest condition; add seeds until error bars tighten; add a real baseline — "NEVER retune toward the target." At ~30 min check the effect is appearing on GPU. Rigor: ≥3 seeds/runs AVERAGED with real error bars, including LLM/agent tasks.

### 5. Integrity

Every number from a real run; never hardcode, fabricate, fit to reported values, handicap a baseline, feed in gold answers, hand-tune priors, retune a proxy to the paper's magnitude, or select seeds/windows/splits/training-horizons/stopping-points after seeing results. Fix hyperparameters before seeing results; any tuning applies symmetrically to all conditions and is disclosed.

### 6. Figure honesty + write-up self-consistency (cheap points lost here)

- Axis labels must reflect the ACTUAL quantities run — "never put paper-scale labels (e.g. '85M params', the paper's step counts) on a smaller proxy." Plot the FULL window even where the result fails or is unfavorable — "cropping to a favorable sub-window (e.g. a single spike) is both a trend loss and an integrity violation."
- Self-consistency pass: every quantitative claim in `writeup.md` (seed count, epoch count, per-panel sample/image counts, dataset sizes, CI/t-multipliers, filenames/paths, figure's data source) must be "READ OFF the final artifacts (code/CSV), not estimated or copied from the paper." A contradicting number (e.g., "a '3 seeds' claim over a 10-seed run, a per-panel count that doesn't match, a stale CSV path, a wrong render source") "halves the write-up score." Same for METHOD/PROCEDURE descriptions — "The same applies… describing the paper's setup when the code ran a different one also halves the write-up score."
- Checklist: figure diffed against the §1 spec; axes uncropped, full window; magnitude reproduced or its absence stated; ≥3 seeds with error bars; figure rendered from the results CSV; contrast VISIBLE; plot and write-up describe the SAME results. Include two attestations in `writeup.md`, both factual and minimal, written from the FINAL run only: `real slice: <ran the real mechanism / 1×1 real cell / impossible because …>` and `budget used: <N>/60 min` where N is elapsed time read verbatim from the environment timer (e.g. `check_time.sh`). A budget/seed/source figure that contradicts the logs halves the write-up score. Disclose EVERY post-hoc/proxy choice; never claim a figure was "matched" when panels/magnitude are missing or call a hand-built component "learned."

**Deliverables:** `plot.png` (matching reference format, all panels/sweep points), runnable code, results CSV(s), and `writeup.md`.

## G.6 Example rubrics

> "Rubrics are generated per task, so each one is specific to the figure it grades. The three below are drawn uniformly at random."

Each rubric has four scored dimensions: **1. Visual fidelity**, **2. Claim reproduction**, **3. Implementation fidelity**, **4. Experimental effort**, each with 0.0 / 0.5 / 1.0 worked score examples.

### Rubric: "How do language models learn facts?" (Zucchet et al., 2025), Figure 5

Preamble: the figure argues that hallucinations — measured as overconfidence in wrong attribute predictions — emerge during pre-training at the same time knowledge is acquired, hurting later fact integration; the middle/right panels show fine-tuning on new individuals rapidly degrading pre-training performance while new knowledge is learned slowly, with replay of pre-training data only partially mitigating it. It is "a conceptual demonstration on the paper's synthetic-biography setup, so the rubric focuses on whether the three-panel comparison is present and shows the qualitative dynamics, not on quantitative match."

1. **Visual fidelity.** Left panel: over pre-training steps, a knowledge-acquisition curve co-emerging with a hallucination/overconfidence signal. Middle/right: two curves each as fine-tuning progresses — attribute loss on pre-training individuals (rising rapidly early) and on fine-tuning individuals (decreasing more slowly), grey dots marking start-of-fine-tuning performance; right panel adds replay. **0.0:** single-panel plot unrelated to the fine-tuning/hallucination dynamics, or panels with only pre-training curves. **0.5:** all three panels with sensible axes but missing grey markers, mislabeled losses, or hallucination collapsed into a single accuracy curve with no calibration signal. **1.0:** three panels matching the caption's structure with reasonable labels/legends, even if colors, fonts, or tick placements differ.
2. **Claim reproduction.** Three connected claims: (i) overconfidence co-emerges with knowledge in pre-training; (ii) fine-tuning produces a fast rise in pre-training loss and slower fall in fine-tuning loss; (iii) replay partially rescues final pre-training loss but does not prevent the initial spike. **0.0:** middle/right show pre-training loss unchanged/improving, or replay panel with no benefit, unacknowledged. **0.5:** forgetting dynamic present in the middle but replay panel identical to no-replay, or left panel lacking any overconfidence signal — with limited acknowledgement. **1.0:** visible co-emergence on left; rapid pre-training-loss increase with slower fine-tuning-loss decrease in middle; replay softens final level but initial jump remains — or honest flagging of any sub-claim that didn't reproduce.
3. **Implementation fidelity.** Requires the synthetic-biography setup: individuals with several attributes, a transformer trained to predict attributes, attribute-level loss measured separately on pre-training vs held-out fine-tuning populations, and a fine-tuning phase with/without replay; the hallucination signal must reflect confidence on inaccurate predictions, not just accuracy. Scaling down model size, individual count, or steps is fine when comparisons are preserved. **0.0:** fine-tuning a public LLM on unrelated text, or token-level cross-entropy on web data. **0.5:** correct biographies/split but conflated populations into one loss, accuracy as hallucination stand-in, or "replay" implemented as continuing pre-training. **1.0:** small transformer on synthetic biographies, cohort split, separate attribute losses, plain vs replay fine-tuning, left-panel signal from confidence on incorrect answers.
4. **Experimental effort.** Judged by iteration toward a working three-panel comparison, not wall-clock: re-running fine-tuning after noticing missing dynamics, tuning LR/steps to make the fast-drop/slow-rise pattern visible, replay as an actual second run. **0.0:** stops after one failed run, placeholder plots, or fabricated curves. **1.0:** gets pre-training working, fixes the forgetting panel (LR/steps/eval split), runs replay as a separate experiment — even at reduced scale with one seed.

### Rubric: "Additive logistic regression: a statistical view of boosting" (Friedman et al., 2000), Figure 5

Preamble: the nested-sphere example (Section 6) uses ten independent standard-normal inputs with the class label determined by whether |x|² exceeds the median of χ²₁₀ — "the true log-odds depend only on the sum of squared coordinates and the problem is exactly additive in x_j²." Figure 5 shows the coordinate functions f_j(x_j) of the additive logistic model fit by LogitBoost with stumps: boosted stumps recover this additive structure, each f_j a smooth symmetric roughly quadratic function, the ten panels essentially interchangeable.

1. **Visual fidelity.** Ten coordinate-function panels (one per input dimension), each plotting fitted f_j vs x_j over a standard-normal support — "ten near-identical symmetric curves rising on both tails — not error curves, not decision boundaries, not a single 2-D plot." **0.0:** test-error-vs-iterations curve, 2-D decision boundary, or single-panel scatter. **0.5:** per-coordinate plots but wrong number of dimensions (2 or 5 instead of 10), or panels plotting something else (e.g., variable-importance bars). **1.0:** ten labeled panels showing f_j(x_j) over roughly a standard-normal range; cosmetic differences cost nothing.
2. **Claim reproduction.** Each f_j should be smooth, symmetric, roughly U-shaped (or inverted-U, sign depending on class coding), and the ten panels essentially the same up to noise; divergence (asymmetric/non-quadratic) should be flagged. **0.0:** flat, monotone, or wildly differing coordinate functions, unacknowledged. **0.5:** some panels symmetric, others noisy/monotone, or too few boosting iterations so the quadratic shape is only faint. **1.0:** ten clear symmetric U/inverted-U panels visually similar across coordinates — or honest note of residual asymmetry with the dominant symmetric shape visible.
3. **Implementation fidelity.** Requires (a) the Section-6 nested-sphere generator — 10 i.i.d. standard-normal coordinates, class thresholded on |x|² at the χ²₁₀ median — and (b) LogitBoost with depth-1 stumps run until coordinate functions stabilize; f_j extracted by aggregating, per dimension, the contributions of all stumps splitting on that dimension. scikit-learn or hand-rolled LogitBoost both valid, given the Newton-style weighted-least-squares update on working responses; logistic-loss gradient boosting on stumps is an acceptable close substitute. **0.0:** a different model (single tree, neural net, AdaBoost with deep trees) on a different dataset. **0.5:** correct DGP but multi-split trees (breaking additivity), or stumps with a marginal sweep (one coordinate varied, others fixed at zero) instead of per-dimension stump aggregation. **1.0:** Section-6 nested spheres (~2000 training points), LogitBoost-with-stumps, f_j from per-dimension stump contributions; budget-driven reductions in iterations/size are fine.
4. **Experimental effort.** About engaging with the additive-recovery comparison: getting LogitBoost on stumps running, iterating on noisy/asymmetric coordinate functions, producing ten interpretable panels. **0.0:** no figure, or an obviously broken first attempt with no diagnostic or rerun. **1.0:** fits, inspects, and reruns with more iterations/a fix when early curves are too noisy — or a clean first result with symmetry validated and no time burned on cosmetics.

### Rubric: "Learning precise timing with LSTM recurrent networks" (Gers et al., 2002), Figure 4

Preamble: the figure asks how the training cost of the NMSD task (delay set I(n)∈{0,1}) scales with the minimum spike interval F, and — "crucially for the paper's central claim" — whether peephole connections from the CEC to the multiplicative gates let LSTMs learn precise timing more efficiently than traditional (forget-gate) LSTM. "Showing peephole LSTM trained with substantially fewer streams than traditional LSTM, particularly at larger F, is the empirical evidence the paper uses to motivate peepholes. This is a **specific empirical comparison**."

1. **Visual fidelity.** Line/curve plot: x-axis = minimum spike interval F, y-axis = average number of training streams to solve NMSD with I(n)∈{0,1}. Expected to show separate curves for peephole and traditional LSTM (or where one variant failed); y-axis plausibly logarithmic. **0.0:** axes unrelated to streams-vs-F (e.g., loss over epochs), or a single unlabeled line with no variant comparison. **0.5:** correct axes but only one curve (peephole alone) with no traditional-LSTM baseline. **1.0:** labeled curves for both variants over the F range, linear or log y-axis — cosmetic differences OK.
2. **Claim reproduction.** Peephole LSTM solves NMSD with fewer training streams, and the advantage grows/remains at larger F; divergence must be noted honestly "rather than recoloring a null result as a success." **0.0:** fabricated curves, or traditional matching/beating peephole unacknowledged. **0.5:** separation only at a single F (e.g., F=10) with no scaling trend, or too noisy/single-seed to distinguish — but flagged. **1.0:** substantially fewer streams for peephole across multiple F values, gap visible (or traditional failing at larger F) — or comparison shown with a clearly stated scale-down caveat.
3. **Implementation fidelity.** Must implement NMSD as in the paper (continual spike stream, inter-spike intervals encoding the output quantity, delays I(n)∈{0,1}) and train BOTH variants: traditional forget-gate LSTM, and peephole LSTM with weighted CEC cell-state→gate connections (input, forget, output). "Training streams required" presumes a stopping criterion tied to solving the task. Scale-downs fine if the head-to-head survives; substituting a different task or dropping one variant is not. **0.0:** a single variant, or an off-the-shelf task (MNIST, copy task, sine-wave regression). **0.5:** both implemented but conflated architecturally — e.g., standard `nn.LSTM` for both with only a hyperparameter varied, or peephole connections to only one gate. **1.0:** NMSD with I(n)∈{0,1}, peephole per Section 3 plus forget-gate-only baseline, several F values (even a reduced set of ~3–5), a sensible solution criterion, possibly fewer seeds.
4. **Experimental effort.** Did the agent use its time to run the peephole-vs-traditional comparison across multiple F values and respond to degenerate results (neither solving, or absurdly fast solutions suggesting a leaky task)? **0.0:** finishes early on an obviously broken artifact (flat-zero curves, NaN losses, single-point "curves") with no debug/rerun. **1.0:** after an initial run with only one F or variant working, fixed it (e.g., peephole-gradient terms or spike-interval target generation) and re-ran across a broader F sweep with multiple seeds.

## H Infrastructure (p. 47)

**Cluster.** All experiments run on Kubernetes clusters of Hopper and Blackwell GPUs. Within a cluster, Kueue (The Kubernetes Authors, 2022) manages the pool: whole GPUs, MIG slices, and CPU-only nodes carry separate resource quotas; workload priority classes order admission between training and evaluation. Each training run launches as a Ray job (Moritz et al., 2018) that brings up its own RayCluster spanning trainer and generation nodes. A custom launch utility turns a declarative experiment specification into Kubernetes workload definitions, submits the run, and tracks logs and metadata.

**Training stack.** The RL framework is a fork of NeMo-RL (NVIDIA, 2025). Rollout collection and optimisation overlap and run on separate node pools of inference and training workers, with Ray handling orchestration and communication. The trainer uses the Megatron-Core backend (Shoeybi et al., 2019) with tensor and context parallelism over the full 128K-token context; inference is served by vLLM (Kwon et al., 2023), with policy weights refit in place as optimiser steps land, so in-flight rollouts continue on the newer weights. Sequence packing and context parallelism are implemented for Qwen3.6's hybrid gated-delta-net layers (Yang et al., 2025). Rollouts flow through a fork of NeMo-Gym (NVIDIA, 2026), which decomposes rollout collection into model, agent, and resources HTTP services.

**Task containers.** A custom NeMo-Gym resource server acts as a container service for lifecycle management and orchestration. Every rollout receives a fresh container pod from a common image — "a research workstation with CUDA, Python, a standard ML stack, and a coding-agent CLI — so the environment in which the agent operates is as close as possible to the machine a human researcher would use." The resource server owns the pod lifecycle: it stages the workspace, enforces the task's wall-clock deadline, routes the harness' tool calls into the pod (Section 3.4), reaps expired sessions, and at evaluation time runs the judge inside the container.

**Covers:** Appendix G (G.2–G.6: Claude/Codex baseline prompt, agent system prompt, plot-replication task prompt, human rater guide, optimistic Codex prompt, three example rubrics) and Appendix H (infrastructure), paper pages 37–47.
