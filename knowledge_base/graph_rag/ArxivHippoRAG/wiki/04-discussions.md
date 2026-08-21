> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Discussions: Ablations, Integration & Efficiency

**In one sentence:** HippoRAG's gains depend on closed/open LLM-based OpenIE (REBEL underperforms badly) and PPR (simple baselines are worse), and it uniquely retrieves all supporting passages in a single step — excelling at path-finding multi-hop questions — at a fraction of IRCoT's cost and latency.

## Key points

- Replacing GPT-3.5 OpenIE with REBEL causes large drops: average R@2 46.2 vs HippoRAG's 57.4 (e.g. MuSiQue R@2 31.7 vs 40.9); GPT-3.5 produces twice as many triples as REBEL, which is biased against triples with general concepts.
- Open-weight Llama-3.1 works as OpenIE: 70B-Instruct beats GPT-3.5 on 2/3 datasets (MuSiQue R@2 41.8, 2Wiki R@5 85.3) and stays competitive on 2Wiki; even 8B-Instruct is competitive everywhere except a substantial 2Wiki drop (R@2 62.5 vs 70.7).
- In a CaRB intrinsic evaluation on 239 gold triples from 20 MuSiQue examples, all LLMs (including Llama-3.1-Instruct, which underperforms GPT-3.5 slightly) vastly outperform REBEL.
- PPR beats both baselines on all three datasets: query-node-only (R_q) averages R@2 50.7 / R@5 56.2 and R_q & neighbors 42.2 / 59.2, vs HippoRAG 57.4 / 72.9; adding neighborhoods without PPR is even worse than query nodes alone.
- Node specificity strongly helps MuSiQue and HotpotQA with almost no change on 2Wiki (named-entity-heavy); synonymy edges have the largest effect on 2Wiki, suggesting noisy entity standardization helps there.
- Single-step multi-hop retrieval: the gap vs ColBERTv2 on all-recall (AR) grows from 3% (R@2) to 6% (R@5) on MuSiQue and from 20% to 38% on 2Wiki (AR@5 75.7 vs 37.1 on 2Wiki... precisely AR@5 75.7 vs 37.1), showing gains come from retrieving ALL supporting passages rather than partial retrieval on more questions.
- Path-finding multi-hop questions (e.g., "Which Stanford professor works on the neuroscience of Alzheimer's?") defeat both ColBERTv2 and IRCoT, while HippoRAG's association web retrieves Thomas Südhof's passages; the birthdate example (Alhandra → Vila de Xira as her place of birth → district) shows HippoRAG directly using an association standard RAG cannot.
- IRCoT also solves multi-hop retrieval but is 10–30× more expensive and 6–13× slower than HippoRAG in online retrieval.

---

## OpenIE Alternatives

To test whether a closed model like GPT-3.5 is essential, the authors replace the OpenIE module with the end-to-end OpenIE model REBEL [34] and the 8B/70B instruction-tuned Llama-3.1 models. Table 5 (row 2) shows REBEL causes large performance drops, underscoring the importance of LLM flexibility: GPT-3.5 produces twice as many triples as REBEL, revealing REBEL's bias against producing triples with general concepts and leaving many useful associations behind. A deeper analysis extracts 239 gold triples from 20 MuSiQue training examples and runs a small-scale intrinsic evaluation with the CaRB [6] framework: Llama-3.1-Instruct models underperform GPT-3.5 only slightly, but all LLMs vastly outperform REBEL (Appendix D).

Exact numbers (Table 5, R@2 / R@5):
- HippoRAG: MuSiQue 40.9/51.9, 2Wiki 70.7/89.1, HotpotQA 60.5/77.7, avg 57.4/72.9
- REBEL: 31.7/39.6, 63.1/76.5, 43.9/59.2, avg 46.2/58.4
- Llama-3.1-8B-Instruct: 40.8/51.9, 62.5/77.5, 59.9/75.1, avg 54.4/67.8
- Llama-3.1-70B-Instruct: 41.8/53.7, 68.8/85.3, 60.8/78.6, avg 57.1/72.5

Llama-3.1-8B is competitive with GPT-3.5 on all datasets except 2Wiki, where performance drops substantially; Llama-3.1-70B outperforms GPT-3.5 in two of three datasets and remains competitive on 2Wiki, offering a cheaper alternative for indexing large corpora (graph statistics in Appendix C).

## PPR Alternatives

To measure how much of HippoRAG's performance comes from PPR, the authors replace PPR output with (row 5) the query node probability [p]_n multiplied by node specificity values, and (row 6) a version that also distributes a small amount of probability to the direct neighbors of each query node. PPR is a much more effective method for including associations for retrieval on all three datasets than both baselines (HippoRAG avg R@2 57.4 / R@5 72.9 vs R_q-nodes-only 50.7/56.2 and R_q-nodes-&-neighbors 42.2/59.2). Notably, adding the neighborhood of R_q nodes without PPR is _worse_ than using the query nodes alone — so naively spreading probability to neighbors hurts rather than helps.

## Knowledge Integration Advantage

HippoRAG's major advantage over conventional RAG in multi-hop QA is performing multi-hop retrieval in a single step. Measured by the percentage of queries where ALL supporting passages are retrieved (all-recall, Appendix/Table 6), the gap vs ColBERTv2 grows from 3% (AR@2) to 6% (AR@5) on MuSiQue and from 20% (AR@2) to 38% (AR@5) on 2WikiMultiHopQA (ColBERTv2 25.1/37.1 vs HippoRAG 45.4/75.7). This shows large improvements come from obtaining all supporting documents, not partial retrieval on more questions.

The distinguishing mechanism is path-finding vs path-following (Table 7). In a path-following question ("In which district was Alhandra born?"), IRCoT performs perfectly by following the single path set by Alhandra's place of birth; HippoRAG also wins by directly using Vila de Xira's connection to Alhandra as her place of birth — an association not stated in Vila de Xira's passage — which standard RAG cannot exploit directly. In a path-finding question ("Which Stanford professor works on the neuroscience of Alzheimer's?"), many paths exist (via Stanford professors or via Alzheimer's neuroscience) and iterative retrieval struggles; both ColBERTv2 and IRCoT fail to retrieve the needed passages, while HippoRAG's web of associations in the hippocampal index plus graph search identifies Thomas Südhof as relevant and retrieves his passages — a question type that is trivial for informed humans but out of reach for current retrievers without further training.

## Efficiency

IRCoT can also solve multi-hop retrieval (Appendix G) but at a steep serving cost: it is 10–30 times more expensive and 6–13 times slower than HippoRAG in online retrieval — arguably the most important factor when serving end users.

**Covers:** Section 5 (Discussions), pages 10-13
