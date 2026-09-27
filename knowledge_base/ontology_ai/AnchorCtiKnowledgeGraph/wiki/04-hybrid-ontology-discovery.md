> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Hybrid Ontology Discovery: DatatypeProperty Triplets, Post-Processing, and Entity/Predicate Typing

**In one sentence:** ANCHOR extracts exhaustive entity-to-literal DatatypeProperty triplets, filters them via IoC detection/noise filtering/duplicate removal, then aligns entities and predicates to formal ontologies via a hybrid embedding-search plus hierarchical-navigation algorithm with SHACL-validated KG construction.

## Key points

- DatatypeProperty triplets capture entity-to-literal associations such as language strings, timestamps, or boolean flags, with the LLM instructed to be exhaustive over every entity pair.
- IoC detection matches entity names against regex patterns and overrides type hints with schema-agnostic descriptors (e.g., "IPv4 address", "SHA-256 hash") for reliable class resolution.
- Noise filtering removes non-entity strings such as temporal expressions, short strings, and common descriptors; duplicate removal merges entities sharing the same normalized key and removes duplicate or dangling triplets.
- Hybrid discovery exposes six tools (classes, attributes, relations × embedding search and hierarchical navigation) over any OWL/SHACL ontology, with pre-computed class-name/description embeddings and an indexed type hierarchy.
- Entity typing (ENTITY mode, Steps 1–2 only) uses `score(u) = 1/2 sim(q, e_name) + 1/2 sim(q, e_desc) + δk` with keyword bonus δk = 0.3 and threshold τ_entity = 0.45, falling back to owl:Thing.
- Predicate typing (PREDICATE mode, all three steps) adds XSD-range boost for DatatypeProperty search, direction-aware +0.10/−0.05 adjustments for ObjectProperty search, τ_predicate = 0.30, and scoped re-search within a collapsed property group anchored at u_scope.
- Predicate fallback is rdfs:label for literal attributes and rdfs:seeAlso for entity relations; SHACL validation checks cardinality/required properties with up to three LLM self-correction retries.

---

## DatatypeProperty triplets and post-processing

**Covers:** extraction tail + Section C intro, post-processing steps

DatatypeProperty triplets capture entity-to-literal associations "such as language strings, timestamps, or boolean flags." The LLM "is instructed to be exhaustive, evaluating every entity pair and capturing all stated attributes regardless of salience."

Post-processing applies "three deterministic post-processing steps: IoC detection, noise filtering, and duplicate removal":

| Step | Mechanism |
|---|---|
| IoC detection | Matches entity names against regex patterns and overrides type hints with schema-agnostic descriptor (e.g., "IPv4 address", "SHA-256 hash") |
| Noise filtering | Removes non-entity strings such as temporal expressions, short strings, and common descriptors |
| Duplicate removal | Merges duplicate entities sharing the same normalized key; removes duplicate or dangling triplets |

"The filtered output is then forwarded to the subsequent hybrid ontology discovery stage."

## Hybrid ontology discovery setup

**Covers:** Section C intro, Algorithm 1 header

"ANCHOR aligns each extracted element to a formal ontology class and property. Hybrid ontology discovery provides this alignment through a uniform tool-based interface between the LLM agent and any OWL/SHACL ontology."

At initialization ANCHOR "parses the target ontology file, pre-computes embeddings for all class names and descriptions, and indexes the type hierarchy. It exposes six tools covering three targets (classes, attributes, relations), each with two operations: (i) embedding-based search that retrieves candidates by semantic similarity, and (ii) hierarchical recursive navigation that the LLM invokes when search confidence is below the threshold τ."

Target ontology sizes (TABLE II):

| Schema | Classes | Relations | Properties |
|---|---|---|---|
| UCO | 419 | 177 | 578 |
| STIX 2.1 | 109 | 92 | 311 |
| MALOnt | 75 | 10 | 12 |

## Entity ontology typing (Algorithm 1, ENTITY mode, Steps 1–2)

**Covers:** Section C.1, Algorithm 1 Steps 1–2

Instantiated "using class-specific semantic search, the root class set U_roots, and owl:Thing as the default fallback" and "executes only Steps 1 and 2 of the discovery process."

Step 1 — embedding-based search:

> `score(u) = 1/2 sim(q, e_name_u) + 1/2 sim(q, e_desc_u) + δk  (1)`

where "q is the query embedding derived from the query hint h (e.g., the entity's type hint)", e_name/e_desc are "pre-computed embeddings of the class name and description, sim(·) denotes cosine similarity, and δk is a fixed keyword bonus (set to 0.3 in our experiments) applied when the query string appears verbatim in the class name or description." "If the top candidate's score meets or exceeds the entity confidence threshold τ_entity (set to 0.45 in our experiments), the class is selected immediately."

Step 2 — hierarchical recursive navigation: "If no candidate from Step 1 clears the threshold τ_entity, the system activates hierarchical recursive navigation. From the set of root classes U_roots, the LLM evaluates semantic definitions of each subclass tier and selects the most logically matching branch, drilling down iteratively until it reaches a leaf node or determines that no sufficiently matching branch remains."

Fallback: "If the recursive navigation fails to identify a suitable class, the entity defaults to owl:Thing" — "This defensive assignment ensures the extracted entity and its associated relations remain in the knowledge graph without introducing an incorrect or unverified type."

Algorithm 1 loop (verbatim structure): `u_curr ← LlmSelect(h, U_roots, RetrieveDesc(U_roots))`; if none return Fallback(m); else `u_scope ← ∅`, iterate `S ← Children(u_curr)`, `u_best ← LlmSelect(h, S, RetrieveDesc(S))`, break with `u_scope ← u_curr` on empty children or no match; ENTITY mode returns `u_scope`.

## Predicate ontology typing (Algorithm 1, PREDICATE mode, Steps 1–3)

**Covers:** Section C.2, Algorithm 1 Step 3

"To assign a formal property URI to each extracted triplet, ANCHOR extends the search-and-navigate strategy used in entity ontology typing. Depending on the triplet type, it determines either an ObjectProperty URI for entity-to-entity relations or a DatatypeProperty URI for entity-to-literal attributes." Uses "all three steps of Algorithm 1, with the algorithm instantiated in PREDICATE mode."

Step 1 — embedding-based search: "ANCHOR deploys two distinct search tools to handle attributes and relations. For literal attributes, the embedding-based search identifies the optimal DatatypeProperty. It extends Equation 1 with a datatype inference heuristic, applying a score boost when the inferred XSD type (e.g., xsd:dateTime, xsd:integer) aligns with the property's declared XML Schema Definition (XSD) range. For entity connections, the relation search targets ObjectProperty URIs by utilizing the evidence sentence captured during triplet extraction as additional context. It applies direction-aware score adjustments, adding a bonus (0.10) for direct forward relations and a minor penalty (−0.05) for inverse relations." "Both tools evaluate properties inherited from the transitive superclass hierarchy, leveraging SHACL domain annotations back-propagated during schema loading."

Step 2 — hierarchical recursive navigation: "If the search score falls below the predicate confidence threshold τ_predicate (set to 0.30), the system triggers LLM-guided traversal. The traversal starting point depends on the target: data-property navigation roots at the bound entity URI, while object-property navigation roots at the (s, o) URI pair. From these roots, the LLM navigates a structured property list organized by inheritance level and domain class. For object properties, the LLM additionally infers the correct assertion direction (forward or inverse)."

Step 3 — scoped embedding search: "Large schemas often group properties under intermediate classes, making exhaustive LLM traversal impractical (e.g., UCO contains 578 properties). When navigation reveals a collapsed property group anchored to an intermediate class u_scope, ANCHOR re-executes the embedding similarity search restricted solely to the properties of that class."

Fallback: "If all three steps fail to identify a matching property, ANCHOR defaults to rdfs:label for literal attributes and rdfs:seeAlso for entity relations" — "this defensive mapping ensures every extracted triplet is preserved in the output graph without fabricating incorrect schema assignments."

## KG construction with SHACL validation (beginning)

**Covers:** Section D opening (partial, continues in next chunk)

"After finalizing the entity and predicate mappings, ANCHOR assembles the typed elements into a unified knowledge graph. To ensure structural integrity, the system applies a SHACL-based validation mechanism that evaluates every entity against the node shapes defined in the target ontology."

It "targets cardinality constraints, verifying that required properties are present and that value counts fall within declared bounds. Because LLM-based extraction often omits mandatory attributes, missing required properties represent the most common source of schema violations in this domain." Example: "under the UCO schema, a cardinality violation occurs if an extracted malware entity lacks the required hash algorithm attribute." On violation "the system generates a structured feedback message detailing the violating entity, the failed constraint, and the expected correction. The LLM agent receives this feedback and re-invokes the appropriate discovery tool" with "this closed-loop self-correction" limited "to three retries."

**Covers:** chunk 04-datatypeproperty-triplets-capture-entity-to-lite (extraction tail through Section D SHACL-validation opening + TABLE II + Buckeye worked-example fragment)
