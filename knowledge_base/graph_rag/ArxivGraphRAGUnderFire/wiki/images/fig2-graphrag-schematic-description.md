**Figure 2 – Schematic of GraphRAG concepts (three panels, a–c).**

**Legend (top):** three node types — *Source Entity* (white circle, green ring), *Intermediate Entity* (white circle, blue ring), and *Endpoint Entity* (filled green / filled blue circles). Edges are labeled with semantic relations (e.g., *Utilize*, *Mitigate by*, *Detect by*).

**Panel (a) – Representative subgraph.** A small text‑derived knowledge graph built from a corpus. The *Source Entity* node "Stuxnet" connects via a *Utilize* edge to the *Intermediate Entity* "DLL Injection," which in turn branches to two *Endpoint Entity* nodes: "Behavior prevention on Endpoint" (via *Mitigate by*) and "OS API Execution" (via *Detect by*). This is the static entity–relation structure GraphRAG extracts.

**Panel (b) – Multi‑hop query.** Over the same skeleton, a single dashed query arrow ("How to mitigate the malware Stuxnet?") arcs from the source "Stuxnet" to the endpoint "Behavior prevention on Endpoint," illustrating a multi‑hop query that traverses the intermediate node "DLL Injection" (path: Stuxnet →DLL Injection→ endpoint).

**Panel (c) – Two related queries.** The panel (a) graph plus two dashed query arrows from the same source: "How to mitigate the malware Stuxnet?" (to "Behavior prevention on Endpoint") and "How to detect the malware Stuxnet?" (to "OS API Execution"). The two queries are *related* because they share common underlying entities/relations (Stuxnet, DLL Injection, the *Utilize* edge) within the same subgraph.

**Flow / architecture.** Reading left‑to‑right across the panels: (a) shows the constructed knowledge graph (entities = nodes, relations = labeled edges); (b) shows how a single query is answered by walking a multi‑hop path through that graph; (c) shows how multiple queries map to overlapping subgraphs, exposing shared structure.

**Takeaway.** GraphRAG turns a text corpus into an explicit entity–relation knowledge graph, so that (i) answers come from traversing multi‑hop paths across entities and (ii) distinct queries can be linked as *related* by the shared subgraph they induce; an LLM is used throughout graph construction and query answering, contrasting with traditional (non‑text) knowledge graphs.