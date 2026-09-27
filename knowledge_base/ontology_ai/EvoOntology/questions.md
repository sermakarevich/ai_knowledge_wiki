---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: EvoOntology: A Self-Evolving Ontology Layer for Data Agents

### Q1. What problem does EvoOntology solve and where does its ontology layer sit?

> [!tip]- Answer
> Data agents face an agent–data gap: heterogeneous sources (tables, CSV, docs, databases, charts, logs) live outside the agent and are reachable only through generic tools, forcing blind exploration. EvoOntology inserts a self-evolving ontology layer of Terms, Mappings, Evidence, and Constraints between the sources and the Data Agent, linked by semantic relations, structural references, and data/ontology interaction paths. See [[wiki/01-evoontology-overview|EvoOntology Overview]].

### Q2. Why do neither raw querying nor static semantic layers scale to heterogeneous data?

> [!tip]- Answer
> Raw-querying agents (e.g. Pourreza and Rafiei 2023; Wang et al. 2025) must blindly probe schemas and guess concept locations, which traps them in repetitive exploration on wide heterogeneous sources. Static semantic layers supply schemas, entities, and metrics but cannot fit large sources into context and are costly to build and adapt manually. See [[wiki/02-agent-data-gap|Agent–Data Gap]].

### Q3. In the cost-in-constant-currency example, what failure does the evolution loop diagnose and what patch follows?

> [!tip]- Answer
> A Builder Data Agent grounds candidate concepts (Cost Table `fact_cost`, metric definitions) across heterogeneous sources using browse/resolve plus SQL/Python execution, recording "No schema-level issue" for Q4. It flags an identified "Constraint conflict (currency)" and responds by patching the parent ontology, contrasting Ontology v1 with the Candidate Ontology. See [[wiki/03-architecture-overview|Cost in Constant Currency Analyse Schema]].

### Q4. What does Figure 2 state about EvoOntology's composition and construction?

> [!tip]- Answer
> Per its caption, EvoOntology comprises a typed content graph, its object schema, and a runtime tool interface exposed through browse (Query → Ranked Terms) and resolve (Term IDs → Mappings, Relations, Constraints). The builder constructs an evidence-grounded initial state while the evolution agent refines it from historical trajectories, gating candidates as Accept (→ Ontology v2.0) or Reject (rollback to v1.0). See [[wiki/04-tool-layer|Tool Layer: browse and resolve]].

### Q5. What are the Content, Schema, and Tool layers, and how is the initial ontology built without gold answers?

> [!tip]- Answer
> The Content Layer is a typed graph of Terms (concepts), Mappings (fields/linking paths), Constraints (valid use), and Evidence, joined by Semantic Relations and Structural References; the Schema Layer defines the object model so updates extend capacity without changing content. The Tool Layer exposes `fbrowse(q, k, n)` and `fresolve(I, c)` via MCP with only a compact manifest in the prompt. See [[wiki/05-content-schema-layers|Content Layer, Schema Layer, and Evidence-Grounded Initialization]].

### Q6. How does evidence-grounded commitment decide which candidate concepts enter L0?

> [!tip]- Answer
> From workload W and sources D the builder proposes C = propose(W) from recurrent entities, metrics, and conditions, then issues probe(c, D) per candidate to check types, values, and semantic consistency. Only verified candidates C+ = {c | verify(probe(c, D)) = 1} are constructed into S0 under schema Γ0, forming L0 = (S0, Γ0, R0) with supporting records kept as Evidence. See [[wiki/05-content-schema-layers|Content Layer, Schema Layer, and Evidence-Grounded Initialization]].

### Q7. How does the evolution loop attribute, patch, and gate a candidate update?

> [!tip]- Answer
> Recurrent signatures Σt = analyze(Tt, Lt) are attributed to Content, Tool, or Schema via α with a stated expected effect, then applied as a single-level patch L′t = patch(Lt, σ, α(σ)) so the difference isolates the hypothesis. The candidate is retained only when backbone-conditional paired validation on the same set V improves by margin τ, scored reciprocally as (ScoreA→B + ScoreB→A)/2, with rejections logged to avoid repeats. See [[wiki/06-evolution-loop|Evolution Loop and Validation Gating]].

### Q8. How does EvoOntology compare against static semantic-layer prompts and episodic memory on DDR-Bench?

> [!tip]- Answer
> EvoOntology gains +17.8 Trajectory-Wise points on average across six backbones (up to +26.7 on GPT-5.5), while Baseline + SL as a static prompt is inconsistent and drops −15.0 on Claude-Sonnet-5 because it competes with other instructions. ReAct + Memory rises only from 69.5 to 75.8 (+6.3) versus 89.5 (+20.0) for EvoOntology, since episodes replay past actions rather than exposing typed, composable structure. See [[wiki/06-evolution-loop|Evolution Loop and Validation Gating]].

### Q9. What does Figure 3 show about Baseline, Initial, and Evolved conditions across the three benchmarks?

> [!tip]- Answer
> Figure 3 compares the primary metric — Overall EX, Trajectory-Wise, and Insight — on BIRD, DDR-Bench (10-K), and InsightBench under Baseline (ReAct w/o ontology), Initial (builder ontology), and Evolved (EvoOntology) conditions. On DDR-Bench the mean Trajectory-Wise score rises 12.3 points from Baseline to Initial plus 7.7 more to Evolved, separating the builder contribution from the self-evolution gain. See [[wiki/07-experiments-main|Main Experimental Results]].

### Q10. Which evolution-loop steps and content families are load-bearing in the ablations?

> [!tip]- Answer
> Removing the paired gate drops DDR-Bench Traj-Wise by −11.2 (full 89.5 → 78.3) and removing attribution drops −6.3, making gate and attribution the two load-bearing loop steps ahead of diagnose (−4.8) and typed patch (−1.7). Masking Mappings drops −13.4 and Evidence −8.7, versus −3.5 for Constraints and −2.1 for Relations, since only Mappings ground Terms to columns and join paths. See [[wiki/08-model-analysis|Per-Backbone Analysis and Insight Metrics]].

### Q11. Are the Content, Tool, and Schema evolution levels complementary or substitutable?

> [!tip]- Answer
> Single-level DDR-Bench gains are +13.2 for Tool-only, +8.7 for Content-only, and +3.6 for Schema-only, versus +20.0 for the full three-level loop at 89.5, so the levels are complementary rather than substitutable. Tool-only recovers the largest single share, consistent with manifest reshaping being the dominant lever from the attribution analysis. See [[wiki/09-ablation-study|Tool-Only Evolution and Jaccard Overlap]].

### Q12. Do different backbones converge to the same ontology, and does each evolved store transfer?

> [!tip]- Answer
> No: pairwise Jaccard overlap of accepted Term-identifier sets never exceeds 0.62, with the two Claude stores sharing less (0.55) than the two GPT stores (0.61), e.g. GPT-5.5 adding SQL fragment libraries absent from Claude-Opus-4.8. In cross-backbone transfer the diagonal is uniformly best in its column and every off-diagonal drops at least 6.6 Traj-Wise points, so backbone-specific evolution is beneficial. See [[wiki/10-evolution-dynamics|Evolution Dynamics and Cross-Backbone Transfer]].

### Q13. How does the ontology layer affect content growth, token cost, and the attribution of gains?

> [!tip]- Answer
> Terms grow from 61 to 80 over five accepted rounds with per-round growth below 5% after round three, flattening alongside performance as early rounds cover recurrent gaps. Although input tokens per turn rise 3.2K → 4.1K, trajectories shorten 14.6 → 8.4 turns so total cost falls 52.6K → 42.0K (~20% below Baseline) while Traj-Wise rises 69.5 → 89.5. See [[wiki/11-efficiency-scaling|Efficiency and Scaling]].

### Q14. How does the card-legality case illustrate a localized Content-level evolution?

> [!tip]- Answer
> The initial ontology has Card and Legality terms grounded to their tables but no interpretation of `legalities.status` values or their format-dependence, so the agent must rediscover the semantics from raw values. The accepted patch adds a Legality Status Code term grounded to `legalities.status` with mapping, value-distribution evidence, and the constraint `legalities.status='Banned'` with `legalities.format=<target format>`, leaving tools, schema, and existing objects untouched. See [[wiki/12-conclusion|Card-Legality Case and Conclusions]].

### Q15. Should a team adopt EvoOntology for a new heterogeneous data-agent deployment?

> [!tip]- Answer
> Yes, with backbone-specific evolution: it beats static semantic layers and episodic memory on all three benchmarks, converges in a few gated rounds, and cuts total tokens ~20% while fixing localized gaps like the card-legality Content patch without touching tools or schema. The caveat is that evolved stores do not transfer across backbones (≥6.6-point drops), so each deployment backbone needs its own evolution run and paired-gate discipline. See [[wiki/12-conclusion|Card-Legality Case and Conclusions]].
