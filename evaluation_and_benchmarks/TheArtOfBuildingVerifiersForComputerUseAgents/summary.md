# The Art of Building Verifiers for Computer Use Agents

**Paper:** [The Art of Building Verifiers for Computer Use Agents (Rosset et al., 2025)](https://arxiv.org/abs/2604.06240)

## Human Readable TL;DR

Imagine you hire someone to do errands on your computer -- book flights, fill out forms, navigate websites. How do you know they actually did the job right, and didn't just say they did? This paper builds a "quality inspector" system that watches everything the agent does (every click, every screenshot) and grades both the process and the final result. It's like having a meticulous supervisor who checks the receipts, not just the agent's word. The inspector catches lies and excuses, and rarely gives a passing grade when the job wasn't actually done.

## TL;DR

This paper presents the Universal Verifier (UV), a principled architecture for evaluating Computer Use Agent (CUA) trajectories. UV separates process rewards from outcome labels, uses non-overlapping rubric criteria generated independently of the trajectory, and employs a divide-and-conquer context management scheme to ground verification in screenshot evidence. On the new CUAVerifierBench benchmark, UV achieves near-zero false positive rates while maintaining Cohen's kappa comparable to inter-annotator agreement, substantially outperforming WebVoyager and WebJudge baselines.

---

## Problem & Motivation

Computer Use Agents (CUAs) can autonomously browse the web, fill forms, and navigate interfaces -- but reliably verifying whether they actually succeeded is an unsolved bottleneck. CUA trajectories are long, visually dense, and ambiguous: agents may partially complete tasks, take unconventional valid paths, or fail subtly at intermediate steps. Existing verifiers like WebVoyager and WebJudge suffer from high false positive rates (>20-45%), often trusting the agent's self-reported answers rather than grounding in visual evidence. This corrupts both evaluation benchmarks and training reward signals. The paper argues that without trustworthy verification, CUA progress itself is unreliable.

---

## Main Original Ideas

1. **Rubrics with Non-overlapping, Independently Generated Criteria** -- Rubrics are generated solely from the task description (never from the trajectory), preventing confirmation bias. The design explicitly avoids phantom criteria, cascading errors, and includes conditional criteria that activate based on runtime conditions.

2. **Separation of Process and Outcome Rewards** -- The verifier produces both a continuous process score (r_proc, 0.0-1.0) evaluating execution quality across sub-goals, and a binary outcome label (r_out) assessing whether the user's goal was achieved. These signals intentionally diverge when environmental blockers prevent success despite correct agent behavior.

3. **Controllable vs. Uncontrollable Failure Attribution** -- A cascading-error-free scoring strategy distinguishes agent mistakes (intent mismatch, hallucinations, execution errors) from external impediments (CAPTCHAs, login walls, availability constraints), preventing unfair penalization.

4. **Divide-and-Conquer Context Management** -- Instead of dumping all screenshots into one LLM call, UV scores each screenshot's relevance per rubric criterion, selects top-k most relevant screenshots per criterion, and performs focused evidence analysis. This overcomes token limits and needle-in-a-haystack problems.

5. **Two-Pass Hallucination Detection** -- Each criterion is scored once with only text actions and once with full screenshot access. Discrepancies between the two passes surface agent hallucinations and fabrications.

6. **CUAVerifierBench** -- A new benchmark with 246 human-labeled CUA trajectories (140 internal + 106 external) providing both process and outcome labels, enabling standardized verifier evaluation.

---

## Key Findings

| Metric | Universal Verifier | WebJudge | WebVoyager |
|---|---|---|---|
| **Outcome Cohen's kappa (Internal)** | **0.64** | 0.44 | 0.31 |
| **Outcome Cohen's kappa (Browserbase)** | **0.58** | 0.26 | 0.13 |
| **Outcome FPR (Internal)** | **0.01** | 0.22 | 0.45 |
| **Outcome FPR (Browserbase)** | **0.08** | 0.22+ | 0.45+ |

- UV achieves near-zero false positive rates, a critical property for reliable training signals -- existing verifiers falsely credit success 22-45% of the time
- Upgrading baseline backbones to GPT-5.2 reduces their FPR but sharply increases FNR, confirming UV's advantage is architectural, not model-driven
- UV's agreement with human labels (kappa 0.58 outcome, 0.43 process) matches inter-annotator agreement among human experts (kappa 0.53-0.57 outcome, 0.36-0.45 process)
- UV-informed annotations substantially improved human annotator agreement (outcome kappa rose from 0.39 to 0.63), with 16.6% of labels flipping -- mostly from "success" to "failure"
- Large-scale re-scoring of existing benchmarks (WebVoyager, Online-Mind2Web, WebTailBench) found FPR consistently above 20%, suggesting current benchmarks over-credit agent success
- An auto-research agent (Claude Code + Opus 4.6) reached ~70% of human expert verifier quality in ~5% of the time (1 day vs. 3 weeks), but struggled with structural design breakthroughs -- when initialized from the expert's best config, it surpassed the expert peak

---

## Suggestions & Future Directions

1. **Human-AI collaborative verifier design** -- The auto-research study suggests a complementary model where human intuition drives foundational architectural decisions while automated agents optimize and fine-tune within that framework.

2. **Improved process evaluation** -- Process scoring showed lower inter-annotator agreement than outcome scoring, indicating inherent subjectivity. Future work should develop more objective process evaluation criteria.

3. **Benchmark recalibration** -- The finding that existing benchmarks systematically over-credit agent success (FPR >20%) calls for community-wide re-evaluation of CUA benchmark results.

4. **Training signal integration** -- The separated process/outcome rewards and controllable/uncontrollable failure attribution are designed to directly improve reinforcement learning training of CUAs, but this downstream application remains to be validated at scale.

5. **Scaling context management** -- The divide-and-conquer approach opens paths for handling even longer trajectories and richer multimodal evidence as CUA tasks grow in complexity.

---

## Authors & Institutions

Corby Rosset (Microsoft Research), Pratyusha Sharma (Microsoft Research), Andrew Zhao (Microsoft Research), Miguel Gonzalez-Fernandez (Browserbase), Ahmed Awadallah (Microsoft Research)
