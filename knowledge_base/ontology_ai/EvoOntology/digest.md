> [[index|Wiki]] | [[summary|Summary]]
# EvoOntology: A Self-Evolving Ontology Layer for Data Agents — Digest

## 1. [[wiki/01-evoontology-overview|EvoOntology: A Self-Evolving Ontology Layer for Data Agents — Overview]]
**In one sentence:** EvoOntology proposes a self-evolving ontology layer that sits between heterogeneous data sources and data agents to close the agent–data gap left by raw exploration and manually constructed semantic layers.
## Key points
- The paper is titled "EvoOntology: A Self-Evolving Ontology Layer for Data Agents" by Meiduo Chong, Shaolei Zhang, Ju Fan, and Xiaoyong Du of Renmin University of China (arXiv:2609.15779v1 [cs.AI], 14 Sep 2026).
- Data agents aim to "fulfill natural-language instructions over heterogeneous data, including tables, files, and databases," per the abstract opening.
- The paper defines "a challenging agent–data gap: heterogeneous data resides outside the agent, while the agent can access it (e.g., column names and file paths) only through generic tools."
- Existing approaches are characterized as a two-way split: they "either let agents directly explore raw data sources or inject manually constructed semantic" layers (sentence truncated in chunk).
- The figure shows heterogeneous sources (Tables, CSV, Docs, Databases, Charts, Logs) mediated by an Ontology Layer with four node types: Terms, Mappings, Evidence, and Constraints.
- The same figure lists three edge types — Semantic Relation, Structural References, Attribute — plus Data interaction and Ontology interaction paths connecting sources, layer, and Data Agent.
- The layer is labeled Self-Evolving with a four-stage loop: Diagnose (Evaluate) (Trajectory) (Content · Tool · Schema) → Refine (Candidate Update) → Update (Evolve) → Evaluate (Parent vs. Candidate) (Improve).

## 2. [[wiki/02-agent-data-gap|Agent–Data Gap: Why Neither Raw Querying nor Semantic Layers Scale]]
**In one sentence:** Data agents face a persistent agent–data gap over heterogeneous sources because raw querying traps them in blind, repetitive exploration while static semantic layers cannot fit into context and are costly to build and adapt, motivating an interactive self-evolving ontology layer.
## Key points
- Data agents aim to solve natural-language tasks over both structured data (tables, databases) and unstructured data (documents, files), and must continuously interact with heterogeneous sources to gather information for the final answer.
- In real-world deployments data resides outside the agent as relational databases, semi-structured filings, and unstructured documents, while the agent can access the data only through generic tools such as SQL interfaces and file readers.
- Because neither the structure nor the content of heterogeneous sources is known a priori, the agent must blindly explore by repeatedly issuing probing queries, guessing where requested concepts are located, and inspecting potentially irrelevant content.
- Raw-querying methods (Pourreza and Rafiei 2023; Wang et al. 2025; Talaei et al. 2024) let agents directly inspect schemas and issue exploratory queries; while effective for small and relatively simple sources, they scale poorly to wide heterogeneous data where agents become trapped in repetitive, inefficient exploration.
- Semantic-layer approaches (Hitzler 2021; dbt Labs 2023; Feng et al. 2024; Chang and Fosler-Lussier 2023) provide metadata including schemas, entities, metrics, and other domain semantics, but incorporating the entire layer into agent context is impractical for large sources due to context-length limitations.
- Existing semantic layers are typically predefined and maintained manually, making them costly to construct and difficult to adapt to new data sources, tasks, and agents — and, as the chunk title states, they "neither scale well to large heterogeneous data sources nor adapt to different agent behaviors."
- The paper therefore advances the intermediate layer from static semantic descriptions to an interactive ontology layer (schema, content, and tool layers encapsulated as an MCP server) that agents flexibly access through tools and that continuously adapts to both data and agent behaviors.

## 3. [[wiki/03-architecture-overview|Cost in Constant Currency Analyse Schema]]
**In one sentence:** This chunk is garbled figure OCR for a "Cost in constant currency" analyse-schema flow in which a Builder Data Agent grounds candidate concepts across heterogeneous sources, records "No schema-level issue" for Q4, and identifies a "Constraint conflict (currency)" that leads to "Patch the Parent Ontology".
## Key points
- The chunk header links three levels: "Cost in constant currency", "Analyse", and "Schema Level".
- For "Q4" the chunk states "No schema-level issue".
- A "Data Agent" / "Builder Agent" step is labeled "Ground Candidate Concepts in Heterogeneous Data".
- A currency problem is flagged verbatim as "Constraint conflict (currency)" with "identified".
- Data execution covers "Tables", "CSV", "Docs", "Databases", "Charts", and "Logs", with "Execute SQL" and "Execute Python".
- Ontology interaction uses "browse" and "resolve" tools over a "Cost Table" (`fact_cost`) and a "Metric Definition".
- The recorded evolution step is "Patch the Parent Ontology", contrasting "Ontology v1" with "Candidate Ontology".
- The cost fact table gives Jan-24 Labor 1,234,567, Jan-24 Freight 234,987, and Feb-24 Labor 1,310,000.

## 4. [[wiki/04-tool-layer|Tool Layer: browse and resolve]]
**In one sentence:** This chunk is a garbled OCR extraction of Figure 2 labels (Tool 1: browse / Tool 2: resolve, mappings, evidence, constraints) plus the Figure 2 caption, and contains no complete argument beyond those fragments.
## Key points
- The only legible tool labels are "Tool 2: resolve" and "Tool 1: browse", with no usable description of their signatures or behavior.
- A legible fragment pairs "Terms IDs → Mappings, Relations, Constraints" and "Query → Ranked Terms" under browse/resolve context, but the surrounding text is column-scrambled.
- A legible fragment labels "Mapping (Exact Fields)" with field-like tokens such as fact_.cost / total_cost, fact_rev / net_revenue, and dim_date / date, but the alignment is corrupted.
- A legible fragment labels "Constraint" examples including "Profit = Revenue - cost", "Revenue excludes cancelled orders", and "Time grain = Month", though layout and duplication are unreliable.
- A legible fragment lists heterogeneous sources as "Tables CSV Docs Databases Charts Logs" and an "Evaluate and Gate the Candidate" branch ("Accept (Candidate Ontology → Ontology v2.0)" vs "Reject (Roll back to Ontology v1.0)"), but no mechanism is stated.
- The only complete sentence is the Figure 2 caption quoted below; no numbers, tables, or mechanisms beyond these fragments can be recovered from this chunk.

## 5. [[wiki/05-content-schema-layers|Content Layer, Schema Layer, and Evidence-Grounded Initialization]]
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

## 6. [[wiki/06-evolution-loop|The single-level difference isolates the attributed]]
**In one sentence:** The chunk defines a reciprocal paired score with validation-gated deployment and reports that EvoOntology improves Trajectory-Wise, Insight/Summary, and EX/VES across backbones while static semantic-layer prompts and episodic memory do not match it.
## Key points
- Reciprocal score is defined as `Score = (ScoreA→B + ScoreB→A) / 2`, following two-fold split-and-swap evaluation (Dietterich 1998; Wang et al. 2026).
- Rejected candidates are not deployed; their signatures, interventions, and evaluation outcomes are logged to avoid repeated ineffective updates, while limiting regressions on the validation set.
- All backbones evolve independently from the same initial state L0, so accepted updates reflect backbone-specific interaction patterns.
- On DDR-Bench 10-K, EvoOntology improves Trajectory-Wise accuracy on all six backbones with average gain +17.8 points, ranging from +4.8 on Qwen3.5-Flash to +26.7 on GPT-5.5.
- Baseline + SL as a static prompt does not consistently improve and drops −15.0 Trajectory-Wise points on Claude-Sonnet-5, because a static fragment competes with other instructions and cannot be pruned per turn, whereas EvoOntology exposes content through MCP tools queried per step.
- ReAct + Memory lifts DDR-Bench Trajectory-Wise from 69.5 to 75.8 (+6.3) but remains 13.7 points below EvoOntology at 89.5 (+20.0), because episodic memory only replays what has been done and does not expose typed, composable structure.
- On InsightBench EvoOntology improves overall performance on every backbone with mean gain 1.9 points and largest improvement +6.1 on DeepSeek-V4-Flash; on BIRD under Oracle Knowledge it improves EX by 7.4 and VES by 8.6 points on average, while Baseline + SL shows mixed EX (down to −5.6 on GPT-5.5) with VES rising.
- Initial builder-constructed ontology versus evolved ontology: on DDR-Bench mean Trajectory-Wise rises 12.3 points from Baseline to Initial plus a further 7.7 points from Initial to Evolved, separating builder contribution from self-evolution gain.

## 7. [[wiki/07-experiments-main|Main Experimental Results (Overall EX)]]
**In one sentence:** This chunk is a garbled extraction of Figure 3 and a baseline table reporting Overall EX values of 82.9, 73.2, and 71.8 (with 81.3 and 70.7 also present) across three benchmarks and several backbones under Baseline, Initial, and Evolved (EvoOntology) conditions.
## Key points
- The chunk's headline numbers are Overall EX (%) values of 82.9, 73.2, and 71.8, with additional Overall EX (%) values of 81.3 and 70.7 present in the same extraction.
- Figure 3 is described verbatim as comparing the "Primary metric on the three benchmarks under three conditions: Baseline, Initial, and Evolved (EvoOntology)".
- The three benchmarks named in the chunk are BIRD, DDR-Bench (10-K), and InsightBench.
- The backbones named on the figure axes/legends are GPT-5.5, GPT-5.6-sol, Claude-Sonnet-5, and Claude-Opus-4.8 (with a fragmented "GPT-5" label also present).
- The metrics named in the chunk are Overall EX (%), Traj-Wise (%)/Trajectory-Wise (%), and Insight (%).
- A block labeled "Baseline (ReAct w/o Ontology)" lists paired numbers per backbone: GPT-5.5 (61.5, 63.4), GPT-5.6-sol (63.5, 65.6), Claude-Sonnet-5 (61.9, 63.7), Claude-Opus-4.8 (67.5, 69.6), DeepSeek-V4-Flash (33.1, 36.4), and Qwen3.5-Flash (46.5, 47.9).
- Prior-method rows appear with paired numbers or dashes: DIN-SQL GPT-4 (50.7, 58.8), DAIL-SQL GPT-4 (54.8, 56.1), TA-SQL GPT-4 (56.2, –), MAC-SQL GPT-4 (57.6, 58.8), MCS-SQL GPT-4 (63.4, –), and CHESS GPT-4o (65.0, 62.8).

## 8. [[wiki/08-model-analysis|Per-Backbone Analysis and Insight Metrics]]
**In one sentence:** Per-backbone results show the builder-constructed ontology improves scores and the self-evolution loop adds further gains through monotonically converging accepted rounds, with ablations identifying the gate and attribution steps (and mappings/evidence families) as the largest contributors.
## Key points
- On BIRD, the mean EX score improves by 5.1 percentage points with the initial ontology and by a further 3.7 percentage points after evolution, while another metric "increases by 0.8 points and then gains another 0.2 points through evolution."
- Under Oracle Knowledge on BIRD (Table 4, VES on a 0–100 scale, parentheses = gain over Baseline), EvoOntology reaches: GPT-5.5 68.9 (+7.4) / 71.1 (+7.7), GPT-5.6-sol 70.7 (+7.2) / 73.0 (+7.4), Claude-Sonnet-5 71.8 (+9.9) / 74.1 (+10.4), Claude-Opus-4.8 78.3 (+10.8) / 80.5 (+10.9), DeepSeek-V4-Flash 39.4 (+6.4) / 44.1 (+7.6), Qwen3.5-Flash 49.1 (+2.5) / 55.2 (+7.3).
- Baseline + SL (ReAct + Semantic Layer) rows in the same table include GPT-5.5 55.9 (−5.6) / 67.7 (+4.3), GPT-5.6-sol 63.0 (−0.5) / 68.9 (+3.3), Claude-Sonnet-5 60.8 (−1.1) / 65.8 (+2.1), Claude-Opus-4.8 66.2 (−1.3) / 75.0 (+5.4), DeepSeek-V4-Flash 36.3 (+3.2) / 37.2 (+0.7), and Qwen3.5-Flash 48.0 (+1.5) / 51.9 (+4.0).
- Figure 4 tracks the primary score across accepted evolution rounds (Traj-Wise on DDR-Bench, Insight on InsightBench, EX on BIRD); all four backbones improve monotonically from Initial, with GPT-5.6-sol reaching 93.5 Traj-Wise after five accepted rounds and Claude-Opus-4.8 reaching 92.3 after four.
- Trajectories "flatten by the last two rounds, which is consistent with the failure signatures becoming rarer once the ontology covers the recurrent cross-filing concepts," supporting that Table 1 gains come from "a converging refinement and not a single fortunate patch."
- Evolution-loop ablation (Table 5, DDR-Bench Traj-Wise %, averaged across four backbones): Full loop 89.5; w/o Gate 78.3 (−11.2); w/o Attribution 83.2 (−6.3); w/o Diagnose 84.7 (−4.8); w/o Patch (free-form) 87.8 (−1.7).
- Content-layer object-family ablation (Table 7, DDR-Bench Traj-Wise %, averaged across four backbones): Full EvoOntology 89.5; w/o Mappings 76.1 (−13.4); w/o Evidence 80.8 (−8.7); w/o Constraints 86.0 (−3.5); w/o Relations 87.4 (−2.1), with terms noted as "cannot be masked in isolation and are omitted."

## 9. [[wiki/09-ablation-study|Ablation study: tool-only evolution and Jaccard overlap]]
**In one sentence:** Table 6 ablates the three editable evolution levels on DDR-Bench averaged across four backbones, reporting tool-only evolution at 82.7 (+13.2), schema-only at 73.1 (+3.6), and full three-level evolution at 89.5 (+20.0), alongside a garbled pairwise Jaccard overlap matrix.
## Key points
- Table 6 is described as an ablation on the three editable levels of the evolution loop on DDR-Bench, averaged across four backbones.
- Tool-only evolution scores 82.7 with a gain of +13.2 reported in the chunk.
- Schema-only evolution scores 73.1 with a gain of +3.6 reported in the chunk.
- Full three-level evolution scores 89.5 with a gain of +20.0 reported in the chunk.
- The chunk contains a "Jaccard overlap" matrix with rows labeled GPT-5.6-sol, Claude-Sonnet-5, and Claude-Opus-4.8, but axis labels and cell alignment are garbled in extraction.
- Reported Jaccard row fragments are: GPT-5.6-sol 0.61 / 1.00 / 0.60 / 0.62; Claude-Sonnet-5 0.58 / 0.60 / 1.00 / 0.55; Claude-Opus-4.8 0.56 / 0.62 / 0.55 / 1.00, with diagonal 1.00 values intact but row-column mapping not recoverable from the chunk.
- Additional numeric fragments (e.g. Sonnet-5 73.1 / 76.8 / 81.3 / 82.1 and Opus-4.8 75.4 / 78.9 / 75.6 / 92.3 under an "Agent backbone (deployment)" axis) appear in the chunk but their column headers are garbled, so no claim about their meaning is made here.

## 10. [[wiki/10-evolution-dynamics|Evolution Dynamics: Pairwise Overlap and Cross-Backbone Transfer]]
**In one sentence:** Different backbones evolve distinct ontology stores from the same initialization (no Term-identifier pair exceeds 0.62 Jaccard overlap), and each store performs best on its own backbone, with every cross-backbone transfer dropping Traj-Wise performance by at least 6.6 points.
## Key points
- Pairwise Jaccard overlap of accepted Term-identifier sets on DDR-Bench never exceeds 0.62 across the four backbones (Figure 5a).
- The two Claude backbones share less with each other (0.55) than the two GPT backbones do (0.61).
- Claude-Opus-4.8 retains more detailed manifest variants than Claude-Sonnet-5, while GPT-5.5 introduces short SQL fragment libraries under Evidence absent from the Claude-Opus-4.8 ontology.
- Identifier overlap alone cannot determine semantic equivalence because different identifiers may encode similar concepts.
- In cross-backbone transfer (Figure 5b), the diagonal is uniformly the highest entry of its column, with every off-diagonal dropping at least 6.6 points relative to the same-backbone store.
- The average column drop from diagonal to off-diagonal ranges from −6.6 (Sonnet-5) to −10.9 (GPT-5.5), indicating backbone-specific evolution is beneficial.
- Context from the same chunk: single-level evolution gains are +13.2 (Tool-only), +8.7 (Content-only), +3.6 (Schema-only) versus +20.0 for the full three-level loop; masking Mappings drops −13.4 and Evidence −8.7 Traj-Wise.

## 11. [[wiki/11-efficiency-scaling|Efficiency and Scaling: Content Growth, Cost, and Attribution]]
**In one sentence:** Ontology content growth concentrates in the first three evolution rounds and then flattens alongside performance, while the ontology layer shortens trajectories enough to cut total tokens per task by ~20% and Tool-level edits contribute most of the accepted gain.
## Key points
- Terms grow from 61 in the Initial ontology to 80 after five accepted rounds on DDR-Bench under GPT-5.6-sol, with per-round growth of every tracked element falling below 5% after round three.
- Content-size curves flatten together with Trajectory-Wise performance, indicating expansion is concentrated in early rounds when recurrent semantic gaps are addressed.
- The Initial ontology raises average input tokens per turn from 3.2K to 4.1K due to the manifest and retrieved semantics, while output tokens per turn stay at 0.4K.
- Average trajectory length falls from 14.6 to 11.2 turns with the Initial ontology and to 8.4 turns with the Evolved ontology, cutting total cost from 52.6K to 50.4K to 42.0K tokens per task.
- The Evolved ontology total cost of 42.0K tokens is approximately 20% below Baseline, while Trajectory-Wise performance rises from 69.5 to 89.5 over the same comparison.
- Tool-level edits account for 57% of cumulative gain across six accepted rounds by improving how existing content is exposed through the manifest and MCP tools.
- Content-level edits contribute 34% across eleven accepted rounds and Schema-level edits contribute the remaining 9% across three accepted rounds, with Content edits more frequent and Schema edits addressing limitations not fixable by content changes alone.

## 12. [[wiki/12-conclusion|Schema Layer Content Layer Schema Layer]]
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

## The argument in five moves
1. Data agents face an agent–data gap: heterogeneous sources live outside the agent and are reachable only through generic tools, so raw querying degrades into blind, repetitive exploration while static semantic layers cannot fit in context and are costly to build and adapt.
2. EvoOntology inserts an interactive ontology layer — a typed content graph (Terms, Mappings, Evidence, Constraints), its object schema, and a runtime tool interface (`fbrowse`/`browse`, `fresolve`/`resolve` plus a compact manifest) exposed as an MCP server — between sources and agent.
3. A builder agent constructs the initial state L0 = (S0, Γ0, R0) without gold answers via workload-guided probing and evidence-grounded commitment, grounding only verified candidates in fields, linking paths, and value distributions.
4. An evolution agent then closes the loop from historical trajectories: diagnose recurrent signatures, attribute each to Content/Tool/Schema, propose a single-level patch, and deploy it only after backbone-conditional paired validation with reciprocal scoring, logging rejections to avoid repeats.
5. Across DDR-Bench, InsightBench, and BIRD on six backbones the Evolved ontology beats Baseline, static-prompt semantic layers, and episodic memory (e.g. +17.8 mean Traj-Wise on DDR-Bench; +7.4 EX / +8.6 VES on BIRD), with ablations showing the gate, attribution, Mappings, and Evidence as load-bearing, evolution converging in early rounds, cutting total tokens ~20%, and diverging per backbone so each store transfers best to its own backbone.
6. A card-legality case illustrates the mechanism: a localized Content-level addition (Legality Status Code term, mapping, evidence, format-dependent constraint) fixes a missing `legalities.status` interpretation without touching tools, schema, or existing objects.
