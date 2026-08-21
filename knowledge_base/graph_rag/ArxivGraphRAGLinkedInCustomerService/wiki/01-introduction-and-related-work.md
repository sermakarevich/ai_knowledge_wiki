> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Related Work

**In one sentence:** Plain-text chunk-based RAG loses both the structure linking customer-service issue tickets and the logical coherence across ticket segments, degrading retrieval and answer quality, so the paper fuses RAG with a knowledge graph that preserves intra-issue structure and inter-issue relations.

## Key points

- Conventional RAG for customer-service support treats a corpus of past issue-tracking tickets as plain text, segmenting tickets into fixed-length chunks to fit embedding-model context limits and then embedding each chunk for retrieval — explicitly ignoring the intra-issue structure and the inter-issue relations between tickets.
- **Limitation 1 (compromised retrieval accuracy from ignoring structure):** issue trackers like Jira are inherently structured and interconnected (e.g. "issue A is related to / copied from / caused by issue B"), yet compressing documents into text chunks discards that relationship information; the paper instead parses each ticket into a tree and links tickets into an interconnected graph to maintain entity relationships.
- **Limitation 2 (reduced answer quality from segmentation):** splitting long tickets into fixed-length segments can cut related content apart, yielding incomplete answers — e.g. a ticket that states the issue at the beginning and the solution at the end may be split between the two, so the solution portion is omitted from the retrieved context.
- The method reports outperforming the baseline by **77.6% in MRR** and by **0.32 in BLEU** on their benchmark datasets, and after ~6 months of deployment at LinkedIn it cut median per-issue resolution time by **28.6%**.
- QA-with-KG work is broadly taxonomy'd into three families: **retrieval-based** (relation extraction / distributed representations, weak on multi-entity questions), **template-based** (hand-crafted templates for encoding complex queries, bounded by template scope), and **semantic-parsing-based** (mapping text to logical forms with predicates drawn from KGs).
- Recent LLM+KG integration work cited includes Think-on-Graph and Reasoning-on-Graph (KG-integrated LLM reasoning), Yang et al. (KG-augmented LLM factual reasoning across training phases), and Wen et al.'s Mindmap / Qi et al. (KGs boosting LLM inference in specialized domains such as medicine and food).
- The authors position their system as applying that LLM+KG synergy specifically to customer-service QA: a two-phase pipeline that first builds a KG (tree per ticket + explicit/implicit inter-ticket links + per-node embeddings) and then, at query time, parses the consumer query into named entities and intents to navigate to relevant sub-graphs for answer generation.

---

## Introduction

Technical support quality underpins customer success (satisfaction and loyalty), and because new inquiries frequently resemble previously resolved issues, rapid and accurate retrieval of relevant past instances is the core of efficient resolution. Recent progress in **embedding-based retrieval (EBR)**, **LLMs**, and **RAG** has improved retrieval and QA for support, but the standard pipeline has two structural weaknesses:

1. **Retrieval-stage structure loss.** Tickets are flattened to plain text, segmented into chunks to fit embedding model context limits, and each chunk embedded for retrieval. In reality, issue trackers like **Jira** are structured and interconnected — issues reference one another with relations such as "related to," "copied from," and "caused by." Compressing a ticket into text chunks throws away this information. The paper's method parses each issue ticket into an intra-issue tree, then connects the tickets into an **interconnected graph** that preserves the intrinsic relations among entities, achieving higher retrieval performance.

2. **Answer-stage quality loss from segmentation.** Fixed-length segmentation to fit embedding context can sever related content, producing incomplete answers. The paper's concrete example: a ticket that describes the **issue at its beginning** and the **solution at its end** may be split in the middle during chunking, so the retrieved context omits the critical solution portion. Preserving the logical coherence of ticket sections is what lets the graph-based approach deliver complete, high-quality responses.

The paper frames its system as addressing both: a Knowledge-Graph-informed RAG that keeps the intra-issue structure and inter-issue relations during retrieval (mitigating Limitation 1) and keeps section coherence during answer generation (mitigating Limitation 2).

## Related Work

The paper situates its work in the **question-answering-with-KGs** literature, giving a three-family taxonomy of how a KG has been used to answer questions over decades of work:

- **Retrieval-based methods** derive answers from the KG using relation extraction or distributed representations; they struggle when a question spans multiple entities.
- **Template-based methods** rely on hand-crafted templates to encode complex queries; they are bounded by the scope of the authored templates.
- **Semantic-parsing-based methods** map free text to **logical forms** whose predicates come from the KG.

The paper then reviews the recent wave of **LLM + KG integration**, noting that these combinations have shown broad efficacy for retrieval and reasoning tasks:

- **Jin et al.** give a comprehensive review of LLM–KG integration, categorizing LLM roles as **Predictors, Encoders, and Aligners**.
- **Think-on-Graph** and **Reasoning-on-Graph** leverage KGs to enhance LLM reasoning capabilities.
- **Yang et al.** augment LLM factual reasoning across various training phases using KGs.
- **Wen et al.'s Mindmap** and **Qi et al.** employ KGs to boost LLM inference in specialized domains (medicine, food).

Against this background, the authors position their own system as a case study of LLM+KG synergy aimed specifically at the customer-service support domain: rather than a general-purpose KG reasoning system, a deployment-focused answer generation pipeline that builds a KG (tree-per-ticket + explicit and implicit inter-ticket links) and uses it to navigate to sub-graphs when answering consumer queries — an application-driven contribution on top of the LLM+KG line of work the paper cites.

**Covers:** pages 1-2 (Abstract, Section 1 Introduction, Section 2 Related Work)
