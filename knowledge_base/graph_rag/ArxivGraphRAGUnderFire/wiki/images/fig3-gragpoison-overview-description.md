**Figure 3 — Overview of the GRAGPOISON attack (pipeline diagram)**

**What it shows.** A left‑to‑right flow diagram of a proposed attack on Graph‑based RAG systems, called *GRAGPOISON*. It depicts how an adversary, starting only from a set of target queries, constructs a single "poisoning text" that, when added to the source corpus, corrupts the graph that the RAG system later builds from that corpus. The diagram is organized into three color‑coded phases (blue → pink → orange), connected by thick red arrows, with a final merge step at the bottom.

**Components and flow (architecture).**

1. **Input — Target Queries (left, blue panel, "Relation Selection").** Represented by chat‑bubble icons (a set of queries, plus ellipsis for many more).
   - *Relation Extraction:* each query is processed (via LLM chain‑of‑thought, per the caption) into a **(speculative) query sub‑graph** — two small example sub‑graphs are sketched.
   - *Sub‑graph Merging:* these speculative sub‑graphs are merged into one combined graph. Within it a **Target Relation** (red edge *r\**) shared across queries is identified, connecting nodes such as *u_r\** and *v_r\**.

2. **Relation Injection (middle, pink panel).** The merged graph is extended by adding a deceptive/competing relation: a new red star node *v_r\** and red edges (*r\**, *r′*) are grafted in among the existing nodes (*u_r\**, *u_r*, *v_r*). A downward dashed arrow labeled **Narrative Generation** produces the **Injection Description *d_r\***** — i.e., natural‑language text that, when indexed, induces the injected relation.

3. **Relation Enhancement (right, orange panel).** The graph is further reinforced with additional supporting nodes/edges (e.g., a highlighted node *v_r⁺*) to raise the centrality/retrieval priority of the injected relation. A second **Narrative Generation** step yields the **Enhancement Description *d_r⁺***.

4. **Merge / Output (bottom).** A plus operator combines the two textual artifacts, *d_r\*** ⊕ *d_r⁺*, into the final **Poisoning Text *d_r^poison*** that is inserted into the source corpus.

**Takeaway.** GRAGPOISON is a corpus‑level (not structure‑level) graph‑poisoning pipeline: it needs no direct access to the knowledge graph; instead it (i) *selects* critical relations shared by target queries via LLM reasoning over the text, (ii) *injects* a competing relation by generating text that creates it, and (iii) *enhances* that relation with extra supporting narratives so it dominates retrieval. The output is a single piece of poisoning text targeting the source documents. The caption emphasizes that, unlike traditional graph poisoning (which assumes explicit graph knowledge and edits nodes/edges/embeddings), this attack operates by generating textual narratives that steer the graph the RAG system itself constructs.

**Other visual on the page (Table 1).** A small results table reporting attack success‑rate‑style percentages of *POISONEDRAG* against NaiveRAG and two Graph‑based RAG variants (GraphRAG, LightRAG) across four datasets (MuSiQue, Geographical, Medical, Cyber‑Security); NaiveRAG is shaded, showing higher values there, while the Graph‑based systems show lower (more resilient) values — supporting the paper's claim that GraphRAG's extraction/reasoning offers some defense.