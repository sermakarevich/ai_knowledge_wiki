> [[index|Wiki]] | [[summary|Summary]]

# HippoRAG — Digest

The whole paper at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction|Abstract & Introduction]]

**In one sentence:** HippoRAG mimics the hippocampal index in human memory by combining an LLM-built schemaless knowledge graph with Personalized PageRank, enabling single-step multi-hop retrieval that is 10–20× cheaper and 6–13× faster than iterative RAG like IRCoT while improving accuracy by up to 20%.

- Mammalian brains evolved long-term memory that integrates new experiences without catastrophic forgetting; LLMs lack an equivalent, continually updating memory, and RAG is the _de facto_ substitute because static models can be presented new knowledge without retraining (model editing [46] has limitations).
- Current RAG fails at knowledge integration across passage boundaries because each new passage is encoded in isolation; tasks such as scientific literature review, legal case briefing, and medical diagnosis require exactly this cross-passage integration, and even multi-hop QA requires joining information between passages.
- The paper defines _path-finding_ multi-hop questions (Figure 1) as the scenario where even perfectly executed multi-step RAG is insufficient: find a _Stanford_ professor who does _Alzheimer's_ research from a pool of passages describing potentially thousands of Stanford professors and Alzheimer's researchers — no passage co-mentions both, so isolated encoding cannot identify Prof. Thomas unless one passage mentions both traits.
- Inspiration is the hippocampal memory indexing theory of Teyler and Discenna [75]: the neocortex processes and stores memory representations, while the C-shaped hippocampus holds a _hippocampal index_ — interconnected indices pointing to neocortical memory units and storing the associations between them; retrieval then completes partial cues via this index (CA3 sub-region [76]).
- HippoRAG's design: (1) an LLM transforms the corpus into a schemaless knowledge graph (KG) acting as the artificial hippocampal index (offline indexing, analogous to neocortical memory encoding), (2) given a query, key concepts are identified, (3) Personalized PageRank (PPR) [30] runs on the KG seeded by the query concepts, exploring KG paths and surfacing relevant subgraphs — multi-hop reasoning in a single retrieval step.
- Headline results: ~3 and 20 points over current RAG methods [10, 35, 53, 70, 71] on MuSiQue [77] and 2WikiMultiHopQA [33]; single-step retrieval matches or beats iterative IRCoT [78] while being 10–30× cheaper and 6–13× faster (abstract states 10–20× cheaper); combining HippoRAG with IRCoT adds complementary gains of up to 4% and 20% on the same datasets and even improves on the easier HotpotQA.
- Code and data are available at https://github.com/OSU-NLP-Group/HippoRAG; the authors also provide a case study on _path-finding_ multi-hop QA showing the potential of their method and the limitations of current ones.

## 2. [[wiki/02-methodology|Detailed Methodology]]

**In one sentence:** HippoRAG builds an open knowledge graph offline (LLM-driven OpenIE triples plus retrieval-encoder synonymy edges) and performs online retrieval by seeding Personalized PageRank from query named entities linked to graph nodes, with node specificity providing a locally computable IDF-like bias over the whole memory-inspired pipeline.

- Offline indexing is a two-step, 1-shot LLM process over each passage: first extract named entities, then feed them into the OpenIE prompt to extract final triples (noun-phrase nodes N and relation edges E) that include concepts beyond named entities — a balance between generality and bias toward named entities.
- Synonymy edges E' are added between two nodes whose retrieval-encoder (M) representations have cosine similarity above a threshold τ, mimicking parahippocampal regions and aiding downstream pattern completion.
- Indexing defines a |N| × |P| matrix P counting how many times each noun phrase appears in each original passage.
- Online retrieval: the LLM (1-shot prompt) extracts query named entities C_q = {c_1, ..., c_n} (e.g. "Stanford", "Alzheimer's") from the query q; these are encoded by the same retrieval encoder M.
- Query nodes R_q = {r_1, ..., r_n} are the nodes r_i = e_k where k = argmax_j cosine_similarity(M(c_i), M(e_j)) — the highest-similarity KG nodes to each query entity.
- PPR is run over the KG (|N| nodes, |E| + |E'| edges) with a personalized start distribution n over N giving each query node equal probability and all other nodes zero; the resulting distribution n' over N is multiplied by the P matrix to obtain p, the per-passage ranking score used for retrieval.
- Node specificity is a neurobiologically plausible, local alternative to IDF: s_i = |P_i|^(−1), where P_i is the set of passages node i was extracted from; it is applied by multiplying each query node probability n by s_i before PPR, modulating the node's own and its neighborhood's probability (illustrated in Figure 2 by the Stanford logo being drawn larger than the Alzheimer's symbol).

## 3. [[wiki/03-experiments-results|Experimental Setup & Retrieval/QA Results]]

**In one sentence:** HippoRAG — a knowledge-graph-backed retrieval method grounded in the hippocampal index theory — beats every single-step baseline on MuSiQue and 2WikiMultiHopQA, is complementary to the multi-step method IRCoT, and lifts QA F1 by up to 17% while running 10–30x cheaper than IRCoT.

- Single-step: HippoRAG (Contriever) hits **2Wiki R@2 = 71.5** vs best baseline GTR 60.2 (+11) and **R@5 = 89.5** vs GTR 67.9 (+20); MuSiQue gains are ~3.
- Single-step best average: HippoRAG (ColBERTv2) **Avg R@2 = 57.4, R@5 = 72.9**, top on both average columns.
- HippoRAG wins on the two main multi-hop datasets (MuSiQue, 2Wiki) and is comparable on the weaker HotpotQA, where ColBERTv2 (R@2 64.7, R@5 79.3) still edges it out.
- HotpotQA lag is attributed to its lower knowledge-integration demands and a concept-context tradeoff (eased by ensembling, Appendix F.2); 2Wiki's entity-centric design suits HippoRAG best.
- Multi-step: IRCoT + HippoRAG (ColBERTv2) reaches **Avg R@5 = 78.2** vs IRCoT + ColBERTv2 70.0; 2Wiki R@5 jumps 93.9 vs 74.4 (~+18%).
- QA (ColBERTv2 backbone): IRCoT + HippoRAG F1 = MuSiQue 33.3 (vs ColBERTv2 26.4, +3), 2Wiki 62.7 (vs 43.3, +17), HotpotQA 59.2 (+1).
- Single-step HippoRAG is on par with / outperforms IRCoT on QA while being **10–30x cheaper and 6–13x faster** (Appendix G).
- Hyperparameters (tuned on 100 MuSiQue train examples): synonymy threshold τ = 0.8, PPR damping factor = 0.5; performance is robust to them.

## 4. [[wiki/04-discussions|Discussions: Ablations, Integration & Efficiency]]

**In one sentence:** HippoRAG's gains depend on closed/open LLM-based OpenIE (REBEL underperforms badly) and PPR (simple baselines are worse), and it uniquely retrieves all supporting passages in a single step — excelling at path-finding multi-hop questions — at a fraction of IRCoT's cost and latency.

- Replacing GPT-3.5 OpenIE with REBEL causes large drops: average R@2 46.2 vs HippoRAG's 57.4 (e.g. MuSiQue R@2 31.7 vs 40.9); GPT-3.5 produces twice as many triples as REBEL, which is biased against triples with general concepts.
- Open-weight Llama-3.1 works as OpenIE: 70B-Instruct beats GPT-3.5 on 2/3 datasets (MuSiQue R@2 41.8, 2Wiki R@5 85.3) and stays competitive on 2Wiki; even 8B-Instruct is competitive everywhere except a substantial 2Wiki drop (R@2 62.5 vs 70.7).
- In a CaRB intrinsic evaluation on 239 gold triples from 20 MuSiQue examples, all LLMs (including Llama-3.1-Instruct, which underperforms GPT-3.5 slightly) vastly outperform REBEL.
- PPR beats both baselines on all three datasets: query-node-only (R_q) averages R@2 50.7 / R@5 56.2 and R_q & neighbors 42.2 / 59.2, vs HippoRAG 57.4 / 72.9; adding neighborhoods without PPR is even worse than query nodes alone.
- Node specificity strongly helps MuSiQue and HotpotQA with almost no change on 2Wiki (named-entity-heavy); synonymy edges have the largest effect on 2Wiki, suggesting noisy entity standardization helps there.
- Single-step multi-hop retrieval: the gap vs ColBERTv2 on all-recall (AR) grows from 3% (R@2) to 6% (R@5) on MuSiQue and from 20% to 38% on 2Wiki (AR@5 75.7 vs 37.1), showing gains come from retrieving ALL supporting passages rather than partial retrieval on more questions.
- Path-finding multi-hop questions (e.g., "Which Stanford professor works on the neuroscience of Alzheimer's?") defeat both ColBERTv2 and IRCoT, while HippoRAG's association web retrieves Thomas Südhof's passages; the birthdate example (Alhandra → Vila de Xira as her place of birth → district) shows HippoRAG directly using an association standard RAG cannot.
- IRCoT also solves multi-hop retrieval but is 10–30× more expensive and 6–13× slower than HippoRAG in online retrieval.

## 5. [[wiki/05-related-work-conclusion|Related Work & Conclusions]]

**In one sentence:** HippoRAG stands apart from every memory-related approach to LLM long-term memory — because it integrates knowledge during offline indexing without the repeated-summarization cost of RAPTOR/MemWalker/GraphRAG and without the continual-learning weakness of parametric memory, and it is concluded to be a powerful, continuously updatable middle ground between standard RAG and parametric memory, though limited by off-the-shelf components and unproven scalability.

- LLM parameters encode a remarkable amount of world knowledge, but updating this store — an essential property of long-term memory — remains surprisingly limited, and no methodology has emerged as a robust continual-learning solution despite fine-tuning, model editing, and external parametric memory modules.
- RAG is a simple way to keep knowledge up to date over time, and multi-step RAG methods can integrate information across new or updated knowledge elements, but this online integration cannot solve complex tasks such as path-finding multi-hop QA where the search entities do not co-occur in any single passage (a condition often true for new information).
- RAPTOR, MemWalker, and GraphRAG integrate knowledge during the offline indexing phase like HippoRAG, but their reliance on summarizing knowledge elements means the summarization must be redone any time new data arrives — whereas HippoRAG integrates continuous new knowledge by simply adding edges to its KG.
- Long-context growth in open and closed LLMs suggests memory storage within massive context windows, but this future is uncertain due to engineering hurdles and apparent limitations of long-context models even at current lengths.
- Multi-hop QA work splits into graph-augmented reading comprehension (GNNs mixing hyperlink/co-occurrence signal with an LM, or injecting KG triples into LLM prompts — generation-level, complementary to HippoRAG's retrieval-level gains) and graph-augmented retrieval (re-rankers trained to traverse existing Wikipedia hyperlink graphs — whereas HippoRAG builds a KG from scratch with LLMs and does multi-hop retrieval without any supervision, making it much more adaptable).
- HippoRAG shows the synergy potential between LLMs and knowledge graphs predicted in the Pan et al. survey: combining LLM knowledge-graph construction with the retrieval strengths of structured knowledge for more effective RAG.
- Conclusion: HippoRAG, although simple, has a strong outlook for overcoming the limitations of standard RAG while retaining advantages over parametric memory, and is positioned as a powerful middle-ground framework for long-term memory in LLMs.
- Known limitations: all components are off-the-shelf with no additional training (the most errors stem from NER and OpenIE, where direct fine-tuning may pay off), graph search is simple PPR (relations do not guide traversal), OpenIE consistency degrades on longer documents, and Llama-3.1 scalability of the synthetic hippocampal index remains empirically unproven at sizes much larger than current benchmarks.

## 6. [[wiki/06-appendix-pipeline-errors|Appendix: Pipeline Walkthrough, Error Analysis & Prompts]]

**In one sentence:** This appendix traces one MuSiQue question end-to-end through HippoRAG's indexing (NER + OpenIE into a knowledge graph) and retrieval (query NER, node retrieval, PPR, passage ranking) stages, quantifies the error modes (NER 48%, OpenIE 28%, PPR 24%), and exposes the exact one-shot JSON prompts used for passage NER, query NER, and OpenIE.

- The worked example uses the MuSiQue path-following question "In which district was Alhandra born?" (answer: Lisbon), resolvable only by two jointly required supporting passages — Alhandra (footballer) and Vila Franca de Xira.
- Indexing runs NER then OpenIE sequentially on every passage, emitting (subject, relation, object) triples that are merged into a single open knowledge graph over the whole corpus; entities recurring across passages become shared nodes.
- Retrieval extracts named entities from the query, maps them to KG nodes with a retrieval encoder, runs personalized PageRank to spread seed probability through the subgraph, then sums node probabilities over their passages to rank passages.
- Contriever-scored similarity densities show HotpotQA's distractors are weak negatives (scoring near its least-similar supporting passages), while MuSiQue and 2WikiMultiHopQA distractors better confound the answer.
- Of 100 tracked HippoRAG errors on MuSiQue, 48% stem from NER limitations (too little query information extracted), 28% from incorrect/missing OpenIE triples, and 24% from PPR failing to find the right subgraph despite good NER and OpenIE.
- The entity-centric design has a concepts-vs-context tradeoff: it excels when one salient entity anchors the answer (e.g., "Sergio Villanueva") but loses on general-concepts questions where context matters (the "protons" example).
- A qualitative case study on path-finding multi-hop questions (book, film, drug lookups) shows HippoRAG chaining disjointed clues through the graph to find answers like Mark Haddon, Black Hawk Down, and Chlorambucil, where ColBERTv2 and IRCoT fail or guess via parametric knowledge instead.
- GPT-3.5 Turbo OpenIE quality degrades substantially on longer passages (F1 71.8 on the 10 shortest vs 53.9 on the 10 longest), hinting at extraction limits tied to passage complexity.
- HippoRAG retrieves 10–30× cheaper and 6–13× faster in online retrieval than IRCoT (query NER only, no per-document LLM processing), at the cost of higher offline indexing ($15 and ~60 min per 10,000 passages with GPT-3.5, reducible with locally deployed Llama-3.1).
- The LLM prompts are minimal one-shot, JSON-only templates for passage NER, query NER, and OpenIE, the latter requiring pronoun resolution and triple linkage to named entities.

## The argument in five moves

1. LLMs have no continually-updating long-term memory; RAG substitutes for it but encodes every passage in isolation, so it cannot connect facts that never co-occur in one passage.
2. Human long-term memory solves this via the hippocampus, which holds an index of associations linking pieces of knowledge stored in the neocortex — HippoRAG copies this structure with an LLM-built knowledge graph as the artificial index.
3. Retrieval becomes a graph walk: extract query entities, seed Personalized PageRank on the matching graph nodes, and let probability spread through associations to surface all relevant passages in one pass — no iterative retrieve-and-reread loop needed.
4. Empirically this beats every single-step baseline on multi-hop QA (MuSiQue, 2WikiMultiHopQA), matches the iterative method IRCoT while being an order of magnitude cheaper and faster online, and the two combine for further gains.
5. Ablations confirm both pillars matter: swapping the LLM-based OpenIE for a weaker extractor (REBEL) or PPR for simpler graph baselines both cause large recall drops.
6. The paper's own qualitative case studies show HippoRAG uniquely solving "path-finding" questions (where the answer entity connects two clue entities that never appear together) that defeat both dense retrievers and iterative RAG.
7. The tradeoff: everything is off-the-shelf and untuned, graph search ignores relation semantics, OpenIE degrades on long passages, and scaling the index far past current benchmark sizes remains unproven — HippoRAG is offered as a promising middle ground between static RAG and parametric memory, not a finished system.
