> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Evaluation Design and RQ1: Fault-Localization Settings and Repair Effectiveness
**In one sentence:** PracRepair is evaluated on Defects4J under both perfect fault localization (exact buggy statement locations provided) and a relaxed setting where they are not, using GPT-3.5-turbo and GPT-4o with reused baseline results and plausible/correct patch counts.
## Key points
- Main experiments use gpt-3.5-turbo and gpt-4o at sampling temperature 1.0 for direct comparability with prior APR studies, with gpt-4, Llama-3, and DeepSeek-v3 deferred to RQ4 generalizability.
- Each bug gets at most 3 independent repair sessions from the original bug context, with the diagnosis loop capped at 10 rounds (averaging no more than 5, terminating when no further diagnostic questions arise) and the refinement loop capped at 3 rounds.
- All experiments ran on Ubuntu 20.04 with a 16-core Intel Xeon processor, 192GB RAM, and eight NVIDIA A800 GPUs.
- Nine baselines are compared (TBar; SelfAPR, KNOD, Tare; Codex, AlphaRepair, ChatRepair, ThinkRepair, RepairAgent, ReinFix), reusing results reported in their original papers because the benchmark split, fault-localization setting, and metrics match.
- Effectiveness is measured as number of plausible patches (pass all developer-written tests, not necessarily correct) and number of correct patches (matches developer fix or is manually judged semantically equivalent).
- Under perfect fault localization, PracRepairGPT-3.5 produces 275 correct / 332 plausible fixes and PracRepairGPT-4o produces 333 correct / 413 plausible fixes summed over Defects4J (Table III).
- Under the relaxed no-perfect-FL setting on Defects4J V1.2, PracRepairNo-PFL achieves 105 correct / 133 plausible fixes, versus ThinkRepairNo-PFL at 80 correct and Codex at 63 (Table IV).
---
## Implementation
**Covers:** base models, sampling, session/loop budgets, hardware

- Base models in main experiments: gpt-3.5-turbo and gpt-4o; generalizability in RQ4 (Section V-D) uses gpt-4, Llama-3, and DeepSeek-v3.
- Sampling temperature set to 1.0, following prior work.
- Maximum 3 repair sessions per bug, each independent and starting from the original bug context.
- Diagnosis loop: at most 10 rounds, averaging no more than 5 since it terminates once no further diagnostic questions are raised; refinement loop: at most 3 rounds, described as a better balance between repair effectiveness (cf. Section V-C).
- Workstation: Ubuntu 20.04, 16-core Intel Xeon processor, 192GB RAM, eight NVIDIA A800 GPUs.

## Baselines and ablation variants
**Covers:** nine baselines with reused results; ablation variant definitions

- Nine state-of-the-art baselines: one traditional (TBar); three learning-based (SelfAPR, KNOD, Tare); five LLM-based (Codex, AlphaRepair, ChatRepair, ThinkRepair, RepairAgent, and ReinFix — listed as five in text with six names).
- Same benchmark split, fault-localization setting, and repair metrics as these studies, so repair results reported in their original papers are reused instead of re-running the tools, per APR community practice.
- Ablation variants: w/o SDC+QFD+FPR (removes all three stages, directly prompts the LLM for a patch); w/o SDC+QFD (investigates Static-dynamic Context Construction contribution); plus variants removing dynamic traces only, replacing question-driven diagnosis with Chain-of-Thought (PracRepair CoT, like ThinkRepair), and replacing it with direct reasoning–tool interleaving with function calls (PracRepair ReAct, like ReInFix).

## Metrics
**Covers:** plausible vs correct patch definitions

- Number of plausible patches: bugs with at least one generated patch passing all developer-written test cases; satisfies the test oracle but is not necessarily semantically correct.
- Number of correct patches: bugs with at least one semantically correct patch; determined by first checking match with the developer-provided fix, otherwise manual semantic-equivalence assessment; correct if it passes either check.

## RQ1: repair effectiveness under two fault-localization settings
**Covers:** perfect-FL vs relaxed no-exact-location setting on Defects4J

- RQ1 evaluates PracRepair on Defects4J under both the standard perfect fault localization setting and a relaxed setting where exact buggy statement locations are unavailable, asking whether it remains effective without perfect FL.
- Under perfect FL, PracRepairGPT-3.5 generates 332 plausible and 275 correct fixes; PracRepairGPT-4o improves to 413 plausible and 333 correct fixes.
- Table III (correct / plausible under perfect FL): D4J V1.2 totals — PracRepairGPT-4o 162/213, PracRepairGPT-3.5 139/167, ReInFixGPT-4o 146/207, ReInFixGPT-3.5 118/152; D4J V2.0 totals — 171/200, 136/165, 145/190, 123/147; sums — 333/413, 275/332, 291/397, 241/299.
- Table IV (correct / plausible without perfect FL on Defects4J V1.2): Chart 12/16, Closure 28/32, Lang 23/31, Math 32/43, Mockito 7/8, Time 3/3; total 105/133 for PracRepairNo-PFL versus ThinkRepairNo-PFL total 80 correct and Codex total 63 (plausible counts unreported, marked "–").
- Fig. 3 shows Venn diagrams of correct patches of PracRepair vs. GPT-3.5-based and GPT-4o-based results on Defects4J V1.2 and V2.0.
