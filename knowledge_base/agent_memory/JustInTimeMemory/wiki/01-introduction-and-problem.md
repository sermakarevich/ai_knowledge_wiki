> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Introduction and Problem: Write-Time vs Just-in-Time Memory Curation
**In one sentence:** The paper argues memory should not be distilled into fixed artifacts at write time — when the future query is unknown — but kept as raw trajectories and curated just-in-time at read time into a task-adaptive payload trained on immediate task success.
## Key points
- Agentic memory systems reuse past experience, but most curate at write time: a completed trajectory is distilled into a fixed artifact (reflection, workflow, skill, reasoning strategy) later retrieved by similarity.
- Write-time curation forces deciding what is worth remembering before the future query is known, irreversibly discarding information and producing a query-independent summary that must serve many downstream tasks.
- Learning a write-time curator is hard because a storage decision's value may only appear when a relevant query arrives many tasks later — a long-horizon credit-assignment problem.
- Just-in-Time Memory (JITMEM) instead retains raw trajectories and defers curation to read time, when the current task is known: a curator synthesizes a compact, task-adaptive payload from retrieved traces plus the new task.
- Because the payload is consumed on the same task, the curator trains directly from immediate task success, avoiding delayed utility signals and artificial grouping of related tasks.
- Across ALFWorld, WebShop, and τ2-bench, JITMEM beats no-memory agents and heuristic/learned write-time methods by 16.2, 16.3, and 3.9 absolute success-rate points over the strongest baseline, respectively.
- Even an untrained curator is already competitive with or surpasses these baselines, showing read-time task-adaptive curation itself is a major source of gain; training compounds it.
---
## Paper identity
**Covers:** title block and arXiv header (arXiv:2609.27334v1 [cs.AI] 23 Sep 2026)

Title: "Just-in-Time Memory: Learning to Curate Task-Adaptive Memory for LLM Agents". Authors: Yefan Zhou*, Yang Li*, Zeyu Leo Liu, Semih Yavuz, Shafiq Joty, Salesforce AI Research (* equal contribution).

## The future-utility question: when should memory be shaped?
**Covers:** Section 1 Introduction, framing

LLM agents are increasingly expected to solve sequences of tasks over time rather than isolated problems. Starting from scratch each task wastes prior experience, motivating agentic memory that persists past trajectories for future behavior. Despite design variation, these methods share one objective: "memory is useful only insofar as it improves future task performance." From this future-utility perspective the paper asks: "when in the agent lifecycle should memory be shaped to best serve that objective?"

## Write-time curation and its two costs
**Covers:** Section 1, write-time paradigm description

Dominant approach: after a task completes, distill its trajectory into a persistent artifact — "verbal reflections", "natural-language insights", "reusable workflows", "executable skills", or "transferable reasoning strategies" — then at inference retrieve artifacts via similarity search into context. Verbatim key claim: "the memory artifact is already fixed before the future query is known" and "Curating memory at write time forces the system to decide what matters before the future task is known."

Two fundamental costs stated:

1. "information loss is premature and irreversible: once details are discarded, a later task that depends on them has no way to recover them."
2. "a single fixed artifact must serve many different future queries, even though the same trajectory may be useful in different ways depending on the task" — e.g. a household interaction might teach one task a state-transition pattern such as heating or cooling an object, while (example truncated in chunk).

## JITMEM inference and training pipeline (Figure 1)
**Covers:** Figure 1 caption and diagram text

Inference (a): given current task xt, retriever fetches raw trajectories from the memory bank; curator distills them conditioned on xt into a task-adaptive payload injected into the executor's context; after execution an executor-as-judge assesses correctness and successful trajectories are stored back. Example payload sections visible: "Relevant Memories", "Strategies Extracted (1. Locate the book …)", "Guidance for This Task (1. Locate the book at areas such as tables … 2. Pick up the book, use the 'take' action …)", "Action Plan (1. Go to a likely location … 2. Take the book…)" for task "Put a book in sofa" with retrieved example "place a pencil on a desk".

Training (b): at each step a task is sampled, relevant trajectories retrieved from a fixed training bank, curator generates multiple candidate payloads, the frozen executor attempts the task with each payload and returns immediate task reward used to update the curator via GRPO.
