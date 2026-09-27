> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Retrieval Refinements: Term Vectors and Subclass Expansion
**In one sentence:** Raw prose windows embed to a blurred centroid that sits too far from terse ontology labels and drops borderline classes below the 0.72 floor, so each window is also queried as a compact proper-noun/abbreviation term vector with best-match-per-class scoring, and every class scoring ≥ 0.80 expands one subClassOf hop downward with children injected at 0.78.
## Key points
- A ~1,500-character prose window (e.g. "The SSP directed the 12th Battalion along the LoC during Operation Vijay . . .") embeds into an average over narrative prose, while a label such as Military Formation ("a body of troops organised for military purposes") has a clean, focused vector.
- The prose centroid sits measurably farther from the label than it should, so borderline classes slip under the cosine floor (0.72) and never reach the catalog.
- G1 extracts proper-noun phrases, abbreviations, and domain-adjacent terms into a pipe-delimited string ("12th Battalion | Operation Vijay | SSP | LoC") and embeds it as a second query vector.
- Every candidate class is scored against both vectors with `score(c) = max_{q in {e(w), e(terms(w))}} cos(q,c) × (1 − λ·pr(c))`, retaining the maximum, because term vectors match the terse register of ontology labels more tightly than running prose.
- Baseline vector retrieval systematically favours well-described general classes: if Organization retrieves at 0.85, the baseline injects it and only it.
- The model then emits Organization even when SecurityForce or TerroristGroup is the correct, more informative type.
- G2 treats a high-confidence match as evidence its children are worth showing: for every class with adjusted score ≥ 0.80, one Cypher hop down subClassOf injects the direct children at 0.78 (just above the floor, below their parent).
- The model then sees the specific options alongside the general one and can choose the tighter fit.
---
## G1: Term vectors alongside content vectors
**Covers:** pp. 9–10, §4.1 Table 3 (G1 row) and G1 text

> "Term vectors match the terse register of ontology labels far more tightly than running prose does."

- Problem (Table 3, G1): "Raw window text embeds to a blurred centroid; cosine distance to a sharply defined ontology label is inflated, dropping relevant classes below the 0.72 floor."
- Refinement (Table 3, G1): "Extract proper nouns, abbreviations, and domain terms from each window and embed them as a second term vector; query with both vectors and keep the best match per class."
- Mechanism: extract the window's proper-noun phrases, abbreviations, and domain-adjacent terms into a compact pipe-delimited string, e.g. ("12th Battalion | Operation Vijay | SSP | LoC"), embed that string as a second query vector, and score every candidate class against both vectors, retaining the maximum:

  `score(c) = max_{q ∈ {e(w), e(terms(w))}} cos(q, c) × (1 − λ·pr(c))`

- Example contrast: the 1,500-character window "The SSP directed the 12th Battalion along the LoC during Operation Vijay . . ." vs. the ontology label Military Formation (definition: "a body of troops organised for military purposes").

## G2: Subclass expansion
**Covers:** pp. 9–10, §4.1 Table 3 (G2 row) and G2 text

- Problem (Table 3, G2): "Hierarchy traversal looks only upward (parent fetch); a high-confidence generic parent is injected without its more specific children, so the model emits Organization where SecurityForce was available."
- Refinement (Table 3, G2): "For every class with adjusted score ≥ 0.80, traverse subClassOf one hop downward and inject the children at score 0.78 (one additional Cypher call)."
- Mechanism: vector retrieval rewards the classes whose definitions resemble the content, which systematically favours well-described general classes; if Organization retrieves at 0.85, the baseline injects it, and only it.
- Fix: for every class with adjusted score ≥ 0.80, one Cypher hop down the subClassOf hierarchy injects the direct children at a score of 0.78 (just above the floor, below their parent), so the model sees the specific options (SecurityForce, TerroristGroup) alongside the general one.

## Placement in the refined pipeline
**Covers:** p. 11, Fig. 3 caption context for G1/G2

- Fig. 3 summary: "G1 adds a second query vector per window" and "G2 widens class coverage downward from high-confidence matches."
- Both refinements are additive within the retained baseline (PageRank penalty + 0.72 floor + token budget): "disabling any refinement degrades precision, never availability."
