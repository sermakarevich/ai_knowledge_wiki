> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# GraphRAG Methodology

**In one sentence:** GraphRAG converts a corpus into a hierarchically summarized knowledge graph — extracting entities, relationships, and claims from text chunks, clustering them into Leiden communities at multiple levels, and writing community summaries bottom-up — then answers global sensemaking queries by a map-reduce process that scores and aggregates parallel community-level answers.

## Key points

- The indexing pipeline has six steps (3.1.1–3.1.6): source documents → text chunks → entities & relationships → knowledge graph → graph communities → community summaries → community answers → global answer.
- Chunk size is a fundamental design decision: longer chunks need fewer LLM extraction calls (lower cost) but suffer degraded recall of information appearing early in the chunk (a recall–precision trade-off).
- Entity/relationship/claim extraction is abstractive summarization: LLMs generate short descriptions, including relationships and claims that may not be explicitly stated; duplicates of the same element are aggregated into nodes/edges with the number of duplicates becoming edge weights.
- Graph communities are found with Leiden community detection, applied hierarchically and recursively until leaf communities can no longer be partitioned; each level yields a partition that is mutually exclusive and collectively exhaustive, enabling divide-and-conquer global summarization.
- Community summaries are generated bottom-up: leaf-level element summaries are prioritized and iteratively added to the LLM context window until the token limit is reached (prioritized by combined source+target node degree in decreasing order); higher-level communities substitute shorter sub-community summaries for longer element summaries until they fit the context window.
- Global query answering is map-reduce: community summaries at a chosen level are shuffled and chunked (distributing relevant information across chunks), each chunk produces a parallel intermediate answer with a 0–100 helpfulness score (score-0 answers filtered out), then answers are sorted by helpfulness and iteratively added into a new context window until the token limit, from which the final global answer is generated.
- Evaluation question generation uses the formula K × N × M: an LLM describes K user personas, N tasks per user, and M high-level questions per (user, task) pair; in this work K = M = N = 5, giving 125 test questions per dataset.
- Evaluation uses an LLM head-to-head judge with three target criteria — Comprehensiveness, Diversity, Empowerment — plus a control criterion, Directness; no method is expected to win across all four, since Directness opposes Comprehensiveness and Diversity.

---

## The GraphRAG Indexing Pipeline (Section 3.1)

Figure 1 of the paper illustrates the high-level data flow; below are the design parameters, techniques, and implementation details for each step.

### Source Documents → Text Chunks (3.1.1)

The documents in the corpus are split into text chunks, and the LLM extracts information from each chunk for downstream processing. Selecting the chunk size is a fundamental design decision: longer text chunks require fewer LLM calls for extraction (which reduces cost) but suffer from degraded recall of information that appears early in the chunk (Kuratov et al., 2024; Liu et al., 2023). Section A.1 of the paper contains prompts and examples of the recall–precision trade-offs.

### Text Chunks → Entities & Relationships (3.1.2)

The LLM is prompted to extract instances of important entities and the relationships between them from a given chunk, and additionally generates short descriptions for the entities and relationships. The paper's worked example chunk is:

> NeoChip's (NC) shares surged in their first week of trading on the NewTech Exchange. However, market analysts caution that the chipmaker's public debut may not reflect trends for other technology IPOs. NeoChip, previously a private entity, was acquired by Quantum Systems in 2016. The innovative semiconductor firm specializes in low-power processors for wearables and IoT devices.

The LLM is prompted such that it extracts the following:

- The entity NeoChip, with description "NeoChip is a publicly traded company specializing in low-power processors for wearables and IoT devices."
- The entity Quantum Systems, with description "Quantum Systems is a firm that previously owned NeoChip."
- A relationship between NeoChip and Quantum Systems, with description "Quantum Systems owned NeoChip from 2016 until NeoChip became publicly traded."

These prompts can be tailored to the domain of the document corpus by choosing domain-appropriate few-shot exemplars for in-context learning (Brown et al., 2020). While the default prompt extracts the broad class of "named entities" like people, places, and organizations and is generally applicable, domains with specialized knowledge (e.g., science, medicine, law) benefit from few-shot exemplars specialized to those domains.

The LLM can also be prompted to extract claims — important factual statements about entities, such as dates, events, and interactions with other entities. With in-context learning exemplars providing domain-specific guidance. Claim descriptions extracted from the example text chunk are as follows:

- NeoChip's shares surged during their first week of trading on the NewTech Exchange.
- NeoChip debuted as a publicly listed company on the NewTech Exchange.
- Quantum Systems acquired NeoChip in 2016 and held ownership until NeoChip went public.

Appendix A contains prompts and details on the implementation of entity and claim extraction.

### Entities & Relationships → Knowledge Graph (3.1.3)

Using an LLM to extract entities, relationships, and claims is a form of abstractive summarization — these are meaningful summaries of concepts that, in the case of relationships and claims, may not be explicitly stated in the text. The extraction process creates multiple instances of a single element because an element is typically detected and extracted multiple times across documents.

In the final step of knowledge graph extraction, these instances become individual nodes and edges in the graph. Entity descriptions are aggregated and summarized for each node and edge; relationships are aggregated into graph edges, where the number of duplicates for a given relationship becomes edge weights; claims are aggregated similarly.

In this manuscript, the analysis uses exact string matching for entity matching — the task of reconciling different extracted names for the same entity (Barlaug and Gulla, 2021; Christen and Christen, 2012; Elmagarmid et al., 2006). Softer matching approaches can be used with minor adjustments to prompts or code. Furthermore, GraphRAG is generally resilient to duplicate entities since duplicates are typically clustered together for summarization in subsequent steps.

### Knowledge Graph → Graph Communities (3.1.4)

Given the graph index created in the previous step, a variety of community detection algorithms may partition the graph into communities of strongly connected nodes (see the surveys by Fortunato, 2010 and Jin et al., 2021). In this pipeline, Leiden community detection (Traag et al., 2019) is used in a hierarchical manner, recursively detecting sub-communities within each detected community until reaching leaf communities that can no longer be partitioned.

Each level of this hierarchy provides a community partition that covers the nodes of the graph in a mutually exclusive, collectively exhaustive way, enabling divide-and-conquer global summarization. An illustration of such hierarchical partitioning on an example dataset appears in Appendix B.

### Graph Communities → Community Summaries (3.1.5)

This step creates report-like summaries of each community in the community hierarchy, using a method designed to scale to very large datasets. These summaries are independently useful as a way to understand the global structure and semantics of the dataset and may themselves be used to make sense of a corpus in the absence of a specific query — for example, a user may scan community summaries at one level looking for general themes of interest, then read linked reports at a lower level providing additional details for each subtopic. Here, though, the focus is on their utility as part of a graph-based index for answering global queries.

GraphRAG generates community summaries by adding various element summaries (for nodes, edges, and related claims) to a community summary template. Community summaries from lower-level communities are used to generate summaries for higher-level communities as follows:

- **Leaf-level communities.** The element summaries of a leaf-level community are prioritized and then iteratively added to the LLM context window until the token limit is reached. The prioritization is as follows: for each community edge in decreasing order of combined source and target node degree (i.e., overall prominence), add descriptions of the source node, target node, the edge itself, and related claims.
- **Higher-level communities.** If all element summaries fit within the token limit of the context window, proceed as for leaf-level communities and summarize all element summaries within the community. Otherwise, rank sub-communities in decreasing order of element summary tokens and iteratively substitute sub-community summaries (shorter) for their associated element summaries (longer) until they fit within the context window.

### Community Summaries → Community Answers → Global Answer (3.1.6)

Given a user query, the community summaries generated in the previous step can be used to generate a final answer in a multi-stage process. The hierarchical nature of the community structure also means that questions can be answered using community summaries from different levels, raising the question of whether a particular level offers the best balance of summary detail and scope for general sensemaking questions (evaluated in Section 4).

For a given community level, the global answer to any user query is generated as follows:

- **Prepare community summaries.** Community summaries are randomly shuffled and divided into chunks of pre-specified token size. This ensures relevant information is distributed across chunks, rather than concentrated (and potentially lost) in a single context window.
- **Map community answers.** Intermediate answers are generated in parallel. The LLM is also asked to generate a score between 0–100 indicating how helpful the generated answer is in answering the target question. Answers with score 0 are filtered out.
- **Reduce to global answer.** Intermediate community answers are sorted in descending order of helpfulness score and iteratively added into a new context window until the token limit is reached. This final context is used to generate the global answer returned to the user.

## Global Sensemaking Question Generation (Section 3.2)

To evaluate the effectiveness of RAG systems for global sensemaking tasks, the authors use an LLM to generate a set of corpus-specific questions designed to assess high-level understanding of a given corpus, without requiring retrieval of specific low-level facts. Given a high-level description of a corpus and its purposes, the LLM is prompted to generate personas of hypothetical users of the RAG system. For each hypothetical user, the LLM is then prompted to specify tasks that this user would use the RAG system to complete. Finally, for each combination of user and task, the LLM is prompted to generate questions that require understanding of the entire corpus. Algorithm 1 describes the approach:

**Algorithm 1: Prompting Procedure for Question Generation**

1. Input: Description of a corpus, number of users K, number of tasks per user N, number of questions per (user, task) combination M.
2. Output: A set of K × N × M high-level questions requiring global understanding of the corpus.
3. Procedure GENERATEQUESTIONS — Based on the corpus description, prompt the LLM to:
   1. Describe personas of K potential users of the dataset.
   2. For each user, identify N tasks relevant to the user.
   3. Specific to each user & task pair, generate M high-level questions that:
      - Require understanding of the entire corpus.
      - Do not require retrieval of specific low-level facts.
4. Collect the generated questions to produce K × N × M test questions for the dataset.

For the evaluation, K = M = N = 5 for a total of 125 test questions per dataset. Table 1 shows example questions for each of the two evaluation datasets:

**Podcast transcripts**
- User: A tech journalist looking for insights and trends in the tech industry
- Task: Understanding how tech leaders view the role of policy and regulation
- Questions:
  1. Which episodes deal primarily with tech policy and government regulation?
  2. How do guests perceive the impact of privacy laws on technology development?
  3. Do any guests discuss the balance between innovation and ethical considerations?
  4. What are the suggested changes to current policies mentioned by the guests?
  5. Are collaborations between tech companies and governments discussed and how?

**News articles**
- User: Educator incorporating current affairs into curricula
- Task: Teaching about health and wellness
- Questions:
  1. What current topics in health can be integrated into health education curricula?
  2. How do news articles address the concepts of preventive medicine and wellness?
  3. Are there examples of health articles that contradict each other, and if so, why?
  4. What insights can be gleaned about public health priorities based on news coverage?
  5. How can educators use the dataset to highlight the importance of health literacy?

## Criteria for Evaluating Global Sensemaking (Section 3.3)

Given the lack of gold standard answers to the activity-based sensemaking questions, the authors adopt the head-to-head comparison approach using an LLM evaluator that judges relative performance according to specific criteria. They designed three target criteria capturing qualities that are desirable for global sensemaking activities. Appendix F shows the prompts for these head-to-head measures, summarized as:

- **Comprehensiveness.** How much detail does the answer provide to cover all aspects and details of the question?
- **Diversity.** How varied and rich is the answer in providing different perspectives and insights on the question?
- **Empowerment.** How well does the answer help the reader understand and make informed judgments about the topic?

Furthermore, a "control criterion" called **Directness** answers "How specifically and clearly does the answer address the question?". In plain terms, directness evaluates the concision of an answer in a generic sense that applies to any generated LLM summarization. It is included to behave as a reference against which the soundness of results for the other criteria can be judged. Since directness is effectively in opposition to comprehensiveness and diversity, no method would be expected to win across all four criteria.

In the evaluations, the LLM is provided with the question, the generated answers from two competing systems, and prompted to compare the two answers according to the criterion before giving a final judgment of which answer is preferred. The LLM either indicates a winner, or returns a tie if they are fundamentally similar. To account for the inherent stochasticity of LLM generation, each comparison is run with multiple replicates and the results are averaged across replicates and questions. An illustration of LLM assessment for answers to a sample question appears in Appendix D.

---

**Covers:** Section 3 (Methods: 3.1 GraphRAG Workflow, 3.2 Global Sensemaking Question Generation, 3.3 Criteria for Evaluating Global Sensemaking).
