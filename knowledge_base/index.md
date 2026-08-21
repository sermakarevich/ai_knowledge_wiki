# Knowledge Base

Curated index of the papers vault, organized into **20 thematic categories**. Each category links to its own page with Obsidian-style refs to every paper in that topic plus a 1-2 sentence summary.

## Categories

- [[agent_harness/agent_harness|Agent Harness & Engineering]] — The deterministic scaffolding around the LLM: tool routing, context management, permissions, execution. Central thesis: harness quality is the new moat.
- [[loop_engineering/loop_engineering|Loop Engineering]] — Engineering the agentic control loop itself: stop prompting agents, design the loops that prompt them. Triggers, verifiable goals, stop conditions, loop safety, and the Ralph loop.
- [[graph_engineering/graph_engineering|Graph Engineering]] — Structuring agentic systems as explicit graphs (nodes, edges, shared state) above loop engineering: the 2026 graph-engineering discourse, topology generation, framework practice, and enterprise governance.
- [[multi_agent_systems/multi_agent_systems|Multi-Agent Systems]] — Coordination, workflow orchestration, collective intelligence, failure attribution, and scaling laws across LLM agents.
- [[skills_and_context_engineering/skills_and_context_engineering|Skills & Context Engineering]] — Reusable procedural skills, prompt/context evolution, and continual learning through externalized artifacts rather than weight updates.
- [[graph_rag/graph_rag|GraphRAG]] — Graph-based retrieval-augmented generation: knowledge-graph indexing and retrieval, measured retrieval quality (recall@k/MRR, multi-hop golden datasets), and retrieval failure modes in production.
- [[rag_and_retrieval/rag_and_retrieval|RAG & Retrieval]] — Retrieval-augmented generation, chunking strategies, document segmentation, knowledge catalogs, and post-RAG paradigms (filesystems, analytical search, skill compilation).
- [[agent_memory/agent_memory|Agent Memory]] — Persistent memory for agents: short-term context management, cross-session memory, graph/associative memory, and cross-domain transfer.
- [[coding_agents/coding_agents|Coding Agents & Code Generation]] — LLM-powered coding agents, code generation, program analysis, SE workflows, and spec-driven development.
- [[code_review/code_review|Code Review]] — Classical software-engineering studies of human Modern Code Review and the new wave of LLM-powered PR review systems; evolvability dominates over bug-finding, whole-repo context separates frontier from diff-only linters.
- [[llm_theory_and_multimodal/llm_theory_and_multimodal|LLM Theory & Multimodal]] — Core LLM theory, transformer architecture, reasoning mechanics, scaling properties, and multimodal models (vision + audio + language).
- [[models/models|Models]] — Specific LLM and multimodal model releases — flagship/frontier model cards, technical reports, and architectural release notes (MoE, Mamba-Transformer hybrids, omnimodal stacks).
- [[training_and_self_evolution/training_and_self_evolution|Training & Self-Evolution]] — Training methods, post-training, self-improvement loops, and closed-loop agentic systems that improve their own data, architecture, or algorithms.
- [[evaluation_and_benchmarks/evaluation_and_benchmarks|Evaluation & Benchmarks]] — Benchmarks, evaluation methodologies, verifiers, and empirical head-to-head comparisons of LLMs and agent systems. (folder created 2026-07-01; was listed here but missing on disk)
- [[safety_and_security/safety_and_security|Safety & Security]] — AI safety, adversarial attacks, privacy, manipulation, and verified/constrained agents — both offensive and defensive research.
- [[claude_ecosystem/claude_ecosystem|Claude Ecosystem]] — Anthropic's Claude models and Claude Code: system cards, best practices, migration guides, reverse-engineered internals, and Mythos.
- [[ai_society_and_economy/ai_society_and_economy|AI Society & Economy]] — AI's impact on work, learning, organizational design, and economic productivity — covering skill formation, workforce restructuring, and AI-vs-human comparisons.
- [[ai_management/ai_management|AI Management]] — How management, teams, and organizations should operate in the AI era: workforce design, team coordination, organizational workflow redesign, and leadership practices for AI-first environments.
- [[ml_systems/ml_systems|ML Systems & Serving]] — ML infrastructure, model serving, request routing, deployment patterns, traffic management, and production system design for large-scale ML.
- [[computational_neuroscience/computational_neuroscience|Computational Neuroscience]] — Connectomics, functional brain imaging, neural simulation, and whole-brain emulation feasibility, from simple organisms up to humans.
