**Figure 2 — Technical summary**

**What it shows.** Four 2×2 confusion matrices (a–d) for NQ, HotpotQA, MultiHop‑RAG, and NovelQA, comparing where *GraphRAG* and *RAG* agree or disagree on answer correctness, using Llama 3.1‑8B. Each cell is a percentage of queries.

**Axes (categorical).** Rows = RAG correctness (top "RAG Correct", bottom "RAG Wrong"); columns = GraphRAG correctness (left "Correct", right "Wrong"). Thus top‑left ≈ both correct, bottom‑right ≈ both wrong, top‑right ≈ RAG‑only correct, bottom‑left ≈ GraphRAG‑only correct.

**Trends.** On fact‑heavy single‑hop sets (NQ, HotpotQA) the two diagonal cells dominate (roughly 45–47% both‑correct and 36–39% both‑wrong), and RAG‑only correct exceeds GraphRAG‑only — RAG has the edge there. On reasoning/multi‑hop sets (MultiHop‑RAG, NovelQA) the pattern shifts: the both‑wrong cell shrinks (notably to ~20% on MultiHop‑RAG) and the GraphRAG‑only cell (~13–14%) becomes comparable to or larger than the RAG‑only cell (~11–17%), indicating GraphRAG's advantage on chaining‑facts queries.

**Takeaway.** The two systems' correct and incorrect sets only partially overlap; each method uniquely answers a non‑trivial slice of queries and they win on different query types (retrieval/detailed facts vs. multi‑hop reasoning). This complementarity is the rationale for the *Selection* (route each query to the better model) and *Integration* (combine both contexts) strategies described in §4.5.