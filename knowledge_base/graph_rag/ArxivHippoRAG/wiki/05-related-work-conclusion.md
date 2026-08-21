> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Related Work & Conclusions

**In one sentence:** HippoRAG stands apart from every memory-related approach to LLM long-term memory — because it integrates knowledge during offline indexing without the repeated-summarization cost of RAPTOR/MemWalker/GraphRAG and without the continual-learning weakness of parametric memory, and it is concluded to be a powerful, continuously updatable middle ground between standard RAG and parametric memory, though limited by off-the-shelf components and unproven scalability.

## Key points

- LLM parameters encode a remarkable amount of world knowledge, but updating this store — an essential property of long-term memory — remains surprisingly limited, and no methodology has emerged as a robust continual-learning solution despite fine-tuning, model editing, and external parametric memory modules.
- RAG is a simple way to keep knowledge up to date over time, and multi-step RAG methods can integrate information across new or updated knowledge elements, but this online integration cannot solve complex tasks such as path-finding multi-hop QA where the search entities do not co-occur in any single passage (a condition often true for new information).
- RAPTOR, MemWalker, and GraphRAG integrate knowledge during the offline indexing phase like HippoRAG, but their reliance on summarizing knowledge elements means the summarization must be redone any time new data arrives — whereas HippoRAG integrates continuous new knowledge by simply adding edges to its KG.
- Long-context growth in open and closed LLMs suggests memory storage within massive context windows, but this future is uncertain due to engineering hurdles and apparent limitations of long-context models even at current lengths.
- Multi-hop QA work splits into graph-augmented reading comprehension (GNNs mixing hyperlink/co-occurrence signal with an LM, or injecting KG triples into LLM prompts — generation-level, complementary to HippoRAG's retrieval-level gains) and graph-augmented retrieval (re-rankers trained to traverse existing Wikipedia hyperlink graphs — whereas HippoRAG builds a KG from scratch with LLMs and does multi-hop retrieval without any supervision, making it much more adaptable).
- HippoRAG shows the synergy potential between LLMs and knowledge graphs predicted in the Pan et al. survey: combining LLM knowledge-graph construction with the retrieval strengths of structured knowledge for more effective RAG.
- Conclusion: HippoRAG, although simple, has a strong outlook for overcoming the limitations of standard RAG while retaining advantages over parametric memory, and is positioned as a powerful middle-ground framework for long-term memory in LLMs.
- Known limitations: all components are off-the-shelf with no additional training (the most errors stem from NER and OpenIE, where direct fine-tuning may pay off), graph search is simple PPR (relations do not guide traversal), OpenIE consistency degrades on longer documents, and Llama-3.1 scalability of the synthetic hippocampal index remains empirically unproven at sizes much larger than current benchmarks.

---

## Parametric Long-Term Memory

It is widely accepted, even among skeptical researchers, that modern LLM parameters encode a remarkable amount of world knowledge, deployable in a flexible and robust manner. However, the ability to update this vast knowledge store — a critical component of any long-term memory system — is still surprisingly limited. Many update techniques exist (standard fine-tuning, model editing, external parametric memory modules modeled on human memory), but a robust methodology for continual learning in LLMs has not yet emerged. This is the main weakness HippoRAG addresses: because its index is a KG, new knowledge is integrated by simply adding edges, requiring no retraining or parameter updates.

## Long Context as Long-Term Memory

Context lengths of both open- and closed-source LLMs have increased dramatically in the past year, and this scaling trend suggests that future LLMs could store long-term memory within a massive context window. However, this future remains largely uncertain due to the many engineering hurdles involved and the apparent limitations of long-context LLMs observed even at current context lengths. HippoRAG's explicit, external, indexed structure thus sidesteps the reliance on ever-longer context windows: retrieval is performed over a structured KG rather than a single monolithic context.

## RAG as Long-Term Memory

Using RAG methods as long-term memory offers a simple way to keep knowledge up to date over time. More sophisticated multi-step RAG methods (multiple retrieval and generation passes) can integrate information across new or updated knowledge elements — another crucial aspect of long-term memory — but this online integration cannot solve more complex knowledge-integration tasks: the path-finding multi-hop QA examples illustrated in the paper (where search entities like "Stanford" and "Alzheimer's" do not appear together in any passage, a condition often satisfied for new information).

RAPTOR, MemWalker, and GraphRAG fall into a closer camp: they integrate knowledge during the offline indexing phase, like HippoRAG, and could in principle handle these more complex tasks. However, all of them integrate information by summarizing knowledge elements, which means that the summarization process must be redone every time new data is added. In contrast, HippoRAG integrates knowledge continuously by simply adding edges to its KG — indexing is incremental rather than a fixed batch of summarization.

Multi-hop QA and graph literature (Section 6.2). Prior work can broadly be divided into two categories: (1) graph-augmented reading comprehension, where a graph is extracted from retrieved documents to improve the model's reasoning, and (2) graph-augmented retrieval, where the model finds relevant documents by traversing a graph.

Graph-augmented reading comprehension: early work are mainly supervised methods that mix signals from a hyperlink or co-occurrence graph with a language model via a GNN; more recent work uses LLMs to inject knowledge-graph triples directly into the prompt. These works share HippoRAG's use of graphs for multi-hop QA, but their improvements are at the *generation* level, whereas HippoRAG's improvements are purely at the *retrieval* level — fully complementary.

Graph-augmented retrieval: prior work learns to rerank modules over existing Wikipedia hyperlink graphs. In contrast, HippoRAG builds its KG from scratch with LLMs and performs multi-hop retrieval without any supervision, making it much more adaptable (it is not dependent on existing hyperlink structures).

LLMs and KGs (Section 6.3). Combining the strengths of LMs and KGs has been active research for many years: augmenting LLMs with a KG in different ways, and augmenting KGs by distilling parametric knowledge from LLMs or by parsing text with LLMs. Pan et al. present an especially comprehensive survey/roadmap for this research direction and highlight the importance of work that *synergizes* the two technologies. HippoRAG joins this line of work: it shows the potential for synergy between LLMs and knowledge graphs, combining the KG-construction ability of LLMs with the retrieval strengths of structured knowledge for more effective RAG.

## Conclusions & Limitations

Final claims: HippoRAG's neurobiologically-motivated methodology, although simple, already shows potential for overcoming the inherent limitations of standard RAG systems while retaining its advantages over parametric memory. Its knowledge-integration capability (strong results on path-following multi-hop QA and promising results on path-finding multi-hop QA), its dramatic efficiency improvements, and its continuously-updating nature make it a powerful middle-ground framework between standard RAG and parametric memory and a compelling solution for long-term memory in LLMs.

Limitations / future directions:
1. All components (NER, OpenIE, PPR, LLM) are currently used off-the-shelf without any additional training. There is considerable room for improvement via component-specific fine-tuning — the error analysis (Appendix F) shows that most errors stem from NER and OpenIE, so direct fine-tuning would likely help.
2. Graph search is simple PPR. There are several possible improvements over simple PPR, e.g. allowing the relations themselves to directly guide graph traversal.
3. As shown in Appendix F.4, OpenIE consistency on longer documents (compared to shorter ones) still needs to be improved.
4. Scalability remains to be empirically validated. Although Llama-3.1 achieves performance close to closed-source models (reducing costs considerably), the efficiency and effectiveness of the synthetic hippocampal index as it scales far beyond current benchmark sizes has yet to be proven.

**Covers:** Sections 6-7 (Related Work, Conclusions & Limitations), pages 13-15
