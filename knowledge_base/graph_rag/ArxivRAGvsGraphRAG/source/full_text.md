## **RAG vs. GraphRAG: A Systematic Evaluation and Key Insights**



Haoyu Han
Michigan State University
East Lansing, MI, USA


Harry Shomer
University of Texas at Arlington
Arlington, TX, USA


Kai Guo

Michigan State University
East Lansing, MI, USA


Hui Liu

Michigan State University
East Lansing, MI, USA


**Abstract**



Li Ma

Michigan State University
East Lansing, MI, USA


Yongjia Lei
University of Oregon
Eugene, OR, USA


Zhigang Hua
Meta Platforms, Inc.
Menlo Park, CA, USA


Charu C. Aggarwal
IBM T.J. Watson Research Center
Yorktown Heights, NY, USA


**Keywords**



Yu Wang
University of Oregon
Eugene, OR, USA


Zhisheng Qi
University of Oregon
Eugene, OR, USA


Bo Long
Meta Platforms, Inc.
Menlo Park, CA, USA


Jiliang Tang
Michigan State University
East Lansing, MI, USA



Retrieval-Augmented Generation (RAG) improves large language
models (LLMs) by retrieving relevant information from external
sources and has been widely adopted for text-based tasks. For structured data, such as knowledge graphs, Graph Retrieval-Augmented
Generation (GraphRAG) retrieves and aggregates information along
graph structures. More recently, GraphRAG has been extended to
general text settings by organizing unstructured text into graph
representations, showing promise for reasoning and grounding.
Despite these advances, existing GraphRAG systems for text data
are often tailored to specific tasks, datasets, and system designs,
resulting in heterogeneous evaluation protocols. Consequently, a
systematic understanding of the relative strengths, limitations, and
trade-offs between RAG and GraphRAG on widely used text benchmarks remains limited. In this paper, we present a comprehensive
benchmark study comparing RAG and GraphRAG on established
text-based tasks, including question answering and query-based
summarization. We introduce a unified evaluation protocol that
standardizes data preprocessing, retrieval configurations, and generation settings, enabling fair and reproducible comparisons. Our results highlight the distinct strengths of RAG and GraphRAG across
different tasks and evaluation perspectives. Building on these findings, we explore selection and integration strategies that combine
the strengths of both paradigms, leading to consistent performance
improvements. We further analyze failure modes, efficiency tradeoffs, and evaluation biases, and highlight key considerations for
designing and evaluating retrieval-augmented generation systems.


Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for components of this work owned by others than the
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
republish, to post on servers or to redistribute to lists, requires prior specific permission
and/or a fee. Request permissions from permissions@acm.org.
_Conference acronym ’XX, Woodstock, NY_
© 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM ISBN 978-1-4503-XXXX-X/2018/06
[https://doi.org/XXXXXXX.XXXXXXX](https://doi.org/XXXXXXX.XXXXXXX)



Retrieval-Augmented Generation, GraphRAG, Large Language Models, Question Answering, Summarization


**ACM Reference Format:**

Haoyu Han, Li Ma, Yu Wang, Harry Shomer, Yongjia Lei, Zhisheng Qi, Kai
Guo, Zhigang Hua, Bo Long, Hui Liu, Charu C. Aggarwal, and Jiliang Tang.
2018. RAG vs. GraphRAG: A Systematic Evaluation and Key Insights. In
_Proceedings of Make sure to enter the correct conference title from your rights_
_confirmation email (Conference acronym ’XX)._ ACM, New York, NY, USA,
[20 pages. https://doi.org/XXXXXXX.XXXXXXX](https://doi.org/XXXXXXX.XXXXXXX)


**1** **Introduction**


Retrieval-Augmented Generation (RAG) has emerged as a practical
paradigm for improving downstream tasks by retrieving relevant
knowledge from external data sources. It has been successfully
deployed in a wide range of real-world applications, including
healthcare [ 47 ], law [ 41 ], finance [ 53 ], and education [ 27 ]. With
the advent of Large Language Models (LLMs), integrating retrieval
into generation further improves faithfulness by mitigating hallucinations and enhancing robustness [ 13, 55 ]. In most existing RAG
systems, retrieval is performed over text corpora.
Graphs provide an explicit representation of relational structure and have long been used across domains such as knowledge
representation, social networks, and biomedical discovery [ 26, 42,
43 ]. Graph Retrieval-Augmented Generation (GraphRAG) has recently gained attention for retrieving and aggregating information
from graph-structured data, including knowledge graphs (KGs) and
molecular graphs [ 11, 29 ]. Beyond leveraging existing graphs, an
emerging line of work extends GraphRAG to text-based tasks by
constructing graphs from unstructured documents, with reported
benefits for global summarization [ 5 ], planning [ 23 ], and reasoning [ 12 ]. However, most GraphRAG studies for text are conducted
under task- and system-specific settings, using bespoke datasets,
graph construction heuristics, and evaluation protocols. This heterogeneity makes it difficult to draw principled conclusions about
_when and why_ explicit graph structures help (or hurt) retrievalaugmented generation, and obscures practical trade-offs such as
construction cost, retrieval latency, and storage footprint.


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.



To address this gap, we conduct a controlled and systematic
benchmark of RAG and GraphRAG on widely used text-based tasks,
focusing on _Question Answering_ (QA) and _Query-based Summa-_
_rization_ . We consider four representative categories of GraphRAG
systems: **(1)** _KG-based GraphRAG_ [ 24 ], which extracts a KG from
text and performs retrieval over the KG; **(2)** _Community-based_
_GraphRAG_ [ 5 ], which performs retrieval over community structures and hierarchical abstractions; **(3)** _Text-centric graph-guided_
_RAG_ [ 16 ], which retrieves original text chunks with the assistance
of a constructed knowledge graph; and **(4)** _Hierarchical summary-_
_based GraphRAG_ [ 32 ], which builds hierarchical summaries to enable multi-granular retrieval without relying on explicit KGs. For
QA, we evaluate both single-hop and multi-hop settings; for summarization, we consider both single-document and multi-document
scenarios. Crucially, we introduce a unified evaluation protocol that
standardizes data preprocessing, retrieval, and generation settings,
enabling fair and reproducible comparisons across paradigms.
Our analysis results lead to several key findings. First, **RAG and**
**GraphRAG exhibit complementary behaviors rather than a**
**consistent winner** . In QA, RAG performs better on single-hop and
detail-oriented factual queries, whereas GraphRAG is more effective
on multi-hop, reasoning-intensive questions. Second, **GraphRAG**
**design choices matter** : for example, community-based global
search can sacrifice query-specific details, hurting detail-oriented
QA, while providing more corpus-level aggregation that benefits
broad or diverse summarization outputs. Third, **evaluation pro-**
**tocol can change conclusions** : we show that LLM-as-a-Judge
evaluation for summarization can be highly sensitive to the presentation order of candidate summaries, introducing strong position
effects that may confound comparisons. Finally, **GraphRAG is**
**not free** : it often incurs higher construction cost, retrieval latency,
and storage footprint, and its performance can be sensitive to the
quality (and cost) of graph construction. These findings suggest
that effective retrieval-augmented generation should not treat RAG
and GraphRAG as mutually exclusive choices. Motivated by this,
we study two practical hybrid strategies: **Selection**, which routes
queries to RAG or GraphRAG based on query type for efficiency,
and **Integration**, which combines evidence from both paradigms to
maximize performance. Across benchmarks, these strategies yield
consistent improvements. Our main contributions are as follows:


- **Systematic Benchmark:** We present a controlled benchmark
comparing RAG and multiple GraphRAG variants across QA and
query-based summarization under a unified evaluation protocol
(consistent preprocessing, retrieval, and generation settings) for
fair and reproducible comparison.

- **Strong, Task-Level Findings:** We identify clear complementarities: RAG is stronger for factual/detail-oriented QA, while
GraphRAG benefits reasoning-intensive QA and produces more
corpus-level, diverse summaries, with outcomes strongly affected
by GraphRAG design choices (e.g., local vs. global search).

- **Hybrid Strategies:** We study **Selection** and **Integration** strategies that combine RAG and GraphRAG, achieving consistent improvements and illustrating effectiveness–efficiency trade-offs.




- **Evaluation and Efficiency Analyses:** We analyze failure modes,
construction/retrieval/storage costs, sensitivity to graph construction quality, and demonstrate strong position effects in LLMas-a-Judge summarization evaluation, highlighting practical considerations for reliable (Graph)RAG assessment.


**2** **Related Works**

**2.1** **Retrieval-Augmented Generation**


Retrieval-Augmented Generation (RAG) has been widely applied
to enhance Large Language Models (LLMs) by retrieving relevant
information from external sources, addressing restricted context
windows, improving factuality, and mitigating hallucinations [ 7, 9 ].
Most RAG systems process text corpora by splitting documents
into chunks [ 8 ]. Given a query, relevant chunks can be retrieved
via lexical search [ 30 ] or semantic similarity search [ 17 ]. Beyond
vanilla retrieval, pre-retrieval processing [ 25, 56 ], post-retrieval
processing [ 2, 46 ], and fine-tuning strategies [ 20 ] further improve
effectiveness across tasks such as question answering [ 48 ], dialogue
generation [ 14 ], and summarization [ 15 ]. Many systems also employ reranking and iterative retrieval to refine evidence selection
and improve answer quality under a fixed context budget. Several
studies benchmark RAG pipelines and evaluation tools across tasks
and domains [ 1, 6, 51 ]. However, existing work rarely provides a
controlled comparison between standard RAG and GraphRAG under unified experimental settings on widely used text benchmarks.


**2.2** **Graph Retrieval-Augmented Generation**


Many real-world scenarios involve graph-structured data, such as
knowledge graphs (KGs), social graphs, and molecular graphs [ 26,
44 ]. GraphRAG incorporates graph structures into retrieval to exploit relational signals among connected nodes [ 11, 29 ]. Early work
primarily studies retrieval over existing KGs for downstream tasks
such as KG-based QA [ 35, 50 ] and fact checking [ 18 ]. Graph structures can also benefit text-centric retrieval; for example, hyperlink
graphs between documents can improve retrieval for question answering [ 21 ]. Recent works further explore constructing graphs
from text to support text-based tasks [ 11 ]. One direction builds
document- or chunk-level graphs to guide retrieval over textual
units [ 2, 21 ]. Another direction constructs entity–relation graphs
from documents (often with LLM assistance) and retrieves information at multiple abstraction levels, such as local neighborhoods
or community-level summaries [ 5, 12 ]. More recently, text-centric
and hierarchical approaches use graph-inspired structures without fully specified entity–relation semantics: RAPTOR constructs
hierarchical summary structures for multi-granular retrieval [ 32 ],
while HippoRAG and its extensions build entity-linked graphs to
guide chunk retrieval [10, 16].
Despite rapid progress, GraphRAG systems for text are often
evaluated under heterogeneous protocols, with varying graph construction methods, retrieval configurations, and even evaluation
criteria. Moreover, graph construction introduces additional costs
(indexing time, retrieval latency, and storage footprint) and can be
sensitive to the quality of the construction model, yet these tradeoffs are not consistently characterized across studies. As a result,
it remains unclear how GraphRAG compares with standard RAG
on general text-based benchmarks and what practical trade-offs it


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY



entails. This motivates our systematic benchmark evaluation under
unified experimental settings.


**3** **Evaluation Framework**


In this section, we describe our evaluation framework [1] and experimental protocol. To ensure fair comparison, we evaluate RAG
and GraphRAG under identical settings whenever applicable, and
otherwise follow the default configurations of each method while
matching key budgets. We decouple retrieval from generation by
first saving retrieved evidence for each method and then using a
unified generation script to produce outputs conditioned on the
saved retrieval results.


**3.1** **RAG Pipeline**


We adopt a standard dense-retrieval RAG pipeline [ 17 ]. Given a
corpus, we segment documents into textual chunks and build an
index by embedding each chunk into a shared vector space. At
inference time, we embed the query, retrieve top-ranked chunks
based on similarity.


**3.2** **GraphRAG Implementations**


GraphRAG designs differ in how structures are constructed and
how structural information is used during retrieval. In this work,
we group GraphRAG approaches into four representative classes
and select representative implementations for each class:
**KG-based GraphRAG.** In KG-based GraphRAG [ 24 ], a knowledge graph is constructed from text. Given a query, relevant entities are identified and aligned to nodes in the KG, and retrieval
traverses multi-hop neighborhoods to collect relational triplets
_(head, relation, tail)_ as evidence. We consider two variants: **(1)** _KG-_
_GraphRAG (Triplets)_, which retrieves only triplets, and **(2)** _KG-_
_GraphRAG (Triplets+Text)_, which retrieves both triplets and their
associated source text. We implement KG-GraphRAG using LlamaIndex [24]. [2]

**Community-based GraphRAG.** Community-based GraphRAG [ 5 ]
further organizes the constructed KG into hierarchical communities using graph clustering algorithms. Each community is associated with a textual summary/report, where lower-level communities capture fine-grained information and higher-level communities provide increasingly abstract representations. We evaluate
two retrieval modes: **Local Search** retrieves entity neighborhoods
and lower-level community reports via entity matching, denoted
as _Community-GraphRAG (Local)_ ; **Global Search** retrieves highlevel community summaries by semantic similarity, denoted as
_Community-GraphRAG (Global)_ . We adopt the implementation of
Edge et al. [5]. [3]

**Text-centric graph-guided RAG.** Text-centric graph-guided methods retain original text chunks as the primary retrieval units while
leveraging graph structures to guide scoring or traversal. We select
HippoRAG2 [ 10 ] as a representative method. HippoRAG2 builds an
entity-linked graph over chunks and retrieves query-relevant entities first, followed by the connected text chunks. Here, the graph


1 https://github.com/haoyuhan1/RAGvsGraphRAG
2 https://www.llamaindex.ai/
3 [https://microsoft.github.io/graphrag](https://microsoft.github.io/graphrag)



acts as an auxiliary structure guiding chunk retrieval rather than
the primary retrieval target.
**Hierarchical summary-based GraphRAG.** Hierarchical summarybased methods construct multi-level hierarchical structures over

text, where higher-level nodes represent progressively more abstract summaries of lower-level content. We adopt RAPTOR [ 32 ] as
a representative method. RAPTOR recursively clusters text chunks
and generates summaries at each level, enabling coarse-to-fine,
multi-granular retrieval without relying on explicit KGs.


**3.3** **Tasks**


We evaluate all methods on two representative text-based tasks:
Question Answering and Query-based Summarization, covering
both single-hop and multi-hop QA, as well as single-document
and multi-document summarization. For single-document tasks,
retrieval is restricted to the corresponding document, while for
multi-document tasks, retrieval is performed over an index constructed from all documents.


**3.4** **Unified Experimental Settings**


To ensure fair comparison across RAG and GraphRAG methods, we
standardize core settings whenever applicable.
**Graph construction.** For GraphRAG methods that require graph
construction from text (e.g., KG-GraphRAG, Community-GraphRAG,
and HippoRAG2), graphs are constructed using GPT-4o-mini; results with GPT-4o are reported in Appendix L.
**Chunking.** We segment documents into chunks of approximately
_256_ tokens for all methods.

**Embedding model and retrieval budget.** We embed queries,
chunks, and graph information into a shared vector space using
OpenAI’s text-embedding-ada-002 model [ 28 ], and retrieve top_𝑘_ candidates by semantic similarity, where _𝑘_ =10 by default.
**Reranking.** When reranking is enabled, we apply a cross-encoder
reranker to reorder retrieved candidates and select the final top_𝑘_ evidence units. We use BAAI/bge-reranker-large [ 45 ] as the
reranker for all methods that support reranking, ensuring consistent
reranking behavior across systems.
**Iterative retrieval.** When iterative retrieval is enabled, we adopt
IRCoT [ 36 ], which interleaves retrieval with intermediate reasoning
steps.
**Generation backbones.** To control for generation capacity, we
use two open-source instruction-tuned LLMs of different sizes as
generators: Llama-3.1-8B-Instruct and Llama-3.1-70B-Instruct [ 4 ].


**4** **Question Answering**


QA is one of the most widely used tasks for evaluating the performance of RAG systems. To systematically assess the effectiveness
of RAG and GraphRAG on general QA settings, we evaluate representative methods on widely used datasets and follow standard
metrics used in prior work.


**4.1** **Datasets and Evaluation Metrics**


To comprehensively evaluate the performance of GraphRAG on
general QA tasks, we select four widely used datasets that cover
different perspectives. For the single-hop QA task, we select the
Natural Questions (NQ) dataset [ 19 ]. For the multi-hop QA task,


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.



we select HotPotQA [ 49 ] and MultiHop-RAG [ 34 ] datasets. The
MultiHop-RAG dataset categorizes queries into four types: Inference, Comparison, Temporal, and Null queries. To further analyze
the performance of RAG and GraphRAG at a finer granularity, we
also include NovelQA [ 38 ], which contains 21 different types of
queries. For more details, please refer to Appendix A.1. We use Precision (P), Recall (R), and F1-score as evaluation metrics for the NQ
and HotPotQA datasets, while accuracy is used for the MultiHopRAG and NovelQA datasets following their original papers.

|Table 1: Performance comparison (%) on NQ and Hotpot.|Col2|Col3|
|---|---|---|
|**Method**<br>**NQ**<br>**Hotpot**<br>P<br>R<br>F1<br>P<br>R<br>F1<br><br><br><br><br><br><br>|**Method**<br>**NQ**<br>**Hotpot**<br>P<br>R<br>F1<br>P<br>R<br>F1<br><br><br><br><br><br><br>|**Method**<br>**NQ**<br>**Hotpot**<br>P<br>R<br>F1<br>P<br>R<br>F1<br><br><br><br><br><br><br>|
|RAG<br>RaptorRAG<br>KG-GraphRAG (Triplets only)<br>KG-GraphRAG (Triplets+Text)<br>Community-GraphRAG (Local)<br>Community-GraphRAG (Global)<br>HippoRAG2|**71.70**<br>**63.93**<br>**64.78**<br>66.06<br>59.56<br>60.04<br>40.09<br>33.56<br>34.28<br>58.36<br>48.93<br>50.27<br>69.48<br>62.54<br>63.01<br>60.76<br>54.99<br>54.48<br>67.25<br>60.42<br>61.03|62.32<br>60.47<br>60.04<br>63.81<br>61.46<br>61.31<br>26.88<br>24.81<br>25.02<br>45.22<br>42.85<br>42.60<br>64.14<br>62.08<br>61.66<br>45.72<br>47.60<br>45.16<br>**65.31**<br>**63.26**<br>**63.01**|



**Table 2: Performance comparison (%) on the MultiHop-RAG.**

|Method|Inference Comparison Null Temporal Overall|
|---|---|
|RAG<br>RaptorRAG<br>KG-GraphRAG (Triplets only)<br>KG-GraphRAG (Triplets+Text)<br>Community-GraphRAG (Local)<br>Community-GraphRAG (Global)<br>HippoRAG2|**92.16**<br>57.59<br>96.01<br>30.70<br>67.02<br>91.91<br>55.26<br>90.03<br>45.28<br>68.78<br>55.76<br>22.55<br>**98.67**<br>18.70<br>41.24<br>67.40<br>34.70<br>97.34<br>17.15<br>48.51<br>86.89<br>60.63<br>80.07<br>50.60<br>69.01<br>89.34<br>**64.02**<br>19.27<br>**53.34**<br>64.40<br>91.54<br>58.41<br>85.71<br>49.91<br>**70.27**|



**4.2** **QA Main Results**


We first compare the vanilla versions of RAG and GraphRAG variants. Unless otherwise specified, we report main-paper results using
Llama-3.1-8B-Instruct. Results using Llama-3.1-70B-Instruct are deferred to the Appendix B. Results on NQ and HotPotQA are shown
in Table 1, and results on MultiHop-RAG are shown in Table 2.
Due to space constraints, we report partial results on NovelQA
in Table 3, with the full breakdown provided in Appendix B. We
summarize key observations below:


(1) **RAG excels on detailed single-hop queries.** RAG achieves
strong performance on the single-hop benchmark NQ and on
the single-hop (sh) and detail-oriented (dtl) subsets of NovelQA
(Tables 1 and 3).
(2) **GraphRAG methods (e.g., HippoRAG2 and Community-**
**GraphRAG (Local)) excel on multi-hop queries.** They perform best on multi-hop QA benchmarks (HotPotQA and MultiHopRAG) and remain competitive on the multi-hop (mh) subset of
NovelQA (Tables 1, 2, and 3).
(3) **Community-GraphRAG (Global) often struggles on QA.**
Global search retrieves high-level community summaries, which
can lose fine-grained evidence and hurt detail-centric QA, as
reflected on detail-oriented subsets in NovelQA. It also performs
poorly on Null queries in MultiHop-RAG (ideally answered as
insufficient information ), suggesting increased hallucination risk. However, summary-level retrieval can be beneficial
for Comparison and Temporal queries in MultiHop-RAG which
require global information.



(4) **KG-based GraphRAG generally underperforms on QA**
**due to limited graph coverage.** KG-GraphRAG retrieves evidence primarily from extracted entities and relations, which
can be incomplete and omit answer-critical information. In
Appendix C, we show that only about 65.8% of answer entities appear in the constructed KG for HotPotQA and 65.5% for
NQ, highlighting the sensitivity of KG-based retrieval to graph
construction quality.

We further provide case studies in Appendix D.


|NQ (Single-hop QA)|Col2|Col3|
|---|---|---|
|60<br>62<br>64<br>66<br>Overall F1 (%)<br>|60<br>62<br>64<br>66<br>Overall F1 (%)<br>|60<br>62<br>64<br>66<br>Overall F1 (%)<br>|
|60<br>62<br>64<br>66<br>Overall F1 (%)<br>|||
|60<br>62<br>64<br>66<br>Overall F1 (%)<br>|||
|60<br>62<br>64<br>66<br>Overall F1 (%)<br>|||


|MultiHop-RAG (Multi-hop QA) RAG (Local) HippoRAG2|Col2|Col3|
|---|---|---|
||||
||||
||||
||||



**Figure 1: Overall QA performance (F1) under different infer-**
**ence strategies on NQ and MultiHop-RAG.**


**4.3** **QA with Reranking and Iterative Retrieval**


In addition to vanilla retrieval, we examine the impact of _rerank-_
_ing_ and _iterative retrieval_ on QA performance. We conduct experiments on **NQ** and **MultiHop-RAG**, representing single-hop and
multi-hop QA scenarios, respectively. Figure 1 summarizes overall
performance under different inference strategies.
Across both datasets, reranking and iterative retrieval generally
improve performance for all methods compared to vanilla inference, indicating that inference-time enhancements provide gains
beyond the underlying retrieval architecture. On **NQ**, both reranking and iterative retrieval (IRCoT) yield consistent improvements,
suggesting that such refinements can be beneficial even for predominantly single-hop QA. Importantly, our earlier conclusion remains
unchanged: RAG still performs better on single-hop, detail-oriented
questions, even when equipped with reranking or iterative retrieval.
On the **MultiHop-RAG** benchmark, the gains from inference-time
strategies are more pronounced. Both reranking and IRCoT lead to
larger absolute improvements than on NQ, highlighting the value
of progressive evidence refinement in multi-hop settings. Under
these enhanced inference strategies, GraphRAG methods also typically outperform RAG. One exception is Community-GraphRAG
(Local) with IRCoT, which exhibits notably low performance on
NULL queries, despite improvements on other categories. This observation remains consistent with our main findings.
Overall, reranking and iterative retrieval are complementary
to both RAG and GraphRAG, and are particularly important for
multi-hop QA. Detailed results are reported in Appendix E and F.


**4.4** **Comparative QA Analysis**


In this section, we provide a detailed comparison of RAG and
GraphRAG, with a focus on their respective strengths and weaknesses. Unless otherwise specified, we consider vanilla RAG and
Community-GraphRAG (Local), and refer to the latter simply as
GraphRAG, as it exhibits performance comparable to RAG in our experiments. We partition all queries into four categories: **(1)** queries






RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


**Table 3: Performance comparison (%) on the NovelQA dataset.**


|RAG|RaptorRAG|
|---|---|
|chara<br>mean<br>plot<br>relat<br>settg<br>span<br>times<br>avg<br>mh<br>68.75<br>52.94<br>58.33<br>75.28<br>92.31<br>64.00<br>33.96<br>47.34<br>sh<br>69.08<br>62.86<br>66.11<br>75.00<br>78.35<br>-<br>-<br>68.73<br>dtl<br>64.29<br>45.51<br>78.57<br>10.71<br>83.78<br>-<br>-<br>55.28<br>avg<br>67.78<br>50.57<br>67.37<br>60.80<br>80.95<br>64.00<br>33.96<br>57.12|chara<br>mean<br>plot<br>relat<br>settg<br>span<br>times<br>avg<br>mh<br>60.42<br>70.59<br>63.89<br>65.17<br>92.31<br>52<br>38.24<br>48.17<br>sh<br>66.45<br>58.57<br>65.27<br>62.50<br>74.23<br>-<br>-<br>66.25<br>dtl<br>62.86<br>48.88<br>80.36<br>28.57<br>78.38<br>-<br>-<br>57.72<br>avg<br>64.44<br>52.83<br>67.67<br>56.80<br>76.87<br>52<br>38.24<br>57.12|
|**KG-GraphRAG (Triplets+Text)**|**Community-GraphRAG (Local)**|
|chara<br>mean<br>plot<br>relat<br>settg<br>span<br>times<br>avg<br>mh<br>52.08<br>52.94<br>44.44<br>55.06<br>69.23<br>64.00<br>28.61<br>38.37<br>sh<br>36.84<br>45.71<br>40.17<br>87.50<br>36.08<br>-<br>-<br>39.93<br>dtl<br>38.57<br>30.90<br>42.86<br>21.43<br>32.43<br>-<br>-<br>33.60<br>avg<br>40.00<br>36.23<br>41.09<br>49.60<br>38.10<br>64.00<br>28.61<br>37.80|chara<br>mean<br>plot<br>relat<br>settg<br>span<br>times<br>avg<br>mh<br>68.75<br>64.71<br>55.56<br>67.42<br>92.31<br>52.00<br>35.83<br>47.01<br>sh<br>59.87<br>58.57<br>65.69<br>87.50<br>64.95<br>-<br>-<br>63.43<br>dtl<br>54.29<br>37.64<br>62.50<br>25.00<br>70.27<br>-<br>-<br>46.88<br>avg<br>60.00<br>44.91<br>64.05<br>59.20<br>68.71<br>52.00<br>35.83<br>53.03|
|**Community-GraphRAG (Global)**|**HippoRAG2**|
|chara<br>mean<br>plot<br>relat<br>settg<br>span<br>times<br>avg<br>mh<br>54.17<br>58.82<br>55.56<br>56.18<br>53.85<br>68<br>20.59<br>34.39<br>sh<br>45.39<br>50.00<br>55.65<br>87.50<br>38.14<br>-<br>-<br>49.65<br>dtl<br>28.57<br>29.78<br>32.14<br>87.50<br>40.54<br>-<br>-<br>30.89<br>avg<br>42.59<br>36.98<br>51.66<br>52.00<br>40.14<br>68<br>20.59<br>39.17|chara<br>mean<br>plot<br>relat<br>settg<br>span<br>times<br>avg<br>mh<br>58.33<br>64.71<br>66.67<br>69.66<br>92.31<br>48<br>37.17<br>47.84<br>sh<br>65.79<br>65.71<br>64.44<br>62.50<br>72.16<br>-<br>-<br>66.25<br>dtl<br>60.00<br>48.88<br>69.64<br>28.57<br>81.08<br>-<br>-<br>55.83<br>avg<br>62.96<br>54.34<br>65.56<br>60.00<br>76.19<br>48<br>37.17<br>56.54|



**(a) NQ**


**(c) MultiHop-RAG**



**(b) HotpotQA**


**(d) NovelQA**



**Figure 2: Confusion matrices comparing GraphRAG and RAG**
**correctness across datasets using Llama 3.1-8B.**


correctly answered by both methods, **(2)** queries correctly answered
only by RAG (RAG-only), **(3)** queries correctly answered only by
GraphRAG (GraphRAG-only), and **(4)** queries incorrectly answered
by both methods.
The confusion matrices representing these four groups using the
Llama 3.1-8B model are shown in Figure 2. Notably, the proportions
of queries correctly answered exclusively by GraphRAG and RAG
are significant. For example, 13.6% of queries are GraphRAG-only,
while 11.6% are RAG-only on MultiHop-RAG dataset. This phenomenon highlights the complementary properties of RAG and
GraphRAG. Therefore, _leveraging their unique advantages has the_
_potential to improve overall performance_ .



**4.5** **Improving QA Performance**


Building on the complementary properties of RAG and GraphRAG,
we investigate the following two strategies to enhance overall QA
performance.


_Strategy 1: RAG vs. GraphRAG Selection._ In Section 4.2, we observe that RAG generally performs well on single-hop queries and
those requiring detailed information, while GraphRAG (CommunityGraphRAG (Local)) excels in multi-hop queries that require reasoning. Therefore, we hypothesize that RAG is well-suited for factbased queries, which rely on direct retrieval and detailed information, whereas GraphRAG is more effective for reasoning-based
queries that involve chaining multiple facts together. Therefore,
given a query, we employ a classification mechanism to determine
whether it is fact-based or reasoning-based. Each query is then
assigned to either RAG or GraphRAG based on the classification
results. Specifically, we leverage the in-context learning ability of
LLMs for classification [3, 40]. Further details and prompts can be
found in Appendix G. In this strategy, either RAG or GraphRAG is
selected for each query, and we refer to this strategy as **Selection** .


_Strategy 2: RAG and GraphRAG Integration._ We further explore
an **Integration** strategy that jointly leverages the complementary
retrieval behaviors of RAG and GraphRAG. For each query, both
methods retrieve relevant information in parallel, and the retrieved
contexts are concatenated and fed into the generator to produce
the final answer. We evaluate the effectiveness of the two proposed
strategies on all selected datasets. For MultiHop-RAG and NovelQA,
we report overall accuracy, while for NQ and HotPotQA, we use
F1 score as the evaluation metric. The results are summarized in

Figure 3 and Appendix H.
Overall, both strategies consistently improve QA performance
across datasets. For instance, on MultiHop-RAG with Llama 3.1-70B,
the Selection and Integration strategies improve the best baseline


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.















**Figure 3: Overall QA performance comparison of different methods.**



**4.6** **Computation and Storage Analysis**

|RAG<br>GraphRAG<br>70 Selection<br>Integration<br>Performance<br>65<br>60<br>55<br>50<br>NQ Hotpot MultiHop-RAG NovelQA<br>(a) Llama3.1-8B<br>Figure 3: Overall QA performanc<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efficient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>Table 4: The time and storage analysis on MultiHop-RAG.<br>Method Construction Time (s) Retrieval time (s) Storage<br>RAG 135 1724 127MB<br>KG-GraphRAG 7702 14434 117MB<br>Community-GraphRAG 5560 1249 165MB|RAG<br>Grap<br>Sele|Col3|hRAG<br>ction|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>|Integration|Integration|Integration|Integration|Integration|Integration|Integration||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(a) Llama3.1-8B**<br>**Figure 3: Overall QA performanc**<br>by 1.1% and 6.4%, respectively. When comparing the two strate-<br>gies, Integration generally achieves higher performance than Selec-<br>ion. However, Selection processes each query using only a single<br>method, making it more computationally efcient. In contrast, Inte-<br>gration requires running both RAG and GraphRAG for every query,<br>eading to higher computational cost.<br>**Table 4: The time and storage analysis on MultiHop-RAG.**<br>Method<br>Construction Time (s)<br>Retrieval time (s)<br>Storage<br>RAG<br>135<br>1724<br>127MB<br>KG-GraphRAG<br>7702<br>14434<br>117MB<br>Community-GraphRAG<br>5560<br>1249<br>165MB<br><br>||~~NQ~~<br>espec<br>erally<br>ction<br>ore c<br>ning b<br>mput<br>** and**|**(a**<br>**Fi**<br>tively. W<br> achieve<br>processe<br>omputati<br>oth RAG<br>ational c<br>**storage**|~~Hot~~<br>**) L**<br>**gu**<br>h<br>s h<br>s e<br>on<br> a<br>os<br>**an**|~~po~~<br>**la**<br>**re**<br>en<br>ig<br>ac<br>all<br>nd<br>t.<br>**al**|~~t~~<br>**ma**<br>** 3:**<br> co<br>he<br>h q<br>y<br> G<br>**ys**|~~Mu~~<br>**3.1-**<br>** Ov**<br>mp<br>r per<br>uer<br>efc<br>raph<br>**is o**|~~ltiH~~<br>**8B**<br>**era**<br>ari<br>for<br>y u<br>ien<br>RA<br>**n**|~~op-~~<br>**ll**<br>ng<br>m<br>sin<br>t. I<br>G<br>**Mu**|~~RA~~<br>**Q**<br>th<br>an<br>g<br>n c<br>for<br>**lti**|~~G~~<br>**A p**<br>e t<br>ce<br>on<br>on<br> e<br>**H**|~~N~~<br>**er**<br>w<br>th<br>ly<br>tr<br>ver<br>**op**|~~ov~~<br>**fo**<br>o s<br>an<br> a<br>ast<br>y<br>**-R**|~~elQ~~<br>**r**<br>tr<br>Se<br>sin<br>, I<br>qu<br>**A**|~~A~~<br>**ma**<br>ate<br>lec<br>gl<br>nte<br>er<br>**G.**|**nc**<br>-<br>-<br>e<br>-<br>y,|
|Method|Method|Co|nstruction|Ti|me (|s)|Ret|riev|al t|im|e (s|)|St|ora|ge|ge|
|RAG<br>KG-GraphRAG<br>Community-GraphRA|RAG<br>KG-GraphRAG<br>Community-GraphRA|G|135<br>7702<br>5560|||||1<br>1<br>1|724<br>443<br>249|4<br>|||12<br>11<br>16|7M<br>7M<br>5M|B<br>B<br>B|B<br>B<br>B|
||||||||||||||||||



In this subsection, we analyze the computational and storage tradeoffs among RAG, KG-GraphRAG, and Community-GraphRAG. Specifically, we report construction time, retrieval latency, and storage
footprint on the MultiHop-RAG dataset. The results are summarized
in Table 4. Results for additional datasets and tasks are provided in
Appendix M. From the results, we have the following observations:


- **Construction time:** Both GraphRAG variants incur substantially higher construction cost than RAG, as they require additional graph construction and preprocessing.

- **Retrieval time:** KG-GraphRAG exhibits the highest retrieval
latency, primarily due to LLM-based entity expansion and multistep graph traversal. In contrast, Community-GraphRAG achieves
the lowest retrieval latency by relying on direct community-level
matching, even outperforming vanilla RAG.

- **Storage:** Community-GraphRAG requires the largest storage
footprint, as it stores both community representations and associated summaries. KG-GraphRAG is more storage-efficient than
Community-GraphRAG and RAG, reflecting a trade-off between
information richness and storage cost.

We additionally report the number of retrieved tokens for each
method and evaluate their performance under a fixed retrieval
token budget, with detailed results provided in the Appendix M.


**4.7** **Graph Construction Model**


In this subsection, we analyze how graph construction quality affects GraphRAG performance. We focus on Community-GraphRAG



|RAG<br>GraphRAG<br>75<br>Selection<br>Integration<br>70 Performance<br>65<br>60<br>55<br>50<br>NQ Hotpot MultiHop-RAG NovelQA<br>(b) Llama3.1-70B<br>omparison of different methods.<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fixed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>different query categories.<br>Table 5: Impact of graph construction models on the<br>MultiHop-RAG dataset using Llama 3.1–70B-Instruct.<br>Graph Construction Inference Comparison NULL Temporal Overall<br>None (RAG) 94.85 56.31 91.36 25.73 65.77<br>GPT-4o-mini 92.03 60.16 88.70 49.06 71.17<br>GPT-4o 93.63 66.59 81.06 58.49 75.08|RAG<br>Grap<br>Sele|Col3|hRAG<br>ction|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|RAG<br>Grap<br>~~Sele~~<br>|RAG<br>Grap<br>~~Sele~~<br>|hRAG<br>~~ction~~<br>|hRAG<br>~~ction~~<br>|hRAG<br>~~ction~~<br>|hRAG<br>~~ction~~<br>|hRAG<br>~~ction~~<br>|hRAG<br>~~ction~~<br>|hRAG<br>~~ction~~<br>||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|Integration|Integration|Integration|Integration|Integration|Integration|Integration|Integration|||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|||||||||||||||||
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08||~~NQ~~<br>**ison**<br>l) as a<br>for gra<br> comp<br>s mult<br>ndix L<br>ent qu<br>**e 5:**<br>**iHop**|~~H~~<br>**(b)**<br>**of difer**<br> represe<br>ph cons<br>onents f<br>iple task<br>. Table 2<br>ery cate<br>**Impact**<br>**-RAG da**|~~ot~~<br>** L**<br>**e**<br>nt<br>tr<br>xe<br>s a<br>8<br>go<br>**o**<br>**t**|~~po~~<br>**la**<br>**nt**<br>ati<br>uct<br>d.<br>nd<br>su<br>rie<br>**f**<br>**ase**|~~t~~<br>**ma**<br>**m**<br>ve<br>io<br>W<br> d<br>mm<br>s.<br>**gr**<br>**t**|~~Mu~~<br>**3.1-**<br>**eth**<br> Gra<br>n, w<br>e ev<br>atas<br>ariz<br>**aph**<br>**usin**|~~ltiH~~<br>**70B**<br>**ods**<br>ph<br>hile<br>alua<br>ets,<br>es<br>** c**<br>**g L**|~~op-~~<br><br>**.**<br>R<br> k<br>te<br> w<br>re<br>**on**<br>**la**|~~RA~~<br>AG<br>ee<br> do<br>ith<br>sul<br>**st**<br>**m**|~~G~~<br> v<br>pin<br>w<br> d<br>ts<br>**ru**<br>**a**|~~N~~<br>ari<br>g<br>ns<br>eta<br>on<br>**ct**<br>**3.1**|~~ov~~<br>an<br>the<br>tre<br>ile<br> M<br>**io**<br>**–7**|~~elQ~~<br>t a<br> r<br>am<br>d<br>ul<br>**n**<br>**0**|~~A~~<br>n<br>etr<br> Q<br>res<br>tiH<br>**m**<br>**B-I**|~~A~~<br>n<br>etr<br> Q<br>res<br>tiH<br>**m**<br>**B-I**|
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08||**ph Con**<br>|**struction**<br>|I|nfe<br>|ren<br>|ce<br><br>|Com<br>|pa<br>|riso<br>|n|N<br>|UL<br>|L<br>|Te|mporal<br>Overall<br><br>|
|~~NQ~~<br>~~Hotpot~~<br>~~MultiHop-RAG~~<br>~~NovelQA~~<br>50<br>55<br>60<br>65<br>70<br>75<br>Performance<br>RAG<br>GraphRAG<br>~~Selection~~<br>Integration<br>**(b) Llama3.1-70B**<br>**omparison of diferent methods.**<br>(Local) as a representative GraphRAG variant and vary the LLM<br>used for graph construction, while keeping the retrieval and gener<br>ation components fxed. We evaluate downstream QA performance<br>across multiple tasks and datasets, with detailed results reported in<br>Appendix L. Table 28 summarizes results on MultiHop-RAG acros<br>diferent query categories.<br>**Table 5: Impact of graph construction models on the**<br>**MultiHop-RAG dataset using Llama 3.1–70B-Instruct.**<br>**Graph Construction**<br>Inference<br>Comparison<br>NULL<br>Temporal<br>Overall<br>None (RAG)<br>94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>GPT-4o-mini<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>GPT-4o<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08||**ph Con**<br>|**struction**<br>|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|


We observe that stronger graph construction models consistently improve QA performance, especially on reasoning-intensive
queries such as Comparison and Temporal. While omitting explicit
graph construction (i.e., RAG) yields strong performance on Inference and NULL queries, it performs poorly on multi-hop reasoning
tasks. In contrast, graphs constructed using more capable LLMs,
such as GPT-4o, substantially improve performance on these challenging categories, leading to the highest overall accuracy. These
results indicate that GraphRAG performance is sensitive to graph
construction quality. However, stronger construction models also
incur higher computational cost, highlighting a trade-off between
graph quality and system efficiency when selecting LLMs for graph

construction.

**Summary.** Across our QA experiments, we find that RAG and
GraphRAG exhibit complementary strengths rather than a clear
dominance. RAG consistently performs well on single-hop, factcentric queries that require precise retrieval of detailed information,
while GraphRAG excels on reasoning-intensive, multi-hop queries
by explicitly modeling relationships among entities. However, these
benefits come with different computational and storage trade-offs,
and GraphRAG performance is further influenced by the quality of
graph construction. Motivated by these observations, we explore
selection and integration strategies that combine the strengths
of both paradigms, leading to consistent improvements in overall
QA performance. Together, these results suggest that effective QA
systems should adaptively balance retrieval precision, reasoning
capability, and system efficiency, rather than relying on a single
retrieval paradigm.


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY



**5** **Query-Based Summarization**


Query-based summarization is a widely used benchmark for evaluating retrieval-augmented generation (RAG) systems [ 30, 52 ]. Recent work has also demonstrated the potential of GraphRAG for
summarization tasks [ 5 ]. However, Edge et al . [5] focus primarily
on global summarization and rely on LLM-as-a-Judge [ 57 ] for evaluation. As shown in Section 5.3, LLM-as-a-Judge introduces position
bias in summarization evaluation, which can compromise result
reliability. Despite the growing interest in GraphRAG, a systematic
comparison between RAG and GraphRAG on general query-based
summarization tasks across widely used datasets remains unexplored. To address this gap, we conduct a comprehensive evaluation
in this section using standard benchmarks and evaluation metrics.


**5.1** **Datasets and Evaluation Metrics**


We evaluate RAG and GraphRAG on four widely used query-based
summarization datasets: two single-document datasets, SQuALITY [ 37 ] and QMSum [ 58 ], and two multi-document datasets, ODSumstory and ODSum-meeting [ 59 ]. Unlike the LLM-generated global
queries used in the unreleased datasets of Edge et al . [5], most
queries in the selected datasets focus on specific roles or events.
Since these datasets contain one or more human-written ground
truth summaries for each query, we leverage ROUGE-2 [ 22 ] and
BERTScore [ 54 ] as evaluation metrics to measure lexical and semantic similarity between the predicted and ground truth summaries.


**5.2** **Summarization Experimental Results**


We evaluate on vanilla RAG and GraphRAG methods, along with
the Integration strategy discussed in Section 4.5. The results of
Llama3.1-8B model on Query-based single document summarization and multiple document summarization are shown in Table 6
and Table 7, respectively. The results of Llama3.1-70B are shown
in Appendix I. Based on these results, we can make the following
observations:

(1) **RAG, RaptorRAG, and HippoRAG2 generally performs**
**well on query-based summarization tasks**, primarily because they retrieve original text chunks that are more closely
aligned with ground truth.
(2) **KG-based GraphRAG benefit from combining triplets**
**with their corresponding text** . This improves performance
by incorporating more details, making predictions closer to the
human-written ground truth summaries.
(3) **Community-based GraphRAG performs better with the**
**Local search method** . Local search retrieves entities, relations,
and low-level communities, while the Global search method
retrieves only high-level summaries. This demonstrates the
importance of detailed information in the selected datasets.
(4) **The Integration strategy often performs comparably to**
**RAG alone**, suggesting that simply concatenating RAG and
GraphRAG evidence does not reliably improve alignment with
detailed ground-truth summaries.


**5.3** **Position Bias in Existing Evaluation**


Based on the results in Section 5.2, Community-based GraphRAG,
particularly with global search, generally underperforms RAG on
the selected datasets. This observation contrasts with the findings



of Edge et al . [5], where Community-based GraphRAG with global
search outperformed both local search and RAG.
This discrepancy can be attributed to two key differences between our evaluation and that of Edge et al . [5] . First, their study
focuses on global summarization, which aims to capture high-level
information from an entire corpus, whereas the datasets used in our
evaluation involve queries targeting specific roles or events. Second,
Edge et al . [5] evaluate performance using LLM-as-a-Judge without
ground-truth references, while we evaluate generated summaries
against human-written references using ROUGE and BERTScore.
These reference-based metrics emphasize factual coverage and finegrained details, which may favor different retrieval behaviors.
To further investigate this difference, we follow Edge et al . [5]
and evaluate RAG and GraphRAG using LLM-as-a-Judge from two
perspectives: _Comprehensiveness_ and _Diversity_ . Comprehensiveness
measures how well a summary covers the details required by the
query, while Diversity assesses whether the summary provides a
broad and globally inclusive view. Prompt details are provided in
Appendix J. For each query, we present summaries generated by
RAG and GraphRAG to the LLM and ask it to select the better one
under each criterion.

To examine potential position effects in LLM-as-a-Judge evaluations, we consider two presentation orders: Order 1 (O1), where the
RAG summary appears first, and Order 2 (O2), where the GraphRAG
summary appears first. For each setting, we report the proportion
of times each method is preferred by the LLM, where a higher
proportion indicates stronger performance under the given presentation order. Figure 4 presents results comparing RAG with
GraphRAG (Local) and GraphRAG (Global) on the QMSum and
ODSum-story datasets; additional results are included in Appendix K. We make two key observations. First, **position bias [** **33** **,** **39** **]**
**is clearly present in LLM-as-a-Judge evaluations for summa-**
**rization**, as reversing the order of presented summaries leads to
substantially different, and in some cases opposite, judgments. This
effect is especially pronounced for the comparison between RAG
and GraphRAG (Local), as shown in Figures 4a and 4c. Second, in
comparisons between RAG and GraphRAG (Global), RAG is consistently preferred in terms of Comprehensiveness, while GraphRAG
(Global) is favored for Diversity (Figures 4b and 4d). This suggests
that **Community-based GraphRAG with global search empha-**
**sizes corpus-level coverage, whereas RAG is more effective**
**at capturing fine-grained, query-specific details** .
Finally, we report additional summarization results with reranking and iterative retrieval in Appendix E and F. We also provide
a detailed analysis of indexing time, retrieval latency, generation
cost, and token and storage usage for both methods in Appendix M.
Furthermore, we examine graph construction with different LLMs
for summarization tasks in Appendix L.
**Summary.** Across query-based summarization benchmarks, RAG
and GraphRAG exhibit different generation characteristic. Under
reference-based metrics, RAG typically better matches detailed,
query-specific ground-truth summaries, whereas GraphRAG, especially community-based global retrieval, tends to produce more
corpus-level and diverse summaries that can deviate from finegrained details. We also find that LLM-as-a-Judge evaluation can
be sensitive to presentation order, raising reliability concerns for
judge-based comparisons. Overall, these results highlight the need


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.


**Table 6: The performance of query-based single document summarization task using Llama 3.1-8B.**







|SQuALITY QMSum<br>Method ROUGE-2 BERTScore ROUGE-2 BERTScore<br>P R F1 P R F1 P R F1 P R F1|SQuALITY|QMSum|
|---|---|---|
|**Method**<br>**SQuALITY**<br>**QMSum**<br>**ROUGE-2**<br>**BERTScore**<br>**ROUGE-2**<br>**BERTScore**<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1|**ROUGE-2**<br>**BERTScore**|**ROUGE-2**<br>**BERTScore**|
|**Method**<br>**SQuALITY**<br>**QMSum**<br>**ROUGE-2**<br>**BERTScore**<br>**ROUGE-2**<br>**BERTScore**<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1<br>P<br>R<br>F1|
|RAG<br>RaptorRAG<br>KG-GraphRAG (Triplets only)<br>KG-GraphRAG (Triplets+Text)<br>Community-GraphRAG (Local)<br>Community-GraphRAG (Global)<br>HippoRAG2<br>Integration|15.09<br>8.74<br>10.08<br>74.54<br>81.00<br>77.62<br><br>14.88<br>8.42<br>9.81<br>74.55<br>81.20<br>77.71<br><br>11.99<br>6.16<br>7.41<br>82.46<br>84.30<br>83.17<br><br>15.00<br>**9.48**<br>10.52<br>**84.37**<br>**85.88**<br>**84.92**<br><br>**15.82**<br>8.64<br>10.10<br>83.93<br>85.84<br>84.66<br><br>10.23<br>6.21<br>6.99<br>82.68<br>84.26<br>83.30<br><br>15.07<br>8.95<br>10.20<br>74.60<br>81.24<br>77.75<br><br>15.69<br>9.32<br>**10.67**<br>74.56<br>81.22<br>77.73<br>**2**|21.50<br>3.80<br>6.32<br>81.03<br>84.45<br>82.69<br>20.38<br>**4.17**<br>**6.68**<br>**81.64**<br>84.57<br>**83.07**<br>13.71<br>2.55<br>4.15<br>80.16<br>82.96<br>81.52<br>16.83<br>3.32<br>5.38<br>80.92<br>83.64<br>82.25<br>20.54<br>3.35<br>5.64<br>80.63<br>84.13<br>82.34<br>10.54<br>1.97<br>3.23<br>79.79<br>82.47<br>81.10<br>21.35<br>4.01<br>6.60<br>81.44<br>**84.63**<br>83.00<br>**1.97**<br>3.80<br>6.34<br>80.89<br>84.47<br>82.63|


**Table 7: The performance of query-based multiple document summarization task using Llama3.1-8B.**








|ODSum-story ODSum-meeting<br>Method ROUGE-2 BERTScore ROUGE-2 BERTScore<br>P R F1 P R F1 P R F1 P R F1<br>RAG 15.39 8.44 9.81 83.87 85.74 84.57 15.50 6.43 8.77 83.12 85.84 84.45<br>RaptorRAG 14.69 8.47 9.62 83.87 85.76 84.58 14.85 6.21 8.44 82.66 85.52 84.06<br>KG-GraphRAG (Triplets only) 11.02 5.56 6.62 82.09 83.91 82.77 11.64 4.87 6.58 81.13 84.32 82.69<br>KG-GraphRAG (Triplets+Text) 9.19 5.82 6.22 79.39 83.30 81.03 11.97 4.97 6.72 81.50 84.41 82.92<br>Community-GraphRAG (Local) 13.84 7.19 8.49 83.19 85.07 83.90 15.65 5.66 8.02 82.44 85.54 83.96<br>Community-GraphRAG (Global) 9.40 4.47 5.46 81.46 83.54 82.30 11.44 3.89 5.59 81.20 84.50 82.81<br>HippoRAG2 15.56 8.43 9.82 83.70 85.71 84.46 15.91 6.09 8.51 82.43 85.55 83.95<br>Integration 14.77 8.55 9.53 83.73 85.56 84.40 15.69 6.15 8.51 82.87 85.81 84.31|ODSum-story|ODSum-meeting|
|---|---|---|
|**Method**<br>**ODSum-story**<br>**ODSum-meeting**<br>**ROUGE-2**<br>**BERTScore**<br>**ROUGE-2**<br>**BERTScore**<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>RAG<br>15.39<br>8.44<br>9.81<br>**83.87**<br>**85.74**<br>84.57<br>15.50<br>**6.43**<br>**8.77**<br>**83.12**<br>**85.84**<br>**84.45**<br>RaptorRAG<br>14.69<br>8.47<br>9.62<br>**83.87**<br>85.76<br>**84.58**<br>14.85<br>6.21<br>8.44<br>82.66<br>85.52<br>84.06<br>KG-GraphRAG (Triplets only)<br>11.02<br>5.56<br>6.62<br>82.09<br>83.91<br>82.77<br>11.64<br>4.87<br>6.58<br>81.13<br>84.32<br>82.69<br>KG-GraphRAG (Triplets+Text)<br>9.19<br>5.82<br>6.22<br>79.39<br>83.30<br>81.03<br>11.97<br>4.97<br>6.72<br>81.50<br>84.41<br>82.92<br>Community-GraphRAG (Local)<br>13.84<br>7.19<br>8.49<br>83.19<br>85.07<br>83.90<br>15.65<br>5.66<br>8.02<br>82.44<br>85.54<br>83.96<br>Community-GraphRAG (Global)<br>9.40<br>4.47<br>5.46<br>81.46<br>83.54<br>82.30<br>11.44<br>3.89<br>5.59<br>81.20<br>84.50<br>82.81<br>HippoRAG2<br>**15.56**<br>8.43<br>**9.82**<br>83.70<br>85.71<br>84.46<br>**15.91**<br>6.09<br>8.51<br>82.43<br>85.55<br>83.95<br>Integration<br>14.77<br>**8.55**<br>9.53<br>83.73<br>85.56<br>84.40<br>15.69<br>6.15<br>8.51<br>82.87<br>85.81<br>84.31|**ROUGE-2**<br>**BERTScore**|**ROUGE-2**<br>**BERTScore**|
|**Method**<br>**ODSum-story**<br>**ODSum-meeting**<br>**ROUGE-2**<br>**BERTScore**<br>**ROUGE-2**<br>**BERTScore**<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>RAG<br>15.39<br>8.44<br>9.81<br>**83.87**<br>**85.74**<br>84.57<br>15.50<br>**6.43**<br>**8.77**<br>**83.12**<br>**85.84**<br>**84.45**<br>RaptorRAG<br>14.69<br>8.47<br>9.62<br>**83.87**<br>85.76<br>**84.58**<br>14.85<br>6.21<br>8.44<br>82.66<br>85.52<br>84.06<br>KG-GraphRAG (Triplets only)<br>11.02<br>5.56<br>6.62<br>82.09<br>83.91<br>82.77<br>11.64<br>4.87<br>6.58<br>81.13<br>84.32<br>82.69<br>KG-GraphRAG (Triplets+Text)<br>9.19<br>5.82<br>6.22<br>79.39<br>83.30<br>81.03<br>11.97<br>4.97<br>6.72<br>81.50<br>84.41<br>82.92<br>Community-GraphRAG (Local)<br>13.84<br>7.19<br>8.49<br>83.19<br>85.07<br>83.90<br>15.65<br>5.66<br>8.02<br>82.44<br>85.54<br>83.96<br>Community-GraphRAG (Global)<br>9.40<br>4.47<br>5.46<br>81.46<br>83.54<br>82.30<br>11.44<br>3.89<br>5.59<br>81.20<br>84.50<br>82.81<br>HippoRAG2<br>**15.56**<br>8.43<br>**9.82**<br>83.70<br>85.71<br>84.46<br>**15.91**<br>6.09<br>8.51<br>82.43<br>85.55<br>83.95<br>Integration<br>14.77<br>**8.55**<br>9.53<br>83.73<br>85.56<br>84.40<br>15.69<br>6.15<br>8.51<br>82.87<br>85.81<br>84.31|P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1<br>P<br>R<br>F1|
|**Method**<br>**ODSum-story**<br>**ODSum-meeting**<br>**ROUGE-2**<br>**BERTScore**<br>**ROUGE-2**<br>**BERTScore**<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>RAG<br>15.39<br>8.44<br>9.81<br>**83.87**<br>**85.74**<br>84.57<br>15.50<br>**6.43**<br>**8.77**<br>**83.12**<br>**85.84**<br>**84.45**<br>RaptorRAG<br>14.69<br>8.47<br>9.62<br>**83.87**<br>85.76<br>**84.58**<br>14.85<br>6.21<br>8.44<br>82.66<br>85.52<br>84.06<br>KG-GraphRAG (Triplets only)<br>11.02<br>5.56<br>6.62<br>82.09<br>83.91<br>82.77<br>11.64<br>4.87<br>6.58<br>81.13<br>84.32<br>82.69<br>KG-GraphRAG (Triplets+Text)<br>9.19<br>5.82<br>6.22<br>79.39<br>83.30<br>81.03<br>11.97<br>4.97<br>6.72<br>81.50<br>84.41<br>82.92<br>Community-GraphRAG (Local)<br>13.84<br>7.19<br>8.49<br>83.19<br>85.07<br>83.90<br>15.65<br>5.66<br>8.02<br>82.44<br>85.54<br>83.96<br>Community-GraphRAG (Global)<br>9.40<br>4.47<br>5.46<br>81.46<br>83.54<br>82.30<br>11.44<br>3.89<br>5.59<br>81.20<br>84.50<br>82.81<br>HippoRAG2<br>**15.56**<br>8.43<br>**9.82**<br>83.70<br>85.71<br>84.46<br>**15.91**<br>6.09<br>8.51<br>82.43<br>85.55<br>83.95<br>Integration<br>14.77<br>**8.55**<br>9.53<br>83.73<br>85.56<br>84.40<br>15.69<br>6.15<br>8.51<br>82.87<br>85.81<br>84.31|15.39<br>8.44<br>9.81<br>**83.87**<br>**85.74**<br>84.57<br>1<br>14.69<br>8.47<br>9.62<br>**83.87**<br>85.76<br>**84.58**<br>1<br>11.02<br>5.56<br>6.62<br>82.09<br>83.91<br>82.77<br>1<br>9.19<br>5.82<br>6.22<br>79.39<br>83.30<br>81.03<br>1<br>13.84<br>7.19<br>8.49<br>83.19<br>85.07<br>83.90<br>1<br>9.40<br>4.47<br>5.46<br>81.46<br>83.54<br>82.30<br>1<br>**15.56**<br>8.43<br>**9.82**<br>83.70<br>85.71<br>84.46<br>**1**<br>14.77<br>**8.55**<br>9.53<br>83.73<br>85.56<br>84.40<br>1|5.50<br>**6.43**<br>**8.77**<br>**83.12**<br>**85.84**<br>**84.45**<br>4.85<br>6.21<br>8.44<br>82.66<br>85.52<br>84.06<br>1.64<br>4.87<br>6.58<br>81.13<br>84.32<br>82.69<br>1.97<br>4.97<br>6.72<br>81.50<br>84.41<br>82.92<br>5.65<br>5.66<br>8.02<br>82.44<br>85.54<br>83.96<br>1.44<br>3.89<br>5.59<br>81.20<br>84.50<br>82.81<br>**5.91**<br>6.09<br>8.51<br>82.43<br>85.55<br>83.95<br>5.69<br>6.15<br>8.51<br>82.87<br>85.81<br>84.31|



















|1.0<br>RAG-Order 1<br>GraphRAG-Local-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Local-Order 2<br>0.6 Proportion<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Local-Order 1<br>RAG-Order 2<br>GraphRAG-Local-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||Gra|phRAG~~-~~Local~~-~~Order 2|phRAG~~-~~Local~~-~~Order 2|phRAG~~-~~Local~~-~~Order 2|phRAG~~-~~Local~~-~~Order 2|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||Gra|phRAG~~-~~Local~~-~~Order 2||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||Gra|phRAG~~-~~Local~~-~~Order 2||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||~~re~~|~~en~~|~~ivenes~~||~~ive~~|~~sit~~||


**(a) QMSum Local**



|1.0<br>RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Gloabl-Order 2<br>0.6 Proportion<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>RAG-Order 2<br>GraphRAG-Gloabl-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|~~re~~|~~e~~|~~si~~|~~enes~~|~~Di~~|~~ersit~~||


**(b) QMSum Global**



|1.0<br>RAG-Order 1<br>GraphRAG-Local-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Local-Order 2<br>0.6 Proportion<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Local-Order 1<br>RAG-Order 2<br>GraphRAG-Local-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||~~re~~|~~en~~|~~ivene~~|~~s~~<br>|~~ive~~|~~sit~~||


**(c) ODSum-story Local**



|1.0<br>RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Gloabl-Order 2<br>0.6 Proportion<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>RAG-Order 2<br>GraphRAG-Gloabl-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2||~~re~~|~~e~~|~~si~~|~~enes~~|~~Di~~|~~ersit~~||


**(d) ODSum-story Global**



**Figure 4: Comparison of LLM-as-a-Judge evaluations for RAG and GraphRAG. "Local" refers to the evaluation of RAG vs.**
**GraphRAG-Local, while "Global" refers to RAG vs. GraphRAG-Global.**



to balance detail fidelity, diversity, evaluation reliability, and system
cost when applying (Graph)RAG to query-based summarization.


**6** **Conclusion**


This work presents a unified benchmark evaluation of RAG and
GraphRAG across both question answering and query-based summarization, clarifying when explicit graph structures help, and
when they do not, under controlled settings. Our analyses reveal
strong task-dependent behaviors: RAG is consistently effective for
single-hop, detail-oriented queries that require precise evidence,
whereas GraphRAG is more advantageous for multi-hop, reasoningintensive QA and tends to produce more corpus-level, diverse summaries. Motivated by these findings, we study two hybrid strategies,



**Selection** and **Integration**, that combine the strengths of both
paradigms and improve QA performance. Beyond effectiveness,
we highlight practical challenges that limit current GraphRAG
systems, including incomplete or noisy graph construction, additional computation and storage overhead, and evaluation artifacts
such as position effects in LLM-as-a-Judge for summarization. Together, these observations point toward the next generation of RAG
systems: approaches that can construct and refine graphs reliably,
adapt retrieval and aggregation to query needs, and deliver stronger
reasoning benefits under realistic efficiency constraints.


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY



**References**


[1] Jiawei Chen, Hongyu Lin, Xianpei Han, and Le Sun. 2024. Benchmarking large
language models in retrieval-augmented generation. In _Proceedings of the AAAI_
_Conference on Artificial Intelligence_, Vol. 38. 17754–17762.

[2] Jialin Dong, Bahare Fatemi, Bryan Perozzi, Lin F Yang, and Anton Tsitsulin. 2024.
Don’t Forget to Connect! Improving RAG with Graph-based Reranking. _arXiv_
_preprint arXiv:2405.18414_ (2024).

[3] Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia,
Jingjing Xu, Zhiyong Wu, Tianyu Liu, et al . 2022. A survey on in-context learning.
_arXiv preprint arXiv:2301.00234_ (2022).

[4] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan,
et al. 2024. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ (2024).

[5] Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva
Mody, Steven Truitt, and Jonathan Larson. 2024. From local to global: A graph
rag approach to query-focused summarization. _arXiv preprint arXiv:2404.16130_
(2024).

[6] Shahul Es, Jithin James, Luis Espinosa-Anke, and Steven Schockaert. 2023. Ragas: Automated evaluation of retrieval augmented generation. _arXiv preprint_
_arXiv:2309.15217_ (2023).

[7] Wenqi Fan, Yujuan Ding, Liangbo Ning, Shijie Wang, Hengyun Li, Dawei Yin,
Tat-Seng Chua, and Qing Li. 2024. A survey on rag meeting llms: Towards
retrieval-augmented large language models. In _Proceedings of the 30th ACM_
_SIGKDD Conference on Knowledge Discovery and Data Mining_ . 6491–6501.

[8] Paulo Finardi, Leonardo Avila, Rodrigo Castaldoni, Pedro Gengo, Celio Larcher,
Marcos Piau, Pablo Costa, and Vinicius Caridá. 2024. The Chronicles of RAG: The
Retriever, the Chunk and the Generator. _arXiv preprint arXiv:2401.07883_ (2024).

[9] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai,
Jiawei Sun, and Haofen Wang. 2023. Retrieval-augmented generation for large
language models: A survey. _arXiv preprint arXiv:2312.10997_ (2023).

[10] Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. 2025.
From rag to memory: Non-parametric continual learning for large language
models. _arXiv preprint arXiv:2502.14802_ (2025).

[11] Haoyu Han, Yu Wang, Harry Shomer, Kai Guo, Jiayuan Ding, Yongjia Lei, Mahantesh Halappanavar, Ryan A Rossi, Subhabrata Mukherjee, Xianfeng Tang, et al .
2024. Retrieval-augmented generation with graphs (graphrag). _arXiv preprint_
_arXiv:2501.00309_ (2024).

[12] Haoyu Han, Yaochen Xie, Hui Liu, Xianfeng Tang, Sreyashi Nag, William Headden, Yang Li, Chen Luo, Shuiwang Ji, Qi He, et al . 2025. Reasoning with Graphs:
Structuring Implicit Knowledge to Enhance LLMs Reasoning. _arXiv preprint_
_arXiv:2501.07845_ (2025).

[13] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian
Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, et al . 2023. A
survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. _arXiv preprint arXiv:2311.05232_ (2023).

[14] Gautier Izacard, Patrick Lewis, Maria Lomeli, Lucas Hosseini, Fabio Petroni,
Timo Schick, Jane Dwivedi-Yu, Armand Joulin, Sebastian Riedel, and Edouard
Grave. 2023. Atlas: Few-shot learning with retrieval augmented language models.
_Journal of Machine Learning Research_ 24, 251 (2023), 1–43.

[15] Zhengbao Jiang, Frank F Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu,
Yiming Yang, Jamie Callan, and Graham Neubig. 2023. Active retrieval augmented
generation. _arXiv preprint arXiv:2305.06983_ (2023).

[16] Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su.
2024. Hipporag: Neurobiologically inspired long-term memory for large language
models. _Advances in Neural Information Processing Systems_ 37 (2024), 59532–
59569.

[17] Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey
Edunov, Danqi Chen, and Wen-tau Yih. 2020. Dense passage retrieval for opendomain question answering. _arXiv preprint arXiv:2004.04906_ (2020).

[18] Jiho Kim, Sungjin Park, Yeonsu Kwon, Yohan Jo, James Thorne, and Edward
Choi. 2023. FactKG: Fact verification via reasoning on knowledge graphs. _arXiv_
_preprint arXiv:2305.06590_ (2023).

[19] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur
Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton
Lee, et al . 2019. Natural questions: a benchmark for question answering research.
_Transactions of the Association for Computational Linguistics_ 7 (2019), 453–466.

[20] Xinze Li, Zhenghao Liu, Chenyan Xiong, Shi Yu, Yu Gu, Zhiyuan Liu, and Ge Yu.
2023. Structure-Aware Language Model Pretraining Improves Dense Retrieval
on Structured Data. _arXiv preprint arXiv:2305.19912_ (2023).

[21] Yongqi Li, Wenjie Li, and Liqiang Nie. 2022. Dynamic graph reasoning for conversational open-domain question answering. _ACM Transactions on Information_
_Systems (TOIS)_ 40, 4 (2022), 1–24.

[22] Chin-Yew Lin. 2004. Rouge: A package for automatic evaluation of summaries.
In _Text summarization branches out_ . 74–81.

[23] Fangru Lin, Emanuele La Malfa, Valentin Hofmann, Elle Michelle Yang, Anthony
Cohn, and Janet B Pierrehumbert. 2024. Graph-enhanced Large Language Models
in Asynchronous Plan Reasoning. _arXiv preprint arXiv:2402.02805_ (2024).




[24] Jerry Liu. 2022. _LlamaIndex_ [. doi:10.5281/zenodo.1234](https://doi.org/10.5281/zenodo.1234)

[25] Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, and Nan Duan. 2023.
Query rewriting for retrieval-augmented large language models. _arXiv preprint_
_arXiv:2305.14283_ (2023).

[26] Yao Ma and Jiliang Tang. 2021. _Deep learning on graphs_ . Cambridge University
Press.

[27] Fatma Miladi, Valéry Psyché, and Daniel Lemire. 2024. Leveraging GPT-4 for
Accuracy in Education: A Comparative Study on Retrieval-Augmented Generation in MOOCs. In _International Conference on Artificial Intelligence in Education_ .
Springer, 427–434.

[28] Zach Nussbaum, John X Morris, Brandon Duderstadt, and Andriy Mulyar. 2024.
Nomic embed: Training a reproducible long context text embedder. _arXiv preprint_
_arXiv:2402.01613_ (2024).

[29] Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao Hong, Yan
Zhang, and Siliang Tang. 2024. Graph retrieval-augmented generation: A survey.
_arXiv preprint arXiv:2408.08921_ (2024).

[30] Ori Ram, Yoav Levine, Itay Dalmedigos, Dor Muhlgay, Amnon Shashua, Kevin
Leyton-Brown, and Yoav Shoham. 2023. In-context retrieval-augmented language
models. _Transactions of the Association for Computational Linguistics_ 11 (2023),
1316–1331.

[31] Keshav Santhanam, Omar Khattab, Jon Saad-Falcon, Christopher Potts, and Matei
Zaharia. 2021. Colbertv2: Effective and efficient retrieval via lightweight late
interaction. _arXiv preprint arXiv:2112.01488_ (2021).

[32] Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and
Christopher D Manning. 2024. Raptor: Recursive abstractive processing for
tree-organized retrieval. In _The Twelfth International Conference on Learning_
_Representations_ .

[33] Lin Shi, Chiyu Ma, Wenhua Liang, Weicheng Ma, and Soroush Vosoughi. 2024.
Judging the judges: A systematic investigation of position bias in pairwise comparative assessments by llms. _arXiv preprint arXiv:2406.07791_ (2024).

[34] Yixuan Tang and Yi Yang. 2024. Multihop-rag: Benchmarking retrievalaugmented generation for multi-hop queries. _arXiv preprint arXiv:2401.15391_
(2024).

[35] Yijun Tian, Huan Song, Zichen Wang, Haozhu Wang, Ziqing Hu, Fang Wang,
Nitesh V Chawla, and Panpan Xu. 2024. Graph neural prompting with large
language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_,
Vol. 38. 19080–19088.

[36] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal.
2022. Interleaving retrieval with chain-of-thought reasoning for knowledgeintensive multi-step questions. _arXiv preprint arXiv:2212.10509_ (2022).

[37] Alex Wang, Richard Yuanzhe Pang, Angelica Chen, Jason Phang, and Samuel R
Bowman. 2022. Squality: Building a long-document summarization dataset the
hard way. _arXiv preprint arXiv:2205.11465_ (2022).

[38] Cunxiang Wang, Ruoxi Ning, Boqi Pan, Tonghui Wu, Qipeng Guo, Cheng Deng,
Guangsheng Bao, Qian Wang, and Yue Zhang. 2024. Novelqa: A benchmark for
long-range novel question answering. _arXiv preprint arXiv:2403.12766_ (2024).

[39] Ziqi Wang, Hanlin Zhang, Xiner Li, Kuan-Hao Huang, Chi Han, Shuiwang Ji,
Sham M Kakade, Hao Peng, and Heng Ji. 2024. Eliminating position bias of
language models: A mechanistic approach. _arXiv preprint arXiv:2407.01100_ (2024).

[40] Jerry Wei, Jason Wei, Yi Tay, Dustin Tran, Albert Webson, Yifeng Lu, Xinyun
Chen, Hanxiao Liu, Da Huang, Denny Zhou, et al . 2023. Larger language models
do in-context learning differently. _arXiv preprint arXiv:2303.03846_ (2023).

[41] Nirmalie Wiratunga, Ramitha Abeyratne, Lasal Jayawardena, Kyle Martin, Stewart Massie, Ikechukwu Nkisi-Orji, Ruvan Weerasinghe, Anne Liret, and Bruno
Fleisch. 2024. CBR-RAG: case-based reasoning for retrieval augmented generation in LLMs for legal question answering. In _International Conference on_
_Case-Based Reasoning_ . Springer, 445–460.

[42] Yaozu Wu, Yankai Chen, Zhishuai Yin, Weiping Ding, and Irwin King. 2023.
A survey on graph embedding techniques for biomedical data: Methods and
applications. _Information Fusion_ 100 (2023), 101909.

[43] Zonghan Wu, Shirui Pan, Fengwen Chen, Guodong Long, Chengqi Zhang, and
S Yu Philip. 2020. A comprehensive survey on graph neural networks. _IEEE_
_transactions on neural networks and learning systems_ 32, 1 (2020), 4–24.

[44] Feng Xia, Ke Sun, Shuo Yu, Abdul Aziz, Liangtian Wan, Shirui Pan, and Huan
Liu. 2021. Graph learning: A survey. _IEEE Transactions on Artificial Intelligence_ 2,
2 (2021), 109–127.

[45] Shitao Xiao, Zheng Liu, Peitian Zhang, and Niklas Muennighoff. 2023.
C-Pack: Packaged Resources To Advance General Chinese Embedding.
[arXiv:2309.07597 [cs.CL]](https://arxiv.org/abs/2309.07597)

[46] Fangyuan Xu, Weijia Shi, and Eunsol Choi. 2023. Recomp: Improving retrievalaugmented lms with compression and selective augmentation. _arXiv preprint_
_arXiv:2310.04408_ (2023).

[47] Ran Xu, Wenqi Shi, Yue Yu, Yuchen Zhuang, Bowen Jin, May D Wang, Joyce C Ho,
and Carl Yang. 2024. Ram-ehr: Retrieval augmentation meets clinical predictions
on electronic health records. _arXiv preprint arXiv:2403.00815_ (2024).

[48] Shi-Qi Yan, Jia-Chen Gu, Yun Zhu, and Zhen-Hua Ling. 2024. Corrective retrieval
augmented generation. _arXiv preprint arXiv:2401.15884_ (2024).


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.


[49] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan
Salakhutdinov, and Christopher D Manning. 2018. HotpotQA: A dataset for diverse, explainable multi-hop question answering. _arXiv preprint arXiv:1809.09600_
(2018).

[50] Michihiro Yasunaga, Hongyu Ren, Antoine Bosselut, Percy Liang, and Jure
Leskovec. 2021. QA-GNN: Reasoning with language models and knowledge
graphs for question answering. _arXiv preprint arXiv:2104.06378_ (2021).

[51] Hao Yu, Aoran Gan, Kai Zhang, Shiwei Tong, Qi Liu, and Zhaofeng Liu. 2024.
Evaluation of retrieval-augmented generation: A survey. In _CCF Conference on_
_Big Data_ . Springer, 102–120.

[52] Zichun Yu, Chenyan Xiong, Shi Yu, and Zhiyuan Liu. 2023. Augmentationadapted retriever improves generalization of language models as generic plug-in.
_arXiv preprint arXiv:2305.17331_ (2023).

[53] Boyu Zhang, Hongyang Yang, Tianyu Zhou, Muhammad Ali Babar, and XiaoYang Liu. 2023. Enhancing financial sentiment analysis via retrieval augmented
large language models. In _Proceedings of the fourth ACM international conference_
_on AI in finance_ . 349–356.

[54] Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q Weinberger, and Yoav
Artzi. 2019. Bertscore: Evaluating text generation with bert. _arXiv preprint_
_arXiv:1904.09675_ (2019).

[55] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou,
Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al . 2023. A survey
of large language models. _arXiv preprint arXiv:2303.18223_ (2023).

[56] Huaixiu Steven Zheng, Swaroop Mishra, Xinyun Chen, Heng-Tze Cheng, Ed H
Chi, Quoc V Le, and Denny Zhou. 2023. Take a step back: Evoking reasoning via
abstraction in large language models. _arXiv preprint arXiv:2310.06117_ (2023).

[57] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu,
Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al . 2023. Judging
llm-as-a-judge with mt-bench and chatbot arena. _Advances in Neural Information_
_Processing Systems_ 36 (2023), 46595–46623.

[58] Ming Zhong, Da Yin, Tao Yu, Ahmad Zaidi, Mutethia Mutuma, Rahul Jha,
Ahmed Hassan Awadallah, Asli Celikyilmaz, Yang Liu, Xipeng Qiu, et al . 2021.
QMSum: A new benchmark for query-based multi-domain meeting summarization. _arXiv preprint arXiv:2104.05938_ (2021).

[59] Yijie Zhou, Kejian Shi, Wencai Zhang, Yixin Liu, Yilun Zhao, and Arman Cohan.
2023. Odsum: New benchmarks for open domain multi-document summarization.
_arXiv preprint arXiv:2309.08960_ (2023).


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


**Appendix**


**A Dataset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .** **12**


A.1 Question Answering . . . . . . . . . . . . . 12


A.2 Query-based Summarization . . . . . . . . . . . 12


**B** **More results on QA datasets . . . . . . . . . . . . . . . .** **12**


B.1 Results with LLaMA 3.1-70B on NQ and Hotpot datasets . 12


B.2 Results with LLaMA 3.1-70B on MultiHop-RAG dataset . . 12


B.3 Results with LLaMA 3.1-8B on NovelQA . . . . . . . 12


B.4 Results with LLaMA 3.1-70B on NovelQA . . . . . . 12


**C Retrieval accuracy of different methods . . . . . . . .** **12**


**D Case studies for the question answering task. . . . .** **14**


**E** **Iterative Retrieval. . . . . . . . . . . . . . . . . . . . . . .** **14**


E.1 Iterative Retrieval for QA . . . . . . . . . . . . 15


E.2 Iterative Retrieval for Query-based Summarization . . . 15


**F** **Reranking. . . . . . . . . . . . . . . . . . . . . . . . . . . .** **15**


F.1 Reranking for QA . . . . . . . . . . . . . . 15


F.2 Reranking for Query-based Summarization . . . . . . 15


**G RAG vs. GraphRAG Selection . . . . . . . . . . . . . . .** **15**


**H RAG and GraphRAG Integration . . . . . . . . . . . . .** **15**


**I** **Query-based Summarization Results with Llama**

**3.1-70B model. . . . . . . . . . . . . . . . . . . . . . . . . . . .** **16**


**J** **The LLM-as-a-Judge Prompt . . . . . . . . . . . . . . .** **16**


**K The LLM-as-a-Judge Results on more datasets . . . .** **17**


**L** **Graph Construction with different LLMs . . . . . . .** **18**


**M Computation and Storage Analysis . . . . . . . . . . .** **19**


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.



**A** **Dataset**


In this section, we introduce the used datasets in the question
answering tasks and query-based summarization tasks.


**A.1** **Question Answering**


In the QA tasks, we use the following four widely used datasets:


- **Natural Questions (NQ)** [ 19 ]: The NQ dataset is a widely used
benchmark for evaluating open-domain question answering systems. Introduced by Google, it consists of real user queries from
Google Search with corresponding answers extracted from the
Wikipedia. Since it primarily contains single-hop questions, we
use NQ as the representative dataset for single-hop QA. We treat
NQ as a single-document QA task, where multiple questions are
associated with each document. Accordingly, we build a separate
RAG system for each document in the dataset.

- **Hotpot** [ 49 ]: HotpotQA is a widely used multi-hop question
dataset that provides 10 paragraphs per question. The dataset
includes varying difficulty levels, with easier questions often
solvable by LLMs. To ensure a more challenging evaluation, we
randomly selected 1,000 hard bridging questions from the development set of HotpotQA. Additionally, we treat HotpotQA
as a multi-document QA task and build a single RAG system to
handle all questions.

- **MultiHop-RAG** [ 34 ]: MultiHop-RAG is a QA dataset designed
to evaluate retrieval and reasoning across multiple documents
with metadata in RAG pipelines. Constructed from English news
articles, it contains 2,556 queries, with supporting evidence distributed across 2 to 4 documents. The dataset includes four query
types: Inference queries, which synthesize claims about a bridge
entity to identify it; Comparison queries, which compare similarities or differences and typically yield "yes" or "no" answers;
Temporal queries, which examine event ordering with answers
like "before" or "after"; and Null queries, where no answer can be
derived from the retrieved documents. It is also a multi-document

QA task.

- **NovelQA** [ 38 ]: NovelQA is a benchmark designed to evaluate
the long-text understanding and retrieval ability of LLMs using manually curated questions about English novels exceeding
50,000 words. The dataset includes queries that focus on minor
details or require cross-chapter reasoning, making them inherently challenging for LLMs. It covers various query types such
as details, multi-hop, single-hop, character, meaning, plot, relation, setting, span, and times. Key challenges highlighted by
NovelQA include grasping abstract meanings (meaning questions), understanding nuanced relationships (relation questions),
and tracking temporal sequences and spatial extents (span and
time questions), emphasizing the difficulty of maintaining and
applying contextual information across long narratives. We use
it for single-document QA task.


**A.2** **Query-based Summarization**


In the Query-based Summarization tasks, we adopt the following
four widely used datasets:


- **SQuALITY** [ 37 ]: SQuALITY (Summary-format QUestion Answering with Long Input Texts) is a question-focused, longdocument, multi-reference summarization dataset. It consists



of short stories from Project Gutenberg, each ranging from 4,000
to 6,000 words. Each story is paired with five questions, and each
question has four reference summaries written by Upwork writers and NYU undergraduates. SQuALITY is designed as a singledocument summarization task, making it a valuable benchmark
for evaluating summarization models on long-form content.

- **QMSum** [ 58 ]: QMSum is a human-annotated benchmark for
query-based, multi-domain meeting summarization, containing
1,808 query-summary pairs from 232 meetings across multiple
domains. We use QMSum as a single-document summarization
task in our evaluation.

- **ODSum** [ 59 ]: The ODSum dataset is designed to evaluate modern
summarization models in multi-document contexts and consists

of two subsets: ODSum-story and ODSum-meeting. ODSumstory is derived from the SQuALITY dataset, while ODSummeeting is constructed from QMSum. We use both ODSum-story
and ODSum-meeting for the multi-document summarization task
in our evaluation.


**B** **More results on QA datasets**


In this section, we present additional results on the NovelQA dataset
that were omitted from the main paper due to space constraints.
Results are organized by model size and method for clarity.


**B.1** **Results with LLaMA 3.1-70B on NQ and**
**Hotpot datasets**


We report the performance of RAG and GraphRAG methods on NQ
and Hotpot datasets with LLaMA 3.1-70B in Table 8.


**B.2** **Results with LLaMA 3.1-70B on**

**MultiHop-RAG dataset**


We report the performance of RAG and GraphRAG methods on
MultiHop-RAG dataset with LLaMA 3.1-70B in Table 9.


**B.3** **Results with LLaMA 3.1-8B on NovelQA**


We report the performance of KG-GraphRAG (Triplets) with LLaMA
3.1-8B in Table 10.


**B.4** **Results with LLaMA 3.1-70B on NovelQA**


Table 11 reports the RAG baseline with LLaMA 3.1-70B. Table 12
presents KG-GraphRAG (Triplets), Table 13 presents KG-GraphRAG
(Triplets+Text), Table 14 presents Community-GraphRAG (Local),
and Table 15 presents Community-GraphRAG (Global), all using
LLaMA 3.1-70B.


**C** **Retrieval accuracy of different methods**


In this section, we compare the retrieval effectiveness of different methods. Since retrieval does not have explicit ground-truth
supervision at the chunk level, we measure _retrieval accuracy_ as
the proportion of examples for which the ground-truth answer
string appears in the retrieved context. We report results on the
**HotpotQA** and **NQ** datasets.
As shown in the Table 16, KG-GraphRAG (Triplets only) achieves
relatively low retrieval accuracy, particularly on NQ. This is primarily due to the incompleteness of the constructed knowledge


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


**Table 8: Performance comparison (%) on NQ and Hotpot datasets using Llama 3.1-70B.**

|NQ Hotpot<br>Method<br>P R F1 P R F1|NQ|Hotpot|
|---|---|---|
|**Method**<br>**NQ**<br>**Hotpot**<br>P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1|P<br>R<br>F1|
|RAG<br>RaptorRAG<br>KG-GraphRAG (Triplets only)<br>KG-GraphRAG (Triplets+Text)<br>Community-GraphRAG (Local)<br>Community-GraphRAG (Global)<br>HippoRAG2|**74.55**<br>**67.82**<br>**68.18**<br>66.32<br>60.74<br>60.59<br>37.84<br>31.22<br>28.50<br>60.91<br>52.75<br>53.88<br>71.27<br>65.46<br>65.44<br>61.15<br>55.52<br>55.05<br>69.69<br>64.32<br>64.03|66.34<br>63.99<br>63.88<br>66.44<br>63.69<br>63.83<br>32.59<br>30.63<br>30.73<br>51.44<br>48.99<br>48.75<br>67.20<br>**64.89**<br>64.60<br>48.33<br>48.56<br>46.99<br>**68.05**<br>64.59<br>**64.93**|



**Table 9: Performance comparison (%) on the MultiHop-RAG dataset using Llama 3.1-70B.**

|Method|Inference Comparison Null Temporal Overall|
|---|---|
|RAG<br>RaptorRAG<br>KG-GraphRAG (Triplets only)<br>KG-GraphRAG (Triplets+Text)<br>Community-GraphRAG (Local)<br>Community-GraphRAG (Global)<br>HippoRAG2|**94.85**<br>56.31<br>91.36<br>25.73<br>65.77<br>92.40<br>57.24<br>**95.02**<br>43.22<br>69.72<br>76.96<br>32.36<br>94.35<br>19.55<br>50.98<br>85.91<br>35.98<br>86.38<br>21.61<br>54.58<br>92.03<br>60.16<br>88.70<br>49.06<br>**71.17**<br>89.09<br>**66.00**<br>13.95<br>**59.18**<br>65.69<br>93.01<br>58.76<br>90.03<br>43.40<br>69.87|



**Table 10: The performance of KG-GraphRAG (Triplets) with Llama 3.1-8B model on NovelQA dataset.**

|KG-GraphRAG(Triplet)|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|31.25<br>17.65<br>41.67<br>50.56<br>38.46<br>64<br>26.47<br>32.89<br>35.53<br>45.71<br>30.54<br>62.5<br>27.84<br>-<br>-<br>33.75<br>31.43<br>24.72<br>35.71<br>17.86<br>27.03<br>-<br>-<br>27.37<br>33.7<br>29.81<br>32.63<br>44<br>28.57<br>64<br>26.47<br>31.88|



**Table 11: The performance of RAG with Llama 3.1-70B model on NovelQA dataset.**

|RAG|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|64.58<br>82.35<br>77.78<br>69.66<br>84.62<br>36<br>36.63<br>48.5<br>70.39<br>70<br>76.57<br>75<br>83.51<br>-<br>-<br>75.27<br>60<br>51.12<br>76.79<br>67.86<br>83.78<br>-<br>-<br>61.25<br>66.67<br>58.11<br>76.74<br>69.6<br>83.67<br>36<br>36.63<br>61.42|



**Table 12: The performance of KG-GraphRAG (Triplets) with Llama 3.1-70B model on NovelQA dataset.**


|KG-GraphRAG (Triplets)|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|50<br>76.47<br>75<br>43.82<br>76.92<br>24<br>22.46<br>33.72<br>52.63<br>62.86<br>55.23<br>12.5<br>50.52<br>-<br>-<br>54.06<br>35.71<br>26.97<br>39.29<br>53.57<br>37.84<br>-<br>-<br>33.6<br>47.78<br>39.62<br>54.68<br>44<br>49.66<br>24<br>22.46<br>41.18|



graphs—only 65.8% of answer entities exist in the HotpotQA KG,
and 65.5% in the NQ KG. In contrast, Community-GraphRAG, which
leverages community-level summarization, demonstrates significantly better retrieval performance. These findings highlight several
potential directions for improvement:



(1) Enhancing KG construction to increase entity and relation cov
erage.
(2) Combining structured graph information with raw text to improve retrieval robustness and completeness.


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.


**Table 13: The performance of KG-GraphRAG (Triplets+Text) with Llama 3.1-70B model on NovelQA dataset.**

|KG-GraphRAG (Triplets+Text)|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|56.25<br>58.82<br>63.89<br>51.69<br>84.62<br>24<br>21.39<br>33.72<br>51.97<br>61.43<br>55.65<br>50<br>50.52<br>-<br>-<br>54.42<br>34.29<br>25.28<br>41.07<br>50<br>37.84<br>-<br>-<br>32.52<br>48.15<br>36.98<br>54.08<br>51.2<br>50.34<br>24<br>21.39<br>41.05|



**Table 14: The performance of Community-GraphRAG (Local) with Llama 3.1-70B model on NovelQA dataset.**

|Community-GraphRAG (Local)|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|77.08<br>70.59<br>63.89<br>77.53<br>92.31<br>28<br>32.35<br>46.68<br>68.42<br>71.43<br>74.9<br>62.5<br>74.23<br>-<br>-<br>72.44<br>55.71<br>37.08<br>69.64<br>64.29<br>75.68<br>-<br>-<br>51.49<br>66.67<br>48.3<br>72.81<br>73.6<br>76.19<br>28<br>32.35<br>57.32|



**Table 15: The performance of Community-GraphRAG (Global) with Llama 3.1-70B model on NovelQA dataset.**


|Community-GraphRAG (Global)|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|47.92<br>58.82<br>55.56<br>57.3<br>61.54<br>16<br>35.83<br>41.53<br>42.76<br>42.86<br>54.39<br>25<br>40.21<br>-<br>-<br>47<br>24.29<br>22.47<br>32.14<br>50<br>35.14<br>-<br>-<br>27.64<br>38.89<br>30.19<br>50.76<br>53.6<br>40.82<br>16<br>35.83<br>40.21|



**Table 16: Retrieval accuracy (%) of different methods on Hot-**
**pot and NQ datasets**

|Method|Hotpot NQ|
|---|---|
|RAG<br>KG-GraphRAG (Triplets only)<br>KG-GraphRAG (Triplets+Text)<br>Community-GraphRAG (Local)<br>Community-GraphRAG (Global)|88.60<br>86.70<br>39.20<br>32.18<br>69.80<br>61.50<br>67.53<br>42.20<br>88.60<br>83.30|



**D** **Case studies for the question answering task**


In this section, we present examples where RAG fails but GraphRAG
succeeds. In Case 1 (Figure 5), RAG fails because it does not retrieve
all the relevant chunks required for answering the multi-hop reasoning question. KG-RAG also fails due to missing information during
knowledge graph construction. However, Community-GraphRAG
is able to answer correctly by leveraging community-level summarizations that capture the necessary context. In Case 2 (Figure 6),
both KG-GraphRAG and Community-GraphRAG succeed because
they capture the reasoning chain—either through explicit graph
paths or through summarization within the same community. In
contrast, RAG fails due to insufficient retrieved information.


**E** **Iterative Retrieval**


Iterative retrieval [ 31, 36 ] is a widely adopted technique for enabling RAG to handle multi-step reasoning tasks. Specifically, at
each iteration, new queries are generated based on the retrieval
results from the previous step. The system then performs another
round of retrieval using the updated queries, repeating the process
until the problem is resolved or a predefined maximum number of



**Figure 5: Case 1 from Hotpot dataset.**


iterations is reached. To further compare the performance of RAG
and GraphRAG, we apply the iterative retrieval method, specifically
IRCoT [36], to all approaches.


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY





**Figure 6: Case 2 from Hotpot dataset.**


**E.1** **Iterative Retrieval for QA**


We evaluate iterative retrieval on the **NQ** and **MultiHop-RAG**
datasets, representing single-hop and multi-hop QA scenarios, respectively. We compare **RAG**, **RaptorRAG**, **Community-GraphRAG**
**(Local)**, and **HippoRAG2** . The results are presented in Table 18.
Overall, iterative retrieval consistently improves the performance
of both RAG and GraphRAG compared to single-step retrieval.
One notable exception is Community-GraphRAG (Local) on the
MultiHop-RAG dataset: the accuracy on NULL queries (which should
be answered as “insufficient information”) drops from 80.07 to 50.50,
even though accuracy on other query types improves. This suggests
that iterative retrieval can encourage over-generation, making the
model more likely to produce an answer rather than abstain when
evidence is insufficient.
Importantly, the relative strengths of the two paradigms remain
unchanged: RAG continues to perform better on single-hop and
detail-oriented questions, while GraphRAG achieves higher accuracy on multi-hop and reasoning-intensive queries.


**E.2** **Iterative Retrieval for Query-based**
**Summarization**


We evaluate iterative retrieval on the **ODSum-story** and **ODSum-**
**meeting** datasets. We compare **RAG**, **RaptorRAG**, **Community-**
**GraphRAG (Local)**, and **HippoRAG2** . The results are presented
in Table 17.

Overall, iterative retrieval improves query-based summarization performance across methods, with particularly clear gains
in BERTScore. This suggests that iterative refinement helps the
model retrieve semantically relevant evidence and better integrate
information across steps, leading to summaries that are closer to



reference summaries in meaning even when lexical overlap even
drops.


**F** **Reranking**


In this section, we study _reranking_ as an inference-time enhancement for both QA and query-based summarization. Concretely, we
first retrieve 20 candidates and then apply the widely used reranker
model, i.e., BAAI/bge-reranker-large, to score candidates with
respect to the query. Finally, we select the top-10 ranked candidates
(under the same retrieval token budget as the vanilla setting) and
pass them to the generator.


**F.1** **Reranking for QA**


We evaluate reranking on the **NQ** and **MultiHop-RAG** datasets,
representing single-hop and multi-hop QA scenarios, respectively.
We compare **RAG**, **RaptorRAG**, **Community-GraphRAG (Lo-**
**cal)**, and **HippoRAG2** . The results are presented in Table 18.
Overall, reranking consistently improves QA performance for
all methods across both datasets, indicating that better evidence selection provides gains beyond the underlying retrieval architecture.
One notable exception is the NULL query type on MultiHop-RAG,
where reranking can reduce abstention accuracy (i.e., predicting
“insufficient information”), suggesting that stronger evidence selection may also encourage over-generation when the query lacks
sufficient support.


**F.2** **Reranking for Query-based Summarization**


We evaluate reranking on the **ODSum-story** and **ODSum-meeting**
datasets. We compare **RAG**, **RaptorRAG**, **Community-GraphRAG**
**(Local)**, and **HippoRAG2** . The results are presented in Table 19.
Overall, reranking yields only marginal changes on query-based
summarization, with performance remaining comparable to the
vanilla setting across methods. This suggests that, unlike QA, summarization quality is less sensitive to fine-grained reordering of
retrieved evidence under a fixed token budget.


**G** **RAG vs. GraphRAG Selection**


We classify QA queries into Fact-based and Reasoning-based queries.
Fact-based queries are processed using RAG, while Reasoning-based
queries are handled by GraphRAG. The Query Classification prompt
is shown in Figure 7.


**H** **RAG and GraphRAG Integration**


In this section, we explore the effect of integrating RAG and GraphRAG
for the question answering task. Specifically, we concatenate the retrieved results from both RAG and GraphRAG before passing them
to the LLM. The results are presented in Table 20, Table 21, Table 22,
Table 23, and Table 24, respectively. For most cases, the integration
of RAG and GraphRAG improves performance. However, we observe a performance drop when integrating with Llama 3.1–8B on
the MultiHop-RAG dataset. This degradation is primarily attributed
to a significant decline on Null queries—those requiring the model
to respond with “Insufficient Information.” By concatenating the
retrieved results from both RAG and GraphRAG, the input length
increases considerably, making the 8B model more susceptible to


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.


**Table 17: The performance of query-based multiple document summarization task in iterative retrieval using Llama3.1-8B.**

|ODSum-story ODSum-meeting<br>Method<br>ROUGE-2 BERTScore ROUGE-2 BERTScore<br>P R F1 P R F1 P R F1 P R F1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|RAG<br>RaptorRAG<br>Community-GraphRAG (Local)<br>HippoRAG2|15.33<br>8.69<br>9.89<br>14.79<br>8.53<br>9.68<br>14.00<br>7.74<br>8.80<br>**15.44**<br>**8.56**<br>**9.87**|83.80<br>85.71<br>84.52<br>83.87<br>85.78<br>84.59<br>83.43<br>85.24<br>84.10<br>83.76<br>**85.74**<br>**84.51**|16.22<br>6.32<br>8.75<br>14.75<br>6.10<br>8.29<br>15.71<br>5.79<br>8.12<br>15.50<br>5.98<br>8.32|83.03<br>85.87<br>84.42<br>82.59<br>85.53<br>84.03<br>82.56<br>85.64<br>84.07<br>82.46<br>85.57<br>83.98|



**Table 18: QA results under different inference strategies on NQ and MultiHop-RAG using Llama3.1-8B.**






|NQ MultiHop-RAG<br>Method Inference<br>Precision Recall F1 Inference Comparison Null Temporal Overall|Col2|Col3|Col4|
|---|---|---|---|
|RAG|Vanilla<br>+ Rerank<br>+ IRCoT|71.70<br>63.93<br>64.78<br>72.89<br>66.15<br>66.49<br>71.92<br>65.47<br>65.72|92.16<br>57.59<br>96.01<br>30.70<br>67.02<br>92.89<br>57.01<br>83.72<br>49.57<br>69.91<br>93.87<br>57.59<br>71.76<br>53.00<br>69.80|
|RaptorRAG|Vanilla<br>+ Rerank<br>+ IRCoT|66.06<br>59.56<br>60.04<br>69.14<br>62.61<br>63.04<br>68.59<br>61.82<br>62.39|91.91<br>55.26<br>90.03<br>45.28<br>68.78<br>93.38<br>60.05<br>87.38<br>48.20<br>71.21<br>94.85<br>57.83<br>85.38<br>46.83<br>70.38|
|Community-GraphRAG (Local)|Vanilla<br>+ Rerank<br>+ IRCoT|69.48<br>62.54<br>63.01<br>70.75<br>63.93<br>64.45<br>70.76<br>63.20<br>63.77|86.89<br>60.63<br>80.07<br>50.60<br>69.01<br>87.50<br>62.85<br>72.76<br>53.52<br>69.76<br>90.69<br>62.62<br>50.50<br>52.32<br>67.80|
|HippoRAG2|Vanilla<br>+ Rerank<br>+ IRCoT|67.25<br>60.42<br>61.03<br>70.57<br>64.20<br>64.50<br>71.04<br>63.77<br>64.54|91.54<br>58.41<br>85.71<br>49.91<br>70.27<br>93.87<br>60.51<br>82.39<br>54.03<br>72.26<br>94.36<br>61.68<br>73.09<br>51.29<br>71.09|



**Table 19: The performance of query-based multiple document summarization task in reranking using Llama3.1-8B.**








|ODSum-story ODSum-meeting<br>Method<br>ROUGE-2 BERTScore ROUGE-2 BERTScore<br>P R F1 P R F1 P R F1 P R F1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|RAG<br>RaptorRAG<br>Community-GraphRAG (Local)<br>HippoRAG2|15.54<br>**8.80**<br>**10.01**<br>15.15<br>8.51<br>9.74<br>13.95<br>7.25<br>8.49<br>**15.65**<br>8.53<br>9.90|**83.86**<br>85.81<br>84.59<br>83.85<br>**85.84**<br>**84.61**<br>83.16<br>85.11<br>83.91<br>83.84<br>85.80<br>84.58|**16.08**<br>**6.38**<br>**8.83**<br>14.76<br>6.18<br>8.40<br>15.51<br>5.63<br>7.96<br>15.70<br>6.10<br>8.48|**83.06**<br>**85.90**<br>**84.45**<br>82.75<br>85.63<br>84.16<br>82.52<br>85.54<br>84.00<br>82.55<br>85.66<br>84.07|



hallucination and the generation of incorrect answers. This vulnerability is more pronounced in the 8B model due to its limited
capacity, whereas the 70B model demonstrates greater robustness
to longer contexts and handles ambiguous information more conservatively. In contrast, for other query types such as Comparison
and Temporal, the integration strategy yields notable gains on both
model sizes.

For the query-based summarization task, we observed that the
Integration strategy generally performs comparably to RAG, but
not significantly better. This is because the evaluation is based
on human-written ground-truth summaries, which tend to focus
on detailed and faithful representations of the original text. RAG
directly retrieves text segments that often match these detailed
references more closely, as shown in Figure 4 of our paper. In
contrast, GraphRAG primarily retrieves structured information
(e.g., entities and relations), which omit finer details needed to
align with ground-truth summaries. As a result, while Integration



combines complementary views, the added structured content from
GraphRAG does not consistently enhance alignment with detailed
ground-truth summaries, leading to comparable or slightly lower

scores.


**I** **Query-based Summarization Results with**
**Llama 3.1-70B model**


In this section, we present the results for Query-based Summarization tasks using the LLaMA 3.1-70B model. The results for
single-document summarization are shown in Table 25, while the
results for multi-document summarization are provided in Table 26.


**J** **The LLM-as-a-Judge Prompt**


The LLM-as-a-Judge prompt can be found in Figure 8.


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY


**Table 20: Performance comparison of RAG, GraphRAG, and their integration on NQ and Hotpot datasets**

|Col1|NQ|Col3|Hotpot|Col5|
|---|---|---|---|---|
|Datasets|Llama 3.1-8B|Llama 3.1-70B|Llama 3.1-8B|Llama 3.1-70B|
|Method|P<br>R<br>F1|P<br>R<br>F1|P<br>R<br>F1|P<br>R<br>F1|
|RAG<br>GraphRAG<br>Integration|71.70<br>63.93<br>64.78<br>69.48<br>62.54<br>63.01<br>72.81<br>65.91<br>66.28|74.55<br>67.82<br>68.18<br>71.27<br>65.46<br>65.44<br>75.67<br>69.75<br>69.75|62.32<br>60.47<br>60.04<br>64.14<br>62.08<br>61.66<br>67.21<br>65.09<br>64.76|66.34<br>63.99<br>63.88<br>67.20<br>64.89<br>64.60<br>69.22<br>66.70<br>66.50|



**Table 21: The performance of Llama 3.1-8B on MultiHop-RAG dataset**


8B Inference Comparison Null Temporal Overall

RAG 92.16 57.59 96.01 30.7 67.02

GraphRAG 86.89 60.63 80.07 50.6 69.01
Integration 89.71 64.14 50.17 53.34 68.19


**Table 22: The performance of Llama 3.1-70B on MultiHop-RAG dataset**


70B Inference Comparison Null Temporal Overall

RAG 94.85 56.31 91.36 25.73 65.77

GraphRAG 92.03 60.16 88.7 49.06 71.17
Integration 96.45 73.48 59.47 66.72 77.62


**Table 23: Performance of integrating RAG and GraphRAG with Llama 3.1–8B on the NovelQA dataset.**

|Integration|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|70.83<br>58.82<br>63.89<br>73.03<br>84.62<br>60.00<br>36.90<br>49.17<br>62.50<br>64.29<br>74.90<br>62.50<br>79.38<br>-<br>-<br>70.85<br>60.00<br>43.82<br>83.93<br>21.43<br>72.97<br>-<br>-<br>54.20<br>63.33<br>50.19<br>75.23<br>60.80<br>78.23<br>60.00<br>36.90<br>58.36|



**Table 24: Performance of integrating RAG and GraphRAG with Llama 3.1–70B on the NovelQA dataset.**

|Integration|character meaning plot relat settg span times avg|
|---|---|
|mh<br>sh<br>dtl<br>avg|77.08<br>70.59<br>83.33<br>77.53<br>92.31<br>44.00<br>37.97<br>51.99<br>74.34<br>74.29<br>82.43<br>75.00<br>87.63<br>-<br>-<br>80.04<br>67.14<br>53.37<br>92.86<br>75.00<br>89.19<br>-<br>-<br>67.21<br>72.96<br>60.00<br>84.29<br>76.80<br>88.44<br>44.00<br>37.97<br>65.97|



**Table 25: The performance of query-based single document summarization task using Llama 3.1-70B.**








|SQuALITY QMSum<br>Method ROUGE-2 BERTScore ROUGE-2 BERTScore<br>P R F1 P R F1 P R F1 P R F1|SQuALITY|QMSum|
|---|---|---|
|Method<br>SQuALITY<br>QMSum<br>ROUGE-2<br>BERTScore<br>ROUGE-2<br>BERTScore<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1|ROUGE-2<br>BERTScore|ROUGE-2<br>BERTScore|
|Method<br>SQuALITY<br>QMSum<br>ROUGE-2<br>BERTScore<br>ROUGE-2<br>BERTScore<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1<br>P<br>R<br>F1|
|RAG<br>KG-GraphRAG(Triplets only)<br>KG-GraphRAG(Triplets+Text)<br>Community-GraphRAG(Local)<br>Community-GraphRAG(Global)<br>Combine|11.85<br>14.24<br>11.00<br>85.96<br>85.76<br>85.67<br>8.53<br>10.28<br>7.46<br>84.13<br>83.97<br>83.89<br>6.57<br>10.14<br>6.00<br>80.52<br>82.23<br>81.07<br>12.54<br>10.31<br>9.61<br>84.50<br>85.33<br>84.71<br>8.99<br>4.78<br>5.60<br>81.64<br>83.64<br>82.44<br>13.59<br>11.32<br>10.55<br>84.88<br>85.76<br>85.12|10.42<br>10.00<br>9.53<br>86.14<br>85.92<br>86.02<br>10.62<br>6.25<br>7.48<br>83.20<br>84.72<br>83.94<br>8.64<br>7.85<br>7.29<br>84.10<br>84.55<br>84.31<br>13.69<br>7.43<br>9.14<br>84.09<br>85.85<br>84.95<br>10.97<br>4.40<br>6.01<br>81.93<br>84.67<br>83.26<br>13.16<br>8.67<br>9.93<br>85.18<br>86.21<br>85.69|



**K** **The LLM-as-a-Judge Results on more datasets**


In the main paper, we present LLM-as-a-Judge results on the **QM-**
**Sum** and **ODSum-story** datasets. Here, we provide additional



results on **SQuALITY** and **ODSum-meeting**, as shown in Figure 9.
Overall, the trends are consistent with those reported in the main
section, and we draw similar observations.


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.


**Table 26: The performance of query-based multiple document summarization task using Llama3.1-70B.**








|ODSum-story ODSum-meeting<br>Method ROUGE-2 BERTScore ROUGE-2 BERTScore<br>P R F1 P R F1 P R F1 P R F1|ODSum-story|ODSum-meeting|
|---|---|---|
|Method<br>ODSum-story<br>ODSum-meeting<br>ROUGE-2<br>BERTScore<br>ROUGE-2<br>BERTScore<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1|ROUGE-2<br>BERTScore|ROUGE-2<br>BERTScore|
|Method<br>ODSum-story<br>ODSum-meeting<br>ROUGE-2<br>BERTScore<br>ROUGE-2<br>BERTScore<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1<br>P<br>R<br>F1|P<br>R<br>F1<br>P<br>R<br>F1|
|RAG<br>KG-GraphRAG(Triplets only)<br>KG-GraphRAG(Triplets+Text)<br>Community-GraphRAG(Local)<br>Community-GraphRAG(Global)<br>Combine|15.60<br>9.98<br>11.09<br>74.80<br>81.29<br>77.89<br>10.08<br>9.12<br>8.48<br>75.71<br>81.93<br>78.66<br>10.98<br>16.67<br>11.42<br>76.74<br>81.92<br>79.21<br>14.20<br>11.34<br>11.25<br>75.44<br>81.81<br>78.46<br>10.46<br>6.30<br>7.08<br>74.63<br>81.24<br>77.77<br>14.76<br>12.17<br>11.72<br>75.39<br>81.75<br>78.41|18.81<br>6.41<br>8.97<br>83.56<br>85.16<br>84.34<br>11.52<br>3.41<br>4.79<br>81.19<br>83.07<br>82.11<br>13.09<br>6.31<br>7.70<br>84.07<br>84.24<br>84.14<br>16.17<br>7.87<br>9.23<br>84.17<br>84.85<br>84.49<br>10.65<br>1.99<br>3.28<br>79.78<br>82.53<br>81.12<br>17.57<br>8.64<br>10.34<br>84.51<br>85.14<br>84.81|



**Figure 7: Prompt for Query Classification.**


**L** **Graph Construction with different LLMs**


In the main paper, we use GPT-4o-mini to extract entities and
relationships for graph construction due to cost considerations.
To investigate whether stronger LLMs yield better performance,
we also use GPT-4o for graph extraction. Specifically, we evaluate this on the MultiHop-RAG and ODSum-story datasets, representing question answering and summarization tasks, respectively.
We focused on Community-GraphRAG (Local) as a representative
method (GraphRAG) and evaluated it with both LLaMA3.1-8B and
LLaMA3.1-70B for generation.
The results are shown in Table 27, Table 28, Table 29 and Table 30,
respectively. The results show that using a stronger LLM (GPT4o) for graph extraction generally improves the performance of
GraphRAG on both question answering and summarization tasks.
However, the overall conclusion regarding the relative performance



**Figure 8: Prompt used for LLM-as-a-Judge evaluation.**


of RAG and GraphRAG remains consistent across different graph
construction backbones.


RAG vs. GraphRAG: A Systematic Evaluation and Key Insights Conference acronym ’XX, June 03–05, 2018, Woodstock, NY



















|1.0<br>RAG-Order 1<br>GraphRAG-Local-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Local-Order 2<br>0.6<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Local-Order 1<br>RAG-Order 2<br>GraphRAG-Local-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br><br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|G~~-~~Order 1<br>raphRAG~~-~~Local~~-~~Order 1<br>AG~~-~~Order 2|G~~-~~Order 1<br>raphRAG~~-~~Local~~-~~Order 1<br>AG~~-~~Order 2|G~~-~~Order 1<br>raphRAG~~-~~Local~~-~~Order 1<br>AG~~-~~Order 2|G~~-~~Order 1<br>raphRAG~~-~~Local~~-~~Order 1<br>AG~~-~~Order 2|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br><br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br><br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br><br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|raphRAG~~-~~Local~~-~~Order 2|||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br><br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br><br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||||||


**(a) SQuALITY Local**



|1.0<br>RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Gloabl-Order 2<br>0.6 Proportion<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>RAG-Order 2<br>GraphRAG-Gloabl-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2||||||||


**(b) SQuALITY Global**



|1.0<br>RAG-Order 1<br>GraphRAG-Local-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Local-Order 2<br>0.6 Proportion<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Local-Order 1<br>RAG-Order 2<br>GraphRAG-Local-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||Gra|phRAG~~-~~Local~~-~~Order 2|phRAG~~-~~Local~~-~~Order 2|phRAG~~-~~Local~~-~~Order 2|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Local~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Local~~-~~Order 2||||||||


**(c) ODSum-meeting Local**



|1.0<br>RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>0.8 RAG-Order 2<br>GraphRAG-Gloabl-Order 2<br>0.6 Proportion<br>0.4<br>0.2<br>0.0<br>Comprehensiveness Diversity|RAG-Order 1<br>GraphRAG-Gloabl-Order 1<br>RAG-Order 2<br>GraphRAG-Gloabl-Order 2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|||||||||
|~~Comprehensiveness~~<br>~~Diversity~~<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Proportion<br>RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|RAG~~-~~Order 1<br>GraphRAG~~-~~Gloabl~~-~~Order 1<br>RAG~~-~~Order 2<br>GraphRAG~~-~~Gloabl~~-~~Order 2|||||||||


**(d) ODSum-meeting Global**



**Figure 9: Comparison of LLM-as-a-Judge evaluations for RAG and GraphRAG. "Local" refers to the evaluation of RAG vs.**
**GraphRAG-Local, while "Global" refers to RAG vs. GraphRAG-Global. "Order 1" corresponds to the prompt where RAG result is**
**presented before GraphRAG, whereas "Order 2" corresponds to the reversed order.**



**Table 27: Performance of different graph construction meth-**
**ods with Llama 3.1–8B on the MultiHop-RAG dataset.**

|In|ference Comparison Null Temporal Overall|
|---|---|
|RAG<br>GPT-4o-mini<br>GPT-4o|92.16<br>57.59<br>96.01<br>30.7<br>67.02<br>86.89<br>60.63<br>80.07<br>50.6<br>69.01<br>88.11<br>62.62<br>70.43<br>49.74<br>68.74|



**Table 28: Performance of different graph construction meth-**
**ods with Llama 3.1–70B on the MultiHop-RAG dataset.**

|70B In|ference Comparison Null Temporal Overall|
|---|---|
|RAG<br>GPT-4o-mini<br>GPT-4o|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>92.03<br>60.16<br>88.70<br>49.06<br>71.17<br>93.63<br>66.59<br>81.06<br>58.49<br>75.08|



**Table 29: Performance of different graph construction meth-**
**ods with Llama 3.1–8B on the ODSum-story dataset.**

|Col1|ROUGE-2|BERTScore|
|---|---|---|
||P<br>R<br>F1|P<br>R<br>F1|
|RAG<br>GPT-4o-mini<br>GPT-4o|15.39<br>8.44<br>9.81<br>13.84<br>7.19<br>8.49<br>13.99<br>7.45<br>8.64|83.87<br>85.74<br>84.57<br>83.19<br>85.07<br>83.90<br>83.24<br>85.1<br>83.94|



**Table 30: Performance of different graph construction meth-**
**ods with Llama 3.1–8B on the ODSum-meeting dataset.**

|Col1|ROUGE-2|BERTScore|
|---|---|---|
||P<br>R<br>F1|P<br>R<br>F1|
|RAG<br>GPT-4o-mini<br>GPT-4o|11.85<br>14.24<br>11.09<br>12.54<br>10.31<br>9.61<br>12.08<br>10.84<br>9.72|85.96<br>85.76<br>85.67<br>84.51<br>85.33<br>84.71<br>84.66<br>85.28<br>84.77|



**M** **Computation and Storage Analysis**


Besides runtime and storage, we also analyze the number of tokens retrieved by Community-GraphRAG and RAG. The results are
shown in Table 31.



**Table 31: The retrieved number of tokens.**

|Col1|RAG Community-GraphRAG|
|---|---|
|MultiHop-RAG<br>ODSum-Story|3631<br>9770<br>2279<br>10244|



In our experimental setup, RAG retrieves the top-10 text chunks,
while Community-GraphRAG (Local) retrieves the top-10 entities
and their associated relations. As shown in Table 31, CommunityGraphRAG results in significantly more input tokens due to the
inclusion of entities, entity descriptions, relations, relation descriptions, and community summaries.
To ensure a fair comparison, we conducted an additional experiment in which we increased the number of retrieved text chunks

for RAG to match the total number of input tokens retrieved by
Community-GraphRAG. The results are shown in Table 32, Table 33, Table 34 and Table 35. While increasing RAG’s input size
does lead to slight performance gains, our main conclusions remain
unchanged: RAG performs better on inference-style queries and
summarization tasks, where detailed information is directly retrievable. In contrast, GraphRAG performs better on complex queries
such as Comparison and Temporal types in MultiHop-RAG, which
require multi-hop reasoning and aggregation.


Conference acronym ’XX, June 03–05, 2018, Woodstock, NY Han et al.


**Table 32: Performance comparison of RAG, token-matched RAG, and GraphRAG using Llama 3.1–8B on MultiHop-RAG dataset.**

|Col1|Inference Comparison Null Temporal Overall|
|---|---|
|RAG<br>RAG_Same Token<br>GraphRAG|92.16<br>57.59<br>96.01<br>30.7<br>67.02<br>95.34<br>59.81<br>89.04<br>36.71<br>69.33<br>86.89<br>60.63<br>80.07<br>50.6<br>69.01|



**Table 33: Performance comparison of RAG, token-matched RAG, and GraphRAG using Llama 3.1–70B on MultiHop-RAG.**

|70B|Inference Comparison Null Temporal Overall|
|---|---|
|RAG<br>RAG_Same Token<br>GraphRAG|94.85<br>56.31<br>91.36<br>25.73<br>65.77<br>95.96<br>59.58<br>88.7<br>43.74<br>71.01<br>92.03<br>60.16<br>88.7<br>49.06<br>71.17|



**Table 34: Performance comparison of RAG, token-matched RAG, and GraphRAG using Llama 3.1–8B on ODSum-Story.**

|8B|ROUGE-2|BERTScore|
|---|---|---|
||P<br>R<br>F1|P<br>R<br>F1|
|RAG<br>RAG_Same Token<br>GraphRAG|15.39<br>8.44<br>9.81<br>14.16<br>10.02<br>10.16<br>13.84<br>7.19<br>8.49|83.87<br>85.74<br>84.57<br>84.34<br>85.74<br>84.82<br>83.19<br>85.07<br>83.9|



**Table 35: Performance comparison of RAG, token-matched RAG, and GraphRAG using Llama 3.1–70B on ODSum-Meeting.**


|Col1|ROUGE-2|BERTScore|
|---|---|---|
||P<br>R<br>F1|P<br>R<br>F1|
|RAG<br>RAG_Same Token<br>GraphRAG|11.85<br>14.24<br>11.09<br>12.82<br>14.07<br>11.34<br>12.54<br>10.31<br>9.61|85.96<br>85.76<br>85.67<br>85.86<br>86<br>85.73<br>84.51<br>85.33<br>84.71|


