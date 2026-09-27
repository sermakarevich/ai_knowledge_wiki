---
type: Research
title: "AgentBrain: which agent second-brain projects are worth using"
description: "Comparison of 20 agent second-brain GitHub projects across capture, linking, memory/recall, and agentic action, converging on a local-first Markdown-plus-graph pipeline with gated writes and skill-packaged action."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-26T00:00:00Z
focus: "Which of these 20 agent second-brain GitHub projects are worth using for a system that captures sources, connects ideas, remembers context, and helps agents act on it, and how do they compare across capture, linking, memory/recall, and agentic action?"
topics:
  - capture-ingest-lanes
  - linking-kg-wiki
  - memory-recall-substrate
  - agentic-action-harness
lenses:
  - tech
  - ai
sources:
  processed: 20
  in_kb: 0
  unreachable: 0
runs:
  - { at: 2026-09-26, added: 20 }
tags: [agent-memory, second-brain, knowledge-graph, recall, skills]
---

# AgentBrain: which agent second-brain projects are worth using

## How to work through this

1. Start with [[overview|overview]] for the topic-level picture (TL;DR, what is established, contested, and open).
2. Read [[digest|digest]] for the full synthesis across all four lanes, then the per-dimension digests in order: capture → linking → memory/recall → action.
3. Check [[agreements|agreements]] for claims backed by two or more independent repos, [[disagreements|disagreements]] for the verdict on contradictions (none found), and [[open_questions|open_questions]] for the 12 unanswered selection questions.
4. Use the lenses below when building: `tech` for system design, `ai` for retrieval and memory architecture.
5. Treat every quantitative claim (LoCoMo, LongMemEval, R@5/token figures) as vendor-reported and unevenly evidenced — let structural fit drive project selection, not benchmarks.

## Cross-cutting

- The 20 projects converge on one architecture: a local-first pipeline from heterogeneous capture lanes into typed, provenance-preserving Markdown stores, then an explicit linking/graph layer, then hybrid scoped recall, then skill-packaged agentic action — with network and model calls at opt-in edges.
- Plain Markdown files are the human-readable store (11 repos); the graph or index is a derived companion layer, not a replacement.
- Local-first by default (12 repos): capture→store→retrieve runs on-device; transcription, enrichment, embeddings, and sync are explicit opt-in edges.
- Provenance is captured at ingest time and kept visible (digests, ledgers, edge tags, write records), never reconstructed later.
- Recall fuses lexical, vector, and graph/structure signals (8 repos) with a deterministic BM25/FTS fallback; flat chat history and single-method vector retrieval are insufficient on their own.
- Graph and link writes are gated — staging, approval, or verdict stands between proposal and canon; recall is scoped and budgeted rather than total.
- Capture and recall are separate seams: one path records experience, a later path injects it, often across agents and sessions.
- Memory feeds action in one loop: skills-as-markdown act on the store under bounded tools, checkpointed durable state, and human gates on outward effects.
- No contradictions were found across the 20 sources; all differences are design choices (graph weight, LLM dependence, store shape, orchestration weight, freshness math, tenancy), not factual disputes.
- Open measurement gaps: no action harness reports task-success/latency/precision for the full loop, and recall benchmarks are vendor-reported — comparative effectiveness remains unproven.

## Lenses

| lens | for |
|---|---|
| [[lenses/tech|tech]] | engineers building agent second-brain systems (store shape, graph weight, capture mouths, gating, deployment) |
| [[lenses/ai|ai]] | AI engineers working with agent memory and RAG (retrieval fusion, distillation, scoping, LLM placement, freshness) |

## Sub-topics

| sub-topic | in one sentence | sources |
|---|---|---|
| [[topics/01-capture-ingest-lanes/digest|capture-ingest-lanes]] | Capture across these systems is a local-first, provenance-preserving lane from heterogeneous sources (clipboard, chat, platforms, libraries, folder drops) into a typed store, with cloud calls confined to opt-in transcription or enrichment. | 5 |
| [[topics/02-linking-kg-wiki/digest|linking-kg-wiki]] | Durable agent memory comes from compiling sources into interlinked markdown plus an explicit graph/provenance layer, with retrieval fusing lexical, vector, and graph signals and every new link gated by review or verdict. | 4 |
| [[topics/03-memory-recall-substrate/digest|memory-recall-substrate]] | Agent memory works best as a durable, inspectable substrate — layered or file-shaped stores of facts, skills, and experience — retrieved through hybrid (BM25 + vector + graph) scoped recall rather than flat chat replay or pure vector search. | 6 |
| [[topics/04-agentic-action-harness/digest|agentic-action-harness]] | Durable agent action comes from skill-packaged playbooks executed over a memory substrate, with delegated multi-agent orchestration, checkpointed recovery, provider-routed model calls, and human approval gates. | 5 |

## Sources

| source | kind | folder |
|---|---|---|
| TencentDBAgentMemory | repo | research_topics/agent_memory/TencentDBAgentMemory |
| ClaudeObsidian | repo | research_topics/agent_memory/ClaudeObsidian |
| Swarmvault | repo | research_topics/agent_memory/Swarmvault |
| OpenSecondBrain | repo | research_topics/agent_memory/OpenSecondBrain |
| OpenViking | repo | research_topics/agent_memory/OpenViking |
| SageWiki | repo | research_topics/agent_memory/SageWiki |
| CogSecondBrain | repo | research_topics/agent_memory/CogSecondBrain |
| AgentSecondBrain | repo | research_topics/agent_memory/AgentSecondBrain |
| Chubbyskills | repo | research_topics/agent_memory/Chubbyskills |
| SecondBrainCloudflare | repo | research_topics/agent_memory/SecondBrainCloudflare |
| Mateclaw | repo | research_topics/agent_memory/Mateclaw |
| RowBot | repo | research_topics/agent_memory/RowBot |
| DocsAgent | repo | research_topics/agent_memory/DocsAgent |
| DocMason | repo | research_topics/agent_memory/DocMason |
| Agentmemory | repo | research_topics/agent_memory/Agentmemory |
| MemU | repo | research_topics/agent_memory/MemU |
| Hindsight | repo | research_topics/agent_memory/Hindsight |
| VaultCurate | repo | research_topics/agent_memory/VaultCurate |
| OpenWiki | repo | research_topics/agent_memory/OpenWiki |
| Makerskills | repo | research_topics/agent_memory/Makerskills |
