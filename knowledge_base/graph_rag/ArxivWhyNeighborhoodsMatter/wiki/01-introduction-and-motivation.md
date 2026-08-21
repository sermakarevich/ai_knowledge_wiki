> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Motivation

**In one sentence:** In Agentic GraphRAG, final citations only capture part of the information the agent relies on, so citation faithfulness should be treated as a trajectory-level problem where traversal, graph structure, and visited-but-uncited entities jointly shape the answer.

## Key points

- Hallucination is a fundamental factuality problem in LLMs because models are rewarded for providing an answer rather than admitting uncertainty, and RAG mitigates it by grounding answers in external sources.
- Graph RAG retrieves directly from knowledge graphs, following typed entity-relation-entity triples via explicit paths, making retrieved evidence more structured and auditable than vector-similarity retrieval.
- Agentic GraphRAG adds autonomy: rather than a single retrieval step, the agent iteratively decides what to query, inspects results, and traverses the graph until it can produce a final answer with cited evidence.
- Prior faithfulness work asks whether cited sources truly supported the answer or whether reliance on them was genuine, but Agentic GraphRAG raises the additional question of whether the cited entities are even a complete account of what the agent used.
- The paper hypothesizes that final citations capture only part of the information the agent relies on, and that visited entities plus the structural context have a measurable effect on the accuracy and robustness of generated answers.
- The contributions are: framing citation faithfulness as a trajectory-level problem; introducing a graph-ablation methodology to test whether cited evidence is necessary, sufficient, and complete; and showing cited entities are often necessary but not sufficient.

---

## Problem: citation faithfulness in Agentic GraphRAG

LLMs are becoming increasingly capable, but factuality and faithfulness remain a fundamental problem due to hallucinations. Hallucination is likely rooted in how LLMs are trained: models are essentially rewarded for providing an answer rather than admitting uncertainty. One solution is to ground answers through Retrieval-Augmented Generation (RAG), where external sources supplement the model's own knowledge. In RAG, sources are typically retrieved from vector databases via semantic similarity. Graph RAG instead retrieves directly from knowledge graphs, following typed entity-relation-entity triples via explicit paths, making retrieved evidence more structured and auditable. Beyond factual grounding, RAG enables a second advantage: attribution — when answers are grounded in retrieved sources, those sources can be cited, making claims verifiable by the reader, which makes RAG useful for improving both accuracy and transparency.

The latest development is the use of AI agents: the combination of reasoning models and the ability to execute actions through tools enables LLMs to achieve a degree of autonomy. The LLM acts as a controller, making decisions based on observations and invoking tools, for example following the ReAct framework. Applied to retrieval, this creates Agentic RAG: rather than a single retrieval step, the agent autonomously and iteratively decides what to query, inspects results, and issues further queries until it can produce a final answer with cited evidence. The same idea applies to Agentic Graph RAG, where the agent can traverse the knowledge graph autonomously to reach the answer.

## Gap in prior work: citations understate the evidential basis

This last setting raises a question about faithfulness and citation management. Prior work usually asks whether cited sources truly supported the answer, or whether the model's reliance on those sources was genuine. Agentic GraphRAG raises an additional question: whether the cited entities are even a complete account of what the agent used to answer. As it traverses the graph, the agent has access to far more than the entities it ultimately cites — neighboring nodes, relation patterns, and community structure are all part of its working context, and any of them may shape its reasoning. Yet only some entities appear in the final citations. If the traversal as a whole meaningfully shapes the answer, then the citation set understates the model's evidential basis, and an audit framed only around "which sources were used" misses part of the graph context that influenced the response.

## Hypothesis and contributions

The authors hypothesize that, in Agentic GraphRAG, final citations capture only part of the information the agent relies on, and that the visited entities together with the structural context have a measurable effect on the accuracy and robustness of generated answers. To test this, they study the impact of cited entities, visited-but-uncited entities, and graph traversal across three settings of Agentic GraphRAG. The paper proposes the following contributions: (1) it frames citation faithfulness in Agentic GraphRAG as a trajectory-level problem, where graph traversal, structure, and visited-but-uncited entities may be relevant to the answer; (2) it introduces a graph-ablation methodology to test whether cited evidence is necessary, sufficient, and complete as an explanation of answer generation; and (3) it shows that cited entities are often necessary but not sufficient, since accurate answers can depend on broader graph context not reflected in the final citations.

---

**Covers:** Section 1 (Introduction), source/full.txt lines 1-73
