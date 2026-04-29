# Coding Agents are Effective Long-Context Processors

**Paper:** [Coding Agents are Effective Long-Context Processors (Cao et al., 2026)](https://arxiv.org/abs/2603.20432)

## Human Readable TL;DR

Imagine you need to find specific facts buried in a library with millions of books. Instead of trying to read everything at once (which even the smartest person would struggle with), you hire a skilled librarian who knows how to use card catalogs, search systems, and can write custom scripts to cross-reference information. This paper shows that AI coding assistants -- tools designed to help programmers write code -- are surprisingly excellent at this "librarian" job. They naturally know how to organize, search, and navigate through massive amounts of text, outperforming purpose-built systems by about 17% on average.

## TL;DR

Off-the-shelf coding agents (Codex/GPT-5, Claude Code/Sonnet 4.5) can externalize long-context processing into explicit file-system navigation and programmatic manipulation, achieving state-of-the-art results on 4/5 benchmarks with an average 17.3% improvement over prior best. The agents autonomously develop task-specific strategies -- iterative query refinement for multi-hop retrieval, programmatic aggregation for analytical tasks, and direct inference for diverse QA -- without any task-specific training or prompting.

---

## Problem & Motivation

Despite LLM context windows scaling to millions of tokens, models suffer from **"context rot"** -- performance degrades as context length increases. The underlying reasoning through latent attention mechanisms remains opaque and uninterpretable. Standard RAG pipelines rely on fixed, shallow retrieval that struggles with multi-hop reasoning. ReAct agents are constrained to predefined tool APIs.

The authors observe that coding agents are trained on code repositories with long files and hierarchical directory structures, implicitly equipping them with skills for organizing, navigating, and manipulating text programmatically. The question: can these software engineering skills transfer to general long-context text processing?

---

## Main Original Ideas

1. **Externalizing long-context processing to coding agents** -- Rather than relying on latent attention or fixed retrieval pipelines, the paper reformulates long-context processing as file-system navigation and manipulation, delegating it to off-the-shelf coding agents with no task-specific fine-tuning.

2. **Corpus-as-file-system formatting** -- Documents are stored as `.txt` files in hierarchical directory structures (mimicking code repositories), enabling agents to use native tools like `grep`, `ripgrep`, `sed`, and custom Python scripts for exploration and extraction.

3. **Emergent task-adaptive strategies** -- The paper identifies and characterizes three distinct processing strategies that agents autonomously develop: iterative query refinement (multi-hop retrieval), programmatic aggregation (analytical tasks), and direct inference (diverse QA) -- without explicit instruction.

4. **Retrieval tool displacement effect** -- A counterintuitive finding that providing retrieval tools (BM25, dense embeddings) can actually suppress agents' native exploration capabilities, sometimes degrading performance.

---

## Key Findings

| Benchmark | Context Scale | Codex (Best) | Claude Code (Best) | Prior SOTA | Improvement |
|---|---|---|---|---|---|
| **BrowseComp-Plus** | 750M tokens | **88.50%** | 85.50% | 80.00% | +8.5% |
| **Oolong-Synthetic** | 536K tokens | **71.75%** | 65.50% | 64.38% | +7.4% |
| **Oolong-Real** | 385K tokens | 35.38% | **37.46%** | 24.09% | +13.4% |
| **LongBench-v2** | 188K tokens | 59.50% | **62.50%** | 63.30% | -0.8% |
| **Natural Questions** | 3T tokens | **56.00%** | -- | 50.90% | +5.1% |

- Hierarchical folder structure significantly outperforms single-file storage (89.0% vs 83.0% on BrowseComp-Plus)
- Agents with retrieval tools issue fewer native search commands (`grep`), suggesting behavioral displacement rather than augmentation
- Coding agents autonomously execute multi-hop reasoning chains (up to 6 hops observed) without explicit chain-of-thought prompting
- Cost per query is competitive with LLM full-context and RLM baselines while delivering superior accuracy
- Results generalize across two different coding agent implementations (Codex/GPT-5 and Claude Code/Sonnet 4.5)

---

## Suggestions & Future Directions

1. **Improved retrieval integration** -- Investigate methods to integrate retrieval tools without suppressing agents' native exploration capabilities, potentially through adaptive tool selection or hybrid strategies.

2. **Specialized agent frameworks** -- Develop frameworks to further optimize coding agents specifically for navigating and reasoning over massive text corpora, beyond their general software engineering training.

3. **Understanding emergent behaviors** -- Further analysis into the precise mechanisms behind task-specific strategy emergence, including what triggers the shift between search-heavy, code-heavy, and direct-inference modes.

4. **File system structure optimization** -- Explore optimal corpus formatting and directory organization strategies that best leverage coding agents' navigation capabilities across different task types.

5. **Cost-performance tradeoffs** -- While competitive, coding agents are more expensive than lightweight RAG; future work could explore efficiency optimizations for practical deployment at scale.

---

## Authors & Institutions

Weili Cao (Duke University), Xunjian Yin (Duke University), Bhuwan Dhingra (Duke University, equal advising), Shuyan Zhou (Duke University, equal advising)
