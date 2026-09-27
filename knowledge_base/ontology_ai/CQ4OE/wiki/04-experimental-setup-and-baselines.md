> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Experimental Setup and Baselines
**In one sentence:** Nine LLMs are evaluated on 99 CQs (CQ2Term) and 118 CQs (CQ2Onto) across six ontologies under zero-shot, iterative, and multi-agent repair strategies, yielding 54 runs and 162 ontologies that show strong vocabulary recovery but steep drops to structure, hierarchy closure, and CQ-level completeness.
## Key points
- CQ2Term covers 99 CQs and CQ2Onto covers 118 CQs across six ontologies, producing 54 runs and 162 ontologies as reference baselines with results and reports in the project repository.
- Nine baselines are tested: DeepSeek V4-Pro, V4-Flash, V3.2; Qwen Plus, Flash, 35B-A3B, 27B; and Gemma 31B-IT, 26B-A4B-IT via OpenRouter at temperature 0 with a 16,384-token output limit, all reusing the MASEO Generation Agent prompting set.
- Three CQ2Onto strategies are compared: zero-shot (full CQ set in one pass), iterative (CQs fed sequentially), and multi-agent (initial ontology refined with RDFLib, HermiT, and OOPS! for up to three iterations with backtracking).
- CQ2Term global F1 spans 59.1% (DeepSeek V3.2) to 66.5% (DeepSeek V4-Pro), class recovery (67.1%) beats property recovery (55.2%), and precision–recall gaps (overall 56.1% vs 71.5%; properties 47.9% vs 69.3%) indicate over-generation.
- CQ-conditioned coverage averages 89.2% at-least-one, 54.8% mean, and only 23.5% full, with Water at 70.6% global F1 but 0% full coverage and Wine at 100% at-least-one but 0% full, so global vocabulary scores hide requirement-localization errors.
- CQ2Onto drops steeply from vocabulary to structure (class F1 averaging 59.7% vs property F1 31.8%; Triple-AC 36.4% vs Triple-G 12.4%; Axiom-AC 35.3% vs Axiom-G 15.0%; closure F1 averaging only 16.7%), and no single model dominates every dimension.
- Strategies differ within 3 percentage points on structural F1 but shape hierarchies differently: iterative is densest (8.6 closure pairs vs 4.9 zero-shot and 4.7 multi-agent) while multi-agent raises CQ-level axiom coverage (Axioms-Mean 18.3% to 24.2%, concentrated in AWO 26.0% to 37.6% and ODRL 23.3% to 32.3%).
- Three recurrent limitations emerge: missing SubClassOf/SubPropertyOf chains, unstable property modeling at nearly half of class F1, and low CQ completeness with Axioms-Full near 2% (2.1%) and Closure-Full unchanged by rescue.
---
## 5 Experimental setup
**Covers:** Section 5 (Experimental Setup and Results opening)

| Item | Value from chunk |
|---|---|
| CQ2Term scope | 99 CQs |
| CQ2Onto scope | 118 CQs |
| Ontologies | Six |
| Models (9) | DeepSeek V4-Pro, V4-Flash, V3.2 [10,9]; Qwen Plus, Flash, 35B-A3B, 27B [44]; Gemma 31B-IT, 26B-A4B-IT [18] |
| Access / decoding | OpenRouter, temperature 0, 16,384 token output limit |
| Prompting | Reuses the prompting set from the MASEO Generation Agent [27] |
| CQ2Term output | Required classes and properties per CQ |
| CQ2Onto strategies | Zero-shot: full CQ set in one pass; iterative: CQs sequentially; multi-agent: refines initial ontology with RDFLib, HermiT [19], and OOPS! [43] for up to three iterations with backtracking |
| Totals | CQ2Term 54 runs; CQ2Onto 162 ontologies |

> "All setups reuse the prompting set from the MASEO Generation Agent [27] so that performance differences reflect the models and strategies rather than prompt design."

## 5.1 Results — CQ2Term term recovery
**Covers:** Section 5.1, CQ2Term paragraph and Figure 2

- Global term F1 ranges from 59.1% (DeepSeek V3.2) to 66.5% (DeepSeek V4-Pro), with five models leading on at least one domain.
- Class recovery exceeds property recovery (67.1% vs 55.2%); precision–recall gaps indicate over-generation (overall 56.1% vs 71.5%; properties 47.9% vs 69.3%).
- Standalone matching: hard matching is conservative (51.7% on classes, 30.0% on properties) while semantic similarity reaches 73.9% and 63.3%; the 33.3-point property gap supports the multi-method aggregation in CQ4OE.
- Figure 2(a): performance varies more by domain than by model, ranging from 48.0% on Wine to 90.5% on AWO.
- Figure 2(b) CQ-conditioned coverage averages 89.2% at-least-one, 54.8% mean, and only 23.5% full; Water reaches 70.6% global F1 but 0% full coverage for every model, and Wine reaches 100% at-least-one but 0% full coverage.
- Interpretation stated in chunk: "by tying every recovered term to the CQ that requires it, CQ4OE exposes requirement-localization errors that global scores hide."

## 5.1 Results — CQ2Onto structure, strategies, and domains
**Covers:** Section 5.1, CQ2Onto paragraphs and Figure 3

- DeepSeek V4-Pro achieves the highest class-label F1 at 66.5%, and Gemma 31B-IT leads on property triple recovery at 41.2%.
- Mean structural F1 across the 18 (domain, strategy) settings ranges from 26.7% for Gemma 26B-A4B-IT to 33.7% for DeepSeek V3.2, with five models leading on at least one domain.
- At CQ level, DeepSeek V4-Flash leads on Axiom-Mean and Closure-Mean at 23.7% and 24.8%; no single model dominates every dimension.
- Vocabulary-to-structure drop: class F1 averaging 59.7% and property F1 31.8%; Triple-AC 36.4% vs Triple-G 12.4% and Axiom-AC 35.3% vs Axiom-G 15.0% (AWO excluded from triple aggregation because its gold range is a complex anonymous OWL expression); closure F1 averages only 16.7%.
- Figure 3(a): domain variation dominates strategy variation; three strategies yield comparable structural F1 within 3 percentage points but shape hierarchy differently — iterative densest at 8.6 closure pairs on average against 4.9 for zero-shot and 4.7 for multi-agent.
- Multi-agent repair (OOPS! and HermiT, no new chains) raises CQ-level axiom coverage (Axioms-Mean) from 18.3% under zero-shot to 24.2%, concentrated in AWO (26.0% → 37.6%) and ODRL (23.3% → 32.3%).
- Per-domain facets: AWO easiest (class F1 87.6%, closure F1 52.2%); Wine strongest axiom scores (Axiom-AC 54.0%, Axiom-G 23.7%); VGO and ODRL show large AC-to-Global triple drops (70.0% to 25.8% and 59.7% to 19.1%); Water splits recognition vs structure (class F1 ≈ 65% but Triple-G ≤ 3.5% and Axiom-G ≤ 6%).
- Figure 3(b): Axioms@1 averages 63.0%, Axioms-Mean 20.2%, Axioms-Full only 2.1%; closure rescue raises Closure-Mean to 21.6% (average gain 1.4 points, shown as ∆) but leaves Closure-Full unchanged; gains concentrate in AWO (30.5% to 37.1%) and Wine (19.8% to 21.3%), with no measurable improvement on ODRL, Water, VGO, or SWO.

> "Models identify relevant entities better than they assemble them into globally correct structures, a distinction that the two-view design of CQ4OE makes explicit and that single-score benchmarks cannot capture."

## Three recurrent LLM limitations
**Covers:** Section 5.1 closing paragraph

1. Rarely generate sufficient SubClassOf or SubPropertyOf chains: VGO and SWO predicted ontologies produce only 0.6 and 0.7 closure pairs against gold 12 and 8; Water recovers flat leaf-to-top edges (e.g., Sensor ⊑ Asset) and misses the chain WaterMeter ⊑ Meter ⊑ Sensor ⊑ Device.
2. Property modeling is unstable, with labels paraphrased or aliased much more often than classes, depressing property F1 to nearly half of class F1.
3. CQ completeness remains low, recovering some axioms per CQ but rarely all, leaving Axiom-Full near 2%.

## 6 Discussion opening (as present in chunk)
**Covers:** Section 6 opening, "Impact and contribution" fragment

- Chunk states CQ4OE addresses a gap where existing evaluations reuse full reference ontologies as undifferentiated gold standards even with knowledge unrelated to the evaluated CQs, making it hard to tell whether a generated ontology satisfies stated requirements or merely overlaps general domain knowledge.
- CQ4OE introduces CQ-aligned gold standards in which terms and TBox axioms are explicitly linked to the CQs that require them, with provenance preserved at the level of each individual class, property and (text cuts off in chunk).

**Covers:** Section 5 through Section 6 opening (Impact and contribution fragment, cut off mid-sentence in chunk)
