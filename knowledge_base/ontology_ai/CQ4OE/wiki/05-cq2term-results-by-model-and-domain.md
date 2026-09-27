> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# CQ2Term results by model and domain
**In one sentence:** Fig. 2 reports CQ2Term term-F1 per model–domain pair and CQ-conditioned coverage averaged over nine LLMs, framing CQ2Term as a test of conceptualization (explicit classes/properties in CQs) distinct from CQ2Onto's deeper requirement reasoning.
## Key points
- Fig. 2 covers six benchmark domains: Wine, AWO, ODRL, Water, VGO, and SWO.
- Fig. 2(a) reports overall term F1 for each model and domain pair, computed by pooling class and property matches before calculating precision, recall, and F1.
- Fig. 2(b) reports CQ-conditioned coverage averaged over nine LLMs, with at-least-one, mean, and full coverage per domain; visible values include 22.0, 20, 8.5, 0.0, 0.6, 0.0.
- The chunk claims CQ-to-axiom provenance at this level is unique: "To our knowledge, no existing benchmark for ontology generation provides this level of CQ-to-axiom provenance."
- CQ2Term targets conceptualization: whether an LLM can recognize and organize the explicit classes and properties in CQs, described as the most immediate semantic content of the requirements and the foundation of downstream ontology since vocabulary selection determines later modeling decisions.
- Isolating conceptualization is said to reduce manual effort enumerating candidate terms and to give a transparent basis for selecting the best-suited model per domain rather than relying on a single aggregate ranking.
- CQ2Onto is introduced as complementary: it evaluates understanding and reasoning over CQ requirements beyond surface vocabulary (sentence truncated in chunk at "whether the model can").
---
## Fig. 2 — CQ2Term results across domains
**Covers:** Fig. 2 caption and panels (a)–(b), p. 14 context

> "Fig. 2: CQ2Term results across six benchmark domains. (a) Overall term F1 for each model and domain pair, computed by pooling class and property matches before calculating precision, recall, and F1. (b) CQ-conditioned coverage averaged over nine LLMs, reporting at-least-one, mean, and full coverage for each domain."

- Panel (b) axis/domain labels present in chunk: Wine, AWO, ODRL, Water, VGO, SWO under "Benchmark Domain"; panel title: "(b) CQ-conditioned coverage averaged over 9 LLMs."
- Numeric labels extracted in reading order: "22.0", "20", "8.5", "0.0", "0.6", "0.0", "0" — per-cell model/domain and per-bar values are garbled in text extraction, so no per-model F1 numbers are recoverable from this chunk.

## Requirement-driven design — two evaluation fronts
**Covers:** provenance paragraph + CQ2Term/CQ2Onto framing (J. Li et al., p. 14)

- Verbatim provenance claim: "no existing benchmark for ontology generation provides this level of CQ-to-axiom provenance" (preceded in chunk by fragment "axiom. To our knowledge, ...").
- CQ2Term role (verbatim core): "targets the conceptualization capability of an LLM by measuring whether a model can recognize and organize the explicit classes and properties expressed in the CQs, which capture the most immediate semantic content of the requirements."
- Rationale given: "Conceptualization is the foundation of any downstream ontology, since vocabulary selection determines all subsequent modeling decisions."
- Claimed benefit: "By isolating this capability, CQ2Term reduces the manual effort that ontology engineers would otherwise spend enumerating candidate terms, and offers practitioners a transparent basis for selecting the model best suited to their domain rather than relying on a single aggregate ranking."
- CQ2Onto role (truncated): "evaluates the ability of a model to understand and reason over CQ requirements beyond recognizing their surface vocabulary. It assesses whether the model can" — chunk ends mid-sentence.

## Note on trailing figure text in this chunk
**Covers:** garbled figure block after p. 14 break

- This chunk file additionally contains fragmented text of CQ2Onto structural/coverage figures (e.g., "CQ2Onto Structural Performance by Domain and Strategy", "CQ2Onto CQ-conditioned Coverage by Domain", rows for WINE/AWO/ODRL/Water/VGO/SWO × zero-shot/iterative/multi-agent across Class, Property, Triple-AC, Triple-G, Axiom-AC, Axiom-G, Closure and Axioms@1/Mean/Full, Closure@1/Mean/Full, Δ Gain); the text layer is column-scrambled (e.g., WINE zero-shot "62.5 38.6 48.0 19.5 54.2 27.7 16.5") and not reliably attributable here, so it is not summarized on this page — see `06-cq2onto-results-and-closure-gains.md` for that content.
