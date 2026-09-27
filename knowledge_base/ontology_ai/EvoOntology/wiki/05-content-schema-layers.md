> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Content Layer, Schema Layer, and Evidence-Grounded Initialization
**In one sentence:** The Content Layer is a typed semantic graph of Terms, Mappings, Constraints, and Evidence linked by Semantic Relations and Structural References under a Schema Layer that defines the object model, initialized by a builder agent through workload-guided probing and evidence-grounded commitment and then refined by trajectory-grounded evolution with single-level patches gated by backbone-conditional paired validation.
## Key points
- The Content Layer St is a typed semantic graph with four node families (Terms, Mappings, Constraints, Evidence) and two edge families (Semantic Relations, Structural References).
- Terms represent domain concepts, Mappings ground them to fields and linking paths, Constraints govern their valid use, and Evidence supports their semantic claims.
- Semantic Relations connect Terms through association, hierarchy, composition, equivalence, or derivation, while Structural References link Terms to Mappings and attach Constraints and Evidence to the objects they govern or support.
- The Schema Layer Γt defines the fields of the four node families, the admissible Semantic Relation types, and the permitted reference patterns, so schema updates extend representational capacity without changing instantiated content.
- The Tool Layer Rt exposes the ontology through `fbrowse(q, k, n)` (top-n semantic matches for query q and kind k) and `fresolve(I, c)` (requested records and linked objects), with only a compact session manifest placed in the prompt and detailed records retrieved on demand.
- Initialization is evidence-grounded and uses no gold answers: from training workload W and sources D the builder proposes C = propose(W) from recurrent entities, metrics, operations, and analytical conditions, then issues probe(c, D) per candidate to find fields/linking paths and inspect types, values, and semantic consistency.
- Only verified candidates are committed: C+ = {c ∈ C | verify(probe(c, D)) = 1}, S0 = construct(C+, D; Γ0), forming L0 = (S0, Γ0, R0), where verify(·) checks declared type, filter, and value-distribution requirements and supporting records are retained as Evidence.
- Evolution is trajectory-grounded: signatures Σt = analyze(Tt, Lt) are attributed via α : Σt → {C, T, S} with a stated expected behavioral effect, applied as a single-level patch L′t = patch(Lt, σ, α(σ)), and retained only when backbone-conditional paired validation on the same V improves by margin τ.
---
## Content Layer: typed semantic graph
"The Content Layer St is a typed semantic graph with four node families and two edge families." The node families "comprise Terms, Mappings, Constraints, and Evidence. Terms represent domain concepts, Mappings ground them to fields and linking paths, Constraints govern their valid use, and Evidence supports their semantic claims." The edge families "comprise Semantic Relations and Structural References. Semantic Relations connect Terms through association, hierarchy, composition, equivalence, or derivation. Structural References link Terms to Mappings and attach Constraints and Evidence to the objects they govern or support." "Figure 2 illustrates these components through a financial-analysis example."

## Schema Layer
"The Schema Layer Γt defines the fields of the four node families, the admissible Semantic Relation types, and the permitted reference patterns. Schema updates can therefore extend the ontology's representational capacity without changing its instantiated content."

## Tool Layer
"The Tool Layer Rt exposes the ontology through two MCP tools and a session manifest. The function fbrowse (q, k, n) retrieves the top-n semantic matches for query q and kind k, while fresolve (I, c) returns the requested records and their linked objects. The manifest provides compact source and usage information at session initialization." "It is the only ontology content placed in the prompt, while detailed records are retrieved on demand."

## Evidence-grounded ontology initialization
"Manually defining domain concepts, field mappings, linking paths, and semantic constraints for each data source requires substantial expert effort. The builder agent constructs an initial ontology from the training workload and raw sources without observing gold answers. The workload identifies semantics relevant to the agent, while executable probes verify their grounding in the underlying data."

### Workload-guided probing
"Given a training workload W and raw sources D, the builder proposes C = propose(W) from recurrent entities, metrics, operations, and analytical conditions. For each candidate c ∈ C, it issues probe(c, D) to identify candidate fields and linking paths and to inspect their types, values, and semantic consistency."

### Evidence-grounded commitment
"Only candidates supported by their probe results are committed to the initial Content Layer:"

> C+ = {c ∈ C | verify(probe(c, D)) = 1}, (1)
> S0 = construct(C+, D; Γ0).

"Here, verify(·) checks the declared type, filter, and value-distribution requirements. Verified candidates are instantiated under Γ0, with their supporting records retained as Evidence. Together with the default Tool Layer R0, they form the initial state L0 = (S0, Γ0, R0)."

## Trajectory-grounded ontology evolution (opening in this chunk)
"Data grounding alone does not ensure that an ontology suits a particular agent. EvoOntology therefore uses historical trajectories as behavioral evidence. Successful executions reveal effective semantic structures and access patterns, while unsuccessful ones expose missing, misleading, or poorly exposed components."

### Trajectory attribution
"Given historical trajectories Tt and the current state Lt, the evolution agent extracts recurrent signatures Σt = analyze(Tt, Lt). Each signature summarizes an interaction pattern, the ontology objects involved, and its observed outcomes. The agent assigns the signature to Content, Tool, or Schema through α : Σt → {C, T, S} and states the expected behavioral effect of an update."

### Localized intervention
"For an attributed signature σ, the agent proposes L′t = patch(Lt, σ, α(σ)). Each candidate modifies one level only. Content interventions add, remove, or revise instantiated semantic objects in St. Tool interventions modify existing tools or add and remove tools in Rt according to observed agent behavior. Schema interventions revise the object model in Γt. Multiple dependent Content objects may be updated together when they implement the same hypothesis."

### Backbone-conditional paired validation
"For backbone m, let φ(L, V; m) denote the score of ontology state L on validation set V. The candidate and its parent are evaluated on the same V with identical decoding and interaction budgets. The candidate is retained only when its improvement reaches margin τ:"

> Lt+1 = Lt′ if φ(L′t, V; m) − φ(Lt, V; m) ≥ τ, else Lt. (2)

**Covers:** chunk 05-content-layer-the-content-layer-st (Content Layer node/edge families; Schema Layer Γt; Tool Layer Rt fbrowse/fresolve + manifest; evidence-grounded initialization Eq. 1 with L0 = (S0, Γ0, R0); trajectory-grounded evolution opening: attribution, localized intervention, paired-validation gating Eq. 2)
