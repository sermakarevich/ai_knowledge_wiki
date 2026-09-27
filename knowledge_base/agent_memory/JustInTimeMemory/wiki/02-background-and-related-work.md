> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Background and Related Work: Read-Time vs Write-Time Memory Curation
**In one sentence:** JITMEM defers curation to read time so a task-conditioned curator can synthesize a compact payload from raw trajectories for the current task, simplifying credit assignment and outperforming write-time curators.
## Key points
- Write-time curation suffers because a trajectory admits many possible lessons but the downstream task is unknown at write time, so curation happens before the task is known.
- JITMEM keeps a passive episodic bank of raw trajectories with nothing discarded at write time; at read time a retriever selects relevant traces and curator πϕ synthesizes a compact task-conditioned payload.
- The same stored trajectory can yield different payloads for different downstream queries, paralleling the reconstructive episodic-memory view of Schacter & Addis (2007).
- Read-time curation collapses credit assignment to a single interaction because the payload is consumed immediately by the current task, avoiding the task-grouping scaffolds needed by learned write-time curators such as Ouyang et al. (2026a).
- JITMEM reports +16.2 (ALFWorld), +16.3 (WebShop), and +3.9 (τ2-bench) absolute success-rate points over all baselines, with compact payloads cutting input tokens 50.3%–56.3% and executor steps 28.4%–31.4% relative to write-time methods.
- Even untrained, read-time curation beats same-model write-time curation (WebShop JITMEM-gemini 61.0 SR vs SkillOS 41.0 SR, both with Gemini-2.5-Pro curator and executor); RL training compounds the gain and the trained curator transfers to stronger executors without retraining.
- Ablations attribute independent gains to task-conditioned curation, quality-filtered storage, and retention of raw trajectories.
---
## Motivation tail: deferring curation to read time
Both failure costs stem from the same root cause: "curation happens before the downstream task is known." JITMEM instead defers curation until read time, "just in time, when the task to be solved is known."

Pipeline: memory bank remains a passive episodic store of raw trajectories; when a new task arrives, a retriever selects relevant traces and a memory curator jointly reads those traces plus the current task to synthesize a compact, task-conditioned payload. Because the curator sees the task, "it can extract exactly the information that is useful for that task."

Learning claim: "the curator can be optimized directly against same-task success, reducing the credit-assignment problem to a single interaction rather than waiting for uncertain future utility," avoiding grouping related tasks to manufacture a signal as in Ouyang et al. (2026a), "whose ablations identify grouping as a major contributor to performance." Instantiation: "JITMEM instantiates this principle as an RL-trained read-time curator operating over a persistent streaming memory bank. Figure 1 provides an overview of the system."

## Contributions
- "Read-time curation enables task-adaptive memory. By deferring curation to read time, the curator sees the current task and can tailor its distillation accordingly. The same stored trajectory yields different payloads for different tasks, a property that write-time curators cannot provide."
- "Read-time curation simplifies credit assignment. Since the curated payload is consumed on the same task it was produced for, the curator's reward is immediate. This collapses credit assignment to a single step, eliminating the task-grouping scaffolds required by learned write-time curators."
- "JITMEM: a read-time memory curator. We introduce JITMEM, which stores raw trajectories losslessly and synthesizes task-conditioned payloads at read time via a curator trained with GRPO over a persistent streaming memory bank."
- "Empirical validation and analysis. Across ALFWorld, WebShop, and τ2-bench, JITMEM outperforms all baselines, including RL-trained write-time curators."

## Related work: heuristic write-time memory
"The dominant approach in agentic memory stores a distilled artifact at the end of each task and retrieves it by similarity at inference," differing in what is distilled: "verbal reflections (Shinn et al., 2023), extracted insights (Zhao et al., 2024), memory streams with periodic summarization (Park et al., 2023), executable skills (Wang et al., 2023), induced workflows (Wang et al., 2024b), memory items at multiple granularities (Fang et al., 2026), self-organizing linked notes (Xu et al., 2026), and reasoning strategies from both successes and failures (Ouyang et al., 2026b)." Ma et al. (2026) use "prediction-error signals to decide which experiences deserve distillation." Shared properties: "curation is triggered at write time, and the stored artifact is query-independent, fixed before any future task is seen." Most competitive instance: "ReasoningBank (Ouyang et al., 2026b)," which "distills transferable reasoning strategies via a prompted LLM and retrieves them by cosine similarity."

## Related work: learned write-time memory
Retroformer (Yao et al., 2024) "fine-tunes a retrospective model to rewrite the agent's prompt, though it operates within a single task instance." RL-optimized memory operations: "Memory-R1 (Yan et al., 2026), Agentic Memory (Yu et al., 2026a) with a progressive GRPO curriculum, Memento (Zhou et al., 2025) with a case-selection policy, and Memory as a Controlled Process (Jiang et al., 2026) with a lightweight control policy." MemRefine (Kim et al., 2026) "compresses the stored bank offline via LLM-guided merging." Common property: "All of these operate at write or maintenance time." Closest prior: "SkillOS (Ouyang et al., 2026a)," which "trains a skill curator with GRPO, but must group related tasks to manufacture a delayed learning signal because the reward for a write decision arrives only when a future query matches."

## Related work: learned in-session working memory vs cross-task memory
RL-managed context within a single execution: "Sculptor (Li et al., 2026a) and ContextCurator (Li et al., 2026b) train policies to compress or restructure the accumulating observation history, MemSearcher (Yuan et al., 2025) iteratively rewrites a fixed-length working memory, and Proactive Memory Agent (Wu et al., 2026b) learns when to inject reminders during long-horizon tasks." Recuris (Yu et al., 2026b) "combines step-level working-memory selection with cross-task skill evolution." Distinction: "All optimize in-session or turn-level context; JITMEM instead curates persistent episodic memory across tasks."

## Related work: read-time and test-time context processing
- Synapse (Zheng et al., 2024) "retrieves full trajectories as exemplars but does not distill or condition on the incoming task."
- MemToolAgent (Er et al., 2026) "adapts how many entries to retrieve based on the similarity distribution, but the entries themselves are distilled at write time and returned unchanged."
- "Decocted experience (Shen et al., 2026) distills past trajectories into lessons, but each lesson is distilled query-independently and the policy is prompted rather than learned."
- "Agentic Plan Caching (Zhang et al., 2026) extracts reusable plan templates, though the plan structure is fixed at extraction."
- "SkillTTA (Wang et al., 2026) synthesizes a task-conditioned skill at test time via meta prompt optimization, but from a preconstructed pool that does not grow during deployment."
- "MemHarness (Wu et al., 2026a), concurrent with our work, also curates at read time: it trains a single policy with GRPO that both adapts retrieved experience and executes the task; because curation and execution are entangled in one model, the trained policy does not transfer across executors." By contrast: "JITMEM decouples the curator from the executor, enabling cross-executor transfer, and operates over a persistent streaming bank. See Luo et al. (2026) for a broader survey."

## Method setup (streaming setting)
"In a streaming task setting, an agent receives a sequence of tasks {x1, x2, ..., xT} one at a time. At each step t, the agent interacts with an environment to solve xt, producing a trajectory ξt = (o1, a1, ..., on, an) of interleaved observations oi and actions ai, and receives a task-success reward rt ∈ [0, 1]." JITMEM builds on four components "(Figure 1): a memory bank Mt that stores raw trajectories from past tasks, a retriever R, a memory curator πϕ, and a frozen agent executor." "Only the curator is trainable. The objective is to maximize expected cumulative task success maxϕ E Σ_{t=1}^{T} rt."

**Covers:** chunk 02-providing-another-with-an-object-placement-strat (motivation tail + contributions + Related Work §2 + Method §3 opening through streaming-setting definition)
