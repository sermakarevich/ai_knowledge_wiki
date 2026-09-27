> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Fig. 2. Architecture of the ANCHOR System
**In one sentence:** The ANCHOR system builds an ontology-aligned threat knowledge graph in three stages — schema-agnostic extraction, hybrid ontology discovery, and SHACL-validated knowledge graph construction with closed-loop self-correction.
## Key points
- The architecture comprises three stages shown in Fig. 2: extraction, hybrid ontology discovery, and knowledge graph construction.
- Stage (i), schema-agnostic extraction, preprocesses CTI documents before any ontology binding.
- Stage (i) extracts entities from the preprocessed CTI documents without binding to a fixed ontology schema.
- Stage (i) also extracts coreferences alongside entities and triplets.
- Stage (i) extracts triplets without binding to a fixed ontology schema.
- Stage (ii), hybrid ontology discovery, maps each entity to an ontology class URI and each predicate to an ontology property URI.
- Stage (ii) uses embedding search when confidence meets threshold τ, and recursive navigation otherwise.
- Stage (iii), knowledge graph construction, applies SHACL validation with closed-loop self-correction to build an ontology-aligned threat knowledge graph.
---
## Schema-agnostic extraction
**Covers:** Fig. 2 stage (i)

Schema-agnostic extraction preprocesses CTI documents and extracts entities, coreferences, and triplets without binding to a fixed ontology schema.

Verbatim source:

> "Schema-agnostic extraction preprocesses CTI documents and extracts entities, coreferences, and triplets without binding to a fixed ontology schema"

## Hybrid ontology discovery
**Covers:** Fig. 2 stage (ii)

Hybrid ontology discovery maps each entity and predicate to an ontology class or property URI via embedding search when confidence meets τ, or recursive navigation otherwise.

Verbatim source:

> "Hybrid ontology discovery maps each entity and predicate to an ontology class or property URI via embedding search when confidence meets τ, or recursive navigation otherwise"

## Knowledge graph construction
**Covers:** Fig. 2 stage (iii)

Knowledge graph construction applies SHACL validation with closed-loop self-correction to build an ontology-aligned threat knowledge graph.

Verbatim source:

> "Knowledge graph construction applies SHACL validation with closed-loop self-correction to build an ontology-aligned threat knowledge graph."

**Covers:** Fig. 2 three-stage architecture: extraction, discovery, KG construction
