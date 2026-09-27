> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction & Motivation

**In one sentence:** Because the sciences face a replication crisis and LLM agents fail at paper replication on three specific fronts (underspecification, training for closed-ended problems, and absence of a hill-climbable reward), we build Replica — a scalable auto-generated figure-replication task space with a low-noise rubric judge — and post-train Faraday, a 27B "AI Scientist" model that uses a 5T-parameter coding agent as a tool and beats Claude Opus 4.8 and GPT-5.5 on held-out replication tasks.

## Key points

- **Motivation:** Replication underpins scientific knowledge (a good explanation is "hard to vary" and falsifiable, per Deutsch 2011), yet the sciences face a replication crisis, notably in machine learning (Kapoor & Narayanan 2022; Semmelrock et al. 2025) — and LLM agents offer a candidate scalable fix, especially for *in silico* research.
- **Challenge (three fronts):** (1) replicating a paper is underspecified by definition — a paper lossily compresses the research; (2) existing agents are trained on well-specified, closed-ended problems (Shao et al. 2024; Gunjal et al. 2025) while replication needs open-ended exploration; (3) harnesses like autoresearch (Karpathy 2026) and AlphaEvolve (Novikov et al. 2025) don't apply because there is no definite reward to hill-climb on a general replication task.
- **Agent design (CAT):** Faraday is a 27B-parameter model (Qwen3.6-27B base) post-trained to direct a coding agent (Codex GPT-5.5, estimated 5T parameters, Li 2026) as a tool — a "layer of scientific intelligence" above the coder that yields a meaningful performance gain over the much larger model alone.
- **Task space (Replica):** 100 ML and AI-for-science papers published 1990–2026, yielding 310 figure-replication tasks; for each paper, Gemini 2.5 Pro redacts individual results figures, each redacted figure defining one task.
- **Reward (rubric judge):** a Claude Opus 4.7 meta-rubric generates a task-specific rubric; a Codex-based judge (multiple samples, given the rollout container with generated figure, codebase, agent trace, and the gold plot) emits overall reward + per-turn credit weights, validated against expert human rankings for low noise.
- **Training recipe:** modified GRPO (Shao et al. 2024) with turn-level credit assignment on the Replica train split — presented as a recipe for stable GRPO on long-horizon, non-verifiable tasks.
- **Results (Figure 2):** Faraday outperforms Claude Opus 4.8 and GPT-5.5 (Codex) on 73% of in-distribution ML tasks and 60% of held-out AI-for-science tasks; +6% over Claude and +8% over Codex on the test split; human experts agree with the rubric judge's ordering.
- **Qualitative finding:** Faraday behaves more like a human scientist — it implements the mechanism behind the claim rather than hard-coding outputs, scales down faithfully to the paper's experimental scope, and avoids shortcuts that would flatter its own result.

---

## Front matter, authors & abstract

Authors (Inherent Laboratories): Damon Falck, Samer Sabri (equal first authors), Anja Surina, Thom Foster, Anya Sims, Sam Devlin, Dylan Rogers, Tantum Collins, Kaloyan Aleksiev (infrastructure lead), Louis Kirsch, Edward Hughes (equal last authors).

The abstract's argument in full: replication is a cornerstone of scientific knowledge and itself requires similar hypothesis-driven exploration to open-ended research. The work (1) develops **Replica**, a scalable task space for paper replication; (2) introduces an **auto-generated rubric-based judge** with low noise that agrees with human assessment of replication quality; (3) post-trains **Faraday**, a 27B-parameter "AI Scientist" agent that leverages coding agents as tools and surpasses Claude Opus 4.8 and GPT-5.5 on held-out replication tasks. Qualitative rollout analysis reveals Faraday adopts a more scientifically-principled approach. The authors believe the results are a stepping stone towards AI agents capable of long-horizon scientific innovation without requiring complex harnesses.

## The replication ideal and the crisis

Science is the search for good explanations about the universe (Deutsch, 2011). An explanation compresses what we know about reality in a reliable way; a good explanation is hard to vary — new contradictory evidence falsifies it rather than being accommodated. Both reliability and falsification rest on experiments replicating: same experiment, same results, up to measurement sensitivity and uncontrollable stochasticity. Replication therefore "underpins the edifice of human scientific knowledge."

Yet the sciences face a **replication crisis**, not least in machine learning (Kapoor & Narayanan, 2022; Semmelrock et al., 2025). LLM-based agents offer a scalable resolution in principle, especially for *in silico* research — but three practical obstacles:

1. **Underspecification by definition.** A paper lossily compresses the research that led to a discovery; restoring the missing details is part of the task.
2. **Mismatched training distribution of existing agents.** Current agents are heavily trained for well-specified, closed-ended problems (Shao et al., 2024; Gunjal et al., 2025), whereas replication requires open-ended exploration to infer missing details.
3. **No reward to hill-climb.** Harnesses such as autoresearch (Karpathy, 2026) and AlphaEvolve (Novikov et al., 2025) don't naturally apply because a general replication task has no definite reward.

Recent work shows frontier agents struggle with many scientific aspects of replication despite engineering proficiency (Kirgis et al., 2026).

## Agent concept: a 27B scientist directing a 5T coder

Faraday is an "AI Scientist" agent (lineage: Schmidhuber 1991; Muggleton & Zauner 2006; Lu et al. 2024; Kirsch 2025) capable of replicating research papers. It employs **Codex GPT-5.5 as a tool**, much as human AI researchers use coding agents. Conceptually, the authors train a layer of scientific intelligence *above* existing coding agents, imbued with intuition for underspecified research problems. The scale inversion is a headline claim: Faraday's 27B parameters direct a model with an estimated 5T parameters (Li, 2026) "in a way that yields a meaningful performance gain over the larger model alone."

## The Replica task space

![We train Faraday on Replica. (1) Construct the Replica task space by curating 100 ML and AI-for-science papers (1990–2026), each redacted-figure from ~310 tasks. (2) Rollouts via the Faraday agent with Codex as a coding tool in a GPU container. (3) Per-task rubric generated by Claude Opus 4.7 from a meta-rubric. (4) Rubric-based multi-sample Codex judge emits reward and per-turn credit weights for modified-GRPO training.](images/fig1.png)
Figure 1's pipeline: ~100 source papers (1990–2026) feed a task-construction stage; each redacted figure + caption becomes one replication task (~310 tasks total). Rollouts run in a container holding the task prompt, the redacted paper PDF, useful research libraries (Python, PyTorch, pdftotext), a Codex terminal, a 1/7 MIG slice of an H200 GPU, and internet access; judging access to the rollout's container includes the gold plot.

Each task requires the agent to **replicate a figure from a paper with limited time and compute budgets, without seeing the original plot**. Success necessitates a small measure of creativity — "navigating novel constraints" in the sense of Boden (1995), Colton & Wiggins (2012), Epstein (2026).

Concretely, per the Figure 1 caption:

1. **Task construction:** curate 100 ML and AI-for-science papers published 1990–2026; use **Gemini 2.5 Pro** to redact individual results figures; each redacted figure yields one task.
2. **Rollout:** agent Faraday (with access to Codex as a code-writing tool) runs in a containerd container provisioned with the task prompt, the redacted paper PDF, the Codex binary, various useful research libraries, a **one-seventh MIG slice of an H200 GPU**, and internet access.
3. **Rubric:** for each task, **Claude Opus 4.7** prompted with a meta-rubric generates a task-specific grading rubric.
4. **Judging:** each rollout is evaluated against that rubric using **multiple samples of a Codex-based judge**, given access to the rollout's container comprising the generated figure, replication codebase, agent rollout, and the "gold plot" from the original paper. The judge provides an overall reward and per-turn credit assignment weights, used to train Faraday with a modified GRPO.

## Judge and training recipe

A coding agent judge assesses each replication using an **auto-generated per-task rubric, validated against expert human rankings**, yielding a low-noise reward signal. **Faraday is produced by post-training Qwen3.6-27B (Qwen Team, 2026) with a turn-level credit variant of GRPO (Shao et al., 2024)** on the Replica train split. (242 in-distribution train tasks; 68 held-out test tasks per the Figure 2 panels.)

## Results overview

Faraday outperforms **Claude Opus 4.8** (hereafter "Claude") and **GPT-5.5** (hereafter "Codex") on **73% of in-distribution ML tasks** and on **60% of held-out AI-for-science tasks**, according to the rubric-based judge. On average, Faraday achieves a **6% improvement over Claude** and an **8% improvement over Codex** on the test split. Optimising Codex's prompt only marginally diminishes the gap. **Human experts rate Faraday as stronger than Claude and Codex on rollouts for which the rubric judge assesses Faraday has an advantage.**

![Faraday replicates better than frontier coding agents: fraction of tasks scoring ≥ σ, in-distribution (left, ML/train, 242 tasks) and out-of-distribution (right, AI-for-science/test, 68 tasks); mean score over eight rollouts per task; ±1 SEM bands; march-of-nines x-axis.](images/fig2.png)
The CDF-style curves show Faraday above all baselines at (nearly) every threshold — mean scores in-distribution roughly Qwen 0.68 < Codex 0.80 < Claude 0.83 < Faraday ~0.86, and out-of-distribution 0.55 < 0.73 < 0.75 < ~0.79 — with a thinner weak tail. Faraday and the raw Qwen base run in the same simple harness (Codex GPT-5.5 as coding tool) and differ only in the Replica RL post-training, so the gap is attributable to training, not harness.

Behaviorally, compared to frontier-model rollouts, Faraday behaves more like a human scientist: it **implements the mechanism behind the claim rather than hard-coding outputs**, it **scales down in a way that remains faithful to the paper's experimental scope**, and it **avoids shortcuts that would flatter its own result**.

## Contributions

1. **Replica** — an automatically generated space of **310 figure-replication tasks** from **100 machine learning and AI-for-science papers** spanning **1990–2026** (Figure 1).
2. A **recipe for stable GRPO post-training in long-horizon, non-verifiable tasks**: a per-task rubric-based judge, multi-sample judge aggregation, and turn-level credit assignment (Sections 3.2 and 3.5).
3. **Faraday** — a 27B-parameter agent that leverages coding agents as tools (CAT), exhibiting greater scientific rigour both quantitatively and qualitatively (Figure 2 and Table 1).

**Covers:** pages 1–2 of the source — title/authors/abstract and Section 1 "Introduction" in full, including Figures 1 and 2 and the contribution list.
