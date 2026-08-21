> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup & Retrieval/QA Results

**In one sentence:** HippoRAG — a knowledge-graph-backed retrieval method grounded in the hippocampal index theory — beats every single-step baseline on MuSiQue and 2WikiMultiHopQA, is complementary to the multi-step method IRCoT, and lifts QA F1 by up to 17% while running 10–30x cheaper than IRCoT.

## Key points

- Single-step: HippoRAG (Contriever) hits **2Wiki R@2 = 71.5** vs best baseline GTR 60.2 (+11) and **R@5 = 89.5** vs GTR 67.9 (+20); MuSiQue gains are ~3.
- Single-step best average: HippoRAG (ColBERTv2) **Avg R@2 = 57.4, R@5 = 72.9**, top on both average columns.
- HippoRAG wins on the two main multi-hop datasets (MuSiQue, 2Wiki) and is comparable on the weaker HotpotQA, where ColBERTv2 (R@2 64.7, R@5 79.3) still edges it out.
- HotpotQA lag is attributed to its lower knowledge-integration demands and a concept-context tradeoff (eased by ensembling, Appendix F.2); 2Wiki's entity-centric design suits HippoRAG best.
- Multi-step: IRCoT + HippoRAG (ColBERTv2) reaches **Avg R@5 = 78.2** vs IRCoT + ColBERTv2 70.0; 2Wiki R@5 jumps 93.9 vs 74.4 (~+18%).
- QA (ColBERTv2 backbone): IRCoT + HippoRAG F1 = Mut 33.3 (vs ColBERTv2 26.4, +3), 2Wiki 62.7 (vs 43.3, +17), HotpotQA 59.2 (+1).
- Single-step HippoRAG is on par with / outperforms IRCoT on QA while being **10–30x cheaper and 6–13x faster** (Appendix G).
- Hyperparameters (tuned on 100 MuSiQue train examples): synonymy threshold τ = 0.8, PPR damping factor = 0.5; performance is robust to them.

---

## Experimental Setup

### Datasets

Evaluated on two challenging multi-hop QA benchmarks, MuSiQue (answerable) and 2WikiMultiHopQA, plus HotpotQA (a weaker multi-hop test with many spurious signals). To limit cost, 1,000 questions are drawn from each validation set. Following IRCoT, all candidate passages (supporting + distractor) from the selected questions form a per-dataset retrieval corpus. Corpus and extracted-KG statistics (Table 1):

| Metric | MuSiQue | 2Wiki | HotpotQA |
|---|---|---|---|
| # of Passages (P) | 11,656 | 6,119 | 9,221 |
| # of Unique Nodes (N) | 91,729 | 42,694 | 82,157 |
| # of Unique Edges (E) | 21,714 | 7,867 | 17,523 |
| # of Unique Triples | 107,448 | 50,671 | 98,709 |
| # of Contriever Synonym Edges (E′) | 145,990 | 146,020 | 159,112 |
| # of ColBERTv2 Synonym Edges (E′) | 191,636 | 82,526 | 171,856 |

### Baselines

Single-step retrieval: BM25, Contriever, GTR, ColBERTv2, plus LLM-augmented methods Propositionizer (rewrites passages into propositions) and RAPTOR (constructs summary nodes). Multi-step retrieval: IRCoT.

### Metrics

Retrieval: recall@2 (R@2) and recall@5 (R@5). QA: exact match (EM) and F1.

### Implementation Details

Default LLM L = GPT-3.5-turbo-1106 (temperature 0); retriever M = Contriever or ColBERTv2. Two hyperparameters tuned on 100 MuSiQue train examples: synonymy threshold τ = 0.8 and PPR damping factor = 0.5 (the probability PPR restarts a random walk from the query nodes rather than continuing). HippoRAG is robust to these settings.

## Single-Step Retrieval Results

HippoRAG outperforms all methods — including LLM-augmented Propositionizer and RAPTOR — on MuSiQue and 2WikiMultiHopQA, and is competitive on HotpotQA. Gains of +11 / +20 on R@2 / R@5 for 2WikiMultiHopQA and ~3 on MuSiQue. Bold marks the best cell per column block.

| Method | MuSiQue R@2 | MuSiQue R@5 | 2Wiki R@2 | 2Wiki R@5 | HotpotQA R@2 | HotpotQA R@5 | Avg R@2 | Avg R@5 |
|---|---|---|---|---|---|---|---|---|
| BM25 [69] | 32.3 | 41.2 | 51.8 | 61.9 | 55.4 | 72.2 | 46.5 | 58.4 |
| Contriever [35] | 34.8 | 46.6 | 46.6 | 57.5 | 57.2 | 75.5 | 46.2 | 59.9 |
| GTR [53] | 37.4 | 49.1 | 60.2 | 67.9 | 59.4 | 73.3 | 52.3 | 63.4 |
| ColBERTv2 [70] | 37.9 | 49.2 | 59.2 | 68.2 | **64.7** | **79.3** | 53.9 | 65.6 |
| RAPTOR [71] | 35.7 | 45.3 | 46.3 | 53.8 | 58.1 | 71.2 | 46.7 | 56.8 |
| RAPTOR (ColBERTv2) | 36.9 | 46.5 | 57.3 | 64.7 | 63.1 | 75.6 | 52.4 | 62.3 |
| Proposition [10] | 37.6 | 49.3 | 56.4 | 63.1 | 58.7 | 71.1 | 50.9 | 61.2 |
| Proposition (ColBERTv2) | 37.8 | 50.1 | 55.9 | 64.9 | 63.9 | 78.1 | 52.5 | 64.4 |
| HippoRAG (Contriever) | **41.0** | **52.1** | **71.5** | **89.5** | 59.0 | 76.2 | **57.2** | 72.6 |
| HippoRAG (ColBERTv2) | 40.9 | 51.9 | 70.7 | 89.1 | 60.5 | 77.7 | **57.4** | **72.9** |

## Multi-Step Retrieval Results

IRCoT and HippoRAG are complementary: using HippoRAG as IRCoT's retriever keeps adding ~+4 R@5 on MuSiQue, +18 on 2WikiMultiHopQA, and +1 on HotpotQA.

| Method | MuSiQue R@2 | MuSiQue R@5 | 2Wiki R@2 | 2Wiki R@5 | HotpotQA R@2 | HotpotQA R@5 | Avg R@2 | Avg R@5 |
|---|---|---|---|---|---|---|---|---|
| IRCoT + BM25 (Default) | 34.2 | 44.7 | 61.2 | 75.6 | 65.6 | 79.0 | 53.7 | 66.4 |
| IRCoT + Contriever | 39.1 | 52.2 | 51.6 | 63.8 | 65.9 | 81.6 | 52.2 | 65.9 |
| IRCoT + ColBERTv2 | 41.7 | 53.7 | 64.1 | 74.4 | **67.9** | **82.0** | 57.9 | 70.0 |
| IRCoT + HippoRAG (Contriever) | 43.9 | 56.6 | 75.3 | 93.4 | 65.8 | 82.3 | 61.7 | 77.4 |
| IRCoT + HippoRAG (ColBERTv2) | **45.3** | **57.6** | **75.8** | **93.9** | 67.0 | **83.0** | **62.7** | **78.2** |

## Question Answering Results

QA reported on the best-performing retrieval backbone, ColBERTv2. Improved retrieval in both single-step (rows 1–3) and multi-step (rows 4–5) yields F1 gains of up to +3 (MuSiQue), +17 (2WikiMultiHopQA), and +1 (HotpotQA) with the same QA reader. Bold marks the best row.

| Retriever | MuSiQue EM | MuSiQue F1 | 2Wiki EM | 2Wiki F1 | HotpotQA EM | HotpotQA F1 | Avg EM | Avg F1 |
|---|---|---|---|---|---|---|---|---|
| None | 12.5 | 24.1 | 31.0 | 39.6 | 30.4 | 42.8 | 24.6 | 35.5 |
| ColBERTv2 | 15.5 | 26.4 | 33.4 | 43.3 | 43.4 | 57.7 | 30.8 | 42.5 |
| HippoRAG (ColBERTv2) | 19.2 | 29.8 | 46.6 | 59.5 | 41.8 | 55.0 | 35.9 | 48.1 |
| IRCoT (ColBERTv2) | 19.1 | 30.5 | 35.4 | 45.1 | 45.5 | 58.4 | 33.3 | 44.7 |
| IRCoT + HippoRAG (ColBERTv2) | **21.9** | **33.3** | **47.7** | **62.7** | **45.7** | **59.2** | **38.4** | **51.7** |

HippoRAG's QA improvements track its retrieval gains. Notably, single-step HippoRAG is on par with or outperforms IRCoT while being 10–30x cheaper and 6–13x faster during online retrieval (Appendix G).

**Covers:** Sections 3-4 (Experimental Setup, Results), pages 7-10
