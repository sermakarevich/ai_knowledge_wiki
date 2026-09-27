[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Coding Agents are Strong Prompt Optimizers (CASD overview)
**In one sentence:** A single offline pass in which an unmodified coding agent analyzes a static corpus of agent trajectories with executable code and distills the findings into a skill file used directly as the optimized system prompt outperforms iterative search-based prompt optimizers while costing about $1.60 with no environment access or validation data.
## Key points
- Coding-Agent Skill Distillation (CASD) replaces iterative search with a single offline analysis pass over a static corpus of agent trajectories using an off-the-shelf, unmodified coding agent.
- The recipe is deliberately simple: give the coding agent the rollout corpus plus a short natural-language instruction, then use the generated skill file directly as the optimized system prompt.
- CASD requires no optimization loop, validation gate, environment interaction, or held-out validation set, and producing an optimized prompt costs approximately $1.60 — over 22× cheaper than validation-gated search.
- Under matched data access across four agentic benchmarks (ALFWorld, τ-bench retail and telecom, SpreadsheetBench-Verified), a single CASD pass outperforms GEPA on three of four benchmarks and validation-gated reflective search (SkillOpt) on all four.
- Average gain over the unoptimized baseline is 16.6 percentage points for CASD versus 10.9 for GEPA and 5.3 for SkillOpt.
- Even when competing methods are granted additional validation data and unrestricted environment access, CASD remains ahead on two of four benchmarks.
- The key insight is reflection scope: instead of reasoning over a small batch of trajectories per optimization step, the coding agent writes and executes analysis code to compute corpus-wide statistics, identifies systematic failure modes, inspects representative episodes, and distills insights into behavioral rules.
---
## Framing: search-based prompt optimization and its limits
**Covers:** title block + Abstract + §1 Introduction (chunk lines 1–60)

- Paper: "Coding Agents are Strong Prompt Optimizers" — Agamdeep Singh, Srishti Gautam, Priyanshu Gupta, Nikita Mehrotra, Tanmay Bakshi, Sumit Gulwani (Microsoft); arXiv:2609.26261v1 [cs.AI] 13 Aug 2026.
- Context: LLM agents are highly sensitive to their system prompts; search-based optimizers treat the prompt as a learnable artifact by iteratively proposing edits, evaluating them through fresh environment rollouts, and retaining only those that improve a validation objective (Zhou et al. 2023; Yang et al. 2024a; Pryzant et al. 2023; Khattab et al. 2024; Opsahl-Ong et al. 2024), with GEPA (Agrawal et al. 2026) strengthening the search with natural-language reflection over sampled trajectories.
- Stated limitation 1: every prompt revision must be validated through fresh environment interaction, keeping the environment, user simulator, and evaluation metric in the optimization loop while cost grows with the number of candidate edits.
- Stated limitation 2: each prompt revision is informed by only a small sample of trajectories, limiting the ability to identify behavioral patterns visible only at corpus scale.
- Corpus-scale examples given in chunk: "a tool was invoked 284 times but duplicated 123 times" and "an entire task category failed in 24 of 24 attempts" — neither reliably discoverable from a single small-sample reflection step.

## CASD: single offline distillation pass
- Approach per Abstract: "Given only a static corpus of agent trajectories, an off-the-shelf coding agent can directly synthesize an optimized prompt, requiring neither environment access nor validation data."
- Recipe: provide the coding agent with the rollout corpus and a short natural-language instruction, then use the generated skill file as the optimized system prompt — "No optimization loop, validation gate, environment interaction, or held-out validation set is required; prompt optimization becomes a single offline pass costing about $1.60."
- What replaces iterative search is corpus-scale reflection: the agent writes and executes analysis code to compute corpus-wide statistics — "per-category pass rates, tool-call histograms, duplicate-call counts, and argument-hallucination frequencies" — before drilling into the episodes those statistics flag as most informative.
- Chunk explicitly links this to program-aided prompting: "Offloading the counting to an interpreter is the same move that makes program-aided prompting exact where free-form reasoning is not (Gao et al. 2023; Chen et al. 2023), applied here to the optimizer rather than to the task solver."
- Claimed consequence: "The resulting prompts are grounded in measured evidence rather than anecdotal observations from a handful of trajectories."

## Headline results and cost (matched data access)
**Covers:** Abstract results sentences + Figure 1 caption

| Comparison (matched data access, 4 benchmarks) | Result stated in chunk |
|---|---|
| CASD vs GEPA (state-of-the-art reflective optimizer) | CASD wins on three of four benchmarks |
| CASD vs validation-gated reflective search (SkillOpt) | CASD wins on all four |
| Avg improvement over unoptimized baseline | 16.6 pp (CASD) vs 10.9 (GEPA) vs 5.3 (SkillOpt) |
| Optimization cost | ~$1.60 for CASD, over 22× cheaper than validation-gated search |
| Extra validation data + unrestricted env access granted to baselines | CASD still ahead on two of four benchmarks |

- Figure 1 (per caption in chunk): left contrasts iterative GEPA/SkillOpt refinement using environment rollouts and validation feedback against CASD's single offline pass over a frozen rollout corpus producing the skill file directly; right shows CASD with the largest average improvement at substantially lower optimization cost.
- Paper's stated conclusion for this chunk: "These results suggest that corpus-scale statistical reflection is a viable alternative to iterative search for prompt optimization."
