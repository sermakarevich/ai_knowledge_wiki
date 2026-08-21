## **SAGE: A Self-Evolving Agentic Graph-Memory** **Engine for Structure-Aware Associative Memory**

**Juntong Wang** [1] _[,]_ [2] **Haoyue Zhao** [3] **Guanghui Pan** [3] **Yanbo Wang** [1] _[,]_ [2]

Xiyuan Wang [1] _[,]_ [2] Qiyan Deng [3] Muhan Zhang [1] _[∗]_

1 Institute for Artificial Intelligence, Peking University
2 School of Intelligence Science and Technology, Peking University
3 School of Computer Science and Technology, Beijing Institute of Technology
`jtwang25@stu.pku.edu.cn`, `18503260963@163.com`, `3220251221@bit.edu.cn`,
`wangyanbo@stu.pku.edu.cn`, `wangxiyuan@pku.edu.cn`, `qiyandeng@bit.edu.cn`, `muhan@pku.edu.cn`


**Abstract**


Long-term memory is becoming a central bottleneck for language agents. Existing
RAG and GraphRAG systems largely treat memory graphs as static retrieval
middleware, which limits their ability to recover complete evidence chains from
partial cues, exploit reusable graph-structural roles, and improve the memory
itself through downstream feedback. We introduce SAGE, a **S** elf-evolving **A** gentic
**G** raph-memory **E** ngine that models graph memory as a dynamic long-term memory
substrate. SAGE couples two roles: a memory writer that incrementally constructs
structured graph memory from interaction histories, and a Graph Foundation Modelbased memory reader to perform retrieval and provide feedback to the memory
writer. We provide rigorous theoretical analyses supporting the effectiveness of
carefully designed architectural components and the framework. Across multi-hop
QA, open-domain retrieval, domain-specific review QA, and long-term agentmemory benchmarks, SAGE improves evidence recovery, answer grounding, and
retrieval efficiency: after two self-evolution rounds, it achieves the best average
rank on multi-hop QA; in zero-shot open-domain transfer, it reaches 82.5/91.6
Recall@2/5 on NQ. Further results on LongMemEval and HaluMem show that
training and reader–writer feedback improve multiple long-term memory and
hallucination-diagnostic metrics, suggesting that self-evolving, structure-aware
graph memory is a promising foundation for robust long-horizon language agents.
[Our code is available here.](https://anonymous.4open.science/r/Unified-Representation-A9D9/)


**1** **Introduction**


As large language models evolve from single-turn question-answering systems into general-purpose
agents for multi-turn dialogue, personalized assistance, multi-agent collaboration, and openenvironment exploration, the system bottleneck is shifting from whether a model can answer within
the current context to whether it can accumulate, organize, invoke, and update memory over longer
time scales. Memory is a core system capability that determines whether Agents can achieve longterm consistency, personalized adaptation, cross-turn reasoning, and self-improvement. **Memory**
**is to Agents what parameters are to foundation models** [Park et al., 2023, Zhong et al., 2024,
Packer et al., 2023, Wu et al., 2025a, Yang et al., 2026]. Recent memory benchmarks have made
this bottleneck explicit, evaluating agents on ultra-long conversational consistency, multi-session
reasoning, temporal reasoning, knowledge updating, selective forgetting, abstention, and hallucination
control [Maharana et al., 2024, Di Wu et al., Hu et al., 2025, Chen et al., 2025a, Li et al., 2026b].


_∗_ Corresponding author.


40th Conference on Neural Information Processing Systems (NeurIPS 2026).


#### **Three Core Challenges in Agent Graph Memory**





















Figure 1: Overview of the three core challenges in agent graph memory, illustrated with a concrete
example. Given the query, _**“Alice mentioned a work in last week’s lab meeting that seemed to be**_
_**inspired by the Cornu Ammonis. Among works in the same field as that work, are there any that**_
_**can also help with agent memory? Give one example,”**_ the memory reader must address associative
and selective reading by expanding sparse partial cues into the correct evidence chain while avoiding
noisy distractors. It must then exploit structural information in the memory graph, such as aliases,
bridges, and hubs, to traverse from Cornu Ammonis to SAGE. Self-evolving memory highlights the
closed loop between writing and reading.


In engineering practice, RAG has become the dominant non-parametric interface for extending
language models with external memory, alleviating the static nature of parametric knowledge and the
limited size of context windows [Lewis et al., 2020]. Yet standard RAG usually retrieves independent
text chunks, whereas long-term agent memory often requires recovering evidence distributed across
entities, events, aliases, temporal constraints, and multi-hop dependencies. GraphRAG takes an
important step by organizing documents, entities, relations, and summaries as graphs, making crossdocument dependencies and reasoning paths more explicit [Edge et al., 2024, Gutiérrez et al., 2024].
However, for long-horizon agents, graph structure should not merely serve as an external retrieval
index. In this work, we study _agent graph memory_ as a coupled write–read–update problem. Given
interaction histories or external documents, a memory writer should construct an **evolving graph**
whose nodes and edges encode entities, episodes, documents, aliases, temporal constraints, and
cross-fragment relations. Given a query, a memory reader should not simply expand from a few
matched entities; it should return a **compact, verifiable evidence chain** . The retrieval outcome
should further **provide feedback about what the graph lacks** . In other words, the graph is not only
built before retrieval and searched afterward; it is the **working substrate through which memory is**
**written, read, corrected, and self-improved** . Around this goal, we identify the following three core
challenges.


**Challenge I: Agent memory requires global associative reading from fragmented cues.** The first
challenge is not merely to retrieve text that is semantically similar to the query, but to reconstruct a
complete reasoning chain from sparse, fragmented, and sometimes indirect cues. In long-term agent
memory, a query may mention only an episodic clue, an alias, or a distant conceptual hint, while
the answer depends on intermediate entities that are not explicitly named. Standard vector retrieval
tends to return locally similar snippets, and many graph-based retrieval methods start propagation
from a small set of query-matched anchor entities. However, if these anchors only cover a local
subgraph, the necessary bridge nodes may lie outside the activated region, leaving the evidence chain
disconnected even after graph propagation. Thus, agent memory reading should not commit too early
to a small set of partial cues [Trivedi et al., 2023, Gutiérrez et al., 2024].


**Challenge II: Agent memory requires learned structural use rather than fixed structural**
**expansion.** The second challenge is that graph structure should not be used only as a fixed index after
graph construction. Many GraphRAG-style systems exploit structure through pre-built communities,
paths, graph indexes, or heuristic expansion rules, but once the graph is constructed, the role of
structure is largely fixed: a hub remains broadly expanded, a bridge may be missed if it is not reached


2


by the initial anchors, and noisy shortcuts may be treated similarly to useful evidence edges. This is
insufficient for agent memory, where the graph itself is continuously updated by new interactions and
where the same topological pattern may have different meanings across domains. A structure-aware
reader should therefore learn how structural roles affect retrieval [Edge et al., 2024, Gutiérrez et al.,
2024, Liu et al., 2025, Luo et al., 2025].


The example in Figure 1 illustrates both challenges. Given the query, the explicit cues are only _Alice_,
_lab meeting_, _Cornu Ammonis_, and _agent memory_ . A retrieval system that only anchors on the most
query-matched nodes may retrieve the meeting note or the biological cue, but still fail to connect
them to _hippocampus_, _HippoRAG_, _GraphRAG_, and finally SAGE. This is the associative-reading
challenge: the system must piece together a long chain from scattered cues. At the same time, the
correct path depends on structural roles: _HippoRAG_ is a bridge, _GraphRAG_ and _RAG_ are hubs that
must be controlled rather than blindly expanded, and the edge from _GraphRAG_ to SAGE is critical
for reaching the final answer. This is the structural-information challenge: the reader must use graph
topology in a learned and selective way, not simply propagate uniformly over a fixed graph.


**Challenge III: Existing methods mostly optimize retrieval trajectories, but rarely optimize the**
**self-evolution of the memory system itself.** Existing RAG and GraphRAG systems often assume
that the external memory graph or knowledge base is already available, so the main problem becomes
how to retrieve from it. For long-term agents, however, writing is itself part of the memory problem.
Conversely, retrieval failures provide useful signals about what the memory graph lacks. For example,
if the reader repeatedly needs to traverse from _Cornu Ammonis_ to _hippocampus-style GraphRAG_
and then to the GraphRAG literature, the memory system should gradually add or strengthen useful
structural links, such as a more direct edge from _hippocampus-style GraphRAG_ to _GraphRAG_ . Thus,
a true agent memory system should not only optimize retrieval trajectories; it should optimize the
memory graph itself through a closed loop in which better reading exposes writing deficiencies, and
better writing makes future reading more accurate, selective, and efficient [Chen et al., 2025a].


To address these challenges, we propose SAGE, a _**S**_ elf-evolving _**A**_ gentic _**G**_ raph-memory _**E**_ ngine.
Unlike GraphRAG systems that mainly use graphs as retrieval middleware, SAGE treats the graph as
a dynamic long-term memory object. It couples two mutually reinforcing components: a memory
writer incrementally constructs and revises graph memory; a Graph Foundation Model-based memory
reader to perform retrieval and provide feedback to the memory writer. SAGE directly targets the
three challenges above: it recovers long reasoning chains from fragmented cues, learns how to use
structural roles rather than propagate uniformly, and continuously improves the graph memory itself
for future queries.


**2** **Related Work**


**Retrieval-Augmented Generation and GraphRAG.** Retrieval-Augmented Generation (RAG)
provides a non-parametric interface for language models by retrieving external evidence before
generation [Lewis et al., 2020]. Many variants further improve retrieval timing, reasoning interaction,
adaptive policies, and hierarchical organization [Jiang et al., 2023, Trivedi et al., 2023, Asai et al.,
2023, Jeong et al., 2024, Sarthi et al., 2024]. GraphRAG enables structured retrieval over crossdocument dependencies and multi-hop evidence paths [Edge et al., 2024, He et al., 2024, Guo et al.,
2024, Li et al., 2024, Wang and Han, 2025, Xu et al., 2025a, Zhao et al., 2025, Zhang et al., 2025c,
Gutiérrez et al., 2024, 2025, Luo et al., 2025]. Another line of work improves retrieval by optimizing
retrieval trajectories, including interleaved retrieval and reasoning, self-reflective retrieval, adaptive
retrieval, multi-agent RAG, and reinforcement-learning-based query rewriting [Trivedi et al., 2023,
Asai et al., 2023, Jeong et al., 2024, Chen et al., 2025b, Cha et al., 2025, Tsang et al., 2025].


**Agent Memory.** Agent memory studies how LLM-based agents store, update, retrieve, and use
past experiences [Park et al., 2023, Zhong et al., 2024, Packer et al., 2023, Chhikara et al., 2025, Xu
et al., 2025b, Rasmussen et al., 2025, Kang et al., 2025, Zhang et al., 2025a, Wu et al., 2025b, Zhang
et al., 2025b, Huang et al., 2025, Yue et al., 2026]. Recent surveys also highlight the importance
of human-inspired and graph-based memory mechanisms for LLM agents [Wu et al., 2025a, Yang
et al., 2026]. Meanwhile, memory benchmarks evaluate long-term consistency, event reasoning,
multi-session reasoning, temporal reasoning, knowledge updating, selective forgetting, abstention,
and hallucination control [Maharana et al., 2024, Di Wu et al., Hu et al., 2025, Chen et al., 2025a, Li
et al., 2026b].


3


Figure 2: Overall pipeline of the proposed **SAGE** . The memory writer incrementally constructs and
updates graph memory from observations through state-conditioned writing actions, and receives
rewards from downstream memory use. The resulting retrieval feedback closes the loop between
writing and reading, enabling graph memory to improve over time.



**Graph Foundation Models.** Graph Foundation Models (GFMs) aim to learn transferable graph representations through large-scale pretraining, allowing models to reuse structural priors and semantic
patterns across graphs, tasks, and domains [Liu et al., 2025]. Representative early works include GCC,
GPT-GNN, and GraphCL, which learn transferable graph representations through cross-network
contrast, generative graph pretraining, and graph augmentation based contrastive learning [Qiu et al.,
2020, Hu et al., 2020, You et al., 2020, Yu et al., 2025].


**3** **Preliminary**


Given a knowledge-intensive memory sample _x_ = ( _q, D, D_ [+] _, y_ ), where _q_ denotes the query, _D_ =
_{d_ _i_ _}_ _[N]_ _i_ =1 [denotes the set of candidate historical memory fragments,] _[ D]_ [+] _[ ⊆D]_ [ denotes the gold]
evidence set that supports the answer, and _y_ denotes the ground-truth answer. The writer is viewed as
a structured policy model: at step _h_, given state _s_ _h_, the policy samples a writing action _a_ _h_ _∼_ _π_ _θ_ ( _· | s_ _h_ )
and updates the partial graph as _G_ _h_ +1 = _G_ _h_ _⊕a_ _h_ . The memory reader _R_ _ϕ_ performs query-conditioned
propagation over the graph, obtains entity relevance scores **s** _E_ = _f_ _ϕ_ ( _q, G_ ) _∈_ R _[|V]_ _[E]_ _[|]_, and then projects
them into memory-fragment scores. The reader finally outputs _D_ � _k_ = TopK _d∈D_ ( **s** _D_ ( _d_ )), � _G_ _q_ is the query-activated subgraph, and ( _D_ [�] _k_ _,_ Π _G_ [�] _qq_ _,_ denotes optional relational Π _q_ ) = _R_ _ϕ_ ( _q, G,_ **M** ), where
paths. The generation model then produces the answer � _y_ = LLM( _q,_ _D_ [�] _k_ _,_ Π _q_ ).


**4** **Method**


At a high level, our method builds a self-evolving graph memory pipeline (Figure 2). The memory
writer _W_ _θ_ first transforms the query and candidate historical memory fragments into a heterogeneous
graph memory _G_ . The memory reader _R_ _ϕ_ then performs query-conditioned activation over _G_ : it
softly locates query-relevant entities, propagates evidence signals through relational structures, and
projects the activated entity-level information back to memory fragments.


**4.1** **Memory Writer: Graph Memory Writing via Reading Feedback**


**Policy-based writing.** The writer is modeled as a sequential decision-making policy. At step
_t_, the state is defined as _s_ _t_ = � _q, D, G_ _t−_ 1 _, D_ _t_ [proc] _−_ 1 �, where _G_ _t−_ 1 is the partially written graph, and
_D_ _t_ [proc] _−_ 1 [denotes the set of processed documents. The action] _[ a]_ _[t]_ [ contains entity-relation triples] [ (] _[u, r, v]_ [)]
together with their source anchors ( _u,_ `source` _, d_ ) . Detailed implementation information is provided
in Appendix O.


4


**Reader-aware Writing Reward.** The writer’s reward stems from the task utility of its written
graph after being accessed by the memory reader. Given the current graph _G_, the frozen reader
returns the evidence _P_ _k_ ( _q, G_ ) . Inspired by [Tsang et al., 2025], we employ two complementary types
of rewards. The first category measures whether the graph is sufficient as a knowledge carrier to
support the derivation of the answer: _r_ ded ( _q, y, G_ ) = I �Judge � _q, y | P_ _k_ ( _q, G_ )� = `Yes` � . The second
category measures whether the graph can serve as a knowledge index to recover the supporting
text: _r_ rec ( _q, D_ [+] _, G_ ) = _[|][P]_ _[k]_ [(] _[q,]_ _|D_ _[G]_ [+] [)] _[∩D]_ _|_ [+] _[|]_ _, r_ pre ( _q, D_ [+] _, G_ ) = _[|][P]_ _[k]_ _|P_ [(] _[q,]_ _k_ ( _[G]_ _q,_ [)] _[∩D]_ _G_ ) _|_ [+] _[|]_ . Where _r_ rec encourages the

coverage of necessary evidence, while _r_ pre penalizes the expansion of irrelevant evidence. To align
with end-to-end question answering, we also use an answer-level auxiliary reward _r_ ans ( _q, y, G_ ) =

ˆ
max _y_ _′_ _∈Y_ ( _y_ ) F1� _y, y_ _[′]_ [�] _,_ ˆ _y_ = LLM � _q, P_ _k_ ( _q, G_ )�, where _Y_ ( _y_ ) is the set of answer aliases. In practice,
we adopt a hybrid task reward _r_ task = _[αr]_ [rec] [+] _α_ _[β]_ + _[r]_ _β_ [p][re] + [+] _γ_ _[γ][r]_ [ded] .


Furthermore, to prevent the policy from inflating the graph size by stacking duplicate triples, we

define a repetition rate: _ρ_ rep ( _G_ ) = _[|][T]_ [(] _[G]_ [)] _[|][ −]_ _|T_ _[|]_ ( [ uni] _G_ ) [q(] _|_ _[T]_ [(] _[G]_ [))] _[|]_ and derive the trajectory return _R_ ( _τ_ ) =

_|τ_ _|_
_r_ task ( _τ_ ) _−_ _λ_ rep _ρ_ rep ( _G_ _τ_ )+ _λ_ fmt � _t_ =1 _[r]_ _t_ [fmt] . This directly addresses the issue revealed by works such
as HaluMem: errors in memory systems often do not emerge only at the answering stage, but are
already written during the extraction and updating phases [Chen et al., 2025a]. We employ standard
clipped GRPO to update the writer.


**4.2** **Memory Reader: Memory Retrieval Based on Graph Foundation Model**


The memory reader must operate stably over graph memory that is continuously updated by the writer.
Dense retrievers mainly learn query–document semantic matching and thus struggle to exploit entity
roles, bridge paths, and cross-community dependencies, while conventional GNN retrievers are often
tied to fixed graph distributions and generalize poorly across domains, users, and evolution stages.
We therefore adopt a Graph Foundation Model (GFM) as the memory reader, whose multi-graph pretraining enables transferable structural priors and lightweight calibration on new graphs [Luo et al.,
2025, Zhang et al., 2025c]. Formally, the memory reader outputs an entity distribution, a document
distribution, and an optional retrieval subgraph _f_ _ϕ_ ( _q, G, D_ ) = � _p_ _ϕ_ ( _e | q, G_ ) _, p_ _ϕ_ ( _d | q, G, D_ ) _, G_ _q_ � .
Where _p_ _ϕ_ ( _e | q, G_ ) represents the entity memory activated by the query, _p_ _ϕ_ ( _d | q, G, D_ ) denotes the
final retrieved textual evidence, and _G_ _q_ provides an interpretable retrieval path. To obtain a compact
and query-aligned activated subgraph, we further introduce a lightweight query-conditioned subgraph
selector; implementation details are provided in Appendix I.


**Cognition-inspired Structured Query Planning.** When humans extract long-term memories, the
brain often automatically generates multi-dimensional retrieval cues to anchor the target based on
only a vague final intention. Inspired by this, we no longer treat the natural language query as a single
retrieval command. Instead, we introduce a planning function _P_ _ω_ to simulate the cue reconstruction
process of the human brain before awakening memory, decomposing the initial query into a set of rich
associative probes: _P_ _ω_ ( _q_ ) = _E_ exp _, A, C_ rel _, C_ hard _, τ, {_ (˜ _q_ _m_ _, α_ _m_ _, t_ _m_ ) _}_ _[M]_ _m_ =1 . Detailed definitions
� �
of the notation, additional information, and the concrete prompt templates and output schema are
provided in Appendix K. This multi-path concurrent awakening method effectively overcomes the
"tip-of-the-tongue phenomenon" (i.e., difficulties in alias alignment or missing bridging entities) and
naturally stitches together forgotten implicit relationships [Trivedi et al., 2023, Asai et al., 2023, Wu
et al., 2025b, Zhang et al., 2025b].


**Soft Addressing and Pre-activation of Memory Fragments.** Cognitive neuroscience reveals
that human memory retrieval involves not only the extraction of perfectly matching information but
also the instinctive awakening of peripherally related memories through _Semantic Priming_ . And to
address the first challenge, we treat the calculation of the query-conditioned entry score _s_ _e_ ( _q_ ) as a
comprehensive assessment of the stimulus intensity across different _Memory Engrams_ :

_s_ _e_ ( _q_ ) = _λ_ 1 Exact( _e, E_ exp ) + _λ_ 2 Alias( _e, A_ ) + _λ_ 3 max _m≤M_ [cos] � Emb(desc( _e_ )) _,_ Emb(˜ _q_ _m_ )�




_[G]_ [)] _[∩D]_ [+] _[|]_

_|D_ [+] _|_ _, r_ pre ( _q, D_ [+] _, G_ ) = _[|][P]_ _[k]_ _|P_ [(] _[q,]_ _k_ ( _[G]_ _q,_ [)] _[∩D]_ _G_ ) _|_ [+] _[|]_



_α_ + _β_ + _γ_ .



+ _λ_ 4 Type( _e, τ_ ) + _λ_ 5 Cons( _e, C_ hard ) + _λ_ 6 � EL( _e | ξ_ ) _._ (1)

_ξ∈_ NER( _q_ )


5


Subsequently, the system employs a Softmax function with a temperature coefficient _T_ 0 to simulate
the brain’s limited Attention Allocation mechanism during retrieval. This normalizes the multidimensional stimulus signals to form the initial activation distribution of the memory atlas _p_ 0 ( _e |_
exp( _s_ _e_ ( _q_ ) _/T_ 0 )
_q_ ) = ~~�~~ _v∈VE_ [exp(] _[s]_ _[v]_ [(] _[q]_ [)] _[/T]_ [0] [)] [. Based on this distribution, we define the initial state of the memory]


_η_
nodes as **h** [(0)] _e_ = � _p_ 0 ( _e | q_ )� _W_ _q_ Emb( _q_ ) + _W_ _x_ **x** _e_ . In this process, **x** _e_ acts as the solidified **long-**
**term memory** (static representation of entities) in the brain, while the query vector adjusted by the
cognitive recall degree _p_ 0 ( _e | q_ ) represents the current **working memory** (task context).


**Synapse-inspired Structurally Conditioned Associative Propagation.** To address the second
challenge while avoiding indiscriminate diffusion, we introduce edge-level vector structural gating in
the GFM. The node-level structural features, edge-pair structural features, and graph-level summary
are defined as:


_ϕ_ ( _v_ ) = � log(1 + _d_ _v_ ) _, c_ _v_ _, κ_ _v_ _,_ _d_ [¯] _N_ ( _v_ ) � _,_ (2)

_ψ_ ( _u, v_ ) = � _|d_ _u_ _−_ _d_ _v_ _|, |N_ ( _u_ ) _∩N_ ( _v_ ) _|,_ Jaccard( _N_ ( _u_ ) _, N_ ( _v_ ))� _,_ (3)

**r** _G_ = � mean _v∈V_ _E_ _ϕ_ ( _v_ ); std _v∈V_ _E_ _ϕ_ ( _v_ ); dens( _G_ )� _._ (4)


Detailed definitions and normalization procedures are provided in Appendix L. The edge structural
context for the _l_ -th layer is **z** [(] _uv_ _[l]_ [)] [=] � _E_ _n_ [(] _[l]_ [)] [(] _[ϕ]_ [(] _[u]_ [));] _[ E]_ _n_ [(] _[l]_ [)] [(] _[ϕ]_ [(] _[v]_ [));] _[ E]_ _p_ [(] _[l]_ [)] [(] _[ψ]_ [(] _[u, v]_ [));] _[ E]_ _g_ [(] _[l]_ [)] [(] **[r]** _G_ [)] �, which generates the vector gating **g** _uv_ [(] _[l]_ [)] [=] **[ 1]** [ +] _[ δ]_ [ tanh] � MLP [(] _g_ _[l]_ [)] [(] **[z]** _uv_ [(] _[l]_ [)] [)] � . Let _η_ _uv_ be the normalized adjacency

weight with self-loops; the message and node updates are **m** [(] _u_ _[l]_ _→_ [)] _v_ [=] _[ η]_ _uv_ **[g]** _uv_ [(] _[l]_ [)] _[⊙]_ _[W]_ [ (] _m_ _[l]_ [)] **[h]** [(] _u_ _[l][−]_ [1)] _,_ **h** [(] _v_ _[l]_ [)] =
LayerNorm � **h** [(] _v_ _[l][−]_ [1)] + PReLU � **b** [(] _[l]_ [)] + [�] _u∈N_ ( _v_ ) **[m]** _u_ [(] _[l]_ _→_ [)] _v_ �� . Unlike traditional heuristic path ex
pansion, PPR walks, or community summarization [Edge et al., 2024, Guo et al., 2024, Wang and
Han, 2025], the system here can actively perform **Inhibition** of non-specific generalized memories
(suppressing hub edges), keenly capture and preserve **long-distance associations** across different
cognitive clusters (lateral thinking/bridge edge preservation), and undergo **Habituation** (weakening
redundant edges) toward highly repetitive local information, much like the human brain.


Traditional query-dependent GNNs or PPR-style expansion can perform multi-hop propagation along
graph structures. But the key issue is not simply to expand the propagation range, but to preserve
the advantage of query-relevant evidence signal over distractor noise under a limited top- _k_ budget.
Proposition 1(i) summarizes this signal–budget view: soft addressing improves the initial evidence
activation, structural gating preserves bridge/evidence paths while suppressing noisy neighborhoods,
and controlled entity-to-document projection converts the entity-level advantage into more efficient
document-level retrieval. Complete definitions, assumptions, and proofs are provided in Appendix B.


**Target Graph Calibration and Cross-graph Structural Priors.** Human memory, on one hand,
reorganizes cues based on the current context, while on the other, it retains relatively stable structured
recall habits. In our self-evolving graph memory, each _G_ generated by the writer per round alters the
local topology and noise distribution; therefore, the reader cannot rely solely on propagation patterns
from a fixed graph.


Since the writer continuously changes the memory graph, the reader must simultaneously adapt to the
current target graph and preserve cross-graph structural priors. This is precisely why we introduce the
context–schema decomposition. As summarized in Proposition 1(ii), the schema channel provides
a transferable structural prior, while the context channel corrects the target-graph residual induced
by the current writer, current domain, entity granularity, and local noise. The complete theoretical
motivation is provided in Appendix C and Appendix D.


First, a feature prompt vector ˜ **p** _f_ is used for a lightweight calibration of the query-activated input
**h** [(0)] _e_ = **p** _f_ _⊙_ **h** [(0)] _e_ [. The contextual calibration channel performs gated propagation on the current]
graph _G_ : **H** ctx = _F_ gate ( **H** [˜] [(0)] _, G_ ; Θ gate ) . Where **H** ctx captures the immediate structural state within
the current memory graph. Simultaneously, the schema prior channel maintains a set of crossgraph structural prompt bases _{_ **P** [(] _j_ _[l]_ [)] _[}]_ _[K]_ _j_ =1 [, which are used to encode stable reading habits formed]

during multi-graph training: _ω_ _j_ [(] _[l]_ [)] = softmax _j_ ( **a** [(] _[l]_ [)] _/T_ _p_ ) _,_ **P** [(] schema _[l]_ [)] [=][ �] _[K]_ _j_ =1 _[ω]_ _j_ [(] _[l]_ [)] **[P]** [(] _j_ _[l]_ [)] [. Propagation is]

executed based on these schema prompts to obtain: **H** sch = _F_ prompt � **H** ˜ (0) _, G_ ; _{_ **P** (schema _l_ ) _[}]_ _l_ _[L]_ =1 � . The


6


final entity representation is jointly determined by the current context and the long-term schema:
**H** ( _q, G_ ) = **H** ctx + _β_ sch **H** sch . Here, **H** ctx is analogous to a context-dependent immediate recall state,
responsible for adapting to the specific graph structure generated by the current writer; **H** sch is akin
to a memory schema formed across experiences, retaining the ability to recognize stable patterns
such as bridge nodes, community boundaries, core–periphery structures, and noise short-circuits.


**Reader Training.** Reader training aims to learn cross-graph transferable retrieval biases through a
two-stage procedure. First, we perform structural contrastive pre-training on multiple augmented
graph views. Then, in the supervised fine-tuning stage, we align these transferable capabilities with
question-driven evidence retrieval by training the reader to identify and rank supporting entities
for each query using weighted classification and multi-positive ranking objectives. Implementation
details are provided in Appendices M and N.


**Writer–Reader Self-evolution.** To address the third challenge, we propose a self-evolution framework. Each of our self-evolution iterations consists of two phases. First, we fix the reader and train
the writer using its retrieval results as rewards. Subsequently, we use the updated writer to generate
new graphs and continue training the reader. The overall procedure is detailed in Algorithm 1.







From a theoretical perspective, this process can be interpreted as approximate coordinate improvement
over a joint memory utility: the writer update improves the readability of the graph memory, while
the reader update reduces writer-induced graph distribution shift and reward bias. We provide the
full coordinate-improvement result, the surrogate reward bias bound, and the analysis of singlesided update bottlenecks in Appendix F. In addition, Proposition 1(iii) shows that although each
writer update changes the graph structure in self-evolving memory, the reader output does not
oscillate arbitrarily with graph evolution. We provide detailed training, inference, memory, and
selector-regularizer complexity analyses in Appendix J.


**5** **Experiments**


This section presents an experimental evaluation centered around four research questions (RQs).
_**RQ1**_ : whether SAGE can bring consistent benefits in tasks such as multi-hop QA and open-domain
transfer;


_**RQ2**_ : whether SAGE is an agent memory system capable of handling long-term conversation history,
knowledge updates, and memory hallucination;


_**RQ3**_ : whether the writer–reader closed loop truly yields self-evolution benefits;


_**RQ4**_ : further analysis of where and how the performance gains come from specific designs.


**Datasets.** We evaluate SAGE on five complementary scenarios. The first category consists of
general QA benchmarks and three multi-hop QA benchmarks, including NQ, PopQA, HotpotQA,
2WikiMultiHopQA, and MuSiQue, used to examine whether the system can recover bridge entities
across documents and combine evidence and reasoning paths. The second category focuses on
a practical e-commerce application scenario, using a Review-Based Question Answering Task:
AmazonQA, to assess its value in real e-commerce applications with real noisy reviews. The third


7


Table 1: Open-domain retrieval results on `NQ` and `PopQA` . We report passage/document-level Recall
(%) at top-2 and top-5 when comparable numbers are available in original papers or later works that
reproduce/cite these methods. Best available results are in **bold** and runner-ups are underlined . **Only**
**rows marked with** **[0-shot]** **are our zero-shot transfer results; baseline rows are not marked as**
**zero-shot.**

### Zero-shot setting applies only to SAGE on NQ and PopQA . Dataset NQ PopQA Method R@2 D R@5 D R@2 D R@5 D BM25 (� SIGIR’94 ) 28. 2 [†] 56. 1 [†] 24. 0 [†] 35. 7 [†] Contriever (� TMLR’22 ) 29. 1 [†] 54. 6 [†] 27. 0 [†] 43. 2 [†] GTR (� EMNLP’22 ) 35. 0 [†] 63. 4 [†] 40. 1 [†] 49. 4 [†] ColBERTv2 (� NAACL’22 ) 36. 8 [⋆] 64. 3 [⋆] – – RAPTOR (� ICLR’24 ) 40. 3 [†] 68. 3 [†] 40. 2 [†] 48. 7 [†] Proposition (� EMNLP’24 ) 33. 1 [⋆] 62. 2 [⋆] – – HippoRAG (� NeurIPS’24 ) 21. 3 [†] 44. 4 [†] 40. 0 [†] 53. 8 [†] HippoRAG 2 (� ICML’25 ) 45. 6 [†] 78. 0 [†] 43. 9 [†] 51. 7 [†] PropRAG (� EMNLP’25 ) – 77. 9 [‡] – 56. 2 [‡] SAGE (ours) [0-shot] 82. 5 [0-shot] 91. 6 [0-shot] 41. 5 [0-shot] 52. 3 [0-shot]


_†_ Values are from the reproduced passage Recall@2/5 evaluation in � . _‡_ Values are from the Recall@5 table in � ; Recall@2
is not reported there. _[⋆]_ Values are from the reproduced single-step retrieval table in �; PopQA is not reported there.


Figure 3: Visualization of the retrieved results.


category comprises long-term agent memory datasets, including LongMemEval and HaluMem, used
to test information extraction from long interaction histories, multi-session reasoning, temporal
reasoning, knowledge updating, abstention, and operation-level hallucination. Table 13 summarizes
the details of each dataset. Further details on baselines and metrics can be found in Appendix R.


**5.1** **End-to-End Effectiveness**


**Multi-hop Question Answering** Table 3 reports the main results on general QA benchmarks and
three multi-hop QA benchmarks. Table 9 reports the results of retrieval performance on multi-hop
QA benchmarks. It is worth mentioning that even when we directly test on NQ and PopQA using a


1 `memobase` : `[https://github.com/memodb-io/memobase](https://github.com/memodb-io/memobase)` .
2 `Supermemory` : `[https://github.com/supermemoryai/supermemory](https://github.com/supermemoryai/supermemory)` .
3 `MemU` : `[https://github.com/NevaMind-AI/memU](https://github.com/NevaMind-AI/memU)` .


8


Table 2: Performance of representative memory systems on `LongMemEval` . We report accuracy (%)
on six task categories: single-session user (SS-U), single-session assistant (SS-A), merged singlesession recall (SSR), single-session preference (SS-P), knowledge update (KU), temporal reasoning
(TR), and multi-session reasoning (MS). SSR is computed as the weighted average of SS-U and SS-A
when both are available; if a source reports only merged single-session recall, SS-U/SS-A are left
blank. Best results are in **bold** and runner-ups are underlined . The darker the cell, the better. Results
are grouped by reporting protocol and should not be treated as a single strict leaderboard. **Only rows**
**marked with** **[0-shot]** **are our zero-shot transfer results; baseline rows and trained variants are not**
**marked as zero-shot.**


**Zero-shot setting applies only to** `Ours` **rows marked with** **[0-shot]** **on** `LongMemEval` **.**

**Dataset** `LongMemEval-S / LongMemEval`

**Method** SS-U SS-A SSR SS-P KU TR MS Overall

_Unified protocol in TiMem (GPT-4o-mini, LLJ accuracy)_

_MemOS evaluation suite (short-answer prompt)_

_Our method_


model trained only on MuSiQue, HotpotQA, and 2WikiMultiHopQA, we still achieve very strong
performance, especially on NQ; see Table 1 for the detailed results.



**Domain-specific Memory** Table 10 reports the results
on AmazonQA. SAGE consistently outperforms the neural baseline R-Net across all metrics, indicating strong
cross-task generalization. After training on AmazonQA,
Ours achieves substantial gains. Overall, training and interaction rounds steadily enhance performance, while the
zero-shot results demonstrate promising transfer ability.


**5.2** **Long-term Agent Memory Evaluation**


The LongMemEval results are shown in Table 2. The
HaluMem results are shown in Table 11. SAGE is compared against highly specialized long-term memory systems, making this a challenging evaluation setting. Although SAGE does not yet surpass the strongest systemlevel baselines. Notably, SAGE +1 round already outperforms Memobase on several metrics, suggesting that it is
competitive despite being less system-engineered. The re

9



Table 4: Retrieval efficiency comparison.
We report retrieval time in seconds on
`HotpotQA`, `MuSiQue`, and `2Wiki` . For
Time, lower is better. Best results are in
**bold** and runner-ups are underlined . The
darker the cell, the better.


**Dataset** `HotpotQA MuSiQue 2Wiki`

**Method** Time _↓_ Time _↓_ Time _↓_

_Single-step retrieval methods_

_Iterative retrieval methods_


Table 3: Results of multi-hop question answering (QA) performance. We report Exact Match (EM)
and F1 score, both reported as percentages (%). Best results are in **bold** and runner-ups are underlined .
The darker the cell, the better.


**Dataset** `HotpotQA` `MuSiQue` `2WikiMultiHopQA`
**Avg. Rank**
**Method** EM F1 EM F1 EM F1

`BM25` (� _arXiv’24_ ) 40. 0 53. 2 19. 5 23. 6 46. 9 57. 9 15. 5


maining gap mainly lies in memory updating and high-coverage extraction, indicating clear potential
for further gains with stronger memory management and update mechanisms.


**5.3** **Further Analysis**

As shown in Table 4, SAGE demonstrates a strong speed advantage. It achieves the fastest retrieval
time, indicating strong potential for practical and large-scale deployment. To further analyze the
interpretability of SAGE, we visualize the retrieved subgraph for a representative case, as shown in
Figure. A detailed case study can be found in P.1. The detailed ablation study design, analysis, and
results for the Memory Writer and Reader can be found in Appendix H and Appendix G, respectively.


**6** **Conclusion**


We presented SAGE, a self-evolving agentic graph-memory engine that treats memory as a dynamic
substrate for writing, reading, and continual improvement. Experiments show that SAGE improves
evidence recovery, grounding, and retrieval efficiency, suggesting that self-evolving graph memory is
a promising foundation for long-horizon language agents.


10


**References**


Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-rag: Learning to
retrieve, generate, and critique through self-reflection. In _The Twelfth International Conference on_
_Learning Representations_, 2023.


Sungguk Cha, DongWook Kim, Taeseung Hahn, Mintae Kim, Youngsub Han, and Byoung-Ki Jeon.
Annotation-free reinforcement learning query rewriting via verifiable search reward. _arXiv preprint_
_arXiv:2507.23242_, 2025.


Ding Chen, Simin Niu, Kehang Li, Peng Liu, Xiangping Zheng, Bo Tang, Xinchi Li, Feiyu Xiong,
and Zhiyu Li. Halumem: Evaluating hallucinations in memory systems of agents. _arXiv preprint_
_arXiv:2511.03506_, 2025a.


Tong Chen, Hongwei Wang, Sihao Chen, Wenhao Yu, Kaixin Ma, Xinran Zhao, Hongming Zhang,
and Dong Yu. Dense x retrieval: What retrieval granularity should we use? In _Proceedings of the_
_2024 Conference on Empirical Methods in Natural Language Processing_, pages 15159–15177,
2024.


Yiqun Chen, Lingyong Yan, Weiwei Sun, Xinyu Ma, Yi Zhang, Shuaiqiang Wang, Dawei Yin,
Yiming Yang, and Jiaxin Mao. Improving retrieval-augmented generation through multi-agent
reinforcement learning. _arXiv preprint arXiv:2501.15228_, 2025b.


Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. Mem0: Building
production-ready ai agents with scalable long-term memory. _arXiv preprint arXiv:2504.19413_,
2025.


Hongwei Wang Di Wu, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu Longmemeval.
Benchmarking chat assistants on long-term interactive memory, 2024. _URL https://arxiv._
_org/abs/2410.10813_, 2:14.


Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt,
Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. From local to global: A
graph rag approach to query-focused summarization. _arXiv preprint arXiv:2404.16130_, 2024.


Zirui Guo, Lianghao Xia, Yanhua Yu, Tian Ao, and Chao Huang. Lightrag: Simple and fast
retrieval-augmented generation. _arXiv preprint arXiv:2410.05779_, 2(3), 2024.


Mansi Gupta, Nitish Kulkarni, Raghuveer Chanda, Anirudha Rayasam, and Zachary C Lipton.
Amazonqa: A review-based question answering task. _arXiv preprint arXiv:1908.04364_, 2019.


Bernal J Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. Hipporag: Neurobiologically
inspired long-term memory for large language models. _Advances in neural information processing_
_systems_, 37:59532–59569, 2024.


Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe Zhou, and Yu Su. From rag to memory:
Non-parametric continual learning for large language models. _arXiv preprint arXiv:2502.14802_,
2025.


Xiaoxin He, Yijun Tian, Yifei Sun, Nitesh V Chawla, Thomas Laurent, Yann LeCun, Xavier Bresson,
and Bryan Hooi. G-retriever: Retrieval-augmented generation for textual graph understanding and
question answering. _Advances in Neural Information Processing Systems_, 37:132876–132907,
2024.


Yuanzhe Hu, Yu Wang, and Julian McAuley. Evaluating memory in llm agents via incremental
multi-turn interactions. _arXiv preprint arXiv:2507.05257_, 2025.


Ziniu Hu, Yuxiao Dong, Kuansan Wang, Kai-Wei Chang, and Yizhou Sun. Gpt-gnn: Generative
pre-training of graph neural networks. In _Proceedings of the 26th ACM SIGKDD international_
_conference on knowledge discovery & data mining_, pages 1857–1867, 2020.


Zhengjun Huang, Zhoujin Tian, Qintian Guo, Fangyuan Zhang, Yingli Zhou, Di Jiang, Zeying
Xie, and Xiaofang Zhou. Licomemory: Lightweight and cognitive agentic memory for efficient
long-term reasoning. _arXiv preprint arXiv:2511.01448_, 2025.


11


Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. GPT-4o system card. _arXiv preprint_
_arXiv:2410.21276_, 2024.


Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand
Joulin, and Edouard Grave. Unsupervised dense information retrieval with contrastive learning.
_arXiv preprint arXiv:2112.09118_, 2021.


Soyeong Jeong, Jinheon Baek, Sukmin Cho, Sung Ju Hwang, and Jong C Park. Adaptive-rag:
Learning to adapt retrieval-augmented large language models through question complexity. In
_Proceedings of the 2024 Conference of the North American Chapter of the Association for Compu-_
_tational Linguistics: Human Language Technologies (Volume 1: Long Papers)_, pages 7036–7050,
2024.


Zhengbao Jiang, Frank F Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang,
Jamie Callan, and Graham Neubig. Active retrieval augmented generation. In _Proceedings of the_
_2023 conference on empirical methods in natural language processing_, pages 7969–7992, 2023.


Jiazheng Kang, Mingming Ji, Zhe Zhao, and Ting Bai. Memory os of ai agent. In _Proceedings of the_
_2025 Conference on Empirical Methods in Natural Language Processing_, pages 25972–25981,
2025.


Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal,
Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. Retrieval-augmented generation for knowledge-intensive nlp tasks. _Advances in neural information processing systems_, 33:
9459–9474, 2020.


Kai Li, Xuanqing Yu, Ziyi Ni, Yi Zeng, Yao Xu, Zheqing Zhang, Xin Li, Jitao Sang, Xiaogang
Duan, Xuelei Wang, et al. Timem: Temporal-hierarchical memory consolidation for long-horizon
conversational agents. _arXiv preprint arXiv:2601.02845_, 2026a.


Mufei Li, Siqi Miao, and Pan Li. Simple is effective: The roles of graphs and large language models
in knowledge-graph-based retrieval-augmented generation. _arXiv preprint arXiv:2410.20724_,
2024.


Yifei Li, Weidong Guo, Lingling Zhang, Rongman Xu, Muye Huang, Hui Liu, Lijiao Xu, Yu Xu, and
Jun Liu. Locomo-plus: Beyond-factual cognitive memory evaluation framework for llm agents.
_arXiv preprint arXiv:2602.10715_, 2026b.


Zhiyu Li, Shichao Song, Hanyu Wang, Simin Niu, Ding Chen, Jiawei Yang, Chenyang Xi, Huayi
Lai, Jihao Zhao, Yezhaohui Wang, et al. Memos: An operating system for memory-augmented
generation (mag) in large language models. _arXiv preprint arXiv:2505.22101_, 2025.


Jiawei Liu, Cheng Yang, Zhiyuan Lu, Junze Chen, Yibo Li, Mengmei Zhang, Ting Bai, Yuan Fang,
Lichao Sun, Philip S Yu, et al. Graph foundation models: Concepts, opportunities and challenges.
_IEEE Transactions on Pattern Analysis and Machine Intelligence_, 2025.


Linhao Luo, Zicheng Zhao, Gholamreza Haffari, Dinh Phung, Chen Gong, and Shirui Pan. Gfm-rag:
graph foundation model for retrieval augmented generation. _arXiv preprint arXiv:2502.01113_,
2025.


Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit Bansal, Francesco Barbieri, and Yuwei
Fang. Evaluating very long-term conversational memory of llm agents. In _Proceedings of the 62nd_
_Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_, pages
13851–13870, 2024.


Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Hernandez Abrego, Ji Ma, Vincent Zhao,
Yi Luan, Keith Hall, Ming-Wei Chang, et al. Large dual encoders are generalizable retrievers.
In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_,
pages 9844–9855, 2022.


Charles Packer, Vivian Fang, Shishir_G Patil, Kevin Lin, Sarah Wooders, and Joseph_E Gonzalez.
Memgpt: towards llms as operating systems. 2023.


12


Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S
Bernstein. Generative agents: Interactive simulacra of human behavior. In _Proceedings of the 36th_
_annual acm symposium on user interface software and technology_, pages 1–22, 2023.


Jiezhong Qiu, Qibin Chen, Yuxiao Dong, Jing Zhang, Hongxia Yang, Ming Ding, Kuansan Wang,
and Jie Tang. Gcc: Graph contrastive coding for graph neural network pre-training. In _Proceedings_
_of the 26th ACM SIGKDD international conference on knowledge discovery & data mining_, pages
1150–1160, 2020.


Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. Zep: a temporal
knowledge graph architecture for agent memory. _arXiv preprint arXiv:2501.13956_, 2025.


Stephen E Robertson and Steve Walker. Some simple effective approximations to the 2-poisson
model for probabilistic weighted retrieval. In _SIGIR’94: Proceedings of the Seventeenth Annual_
_International ACM-SIGIR Conference on Research and Development in Information Retrieval,_
_organised by Dublin City University_, pages 232–241. Springer, 1994.


Keshav Santhanam, Omar Khattab, Jon Saad-Falcon, Christopher Potts, and Matei Zaharia. Colbertv2:
Effective and efficient retrieval via lightweight late interaction. In _Proceedings of the 2022_
_Conference of the North American Chapter of the Association for Computational Linguistics:_
_Human Language Technologies_, pages 3715–3734, 2022.


Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christopher D Manning.
Raptor: Recursive abstractive processing for tree-organized retrieval. In _The Twelfth International_
_Conference on Learning Representations_, 2024.


Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. MuSiQue: Multihop
questions via single-hop question composition. _Transactions of the Association for Computational_
_Linguistics_, 10:539–554, 2022.


Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Interleaving retrieval
with chain-of-thought reasoning for knowledge-intensive multi-step questions. In _Proceedings of_
_the 61st annual meeting of the association for computational linguistics (volume 1: long papers)_,
pages 10014–10037, 2023.


Hong Ting Tsang, Jiaxin Bai, Haoyu Huang, Qiao Xiao, Tianshi Zheng, Baixuan Xu, Shujie Liu, and
Yangqiu Song. Autograph-r1: End-to-end reinforcement learning for knowledge graph construction.
_arXiv preprint arXiv:2510.15339_, 2025.


Jingjin Wang and Jiawei Han. Proprag: Guiding retrieval with beam search over proposition paths.
In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_,
pages 6223–6238, 2025.


Yu Wang and Xi Chen. Mirix: Multi-agent memory system for llm-based agents. _arXiv preprint_
_arXiv:2507.07957_, 2025.


Yaxiong Wu, Sheng Liang, Chen Zhang, Yichao Wang, Yongyue Zhang, Huifeng Guo, Ruiming
Tang, and Yong Liu. From human memory to ai memory: A survey on memory mechanisms in the
era of llms. _arXiv preprint arXiv:2504.15965_, 2025a.


Yaxiong Wu, Yongyue Zhang, Sheng Liang, and Yong Liu. Sgmem: Sentence graph memory for
long-term conversational agents. _arXiv preprint arXiv:2509.21212_, 2025b.


Tianyang Xu, Haojie Zheng, Chengze Li, Haoxiang Chen, Yixin Liu, Ruoxi Chen, and Lichao Sun.
Noderag: Structuring graph-based rag with heterogeneous nodes. _arXiv preprint arXiv:2504.11544_,
2025a.


Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan, and Yongfeng Zhang. A-mem: Agentic
memory for llm agents. _arXiv preprint arXiv:2502.12110_, 2025b.


Chang Yang, Chuang Zhou, Yilin Xiao, Su Dong, Luyao Zhuang, Yujing Zhang, Zhu Wang, Zijin
Hong, Zheng Yuan, Zhishang Xiang, et al. Graph-based agent memory: Taxonomy, techniques,
and applications. _arXiv preprint arXiv:2602.05665_, 2026.


13


Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov,
and Christopher D Manning. HotpotQA: A dataset for diverse, explainable multi-hop question
answering. In _Proceedings of the 2018 Conference on Empirical Methods in Natural Language_
_Processing_, pages 2369–2380, 2018.


Yuning You, Tianlong Chen, Yongduo Sui, Ting Chen, Zhangyang Wang, and Yang Shen. Graph
contrastive learning with augmentations. _Advances in neural information processing systems_, 33:
5812–5823, 2020.


Xingtong Yu, Zechuan Gong, Chang Zhou, Yuan Fang, and Hui Zhang. Samgpt: Text-free graph
foundation model for multi-domain pre-training and cross-domain adaptation. In _Proceedings of_
_the ACM on Web Conference 2025_, pages 1142–1153, 2025.


Juwei Yue, Chuanrui Hu, Jiawei Sheng, Zuyi Zhou, Wenyuan Zhang, Tingwen Liu, Li Guo, and
Yafeng Deng. Hypermem: Hypergraph memory for long-term conversations. _arXiv preprint_
_arXiv:2604.08256_, 2026.


Guibin Zhang, Muxin Fu, Guancheng Wan, Miao Yu, Kun Wang, and Shuicheng Yan. G-memory:
Tracing hierarchical memory for multi-agent systems. _arXiv preprint arXiv:2506.07398_, 2025a.


Kai Zhang, Xinyuan Zhang, Ejaz Ahmed, Hongda Jiang, Caleb Kumar, Kai Sun, Zhaojiang Lin, Sanat
Sharma, Shereen Oraby, Aaron Colak, et al. Assomem: Scalable memory qa with multi-signal
associative retrieval. _arXiv preprint arXiv:2510.10397_, 2025b.


Qinggang Zhang, Shengyuan Chen, Yuanchen Bei, Zheng Yuan, Huachi Zhou, Zijin Hong, Hao Chen,
Yilin Xiao, Chuang Zhou, Junnan Dong, et al. A survey of graph retrieval-augmented generation
for customized large language models. _arXiv preprint arXiv:2501.13958_, 2025c.


Yibo Zhao, Jiapeng Zhu, Ye Guo, Kangkang He, and Xiang Li. Eˆ 2graphrag: Streamlining graphbased rag for high efficiency and effectiveness. _arXiv preprint arXiv:2505.24226_, 2025.


Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large
language models with long-term memory. In _Proceedings of the AAAI conference on artificial_
_intelligence_, volume 38, pages 19724–19731, 2024.


14


**Algorithm 1:** Writer–Reader Self-evolution Training for SAGE
**Input:** Training set _D_ train, writer _π_ _θ_ 0, GFM reader _f_ _ϕ_ 0, self-evolution iterations _T_
**Output:** Trained writer _π_ _θ_ _T_ and reader _f_ _ϕ_ _T_
**1** **for** _t_ = 0 _, . . ., T −_ 1 **do**

**2** `// Writer update:` `fixed GFM reader as reward environment`

**3** **for** _each sample x_ = ( _q, D, D_ [+] _, y_ ) _∈D_ train **do**

**4** Sample _G_ graph construction trajectories _{τ_ _i_ _}_ _[G]_ _i_ =1 [from] _[ π]_ _[θ]_ _t_ [;]

**5** **for** _i_ = 1 _, . . ., G_ **do**

**6** Obtain graph _G_ _i_ and retrieve _P_ _k_ ( _q, G_ _i_ ) using _f_ _ϕ_ _t_ ;

**7** Calculate return _R_ _i_ ;


**8** **end**

**9** Update writer _π_ _θ_ _t_ ;

**10** **end**

**11** `// Reader update:` `improved graphs as memory substrate`

**12** Construct a set of graph memories _{G_ _x_ _}_ for the training corpus using _π_ _θ_ _t_ +1 ;

**13** Update GFM reader _f_ _ϕ_ _t_ on _{G_ _x_ _}_ ;

**14** **end**


**A** **Additional Analysis of the Memory Writer**


This appendix provides a detailed analysis of the memory writer experiments in the main text.


**A.1** **Reward Design and Writer Behavior**


In Table 5, different RL rewards induce different writer behaviors. GFM-pretrained-only achieves Precision/Recall/Deducible of 0 _._ 838 _/_ 0 _._ 818 _/_ 0 _._ 510, while GFM-finetuned achieves 0 _._ 824 _/_ 0 _._ 813 _/_ 0 _._ 512,
indicating that relying solely on supervised finetuning cannot stably improve the utility of graph
memory for a frozen reader. This result is also consistent with our setup: the goal of the memory
writer is not to reproduce a static graph format.


RL-Recall improves Precision and Recall to 0 _._ 889 _/_ 0 _._ 835, but Deducible drops to 0 _._ 502 . This
shows that rewarding only supporting context coverage encourages the writer to store more locally
relevant evidence, but does not necessarily lead to a complete multi-hop reasoning chain. RLF1 further raises Recall to 0 _._ 881, but Deducible is only 0 _._ 497, again indicating a gap between
retrieval matching quality and answer deducibility: the reader hitting the supporting contexts does
not guarantee that these contexts are organized in a way sufficient to support answer reasoning. In
contrast, RL-Deduce achieves 0 _._ 861 _/_ 0 _._ 892 _/_ 0 _._ 517, showing that using answer deducibility directly
as feedback can encourage the writer to focus more on bridging entities, cross-document relations,
and answer-relevant causal or attribute paths.


RL-Hybrid achieves Precision and Recall of **0** _._ **902** and **0** _._ **917**, respectively, representing improvements of +0 _._ 064 and +0 _._ 099 over pretrained-only, while Deducible reaches 0 _._ 522 . This indicates
that hybrid rewards can mitigate the bias of a single reward: they both avoid the introduction of too
much weakly relevant evidence caused by a pure recall reward and prevent a pure deducibility reward
from overfavoring short paths or local answer clues. Hybrid + frozen answer API achieves the highest
Deducible, at **0** _._ **526**, but Precision and Recall drop to 0 _._ 832 _/_ 0 _._ 874 . This suggests that stronger
answer-side feedback can further improve reasoning usability, but it may also make the writer more
conservative, writing only evidence directly related to the final answer and thereby sacrificing some
supporting context coverage.


**A.2** **Cross-domain Transfer**


Table 6 shows that the base writer trained on HotpotQA/MuSiQue has a certain degree of transferability to new domains, but training on the target domain remains very important. On GRBench, Base _→_ GRBench achieves Precision/Recall/Deducible of 0 _._ 575 _/_ 0 _._ 609 _/_ 0 _._ 411, while GRBench train _→_ val improves to 0 _._ 794 _/_ 0 _._ 833 _/_ 0 _._ 596 . This improvement indicates that the writing
strategy learned for multi-hop QA can transfer to structured product or domain graph memory tasks,


15


|reward|Col2|Col3|Col4|Col5|Col6|Col7|Col8|
|---|---|---|---|---|---|---|---|
|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|
|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>11<br>528<br>10<br>12<br>18<br>15<br>05|
||0.5||0.|0.5<br>|0.5|0.5<br>0.5|0.5|
|||||||||
|||||||||


|reward|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|
|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|0.639<br>.547<br>0.613<br>0.615<br>25<br>05<br>25<br>528|
|||0<br>0.5|0<br>0.5|0<br>0.5|0.5||0.5|0.5||0.|
||||||||||||
||||||||||||
|||n<br>of|n<br>of|n<br>of|f<br>off@|f<br>off@|10<br>off@|10<br>off@|10<br>off@|10<br>off@|


|Top-k budget sweep Ranker variants<br>1.0 reward 1.0 reward<br>deducible deducible<br>0.8 0.8<br>0.6 0.6 Mean 0.5110.617 0.5280.623 0.5100.593 0.5120.605 0.5180.622 0.5150.591 0.5050.612 Mean 0.620 0.519 0.630 0.544 0.626 0.538 0.626 0.519 0.604 00 .. 55 12 7 02 . 0. 56 91 53 0.506<br>0.4 0.4<br>0.2 0.2<br>0.0 0.0<br>3 5 10 20 40 60 80 idf-topk20 topk20 idf-only raw topk5 idf-tt oo pp kk 64 00|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|3<br>5<br>10<br>20<br>40<br>60<br>80<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>0.511<br>0.528<br>0.510<br>0.512<br>0.518<br>0.515<br>0.505<br>Top~~-~~k budget sweep<br>~~reward~~<br>deducible<br>idf-topk20<br>topk20<br>idf-only<br>raw<br>topk5<br>topk40<br>idf-topk60<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>0.519<br>0.544<br>0.538<br>0.519<br>0.522<br>0.517<br>0.506<br>Ranker variants<br>~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|~~reward~~<br>deducible|
|3<br>5<br>10<br>20<br>40<br>60<br>80<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>0.511<br>0.528<br>0.510<br>0.512<br>0.518<br>0.515<br>0.505<br>Top~~-~~k budget sweep<br>~~reward~~<br>deducible<br>idf-topk20<br>topk20<br>idf-only<br>raw<br>topk5<br>topk40<br>idf-topk60<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>0.519<br>0.544<br>0.538<br>0.519<br>0.522<br>0.517<br>0.506<br>Ranker variants<br>~~reward~~<br>deducible|0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>19<br>.544<br>538<br>19<br>22<br>17<br>06|0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>19<br>.544<br>538<br>19<br>22<br>17<br>06|0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>19<br>.544<br>538<br>19<br>22<br>17<br>06|0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>19<br>.544<br>538<br>19<br>22<br>17<br>06|0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>19<br>.544<br>538<br>19<br>22<br>17<br>06|
|3<br>5<br>10<br>20<br>40<br>60<br>80<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>0.511<br>0.528<br>0.510<br>0.512<br>0.518<br>0.515<br>0.505<br>Top~~-~~k budget sweep<br>~~reward~~<br>deducible<br>idf-topk20<br>topk20<br>idf-only<br>raw<br>topk5<br>topk40<br>idf-topk60<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>0.519<br>0.544<br>0.538<br>0.519<br>0.522<br>0.517<br>0.506<br>Ranker variants<br>~~reward~~<br>deducible|0.5<br>0||0.<br>|0.5<br>0.5<br>0.5|0.5|
|3<br>5<br>10<br>20<br>40<br>60<br>80<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>0.511<br>0.528<br>0.510<br>0.512<br>0.518<br>0.515<br>0.505<br>Top~~-~~k budget sweep<br>~~reward~~<br>deducible<br>idf-topk20<br>topk20<br>idf-only<br>raw<br>topk5<br>topk40<br>idf-topk60<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>0.519<br>0.544<br>0.538<br>0.519<br>0.522<br>0.517<br>0.506<br>Ranker variants<br>~~reward~~<br>deducible||||||
|3<br>5<br>10<br>20<br>40<br>60<br>80<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>0.511<br>0.528<br>0.510<br>0.512<br>0.518<br>0.515<br>0.505<br>Top~~-~~k budget sweep<br>~~reward~~<br>deducible<br>idf-topk20<br>topk20<br>idf-only<br>raw<br>topk5<br>topk40<br>idf-topk60<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>0.519<br>0.544<br>0.538<br>0.519<br>0.522<br>0.517<br>0.506<br>Ranker variants<br>~~reward~~<br>deducible||||||
|3<br>5<br>10<br>20<br>40<br>60<br>80<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.617<br>0.623<br>0.593<br>0.605<br>0.622<br>0.591<br>0.612<br>0.511<br>0.528<br>0.510<br>0.512<br>0.518<br>0.515<br>0.505<br>Top~~-~~k budget sweep<br>~~reward~~<br>deducible<br>idf-topk20<br>topk20<br>idf-only<br>raw<br>topk5<br>topk40<br>idf-topk60<br>0.0<br>0.2<br>0.4<br>0.6<br>0.8<br>1.0<br>Mean<br>0.620<br>0.630<br>0.626<br>0.626<br>0.604<br>0.613<br>0.595<br>0.519<br>0.544<br>0.538<br>0.519<br>0.522<br>0.517<br>0.506<br>Ranker variants<br>~~reward~~<br>deducible|||||opk60|



Figure 4: Freeze the sensitivity analysis on the reader side. The impact of the initial-entity weight
on reward and Deducible is the most stable; the top- _k_ and ranker variants exhibit a non-monotonic
budget–noise trade-off.


but the entity types, attribute relations, and evidence granularity in the target domain still need to be
re-adapted.


On HaluMem and LongMemEval, cross-domain differences are even more pronounced. The
Base _→_ HaluMem results are 0 _._ 230 _/_ 0 _._ 448 _/_ 0 _._ 299, which improve to 0 _._ 312 _/_ 0 _._ 708 _/_ 0 _._ 438 after training
on the target domain; the Base _→_ LongMemEval results are 0 _._ 232 _/_ 0 _._ 376 _/_ 0 _._ 475, which improve to
0 _._ 377 _/_ 0 _._ 439 _/_ 0 _._ 531 after training on the target domain. These results indicate that memory writing in
agent memory tasks requires not only extracting explicit facts, but also maintaining user preferences,
temporal order, state updates, and long-term consistency. In traditional multi-hop QA, supporting
contexts often form a relatively static set of evidence centered around a single question, whereas information in long-term memory tasks changes over time and involves personalization, conflict updates,
and context dependence. Therefore, although reader-aware RL feedback can provide transferable
writing principles, interaction feedback from the target domain remains crucial for achieving stable
performance.


**A.3** **Writing Protocol and Interaction Budget**


Table 7 shows that the writing protocol significantly changes the trade-off among Precision, Recall,
and Deducible. The results for Tight=True are 0 _._ 836 _/_ 0 _._ 806 _/_ 0 _._ 515 ; the results for Tight=False are
0 _._ 845 _/_ 0 _._ 851 _/_ 0 _._ 506 . After relaxing the protocol, Recall improves noticeably, indicating that the
writer can write more potentially relevant evidence; however, Deducible declines, suggesting that the
additional evidence also contains more noise, redundant facts, or weakly related local information.
Although this content may increase the coverage of supporting context, it can dilute the reasoning
chain that truly supports the answer.


Iterative writing further highlights the role of the interaction budget. For Iterative, 12 turns, tight,
Precision/Recall/Deducible are 0 _._ 852 _/_ 0 _._ 829 _/_ 0 _._ 516 ; after increasing to 20 turns, Recall reaches the
highest value of **0** _._ **881**, indicating that multi-turn reader feedback helps the writer complete crossdocument bridging paths. For Iterative, 24 turns, loose, Precision and Deducible reach **0** _._ **863** and
**0** _._ **531**, respectively, but Recall falls back to 0 _._ 826 . This shows that more rounds of interaction are
not simply “the longer, the better”: the benefit comes from the writer revising the graph structure
based on reader feedback, whereas when the protocol is too loose or the writing space becomes too
large, the additional content may alter the reader’s ranking, causing some gold supporting contexts to
be pushed out of the top results.


**A.4** **Reader-side Sensitivity**


Figure 4 analyzes the impact of the frozen reader setting on writer training results. First, the top- _k_
budget sweep shows a non-monotonic trend: at _k_ = 5, reward and Deducible are 0 _._ 623 _/_ 0 _._ 528, the
better setting in this group; at _k_ = 40, reward remains at 0 _._ 622, but Deducible drops to 0 _._ 518 ; at
_k_ = 60, reward further declines to 0 _._ 591 . This indicates that expanding the retrieval budget does not
necessarily lead to better reader feedback. Although a larger top- _k_ improves potential coverage, it
also introduces more weakly related or redundant evidence, diluting the reasoning chain that truly
supports the answer.


16


0.0


1.0


0.8


0.6


0.4


0.2


0.0



1.0


0.8


0.6


0.4


0.2


0.0

|8|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|0.585<br>0.610<br>0.582<br>0.619<br>0.597<br><br><br>|
|~~0~~|~~.510~~|~~.510~~||~~0.520~~|~~0.520~~||~~0.512~~|~~0.512~~|~~0.522~~|0.500|0.500|
|~~0~~||||||||||||
|||||||||||||
|||||||||||||



1.0


0.8


0.6


0.4


0.2


0.0






|0.585 0.621 0.617 0.625|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||~~0.510~~|~~0.510~~||~~0.516~~|~~0.516~~||~~0.517~~|~~0.517~~||~~0.518~~|~~0.518~~|
||||||||||||||
||||||||||||||
||||||||||||||


|0 Rollout group size|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|0.610<br>0.590<br>0.611<br>0.620<br><br><br>|
||~~0.511~~|~~0.511~~||0.503|0.503||~~0.525~~|~~0.531~~|~~0.531~~|
|||||||||||
|||||||||||
|||||||||||


|Warmup ratio|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||
|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|0.601<br>0.600<br>0.585<br>0.614<br><br><br>|
|||~~0.521~~|~~0.521~~||~~0.529~~|~~0.529~~||~~0.510~~|~~0.510~~||~~0.513~~|~~0.513~~|
||||||||||||||
||||||||||||||
||||||||||||||



Figure 5: Training regularization and scaling analysis. A larger rollout group size and a moderate
warmup ratio show a slight advantage in this batch of results, but the gains are smaller than the effects
of reward design, the reader-side initial-entity weight, and the writing protocol.


The ranker variants also reflect a similar coverage–noise trade-off. topk20 achieves the highest reward
and Deducible, at 0 _._ 630 _/_ 0 _._ 544, respectively; idf-only and raw both have a reward of 0 _._ 626, but their
Deducible scores are 0 _._ 538 and 0 _._ 519, respectively; idf-topk60 declines to 0 _._ 595 _/_ 0 _._ 506 . This shows
that the reader ranker cannot rely solely on entity overlap or on expanding the candidate set, but
instead must strike a balance among entity matching, semantic relevance, and contextual compactness.
For the writer, an overly weak ranker makes it difficult for effective graph structure to be read out,
while an overly broad candidate space amplifies the negative impact of noisy writes.


Initial-entity weight is the most stable factor among the three groups of reader-side settings. When
initial-entity weight is enabled, reward reaches 0 _._ 639 and Deducible is 0 _._ 525 ; when it is disabled,
reward drops significantly to 0 _._ 547 and Deducible falls to 0 _._ 505 . Even when the budget is increased
after disabling it, the rewards for off@10 and off@40 recover only to 0 _._ 613 and 0 _._ 615 . This indicates
that the initial entity anchor is crucial in multi-hop graph retrieval: it helps the reader enter the correct
local subgraph from the question entity and expand along the bridging relations written by the writer
to the evidence supporting the answer. Without this anchor, simply increasing the retrieval budget
cannot fully compensate for the deviation in graph traversal direction.


**A.5** **Training Stability and Regularization**


Figure 5 shows the effects of training regularization and rollout settings on the writer. First, the
repetition penalty affects both reward and Deducible, but the trend is not monotonic. Without any
penalty, the result is 0 _._ 585 _/_ 0 _._ 510 ; with a penalty of 0 _._ 10, it improves to 0 _._ 610 _/_ 0 _._ 520 ; with a penalty
of 0 _._ 50, it reaches the best result in this group at 0 _._ 619 _/_ 0 _._ 522 ; after further increasing it to 1 _._ 00,
it drops to 0 _._ 597 _/_ 0 _._ 500 . This indicates that a moderate penalty on repeated triples can suppress
redundant edges and cyclic expressions, but an overly strong penalty may limit the writer’s necessary
restatement of key facts. Especially in multi-hop reasoning, the same bridging entity often needs to
appear in multiple relational paths, so repetition is not always meaningless noise.


Rollout filtering brings consistent but limited gains. When filtering is disabled, reward/Deducible
is 0 _._ 585 _/_ 0 _._ 510 ; after applying `thr_80`, `thr_90`, and `thr_95`, reward increases to 0 _._ 621, 0 _._ 617, and
0 _._ 625, respectively, while Deducible remains stable at 0 _._ 516 – 0 _._ 518 . This suggests that filtering out
low-quality rollouts can reduce the interference of noisy trajectories with policy updates, allowing the
writer to learn effective writing strategies more stably. However, the differences between thresholds
are small, indicating that the main role of filtering is to remove obviously negative samples rather
than determine the final performance ceiling.


17


Rollout group size and warmup ratio further affect training stability. As group size increases from
_n_ = 1 to _n_ = 10, reward/Deducible rises from 0 _._ 610 _/_ 0 _._ 511 to 0 _._ 620 _/_ 0 _._ 531, indicating that a larger
group size can provide more reliable relative preference estimates and help RL distinguish more
accurately between effective and ineffective writing. The optimal warmup ratio appears at 0 _._ 20,
where Deducible reaches 0 _._ 529 ; too little warmup may lead to unstable early policy updates, while too
much warmup may delay the effect of the RL signal. Overall, these regularization and training scale
settings can improve stability, but their gains are smaller than those from reward design, reader-side
initial-entity weight, and the interaction protocol itself. This shows that the core improvement of
the memory writer comes from reader-aware RL feedback: it forces the graph constructor to learn
to preserve bridging entities, cross-document relations, and evidence chains that support answer
derivation, while also reducing repetitive structures and irrelevant local facts.


**B** **Signal-to-Noise Ratio and Retrieval Budget of Structurally Gated**
**Propagation**


This section analyzes the structural capability of the GFM memory reader in SAGE from the perspective of signal propagation and retrieval budget. Unlike graph-isomorphism expressivity analyses
centered on _k_ -WL, we focus on the following question: on noisy graph memories dynamically written
by the memory writer, how do soft addressing, structurally gated propagation, context–schema dualchannel calibration, and entity-to-document projection jointly improve the ratio of query-relevant
evidence signal to distractor noise, thereby reducing the top- _k_ retrieval budget required to achieve a
given level of evidence coverage?


**B.1** **Review of the SAGE-GFM Reader Formalization**


Given a sample _x_ = ( _q, D, D_ [+] _, y_ ), where _q_ denotes the query, _D_ = _{d_ _i_ _}_ _[N]_ _i_ =1 [denotes the candidate]
memory fragments, and _D_ [+] _⊆_ _D_ denotes the gold evidence set supporting the answer _y_, the memory
writer constructs a heterogeneous graph


_G_ = _W_ _θ_ ( _q, D_ ) = ( _V_ _E_ _∪_ _V_ _D_ _, E_ _EE_ _∪_ _E_ _ED_ ) _,_ (5)


where _V_ _E_ is the set of entity nodes, _V_ _D_ is the set of memory-fragment nodes, _E_ _EE_ denotes entity–
entity relation edges, and _E_ _ED_ denotes entity–text-fragment anchoring edges. The GFM memory
reader outputs an entity distribution, a document distribution, and an optional activated subgraph:

_f_ _ϕ_ ( _q, G, D_ ) = � _p_ _ϕ_ ( _e | q, G_ ) _, p_ _ϕ_ ( _d | q, G, D_ ) _, G_ _q_ � _._ (6)


The reader first uses query planning and soft addressing to generate query-conditioned initial activation
for entities. Let _s_ _e_ ( _q_ ) denote the entry score of entity _e_, which integrates multiple cues such as
explicit entities, aliases, pseudo-query similarity, answer type, hard constraints, and entity linking.
The initial activation distribution is then given by


exp( _s_ _e_ ( _q_ ) _/T_ 0 )
_p_ 0 ( _e | q_ ) = (7)
~~�~~ _v∈V_ _E_ [exp(] _[s]_ _[v]_ [(] _[q]_ [)] _[/T]_ [0] [)] _[.]_


The initial entity representation is written as


_η_
_h_ [(0)] _e_ = � _p_ 0 ( _e | q_ )� _W_ _q_ Emb( _q_ ) + _W_ _x_ _x_ _e_ _,_ 0 _≤_ _η ≤_ 1 _._ (8)


The reader then constructs structural gates using node-level structural features, edge-pair structural
features, and graph-level structural summaries. Specifically, let

_φ_ ( _v_ ) = � log(1 + _d_ _v_ ) _, c_ _v_ _, κ_ _v_ _,_ _d_ [¯] _N_ ( _v_ ) � _,_ (9)

_ψ_ ( _u, v_ ) = � _|d_ _u_ _−_ _d_ _v_ _|, |N_ ( _u_ ) _∩N_ ( _v_ ) _|,_ Jaccard( _N_ ( _u_ ) _, N_ ( _v_ ))� _,_ (10)

_r_ _G_ = � mean _v∈V_ _E_ _φ_ ( _v_ ); std _v∈V_ _E_ _φ_ ( _v_ ); dens( _G_ )� _._ (11)


The edge structural context at layer _l_ is

_z_ _uv_ [(] _[l]_ [)] [=] � _E_ _n_ [(] _[l]_ [)] [(] _[φ]_ [(] _[u]_ [));] _[ E]_ _n_ [(] _[l]_ [)] [(] _[φ]_ [(] _[v]_ [));] _[ E]_ _p_ [(] _[l]_ [)] [(] _[ψ]_ [(] _[u, v]_ [));] _[ E]_ _g_ [(] _[l]_ [)] [(] _[r]_ _[G]_ [)] � _,_ (12)


which generates the vector-valued gate

_g_ _uv_ [(] _[l]_ [)] [= 1 +] _[ δ]_ [ tanh] � MLP [(] _g_ _[l]_ [)] [(] _[z]_ _uv_ [(] _[l]_ [)] [)] � _._ (13)


18


Let _η_ _uv_ _≥_ 0 denote the normalized adjacency weight with self-loops. The message and node update

are


_m_ [(] _u_ _[l]_ _→_ [)] _v_ [=] _[ η]_ _[uv]_ _[g]_ _uv_ [(] _[l]_ [)] _[⊙]_ _[W]_ [ (] _m_ _[l]_ [)] _[h]_ [(] _u_ _[l][−]_ [1)] _,_ (14)



� _m_ [(] _u_ _[l]_ _→_ [)] _v_

_u∈N_ ( _v_ )

















_._ (15)




_h_ [(] _v_ _[l]_ [)] = LayerNorm



 _h_ [(] _v_ _[l][−]_ [1)] + PReLU



_b_ [(] _[l]_ [)] +
�
 _u∈N_ (



In addition, the reader combines a contextual calibration channel on the current graph with a crossgraph schema prior channel:
_H_ ( _q, G_ ) = _H_ ctx + _β_ sch _H_ sch _._ (16)


**B.2** **Recoverable Evidence Region and Effective Signal-to-Noise Ratio**


**Definition B.1** (Recoverable Evidence Region) **.** Fix a query _q_ and the current memory graph _G_ . Let
_R_ _q_ _⊆_ _V_ _E_ denote the recoverable evidence region under query _q_, namely the set of entities jointly
determined by the current graph structure, anchoring edges, and reader-reachable paths. This set
contains nodes that support the answer, connect supporting documents, or serve as bridge entities.
If the entity anchor set of document _d_ is denoted by _A_ ( _d_ ) _⊆_ _V_ _E_, then the anchor coverage of the
current graph over the gold evidence is defined as

_ρ_ _A_ = _[|{][d][ ∈]_ _[D]_ [+] [ :] _[ A]_ [(] _[d]_ [)] _[ ∩]_ _[R]_ _[q]_ _[ ̸]_ [=][ ∅] _[}|]_ _._ (17)

_|D_ [+] _|_


**Definition B.2** (Query-Relevant Scalar Activation) **.** Let _r_ _q_ be the direction induced by the query
representation or the final scoring head. The nonnegative query-relevant activation of node _v_ at layer
_l_ is defined as
_a_ [(] _v_ _[l]_ [)] = � _⟨r_ _q_ _, h_ [(] _v_ _[l]_ [)] _[⟩]_ � + _[,]_ (18)

where [ _t_ ] + = max _{t,_ 0 _}_ . The evidence signal mass, noise mass, and effective signal-to-noise ratio at
layer _l_ are respectively defined as


_S_ _l_ = � _a_ [(] _v_ _[l]_ [)] _[,]_ (19)

_v∈R_ _q_

_N_ _l_ = � _a_ [(] _v_ _[l]_ [)] _[,]_ (20)

_v∈V_ _E_ _\R_ _q_

SNR _l_ = _N_ _[S]_ _[l]_ _l_ _,_ (21)


with the convention that SNR _l_ = + _∞_ when _N_ _l_ = 0.

_Remark_ B.3 (Scope of the Scalar-Channel Analysis) _._ Equation (18) does not assume that the full
vector update in Eq. (15) is a nonnegative linear recurrence in every coordinate. LayerNorm, PReLU,
residual connections, and linear transformations may all change representation directions. We
only analyze the query-relevant channel on which the final retrieval score depends, and absorb the
additional effects caused by nonlinearities and directional shifts into a perturbation term. This avoids
an overly strong coordinate-wise monotonicity assumption.


**B.3** **Aggregate Propagation Assumptions and Structural Gating Coefficients**


Idealized analyses often assume that every evidence edge has a uniform lower gate bound _g_ + and
every noisy edge has a uniform upper gate bound _g_ _−_ . However, in graph memories dynamically
constructed by an LLM writer, edges may be missing, erroneous, or repeated; some evidence edges
may be underestimated, while some distractor edges may receive high gates. We therefore adopt an
aggregate propagation assumption.

**Assumption B.4** (Query-Relevant Effective Propagation Operator) **.** Fix a query _q_, the current graph
memory _G_, and the reader representation at layer _l_ . For each layer _l ∈{_ 1 _, . . ., L}_, there exists a
nonnegative matrix _T_ _l_ _∈_ R _[|]_ _≥_ _[V]_ 0 _[E]_ _[|×|][V]_ _[E]_ _[|]_ and a nonnegative perturbation vector _ϵ_ _l_ _∈_ R _[|]_ _≥_ _[V]_ 0 _[E]_ _[|]_ [such that the]
query-relevant activation vector at layer _l_,



_a_ [(] _[l]_ [)] = � _a_ [(] _v_ _[l]_ [)] �


19



_v∈V_ _E_ _[,]_


is controlled by the previous-layer activation _a_ [(] _[l][−]_ [1)] in the following coordinate-wise sense:


_a_ [(] _[l]_ [)] _⪯_ _T_ _l_ _a_ [(] _[l][−]_ [1)] + _ϵ_ _l_ _._ (22)


Here, _⪯_ denotes coordinate-wise inequality. The operator _T_ _l_ denotes the effective propagation
operator induced by the _l_ -th layer on the query-relevant scalar channel. It absorbs the combined
effects of normalized adjacency weights _η_ _uv_, structural gates _g_ _uv_ [(] _[l]_ [)] [, message projection] _[ W]_ [ (] _m_ _[l]_ [)] [, context–]
schema representation composition, and final scoring-channel projection into a single nonnegative
propagation kernel. In other words, _T_ _l_ ( _u, v_ ) is the effective nonnegative contribution strength of the
query-relevant activation of node _v_ at the previous layer to node _u_ at layer _l_ .


The perturbation term _ϵ_ _l_ absorbs residual effects that are difficult to exactly characterize by nonnegative linear propagation, including LayerNorm, PReLU, residual connections, vector-direction
rotation, scoring-channel mismatch, and finite-parameter approximation error.


Furthermore, we only require the propagation process to preserve effective signal in the evidence
region in an aggregate sense. We do not require the structural gate to perfectly distinguish every
evidence edge from every noisy edge. The operator _T_ _l_ may allow some evidence edges to be
underestimated and some distractor edges to be overestimated; the aggregate propagation coefficients
defined below only characterize the overall effect of these local errors on the evidence and noise
regions.


Let

¯
_R_ _q_ = _V_ _E_ _\ R_ _q_ _._

Partition _T_ _l_ according to the node sets _R_ _q_ and _R_ [¯] _q_ :



�



_T_ _l_ =



_T_ [(] _[l]_ [)] _T_ [(] _[l]_ [)]
_RR_ _RR_ [¯]
_T_ [(] ¯ _[l]_ [)] _T_ [(] ¯ _[l]_ [)]
� _RR_ _RR_ [¯]



_._ (23)



Here, _T_ _RR_ [(] _[l]_ [)] [denotes effective propagation within the evidence region,] _[ T]_ [ (] _R_ ¯ _[l]_ _R_ [)][¯] [denotes effective propaga-]

tion within the noise region, _T_ _RR_ [(] ¯ _[l]_ [)] [denotes leakage propagation from the evidence region to the noise]

region, and _T_ _R_ [(] _[l]_ _R_ [)][¯] [denotes propagation from the noise region to the evidence region.]

**Definition B.5** (Aggregate Propagation Coefficients) **.** Given the effective propagation operator _T_ _l_ at
layer _l_ and its block decomposition in Eq. (23), define the three aggregate propagation coefficients
_A_ _l_, _B_ _l_, and _C_ _l_ as follows.


_A_ _l_ is the evidence-retention coefficient. It characterizes the minimum fraction of total mass that
remains inside the evidence region _R_ _q_ after any nonnegative evidence signal _x_ propagates one layer
within _R_ _q_ . Formally, _A_ _l_ is any nonnegative constant satisfying



_A_ _l_ _≤_ inf
_x∈_ R _|≥Rq_ 0 _|_ _[,]_ **[ 1]** _[⊤]_ _[x>]_ [0]



**1** _[⊤]_ _T_ [(] _[l]_ [)]
_RR_ _[x]_
_._ (24)
**1** _[⊤]_ _x_



Equivalently, for any nonnegative evidence signal _x ∈_ R _[|]_ _≥_ _[R]_ 0 _[q]_ _[|]_ [with] **[ 1]** _[⊤]_ _[x >]_ [ 0][,]


**1** _[⊤]_ _T_ [(] _[l]_ [)]
_RR_ _[x][ ≥]_ _[A]_ _[l]_ **[ 1]** _[⊤]_ _[x.]_


_B_ _l_ is the noise self-propagation coefficient. It characterizes the maximum extent to which any
nonnegative noise signal _y_ can be retained or expanded after one layer of propagation inside the noise
region _R_ [¯] _q_ . Formally, _B_ _l_ is any nonnegative constant satisfying



_B_ _l_ _≥_ sup

_y∈_ R _|≥Rq_ [¯] 0 _|_ _[,]_ **[ 1]** _[⊤]_ _[y>]_ [0]



**1** _[⊤]_ _T_ [(] ¯ _[l]_ [)]
_RR_ [¯] _[y]_
_._ (25)
**1** _[⊤]_ _y_



Equivalently, for any nonnegative noise signal _y ∈_ R _[|]_ _≥_ [ ¯] _R_ 0 _q_ _|_ [with] **[ 1]** _[⊤]_ _[y >]_ [ 0][,]


**1** _[⊤]_ _T_ [(] ¯ _[l]_ [)]
_RR_ [¯] _[y][ ≤]_ _[B]_ _[l]_ **[ 1]** _[⊤]_ _[y.]_


20


_C_ _l_ is the evidence-to-noise leakage coefficient. It characterizes the maximum fraction of an arbitrary
nonnegative signal in the evidence region that can leak into the non-evidence region _R_ [¯] _q_ after one
layer of propagation. Formally, _C_ _l_ is any nonnegative constant satisfying



_C_ _l_ _≥_ sup

_x∈_ R _|≥Rq_ 0 _|_ _[,]_ **[ 1]** _[⊤]_ _[x>]_ [0]



**1** _[⊤]_ _T_ [(] ¯ _[l]_ [)]
_RR_ _[x]_
_._ (26)
**1** _[⊤]_ _x_



Equivalently, for any nonnegative evidence signal _x ∈_ R _[|]_ _≥_ _[R]_ 0 _[q]_ _[|]_ [with] **[ 1]** _[⊤]_ _[x >]_ [ 0][,]


**1** _[⊤]_ _T_ [(] ¯ _[l]_ [)]
_RR_ _[x][ ≤]_ _[C]_ _[l]_ **[ 1]** _[⊤]_ _[x.]_


Finally, let
_ξ_ _l_ = **1** _[⊤]_ _ϵ_ _l,_ ¯ _R_ (27)

denote the total perturbation mass injected into the noise region _R_ [¯] _q_ at layer _l_ by nonlinearities,
normalization, representation-direction shifts, and approximation errors. Here, _ϵ_ _l,_ ¯ _R_ [denotes the]
restriction of the perturbation vector _ϵ_ _l_ to _R_ [¯] _q_ .

**Lemma B.6** (Aggregate Propagation Recurrence) **.** _Under Assumption B.4 and Definition B.5, if_
_S_ _l−_ 1 _>_ 0 _and N_ _l−_ 1 _≥_ 0 _, then layer l satisfies_


_S_ _l_ _≥_ _A_ _l_ _S_ _l−_ 1 _,_ (28)

_N_ _l_ _≤_ _B_ _l_ _N_ _l−_ 1 + _C_ _l_ _S_ _l−_ 1 + _ξ_ _l_ _._ (29)


_Proof._ Let _a_ [(] _R_ _[l][−]_ [1)] and _a_ [(] _R_ ¯ _[l][−]_ [1)] be the restrictions of _a_ [(] _[l][−]_ [1)] to _R_ _q_ and _R_ [¯] _q_, respectively. By the definition
of the evidence-retention coefficient in Eq. (24), the total mass retained within the evidence region
through _R_ _q_ _→_ _R_ _q_ propagation is at least


**1** _[⊤]_ _T_ _RR_ [(] _[l]_ [)] _[a]_ [(] _R_ _[l][−]_ [1)] _≥_ _A_ _l_ **1** _[⊤]_ _a_ [(] _R_ _[l][−]_ [1)] = _A_ _l_ _S_ _l−_ 1 _,_ (30)


and thus _S_ _l_ _≥_ _A_ _l_ _S_ _l−_ 1 .


On the other hand, the layer- _l_ mass in the noise region can be upper-bounded by three terms: noise
self-propagation, evidence leakage, and perturbation:


_N_ _l_ _≤_ **1** _[⊤]_ _T_ _R_ [(] ¯ _[l]_ _R_ [)][¯] _[a]_ [(] _R_ ¯ _[l][−]_ [1)] + **1** _[⊤]_ _T_ _RR_ [(] ¯ _[l]_ [)] _[a]_ _R_ [(] _[l][−]_ [1)] + **1** _[⊤]_ _ϵ_ _l,_ ¯ _R_ _[.]_ (31)


Using Eqs. (25), (26), and (27), we obtain


_N_ _l_ _≤_ _B_ _l_ _N_ _l−_ 1 + _C_ _l_ _S_ _l−_ 1 + _ξ_ _l_ _._ (32)


This proves the lemma.


**B.4** **Realistic Aggregate Signal-to-Noise Ratio Bound**


**Theorem B.7** (Realistic Aggregate SNR Bound) **.** _Assume that for all_ _l_ = 1 _, . . ., L_ _, there exist_ _A_ _l_ _>_ 0 _,_
_B_ _l_ _≥_ 0 _, C_ _l_ _≥_ 0 _, and ξ_ _l_ _≥_ 0 _such that the recurrences in Eqs._ (28) _–_ (29) _hold. Let_

_Q_ _l_ = SNR _[−]_ _l_ [1] = _[N]_ _S_ _l_ _[l]_ _._ (33)


_Then_



_L_
�
� _t_ = _i_ +1



�



_Q_ _L_ _≤_



_L_
�
� _l_ =1



_B_ _l_

_A_ _l_



_Q_ 0 +



_L_
�


_i_ =1



_C_ _i_ _ξ_ _i_

+

� _A_ _i_ _A_ _i_ _S_ _i−_ 1



_B_ _t_
_._ (34)
_A_ _t_



_Equivalently, if the right-hand side is finite, then_



_L_
�
� _t_ = _i_ +1



�



� _−_ 1



_L_
�


_i_ =1


21



_C_ _i_ _ξ_ _i_

+

� _A_ _i_ _A_ _i_ _S_ _i−_ 1



_B_ _t_

_A_ _t_



SNR _L_ _≥_



_L_
�
�� _l_ =1



_B_ _l_

_A_ _l_



SNR _[−]_ 0 [1] +



_._ (35)



_The empty product is defined as_ 1 _._


_Proof._ By Lemma B.6, for any _l_,


_S_ _l_ _≥_ _A_ _l_ _S_ _l−_ 1 _,_ _N_ _l_ _≤_ _B_ _l_ _N_ _l−_ 1 + _C_ _l_ _S_ _l−_ 1 + _ξ_ _l_ _._ (36)


Therefore,




_[ξ]_ _[l]_

_[N]_ _[l]_ _≤_ _[B]_ _[l]_ _[N]_ _[l][−]_ [1] [ +] _[ C]_ _[l]_ _[S]_ _[l][−]_ [1] [ +]

_S_ _l_ _A_ _l_ _S_ _l−_ 1



_Q_ _l_ = _[N]_ _[l]_



(37)
_A_ _l_ _S_ _l−_ 1




_[B]_ _[l]_ _Q_ _l−_ 1 + _[C]_ _[l]_

_A_ _l_ _A_ _l_



= _[B]_ _[l]_




_[C]_ _[l]_ + _ξ_ _l_ _._ (38)

_A_ _l_ _A_ _l_ _S_ _l−_ 1



Let
_r_ _l_ = _[B]_ _[l]_




_[C]_ _[l]_ + _ξ_ _l_ _._ (39)

_A_ _l_ _A_ _l_ _S_ _l−_ 1




_[B]_ _A_ _l_ _[l]_ _,_ _d_ _l_ = _A_ _[C]_ _[l]_ _l_



Then
_Q_ _l_ _≤_ _r_ _l_ _Q_ _l−_ 1 + _d_ _l_ _._ (40)
Expanding this first-order nonhomogeneous recurrence yields



_L_
� _r_ _t_ _._ (41)

_t_ = _i_ +1



_Q_ _L_ _≤_



_L_
� _r_ _l_
� _l_ =1 �



_Q_ 0 +



_L_
� _d_ _i_


_i_ =1



Substituting back _r_ _l_ and _d_ _l_ proves Eq. (34). Since SNR _L_ = _Q_ _[−]_ _L_ [1] [, Eq. (35) follows.]


**Corollary B.8** (Layer-Homogeneous Case) **.** _If_ _A_ _l_ = _A >_ 0 _,_ _B_ _l_ = _B ≥_ 0 _,_ _C_ _l_ = _C ≥_ 0 _, and_ _ξ_ _l_ = 0 _,_
_then_



_L−_ 1
�


_i_ =0



_B_
� _A_



_i_ [�] _[−]_ [1]
�



SNR _L_ _≥_



_L_

_B_
�� _A_ � SNR _[−]_ 0 [1] + _[C]_ _A_



_B_


_A_

��



_L_
� SNR _[−]_ 0 [1] + _[C]_ _A_



_._ (42)



_If further C_ = 0 _, then_



_A_ _L_
SNR _L_ _≥_ SNR 0 _._ (43)
� _B_ �



_Proof._ Substituting _A_ _l_ = _A_, _B_ _l_ = _B_, _C_ _l_ = _C_, and _ξ_ _l_ = 0 into Theorem B.7 and simplifying the
resulting geometric series gives the result.


**Corollary B.9** (Ideal Edge-Wise Gating as a Special Case) **.** _Suppose there exist constants_ _g_ + _> g_ _−_ _>_
0 _,_ _α_ + _>_ 0 _,_ _α_ _−_ _>_ 0 _,_ _g_ 0 _≥_ 0 _, and_ _λ_ leak _≥_ 0 _such that the effective retention inside the evidence region_
_is_ _A_ = _g_ + _α_ + _, the self-propagation inside the noise region is_ _B_ = _g_ _−_ _α_ _−_ _, the evidence-to-noise_
_leakage is C_ = _g_ 0 _λ_ leak _, and ξ_ _l_ = 0 _. Then Theorem B.7 reduces to_



_L−_ 1
�


_i_ =0



_g_ _−_ _α_ _−_
� _g_ + _α_ +



_i_ [�] _[−]_ [1]
�



SNR _L_ _≥_



_g_ _−_ _α_ _−_


_g_ + _α_ +

��



_L_
SNR _[−]_ 0 [1] + _[g]_ [0] _[λ]_ [leak]
� _g_ + _α_ +



_._ (44)



_If λ_ leak = 0 _, then_



SNR _L_ _≥_ _g_ + _α_ +
� _g_ _−_ _α_ _−_



_L_

SNR 0 _._ (45)
�



**B.5** **Document Retrieval Budget**


The final retrieval targets of the SAGE-GFM reader are memory fragments or documents. Therefore,
we need to convert the entity-level SNR bound into a document-level top- _k_ budget bound. Let the
final document score be _S_ _D_ ( _d_ ), and let the top- _k_ retrieval result be


_P_ _k_ ( _q, G_ ) = Top- _k_ _d∈D_ _S_ _D_ ( _d_ ) _._ (46)


**Definition B.10** ( _ρ_ -Coverage Retrieval Budget) **.** Given 0 _< ρ ≤_ _ρ_ _A_, let

_m_ _ρ_ = _⌈ρ|D_ [+] _|⌉._ (47)


The minimum top- _k_ budget required to achieve _ρ_ -level gold evidence coverage is defined as

_B_ _ρ_ ( _q, G_ ) = min � _k_ : _|P_ _k_ ( _q, G_ ) _∩_ _D_ [+] _| ≥_ _m_ _ρ_ � _._ (48)

Let _τ_ _ρ_ [+] [denote the] _[ m]_ _[ρ]_ [-th largest score among gold evidence documents, namely the gold score]
threshold required to achieve _ρ_ -coverage.


22


**Lemma B.11** (Quantile Retrieval Budget Bound) **.** _Let the total score mass of distractor documents_
_be_
_M_ _L_ _[−]_ [=] � _S_ _D_ ( _d_ ) _._ (49)

_d∈D\D_ [+]

_If τ_ _ρ_ [+] _[>]_ [ 0] _[, then]_


_L_
_B_ _ρ_ ( _q, G_ ) _≤_ _m_ _ρ_ + _[M]_ _τ_ _ρ_ [+] _[ −]_ _._ (50)


_Proof._ Define the set of distractor documents whose scores are not lower than _τ_ _ρ_ [+] [as]

_N_ _ρ_ = _{d ∈_ _D \ D_ [+] : _S_ _D_ ( _d_ ) _≥_ _τ_ _ρ_ [+] _[}][.]_ (51)

For any _d ∈N_ _ρ_, we have _S_ _D_ ( _d_ ) _≥_ _τ_ _ρ_ [+] [, and hence]

_|N_ _ρ_ _|τ_ _ρ_ [+] _[≤]_ � _S_ _D_ ( _d_ ) _≤_ _M_ _L_ _[−]_ _[.]_ (52)

_d∈N_ _ρ_


Thus _|N_ _ρ_ _| ≤_ _M_ _L_ _[−]_ _[/τ]_ [ +] _ρ_ [. To ensure that the top-] _[k]_ [ results contain at least] _[ m]_ _[ρ]_ [gold evidence documents,]
it suffices to include these _m_ _ρ_ gold documents and all distractors whose scores are not lower than the
threshold _τ_ _ρ_ [+] [. Therefore,]


_L_
_B_ _ρ_ ( _q, G_ ) _≤_ _m_ _ρ_ + _|N_ _ρ_ _| ≤_ _m_ _ρ_ + _[M]_ _τ_ _ρ_ [+] _[ −]_ _._ (53)

This proves the lemma.


To use entity-level SNR for document-level retrieval, we need to control the noise expansion introduced by entity-to-document projection.

**Assumption B.12** (Projection Noise and Gold Score Concentration) **.** There exist constants _K_ _A_ _≥_ 0,
_ζ_ _A_ _≥_ 0, and _c_ _ρ_ _∈_ (0 _,_ 1] such that the final document scores satisfy


_M_ _L_ _[−]_ _[≤]_ _[K]_ _[A]_ _[N]_ _[L]_ [ +] _[ ζ]_ _[A]_ _[,]_ (54)

_τ_ _ρ_ [+] _[≥]_ _m_ _[c]_ _[ρ]_ _ρ_ _S_ _L_ _._ (55)


Here, _K_ _A_ is the noise expansion factor of entity-to-document projection, _ζ_ _A_ denotes the projection
residual caused by incorrect anchors, missing anchors, or additional text-similarity terms, and _c_ _ρ_
measures whether the evidence signal is effectively distributed over at least _m_ _ρ_ gold documents.
**Theorem B.13** (Realistic Signal–Noise–Budget Bound) **.** _Under the conditions of Theorem B.7,_
_further assume that Assumption B.12 holds. Then_




_[K]_ _[A]_

SNR _[−]_ _L_ [1] [+] _[m]_ _[ρ]_ _[ζ]_ _[A]_
_c_ _ρ_ _c_ _ρ_ _S_ _L_



_B_ _ρ_ ( _q, G_ ) _≤_ _m_ _ρ_ + _[m]_ _[ρ]_ _[K]_ _[A]_



_._ (56)
_c_ _ρ_ _S_ _L_



_Substituting Theorem B.7 further yields the explicit upper bound_



_B_ _l_

_A_ _l_

�



_B_ _ρ_ ( _q, G_ ) _≤_ _m_ _ρ_ + _[m]_ _[ρ]_ _[K]_ _[A]_

_c_ _ρ_



_L_
�
� � _l_ =1



SNR _[−]_ 0 [1]



(57)



_L_
�
� _t_ = _i_ +1



_L_
�
�



�



+ _[m]_ _[ρ]_ _[ζ]_ _[A]_ _._

_c_ _ρ_ _S_ _L_



+



_L_
�


_i_ =1



_C_ _i_ _ξ_ _i_

+

� _A_ _i_ _A_ _i_ _S_ _i−_ 1



_C_ _i_
� _A_ _i_



_B_ _t_

_A_ _t_



_Proof._ By Lemma B.11,


By Assumption B.12,



_L_
_B_ _ρ_ ( _q, G_ ) _≤_ _m_ _ρ_ + _[M]_ _τ_ _ρ_ [+] _[ −]_ _._ (58)



_M_ _L_ _[−]_ _≤_ _[K]_ _[A]_ _[N]_ _[L]_ [ +] _[ζ]_ _[A]_
_τ_ _ρ_ [+] ( _c_ _ρ_ _/m_ _ρ_ ) _S_ _L_




_[A]_ _[N]_ _[L]_ [ +] _[ζ]_ _[A]_

= _[m]_ _[ρ]_ _[K]_ _[A]_
( _c_ _ρ_ _/m_ _ρ_ ) _S_ _L_ _c_ _ρ_



_N_ _L_



_N_ _L_ + _[m]_ _[ρ]_ _[ζ]_ _[A]_

_S_ _L_ _c_ _S_ _L_



_._ (59)
_c_ _ρ_ _S_ _L_



_c_ _ρ_



Since _N_ _L_ _/S_ _L_ = SNR _[−]_ _L_ [1] [, Eq. (56) follows. Substituting the upper bound on] [ SNR] _[−]_ _L_ [1] from Theorem B.7 into Eq. (56) gives Eq. (57).


23


**Corollary B.14** (Full Evidence Recovery Budget) **.** _If_ _ρ_ = 1 _and_ _ρ_ _A_ = 1 _, then_ _m_ _ρ_ = _|D_ [+] _|_ _, and_
_B_ _ρ_ ( _q, G_ ) _reduces to the full evidence recovery budget. In this case, Theorem B.13 provides an upper_
_bound on the top-k budget required to recover all gold evidence._


**B.6** **Interpretation of the Theoretical Bound for the SAGE Design**


Theorem B.7 and Theorem B.13 unify four reader design factors under the same retrieval-budget
upper bound. To avoid relying only on intuitive discussion, we provide several direct monotonicity
propositions.
_Proposition_ 2 (Monotonicity of the Budget Bound) _._ Fix _m_ _ρ_, _K_ _A_, _c_ _ρ_, _ζ_ _A_, _S_ _L_, and SNR 0, and define



_B_ _l_

_A_ _l_

�



_L_
�
� _t_ = _i_ +1



_L_
�


_i_ =1



_C_ _i_ _ξ_ _i_

+

� _A_ _i_ _A_ _i_ _S_ _i−_ 1



_B_ _t_
_._ (60)
_A_ _t_



Γ _L_ =



_L_
�
� _l_ =1



SNR _[−]_ 0 [1] +



Then the budget upper bound




_[K]_ _[A]_

Γ _L_ + _[m]_ _[ρ]_ _[ζ]_ _[A]_
_c_ _ρ_ _c_ _ρ_ _S_ _L_



_U_ _ρ_ = _m_ _ρ_ + _[m]_ _[ρ]_ _[K]_ _[A]_



(61)
_c_ _ρ_ _S_ _L_



is monotonically nondecreasing in Γ _L_, _K_ _A_, and _ζ_ _A_, and monotonically nonincreasing in _c_ _ρ_ and _S_ _L_ .
If all other terms in the products are fixed, decreasing any of _B_ _l_ _/A_ _l_, _C_ _l_ _/A_ _l_, or _ξ_ _l_ _/_ ( _A_ _l_ _S_ _l−_ 1 ) cannot
increase _U_ _ρ_ .


_Proof._ The partial derivatives of _U_ _ρ_ with respect to Γ _L_, _K_ _A_, and _ζ_ _A_ are nonnegative, while the
partial derivatives with respect to _c_ _ρ_ and _S_ _L_ are nonpositive. Moreover, Γ _L_ is a nonnegative linear
or multiplicative combination of _B_ _l_ _/A_ _l_, _C_ _l_ _/A_ _l_, and _ξ_ _l_ _/_ ( _A_ _l_ _S_ _l−_ 1 ) . When the other terms are fixed,
decreasing any such nonnegative term cannot increase Γ _L_ . The proposition follows.


_Proposition_ 3 (Effect of Soft Addressing) _._ If soft addressing increases the initial evidence signal _S_ 0
and decreases the initial noise mass _N_ 0, thereby increasing SNR 0, then, with all other coefficients
fixed, the budget upper bound in Theorem B.13 does not increase. In particular, explicit entities,
aliases, pseudo-queries, type constraints, hard constraints, and entity-linking signals in query planning
improve the final budget bound whenever they increase _S_ 0 _/N_ 0 in an aggregate sense.
_Proposition_ 4 (Aggregate Advantage of Structural Gating) _._ Compared with a reader without structural
gating, suppose the structurally gated reader satisfies


_B_ _l_ [gate] _l_ _C_ _l_ [gate] _l_ _ξ_ _l_ [gate] _ξ_ _l_ [plain]
_A_ [gate] _l_ _≤_ _[B]_ _A_ [plain] _l_ [plain] _,_ _A_ [gate] _l_ _≤_ _[C]_ _A_ [plain] _l_ [plain] _,_ _A_ [gate] _l_ _S_ _l_ [gate] _−_ 1 _≤_ _A_ [plain] _l_ _S_ _l_ [plain] _−_ 1 _._ (62)


Then the budget upper bound of the structurally gated reader is no larger than that of the ungated
reader.

_Proposition_ 5 (Stability Interpretation of the Context–Schema Dual Channel) _._ Let _δ_ _l_ denote the
failure probability of the aggregate recurrences in Eqs. (28)–(29) at layer _l_ . If the schema prior
channel reduces the variance of cross-graph structural-role estimation and the context calibration
channel reduces the current-graph adaptation error, so that _δ_ _l_ decreases to _δ_ _l_ _[′]_ [with] _[ δ]_ _l_ _[′]_ _[≤]_ _[δ]_ _[l]_ [, then the]
probability lower bound under which Theorem B.7 and Theorem B.13 simultaneously hold improves
from 1 _−_ [�] _[L]_ _l_ =1 _[δ]_ _[l]_ [ to][ 1] _[ −]_ [�] _[L]_ _l_ =1 _[δ]_ _l_ _[′]_ [.]


The core quantities derived above are



�



_L_
�
� _t_ = _i_ +1



_L_
�


_i_ =1



_C_ _i_ _ξ_ _i_

+

� _A_ _i_ _A_ _i_ _S_ _i−_ 1



_BA_ _tt_ _,_ (63)



SNR _[−]_ _L_ [1] _≤_



_L_
� _BA_ _ll_
� _l_ =1



SNR _[−]_ 0 [1] +



and
_B_ _ρ_ ( _q, G_ ) _≤_ _m_ _ρ_ + _[m]_ _[ρ]_ _[K]_ _[A]_



_._ (64)
_c_ _ρ_ _S_ _L_




_[ρ]_ _[K]_ _[A]_

SNR _[−]_ _L_ [1] [+] _[m]_ _[ρ]_ _[ζ]_ _[A]_
_c_ _ρ_ _c_ _ρ_ _S_ _L_



Equation (63) shows that soft addressing reduces the amount of noise that subsequent propagation
must overcome by improving the initial SNR 0 ; structural gating improves aggregate evidence
retention and noise suppression by increasing _A_ _l_ and decreasing _B_ _l_ and _C_ _l_ ; the context–schema dual


24


channel makes these aggregate inequalities more stable on dynamic graph memories by reducing
cross-graph structural-role estimation error; and entity-to-document projection converts entity-level
SNR into document-level budget efficiency by decreasing _K_ _A_ and _ζ_ _A_ and increasing _c_ _ρ_ . Equation (64)
further shows that the advantage of SAGE-GFM does not rely on perfect edge-wise classification or
zero-leakage assumptions. As long as evidence-retention dominance is achieved in an aggregate or
high-probability sense, i.e., _B_ _l_ _/A_ _l_ and _C_ _l_ _/A_ _l_ are sufficiently small, the reader can improve queryrelevant SNR and reduce the top- _k_ retrieval budget required to achieve a given level of evidence

coverage.


**C** **Target Graph Calibration and Cross-graph Structural Priors**


**C.1** **Structural Role Decomposition Assumption**


**Definition C.1** (Structural role mapping) **.** Given a graph _G_, a mapping


_ρ_ _G_ : _V_ ( _G_ ) _→R_ (65)


is called a structural role mapping, where _R_ is the structural role space. _ρ_ _G_ ( _v_ ) can be jointly determined by _φ_ _G_ ( _v_ ), the structural statistics of edges incident to _v_, local community-boundary statistics,
and other graph-structure summaries. Typical structural roles include hub, bridge, community core,
boundary node, and noisy shortcut.

**Definition C.2** (Target graph reading risk) **.** Fix a target graph _G_ . Let _D_ _G_ be the query–node sampling
distribution on the target graph, and let _f_ _G_ _[⋆]_ [(] _[q, v]_ [)] [ be the ideal evidence relevance function. For any]
measurable function _f_, define the squared risk as

_R_ _G_ ( _f_ ) = E ( _q,v_ ) _∼D_ _G_ �( _f_ ( _q, v, G_ ) _−_ _f_ _G_ _[⋆]_ [(] _[q, v]_ [))] [2] [�] _._ (66)


**Assumption C.3** (Context–schema decomposability) **.** For every target graph _G_, the ideal reading
function can be decomposed as


_f_ _G_ _[⋆]_ [(] _[q, v]_ [) =] _[ f]_ sch _[ ⋆]_ [(] _[q, ρ]_ _[G]_ [(] _[v]_ [)) +] _[ f]_ ctx _[ ⋆]_ _,G_ [(] _[q, v]_ [)] _[,]_ (67)


where _f_ sch _[⋆]_ [denotes the cross-graph shared structural reading rule, and] _[ f]_ ctx _[ ⋆]_ _,G_ [denotes the target-graph]
residual induced by the current writer, current domain, current entity naming, local noise, and writing
style.


Equation (67) corresponds exactly to the structural design of SAGE: _H_ sch is used to approximate
_f_ sch _[⋆]_ [, and] _[ H]_ [ctx] [ is used to approximate] _[ f]_ ctx _[ ⋆]_ _,G_ [. The next subsection gives the risk meaning of this]
decomposition.


**C.2** **Approximation Risk of Context–schema Decomposition**


**Theorem C.4** (Context–schema decomposition reduces target-graph approximation risk) **.** _Suppose_
_Assumption 2.3 holds. Let_ _H_ sch _be the schema function class, let_ _H_ ctx _,G_ _be the target-graph context_
_function class, and define the sum class_


_H_ sch + _H_ ctx _,G_ = _{f_ _s_ + _f_ _c_ : _f_ _s_ _∈H_ sch _, f_ _c_ _∈H_ ctx _,G_ _}._ (68)


_If there exist ϵ_ sch _, ϵ_ ctx _≥_ 0 _such that_

inf �( _f_ _s_ ( _q, ρ_ _G_ ( _v_ )) _−_ _f_ sch _[⋆]_ [(] _[q, ρ]_ _[G]_ [(] _[v]_ [)))] [2] [�] _≤_ _ϵ_ sch _,_ (69)
_f_ _s_ _∈H_ sch [E]


inf �( _f_ _c_ ( _q, v, G_ ) _−_ _f_ ctx _[⋆]_ _,G_ [(] _[q, v]_ [))] [2] [�] _≤_ _ϵ_ ctx _,_ (70)
_f_ _c_ _∈H_ ctx _,G_ [E]


_where both expectations are over_ ( _q, v_ ) _∼D_ _G_ _, then_


inf (71)
_f_ _∈H_ sch + _H_ ctx _,G_ _[R]_ _[G]_ [(] _[f]_ [)] _[ ≤]_ [2] _[ϵ]_ [sch] [ + 2] _[ϵ]_ [ctx] _[.]_


_Proof.f_ ˆ _c_ _∈H_ Take any ctx _,G_ such that _α >_ 0 . By the two approximation error conditions, there exist _f_ [ˆ] _s_ _∈H_ sch and

E[( _f_ [ˆ] _s_ _−_ _f_ sch _[⋆]_ [)] [2] []] _[ ≤]_ _[ϵ]_ [sch] [+] _[ α,]_ E[( _f_ [ˆ] _c_ _−_ _f_ ctx _[⋆]_ _,G_ [)] [2] []] _[ ≤]_ _[ϵ]_ [ctx] [+] _[ α.]_ (72)


25


Let _f_ [ˆ] = _f_ [ˆ] _s_ + _f_ [ˆ] _c_ . By the decomposition in Eq. (67), we have


ˆ
_f −_ _f_ _G_ _[⋆]_ [= ( ˆ] _[f]_ _[s]_ _[−]_ _[f]_ sch _[ ⋆]_ [) + ( ˆ] _[f]_ _[c]_ _[−]_ _[f]_ ctx _[ ⋆]_ _,G_ [)] _[.]_ (73)


Using ( _a_ + _b_ ) [2] _≤_ 2 _a_ [2] + 2 _b_ [2], we obtain


_R_ _G_ ( _f_ [ˆ] ) = E[( _f_ [ˆ] _−_ _f_ _G_ _[⋆]_ [)] [2] []]

_≤_ 2E[( _f_ [ˆ] _s_ _−_ _f_ sch _[⋆]_ [)] [2] [] + 2][E][[( ˆ] _[f]_ _[c]_ _[−]_ _[f]_ ctx _[ ⋆]_ _,G_ [)] [2] []]


_≤_ 2 _ϵ_ sch + 2 _ϵ_ ctx + 4 _α._ (74)


Since _α >_ 0 is arbitrary, taking the infimum yields the conclusion.


_Proposition_ 6 (Residual bias of schema-only models) _._ Further assume that _L_ 2 ( _D_ _G_ ) is a Hilbert space,
_H_ sch is a closed linear subspace of it, and _f_ sch _[⋆]_ _[∈H]_ [sch] [. If only a schema-only model] _[ f]_ _[s]_ _[ ∈H]_ [sch] [ is]
used, then
_f_ _s_ _∈H_ inf sch _[R]_ _[G]_ [(] _[f]_ _[s]_ [) = dist] _L_ [2] 2 ( _D_ _G_ ) [(] _[f]_ ctx _[ ⋆]_ _,G_ _[,][ H]_ [sch] [)] _[.]_ (75)


Therefore, as long as the target-graph residual _f_ ctx _[⋆]_ _,G_ [does not belong to] _[ H]_ [sch] [, a schema-only reader]
has an irreducible target-graph bias.


_Proof._ By _f_ sch _[⋆]_ _[∈H]_ [sch] [ and the linearity of] _[ H]_ [sch] [, any] _[ f]_ _[s]_ _[ ∈H]_ [sch] [ can be written as] _[ f]_ _[s]_ [ =] _[ f]_ sch _[ ⋆]_ [+] _[ g]_ [,]
where _g ∈H_ sch . Thus,


2
_R_ _G_ ( _f_ _s_ ) = �� _f_ _s_ _−_ _f_ sch _⋆_ _[−]_ _[f]_ ctx _[ ⋆]_ _,G_ �� _L_ 2 ( _D_ _G_ )


2
= �� _g −_ _f_ ctx _⋆_ _,G_ �� _L_ 2 ( _D_ _G_ ) _[.]_ (76)


Taking the infimum over _f_ _s_ _∈H_ sch is equivalent to taking the infimum over _g ∈H_ sch, and Eq. (75)
follows from the definition of distance.


_Remark_ C.5 _._ Proposition 2.5 shows that the cross-graph schema prior can only characterize crossgraph shared structural rules and cannot replace target graph calibration. In contrast, the role of the
target graph calibration channel _H_ ctx is to absorb _f_ ctx _[⋆]_ _,G_ [, namely the local noise, entity granularity,]
relation style, and domain residual of the graph generated by the current writer.


**C.3** **Sample Complexity Advantage of Schema Prior**


**Lemma C.6** (Uniform convergence for bounded loss classes) **.** _Let_ _F_ _be a function class, and let the_
_loss_ _ℓ_ _f_ ( _z_ ) _∈_ [0 _,_ 1] _. Given_ _n_ _independent samples_ _S_ = _{z_ _i_ _}_ _[n]_ _i_ =1 _[, define the true risk]_ _[ R]_ [(] _[f]_ [) =][ E][[] _[ℓ]_ _[f]_ [(] _[z]_ [)]]
_and the empirical risk_ _R_ [�] _S_ ( _f_ ) = _n_ _[−]_ [1] [ �] _[n]_ _i_ =1 _[ℓ]_ _[f]_ [(] _[z]_ _[i]_ [)] _[. Then, with probability at least]_ [ 1] _[ −]_ _[δ]_ _[, for all]_
_f ∈F simultaneously,_



_R_ ( _f_ ) _≤_ _R_ [�] _S_ ( _f_ ) + 2 Rad _n_ ( _ℓ_ _◦F_ ) + 3

�



log(2 _/δ_ )

2 _n_ _,_ (77)



_where_ Rad _n_ ( _ℓ_ _◦F_ ) _is an upper bound on the empirical Rademacher complexity of the loss-composed_
_class._


_Proof._ This is a direct result of the standard symmetrization and McDiarmid/Hoeffding concentration
inequalities for bounded loss function classes. Specifically, let



_Z_ ( _S_ ) = sup
_f_ _∈F_



�
_R_ ( _f_ ) _−_ _R_ _S_ ( _f_ ) _._ (78)
��� ���



By symmetrization, E _Z_ ( _S_ ) _≤_ 2 Rad _n_ ( _ℓ_ _◦F_ ) . Moreover, since changing one sample can change
_Z_ ( _S_ ) by at most 1 _/n_, McDiarmid’s inequality gives



_Z_ ( _S_ ) _≤_ E _Z_ ( _S_ ) + 3

~~�~~



log(2 _/δ_ )

(79)
2 _n_



with probability at least 1 _−_ _δ_ . Combining the two inequalities gives the conclusion.


26


**Theorem C.7** (Schema prior reduces the sample complexity of target-graph adaptation) **.** _Fix a target_
_graph_ _G_ _, and suppose the number of supervised samples available for reader calibration on the_
_target graph is_ _n_ _G_ _. Let_ _H_ full _be the full reader class that needs to be learned on the target graph_
_when no schema prior is used; let_ _H_ res _be the residual class that only needs to be learned given a_
_schema prior_ _f_ _s_ _, with the combined model_ _f_ = _f_ _s_ + _f_ _r_ _,_ _f_ _r_ _∈H_ res _. Let_ _f_ [ˆ] full _and_ _f_ [ˆ] res _be the empirical_
_risk minimizers over the two classes, respectively. Then, with probability at least_ 1 _−_ _δ,_



_R_ _G_ ( _f_ [ˆ] full ) _≤_ inf
_f_ _∈H_ full _[R]_ _[G]_ [(] _[f]_ [) + 4 Rad] _[n]_ _[G]_ [(] _[ℓ]_ _[◦H]_ [full] [) + 6]



�



log(4 _/δ_ )

2 _n_ _G_ _,_ (80)



_R_ _G_ ( _f_ _s_ + _f_ [ˆ] res ) _≤_ inf
_f_ _r_ _∈H_ res _[R]_ _[G]_ [(] _[f]_ _[s]_ [ +] _[ f]_ _[r]_ [) + 4 Rad] _[n]_ _[G]_ [(] _[ℓ]_ _[◦]_ [(] _[f]_ _[s]_ [ +] _[ H]_ [res] [)) + 6]

�


_If the complexities satisfy_



log(4 _/δ_ )

_._ (81)
2 _n_ _G_



_d_ full


_n_ _G_

�



�



Rad _n_ _G_ ( _ℓ_ _◦H_ full ) = _O_ [�]



��



_,_ Rad _n_ _G_ ( _ℓ_ _◦_ ( _f_ _s_ + _H_ res )) = _O_ [�]



� ~~�~~



_d_ res


_n_ _G_



_,_ (82)



_and_ _d_ res _≪_ _d_ full _, then the schema prior reduces target-graph learning from estimating the full_
_reading function to estimating the residual, and lowers the estimation error term for target-graph_
_adaptation._


_Proof._ For any function class _F_, let _f_ [ˆ] be the empirical risk minimizer and let _f_ _[◦]_ _∈_ arg inf _f_ _∈F_ _R_ ( _f_ )
be the true risk minimizer. By empirical optimality, _R_ [�] ( _f_ [ˆ] ) _≤_ _R_ [�] ( _f_ _[◦]_ ), so


_R_ ( _f_ [ˆ] ) _−_ _R_ ( _f_ _[◦]_ ) = _R_ ( _f_ [ˆ] ) _−_ _R_ [�] ( _f_ [ˆ] ) + _R_ [�] ( _f_ [ˆ] ) _−_ _R_ [�] ( _f_ _[◦]_ ) + _R_ [�] ( _f_ _[◦]_ ) _−_ _R_ ( _f_ _[◦]_ )



_≤_ 2 sup
_f_ _∈F_



�
_R_ ( _f_ ) _−_ _R_ ( _f_ ) _._ (83)
��� ���



Applying Lemma 2.7 to _F_ = _H_ full and _F_ = _f_ _s_ + _H_ res, respectively, and combining the two
probability events by a union bound, gives Eq. (80) and Eq. (81). The complexity-order conclusion
follows by substituting the corresponding Rademacher upper bounds.


_Remark_ C.8 _._ Theorem 2.8 gives the key theoretical motivation for the schema prior: in self-evolving
memory, each new graph generated by the writer usually provides only limited supervised signal.
If the reader relearns the full reading function from the target graph in every round, high-variance
estimation arises; the schema prior fixes or strongly regularizes the cross-graph shared structural rules,
so that target-graph calibration only needs to learn the residual, thereby reducing sample complexity.


**D** **Writer-induced Graph Distribution Shift and Target Graph Calibration**


**D.1** **Writer-induced Dynamic Graph Distribution**


The writer parameter _θ_ induces a graph distribution _P_ _θ_ ( _G | q, D_ ) on the sample ( _q, D_ ) . For notational
simplicity, denote the joint distribution of ( _q, D, D_ [+] _, y, G_ ) by Π _θ_ . Given the reader parameter _ϕ_,
define the reader risk as

_L_ _R_ ( _ϕ_ ; _θ_ ) = E ( _q,D,D_ + _,y,G_ ) _∼_ Π _θ_ � _ℓ_ _R_ ( _R_ _ϕ_ ( _q, G, D_ ) _, D_ [+] _, y_ )� _._ (84)


Here, _ℓ_ _R_ can be supporting-entity BCE, multi-positive ranking loss, document recall loss, or a
combination thereof.

_Proposition_ 7 (Writer updates cause reader distribution shift) _._ Assume 0 _≤_ _ℓ_ _R_ _≤_ 1 . For any fixed _ϕ_
and any writer parameters _θ, θ_ _[′]_, we have


_|L_ _R_ ( _ϕ_ ; _θ_ _[′]_ ) _−L_ _R_ ( _ϕ_ ; _θ_ ) _| ≤_ TV(Π _θ_ _[′]_ _,_ Π _θ_ ) _,_ (85)


where TV is the total variation distance. If, further, _ℓ_ _R_ ( _R_ _ϕ_ ( _q, G, D_ ) _, D_ [+] _, y_ ) is _L_ _ℓ_ -Lipschitz with
respect to the graph variable under some graph metric _d_ _G_, then


_|L_ _R_ ( _ϕ_ ; _θ_ _[′]_ ) _−L_ _R_ ( _ϕ_ ; _θ_ ) _| ≤_ _L_ _ℓ_ _W_ 1 (Π _θ_ _′_ _,_ Π _θ_ ) _,_ (86)


where _W_ 1 is the first-order Wasserstein distance induced by _d_ _G_ .


27


_Proof._ For the bounded loss case, let _h_ _ϕ_ ( _q, D, D_ [+] _, y, G_ ) = _ℓ_ _R_ ( _R_ _ϕ_ ( _q, G, D_ ) _, D_ [+] _, y_ ) _∈_ [0 _,_ 1] . Then



_|L_ _R_ ( _ϕ_ ; _θ_ _[′]_ ) _−L_ _R_ ( _ϕ_ ; _θ_ ) _|_ =
����



_h_ _ϕ_ _d_ Π _θ_ _′_ _−_ _h_ _ϕ_ _d_ Π _θ_
� �



_≤_ TV(Π _θ_ _′_ _,_ Π _θ_ ) _,_ (87)
����



where the last step follows from the dual definition of total variation. If _h_ _ϕ_ is _L_ _ℓ_ -Lipschitz, the
Wasserstein upper bound follows from the Kantorovich–Rubinstein duality.


**Corollary D.1** (Necessity of target graph calibration) **.** _If updating the writer from_ _θ_ _to_ _θ_ _[′]_ _causes_
TV(Π _θ_ _′_ _,_ Π _θ_ ) _to be non-negligible, then the risk of a fixed reader_ _ϕ_ _on the new graph distribution_
_may increase. Therefore, target graph calibration of the reader, namely_ _ϕ �→_ _ϕ_ _[′]_ _to reduce_ _L_ _R_ ( _ϕ_ _[′]_ ; _θ_ _[′]_ ) _,_
_is a necessary mechanism for handling writer-induced graph distribution shift._


_Proof._ By Proposition 3.1, writer distribution shift can directly change the new-distribution risk of
the fixed reader. If the reader is not updated, there is no optimization mechanism to offset this drift
term. Target graph calibration is precisely re-optimization of _L_ _R_ ( _·_ ; _θ_ _[′]_ ), and is therefore a natural step
for reducing the risk on the new graph.


**E** **Reader Stability under Dynamic Graph Evolution**


**E.1** **Realistic Graph Evolution Distance**


Real graphs often contain hubs, node additions and deletions, alias merges, anchor rewrites, and
structural statistics that are not globally Lipschitz. Therefore, we use the augmented graph drift
actually perceived by the reader to measure graph evolution.

**Definition E.1** (Padding alignment and presence bit) **.** Given two consecutive-round graphs _G_ and
_G_ _[′]_, align them through persistent memory ids to a common node universe _V_ [¯] = _V_ ( _G_ ) _∪_ _V_ ( _G_ _[′]_ ) . If
a node exists only in one graph, it is treated as an isolated padding node in the other graph, and a
presence bit is added to its features. The aligned node feature matrices are still denoted by _X, X_ _[′]_ .

**Definition E.2** (Augmented graph drift) **.** Let _A, A_ _[′]_ be self-looped row-normalized adjacency matrices,
let _S_ _q_ _, S_ _q_ _[′]_ [be the entry score vectors before soft addressing, and let] _[ B, B]_ _[′]_ [ be row-normalized entity-]
to-document anchoring matrices. Define



∆ _X_ = _∥X −_ _X_ _[′]_ _∥_ 2 _,∞_ _,_ ∆ _A_ = _∥A −_ _A_ _[′]_ _∥_ _∞_ _,_ ∆ seed = �� _S_ _q_ _−_ _S_ _q′_ �� _∞_ _[,]_ ∆ _B_ = _∥B −_ _B_ _[′]_ _∥_ _∞_ _,_
(88)
where
_∥H∥_ 2 _,∞_ = max _v∈V_ [¯] _[∥][h]_ _[v]_ _[∥]_ [2] _[,]_ _∥A∥_ _∞_ = max _v_ � _|A_ _vu_ _| ._ (89)



�



_|A_ _vu_ _| ._ (89)

_u_



For the gate input _z_ _uv_ [(] _[l]_ [)] [at layer] _[ l]_ [, define the weighted structural drift as]



∆ [(] _Z_ _[l]_ [)] [= max]
_v_



� _A_ _[′]_ _vu_ ��� _z_ _uv_ ( _l_ ) _[−]_ _[z]_ _uv_ _[′]_ [(] _[l]_ [)] ��� 2 _[,]_ ∆ _Z_ = max 1 _≤l≤L_ [∆] _Z_ [(] _[l]_ [)] _[.]_ (90)

_u_



The total augmented graph drift is defined as


∆ aug ( _G, G_ _[′]_ ; _q_ ) = ∆ _X_ + ∆ _A_ + ∆ seed + ∆ _Z_ + ∆ _B_ _._ (91)


**E.2** **Stability Assumptions**


**Assumption E.3** (Normalized adjacency) **.** For all considered graphs, _A_ _vu_ _≥_ 0 and

� _A_ _vu_ = 1 _,_ _∀v ∈_ _V ._ [¯] (92)


_u_


Therefore, _∥A∥_ _∞_ = 1 . This assumption allows high-degree hubs to exist, but prevents single-layer
propagation from being unboundedly amplified by node degree.

**Assumption E.4** (Trajectory-local boundedness) **.** For graph pairs _G, G_ _[′]_ on the training and inference
trajectories, there exist constants _B_ _l_ such that

_H_ ( _l_ ) ( _q, G_ ) _H_ ( _l_ ) ( _q, G_ _′_ ) _l_ = 0 _, . . ., L._ (93)
��� ��� 2 _,∞_ _[≤]_ _[B]_ _[l]_ _[,]_ ��� ��� 2 _,∞_ _[≤]_ _[B]_ _[l]_ _[,]_


28


**Assumption E.5** (Locally Lipschitz modules) **.** In a neighborhood of the training trajectory, the _l_ -th
layer satisfies
_W_ ( _ml_ ) (94)
��� ��� 2 _[≤]_ _[M]_ _[l]_ _[,]_
���MLP ( _gl_ ) [(] _[z]_ [)] _[ −]_ [MLP] [(] _g_ _[l]_ [)] [(] _[z]_ _[′]_ [)] ��� _∞_ _[≤]_ _[L]_ _[g,l]_ _[ ∥][z][ −]_ _[z]_ _[′]_ _[∥]_ [2] _[ .]_ (95)


The Lipschitz constant of PReLU is _L_ _σ_, and the Lipschitz constant of LayerNorm with a numerical
stabilizer in this trajectory neighborhood is _L_ LN _,l_ .


**Assumption E.6** (Local Lipschitzness of score head and projection) **.** The entity score head satisfies


_∥s_ _E_ ( _q, G_ ) _−_ _s_ _E_ ( _q, G_ _[′]_ ) _∥_ _∞_ _≤_ _L_ _E_ _∥H_ ( _q, G_ ) _−_ _H_ ( _q, G_ _[′]_ ) _∥_ 2 _,∞_ _._ (96)


Meanwhile, _∥s_ _E_ ( _q, G_ ) _∥_ _∞_ _≤_ _S_ _E_, and _B_ is row-normalized, so _∥B∥_ _∞_ _≤_ 1.


**E.3** **Stability of Soft Addressing and Initial Representation**


**Lemma E.7** (Softmax and pre-activation stability) **.** _Let_


_p_ = softmax( _S/T_ 0 ) _,_ _p_ _[′]_ = softmax( _S_ _[′]_ _/T_ 0 ) _._ (97)


_Then_
_∥p −_ _p_ _[′]_ _∥_ _∞_ _≤_ _T_ [1] 0 _∥S −_ _S_ _[′]_ _∥_ _∞_ _._ (98)

_Furthermore, let a_ _v_ = ( _p_ _v_ + _ϵ_ _p_ ) _[η]_ _and a_ _[′]_ _v_ [= (] _[p]_ _[′]_ _v_ [+] _[ ϵ]_ _[p]_ [)] _[η]_ _[, where]_ [ 0] _[ < η][ ≤]_ [1] _[. Then]_


_p_
_∥a −_ _a_ _[′]_ _∥_ _∞_ _≤_ _[ηϵ]_ _T_ _[η]_ 0 _[−]_ [1] _∥S −_ _S_ _[′]_ _∥_ _∞_ _._ (99)


_Proof._ The Jacobian of softmax is _J_ ( _z_ ) = diag( _p_ ) _−_ _pp_ _[⊤]_ . For any row _i_,

� _|J_ _ij_ ( _z_ ) _|_ = 2 _p_ _i_ (1 _−_ _p_ _i_ ) _≤_ 1 _._ (100)

_j_


Thus, _∥J_ ( _z_ ) _∥_ _∞→∞_ _≤_ 1. By the mean value theorem and setting _z_ = _S/T_ 0, we obtain

_∥p −_ _p_ _[′]_ _∥_ _∞_ _≤_ _T_ [1] 0 _∥S −_ _S_ _[′]_ _∥_ _∞_ _._ (101)


The function _t �→_ ( _t_ + _ϵ_ _p_ ) _[η]_ is Lipschitz on [0 _,_ 1], with constant at most _ηϵ_ _[η]_ _p_ _[−]_ [1] . Composing the two
inequalities gives the conclusion.


**Lemma E.8** (Initial node representation stability) **.** _Let u_ _q_ = _W_ _q_ Emb( _q_ ) _, and define_


_h_ [(0)] _v_ = _a_ _v_ ( _q_ ) _u_ _q_ + _W_ _x_ _x_ _v_ _._ (102)


_Then_
_H_ (0) ( _q, G_ ) _−_ _H_ (0) ( _q, G_ _′_ ) (103)
��� ��� 2 _,∞_ _[≤]_ _[C]_ [init] [(∆] [seed] [ + ∆] _[X]_ [)] _[,]_


_where_


_p_
_C_ init = _[ηϵ]_ _[η][−]_ [1] _∥u_ _q_ _∥_ 2 + _∥W_ _x_ _∥_ 2 _._ (104)
_T_ 0


_Proof._ For any node _v_,


_h_ [(0)] _v_ _−_ _h_ _[′]_ _v_ [(0)] = ( _a_ _v_ _−_ _a_ _[′]_ _v_ [)] _[u]_ _[q]_ [+] _[ W]_ _[x]_ [(] _[x]_ _[v]_ _[−]_ _[x]_ _[′]_ _v_ [)] _[.]_ (105)


Taking the norm and applying Lemma 4.8 gives

_h_ (0) _v_ _−_ _h_ _[′]_ _v_ [(0)] _p_ _∥u_ _q_ _∥_ 2 ∆ seed + _∥W_ _x_ _∥_ 2 ∆ _X_ _._ (106)
��� ��� 2 _[≤]_ _[ηϵ]_ _T_ _[η]_ 0 _[−]_ [1]


Taking the maximum over _v_ gives the conclusion.


29


**E.4** **Single-layer Stability of Structurally Gated Propagation**


**Lemma E.9** (Boundedness and stability of structural gate) **.** _The structural gate of layer l,_

_g_ _uv_ [(] _[l]_ [)] [= 1 +] _[ δ]_ [ tanh(MLP] [(] _g_ _[l]_ [)] [(] _[z]_ _uv_ [(] _[l]_ [)] [))] _[,]_ (107)


_satisfies_
_g_ _uv_ ( _l_ ) (108)
��� ��� _∞_ _[≤]_ [1 +] _[ δ,]_


_and_
_g_ _uv_ ( _l_ ) _[−]_ _[g]_ _uv_ _[′]_ [(] _[l]_ [)] _z_ _uv_ ( _l_ ) _[−]_ _[z]_ _uv_ _[′]_ [(] _[l]_ [)] (109)
��� ��� _∞_ _[≤]_ _[δL]_ _[g,l]_ ��� ��� 2 _[.]_


_Proof._ Since the range of tanh is contained in [ _−_ 1 _,_ 1], the first statement follows immediately.
Moreover, because tanh is 1-Lipschitz and MLP [(] _g_ _[l]_ [)] [is] _[ L]_ _[g,l]_ [-Lipschitz in the trajectory neighborhood,]
��� _g_ _uv_ ( _l_ ) _[−]_ _[g]_ _uv_ _[′]_ [(] _[l]_ [)] ��� _∞_ _[≤]_ _[δ]_ ���MLP ( _gl_ ) [(] _[z]_ _uv_ [(] _[l]_ [)] [)] _[ −]_ [MLP] [(] _g_ _[l]_ [)] [(] _[z]_ _uv_ _[′]_ [(] _[l]_ [)] [)] ��� _∞_

_≤_ _δL_ _g,l_ _z_ _uv_ ( _l_ ) _[−]_ _[z]_ _uv_ _[′]_ [(] _[l]_ [)] (110)
��� ��� 2 _[.]_


**Lemma E.10** (Single-layer stability of structurally gated propagation) **.** _Define_


_D_ _l_ = _H_ ( _l_ ) ( _q, G_ ) _−_ _H_ ( _l_ ) ( _q, G_ _′_ ) (111)
��� ��� 2 _,∞_ _[.]_


_Under Assumptions 4.5–4.7, the l-th propagation layer satisfies_

_D_ _l_ _≤_ _α_ _l_ _D_ _l−_ 1 + _β_ _l_ _[A]_ [∆] _[A]_ [+] _[ β]_ _l_ _[Z]_ [∆] [(] _Z_ _[l]_ [)] _[,]_ (112)


_where one can take_
_α_ _l_ = _L_ LN _,l_ �1 + _L_ _σ_ (1 + _δ_ ) _M_ _l_ � _,_ (113)

_β_ _l_ _[A]_ [=] _[ L]_ [LN] _[,l]_ _[L]_ _[σ]_ [(1 +] _[ δ]_ [)] _[M]_ _[l]_ _[B]_ _[l][−]_ [1] _[,]_ _β_ _l_ _[Z]_ [=] _[ L]_ [LN] _[,l]_ _[L]_ _[σ]_ _[δL]_ _[g,l]_ _[M]_ _[l]_ _[B]_ _[l][−]_ [1] _[.]_ (114)



_Proof._ Write
_M_ _v_ = �



_A_ _[′]_ _vu_ _[g]_ _uv_ _[′]_ _[⊙]_ _[Wh]_ _[′]_ _u_ _[,]_ (115)

_u_



� _A_ _vu_ _g_ _uv_ _⊙_ _Wh_ _u_ _,_ _M_ _v_ _[′]_ [=] �


_u_ _u_



where the layer index _l_ is omitted. Adding and subtracting intermediate terms gives


_M_ _v_ _−_ _M_ _v_ _[′]_ [=] � _A_ _vu_ _g_ _uv_ _⊙_ _W_ ( _h_ _u_ _−_ _h_ _[′]_ _u_ [)]


_u_

+ �( _A_ _vu_ _−_ _A_ _[′]_ _vu_ [)] _[g]_ _[uv]_ _[⊙]_ _[Wh]_ _[′]_ _u_


_u_

+ � _A_ _[′]_ _vu_ [(] _[g]_ _[uv]_ _[−]_ _[g]_ _uv_ _[′]_ [)] _[ ⊙]_ _[Wh]_ _[′]_ _u_ _[.]_ (116)


_u_



The first term is controlled by row-normalization, _∥g_ _uv_ _∥_ _∞_ _≤_ 1 + _δ_, and _∥W_ _∥_ 2 _≤_ _M_ _l_ :


� _A_ _vu_ _g_ _uv_ _⊙_ _W_ ( _h_ _u_ _−_ _h_ _[′]_ _u_ [)] _≤_ (1 + _δ_ ) _M_ _l_ _D_ _l−_ 1 _._

����� _u_ ����� 2



�



_≤_ (1 + _δ_ ) _M_ _l_ _D_ _l−_ 1 _._ (117)
����� 2



_A_ _vu_ _g_ _uv_ _⊙_ _W_ ( _h_ _u_ _−_ _h_ _[′]_ _u_ [)]

_u_



The second term satisfies


�( _A_ _vu_ _−_ _A_ _[′]_ _vu_ [)] _[g]_ _[uv]_

����� _u_



�



( _A_ _vu_ _−_ _A_ _[′]_ _vu_ [)] _[g]_ _[uv]_ _[⊙]_ _[Wh]_ _[′]_ _u_

_u_



_≤_ (1+ _δ_ ) _M_ _l_ _B_ _l−_ 1 � _|A_ _vu_ _−_ _A_ _[′]_ _vu_ _[| ≤]_ [(1+] _[δ]_ [)] _[M]_ _[l]_ _[B]_ _[l][−]_ [1] [∆] _[A]_ _[.]_ [ (118)]
����� 2 _u_



For the third term, by Lemma 4.10,


� _A_ _[′]_ _vu_ [(] _[g]_ _[uv]_ _[−]_ _[g]_ _uv_ _[′]_ [)]

����� _u_



�



_A_ _[′]_ _vu_ [(] _[g]_ _[uv]_ _[−]_ _[g]_ _uv_ _[′]_ [)] _[ ⊙]_ _[Wh]_ _[′]_ _u_

_u_



_≤_ _δL_ _g,l_ _M_ _l_ _B_ _l−_ 1 � _A_ _[′]_ _vu_ ��� _z_ _uv_ ( _l_ ) _[−]_ _[z]_ _uv_ _[′]_ [(] _[l]_ [)] ��� 2
����� 2 _u_

_≤_ _δL_ _g,l_ _M_ _l_ _B_ _l−_ 1 ∆ [(] _Z_ _[l]_ [)] _[.]_ (119)


30


Therefore,


_∥M_ _v_ _−_ _M_ _v_ _[′]_ _[∥]_ 2 _[≤]_ [(1 +] _[ δ]_ [)] _[M]_ _[l]_ _[D]_ _[l][−]_ [1] [+ (1 +] _[ δ]_ [)] _[M]_ _[l]_ _[B]_ _[l][−]_ [1] [∆] _[A]_ [+] _[ δL]_ _[g,l]_ _[M]_ _[l]_ _[B]_ _[l][−]_ [1] [∆] [(] _Z_ _[l]_ [)] _[.]_ (120)


By the _L_ _σ_ -Lipschitz property of PReLU, the residual structure, and the _L_ LN _,l_ -Lipschitz property of
LayerNorm,

_h_ ( _vl_ ) _[−]_ _[h]_ _[′]_ _v_ [(] _[l]_ [)] _h_ ( _vl−_ 1) _−_ _h_ _[′]_ _v_ [(] _[l][−]_ [1)] _v_ _[∥]_ 2 _._ (121)
��� ��� 2 _[≤]_ _[L]_ [LN] _[,l]_ ���� ��� 2 [+] _[ L]_ _[σ]_ _[ ∥][M]_ _[v]_ _[ −]_ _[M]_ _[ ′]_ �


Taking the maximum over _v_ gives Eq. (112).


**E.5** **Stability of Representations, Scores, and Retrieval Sets**


**Theorem E.11** (Local stability of structurally gated representations to augmented graph drift) **.** _Under_
_Assumptions 4.5–4.7, L-layer structurally gated propagation satisfies_



�



_L_
� _α_ _l_
� _l_ = _t_ +1



_β_ _t_ _[A]_ [∆] _[A]_ [+] _[ β]_ _t_ _[Z]_ [∆] [(] _Z_ _[t]_ [)] _._ (122)
�
��



_D_ _L_ _≤_



_L_
� _α_ _l_
� _l_ =1



_D_ 0 +



_L_
�


_t_ =1



_Therefore, there exists a constant C_ _H_ _>_ 0 _such that_

_H_ ( _L_ ) ( _q, G_ ) _−_ _H_ ( _L_ ) ( _q, G_ _′_ ) (123)
��� ��� 2 _,∞_ _[≤]_ _[C]_ _[H]_ [(∆] _[X]_ [ + ∆] [seed] [ + ∆] _[A]_ [ + ∆] _[Z]_ [)] _[.]_


_Proof._ By Lemma 4.11, the recursion in Eq. (112) holds. Unrolling the recursion layer by layer gives
Eq. (122). By Lemma 4.9,
_D_ 0 _≤_ _C_ init (∆ _X_ + ∆ seed ) _._ (124)

Substituting ∆ [(] _Z_ _[t]_ [)] _[≤]_ [∆] _[Z]_ [ and merging all layer-related constants into] _[ C]_ _[H]_ [ gives the conclusion.]


**Theorem E.12** (Stability of context/schema dual channels) **.** _If the two channels respectively satisfy_


_∥H_ ctx ( _q, G_ ) _−_ _H_ ctx ( _q, G_ _[′]_ ) _∥_ 2 _,∞_ _≤_ _C_ ctx ∆ aug _,_ (125)


_∥H_ sch ( _q, G_ ) _−_ _H_ sch ( _q, G_ _[′]_ ) _∥_ 2 _,∞_ _≤_ _C_ sch ∆ aug _,_ (126)


_then the additive fusion in Eq._ ( **??** ) _satisfies_


_∥H_ ( _q, G_ ) _−_ _H_ ( _q, G_ _[′]_ ) _∥_ 2 _,∞_ _≤_ ( _C_ ctx + _|β_ sch _| C_ sch )∆ aug _._ (127)


_If a normalized or gated convex fusion theoretical form is adopted,_


_H_ _λ_ ( _q, G_ ) = (1 _−_ _λ_ ) _H_ ctx ( _q, G_ ) + _λH_ sch ( _q, G_ ) _,_ 0 _≤_ _λ ≤_ 1 _,_ (128)


_then_
_∥H_ _λ_ ( _q, G_ ) _−_ _H_ _λ_ ( _q, G_ _[′]_ ) _∥_ 2 _,∞_ _≤_ �(1 _−_ _λ_ ) _C_ ctx + _λC_ sch �∆ aug _._ (129)


_In particular, if C_ sch _< C_ ctx _, increasing λ decreases this worst-case stability upper bound._


_Proof._ The additive fusion case follows directly from the triangle inequality:


_∥H_ ( _G_ ) _−_ _H_ ( _G_ _[′]_ ) _∥_ 2 _,∞_ _≤∥H_ ctx ( _G_ ) _−_ _H_ ctx ( _G_ _[′]_ ) _∥_ 2 _,∞_ + _|β_ sch _| ∥H_ sch ( _G_ ) _−_ _H_ sch ( _G_ _[′]_ ) _∥_ 2 _,∞_
_≤_ ( _C_ ctx + _|β_ sch _| C_ sch )∆ aug _._ (130)


The convex fusion case is analogous:


_∥H_ _λ_ ( _G_ ) _−_ _H_ _λ_ ( _G_ _[′]_ ) _∥_ 2 _,∞_ _≤_ (1 _−_ _λ_ ) _C_ ctx ∆ aug + _λC_ sch ∆ aug _._ (131)


If _C_ sch _< C_ ctx, the right-hand side is monotonically decreasing in _λ_ .


_Remark_ E.13 _._ Equation (127) does not claim that the schema prior necessarily reduces the worst-case
Lipschitz constant of additive fusion; its main theoretical role also lies in risk decomposition and
sample complexity reduction. If additional gating, normalization, or regularization constraints are
adopted in the implementation, then Eq. (129) shows that the schema channel can also serve as a
low-sensitivity channel to reduce graph evolution drift.


31


**Theorem E.14** (Stability of entity scores and document scores) **.** _Under Assumption 4.7, there exist_
_constants C_ _E_ _, C_ _D_ _>_ 0 _such that_


_∥s_ _E_ ( _q, G_ ) _−_ _s_ _E_ ( _q, G_ _[′]_ ) _∥_ _∞_ _≤_ _C_ _E_ ∆ aug _,_ (132)


_∥s_ _D_ ( _q, G_ ) _−_ _s_ _D_ ( _q, G_ _[′]_ ) _∥_ _∞_ _≤_ _C_ _D_ ∆ aug _._ (133)


_For additive fusion, one can take_


_C_ _E_ = _L_ _E_ ( _C_ ctx + _|β_ sch _| C_ sch ) _,_ _C_ _D_ = _C_ _E_ + _S_ _E_ _._ (134)


_Proof._ The entity score upper bound follows from the Lipschitz property of the score head and
Theorem 4.13. For document projection, _s_ _D_ = _Bs_ _E_, and therefore


_s_ _D_ ( _G_ ) _−_ _s_ _D_ ( _G_ _[′]_ ) = _B_ _G_ ( _s_ _E_ ( _G_ ) _−_ _s_ _E_ ( _G_ _[′]_ )) + ( _B_ _G_ _−_ _B_ _G_ _′_ ) _s_ _E_ ( _G_ _[′]_ ) _._ (135)


Taking the _ℓ_ _∞_ norm and using _∥B_ _G_ _∥_ _∞_ _≤_ 1 gives


_∥s_ _D_ ( _G_ ) _−_ _s_ _D_ ( _G_ _[′]_ ) _∥_ _∞_ _≤∥s_ _E_ ( _G_ ) _−_ _s_ _E_ ( _G_ _[′]_ ) _∥_ _∞_ + _∥B_ _G_ _−_ _B_ _G_ _′_ _∥_ _∞_ _∥s_ _E_ ( _G_ _[′]_ ) _∥_ _∞_ _._ (136)


Using _∥s_ _E_ ( _G_ _[′]_ ) _∥_ _∞_ _≤_ _S_ _E_ and ∆ _B_ _≤_ ∆ aug gives the document score stability.


**Theorem E.15** (Boundary stability of hard top- _k_ ) **.** _Let_ _s_ = _s_ _D_ ( _q, G_ ) _and_ _s_ _[′]_ = _s_ _D_ ( _q, G_ _[′]_ ) _, and_

_suppose_
_∥s −_ _s_ _[′]_ _∥_ _∞_ _≤_ _ϵ_ _s_ _._ (137)


_Let t_ _k_ = _s_ ( _k_ ) _be the k-th largest score in s, and define the boundary set_


_B_ _k,_ 2 _ϵ_ _s_ ( _s_ ) = _{d_ : _|s_ _d_ _−_ _t_ _k_ _| ≤_ 2 _ϵ_ _s_ _}._ (138)


_Then_
Top _-k_ ( _s_ ) _△_ Top _-k_ ( _s_ _[′]_ ) _⊆B_ _k,_ 2 _ϵ_ _s_ ( _s_ ) _,_ (139)


_and hence_
_|_ Top _-k_ ( _s_ ) _△_ Top _-k_ ( _s_ _[′]_ ) _| ≤|B_ _k,_ 2 _ϵ_ _s_ ( _s_ ) _| ._ (140)

_In particular, if s_ ( _k_ ) _−_ _s_ ( _k_ +1) _>_ 2 _ϵ_ _s_ _, then_ Top _-k_ ( _s_ ) = Top _-k_ ( _s_ _[′]_ ) _._


_Proof._ Take any _i ∈_ Top- _k_ ( _s_ ) _\_ Top- _k_ ( _s_ _[′]_ ) . Since _i_ drops out of the top- _k_, there exists _j /∈_ Top- _k_ ( _s_ )
such that _j ∈_ Top- _k_ ( _s_ _[′]_ ) and _s_ _[′]_ _j_ _[≥]_ _[s]_ _[′]_ _i_ [. By the perturbation bound,]


_s_ _j_ + _ϵ_ _s_ _≥_ _s_ _[′]_ _j_ _[≥]_ _[s]_ _[′]_ _i_ _[≥]_ _[s]_ _[i]_ _[−]_ _[ϵ]_ _[s]_ _[,]_ (141)


so _s_ _i_ _≤_ _s_ _j_ + 2 _ϵ_ _s_ _≤_ _t_ _k_ + 2 _ϵ_ _s_ . Since _i ∈_ Top- _k_ ( _s_ ), we have _s_ _i_ _≥_ _t_ _k_, and hence _i ∈B_ _k,_ 2 _ϵ_ _s_ ( _s_ ) . A
symmetric argument for _j ∈_ Top- _k_ ( _s_ _[′]_ ) _\_ Top- _k_ ( _s_ ) gives _j ∈B_ _k,_ 2 _ϵ_ _s_ ( _s_ ) . Therefore, the symmetric
difference is contained in the boundary set. If _s_ ( _k_ ) _−_ _s_ ( _k_ +1) _>_ 2 _ϵ_ _s_, boundary exchange cannot occur,
and the top- _k_ set remains unchanged.


**Corollary E.16** (Top- _k_ boundary stability under graph evolution) **.** _By Theorem 4.15, taking_ _ϵ_ _s_ =
_C_ _D_ ∆ aug ( _G, G_ _[′]_ ; _q_ ) _yields_


_P_ _k_ ( _q, G_ ) _△P_ _k_ ( _q, G_ _[′]_ ) _⊆B_ _k,_ 2 _C_ _D_ ∆ aug ( _s_ _D_ ( _q, G_ )) _._ (142)


_Therefore, the instability of hard top-k is restricted to candidates near the original score boundary._


**Theorem E.17** (Stability of soft retrieval distribution) **.** _Let_


_π_ _D_ ( _q, G_ ) = softmax( _s_ _D_ ( _q, G_ ) _/τ_ ) _._ (143)


_If ∥s_ _D_ ( _q, G_ ) _−_ _s_ _D_ ( _q, G_ _[′]_ ) _∥_ _∞_ _≤_ _ϵ_ _s_ _, then_

_∥π_ _D_ ( _q, G_ ) _−_ _π_ _D_ ( _q, G_ _[′]_ ) _∥_ 1 _≤_ [2] (144)

_τ_ _[ϵ]_ _[s]_ _[.]_


_Therefore,_

_∥π_ _D_ ( _q, G_ ) _−_ _π_ _D_ ( _q, G_ _[′]_ ) _∥_ 1 _≤_ [2] _[C]_ _[D]_ ∆ aug ( _G, G_ _[′]_ ; _q_ ) _._ (145)

_τ_


32


_Proof._ The Jacobian of softmax is _J_ ( _z_ ) = diag( _π_ ) _−_ _ππ_ _[⊤]_ . For any perturbation _r_,


_J_ ( _z_ ) _r_ = _π ⊙_ ( _r −_ E _π_ _r_ ) _._ (146)


If _∥r∥_ _∞_ _≤_ 1, then _|r_ _i_ _−_ E _π_ _r| ≤_ 2, so


_∥J_ ( _z_ ) _r∥_ 1 _≤_ � _π_ _i_ _|r_ _i_ _−_ E _π_ _r| ≤_ 2 _._ (147)


_i_


Thus, the _ℓ_ _∞_ _→_ _ℓ_ 1 Lipschitz constant of softmax is at most 2. Since the input is _s_ _D_ _/τ_, we obtain


_∥π_ _D_ ( _s_ ) _−_ _π_ _D_ ( _s_ _[′]_ ) _∥_ 1 _≤_ [2] (148)

_τ_ _[∥][s][ −]_ _[s]_ _[′]_ _[∥]_ _[∞]_ _[.]_


Substituting Theorem 4.15 gives the conclusion.


**Theorem E.18** (High-probability graph evolution stability) **.** _If the writer’s single-round graph update_
_satisfies_
P[∆ aug ( _G, G_ _[′]_ ; _q_ ) _> ϵ_ ] _≤_ _δ,_ (149)


_then_
P [ _∥s_ _D_ ( _q, G_ ) _−_ _s_ _D_ ( _q, G_ _[′]_ ) _∥_ _∞_ _> C_ _D_ _ϵ_ ] _≤_ _δ._ (150)


_If_ E[∆ aug ( _G, G_ _[′]_ ; _q_ )] _≤_ _ϵ_ ¯ _, then_


E [ _∥s_ _D_ ( _q, G_ ) _−_ _s_ _D_ ( _q, G_ _[′]_ ) _∥_ _∞_ ] _≤_ _C_ _D_ _ϵ._ ¯ (151)


_Proof._ By Theorem 4.15, for any graph pair, we have


_∥s_ _D_ ( _q, G_ ) _−_ _s_ _D_ ( _q, G_ _[′]_ ) _∥_ _∞_ _≤_ _C_ _D_ ∆ aug ( _G, G_ _[′]_ ; _q_ ) _._ (152)


Therefore, the event _{∥s_ _D_ ( _q, G_ ) _−_ _s_ _D_ ( _q, G_ _[′]_ ) _∥_ _∞_ _> C_ _D_ _ϵ}_ implies the event _{_ ∆ aug ( _G, G_ _[′]_ ; _q_ ) _> ϵ}_,
so the probability upper bound follows immediately. The expectation conclusion follows by taking
expectations on both sides of the deterministic inequality.


**E.6** **Local Influence Cone**


_Proposition_ 8 (Influence cone of local graph updates) _._ Suppose the writer only changes nodes, edges,
anchors, or attributes on a primitive set _U_ . Suppose that the structural gate input _z_ _uv_ [(] _[l]_ [)] [, except for the]
graph-level summary, only depends on a local neighborhood of radius _r_ _z_, and that _G_ and _G_ _[′]_ are
exactly the same outside _N_ _L_ + _r_ _z_ ( _U_ ). If graph-level summary drift is ignored, then for any


_v /∈N_ _L_ + _r_ _z_ ( _U_ ) _,_ (153)


we have
_h_ [(] _v_ _[L]_ [)] ( _q, G_ ) = _h_ [(] _v_ _[L]_ [)] ( _q, G_ _[′]_ ) _._ (154)


If the graph-level summary drift is _ρ_ _g_ = _∥r_ _G_ _−_ _r_ _G_ _′_ _∥_ 2, then there exists a constant _C_ _g_ such that

_h_ ( _vL_ ) ( _q, G_ ) _−_ _h_ [(] _v_ _[L]_ [)] ( _q, G_ _[′]_ ) (155)
��� ��� 2 _[≤]_ _[C]_ _[g]_ _[ρ]_ _[g]_ _[.]_


_Proof._ First consider the case without graph-level summary drift. We induct on the layer index _l_ .
For _l_ = 0, if _v /∈N_ _L_ + _r_ _z_ ( _U_ ), then its node features, presence bit, and seed score are all identical,
so _h_ [(0)] _v_ [(] _[G]_ [) =] _[ h]_ [(0)] _v_ [(] _[G]_ _[′]_ [)] [. Suppose that at layer] _[ l][ −]_ [1] [, all nodes whose distance from] _[ U]_ [ exceeds]
_L_ + _r_ _z_ _−_ ( _l −_ 1) have identical representations. If _v /∈N_ _L_ + _r_ _z_ _−l_ ( _U_ ), then all its one-hop neighbors _u_
do not belong to _N_ _L_ + _r_ _z_ _−_ ( _l−_ 1) ( _U_ ) ; by the induction hypothesis, _h_ [(] _u_ _[l][−]_ [1)] ( _G_ ) = _h_ [(] _u_ _[l][−]_ [1)] ( _G_ _[′]_ ) . Meanwhile,
the radius- _r_ _z_ local structural contexts of all relevant edges are also identical, so the gate, message
multiset, and aggregation result are identical, and hence _h_ [(] _v_ _[l]_ [)] [(] _[G]_ [) =] _[ h]_ [(] _v_ _[l]_ [)] [(] _[G]_ _[′]_ [)] [. Taking] _[ l]_ [ =] _[ L]_ [ gives the]
first conclusion. If graph-level summary drift exists, then the gate input has an additional uniform
perturbation term _ρ_ _g_, and a _C_ _g_ _ρ_ _g_ -type upper bound follows from Lemma 4.10 and the recursion in
Theorem 4.12.


33


**F** **Theoretical Motivation of the Self-evolving Writer–Reader Loop**


**F.1** **Joint Memory Utility**


The reader-aware writer reward can consist of evidence coverage, precision, deducibility, and answer
utility. Abstractly, define the joint memory utility as

_J_ ( _θ, ϕ_ ) = E ( _q,D,D_ + _,y_ ) � _U_ � _R_ _ϕ_ ( _q, W_ _θ_ ( _q, D_ ) _, D_ ) _, D_ [+] _, y_ �� _,_ (156)


where _U_ can be taken as


_[β][r]_ [p][re] [ +] _[γ][r]_ [ded]
_U_ = _[αr]_ [rec] [ +] _−_ _λ_ rep _ρ_ rep + _λ_ fmt _r_ fmt _,_ (157)

_α_ + _β_ + _γ_


or an extended form including answer-level reward. This definition places the writer’s graph construction quality and the reader’s graph reading ability under the same objective.


**F.2** **Approximate Coordinate Improvement**


**Theorem F.1** (The self-evolution process is approximate coordinate improvement on joint utility) **.**
_Suppose that the writer update at round r satisfies_

_J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [)] ) _≥J_ ( _θ_ [(] _[r]_ [)] _, ϕ_ [(] _[r]_ [)] ) + ∆ [(] _W_ _[r]_ [)] _[−]_ _[ϵ]_ [(] _W_ _[r]_ [)] _[,]_ (158)


_and the reader update satisfies_

_J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [+1)] ) _≥J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [)] ) + ∆ [(] _R_ _[r]_ [)] _[−]_ _[ϵ]_ [(] _R_ _[r]_ [)] _[.]_ (159)


_Then one full round of writer–reader self-evolution satisfies_

_J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [+1)] ) _−J_ ( _θ_ [(] _[r]_ [)] _, ϕ_ [(] _[r]_ [)] ) _≥_ ∆ [(] _W_ _[r]_ [)] [+ ∆] [(] _R_ _[r]_ [)] _[−]_ _[ϵ]_ [(] _W_ _[r]_ [)] _[−]_ _[ϵ]_ [(] _R_ _[r]_ [)] _[.]_ (160)

_Therefore, as long as_ ∆ [(] _W_ _[r]_ [)] [+ ∆] [(] _R_ _[r]_ [)] _[> ϵ]_ [(] _W_ _[r]_ [)] [+] _[ ϵ]_ [(] _R_ _[r]_ [)] _[, the joint memory utility improves in that round.]_


_Proof._ By telescoping decomposition,


_J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [+1)] ) _−J_ ( _θ_ [(] _[r]_ [)] _, ϕ_ [(] _[r]_ [)] )


= _J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [+1)] ) _−J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [)] ) + _J_ ( _θ_ [(] _[r]_ [+1)] _, ϕ_ [(] _[r]_ [)] ) _−J_ ( _θ_ [(] _[r]_ [)] _, ϕ_ [(] _[r]_ [)] ) _._ (161)
� � � �


Substituting Eq. (158) and Eq. (159), respectively, gives the conclusion.


**F.3** **Reader Reward Bias and Calibration Benefit**


**Definition F.2** (True utility and reader surrogate reward) **.** Let _U_ _[⋆]_ ( _G_ ) denote the true utility of
graph memory _G_ with respect to the downstream task, and let _U_ [�] _ϕ_ ( _G_ ) denote the surrogate reward
constructed from the readout result of reader _R_ _ϕ_ . We say that the reader reward bias is at most _ϵ_ _ϕ_ if,
for all considered graphs _G_,
_U_ _ϕ_ ( _G_ ) _−_ _U_ _⋆_ ( _G_ ) _≤_ _ϵ_ _ϕ_ _._ (162)
���� ���

**Theorem F.3** (Surrogate reward improvement to true utility improvement) **.** _If the reader reward bias_
_is at most ϵ_ _ϕ_ _, and the writer update improves the surrogate reward by_


� �
_U_ _ϕ_ ( _G_ _θ_ _′_ ) _−_ _U_ _ϕ_ ( _G_ _θ_ ) _≥_ ∆ _,_ (163)


_then the true utility satisfies_
_U_ _[⋆]_ ( _G_ _θ_ _′_ ) _−_ _U_ _[⋆]_ ( _G_ _θ_ ) _≥_ ∆ _−_ 2 _ϵ_ _ϕ_ _._ (164)


_Proof._ By the bias assumption,

_U_ _[⋆]_ ( _G_ _θ_ _′_ ) _≥_ _U_ [�] _ϕ_ ( _G_ _θ_ _′_ ) _−_ _ϵ_ _ϕ_ _,_ _U_ _[⋆]_ ( _G_ _θ_ ) _≤_ _U_ [�] _ϕ_ ( _G_ _θ_ ) + _ϵ_ _ϕ_ _._ (165)


Subtracting the two inequalities gives

_U_ _[⋆]_ ( _G_ _θ_ _′_ ) _−_ _U_ _[⋆]_ ( _G_ _θ_ ) _≥_ _U_ [�] _ϕ_ ( _G_ _θ_ _′_ ) _−_ _U_ [�] _ϕ_ ( _G_ _θ_ ) _−_ 2 _ϵ_ _ϕ_ _≥_ ∆ _−_ 2 _ϵ_ _ϕ_ _._ (166)


34


**Corollary F.4** (Reader calibration reduces writer optimization bias) **.** _If the reader is calibrated from_
_ϕ_ _to_ _ϕ_ _[′]_ _and reduces the reward bias from_ _ϵ_ _ϕ_ _to_ _ϵ_ _ϕ_ _′_ _, where_ _ϵ_ _ϕ_ _′_ _< ϵ_ _ϕ_ _, then for the same surrogate_
_reward improvement_ ∆ _, the lower bound on true utility improvement increases by_


2( _ϵ_ _ϕ_ _−_ _ϵ_ _ϕ_ _′_ ) _._ (167)


_Proof._ By Theorem 5.3, the true utility improvement lower bound before calibration is ∆ _−_ 2 _ϵ_ _ϕ_, and
after calibration it is ∆ _−_ 2 _ϵ_ _ϕ_ _′_ . Subtracting the two gives the result.


**F.4** **Irreducible Bottlenecks of Single-sided Updates**


_Proposition_ 9 (Lower-bound bottlenecks of single-sided updates) _._ Assume that the overall error can
be decomposed as
_E_ ( _θ, ϕ_ ) = _E_ write ( _θ_ ) + _E_ read ( _ϕ_ ; _θ_ ) + _ϵ_ int ( _θ, ϕ_ ) _,_ (168)


where all terms are nonnegative. If only the reader is updated, i.e., _ϕ �→_ _ϕ_ _[′]_ while _θ_ is fixed, then


_E_ ( _θ, ϕ_ _[′]_ ) _≥E_ write ( _θ_ ) _._ (169)


If only the writer is updated, i.e., _θ �→_ _θ_ _[′]_ while _ϕ_ is fixed, then


_E_ ( _θ_ _[′]_ _, ϕ_ ) _≥E_ read ( _ϕ_ ; _θ_ _[′]_ ) _._ (170)


Therefore, reader-only updates cannot compensate for evidence chains that the writer has not written;
writer-only updates cannot guarantee that a fixed reader can read out the evidence structures in the
new graph distribution.


_Proof._ By the decomposition in Eq. (168) and the nonnegativity of all terms,


_E_ ( _θ, ϕ_ _[′]_ ) = _E_ write ( _θ_ ) + _E_ read ( _ϕ_ _[′]_ ; _θ_ ) + _ϵ_ int ( _θ, ϕ_ _[′]_ ) _≥E_ write ( _θ_ ) _._ (171)


The second inequality is analogous.


**F.5** **Stability of Closed-loop Graph Evolution and Parameter Updates**


**Theorem F.5** (Score drift control under multi-round self-evolution) **.** _Let the graph at round_ _r_ _be_
_G_ [(] _[r]_ [)] _, and the reader parameter be ϕ_ [(] _[r]_ [)] _. If single-step graph stability satisfies_

_s_ _D_ ( _q, G_ ( _r_ +1) ; _ϕ_ ( _r_ ) ) _−_ _s_ _D_ ( _q, G_ ( _r_ ) ; _ϕ_ ( _r_ ) ) (172)
��� ��� _∞_ _[≤]_ _[C]_ _[D]_ [∆] _[r]_ _[,]_


_where_ ∆ _r_ = ∆ aug ( _G_ [(] _[r]_ [)] _, G_ [(] _[r]_ [+1)] ; _q_ ) _; and if the score is locally Lipschitz with respect to the parame-_
_ter:_
_∥s_ _D_ ( _q, G_ ; _ϕ_ ) _−_ _s_ _D_ ( _q, G_ ; _ϕ_ _[′]_ ) _∥_ _∞_ _≤_ _C_ _ϕ_ _∥ϕ −_ _ϕ_ _[′]_ _∥_ 2 _,_ (173)


_then_
_s_ _D_ ( _q, G_ ( _T_ ) ; _ϕ_ ( _T_ ) ) _−_ _s_ _D_ ( _q, G_ (0) ; _ϕ_ (0) )
��� ��� _∞_



(174)

_._
�



_≤_



_T −_ 1
�


_r_ =0



_C_ _D_ ∆ _r_ + _C_ _ϕ_ _ϕ_ ( _r_ +1) _−_ _ϕ_ ( _r_ )
� ��� ��� 2



_Proof._ For each _r_, adding and subtracting the intermediate term _s_ _D_ ( _q, G_ [(] _[r]_ [+1)] ; _ϕ_ [(] _[r]_ [)] ) gives

_s_ _D_ ( _q, G_ ( _r_ +1) ; _ϕ_ ( _r_ +1) ) _−_ _s_ _D_ ( _q, G_ ( _r_ ) ; _ϕ_ ( _r_ ) )
��� ��� _∞_


_≤_ _s_ _D_ ( _q, G_ ( _r_ +1) ; _ϕ_ ( _r_ +1) ) _−_ _s_ _D_ ( _q, G_ ( _r_ +1) ; _ϕ_ ( _r_ ) ) _s_ _D_ ( _q, G_ ( _r_ +1) ; _ϕ_ ( _r_ ) ) _−_ _s_ _D_ ( _q, G_ ( _r_ ) ; _ϕ_ ( _r_ ) )
��� ��� _∞_ [+] ��� ��� _∞_

_≤_ _C_ _ϕ_ _ϕ_ ( _r_ +1) _−_ _ϕ_ ( _r_ ) (175)
��� ��� 2 [+] _[ C]_ _[D]_ [∆] _[r]_ _[.]_


Summing over _r_ = 0 _, . . ., T −_ 1 and using the triangle inequality gives the conclusion.


35


Table 5: Training results for the memory writer. _GFM-_
_pretrained-only_ refers to using rewards fed back only
by the pretrained memory reader, while _GFM-finetuned_
further refers to using the fine-tuned memory reader.


Methods Prec. _↑_ Recall _↑_ Deducible _↑_


GFM-pretrained-only 0.838 0.818 0.510
GFM-finetuned 0.824 0.813 0.512
RL-Recall 0.889 0.835 0.502

RL-F1 0.839 0.881 0.497

RL-Deduce 0.861 0.892 0.517
RL-Hybrid **0.902** **0.917** 0.522
Hybrid + frozen answer API 0.832 0.874 **0.526**


**Corollary F.6** (High-probability multi-round stability) **.** _If_ P[∆ _r_ _> ϵ_ _r_ ] _≤_ _δ_ _r_ _, then with probability at_
_least_ 1 _−_ [�] _[T]_ _r_ =0 _[ −]_ [1] _[δ]_ _[r]_ _[,]_
_s_ _D_ ( _q, G_ ( _T_ ) ; _ϕ_ ( _T_ ) ) _−_ _s_ _D_ ( _q, G_ (0) ; _ϕ_ (0) )
��� ��� _∞_



(176)

_._
�



_≤_



_T −_ 1
�


_r_ =0



_C_ _D_ _ϵ_ _r_ + _C_ _ϕ_ _ϕ_ ( _r_ +1) _−_ _ϕ_ ( _r_ )
� ��� ��� 2



_Proof._ By a union bound, the event _{∀r,_ ∆ _r_ _≤_ _ϵ_ _r_ _}_ holds with probability at least 1 _−_ [�] _r_ _[δ]_ _[r]_ [.]

Applying Theorem 5.7 on this event gives the conclusion.


**G** **Analysis of the Memory Writer**


This section further analyzes the memory writer while keeping the memory reader fixed. The experiments mainly use HotpotQA and MuSiQue. To further examine domain transfer capability, we also
evaluate the trained writing policy on GRBench-Amazon, HaluMem-Medium, and LongMemEvalOracle [ **??** ]. We primarily report Precision, Recall, and Deducible: the first two measure whether the
text retrieved by the reader covers the gold supporting contexts, while Deducible is determined by a
judge as to whether the standard answer can be inferred from the retrieved context, thus more directly
reflecting whether the graph memory is usable for reasoning.


Table 5 shows that different rewards have different preferences. Overall, RL-Hybrid achieves the
best overall results, indicating that hybrid rewards can simultaneously constrain the selectivity and
coverage of graph writing. _Hybrid + frozen answer API_ achieves the highest Deducible but slightly
lower retrieval Precision/Recall, suggesting that answer-side feedback helps improve reasoning
usability, but may also make the writer more conservatively inclined to write evidence that directly
supports the answer. Table 6 shows that a writer learned on HotpotQA/MuSiQue can transfer to
GRBench, HaluMem, and LongMemEval, but continued training on the target domain still brings
significant improvements. This indicates that the memory structure in agent memory scenarios is
not entirely similar to that in traditional multi-hop QA, so target-domain feedback remains crucial.
Table 7 further shows that the writing protocol and interaction budget affect the trade-off between
coverage and noise. Relaxing the tight prompt can improve Recall, but reduces Deducible; increasing
iterative turns helps complete cross-document bridging paths, but when the budget is too large or
the protocol is too loose. More detailed reader-side sensitivity, training stability, and regularization
analyses are provided in Appendix A.


**H** **Ablation Study of the Memory Reader**


We conduct ablation studies to isolate the contribution of each major component in the memory
reader. All variants use the same writer-produced graph memory and the same retrieval budget unless
the ablated component directly changes the retrieval mechanism. The ablations are organized around
four questions: (1) whether structured query planning and global soft addressing are necessary for
recovering evidence from fragmented cues; (2) whether structurally gated propagation improves over


36


Table 6: Cross-dataset memory writing results. “Base _→_ Target”
indicates direct evaluation on the target domain after training
on the HotpotQA/MuSiQue base; “Target train _→_ val” indicates
training and validation on the target domain.


Settings Prec. _↑_ Recall _↑_ Deducible _↑_


Base _→_ GRBench 0.575 0.609 0.411

GRBench train _→_ val 0.794 0.833 0.596

Base _→_ HaluMem 0.230 0.448 0.299

HaluMem train _→_ val 0.312 0.708 0.438
Base _→_ LongMemEval 0.232 0.376 0.475
LongMem train _→_ LongMemEval 0.377 0.439 0.531


Table 7: Ablation of writing protocols and interaction budgets. Tight=True indicates that the writer
performs a single-round graph write under a stricter evidence budget, meaning the reader exposes
only fewer, higher-confidence candidate pieces of evidence to the writer; Tight=False indicates that
this evidence budget is relaxed, allowing the writer to access a broader candidate context. Iterative
indicates that multi-round interactive writer–reader writing is enabled: the writer first writes the initial
graph memory, the reader then returns retrieval feedback based on the current graph, and the writer
continues to supplement or revise the graph structure. Here, 12/20/24 turns indicates the maximum
number of interaction rounds allowed, and tight/loose indicates that strict or relaxed evidence budget
constraints are still used during this multi-round interaction process.


Settings Prec. _↑_ Recall _↑_ Deducible _↑_


Tight=True 0.836 0.806 0.515
Tight=False 0.845 0.851 0.506
Iterative, 12 turns, tight 0.852 0.829 0.516
Iterative, 20 turns, tight 0.835 **0.881** 0.522
Iterative, 24 turns, loose **0.863** 0.826 **0.531**


uniform graph propagation; (3) whether cross-graph structural priors and target-graph calibration
are both needed for evolving graph memory; and (4) whether reader training and entity-to-document
projection are important for converting entity-level activation into document-level retrieval.


Table 8 summarizes the results. The first group evaluates how the reader handles fragmented cues.
Removing structured query planning, alias/constraint cues, or global soft addressing forces the reader
to rely more heavily on surface-level query matches or a small number of anchor entities, directly
testing whether the complete evidence chain can still be recovered when distant bridge nodes are not
initially activated. The second group studies whether the reader uses graph structure in a learned
and selective way. Removing structural gates or replacing them with uniform message passing tests
whether treating hub edges, bridge edges, redundant edges, and noisy shortcuts similarly harms
retrieval. The third group examines the context–schema decomposition: the schema channel captures
transferable structural reading patterns, while the context channel adapts the reader to the current
writer-produced graph. The last group evaluates the selector, entity-to-document projection, GFM
pre-training, and supervised retrieval fine-tuning.


The ablation results show the relative contribution of each memory-reader component. First, structured
query planning and global soft addressing are important for fragmented-cue retrieval: removing
them noticeably weakens performance, especially on MuSiQue and 2WikiMultiHopQA, where
evidence chains are more likely to depend on implicit bridge entities. Second, structurally gated
propagation consistently improves over uniform message passing, indicating that graph structure
should be used selectively rather than as a fixed expansion rule. Among the structural inputs, graphlevel summaries have a relatively smaller effect, while node-level and edge-pair features are more
important for recognizing hubs, bridges, and cross-community evidence paths. Third, both the schema
prior and context calibration channels contribute to performance, suggesting that the reader benefits
from preserving transferable structural priors while adapting to the current writer-produced graph.
Finally, supervised retrieval fine-tuning is essential for aligning the GFM reader with documentlevel evidence retrieval, whereas GFM pre-training provides transferable structural initialization that
improves stability across datasets.


37


Table 8: Ablation study of the memory reader on multi-hop QA retrieval. We report document-level
Recall (%) at top-2 and top-5. All variants use the same writer-produced graph memory unless
otherwise specified.

|Reader Variant|HotpotQA|MuSiQue|2WikiMultiHopQA|
|---|---|---|---|
||R@2<br>R@5|R@2<br>R@5|R@2<br>R@5|
|**SAGE**|**65.1**<br>**77.6**|**43.2**<br>**53.1**|**83.6**<br>**88.6**|



_Query planning and global addressing_
SAGE w/o Structured Query Planning 62.7 75.1 40.4 50.1 80.7 86.6
SAGE w/o Global Soft Addressing 59.3 72.5 37.6 47.4 75.9 83.1
SAGE w/o Alias and Constraint Cues 63.0 75.8 41.0 50.8 80.8 86.9
SAGE w/ Anchor-only Initialization 58.6 71.4 36.8 46.5 74.2 82.4

_Structurally conditioned propagation_
SAGE w/o Structural Gate 60.4 73.2 39.2 48.7 78.1 84.9
SAGE w/o Node Structural Features 62.1 74.8 40.5 50.0 80.0 86.0
SAGE w/o Edge-pair Structural Features 61.5 74.0 40.1 49.4 79.1 85.6
SAGE w/o Graph-level Summary 63.2 75.9 41.6 51.0 81.3 87.0
SAGE w/ Uniform Message Passing 58.9 71.8 37.5 46.9 75.3 82.9

_Cross-graph priors and target-graph calibration_
SAGE w/o Schema Prior Channel 62.4 75.0 40.9 50.6 80.4 86.4
SAGE w/o Context Calibration Channel 61.8 74.3 40.0 49.8 79.5 85.9
SAGE w/o Context–Schema Fusion 60.7 73.5 39.1 48.6 77.8 84.7

_Selector, projection, and reader training_
SAGE w/o Controlled Entity-to-Document Projection 60.9 73.9 38.7 48.2 77.2 84.4
SAGE w/o Query-conditioned Selector 63.9 76.5 41.9 52.0 82.2 87.6
SAGE w/ Vanilla GNN Reader 57.2 70.6 36.3 45.2 72.8 80.7


**I** **Implementation Details of the Query-conditioned Subgraph Selection**
**Regularizer**


We provide the implementation details of the query-conditioned subgraph selector. In addition to
the base entity scoring, it further learns a soft gating probability _π_ _e_ ( _q_ ), which characterizes whether
entity _e_ should enter the reading subgraph of the current query _q_ . This module performs lightweight
reweighting of the final entity score, and constrains the reading subgraph through several structural
regularizers during training.


**Query-conditioned Selection Probability.** Given a query _q_ and a graph _G_ = ( _V, E_ ), let **h** _e_ _∈_ R _[d]_
denote the representation of entity node _e ∈V_ after propagation by the GFM backbone, and let
**z** _q_ _∈_ R _[d]_ denote the query representation output by the query encoder and then linearly projected.
Here, _d_ is the hidden dimension. The selector first projects the node representation and the query
representation into the same selector space:


**u** _e_ = _W_ _n_ **h** _e_ _,_ **v** _q_ = _W_ _s_ **z** _q_ _,_ (177)


where _W_ _n_ _∈_ R _[d]_ _[s]_ _[×][d]_ is the node-side projection matrix, _W_ _s_ _∈_ R _[d]_ _[s]_ _[×][d]_ is the query-side projection
matrix, and _d_ _s_ is the hidden dimension of the selector space. In our implementation, we set _d_ _s_ = _d_,
but the two do not have to be equal. Then, the selector obtains the selection logit of entity _e_ with
respect to query _q_ through a scaled inner product:


_e_ **[v]** _[q]_
_ζ_ _e_ ( _q_ ) = **[u]** _[⊤]_ _,_ (178)
_T_ _s_


where _T_ _s_ _>_ 0 is the selector temperature coefficient. The final soft selection probability is defined as


1
_π_ _e_ ( _q_ ) = sigmoid( _ζ_ _e_ ( _q_ )) = 1 + exp( _−ζ_ _e_ ( _q_ )) _[.]_ (179)


Here, _π_ _e_ ( _q_ ) _∈_ (0 _,_ 1) can be understood as the soft probability that entity _e_ is included in the reading
subgraph of the current query. During training, we directly use _π_ _e_ ( _q_ ) for differentiable optimization;
during inference, we can either continue to use the soft probability for reweighting, or obtain a
discrete subgraph according to a threshold _τ_ _π_ :


_V_ _q_ = _{e ∈V | π_ _e_ ( _q_ ) _> τ_ _π_ _},_ _E_ _q_ = _{_ ( _u, v_ ) _∈E | u, v ∈V_ _q_ _}._ (180)


38


Let _a_ _e_ ( _q_ ) denote the base entity score given by the GFM backbone reader. This score is usually
obtained from the similarity between the node representation and the query representation, for
example
_a_ _e_ ( _q_ ) = **h** _[⊤]_ _e_ **[z]** _[q]_ _[.]_ (181)

Finally, we have:
_a_ [final] _e_ ( _q_ ) = _a_ _e_ ( _q_ ) + _λ_ _s_ _ζ_ _e_ ( _q_ ) _,_ (182)

where _λ_ _s_ _≥_ 0 controls the influence of the selector logit on the final entity ranking.


**Query–Subgraph Contrastive Regularizer.** Using only Eq. (182) to fuse the selector score can
easily lead to two types of degeneration: first, the selector may assign high probabilities to most
nodes, thereby degenerating into full-graph activation; second, the selector may only learn local
high-frequency entities, without forming a subgraph representation that is consistent with the overall
semantics of the query. To this end, we first construct a query-conditioned subgraph representation
weighted by the selection probabilities:



¯
�
**h** _π_ ( _q_ ) =



� _e∈V_ _[π]_ _[e]_ [(] _[q]_ [)] **[h]** _[e]_

~~�~~ _e∈V_ _[π]_ _[e]_ [(] _[q]_ [) +]



(183)
_e∈V_ _[π]_ _[e]_ [(] _[q]_ [) +] _[ ϵ,]_



where _ϵ >_ 0 is a numerical stability term, which avoids an excessively small denominator when all
_π_ _e_ ( _q_ ) are close to 0 . **h** [¯] _π_ ( _q_ ) can be understood as the semantic center of the soft subgraph activated
by the current selector.


For a mini-batch _B_ = _{q_ _i_ _}_ _[B]_ _i_ =1 [, we treat] [ (¯] **[h]** _[π]_ [(] _[q]_ _[i]_ [)] _[,]_ **[ z]** _[q]_ _i_ [)] [ within the same sample as a positive pair, and]
treat ( **h** [¯] _π_ ( _q_ _i_ ) _,_ **z** _q_ _j_ ), _j ̸_ = _i_, as in-batch negative pairs. The query–subgraph contrastive loss is defined

as



~~�~~ _Bj_ =1 [exp] ~~�~~ sim( **h** [¯] _π_ ( _q_ _i_ ) _,_ **z** _q_ _j_ ) _/T_ _n_ ~~�~~ _,_ (184)



Ω nce = _−_ _B_ [1]



_B_
�



exp �sim( **h** [¯] _π_ ( _q_ _i_ ) _,_ **z** _q_ _i_ ) _/T_ _n_ �

� log _B_

_i_ =1 ~~�~~ =1 [exp] ~~�~~ sim( **h** [¯] _π_ ( _q_ _i_ ) _,_ **z** _q_ _j_ )



where _T_ _n_ _>_ 0 is the contrastive learning temperature coefficient, and sim( _·, ·_ ) is the similarity
function. In implementation, we usually apply product similarity, so that sim( **h** [¯] _π_ ( _q_ ) _,_ **z** _q_ ) = _∥_ **h** ~~[¯]~~ _π_ **h** ¯ _ℓ_ ( _π_ _q_ (2) _q∥_ normalization to ) 2 _[⊤]_ _∥_ **zz** _qq_ _∥_ 2 [. This term encourages the soft subgraph] **h** [¯] _π_ ( _q_ ) and **z** _q_, and use inner
activated by the selector to semantically represent the current query, rather than only selecting nodes
with high frequency or high centrality in the graph.


**Size Regularizer.** To prevent the selector from improving recall by activating a large number of
nodes, we use the average selection probability as a size penalty:



Ω size = _|V|_ [1]



� _π_ _e_ ( _q_ ) _._ (185)


_e∈V_



This term approximately represents the expected proportion of activated nodes. Minimizing Ω size
pushes the model to select a smaller reading subgraph. However, this term cannot be used alone;
otherwise, the selector may degenerate into selecting too few nodes or even no nodes. Therefore,
it needs to be jointly optimized with Ω nce and the main retrieval loss: the former ensures query
relevance, while the latter ensures that the selected structure can still support correct entity and
document recall.


**Connectivity Smoothing Regularizer.** In addition to controllable size, an effective reading subgraph should also have local structural coherence. If the selection probabilities of adjacent nodes
differ too much, the model may form several isolated activated points, making multi-hop paths
difficult to explicitly utilize. To this end, we use a smoothing penalty on edges:



Ω con = _|E|_ [1]



� ( _π_ _u_ ( _q_ ) _−_ _π_ _v_ ( _q_ )) [2] _._ (186)

( _u,v_ ) _∈E_



Here, ( _u, v_ ) is a directed or undirected edge in the graph, depending on whether edge directions
are preserved during graph construction. If an undirected graph is used, _E_ can be viewed as the
symmetrized edge set. This term does not force all selected nodes to be strictly connected, but
encourages adjacent nodes to have similar selection probabilities. In matrix form, if _**π**_ ( _q_ ) _∈_ R _[|V|]_ is


39


the selection probability vector composed of _π_ _e_ ( _q_ ), and **L** is the graph Laplacian matrix, then this
term is equivalent to Laplacian smoothing:


Ω con _∝_ _**π**_ ( _q_ ) _[⊤]_ **L** _**π**_ ( _q_ ) _._ (187)


Therefore, it is consistent with the classical assumption of graph signal smoothing: query relevance, as
a soft signal on the graph, should maintain a certain degree of continuity within local neighborhoods.


**Computational Complexity of the Selector Itself.** Let the batch size be _B_, the number of nodes
be _n_ = _|V|_, the number of edges be _m_ = _|E|_, and the hidden dimension be _d_ . The cost of computing
_W_ _n_ **h** _e_ is _O_ ( _Bnd_ [2] ), the cost of computing _W_ _s_ **z** _q_ is _O_ ( _Bd_ [2] ), and the cost of the inner-product logits
is _O_ ( _Bnd_ ) . If we cache _W_ _n_ **h** _e_ in advance, this term can be reduced to _O_ ( _Bnd_ ) . For the contrastive
term, the cost of the subgraph pooling in Eq. (183) is _O_ ( _Bnd_ ), and the cost of the in-batch NCE
similarity matrix is _O_ ( _B_ [2] _d_ ) ; the size term has cost _O_ ( _Bn_ ) ; the connectivity term needs to traverse
edges and has cost _O_ ( _Bm_ ). Therefore, the additional complexity of the selector during training is


_O_ � _Bnd_ [2] + _Bnd_ + _B_ [2] _d_ + _Bm_ � _,_ (188)


and if the quadratic term of the linear projection is ignored or cached, it can be approximated as


_O_ � _Bnd_ + _B_ [2] _d_ + _Bm_ � _._ (189)


During inference, if only the selector logit is used to fuse entity scores, without computing NCE, size,
and connectivity regularizers, then the additional cost is mainly _O_ ( _Bnd_ [2] + _Bnd_ ), or _O_ ( _Bnd_ ) under
caching/lightweight projection.


**J** **Training and Inference Complexity**


For ease of exposition, suppose that the graph _G_ = ( _V, E_ ) has _n_ = _|V|_ entity nodes and _m_ = _|E|_
entity-relation edges. If self-loops are added in GCN propagation, we denote ˜ _m_ = _m_ + _n_ . Let the
hidden dimension be _d_, the number of propagation layers be _L_, the batch size be _B_, and the number
of pseudo-queries be _M_ . Therefore, one real query together with _M_ pseudo-queries requires _M_ + 1
graph reads. Let **M** _∈{_ 0 _,_ 1 _}_ _[n][×][N]_ _[D]_ denote the sparse entity–document association matrix, where _N_ _D_
is the number of documents, and nnz( **M** ) is the number of nonzero entity–document links. Let _K_ _e_
denote the number of top entities used for document projection, and let _f_ [¯] denote the average number
of documents linked to the top entities.


**J.1** **Offline Structural Feature and Indexing Cost**


Let the dimension of node structural features be _p_ _n_, the dimension of edge structural features be _p_ _e_,
and the dimension of graph-level summaries be _p_ _g_ . In the current implementation, _p_ _n_, _p_ _e_, and _p_ _g_ are
all small constants.


Given that the adjacency list has been constructed, degrees and average neighbor degrees can be
computed in _O_ ( _n_ + _m_ ) time. Clustering coefficients and the number of common neighbors require
computing intersections of neighbor sets, whose complexity can be written as



� min _{_ deg( _u_ ) _,_ deg( _v_ ) _}_

( _u,v_ ) _∈E_







_._ (190)




_O_







_n_ + _m_ +
�
 ( _u,v_ )



In sparse graphs or graphs with bounded average degree, Eq. (190) is approximately _O_ ( _n_ + _m_ ) ;
in extremely dense graphs, the worst case can reach _O_ ( _n_ [3] ) . These structural features and the
entity–document matrix can both be precomputed and cached offline, with space cost


_O_ ( _np_ _n_ + _mp_ _e_ + _p_ _g_ + nnz( **M** )) _._ (191)


Since this part does not depend on a specific query, when evaluating multiple queries on the same
candidate graph in the self-evolving memory loop, the same set of structural features and entity–
document indices can be reused.


40


**J.2** **Forward Propagation Complexity of the Structurally Gated GFM**


We first consider a single forward propagation for one query on one graph. A standard GCN layer
contains two parts: node linear transformation and sparse adjacency aggregation. The cost of node
linear transformation is _O_ ( _nd_ [2] ), and the cost of edge-level message aggregation is _O_ ( ˜ _md_ ) . Therefore,
the complexity of a standard GCN layer is


_C_ plain = _O_ � _nd_ [2] + ˜ _md_ � _._ (192)


Beyond ordinary message propagation, a structurally gated layer generates a vector gate for each
edge. Its message form is
**m** _u→v_ = _≫_ _uv_ _⊙W_ **h** _u_ _,_ (193)


where **h** _u_ is the source node representation, _W ∈_ R _[d][×][d]_ is the node linear transformation matrix,
_≫_ _uv_ _∈_ R _[d]_ is the structural gate vector of edge ( _u, v_ ), and _⊙_ denotes element-wise multiplication.
Let _d_ _g_ denote the encoding dimension of structural features, and let _h_ _g_ denote the hidden dimension
of the gating MLP. If the gate uses four types of inputs, namely source-node structure, target-node
structure, edge-pair structure, and graph-level summary, then the gate generation cost can be written

as

_C_ gate = _O_ _np_ _n_ _d_ _g_ + _mp_ _e_ _d_ _g_ + _p_ _g_ _d_ _g_
�

(194)
+ _m_ (4 _d_ _g_ _h_ _g_ + _h_ _g_ _d_ ) _._
�


Here, _np_ _n_ _d_ _g_ comes from node structural feature encoding, _mp_ _e_ _d_ _g_ comes from edge structural feature
encoding, _p_ _g_ _d_ _g_ comes from graph-level summary encoding, and _m_ (4 _d_ _g_ _h_ _g_ + _h_ _g_ _d_ ) comes from the
per-edge gating MLP. If edge-pair features or graph-level summaries are disabled, the corresponding
terms in Eq. (194) can be removed. If _d_ _g_ and _h_ _g_ are regarded as being of the same order as _d_, then
gate generation is _O_ ( _md_ [2] ) in the worst case; if the gating MLP is regarded as a small constantwidth module, or if low-rank/dimension-wise gating is adopted, it can be approximated as _O_ ( _md_ ) .
Therefore, the complexity of a structurally gated layer is


_C_ gated = _O_ � _nd_ [2] + ˜ _md_ + _C_ gate � _._ (195)


The current implementation supports dual structural prompts: one is a holistic gated branch, and
the other is a specific prompt branch. If only a standard GCN is used, the per-layer cost is _C_ plain ;
if only a structurally gated GCN is used, the per-layer cost is _C_ gated ; if one gated branch and one
standard branch are used simultaneously, the per-layer cost is approximately _C_ gated + _C_ plain . Let
_ρ_ plain _∈{_ 0 _,_ 1 _}_ denote whether the standard prompt branch is enabled, and let _ρ_ gated _∈{_ 0 _,_ 1 _}_ denote
whether the structurally gated branch is enabled. Then the GFM encoding cost for one batch can be
uniformly written as


_C_ enc ( _B_ ) = _O_ ( _BL_ ( _ρ_ plain _C_ plain + _ρ_ gated _C_ gated )) _._ (196)


The factor _B_ appears because, in the current implementation, each query in a batch separately
constructs query-conditioned node inputs and performs graph encoding. If query-independent
structural gates for a fixed graph are cached during inference, part of the gate cost can be reduced;
however, based on the current code implementation, Eq. (196) is a more conservative upper bound.


In the most common simplified analysis, we set _B_ = 1, _M_ = 0, disable dual branches, and regard
the gating MLP as a lightweight constant-width module. Then Eq. (196) degenerates to


_O_ � _L_ ( _md_ + _d_ [2] _n_ )� _,_ (197)


which is exactly the core propagation complexity given in the main text. Here, _md_ corresponds to
edge-level messages, structural gating, and sparse aggregation, while _d_ [2] _n_ corresponds to node linear
projection.


**J.3** **Entity Scoring, Selector Regularization, and Document Projection Complexity**


After GFM encoding obtains node representations, entity scoring is usually obtained by


_a_ _e_ ( _q_ ) = **h** _[⊤]_ _e_ **[z]** _[q]_ (198)


41


For one batch, the complexity of this step is
_C_ score ( _B_ ) = _O_ ( _Bnd_ ) _._ (199)

If the query-conditioned subgraph selector in Appendix I is enabled, then the additional inferencestage cost is
_C_ sel _,_ infer ( _B_ ) = _O_ ( _Bnd_ [2] + _Bnd_ ) _,_ (200)
which can be approximated as _O_ ( _Bnd_ ) if the node-side projection is cached or a lightweight
projection is used. During training, NCE, the size term, and the connectivity term also need to be
computed, with additional complexity
_C_ sel _,_ train ( _B_ ) = _O_ ( _Bnd_ [2] + _Bnd_ + _B_ [2] _d_ + _Bm_ ) _._ (201)

Here, _B_ [2] _d_ comes from the in-batch query–subgraph contrastive matrix, and _Bm_ comes from the
edge-level connectivity smoothing term.


Entity-to-document projection is performed by the entity–document matrix **M** . If full sparse matrix
multiplication is used, the complexity is
_C_ doc _,_ full ( _B_ ) = _O_ ( _B_ nnz( **M** )) _._ (202)

The `IDFWeightedRanker` in the current code belongs to this type: it first constructs IDF weights
according to entity occurrence frequency, and then performs sparse matrix multiplication. If top- _K_ _e_
entity projection is used, conceptually only the inverted lists corresponding to these entities need to
be accessed, so the complexity can be written as
_C_ doc _,_ top _K_ ( _B_ ) = _O_ � _Bn_ log _K_ _e_ + _BK_ _e_ _f_ [¯] � _,_ (203)

where _Bn_ log _K_ _e_ comes from top- _K_ _e_ entity selection, and _BK_ _e_ _f_ [¯] comes from accessing the documents linked on average by the top entities. If the final document top- _K_ ranking is performed over
all _N_ _D_ documents, the complexity is _O_ ( _BN_ _D_ log _K_ ) ; if it is performed only over the candidate
document pool, it is _O_ ( _BN_ cand log _K_ ), where _N_ cand _≪_ _N_ _D_ .


**J.4** **Training Complexity**


The main costs in the training stage come from GFM forward propagation, the entity-level retrieval
loss, the optional selector regularizer, and backpropagation. Let _κ_ bw denote the constant-factor cost
of backpropagation relative to forward propagation, which can usually be regarded as a constant
between 2 and 3 . If the entity-level training loss is BCE, ranking loss, or ListCE, then because the
predicted scores of _n_ entities need to be supervised or ranked, the loss computation complexity is
_C_ loss ( _B_ ) = _O_ ( _Bn_ ) _._ (204)

Therefore, when the selector is not enabled, the complexity of a single training batch is
_C_ train = _O_ ( _κ_ bw [ _C_ enc ( _B_ ) + _C_ score ( _B_ ) + _C_ loss ( _B_ )]) _._ (205)

After enabling the query-conditioned subgraph selector, the training complexity becomes

_C_ train [sel] [=] _[ O]_ [ (] _[κ]_ [bw] [[] _[C]_ [enc] [(] _[B]_ [) +] _[ C]_ [score] [(] _[B]_ [) +] _[ C]_ [loss] [(] _[B]_ [) +] _[ C]_ [sel] _[,]_ [train] [(] _[B]_ [)])] _[ .]_ (206)

If a document-level loss is also explicitly added during training, then entity-to-document projection
needs to be additionally performed, with cost _C_ doc _,_ full ( _B_ ) or _C_ doc _,_ top _K_ ( _B_ ).


**J.5** **Inference Complexity**


The inference stage first performs query encoding, named entity recognition, and entity linking,
whose total cost is denoted as _C_ prep ( _q_ ) . This part depends on the adopted text encoder, NER model,
and entity linking model, and does not belong to the graph propagation backbone. Given the prepared
query embedding and query entity mask, the core reading complexity of a single query is


_C_ infer ( _q_ ) =( _M_ + 1) _C_ enc (1) + _C_ score (1) + _C_ sel _,_ infer (1) + _C_ doc (1)
� � (207)

+ _C_ fuse ( _M, K_ ) _,_


where _M_ is the number of pseudo-queries, _C_ doc (1) can take the complexity of full sparse projection
or top- _K_ _e_ inverted projection, and _C_ fuse ( _M, K_ ) is the cost of fusing the results from the main query
and pseudo-queries. If each query keeps _K_ candidate documents, then the cost of simple weighted
merging is
_C_ fuse ( _M, K_ ) = _O_ (( _M_ + 1) _K_ log(( _M_ + 1) _K_ )) _,_ (208)


42


**J.6** **Space Complexity**


The model parameter space mainly comes from the GFM backbone, structural prompts, the structurally gated MLP, selector projections, and text projection layers. If we only discuss graph- related
runtime space, offline graph storage requires


_O_ ( _n_ + _m_ + nnz( **M** ) + _np_ _n_ + _mp_ _e_ + _p_ _g_ ) _._ (209)


During training, node activations of each layer need to be saved, and the space complexity is on the
order of
_O_ ( _BLnd_ ) (210)
If structurally gated edge messages are fully materialized, they require _O_ ( _md_ ) GPU memory; the
current implementation adopts edge chunk streaming. Let the chunk size be _c_, then the peak memory
of gated messages can be reduced to
_O_ ( _cd_ ) _,_ (211)

where _c ≪_ _m_ . This is also one of the key engineering designs that makes the current implementation
suitable for large-graph reading. If `return_gate` is enabled and the gate vectors of all edges are
saved for visualization or interpretation, then the space will rise again to _O_ ( _md_ ) . If document scoring
materializes all _N_ _D_ document scores, it requires _O_ ( _BN_ _D_ ) space; if only a candidate document heap
is maintained, it can be reduced to _O_ ( _BK_ ) or _O_ ( _BK_ _e_ _f_ [¯] ).


**J.7** **Complexity Comparison with Related Work**


**Overall Comparison.** From the perspective of complexity, standard dense RAG has the lightest
online retrieval cost, but it is difficult to explicitly model cross-document relations; multi-step
RAG improves complex reasoning ability through multiple rounds of retrieval, but its cost grows
linearly with the number of LLM calls; GraphRAG-style methods shift a large amount of cost to
offline graph construction and summary generation; SubgraphRAG reduces online cost through
lightweight triple scoring, but its effectiveness depends on the candidate triple set and structural
distance features; GFM-RAG and our reader concentrate the main computation on one or a small
number of query-conditioned graph propagations. Therefore, when the self-evolving memory loop
needs to repeatedly evaluate the retrievability of different written graphs, the advantage of our design
lies in the following: each evaluation does not need to start multi-round LLM agentic search, but
instead quickly obtains differentiable or scoreable retrieval feedback through a fixed GFM reader,
structurally gated propagation, and sparse document projection. This allows the graph writing strategy
to perform high-frequency comparison and optimization over a large number of candidate memory
graphs.


**K** **Implementation Details of Structured Query Planning**


**K.1** **Detailed definitions of the notation and additional information**


In _P_ _ω_ ( _q_ ) = _E_ exp _, A, C_ rel _, C_ hard _, τ, {_ (˜ _q_ _m_ _, α_ _m_ _, t_ _m_ ) _}_ _[M]_ _m_ =1, _E_ exp acts as a direct anchor for memory
� �
(explicit entities); _A_ maps the brain’s multiple representational habits for the same concept (aliases);
_C_ rel simulates the relational network in semantic memory; _C_ hard serves as the spatiotemporal and
logical boundaries of episodic memory (such as hard constraints like time and location); _τ_ presets the
cognitive template of the target memory (answer type); and the pseudo-queries ˜ _q_ _m_ with confidence
_α_ _m_ and intent _t_ _m_ are analogous to the multiple exploratory recalls conducted in the human mind
(Simulated Recall).


**K.2** **Two-stage Planning: Extraction and Inference**


Natural-language questions often compress key retrieval cues into implicit relations, such as “the
birthplace of the author”, “the publication year of the only mystery novel of a certain work”, or “the
death date of the father”. If the original question is sent as a whole to the entity linker, the system can
easily hit only surface entities while missing bridge entities or answer-type constraints. Therefore,
the query planner is defined as a structured function


_P_ ( _q_ ) = � _E_ exp _, A, C_ rel _, C_ hard _, τ, {_ (˜ _q_ _m_ _, α_ _m_ ) _}_ _[M]_ _m_ =1 � _._ (212)


43


**Extractor prompt template.**

```
 You are a retrieval planner for graph-based multi-hop QA.
 Question:
 {QUESTION}

 Extract structured retrieval signals.
 Return JSON only with keys:
 {
  "explicit_entities": [string],
  "candidate_aliases": {"entity": [alias]},
  "relation_clues": [string],
  "constraints": {},
  "answer_type": "string"
 }
 Rules: keep entries short, avoid explanations, keep empty fields as [] or {}.

```

Figure 6: Metadata of the case study from `HotpotQA` .
**Inferer prompt template.**

```
 You are a retrieval planner for graph-based multi-hop QA.
 Question:
 {QUESTION}

 Structured extraction:
 {EXTRACTOR_JSON}

 Generate at most M retrieval intents that help locate:
 - evidence directly supporting the target relation;
 - bridge entities required for multi-hop reasoning;
 - documents likely to contain the target attribute;
 - evidence satisfying temporal, spatial, type, comparison or negation constraints;
 - evidence using aliases or alternative mentions.
 Return JSON only with keys:
 {
  "pseudo_queries": [string],
  "rewriter_confidence": [number]
 }

```

Figure 7: Metadata of the case study from `HotpotQA` .


It consists of two stages: _Extractor_ 6 extracts explicit entities, aliases, relation clues, hard constraints,
and the answer type; _Inferer_ 7 generates at most _M_ retrieval intents based on the extraction results.


**L** **Computation Details of Topological Structural Features**


**L.1** **Normalized Structural Graph**


Structural features are computed on an undirected, self-loop-free, binarized adjacency matrix _A_ _s_ :


_A_ _s_ = I[( _A_ + _A_ _[⊤]_ ) _>_ 0] _,_ diag( _A_ _s_ ) = 0 _._ (213)


This avoids drastic fluctuations in topological statistics caused by unstable relation-extraction directions. Message propagation can still use the original bidirectional edges or relation-aware graph;
structural statistics are only used as gating conditions.


**L.2** **Node-level Structural Features**


For node _v_, let _N_ ( _v_ ) = _{u_ : _A_ _s,uv_ = 1 _}_ and _d_ _v_ = _|N_ ( _v_ ) _|_ . The node-level features are


_ϕ_ ( _v_ ) = � log(1 + _d_ _v_ ) _, c_ _v_ _, κ_ _v_ _,_ _d_ [¯] _N_ ( _v_ ) � _._ (214)


The local clustering coefficient is



_c_ _v_ =










_d_ _v_ ( _d_ 2 _v_ _T −_ _v_ 1) _[,]_ _d_ _v_ _≥_ 2 _,_



_d_ _v_ ( _d_ _v_ _−_ 1) (215)

0 _,_ _d_ _v_ _<_ 2 _,_



44


where _T_ _v_ is the number of undirected edges inside the neighborhood of _v_ ; _κ_ _v_ is the core number; and
the average neighbor degree is



_d_ ¯ _N_ ( _v_ ) =










1

_d_ _v_



_d_ _v_ _u_ _v_ (216)

0 _,_ _d_ _v_ = 0 _._



�



_u∈N_ ( _v_ ) _[d]_ _[u]_ _[,]_ _d_ _v_ _>_ 0 _,_



These quantities respectively characterize node frequency, local clustering, core/peripheral position,
and neighborhood density. For RAG memory, they correspond to four common structural risks:
over-propagation by high-frequency hubs, redundant diffusion inside clustered regions, ignored
peripheral bridge entities, and scale mismatch between sparse and dense regions.


**L.3** **Edge-pair Structural Features**


For an undirected structural edge ( _u, v_ ), the pairwise features are

_ψ_ ( _u, v_ ) = � _|d_ _u_ _−_ _d_ _v_ _|,_ CN( _u, v_ ) _,_ Jac( _u, v_ )� _,_ (217)


where

_|N_ ( _u_ ) _∩N_ ( _v_ ) _|_
CN( _u, v_ ) = _|N_ ( _u_ ) _∩N_ ( _v_ ) _|,_ Jac( _u, v_ ) = (218)
_|N_ ( _u_ ) _∪N_ ( _v_ ) _|_ + _ε_ _[.]_

Degree difference reflects cross-level connections, while common neighbors and Jaccard reflect local
community overlap. Based on these features, the gate can distinguish intra-community evidence
aggregation edges from cross-community bridge edges.


**L.4** **Graph-level Summary and Normalization**


The graph-level summary concatenates the mean, standard deviation, and density of node features:

**r** _G_ = � mean _v∈V_ _ϕ_ ( _v_ ); std _v∈V_ _ϕ_ ( _v_ ); dens( _G_ )� _,_ (219)


where



dens( _G_ ) =










2 _m_ _s_ _n ≥_ 2 _,_
_n_ ( _n −_ 1) _[,]_



_n_ ( _n −_ 1) (220)

0 _,_ _n <_ 2 _,_



_n_ = _|V|_, and _m_ _s_ is the number of undirected structural edges. To remove graph-size differences,
node and edge features are z-scored within each graph, and the graph-level summary computes global
mean and standard deviation over the set of training graphs:

¯ **r** _G_ = **[r]** _σ_ _[G]_ _r_ _[ −]_ + _[µ]_ _ε_ _[r]_ _[.]_ (221)


If the standard deviation of a certain dimension is close to zero, we only perform centering to avoid
division by an unstable small value.


**L.5** **Gating Input Encoding**


For each message edge _u →_ _v_, the structural gate reads the source node, target node, pairwise
features, and graph-level summary:

¯ ¯
_ϕ_ ( _u_ ) = NormNode( _ϕ_ ( _u_ )) _,_ _ψ_ ( _u, v_ ) = NormPair( _ψ_ ( _u, v_ )) _,_ (222)

_u_ [(] _u_ _[l]_ [)] [=] _[ E]_ _n_ [(] _[l]_ [)] [(¯] _[ϕ]_ [(] _[u]_ [))] _[,]_ _u_ [(] _v_ _[l]_ [)] = _E_ _n_ [(] _[l]_ [)] [(¯] _[ϕ]_ [(] _[v]_ [))] _[,]_ (223)

_v_ _uv_ [(] _[l]_ [)] [=] _[ E]_ _p_ [(] _[l]_ [)] [( ¯] _[ψ]_ [(] _[u, v]_ [))] _[,]_ _r_ _G_ [(] _[l]_ [)] [=] _[ E]_ _g_ [(] _[l]_ [)] [(¯] **[r]** _[G]_ [)] _[.]_ (224)

The encoders _E_ _n_ _, E_ _p_ _, E_ _g_ are all two-layer MLPs. The concatenated gating input is

**z** [(] _uv_ _[l]_ [)] [= [] **[u]** [(] _u_ _[l]_ [)] [;] **[ u]** [(] _v_ _[l]_ [)] [;] **[ v]** _uv_ [(] _[l]_ [)] [;] **[ r]** [(] _G_ _[l]_ [)] []] _[.]_ (225)


The gate itself is a vector rather than a scalar:

**g** _uv_ [(] _[l]_ [)] [=] **[ 1]** [ +] _[ δ]_ [ tanh] � MLP [(] _g_ _[l]_ [)] [(] **[z]** [(] _uv_ _[l]_ [)] [)] � _,_ _δ_ = 0 _._ 1 _._ (226)

The last layer of the gating MLP is initialized to zero, so initially **g** _uv_ [(] _[l]_ [)] [=] **[ 1]** [. At the beginning]
of training, the model does not destroy the original propagation scale; the learned structural bias
gradually emerges in a residual manner.


45


**L.6** **Message Propagation with Normalized Weights**


Let E [˜] be the edge set after adding self-loops. Structural gates are used for non-self-loop edges, and
unit gates are used for self-loops. The GCN normalization coefficient is


_w_ _uv_ ˜
_η_ _uv_ = ˜ _,_ _d_ _v_ = � _w_ _uv_ _,_ (227)
~~�~~ _d_ _u_ ˜ _d_ _v_ _u_ :( _u,v_ ) _∈_ E [˜]


where _w_ _uv_ defaults to 1, but can also come from edge weights. The propagation at layer _l_ is


**m** [(] _u_ _[l]_ _→_ [)] _v_ [=] _[ η]_ _[uv]_ **[g]** _uv_ [(] _[l]_ [)] _[⊙]_ _[W]_ [ (] _[l]_ [)] **[h]** [(] _u_ _[l][−]_ [1)] _,_ (228)



� **m** [(] _u_ _[l]_ _→_ [)] _v_

_u_ :( _u,v_ ) _∈_ E [˜]



**h** [(] _v_ _[l]_ [)] = _σ_







**b** [(] _[l]_ [)] +
�
 _u_ :( _u,v_ )



 _._ (229)





The multi-layer wrapper also contains inter-layer residuals: when _l >_ 1 and the dimensions are
consistent,
**H** [(] _[l]_ [)] _←_ **H** [(] _[l]_ [)] + **H** [(] _[l][−]_ [1)] _._ (230)


This residual and Eq. (226) form a dual stability mechanism: the former stabilizes deep propagation,
while the latter stabilizes structural modulation.


**L.7** **Chunked Gating and GPU Memory Complexity**


Explicitly storing all gates requires _O_ ( _|_ E _|d_ ) GPU memory. For large graphs, gates are computed by
edge chunks:



E =


Each edge chunk sequentially executes



_B_ _e_
� E _b_ _,_ _|_ E _b_ _| ≤_ _C_ _e_ _._ (231)


_b_ =1



**g** _b_ _→_ **m** _b_ _→_ scatter_add( **m** _b_ ) _,_ (232)


and immediately releases the intermediate gate tensor. Online GPU memory is reduced from _O_ ( _|_ E _|d_ )
to _O_ ( _C_ _e_ _d_ ), while the time complexity remains linear, _O_ ( _|_ E _|d_ ) . This is especially important for selfevolving memory, because the same reader needs to repeatedly evaluate candidate graphs produced
by different writers.


**M** **Pretraining Objective and Augmented Views**


**M.1** **GraphCL View Construction**


The goal of the pretraining stage is to learn cross-graph transferable structural–semantic propagation,
rather than fitting specific question-answering labels. Given the original graph view ( _G_ 0 _, X_ 0 ), we
construct two augmented views ( _G_ 1 _, X_ 1 ), ( _G_ 2 _, X_ 2 ) and one negative feature view ( _G_ 0 _, X_ _[−]_ ) . The
augmentation types include edge perturbation, feature masking, node perturbation, and subgraph
sampling; let the augmentation operators be _A_ 1 _, A_ 2, then


( _G_ _j_ _, X_ _j_ ) = _A_ _j_ ( _G_ 0 _, X_ 0 ) _,_ _j ∈{_ 1 _,_ 2 _}._ (233)


If structural gating is enabled, each view precomputes its own node structural features, edge-pair
features, and graph-level summary; the negative feature view shares the base graph structure, but its
node features are shuffled or replaced.


**M.2** **Graph-level Contrastive Objective**


The encoder outputs four sets of node representations:


_H_ 0 = _f_ _θ_ ( _X_ 0 _, G_ 0 ) _,_ _H_ 1 = _f_ _θ_ ( _X_ 1 _, G_ 1 ) _,_ _H_ 2 = _f_ _θ_ ( _X_ 2 _, G_ 2 ) _,_ _H_ _[−]_ = _f_ _θ_ ( _X_ _[−]_ _, G_ 0 ) _._ (234)


46


The graph readout of each augmented view is



 _,_ _j ∈{_ 1 _,_ 2 _}._ (235)





_c_ _j_ = sigmoid







 _|V_ [1]



_|V_ _j_ _|_



� _H_ _j,v_

_v∈V_ _j_



The bilinear discriminator
_D_ ( _c, h_ ) = _h_ _[⊤]_ _W_ _D_ _c_ (236)
determines whether the node representation comes from the same graph semantics. The pretraining
loss is



_L_ GCL = [1]

2



2
� �BCE � _D_ ( _c_ _j_ _, H_ 0 ) _,_ **1** � + BCE � _D_ ( _c_ _j_ _, H_ _[−]_ ) _,_ **0** �� _._ (237)

_j_ =1



When edge-level gating is enabled, traditional static structural prompts are neutralized into identity
mappings to avoid scale confusion caused by two sets of structural modulations acting simultaneously;
the structural bias is mainly carried by the target edge’s **g** _uv_ [(] _[l]_ [)] [.]


**M.3** **Feature Alignment Layer**


When the input dimensions produced by different graphs or different text encoders are consistent but
their distributions have large shifts, the feature alignment layer can be enabled:
Align( _x_ ) = Dropout (LayerNorm (PReLU( _W_ _a_ _x_ + _b_ _a_ ))) _._ (238)

_W_ _a_ is initialized as the identity matrix, and _b_ _a_ is initialized as zero. Therefore, this layer is initially an
approximately identity transformation; after training, it absorbs inter-graph feature-scale differences
without changing the core structure of the graph propagator.


**N** **Supervised Fine-tuning Objective**


**N.1** **Entity-level Supervision**


For each question _q_ _b_, the data provide a supporting-entity mask _y_ _b,e_ _∈{_ 0 _,_ 1 _}_ . The model outputs
entity logits _a_ _b,e_ . The weighted BCE is defined as



_L_ bce = [1]

_B_



_B_
�


_b_ =1



� _e_ _[w]_ _[b][,][e]_ [ BCEWithLo][g][its][(] _[a]_ _[b][,][e]_ _[,]_ _[y]_ _[b]_ _[,][e]_ [)]

_._ (239)

~~�~~ _e_ _[w]_ _[b,e]_ [ +] _[ ε]_



Positive weights are uniformly normalized within the positive set; if the adversarial temperature _T_ _a_ is
enabled for negative weights, they are computed by applying softmax to the current model scores:

exp( _a_ _b,e_ _/T_ _a_ )
_w_ _b,e_ _[−]_ [=] ~~�~~ _v_ : _y_ _b,v_ =0 [exp(] _[a]_ _[b,v]_ _[/T]_ _[a]_ [)] _[,]_ _y_ _b,e_ = 0 _._ (240)


If _T_ _a_ = 0, the negative weights degenerate into a uniform distribution. This design makes training
focus more on high-scoring hard negatives, rather than being dominated by a large number of
obviously irrelevant entities.


**N.2** **Multi-positive List Cross-Entropy**


Using only BCE treats each entity as an independent binary classification problem, lacking the
constraint that “supporting entities should collectively rank near the top of the same candidate list”.
To this end, we introduce a multi-positive list loss. Let

_p_ _b,e_ = ~~�~~ _v_ [sigmoid(] sigmoid( _[a]_ _a_ _[b,v]_ _b,e_ ) [) +] _[ ε.]_ (241)

If sample _b_ has at least one supporting entity, the list loss is



1
_L_ list = _−_
_|B_ + _|_



�

_b∈B_ +



� log( _p_ _b,e_ + _ε_ ) _._ (242)

_e∈Y_ _E_ ( _q_ _b_ )



1

_|Y_ _E_ ( _q_ _b_ ) _|_



Samples with empty supporting-entity sets are skipped. The final entity fine-tuning objective is
_L_ ent = _λ_ bce _L_ bce + _λ_ list _L_ list _,_ ( _λ_ bce _, λ_ list ) = (0 _._ 3 _,_ 0 _._ 7) _._ (243)


47


**N.3** **Optional Document-level Supervision**


If the training configuration provides a document-level loss, entity logits are first projected into
document logits: ˜
_S_ _b_ = _a_ _[⊤]_ _b_ **[M]** _[,]_ (244)

and then the same type of BCE or list loss is computed with the supporting-document mask _z_ _b,i_ . This
term is suitable for tasks where entity annotations are noisy but the document support set is reliable;
if it is not enabled, training is entirely driven by the entity-level support set, and document ranking is
obtained through projection only during inference or validation.


**O** **Memory Writer Implementation Details**


**O.1** **The Markov Decision Process for Multi-turn Graph Construction**


Specifically, the training of our graph constructor is implemented through VeRL’s multi-turn GRPO
loop. The state machine of the interactor can be abstracted as a finite-horizon MDP:


_M_ = ( _S, A, P, R, ρ_ 0 _, H_ ) _._ (245)


Given a sample _x_, at round _t_, the state can be written as


_s_ _t_ = ( _q, G_ _t_ _, D_ _t_ [proc] _, D_ _t_ [rem] _, ζ_ _t_ ) _,_ (246)


where _G_ _t_ is the current partially written graph, _D_ _t_ [proc] and _D_ _t_ [rem] denote the processed and remaining
documents, respectively, and _ζ_ _t_ is an interaction control flag, such as whether the process is still in
the graph-construction stage or has already switched to the RAG stage. The action is generated by
the language model in JSON format:
_a_ _t_ _∼_ _π_ _θ_ ( _· | s_ _t_ ) _,_ (247)

and is restricted to two types of legal actions:


1. **Triple** **action** : output a JSON array, where each element is of the form
_{_ `subject` _,_ `relation` _,_ `object` _}_, representing the set of facts _T_ _t_ written in the current
round;

2. **Termination action** : after graph construction is completed, output a JSON object carrying the
terminal fields required by the reader side, such as `answer`, `recall`, `precision`, `deducible`,
and so on.


In implementation, the environment first checks whether the action can be parsed by `json_repair`,
and strictly cleans the triples: items with missing keys, empty strings, or non-dictionary entries are
all removed. If illegal JSON is output during the graph-construction stage, the interaction terminates
immediately and returns zero reward; if legal triples are output, the environment proceeds to the next
round and returns a round-level format reward. The corresponding environment transition can be
written as



_s_ _t_ +1 = _P_ ( _s_ _t_ _, a_ _t_ ) =



( _q, G_ _t_ _⊕T_ _t_ _, D_ _t_ [proc] _∪{d_ _t_ _}, D_ _t_ [rem] _\ {d_ _t_ _}, ζ_ _t_ +1 ) _,_ _a_ _t_ is legal _,_

( _q, G_ _t_ _, D_ _t_ [proc] _, D_ _t_ [rem] _,_ STOP) _,_ _a_ _t_ is illegal _,_



( _q, G_ _t_ _, D_ _t_ [proc] _, D_ _t_ [rem] _,_ RAG) _,_ _a_ _t_ triggers the reading stage _._

(248)



**Iterative and non-iterative writing.** Two strategies are supported. In the non-iterative mode, the
model reads the entire context _D_ at once and outputs all triples. In the iterative mode, the environment
reads the documents segment by segment in document order, and in each round the model is only
allowed to write triples for the current document. After all documents have been processed, the
environment then switches to the RAG stage. If _T_ _i_ denotes the set of triples output for document _d_ _i_,
then the final graph constructed in the iterative mode is _G_ = [�] _[m]_ _i_ =1 _[T]_ _[i]_ [, where] _[ ⊕]_ [denotes edge-set]
union and node deduplication. We adopt the iterative strategy by default, because it decomposes the
long-context problem into a sequence of local writing decisions, significantly reducing the difficulty
of performing global planning in advance. At the same time, it also allows the source document
of each triple to be precisely recorded, providing explicit source edges for subsequent text-graph
retrieval.


48


**Constructing text-graph memory from output triples.** To enable the frozen retriever to operate
under the **graph-guided text retrieval** setting, the environment does not directly pass the raw triple
strings to the retriever. Instead, it first constructs a text graph with document nodes:


_G_ = ( _V_ _e_ _∪V_ _d_ _, E_ _ee_ _∪E_ _ed_ ) _,_ (249)


where the entity node set _V_ _e_ comes from the subjects and objects in the triples, and the document
node set _V_ _d_ = _{d_ 1 _, . . ., d_ _m_ _}_ corresponds to the original documents in the context. The entity-entity
edges are defined as
_E_ _ee_ = _{_ ( _u, r, v_ ) _|_ ( _u, r, v_ ) _∈T },_ (250)

and the entity-document source edges are defined as


_E_ _ed_ = _{_ ( _u,_ `source` _, d_ _i_ ) _,_ ( _v,_ `source` _, d_ _i_ ) _|_ ( _u, r, v_ ) _∈T_ _i_ _}._ (251)


In the iterative mode, the source edges are explicit, because the environment already knows that the
triples in each round come from the current document. In the non-iterative mode, we use a heuristic
alignment method based on tokenizer token overlap to map each triple to the most similar document.
The significance of this design is that, after separating writing from reading, the graph constructor is
only responsible for deciding “what to write into memory”; as for how the reader aggregates entities
on the graph and retrieves documents, this is entirely determined by the frozen _f_ _ϕ_ .


**Frozen GFM retrieval environment.** When training the graph constructor, the reader _f_ _ϕ_ is fixed
as the already trained GFM retriever. Let the entity set be _V_ _e_ = _{e_ 1 _, . . ., e_ _n_ _}_ and the document set
be _V_ _d_ = _{d_ 1 _, . . ., d_ _M_ _}_ . We then construct:


1. the relation-edge index **E** with both forward and reverse directions, together with the relation
types **r** ;
2. the sparse entity-document matrix **M** _∈{_ 0 _,_ 1 _}_ _[n][×][M]_, where _M_ _ij_ = 1 if entity _e_ _i_ appears in
document _d_ _j_ ;
3. the question-related entity mask **m** _q_ _∈{_ 0 _,_ 1 _}_ _[n]_, which is obtained preferentially through lexical
matching with the question; if lexical matching fails, it falls back to a heuristic seed set ranked
by entity degree.


After encoding the question as a vector **q** and the relation names as a matrix **R**, the frozen GFM
forward pass computes the entity relevance scores:


**s** _e_ = _f_ _ϕ_ ( _G,_ **q** _,_ **m** _q_ ; _ϕ_ ) _∈_ R _[n]_ _._ (252)


The entity scores are then projected into document scores. Let **M** Top- _k_ ( **s** _e_ ) denote the masking
operation that retains only the top- _K_ entity scores, and let **w** idf denote the inverse-frequency weights
defined according to the document frequency of each entity. The four document-scoring modes can
be written uniformly as



˜ **s** _e_ =



 **sMw** _e_ idf _,_ Top _⊙_ - _k_ **s** ( _e_ **s** _,_ _e_ ) _,_ `idfrawtopk` _,,_ _,_

 **w** idf _⊙_ **M** Top- _k_ ( **s** _e_ ) _,_ `idf_topk` _,_



(253)



and the document scores are obtained by


**s** _d_ = **M** _[⊤]_ ˜ **s** _e_ _._ (254)


We then take Top- _k_ ( **s** _d_ ) as the retrieval result. In actual use, we also enable
`init_entities_weight`, that is, during the GFM forward pass, a 1 _/f_ ( _e_ ) weight is applied to
high-frequency entities to suppress the dominance of entities connected to too many documents in
the retrieval results.


**P** **Additional Detailed Experimental Results**


The results of retrieval performance on multi-hop QA benchmarks are in Table 9.


The results on AmazonQA are in Table 10.


The HaluMem results are shown in Table 11.


49


Table 9: Results of retrieval performance on multi-hop QA benchmarks. We report document-level
Recall (%) at top-2 and top-5. Best results are in **bold** and runner-ups are underlined . The darker the
cell, the better.


**Dataset** `HotpotQA` `MuSiQue` `2WikiMultiHopQA`
**Avg. Rank**
**Method** R@2 R@5 R@2 R@5 R@2 R@5

**SAGE (ours)** 65. 1 77. 6 43. 2 53. 1 83. 6 88. 6 7. 0


**P.1** **Path Interpretations**


We provide path interpretations of SAGE for multi-hop reasoning in Table 12. The importance of
each path to the final prediction can be measured by the partial derivative of the prediction score with
respect to the triples at each reasoning layer. The top- _k_ path interpretations are then obtained by
selecting the top- _k_ longest paths with beam search.


As shown in Table 12, SAGE successfully identifies the answer by connecting two key constraints
in the question: the person who presented the Australia 2022 FIFA World Cup bid and the person
born on October 22, 1930. Specifically, the first path starts from the entity “the bid for the 2022 FIFA
World Cup” and follows the inverse relation of “was one of the representatives of” to reach “Frank
Lowy”. Then, through an entity-equivalence relation, it links “Frank Lowy” to “Sir Frank P. Lowy”,
whose birth date is “22 October 1930”. The second path verifies the reasoning in the reverse direction
by starting from the birth date and tracing back to the representative of the World Cup bid. These
paths demonstrate that SAGE can effectively align different surface forms of the same entity and
integrate multiple question constraints within a single-step retrieval process, showing its ability to
perform interpretable multi-hop reasoning.


**Q** **Dataset Details**


Table 13 summarizes the details of each dataset.


**General and Multi-hop QA.** We first evaluate SAGE on a set of general open-domain and multihop QA benchmarks that stress different aspects of retrieval-augmented reasoning. `NQ-Open` is
derived from Natural Questions and is widely used as a standard open-domain short-answer QA
benchmark; it evaluates whether a system can retrieve and ground factual answers from a large
Wikipedia-scale corpus. `PopQA` complements NQ by focusing on entity-centric factual questions
whose subjects span different popularity levels, making it particularly useful for testing whether
a retrieval or memory system can recover long-tail factual knowledge rather than relying only on
parametric memorization. `HotpotQA` contains Wikipedia-based multi-hop questions with sentence

50


Table 10: Performance of representative baselines on the original `AmazonQA` full-test protocol. BLEU1/2/3/4 are denoted as B-1/2/3/4, and R denotes ROUGE. Best results are in **bold** and runner-ups are
underlined . **Only rows marked with** **[0-shot]** **are our zero-shot transfer results; baseline rows and**
**trained variants are not marked as zero-shot.**


**Zero-shot setting applies only to** `Ours` **rows marked with** **[0-shot]** **on** `AmazonQA` **.**

**Method** B-1 B-2 B-3 B-4 R

_Heuristic baselines from the original_ _`AmazonQA`_ _protocol_

_Neural baseline from the original_ _`AmazonQA`_ _protocol_
`R-Net` (� _IJCAI’19_ ) 47. 04 40. 32 31. 48 23. 92 40. 22

_Human answers under the original_ _`AmazonQA`_ _protocol_

_Our method_


Table 11: Results on `HaluMem-Medium` . We report memory extraction metrics, memory updating
metrics, and memory question-answering metrics. R denotes Recall, W-R denotes Weighted Recall,
T-P denotes Target Memory Precision, Acc. denotes Memory Accuracy, FMR denotes False Memory
Resistance, F1 denotes Memory Extraction F1-score, C denotes Correct Rate, H denotes Hallucination
Rate, and O denotes Omission Rate. For R, W-R, T-P, Acc., FMR, F1, and C, higher is better; for H
and O, lower is better. Best results are in **bold** and runner-ups are underlined . The darker the cell, the
better. For systems whose public reports only provide a subset of metrics, missing entries are denoted
by “–”. **Only rows marked with** **[0-shot]** **are our zero-shot results; baseline rows and trained SAGE**
**rows are not marked as zero-shot.**


**Zero-shot setting applies only to SAGE variants marked with** **[0-shot]** **on** `HaluMem-Medium` **.**

**Dataset** `Memory Extraction` `Memory Updating` `Memory QA`

**Method** R _↑_ W-R _↑_ T-P _↑_ Acc. _↑_ FMR _↑_ F1 _↑_ C _↑_ H _↓_ O _↓_ C _↑_ H _↓_ O _↓_

_Memory-system baselines from the original_ _`HaluMem`_ _benchmark_


level supporting facts, allowing us to evaluate not only answer correctness but also whether the
system can recover bridge evidence and produce interpretable reasoning chains. `2WikiMultiHopQA`
further stresses structured multi-hop reasoning by combining Wikipedia text with Wikidata-derived
relations and providing evidence paths for 2–4 hop questions. Finally, `MuSiQue` is designed to reduce
shortcut reasoning by composing connected single-hop questions into 2–4 hop questions, making it a
strong testbed for evaluating whether SAGE can retrieve and integrate multiple pieces of evidence in
a genuinely compositional manner.


**E-commerce Review-based QA.** We use `AmazonQA` to evaluate SAGE in a practical, noisy, usergenerated e-commerce setting. Unlike Wikipedia-style QA benchmarks, `AmazonQA` consists of
real product questions, community answers, product reviews, and product metadata, and includes
answerability annotations indicating whether a question can be answered from available reviews.
This makes it a suitable benchmark for testing whether a memory system can identify useful evidence
from noisy review collections, distinguish answerable from unanswerable questions, and synthesize
grounded answers from multiple user-generated snippets. From the perspective of self-evolving


51


Table 12: Path interpretations of SAMGPT for multi-hop reasoning, where _r_ _[−]_ [1] denotes the inverse
of original relation.






|Question|Which man who presented the Australia 2022 FIFA World Cup bid was born on October 22<br>1930?|
|---|---|
|**Answer**|Frank Lowy|
|**Sup. Doc.**|[ “Frank Lowy”, “Australia 2022 FIFA World Cup bid”]|
|**Paths**|1: (the bid for the 2022 ffa world cup, was one of the representatives of_−_1, frank lowy)<br>_→_(frank lowy, equivalent, sir frank p lowy)_ →_(sir frank p lowy, was born on, 22 october<br>1930)<br>2: (22 october 1930, was born on_−_1, sir frank p lowy)_ →_(sir frank p lowy, equivalent, frank<br>lowy)_ →_(frank lowy, was one of the representatives of, the bid for the 2022 ffa world cup)|



Table 13: Dataset statistics and evaluation scenarios. We evaluate SAGE on three complementary
categories: general and multi-hop QA, practical e-commerce review QA, and long-term agent
memory. “Train/Dev/Test” denotes the standard split when available. For benchmark-only datasets
without a conventional supervised training split, we report the total number of evaluation instances or
benchmark scale.


**Category** **Dataset** **Scale / Split** **Evidence Source** **Task Type** **Key Capabilities** **Main Metrics**



General /
Multi-hop QA



`NQ-Open` (�; �) 79,168 / 8,757 / 3,610 English Wikipedia Open-domain short-answer Factual retrieval; entity-level
QA knowledge access; opendomain answer generation



`PopQA` (�) 14,267 QA pairs Wikidata triples +
Wikipedia page-view
popularity


`HotpotQA` (�) 90,447 / 7,405 / 7,405 Wikipedia paragraphs;
10-paragraph distractor
setting



Entity-centric open-domain Long-tail factual recall; paraQA metric vs. non-parametric memory; retrieval under entity popularity shift

Explainable 2-hop QA Bridge-entity recovery; comparison reasoning; sentence-level
supporting facts



`2WikiMultiHopQA` (�) 167,454 / 12,576 / Wikipedia + Wikidata; 2–4 hop multi-hop QA Reasoning-path recovery; com12,576 10 passages per instance parison, bridge, and bridgecomparison reasoning

`MuSiQue` (�) 19,938 / 2,417 / 2,459 Composed single-hop 2–4 hop connected multi- Connected reasoning; shortcut(24,814 total) QA over textual passages hop QA resistant evidence aggregation;
multi-hop compositionality



E-commerce
Review QA `AmazonQA` (�) 923K questions; 3.6M answers; 14M reviews;
156K products


Long-term `LongMemEval` (�) 500 eval. instances per
Agent Memory file; `S` : _∼_ 115K tokens
/ 30–40 sessions; `M` :
_∼_ 1.5M tokens / _∼_ 500
sessions; `Oracle` : evidence sessions only

`HaluMem` (�) `Medium` : 20 users,
30,073 dialogue
rounds, _∼_ 160K tokens/user, 14,948 memory
points, 3,467 QA pairs;
`Long` : 53,516 rounds,
_∼_ 1M tokens/user



Amazon product reviews,
questions, answers, and
product metadata



Review-based QA with an- Noisy review retrieval; answerswerability annotation able / unanswerable detection;
evidence synthesis from usergenerated reviews



Long multi-session Long-term interactive mem- Information extraction; multihuman–AI chat histories ory QA session reasoning; temporal reasoning; knowledge update; abstention



Synthetic long-term
human–AI interaction
histories with memory
points and multi-type
questions



Operation-level memory Memory extraction; memory
hallucination benchmark updating; memory QA; hallucination, omission, and conflict
propagation across memory operations



EM / F1 / Acc.; Recall@k


Acc. / EM; long-tail
breakdown


Answer EM/F1; Support
EM/F1; Joint EM/F1


Answer EM/F1; Evidence / path recall


Answer EM/F1; Support
/ evidence recall


BLEU / ROUGE; answerability Acc./F1; groundedness


Overall Acc.; categorywise Acc.; context tokens; latency


Extraction R/P/F1; Updating C/H/O; QA C/H/O



memory, AmazonQA is especially valuable because the system must learn which review facts, product
attributes, and user opinions are worth indexing for future retrieval, rather than simply matching a
question to a clean encyclopedic passage.


**Long-term Agent Memory.** To move beyond conventional RAG evaluation, we further evaluate
SAGE on long-term agent memory benchmarks. `LongMemEval` is designed to assess the longterm memory abilities of chat assistants over extended multi-session interaction histories. It covers
five core memory abilities: information extraction, multi-session reasoning, temporal reasoning,
knowledge updates, and abstention. This benchmark directly tests whether SAGE can retrieve sparse
but relevant memory traces from long histories, combine evidence across sessions, respect temporal
order, and update previously stored information when new interactions supersede old memories.
We use `HaluMem` as a complementary benchmark for evaluating hallucination in memory systems.
Rather than only measuring end-to-end QA accuracy, HaluMem decomposes memory evaluation into
memory extraction, memory updating, and memory question answering, thereby revealing at which
operational stage hallucinations, omissions, or conflicts arise. This is particularly important for our
setting because errors introduced during graph construction or memory updating may propagate to
graph-guided retrieval and final answer generation.


52


**Evaluation Rationale.** Together, these datasets form a progressively broader evaluation suite.
NQ and PopQA test factual open-domain retrieval; HotpotQA, 2WikiMultiHopQA, and MuSiQue
test multi-hop evidence composition; AmazonQA evaluates noisy real-world review memory in an
e-commerce domain; LongMemEval tests long-horizon interactive memory; and HaluMem diagnoses
operation-level hallucinations in memory systems. This combination allows us to evaluate SAGE not
merely as a retrieval-augmented QA pipeline, but as a self-evolving memory system that must decide
what to store, how to organize stored information, how to retrieve it under different query conditions,
and how to update or suppress unreliable memories over time.


**R** **Baselines and Metrics**


**Baselines.** We evaluate SAGE against state-of-the-art baselines, including their combined variants,
which are grouped into **four** categories:


- _**Base LLM:**_ `GPT-4o-mini` Hurst et al. [2024].


- _**Single-step RAGs:**_ including `BM25` Robertson and Walker [1994], `Contriever` Izacard et al.

[2021], `GTR` Ni et al. [2022], `ColBERTv2` Santhanam et al. [2022], `RAPTOR` Sarthi et al. [2024], and
`Proposition` Chen et al. [2024].


- _**Graph-enhanced RAGs:**_ including `GraphRAG` Edge et al. [2024], `G-Retriever` He et al. [2024],
`LightRAG` Guo et al. [2024], `HippoRAG` Gutiérrez et al. [2024], `HippoRAG 2` Gutiérrez et al.

[2024], `SubgraphRAG` Li et al. [2024], `PropRAG` Wang and Han [2025], and the closely related
`GFM-RAG` Luo et al. [2025].


- _**Multi-step RAGs:**_ `IRCoT` Trivedi et al. [2023], `FLARE` Jiang et al. [2023], and `Adaptive-RAG` Jeong
et al. [2024].


In particular, `IRCoT` Trivedi et al. [2023] is a general multi-step reasoning framework that can be
integrated with non-iterative retrievers, allowing both single-step RAG and graph-based methods
to conduct multi-hop reasoning through interleaved retrieval and generation. Table **??** presents a
comprehensive comparison between all baselines and SAGE.


**Metrics.** To evaluate retrieval quality, we report Recall@2 and Recall@5 for both retrieved entities
and documents, denoted as R@2/5 E and R@2/5 D, respectively.. For end-to-end QA evaluation, we
use standard metrics, including Exact Match (EM), F1 score, Precision (P), and Recall (R), in the
main experiments to comprehensively measure answer correctness and coverage.


**Limitations**


SAGE treats graph memory as a dynamic substrate for writing, reading, and self-evolution, but its
effectiveness still depends on the quality of entity extraction, relation writing, source anchoring, and
reader feedback. Errors introduced during graph construction may propagate to retrieval and final
answer generation, especially in long-term memory settings involving temporal updates, conflicting
user preferences, or sparse evidence. Our experiments show promising results across multi-hop
QA, open-domain retrieval, review-based QA, and long-term agent-memory benchmarks, but the
current system still leaves room for improvement on memory updating, high-coverage extraction,
and hallucination control in more realistic deployments. The theoretical analysis also relies on
assumptions such as bounded graph drift, aggregate signal propagation, and local Lipschitz stability,
which provide useful intuition but may not capture all failure modes of large-scale, noisy, continuously
evolving memory graphs.


**Broader Impact**


This work may have positive societal impact by improving the reliability and grounding of longhorizon language agents. A structure-aware and self-evolving memory system can help agents
recover evidence chains from fragmented cues, maintain more consistent long-term interactions,
and reduce unsupported answers in applications such as knowledge assistance, research support,
customer support, and review-based question answering. At the same time, long-term agent memory


53


raises important risks. If deployed on personal or sensitive interaction histories, such systems
may store private information, infer user preferences, preserve outdated or incorrect memories,
or enable profiling and surveillance. Incorrect graph writes or retrieval failures may also lead to
confidently grounded but wrong answers. Practical deployments should therefore use consent-based
data collection, data minimization, access control, deletion and forgetting mechanisms, provenance
tracking, auditing, and human oversight for high-stakes use cases.


**Compute Resources**


All experiments were run on a server equipped with 8 NVIDIA A100 GPUs. The main computational
cost of SAGE comes from graph-memory construction, GFM-based graph propagation, selector
regularization, and entity-to-document projection. Appendix J analyzes the training and inference
complexity in terms of the number of graph nodes _n_, edges _m_, hidden dimension _d_, propagation layers
_L_, batch size _B_, pseudo-queries _M_, and entity-document links. In our implementation, structural
features and entity-document indices can be precomputed and cached, while edge-level gates are
computed in chunks to reduce peak GPU memory from _O_ ( _|E|d_ ) to _O_ ( _C_ _e_ _d_ ) for chunk size _C_ _e_ .
The dominant inference cost is one or a small number of query-conditioned graph propagations
followed by sparse document projection, making the reader suitable for repeated evaluation inside
the self-evolving writer–reader loop.


**Licenses and Existing Assets**


This paper uses existing public benchmarks and baselines, including NQ-Open, PopQA, HotpotQA, 2WikiMultiHopQA, MuSiQue, AmazonQA, LongMemEval, HaluMem, BM25, Contriever,
GTR, ColBERTv2, RAPTOR, GraphRAG, G-Retriever, LightRAG, HippoRAG, HippoRAG 2, SubgraphRAG, PropRAG, GFM-RAG, IRCoT, FLARE, and Adaptive-RAG. We cite the original papers
or repositories for these assets and use them only for research evaluation under their stated licenses
and terms of use. We do not redistribute modified versions of the datasets beyond the preprocessing
scripts and instructions needed for reproducibility. The released code is intended for research use and
includes documentation for environment setup, data preparation, training, and evaluation.


54


**NeurIPS Paper Checklist**


The checklist is designed to encourage best practices for responsible machine learning research,
addressing issues of reproducibility, transparency, research ethics, and societal impact. Do not remove
the checklist: **The papers not including the checklist will be desk rejected.** The checklist should
follow the references and follow the (optional) supplemental material. The checklist does NOT count
towards the page limit.


Please read the checklist guidelines carefully for information on how to answer these questions. For
each question in the checklist:


    - You should answer [Yes], [No], or [N/A].


    - [N/A] means either that the question is Not Applicable for that particular paper or the
relevant information is Not Available.


    - Please provide a short (1–2 sentence) justification right after your answer (even for [N/A]).


**The checklist answers are an integral part of your paper submission.** They are visible to the
reviewers, area chairs, senior area chairs, and ethics reviewers. You will also be asked to include it
(after eventual revisions) with the final version of your paper, and its final version will be published
with the paper.


The reviewers of your paper will be asked to use the checklist as one of the factors in their evaluation.
While [Yes] is generally preferable to [No], it is perfectly acceptable to answer [No] provided a
proper justification is given (e.g., error bars are not reported because it would be too computationally
expensive” or “we were unable to find the license for the dataset we used”). In general, answering

[No] or [N/A] is not grounds for rejection. While the questions are phrased in a binary way, we
acknowledge that the true answer is often more nuanced, so please just use your best judgment and
write a justification to elaborate. All supporting evidence can appear either in the main paper or the
supplemental material, provided in appendix. If you answer [Yes] to a question, in the justification
please point to the section(s) where related material for the question can be found.


IMPORTANT, please:


    **Delete this instruction block, but keep the section heading “NeurIPS Paper Checklist"**,


    - **Keep the checklist subsection headings, questions/answers and guidelines below.**


    - **Do not modify the questions and only use the provided macros for your answers** .


1. **Claims**


Question: Do the main claims made in the abstract and introduction accurately reflect the
paper’s contributions and scope?


Answer: [Yes]


Justification: The abstract and introduction state the scope of SAGE as a self-evolving agentic
graph-memory engine for long-term memory, structure-aware retrieval, and evidence-chain
recovery. The theoretical results and experiments across multi-hop QA, open-domain
retrieval, review-based QA, and long-term agent-memory benchmarks support the stated
contributions.


Guidelines:


       - The answer [N/A] means that the abstract and introduction do not include the claims
made in the paper.

       - The abstract and/or introduction should clearly state the claims made, including the
contributions made in the paper and important assumptions and limitations. A [No] or

[N/A] answer to this question will not be perceived well by the reviewers.

       - The claims made should match theoretical and experimental results, and reflect how
much the results can be expected to generalize to other settings.

       - It is fine to include aspirational goals as motivation as long as it is clear that these goals
are not attained by the paper.


2. **Limitations**


55


Question: Does the paper discuss the limitations of the work performed by the authors?

Answer: [Yes]

Justification: The paper includes a limitations discussion covering the dependence on
graph-writing quality, memory updating, domain adaptation, hallucination control, and
assumptions used in the theoretical analysis.

Guidelines:


    - The answer [N/A] means that the paper has no limitation while the answer [No] means
that the paper has limitations, but those are not discussed in the paper.

   - The authors are encouraged to create a separate “Limitations” section in their paper.

    - The paper should point out any strong assumptions and how robust the results are to
violations of these assumptions (e.g., independence assumptions, noiseless settings,
model well-specification, asymptotic approximations only holding locally). The authors
should reflect on how these assumptions might be violated in practice and what the
implications would be.

    - The authors should reflect on the scope of the claims made, e.g., if the approach was
only tested on a few datasets or with a few runs. In general, empirical results often
depend on implicit assumptions, which should be articulated.

    - The authors should reflect on the factors that influence the performance of the approach.
For example, a facial recognition algorithm may perform poorly when image resolution
is low or images are taken in low lighting. Or a speech-to-text system might not be
used reliably to provide closed captions for online lectures because it fails to handle
technical jargon.

    - The authors should discuss the computational efficiency of the proposed algorithms
and how they scale with dataset size.

    - If applicable, the authors should discuss possible limitations of their approach to
address problems of privacy and fairness.

    - While the authors might fear that complete honesty about limitations might be used by
reviewers as grounds for rejection, a worse outcome might be that reviewers discover
limitations that aren’t acknowledged in the paper. The authors should use their best
judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers
will be specifically instructed to not penalize honesty concerning limitations.

3. **Theory assumptions and proofs**


Question: For each theoretical result, does the paper provide the full set of assumptions and
a complete (and correct) proof?

Answer: [Yes]

Justification: The paper states theoretical results in the main text and provides complete
assumptions, theorem statements, lemmas, and proofs in the appendix, including analyses of
signal-to-noise ratio, retrieval budget, target-graph calibration, stability, and self-evolution.

Guidelines:


   - The answer [N/A] means that the paper does not include theoretical results.

    - All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced.

    - All assumptions should be clearly stated or referenced in the statement of any theorems.

    - The proofs can either appear in the main paper or the supplemental material, but if
they appear in the supplemental material, the authors are encouraged to provide a short
proof sketch to provide intuition.

    - Inversely, any informal proof provided in the core of the paper should be complemented
by formal proofs provided in appendix or supplemental material.

   - Theorems and Lemmas that the proof relies upon should be properly referenced.

4. **Experimental result reproducibility**


Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions
of the paper (regardless of whether the code and data are provided or not)?


56


Answer: [Yes]


Justification: The paper describes the architecture, training procedure, datasets, baselines,
evaluation metrics, ablations, and implementation details needed to reproduce the main
experimental claims. Additional details are provided in the appendix and the released code.


Guidelines:


   - The answer [N/A] means that the paper does not include experiments.

    - If the paper includes experiments, a [No] answer to this question will not be perceived
well by the reviewers: Making the paper reproducible is important, regardless of
whether the code and data are provided or not.

    - If the contribution is a dataset and/or model, the authors should describe the steps taken
to make their results reproducible or verifiable.

    - Depending on the contribution, reproducibility can be accomplished in various ways.
For example, if the contribution is a novel architecture, describing the architecture fully
might suffice, or if the contribution is a specific model and empirical evaluation, it may
be necessary to either make it possible for others to replicate the model with the same
dataset, or provide access to the model. In general. releasing code and data is often
one good way to accomplish this, but reproducibility can also be provided via detailed
instructions for how to replicate the results, access to a hosted model (e.g., in the case
of a large language model), releasing of a model checkpoint, or other means that are
appropriate to the research performed.

    - While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the
nature of the contribution. For example
(a) If the contribution is primarily a new algorithm, the paper should make it clear how
to reproduce that algorithm.
(b) If the contribution is primarily a new model architecture, the paper should describe
the architecture clearly and fully.
(c) If the contribution is a new model (e.g., a large language model), then there should
either be a way to access this model for reproducing the results or a way to reproduce
the model (e.g., with an open-source dataset or instructions for how to construct
the dataset).
(d) We recognize that reproducibility may be tricky in some cases, in which case
authors are welcome to describe the particular way they provide for reproducibility.
In the case of closed-source models, it may be that access to the model is limited in
some way (e.g., to registered users), but it should be possible for other researchers
to have some path to reproducing or verifying the results.


5. **Open access to data and code**


Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental
material?


Answer: [Yes]


Justification: The paper provides open access to the code and data instructions, together
with scripts and documentation for reproducing the main experimental results.


Guidelines:


   - The answer [N/A] means that paper does not include experiments requiring code.

    - Please see the NeurIPS code and data submission guidelines ( `[https://neurips.cc](https://neurips.cc/public/guides/CodeSubmissionPolicy)`
`[/public/guides/CodeSubmissionPolicy](https://neurips.cc/public/guides/CodeSubmissionPolicy)` ) for more details.

    - While we encourage the release of code and data, we understand that this might not
be possible, so [No] is an acceptable answer. Papers cannot be rejected simply for not
including code, unless this is central to the contribution (e.g., for a new open-source
benchmark).

    - The instructions should contain the exact command and environment needed to run to
reproduce the results. See the NeurIPS code and data submission guidelines ( `[https:](https://neurips.cc/public/guides/CodeSubmissionPolicy)`
`[//neurips.cc/public/guides/CodeSubmissionPolicy](https://neurips.cc/public/guides/CodeSubmissionPolicy)` ) for more details.


57


    - The authors should provide instructions on data access and preparation, including how
to access the raw data, preprocessed data, intermediate data, and generated data, etc.

    - The authors should provide scripts to reproduce all experimental results for the new
proposed method and baselines. If only a subset of experiments are reproducible, they
should state which ones are omitted from the script and why.

    - At submission time, to preserve anonymity, the authors should release anonymized
versions (if applicable).

    - Providing as much information as possible in supplemental material (appended to the
paper) is recommended, but including URLs to data and code is permitted.


6. **Experimental setting/details**


Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer) necessary to understand the results?


Answer: [Yes]


Justification: The paper specifies the datasets, evaluation scenarios, baselines, metrics,
training procedures, and implementation details in the experimental section and appendices.
Dataset statistics, reader training, writer implementation, and ablation settings are also
reported.


Guidelines:


   - The answer [N/A] means that the paper does not include experiments.

    - The experimental setting should be presented in the core of the paper to a level of detail
that is necessary to appreciate the results and make sense of them.

    - The full details can be provided either with the code, in appendix, or as supplemental
material.


7. **Experiment statistical significance**


Question: Does the paper report error bars suitably and correctly defined or other appropriate
information about the statistical significance of the experiments?


Answer: [Yes]


Justification: The paper reports error bars or statistical significance information for the
experiments supporting the main empirical claims, and states how the variability is computed.


Guidelines:


   - The answer [N/A] means that the paper does not include experiments.

    - The authors should answer [Yes] if the results are accompanied by error bars, confidence
intervals, or statistical significance tests, at least for the experiments that support the
main claims of the paper.

    - The factors of variability that the error bars are capturing should be clearly stated (for
example, train/test split, initialization, random drawing of some parameter, or overall
run with given experimental conditions).

    - The method for calculating the error bars should be explained (closed form formula,
call to a library function, bootstrap, etc.)

   - The assumptions made should be given (e.g., Normally distributed errors).

    - It should be clear whether the error bar is the standard deviation or the standard error

of the mean.

    - It is OK to report 1-sigma error bars, but one should state it. The authors should
preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis
of Normality of errors is not verified.

    - For asymmetric distributions, the authors should be careful not to show in tables or
figures symmetric error bars that would yield results that are out of range (e.g., negative
error rates).

    - If error bars are reported in tables or plots, the authors should explain in the text how
they were calculated and reference the corresponding figures or tables in the text.


8. **Experiments compute resources**


58


Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce
the experiments?


Answer: [Yes]


Justification: The paper reports computational complexity and compute-resource information
in the Compute Resources section and Appendix J. The experiments were run on a server
equipped with 8 NVIDIA A100 GPUs.


Guidelines:


    - The answer [N/A] means that the paper does not include experiments.

    - The paper should indicate the type of compute workers CPU or GPU, internal cluster,
or cloud provider, including relevant memory and storage.

    - The paper should provide the amount of compute required for each of the individual
experimental runs as well as estimate the total compute.

    - The paper should disclose whether the full research project required more compute
than the experiments reported in the paper (e.g., preliminary or failed experiments that
didn’t make it into the paper).


9. **Code of ethics**


Question: Does the research conducted in the paper conform, in every respect, with the
NeurIPS Code of Ethics `[https://neurips.cc/public/EthicsGuidelines](https://neurips.cc/public/EthicsGuidelines)` ?


Answer: [Yes]


Justification: The research conforms to the NeurIPS Code of Ethics. It uses public benchmark
datasets, does not involve human subjects or crowdsourcing, and does not release high-risk
personal data.


Guidelines:


    - The answer [N/A] means that the authors have not reviewed the NeurIPS Code of
Ethics.

    - If the authors answer [No], they should explain the special circumstances that require a
deviation from the Code of Ethics.

    - The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction).


10. **Broader impacts**


Question: Does the paper discuss both potential positive societal impacts and negative
societal impacts of the work performed?


Answer: [Yes]

Justification: The paper discusses positive impacts such as improving grounded longterm memory for language agents, as well as negative impacts such as privacy, profiling,
surveillance, outdated memory retention, and hallucination risks.


Guidelines:


    - The answer [N/A] means that there is no societal impact of the work performed.

    - If the authors answer [N/A] or [No], they should explain why their work has no societal
impact or why the paper does not address societal impact.

    - Examples of negative societal impacts include potential malicious or unintended uses
(e.g., disinformation, generating fake profiles, surveillance), fairness considerations
(e.g., deployment of technologies that could make decisions that unfairly impact specific
groups), privacy considerations, and security considerations.

    - The conference expects that many papers will be foundational research and not tied
to particular applications, let alone deployments. However, if there is a direct path to
any negative applications, the authors should point it out. For example, it is legitimate
to point out that an improvement in the quality of generative models could be used to
generate Deepfakes for disinformation. On the other hand, it is not needed to point out
that a generic algorithm for optimizing neural networks could enable people to train
models that generate Deepfakes faster.


59


    - The authors should consider possible harms that could arise when the technology is
being used as intended and functioning correctly, harms that could arise when the
technology is being used as intended but gives incorrect results, and harms following
from (intentional or unintentional) misuse of the technology.

    - If there are negative societal impacts, the authors could also discuss possible mitigation
strategies (e.g., gated release of models, providing defenses in addition to attacks,
mechanisms for monitoring misuse, mechanisms to monitor how a system learns from
feedback over time, improving the efficiency and accessibility of ML).

11. **Safeguards**


Question: Does the paper describe safeguards that have been put in place for responsible
release of data or models that have a high risk for misuse (e.g., pre-trained language models,
image generators, or scraped datasets)?

Answer: [N/A]

Justification: The paper does not release a high-risk pretrained language model, image
generator, scraped dataset, or other asset requiring special misuse safeguards.

Guidelines:


    - The answer [N/A] means that the paper poses no such risks.

    - Released models that have a high risk for misuse or dual-use should be released with
necessary safeguards to allow for controlled use of the model, for example by requiring
that users adhere to usage guidelines or restrictions to access the model or implementing
safety filters.

    - Datasets that have been scraped from the Internet could pose safety risks. The authors
should describe how they avoided releasing unsafe images.

    - We recognize that providing effective safeguards is challenging, and many papers do
not require this, but we encourage authors to take this into account and make a best
faith effort.

12. **Licenses for existing assets**


Question: Are the creators or original owners of assets (e.g., code, data, models), used in
the paper, properly credited and are the license and terms of use explicitly mentioned and
properly respected?

Answer: [Yes]

Justification: The paper cites the creators of the existing datasets, models, and baselines
used in the experiments, and the license section states that their licenses and terms of use
are respected.

Guidelines:


    - The answer [N/A] means that the paper does not use existing assets.

    - The authors should cite the original paper that produced the code package or dataset.

    - The authors should state which version of the asset is used and, if possible, include a
URL.

    - The name of the license (e.g., CC-BY 4.0) should be included for each asset.

    - For scraped data from a particular source (e.g., website), the copyright and terms of
service of that source should be provided.

    - If assets are released, the license, copyright information, and terms of use in the package
should be provided. For popular datasets, `paperswithcode.com/datasets` has
curated licenses for some datasets. Their licensing guide can help determine the license
of a dataset.

    - For existing datasets that are re-packaged, both the original license and the license of
the derived asset (if it has changed) should be provided.

    - If this information is not available online, the authors are encouraged to reach out to
the asset’s creators.

13. **New assets**


Question: Are new assets introduced in the paper well documented and is the documentation
provided alongside the assets?


60


Answer: [N/A]

Justification: The paper does not introduce or release a new dataset, benchmark, or model
asset. The released code is provided for reproducibility and documented separately.

Guidelines:


    - The answer [N/A] means that the paper does not release new assets.

    - Researchers should communicate the details of the dataset/code/model as part of their
submissions via structured templates. This includes details about training, license,
limitations, etc.

    - The paper should discuss whether and how consent was obtained from people whose
asset is used.

    - At submission time, remember to anonymize your assets (if applicable). You can either
create an anonymized URL or include an anonymized zip file.

14. **Crowdsourcing and research with human subjects**


Question: For crowdsourcing experiments and research with human subjects, does the paper
include the full text of instructions given to participants and screenshots, if applicable, as
well as details about compensation (if any)?

Answer: [N/A]

Justification: The paper does not involve crowdsourcing experiments or research with human
subjects.

Guidelines:


    - The answer [N/A] means that the paper does not involve crowdsourcing nor research
with human subjects.

    - Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be
included in the main paper.

    - According to the NeurIPS Code of Ethics, workers involved in data collection, curation,
or other labor should be paid at least the minimum wage in the country of the data
collector.

15. **Institutional review board (IRB) approvals or equivalent for research with human**
**subjects**

Question: Does the paper describe potential risks incurred by study participants, whether
such risks were disclosed to the subjects, and whether Institutional Review Board (IRB)
approvals (or an equivalent approval/review based on the requirements of your country or
institution) were obtained?

Answer: [N/A]

Justification: The paper does not involve crowdsourcing experiments or research with human
subjects, so IRB approval or equivalent review is not applicable.

Guidelines:


    - The answer [N/A] means that the paper does not involve crowdsourcing nor research
with human subjects.

    - Depending on the country in which research is conducted, IRB approval (or equivalent)
may be required for any human subjects research. If you obtained IRB approval, you
should clearly state this in the paper.

    - We recognize that the procedures for this may vary significantly between institutions
and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the
guidelines for their institution.

    - For initial submissions, do not include any information that would break anonymity (if
applicable), such as the institution conducting the review.

16. **Declaration of LLM usage**


Question: Does the paper describe the usage of LLMs if it is an important, original, or
non-standard component of the core methods in this research? Note that if the LLM is used
only for writing, editing, or formatting purposes and does _not_ impact the core methodology,
scientific rigor, or originality of the research, declaration is not required.


61


Answer: [Yes]

Justification: The paper describes the use of LLMs in the system, including the memory
writer, structured query planning prompts, and answer generation. This usage is part of the
proposed method rather than only writing, editing, or formatting assistance.

Guidelines:


  - The answer [N/A] means that the core method development in this research does not
involve LLMs as any important, original, or non-standard components.

  - Please refer to our LLM policy in the NeurIPS handbook for what should or should not
be described.


62


