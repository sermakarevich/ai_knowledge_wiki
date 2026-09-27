> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Schema Layer Content Layer Schema Layer
**In one sentence:** Figure 8 shows ontology evolution for a card-legality task fixing a missing interpretation of `legalities.status` by adding a Legality Status Code term, its mapping and evidence, and a format-dependent constraint, without changing existing Card/Legality objects or tools.
## Key points
- The initial ontology has general Card and Legality semantics but no explicit interpretation of legality status values.
- Schema observations for the two tables (cards schema, legalities schema) are retained as Evidence, letting the agent locate the relevant table but not interpret `legalities.status` values.
- The missing semantics are that legality status must be interpreted relative to a particular game format (`legalities.format` plus `legalities.status`).
- The evolution agent attributes the limitation to the Content Layer, since browse/resolve tools already retrieve the objects and the Schema Layer can already represent the knowledge.
- The accepted patch adds a Legality Status Code Term grounded to `legalities.status`, with Mapping and Evidence recording the observed distribution of status values.
- The new Constraint states that identifying banned cards requires both `legalities.status = 'Banned'` and `legalities.format = <target format>`.
- The candidate introduces no Tool- or Schema-level modification, leaves existing Card and Legality objects unchanged, and becomes part of the evolved ontology Lt after paired validation.
- With the evolved ontology, browse surfaces Legality Status Code for banned/legal queries and resolve returns the Mapping, Evidence, and Constraint, while native SQL execution still applies the filter and verifies records.
---
## Figure 8: evolution of the ontology for a card-legality task
**Covers:** closing recap of schema/content layers and conclusions (chunk 12-schema-layer-content-layer-schema-layer: Figure 8 card-legality evolution case)

The figure contrasts an Initial state (general Card and Legality semantics, no explicit interpretation of legality status) with an Evolved state that adds a Legality Status Code Term, its Mapping and Evidence, and a Constraint relating the status value to the requested format; red dashed boxes mark the added or refined objects.

| Layer | Initial | Evolved |
|---|---|---|
| Term | Card, Legality | Card, Legality, plus Legality Status Code |
| Mapping | Cards.uuid / cards schema | Cards.uuid / cards schema, plus grounding of Legality Status Code to `legalities.status` |
| Evidence | cards schema, legalities schema | prior evidence plus observed distribution of status values |
| Constraint | No legality rule | Banned-card rule requiring status and format |

## Initial gap
Schema observations for the two tables are retained as Evidence. Although these objects allow the agent to locate the relevant table, the ontology does not explain how the values of `legalities.status` should be interpreted. It also does not make explicit that legality status is defined relative to a particular game format. The agent must therefore rediscover these semantics from raw values during execution.

## Attributed limitation
The evolution agent attributes this limitation to the Content Layer. The existing browse and resolve tools can already retrieve the relevant objects, and the Schema Layer can represent the required knowledge. The missing component is a reusable semantic description of the status field and its applicability condition.

## Localized intervention
The Candidate adds a new Term, Legality Status Code, and grounds it to `legalities.status`. An Evidence object records the observed distribution of the status values. A Constraint then states the rule, quoted verbatim:

> "To identify banned cards, use: legalities.status='Banned' with legalities.format=<target format>"

The existing Card and Legality objects remain unchanged, and the Candidate introduces no Tool- or Schema-level modification. After passing paired validation, the Candidate becomes part of the Evolved ontology Lt.

## Effect on agent interaction
With the Evolved ontology, browse can surface Legality Status Code for queries involving banned or legal cards. The agent can then use resolve to obtain the physical Mapping, the supporting Evidence, and the format-dependent Constraint. Native SQL execution remains responsible for applying the filter and verifying the returned records. The case shows that evolution can correct a specific semantic gap by adding a small connected set of objects. The ontology retains its existing structure and interface while providing the agent with the missing interpretation required for the task.
