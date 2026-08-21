## **MemGraphRAG: Memory-based Multi-Agent System for Graph** **Retrieval-Augmented Generation**



Yunbo Tang
tangyunbo@stu.xmu.edu.cn
Xiamen University [1]

Xiamen, China


Jinsong Su [†]

jssu@xmu.edu.cn
Xiamen University [1, 2, 3]

Xiamen, China



Chuanjie Wu [∗]

wuchuanjie@stu.xmu.edu.cn
Xiamen University [1, 2]

Xiamen, China


Zerui Chen

chenzerui1@stu.xmu.edu.cn
Xiamen University [1]

Xiamen, China



Zhishang Xiang [∗]

xiangzhishang@stu.xmu.edu.cn
Xiamen University [2, 3]

Xiamen, China


Qinggang Zhang [†]

qinggangzhang@jlu.edu.cn
Jilin University
Changchun, China



**Abstract**


Retrieval-Augmented Generation (RAG) has become an essential
method for mitigating hallucinations in Large Language Models
(LLMs) by leveraging external knowledge. Although effective for
simple queries, traditional RAG struggles with large-scale, unstructured corpora where information is highly fragmented. Graphbased RAG (GraphRAG) incorporates knowledge graphs to capture
structural relationships, enabling more comprehensive retrieval
for complex reasoning. However, existing GraphRAG methods rely
on isolated, fragment-level extraction for graph construction, lacking a global perspective on the whole corpus. As a result, these
methods frequently lead to thematically inconsistent, logically
conflicting, and structurally fragmented graphs that degrade retrieval performance. In this paper, we propose MemGraphRAG,
a novel framework that introduces a memory-based multi-agent
system to ensure high-quality graph construction. Specifically,
MemGraphRAG employs a collaborative society of agents supported by shared memory, which provides a unified global context
throughout the extraction process. This mechanism allows agents
to dynamically resolve logical conflicts and maintain structural
connectivity throughout the corpus. Furthermore, we propose a
memory-aware hierarchical retrieval algorithm tailored for the constructed graph. Extensive experiments on multiple benchmarks
demonstrate that MemGraphRAG outperforms the state-of-the-art
baseline models with comparable efficiency. Our code is available
[at https://github.com/XMUDeepLIT/MemGraphRAG.](https://github.com/XMUDeepLIT/MemGraphRAG)


∗ Contributed equally.

- Corresponding author.
1 School of Informatics
2 Key Laboratory of Digital Protection and Intelligent Processing of Intangible Cultural
Heritage of Fujian and Taiwan,Ministry of Culture and Tourism
3 Institute of Artificial Intelligence


[This work is licensed under a Creative Commons Attribution 4.0 International License.](https://creativecommons.org/licenses/by/4.0)

_KDD 2026, Jeju Island, Republic of Korea._
© 2026 Copyright held by the owner/author(s).
ACM ISBN 979-8-4007-2259-2/2026/08
[https://doi.org/10.1145/3770855.3818074](https://doi.org/10.1145/3770855.3818074)



**CCS Concepts**


- **Information systems** → **Retrieval models and ranking** ; •
**Computing methodologies** → _Information extraction; Knowledge_
_representation and reasoning_ .


**Keywords**


RAG, GraphRAG, Multi Agent, Agent Memory, Indexing Graph


**ACM Reference Format:**

Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang,
and Jinsong Su. 2026. MemGraphRAG: Memory-based Multi-Agent System
for Graph Retrieval-Augmented Generation. In _Proceedings of the 32nd ACM_
_SIGKDD Conference on Knowledge Discovery and Data Mining V.2 (KDD_
_2026), August 9–13, 2026, Jeju Island, Republic of Korea._ ACM, New York, NY,
[USA, 20 pages. https://doi.org/10.1145/3770855.3818074](https://doi.org/10.1145/3770855.3818074)


**1** **Introduction**


Recently, Retrieval-Augmented Generation (RAG) effectively extends the capabilities of Large Language Models (LLMs) by leveraging external knowledge [ 16, 31, 63 ]. However, existing RAG systems
suffer from critical challenges in real-world scenarios. This is due to
the unstructured and heterogeneous nature of large-scale corpora,
where relevant information is often sparsely distributed. The contexts retrieved by RAG systems are often noisy and lack structural
coherence. Although recent methods attempt to segment documents into smaller chunks for efficient indexing [ 2, 27, 29 ], this
strategy disrupts long-range dependencies and loses critical contextual details. As a result, the retrieved contexts are often incoherent
or insufficient for complex reasoning tasks [23, 62].
To address these limitations, Graph Retrieval-Augmented Generation (GraphRAG) [ 41, 52, 62 ] has emerged as a powerful paradigm,
leveraging external structured graphs to model the hierarchical
structure of background knowledge [ 23, 57 ]. Early efforts, such as
RAPTOR [ 44 ] and Microsoft’s GraphRAG [ 12 ], organize knowledge
through recursive summarization and community-level abstractions to support coarse-to-fine retrieval, thereby facilitating comprehensive response generation. Subsequent methods, including GFMRAG [ 37 ], G-Retriever [ 24 ], and LightRAG [ 17 ], further incorporate
specialized retrieval mechanisms and learning objectives to improve
multi-hop generalization, scalability, and efficiency. Most recently,
HippoRAG [ 19 ]and its enhancement HippoRAG2 [ 20 ] have drawn
inspiration from cognitive associative memory, utilizing algorithms
such as Personalized PageRank to simulate multi-hop reasoning


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su





Retrieval

Merging


Construction Knowledge Graph



Local Information Only









SubGraph









**Figure 2: (Left) Evaluation of representative RAG and**
**GraphRAG systems. The radius reflecting performance of**
**each systems.** _**Relevance**_ **measuring context relevance to the**
**query.** _**Recall**_ **measuring whether sufficient evidence is cov-**
**ered. (Right) Impact of removing irrelevant triples based on**
**schema frequency on the final performance (LLM-ACC).**


pathways. These strategies demonstrate the potential of graph-baed
retrieval in addressing the core limitations of traditional RAG.
However, contrary to their theoretical advantages, GraphRAG
systems frequently underperform naive RAG systems in many
real-world applications [ 22, 52, 69, 70 ]. This performance decline
is primarily due to the low quality of automatically constructed
knowledge graphs [ 52, 70 ]. Although graph-based retrieval enhances relevant knowledge recall, errors in graph construction
introduce substantial noise into the retrieved contexts simultane
ously. Fundamentally, these challenges persist because existing
pipelines typically derive knowledge from isolated local segments,
lacking a global perspective on the previously processed context.
This isolation leads to three critical deficiencies that undermine

graph quality: (i) **thematic irrelevance** : extracted triples are often
irrelevant to the central theme, introducing meaningless facts. (ii)
**logical inconsistency** : contradictory facts may emerge within a
single subgraph, compromising semantic coherence. (iii) **structural**
**fragmentation** : the built graphs often suffer from fragmentation
issues, where the isolated nodes and disconnected components
weaken the core advantage of the knowledge graph in supporting
global comprehension and multi-hop reasoning.



While some recent studies attempt to improve graph quality
before extraction by filtering triples using predefined schema [ 9,
45 ], these approaches suffer from limited generalization and high
manual costs. Other efforts seek to improve graph quality through
bottom-up clustering-based community summarization [ 12, 20, 50 ]
or topic modeling [ 44 ]. Nevertheless these unsupervised approaches
remain susceptible to error propagation, because inaccuracies in
entity relations tend to be amplified at high-level summaries.
To address this, we revisit the pipeline of existing GraphRAG
systems and propose a **Mem** ory-Based Multi-Agent Framework
for **Graph R** etrieval- **A** ugmented **G** eneration ( **MemGraphRAG** ).
Specifically, MemGraphRAG employs a collaborative society of
agents supported by a novel Three-Layer Global Memory. This
shared memory structure serves as a unified knowledge repository,
providing a global perspective that enables agents to dynamically
coordinate the extraction process, resolve conflicts upon detection,
and integrate fragmented information across the entire corpus. To
summarize, our contributions are listed as follows:


  - We identify the root cause of performance degradation in
existing GraphRAG systems: the reliance on isolated local
extraction. We demonstrate how this lack of global context
inevitably leads to three critical deficiencies: thematic irrelevance, logical inconsistency, and structural fragmentation.

  - We propose MemGraphRAG, which introduces a memorybased multi-agent system into graph construction. The shared
memory not only maintains global thematic consistency to
prevent irrelevance and fragmentation, but also provides
grounded evidence to resolve local logical inconsistencies.
Besides, we propose a memory-aware hierarchical retrieval
algorithm tailored for the constructed graph.

  - We conduct extensive experiments on four benchmark datasets,
demonstrating that MemGraphRAG consistently outperforms
state-of-the-art baselines in terms of graph quality, retrieval
quality and generation accuracy, validating its practicality
for real-world applications.


**2** **Problem Statement**


To facilitate subsequent discussion, we first introduce key definitions for the knowledge representation, and then present the
complete problem formulation of GraphRAG.


**2.1** **Key Definitions**


We first provide formal definitions for the core components of our
knowledge representation:
(i) **type (** _𝑡_ **) and entity (** _𝑒_ **)** : a type _𝑡_ (e.g., _person_ ) denotes an
abstract category, while an entity _𝑒_ (e.g., _Einstein_ ) is a concrete
instance. Formally, a typing function _𝜙_ assigns each entity to its
specific type, denoted as _𝜙_ ( _𝑒_ ) = _𝑡_ .
(ii) **schema (** _𝑠_ **) and fact (** _𝑓_ **)** : a schema _𝑠_ = ( _𝑡_ _ℎ_ _,𝑟,𝑡_ _𝑡_ ) (e.g., ( _person_,
_born_in_, _country_ )) specifies a logical constraint. _𝑡_ _ℎ_ _,𝑡_ _𝑡_ represent the
head and tail types, respectively, _𝑟_ denotes a semantic relation.
Based on this structure, a fact _𝑓_ = ( _𝑒_ _ℎ_ _,𝑟,𝑒_ _𝑡_ ) (e.g., ( _Einstein_, _born_in_,
_Germany_ )) is a concrete instantiation of a schema, where _𝑒_ _ℎ_ _,𝑒_ _𝑡_
represent the head and tail entity.


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.





1) Mutually Exclusive Conflict













how automatic graph construction affects retrieval quality and
downstream generation.


**3.1** **Performance Degradation**


We first compare Vanilla RAG with recent GraphRAG systems (MSGraphRAG, HippoRAG, and GFM-RAG) in the G-Medical dataset[ 52 ].
As shown in Figure 2(a), GraphRAG methods achieve higher retrieval Recall (e.g., GFM-RAG: 84.3% vs. RAG: 71.8%), but suffer a
substantial drop in Relevance (38.5% vs. 62.9%), leading to noisier
contexts and lower generation accuracy. These results indicate that
existing GraphRAG pipelines often expand the retrieval coverage
at the cost of introducing excessive irrelevant information, which
ultimately harms the QA performance.


**3.2** **Error Analysis**


To further investigate why graph construction introduces noise
and conflicts, we hypothesize that the root cause lies in the isolated
local extraction paradigm adopted by most baselines. Without a persistent global memory, extraction LLMs process document chunks
independently, which leads to systematic issues in graph quality.
Specifically, we summarize the major failure modes as follows:
**Thematic Irrelevance.** Without a global view of the corpus
theme, local extraction tends to introduce off-topic triples. To quantify this effect, we conduct a filtering experiment (Figure 2(b)) that
removes triples based on schema frequency. Interestingly, filtering
out 40% of low-frequency triples slightly improves accuracy (65.28%
vs. 64.85%), suggesting that a large fraction of extracted triples are
thematically irrelevant noise.
**Logical Inconsistency.** Independent extraction also introduces
semantic contradictions into the merged graph. As illustrated in
Figure 3, we observe mutually exclusive conflicts, temporal conflicts, and granularity conflicts, which create inconsistent reasoning
paths and confuse downstream retrieval. More conflict analyses are
provided in Appendix C.
**Structural Fragmentation.** Due to missing global coreference
resolution and schema alignment, key entities are often duplicated
or scattered across disconnected subgraphs. This fragmentation
prevents effective multi-hop traversal and reduces the usefulness
of the graph for global reasoning.


**3.3** **Discussion**


Current GraphRAG systems exhibit two fundamental limitations.
**First, existing GraphRAG systems exhibit a fundamental**
**trade-off between recall and relevance.** Although graph expansion improves coverage, it often retrieves irrelevant evidence
that overwhelms the LLM and degrades generation accuracy. **Sec-**
**ond, current GraphRAG systems lack a global memory mech-**
**anism during graph construction.** Most systems rely on isolated local extraction, processing document chunks independently
without maintaining a persistent global state. As a result, the constructed graph fails to preserve thematic coherence and resolve
cross-document conflicts, leading to _thematic irrelevance_, _logical_
_inconsistency_, and _structural fragmentation_ in downstream retrieval
and reasoning processes.































**Figure 3: Illustration of three conflict types in extracted**
**graphs: 1) Mutually Exclusive Conflict from logically incom-**
**patible facts, 2) Temporal Conflict caused by missing tem-**
**poral grounding for time-varying states, and 3) Granularity**
**Conflict arising from inconsistent abstraction levels for the**
**same entity or concept. Details are in Table 8 in Appendix C**


(iii) **ontology (** O **)** : the ontology O is defined as the collection
of all valid schemas, denoted as O = { _𝑠_ 1 _, . . .,𝑠_ | O| } . It includes the
theme and logical rules of the whole knowledge graph.
(iv) **passage (** _𝑝_ **)** : a passage _𝑝_ denotes the specific text segment
acting as the source of the extracted information. We define a
function _𝜓_ ( _𝑓_ ) = _𝑝_ to trace each fact _𝑓_ back to its origin.
Detailed definitions are provided in Appendix **??** .


**2.2** **Problem Formulation**


We formally formulate the task of GraphRAG as a unified framework composed of two distinct phases:
(i) **Offline Graph Structure Construction** . Given a corpus of
unstructured documents D = { _𝑑_ 1 _,𝑑_ 2 _, ...,𝑑_ | D| }, the primary objective is to transform raw text into a structured graph G = (V _,_ E) .
In our framework, the vertex set V is heterogeneous, comprising
entities, types, and passages ( V = V _𝑒_ ∪V _𝑡_ ∪V _𝑝_ ), and the edge
set E encodes the semantic dependencies between them. Formally,
this construction process is formalized as


G = GraphConstructor(D) (1)


where GraphConstructor(*) maps the unstructured corpus to a
semantic graph topology, facilitating the efficient navigation from
abstract concepts to concrete evidence.
(ii) **Online Graph-Enhanced Retrieval and Reasoning** . Based
on the constructed graph G, the system processes a user query _𝑞_ to
generate a final answer _𝑎_ . Unlike extracting isolated text segments,
this phase involves identifying optimal reasoning paths within the
graph to curate a structured context. The process is formulated as


_𝑎_ = LLM(Retriever( _𝑞,_ G)) (2)


where Retriever(*) identifies the most relevant graph elements
(subgraphs) to support grounded answer generation.


**3** **Preliminary Study**


Although knowledge graphs can model complex dependencies, recent benchmarks show that advanced GraphRAG systems may
underperform naive RAG in real-world QA tasks [ 52, 70 ]. To investigate this issue, we conduct two preliminary studies to analyze


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su














































|Memory-based Indexing Graph Construction|Memory-guided Online Retrieval|
|---|---|
|Unstructured<br>Documents<br>Extraction Agent<br>Conflict Detector<br>Conflict Handler<br>**Three-Layer Global Memory**<br>（Person, Rule, Country)<br>…<br>(Person, Native, Location)<br>(Company, Create, Product)<br>**Pending Schema**<br>**Frequency**<br>**Filter**<br>(Country, Capital, City)<br>…<br>(Person, Job, Profession)<br>(Person, Birthyear, Year)<br>**Stable Schema**<br>Article 288<br>Simpson Sean is a Canadian ice ho-<br><br><br>**Fact Layer (**𝑴𝒇𝒂𝒄**)**<br>**Ontology Layer (**𝑴𝒐𝒏𝒕**)**<br>**Passage Layer (**𝑴𝒑𝒂𝒔**)**<br>(Louis XIV, Rule, France)<br>…<br>(Drake, Native, Toronto)<br>(OpenAI, Create, ChatGPT)<br>**Inactive Instances**<br>(Newton, Birthyear, 1643)<br>…<br>(Newton, Birthyear, 1645)<br>(Simpson, Job, Coach)<br>**trigger**<br>**Multi-Agent Group**<br>Conflict<br>Found<br><br>Original<br><br>Update<br>**Ontology Graph**<br>**Entity:**UK<br>Conflict<br>Propagation<br>**_Ontology_**<br>**Passage**<br>**Entity:**Simpson Sean<br>**Type:**Person<br>**Relation:**Job<br>**Type:**Profession<br>**Weight:**5<br>**_Ontology_**<br>**Schema**<br>**Entity:**Coach<br>**Relation:**Job<br>**Entity:**Simpson Sean<br>**Weight:**1<br>**_Ontology_**<br>**Fact**<br>**Passage Graph**<br>**Fact Graph**<br>**Active Facts**<br>**Hierarchical Graph**|𝑴𝒐𝒏𝒕<br>𝑴𝒇𝒂𝒄<br>𝑴𝒑𝒂𝒔<br>Question<br>(𝑠𝑖𝑚> 𝜏)<br>Retrieved<br>Passages<br>Retrieved<br>Facts<br>**Answer**<br>**Schema**<br>**Fact**<br>**Passage**<br>**Type**<br>**Entity**<br>**Personalized**<br>**PageRank**|







**Figure 4: Overview of the MemGraphRAG framework with two phases: (i) Memory-Based Indexing Graph Construction, where**
**Global Memory (** M **) and the Knowledge Graph (** G **) co-evolve via unified schema filtering, global adjudication, and memory-**
**guided bridging; and (ii) Memory-Guided Online Retrieval, which leverages multi-layer memory filtering, structure-aware**
**node initialization, and Personalized PageRank to identify globally relevant contexts for generation.**



**4** **Our Framework**


To overcome fragmented extraction and enable coherent graph evolution, we propose **MemGraphRAG**, a memory-based framework
for constructing and maintaining high-quality knowledge graphs.
Our key insight is that reliable graph construction requires not
only structured storage, but also persistent coordination and correction across documents. As illustrated in Figure 4, it consists of
two collaborative modules: Memory-based Graph Construction and
Memory-guided Retrieval. We first introduce the foundational architecture, followed by the graph construction and retrieval pipelines.


**4.1** **MemGraphRAG Architecture**


MemGraphRAG consists of three core components: a _Global Mem-_
_ory_ that stores schemas, facts, and passages at different granularities
and supports the construction of the _Hierarchical Indexing Graph_,
and a _Multi-Agent Group_ that interacts with memory to iteratively
extract, detect, and resolve conflicts. Specifically:
**Global Memory (** M **)** organizes the extracted knowledge into
a three-tier hierarchy, including an _Ontology Layer_ ( M _𝑜𝑛𝑡_ ) that
stores schemas with extraction frequencies, a _Fact Layer_ ( M _𝑓𝑎𝑐_ ) that
maintains concrete facts, and a _Passage Layer_ ( M _𝑝𝑎𝑠_ ) that preserves
original text passages for evidence grounding. To strengthen crosslayer associations, we introduce a _dense indexing mechanism_ that
enforces schema consistency and evidence traceability through two
bidirectional interactions, where _schema-instance alignment_ links
schemas with facts and _fact-evidence grounding_ connects facts with
their supporting passages. (See more details in Appendix D.2).
**Hierarchical Indexing Graph** ( G ). It provides a unified representation spanning abstract schemas, concrete facts, and textual
evidence. It consists of three interconnected graph views: (i) _Se-_
_mantic Ontology Graph_ G _𝑜𝑛𝑡_, derived from M _𝑜𝑛𝑡_, which encodes
schema-level type relations and structural constraints; (ii) _Fact_



_Graph_ G _𝑓𝑎𝑐_, constructed from M _𝑓𝑎𝑐_, which represents instantiated entity-relation triples for multi-hop reasoning; and (iii) _Source_
_Evidence Graph_ G _𝑝𝑎𝑠_, induced from M _𝑝𝑎𝑠_, which grounds facts in
G _𝑓𝑎𝑐_ back to their supporting passages. This hierarchical design
enables reasoning to traverse from abstract semantics to grounded
evidence. More details are provided in Appendix D.2.
**Multi-Agent Group** ( A ). We introduce a group of agents A =
{ _𝐴_ _𝑒𝑥𝑡_ _,𝐴_ _𝑑𝑒𝑡_ _,𝐴_ _𝑟𝑒𝑠_ } . Specifically: (i) the _Extraction Agent_ _𝐴_ _𝑒𝑥𝑡_ extracts
schemas, facts, and passages into M with evidence grounding; (ii)
the _Conflict Detection Agent_ _𝐴_ _𝑑𝑒𝑡_ monitors M _𝑓𝑎𝑐_ to detect redundancy, structural anomalies, and logical inconsistencies; and (iii) the
_Conflict Resolution Agent_ _𝐴𝑟𝑒𝑠_ leverages schema constraints from
M _𝑜𝑛𝑡_ and historical evidence from M _𝑝𝑎𝑠_ to resolve conflicts and
maintain global consistency in G . This design separates extraction,
diagnosis, and correction for reliable graph construction.


**4.2** **Memory-based Indexing Graph**
**Construction**


Traditional graph construction often processes document chunks
in isolation, resulting in index fragmentation and noise accumulation. To address the critical limitations of _Thematic Irrelevance_,
_Logical Inconsistency_, and _Structural Fragmentation_ identified in
our pilot study, we reformulate knowledge graph construction as a
dynamic co-evolution process between the Global Memory M and
the Knowledge Graph G . Distinct from static extraction pipelines,
our approach adheres to three core principles designed to systematically resolve these issues: (i) **Thematic Denoising via Unified**
**Schema Filtering** : Addressing _Thematic Irrelevance_, we employ a
unified schema to rigorously filter and manage extracted triples,
ensuring that only thematically relevant knowledge is retained; (ii)
**Consistency Maintenance via Global Adjudication** : To resolve
_Logical Inconsistency_, we utilize the global memory to assist agents


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.



in detecting and adjudicating semantic contradictions across disparate documents, thereby ensuring the logical unity of the graph;
iii) **Structural Unification via Memory-Guided Bridging** : To
overcome _Structural Fragmentation_, we leverage the global memory to identify and merge equivalent entities across disconnected
subgraphs. By connecting isolated local extractions and aligning
them with the global ontology, we construct a cohesive and interconnected knowledge representation. Specifically, our graph
construction procedure is described as follows:


_4.2.1_ _Thematic Denoising via Unified Schema Filtering._ Graph construction begins with the _Extraction Agent_ _𝐴_ _𝑒𝑥𝑡_, which transforms
each document chunk _𝑐_ _𝑖_ into structured memory entries. Rather
than producing triples alone, _𝐴_ _𝑒𝑥𝑡_ jointly constructs entries for all
three layers of Global Memory M by generating candidate schemas,
instantiated facts, and their supporting passages:


_𝐴_ _𝑒𝑥𝑡_ ( _𝑐_ _𝑖_ ) →{S _𝑐𝑎𝑛𝑑_ ∈M _𝑜𝑛𝑡_ _,_ T _𝑐𝑎𝑛𝑑_ ∈M _𝑓𝑎𝑐_ _,_ P _𝑠𝑟𝑐_ ∈M _𝑝𝑎𝑠_ } _._ (3)


This design ensures that each extracted triple is strictly aligned
with a schema and grounded in source evidence. To mitigate hallucination accumulation, newly generated schemas are initially treated
as candidates and are promoted to stable schemas only when their
empirical frequency exceeds a threshold:


M _𝑜𝑛𝑡_ _[𝑠𝑡𝑎𝑏𝑙𝑒]_ = { _𝑠_ ∈M _𝑜𝑛𝑡_ | Freq( _𝑠_ ) ≥ _𝜏_ } _._ (4)


Accordingly, only facts aligned with stable schemas are activated for
downstream graph construction and reasoning. Detailed extraction
procedures are provided in Appendix D.3.1.


_4.2.2_ _Consistency Maintenance via Global Adjudication._ During
evolutionary extraction, newly activated triples may introduce redundancy or semantic conflicts with existing facts. To ensure the
long-term consistency of the _Fact Layer_ M _𝑓𝑎𝑐_, We deploy a decoupled diagnosis and correction loop, where the _Conflict Detection_
_Agent_ ( _𝐴_ _𝑑𝑒𝑡_ ) and the _Conflict Resolution Agent_ ( _𝐴_ _𝑟𝑒𝑠_ ) collaborate
to continuously maintain memory integrity. Specifically, when a
new triple _𝑡_ _𝑛𝑒𝑤_ ∈M _𝑓𝑎𝑐_ becomes active, _𝐴_ _𝑑𝑒𝑡_ asynchronously scans
existing facts and identifies a conflict set F _𝑐𝑜𝑛𝑓_ based on semantic
similarity and ontology-level structural constraints:


F _𝑐𝑜𝑛𝑓_ = { _𝑡_ [′] ∈M _𝑓𝑎𝑐_ | Sim( _𝑡_ _𝑛𝑒𝑤_ _,𝑡_ [′] ) _> 𝛿_ ∨ Match( _𝑡_ _𝑛𝑒𝑤_ _,𝑡_ [′] ) } _._ (5)


If F _𝑐𝑜𝑛𝑓_ is non-empty, _𝐴_ _𝑟𝑒𝑠_ is triggered to resolve the detected
inconsistencies. Rather than generating corrections heuristically,
_𝐴_ _𝑟𝑒𝑠_ leverages _fact-evidence grounding_ to retrieve the provenance
passages from M _𝑝𝑎𝑠_ and adjudicates conflicts by comparing the
corresponding textual evidence. This evidence-driven resolution
enables reliable corrective actions such as filtering invalid facts,
merging redundant triples, and resolving temporal or granularity inconsistencies, thereby ensuring that M _𝑓𝑎𝑐_ remains globally
coherent throughout the graph construction process.


_4.2.3_ _Structural Unification via Memory-Guided Bridging._ In the
final phase, we project the refined Global Memory M into the
_Hierarchical Indexing Graph_ G by constructing three interconnected
graph views. Specifically, we build the _Semantic Ontology Graph_
G _𝑜𝑛𝑡_ directly from M _𝑜𝑛𝑡_, where nodes and edges encode schemalevel types and their valid relations, serving as the logical backbone
of the overall structure. We then construct the _Fact Graph_ G _𝑓𝑎𝑐_
from M _𝑓𝑎𝑐_, where entities form nodes and instantiated triples form



edges, enabling multi-hop reasoning over concrete facts. To improve
connectivity and reduce fragmentation, we further augment G _𝑓𝑎𝑐_
by introducing additional bridging edges, including type-based
connections derived from shared stable schema types in G _𝑜𝑛𝑡_ and
similarity-based connections between entities with high embedding
similarity. Finally, we induce the _Source Evidence Graph_ G _𝑝𝑎𝑠_ from
M _𝑝𝑎𝑠_, which links facts and entities in G _𝑓𝑎𝑐_ back to their originating
passages, ensuring that every reasoning path remains traceable to
grounded textual evidence.


**4.3** **Memory-guided Online Retrieval**


Building upon the Global Hierarchical Graph G and Global Memory
M, we perform memory-guided retrieval and reasoning in three
stages: (i) **Multi-Layer Memory Retrieval**, which retrieves candidate schemas, facts, and passages from M _𝑜𝑛𝑡_, M _𝑓𝑎𝑐_, and M _𝑝𝑎𝑠_ ; (ii)
**Structure-Aware Node Initialization**, which maps the retrieved
evidence to initial node weights based on semantic relevance and
structural signals; and (iii) **Graph Propagation**, which runs Personalized PageRank (PPR) over the heterogeneous graph to rank
globally important nodes and passages for LLM generation.


_4.3.1_ _Multi-Layer Memory Filtering._ The retrieval phase initiates
by querying the three distinct layers of the Global Memory M in
parallel. Given a user query q, we retrieve top- _𝐾_ candidates from
M in parallel, including schemas from M _𝑜𝑛𝑡_, facts from M _𝑓𝑎𝑐_, and
passages from M _𝑝𝑎𝑠_ . To reduce noise before graph reasoning, we
retain only schemas and facts whose semantic similarity satisfies
Sim( q _,_ x ) _> 𝜏_ . This filtering ensures that subsequent node initialization is seeded with high-confidence structural evidence. If no
valid structural candidates remain (i.e., S _𝑟𝑒𝑡_ ∪F _𝑟𝑒𝑡_ = ∅ ), we fall
back to standard RAG retrieval by directly selecting passages from
M _𝑝𝑎𝑠_ based on query similarity.


_4.3.2_ _Structure-Aware Node Initialization._ To seed graph propagation with query-specific context, we project the retrieved evidence
onto the heterogeneous graph by defining an initial reset probability distribution _𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑣_ ) for each node _𝑣_ ∈G . This distribution
assigns the starting importance of nodes before propagation. We
then initialize _𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑣_ ) along three complementary dimensions, as
detailed below.

**Entity Node Initialization via Facts:** To ensure that graph propagation originates from grounded evidence, we initialize each entity
node _𝑒_ based on the relevance of its associated retrieved facts. Specifically, its initial weight is defined as the mean similarity over all
query-relevant facts containing _𝑒_ :



1
_𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑒_ ) =
| F _𝑒_ |



∑︁ Sim(q _,_ f ) _,_ (6)

_𝑓_ ∈F _𝑒_



where F _𝑒_ ⊆F _𝑟𝑒𝑡_ denotes the subset of retrieved facts that contain
entity _𝑒_ . If F _𝑒_ = ∅, we set _𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑒_ ) = 0.
**Type Node Initialization via Schemas:** We further initialize
type nodes _𝑡_ ∈G schema based on the retrieved schemas from M ont
to avoid introducing irrelevant semantics. A critical challenge is
that type nodes often exhibit exceptionally large degrees (e.g., a
generic “Person” node connected to thousands of entities). Directly
activating such high-degree nodes would spread importance across
overly many nodes, introducing significant noise. To address this


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su


**Table 1: Generation performance of different GraphRAG methods. The best result is bold, and the second is** **underline** **. The**
**column** Δ **indicates the performance gain of our MemGraphRAG (59.25) compared to each baseline. Background colors in** Δ
**columns represent the magnitude of improvement (Darker green = larger gap).**


**HotpotQA** **2WikiMultiHopQA** **MuSiQue** **G-Medical** **G-Novel** **Overall**
**Method**


Str-Acc. LLM-Acc. Str-Acc. LLM-Acc. Str-Acc. LLM-Acc. LLM-Acc. LLM-Acc. Avg. Δ


_**Direct Zero-shot LLM Inference**_


_**Vanilla Retrieval-Augmented-Generation**_


_**Graph-based Retrieval-Augmented-Generation Methods**_



issue, we introduce a structural regularization term that combines
semantic relevance with a log-degree penalty:



1

[�] �� |S _𝑡_ | _𝑠_ ∑︁ ∈S _𝑡_ Sim(q _,_ s)� [�] �


� **����������������������** �� **����������������������** �



1
×
log(deg( _𝑡_ ) + 1)

� **���������������** �� **���������������** �


Hub Suppression



_𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑡_ ) = [�] �
�



1

|S _𝑡_ |



∑︁



(7)



Schema Relevance



where S _𝑡_ denotes the retrieved schemas associated with _𝑡_ . This
design incorporates schema-level relevance while preventing overly
generic types from dominating propagation.
**Passage Node Initialization via Information Density:** Finally,
we initialize the Passage Nodes ( _𝑝_ ∈ _𝐺_ _𝑝𝑎𝑠_ ) by combining semantic
relevance with an information density prior:



�



_𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑝_ ) = Sim(q _,_ d _𝑝_ ) × _𝛼_ × _𝜎_



� _𝑒_ ∈E _𝑝_ [IDF][(] _[𝑒]_ [)]
� log(|E _𝑝_ | + 1)



(8)



_4.3.3_ _Personalized PageRank._ After initialization, we run Personalized PageRank (PPR) on the heterogeneous graph to propagate
query-specific importance. Starting from the normalized distribution v [(][0][)], the iteration is defined as v [(] _[𝑘]_ [+][1][)] = ( 1 − _𝜆_ ) Wv [(] _[𝑘]_ [)] + _𝜆_ v [(][0][)],
where W denotes the transition matrix and _𝜆_ is the damping factor.
We set _𝜆_ = 0 _._ 5 to limit propagation within a local neighborhood
and reduce semantic drift. After convergence, we select the top- _𝐾_
passages and top- _𝑀_ entities ranked by v [(∞)] for LLM inference.


**5** **Experiments**


In this section, our aim is to answer the following questions: **Q1**
(Generation Accuracy): How does MemGraphRAG perform compared to state-of-the-art GraphRAG methods in terms of generation performance? **Q2** (Retrieval Analysis): How does our retrieval
method compare to other frameworks in terms of performance and
efficiency? **Q3** (Graph Adaptability Analysis): Can the graph constructed by MemGraphRAG generalize to other GraphRAG methods? **Q4** (Ablation Study): What contribution does each component
of MemGraphRAG make to the overall performance? (Note that additional experiments and case studies are provided in Appendix A.)


**5.1** **Experimental Setting**


**Datasets.** We first evaluate the effectiveness of MemGraphRAG on
three widely-used multi-hop QA datasets, including HotpotQA [ 59 ],
2WikiMultiHopQA (2Wiki) [ 25 ], MuSiQue [ 47 ]. We follow the



� **�������������������** �� **�������������������** �


Information Density Term


This scoring function combines semantic alignment Sim( q _,_ d _𝑝_ ), a
dampening factor _𝛼_ (set to 0.05) to prevent passage nodes from dominating propagation, and an _Information Density Term_ that favors
passages containing rare and informative entities by aggregating
their IDF scores with log-normalization. Detailed initialization procedures are provided in Appendix E.1.


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.


**Table 2: Retrieval performance of different GraphRAG methods on G-Bench(Medical).**


**Fact Retrieval** **Complex Reasoning** **Contextual** **Creative Gen**
**Method** **Retrieval Time**

Recall Relevance Recall Relevance Recall Relevance Recall Relevance


RAPTOR [44] 85.40 69.38 89.70 53.20 88.86 58.73 72.70 52.71 0.171
Lazy-GraphRAG [8] 74.29 19.90 78.65 17.50 78.72 21.35 83.41 15.09 9.835
LightRAG [17] 80.32 41.27 82.91 42.79 85.71 43.11 81.34 45.17 11.052
HippoRAG [19] 87.25 52.44 83.80 42.19 83.46 49.13 81.66 45.03 1.586
HippoRAG2 [20] 78.70 87.96 77.00 80.94 77.40 86.85 61.12 78.64 2.157
GFM-RAG [37] **90.08** 57.90 85.03 33.06 78.62 40.14 83.51 22.87 1.375
LinearRAG [70] 88.86 86.09 87.03 81.58 89.13 **87.89** 89.08 72.74 0.123


**MemGraphRAG(ours)** 89.56 **88.53** **90.42** **82.64** **89.57** 86.91 **89.86** **79.12** **0.061**



settings used in [ 19, 20 ] for a fair comparison, choosing 1,000
questions from each validation set. We also test our approach
on G-Bench(Medical) and G-bench(Novel) [ 52 ] to evaluate MemGraphRAG on complex reasoning across medical, novel knowledge.
More details about datasets can be found in Appendix F.
**Baselines.** We categorize all baselines into three groups: (i) Zeroshot LLM Inference: We evaluate several foundational models in
cluding LLaMA3 (8B) and LLaMA3 (13B) [ 11 ], as well as GPT-3.5turbo and GPT-4o-mini [ 40 ]. (ii) We deploy Vanilla RAG across multiple retrieval configurations (retrieving 1, 3, or 5 top passages). (iii)
State-of-the-art GraphRAG Systems: We compare against leading
GraphRAG implementations, including KGP [ 51 ], G-retriever [ 24 ],
LightRAG [ 17 ], RAPTOR [ 44 ], MS-GraphRAG[ 12 ], HippoRAG [ 19,
20 ], GFM-RAG [ 37 ], LazyGRAG[ 8 ], E [2] GraphRAG [ 64 ], LogicRAG[ 6 ]
and LinearRAG[70].
**Evaluation Metrics.** We evaluate our method using four metrics across two categories. For QA performance, following existing
work[ 6, 70 ], we use: 1) String-based accuracy (Str-Acc.), which computes whether the gold answer is included in the generated answer
after normalizing them to lowercase words, and 2) LLM-based accuracy (LLM-Acc.), which lets an LLM decide whether the generated
answer correctly matches the gold answer. For GraphRAG-bench,
since golden answers consist of lengthy descriptive statements, we
only evaluate using LLM-ACC. For retrieval quality assessment, we
adopt metrics from GraphRAG-Bench [ 52 ]: 1) _Context Relevance_,
which measures semantic alignment between questions and retrieved passages, and 2) _Evidence Recall_, which evaluates whether
the retrieved contents contain all the necessary information that
used for generating the correct answer.
**Implementation Details.** For consistency, all methods use the
same embedding model ( _i.e._, NV-Embed-v2 [ 39 ]). We set _𝑘_ =5 for
top- _𝑘_ retrieval in all methods. For both offline indexing (graph
construction) and online generation, we adopt GPT-4o-mini as the
default LLM (additional open-source LLM results are reported in
Appendix A). For evaluation, we use GPT-4o-mini to compute the
LLM-Acc metric. To ensure reproducibility, we set the inference
temperature to 0 for all LLM calls.


**5.2** **Generation Accuracy (Q1)**


To address Q1, we conduct a comprehensive evaluation of generation performance by comparing various baseline methods with



MemGraphRAG across four benchmark datasets. The detailed experimental results are presented in Table 1. Based on our analysis,
we derive the following key observations.
**RAG system significantly enhances the LLM generation**
**performance.** Direct inference (without retrieval) yields the lowest
scores across all benchmarks. For instance, GPT-4o-mini achieves a
mere 14.65% average accuracy on MuSiQue in a zero-retrieval setting. Integrating retrieved contexts via Vanilla RAG (top-5) doubles
this performance to 30.15%. This confirms that retrieval augmentation is essential for knowledge-intensive tasks.
**Graph-based retrieval is more effective for multi-hop rea-**
**soning.** While increasing the retrieval count ( _𝑘_ ) improves Vanilla
RAG, the performance gains quickly plateau. This limitation stems
from Vanilla RAG’s reliance on surface-level keyword matching,
which often overlooks the logical bridges required for multi-hop
reasoning. In contrast, GraphRAG methods explicitly capture structural dependencies and consistently, and often deliver stronger
results. Notably, HippoRAG 2 emerges as a competitive baseline,
achieving 38.30% and 56.48% LLM-based accuracy on MuSiQue and
G-novel, respectively.
**MemGraphRAG consistently surpasses existing GraphRAG**
**baselines.** While exiting GraphRAGs attempt to align semantics
through graph structures, they are often sensitive to noise and
low-quality indexing introduced by solated chunk- level extraction.
In contrast, MemGraphRAG mitigates these issues by providing
more reliable indexing and retrieval, achieves the best results across
all datasets. It reaches 59.25% average accuracy, yielding a 2.10%
absolute gain over the strongest baseline.


**5.3** **Retrieval Analysis (Q2)**


To evaluate the retrieval performance of MemGraphRAG, we conducted tests across four distinct task levels on the GraphRAGBench. We utilized Recall and Relevance as metrics to assess the

GraphRAG’s capacity for retrieving both comprehensive and precise information. Additionally, to assess practical deployment feasibility, we recorded the average retrieval time (in seconds) across all
queries. The experimental results are presented in Table 2.
**MemGraphRAG achieves consistently strong retrieval per-**
**formance, balancing high recall with high relevance.** MemGraphRAG consistently ranks at the top in _Complex Reasoning_ tasks
(Recall: 90.42, Relevance: 82.64) and _Fact Retrieval_ tasks, significantly outperforming baselines such as HippoRAG2 and LightRAG.


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su


**Table 3: Adaptability Analysis: MemGraphRAG as a universal graph constructor across different frameworks. The** **blue rows**

**indicate experiments using MemGraphRAG’s constructed graph, while the** **purple row** **represents our full framework. The**
**rightmost column shows the performance gain.**


|GraphConstructor Retriever|HotpotQA 2Wiki MuSiQue G-Medical G-Novel Average Δ|
|---|---|
|HippoRAG [19]<br>HippoRAG [19]<br>MemGraphRAG<br>HippoRAG [19]<br>HippoRAG2 [20]<br>HippoRAG2 [20]<br>MemGraphRAG<br>HippoRAG2 [20]<br>MS-GraphRAG [12]<br>MS-GraphRAG [12]<br>MemGraphRAG<br>MS-GraphRAG [12]<br>LazyGraphRAG [8]<br>LazyGraphRAG [8]<br>MemGraphRAG<br>LazyGraphRAG [8]|59.90<br>64.40<br>28.20<br>57.06<br>45.77<br>51.07<br>**+8.61**<br>60.65<br>65.25<br>29.00<br>57.75<br>46.24<br>51.78<br>**+7.90**<br>66.20<br>61.05<br>35.25<br>64.85<br>56.48<br>56.77<br>**+2.91**<br>66.00<br>61.20<br>35.40<br>65.42<br>**56.76**<br>56.96<br>**+2.72**<br>47.55<br>42.95<br>22.15<br>55.67<br>50.43<br>43.75<br>**+15.93**<br>48.00<br>43.20<br>22.45<br>56.53<br>50.88<br>44.21<br>**+15.47**<br>48.25<br>42.35<br>23.15<br>56.63<br>51.56<br>44.39<br>**+15.29**<br>48.75<br>42.55<br>23.50<br>57.98<br>52.06<br>44.97<br>**+14.71**|
|MemGraphRAG<br>MemGraphRAG|**69.40**<br>**70.05**<br>**36.15**<br>**68.40**<br>54.41<br>**59.68**<br>**-**|



These results indicate that our approach effectively filters noise
and invalid entity relationships, enabling the system to precisely
pinpoint entities and relations relevant to the query. Unlike methods that sacrifice precision for coverage, MemGraphRAG maintains
superior relevance while capturing broad context, thereby validating the effectiveness of our _Global Adjudication_ mechanism for
consistency maintenance in constructing high-quality graphs.
**MemGraphRAG achieves the lowest retrieval latency, show-**
**ing superior online inference efficiency.** MemGraphRAG requires an average of only 0.061 seconds per retrieval, which is significantly faster than LightRAG (11.052s) and HippoRAG (1.586s). This
efficiency is attributed to our lightweight retrieval process, which
relies on efficient Personalized PageRank (PPR) rather than computationally expensive real-time LLM filtering or iterative reasoning
loops. Consequently, MemGraphRAG delivers high-precision complex reasoning while maintaining low latency in practice.


**5.4** **Indexing Graph Adaptability Analysis (Q3)**


To evaluate whether our constructed index graph can seamlessly
adapt to different GraphRAG frameworks, we conducted a transferability experiment. Our pilot study previously identified that
existing graph construction methods suffer from critical deficiencies, including Thematic Irrelevance, Logical Inconsistency, and
Structural Fragmentation. Consequently, we assess whether the
structural unification enabled by MemGraphRAG through MemoryGuided Bridging can mitigate these issues for other frameworks.
Specifically, we replaced the native graph construction modules
of HippoRAG, HippoRAG2, MS-GraphRAG, and LazyGraphRAG
with the graph constructed by MemGraphRAG, while retaining
their original downstream retrieval and reasoning mechanisms.
The comparative experimental results are presented in Table 3.
**MemGraphRAG consistently improves retrieval perfor-**
**mance across all evaluated GraphRAG frameworks, serving**
**as a universal high-quality graph constructor.** As shown in
the results, replacing the original graphs with MemGraphRAGconstructed graphs leads to consistent improvements for all baseline
retrievers across all datasets. For instance, the average performance
of HippoRAG increases from 51.07 to 51.78, and MS-GraphRAG
improves from 43.75 to 44.21. This consistent improvement shows
that our memory-driven global construction mechanism effectively



**Figure 5: Ablation study of MemGraphRAG on three datasets.**


mitigates structural fragmentation and logical inconsistencies. By
producing a more cohesive and thematically aligned knowledge
structure, MemGraphRAG substantially strengthens the effectiveness of existing retrievers, demonstrating its robustness as a foundational indexing solution.


**5.5** **Ablation Study (Q4)**


To verify the contribution of each module in MemGraphRAG, we
conduct an ablation study on HotpotQA, 2WikiMultiHopQA, and
G-Medical. We compare the full model with four variants that
remove the _Schema Filter_, _Conflict Resolution_, _Hub Suppression_, and
the _Information Density Term_, respectively. As shown in Figure 5,
MemGraphRAG consistently achieves the best performance across
all datasets (e.g., 69.40% on HotpotQA), which indicates that these
memory-driven graph construction and initialization mechanisms
are jointly crucial for building a robust knowledge graph.
**w/o Schema Filter:** Removing _Unified Schema Filtering_ causes a
clear degradation, especially on 2WikiMultiHopQA and G-Medical
(68.10% and 65.92%). Without the frequency-based stability constraint ( Freq( _𝑠_ ) ≥ _𝜏_ ), low-frequency and off-topic schemas are
retained, introducing noisy triples that weaken semantic focus.
**w/o Conflict Resolution:** Excluding _Global Adjudication_ leads
to the largest drop on HotpotQA (66.95%). Without conflict detection and resolution, the fact layer accumulates contradictory or
redundant triples, which disrupts multi-hop reasoning chains and
increases the chance of retrieving inconsistent evidence.


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.



**w/o Hub Suppression:** Removing _Hub Suppression_ reduces accuracy (67.22% on HotpotQA). Without degree-based regularization,
generic high-degree nodes dominate propagation, causing semantic
drift toward irrelevant subgraphs.
**w/o Information Density Term:** Dropping the _Information_
_Density Term_ yields a smaller but consistent decline (68.67% on
HotpotQA). Without IDF-style weighting, passage initialization
cannot prioritize discriminative evidence, weakening the model’s
ability to anchor reasoning on informative documents.


**6** **Conclusion**


In this paper, we propose MemGraphRAG, a novel GraphRAG
framework that integrates a global memory mechanism into the
knowledge graph construction process. By leveraging a shared hierarchical memory structure, our multi-agent system collaboratively
maintains a global perspective throughout both the extraction and
retrieval phases. This paradigm effectively overcomes key limitations of traditional GraphRAG approaches that rely on isolated
local extraction. It systematically mitigates thematic irrelevance,
logical inconsistency, and structural fragmentation, thereby enabling a globally consistent indexing graph. Extensive experiments
demonstrate that MemGraphRAG consistently outperforms stateof-the-art baselines in terms of graph quality, retrieval precision,
and generation accuracy, providing a robust solution for deploying
reliable RAG systems in complex real-world scenarios.


**Limitation**


While MemGraphRAG demonstrates strong robustness in processing large-scale textual corpora and constructing globally consistent
knowledge graphs, its current design is limited to unimodal textual
inputs. However, real-world knowledge repositories are inherently
multimodal, containing heterogeneous formats such as statistical
charts, technical diagrams, document layouts, and embedded images in academic papers or financial reports. Currently, our framework requires non-textual elements to be transcribed or described
in text before processing, which may lead to the loss of critical visual semantics and spatial relationships. For example, quantitative
trends in line charts or complex structures in scientific diagrams
often contain dense information that textual descriptions cannot
fully capture, potentially causing information loss during indexing.
Extending the _Global Hierarchical Graph_ to incorporate multimodal
nodes (e.g., embedding visual patches into the _Fact Layer_ M _𝑓𝑎𝑐_ or
the _Passage Layer_ M _𝑝𝑎𝑠_ ) is a promising direction for future work.
Such an extension could enable cross-modal reasoning, allowing the
multi-agent system to verify textual claims against visual evidence
and further improve the versatility of MemGraphRAG.


**Acknowledgments**


The project was supported by Natural Science Foundation of Fujian
Province of China (No. 2024J011001) and the Public Technology
Service Platform Project of Xiamen (No.3502Z20231043). We also
thank the reviewers for their insightful comments.


**References**


[1] Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. 2023.
Self-rag: Learning to retrieve, generate, and critique through self-reflection. In
_International Conference on Learning Representations (ICLR)_ .




[2] Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George Bm Van Den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, et al . 2022. Improving language models by retrieving
from trillions of tokens. In _International Conference on Machine Learning (ICML)_ .

[3] Mingyang Chen, Linzhuang Sun, Tianpeng Li, Haoze Sun, Yijie Zhou, Chenzheng
Zhu, Haofen Wang, Jeff Z. Pan, Wen Zhang, Huajun Chen, Fan Yang, Zenan
Zhou, and Weipeng Chen. 2025. ReSearch: Learning to Reason with Search for
[LLMs via Reinforcement Learning. arXiv:2503.19470 [cs.AI] https://arxiv.org/](https://arxiv.org/abs/2503.19470)
[abs/2503.19470](https://arxiv.org/abs/2503.19470)

[4] Shengyuan Chen, Zheng Yuan, Qinggang Zhang, Wen Hua, Jiannong Cao, and
Xiao Huang. 2025. Neuro-Symbolic Entity Alignment via Variational Inference.
_The Thirty-ninth Annual Conference on Neural Information Processing Systems_
(2025).

[5] Shengyuan Chen, Qinggang Zhang, Junnan Dong, Wen Hua, Qing Li, and Xiao
Huang. 2024. Entity alignment with noisy annotations from large language
models. _The Thirty-Eighth Annual Conference on Neural Information Processing_
_Systems_ (2024).

[6] Shengyuan Chen, Chuang Zhou, Zheng Yuan, Qinggang Zhang, Zeyang Cui, Hao
Chen, Yilin Xiao, Jiannong Cao, and Xiao Huang. 2025. You Don’t Need Pre-built
Graphs for RAG: Retrieval Augmented Generation with Adaptive Reasoning
Structures. _arXiv preprint arXiv:2508.06105_ (2025).

[7] CircleMind-AI. 2024. FastGraphRAG: High-speed graph-based retrievalaugmented generation. _CircleMind-AI Blog_ (2024).

[8] Jonathan Larson Darren Edge, Ha Trinh. 2024. LazyGraphRAG: Setting a new
standard for quality and cost. _Microsoft Blog_ (2024).

[9] Junnan Dong, Siyu An, Yifei Yu, Qian-Wen Zhang, Linhao Luo, Xiao Huang,
Yunsheng Wu, Di Yin, and Xing Sun. 2025. Youtu-GraphRAG: Vertically Unified
[Agents for Graph Retrieval-Augmented Complex Reasoning. arXiv:2508.19855](https://arxiv.org/abs/2508.19855)
[https://arxiv.org/abs/2508.19855](https://arxiv.org/abs/2508.19855)

[10] Su Dong, Qinggang Zhang, Yilin Xiao, Shengyuan Chen, Chuang Zhou, and Xiao
Huang. 2026. Use Graph When It Needs: Efficiently and Adaptively Integrating
Retrieval-Augmented Generation with Graphs. _arXiv preprint arXiv:2602.03578_
(2026).

[11] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan,
et al. 2024. The llama 3 herd of models. _arXiv e-prints_ (2024), arXiv–2407.

[12] Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva
Mody, Steven Truitt, and Jonathan Larson. 2024. From local to global: A graph
rag approach to query-focused summarization. _arXiv preprint arXiv:2404.16130_
(2024).

[13] Junfeng Fang, Houcheng Jiang, Kun Wang, Yunshan Ma, Shi Jie, Xiang Wang,
Xiangnan He, and Tat-Seng Chua. 2024. Alphaedit: Null-space constrained
knowledge editing for language models. _arXiv preprint arXiv:2410.02355_ (2024).

[14] Junfeng Fang, Yukai Wang, Ruipeng Wang, Zijun Yao, Kun Wang, An Zhang,
Xiang Wang, and Tat-Seng Chua. 2025. Safemlrm: Demystifying safety in multimodal large reasoning models. _arXiv preprint arXiv:2504.08813_ (2025).

[15] Linfeng Gao, Baolong Bi, Zheng Yuan, Le Wang, Zerui Chen, Zhimin Wei,
Shenghua Liu, Qinggang Zhang, and Jinsong Su. 2025. Probing Latent Knowledge Conflict for Faithful Retrieval-Augmented Generation. _arXiv preprint_
_arXiv:2510.12460_ (2025).

[16] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai,
Jiawei Sun, and Haofen Wang. 2023. Retrieval-augmented generation for large
language models: A survey. _arXiv preprint arXiv:2312.10997_ (2023).

[17] Zirui Guo, Lianghao Xia, Yanhua Yu, Tu Ao, and Chao Huang. 2024. LightRAG:
Simple and Fast Retrieval-Augmented Generation. _arXiv preprint arXiv:2410.05779_
(2024).

[18] Anton Gusarov, Anastasia Volkova, Valentin Khrulkov, Andrey Kuznetsov, Evgenii Maslov, and Ivan Oseledets. 2025. Multi-Agent GraphRAG: A Text-toCypher Framework for Labeled Property Graphs. [arXiv:2511.08274 [cs.AI]](https://arxiv.org/abs/2511.08274)
[https://arxiv.org/abs/2511.08274](https://arxiv.org/abs/2511.08274)

[19] Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su.
2024. HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. In _Advances in Neural Information Processing Systems (NeurIPS)_ .

[20] Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. 2025.
From rag to memory: Non-parametric continual learning for large language
models. _arXiv preprint arXiv:2502.14802_ (2025).

[21] Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Ming-Wei
Chang. 2020. REALM: Retrieval-Augmented Language Model Pre-Training.
[arXiv:2002.08909 [cs.CL] https://arxiv.org/abs/2002.08909](https://arxiv.org/abs/2002.08909)

[22] Haoyu Han, Harry Shomer, Yu Wang, Yongjia Lei, Kai Guo, Zhigang Hua, Bo
Long, Hui Liu, and Jiliang Tang. 2025. Rag vs. graphrag: A systematic evaluation
and key insights. _arXiv preprint arXiv:2502.11371_ (2025).

[23] Haoyu Han, Yu Wang, Harry Shomer, Kai Guo, Jiayuan Ding, Yongjia Lei, Mahantesh Halappanavar, Ryan A Rossi, Subhabrata Mukherjee, Xianfeng Tang, et al .
2024. Retrieval-augmented generation with graphs (graphrag). _arXiv preprint_
_arXiv:2501.00309_ (2024).

[24] Xiaoxin He, Yijun Tian, Yifei Sun, Nitesh V Chawla, Thomas Laurent, Yann
LeCun, Xavier Bresson, and Bryan Hooi. 2024. G-retriever: Retrieval-augmented


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su



generation for textual graph understanding and question answering. _arXiv_
_preprint arXiv:2402.07630_ (2024).

[25] Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. 2020.
Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning
steps. _arXiv preprint arXiv:2011.01060_ (2020).

[26] Zijin Hong, Zheng Yuan, Qinggang Zhang, Hao Chen, Junnan Dong, Feiran
Huang, and Xiao Huang. 2024. Next-Generation Database Interfaces: A Survey
of LLM-based Text-to-SQL. _arXiv preprint arXiv:2406.08426_ (2024).

[27] Gautier Izacard, Patrick Lewis, Maria Lomeli, Lucas Hosseini, Fabio Petroni, Timo
Schick, Jane Dwivedi-Yu, Armand Joulin, Sebastian Riedel, and Edouard Grave.
2023. Atlas: Few-shot learning with retrieval augmented language models. _The_
_Journal of Machine Learning Research (JMLR)_ (2023).

[28] Houcheng Jiang, Junfeng Fang, Ningyu Zhang, Guojun Ma, Mingyang Wan, Xiang
Wang, Xiangnan He, and Tat-seng Chua. 2025. AnyEdit: Edit Any Knowledge
Encoded in Language Models. _ICML_ (2025).

[29] Zhengbao Jiang, Frank F Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu,
Yiming Yang, Jamie Callan, and Graham Neubig. 2023. Active retrieval augmented
generation. In _Empirical Methods in Natural Language Processing (EMNLP)_ .

[30] Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan Arik, Dong Wang,
Hamed Zamani, and Jiawei Han. 2025. Search-R1: Training LLMs to Reason and
[Leverage Search Engines with Reinforcement Learning. arXiv:2503.09516 [cs.CL]](https://arxiv.org/abs/2503.09516)
[https://arxiv.org/abs/2503.09516](https://arxiv.org/abs/2503.09516)

[31] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,
Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al .
2020. Retrieval-augmented generation for knowledge-intensive nlp tasks. In
_Advances in Neural Information Processing Systems (NeurIPS)_ .

[32] Xiaoxi Li, Guanting Dong, Jiajie Jin, Yuyao Zhang, Yujia Zhou, Yutao Zhu, Peitian
Zhang, and Zhicheng Dou. 2025. Search-o1: Agentic Search-Enhanced Large
[Reasoning Models. arXiv:2501.05366 [cs.AI] https://arxiv.org/abs/2501.05366](https://arxiv.org/abs/2501.05366)

[33] Lei Liang, Mengshu Sun, Zhengke Gui, Zhongshu Zhu, Zhouyu Jiang, Ling Zhong,
Yuan Qu, Peilong Zhao, Zhongpu Bo, Jin Yang, et al . 2024. Kag: Boosting llms
in professional domains via knowledge augmented generation. _arXiv preprint_
_arXiv:2409.13731_ (2024).

[34] Yujie Lin, Kunquan Li, YiXuan Liao, Xiaoxin Chen, and Jinsong Su. 2026. Bidirectional Bias Attribution: Debiasing Large Language Models without Modifying Prompts. In _The Fourteenth International Conference on Learning Representa-_
_tions_ [. https://openreview.net/forum?id=mUTN9VIaSy](https://openreview.net/forum?id=mUTN9VIaSy)

[35] Yujie Lin, Chengyi Yang, Zhishang Xiang, Yiping Song, and Jinsong Su. 2026.
ZeroUnlearn: Few-Shot Knowledge Unlearning in Large Language Models.
[arXiv:2605.18879 [cs.LG] https://arxiv.org/abs/2605.18879](https://arxiv.org/abs/2605.18879)

[36] LINHAO LUO, Yuan-Fang Li, Reza Haf, and Shirui Pan. 2024. Reasoning on
Graphs: Faithful and Interpretable Large Language Model Reasoning. In _The_
_Twelfth International Conference on Learning Representations_ .

[37] Linhao Luo, Zicheng Zhao, Gholamreza Haffari, Dinh Phung, Chen Gong, and
Shirui Pan. 2025. GFM-RAG: graph foundation model for retrieval augmented
generation. _arXiv preprint arXiv:2502.01113_ (2025).

[38] Renqiang Luo, Huafei Huang, Shuo Yu, Fengqi Yu, Feng Xia, Sajal K. Das, and
Chengqi Zhang. 2026. Utility-Preserving Federated Graph Learning with DualPerspective Fairness. _IEEE Transactions on Pattern Analysis and Machine Intelli-_
_gence_ (2026).

[39] Gabriel de Souza P Moreira, Radek Osmulski, Mengyao Xu, Ronay Ak, Benedikt
Schifferer, and Even Oldridge. 2024. NV-Retriever: Improving text embedding
models with effective hard-negative mining. _arXiv preprint arXiv:2407.15831_
(2024).

[40] OpenAI. 2023. GPT-4 Technical Report. _OpenAI Blog_ (2023).

[41] Tyler Thomas Procko and Omar Ochoa. 2024. Graph retrieval-augmented generation for large language models: A survey. In _Conference on AI, Science, Engineering,_
_and Technology (AIxSET)_ .

[42] Hongjin Qian, Zheng Liu, Peitian Zhang, Kelong Mao, Defu Lian, Zhicheng Dou,
and Tiejun Huang. 2025. MemoRAG: Boosting Long Context Processing with
[Global Memory-Enhanced Retrieval Augmentation. arXiv:2409.05591 [cs.CL]](https://arxiv.org/abs/2409.05591)
[https://arxiv.org/abs/2409.05591](https://arxiv.org/abs/2409.05591)

[43] Meng Qu and Jian Tang. 2019. Probabilistic Logic Neural Networks for Reasoning. In _Advances in Neural Information Processing Systems (NeurIPS)_ . Vancouver,
Canada, 7710–7720.

[44] Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and
Christopher D. Manning. 2024. RAPTOR: Recursive Abstractive Processing for
Tree-Organized Retrieval. In _International Conference on Learning Representations_
_(ICLR)_ .

[45] Kartik Sharma, Peeyush Kumar, and Yunqing Li. 2024. OG-RAG: OntologyGrounded Retrieval-Augmented Generation For Large Language Models. _arXiv_
_preprint arXiv:2412.15235_ (2024).

[46] Jiashuo Sun, Chengjin Xu, Lumingyuan Tang, Saizhuo Wang, Chen Lin, Yeyun
Gong, Lionel Ni, Heung-Yeung Shum, and Jian Guo. 2024. Think-on-Graph: Deep
and Responsible Reasoning of Large Language Model on Knowledge Graph. In
_International Conference on Learning Representations (ICLR)_ .

[47] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal.
2022. MuSiQue: Multi-hop Questions via Single-hop Question Composition.



_Transactions of the Association for Computational Linguistics_ 10 (2022), 539–554.

[48] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal.
2023. Interleaving retrieval with chain-of-thought reasoning for knowledgeintensive multi-step questions. In _Proceedings of the 61st annual meeting of the_
_association for computational linguistics (volume 1: long papers)_ . 10014–10037.

[49] Hong Ting Tsang, Jiaxin Bai, Haoyu Huang, Qiao Xiao, Tianshi Zheng, Baixuan
Xu, Shujie Liu, and Yangqiu Song. 2025. AutoGraph-R1: End-to-End Reinforce[ment Learning for Knowledge Graph Construction. arXiv:2510.15339 [cs.CL]](https://arxiv.org/abs/2510.15339)
[https://arxiv.org/abs/2510.15339](https://arxiv.org/abs/2510.15339)

[50] Shu Wang, Yixiang Fang, Yingli Zhou, Xilin Liu, and Yuchi Ma. 2025. ArchRAG:
Attributed Community-based Hierarchical Retrieval-Augmented Generation.
_arXiv preprint arXiv:2502.09891_ (2025).

[51] Yu Wang, Nedim Lipka, Ryan A Rossi, Alexa Siu, Ruiyi Zhang, and Tyler Derr.
2024. Knowledge graph prompting for multi-document question answering. In
_Conference on Artificial Intelligence (AAAI)_ .

[52] Zhishang Xiang, Chuanjie Wu, Qinggang Zhang, Shengyuan Chen, Zijin Hong,
Xiao Huang, and Jinsong Su. 2025. When to use graphs in rag: A comprehensive analysis for graph retrieval-augmented generation. _arXiv preprint_
_arXiv:2506.05690_ (2025).

[53] Zhishang Xiang, Chengyi Yang, Zerui Chen, Zhimin Wei, Yunbo Tang, Zongpei
Teng, Zexi Peng, Zongxia Li, Chengsong Huang, Yicheng He, et al . 2026. A
Systematic Survey of Self-Evolving Agents: From Model-Centric to EnvironmentDriven Co-Evolution. (2026).

[54] Yilin Xiao, Chuang Zhou, Qinggang Zhang, Su Dong, Shengyuan Chen, and Xiao
Huang. 2025. LAG: Logic-Augmented Generation from a Cartesian Perspective.
_arXiv preprint arXiv:2508.05509_ (2025).

[55] Yilin Xiao, Chuang Zhou, Qinggang Zhang, Bo Li, Qing Li, and Xiao Huang. 2025.
Reliable Reasoning Path: Distilling Effective Guidance for LLM Reasoning with
[Knowledge Graphs. arXiv:2506.10508 [cs.CL]](https://arxiv.org/abs/2506.10508)

[56] Cehao Yang, Xiaojun Wu, Xueyuan Lin, Chengjin Xu, Xuhui Jiang, Yuanliang Sun,
Jia Li, Hui Xiong, and Jian Guo. 2025. GraphSearch: An Agentic Deep Searching
[Workflow for Graph Retrieval-Augmented Generation. arXiv:2509.22009 [cs.CL]](https://arxiv.org/abs/2509.22009)
[https://arxiv.org/abs/2509.22009](https://arxiv.org/abs/2509.22009)

[57] Chang Yang, Chuang Zhou, Yilin Xiao, Su Dong, Luyao Zhuang, Yujing Zhang,
Zhu Wang, Zijin Hong, Zheng Yuan, Zhishang Xiang, et al . 2026. Graphbased Agent Memory: Taxonomy, Techniques, and Applications. _arXiv preprint_
_arXiv:2602.05665_ (2026).

[58] Diji Yang, Jinmeng Rao, Kezhen Chen, Xiaoyuan Guo, Yawen Zhang, Jie Yang, and
Yi Zhang. 2024. Im-rag: Multi-round retrieval-augmented generation through
learning inner monologues. In _Proceedings of the 47th International ACM SIGIR_
_Conference on Research and Development in Information Retrieval_ . 730–740.

[59] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan
Salakhutdinov, and Christopher D Manning. 2018. HotpotQA: A dataset for diverse, explainable multi-hop question answering. In _Empirical Methods in Natural_
_Language Processing (EMNLP)_ .

[60] Zheng Yuan, Hao Chen, Zijin Hong, Qinggang Zhang, Feiran Huang, Qing Li, and
Xiao Huang. 2025. Knapsack optimization-based schema linking for llm-based
Text-to-SQL generation. _arXiv preprint arXiv:2502.12911_ (2025).

[61] Fangyuan Zhang, Zhengjun Huang, Yingli Zhou, Qintian Guo, Zhixun Li, Wensheng Luo, Di Jiang, Yixiang Fang, and Xiaofang Zhou. 2025. EraRAG: Efficient
and Incremental Retrieval Augmented Generation for Growing Corpora. _arXiv_
_preprint arXiv:2506.20963_ (2025).

[62] Qinggang Zhang, Shengyuan Chen, Yuanchen Bei, Zheng Yuan, Huachi Zhou,
Zijin Hong, Junnan Dong, Hao Chen, Yi Chang, and Xiao Huang. 2025. A Survey of Graph Retrieval-Augmented Generation for Customized Large Language
Models. _arXiv preprint arXiv:2501.13958_ (2025).

[63] Qinggang Zhang, Zhishang Xiang, Yilin Xiao, Le Wang, Junhui Li, Xinrun Wang,
and Jinsong Su. 2025. FaithfulRAG: Fact-Level Conflict Modeling for ContextFaithful Retrieval-Augmented Generation. _arXiv preprint arXiv:2506.08938_ (2025).

[64] Yibo Zhao, Jiapeng Zhu, Ye Guo, Kangkang He, and Xiang Li. 2025. Eˆ 2GraphRAG:
Streamlining Graph-based RAG for High Efficiency and Effectiveness. _arXiv_
_preprint arXiv:2505.24226_ (2025).

[65] Baolin Zheng, Guanlin Chen, Hongqiong Zhong, Qingyang Teng, Yingshui Tan,
Zhendong Liu, Weixun Wang, Jiaheng Liu, Jian Yang, Huiyun Jing, et al . 2025.
USB: A Comprehensive and Unified Safety Evaluation Benchmark for Multimodal
Large Language Models. _arXiv preprint arXiv:2505.23793_ (2025).

[66] Qihuang Zhong, Haiyun Li, Luyao Zhuang, Juhua Liu, and Bo Du. 2024. Iterative
data generation with large language models for aspect-based sentiment analysis.
_arXiv preprint arXiv:2407.00341_ (2024).

[67] Chulun Zhou, Qiujing Wang, Mo Yu, Xiaoqian Yue, Rui Lu, Jiangnan Li, Yifan
Zhou, Shunchi Zhang, Jie Zhou, and Wai Lam. 2025. The essence of contextual understanding in theory of mind: A study on question answering with
story characters. In _Proceedings of the 63rd Annual Meeting of the Association for_
_Computational Linguistics (Volume 1: Long Papers)_ . 22612–22631.

[68] Chulun Zhou, Chunkang Zhang, Guoxin Yu, Fandong Meng, Jie Zhou, Wai Lam,
and Mo Yu. 2025. Improving Multi-step RAG with Hypergraph-based Memory
for Long-Context Complex Relational Modeling. _arXiv preprint arXiv:2512.23959_
(2025).


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.




[69] Yingli Zhou, Yaodong Su, Youran Sun, Shu Wang, Taotao Wang, Runyuan He,
Yongwei Zhang, Sicong Liang, Xilin Liu, Yuchi Ma, et al . 2025. In-depth Analysis
of Graph-based RAG in a Unified Framework. _arXiv preprint arXiv:2503.04338_
(2025).

[70] Luyao Zhuang, Shengyuan Chen, Yilin Xiao, Huachi Zhou, Yujing Zhang, Hao
Chen, Qinggang Zhang, and Xiao Huang. 2025. LinearRAG: Linear Graph
Retrieval Augmented Generation on Large-scale Corpora. _arXiv preprint_
_arXiv:2510.10114_ (2025).


**A** **Additional Experiments**

**A.1** **Ablation on Backbone LLMs**


To further evaluate the universality and robustness of MemGraphRAG,
we conducted experiments utilizing the stronger llama-3-70binstruct as the underlying backbone model. We compared our
method against a comprehensive suite of baselines, ranging from
non-structured methods (e.g., Vanilla RAG) to state-of-the-art graphbased approaches (e.g., HippoRAG2, E2GraphRAG). The results are
detailed in Table 4.

**MemGraphRAG consistently achieves state-of-the-art per-**
**formance across all evaluated datasets, highlighting its com-**
**patibility and robustness across different backbone models.**
As shown in the table, MemGraphRAG achieves the highest average
performance of 58.41%, significantly outperforming the strongest
baseline, HippoRAG2 (55.41%), and surpassing standard graphbased methods like LightRAG (47.81%) by a substantial margin.
First, compared to non-structured methods, our approach exhibits
a dominant advantage over Vanilla RAG (Top-5 average: 47.52%),
validating that our memory-driven graph structure effectively captures long-range dependencies that vector retrieval misses. Second,
in the realm of graph-based RAG, MemGraphRAG excels particularly in multi-hop reasoning tasks. On the 2WikiMultiHopQA
dataset, we achieve a Containment Accuracy of 69.40% and an LLM
Accuracy of 66.80%, notably higher than HippoRAG2 (61.90% and
54.40%, respectively). This indicates that our method constructs
a more connected and logically coherent graph, enabling the retriever to accurately locate multi-hop evidence chains. Furthermore,
on domain-specific datasets like G-Medical, MemGraphRAG maintains its lead (67.13%), proving its robustness in handling specialized
knowledge. Collectively, these results confirm that MemGraphRAG
provides a high-quality, globally consistent indexing structure that
universally enhances the reasoning capabilities of LLMs.


**A.2** **Graph Analysis**


To more intuitively assess the quality of the index graphs produced
by our memory-based construction approach, we analyze their
topological properties and compare MemGraphRAG with existing
baselines in terms of connectivity, redundancy, and semantic aggregation. Following previous study [ 52 ], we assessed the Average
Degree and Average Clustering Coefficient of the index graphs
constructed by various GraphRAG frameworks on the G-Medical
and G-Novel datasets. The comparative results are presented in
Table 5 and Figure 6.
**MemGraphRAG demonstrates superior entity-level con-**
**nectivity compared to existing GraphRAG methods.** MemGraphRAG achieves the highest Average Degree on both datasets,
reaching 14.37 on the Medical dataset (surpassing HippoRAG2’s
13.31) and 9.26 on the Novel dataset (surpassing HippoRAG2’s 8.75).



This improvement indicates that our memory consistency maintenance mechanism effectively links entities scattered across different
document chunks. As a result, it bridges fragmented subgraphs and
enables more robust long-range reasoning paths.
**MemGraphRAG demonstrates superior subgraph-level se-**
**mantic clustering than existing GraphRAG methods.** MemGraphRAG also attains the highest Average Clustering Coefficients,
with 0.865 on the G-Novel and 0.527 on the G-Medical. These re
sults indicate that nodes in MemGraphRAG tend to share common
neighbors, leading to denser local connectivity and clearer semantic clusters. This further shows that MemGraphRAG integrates
dispersed knowledge into a more unified and highly structured
index graph, instead of yielding sparse graphs composed of loosely
related facts.


**Figure 6: Multi-dimensional assessment of graph quality.**


**A.3** **Case Study**


We conduct a qualitative analysis in Table 6 and Table 7 to illustrate
how MemGraphRAG overcomes the limitations of isolated extraction by ensuring logical consistency and thematic purity through
its global memory mechanism.
1) **Case Study on Conflict Resolution.** Table 6 illustrates a
representative scenario of Mutually Exclusive Conflict, where disparate documents claim conflicting birth years for the same entity
("1645" vs. "1643"). Traditional pipelines simply aggregate these contradictions, leading to ambiguous reasoning paths. MemGraphRAG
addresses this through Global Adjudication. Upon detecting the
conflict, the Resolution Agent ( _𝐴_ _𝑟𝑒𝑠_ ) retrieves the original provenance from the Passage Layer ( _𝑀_ _𝑝𝑎𝑠_ ) and validates the correct fact
("1643") before indexing. This mechanism effectively eliminates
logical incoherence, enabling the retriever to provide an accurate
context for the LLM.

2) **Case Study on Thematic Denoising.** In domain-specific
tasks (e.g., medical protocols), LLMs often extract irrelevant noise
alongside core facts. As shown in Table 6, the baseline graph is polluted by irrelevant triples (e.g., Patient prefers Tea), which distracts
the retrieval process. MemGraphRAG mitigates this via Unified
Schema Filtering. By treating extracted schemas as candidate and
only stabilizing those that exceed a frequency threshold ( _𝜏_ ), our


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su


**Table 4: Comparison of different methods. The column** Δ **shows the improvement of MemGraphRAG (58.41) over baselines.**
**Darker green in** Δ **indicates a larger performance gap.**


**HotpotQA** **2WikiMultiHopQA** **MuSiQue** **G-Medical** **G-Novel** **Overall**
**Method**

Contain-Acc. LLM-Acc. Contain-Acc LLM-Acc Contain-Acc LLM-Acc LLM-Acc LLM-Acc Avg. Δ


_**Non-structure Methods**_


_**Graph-based RAG Methods**_



**Table 5: Quality evaluation of indexing graph construction**
**in GraphRAG frameworks.**


**Method** **G-Novel** **G-Medical** **HotpotQA**

**Degree** **Clust. Coeff** **Degree** **Clust. Coeff** **Degree** **Clust. Coeff**


**MS-GraphRAG** [12] 1.48 0.315 1.82 0.300 1.56 0.334
**HippoRAG2** [20] 8.75 0.657 13.31 0.497 7.96 0.613
**LightRAG** [17] 2.10 0.212 2.58 0.139 2.18 0.236
**Fast-GraphRAG** [7] 3.19 0.324 5.50 0.347 3.04 0.336
**HippoRAG** [19] 1.73 0.100 2.06 0.087 1.86 0.140


**MemGraphRAG(ours)** **9.26** **0.865** **14.37** **0.527** **8.92** **0.725**


system successfully filters out irrelevant noise while retaining sta_𝑡𝑟𝑒𝑎𝑡𝑠_
ble clinical patterns (e.g., _𝐷𝑟𝑢𝑔_ −−−−−→ _𝐷𝑖𝑠𝑒𝑎𝑠𝑒_ ). This results in a
cleaner Fact Graph ( _𝐺_ _𝑓𝑎𝑐_ ) that strictly follows the domain ontology,
significantly improving retrieval precision.


**B** **Related Work**

**B.1** **Retrieval-Augmented Generation**


While Large Language Models (LLMs) have demonstrated impressive capabilities, they remain prone to hallucination [ 10, 13 – 15, 26,
28, 34, 35, 60, 65, 66 ]. Retrieval-Augmented Generation (RAG) mitigates this by grounding generation in external evidence [ 2, 21, 27,
42, 61, 67, 68 ]. However, effectively organizing fragmented knowledge from distributed documents to support complex reasoning
remains a persistent challenge.
To address this, recent research has evolved from simple retrieval
to Reasoning-enhanced RAG [ 1, 3, 30, 32, 53 ]. Departing from static
index construction, this paradigm focuses on interleaving the retrieval process with the logical flow of the LLM. Several approaches
optimize the retrieval process through Chain-of-Thought prompting, recursive inner monologues, or logical decomposition, such as
IRCoT [ 48 ], IM-RAG [ 58 ], and LAG [ 54 ]. LogicRAG [ 6 ] advances
this direction by eliminating pre-built graphs entirely, instead constructing a reasoning Directed Acyclic Graph (DAG) dynamically



at inference time to enable adaptive retrieval planning. While effective, these methods typically operate within the constraints of
fixed resources or rely on the LLM’s inherent reasoning capabilities
rather than structured knowledge representation.


**B.2** **Graph Retrieval-Augmented Generation**


To overcome the limitations of unstructured text chunks, GraphRAG
focuses on explicit graph structure construction to capture global
dependencies and structural patterns. Current approaches can be
categorized into two primary construction paradigms:
**Relation-extraction-based Construction.** This line of work [ 6,
17 – 19, 38, 49, 55, 56, 64, 69 ] structures text corpora into Knowledge
Graphs (KGs) by extracting triples to form atomic knowledge units.
These units are subsequently unified via entity alignment [ 4, 5 ],
enabling the application of sophisticated graph reasoning algorithms [ 36, 43, 46 ]. Some methods augment reasoning by integrating
these static KGs as navigational aids, such as Think-on-Graph [ 46 ]
and RRP [ 55 ]. However, independent OpenIE extraction often leads
to inconsistency. Although schema-guided approaches [ 33, 45 ] attempt to standardize this, they entail high manual costs. Addressing
these inefficiencies, LinearRAG [ 70 ] proposes a relation-free “TriGraph” based on lightweight entity extraction, achieving linear
scalability without the noise associated with traditional triple ex
traction.

**Clustering-based Hierarchy Construction.** Complementary
to triple-based methods, this category focuses on capturing global
information by identifying dense structural patterns. Methods typically employ community detection algorithms, such as Louvain or
Leiden, to recursively aggregate entities into clusters [ 12, 19, 44 ].
These clusters serve as hierarchical summaries, abstracting raw
passages into topic-level communities to provide a macro-level perspective. Despite its utility in summarizing high-level themes, this
unsupervised approach faces limitations regarding precision, as inaccuracies in low-level entity relationships can propagate upward,


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.


**Table 6: Case Study: Resolving Logic Conflicts via Global Adjudication. Comparing how MemGraphRAG handles contradictory**
**birth years across documents versus a Traditional GraphRAG baseline.**












|Pipeline Phase|Traditional GraphRAG (Baseline)|MemGraphRAG (Ours)|
|---|---|---|
|**1. Input Corpus**|Doc A:_ “Newton was born in 1645.”_<br>Doc B:_ “Isaac Newton, born 1643...”_|**Same Corpus**: Contains mutually exclusive facts due to<br>source errors or extraction noise.|
|**2. Graph Construction**|**Isolated Extraction**:<br>_𝑇_1 : (_𝑁𝑒𝑤𝑡𝑜𝑛,𝑏𝑜𝑟𝑛_𝑖𝑛,_ 1645)<br>_𝑇_2 : (_𝑁𝑒𝑤𝑡𝑜𝑛,𝑏𝑜𝑟𝑛_𝑖𝑛,_ 1643)<br>→_Both edges added to Graph 𝐺._|**Global Adjudication**:<br>_𝐴𝑑𝑒𝑡_detects Confict:_ 𝑇_1 ⊥_𝑇_2<br>→_𝐴𝑟𝑒𝑠_checks Evidence (_𝑀𝑝𝑎𝑠_)<br>→**Update**: Keep_ 𝑇_2, Discard_ 𝑇_1.|
|**3. Retrieval Query**|**Q: “When was Isaac Newton born?”**|**Q: “When was Isaac Newton born?”**|
|**4. Retrieval Process**|**Noisy Activation**:<br>Query triggers both nodes: {1645_,_ 1643}<br>→Retriever fetches conficting context.|**Consistent Path**:<br>Query triggers verifed node: {1643}<br>→Trace back to_ 𝑀𝑝𝑎𝑠_evidence.|
|**5. Final Answer**|_“Newton was born in 1645 or 1643...”_<br>(**Ambiguous / Hallucinated**)|_“Isaac Newton was born in 1643.”_<br>(**Precise & Verifed**)|



**Table 7: Case Study: Thematic Denoising in Medical Protocols. Demonstrating how MemGraphRAG filters irrelevant extraction**
**noise using Unified Schema Filtering.**









|Pipeline Phase|Traditional GraphRAG (Baseline)|MemGraphRAG (Ours)|
|---|---|---|
|**1. Input Corpus**|Chunk 1:_ “Osimertinib treats EGFR-mutant NSCLC.”_<br>Chunk 2:_ “Patient prefers tea over cofee.”_|**Same Corpus**: Mixture of clinical facts and irrelevant patient<br>anecdotes.|
|**2. Graph Construction**|**Full Extraction**:<br>_𝑇_1 : (_𝑂𝑠𝑖𝑚𝑒𝑟𝑡𝑖𝑛𝑖𝑏,𝑡𝑟𝑒𝑎𝑡, 𝑁𝑆𝐶𝐿𝐶_)<br>_𝑇_2 : (_𝑃𝑎𝑡𝑖𝑒𝑛𝑡, 𝑝𝑟𝑒𝑓𝑒𝑟,𝑇𝑒𝑎_)<br>→_Noise 𝑇_2 _pollutes the graph._|**Schema Filtering**:<br>Schema_ 𝑆_1(_𝐷𝑟𝑢𝑔,𝑡𝑟𝑒𝑎𝑡, 𝐷𝑖𝑠_) freq ≥_𝜏_→**Stable**<br>Schema_ 𝑆_2(_𝑃𝑎𝑡, 𝑝𝑟𝑒𝑓, 𝐵𝑒𝑣_) freq_ < 𝜏_→**Pending**<br>→**Result**: Only_ 𝑇_1 activated in_ 𝐺𝑓𝑎𝑐_.|
|**3. Retrieval Query**|**Q: “What is the standard treatment for NSCLC?”**|**Q: “What is the standard treatment for NSCLC?”**|
|**4. Retrieval Process**|**Drifting Path**:<br>Node_ NSCLC_ →_Patient_ →_Tea_<br>→Retrieves irrelevant dietary info.|**Focused Path**:<br>Node_ NSCLC_ →_Osimertinib_<br>→Strictly follows clinical ontology.|
|**5. Final Answer**|_“Osimertinib is used. Patients may prefer tea.”_<br>(**Unprofessional / Distracted**)|_“Osimertinib is the recommended treatment.”_<br>(**Professional & Concise**)|


and the iterative clustering of large-scale graphs poses significant
bottlenecks for real-time deployment.


**C** **Details of Preliminary Study**


Independent extraction across different chunks may introduce conflicting information into the merged graph, resulting in semantic
contradictions. In our preliminary study, we identify three major
types of such conflicts, as summarized in Table 8. Specifically:


  - **Mutually Exclusive Conflict:** Facts that cannot coexist
in reality. For example, Chunk A yields _(Newton, Birth year,_
_1643)_ while Chunk B yields _(Newton, Birth year, 1645)_ .

  - **Temporal Conflict:** Contradictions arising from time-variant
facts. A corpus spanning different years may generate both
_(Biden, President, USA)_ and _(Trump, President, USA)_ without
temporal qualifiers, confusing the retriever.

  - **Granularity Conflict:** Facts describing the same reality at
incompatible abstraction levels. For instance, connecting an
entity to both specific and general concepts, such as _(Xiao_
_Ming, born_in, Shanghai)_ and _(Xiao Ming, born_in, China)_, or



_(AI, subclass, NLP)_ vs. _(AI, subclass, Unsupervised Learning)_ .
These inconsistencies create redundant paths that dilute the
reasoning focus.


**D** **Details of the Proposed Method**

**D.1** **Key Definitions**


To establish a rigorous foundation for the subsequent methodology,
we first provide formal definitions for the core components of our
hierarchical knowledge representation:
(i) **Type (** _𝑡_ **) and Entity (** _𝑒_ **)** : We distinguish between abstract
concepts and concrete instances. A type _𝑡_ ∈T denotes a high-level
taxonomic category (e.g., _Person_ ) that serves as a semantic anchor.
An entity _𝑒_ ∈E refers to a specific instance grounded in the text
(e.g., _Einstein_ ), where each entity is associated with a type through
a mapping function _𝜙_ ( _𝑒_ ) = _𝑡_ .
(ii) **Schema (** _𝑠_ **) and Fact (** _𝑓_ **)** : We define knowledge triples at two
levels of abstraction. A schema _𝑠_ = ( _𝑡_ _ℎ_ _,𝑟,𝑡_ _𝑡_ ) specifies a structural
constraint, where _𝑡_ _ℎ_ _,𝑡_ _𝑡_ ∈T represent the head and tail types, and
_𝑟_ denotes a semantic relation (e.g., ( _Person_, _born_in_, _Country_ )). A


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su


**Table 8: Taxonomy of Knowledge Conflicts in Graph Retrieval-Augmented Systems.**












|Conflict Type|Definition|Mechanism & Impact|Illustrative Examples|
|---|---|---|---|
|**Mutually**<br>**Exclusive**<br>**Confict**|Logically incompatible facts<br>that cannot simultaneously<br>hold true within a single do-<br>main of discourse.|**Mechanism:** Distinct sources at-<br>tribute divergent values to a func-<br>tional property (single-value at-<br>tribute).<br>**Impact:** Introduces binary logical<br>contradictions that halt determinis-<br>tic reasoning.|_Attribute Value Clash:_<br>Source A:_ (Newton, born_in,_<br>_1643)_<br>Source B:_ (Newton, born_in,_<br>_1645)_|
|**Temporal Confict**|Inconsistencies<br>arising<br>from<br>state<br>changes<br>in<br>time-variant<br>facts<br>when<br>temporal<br>metadata<br>is<br>absent.|**Mechanism:** Facts valid in disjoint<br>time intervals (_𝑇_1 ≠_𝑇_2) are fattened<br>into a static knowledge base.<br>**Impact:** Confuses the retriever by<br>presenting outdated or competing<br>truths as currently valid.|_Role Evolution:_<br>_𝑇_2020:_ (Trump, President, USA)_<br>_𝑇_2021:_ (Biden, President, USA)_<br>_(Both retrieved without times-_<br>_tamps)_|
|**Granularity Confict**|Discrepancies in the level of<br>abstraction or specifcity re-<br>garding the same entity or<br>concept.|**Mechanism:** Simultaneous map-<br>ping of an entity to hierarchically<br>distinct nodes (e.g., specifc vs. gen-<br>eral) within an ontology.<br>**Impact:** Creates redundant infer-<br>ence paths and dilutes reasoning<br>precision.|_Geospatial:_<br>_(Xiao Ming, born_in, Shanghai)_<br>vs._ (Xiao Ming, born_in, China)_<br>_Taxonomical:_<br>_(AI, subclass, NLP)_ vs._ (AI, sub-_<br>_class, Machine Learning)_|



fact _𝑓_ = ( _𝑒_ _ℎ_ _,𝑟,𝑒_ _𝑡_ ) is a concrete instantiation of a schema, where
_𝑒_ _ℎ_ _,𝑒_ _𝑡_ ∈E (e.g., ( _Einstein_, _born_in_, _Germany_ )).
(iii) **Ontology (** O **)** : The ontology is defined as the structured collection of all valid schemas, denoted as O = { _𝑠_ 1 _, . . .,𝑠_ _𝑛_ } . It governs
the structural rules of the knowledge graph by enforcing semantic
constraints, ensuring that all extracted facts conform to predefined
schema specifications.
(iv) **Passage (** _𝑝_ **)** : A passage _𝑝_ ∈P represents a granular segment
of raw text from the corpus, serving as the evidence grounding
unit. Specifically, each extracted fact _𝑓_ is explicitly linked to its
supporting textual evidence through a mapping function _𝜓_ ( _𝑓_ ) →

_𝑝_ _𝑖_ .


**D.2** **MemGraphRAG architecture**


To overcome fragmented extraction and support the coherent evolution of knowledge graphs, we propose the MemGraphRAG architecture. Our core premise is that high-quality graph construction
requires not only structured storage, but also active management of
knowledge. The system is built upon two complementary components: (i) a _Hierarchical Memory Architecture_ that organizes schemas,
facts, and passages across different abstraction levels, and (ii) a
_Multi-Agent System_ that serves as the dynamic execution engine,
leveraging memory to drive the iterative “extract–verify–modify”
process. In the following sections, we describe how these components work together to ensure global consistency.
**Global Memory**, which organizes knowledge in a three-tier
structure that aligns abstract schemas, concrete facts, and supporting evidence. The top-level _Ontology Layer_ ( M _𝑜𝑛𝑡_ ) maintains
schema patterns with their statistical frequencies, providing semantic structure and global theme for graph construction. The middle



_Fact Layer_ ( M _𝑓𝑎𝑐_ ) stores instantiated triples derived from these
schemas. The lowest _Passage Layer_ ( M _𝑝𝑎𝑠_ ) preserves the original
source passages, ensuring that extracted facts remain grounded in
their linguistic context.
To strengthen associations across layers, we introduce a **dense**
**indexing mechanism** that enforces structural consistency through
bidirectional interactions. Specifically, _Schema–Instance Alignment_
is established not merely as a one-way classification, but as a mutual
binding between abstraction and instantiation. On the bottom-up
direction, we define a mapping


Φ : M _𝑓𝑎𝑐_ →M _𝑜𝑛𝑡_ _,_ (9)


which enforces strict typing by assigning each triple _𝑡_ ∈M _𝑓𝑎𝑐_ to
a schema constraint _𝑠_ ∈M _𝑜𝑛𝑡_ . On the top-down direction, each
schema _𝑠_ induces its instantiation set


T ( _𝑠_ ) = { _𝑡_ ∈M _𝑓𝑎𝑐_ | Φ( _𝑡_ ) = _𝑠_ } _,_ |T ( _𝑠_ )| ≥ 0 _,_ (10)


capturing the duality that schemas constrain facts while facts substantiate schemas.

Simultaneously, _Fact–Evidence Grounding_ is modeled via a bidirectional relation
Ψ ⊆M _𝑓𝑎𝑐_ × M _𝑝𝑎𝑠_ _,_ (11)
which links each fact to its supporting passages (provenance) while
allowing passages to index the facts they yield (extraction). For any
triple _𝑡_, we define its evidence set as


E( _𝑡_ ) = { _𝑝_ ∈M _𝑝𝑎𝑠_ | ( _𝑡, 𝑝_ ) ∈ Ψ } _,_ |E( _𝑡_ )| ≥ 1 _._ (12)


Together, these bidirectional mappings ensure that the graph is
both logically governed by the ontology and rigorously grounded
in textual evidence.


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.



**Hierarchical Indexing Graph**, which provides a unified representation spanning abstract schemas, concrete facts, and textual
evidence. Concretely, we organize G into three interconnected
graph views that enable hierarchical navigation from high-level
semantic concepts to fine-grained supporting passages. (i) _Semantic_
_Ontology Graph (_ G _𝑜𝑛𝑡_ _)_ : Derived from the ontology layer M _𝑜𝑛𝑡_, G _𝑜𝑛𝑡_
forms a high-level network of domain types and schema relations.
It serves as the logical backbone of the overall graph by encoding
valid relational patterns and domain constraints. (ii) _Fact Graph_
_(_ G _𝑓𝑎𝑐_ _)_ : Constructed from the fact layer M _𝑓𝑎𝑐_, G _𝑓𝑎𝑐_ represents an
entity-relation graph over instantiated triples, which acts as the primary substrate for multi-hop reasoning. (iii) _Source Evidence Graph_
_(_ G _𝑝𝑎𝑠_ _)_ : Induced from the passage layer M _𝑝𝑎𝑠_, G _𝑝𝑎𝑠_ grounds entities
and relations in G _𝑓𝑎𝑐_ back to their originating text passages, providing fine-grained evidence support for faithful answer generation.
Together, this multi-view architecture enables structured reasoning
that progressively traverses from G _𝑜𝑛𝑡_ to G _𝑓𝑎𝑐_, and finally to G _𝑝𝑎𝑠_
for evidence retrieval.

**Multi-Agent System**, which introduces the dynamic execution
units that drive the system’s evolution, is formulated as a collaborative ecosystem of specialized agents interacting with M through
distinct cognitive roles. Specifically, the Multi-Agent System is defined as A = _𝐴_ _𝑒𝑥𝑡_ _,𝐴_ _𝑑𝑒𝑡_ _,𝐴_ _𝑟𝑒𝑠_, where each agent focuses on a separate function. Our design philosophy emphasizes the decoupling of
generation, diagnosis, and correction to ensure high-fidelity graph
construction: (i) the **Extraction Agent** ( _𝐴_ _𝑒𝑥𝑡_ ), which initializes the
graph by processing input documents and populating all three layers of M (Schema, Fact, and Passage) in parallel, ensuring that each
extracted fact is grounded in supporting evidence; (ii) the **Conflict**
**Detection Agent** ( _𝐴_ _𝑑𝑒𝑡_ ), which is triggered by updates in the Fact
Layer ( M _𝑓𝑎𝑐_ ) and performs purely diagnostic checks to identify
structural anomalies, redundancy, and logical inconsistencies; and
(iii) the **Conflict Resolution Agent** ( _𝐴𝑟𝑒𝑠_ ), which resolves conflicts flagged by _𝐴_ _𝑑𝑒𝑡_ by leveraging the global context stored in M,
including historical evidence in M _𝑝𝑎𝑠_ and schema constraints in
M _𝑜𝑛𝑡_, thereby maintaining the global consistency of G.


**D.3** **Memory-based Indexing Graph**
**Construction**


Traditional graph construction often processes document chunks in
isolation, leading to redundant entities and fragmented subgraphs.
To address this, we reframe graph construction not as a one-off
extraction task, but as a **dynamic co-evolution process** between
the Global Memory M and the Knowledge Graph G . Driven by the
memory system, we implement two strategic paradigms to ensure
structural integrity: (i) **Structure Optimization via Progressive**
**Construction** : Instead of trusting LLM outputs immediately, we
treat extractions as hypotheses. The memory acts as a “probationary sandbox,” allowing the graph to evolve via an iterative “extract–verify–modify” cycle that filters noise before it pollutes the
graph structure. (ii) **Conflict Resolution via Global Perspec-**
**tive** : By maintaining a persistent global state, our shared memory
enables the system to detect and resolve semantic contradictions
(e.g., logical, temporal, or granular conflicts) that span across disparate documents, ensuring a unified and consistent knowledge
representation.



_D.3.1_ _Thematic Denoising via Unified Schema Filtering._ To mitigate
the stochastic hallucinations inherent in LLMs and ensure statistical
consensus, we implement a **“Probationary Extraction Protocol.”**
This protocol enforces a strict separation between raw extractions
and validated knowledge.
**First, Composite Extraction into Memory.** The process initiates by partitioning the document stream into uniform chunks
_𝑐_ _𝑖_ ∈C . For each chunk, the Extraction Agent ( _𝐴_ _𝑒𝑥𝑡_ ) generates a
_Composite Extraction Record_ that simultaneously populates all three
memory layers:


_𝐴_ _𝑒𝑥𝑡_ ( _𝑐_ _𝑖_ ) →{ _𝑂_ cand _,𝑇_ cand _, 𝑃_ src } (13)


where _𝑂_ cand and _𝑇_ cand represent candidate schemas and triples, and
_𝑃_ src anchors them to the source text.
**Second, The Ontology Filter Mechanism.** Crucially, newly
extracted schemas are initially assigned a logical “Candidate State”
(Pending). While physically stored in memory for tracking, they
remain _invisible_ to the global graph structure G . This isolation
prevents low-frequency noise from polluting the index.
**Finally, Confidence-Driven State Promotion.** We formalize
the evolution of knowledge using a frequency-based confidence
function. A schema transitions from “Pending” to “Stable” only
when its extraction frequency across the corpus exceeds a statistical
threshold _𝜏_ :



State( _𝑜_ ) = 




Stable _,_ if Freq( _𝑜_ ) ≥ _𝜏,_

(14)
Pending _,_ otherwise _._



This transition triggers a _cascading activation_ : only triples governed
by a stable schema are flagged as “Active.” Only these active triples
are permitted to enter the subsequent conflict detection phase,
ensuring the graph is constructed solely from consensus-verified
knowledge.


_D.3.2_ _Consistency Maintenance via Global Adjudication._ Dynamic
graph updates inevitably introduce contradictions. To ensure trustworthiness, we implement a collaborative mechanism where agents
utilize Global Memory as the “ground truth” for adjudication.
**Step 1: Asynchronous Conflict Triggering.** The Conflict Detection Agent ( _𝐴_ _𝑑𝑒𝑡_ ) is triggered strictly when a triple _𝑡_ new transitions to an “Active” state. _𝐴_ _𝑑𝑒𝑡_ performs a hybrid scan over the
existing Fact Memory ( M fac ), utilizing both vector similarity and
symbolic matching to identify potential conflict candidates _𝑇_ conf :


_𝑇_ conf = { _𝑡_ [′] ∈M fac | Sim( _𝑡_ new _,𝑡_ [′] ) _> 𝛿_ ∨ Match( _𝑡_ new _,𝑡_ [′] )} _._ (15)


If _𝑇_ conf ≠ ∅, the resolution protocol is initiated.
**Step 2: Evidence Retrieval and Adjudication.** Unlike blackbox resolution, our approach is evidence-driven. The Conflict Resolution Agent ( _𝐴_ _𝑟𝑒𝑠_ ) leverages the memory mapping Ψ to retrieve the
original provenance for both the new assertion and the conflicting
facts. It constructs a context window _𝐶_ ctx containing the raw source

passages:
_𝐶_ ctx = Ψ( _𝑡_ new ) ∪ � Ψ( _𝑡_ [′] ) _._ (16)

_𝑡_ [′] ∈ _𝑇_ conf

Based on _𝐶_ ctx, _𝐴_ _𝑟𝑒𝑠_ reasons to determine factual validity, effectively
acting as a judge reviewing case files.


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su


**Algorithm 1** Memory-based Indexing Graph Construction


**Require:** Document stream D; Global memory M = { _𝑀_ _𝑜𝑛𝑡_ _, 𝑀_ _𝑓𝑎𝑐_ _, 𝑀_ _𝑝𝑎𝑠_ }; schema threshold _𝜏_ ; conflict threshold _𝛿_ ; bridging threshold _𝛿_ _𝑏_
**Ensure:** Global hierarchical graph G

1: **Stage I: Composite Extraction into Memory (Sandbox)**

2: **for** each chunk _𝑐_ _𝑖_ from D **do**

3: { _𝑂_ _𝑐𝑎𝑛𝑑_ _,𝑇_ _𝑐𝑎𝑛𝑑_ _, 𝑃_ _𝑠𝑟𝑐_ } ← _𝐴_ _𝑒𝑥𝑡_ ( _𝑐_ _𝑖_ ) _⊲_ Extract candidate schemas, triples, and provenance

4: Store _𝑂_ _𝑐𝑎𝑛𝑑_ _,𝑇_ _𝑐𝑎𝑛𝑑_ _, 𝑃_ _𝑠𝑟𝑐_ into ( _𝑀_ _𝑜𝑛𝑡_ _, 𝑀_ _𝑓𝑎𝑐_ _, 𝑀_ _𝑝𝑎𝑠_ ) _⊲_ Probationary storage: extraction as hypotheses

5: **end for**


6: **Stage II: Unified Schema Filtering and Triple Activation**

7: **for** each schema _𝑜_ ∈ _𝑀_ _𝑜𝑛𝑡_ **do**

8: **if** Freq( _𝑜_ ) ≥ _𝜏_ **then**

9: State( _𝑜_ ) ← Stable _⊲_ Promote only consensus schemas

10: **end if**


11: **end for**

12: **for** each triple _𝑡_ ∈ _𝑀_ _𝑓𝑎𝑐_ **do**

13: **if** State(Schema( _𝑡_ )) = Stable **then**

14: State( _𝑡_ ) ← Active _⊲_ Activate only triples governed by stable schema

15: **end if**


16: **end for**


17: **Stage III: Conflict Detection and Evidence-based Adjudication**

18: **for** each newly active triple _𝑡_ _𝑛𝑒𝑤_ **do**

19: F _𝑐𝑜𝑛𝑓_ ←{ _𝑡_ [′] ∈ _𝑀_ _𝑓𝑎𝑐_ | Sim( _𝑡_ _𝑛𝑒𝑤_ _,𝑡_ [′] ) _> 𝛿_ ∨ Match( _𝑡_ _𝑛𝑒𝑤_ _,𝑡_ [′] )} _⊲_ Global scan for logical/temporal/granularity conflicts

20: **if** F _𝑐𝑜𝑛𝑓_ ≠ ∅ **then**

21: _𝐶_ _𝑐𝑡𝑥_ ← Ψ( _𝑡_ _𝑛𝑒𝑤_ ) ∪ [�] _𝑡_ [′] ∈F _𝑐𝑜𝑛𝑓_ [Ψ][(] _[𝑡]_ [′] [)] _⊲_ Retrieve provenance passages as evidence

22: _𝐴_ _𝑟𝑒𝑠_ updates _𝑡_ _𝑛𝑒𝑤_ and F _𝑐𝑜𝑛𝑓_ based on _𝐶_ _𝑐𝑡𝑥_ _⊲_ Discard / refine / temporally augment conflicting facts

23: **end if**


24: **end for**


25: **Stage IV: Multi-view Projection and Memory-guided Bridging**

26: Construct G _𝑜𝑛𝑡_ from stable schemas in _𝑀_ _𝑜𝑛𝑡_
27: Construct G _𝑓𝑎𝑐_ from active triples in _𝑀_ _𝑓𝑎𝑐_
28: Construct G _𝑝𝑎𝑠_ from provenance passages in _𝑀_ _𝑝𝑎𝑠_ _⊲_ Project memory layers into graph views

29: Add type-based edges linking entities with shared schema types _⊲_ Type-based bridging for disjoint subgraphs

30: Add similarity-based edges if Sim( _𝑒_ _𝑖_ _,𝑒_ _𝑗_ ) _> 𝛿_ _𝑏_ _⊲_ Embedding-based bridging for long-range connectivity

31: Merge all views into global hierarchical graph G

32: **return** G



**Step 3: Taxonomy-Based Resolution Strategies.** Based on
the evidence, _𝐴_ _𝑟𝑒𝑠_ executes targeted updates to resolve specific
conflict types:


  - _Mutually Exclusive Conflict (Logical):_ For contradictory facts
(e.g., conflicting birthplaces), the agent compares evidence
reliability to discard the erroneous fact.

  - _Temporal Conflict:_ For facts valid in different periods (e.g.,
distinct presidential terms), the agent resolves ambiguity by
appending temporal attributes (e.g., adding “46th” vs. “47th”).

  - _Granularity Conflict (Structural):_ For facts describing the
same reality at different abstraction levels (e.g., “Shanghai”
vs. “China”), the agent refines predicates to allow logical
coexistence (e.g., _born_city_ vs. _born_country_ ).


_D.3.3_ _Structural Unification via Memory-Guided Bridging._ The final phase transforms the validated contents of the memory system
into a navigable Global Hierarchical Graph G . We adopt a **multi-**
**view projection strategy** that maps the three memory layers into



corresponding graph views: G _𝑜𝑛𝑡_ (Schema View), G _𝑓𝑎𝑐_ (Fact View),
and G _𝑝𝑎𝑠_ (Source View).
To address the common issue of disjoint subgraphs in extracted
knowledge, we augment the primary reasoning substrate, G _𝑓𝑎𝑐_,
with two **memory-enabled connectivity mechanisms** :


(1) **Type-Based Bridging:** Leveraging M _𝑜𝑛𝑡_, disjoint entities
are explicitly connected if they map to the same high-level
schema type (e.g., connecting all _Researchers_ regardless of
their document origin).
(2) **Similarity-Based Bridging:** Leveraging embedding storage in M, we introduce implicit edges between entity pairs
whose vector similarity exceeds a threshold _𝛿_ .

These mechanisms leverage the global nature of memory to connect
long-distance entities, significantly enhancing the graph’s ability
to support multi-hop reasoning across documents where explicit
textual links are missing.


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.


**Algorithm 2** Memory-guided Online Retrieval


**Require:** Query embedding q; Graph G with transition matrix M; Memory M = { _𝑀_ _𝑜𝑛𝑡_ _, 𝑀_ _𝑓𝑎𝑐_ _, 𝑀_ _𝑝𝑎𝑠_ } ; top- _𝐾_ ; threshold _𝜏_ ; damping _𝜆_ ; balance

_𝛼_

**Ensure:** Evidence set C for downstream LLM generation


1: **Stage I: Multi-layer Retrieval and Filtering**

2: S _𝑟𝑎𝑤_ ← TopK( _𝑀_ _𝑜𝑛𝑡_ _,_ q _, 𝐾_ ); F _𝑟𝑎𝑤_ ← TopK( _𝑀_ _𝑓𝑎𝑐_ _,_ q _, 𝐾_ ); P _𝑟𝑎𝑤_ ← TopK( _𝑀_ _𝑝𝑎𝑠_ _,_ q _, 𝐾_ ) _⊲_ Align query with ontology, facts, and passages

3: S _𝑟𝑒𝑡_ ←{ _𝑠_ ∈S _𝑟𝑎𝑤_ | Sim(q _,_ s) _> 𝜏_ }; F _𝑟𝑒𝑡_ ←{ _𝑓_ ∈F _𝑟𝑎𝑤_ | Sim(q _,_ f) _> 𝜏_ }

4: **if** S _𝑟𝑒𝑡_ ∪F _𝑟𝑒𝑡_ = ∅ **then**

5: **return** P _𝑟𝑎𝑤_ _⊲_ Fallback to standard RAG


6: **end if**


7: **Stage II: Structure-aware Node Initialization**

8: Define reset weights _𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑣_ ) on nodes _𝑣_ ∈G:

9: _Entity nodes:_ _𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑒_ ) = | F1 _𝑒_ | � _𝑓_ ∈F _𝑒_ [Sim][(][q] _[,]_ [ f][)] _[,]_ [ F] _𝑒_ [=][ {] _[𝑓]_ [∈F] _𝑟𝑒𝑡_ [|] _[ 𝑒]_ [∈] _[𝑓]_ [}] _⊲_ Ground by query-relevant facts

10: _Type nodes:_ _𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑡_ ) = � |S1 _𝑡_ | � _𝑠_ ∈S _𝑡_ [Sim][(][q] _[,]_ [ s][)] � - log(deg1( _𝑡_ )+1) _[,]_ [ S] _[𝑡]_ [=][ {] _[𝑠]_ [∈S] _[𝑟𝑒𝑡]_ [|] _[ 𝑡]_ [∈] _[𝑠]_ [}] _⊲_ Schema relevance + hub suppression



11: _Passage nodes:_ _𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑝_ ) = Sim(q _,_ d _𝑝_ ) · _𝛼_ - _𝜎_ �log _𝑒_ ∈E (| E _𝑝_ _𝑝_ [IDF] |+1 [(] _[𝑒]_ ) [)]
�

12: Normalize _𝑃_ _𝑖𝑛𝑖𝑡_ into p [(][0][)] with [�] _𝑣_ [p] [(][0][)] [ (] _[𝑣]_ [)][ =][ 1]


13: **Stage III: PPR Propagation and Evidence Selection**

14: **repeat**



_⊲_ Semantic alignment + information density
�



15: p [(] _[𝑘]_ [+][1][)] ←(1 − _𝜆_ )Mp [(] _[𝑘]_ [)] + _𝜆_ p [(][0][)] _⊲_ Personalized PageRank with restart

16: **until** convergence

17: Select top-ranked passages P [∗] and entities E [∗] by p [(∞)]

18: C ←P [∗] ∪E [∗]


19: **return** C



**E** **Prompt Set**


To provide a more intuitive illustration of our graph construction
procedure and ensure reproducibility, we present the _Conflict De-_
_tection_ and _Conflict Resolution_ components used in MemGraphRAG
indexing, as shown in Figure 7 and 8.


**E.1** **Memory-guided Online Retrieval**


Building upon the constructed Global Hierarchical Graph G and
the Global Memory M, this section details our memory-guided
retrieval and reasoning mechanism. To bridge the gap between the
user query and the complex graph topology, the inference workflow
unfolds through three logically progressive stages: The workflow
consists of three key steps: i) **Multi-Layer Memory Retrieval**,
which retrieves initial initial candidate evidence, including schemas
_𝑠_, facts _𝑓_, and passages _𝑝_ from _𝑀_ _𝑜𝑛𝑡_, _𝑀_ _𝑓𝑎𝑐_, and _𝑀_ _𝑝𝑎𝑠_, respectively.
It then applies a preliminary noise filtering process to ensure relevance. ii) **Structure-Aware Node Initialization**, which projects
the retrieved evidence onto the graph structure by mapping them to
initial node weights. We apply distinct scoring strategies for Entity
nodes _𝑒_, Type nodes _𝑡_, and Passage nodes _𝑝_, integrating semantic relevance, topological constraints, and information density. iii)
**Graph Propagation**, which executes the Personalized PageRank
(PPR) algorithm on the heterogeneous graph, initiating from the
weighted nodes. This propagation diffuses importance across the
graph to identify the most globally significant passages and nodes,
which are then selected for downstream LLM generation.


_E.1.1_ _Multi-Layer Memory Filtering._ The retrieval phase initiates
by querying the three distinct layers of the Global Memory M in



parallel. Given a user query q, we parallelly retrieve top- _𝐾_ candidates from _𝑀_ _𝑜𝑛𝑡_, _𝑀_ _𝑓𝑎𝑐_, and _𝑀_ _𝑝𝑎𝑠_ respectively. To prevent lowrelevance noise from propagating into the graph reasoning stage,
we apply a strict relevance filter. For the retrieved schemas S _𝑟𝑒𝑡_
and facts F _𝑟𝑒𝑡_, only candidates satisfying a semantic similarity
threshold Sim( q _,_ x ) _> 𝜏_ are retained. This filtering ensures that
the subsequent node initialization is seeded exclusively with highconfidence structural evidence. Crucially, to guarantee system robustness, if the filtering process yields no valid structural evidence
(i.e., _𝑆_ ret ∪ _𝐹_ ret = ∅ ), the framework adaptively falls back to a standard RAG mode, relying solely on the direct similarity between the
query and the content in _𝑀_ _𝑝𝑎𝑠_ for answer generation.


_E.1.2_ _Structure-Aware Node Initialization._ To seed the subsequent
graph propagation process with specific semantic context, we must
project the retrieved evidence onto the heterogeneous graph topology. Formally, we define an initial reset probability distribution
_𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑣_ ) for any node _𝑣_ ∈G . This distribution provides an initial importance score for the inference algorithm, quantifying the intrinsic
significance of each node prior to information diffusion.
**1. Entity Node Initialization via Facts:** To ensure that graph
propagation originates from grounded evidence, we first initialize
entity nodes based on the relevance of their associated facts retrieved from M _𝑓𝑎𝑐_ . Formally, we quantify the initial importance
of an entity e as the mean semantic similarity of all filtered facts
containing it:



1
_𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑒_ ) =
|F _𝑒_ |



∑︁ Sim(q _,_ f) (17)

_𝑓_ ∈F _𝑒_


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su





**Figure 7: The prompt used for Conflict Detection Agent.**



where F _𝑒_ ⊆F _𝑟𝑒𝑡_ denotes the subset of query-relevant facts
contain entity _𝑒_ . If F _𝑒_ = ∅, the weight defaults to 0. This aggregation
strategy ensures that entities are activated strictly by explicit, queryrelevant factual support.
**2. Type Node Initialization via Schemas:** To incorporate
macro-level domain knowledge and avoid introducing irrelevant
semantics, we further initialize type nodes _𝑡_ ∈G schema based on
the retrieved schemas from M ont . A critical challenge is that type
nodes often exhibit disproportionately large degrees (e.g., a generic
“Person” node connected to thousands of entities). Activating such
high-degree nodes directly would cause importance to diffuse too
broadly across the graph, thereby introducing substantial noise. To
address this issue, we introduce a structural regularization term
that combines semantic relevance with a log-degree penalty:



leverages ontology as a weak supervision signal while strictly constraining the diffusion radius of overly generic concepts.
**3. Passage Initialization with Information Density:** Finally,
we need to initialize the Passage Nodes ( _𝑝_ ∈ _𝐺_ _𝑝𝑎𝑠_ ). We formulate the
comprehensive scoring function to prioritize semantically relevant
sources with high-value information, while avoiding dominance
over finer-grained entity nodes, as follows:



�



_𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑝_ ) = Sim(q _,_ d _𝑝_ ) × _𝛼_ × _𝜎_



� _𝑒_ ∈E _𝑝_ [IDF][(] _[𝑒]_ [)]
� log(|E _𝑝_ | + 1)



(19)



∑︁ Sim(q _,_ s)

_𝑠_ ∈S _𝑡_



1
×
log(deg( _𝑡_ ) + 1)

� **��������������** �� **��������������** �


Hub Suppression



�



_𝑃_ _𝑖𝑛𝑖𝑡_ ( _𝑡_ ) =



1

|S _𝑡_ |
�



(18)



� **������������������** �� **������������������** �


Information Density Term


This formula integrates three critical dimensions: (i) _Semantic Align-_
_ment_ ( Sim ), which measures the vector similarity between the query
_𝑞_ and the passage embedding _𝑑_ _𝑝_ ; (ii) _Structural Balance_ ( _𝛼_ ), a dampening coefficient empirically set to 0.05, which prevents dense passage nodes from overwhelming sparse entity nodes during the
initial propagation phase and ensures a balanced importance distribution; and (iii) _Information Density Term_, which quantifies content



� **���������������������** �� **���������������������** �



Schema Relevance



where S _𝑡_ denotes the subset of retrieved schemas corresponding
to type _𝑡_, deg( _𝑡_ ) is the node degree. This formulation effectively


MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea.





**Figure 8: The prompt used for Conflict Resolution Agent.**



quality by summing the Inverse Document Frequency (IDF) of entities _𝐸_ _𝑝_ within the passage and applying log-normalization, thereby
rewarding passages that contain rare and discriminative facts rather
than generic, verbose content.


_E.1.3_ _Personalized PageRank._ Following the initialization phase,
We execute the Personalized PageRank (PPR) algorithm on the
heterogeneous graph to diffuse the initial semantic energy. The
propagation uses the normalized vector p [(][0][)] as the starting distribution and follows the iteration:


v [(] _[𝑘]_ [+][1][)] = (1 − _𝜆_ )Wv [(] _[𝑘]_ [)] + _𝜆_ v [(][0][)] (20)


where W is the transition matrix of the graph. We specifically set
the damping factor _𝜆_ = 0 _._ 5 to restrict the random walk to a local
neighborhood, thereby preventing semantic drift into irrelevant
multi-hop connections. Upon convergence to v [(∞)] the top-K passages and top-M entities with the highest scores are selected as the
context window for LLM inference.


**F** **Benchmark Dataset**


We first evaluate the effectiveness of MemGraphRAG on three
widely-used multi-hop QA datasets, including HotpotQA [ 59 ], 2WikiMultiHopQA (2Wiki) [ 25 ] and MuSiQue [ 47 ] and two GraphRAG
benchmarks: G-bench (Novel) and G-bench (Medical) [ 52 ]. We provide a concise overview of each dataset’s key characteristics below.
**(i) HotpotQA [** **59** **]:** A widely adopted dataset for evaluating
multi-hop reasoning across disparate texts. It requires models to filter through distractor paragraphs and synthesize information from



multiple supporting documents to answer complex queries, thereby
testing the system’s ability to perform effective cross-document
evidence retrieval.

**(ii) 2WikiMultiHopQA (2Wiki) [** **25** **]:** A benchmark derived
from Wikipedia knowledge graphs, specifically constructed to test
structured reasoning. It consists of queries that necessitate aggregating evidence chains from two to four specific articles, focusing
on the model’s capacity to handle complex entity relationships and
maintain logical consistency.
**(iii) MuSiQue [** **47** **]:** A challenging dataset designed to minimize
reasoning shortcuts often found in earlier benchmarks. It features
connected reasoning chains of 2-4 hops, requiring systems to perform strictly sequential logical inference across multiple documents
to derive the correct answer.

**(iv) G-bench (Novel) & G-bench (Medical)** [ 52 ]: Two domainspecific benchmarks tailored to evaluate GraphRAG performance
on hierarchical retrieval and deep contextual understanding. The
_Medical_ subset utilizes NCCN guidelines to test the handling of
dense, rule-based clinical protocols, while the _Novel_ subset employs literary texts from Gutenberg to assess the comprehension of
implicit, non-linear narrative structures.


**G** **Implementation Details of Baselines**


In our experiments, we compare our method against several widely
used GraphRAG models.


KDD 2026, August 9–13, 2026, Jeju Island, Republic of Korea. Chuanjie Wu, Zhishang Xiang, Yunbo Tang, Zerui Chen, Qinggang Zhang, and Jinsong Su



**KGP** [ 51 ] facilitates multi-document question answering by constructing a graph where nodes represent passages or document
structures. It employs an LLM-driven traversal agent to navigate
semantic and structural connections, progressively aggregating
supporting context for the final response.
**G-Retriever** [ 24 ] targets real-world textual graphs by formulating the subgraph retrieval task as a Prize-Collecting Steiner Tree
(PCST) optimization problem. This approach extracts the most relevant subgraph to fit within the LLM context window, enabling
effective conversational QA while mitigating hallucination and
ensuring scalability.
**RAPTOR** [ 44 ] employs a recursive abstraction approach to construct a hierarchical tree structure. By clustering and summarizing
text chunks from the bottom up, it enables the retrieval of information at varying levels of granularity, capturing both high-level
context and fine-grained details for holistic understanding.
**MS-GraphRAG** [ 12 ] enhances global corpus understanding by
building an entity-relation graph and pre-computing communitylevel summaries. It answers queries by synthesizing insights from
these communities, offering improved comprehensiveness for questions that span the entire document collection.
**LazyGraphRAG** [ 8 ] introduces a cost-effective paradigm that
eliminates the need for expensive up-front summarization of source
data. By avoiding the pre-computation of community hierarchies,
it reduces indexing costs to the level of standard vector RAG while
maintaining superior performance on local queries and competitive
quality on global queries compared to full-graph approaches.
**LightRAG** [ 17 ] introduces a two-tier retrieval strategy designed
to capture both detailed entity relationships and broader thematic
contexts. It utilizes graph-enhanced indexing to facilitate rapid
access to relevant information and allows for seamless integration
of new data via an incremental update algorithm.
**HippoRAG** [ 19 ] proposes a neurobiologically inspired framework that orchestrates LLMs, knowledge graphs, and Personalized



PageRank. It acts as a dual-system memory model to enable deep
knowledge integration, facilitating robust retrieval for scenarios
requiring the synthesis of information from multiple sources.
**HippoRAG2** [ 20 ] extends the Personalized PageRank-based
framework of its predecessor by optimizing passage contextualization and the online interaction with LLMs. These enhancements

enable the model to mimic human long-term memory more effectively, balancing robust factual recall with complex associative
reasoning.
**E** [2] **GraphRAG** [ 64 ] optimizes the GraphRAG paradigm by establishing bidirectional indexes between document chunks and entities.
It combines a summary tree with a lightweight entity graph to facilitate fast lookup, enabling an adaptive retrieval process that seamlessly integrates local context and global understanding without
manual query mode selection.
**GFM-RAG** [ 37 ] introduces a Graph Foundation Model (GFM)
designed for zero-shot application on unseen datasets. It employs
a pre-trained Graph Neural Network to reason over graph structures, effectively capturing complex query-knowledge relationships
while mitigating the impact of noise and incompleteness in the constructed graphs.
**LogicRAG** [ 6 ] introduces a dynamic retrieval paradigm where
query-specific logic is modeled as a directed acyclic graph at inference time. By linearizing this graph via topological sort, it guides
the retrieval process through a logically consistent sequence of subproblems, significantly reducing token usage compared to static
graph approaches.
**LinearRAG** [ 70 ] challenges the reliance on costly and unstable
relation extraction in existing methods. It constructs a relation-free
hierarchical structure termed “Tri-Graph” using lightweight entity
extraction and semantic linking. This approach scales linearly with
corpus size and employs a two-stage retrieval strategy involving
local entity activation and global importance aggregation.


