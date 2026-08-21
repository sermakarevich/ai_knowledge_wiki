# Task: Extract wiki page 04 — Implementation Details and Appendix — GraphScout paper

You are writing ONE page of an LLM-wiki for the paper "GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning" (Ying et al., 2026).

**Context is tight on this model — read ONLY the two files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input files (read exactly these, in full)

1. `/Users/sergii/.kb/papers/ArxivGraphScout/source/chunks/04.txt` — the source text for this page (covers Appendix A: RL hyperparameters, hardware/software config, GRBENCH dataset details, baseline configuration, Group Relative Policy Optimization derivation; Appendix B: Graph Quizzer diversity analysis, tool-invocation reliability, and a worked case study; plus prompt templates). **This is the last part of the document, note it does NOT include the References/bibliography list — that was deliberately excluded from the wiki.**
2. `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/images/descriptions.md` — read only the entry titled `fig78-quizzer-diversity-and-tokens.png (Figures 7, 8 + Table 5)`; ignore the other entries in that file.

## Output file

Write to: `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/04-implementation-details-and-appendix.md`

**If this file already exists (a retry), overwrite it completely.**

## Required page format (fill this in from the chunk text — do not invent facts not in the chunk)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Implementation Details and Appendix

**In one sentence:** <the chapter's whole argument: the concrete training/hardware setup, the GRPO derivation, and evidence (diversity analysis, tool-reliability numbers, a worked failure/success case) that the Graph Quizzer's synthetic data and Graph Solver's training genuinely work as intended>

## Key points

- <5-8 bullets with real content — e.g. the specific hardware (GPU count/type), the RL algorithm details, the dataset composition, the failed-tool-call rate before/after training, and one concrete detail from the case study>

---

## RL hyperparameters and training setup

<Appendix A.1: training settings used for GraphScout, referencing Table 3 if numbers are given in the text>

## Hardware and software configuration

<Appendix A.2: exact hardware (GPU model/count/memory, CPU, system memory), software (CUDA version, verl framework)>

## GRBENCH dataset details

<Appendix A.3: what GRBENCH is, its domains, how it's structured>

## Baseline configurations

<Appendix A.4: PolyG, GraphCounselor, and LLM backbones used for baselines (GPT-4o, GLM-4.6, Qwen-Max, DeepSeek-Chat), embedding model used (Qwen3-text-embedding-v4)>

## Group Relative Policy Optimization (GRPO) — derivation

<Appendix A.5: the full derivation as described in the chunk — group-relative advantage normalization, the clipped surrogate objective, the KL regularization term, and why GRPO is used instead of PPO's learned value function. Preserve named quantities (advantage, clipping hyperparameter, KL weight) even if you cannot re-typeset every symbol perfectly.>

## Graph Quizzer diversity analysis

<Appendix B.1: the de-conditioned annotation methodology (using DeepSeek-Chat as judge without seeing the original generation parameters), and the resulting distribution findings (difficulty, question pattern, answer pattern balance; token-length and clue-node-count distributions)>

## Tool invocation reliability

<Appendix B.1.1 / Table 5: the failed-tool-call rate before ("w/o train") vs after ("w/ train") GraphScout training, across domains, with exact percentages>

## Case study

<Appendix B.2: the worked example — the question asked, the ground truth, and how a baseline method (e.g. GraphCoT) failed vs how GraphScout succeeds, using the concrete turns/thoughts/actions given in the chunk if present>

![Figure 7-8 and Table 5: Graph Quizzer diversity and tool-reliability](images/fig78-quizzer-diversity-and-tokens.png)

**Covers:** Appendix A (Implementation Details, A.1-A.5), Appendix B (Additional Analysis and Experiments, B.1-B.2)
```

## Rules

- Preserve exact numbers and named settings (GPU model, CUDA version, percentages) as they appear in the chunk.
- The `## Key points` block must stand alone as the chapter at medium depth — write real claims, not topic labels.
- Do not fabricate content beyond what's in the chunk text and the one figure description you read. If a subsection genuinely has no content in the chunk (e.g. no case-study turns given), say so briefly rather than inventing detail.
- No git commands. No fleet commands other than the close command below.
- Touch ONLY the one output file listed above.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 04 extracted"`
