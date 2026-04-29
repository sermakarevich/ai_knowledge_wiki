# ChromaFs: How We Built a Virtual Filesystem for Our Assistant

**Post:** [How We Built a Virtual Filesystem for Our Assistant (Mintlify Engineering, 2024)](https://www.mintlify.com/blog/how-we-built-a-virtual-filesystem-for-our-assistant)

## Human Readable TL;DR

Imagine your AI assistant can only answer questions by flipping through a few random pages of a book at a time -- it misses anything that requires reading the whole chapter. Mintlify's team wanted their documentation assistant to browse docs like a developer browses a codebase. Instead of booting up expensive virtual computers for each user, they invented a fake filesystem that tricks the AI into thinking it's using real Unix commands, when actually it's just querying their existing database. It's like building a movie set instead of a real city -- fast, cheap, and good enough for the job.

## TL;DR

Mintlify replaced traditional RAG (top-K chunk retrieval) for their docs assistant with a virtual filesystem (ChromaFs) that maps Unix commands (`grep`, `cat`, `ls`, `find`) to queries against their existing Chroma vector database. This eliminated the need for per-session sandboxed containers (~46s P90 boot, ~$70K/year) in favor of ~100ms initialization at near-zero marginal cost, while supporting RBAC, lazy remote file loading, and optimized two-stage grep.

---

## Problem & Motivation

Standard RAG only retrieves chunks matching a specific query. This fails when:
- Answers span multiple pages
- Exact syntax the user needs isn't captured in the top-K results
- Reasoning requires traversing or exploring the documentation structure

The desired solution: give agents the ability to explore docs like a developer explores a codebase -- using familiar Unix primitives. The obvious path (real sandboxed containers) proved unviable at scale: P90 boot ~46s, cost ~$70K/year for 850K monthly conversations.

---

## Main Original Ideas

1. **Documentation as Filesystem** -- Treat documentation pages as files and sections as directories. Agents get `grep`, `cat`, `ls`, `find`, `cd` -- standard Unix tools sufficient for exploration without needing true OS virtualization.

2. **ChromaFs: Virtualized Filesystem over a Vector DB** -- Rather than virtualizing hardware, intercept filesystem calls and translate them into Chroma database queries. Reuses existing search infrastructure with zero new systems.

3. **Gzipped Path Tree for Directory Bootstrapping** -- Store the entire directory structure as gzipped JSON in Chroma (`__path_tree__`). On init, decompress into in-memory `Set<string>` and `Map<string, string[]>`. All `ls`/`cd`/`find` operations hit local memory, not the network.

4. **Metadata-Driven RBAC** -- Embed `isPublic` and `groups` fields in the path tree. Prune inaccessible paths before exposing the filesystem to the agent. No Linux permissions, no per-tier container images -- just metadata filtering.

5. **Two-Stage Grep Optimization** -- Recursive grep over a network DB would be too slow. Stage 1: coarse filter via Chroma (`$contains` / `$regex`) to find candidate files. Stage 2: bulk-prefetch matched chunks to Redis, rewrite grep to target only those files, execute final filter in-memory via just-bash.

6. **Lazy Remote File Pointers** -- Large files (e.g., OpenAPI specs in S3) appear in directory listings but are only fetched on `cat`. Stateless sessions: all writes throw `EROFS` errors, no cleanup needed.

---

## Key Findings

| Approach | P90 Boot Time | Marginal Cost / Conversation |
|---|---|---|
| Sandboxed containers | ~46 seconds | ~$0.0137 (~$70K/year) |
| **ChromaFs** | **~100 milliseconds** | **~$0** |

- 460x reduction in session initialization latency
- Zero additional infrastructure cost (reuses existing Chroma)
- Handles 850,000 monthly conversations, 30,000+ daily
- Access control is cleaner than OS-level `chmod`: metadata pruning means the agent literally cannot see unauthorized paths

---

## Suggestions & Future Directions

1. **Write support** -- Currently all mutations throw `EROFS`. Enabling stateful writes would unlock agentic documentation editing workflows.
2. **Broader filesystem backends** -- The `IFileSystem` interface from just-bash makes it straightforward to plug in other backends (S3, databases, APIs) beyond Chroma.
3. **Agent filesystem as a pattern** -- The post implicitly suggests this architecture generalizes: any agent operating over structured content (wikis, codebases, knowledge bases) could benefit from a virtualized filesystem layer over existing search infrastructure.

---

## Authors & Institutions

Mintlify Engineering Team (Mintlify, Inc.)
