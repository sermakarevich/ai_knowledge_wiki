# Don't Retrieve, Navigate: Distilling Enterprise Knowledge into Navigable Agent Skills for QA and RAG

**Paper:** [Don't Retrieve, Navigate: Distilling Enterprise Knowledge into Navigable Agent Skills for QA and RAG (Yiqun Sun, Pengfei Wei, Lawrence B. Hsieh, 2026)](https://arxiv.org/pdf/2604.14572)

## Human Readable TL;DR

Imagine a library where you usually just yell a question at the librarian and they hand you a pile of pages that might have the answer. That's how most AI assistants work today -- they guess which pages match your question. This paper instead turns the whole library into a browsable filing cabinet with labeled drawers and folders, and hands the AI the map. The AI now walks to the right drawer, opens the right folder, and picks the exact document it needs -- so it gives you better, more complete answers even when your question touches several topics.

## TL;DR

CORPUS2SKILL replaces retrieve-then-generate RAG with a compile-then-navigate-then-generate paradigm. Offline, it transforms a document corpus into a hierarchical filesystem of `SKILL.md` and `INDEX.md` files via iterative K-Means clustering plus LLM summarization. At query time, an LLM agent navigates this tree using only file-browsing and `get_document` tools -- no embedding index, no vector search. On the WixQA enterprise QA benchmark, it beats dense, hybrid, RAPTOR, and agentic RAG baselines across six quality metrics (e.g., +19% Token F1 over Agentic, +27% over Dense), at roughly 1.75x the per-query cost of agentic RAG.

---

## Problem & Motivation

Traditional RAG treats the LLM as a passive consumer of retrieved passages. The model has no "map" of the knowledge base -- it cannot see how topics are organized, cannot tell whether retrieved evidence is complete, and cannot reason about alternative search paths. This becomes acute for multi-topic enterprise queries like "How do I switch my Wix business from sole proprietorship to LLC?" where relevant evidence is scattered.

Agentic RAG adds iterative search but still operates "without a map" -- each search query is a shot in the dark guided by the agent's priors, not by knowledge of the corpus. Hierarchical methods like RAPTOR and GraphRAG build structure during indexing but collapse back to embedding similarity at query time, so the hierarchy remains invisible to the agent. Meanwhile, LLM-agent research shows that filesystem-style "skill packages" with progressive disclosure let agents operate effectively over large instruction sets. CORPUS2SKILL repurposes that mechanism: make the corpus structure itself the primary interface the agent reasons over.

---

## Main Original Ideas

1. **Compile-then-navigate-then-generate paradigm.** Shifts investment from query-time retrieval tuning to offline compilation of a navigable structure, then lets the agent browse that structure at query time. Positions the hierarchy itself -- not a retriever -- as the LLM's interface to the corpus.

2. **Corpus-as-skill-tree.** Each node in the document hierarchy is materialized as a directory containing `SKILL.md` (root) or `INDEX.md` (subnodes) with YAML frontmatter, a summary, listings of children, and routing instructions. Full documents live outside the tree in `documents.json` keyed by content hash, so navigation files stay small.

3. **Iterative embed-cluster-summarize loop.** Bottom-up hierarchy construction where each level (i) clusters current embeddings with K-Means, (ii) has an LLM summarize each cluster from representative members, (iii) re-embeds those summaries, and repeats until the number of top-level clusters drops below `K`. Depth grows as `O(log_p N)`.

4. **Embedding-free serve phase.** At query time there is no vector database, no FAISS index, no BM25 -- the agent gets only two tools: file `view` (via `code_execution`) and `get_document(doc_id)`. This cleanly separates navigational actions from evidence retrieval.

5. **Skills API with progressive disclosure.** Only skill names and one-line descriptions (~200 tokens) are preloaded; `SKILL.md` / `INDEX.md` bodies are pulled in on demand. The agent sees a "bird's-eye view" first and drills in only where promising.

6. **Two-tool, 2-3-turn navigation workflow.** A grounded answer typically requires one read of a top-level `SKILL.md`, one or two `INDEX.md` reads, then one or more `get_document` calls -- enabling explicit backtracking and cross-branch synthesis behaviors that flat retrieval cannot express.

---

## Key Findings

**Main quality comparison on WixQA (6,221 support articles, 200 expert questions; all systems use Claude Sonnet for generation):**

| System | Token F1 | Factuality | Context Recall | $/query |
|---|---|---|---|---|
| BM25 | 0.335 | 0.608 | 0.479 | low |
| Dense (Qwen3-Emb + FAISS) | 0.363 | 0.641 | 0.512 | low |
| Hybrid (RRF) | 0.371 | 0.654 | 0.528 | low |
| RAPTOR | 0.402 | 0.675 | 0.616 | $0.012 |
| Agentic RAG (10 rounds) | 0.388 | 0.724 | 0.481 | $0.098 |
| **CORPUS2SKILL** | **0.460** | **0.729** | **0.652** | $0.172 |

- **+19% Token F1 over Agentic**, **+27% over Dense**, best across all six quality metrics.
- Context Recall of 0.652 vs. 0.481 for Agentic shows markedly more complete evidence gathering.
- CORPUS2SKILL produced fewer output tokens per query (752) than Agentic (1,391) despite higher input tokens (53,487) -- answers are more targeted.
- Cost is ~1.75x Agentic and ~14x RAPTOR, driven by Skills API input-token overhead.

**Ablations:**
- Narrower tree (`p=5`, 4 levels) nudges quality up (F1 0.461, Factuality 0.736) for +8% cost.
- Wider, shallow tree (`p=20`, 2 skills × ~3k docs each) breaks routing: F1 drops 21%, Factuality drops 44%.
- Agent exploration budget (5 / 10 / 20 rounds) barely moves quality -- the hierarchy is self-sufficient.
- Swapping serving LLM Sonnet → Haiku: -8% F1, -12% Factuality, **+Context Recall to 0.705**, -50% cost. The compiled tree is robust to the agent LLM.

**Compilation cost:** 6.5 minutes on a 32-CPU server for the full WixQA corpus (branching `p=10`, `K=7`, 3-level tree with 6 top skills, 665 navigation files, 13 MB document store).

**Failure mode:** Hard single-path clustering creates blind spots for documents spanning multiple topics.

---

## Suggestions & Future Directions

1. **Prompt caching** to reduce input-token cost from repeated navigation file inclusion under the Skills API.
2. **Soft or multi-parent cluster assignments** to handle documents belonging to more than one topic and eliminate the dominant failure mode.
3. **Incremental compilation** -- current pipeline is batch; additions/deletions to the corpus require recompilation, risking stale answers.
4. **Scaling beyond Skills API limits** -- explore alternative hierarchy layouts when corpus size exceeds per-skill / per-file API constraints.
5. **Reserve for high-value queries** -- given per-query cost, route low-value traffic to cheaper flat RAG and reserve CORPUS2SKILL for queries where quality justifies ~$0.17.
6. **Human-in-the-loop verification** for high-stakes deployments; summarization may also inadvertently reveal corpus structure, which matters for sensitive domains.

---

## Authors & Institutions

Yiqun Sun, Pengfei Wei, Lawrence B. Hsieh -- Magellan Technology Research Institute (MTRI).
