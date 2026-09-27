> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# EvoOntology: A Self-Evolving Ontology Layer for Data Agents — Overview
**In one sentence:** EvoOntology proposes a self-evolving ontology layer that sits between heterogeneous data sources and data agents to close the agent–data gap left by raw exploration and manually constructed semantic layers.
## Key points
- The paper is titled "EvoOntology: A Self-Evolving Ontology Layer for Data Agents" by Meiduo Chong, Shaolei Zhang, Ju Fan, and Xiaoyong Du of Renmin University of China (arXiv:2609.15779v1 [cs.AI], 14 Sep 2026).
- Data agents aim to "fulfill natural-language instructions over heterogeneous data, including tables, files, and databases," per the abstract opening.
- The paper defines "a challenging agent–data gap: heterogeneous data resides outside the agent, while the agent can access it (e.g., column names and file paths) only through generic tools."
- Existing approaches are characterized as a two-way split: they "either let agents directly explore raw data sources or inject manually constructed semantic" layers (sentence truncated in chunk).
- The figure shows heterogeneous sources (Tables, CSV, Docs, Databases, Charts, Logs) mediated by an Ontology Layer with four node types: Terms, Mappings, Evidence, and Constraints.
- The same figure lists three edge types — Semantic Relation, Structural References, Attribute — plus Data interaction and Ontology interaction paths connecting sources, layer, and Data Agent.
- The layer is labeled Self-Evolving with a four-stage loop: Diagnose (Evaluate) (Trajectory) (Content · Tool · Schema) → Refine (Candidate Update) → Update (Evolve) → Evaluate (Parent vs. Candidate) (Improve).
---
## Title and authorship
EvoOntology: A Self-Evolving Ontology Layer for Data Agents. Authors: Meiduo Chong, Shaolei Zhang (* corresponding), Ju Fan, Xiaoyong Du, Renmin University of China (zhongmeiduo210@ruc.edu.cn, zhangshaolei98@ruc.edu.cn). Identifier: "arXiv:2609.15779v1 [cs.AI] 14 Sep 2026".

## Abstract opening: the agent–data gap
Verbatim from the chunk: "Data agents aim to fulfill natural-language instructions over heterogeneous data, including tables, files, and databases." Followed by: "However, data agents face a challenging agent–data gap: heterogeneous data resides outside the agent, while the agent can access it (e.g., column names and file paths) only through generic tools. Existing approaches either let agents directly explore raw data sources or inject manually constructed semantic" — truncated at "semantic" in this chunk.

## Figure: self-evolving ontology layer
The chunk preserves a fragmented Figure 1: left side "Heterogeneous Data Sources" listing "Tables CSV Docs Databases Charts Logs"; center "Ontology Layer"; right side "Data Agent". Node types: "Terms", "Mappings", "Evidence", "Constraints". Edge types: "Semantic Relation", "Structural References", "Attribute". Interaction labels: "Data interaction" and "Ontology interaction". Evolution loop labels: "Diagnose (Evaluate) (Trajectory) (Content · Tool · Schema)", "Refine (Candidate Update)", "Update (Evolve)", "Evaluate (Parent vs. Candidate) (Improve)", with the loop headed "Self-Evolving".

**Covers:** Paper title/authorship header + Abstract opening (agent–data gap statement) + Figure 1 fragments (heterogeneous sources, ontology layer node/edge types, self-evolving Diagnose–Refine–Update–Evaluate loop)
