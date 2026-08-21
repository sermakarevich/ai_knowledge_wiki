**Technical summary**

This page (p. 44) is **not a quantitative plot** — it contains no data axes, curves, or trends. It is a methods appendix presenting two LLM prompt templates (Figures 6–7) and the formal definitions behind the topological structural features used by the model. Treat the numeric symbols (e.g., the cap *M*, the degree threshold *d_v ≥ 2*) as definitional/approximate rather than measured values.

**What it shows**

- **Figure 6 – Extractor prompt template.** A boxed system prompt for a "retrieval planner for graph‑based multi‑hop QA." Given a `{QUESTION}`, it instructs the model to return *JSON only* with five keys: `explicit_entities` (list of strings), `candidate_aliases` (entity→alias map), `relation_clues` (strings), `constraints` (map), and `answer_type` (string). Rule: keep entries short, no explanations, empty fields as `[]`/`{}`.
- **Figure 7 – Inferer prompt template.** A second boxed prompt that consumes the prior stage's output (`{EXTRACTOR_JSON}`) and generates **at most *M* retrieval intents** targeting: direct evidence for the target relation, bridge entities for multi‑hop reasoning, documents likely to hold the target attribute, constraint‑satisfying evidence (temporal/spatial/type/comparison/negation), and alias/alternative‑mention evidence. Output is *JSON only* with `pseudo_queries` (strings) and `rewriter_confidence` (numbers).
- **Section L – Computation of topological structural features.**
  - *L.1 Normalized structural graph (Eq. 213):* features are computed on an undirected, self‑loop‑free, binarized adjacency matrix, 𝒜_s = 𝟙[(𝒜 + 𝒜ᵀ) > 0] with diag(𝒜_s) = 0. Rationale: binarizing/symmetrizing avoids unstable topology statistics from extraction direction; the original directed/typed graph is still used for message passing, with these stats only as gating conditions.
  - *L.2 Node‑level features (Eq. 214):* for node *v* with degree *d_v* and neighborhood 𝒩(v), the feature vector is φ(v) = [log(1 + d_v), c_v, κ_v, d̄_{𝒩(v)}].
  - *Local clustering coefficient (Eq. 215):* c_v = 2T_v / [d_v(d_v − 1)] for d_v ≥ 2, else 0.

**Takeaway**

The figure documents the **two‑stage retrieval‑planning design** (an extractor that pulls structured signals → an inferer that turns them into a bounded set of pseudo‑queries with confidence) **plus the exact graph‑theoretic definitions** (symmetric binarized adjacency, log‑degree, clustering coefficient, degree, neighbor‑degree statistics) that the system uses as structural gating features. There are no empirical axes or trends here; the value is in specifying the prompts and the feature math reproducibly.