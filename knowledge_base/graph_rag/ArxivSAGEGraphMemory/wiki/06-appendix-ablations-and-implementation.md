> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix G–O: Ablations, Implementation, and Complexity of SAGE

**In one sentence:** With each major component of SAGE ablated or fixed in turn, the appendix shows that hybrid reward RL is the best writer, query planning and soft addressing are essential for fragmented-cue retrieval, structurally gated propagation beats uniform message passing, and the full system's training/inference costs stay within the same order as a standard GCN forward pass.

## Key points

- **Writer:** RL-Hybrid reward wins overall; "Hybrid + frozen answer API" gets the highest Deducible but slightly lower Retrievable Precision/Recall. Cross-dataset transfer works but target-domain continued-training still gives large gains (e.g. HaluMem Deducible rises 0.299 → 0.438).
- **Reader ablation (Table 8):** Full SAGE hits 65.1/77.6 R@2/R@5 (HotpotQA), 43.2/53.1 (MuSiQue), 83.6/88.6 (2WikiMultiHopQA). The weakest variants are Vanilla GNN Reader (57.2 R@2 HotpotQA, 72.8 R@2 2WikiMultiHopQA — 7.9 and 10.8 below SAGE), Anchor-only Initialization, and removal of Global Soft Addressing.
- **Structurally gated vs uniform propagation:** Removing the structural gate drops HotpotQA R@2 from 65.1 to 60.4 (−4.7); uniform message passing from 65.1 to 58.9 (−6.2). Both structural gate and uniform propagation outperform a vanilla GNN.
- **Selector:** The query-conditioned selector adds a soft gate π_e(q) ∈ (0,1) on top of the entity score a_e(q), with three regularizers (contrastive NCE, size penalty, connectivity/Laplacian smoothing). Added training cost is O(Bnd² + Bnd + B²d + Bm); inference cost reduces to O(Bnd) with cached node-side projection.
- **Complexity:** The core graph-propagation cost per batch is O(L(md + d²n)), where L is number of graph layers, d is hidden dimension, n is entities, m is edges. Entity-to-document projection via the entity–document matrix M costs O(B·nnz(M)) full or O(Bn·log K_e + BK_e·f̄) top-K_e. The chunked gating design reduces peak GPU memory from O(|E|d) to O(C_e·d) with C_e ≪ |E| edge-chunk size.
- **SFT objective:** L_ent = 0.3·L_bce + 0.7·L_list, where L_bce is weighted BCE on entity support masks and L_list is a multi-positive list cross-entropy that enforces collective top-ranking of supporting entities.
- **Pretraining:** GraphCL-style contrastive with two augmented views (edge perturbation, feature masking, node perturbation, subgraph sampling) plus one negative feature view, using a bilinear discriminator on node-vs-graph semantic matching.
- **Writer MDP:** Finite-horizon MDP with state (q, G_t, D_t^proc, D_t^rem, ζ_t); two legal actions — triple output or termination. Training is via VeRL's multi-turn GRPO. Iterative writing (default) decomposes long-context into per-document writing decisions.

---

## G — Analysis of the Memory Writer

This section keeps the reader fixed and varies the writer's reward function, training domain, and writing protocol. Metrics: **Precision**, **Recall** (both measure whether retrieved text covers gold supporting contexts), and **Deducible** (a judge decides whether the standard answer is inferable from the retrieved context, i.e. whether the graph memory is usable for reasoning).

### Table 6 — Cross-dataset memory writing results

"Base → Target" = direct evaluation after training on HotpotQA/MuSiQue base. "Target train → val" = training and validation on the target domain.

| Setting | Prec. ↑ | Recall ↑ | Deducible ↑ |
|---|---|---|---|
| Base → GRBench | 0.575 | 0.609 | 0.411 |
| GRBench train → val | **0.794** | **0.833** | **0.596** |
| Base → HaluMem | 0.230 | 0.448 | 0.299 |
| HaluMem train → val | 0.312 | **0.708** | **0.438** |
| Base → LongMemEval | 0.232 | 0.376 | 0.475 |
| LongMem train → LongMemEval | **0.377** | **0.439** | **0.531** |

### Table 7 — Writing protocol ablation

| Setting | Prec. ↑ | Recall ↑ | Deducible ↑ |
|---|---|---|---|
| Tight = True | 0.836 | 0.806 | 0.515 |
| Tight = False | 0.845 | 0.851 | 0.506 |
| Iterative, 12 turns, tight | 0.852 | 0.829 | 0.516 |
| Iterative, 20 turns, tight | 0.835 | **0.881** | 0.522 |
| Iterative, 24 turns, loose | **0.863** | 0.826 | **0.531** |

**Interpretation:** Relaxing the tight prompt improves Recall but reduces Deducible (the writer writes more broadly but with less reasoning-relevant precision). Increasing iterative turns helps complete cross-document bridging paths; 20 turns tight gives the best Recall (0.881), while 24 turns loose gives the best Precision (0.863) and Deducible (0.531). The optimal tradeoff is domain- and budget-dependent.

## H — Ablation Study of the Memory Reader

All variants use the same writer-produced graph memory and retrieval budget. The ablation is organized around four questions:

1. Are structured query planning and global soft addressing necessary for recovering evidence from fragmented cues?
2. Does structurally gated propagation improve over uniform message passing?
3. Are cross-graph structural priors and target-graph calibration both needed?
4. Are reader training and entity-to-document projection important?

### Table 8 — Reader component ablation (document-level Recall %)

| Variant | HotpotQA R@2 | HotpotQA R@5 | MuSiQue R@2 | MuSiQue R@5 | 2WikiMultiHopQA R@2 | 2WikiMultiHopQA R@5 |
|---|---|---|---|---|---|---|
| **SAGE (full)** | **65.1** | **77.6** | **43.2** | **53.1** | **83.6** | **88.6** |
| w/o Structured Query Planning | 62.7 | 75.1 | 40.4 | 50.1 | 80.7 | 86.6 |
| w/o Global Soft Addressing | 59.3 | 72.5 | 37.6 | 47.4 | 75.9 | 83.1 |
| w/o Alias and Constraint Cues | 63.0 | 75.8 | 41.0 | 50.8 | 80.8 | 86.9 |
| w/ Anchor-only Initialization | 58.6 | 71.4 | 36.8 | 46.5 | 74.2 | 82.4 |
| w/o Structural Gate | 60.4 | 73.2 | 39.2 | 48.7 | 78.1 | 84.9 |
| w/o Node Structural Features | 62.1 | 74.8 | 40.5 | 50.0 | 80.0 | 86.0 |
| w/o Edge-pair Structural Features | 61.5 | 74.0 | 40.1 | 49.4 | 79.1 | 85.6 |
| w/o Graph-level Summary | 63.2 | 75.9 | 41.6 | 51.0 | 81.3 | 87.0 |
| w/ Uniform Message Passing | 58.9 | 71.8 | 37.5 | 46.9 | 75.3 | 82.9 |
| w/o Schema Prior Channel | 62.4 | 75.0 | 40.9 | 50.6 | 80.4 | 86.4 |
| w/o Context Calibration Channel | 61.8 | 74.3 | 40.0 | 49.8 | 79.5 | 85.9 |
| w/o Context–Schema Fusion | 60.7 | 73.5 | 39.1 | 48.6 | 77.8 | 84.7 |
| w/o Controlled Entity-to-Document Projection | 60.9 | 73.9 | 38.7 | 48.2 | 77.2 | 84.4 |
| w/o Query-conditioned Selector | 63.9 | 76.5 | 41.9 | 52.0 | 82.2 | 87.6 |
| w/ Vanilla GNN Reader | 57.2 | 70.6 | 36.3 | 45.2 | 72.8 | 80.7 |

**Key findings:**

- **Fragmented-cue retrieval:** Removing query planning, alias/constraint cues, or global soft addressing noticeably weakens performance, especially on MuSiQue and 2WikiMultiHopQA where evidence chains depend on implicit bridge entities. Global Soft Addressing removal causes the largest HotpotQA R@2 drop (−5.8).
- **Structural gating:** Gated propagation consistently outperforms uniform message passing (e.g. HotpotQA R@2: 65.1 vs 58.9). Node-level and edge-pair features are more important than graph-level summaries for recognizing hubs and bridges.
- **Context–schema decomposition:** Both the schema prior channel (transferable structural reading patterns) and the context calibration channel (adapting to the current graph) contribute. Removing either or their fusion hurts all three datasets.
- **Selector and projection:** The query-conditioned selector and entity-to-document projection are important. A vanilla GNN reader (no SAGE architecture) performs worst, confirming the benefit of the full design.
- **Supervised fine-tuning:** Essential for aligning the GFM reader with document-level evidence retrieval.

## I — Query-conditioned Subgraph Selection

### I.1 Query-conditioned Selection Probability

Given a query q and a graph G = (V, E), let h_e ∈ R^d be the entity node representation after GFM propagation, and z_q ∈ R^d be the query representation. The selector projects both into a selector space:

- u_e = W_n h_e, v_q = W_s z_q (Eq. 177)
- Selection logit: ζ_e(q) = u_e^T v_q / T_s (Eq. 178)
- Soft probability: π_e(q) = sigmoid(ζ_e(q)) (Eq. 179)
- Discrete subgraph at threshold τ_π: V_q = {e ∈ V | π_e(q) > τ_π}, E_q = {(u,v) ∈ E | u,v ∈ V_q} (Eq. 180)

The base entity score a_e(q) = h_e^T z_q (Eq. 181) is combined with the selector:

**a_final_e(q) = a_e(q) + λ_s ζ_e(q)** (Eq. 182), where λ_s ≥ 0 controls selector influence.

### I.2 Query–Subgraph Contrastive Regularizer (Eq. 183–184)

Soft subgraph representation: h̄_π(q) = Σ_e π_e(q) h_e / (Σ_e π_e(q) + ε) (Eq. 183). In-batch NCE loss: positive pair (h̄_π(q_i), z_{q_i}), negatives (h̄_π(q_i), z_{q_j}), j ≠ i, with temperature T_n and normalized dot-product similarity. This encourages the soft subgraph to semantically represent the query rather than just selecting high-frequency or high-centrality nodes.

### I.3 Size Regularizer (Eq. 185)

ℒ_size = |V|^{-1} Σ_e π_e(q) — the average selection probability. Pushes the model to select a smaller reading subgraph, but must be co-optimized with ℒ_nce and the main retrieval loss to avoid degenerating to selecting no nodes.

### I.4 Connectivity Smoothing Regularizer (Eq. 186–187)

ℒ_con = |E|^{-1} Σ_{(u,v)∈E} (π_u(q) − π_v(q))² (Eq. 186). In matrix form: ℒ_con ∝ π(q)^T L π(q) (Eq. 187), where L is the graph Laplacian — classical Laplacian smoothing. Encourages adjacent nodes to have similar selection probabilities so multi-hop paths remain usable.

### I.5 Selector Complexity

Training: O(Bnd² + Bnd + B²d + Bm) (Eq. 188), reducible to O(Bnd + B²d + Bm) with cached node-side projection (Eq. 189). Inference (logit fusion only, no regularizers): O(Bnd² + Bnd) or O(Bnd) with caching.

## J — Training and Inference Complexity

Let n = |V|, m = |E|, d = hidden dimension, L = number of propagation layers, B = batch size, M = number of pseudo-queries.

### J.1 Offline Structural Features and Indexing

- Degrees, avg neighbor degrees: O(n + m)
- Clustering coefficients / common neighbors: O(n + m + Σ_{(u,v)∈E} min{deg(u), deg(v)}) (Eq. 190), ≈ O(n+m) for sparse graphs, worst case O(n³)
- Storage: O(np_n + mp_e + p_g + nnz(M)) (Eq. 191), where p_n, p_e, p_g are small constants
- Precomputed once, reused across multiple queries on the same graph

### J.2 Structurally Gated GFM Forward

- Standard GCN layer: C_plain = O(nd² + m̃d) (Eq. 192), m̃ = m + n
- Gate generation: C_gate = O(np_n d_g + mp_e d_g + p_g d_g + m(4d_g h_g + h_g d)) (Eq. 194)
- Structurally gated layer: C_gated = O(nd² + m̃d + C_gate) (Eq. 195)
- Batch encoding: C_enc(B) = O(BL(ρ_plain C_plain + ρ_gated C_gated)) (Eq. 196)
- Simplified (B=1, M=0, no dual branch, constant-width gate MLP): O(L(md + d²n)) (Eq. 197)
  - md: edge-level messages, structural gating, sparse aggregation
  - d²n: node linear projections

### J.3 Entity Scoring, Selector, and Document Projection

- Entity scoring: C_score(B) = O(Bnd) (Eq. 199)
- Selector inference: C_sel,infer(B) = O(Bnd² + Bnd) (Eq. 200), ≈ O(Bnd) with caching
- Selector training: C_sel,train(B) = O(Bnd² + Bnd + B²d + Bm) (Eq. 201)
- Full document projection: C_doc,full(B) = O(B·nnz(M)) (Eq. 202)
- Top-K_e document projection: C_doc,topK(B) = O(Bn log K_e + BK_e f̄) (Eq. 203)
- Final top-K document ranking: O(BN_D log K) full or O(BN_cand log K) candidate pool

### J.4 Training Complexity

Loss computation (BCE, ranking, or ListCE): C_loss(B) = O(Bn) (Eq. 204).

- Without selector: C_train = O(κ_bw [C_enc(B) + C_score(B) + C_loss(B)]) (Eq. 205)
- With selector: C_train,sel = O(κ_bw [C_enc(B) + C_score(B) + C_loss(B) + C_sel,train(B)]) (Eq. 206)
- κ_bw ≈ 2–3 (backprop overhead)
- Document-level loss adds C_doc,full(B) or C_doc,topK(B)

### J.5 Inference Complexity

C_infer(q) = (M+1) C_enc(1) + C_score(1) + C_sel,infer(1) + C_doc(1) + C_fuse(M, K) (Eq. 207). Fusing M+1 sets of K candidates: C_fuse(M,K) = O((M+1)K log((M+1)K)) (Eq. 208).

### J.6 Space Complexity

- Offline graph storage: O(n + m + nnz(M) + np_n + mp_e + p_g) (Eq. 209)
- Training node activations: O(BLnd) (Eq. 210)
- Gated edge messages: O(md) if fully materialized, O(cd) with edge-chunk streaming (Eq. 211), c ≪ m
- Document scoring: O(BN_D) full, O(BK) or O(BK_e f̄) with candidate heap

### J.7 Complexity Comparison

SAGE's design advantage in the self-evolving loop: each evaluation of a candidate graph is a single or small number of GFM forward passes (O(L(md + d²n))), not multi-round LLM agentic search. This enables high-frequency comparison and optimization over many candidate memory graphs without paying LLM inference costs per evaluation.

## K — Structured Query Planning

### K.1 Notation

P_ω(q) = (E_exp, A, C_rel, C_hard, τ, {(q̃_m, α_m, t_m)}_{m=1}^M) where:
- **E_exp** — explicit entities (direct anchors)
- **A** — candidate aliases
- **C_rel** — relation clues (semantic relational network)
- **C_hard** — hard constraints (spatiotemporal, logical boundaries)
- **τ** — answer type (cognitive template)
- **q̃_m** — pseudo-queries (simulated recall)
- **α_m** — confidence
- **t_m** — intent

### K.2 Two-stage Planning: Extraction and Inference

P(q) = (E_exp, A, C_rel, C_hard, τ, {(q̃_m, α_m)}_{m=1}^M) (Eq. 212)

![Extractor and Inferer prompt templates](images/06-fig6-fig7-casestudy.png)

**Figure 6 — Extractor prompt template:**

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

**Figure 7 — Inferer prompt template:**

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

The Extractor pulls structured retrieval signals from the question; the Inferer converts those signals into at most M pseudo-queries with confidence scores. This two-stage decomposition lets the reader address fragmented cues and multi-hop bridge entities that a raw question would miss.

## L — Topological Structural Features

### L.1 Normalized Structural Graph (Eq. 213)

Structural features are computed on a binarized, undirected, self-loop-free adjacency: A_s = I[(A + A^T) > 0], diag(A_s) = 0. This avoids unstable topology statistics from direction-dependent relation extraction. Message propagation still uses the original directed/typed graph; these features serve only as gating conditions.

### L.2 Node-level Features (Eq. 214–216)

For node v with neighborhood N(v) and degree d_v:

**φ(v) = [log(1 + d_v), c_v, κ_v, d̄_{N(v)}]**

- log(1 + d_v): node frequency (log-scaled degree)
- c_v = 2T_v / [d_v(d_v − 1)] for d_v ≥ 2, else 0 (Eq. 215): local clustering coefficient
- κ_v: core number (core/peripheral position)
- d̄_{N(v)} = (1/d_v) Σ_{u∈N(v)} d_u for d_v > 0, else 0 (Eq. 216): average neighbor degree

These map to four RAG structural risks: over-propagation by hubs, redundant diffusion in clusters, ignored peripheral bridges, and scale mismatch between sparse and dense regions.

### L.3 Edge-pair Features (Eq. 217–218)

For edge (u, v): **ψ(u,v) = [|d_u − d_v|, CN(u,v), Jac(u,v)]** where CN = |N(u) ∩ N(v)| and Jac = |N(u) ∩ N(v)| / (|N(u) ∪ N(v)| + ε). Degree difference reflects cross-level connections; CN and Jacard reflect local community overlap. The gate uses these to distinguish intra-community aggregation edges from cross-community bridge edges.

### L.4 Graph-level Summary and Normalization (Eq. 219–221)

**r_G = [mean_v φ(v); std_v φ(v); dens(G)]** where dens(G) = 2m_s / [n(n−1)] for n ≥ 2. Normalized: r̄_G = (r_G − μ_r) / (σ_r + ε), with per-graph z-scoring of node/edge features.

### L.5 Gating Input Encoding (Eq. 222–226)

Each encoder E_n, E_p, E_g is a two-layer MLP. Concatenated gating input: **z_uv^[l] = [u_u^[l]; u_v^[l]; v_uv^[l]; r_G^[l]]**. Gate: **g_uv^[l] = 1 + δ tanh(MLP_g^[l](z_uv^[l]))**, with δ = 0.1 (Eq. 226). The MLP's last layer is zero-initialized so the gate starts at 1 (identity), and structural bias emerges gradually — a residual mechanism that prevents training instability early on.

### L.6 Message Propagation (Eq. 227–230)

GCN normalization: η_uv = 1 / √(d̃_u d̃_v) (Eq. 227), d̃_v = Σ_{u:(u,v)∈Ẽ} w_uv. Message: **m_{u→v}^[l] = η_uv g_uv^[l] ⊙ W^[l] h_u^[l−1]** (Eq. 228). Update: **h_v^[l] = σ(b^[l] + Σ_u m_{u→v}^[l])** (Eq. 229). Inter-layer residual: H^[l] ← H^[l] + H^[l−1] for l > 1 (Eq. 230). The residual (Eq. 230) and zero-initialized gate (Eq. 226) form a dual stability mechanism.

### L.7 Chunked Gating (Eq. 231–232)

Edges partitioned into B_e chunks, each of size ≤ C_e. Per chunk: compute gate → compute message → scatter_add → release gate tensor. GPU memory: O(C_e d) instead of O(|E|d), with C_e ≪ |E|. Time complexity remains O(|E|d). Critical for self-evolving loops where the same reader evaluates many candidate graphs.

## M — Pretraining (GraphCL)

### M.1 View Construction (Eq. 233)

From (G_0, X_0), construct two augmented views (G_j, X_j) = A_j(G_0, X_0), j ∈ {1,2}, and one negative feature view (G_0, X_−). Augmentation types: edge perturbation, feature masking, node perturbation, subgraph sampling.

### M.2 Graph-level Contrastive Loss (Eq. 234–237)

Encodings: H_j = f_θ(X_j, G_j). Graph readout: c_j = sigmoid(|V_j|^{-1} Σ_{v∈V_j} H_{j,v}) (Eq. 235). Bilinear discriminator: D(c, h) = h^T W_D c (Eq. 236). Loss: ℒ_GCL = (1/2)[BCE(D(c_1, H_0), 1) + BCE(D(c_1, H_−), 0) + BCE(D(c_2, H_0), 1) + BCE(D(c_2, H_−), 0)] (Eq. 237).

When edge-level gating is enabled, static structural prompts are neutralized (identity) to avoid competing structural modulations; structural bias is carried solely by the learned gate g_uv^[l].

### M.3 Feature Alignment Layer (Eq. 238)

Align(x) = Dropout(LayerNorm(PReLU(W_a x + b_a))). W_a initialized to identity, b_a to zero — approximately identity initially, absorbs inter-graph feature-scale differences after training.

## N — Supervised Fine-tuning Objective

### N.1 Entity-level Weighted BCE (Eq. 239–240)

ℒ_bce = (1/B) Σ_b [Σ_e w_{b,e} BCEWithLogits(a_{b,e}, y_{b,e})] / (Σ_e w_{b,e} + ε) (Eq. 239). Positive weights normalized within the positive set. Negative weights via adversarial temperature T_a: w_{b,e}^{−} = exp(a_{b,e}/T_a) / Σ_{v:y_{b,v}=0} exp(a_{b,v}/T_a) (Eq. 240). Focuses training on high-scoring hard negatives.

### N.2 Multi-positive List Cross-Entropy (Eq. 241–243)

p_{b,e} = sigmoid(a_{b,e}) / (Σ_v sigmoid(a_{b,v}) + ε) (Eq. 241). List loss: ℒ_list = −(1/|B⁺|) Σ_{b∈B⁺} [1/|Y_E(q_b)| Σ_{e∈Y_E(q_b)} log(p_{b,e} + ε)] (Eq. 242). Ensures supporting entities collectively rank near the top.

**Final objective: ℒ_ent = 0.3 · ℒ_bce + 0.7 · ℒ_list** (Eq. 243).

### N.3 Optional Document-level Supervision (Eq. 244)

If enabled: S̃_b = a_b^T M (Eq. 244), then compute BCE or list loss with document mask z_{b,i}. Useful when entity annotations are noisy but document support sets are reliable.

## O — Memory Writer Implementation (MDP)

### O.1 Multi-turn Graph Construction MDP (Eq. 245–254)

**MDP:** M = (S, A, P, R, ρ_0, H) (Eq. 245). Trained via VeRL's multi-turn GRPO loop.

**State at round t:** s_t = (q, G_t, D_t[proc], D_t[rem], ζ_t) (Eq. 246), where G_t is the current partially-written graph, D_t[proc]/D_t[rem] are processed/remaining documents, ζ_t is a stage control flag.

**Actions (Eq. 247):** a_t ∼ π_θ(·|s_t), two legal types:
1. **Triple action:** JSON array of {subject, relation, object} — facts T_t written this round.
2. **Termination action:** JSON object with terminal fields (answer, recall, precision, deducible, etc.).

**Transition (Eq. 248):**
| Condition | Next state |
|---|---|
| a_t is legal | (q, G_t ⊕ T_t, D_t[proc] ∪ {d_t}, D_t[rem] \ {d_t}, ζ_{t+1}) |
| a_t is illegal | (q, G_t, D_t[proc], D_t[rem], STOP) |
| a_t triggers reading | (q, G_t, D_t[proc], D_t[rem], RAG) |

Environment validates JSON with `json_repair`; illegal JSON during graph construction → zero reward + termination.

**Iterative vs non-iterative writing:**
- **Non-iterative:** model reads entire context D at once, outputs all triples.
- **Iterative (default):** documents processed in order; per round the model writes triples only for the current document. Final graph: G = ⊕_{i=1}^{m} T_i, where ⊕ is edge-set union with node deduplication.

Iterative mode decomposes long-context into local writing decisions and records explicit source-document edges for text-graph retrieval.

**Text-graph construction (Eq. 249–251):**
G = (V_e ∪ V_d, E_ee ∪ E_ed) (Eq. 249), where V_e = entity nodes, V_d = document nodes.
- E_ee = {(u, r, v) | (u, r, v) ∈ T} (Eq. 250)
- E_ed = {(u, source, d_i), (v, source, d_i) | (u, r, v) ∈ T_i} (Eq. 251)

In iterative mode, source edges are explicit. In non-iterative mode, a tokenizer-overlap heuristic maps triples to the most similar document.

**Frozen GFM retrieval environment:** Reader f_ϕ is fixed. Constructs:
1. Relation-edge index E (forward + reverse) with types r
2. Sparse entity-document matrix M ∈ {0,1}^{n×M}, M_ij = 1 iff entity e_i is in document d_j
3. Question entity mask m_q ∈ {0,1}^n (lexical match first, degree-ranked heuristic fallback)

Entity scores: s_e = f_ϕ(G, q, m_q; ϕ) ∈ R^n (Eq. 252).

**Document scoring (Eq. 253–254).** Let M_Top-k(s_e) denote masking that retains only the top-K entity scores, and w_idf the inverse-frequency weights by entity document frequency. The four document-scoring modes can be written uniformly as a piecewise definition of s̃_e (Eq. 253); the piece explicitly given is, for mode `idfrawtopk`, s̃_e = s_e ⊙ (M_Top-k(s_e) · w_idf), and for mode `idf_topk`, s̃_e = w_idf ⊙ M_Top-k(s_e). Document scores are then **s_d = M^T s̃_e** (Eq. 254), and Top-k(s_d) is taken as the retrieval result.

`init_entities_weight` also enabled: during GFM forward pass, 1/f(e) weight applied to high-frequency entities to suppress their dominance.

**Covers:** source lines 3710–5066 (Appendix G through O).
