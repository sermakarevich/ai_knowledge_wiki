**Figure 4 — Technical summary**

**What it shows.** This is an *architecture/pipeline diagram* (not a quantitative plot), illustrating the **MemGraphRAG** framework. It is split into two side‑by‑side panels representing the two phases of the system, with a color legend (Type / Entity / Schema / Fact / Passage) on the right.

**Left panel — Memory‑based Indexing Graph Construction.** Three interlocking sub‑components:
- *Multi‑Agent Group*: unstructured documents feed an **Extraction Agent**, whose output is passed to a **Conflict Detector** and **Conflict Handler** (with audit, conflict‑triple / correct‑triple, and propagation loops) for global adjudication.
- *Three‑Layer Global Memory (M)*: an **Ontology Layer** (M_ont; pending vs. stable schemas with a frequency filter), a **Fact Layer** (M_fac; active vs. inactive instances), and a **Passage Layer** (M_pas; source text, e.g. the "Article 269" hockey‑player snippet), linked by a "trigger" / dense‑indexing mechanism.
- *Hierarchical Graph (G)*: an **Ontology Graph** (schema‑level type/relation nodes with an illustrative weight ≈ 5), a **Fact Graph** (entity–relation triples, weight ≈ 1), and a **Passage Graph** (grounding text), connected top‑down (schema → fact → passage).

**Right panel — Memory‑Guided Online Retrieval.** A question is encoded against the three memory layers (M_pas, M_fac, M_ont), filtered by a similarity threshold (sim > τ), and scored with **Personalized PageRank** to select retrieved facts and passages that form the answer context.

**Axes / trends.** N/A — there are no numerical axes or trend lines; the "direction" to read is the data/co‑evolution flow: documents → memory + graph construction (left) → memory‑guided retrieval (right). The numeric weights shown (≈ 5, ≈ 1) are schematic examples, not measured values.

**Takeaway.** MemGraphRAG couples a *persistent three‑tier global memory* with a *hierarchical knowledge graph* so they co‑evolve (unified schema filtering + global conflict adjudication + memory‑guided bridging), and at query time uses multi‑layer memory filtering plus structure‑aware **Personalized PageRank** to surface globally relevant, evidence‑grounded context for generation — i.e., a memory‑augmented, multi‑agent RAG design aimed at reducing fragmentation and inconsistency.