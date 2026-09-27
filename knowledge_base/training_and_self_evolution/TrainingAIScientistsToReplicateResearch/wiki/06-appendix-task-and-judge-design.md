> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Task Construction, Judge Analyses, Ablations, and Human Studies

**In one sentence:** Faraday generalises beyond its training envelope — to full-scale replication (8 h, 8 B300 GPUs) and to a stronger coding-agent tool — its turn-level credit assignment and coder-tool design are validated by ablations and distribution analyses, and human studies show the rubric judge tracks human taste (63% of disputed pairs) and that human experts prefer Faraday to the baselines (80%/88%) when the judge puts it clearly ahead.

## Key points
- **Full-scale generalisation:** Faraday beats Claude on average of a rubric judge on 8 held-out full-scale replication tasks (up to 8 h and 8 B300 GPUs, context raised from 128K to 256K) and wins 5 of 8 tasks (Figure A.1).
- **Tool generalisation:** The last Faraday checkpoint trained only with GPT-5.4 mini as the Codex tool performs *better* than Claude on held-out tasks when the tool is swapped to GPT-5.5 — no retraining needed (Figure A.2).
- **Credit-assignment ablation:** Removing turn-level credit assignment from a late checkpoint causes rapid training collapse; carry-forward mean reward collapses after ~50 steps, token entropy spikes then collapses, and Jensen–Shannon divergence between generation and policy grows by two orders of magnitude (Figure B.1).
- **Coder-tool ablation:** A from-scratch Qwen3.6-27B run without the coding-agent tool ("Faraday Coder") training collapses after ~300 steps and is weaker at equal step count — even with *twice* the time horizon (60 min vs 30 min) — suggesting the researcher-model ceiling exceeds the coder-model ceiling (Figure B.2).
- **Credit distribution:** Across 577,585 turns (steps 491–635 of the Faraday lineage), the judge concentrates credit in the early-to-middle of rollouts and weights turns that delegate to the coding agent more heavily (Figure C.1).
- **Post-training recipe:** Rollout staleness capped at 3–6 optimizer steps, bf16 precision (more stable than fp8), leave-one-out group-relative advantage, DAPO token-level loss with asymmetric clip (ε_l=0.15, ε_h=0.35), IcePop discrepancy masking (likelihood ratio ∈ [0.3, 4]), KL penalty β=3×10⁻³; a 5-stage lineage ends at step 659 (Table D.1).
- **Human studies:** Judge-comparison: 76 rankings from 19 participants; humans side with the rubric judge on 63% of disputed pairs (p = 0.109, above chance, not significant). Agent-comparison: 41 rankings from 11 participants; Faraday preferred over Claude in 80% and Codex in 88% of rankings, above both in 71% (p < 0.01).
- **Innovation-task variants:** Each of ten source figures yields two variants — (a) keep the claim, swap the dataset/environment; (b) keep the setting, reverse the claim — with gold plot, caption, and paper text rewritten together so recall of the published result gives limited benefit (Tables F.3–F.4).

---

## A. Generalisation

### A.1 Full-scale replication

Faraday is trained to complete **scaled-down** replications of a single figure under a one-hour time limit and a one-seventh MIG GPU slice (30 minutes early in training, raised to one hour in later stages). Building on prior evidence that a horizon curriculum can induce generalisation to longer horizons (Kim et al., 2026), the authors test Faraday's ability to generalise to full-scale replication given the necessary time and compute.

**Task selection.** Eight replication tasks are chosen from outside Faraday's training distribution, filtered with Claude Opus 4.8 so that at most 8 hours and 8 B300 GPUs should suffice to replicate the figure. Five tasks come from AI-for-science papers (Xie & Grossman, 2017; Chithrananda et al., 2020; Ramsundar et al., 2015; Xu et al., 2025a; Bhattacharjee, 2026) and three from ML papers (Gu et al., 2026; Lin, 2026; Yuan et al., 2026). Three of the eight papers were first made public *after* the knowledge cutoffs of Claude Opus 4.8, GPT-5.5, and Qwen3.6-27B. Faraday's context limit is raised to its maximum 256K (from 128K during training); the 8-hour cap is chosen because it approximates the horizon allowed by the increased context limit without compaction.

**Method and result.** Claude Opus 4.8 estimates, per paper, the hours and B300 GPUs (capped at 8 h / 8 GPUs) needed to replicate one figure with no scale-down. One rollout per task is run for Faraday and for Claude under the estimated resources. Faraday outperforms Claude on average per the rubric judge and wins 5 of 8 tasks (mean lines above Claude in Figure A.1) — evidence that Faraday generalises to longer horizons and larger compute. Caveat: the rubric judge was not validated against human ratings at this scale, identified as important future work.

> *Figure A.1 (caption):* On eight held-out tasks, with access to up to eight hours and eight B300 GPUs, Faraday performs better than Claude according to the rubric judge (horizontal rules = means over tasks) and outperforms it on five of eight tasks.

### A.2 Stronger coding agent tool

Since frontier coding agents improve frequently, the authors test whether Faraday can effectively use a stronger coding tool than it was trained with. Recall that Faraday was initially trained with **GPT-5.4 mini** as the model backing the **Codex** tool. The last checkpoint of Faraday's lineage that was trained *only* with GPT-5.4 mini as a tool is evaluated on the **Replica test split** using, first, GPT-5.4 mini and then **GPT-5.5**, as the coding-agent model.

Figure A.2 shows this partially trained version makes effective use of the stronger agent: swapping in GPT-5.5 boosts its scores on held-out AI-for-science tasks. Conclusion: Faraday is not specialised to its train-time coding agent and generalises to a stronger one without retraining.

> *Figure A.2 (caption):* Each point is an individual task (mean of four rollouts); horizontal rules are means across tasks. The GPT-5.4-mini-only checkpoint performs better when the coding agent is GPT-5.5.

## B. Ablations

### B.1 Turn-level credit assignment

> *Figure B.1 (caption):* Starting from a late checkpoint in Faraday's training lineage, removing turn-level credit assignment causes rapid destabilisation and collapse. (Left) With turn-level credit assignment, carry-forward mean reward (mean over all tasks of the most recent reward achieved on each task) rises steadily; with uniform credit assignment it **collapses after 50 steps**. (Centre) Around the same time, token entropy of the policy trained without turn-level credit assignment spikes and then collapses. (Right) Leading up to collapse, the **Jensen–Shannon divergence** between generation policy and training policy (which differ due to asynchronous training) begins to increase, eventually growing by **two orders of magnitude**; the authors find this a common precursor to such collapses.

### B.2 Coding agent as a tool

> *Figure B.2 (caption):* Qwen3.6-27B trained from scratch with the same hyperparameters as the last tail-patch of Faraday's lineage but **without** the coding-agent tool ("Faraday Coder") collapses after ~300 steps and performs more weakly than Faraday's lineage at equal step count. Notably, during the pre-collapse period Faraday Coder had **twice the time horizon (60 minutes)** of Faraday (30 minutes) and still performed consistently worse — suggesting the ceiling for the coder model is lower than for the researcher model. As in Figure B.1 (left), curves show carry-forward mean reward; ghosted curves are per-step mean reward.

## C. Analyses

### C.1 Credit assignment distribution

> *Figure C.1 (caption):* Data from **577,585 turns** of the Faraday training lineage with turn-level credit assignment enabled (every turn from steps 491–635). (Left) Credit is concentrated in the **early-to-middle** stages of a rollout, where load-bearing decisions are most commonly made. (Right) More weight is given to turns that **delegate to the coding agent tool**, capturing the importance of appropriate delegation. Turn types are assigned post-hoc by regular-expression match on the turn text.

### C.2 Scores by rubric dimension

> *Figure C.2 (caption):* The left-hand panel of Figure 2 split out into the five score dimensions of the rubric judge; each panel shows the fraction of the **242 tasks** in the Replica train split with a mean score over eight rollouts of at least σ in the corresponding dimension (SEM omitted for clarity). Faraday's replications consistently have **more experimental depth**, **better claim reproduction**, and **higher visual fidelity** to the original figure; it approximately **matches Claude** in implementation fidelity (faithfulness to the paper's methodology) and scientific integrity (not cheating while completing the task). See Section 3.2 for dimension definitions.

### C.3 Within-rollout behaviour

> *Figure C.3 (caption):* Within-rollout plots of elapsed minutes (x-axis) vs rubric judge score (y-axis), on nine randomly sampled test tasks using the strongest of Faraday's eight evaluation rollouts (per Figure 2). Green line = best score seen so far; grey = latest score. Faraday builds on previous discoveries to find new insights at test time, like existing AI Scientist agents — but requires **no hand-coded evolutionary harness** and has **no access to a reward function** at test time; the y-axis is computed post-hoc by the rubric judge and never provided to Faraday.

## D. Supplementary methods

### D.1 Task space (contamination position)

The authors acknowledge that some chosen papers and figures are almost certainly in the pre-training data of frontier multimodal models, and are "equally certain" no frontier model has been trained on the **process data** that produced the original figures (never recorded or released). Since most originals were generated under very different resource/time constraints than in Replica, and the object of study is the **process** of replication rather than exact figure fidelity, pre-training contamination with paper details is not viewed as a problem (though it is considered in interpreting results, Section 4.2). **Figure redaction** was chosen to decontaminate the agent's context (encouraging a rigorous replication process) and to help the judge detect cheating, such as reverse-engineering data by downloading the original plot.

### D.2 Post-training

- Rollouts are generated on dedicated inference workers and consumed asynchronously by the training engine; **rollout staleness capped at 3–6 optimiser steps**.
- Generation and training in **bf16** (found more stable than fp8).
- Unlike vanilla GRPO: **leave-one-out baseline** for the group-relative advantage (Ahmadian et al., 2024); **DAPO**'s token-level loss and asymmetric clip-higher (Yu et al., 2025) with ε_l = 0.15, ε_h = 0.35; **IcePop**'s token-level discrepancy masking (Ling Team, 2025), zeroing tokens whose sampler–trainer likelihood ratio falls outside [0.3, 4].
- GRPO's small KL penalty vs base model kept: β = 3×10⁻³.
- Final checkpoint is **step 659**, the end of a multi-stage lineage: most training used cheaper GPT-5.4 mini and 30-minute tasks; final stages tail-patched with GPT-5.5 and one-hour duration.

**Table D.1 — Stages of the Faraday training lineage** (deltas from previous stage):

| Stage | Steps | Description |
|---|---|---|
| I | 1–100 | fp8 rollout precision, GPT-5.4 mini coding agent as a tool; 30-minute task horizon; learning rate 3×10⁻⁶; 4 steps off-policy; 1 judge sample; uniform credit assignment |
| II | 101–382 | bf16 rollout precision; learning rate 6×10⁻⁶; 3 steps off-policy |
| III | 383–489 | GPT-5.5 coding agent as a tool; 60-minute task horizon |
| IV | 491–635 | 3 judge samples; turn-level credit assignment |
| V | 636–659 | Fixes to task captions in 17% of tasks |

## E. Supplementary discussion (scaling axes)

- **Task space:** Papers accepted at ICML, ICLR, and NeurIPS alone could yield **36,000 tasks per year** — two orders of magnitude larger than the current set. Greater diversity of resource constraints and task variants demanding innovation beyond replication produce a "further combinatorial explosion." Difficulty: some tasks are results that simply do not replicate (mitigated so far by choosing well-regarded, highly cited papers). Scaling would require **judges that recognise non-replicability** and agents that robustly test and honestly report it. A larger task space may enable training an agent general enough to evaluate on different-API benchmarks such as **PaperBench** (Starace et al., 2025).
- **Base-model size:** Scaling the base model by an order of magnitude would give much stronger foundational capabilities; a **multimodal** base model may also help (tasks rely on generating and interpreting figures).
- **Harness:** The CAT paradigm does not preclude using/optimising a harness around the outer model at train time — an inference-time improvement operator yielding stronger trajectories to learn from (Silver et al., 2016; Anthony et al., 2017; Surina et al., 2025).

## F. Human studies

Two studies, both blind (participants receive no model-identity information) and both using the interface/instructions of Appendix G.4; they differ only in which rollouts a participant sees. In both, the rollout-selection rule is fixed before data collection.

### F.1 Judge comparison

**Question:** does the rubric judge track human taste where it and the baseline judge disagree?

**Methods.** A participant ranks **six rollouts of one task**: four from the training run (sampled from four 50-step windows: **143–192, 291–340, 438–487, 586–635**, one rollout per window drawn uniformly at random among those that finished and produced a figure) and one each from Claude and Codex (each with a set of eight rollouts per task, one taken uniformly at random). Tasks are selected for **judge disagreement** (agreement is uninformative). Initial pool: 131 tasks judged tractable for an expert ML-background human; kept are tasks whose six rollout scores are more spread than the median task under *both* judges; drawn most-disputed-first, skipping already-drawn papers, stopping at **10 tasks from 10 papers** (Table F.1). A **pair of rollouts is disputed** when the two judges order it oppositely and the score gap exceeds **0.02** under both judges (to exclude gaps inside measured judge noise). Analysis: **binomial mixed-effects model with a task random effect**, against the null that humans side equally with the two judges.

**Table F.1 — Ten judge-comparison tasks (all from train split)** (labels as in Figure 3, left):

| Paper | Fig. | Label | What the figure claims |
|---|---|---|---|
| A Generalist Agent — Reed et al. (2022) | 5 | Gato | A single pretrained policy reaches a large fraction of expert score across many control tasks. |
| Asynchronous Methods for Deep Reinforcement Learning — Mnih et al. (2016) | 3 | A3C | More parallel threads make the one-step methods more data-efficient, not just faster. |
| Auto-Encoding Variational Bayes — Kingma & Welling (2013) | 2 | VAE | The AEVB estimator converges faster and to a better bound than wake-sleep, without overfitting at higher latent dimension. |
| Evolution through Large Models — Lehman et al. (2023) | 1 | ELM | LLM diff mutation fixes several coupled bugs at once, where genetic-programming mutation fails. |
| Exploring Strategies for Training Deep Neural Networks — Larochelle et al. (2009) | 9 | Deep-nets | Constant-width layers beat widening ones at matched capacity, under both pretraining schemes. |
| Gradient-Based Learning Applied to Document Recognition — LeCun et al. (1998) | 12 | LeNet | Memory-based classifiers need orders of magnitude more storage than convolutional networks. |
| Learning Precise Timing with LSTM Recurrent Networks — Gers et al. (2002) | 8 | LSTM | A trained peephole LSTM spikes on time, at both a short and a long interval. |
| SMOTE — Chawla et al. (2002) | 23 | SMOTE | Over-sampling the minority class and under-sampling the majority matches under-sampling alone when training a Ripper classifier on the Can dataset. |
| Scaling In-Context Online Learning Capability of LLMs via Cross-Episode Meta-RL — Lin et al. (2026) | 1 | ICL | Cross-episode meta-RL lifts a small model to frontier level on unseen interactive environments. |
| The AI Scientist — Lu et al. (2024) | 2 | AI-Sci | Reflection and one-shot prompting improve the automated reviewer's accuracy; ensembling mainly cuts variance. |

**Results.** 76 rankings from **19 participants**. Participants side with the **rubric judge on 63% of disputed pairs** — higher than chance but not significantly so (**p = 0.109**).

### F.2 Agent comparison

**Question:** do human experts agree with the rubric judge when it places Faraday clearly ahead of a baseline?

**Methods.** Each participant ranks **three rollouts per task**: one Faraday, one Claude, one Codex — all from the same evaluation set used for Figure 2 and Figure 4. Rollouts are selected for **judge margin**: a triplet is eligible when the rubric judge puts Faraday at least **0.2** above both baselines (judge scale 0–1). Tasks are further filtered for human-judging tractability (expert, general ML background), yielding **29 tasks** (Table F.2) from both train and test splits. The design supports a *conditional* claim: whether humans agree with the judge's verdicts under a clear Faraday advantage, not Faraday's average standing.

**Results.** 41 rankings from **11 participants**. Against the null of no human preference: participants prefer **Faraday to Claude in 80%** of rankings and **to Codex in 88%**, and rank it **above both baselines in 71%**, all significantly higher than chance (**p < 0.01**).

**Table F.2 — The 29 agent-comparison tasks.** *ML (train)*:
- A Generalist Agent — Reed et al. (2022), Fig. 5: a single pretrained generalist policy reaches a large fraction of expert score across many control tasks.
- Additive Logistic Regression — Friedman et al. (2000), Fig. 1: on nested spheres, both AdaBoost variants drive test error below bagging as trees are added.
- Asynchronous Methods for Deep RL — Mnih et al. (2016), Fig. 4: every asynchronous method trains faster in wall-clock time as parallel actor-learners are added.
- Automated Design of Agentic Systems — Hu et al. (2024), Fig. 3: searching over agent code with a growing archive keeps finding better ARC agents as search proceeds.
- Darwin-Gödel Machine — Zhang et al. (2026a), Fig. 4: self-improved agents keep their advantage when transferred to other models, benchmarks, and programming languages.
- Diversity is All You Need — Eysenbach et al. (2019), Fig. 6: DIAYN's reward on a hierarchical task rises with the number of skills, and beats VIME exploration.
- Dropout — Srivastava et al. (2014), Fig. 4: dropout lowers test error at every depth and width tried.
- Evolution through Large Models — Lehman et al. (2023), Fig. 15: fine-tuned LLM mutators complete out-of-distribution solutions better when trained at a higher threshold.
- Gradient-Based Learning... — LeCun et al. (1998), Fig. 12: memory-based classifiers need orders of magnitude more storage than convolutional networks.
- Greedy Function Approximation — Friedman (2001), Fig. 3: MARS makes more frequent larger and smaller errors than boosted trees.
- HOGWILD! — Recht et al. (2011), Fig. 3: lock-free parallel SGD speeds up matrix completion substantially, and holds much of that speedup as update delays grow.
- ImageNet Classification with Deep ConvNets — Krizhevsky et al. (2012), Fig. 1: a four-layer convnet with ReLUs reaches 25% training error on CIFAR-10 ~6× faster than with tanh.
- Manifold Regularization — Belkin et al. (2006), Fig. 5: on USPS digits, Laplacian regularisation cuts error of RLS and SVM, largest gain when labels are scarce.
- Manifold Regularization — Belkin et al. (2006), Fig. 8: on WebKB, the Laplacian variants lead at every label budget and improve further with more unlabelled data.
- Meta-Learning Backpropagation and Improving It — Kirsch & Schmidhuber (2021), Fig. 5: a meta-RNN cloned from backpropagation learns MNIST faster after meta-learning, without losing ground OOD on Fashion-MNIST.
- Scaling In-Context Online Learning... — Lin et al. (2026), Fig. 1: cross-episode meta-RL lifts a small model to frontier level on unseen interactive environments.
- The AI Scientist — Lu et al. (2024), Fig. 4: the automated reviewer's score distribution for AI-generated papers varies across three research domains and four foundation models.
- Toolformer — Schick et al. (2023), Fig. 4: GPT-J models >1000M params finetuned with Toolformer learn to make good use of API calls.

*AI-for-science (test)*:
- Foundational LLMs for Materials Research — Mishra et al. (2024), Fig. 3: continued pretraining on materials literature beats general frontier models at extracting structured materials information.
- A Foundation Model for the Earth System — Bodnar et al. (2025), Fig. 2: air-quality forecasts match or beat the operational CAMS system at a fraction of the compute.
- A Generative Model for Inorganic Materials Design — Zeni et al. (2025), Fig. 2: generated crystals are more often stable, unique, and new than earlier generative baselines.
- Accurate Structure Prediction of Biomolecular Interactions with AlphaFold 3 — Abramson et al. (2024), Fig. 4: the model's own confidence scores track the accuracy of its predicted interfaces and chains.
- CLOUD — Xu et al. (2025a), Fig. 2: a symmetry-aware string representation matches structure-based models on MatBench regression, and pretraining improves it.
- FourCastNet — Pathak et al. (2022), Fig. 1: a 96-hour global near-surface wind forecast reproduces the observed field at 0.25° resolution.
- FourCastNet — Pathak et al. (2022), Fig. 4: an ensemble forecast tracks Hurricane Michael's path and rapid intensification over four days.
- GraphCast — Lam et al. (2023), Fig. 2: the model beats the operational HRES forecast at nearly all lead times.
- GraphCast — Lam et al. (2023), Fig. 4: training on more recent data improves skill on a held-out later year, most at short lead times.
- MACE — Batatia et al. (2022), Fig. 3: the model follows the reference energy along three cuts of a molecule's PES more closely than BOTNet and NequIP.
- Scaling Deep Learning for Materials Discovery — Merchant et al. (2023), Fig. 2: discovered stable crystals reach compositions of four or more elements.

### F.3 "Innovation" tasks

The ten source tasks behind Figure 5 (right) are drawn uniformly at random from the Replica splits. **Each source figure yields two variants:** (a) keeps the paper's claim but swaps the dataset or environment; (b) keeps the setting but changes the claim, usually reversing it. In both cases the "gold plot," its caption, and the paper text are rewritten together, so the published result is no longer the target and recall is of limited benefit.

**Table F.3 — Ten "innovation" tasks from train-split papers** (variant pairs):

- **Adam** (Kingma & Ba, 2014, Fig. 4): (a) Adam's bias-correction step matters — leaving it out makes training unstable at some hyperparameter settings. (b) The bias-correction step is unnecessary — training goes just as well without it.
- **Reducing the Dimensionality of Data** (Hinton & Salakhutdinov, 2006, Fig. 3): (a) "Autoencoder" — a neural network can squeeze images of handwritten digits down to two numbers and still keep the digits apart, where the standard linear method jumbles them. (b) The two-number summary is no better than the linear one; both jumble the classes together.
- **Execution-Grounded Automated AI Research** (Si et al., 2026, Fig. 2): (a) An AI system turns most of its own research ideas into working code, and its best idea beats the human baseline. (b) The system rarely gets its ideas running, and none of the fifty it does run beat the baseline.
- **Shifting Inductive Bias with SSA** (Schmidhuber et al., 1997, Fig. 6): (a) A program that rewrites its own code does so ever more often while still learning, then eases off once little is left to learn. (b) It rewrites itself ever more often right up to the end, never noticing it has stopped learning (measured in a two-agent key-and-door task).
- **Social Influence as Intrinsic Motivation** (Jaques et al., 2019, Fig. 4): (a) Agents only learn to use a communication channel usefully when rewarded for influencing one another. (b) The reward for influencing one another adds nothing; a plain communication channel does just as well (in two different multi-agent games).

**Table F.4 — Ten "innovation" tasks from test-split papers** (columns and variant construction as in Table F.3):

- **A Foundation Model for the Earth System** (Bodnar et al., 2025, Fig. 2): "Aurora" (a) An AI weather model predicts air pollution as well as the established physics-based system (CAMS) (measured against a different reference dataset). (b) The physics-based system beats the AI model on most air-pollution measures, leaving only the cost saving.
- **CLOUD** (Xu et al., 2025a, Fig. 2): (a) Describing a crystal by its symmetry alone predicts material properties about as well as models that see the full 3D structure, and pre-training helps (on a different materials benchmark). (b) Pre-training makes the model *worse*, raising the error on most benchmarks (trained on a different molecule database).
- **Molecular Atomization Energies with ML** (Rupp et al., 2012, Fig. 2): "Coulomb ML" (a) ML predicts a molecule's energy far more accurately than standard chemistry approximations. (b) The model is no more accurate than those approximations, however much training data it is given.
- **Efficient Discovery of Protein Responses** (Kangas et al., 2014, Fig. 3): (a) A drug-screening model predicts how untested compounds behave, but barely generalises to untested proteins (on a different screening database). (b) The model handles untested proteins just as well as untested compounds.
- **Physics Informed Deep Learning (Part I)** (Raissi et al., 2017, Fig. 3): "PINN" (a) A neural network taught the underlying physics can jump a simulation forward in one huge time step and still get the answer nearly exactly right (for a wave equation rather than a shock-forming one). (b) The single huge time step fails, smearing out the sharp shock the equation should produce.

## G. Prompts (boundary of this chunk)

The appendix continues with **G.1 Faraday system prompt**, of which this chunk includes only the opening line:

> "You are Faraday, an autonomous AI researcher. You operate inside a containerized workspace."

**Covers:** Appendix A (Generalisation: full-scale replication, stronger coding-agent tool), B (Ablations: turn-level credit assignment, coding agent as a tool), C (Analyses: credit-assignment distribution, rubric-dimension scores, within-rollout behaviour), D (Supplementary methods: task space, post-training + Table D.1), E (Supplementary discussion), F (Human studies: judge comparison + Table F.1, agent comparison + Table F.2, innovation tasks + Tables F.3–F.4), and the opening of G.1 (Faraday system prompt) — paper pages 24–36.
