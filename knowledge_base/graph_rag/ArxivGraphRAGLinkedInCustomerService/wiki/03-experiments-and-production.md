> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments and Production Results

**In one sentence:** The KG-enhanced RAG system beat the plain-text baseline by 77.6% in MRR and 0.32 in BLEU on the golden dataset, and in a live LinkedIn A/B deployment cut median issue resolution time by 28.6% (7h → 5h).

## Key points

- Retrieval: MRR jumps from 0.522 (baseline) to 0.927 (experiment) — a 77.6% relative improvement; Recall@3 rises from 0.640 to 1.000 and NDCG@3 from 0.520 to 0.946.
- Exact-hit retrieval also nearly perfect: Recall@1 goes 0.400 → 0.860 and NDCG@1 goes 0.400 → 0.860.
- Generation: BLEU 0.057 → 0.377 (+0.32), METEOR 0.279 → 0.613, ROUGE 0.183 → 0.546 — consistent gains across all answer-quality metrics.
- Production A/B test on LinkedIn's customer-service team (multiple product lines, random split): the tool-using group cut mean resolution time 40h → 15h, median (P50) 7h → 5h (−28.6%), and P90 87h → 47h.
- Both arms used the **same** GPT-4 LLM and the same E5 embedding model, isolating the KG-templated retrieval methodology as the differentiator.
- Evaluation used a curated "golden" dataset of typical queries, support tickets, and their authoritative solutions; retrieved context scored with MRR, Recall@K, NDCG@K, and generated answers scored against golden solutions with BLEU, ROUGE, METEOR.
- Conclusions: KG + RAG improves retrieval, answering accuracy, and overall service effectiveness; three future directions — automated graph-template extraction, dynamic KG updates from user queries, and applicability beyond customer service.

---

## Experiment Design

Evaluation used a curated "golden" dataset comprising typical customer queries, support tickets, and their authoritative solutions. The control group operated on conventional text-based embedding-based retrieval (EBR); the experimental group applied the paper's KG-templated RAG methodology. To keep the comparison fair, **both groups used the same LLM (GPT-4) and the same embedding model (E5)**, so the measured differences are attributable to the retrieval methodology itself.

Retrieval efficacy was measured with:
- **MRR (Mean Reciprocal Rank)** — average inverse rank of the initial correct response;
- **Recall@K** — likelihood that a relevant item appears within the top-K selections;
- **NDCG@K** — rank quality considering both position and pertinence of items.

Question-answering performance measured generated responses against the golden solutions using **BLEU**, **ROUGE**, and **METEOR** scores (standard n-gram-overlap and synonym-aware answer evaluation metrics).

## Results

**Table 1: Retrieval Performance**

| | MRR | Recall@K (K=1) | Recall@K (K=3) | NDCG@K (K=1) | NDCG@K (K=3) |
|---|---|---|---|---|---|
| Baseline | 0.522 | 0.400 | 0.640 | 0.400 | 0.520 |
| Experiment | 0.927 | 0.860 | 1.000 | 0.860 | 0.946 |

**Table 2: Question Answering Performance**

| | BLEU | METEOR | ROUGE |
|---|---|---|---|
| Baseline | 0.057 | 0.279 | 0.183 |
| Experiment | 0.377 | 0.613 | 0.546 |

The method shows consistent improvements across **all** metrics. Most strikingly, it surpasses the baseline by **77.6% in MRR** (0.522 → 0.927) and by **0.32 in BLEU** (0.057 → 0.377), substantiating superior retrieval efficacy and question-answering accuracy. The K=3 recall reaching 1.000 means the correct chunk was always retrieved within the top 3 for the graph-augmented system, versus only 64% for plain-text EBR.

## Production Deployment

LinkedIn's customer service team deployed the method covering **multiple product lines**. The team was split **randomly** into two groups: one used the system, the other continued with traditional manual methods.

**Table 3: Customer Support Issue Resolution Time**

| Group | Mean | P50 | P90 |
|---|---|---|---|
| Tool Not Used | 40 Hours | 7 Hours | 87 Hours |
| Tool Used | 15 hours | 5 hours | 47 hours |

The group using the system achieved significant gains, reducing the **median (P50) resolution time per issue by 28.6%** (7h → 5h), mean time from 40h to 15h, and the tail P90 from 87h to 47h — highlighting the system's effectiveness in enhancing real-world customer-service efficiency beyond offline metrics.

## Conclusions and Future Work

The paper concludes that integrating retrieval-augmented generation (RAG) with a knowledge graph (KG) significantly advances automated question answering for customer service: retrieval and answering metrics both improved, along with overall service effectiveness in the live deployment.

Three future-work directions are named:
1. **Automated graph-template extraction** — an automated mechanism for extracting graph templates, which would enhance system adaptability (templates are currently hand-crafted from support-ticket analysis).
2. **Dynamic KG updates** — investigating dynamic updates to the knowledge graph based on user queries to improve real-time responsiveness.
3. **Broader applicability** — exploring the system's applicability in other contexts beyond customer service.

**Covers:** pages 4-5 (Section 4 Experiment, Section 5 Production Use Case, Section 6 Conclusions and Future Work)
