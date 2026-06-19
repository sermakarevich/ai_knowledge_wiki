# Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation

**Paper:** [Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation (Fu et al., 2025)](https://arxiv.org/abs/2604.12965)

## Human Readable TL;DR

Imagine a library with millions of books and a super-smart librarian who can find the perfect book for you -- but reading every book title takes too long. This paper teaches the librarian to mentally organize books into a tree of shelves and sections, so they can quickly navigate to the right shelf instead of scanning everything. As a bonus, the librarian also gets smarter over time by noticing which sections of the library each visitor frequents, without needing anyone to explicitly say "this is your favorite genre."

## TL;DR

This paper proposes HILL (Hierarchical Index Learning), a method for jointly learning a hierarchical tree index over item embeddings in a large-scale neural retrieval model (Meta's MoNN). The index uses cross-layer residual quantization to enable beam-search retrieval that is both fast and exact. A secondary discovery shows that intermediate nodes in the learned tree are high-quality data sources enabling "test-time training" -- fine-tuning the model during inference to adapt to distribution shifts without ground-truth labels. Deployed at Meta, a 2-layer stacked MoNN with HILL achieves +2.57% online ads metric gain at 3.9x vs. 24.6x infrastructure cost for the unindexed large model.

---

## Problem & Motivation

Deploying large-scale foundation retrieval models in industrial recommendation systems is prohibitively expensive. Scoring every user-item pair at query time is infeasible at billions of items. Existing workarounds -- offline pre-computation (stale results) and model distillation (weaker model) -- sacrifice either freshness or representational power. Traditional ANN indexes (e.g., FAISS flat search) are designed for simple embeddings and do not co-train with the complex neural networks used in modern foundation models, leading to suboptimal recall. The paper asks: can we learn an index that is native to the model's representation space, enables fast beam-search at serving time, and preserves retrieval exactness?

---

## Main Original Ideas

1. **Hierarchical Index Learning (HILL)** -- Jointly trains a hierarchical tree index alongside the foundation retrieval model (MoNN). Item embeddings are soft-assigned to learnable index-node embeddings via cross-attention; the model optimizes against a pseudo-item embedding constructed as a weighted sum over index nodes.

2. **Cross-Layer Residual Quantization** -- Builds a multi-layer tree by repeatedly quantizing the residual error between the original embedding and the reconstruction from the previous layer, capturing coarse-to-fine semantics from root to leaf.

3. **Training Stability Tricks** -- Three complementary techniques: (a) Softmax temperature scheduler transitioning from soft to hard assignments to close the train-serve gap; (b) FLOPs regularizer preventing cluster collapse; (c) linear warmup of index loss weight for stable early training.

4. **EM Approximation** -- A fast alternative that decouples index assignment (E-step via FAISS K-Means) from model training (M-step), useful for quick updates under compute constraints.

5. **Test-Time Training via Index Nodes** -- Intermediate nodes on the beam-search path from root to a relevant item act as implicit category labels. Pairing these nodes with the querying user generates new labeled examples for fine-tuning the pre-trained model at inference, improving adaptation to evolving distributions without explicit labels.

6. **Stacked MoNN Deployment** -- Multi-layer MoNN architecture where coarser index levels use more expressive MoNN blocks (MoNN Large) and finer levels use cheaper blocks (MoNN Small), balancing quality and cost across the retrieval funnel.

---

## Key Findings

| Model | NE Gain vs. TTSN | Recall Gain | Infra Cost |
|---|---|---|---|
| MoNN Small | -0.50% | +3.1% | 1.4x |
| MoNN Large | -0.89% | +6.5% | 24.6x |
| 2L MoNN (L+S) + HILL | **-0.97%** | **+6.0%** | **3.9x** |
| 3L MoNN + HILL | -1.07% | +6.7% | 5.7x |

- **Online A/B:** 2-layer stacked MoNN with HILL achieved **+2.57% ads metric gain** vs. MoNN Small baseline in Meta production.
- **Public benchmarks (Gowalla/Yelp2018/Amazon-Book):** HILL + NESCL outperformed all baselines (BPR, LightGCN, SimpleX, SGL-ED, MGDCF) on Recall@20 and NDCG@20.
- **Ablation:** Removing the temperature scheduler is the most damaging (-0.10% NE); balanced index distribution and warmup each contribute an additional ~0.03--0.05% NE.
- **EM approximation** stays within 0.04% NE of full HILL, making it a viable low-cost alternative.
- **Test-time training parameters:** depth $\phi_{DEP}=2$ and interest rate $\phi_{IR}=0.4$--$0.8$ (layer-dependent) give the best gains; going deeper introduces noise from generic high-level nodes.

---

## Suggestions & Future Directions

1. The authors express hope that systematic documentation of MoNN and HILL accelerates community research on next-generation foundational retrieval models.
2. The EM approximation is proposed as a practical path for production systems with strict latency budgets, with potential for further optimization.
3. Test-time training via index nodes opens a broader research question: can hierarchical indexes be used for continual/online learning in recommendation without any explicit label collection?
4. The stacked MoNN design suggests a general principle -- heterogeneous complexity across retrieval funnel layers -- worth exploring in other domains.

---

## Authors & Institutions

Dongqi Fu, Kaushik Rangadurai, Haiyu Lu, Yunchen Pu, Siyang Yuan, Minhui Huang, Yiqun Liu, Golnaz Ghasemiesfeh, Xingfeng He, Fangzhou Xu, Andrew Cui, Vidhoon Viswanathan, Lin Yang, Liang Wang, Jiyan Yang, Chonglin Sun -- all at **Meta, USA**.
