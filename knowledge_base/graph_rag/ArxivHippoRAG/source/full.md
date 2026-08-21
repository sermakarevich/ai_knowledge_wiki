## **HippoRAG: Neurobiologically Inspired** **Long-Term Memory for Large Language Models**

**Bernal Jiménez Gutiérrez** **Yiheng Shu**
The Ohio State University The Ohio State University


**Yu Gu** **Michihiro Yasunaga** **Yu Su**
The Ohio State University Stanford University The Ohio State University


**Abstract**


In order to thrive in hostile and ever-changing natural environments, mammalian
brains evolved to store large amounts of knowledge about the world and continually
integrate new information while avoiding catastrophic forgetting. Despite their
impressive accomplishments, large language models (LLMs), even with retrievalaugmented generation (RAG), still struggle to efficiently and effectively integrate
a large amount of new experiences after pre-training. In this work, we introduce
HippoRAG, a novel retrieval framework inspired by the hippocampal indexing
theory of human long-term memory to enable deeper and more efficient knowledge
integration over new experiences. HippoRAG synergistically orchestrates LLMs,
knowledge graphs, and the Personalized PageRank algorithm to mimic the different
roles of neocortex and hippocampus in human memory. We compare HippoRAG
with existing RAG methods on multi-hop question answering (QA) and show that
our method outperforms the state-of-the-art methods remarkably, by up to 20 %.
Single-step retrieval with HippoRAG achieves comparable or better performance
than iterative retrieval like IRCoT while being 10     - 20 times cheaper and 6     - 13 times
faster, and integrating HippoRAG into IRCoT brings further substantial gains.
Finally, we show that our method can tackle new types of scenarios that are out of
reach of existing methods. [1]


**1** **Introduction**


Millions of years of evolution have led mammalian brains to develop the crucial ability to store large
amounts of world knowledge and continuously integrate new experiences without losing previous
ones. This exceptional long-term memory system eventually allows us humans to keep vast stores of
continuously updating knowledge that forms the basis of our reasoning and decision making [19].


Despite the progress of large language models (LLMs) in recent years, such a continuously updating
long-term memory is still conspicuously absent from current AI systems. Due in part to its ease of
use and the limitations of other techniques such as model editing [ 46 ], retrieval-augmented generation
(RAG) has become the _de facto_ solution for long-term memory in LLMs, allowing users to present
new knowledge to a static model [36, 42, 66, 87].


However, current RAG methods are still unable to help LLMs perform tasks that require integrating
new knowledge across passage boundaries since each new passage is encoded in isolation. Many
important real-world tasks, such as scientific literature review, legal case briefing, and medical
diagnosis, require knowledge integration across passages or documents. Although less complex,


1
Code and data are available at `[https://github.com/OSU-NLP-Group/HippoRAG](https://github.com/OSU-NLP-Group/HippoRAG)` .


38th Conference on Neural Information Processing Systems (NeurIPS 2024).


Offline Indexing Online Retrieval








|&|%|!|
|---|---|---|
|'|#|"|









Answer:







Prof. Thomas




|Col1|&|%|"|&|
|---|---|---|---|---|
|Current<br>$|$|!|'|#|
|Human<br>RAG|Human<br>RAG|Human<br>RAG|Human<br>RAG|Human<br>RAG|
|Memory<br>**HippoRAG**|Memory<br>**HippoRAG**|Memory<br>**HippoRAG**|Memory<br>**HippoRAG**|Memory<br>**HippoRAG**|









Figure 1: **Knowledge Integration & RAG.** Tasks that require knowledge integration are particularly
challenging for current RAG systems. In the above example, we want to find a _Stanford_ professor
that does _Alzheimer’s_ research from a pool of passages describing potentially thousands _Stanford_
professors and _Alzheimer’s_ researchers. Since current methods encode passages in isolation, they
would struggle to identify _Prof. Thomas_ unless a passage mentions both characteristics at once. In
contrast, most people familiar with this professor would remember him quickly due to our brain’s
associative memory capabilities, thought to be driven by the index structure depicted in the C-shaped
hippocampus above (in blue). Inspired by this mechanism, **HippoRAG** allows LLMs to build and
leverage a similar graph of associations to tackle knowledge integration tasks.


standard multi-hop question answering (QA) also requires integrating information between passages
in a retrieval corpus. In order to solve such tasks, current RAG systems resort to using multiple
retrieval and LLM generation steps iteratively to join disparate passages [ 64, 78 ]. Nevertheless, even
perfectly executed multi-step RAG is still oftentimes insufficient to accomplish many scenarios of
knowledge integration, as we illustrate in what we call _path-finding_ multi-hop questions in Figure 1.


In contrast, our brains are capable of solving challenging knowledge integration tasks like these with
relative ease. The hippocampal memory indexing theory [ 75 ], a well-established theory of human
long-term memory, offers one plausible explanation for this remarkable ability. Teyler and Discenna

[75] propose that our powerful context-based, continually updating memory relies on interactions
between the neocortex, which processes and stores actual memory representations, and the C-shaped
hippocampus, which holds the _hippocampal index_, a set of interconnected indices which point to
memory units on the neocortex and stores associations between them [19, 76].


In this work, we propose HippoRAG, a RAG framework that serves as a long-term memory for LLMs
by mimicking this model of human memory. Our novel design first models the neocortex’s ability to
process perceptual input by using an LLM to transform a corpus into a schemaless knowledge graph
(KG) as our artificial hippocampal index. Given a new query, HippoRAG identifies the key concepts
in the query and runs the Personalized PageRank (PPR) algorithm [ 30 ] on the KG, using the query
concepts as the seeds, to integrate information across passages for retrieval. PPR enables HippoRAG
to explore KG paths and identify relevant subgraphs, essentially performing multi-hop reasoning in a
single retrieval step.


This capacity for _single-step multi-hop_ retrieval yields strong performance improvements of around
3 and 20 points over current RAG methods [ 10, 35, 53, 70, 71 ] on two popular multi-hop QA
benchmarks, MuSiQue [ 77 ] and 2WikiMultiHopQA [ 33 ]. Additionally, HippoRAG’s online retrieval
process is 10 to 30 times cheaper and 6 to 13 times faster than current iterative retrieval methods
like IRCoT [ 78 ], while still achieving comparable performance. Furthermore, our approach can be
combined with IRCoT to provide complementary gains of up to 4 % and 20 % on the same datasets
and even obtain improvements on HotpotQA, a less challenging multi-hop QA dataset. Finally, we


2


provide a case study illustrating the limitations of current methods as well as our method’s potential
on the previously discussed _path-finding_ multi-hop QA setting.


**2** **HippoRAG**


In this section, we first give a brief overview of the hippocampal memory indexing theory, followed
by how HippoRAG’s indexing and retrieval design was inspired by this theory, and finally offer a
more detailed account of our methodology.


**2.1** **The Hippocampal Memory Indexing Theory**


The hippocampal memory indexing theory [ 75 ] is a well-established theory that provides a functional
description of the components and circuitry involved in human long-term memory. In this theory,
Teyler and Discenna [75] propose that human long-term memory is composed of three components
that work together to accomplish two main objectives: _pattern separation_, which ensures that the
representations of distinct perceptual experiences are unique, and _pattern completion_, which enables
the retrieval of complete memories from partial stimuli [19, 76].


The theory suggests that pattern separation is primarily accomplished in the memory encoding
process, which starts with the **neocortex** receiving and processing perceptual stimuli into more easily
manipulatable, likely higher-level, features, which are then routed through the **parahippocampal**
**regions** (PHR) to be indexed by the hippocampus. When they reach the **hippocampus**, salient signals
are included in the hippocampal index and associated with each other.


After the memory encoding process is completed, pattern completion drives the memory retrieval
process whenever the hippocampus receives partial perceptual signals from the PHR pipeline. The
hippocampus then leverages its context-dependent memory system, thought to be implemented
through a densely connected network of neurons in the CA3 sub-region [ 76 ], to identify complete and
relevant memories within the hippocampal index and route them back through the PHR for simulation
in the neocortex. Thus, this complex process allows for new information to be integrated by changing
only the hippocampal index instead of updating neocortical representations.


**2.2** **Overview**


Our proposed approach, HippoRAG, is closely inspired by the process described above. As shown
in Figure 2, each component of our method corresponds to one of the three components of human
long-term memory. A detailed example of the HippoRAG process can be found in Appendix A.


**Offline Indexing.** Our offline indexing phase, analogous to memory encoding, starts by leveraging a
strong instruction-tuned **LLM**, our artificial neocortex, to extract knowledge graph (KG) triples. The
KG is schemaless and this process is known as open information extraction (OpenIE) [ 3, 5, 60, 98 ].
This process extracts salient signals from passages in a retrieval corpus as discrete noun phrases
rather than dense vector representations, allowing for more fine-grained pattern separation. It is
therefore natural to define our artificial hippocampal index as this open **KG**, which is built on the
whole retrieval corpus passage-by-passage. Finally, to connect both components as is done by the
parahippocampal regions, we use off-the-shelf dense encoders fine-tuned for retrieval ( **retrieval**
**encoders** ). These retrieval encoders provide additional edges between similar but not identical noun
phrases within this KG to aid in downstream pattern completion.


**Online Retrieval.** These same three components are then leveraged to perform online retrieval
by mirroring the human brain’s memory retrieval process. Just as the hippocampus receives input
processed through the neocortex and PHR, our LLM-based neocortex extracts a set of salient named
entities from a query which we call _query named entities_ . These named entities are then linked to
nodes in our KG based on the similarity determined by retrieval encoders; we refer to these selected
nodes as _query nodes_ . Once the query nodes are chosen, they become the partial cues from which our
synthetic hippocampus performs pattern completion. In the hippocampus, neural pathways between
elements of the hippocampal index enable relevant neighborhoods to become activated and recalled
upstream. To imitate this efficient graph search process, we leverage the Personalized PageRank
(PPR) algorithm [ 30 ], a version of PageRank that distributes probability across a graph only through
a set of user-defined source nodes. This constraint allows us to bias the PPR output only towards the


3


Hippocampus


KG + Personalized PageRank



Parahippocampal Regions


Retrieval Encoders


(,



(,





Neocortex


LLM


Open IE


NER













**Offline**
**Indexing**


**Online**

**Retrieval**



Passages


Query





















Figure 2: **Detailed HippoRAG Methodology.** We model the three components of human long-term
memory to mimic its pattern separation and completion functions. For offline indexing **(Middle)**,
we use an LLM to process passages into open KG triples, which are then added to our artificial
hippocampal index, while our synthetic parahippocampal regions (PHR) detect synonymy. In the
example above, triples involving Professor Thomas are extracted and integrated into the KG. For
online retrieval **(Bottom)**, our LLM neocortex extracts named entities from a query while our
parahippocampal retrieval encoders link them to our hippocampal index. We then leverage the
Personalized PageRank algorithm to enable context-based retrieval and extract Professor Thomas. [4]


set of query nodes, just as the hippocampus extracts associated signals from specific partial cues. [2]
Finally, as is done when the hippocampal signal is sent upstream, we aggregate the output PPR node
probability over the previously indexed passages and use that to rank them for retrieval.


**2.3** **Detailed Methodology**


**Offline Indexing.** Our indexing process involves processing a set of passages _P_ using an instructiontuned LLM _L_ and a retrieval encoder _M_ . As seen in Figure 2 we first use _L_ to extract a set of noun
phrase nodes _N_ and relation edges _E_ from each passage in _P_ via OpenIE. This process is done via
1-shot prompting of the LLM with the prompts shown in Appendix I. Specifically, we first extract a
set of named entities from each passage. We then add the named entities to the OpenIE prompt to
extract the final triples, which also contain concepts (noun phrases) beyond named entities. We find
that this two-step prompt configuration leads to an appropriate balance between generality and bias
towards named entities. Finally, we use _M_ to add the extra set of _synonymy_ relations _E_ _[′]_ discussed
above when the cosine similarity between two entity representations in _N_ is above a threshold _τ_ . As
stated above, this introduces more edges to our hippocampal index and allows for more effective
pattern completion. This indexing process defines a _|N_ _| × |P_ _|_ matrix **P**, which contains the number
of times each noun phrase in the KG appears in each original passage.


**Online Retrieval.** During the retrieval process, we prompt _L_ using a 1-shot prompt to extract a set
of named entities from a query _q_, our previously defined query named entities _C_ _q_ = _{c_ 1 _, ..., c_ _n_ _}_
( _Stanford_ and _Alzheimer’s_ in our Figure 2 example). These named entities _C_ _q_ from the query are
then encoded by the same retrieval encoder _M_ . Then, the previously defined query nodes are
chosen as the set of nodes in _N_ with the highest cosine similarity to the query named entities
_C_ _q_ . More formally, query nodes are defined as _R_ _q_ = _{r_ 1 _, ..., r_ _n_ _}_ such that _r_ _i_ = _e_ _k_ where _k_ =
arg max _j_ _cosine_ _ _similarity_ ( _M_ ( _c_ _i_ ) _, M_ ( _e_ _j_ )), represented as the _Stanford_ logo and the _Alzheimer’s_
purple ribbon symbol in Figure 2.


2 Intriguingly, some work in cognitive science has also found a correlation between human word recall and
the output of the PageRank algorithm [25].
4 Many details around the hippocampal memory indexing theory are omitted from this study for simplicity.
We encourage interested reader to follow the references in §2.1 for more.


4


After the query nodes _R_ _q_ are found, we run the PPR algorithm over the hippocampal index, i.e., a
KG with _|N_ _|_ nodes and _|E|_ + _|E_ _[′]_ _|_ edges (triple-based and synonymy-based), using a personalized
probability distribution [#»] _n_ defined over _N_, in which each query node has equal probability and all
other nodes have a probability of zero. This allows probability mass to be distributed to nodes that are
primarily in the (joint) neighborhood of the query nodes, such as _Professor Thomas_, and contribute to
eventual retrieval. After running the PPR algorithm, we obtain an updated probability distribution #»
_n_ _[′]_ over _N_ . Finally, in order to obtain passage scores, we multiply _n_ [#»] _[′]_ with the previously defined **P**
matrix to obtain [#»] _p_, a ranking score for each passage, which we use for retrieval.


**Node Specificity.** We introduce node specificity as a neurobiologically plausible way to further
improve retrieval. It is well known that global signals for word importance, like inverse document
frequency (IDF), can improve information retrieval. However, in order for our brain to leverage IDF
for retrieval, the number of total “passages” encoded would need to be aggregated with all node
activations before memory retrieval is complete. While simple for normal computers, this process
would require activating connections between an aggregator neuron and all nodes in the hippocampal
index every time retrieval occurs, likely introducing prohibitive computational overhead. Given
these constraints, we propose _node specificity_ as an alternative IDF signal which requires only local
signals and is thus more neurobiologically plausible. We define the node specificity of node _i_ as
_s_ _i_ = _|P_ _i_ _|_ _[−]_ [1], where _P_ _i_ is the set of passages in _P_ from which node _i_ was extracted, information that
is already available at each node. Node specificity is used in retrieval by multiplying each query node
probability [#»] _n_ with _s_ _i_ before PPR; this allows us to modulate each of their neighborhood’s probability
as well as their own. We illustrate node specificity in Figure 2 through relative symbol size: the
_Stanford_ logo grows larger than the _Alzheimer’s_ symbol since it appears in fewer documents.


**3** **Experimental Setup**


**3.1** **Datasets**


We evaluate our method’s retrieval capabilities primarily on two challenging multi-hop QA benchmarks, **MuSiQue** (answerable) [ 77 ] and **2WikiMultiHopQA** [ 33 ]. For completeness, we also
include the **HotpotQA** [ 89 ] dataset even though it has been found to be a much weaker test for
multi-hop reasoning due to many spurious signals [ 77 ], as we also show in Appendix B. To limit
the experimental cost, we extract 1 _,_ 000 questions from each validation set as done in previous work

[ 63, 78 ]. In order to create a more realistic retrieval setting, we follow IRCoT [ 78 ] and collect all
candidate passages (including supporting and distractor passages) from our selected questions and
form a retrieval corpus for each dataset. The details of these datasets are shown in Table 1.


Table 1: Retrieval corpora and extracted KG statistics for each of our 1 _,_ 000 question dev sets.


**MuSiQue** **2Wiki** **HotpotQA**


# of Passages ( _P_ ) 11 _,_ 656 6 _,_ 119 9 _,_ 221
# of Unique Nodes ( _N_ ) 91 _,_ 729 42 _,_ 694 82 _,_ 157
# of Unique Edges ( _E_ ) 21 _,_ 714 7 _,_ 867 17 _,_ 523
# of Unique Triples 107 _,_ 448 50 _,_ 671 98 _,_ 709
# of Contriever Synonym Edges ( _E_ _[′]_ ) 145 _,_ 990 146 _,_ 020 159 _,_ 112
# of ColBERTv2 Synonym Edges ( _E_ _[′]_ ) 191 _,_ 636 82 _,_ 526 171 _,_ 856


**3.2** **Baselines**


We compare against several strong and widely used retrieval methods: **BM25** [ 69 ], **Contriever** [ 35 ],
**GTR** [ 53 ] and **ColBERTv2** [ 70 ]. Additionally, we compare against two recent LLM-augmented
baselines: **Propositionizer** [ 10 ], which rewrites passages into propositions, and **RAPTOR** [ 71 ],
which constructs summary nodes to ease retrieval from long documents. In addition to the single-step
retrieval methods above, we also include the multi-step retrieval method **IRCoT** [78] as a baseline.


**3.3** **Metrics**


We report retrieval and QA performance on the datasets above using recall@2 and recall@5 (R@2
and R@5 below) for retrieval and exact match (EM) and F1 scores for QA performance.


5


Table 2: **Single-step retrieval performance.** HippoRAG outperforms all baselines on MuSiQue and
2WikiMultiHopQA and achieves comparable performance on the less challenging HotpotQA dataset.


**MuSiQue** **2Wiki** **HotpotQA** **Average**


R@2 R@5 R@2 R@5 R@2 R@5 R@2 R@5


BM25 [69] 32 _._ 3 41 _._ 2 51 _._ 8 61 _._ 9 55 _._ 4 72 _._ 2 46 _._ 5 58 _._ 4
Contriever [35] 34 _._ 8 46 _._ 6 46 _._ 6 57 _._ 5 57 _._ 2 75 _._ 5 46 _._ 2 59 _._ 9
GTR [53] 37 _._ 4 49 _._ 1 60 _._ 2 67 _._ 9 59 _._ 4 73 _._ 3 52 _._ 3 63 _._ 4
ColBERTv2 [70] 37 _._ 9 49 _._ 2 59 _._ 2 68 _._ 2 **64** _._ **7** **79** _._ **3** 53 _._ 9 65 _._ 6
RAPTOR [71] 35 _._ 7 45 _._ 3 46 _._ 3 53 _._ 8 58 _._ 1 71 _._ 2 46 _._ 7 56 _._ 8
RAPTOR (ColBERTv2) 36 _._ 9 46 _._ 5 57 _._ 3 64 _._ 7 63 _._ 1 75 _._ 6 52 _._ 4 62 _._ 3
Proposition [10] 37 _._ 6 49 _._ 3 56 _._ 4 63 _._ 1 58 _._ 7 71 _._ 1 50 _._ 9 61 _._ 2
Proposition (ColBERTv2) 37 _._ 8 50 _._ 1 55 _._ 9 64 _._ 9 63 _._ 9 78 _._ 1 52 _._ 5 64 _._ 4


HippoRAG (Contriever) **41** _._ **0** **52** _._ **1** **71** _._ **5** **89** _._ **5** 59 _._ 0 76 _._ 2 57 _._ 2 72 _._ 6
HippoRAG (ColBERTv2) 40 _._ 9 51 _._ 9 70 _._ 7 89 _._ 1 60 _._ 5 77 _._ 7 **57** _._ **4** **72** _._ **9**


Table 3: **Multi-step retrieval performance.** Combining HippoRAG with standard multi-step retrieval
methods like IRCoT results in strong complementary improvements on all three datasets.


**MuSiQue** **2Wiki** **HotpotQA** **Average**


R@2 R@5 R@2 R@5 R@2 R@5 R@2 R@5


IRCoT + BM25 (Default) 34 _._ 2 44 _._ 7 61 _._ 2 75 _._ 6 65 _._ 6 79 _._ 0 53 _._ 7 66 _._ 4
IRCoT + Contriever 39 _._ 1 52 _._ 2 51 _._ 6 63 _._ 8 65 _._ 9 81 _._ 6 52 _._ 2 65 _._ 9

IRCoT + ColBERTv2 41 _._ 7 53 _._ 7 64 _._ 1 74 _._ 4 **67** _._ **9** 82 _._ 0 57 _._ 9 70 _._ 0


IRCoT + HippoRAG (Contriever) 43 _._ 9 56 _._ 6 75 _._ 3 93 _._ 4 65 _._ 8 82 _._ 3 61 _._ 7 77 _._ 4
IRCoT + HippoRAG (ColBERTv2) **45** _._ **3** **57** _._ **6** **75** _._ **8** **93** _._ **9** 67 _._ 0 **83** _._ **0** **62** _._ **7** **78** _._ **2**


**3.4** **Implementation Details**


By default, we use `GPT-3.5-turbo-1106` [ 55 ] with temperature of 0 as our LLM _L_ and Contriever

[ 35 ] or ColBERTv2 [ 70 ] as our retriever _M_ . We use 100 examples from MuSiQue’s training data
to tune HippoRAG’s two hyperparameters: the synonymy threshold _τ_ at 0 _._ 8 and the PPR damping
factor at 0 _._ 5, which determines the probability that PPR will restart a random walk from the query
nodes instead of continuing to explore the graph. Generally, we find that HippoRAG’s performance
is rather robust to its hyperparameters. More implementation details can be found in Appendix H.


**4** **Results**


We present our retrieval and QA experimental results below. Given that our method indirectly affects
QA performance, we report QA results on our best-performing retrieval backbone ColBERTv2 [ 70 ].
However, we report retrieval results for several strong single-step and multi-step retrieval techniques.


**Single-Step Retrieval Results.** As seen in Table 2, HippoRAG outperforms all other methods,
including recent LLM-augmented baselines such as Propositionizer and RAPTOR, on our main
datasets, MuSiQue and 2WikiMultiHopQA, while achieving competitive performance on HotpotQA.
We notice an impressive improvement of 11 and 20 % for R@2 and R@5 on 2WikiMultiHopQA
and around 3 % on MuSiQue. This difference can be partially explained by 2WikiMultiHopQA’s
entity-centric design, which is particularly well-suited for HippoRAG. Our lower performance on
HotpotQA is mainly due to its lower knowledge integration requirements, as explained in Appendix
B, as well as a due to a concept-context tradeoff which we alleviate with an ensembling technique
described in Appendix F.2.


**Multi-Step Retrieval Results.** For multi-step or iterative retrieval, our experiments in Table 3
demonstrate that IRCoT [ 78 ] and HippoRAG are complementary. Using HippoRAG as the retriever for IRCoT continues to bring R@5 improvements of around 4 % for MuSiQue, 18 % for
2WikiMultiHopQA and an additional 1% on HotpotQA.


6


Table 4: **QA performance.** HippoRAG’s QA improvements correlate with its retrieval improvements
on single-step (rows 1-3) and multi-step retrieval (rows 4-5).


**MuSiQue** **2Wiki** **HotpotQA** **Average**


Retriever EM F1 EM F1 EM F1 EM F1


None 12 _._ 5 24 _._ 1 31 _._ 0 39 _._ 6 30 _._ 4 42 _._ 8 24 _._ 6 35 _._ 5

ColBERTv2 15 _._ 5 26 _._ 4 33 _._ 4 43 _._ 3 43 _._ 4 57 _._ 7 30 _._ 8 42 _._ 5
HippoRAG (ColBERTv2) 19 _._ 2 29 _._ 8 46 _._ 6 59 _._ 5 41 _._ 8 55 _._ 0 35 _._ 9 48 _._ 1


IRCoT (ColBERTv2) 19 _._ 1 30 _._ 5 35 _._ 4 45 _._ 1 45 _._ 5 58 _._ 4 33 _._ 3 44 _._ 7
IRCoT + HippoRAG (ColBERTv2) **21** _._ **9** **33** _._ **3** **47** _._ **7** **62** _._ **7** **45** _._ **7** **59** _._ **2** **38** _._ **4** **51** _._ **7**


**Question Answering Results.** We report QA results for HippoRAG, the strongest retrieval baselines,
ColBERTv2 and IRCoT, as well as IRCoT using HippoRAG as a retriever in Table 4. As expected,
improved retrieval performance in both single and multi-step settings leads to strong overall improvements of up to 3 %, 17 % and 1 % F1 scores on MuSiQue, 2WikiMultiHopQA and HotpotQA
respectively using the same QA reader. Notably, single-step HippoRAG is on par or outperforms
IRCoT while being 10 - 30 times cheaper and 6 - 13 times faster during online retrieval (Appendix G).


**5** **Discussions**


**5.1** **What Makes HippoRAG Work?**


**OpenIE Alternatives.** To determine if using a closed model like GPT-3.5 is essential to retain our
performance improvements, we replace it with an end-to-end OpenIE model REBEL [ 34 ] as well
as the 8B and 70B instruction-tuned versions of Llama-3.1, a class of strong open-weight LLMs

[ 1 ]. As shown in Table 5 row 2, building our KG using REBEL results in large performance drops,
underscoring the importance of LLM flexibility. Specifically, GPT-3.5 produces twice as many triples
as REBEL, indicating its bias against producing triples with general concepts and leaving many
useful associations behind.


In terms of open-weight LLMs, Table 5 (rows 3-4) shows that the performance of Llama-3.1-8B is
competitive with GPT-3.5 in all datasets except for 2Wiki, where performance drops substantially.
Nevertheless, the stronger 70B counterpart outperforms GPT-3.5 in two out of three datasets and is still
competitive in 2Wiki. The strong performance of Llama-3.1-70B and the comparable performance of
even the 8B model is encouraging since it offers a cheaper alternative for indexing over large corpora.
The graph statistics for these OpenIE alternatives can be found in Appendix C.


To understand the relationship between OpenIE and retrieval performance more deeply, we extract
239 gold triples from 20 examples from the MuSiQue training set. We then perform a small-scale
intrinsic evaluation using the CaRB [ 6 ] framework for OpenIE. We find that both Llama-3.1-Instruct


Table 5: **Dissecting HippoRAG.** To understand what makes it work well, we replace its OpenIE
module and PPR with plausible alternatives and ablate node specificity and synonymy-based edges.


**MuSiQue** **2Wiki** **HotpotQA** **Average**


R@2 R@5 R@2 R@5 R@2 R@5 R@2 R@5


HippoRAG 40 _._ 9 51 _._ 9 **70** _._ **7** **89** _._ **1** 60 _._ 5 77 _._ 7 **57** _._ **4** **72** _._ **9**



OpenIE
Alternatives



REBEL [34] 31 _._ 7 39 _._ 6 63 _._ 1 76 _._ 5 43 _._ 9 59 _._ 2 46 _._ 2 58 _._ 4
Llama-3.1-8B-Instruct [1] 40 _._ 8 51 _._ 9 62 _._ 5 77 _._ 5 59 _._ 9 75 _._ 1 54 _._ 4 67 _._ 8
Llama-3.1-70B-Instruct [1] **41** _._ **8** **53** _._ **7** 68 _._ 8 85 _._ 3 **60** _._ **8** **78** _._ **6** 57 _._ 1 72 _._ 5



PPR _R_ _q_ Nodes Only 37 _._ 1 41 _._ 0 59 _._ 1 61 _._ 4 55 _._ 9 66 _._ 2 50 _._ 7 56 _._ 2
Alternatives _R_ _q_ Nodes & Neighbors 25 _._ 4 38 _._ 5 53 _._ 4 74 _._ 7 47 _._ 8 64 _._ 5 42 _._ 2 59 _._ 2


Ablations w/o Node Specificity 37 _._ 6 50 _._ 2 70 _._ 1 88 _._ 8 56 _._ 3 73 _._ 7 54 _._ 7 70 _._ 9
w/o Synonymy Edges 40 _._ 2 50 _._ 2 69 _._ 2 85 _._ 6 59 _._ 1 75 _._ 7 56 _._ 2 70 _._ 5


7


models underperform GPT-3.5 slightly on this intrinsic evaluation but all LLMs vastly outperform
REBEL. More details about this evaluation experiments can be found in Appendix D.


**PPR Alternatives.** As shown in Table 5 (rows 5-6), to examine how much of our results are due to
the strength of PPR, we replace the PPR output with the query node probability [#»] _n_ multiplied by node
specificity values (row 5) and a version of this that also distributes a small amount of probability to the
direct neighbors of each query node (row 6). First, we find that PPR is a much more effective method
for including associations for retrieval on all three datasets compared to both simple baselines. It is
interesting to note that adding the neighborhood of _R_ _q_ nodes without PPR leads to worse performance
than only using the query nodes themselves.


**Ablations.** As seen in Table 5 (rows 7-8), node specificity obtains considerable improvements on
MuSiQue and HotpotQA and yields almost no change in 2WikiMultiHopQA. This is likely because
2WikiMultiHopQA relies on named entities with little differences in terms of term weighting. In
contrast, synonymy edges have the largest effect on 2WikiMultiHopQA, suggesting that noisy entity
standardization is useful when most relevant concepts are named entities, and improvements to
synonymy detection could lead to stronger performance in other datasets.


**5.2** **HippoRAG’s Advantage: Single-Step Multi-Hop Retrieval**


A major advantage of HippoRAG over conventional RAG methods in multi-hop QA is its ability
to _perform multi-hop retrieval in a single step_ . We demonstrate this by measuring the percentage
of queries where _all_ the supporting passages are retrieved successfully, a feat that can only be
accomplished through successful multi-hop reasoning. Table 6 below shows that the gap between
our method and ColBERTv2, using the top- 5 passages, increases even more from 3 % to 6 % on
MuSiQue and from 20 % to 38 % on 2WikiMultiHopQA, suggesting that large improvements come
from obtaining all supporting documents rather than achieving partially retrieval on more questions.


Table 6: **All-Recall metric.** We measure the percentage of queries for which all supporting passages
are successfully retrieved (all-recall, denoted as AR@2 or AR@5) and find even larger performance
improvements for HippoRAG.


**MuSiQue** **2Wiki** **HotpotQA** **Average**


AR@2 AR@5 AR@2 AR@5 AR@2 AR@5 AR@2 AR@5


ColBERTv2 [70] 6 _._ 8 16 _._ 1 25 _._ 1 37 _._ 1 33 _._ 3 59 _._ 0 21 _._ 7 37 _._ 4
HippoRAG 10 _._ 2 22 _._ 4 45 _._ 4 75 _._ 7 33 _._ 8 57 _._ 9 29 _._ 8 52 _._ 0


We further illustrate HippoRAG’s unique _single-step multi-hop retrieval_ ability through the first
example in Table 7. In this example, even though _Alhandra_ was not mentioned in _Vila de Xira’s_
passage, HippoRAG can directly leverage Vila de Xira’s connection to Alhandra as his place of
birth to determine its importance, something that standard RAG methods would be unable to do
directly. Additionally, even though IRCoT can also solve this multi-hop retrieval problem, as shown
in Appendix G, it is 10 - 30 times more expensive and 6 - 13 times slower than ours in terms of online
retrieval, arguably the most important factor when it comes to serving end users.


Table 7: **Multi-hop question types.** We show example results for different approaches on path-finding
vs. path-following multi-hop questions.


**Question** **HippoRAG** **ColBERTv2** **IRCoT**



**1. Alhandra**

**2. Vila de Xira**

**3.** Póvoa de

Santa Iria


**1.** Brian Knutson

**2.** Eric Knudsen

**3.** Lisa Giocomo



**1. Alhandra**

**2. Vila de Xira**
**3.** Portugal


**1. Thomas Südhof**

**2.** Karl Deisseroth
**3.** Robert Sapolsky


8



**1. Alhandra**

**2.** Dimuthu
Abayakoon
**3.** Ja‘ar


**1.** Brian Knutson

**2.** Eric Knudsen

**3.** Lisa Giocomo



PathFollowing


PathFinding



In which

district was

**Alhandra**

born?


Which **Stanford**
professor works on
the neuroscience

of **Alzheimer’s** ?


**5.3** **HippoRAG’s Potential: Path-Finding Multi-Hop Retrieval**


The second example in Table 7, also present in Figure 1, shows a type of questions that is trivial
for informed humans but out of reach for current retrievers without further training. This type of
questions, which we call _path-finding_ multi-hop questions, requires identifying one path between a
set of entities when many paths exist to explore instead of _following_ a specific path, as in standard
multi-hop questions. [5]


More specifically, a simple iterative process can retrieve the appropriate passages for the first
question by following the one path set by _Alhandra’s_ one place of birth, as seen by IRCoT’s perfect
performance. However, an iterative process would struggle to answer the second question given
the many possible paths to explore—either through professors at _Stanford University_ or professors
working on the neuroscience of _Alzheimer’s_ . It is only by associating disparate information about
Thomas Südhof that someone who knows about this professor would be able to answer this question
easily. As seen in Table 7, both ColBERTv2 and IRCoT fail to extract the necessary passages since
they cannot access these associations. On the other hand, HippoRAG leverages its web of associations
in its hippocampal index and graph search algorithm to determine that Professor Thomas is relevant
to this query and retrieves his passages appropriately. More examples of these path-finding multi-hop
questions can be found in our case study in Appendix E.


**6** **Related Work**


**6.1** **LLM Long-Term Memory**


**Parametric Long-Term Memory.** It is well-accepted, even among skeptical researchers, that the
parameters of modern LLMs encode a remarkable amount of world knowledge [ 2, 12, 23, 28, 31, 39,
62, 79 ], which can be leveraged by an LLM in flexible and robust ways [ 81, 83, 93 ]. Nevertheless, our
ability to update this vast knowledge store, an essential part of any long-term memory system, is still
surprisingly limited. Although many techniques to update LLMs exist, such as standard fine-tuning,
model editing [ 15, 49, 50, 51, 52, 95 ] and even external parametric memory modules inspired by
human memory [ 58, 82, 32 ], no methodology has yet to emerge as a robust solution for continual
learning in LLMs [26, 46, 97].


**RAG as Long-Term Memory.** On the other hand, using RAG methods as a long-term memory
system offers a simple way to update knowledge over time [ 36, 42, 66, 73 ]. More sophisticated
RAG methods, which perform multiple steps of retrieval and generation from an LLM, are even
able to integrate information across new or updated knowledge elements[38, 64, 72, 78, 88, 90, 92],
another crucial aspect of long-term memory systems. As discussed above, however, this type of
online information integration is unable to solve the more complex knowledge integration tasks that
we illustrate with our _path-finding_ multi-hop QA examples.


Some other methods, such as RAPTOR [ 71 ], MemWalker [ 9 ] and GraphRAG [ 18 ], integrate information during the offline indexing phase similarly to HippoRAG and might be able to handle these
more complex tasks. However, these methods integrate information by summarizing knowledge
elements, which means that the summarization process must be repeated any time new data is added.
In contrast, HippoRAG can continuously integrate new knowledge by simply adding edges to its KG.


**Long Context as Long-Term Memory.** Context lengths for both open and closed source LLMs have
increased dramatically in the past year [ 11, 17, 22, 61, 68 ]. This scaling trend seems to indicate that
future LLMs could perform long-term memory storage within massive context windows. However,
the viability of this future remains largely uncertain given the many engineering hurdles involved and
the apparent limitations of long-context LLMs, even within current context lengths [41, 45, 96, 21].


**6.2** **Multi-Hop QA & Graphs**


Many previous works have also tackled multi-hop QA using graph structures. These efforts can
be broadly divided in two major categories: 1) graph-augmented reading comprehension, where a


5 Path-finding questions require knowledge integration when search entities like _Stanford_ and _Alzheimer’s_ do
not happen to appear together in a passage, a condition which is often satisfied for new information.


9


graph is extracted from retrieved documents and used to improve a model’s reasoning process and 2)
graph-augmented retrieval, where models find relevant documents by traversing a graph structure.


**Graph-Augmented Reading Comprehension.** Earlier works in this category are mainly supervised
methods which mix signal from a hyperlink or co-occurrence graph with a language model through a
graph neural network (GNN) [ 20, 67, 65 ]. More recent works use LLMs and introduce knowledge
graph triples directly into the LLM prompt [ 57, 43, 47 ]. Although these works share HippoRAG’s
use of graphs for multi-hop QA, their generation-based improvements are fully complementary to
HippoRAG’s, which are solely based on improved retrieval.


**Graph-Augmented Retrieval.** In this second category, previous work trains a re-ranking module
which can traverse a graph made using Wikipedia hyperlinks [ 16, 100, 54, 14, 4, 44 ]. HippoRAG,
in contrast, builds a KG from scratch using LLMs and performs multi-hop retrieval without any
supervision, making it much more adaptable.


**6.3** **LLMs & KGs**


Combining the strengths of language models and knowledge graphs has been an active research
direction for many years, both for augmenting LLMs with a KG in different ways [ 48, 80, 84 ] or
augmenting KGs by either distilling knowledge from an LLM’s parametric knowledge [ 7, 85 ] or
using them to parse text directly [ 8, 29, 94 ]. In an exceptionally comprehensive survey, Pan et al. [56]
present a roadmap for this research direction and highlight the importance of work which _synergizes_
these two important technologies [ 37, 74, 27, 91, 99 ]. Like these works, HippoRAG shows the
potential for synergy between these two technologies, combining the knowledge graph construction
abilities of LLMs with the retrieval advantages of structured knowledge for more effective RAG.


**7** **Conclusions & Limitations**


Our proposed neurobiologically principled methodology, although simple, already shows promise for
overcoming the inherent limitations of standard RAG systems while retaining their advantages over
parametric memory. HippoRAG’s knowledge integration capabilities, demonstrated by its strong
results on _path-following_ multi-hop QA and promise on _path-finding_ multi-hop QA, as well as its
dramatic efficiency improvements and continuously updating nature, makes it a powerful middleground framework between standard RAG methods and parametric memory and offers a compelling
solution for long-term memory in LLMs.


Nevertheless, several limitations can be addressed in future work to enable HippoRAG to achieve
this goal better. First, we note that all components of HippoRAG are currently used off-the-shelf
without any extra training. There is therefore much room to improve our method’s practical viability
by performing specific component fine-tuning. This is evident in the error analysis discussed in
Appendix F, which shows most errors made by our system are due to NER and OpenIE and thus
could benefit from direct fine-tuning. Given that the rest of the errors are graph search errors, also in
Appendix F, we note that several avenues for improvements over simple PPR exist, such as allowing
relations to guide graph traversal directly. Additionally, as shown in Appendix F.4, more work must
be done to improve the consistency of OpenIE in longer compared to shorter documents. Finally,
and perhaps most importantly, HippoRAG’s scalability still calls for further validation. Although we
show that Llama-3.1 could obtain similar performance to closed-source models and thus reduce costs
considerably, we are yet to empirically prove the efficiency and efficacy of our synthetic hippocampal
index as its size grows way beyond current benchmarks.


**Acknowledgments**


The authors would like to thank colleagues from the OSU NLP group and Percy Liang for
their thoughtful comments. This research was supported in part by NSF OAC 2112606, NIH
R01LM014199, ARL W911NF2220144, and Cisco. The views and conclusions contained herein
are those of the authors and should not be interpreted as representing the official policies, either
expressed or implied, of the U.S. government. The U.S. Government is authorized to reproduce and
distribute reprints for Government purposes notwithstanding any copyright notice herein.


10


**References**


[1] AI@Meta. Llama 3 model card. 2024. URL `[https://github.com/meta-llama/llama3/](https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md)`
`[blob/main/MODEL_CARD.md](https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md)` .


[2] B. AlKhamissi, M. Li, A. Celikyilmaz, M. T. Diab, and M. Ghazvininejad. A review on
language models as knowledge bases. _ArXiv_, abs/2204.06031, 2022. URL `[https://arxiv.](https://arxiv.org/abs/2204.06031)`
`[org/abs/2204.06031](https://arxiv.org/abs/2204.06031)` .


[3] G. Angeli, M. J. Johnson Premkumar, and C. D. Manning. Leveraging linguistic structure
for open domain information extraction. In C. Zong and M. Strube, editors, _Proceedings_
_of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th_
_International Joint Conference on Natural Language Processing (Volume 1: Long Papers)_,
pages 344–354, Beijing, China, July 2015. Association for Computational Linguistics. doi:
10.3115/v1/P15-1034. URL `[https://aclanthology.org/P15-1034](https://aclanthology.org/P15-1034)` .


[4] A. Asai, K. Hashimoto, H. Hajishirzi, R. Socher, and C. Xiong. Learning to retrieve reasoning
paths over wikipedia graph for question answering. In _International Conference on Learning_
_Representations_, 2020. URL `[https://openreview.net/forum?id=SJgVHkrYDH](https://openreview.net/forum?id=SJgVHkrYDH)` .


[5] M. Banko, M. J. Cafarella, S. Soderland, M. Broadhead, and O. Etzioni. Open information
extraction from the web. In _Proceedings of the 20th International Joint Conference on Artifical_
_Intelligence_, IJCAI’07, page 2670–2676, San Francisco, CA, USA, 2007. Morgan Kaufmann
Publishers Inc.


[6] S. Bhardwaj, S. Aggarwal, and Mausam. CaRB: A crowdsourced benchmark for open IE. In
K. Inui, J. Jiang, V. Ng, and X. Wan, editors, _Proceedings of the 2019 Conference on Empirical_
_Methods in Natural Language Processing and the 9th International Joint Conference on_
_Natural Language Processing (EMNLP-IJCNLP)_, pages 6262–6267, Hong Kong, China,
Nov. 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1651. URL
`[https://aclanthology.org/D19-1651](https://aclanthology.org/D19-1651)` .


[7] A. Bosselut, H. Rashkin, M. Sap, C. Malaviya, A. Celikyilmaz, and Y. Choi. COMET:
Commonsense transformers for automatic knowledge graph construction. In A. Korhonen,
D. Traum, and L. Màrquez, editors, _Proceedings of the 57th Annual Meeting of the Association_
_for Computational Linguistics_, pages 4762–4779, Florence, Italy, July 2019. Association for
Computational Linguistics. doi: 10.18653/v1/P19-1470. URL `[https://aclanthology.](https://aclanthology.org/P19-1470)`
`[org/P19-1470](https://aclanthology.org/P19-1470)` .


[8] B. Chen and A. L. Bertozzi. AutoKG: Efficient Automated Knowledge Graph Generation
for Language Models. In _2023 IEEE International Conference on Big Data (BigData)_,
pages 3117–3126, Los Alamitos, CA, USA, dec 2023. IEEE Computer Society. doi: 10.
1109/BigData59044.2023.10386454. URL `[https://doi.ieeecomputersociety.org/10.](https://doi.ieeecomputersociety.org/10.1109/BigData59044.2023.10386454)`
`[1109/BigData59044.2023.10386454](https://doi.ieeecomputersociety.org/10.1109/BigData59044.2023.10386454)` .


[9] H. Chen, R. Pasunuru, J. Weston, and A. Celikyilmaz. Walking Down the Memory Maze:
Beyond Context Limit through Interactive Reading. _CoRR_, abs/2310.05029, 2023. doi:
10.48550/ARXIV.2310.05029. URL `[https://doi.org/10.48550/arXiv.2310.05029](https://doi.org/10.48550/arXiv.2310.05029)` .


[10] T. Chen, H. Wang, S. Chen, W. Yu, K. Ma, X. Zhao, H. Zhang, and D. Yu. Dense x retrieval:
What retrieval granularity should we use? _arXiv preprint arXiv:2312.06648_, 2023. URL
`[https://arxiv.org/abs/2312.06648](https://arxiv.org/abs/2312.06648)` .


[11] Y. Chen, S. Qian, H. Tang, X. Lai, Z. Liu, S. Han, and J. Jia. Longlora: Efficient fine-tuning of
long-context large language models. _arXiv:2309.12307_, 2023.


[12] Y. Chen, P. Cao, Y. Chen, K. Liu, and J. Zhao. Journey to the center of the knowledge neurons:
Discoveries of language-independent knowledge neurons and degenerate knowledge neurons.
_Proceedings of the AAAI Conference on Artificial Intelligence_, 38(16):17817–17825, Mar.
2024. doi: 10.1609/aaai.v38i16.29735. URL `[https://ojs.aaai.org/index.php/AAAI/](https://ojs.aaai.org/index.php/AAAI/article/view/29735)`
`[article/view/29735](https://ojs.aaai.org/index.php/AAAI/article/view/29735)` .


[13] G. Csárdi and T. Nepusz. The igraph software package for complex network research. 2006.
URL `[https://igraph.org/](https://igraph.org/)` .


11


[14] R. Das, A. Godbole, D. Kavarthapu, Z. Gong, A. Singhal, M. Yu, X. Guo, T. Gao, H. Zamani,
M. Zaheer, and A. McCallum. Multi-step entity-centric information retrieval for multihop question answering. In A. Fisch, A. Talmor, R. Jia, M. Seo, E. Choi, and D. Chen,
editors, _Proceedings of the 2nd Workshop on Machine Reading for Question Answering_, pages
113–118, Hong Kong, China, Nov. 2019. Association for Computational Linguistics. doi:
10.18653/v1/D19-5816. URL `[https://aclanthology.org/D19-5816](https://aclanthology.org/D19-5816)` .


[15] N. De Cao, W. Aziz, and I. Titov. Editing factual knowledge in language models. In M.-F.
Moens, X. Huang, L. Specia, and S. W.-t. Yih, editors, _Proceedings of the 2021 Conference on_
_Empirical Methods in Natural Language Processing_, pages 6491–6506, Online and Punta Cana,
Dominican Republic, Nov. 2021. Association for Computational Linguistics. doi: 10.18653/
v1/2021.emnlp-main.522. URL `[https://aclanthology.org/2021.emnlp-main.522](https://aclanthology.org/2021.emnlp-main.522)` .


[16] M. Ding, C. Zhou, Q. Chen, H. Yang, and J. Tang. Cognitive graph for multi-hop reading
comprehension at scale. In A. Korhonen, D. Traum, and L. Màrquez, editors, _Proceedings of_
_the 57th Annual Meeting of the Association for Computational Linguistics_, pages 2694–2703,
Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/
P19-1259. URL `[https://aclanthology.org/P19-1259](https://aclanthology.org/P19-1259)` .


[17] Y. Ding, L. L. Zhang, C. Zhang, Y. Xu, N. Shang, J. Xu, F. Yang, and M. Yang. Longrope:
Extending llm context window beyond 2 million tokens. _ArXiv_, abs/2402.13753, 2024. URL
`[https://api.semanticscholar.org/CorpusID:267770308](https://api.semanticscholar.org/CorpusID:267770308)` .


[18] D. Edge, H. Trinh, N. Cheng, J. Bradley, A. Chao, A. Mody, S. Truitt, and J. Larson. From
local to global: A graph rag approach to query-focused summarization. 2024. URL `[https:](https://arxiv.org/abs/2404.16130)`
`[//arxiv.org/abs/2404.16130](https://arxiv.org/abs/2404.16130)` .


[19] H. Eichenbaum. A cortical–hippocampal system for declarative memory. _Nature Reviews_
_Neuroscience_, 1:41–50, 2000. URL `[https://www.nature.com/articles/35036213](https://www.nature.com/articles/35036213)` .


[20] Y. Fang, S. Sun, Z. Gan, R. Pillai, S. Wang, and J. Liu. Hierarchical graph network for multihop question answering. In B. Webber, T. Cohn, Y. He, and Y. Liu, editors, _Proceedings of the_
_2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_, pages
8823–8838, Online, Nov. 2020. Association for Computational Linguistics. doi: 10.18653/v1/
2020.emnlp-main.710. URL `[https://aclanthology.org/2020.emnlp-main.710](https://aclanthology.org/2020.emnlp-main.710)` .


[21] Y. Fu. Challenges in deploying long-context transformers: A theoretical peak performance
analysis, 2024. URL `[https://arxiv.org/abs/2405.08944](https://arxiv.org/abs/2405.08944)` .


[22] Y. Fu, R. Panda, X. Niu, X. Yue, H. Hajishirzi, Y. Kim, and H. Peng. Data engineering for
scaling language models to 128k context, 2024.


[23] M. Geva, J. Bastings, K. Filippova, and A. Globerson. Dissecting recall of factual associations
in auto-regressive language models. In H. Bouamor, J. Pino, and K. Bali, editors, _Proceedings_
_of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP_
_2023, Singapore, December 6-10, 2023_, pages 12216–12235. Association for Computational
Linguistics, 2023. doi: 10.18653/V1/2023.EMNLP-MAIN.751. URL `[https://doi.org/](https://doi.org/10.18653/v1/2023.emnlp-main.751)`
`[10.18653/v1/2023.emnlp-main.751](https://doi.org/10.18653/v1/2023.emnlp-main.751)` .


[24] C. Gormley and Z. J. Tong. Elasticsearch: The definitive guide. 2015. URL `[https://www.](https://www.elastic.co/guide/en/elasticsearch/guide/master/index.html)`
`[elastic.co/guide/en/elasticsearch/guide/master/index.html](https://www.elastic.co/guide/en/elasticsearch/guide/master/index.html)` .


[25] T. L. Griffiths, M. Steyvers, and A. J. Firl. Google and the mind. _Psychological Science_, 18:
1069 – 1076, 2007. URL `[https://cocosci.princeton.edu/tom/papers/google.pdf](https://cocosci.princeton.edu/tom/papers/google.pdf)` .


[26] J.-C. Gu, H.-X. Xu, J.-Y. Ma, P. Lu, Z.-H. Ling, K.-W. Chang, and N. Peng. Model Editing
Can Hurt General Abilities of Large Language Models, 2024.


[27] Y. Gu, X. Deng, and Y. Su. Don’t generate, discriminate: A proposal for grounding language models to real-world environments. In A. Rogers, J. Boyd-Graber, and N. Okazaki,
editors, _Proceedings of the 61st Annual Meeting of the Association for Computational_
_Linguistics (Volume 1: Long Papers)_, pages 4928–4949, Toronto, Canada, July 2023.
Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.270. URL
`[https://aclanthology.org/2023.acl-long.270](https://aclanthology.org/2023.acl-long.270)` .


12


[28] W. Gurnee and M. Tegmark. Language models represent space and time. In _The Twelfth_
_International Conference on Learning Representations_, 2024. URL `[https://openreview.](https://openreview.net/forum?id=jE8xbmvFin)`
`[net/forum?id=jE8xbmvFin](https://openreview.net/forum?id=jE8xbmvFin)` .


[29] J. Han, N. Collier, W. Buntine, and E. Shareghi. PiVe: Prompting with Iterative Verification
Improving Graph-based Generative Capability of LLMs, 2023.


[30] T. H. Haveliwala. Topic-sensitive pagerank. In D. Lassner, D. D. Roure, and A. Iyengar, editors,
_Proceedings of the Eleventh International World Wide Web Conference, WWW 2002, May 7-11,_
_2002, Honolulu, Hawaii, USA_, pages 517–526. ACM, 2002. doi: 10.1145/511446.511513.
URL `[https://dl.acm.org/doi/10.1145/511446.511513](https://dl.acm.org/doi/10.1145/511446.511513)` .


[31] Q. He, Y. Wang, and W. Wang. Can language models act as knowledge bases at scale?, 2024.


[32] Z. He, L. Karlinsky, D. Kim, J. McAuley, D. Krotov, and R. Feris. CAMELot: Towards large
language models with training-free consolidated associative memory. In _First Workshop on_
_Long-Context Foundation Models @ ICML 2024_, 2024. URL `[https://openreview.net/](https://openreview.net/forum?id=VLDTzg1a4Y)`
`[forum?id=VLDTzg1a4Y](https://openreview.net/forum?id=VLDTzg1a4Y)` .


[33] X. Ho, A.-K. Duong Nguyen, S. Sugawara, and A. Aizawa. Constructing a multi-hop QA
dataset for comprehensive evaluation of reasoning steps. In D. Scott, N. Bel, and C. Zong,
editors, _Proceedings of the 28th International Conference on Computational Linguistics_, pages
6609–6625, Barcelona, Spain (Online), Dec. 2020. International Committee on Computational
Linguistics. doi: 10.18653/v1/2020.coling-main.580. URL `[https://aclanthology.org/](https://aclanthology.org/2020.coling-main.580)`
`[2020.coling-main.580](https://aclanthology.org/2020.coling-main.580)` .


[34] P.-L. Huguet Cabot and R. Navigli. REBEL: Relation extraction by end-to-end language
generation. In M.-F. Moens, X. Huang, L. Specia, and S. W.-t. Yih, editors, _Findings of the_
_Association for Computational Linguistics: EMNLP 2021_, pages 2370–2381, Punta Cana,
Dominican Republic, Nov. 2021. Association for Computational Linguistics. doi: 10.18653/
v1/2021.findings-emnlp.204. URL `[https://aclanthology.org/2021.findings-emnlp.](https://aclanthology.org/2021.findings-emnlp.204)`
`[204](https://aclanthology.org/2021.findings-emnlp.204)` .


[35] G. Izacard, M. Caron, L. Hosseini, S. Riedel, P. Bojanowski, A. Joulin, and E. Grave.
Unsupervised dense information retrieval with contrastive learning, 2021. URL `[https:](https://arxiv.org/abs/2112.09118)`
`[//arxiv.org/abs/2112.09118](https://arxiv.org/abs/2112.09118)` .


[36] G. Izacard, P. Lewis, M. Lomeli, L. Hosseini, F. Petroni, T. Schick, J. A. Yu, A. Joulin,
S. Riedel, and E. Grave. Few-shot learning with retrieval augmented language models. _ArXiv_,
abs/2208.03299, 2022. URL `[https://arxiv.org/abs/2208.03299](https://arxiv.org/abs/2208.03299)` .


[37] J. Jiang, K. Zhou, Z. Dong, K. Ye, X. Zhao, and J.-R. Wen. StructGPT: A general
framework for large language model to reason over structured data. In H. Bouamor,
J. Pino, and K. Bali, editors, _Proceedings of the 2023 Conference on Empirical Meth-_
_ods in Natural Language Processing_, pages 9237–9251, Singapore, Dec. 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.emnlp-main.574. URL
`[https://aclanthology.org/2023.emnlp-main.574](https://aclanthology.org/2023.emnlp-main.574)` .


[38] Z. Jiang, F. Xu, L. Gao, Z. Sun, Q. Liu, J. Dwivedi-Yu, Y. Yang, J. Callan, and G. Neubig.
Active retrieval augmented generation. In H. Bouamor, J. Pino, and K. Bali, editors, _Proceed-_
_ings of the 2023 Conference on Empirical Methods in Natural Language Processing_, pages
7969–7992, Singapore, Dec. 2023. Association for Computational Linguistics. doi: 10.18653/
v1/2023.emnlp-main.495. URL `[https://aclanthology.org/2023.emnlp-main.495](https://aclanthology.org/2023.emnlp-main.495)` .


[39] S. Kambhampati. Can large language models reason and plan? _Annals of the New York_
_Academy of Sciences_, 2024. URL `[https://nyaspubs.onlinelibrary.wiley.com/doi/](https://nyaspubs.onlinelibrary.wiley.com/doi/abs/10.1111/nyas.15125)`
`[abs/10.1111/nyas.15125](https://nyaspubs.onlinelibrary.wiley.com/doi/abs/10.1111/nyas.15125)` .


[40] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and
I. Stoica. Efficient memory management for large language model serving with pagedattention.
In _Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles_, 2023.


13


[41] M. Levy, A. Jacoby, and Y. Goldberg. Same task, more tokens: the impact of input length on
the reasoning performance of large language models, 2024.


[42] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis,
W.-t. Yih, T. Rocktäschel, S. Riedel, and D. Kiela. Retrieval-augmented generation for
knowledge-intensive NLP tasks. In _Proceedings of the 34th International Conference on_
_Neural Information Processing Systems_, NIPS ’20, Red Hook, NY, USA, 2020. Curran
Associates Inc. ISBN 9781713829546. URL `[https://dl.acm.org/doi/abs/10.5555/](https://dl.acm.org/doi/abs/10.5555/3495724.3496517)`
`[3495724.3496517](https://dl.acm.org/doi/abs/10.5555/3495724.3496517)` .


[43] R. Li and X. Du. Leveraging structured information for explainable multi-hop question
answering and reasoning. In H. Bouamor, J. Pino, and K. Bali, editors, _Findings of the_
_Association for Computational Linguistics: EMNLP 2023_, pages 6779–6789, Singapore, Dec.
2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-emnlp.452.
URL `[https://aclanthology.org/2023.findings-emnlp.452](https://aclanthology.org/2023.findings-emnlp.452)` .


[44] S. Li, X. Li, L. Shang, X. Jiang, Q. Liu, C. Sun, Z. Ji, and B. Liu. Hopretriever: Retrieve
hops over wikipedia to answer complex questions. _Proceedings of the AAAI Conference on_
_Artificial Intelligence_, 35:13279–13287, 05 2021. doi: 10.1609/aaai.v35i15.17568.


[45] T. Li, G. Zhang, Q. D. Do, X. Yue, and W. Chen. Long-context LLMs Struggle with Long
In-context Learning, 2024.


[46] Z. Li, N. Zhang, Y. Yao, M. Wang, X. Chen, and H. Chen. Unveiling the pitfalls of knowledge
editing for large language models. In _The Twelfth International Conference on Learning_
_Representations_, 2024. URL `[https://openreview.net/forum?id=fNktD3ib16](https://openreview.net/forum?id=fNktD3ib16)` .


[47] Y. Liu, X. Peng, T. Du, J. Yin, W. Liu, and X. Zhang. ERA-CoT: Improving chain-ofthought through entity relationship analysis. In L.-W. Ku, A. Martins, and V. Srikumar,
editors, _Proceedings of the 62nd Annual Meeting of the Association for Computational_
_Linguistics (Volume 1: Long Papers)_, pages 8780–8794, Bangkok, Thailand, Aug. 2024.
Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.476. URL
`[https://aclanthology.org/2024.acl-long.476](https://aclanthology.org/2024.acl-long.476)` .


[48] L. LUO, Y.-F. Li, R. Haf, and S. Pan. Reasoning on graphs: Faithful and interpretable
large language model reasoning. In _The Twelfth International Conference on Learning_
_Representations_, 2024. URL `[https://openreview.net/forum?id=ZGNWW7xZ6Q](https://openreview.net/forum?id=ZGNWW7xZ6Q)` .


[49] K. Meng, D. Bau, A. Andonian, and Y. Belinkov. Locating and editing factual associations in
gpt. In _Neural Information Processing Systems_, 2022.


[50] E. Mitchell, C. Lin, A. Bosselut, C. Finn, and C. D. Manning. Fast model editing at scale.
_ArXiv_, abs/2110.11309, 2021.


[51] E. Mitchell, C. Lin, A. Bosselut, C. D. Manning, and C. Finn. Memory-based model editing at
scale. _ArXiv_, abs/2206.06520, 2022.


[52] T. T. Nguyen, T. T. Huynh, P. L. Nguyen, A. W.-C. Liew, H. Yin, and Q. V. H. Nguyen. A
survey of machine unlearning. _arXiv preprint arXiv:2209.02299_, 2022.


[53] J. Ni, C. Qu, J. Lu, Z. Dai, G. Hernandez Abrego, J. Ma, V. Zhao, Y. Luan, K. Hall, M.W. Chang, and Y. Yang. Large dual encoders are generalizable retrievers. In Y. Goldberg,
Z. Kozareva, and Y. Zhang, editors, _Proceedings of the 2022 Conference on Empirical Methods_
_in Natural Language Processing_, pages 9844–9855, Abu Dhabi, United Arab Emirates, Dec.
2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.emnlp-main.669.
URL `[https://aclanthology.org/2022.emnlp-main.669](https://aclanthology.org/2022.emnlp-main.669)` .


[54] Y. Nie, S. Wang, and M. Bansal. Revealing the importance of semantic retrieval for machine
reading at scale. In K. Inui, J. Jiang, V. Ng, and X. Wan, editors, _Proceedings of the 2019_
_Conference on Empirical Methods in Natural Language Processing and the 9th International_
_Joint Conference on Natural Language Processing (EMNLP-IJCNLP)_, pages 2553–2566,
Hong Kong, China, Nov. 2019. Association for Computational Linguistics. doi: 10.18653/v1/
D19-1258. URL `[https://aclanthology.org/D19-1258](https://aclanthology.org/D19-1258)` .


14


[55] OpenAI. GPT-3.5 Turbo, 2024. URL `[https://platform.openai.com/docs/models/](https://platform.openai.com/docs/models/gpt-3-5-turbo)`
`[gpt-3-5-turbo](https://platform.openai.com/docs/models/gpt-3-5-turbo)` .


[56] S. Pan, L. Luo, Y. Wang, C. Chen, J. Wang, and X. Wu. Unifying large language models and
knowledge graphs: A roadmap. _IEEE Transactions on Knowledge and Data Engineering_,
pages 1–20, 2024. doi: 10.1109/TKDE.2024.3352100.


[57] J. Park, A. Patel, O. Z. Khan, H. J. Kim, and J.-K. Kim. Graph elicitation for guiding multi-step
reasoning in large language models, 2024. URL `[https://arxiv.org/abs/2311.09762](https://arxiv.org/abs/2311.09762)` .


[58] S. Park and J. Bak. Memoria: Resolving fateful forgetting problem through human-inspired
memory architecture. In _ICML_, 2024. URL `[https://openreview.net/forum?id=](https://openreview.net/forum?id=yTz0u4B8ug)`
`[yTz0u4B8ug](https://openreview.net/forum?id=yTz0u4B8ug)` .


[59] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin,
N. Gimelshein, L. Antiga, A. Desmaison, A. Köpf, E. Z. Yang, Z. DeVito, M. Raison,
A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang, J. Bai, and S. Chintala. Pytorch: An imperative
style, high-performance deep learning library. In H. M. Wallach, H. Larochelle, A. Beygelzimer, F. d’Alché-Buc, E. B. Fox, and R. Garnett, editors, _Advances in Neural Information_
_Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019,_
_NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada_, pages 8024–8035, 2019. URL
`[https://dl.acm.org/doi/10.5555/3454287.3455008](https://dl.acm.org/doi/10.5555/3454287.3455008)` .


[60] K. Pei, I. Jindal, K. C.-C. Chang, C. Zhai, and Y. Li. When to use what: An in-depth
comparative empirical analysis of OpenIE systems for downstream applications. In A. Rogers,
J. Boyd-Graber, and N. Okazaki, editors, _Proceedings of the 61st Annual Meeting of the_
_Association for Computational Linguistics (Volume 1: Long Papers)_, pages 929–949, Toronto,
Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.
acl-long.53. URL `[https://aclanthology.org/2023.acl-long.53](https://aclanthology.org/2023.acl-long.53)` .


[61] B. Peng, J. Quesnelle, H. Fan, and E. Shippole. Yarn: Efficient context window extension of
large language models, 2023.


[62] F. Petroni, T. Rocktäschel, S. Riedel, P. Lewis, A. Bakhtin, Y. Wu, and A. Miller. Language
models as knowledge bases? In K. Inui, J. Jiang, V. Ng, and X. Wan, editors, _Proceedings_
_of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th_
_International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)_, pages
2463–2473, Hong Kong, China, Nov. 2019. Association for Computational Linguistics. doi:
10.18653/v1/D19-1250. URL `[https://aclanthology.org/D19-1250](https://aclanthology.org/D19-1250)` .


[63] O. Press, M. Zhang, S. Min, L. Schmidt, N. Smith, and M. Lewis. Measuring and narrowing
the compositionality gap in language models. In H. Bouamor, J. Pino, and K. Bali, editors,
_Findings of the Association for Computational Linguistics: EMNLP 2023_, pages 5687–5711,
Singapore, Dec. 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.
findings-emnlp.378. URL `[https://aclanthology.org/2023.findings-emnlp.378](https://aclanthology.org/2023.findings-emnlp.378)` .


[64] O. Press, M. Zhang, S. Min, L. Schmidt, N. A. Smith, and M. Lewis. Measuring and narrowing
the compositionality gap in language models, 2023. URL `[https://openreview.net/](https://openreview.net/forum?id=PUwbwZJz9dO)`
`[forum?id=PUwbwZJz9dO](https://openreview.net/forum?id=PUwbwZJz9dO)` .


[65] L. Qiu, Y. Xiao, Y. Qu, H. Zhou, L. Li, W. Zhang, and Y. Yu. Dynamically fused graph
network for multi-hop reasoning. In A. Korhonen, D. Traum, and L. Màrquez, editors,
_Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_,
pages 6140–6150, Florence, Italy, July 2019. Association for Computational Linguistics. doi:
10.18653/v1/P19-1617. URL `[https://aclanthology.org/P19-1617](https://aclanthology.org/P19-1617)` .


[66] O. Ram, Y. Levine, I. Dalmedigos, D. Muhlgay, A. Shashua, K. Leyton-Brown, and
Y. Shoham. In-context retrieval-augmented language models. _Transactions of the Asso-_
_ciation for Computational Linguistics_, 11:1316–1331, 2023. doi: 10.1162/tacl_a_00605. URL
`[https://aclanthology.org/2023.tacl-1.75](https://aclanthology.org/2023.tacl-1.75)` .


15


[67] G. Ramesh, M. N. Sreedhar, and J. Hu. Single sequence prediction over reasoning graphs for
multi-hop QA. In A. Rogers, J. Boyd-Graber, and N. Okazaki, editors, _Proceedings of the 61st_
_Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_,
pages 11466–11481, Toronto, Canada, July 2023. Association for Computational Linguistics.
doi: 10.18653/v1/2023.acl-long.642. URL `[https://aclanthology.org/2023.acl-long.](https://aclanthology.org/2023.acl-long.642)`
`[642](https://aclanthology.org/2023.acl-long.642)` .


[68] M. Reid, N. Savinov, D. Teplyashin, D. Lepikhin, T. Lillicrap, J.-b. Alayrac, R. Soricut,
A. Lazaridou, O. Firat, J. Schrittwieser, et al. Gemini 1.5: Unlocking multimodal understanding
across millions of tokens of context. _arXiv preprint arXiv:2403.05530_, 2024. URL `[https:](https://arxiv.org/abs/2403.05530)`
`[//arxiv.org/abs/2403.05530](https://arxiv.org/abs/2403.05530)` .


[69] S. E. Robertson and S. Walker. Some simple effective approximations to the 2-poisson
model for probabilistic weighted retrieval. In W. B. Croft and C. J. van Rijsbergen, editors,
_Proceedings of the 17th Annual International ACM-SIGIR Conference on Research and_
_Development in Information Retrieval. Dublin, Ireland, 3-6 July 1994 (Special Issue of the_
_SIGIR Forum)_, pages 232–241. ACM/Springer, 1994. doi: 10.1007/978-1-4471-2099-5\_24.
URL `[https://link.springer.com/chapter/10.1007/978-1-4471-2099-5_24](https://link.springer.com/chapter/10.1007/978-1-4471-2099-5_24)` .


[70] K. Santhanam, O. Khattab, J. Saad-Falcon, C. Potts, and M. Zaharia. ColBERTv2: Effective
and efficient retrieval via lightweight late interaction. In M. Carpuat, M.-C. de Marneffe, and
I. V. Meza Ruiz, editors, _Proceedings of the 2022 Conference of the North American Chapter_
_of the Association for Computational Linguistics: Human Language Technologies_, pages 3715–
3734, Seattle, United States, July 2022. Association for Computational Linguistics. doi: 10.
18653/v1/2022.naacl-main.272. URL `[https://aclanthology.org/2022.naacl-main.](https://aclanthology.org/2022.naacl-main.272)`
`[272](https://aclanthology.org/2022.naacl-main.272)` .


[71] P. Sarthi, S. Abdullah, A. Tuli, S. Khanna, A. Goldie, and C. D. Manning. RAPTOR:
recursive abstractive processing for tree-organized retrieval. _CoRR_, abs/2401.18059, 2024.
doi: 10.48550/ARXIV.2401.18059. URL `[https://arxiv.org/abs/2401.18059](https://arxiv.org/abs/2401.18059)` .


[72] Z. Shao, Y. Gong, Y. Shen, M. Huang, N. Duan, and W. Chen. Enhancing retrieval-augmented
large language models with iterative retrieval-generation synergy. In H. Bouamor, J. Pino,
and K. Bali, editors, _Findings of the Association for Computational Linguistics: EMNLP_
_2023_, pages 9248–9274, Singapore, Dec. 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-emnlp.620. URL `[https://aclanthology.org/2023.](https://aclanthology.org/2023.findings-emnlp.620)`
`[findings-emnlp.620](https://aclanthology.org/2023.findings-emnlp.620)` .


[73] W. Shi, S. Min, M. Yasunaga, M. Seo, R. James, M. Lewis, L. Zettlemoyer, and W. tau Yih.
Replug: Retrieval-augmented black-box language models. _ArXiv_, abs/2301.12652, 2023. URL
`[https://api.semanticscholar.org/CorpusID:256389797](https://api.semanticscholar.org/CorpusID:256389797)` .


[74] J. Sun, C. Xu, L. Tang, S. Wang, C. Lin, Y. Gong, L. Ni, H.-Y. Shum, and J. Guo. Thinkon-graph: Deep and responsible reasoning of large language model on knowledge graph.
In _The Twelfth International Conference on Learning Representations_, 2024. URL `[https:](https://openreview.net/forum?id=nnVO1PvbTv)`
`[//openreview.net/forum?id=nnVO1PvbTv](https://openreview.net/forum?id=nnVO1PvbTv)` .


[75] T. J. Teyler and P. Discenna. The hippocampal memory indexing theory. _Behavioral neuro-_
_science_, 100 2:147–54, 1986. URL `[https://pubmed.ncbi.nlm.nih.gov/3008780/](https://pubmed.ncbi.nlm.nih.gov/3008780/)` .


[76] T. J. Teyler and J. W. Rudy. The hippocampal indexing theory and episodic memory: Updating the index. _Hippocampus_, 17, 2007. URL `[https://pubmed.ncbi.nlm.nih.gov/](https://pubmed.ncbi.nlm.nih.gov/17696170/)`
`[17696170/](https://pubmed.ncbi.nlm.nih.gov/17696170/)` .


[77] H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal. MuSiQue: Multihop questions
via single-hop question composition. _Trans. Assoc. Comput. Linguistics_, 10:539–554, 2022.
doi: 10.1162/TACL\_A\_00475. URL `[https://aclanthology.org/2022.tacl-1.31/](https://aclanthology.org/2022.tacl-1.31/)` .


[78] H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal. Interleaving retrieval with chainof-thought reasoning for knowledge-intensive multi-step questions. In A. Rogers, J. BoydGraber, and N. Okazaki, editors, _Proceedings of the 61st Annual Meeting of the Association for_
_Computational Linguistics (Volume 1: Long Papers)_, pages 10014–10037, Toronto, Canada,
July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.557.
URL `[https://aclanthology.org/2023.acl-long.557](https://aclanthology.org/2023.acl-long.557)` .


16


[79] C. Wang, X. Liu, Y. Yue, X. Tang, T. Zhang, C. Jiayang, Y. Yao, W. Gao, X. Hu, Z. Qi,
Y. Wang, L. Yang, J. Wang, X. Xie, Z. Zhang, and Y. Zhang. Survey on factuality in large
language models: Knowledge, retrieval and domain-specificity, 2023.


[80] J. Wang, Q. Sun, N. Chen, X. Li, and M. Gao. Boosting language models reasoning with
chain-of-knowledge prompting, 2023.


[81] X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and
D. Zhou. Self-consistency improves chain of thought reasoning in language models. In
_The Eleventh International Conference on Learning Representations_, 2023. URL `[https:](https://openreview.net/forum?id=1PL1NIMMrw)`
`[//openreview.net/forum?id=1PL1NIMMrw](https://openreview.net/forum?id=1PL1NIMMrw)` .


[82] Y. Wang, Y. Gao, X. Chen, H. Jiang, S. Li, J. Yang, Q. Yin, Z. Li, X. Li, B. Yin, J. Shang, and
J. Mcauley. MEMORYLLM: Towards self-updatable large language models. In R. Salakhutdinov, Z. Kolter, K. Heller, A. Weller, N. Oliver, J. Scarlett, and F. Berkenkamp, editors,
_Proceedings of the 41st International Conference on Machine Learning_, volume 235 of _Pro-_
_ceedings of Machine Learning Research_, pages 50453–50466. PMLR, 21–27 Jul 2024. URL
`[https://proceedings.mlr.press/v235/wang24s.html](https://proceedings.mlr.press/v235/wang24s.html)` .


[83] J. Wei, X. Wang, D. Schuurmans, M. Bosma, brian ichter, F. Xia, E. H. Chi, Q. V. Le, and
D. Zhou. Chain of thought prompting elicits reasoning in large language models. In A. H. Oh,
A. Agarwal, D. Belgrave, and K. Cho, editors, _Advances in Neural Information Processing_
_Systems_, 2022. URL `[https://openreview.net/forum?id=_VjQlMeSB_J](https://openreview.net/forum?id=_VjQlMeSB_J)` .


[84] Y. Wen, Z. Wang, and J. Sun. Mindmap: Knowledge graph prompting sparks graph of thoughts
in large language models. _arXiv preprint arXiv:2308.09729_, 2023.


[85] P. West, C. Bhagavatula, J. Hessel, J. Hwang, L. Jiang, R. Le Bras, X. Lu, S. Welleck, and
Y. Choi. Symbolic knowledge distillation: from general language models to commonsense
models. In M. Carpuat, M.-C. de Marneffe, and I. V. Meza Ruiz, editors, _Proceedings of_
_the 2022 Conference of the North American Chapter of the Association for Computational_
_Linguistics: Human Language Technologies_, pages 4602–4625, Seattle, United States, July
2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.naacl-main.341.
URL `[https://aclanthology.org/2022.naacl-main.341](https://aclanthology.org/2022.naacl-main.341)` .


[86] T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi, P. Cistac, T. Rault, R. Louf,
M. Funtowicz, J. Davison, S. Shleifer, P. von Platen, C. Ma, Y. Jernite, J. Plu, C. Xu, T. L.
Scao, S. Gugger, M. Drame, Q. Lhoest, and A. M. Rush. Huggingface’s transformers:
State-of-the-art natural language processing. _ArXiv_, abs/1910.03771, 2019. URL `[https:](https://arxiv.org/abs/1910.03771)`
`[//arxiv.org/abs/1910.03771](https://arxiv.org/abs/1910.03771)` .


[87] J. Xie, K. Zhang, J. Chen, R. Lou, and Y. Su. Adaptive chameleon or stubborn sloth: Revealing
the behavior of large language models in knowledge conflicts. In _The Twelfth International_
_Conference on Learning Representations_, 2024. URL `[https://openreview.net/forum?](https://openreview.net/forum?id=auKAUJZMO6)`
`[id=auKAUJZMO6](https://openreview.net/forum?id=auKAUJZMO6)` .


[88] W. Xiong, X. Li, S. Iyer, J. Du, P. Lewis, W. Y. Wang, Y. Mehdad, S. Yih, S. Riedel, D. Kiela,
and B. Oguz. Answering complex open-domain questions with multi-hop dense retrieval. In
_International Conference on Learning Representations_, 2021. URL `[https://openreview.](https://openreview.net/forum?id=EMHoBG0avc1)`
`[net/forum?id=EMHoBG0avc1](https://openreview.net/forum?id=EMHoBG0avc1)` .


[89] Z. Yang, P. Qi, S. Zhang, Y. Bengio, W. W. Cohen, R. Salakhutdinov, and C. D. Manning.
HotpotQA: A dataset for diverse, explainable multi-hop question answering. In E. Riloff,
D. Chiang, J. Hockenmaier, and J. Tsujii, editors, _Proceedings of the 2018 Conference_
_on Empirical Methods in Natural Language Processing, Brussels, Belgium, October 31 -_
_November 4, 2018_, pages 2369–2380. Association for Computational Linguistics, 2018. doi:
10.18653/V1/D18-1259. URL `[https://aclanthology.org/D18-1259/](https://aclanthology.org/D18-1259/)` .


[90] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao. ReAct: Synergizing reasoning and acting in language models. In _International Conference on Learning_
_Representations (ICLR)_, 2023.


17


[91] M. Yasunaga, A. Bosselut, H. Ren, X. Zhang, C. D. Manning, P. Liang, and J. Leskovec.
Deep bidirectional language-knowledge graph pretraining. In _Neural Information Processing_
_Systems (NeurIPS)_, 2022. URL `[https://arxiv.org/abs/2210.09338](https://arxiv.org/abs/2210.09338)` .


[92] O. Yoran, T. Wolfson, B. Bogin, U. Katz, D. Deutch, and J. Berant. Answering questions
by meta-reasoning over multiple chains of thought. In _The 2023 Conference on Empirical_
_Methods in Natural Language Processing_, 2023. URL `[https://openreview.net/forum?](https://openreview.net/forum?id=ebSOK1nV2r)`
`[id=ebSOK1nV2r](https://openreview.net/forum?id=ebSOK1nV2r)` .


[93] W. Yu, D. Iter, S. Wang, Y. Xu, M. Ju, S. Sanyal, C. Zhu, M. Zeng, and M. Jiang. Generate
rather than retrieve: Large language models are strong context generators. In _The Eleventh_
_International Conference on Learning Representations_, 2023. URL `[https://openreview.](https://openreview.net/forum?id=fB0hRu9GZUS)`
`[net/forum?id=fB0hRu9GZUS](https://openreview.net/forum?id=fB0hRu9GZUS)` .


[94] K. Zhang, B. Jimenez Gutierrez, and Y. Su. Aligning instruction tasks unlocks large language
models as zero-shot relation extractors. In A. Rogers, J. Boyd-Graber, and N. Okazaki,
editors, _Findings of the Association for Computational Linguistics: ACL 2023_, pages 794–812,
Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/
2023.findings-acl.50. URL `[https://aclanthology.org/2023.findings-acl.50](https://aclanthology.org/2023.findings-acl.50)` .


[95] N. Zhang, Y. Yao, B. Tian, P. Wang, S. Deng, M. Wang, Z. Xi, S. Mao, J. Zhang, Y. Ni,
et al. A comprehensive study of knowledge editing for large language models. _arXiv preprint_
_arXiv:2401.01286_, 2024.


[96] X. Zhang, Y. Chen, S. Hu, Z. Xu, J. Chen, M. K. Hao, X. Han, Z. L. Thai, S. Wang, Z. Liu,
and M. Sun. _∞_ bench: Extending long context evaluation beyond 100k tokens, 2024.


[97] Z. Zhong, Z. Wu, C. D. Manning, C. Potts, and D. Chen. Mquake: Assessing knowledge editing
in language models via multi-hop questions. In _Conference on Empirical Methods in Natural_
_Language Processing_, 2023. URL `[https://aclanthology.org/2023.emnlp-main.971.](https://aclanthology.org/2023.emnlp-main.971.pdf)`
`[pdf](https://aclanthology.org/2023.emnlp-main.971.pdf)` .


[98] S. Zhou, B. Yu, A. Sun, C. Long, J. Li, and J. Sun. A survey on neural open information
extraction: Current status and future directions. In L. D. Raedt, editor, _Proceedings of the_
_Thirty-First International Joint Conference on Artificial Intelligence, IJCAI-22_, pages 5694–
5701. International Joint Conferences on Artificial Intelligence Organization, 7 2022. doi:
10.24963/ijcai.2022/793. URL `[https://doi.org/10.24963/ijcai.2022/793](https://doi.org/10.24963/ijcai.2022/793)` . Survey
Track.


[99] H. Zhu, H. Peng, Z. Lyu, L. Hou, J. Li, and J. Xiao. Pre-training language model incorporating domain-specific heterogeneous knowledge into a unified representation. _Expert_
_Systems with Applications_, 215:119369, 2023. ISSN 0957-4174. doi: https://doi.org/10.1016/
j.eswa.2022.119369. URL `[https://www.sciencedirect.com/science/article/pii/](https://www.sciencedirect.com/science/article/pii/S0957417422023879)`
`[S0957417422023879](https://www.sciencedirect.com/science/article/pii/S0957417422023879)` .


[100] Y. Zhu, L. Pang, Y. Lan, H. Shen, and X. Cheng. Adaptive information seeking for opendomain question answering. In M.-F. Moens, X. Huang, L. Specia, and S. W.-t. Yih, editors,
_Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_,
pages 3615–3626, Online and Punta Cana, Dominican Republic, Nov. 2021. Association
for Computational Linguistics. doi: 10.18653/v1/2021.emnlp-main.293. URL `[https://](https://aclanthology.org/2021.emnlp-main.293)`
`[aclanthology.org/2021.emnlp-main.293](https://aclanthology.org/2021.emnlp-main.293)` .


18


**Appendices**


Within this supplementary material, we elaborate on the following aspects:


   - Appendix A: HippoRAG Pipeline Example

   - Appendix B: Dataset Comparison

    - Appendix C: Ablation Statistics

    - Appendix D: Intrinsic OpenIE Evaluation

   - Appendix E: Path-Finding Multi-Hop Case Study

    - Appendix F: Error Analysis

   - Appendix G: Cost and Efficiency Comparison

   - Appendix H: Implementation Details & Compute Requirements

   - Appendix I: LLM Prompts


19


Figure 3: **HippoRAG Pipeline Example (Question and Annotations). (Top)** We provide an
example question and its answer. **(Middle & Bottom)** The supporting and distractor passages for this
question. Two supporting passages are needed to solve this question. The excerpts of the distractor
passages are related to the “district” mentioned in the question.


**A** **HippoRAG Pipeline Example**


To better demonstrate how our HippoRAG pipeline works, we use the _path-following_ example from
the MuSiQue dataset shown in Table 7. We use HippoRAG’s indexing and retrieval processes to
follow this question and a subset of the associated corpus. The question, its answer, and its supporting
and distractor passages are as shown in Figure 3. The indexing stage is shown in Figure 4, showing
both the OpenIE procedure as well as the relevant subgraph of our KG. Finally, we illustrate the
retrieval stage in Figure 5, including query NER, query node retrieval, how the PPR algorithm
changes node probabilities, and how the top retrieval results are calculated.


20


Figure 4: **HippoRAG Pipeline Example (Indexing).** NER and OpenIE are sequentially conducted
on each passage of the corpus. Thus, an open knowledge graph is formed for the entire corpus. We
only show the relevant subgraph from the KG.


21


Figure 5: **HippoRAG Pipeline Example (Retrieval).** For retrieval, the named entities in the query
are extracted from the question **(Top)**, after which the query nodes are chosen using a retrieval
encoder. In this case, the name of the query named entity, “Alhandra”, is equivalent to its KG node.
**(Middle)** We then set the personalized probabilities for PPR based on the retrieved query nodes.
After PPR, the query node probability is distributed according to the subgraph in Figure 4, leading to
some probability mass on the node “Vila France de Xira”. **(Bottom)** These node probabilities are
then summed over the passages they appear in to obtain the passage-level ranking. The top-ranked
nodes after PPR are highlighted in the top-ranked passages.


22


**B** **Dataset Comparison**


To analyze the differences between the three datasets we use, we pay special attention to the quality of
the distractor passages, i.e., whether they can be effectively confounded with the supporting passages.
We use Contriever [ 35 ] to calculate the match score between questions and candidate passages and
show their densities in Figure 6. In an ideal case, the distribution of distractor scores should be
close to the mean of the support passage scores. However, it can be seen that the distribution of
the distractor scores in HotpotQA is much closer to the lower bound of the support passage scores
compared to the other two datasets.















Figure 6: Density of similarity scores of candidate passages (distractors and supporting passages)
obtained by Contriever. The similarity score of HotpotQA distractors is not substantially larger than
that of the least similar supporting passages, meaning that these distractors are not very effective.


**C** **Ablation Statistics**


We use GPT-3.5 Turbo, REBEL [ 34 ] and Llama-3.1 (8B and 70B) [ 1 ] for OpenIE ablation experiments.
As shown in Table 8, compared to both GPT-3.5 Turbo and both Llama models, REBEL generates
around half the number of nodes and edges. This illustrates REBEL’s lack of flexibility in open
information extraction when compared to using both open and closed-source LLMs. Meanwhile,
both Llama-3.1 versions produce a similar amount of OpenIE triples than GPT-3.5 Turbo.


Table 8: Knowledge graph statistics using different OpenIE methods.


**Model** **Count** **MuSiQue** **2Wiki** **HotpotQA**



GPT-3.5 Turbo (1106)

[55] (Default)


REBEL-large

[34]


Llama-3.1-8B-Instruct

[1]


Llama-3.1-70B-Instruct

[1]



# of Unique Nodes ( _N_ ) 91 _,_ 729 42 _,_ 694 82 _,_ 157
# of Unique Edges ( _E_ ) 21 _,_ 714 7 _,_ 867 17 _,_ 523
# of Unique Triples 107 _,_ 448 50 _,_ 671 98 _,_ 709
# of ColBERTv2 Synonym Edges ( _E_ _[′]_ ) 191 _,_ 636 82 _,_ 526 171 _,_ 856


# of Unique Nodes ( _N_ ) 36 _,_ 653 22 _,_ 146 30 _,_ 426
# of Unique Edges ( _E_ ) 269 211 262
# of Unique Triples 52 _,_ 102 30 _,_ 428 42 _,_ 038
# of ColBERTv2 Synonym Edges ( _E_ _[′]_ ) 48 _,_ 213 33 _,_ 072 39 _,_ 053


# of Unique Nodes ( _N_ ) 86 _,_ 864 37 _,_ 875 76 _,_ 311
# of Unique Edges ( _E_ ) 22 _,_ 807 6 _,_ 729 18 _,_ 109
# of Unique Triples 118 _,_ 430 47 _,_ 420 104 _,_ 981
# of ColBERTv2 Synonym Edges ( _E_ _[′]_ ) 155 _,_ 889 72 _,_ 963 139 _,_ 181


# of Unique Nodes ( _N_ ) 80 _,_ 634 39 _,_ 845 70 _,_ 304
# of Unique Edges ( _E_ ) 22 _,_ 120 6 _,_ 996 16 _,_ 404
# of Unique Triples 120 _,_ 514 55 _,_ 940 105 _,_ 281
# of ColBERTv2 Synonym Edges ( _E_ _[′]_ ) 140 _,_ 328 69 _,_ 125 119 _,_ 948



**D** **Intrinsic OpenIE Evaluation**


In order to better understand how OpenIE and retrieval interact, we extracted gold triples from 20
documents from the MuSiQue training dataset. In total, we extracted 239 gold triples. From the


23


results in Table 9, we first note that there is a massive difference between end-to-end information
extraction systems like REBEL and LLMs. Additionally, we note that there is some correlation
better OpenIE and retrieval performance, given that the 8B Llama-3.1-Instruct version performs
worse that its 70B counterpart in both retrieval and intrinsic metrics. More specifically, we see that
this larger model only provides intrinsic improvements in the recall metric, which seems specially
important in improving retrieval performance. Finally, we note that this evaluation is not perfectly
correlated with retrieval performance, since GPT-3.5’s intrinsic performance is much stronger than
Llama-3.1-70B-Instruct while its retrieval score is only slightly higher.


Table 9: Intrinsic OpenIE evaluation using the CaRB [6] framework on 20 annotated passages.


**AUC** **Precision** **Recall** **F1**


GPT-3.5 Turbo (1106) [55] (Default) 46 _._ 5 68 _._ 4 55 _._ 2 61 _._ 1
Llama-3.1-8B-Instruct [1] 40 _._ 0 66 _._ 4 48 _._ 1 55 _._ 8
Llama-3.1-70B-Instruct [1] 42 _._ 3 66 _._ 3 50 _._ 9 57 _._ 6
REBEL [34] 1 _._ 0 8 _._ 0 1 _._ 8 2 _._ 9


**E** **Case Study on Path-Finding Multi-Hop QA**


As discussed above, path-finding multi-hop questions across passages are exceedingly challenging
for single-step and multi-step RAG methods such as ColBERTv2 and IRCoT. These questions require
integrating information across multiple passages to find relevant entities among many possible
candidates, such as finding all Stanford professors who work on the neuroscience of Alzheimer’s.


**E.1** **Path-Finding Multi-Hop Question Construction Process**


These questions and the curated corpora around them were built through the following procedure.
The first two questions follow a slightly separate process as the third one as well as the motivating
example in the main paper. For the first two, we first identify a book or movie and then found the
book’s author or the movie’s director. We would then find 1) a trait for either the book/movie and 2)
another trait for the author/director. These two traits would then be used to extract distractors from
Wikipedia for each question.


For the third question and our motivating example, we first choose a professor or a drug at random as
the answer for each question. We then obtain the university the professor works at or the disease the
drug treats as well as one other trait for the professor or drug (in these questions research topic and
mechanism of action were chosen). In these questions, distractors were extracted from Wikipedia
using the University or disease on the one hand and the research topic or mechanism of action on
the other. This process, although quite tedious, allowed us to curate these challenging but realistic
path-finding multi-hop questions.


**E.2** **Qualitative Analysis**


In Table 10, we show three more examples from three different domains that illustrate HippoRAG’s
potential for solving retrieval tasks that require such cross-passage knowledge integration.


In the first question of Table 10, we want to find a book published in **2012** by an English author
who won a specific award. In contrast to HippoRAG, ColBERTv2 and IRCoT are unable to identify
**Mark Haddon** as such an author. ColBERTv2 focuses on passages related to awards while IRCoT
mistakenly decides that Kate Atkinson is the answer to such question since she won the same award
for a book published in 1995. For the second question, we wanted to find a war film based on a
non-fiction book directed by someone famous for sci-fi and crime movies. HippoRAG is able to find
our answer **Black Hawk Down** by **Ridley Scott** within the first four passages, while ColBERTv2
misses the answer completely and retrieves other films and film collections. In this instance, even
though IRCoT is able to retrieve Ridley Scott, it does so mainly through parametric knowledge. The
chain-of-thought output discusses his and Denis Villeneuve fame as well as their sci-fi and crime
experience. Given the three-step iteration restriction used here and the need to explore two directors,
the specific war film **Black Hawk Down** was not identified. Although a bit convoluted, people often


24


ask these first two questions to remember a specific movie or book they watched or heard about from
only a handful of disjointed details.


Finally, the third question is more similar to the motivating example in the main paper and shows
the importance of this type of question in real-world domains. In this question, we ask for a
drug used to treat lymphocytic leukemia through a specific mechanism (cytosolic p53 interaction).
While HippoRAG is able to leverage the associations within the supporting passages to identify
the **Chlorambucil** passage as the most important, ColBERTv2 and IRCoT are only able to extract
passages associated with lymphocytic leukemia. Interestingly enough, IRCoT uses its parametric
knowledge to guess that Venetoclax, which also treats leukemia, would do so through the relevant
mechanism even though no passage in the curated dataset explicitly stated this.


Table 10: Ranking result examples for different approaches on several path-finding multi-hop
questions.


**Question** **HippoRAG** **ColBERTv2** **IRCoT**



**1.** Kate Atkinson
**2.** Leon Garfield
Awards

**3.** Twelve Bar
Blues (novel)


**1. Ridley Scott**
**2.** Peter Hyams
**3.** Paul Greengrass
**4.** List of book-based
war films


**1.** Venetoclax
**2. Lymphocytic**
**leukemia**

**3.** Idelalisib



**1.** World Book Club

Prize winners
**2.** Leon Garfield
Awards

**3.** Twelve Bar
Blues (novel)


**1.** Paul Greengrass
**2.** List of book-based
war films
**3.** Korean War Films
**4.** All the King’s
Men Book


**1. Lymphocytic**
**leukemia**

**2.** Obinutuzumab

**3.** Venetoclax



Which book was
published in **2012** by an
**English** author who is a
**Whitbread Award**

winner?


Which **war film** based
on a **non fiction book**
was directed by someone
famous in the **science**
**fiction** and **crime**
**genres** ?


What drug is used to
treat **chronic**
**lymphocytic leukemia**
by interacting with
**cytosolic p53** ?


**F** **Error Analysis**


**F.1** **Overview**



**1.** Oranges Are
Not the Only Fruit
**2.** William Trevor
Legacies
**3. Mark Haddon**


**1.** War Film

**2.** Time de Zarn

**3.** Outline of Sci-Fi

**4. Black Hawk**

**Down**


**1. Chlorambucil**
**2. Lymphocytic**
**leukemia**
**3.** Mosquito bite
allergy



In this section, we provide a detailed error analysis of 100 errors made by HippoRAG on the MuSiQue
dataset. As shown in Table 11, these errors can be categorized into three main types: NER, OpenIE
and PPR.


The main error type, with nearly half of all error examples, is due to limitations of our NER based
design. As further discussed in §F.2, our NER design does not extract enough information from
the query for retrieval. For example, in the question “When was one internet browser’s version of
Windows 8 made accessible?”, only the phrase “Windows 8” is extracted, leaving any signal about
“browsers” or “accessibility” behind for the subsequent graph search. OpenIE errors, the second most
common, are discussed in more detail in §F.3.


We define the third error category as cases where both NER and OpenIE are functioning properly but
the PPR algorithm is still unable to identify relevant subgraphs, often due to confounding signals.
For instance, consider the query “How many refugees emigrated to the European country where
Huguenots felt a kinship for emigration?”. Despite the term “Huguenots” being accurately extracted
from both the question and the supporting passages, and the PPR algorithm initiating with the nodes
labeled “European” and “Huguenots”, the PPR algorithm struggles to find the appropriate subgraphs
around them that define the most related passage. This occurs when multiple passages exist in the
corpus that discuss very similar topics since the PPR algorithm is not able to leverage query context
directly.


25


Table 11: Error analysis on MuSiQue.


**Error Type** **Error Percentage** (%)


NER Limitation 48
Incorrect/Missing OpenIE 28
PPR 24


**F.2** **Concepts vs. Context Tradeoff**


Given our method’s entity-centric nature in extraction and indexing, it has a strong bias towards
concepts that leaves many contextual signals unused. This design enables single-step multi-hop
retrieval while also enabling contextual cues to avoid distracting from more salient entities. As seen
in the first example in Table 12, ColBERTv2 uses the context to retrieve passages that are related to
famous Spanish navigators but not “Sergio Villanueva”, who is a boxer. In contrast, HippoRAG is
able to hone in on “Sergio” and retrieve one relevant passage.


Unfortunately, this design is also one of our method’s greatest limitations since ignoring contextual
cues accounts for around 48 % of errors in our small-scale error analysis. This problem is more apparent in the second example since the concepts are general, making the context more important. Since
the only concept tagged by HippoRAG is “protons”, it extracts passages related to “Uranium” and
“nuclear weapons” while ColBERTv2 uses the context to extract more relevant passages associated
with the discovery of atomic numbers.


Table 12: Examples showing the concept-context tradeoff on MuSiQue.


**Question** **HippoRAG** **ColBERTv2**



Whose father was a navigator
who explored the east coast
of the continental region where
**Sergio Villanueva** would
later be born?


What undertaking included the
person who discovered that the
number of **protons** in each
element’s atoms is unique?



**Sergio Villanueva**
César Gaytan
Faustino Reyes


Uranium

Chemical element
History of nuclear weapons



Francisco de Eliza (navigator)
Exploration of N. America
Vicente Pinzón (navigator)


**Atomic number**
Atomic theory
Atomic nucleus



Table 13: **Single-step retrieval performance.** HippoRAG performs substantially better on MuSiQue
and 2WikiMultiHopQA than all baselines and achieves comparable performance on the less challenging HotpotQA dataset.


**Model** **Retriever** **MuSiQue** **2Wiki** **HotpotQA** **Average**


R@2 R@5 R@2 R@5 R@2 R@5 R@2 R@5


Contriever 34 _._ 8 46 _._ 6 46 _._ 6 57 _._ 5 57 _._ 2 75 _._ 5 46 _._ 2 59 _._ 9
Baseline
ColBERTv2 37 _._ 9 49 _._ 2 59 _._ 2 68 _._ 2 **64** _._ **7** 79 _._ 3 53 _._ 9 65 _._ 6


Contriever 41 _._ 0 52 _._ 1 71 _._ 5 **89** _._ **5** 59 _._ 0 76 _._ 2 57 _._ 2 72 _._ 6
HippoRAG
ColBERTv2 40 _._ 9 51 _._ 9 70 _._ 7 89 _._ 1 60 _._ 5 77 _._ 7 57 _._ 4 72 _._ 9


HippoRAG w/ Contriever 42 _._ 3 54 _._ 5 71 _._ 3 87 _._ 2 60 _._ 6 79 _._ 1 58 _._ 1 73 _._ 6
Uncertainty Ensemble ColBERTv2 **42** _._ **5** **54** _._ **8** **71** _._ **9** 89 _._ 0 62 _._ 5 **80** _._ **0** **59** _._ **0** **74** _._ **6**


To get a better trade-off between concepts and context, we introduce an ensembling setting where
HippoRAG scores are ensembled with dense retrievers when our parahippocampal region shows
uncertainty regarding the link between query and KG entities. This process represents instances
when no hippocampal index was fully activated by the upstream parahippocampal signal and thus
the neocortex must be relied on more strongly. We only use uncertainty ensembling if one of the
query-KG entity scores _cosine_ _ _similarity_ ( _M_ ( _c_ _i_ ) _, M_ ( _e_ _j_ )) is lower than a threshold _θ_, for example,
if there was no _Stanford_ node in the KG and the closest node in the KG is something that has a cosine
similarity lower than _θ_ such as _Stanford Medical Center_ . The final passage score for uncertainty


26


ensembling is the average of the HippoRAG scores and standard passage retrieval using model _M_,
both of which are first normalized into the 0 to 1 over all passages.


When HippoRAG is ensembled with _M_ under _“Uncertainty Ensemble”_, it further improves on
MuSiQue and outperforms our baselines in R@5 for HotpotQA, as shown in Table 13. When used in
combination with IRCoT, as shown in Table 14, the ColBERTv2 ensemble outperforms all previous
baselines in both R@2 and R@5 on HotpotQA. Although the simplicity of this approach is promising,
more work needs to be done to solve this context-context tradeoff since simple ensembling does
lower performance in some cases, especially for the 2WikiMultiHopQA dataset.


Table 14: **Multi-step retrieval performance.** Combining HippoRAG with standard multi-step
retrieval methods like IRCoT results in substantial improvements on all three datasets.


**Model** **Retriever** **MuSiQue** **2Wiki** **HotpotQA** **Average**


R@2 R@5 R@2 R@5 R@2 R@5 R@2 R@5


IRCoT Contriever 39 _._ 1 52 _._ 2 51 _._ 6 63 _._ 8 65 _._ 9 81 _._ 6 52 _._ 2 65 _._ 9

ColBERTv2 41 _._ 7 53 _._ 7 64 _._ 1 74 _._ 4 67 _._ 9 82 _._ 0 57 _._ 9 70 _._ 0


IRCoT + HippoRAG Contriever 43 _._ 9 56 _._ 6 75 _._ 3 93 _._ 4 65 _._ 8 82 _._ 3 61 _._ 7 77 _._ 4
ColBERTv2 **45** _._ **3** 57 _._ 6 **75** _._ **8** **93** _._ **9** 67 _._ 0 83 _._ 0 **62** _._ **7** 78 _._ 2


IRCoT + HippoRAG w/ Contriever 44 _._ 4 **58** _._ **5** 75 _._ 3 91 _._ 5 66 _._ 9 85 _._ 0 62 _._ 2 **78** _._ **3**
Uncertainty Ensemble ColBERTv2 40 _._ 2 53 _._ 4 74 _._ 5 91 _._ 2 **68** _._ **2** **85** _._ **3** 61 _._ 0 76 _._ 6


**F.3** **OpenIE Limitations**


OpenIE is a critical step in extracting structured knowledge from unstructured text. Nonetheless,
its shortcomings can result in gaps in knowledge that may impair retrieval and QA capabilities. As
shown in Table 15, GPT-3.5 Turbo overlooks the crucial song title “Don’t Let Me Wait Too Long”
during the OpenIE process. This title represents the most significant element within the passage. A
probable reason is that the model is insensitive to such a long entity. Besides, the model does not
accurately capture the beginning and ending years of the war, which are essential for the query. This
is an example of how models routinely ignore temporal properties. Overall, these failures highlight
the need to improve the extraction of critical information.


Table 15: Open information extraction error examples on MuSiQue.


**Question** **Passage** **Missed Triples**



(Don’t Let Me Wait
Too Long, sequenced
on, side one of the LP)


(Mexican-American
War, starts, 1846),
(Mexican-American
War, ends, 1848)



What company is the label responsible for “Don’t Let Me
Wait Too Long” a part of?


When did the president of the
Confederate States of America
end his fight in the MexicanAmerican war?



“Don’t Let Me Wait Too Long” was sequenced
on side one of the LP, between the ballads “The
Light That Has Lighted the World” and “Who
Can See It” ...


Jefferson Davis fought in the Mexican–American War (1846–1848), as the
colonel of a volunteer regiment ...



**F.4** **OpenIE Document Length Analysis**


Finally, we present a small-scale intrinsic experiment to help us understand the robustness of our
OpenIE methods to increasing passage length. The length-dependent evaluation results in Table 16,
show that GPT-3.5-Turbo OpenIE results deteriorate substantially when extracting from longer instead
of shorter passages. This is likely due to a higher sentence and paragraph complexity for longer
passages which leads to lower quality extraction. More work is needed to address this limitation since
further chunking would only create other issues due to sentence interdependence.


27


Table 16: Intrinsic OpenIE evaluation using the CaRB [ 6 ] framework. Performance difference
between the 10 longest and 10 shortest annotated passages using our default GPT-3.5 Turbo (1106)
model.


**AUC** **Precision** **Recall** **F1**


10 Shortest Passages 58 _._ 9 79 _._ 2 65 _._ 7 71 _._ 8
10 Longest Passages 39 _._ 0 60 _._ 7 48 _._ 5 53 _._ 9


**G** **Cost and Efficiency Comparison**


One of HippoRAG’s main advantages against iterative retrieval methods is the dramatic online
retrieval efficiency gains brought on by its single-step multi-hop retrieval ability in terms of both
cost and time. Specifically, as seen in Table 17, retrieval costs for IRCoT are 10 to 30 times higher
than HippoRAG since it only requires extracting relevant named entities from the query instead of
processing all of the retrieved documents. In systems with extremely high usage, a cost difference of
an order of magnitude such as this one could be extremely important. The difference with IRCoT in
terms of latency is also substantial, although more challenging to measure exactly. Also as seen in
Table 17, HippoRAG can be 6 to 13 times faster than IRCoT, depending on the number of retrieval
rounds that need to be executed (2-4 in our experiments). [6]


Table 17: Average cost and efficiency measurements for online retrieval using GPT-3.5 Turbo on
1 _,_ 000 queries.


**ColBERTv2** **IRCoT** **HippoRAG**


API Cost ($) 0 1-3 0 _._ 1
Time (minutes) 1 20-40 3


Although offline indexing time and costs are higher for HippoRAG than IRCoT—around 10 times
slower and $ 15 more expensive for every 10 _,_ 000 passages [7], these costs can be dramatically reduced
by leveraging open source LLMs. As shown in our ablation study in Table 5 Llama-3.1-70B-Instruct

[ 1 ] performs similarly to GPT-3.5 Turbo even though it can be deployed locally using vLLM [ 40 ]
and 4 H100 GPUs to index 10,000 documents in around 4 hours, as seen in Table 18. Additionally,
since these costs could be even further reduced by locally deploying this model, the barriers for using
HippoRAG at scale could be well within the computational budget of many organizations. Finally,
we note that even if LLM generation cost drops, the online retrieval efficiency gains discussed above
remain intact given that the number of tokens required for IRCoT vs. HippoRAG stay constant and
LLM use is likely to also remain the system’s main computational bottleneck.


Table 18: Average cost and latency measurements for offline indexing using GPT-3.5 Turbo and
locally deployed Llama-3.1 (8B and 70B) using vLLM on 10 _,_ 000 passages.


**Model** **Metric** **ColBERTv2** **IRCoT** **HippoRAG**


GPT-3.5 Turbo-1106 (Main Results) API Cost ($) 0 0 15
Time (minutes) 7 7 60


GPT-3.5 Turbo-0125 API Cost ($) 0 0 8
Time (minutes) 7 7 60


Llama-3.1-8B-Instruct API Cost ($) 0 0 0
Time (minutes) 7 7 120


Llama-3.1-70B-Instruct API Cost ($) 0 0 0
Time (minutes) 7 7 250


6 We use a single thread to query the OpenAI API for online retrieval in both IRCoT and HippoRAG. Since
IRCoT is an iterative process and each of the iterations must be done sequentially, these speed comparisons are
appropriate.
7 To speed up indexing, we use 10 threads querying _gpt-3.5-turbo-1106_ through the OpenAI API in parallel.
At the time of writing, the cost of the API is $1 for a million input tokens and $2 for a million output tokens.


28


**H** **Implementation Details & Compute Requirements**


Apart from the details included in §3.4, we use implementations based on PyTorch [ 59 ] and HuggingFace [ 86 ] for both Contriever [ 35 ] and ColBERTv2 [ 70 ]. We use the python-igraph [ 13 ]
implementation of the PPR algorithm. For BM25, we employ Elastic Search [ 24 ]. For multi-step
retrieval, we use the same prompt implementation as IRCoT [ 78 ] and retrieve the top- 10 passages at
each step. We set the maximum number of reasoning steps to 2 for HotpotQA and 2WikiMultiHopQA
and 4 for MuSiQue due to their maximum reasoning chain length. We combine IRCoT with different
retrievers by replacing its base retriever BM25 with each retrieval method, including HippoRAG,
noted as “IRCoT + HippoRAG” below. [8] For the QA reader, we use top- 5 retrieved passages as the
context and 1-shot QA demonstration with CoT prompting strategy [78].


In terms of compute requirements, most of our compute requirements are unfortunately not disclosed
by the OpenAI. We run ColBERTv2 and Contriever for indexing and retrieval we use 4 NVIDIA
RTX A6000 GPUs with 48GB of memory. For indexing with Llama-3.1 models, we use 4 NVIDIA
H100 GPUs with 80GB of memory. Finally, we used 2 AMD EPYC 7513 32-Core Processors to run
the Personalized PageRank algorithm.


**I** **LLM Prompts**


The prompts we used for indexing and query NER are shown in Figure 7 and Figure 8, while the
OpenIE prompt is shown in Figure 9.











Figure 7: Prompt for passage NER during indexing.


8 Since the original IRCoT does not provide a score for each retrieved passage, we employ beam search for
the iterative retrieval process. Each candidate passage maintains the highest historical score during beam search.


29


Figure 8: Prompt for query NER during retrieval.


30


Figure 9: Prompt for OpenIE during indexing.


31


