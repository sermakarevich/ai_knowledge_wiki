# Bridging Code Property Graphs and Language Models for Program Analysis

**Paper:** [Bridging Code Property Graphs and Language Models for Program Analysis (Lekssays, 2026)](https://arxiv.org/abs/2603.24837v1)

## Human Readable TL;DR

Imagine a security expert trying to find hidden flaws in a massive software project -- like searching for a single weak link in a chain that stretches across thousands of pages of instructions. Current AI assistants can only look at a few pages at a time and miss problems that span across many pages. This paper introduces a tool called codebadger that acts like a smart magnifying glass for AI: instead of reading everything, it lets the AI follow specific trails through the code -- like tracing a water leak back to its source -- so it can find and fix security problems in huge software projects that were previously too large for AI to handle.

## TL;DR

codebadger is an open-source MCP server that bridges Joern's Code Property Graph (CPG) engine with LLMs, providing high-level tools for program slicing, taint tracking, data flow analysis, and semantic code navigation. This eliminates the need for LLMs to generate complex CPGQL queries or load entire repositories into context windows. The system was validated by auditing memory safety in an 8,000-method codebase (GGML), discovering a previously unreported buffer overflow in libtiff, and generating a correct first-attempt patch for CVE-2025-6021 in libxml2.

---

## Problem & Motivation

LLMs face three critical barriers when analyzing security vulnerabilities in real-world codebases:

1. **Token limits** prevent loading entire repositories -- an 8,000-method codebase would require hundreds of millions of tokens, far exceeding even extended context windows.
2. **Code embeddings lack semantic depth** -- RAG-based retrieval captures syntactic patterns but misses inter-procedural relationships like "function A's return value flows into function B's buffer write."
3. **LLMs struggle with complex static analysis queries** -- CPGQL is a domain-specific language rarely seen in training corpora, causing models to hallucinate API methods or produce syntactically invalid queries.

These limitations force a trade-off between analyzing small isolated snippets (missing cross-function vulnerabilities) or loading large contexts (exceeding token budgets and degrading reasoning quality). Neither approach enables the analyst-like reasoning required for vulnerability management at scale.

---

## Main Original Ideas

1. **MCP-based CPG Integration:** codebadger exposes Joern's CPG engine through the Model Context Protocol (MCP), providing high-level abstraction tools (program slicing, taint tracking, data flow analysis, call graph extraction, bounds checking) that translate LLM requests into CPGQL queries without requiring the LLM to learn or generate CPGQL syntax.

2. **Semantic Navigation over Exhaustive Reading:** Instead of loading entire codebases, codebadger enables LLMs to navigate code semantically -- following data flows, call graphs, and dependency chains -- mirroring how human security analysts work. This reduces token consumption to only the relevant code snippets.

3. **Session-based Architecture with Caching:** The system uses Docker-containerized Joern sessions with Redis-managed state and CPG caching by source hash and language. This supports concurrent, isolated analysis contexts with efficient reuse of previously generated graphs.

4. **Backward Slicing for Vulnerability Context:** The tool implements backward program slicing (Algorithm 2 in the paper) that isolates vulnerability-relevant code segments by tracing upstream data and control dependencies from a criterion point, reducing codebase size by up to 90%.

5. **Taint Flow Analysis Pipeline:** A structured taint propagation algorithm (Algorithm 1) identifies flows from untrusted sources to sensitive sinks via forward PDG traversal, with configurable path limits to manage computational complexity.

---

## Key Findings

### Use Case Results

| Use Case | Target | Scale | Key Result |
|---|---|---|---|
| Code Comprehension | GGML library | 1,151 files, 246k LOC, 8,667 methods | Identified unbounded alloca, integer overflows in allocation calculations, unchecked pointer arithmetic |
| Vulnerability Discovery | libtiff | 828 files, 127k LOC | Discovered **previously unreported buffer overflow** in `gtStripContig()` via unvalidated `col_offset`; confirmed with ASAN |
| Exploit Generation | libtiff | Same as above | Generated working PoC with crafted TIFF files (`col_offset=356`, `width=256`); ASAN confirmed heap-buffer-overflow |
| Vulnerability Patching | libxml2 (CVE-2025-6021) | 1,574 files, 335k LOC | Generated **correct patch on first attempt** for integer overflow in `xmlBuildQName`; closely matched maintainers' fix |

### Qualitative Findings

- The agent successfully performed structured audit workflows (summarize, locate sources/sinks, trace flows, validate patterns) that mirror human analyst practices
- Inter-procedural vulnerabilities requiring cross-method data flow tracking were successfully identified -- something RAG-based approaches would likely miss
- The libtiff vulnerability was inherently inter-procedural, requiring tracking of `col_offset` from the `TIFFRGBAImage` structure across method boundaries
- The libxml2 patch correctly introduced `size_t` type changes, explicit integer overflow checks, and safe length calculations
- LLMs occasionally still require direct CPGQL queries via `run_cpgql_query`, where Claude Sonnet 4.5 sometimes fails

---

## Suggestions & Future Directions

1. **Large-scale Quantitative Evaluation:** The current validation relies on qualitative case studies; rigorous benchmarking against established vulnerability detection datasets is identified as critical future work.

2. **Dynamic Analysis Integration:** Combining static CPG-based analysis with dynamic analysis techniques to address runtime vulnerabilities (e.g., race conditions) that Joern's static approach cannot capture.

3. **Expanding Language Support:** Extending codebadger to support emerging programming languages and systems beyond the currently supported C/C++, Java, and Python.

4. **LLM Behavior Monitoring and Optimization:** Investigating automated processes to monitor and optimize how LLMs use taint analysis tools at scale in large vulnerability detection pipelines.

5. **Resource Scalability:** Addressing the overhead of CPG generation for very large repositories (e.g., Linux kernel), which requires substantial RAM that can be prohibitive in resource-constrained environments.

6. **Improving Direct Query Generation:** Despite high-level abstractions, LLMs still sometimes need raw CPGQL queries and struggle with them -- improving this capability remains an open challenge.

---

## Authors & Institutions

Ahmed Lekssays -- Qatar Computing Research Institute (QCRI), Doha, Qatar
