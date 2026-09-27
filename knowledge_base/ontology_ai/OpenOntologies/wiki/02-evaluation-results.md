> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Condition Input F1: LLM Alone vs Raw File vs MCP Tools

**In one sentence:** Giving the LLM a raw OWL file hurts extraction (F1 0.323 vs 0.431 unaided), while structured MCP/SPARQL tool access raises it to 0.717, and stable matching — not signal weights — dominates alignment.

## Key points
- Condition B (LLM, no tools, name lists) scores F1 0.431, Condition D (LLM + raw OWL file in context) scores 0.323, and Condition C (LLM + MCP tools, file via SPARQL) scores 0.717.
- Raw-file reading (D) is 25% worse than unaided LLM (B) because the LLM makes systematic extraction errors on raw Turtle, especially domain/range triples (F1 = 0.0 on 4 of 9 ontologies for domain extraction).
- Structured tools provide +122% over raw file access, while B-to-C improvement is +66% F1; richer input without tools hurts, so MCP tools are a qualitatively different access modality, not merely richer input.
- Condition D varies widely by Turtle complexity: NordStream 0.692, FOAF 0.647, GoodRelations 0.632 versus Time 0.087, Pizza 0.154, ERA 0.058.
- Alignment ablation on OAEI Anatomy (min confidence 0.80): all five stable-matching configurations score F1 0.830–0.834, while all three without stable matching score identical F1 0.728, so signal weights change F1 by less than 0.004.
- OWL-RL vs HermiT on LUBM gives different reasoning profiles/outputs: at 50,000 axioms OWL-RL takes 15 ms vs HermiT 24,490 ms (1,633× ratio); on Pizza (4,179 triples) HermiT computes 312 subsumptions in 213 ms while OWL-RL materialises inferred triples in 43 ms without the same subsumptions.
- LLM-driven Pizza construction via the MCP pipeline produces a 91-class ontology in under 5 minutes with 96% class coverage (95/99 classes), versus ~4 hours manual work; the 4 missing classes are teaching artifacts for OWL syntax variants.

---

## Conditions and F1 results

| Condition | Input | F1 |
|---|---|---|
| B LLM, no tools | Name lists | 0.431 |
| D LLM + raw OWL file | File in context | 0.323 |
| C LLM + MCP tools | File via SPARQL | 0.717 |

**Covers:** chunk 02-condition-input-f1-b-llm-no, conditions table B/D/C

## Why D < B

The LLM reading raw Turtle makes systematic extraction errors, particularly on domain/range triples (F1 = 0.0 on 4 of 9 ontologies for domain extraction). Turtle syntax is ambiguous to read: property IRIs are confused with class IRIs, language tags cause mismatches, and multi-line axiom blocks are missed. The LLM's training knowledge (Condition B) is more accurate than its ability to parse raw syntax (Condition D).

**Covers:** chunk 02-condition-input-f1-b-llm-no, Why D < B paragraph

## Per-ontology variance

Condition D performance varies widely: NordStream F1 = 0.692, FOAF 0.647, GoodRelations 0.632 (simpler Turtle), but Time 0.087, Pizza 0.154, ERA 0.058 (complex Turtle with restrictions, annotations, and large file sizes).

**Covers:** chunk 02-condition-input-f1-b-llm-no, per-ontology variance paragraph

## Disentanglement

The improvement from B to C (+66% F1) combines two factors: richer input and structured tool access. Condition D isolates these: richer input without tools hurts (−25% vs B), while structured tools provide +122% over raw file access. MCP tools are not merely "richer input"; they provide a qualitatively different access modality.

**Covers:** chunk 02-condition-input-f1-b-llm-no, disentanglement paragraph

## Reasoning performance (OWL-RL vs HermiT)

These are different reasoning profiles producing different outputs.

Table 4. LUBM reasoning: OWL-RL (polynomial, incomplete) vs HermiT (exponential, complete). Different profiles, different outputs.

| Axioms | OWL-RL | HermiT | Time ratio |
|---|---|---|---|
| 1,000 | 15 ms | 112 ms | 7.5× |
| 5,000 | 14 ms | 410 ms | 29× |
| 10,000 | 14 ms | 1,200 ms | 86× |
| 50,000 | 15 ms | 24,490 ms | 1,633× |

On the Pizza ontology (4,179 triples), HermiT computes 312 subsumptions in 213 ms; OWL-RL materialises inferred triples in 43 ms but does not compute the same subsumptions. Verbatim claim: "We do not claim to be a 'faster HermiT.'" OWL-RL covers the inference patterns needed for engineering workflows at interactive speeds.

**Covers:** chunk 02-condition-input-f1-b-llm-no, section 4.4 Reasoning Performance

## Pizza ontology construction

Using the Manchester Pizza Tutorial (~4 hours manual work), LLM-driven construction through the MCP tool pipeline produces a 91-class ontology in under 5 minutes, achieving 96% class coverage (95/99 classes). The 4 missing classes are teaching artifacts that exist only to demonstrate OWL syntax variants.

**Covers:** chunk 02-condition-input-f1-b-llm-no, section 4.5 Pizza Ontology Construction

## Ablation: stable matching dominates alignment

Five weight configurations with stable matching enabled, three without (Table 5). All results verified and reproducible from `benchmark/oaei/run ablation.py`.

Table 5. Ablation on OAEI Anatomy (min confidence = 0.80):

| Stable | Weights | Cands | P | R | F1 |
|---|---|---|---|---|---|
| Yes | Full [.25,.20,.15,.15,.15,.10] | 1,152 | 0.965 | 0.734 | 0.834 |
| Yes | Label only [1,0,0,0,0,0] | 1,152 | 0.963 | 0.732 | 0.831 |
| Yes | Structural only [0,.25,.25,.20,.20,.10] | 1,152 | 0.962 | 0.731 | 0.831 |
| Yes | Equal [.167 each] | 1,153 | 0.961 | 0.731 | 0.830 |
| Yes | Label+parent [.4,0,.4,0,0,.2] | 1,154 | 0.964 | 0.734 | 0.833 |
| No | Full | 1,590 | 0.711 | 0.746 | 0.728 |
| No | Label only | 1,590 | 0.711 | 0.746 | 0.728 |
| No | Structural only | 1,590 | 0.711 | 0.746 | 0.728 |

Finding: "signal weights are irrelevant. All five configurations with stable matching produce F1 between 0.830 and 0.834. All three without-stable-matching configurations produce identical F1 = 0.728."

Table 6. Threshold sensitivity with stable matching (full weights):

| Threshold | Cands | P | R | F1 |
|---|---|---|---|---|
| 0.70 | 1,912 | 0.643 | 0.811 | 0.717 |
| 0.75 | 1,474 | 0.821 | 0.798 | 0.809 |
| 0.80 | 1,154 | 0.961 | 0.732 | 0.831 |
| 0.85 | 1,069 | 0.977 | 0.689 | 0.808 |

Why: "On the Anatomy track, most class pairs have no structural data (no shared properties, no instances, no OWL restrictions). When structural signals are all zero, confidence falls back to label similarity. Changing weights on zero-valued signals has no effect. The stable matching constraint selects the top candidate per class, producing a clean 1-to-1 assignment regardless of how the scores were computed."

Threshold sensitivity: "With stable matching, the confidence threshold affects the precision-recall trade-off."

Implication: "The alignment improvement from F1 = 0.182 to F1 = 0.832 is entirely attributable to the matching strategy. For ontologies with limited structural metadata, the assignment constraint matters more than the similarity function."

**Covers:** chunk 02-condition-input-f1-b-llm-no, section 5 Ablation tables 5–6

## Discussion, limitations, conclusion (as given in chunk)

Discussion verbatim points: "Tool access is qualitatively different from information access. The Condition D result (raw file F1 = 0.323 < bare LLM F1 = 0.431) challenges the assumption that giving an LLM more information always helps."; "spending effort on signal engineering (embedding models, property overlap, structural similarity) yields less than 0.004 F1 improvement when stable matching is applied"; two open challenges are the Conference track (F1 = 0.438, label-centric approaches fail under heterogeneous modelling styles) and the Anatomy recall gap (0.733 vs 0.922, requires domain-specific background knowledge).

Limitations: OAEI results not independently evaluated (not yet submitted to official campaign; measured against published reference alignments; planned OAEI 2026); signal ablation limited to Anatomy where structural signals are mostly zero; Condition D methodology uses Claude subagents reading files via Read tool, possibly overestimating D; OWL-RL incomplete for OWL-DL; single-developer project (17,400 lines of Rust); all LLM benchmarks use Claude, other models not evaluated.

Conclusion: "stable 1-to-1 matching is the dominant factor in ontology alignment: it improves OAEI Anatomy F1 from 0.182 to 0.832, while signal weights change F1 by less than 0.004. The same method achieves F1 = 0.438 on the Conference track."; "an LLM reading raw OWL (F1 = 0.323) performs worse than unaided inference (F1 = 0.431), while MCP tools achieve F1 = 0.717."

**Covers:** chunk 02-condition-input-f1-b-llm-no, sections 6 Discussion, 7 Limitations, 8 Conclusion
