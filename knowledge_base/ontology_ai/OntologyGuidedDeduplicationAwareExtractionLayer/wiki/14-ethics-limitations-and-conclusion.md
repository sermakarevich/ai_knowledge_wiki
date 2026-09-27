> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Ethics, Broader Impact, Limitations and Conclusion
**In one sentence:** Person-identity extraction from intelligence documents carries dual-use misidentification and surveillance risks mitigated by conservative no-name-only merging, a hard-conflict guard, human review with provenance, and governed deployment on synthetic/fictional data, while the production layer's ontology guidance, layered deduplication, and robustness passes cut hallucinations to zero and tripled relations and generalise to other governed-schema settings.
## Key points
- Dual-use scope: the system extracts and resolves identities of people from intelligence-domain documents, with misidentification (attributing one person's actions to another via erroneous merge) and surveillance (higher-recall person-centric search) named as the two explicit harms.
- Conservative merge policy: context-validated deduplication never auto-merges on name similarity alone, a hard-conflict guard forbids merging entities with contradictory discriminator attributes regardless of score, and borderline pairs are exported for human review rather than resolved silently.
- Auditability: every merge decision carries provenance so downstream consumers can audit why two mentions were linked.
- Governance prescription: deployments should restrict access to authorised analysts, log queries, and operate within applicable legal frameworks for the jurisdiction of use.
- Data ethics: all person and organisation names in the paper's examples are fictional placeholders with no real individuals' data reproduced, and evaluation corpora are synthetic intelligence-style documents created for system development.
- Principal advantages (threefold): ontology-guided extraction with live graph retrieval cuts catalog prompt overhead by roughly 94% versus static domain slices; six zero-inference rule-based algorithms plus embedding resolution with hard-conflict guard raised search recall from roughly 70 to 95 percent without a single false merge; per-page OCR classifier plus quality-gated relationship second pass give robustness, with the full pipeline cutting hallucinated entities from 174 to zero while tripling relationship coverage on naval intelligence documents.
- Generalisation: the architecture applies beyond intelligence analysis to compliance monitoring, investigative journalism, and enterprise knowledge management, with ontology grounding, deduplication, and graceful degradation adoptable independently by existing pipelines.
- Reproducibility: Python against an OpenAI-compatible endpoint with all thresholds/weights in text and Appendix B; extraction via locally hosted Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology (4-bit AWQ quantisation of Qwen3.5-9B [35]) served via vLLM [2] plus Konect-U/Qwen3-Embedding-0.6B-Ontology; spreadsheet plan-then-execute and all dedup algorithms deterministic given fixed extraction output; synthetic docs not redistributable but ground-truth labels and per-run metric tables reproduced; code/proprietary prompts, open reference implementation under consideration.
---
## 10 Ethics and broader impact
**Covers:** Section 10
- Capability framing: "extracts and resolves identities of people from intelligence-domain documents, a capability with inherent dual-use risk."
- Harm 1 — Misidentification: "an erroneous entity merge can attribute one person's actions to another."
- Mitigations: "context-validated deduplication never auto-merges on name similarity alone, a hard-conflict guard forbids merging entities with contradictory discriminator attributes regardless of score, and borderline pairs are exported for human review rather than resolved silently" plus "Every merge decision carries provenance, so downstream consumers can audit why two mentions were linked."
- Harm 2 — Surveillance: "alias expansion and cross-document resolution increase the recall of person-centric search, which is precisely the property that makes the system useful and the property that demands governance."
- Governance: "Deployments should restrict access to authorised analysts, log queries, and operate within applicable legal frameworks for the jurisdiction of use."
- Data: "All person and organisation names appearing in this paper's examples are fictional placeholders; no real individuals' data are reproduced" and "The evaluation corpora are synthetic intelligence-style documents created for system development."
## 11 Conclusion
**Covers:** Section 11
- Framing: "a production extraction layer that converts a heterogeneous, real-time document stream into a validated, ontology-aligned knowledge graph" with "principal advantages are threefold."
- First: "ontology-guided extraction with live graph retrieval aligns emitted types with a formal schema while cutting catalog prompt overhead by roughly 94 percent relative to static domain slices" with "the four retrieval refinements (term vectors, subclass expansion, predicate full-text search, and density-ranked windowing) recover the specific classes and predicates that embedding similarity alone misses."
- Second: "the layered deduplication design, six zero-inference rule-based algorithms followed by embedding-based resolution with a hard-conflict guard, raised search recall from roughly 70 to 95 percent without a single false merge."
- Third: "the per-page OCR classifier and the quality-gated relationship second pass make the pipeline robust to mixed documents and to silent under-extraction, and the empirical evaluation on naval intelligence documents showed the full pipeline cutting hallucinated entities from 174 to zero while tripling relationship coverage."
- Generalisation: "any setting that must turn unstructured documents into a queryable graph under a governed schema, including compliance monitoring, investigative journalism, and enterprise knowledge management" and "each component can be adopted independently by existing extraction pipelines" because "ontology grounding, deduplication, and graceful degradation are architectural concerns rather than afterthoughts."
## Reproducibility statement
**Covers:** Reproducibility statement
- Implementation: "implemented in Python against an OpenAI-compatible inference endpoint; all thresholds, weights, and configuration knobs referenced in the paper are reported in the text and in Appendix B."
- Models: "Extraction uses the locally hosted, ontology-tuned model Konect-U/Qwen3.5-9B-AWQ-4bit-Ontology (a 4-bit AWQ quantisation of Qwen3.5-9B [35]) served via vLLM [2], with the companion embedding model Konect-U/Qwen3-Embedding-0.6B-Ontology for retrieval and resolution."
- Determinism: "the spreadsheet plan-then-execute stage and all deduplication algorithms are deterministic given a fixed extraction output."
- Data/code: "evaluation documents are synthetic intelligence-style corpora created for development and cannot be redistributed in full; the ground-truth label lists and per-run metric tables are reproduced in the paper" and "Code and prompts are proprietary to the production deployment at the time of writing; an open reference implementation is under consideration."
## References in this chunk
**Covers:** References [1]–[36] as listed in chunk (pp. 40–42)
- Retrieval/serving grounding cited: vLLM [2], Qwen3.5-9B / Qwen3 report [35], Kafka [1, 36], Pydantic [5], FAISS-style similarity search [33], long-context use [34], PyMuPDF [32].
- KG/LLM background cited: LLM×KG roadmap [3], LLM KG construction survey [4], RAG [6], ontology specifications [17], PageRank [18].
- Entity-resolution background cited: end-to-end ER [7], blocking/filtering [8], record linkage theory [19], duplicate detection survey [20], deep/transformer matching [21, 22], name-matching and string metrics [9, 23–28], entity linking/disambiguation [29, 30], Sentence-BERT [31].
- Extraction background cited: few-shot LM [12], Transformer [11], ChatIE [13], GPT-NER [14], REBEL [15], relation extraction in LLM era [16].
**Covers:** Sections 10–11, Reproducibility statement, References [1]–[36]
