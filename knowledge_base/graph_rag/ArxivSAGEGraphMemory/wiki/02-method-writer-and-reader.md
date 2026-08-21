> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Method: Memory Writer + Memory Reader (Sec 4, 4.1, 4.2)

**In one sentence:** SAGE couples a policy-based memory writer (trained with reader-aware GRPO rewards to emit compact, grounded triple graphs) with a Graph-Foundation-Model memory reader (structured query planning + soft addressing + gated structural propagation under a context/schema split), and alternates the two in a self-evolution loop whose writer update raises graph readability while the reader update cancels writer-induced distribution shift.

## Key points

- The pipeline has two stages: the writer *W*<sub>θ</sub> turns the query *q* and candidate historical fragments *D* into a heterogeneous graph memory *G*, and the reader *R*<sub>φ</sub> performs query-conditioned activation over *G* — soft-locates relevant entities, propagates evidence through relations, and projects entity-level activations back to memory fragments (Section 4).
- Writing is a sequential policy: state *s*<sub>t</sub> = (*q, D, G*<sub>t−1</sub>, *D*<sub>t−1</sub><sup>[proc]</sup>), action *a*<sub>t</sub> = entity–relation triples (*u, r, v*) plus source anchors (*u*, `source`, *d*); the reward is reader-aware (the writer is scored by how well the frozen reader can derive an answer and recover supporting text from the written graph), and the writer is updated with standard clipped GRPO (Section 4.1).
- The hybrid task reward is *r*<sub>task</sub> = (α*r*<sub>rec</sub> + β*r*<sub>pre</sub> + γ*r*<sub>ded</sub>)/(α+β+γ), where *r*<sub>rec</sub> rewards coverage of gold evidence *D*<sup>+</sup> by the reader's top-*k* set *P*<sub>k</sub>(*q, G*), *r*<sub>pre</sub> penalizes irrelevant evidence expansion, *r*<sub>ded</sub> = 1{Judge(*q, y | P*<sub>k</sub>(q, G)*`) = Yes`}, and an answer-level auxiliary *r*<sub>ans</sub> uses F1 against the answer alias set *Y*(y); a repetition penalty ρ<sub>rep</sub>(G) in the trajectory return stops the policy from inflating the graph with duplicate triples (Section 4.1).
- The reader is a Graph Foundation Model (GFM) — chosen because dense retrievers can't exploit entity roles/bridge paths and per-domain GNNs generalize poorly — and outputs *f*<sub>φ</sub>(*q, G, D*) = (*p*<sub>φ</sub>(e|q,G), *p*<sub>φ</sub>(d|q,G,D), *G*<sub>q</sub>): entity distribution, document distribution, and an interpretable retrieval subgraph, plus a lightweight query-conditioned subgraph selector (Section 4.2).
- Cognition-inspired query planning decomposes the query into associative probes *P*<sub>ω</sub>(*q*) = (E<sup>exp</sup>, A, C<sup>rel</sup>, C<sup>hard</sup>, τ, {(q̃<sub>m</sub>, α<sub>m</sub>, t<sub>m</sub>)})<sub>m=1..M</sub> to counter "tip-of-the-tongue" alias/bridging failures; soft addressing scores each entity with the six-term Eq. (1) (exact match, alias, max-probe embedding cosine, entity type, constraint consistency, NER cross-link), normalizes with temperature *T*₀, and seeds *h*<sub>e</sub><sup>(0)</sup> = *p*₀(e|q)·W<sub>q</sub>Emb(q) + W<sub>x</sub>**x**<sub>e</sub> (working memory ⊕ solidified long-term memory) (Section 4.2).
- A synapse-inspired edge-level vector gate **g**<sub>uv</sub><sup>[l]</sup> = 1 + δ·tanh(MLP<sub>g</sub><sup>[l]</sup>(**z**<sub>uv</sub><sup>[l]</sup>)) — built from node features φ(v), edge-pair features ψ(u,v), and a graph summary **r**<sub>G</sub> — enables three brain-like behaviors absent in PPR/community expansion: Inhibition of hub edges, preservation of long-distance bridge/association edges, and Habituation of redundant local edges (Section 4.2).
- Target-graph adaptation uses a context–schema decomposition: **H**(*q,G*) = **H**<sup>ctx</sup> + β<sub>sch</sub>**H**<sup>sch</sup>, where the gated context channel calibrates to the current writer-generated graph and the schema channel is a softmax-weighted mix of cross-graph structural prompt bases {**P**<sub>j</sub><sup>[l]</sup>}<sub>j=1..K</sub> retaining stable patterns (bridge nodes, community boundaries, core–periphery, noise short-circuits) (Section 4.2).
- Self-evolution alternates: freeze the reader and train the writer with retrieval-based rewards, then freeze the writer and retrain the reader on its new graphs (Algorithm 1); this is an approximate coordinate improvement over a joint memory-utility objective, and Proposition 1(iii) shows the reader output does not oscillate arbitrarily as the graph evolves under writer updates (Section 4.2).

---

## 4 Method (overview)

At a high level, SAGE builds a **self-evolving graph memory pipeline** (Figure 2). The memory writer *W*<sub>θ</sub> first transforms the query and candidate historical memory fragments into a heterogeneous graph memory *G*. The memory reader *R*<sub>φ</sub> then performs query-conditioned activation over *G*: it softly locates query-relevant entities, propagates evidence signals through relational structures, and projects the activated entity-level information back to memory fragments. The two components are then coupled in a writer–reader self-evolution loop (Section 4.2 below).

![Figure 2: SAGE's self-evolving pipeline — the memory writer W_θ turns the query and candidate memory fragments into graph G, and the memory reader R_φ activates entities, propagates evidence through the graph, and projects back to memory fragments.](images/02-fig2-pipeline.png)

*(The figure-description file for this image was empty in the source snapshot, so the caption above paraphrases the Section 4 overview in the chunk rather than figure-internal details that could not be verified.)*

## 4.1 Memory Writer: Graph Memory Writing via Reading Feedback

### Policy-based writing

The writer is modeled as a **sequential decision-making policy**. At step *t*:

- **State:** *s*<sub>t</sub> = (*q, D, G*<sub>t−1</sub>, *D*<sub>t−1</sub><sup>[proc]</sup>), where *G*<sub>t−1</sub> is the partially written graph and *D*<sub>t−1</sub><sup>[proc]</sup> is the set of already processed documents.
- **Action:** *a*<sub>t</sub> contains entity–relation triples (*u, r, v*) together with their **source anchors** (*u*, `source`, *d*) — i.e., each triple is grounded to the document it was extracted from (implementation details in Appendix O).

### Reader-aware writing reward

The writer's reward comes from the **task utility of its written graph after being accessed by the memory reader**: given the current graph *G*, the *frozen* reader returns evidence *P*<sub>k</sub>(*q, G*). Two complementary reward categories (inspired by Tsang et al., 2025):

1. **Deduction reward** — is the graph sufficient as a *knowledge carrier* to support deriving the answer?

   *r*<sub>ded</sub>(*q, y, G*) = 1{Judge(*q, y* | *P*<sub>k</sub>(q, G)*`) = Yes`}

2. **Recall / precision** — can the graph serve as a *knowledge index* to recover the supporting text?

   - *r*<sub>rec</sub>(*q, D*<sup>+</sup>, G*) = |*P*<sub>k</sub>(*q, G*)* ∩ *D*<sup>+</sup>| / |*D*<sup>+</sup>| (coverage of necessary evidence)
   - *r*<sub>pre</sub>(*q, D*<sup>+</sup>, G*) = |*P*<sub>k</sub>(*q, G*) ∩ *D*<sup>+</sup>| / |*P*<sub>k</sub>(*q, G*)*| (penalizes expansion of irrelevant evidence)

Additionally, to align with end-to-end QA, an **answer-level auxiliary reward**:

*r*<sub>ans</sub>(*q, y, G*) = max<sub>y′∈Y(y)</sub> F1(*y, y′*), where ŷ = LLM(*q, P*<sub>k</sub>(q, G)*) and *Y*(*y*) is the set of answer aliases.

In practice SAGE adopts a **hybrid task reward**:

*r*<sub>task</sub> = (α*r*<sub>rec</sub> + α'β*r*<sub>pre</sub> + γ*r*<sub>ded</sub>)/(α + β + γ)

*(the chunk's typesetting renders the numerator as `αr_rec + αβ r_pre + γ r_ded` over the denominator `α + β + γ`.)*

**Anti-redundancy.** To stop the policy from inflating graph size by stacking duplicate triples, SAGE defines a **repetition rate**

ρ<sub>rep</sub>(G) = (|T(G)| − |T<sub>uni</sub>(G)|) / |T(G)|

and derives the **trajectory return**

R(τ) = r<sub>task</sub>(τ) − λ<sub>rep</sub>·ρ<sub>rep</sub>(G<sub>τ</sub>) + λ<sub>fmt</sub> Σ<sub>t=1..|τ|</sub> r<sub>t</sub><sup>fmt</sup>

This directly addresses the phenomenon reported by HaluMem (Chen et al., 2025a): memory-system errors often originate *at extraction/time of writing*, not at the answering stage. The writer is updated with **standard clipped GRPO**.

## 4.2 Memory Reader: Memory Retrieval Based on Graph Foundation Model

**Why a GFM.** The reader must operate stably over a graph that the writer continuously updates. Dense retrievers learn only query–document semantic matching (can't exploit entity roles, bridge paths, cross-community dependencies); conventional GNN retrievers are tied to fixed graph distributions and generalize poorly across domains, users, and evolution stages. SAGE therefore uses a **Graph Foundation Model (GFM)** — its multi-graph pretraining gives transferable structural priors and lightweight calibration on new graphs (Luo et al., 2025; Zhang et al., 2025c). Formally the reader outputs an entity distribution, a document distribution, and an optional retrieval subgraph:

*f*<sub>φ</sub>(*q, G, D*) = ( *p*<sub>φ</sub>(e | q, G),  *p*<sub>φ</sub>(d | q, G, D),  *G*<sub>q</sub> )

where *p*<sub>φ</sub>(e|q,G) is the query-activated entity memory, *p*<sub>φ</sub>(d|q,G,D) the final retrieved textual evidence, and *G*<sub>q</sub> an interpretable retrieval path. A lightweight **query-conditioned subgraph selector** further yields a compact, query-aligned activated subgraph (Appendix I).

### Cognition-inspired Structured Query Planning

Human long-term-memory extraction is anchored by the brain's *automatic generation of multi-dimensional retrieval cues* from a vague final intention. SAGE applies the same idea: it stops treating the natural-language query as a single retrieval command and instead introduces a **planning function** *P*<sub>ω</sub> that simulates the brain's cue-reconstruction before "awakening" memory, decomposing the query into a set of rich associative probes:

*P*<sub>ω</sub>(*q*) = ( E<sup>exp</sup>, A, C<sup>rel</sup>, C<sup>hard</sup>, τ, {(q̃<sub>m</sub>, α<sub>m</sub>, t<sub>m</sub>)}<sub>m=1..M</sub> )

This multi-path concurrent awakening overcomes the **"tip-of-the-tongue phenomenon"** (alias alignment failures, missing bridging entities) and stitches together forgotten implicit relationships (Trivedi et al., 2023; Asai et al., 2023; Wu et al., 2025b; Zhang et al., 2025b). Full notation, prompt templates, and output schema are in Appendix K.

### Soft Addressing and Pre-activation of Memory Fragments

Cognitive neuroscience notes that human retrieval involves not just extracting exact matches but an *instinctive awakening of peripherally related memories* (**Semantic Priming**). SAGE treats the query-conditioned entry score *s*<sub>e</sub>(q) as a comprehensive assessment of stimulus intensity across different **Memory Engrams** — this is what the paper refers to as addressing its **first challenge**:

**Entry score (Eq. 1):**

s<sub>e</sub>(q) = λ₁ Exact(e, E<sup>exp</sup>) + λ₂ Alias(e, A) + λ₃ max<sub>m≤M</sub> cos( Emb(desc(e)), Emb(q̃<sub>m</sub>) ) + λ₄ Type(e, τ) + λ₅ Cons(e, C<sup>hard</sup>) + λ₆ Σ<sub>ξ∈NER(q)</sub> EL(e | ξ)

The **Softmax** over entities with temperature *T*₀ (simulating the brain's limited **Attention Allocation**) normalizes these multi-dimensional stimulus signals into the initial activation distribution of the "memory atlas":

p₀(e | q) = exp(s<sub>e</sub>(q)/T₀) / Σ<sub>v∈V_E</sub> exp(s<sub>v</sub>(q)/T₀)

From this the initial node state mixes the query-conditioned component with a static entity representation:

**h**<sub>e</sub><sup>(0)</sup> = p₀(e|q)·W<sub>q</sub>Emb(q) + W<sub>x</sub>**x**<sub>e</sub>

Here **x**<sub>e</sub> is the solidified **long-term memory** (static entity representation) and the query vector weighted by recall degree p₀(e|q) is the current **working memory** (task context).

### Synapse-inspired Structurally Conditioned Associative Propagation

To address the **second challenge** while avoiding indiscriminate diffusion, SAGE introduces **edge-level vector structural gating** in the GFM. Three structural features (Appendix L for definitions/normalization):

- **Node-level (Eq. 2):** φ(v) = ( log(1+d_v), c_v, κ_v, d̄_N(v) )
- **Edge-pair (Eq. 3):** ψ(u,v) = ( |d_u − d_v|, |N(u) ∩ N(v)|, Jaccard(N(u), N(v)) )
- **Graph-level summary (Eq. 4):** **r**_G = ( mean<sub>v∈V_E</sub> φ(v); std<sub>v∈V_E</sub> φ(v); dens(G) )

For the *l*-th layer, the **edge structural context** concatenates node and pair embeddings plus the graph summary:

**z**<sub>uv</sub><sup>[l]</sup> = [ E_n<sup>[l]</sup>(φ(u)); E_n<sup>[l]</sup>(φ(v)); E_p<sup>[l]</sup>(ψ(u,v)); E_g<sup>[l]</sup>(**r**_G) ]

which generates the **vector gate**

**g**<sub>uv</sub><sup>[l]</sup> = 1 + δ·tanh( MLP_g<sup>[l]</sup>(**z**<sub>uv</sub><sup>[l]</sup>) )

Let η<sub>uv</sub> be the normalized adjacency weight with self-loops. Message and node updates:

**m**<sub>u→v</sub><sup>[l]</sup> = η<sub>uv</sub> · **g**<sub>uv</sub><sup>[l]</sup> ⊙ W_(m<sup>[l]</sup>) **h**<sub>u</sub><sup>[l−1]</sup>

**h**<sub>v</sub><sup>[l]</sup> = LayerNorm( **h**<sub>v</sub><sup>[l−1]</sup> + PReLU( **b**<sup>[l]</sup> + Σ<sub>u∈N(v)</sub> **m**<sub>u→v</sub><sup>[l]</sup> ) )

Unlike heuristic path expansion, PPR walks, or community summarization (Edge et al., 2024; Guo et al., 2024; Wang & Han, 2025), this system can actively perform three brain-like behaviors:

1. **Inhibition** — suppress non-specific generalized memories (hub edges).
2. **Long-distance association capture** — preserve lateral-thinking/bridge edges across cognitive clusters.
3. **Habituation** — weaken redundant local edges.

**Signal–budget view (Proposition 1(i)).** Traditional query-dependent GNNs or PPR-style expansion can multi-hop propagate along graph structure, but the key issue is not expanding propagation range — it's preserving the *signal advantage* of query-relevant evidence over distractor noise under a limited top-*k* budget. Proposition 1(i) (Appendix B) summarizes: soft addressing improves the initial evidence activation; the structural gating preserves bridge/evidence paths while suppressing noisy neighborhoods; and controlled entity→document projection converts the entity-level advantage into more efficient document-level retrieval.

### Target Graph Calibration and Cross-graph Structural Priors

The writer continuously changes the memory graph per round — each *G* alters local topology and noise distribution, so the reader cannot rely on propagation patterns of a single fixed graph. It must **simultaneously adapt to the current target graph and retain cross-graph structural priors**. This motivates the **context–schema decomposition**, where Proposition 1(ii) (Appendix C/D) states: the *schema channel* provides the transferable structural prior, while the *context channel* corrects the target-graph residual induced by (current writer, current domain, entity granularity, local noise).

**Contextual calibration.** A feature prompt vector **p̃**_f* calibrates the query-activated input: h<sub>e</sub><sup>(0)</sup> = p̃_f ⊙ **h**<sub>e</sub><sup>(0)</sup>. The contextual channel then performs **gated propagation** on the current graph *G*:

**H**<sup>ctx</sup> = F_gate( **H̃**<sup>(0)</sup>, G; Θ_gate )

This captures the immediate structural state within the current memory graph.

**Schema prior channel.** In parallel, a set of cross-graph structural prompt bases {**P**<sub>j</sub><sup>[l]</sup>}<sub>j=1..K</sub> encodes the **stable reading habits** formed during multi-graph training. Per-layer attention over these bases:

ω<sub>j</sub><sup>[l]</sup> = softmax_j(a<sup>[l]</sup>/T_p),   **P**_schema<sup>[l]</sup> = Σ<sub>j=1..K</sub> ω<sub>j</sub><sup>[l]</sup> **P**<sub>j</sub><sup>[l]</sup>

Propagation over the schema prompts yields:

**H**<sup>sch</sup> = F_prompt( **H̃**<sup>(0)</sup>, G; { **P**_schema<sup>[l]</sup> }<sub>l=1..L</sub> )

**Final entity representation** jointly determined by current context and long-term schema:

**H**(*q, G*) = **H**<sup>ctx</sup> + β_sch **H**<sup>sch</sup>

- **H**<sup>ctx</sup> — context-dependent immediate recall state, adapting to the specific graph the current writer generated.
- **H**<sup>sch</sup> — memory schema formed across experiences, retaining ability to recognize stable patterns (bridge nodes, community boundaries, core–periphery structures, noise short-circuits).

### Reader Training

The reader is trained to learn **cross-graph transferable retrieval biases** in two stages:

1. **Structural contrastive pre-training** on multiple augmented graph views.
2. **Supervised fine-tuning** — the reader is trained to identify and rank supporting entities for each query using **weighted classification** and **multi-positive ranking** objectives.

Details in Appendices M and N.

### Writer–Reader Self-evolution

To address the **third challenge**, SAGE proposes a **self-evolution framework** detailed in **Algorithm 1**, where each iteration has two phases:

1. **Freeze the reader; train the writer** using the reader's retrieval results as the reward signal (Section 4.1 rewards).
2. **Generate new graphs with the updated writer; continue training the reader.**

**Theoretical interpretation.** This alternate process is an **approximate coordinate improvement over a joint memory utility**: the writer update improves graph readability, and the reader update reduces writer-induced graph distribution shift and reward bias. Full coordinate-improvement analysis, a **surrogate reward bias bound**, and single-sided update bottleneck analysis are in Appendix F. **Proposition 1(iii)** shows that even though each writer update changes the graph structure, the reader output **does not oscillate arbitrarily** with graph evolution. Full **training, inference, memory, and selector-regularizer complexity** analyses are in Appendix J.

**Covers:** SAGE Method, Section 4 (4.1 Memory Writer, 4.2 Memory Reader); source lines 226–442.
