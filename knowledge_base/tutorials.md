# Tutorials

Hands-on, runnable tutorials (Docker + `uv` + Python + `justfile` where it applies) homed under the research topic they belong to, at `research_topics/<topic>/tutorials/<name>/`. Each folder has an `index.md` in simple language; read one with `ai show research_topics/<topic>/tutorials/<name>` (or open the path). Non-AI tool tutorials (databases, observability, infrastructure, dev tools) stay in [../tutorials/index.md](../tutorials/index.md).

## Agent Harness & Engineering (`agent_harness`)

- [beads](agent_harness/tutorials/beads/index.md) — Beads from zero: a lightweight, dependency-aware issue tracker (embedded Dolt SQL database) for AI coding agents, CLI-first with `--json` for scripting, plus fleet integration.
- [mcp](agent_harness/tutorials/mcp/index.md) — Model Context Protocol (MCP): a weather server and a client.

## Coding Agents & Code Generation (`coding_agents`)

- [herdr](coding_agents/tutorials/herdr/index.md) — Herdr, a mouse-first terminal multiplexer for coding agents: install, the workspace→tab→pane→agent model, pane split/move/resize/zoom/swap/close (mouse + `Ctrl+B` + CLI), the full keymap cheat-sheet, and power features (sessions, agents, remote/phone, notifications, plugins).

## Evaluation & Benchmarks (`evaluation_and_benchmarks`)

- [evals](evaluation_and_benchmarks/tutorials/evals/index.md) — How to measure whether an LLM app actually works: product evals (error analysis, code-graded checks, LLM-as-judge + human alignment, statistics with error bars, RAG metrics, hallucination detectors, agent evals) and model benchmarks (GSM8K, IFEval, prompt sensitivity), all run locally on one helpdesk app and public human-labeled sets, with every result in one table.
- [jev](evaluation_and_benchmarks/tutorials/jev/index.md) — TypeSafe **Jev**, a "System One" model that answers typed questions (Choice / Score / Noul) with probabilities instead of text: notebook with the docs' basic examples, confidence-routing / composite-scoring / fan-out patterns, and an advanced section that scores `~/git/fleet`'s architecture, ranks an improvement backlog and scans all source files against fleet's own ADR rules.

## GraphRAG (`graph_rag`)

- [graph_rag](graph_rag/tutorials/graph_rag/index.md) — Graph RAG from zero: ingest unknown documents, let an LLM discover the schema and extract entities/relationships, insert them into Neo4j with proper labels/relationship types/properties, embed, retrieve (local and global search), keep the graph updated.
- [neo4j](graph_rag/tutorials/neo4j/index.md) — Neo4j graph database from zero: Docker setup, core concepts (nodes, relationships, Cypher), inserting data, basic and advanced queries, Python driver patterns.

## LLM Theory & Multimodal (`llm_theory_and_multimodal`)

- [llm_blocks](llm_theory_and_multimodal/tutorials/llm_blocks/index.md) — LLM building blocks with intuition, from-scratch PyTorch, tests against transformers, and reproducible plots: neural-net basics, tokens/embeddings, attention (GQA, QK-norm, KV cache), RoPE, normalization/residuals, SwiGLU MLP and MoE, linear attention/Gated DeltaNet, sampling, training dynamics, assembling a decoder that matches Qwen3 exactly.

## RAG & Retrieval (`rag_and_retrieval`)

- [rag](rag_and_retrieval/tutorials/rag/index.md) — RAG from zero, hands-on: open-source frameworks (LangChain/LangGraph, LlamaIndex, Haystack, DSPy), systems (LightRAG, RAGFlow, Open WebUI), vector stores and rerankers compared on one corpus and one scoreboard; chunking/hybrid/reranking/query-rewriting tricks measured; evaluation with a local judge and RAGAS; production checklist.

## Training & Self-Evolution (`training_and_self_evolution`)

- [llm_training](training_and_self_evolution/tutorials/llm_training/index.md) — LLM training and fine-tuning from zero on one RTX 4090: build a ~110M Qwen3.5-architecture model from scratch (tokenizer, pre-train, SFT, DPO, GRPO, export to GGUF/Ollama) and fine-tune real Qwen models to a cybersecurity domain (LoRA/QLoRA, catastrophic-forgetting mitigations), every number pulled from a runnable `just` + `uv` project.
