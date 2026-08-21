> [[index|Wiki]] | [[summary|Summary]]

# HiGram — Digest

The whole paper at medium depth: every wiki page's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-hierarchical-memory-and-method|Hierarchical Memory and the HiGram Method]]

**In one sentence:** HiGram organizes agent memory into a two-tier hierarchical graph (upper-level abstraction nodes over fine-grained MemoryUnits) and, given a query and an update, localizes the affected evidence path via MicroGraphs before performing coordinated intra-unit and inter-unit rewrites strictly within that bounded region.

- Existing graph-based agent memories are flat and unit-independent: retrieval over an ever-growing flat graph pulls in irrelevant context, and independent unit-wise rewrites require repeated global searches to cover all changes an update propagates, causing high token cost.
- HiGram's core diagnosis: there is a granularity mismatch between how memory is organized/updated (over the whole graph, per unit) and how evidence is actually used (small, localized, interconnected evidence paths).
- The hierarchical memory separates coarse organization (subject / object-category / context upper-level nodes) from fine factual storage (MemoryUnits with explicit inter-unit dependency edges and lifecycle statuses: active, superseded, outdated, pending).
- MicroGraphs are not new memory layers but localized views of the global graph keyed by a (subject, object-category) node pair — chosen because both are stable across temporal updates — used to cheaply retrieve the relevant memory region before detailed evidence selection.
- Path-level localization: temporary MemoryUnits for the query/update → anchor extraction → candidate MicroGraph selection (relevance-ranked, top-Kg) → support subgraph → enumeration of up to Kp candidate evidence paths scored by attribute matching, dependency consistency, temporal validity, and contextual compatibility → single selected evidence path = the rewrite region.
- Coordinated rewriting works only inside the selected path: intra-unit rewriting updates affected MemoryUnit states (new facts committed as active, existing ones revised with temporal/contextual consistency), then inter-unit rewriting re-validates the dependencies of dependent MemoryUnits — dependencies are never blindly inherited and unsupported downstream conclusions are marked outdated.
- Positioning: unlike flat graph-memory baselines and few concurrent hierarchical works (which focus on consolidation), HiGram is the first (in this framing) to combine coarse-to-fine graph organization with query- AND update-conditioned evidence-path localization plus coordinated dependency revision.
- Reported effect (LoCoMo table in this chunk): HiGram improves answer quality (F1/BLEU/LLM-judge across single-hop, multi-hop, open-domain, temporal, adversarial questions) while running at ~2k average token length — far below LLM-based baselines like LoCoMo (~28k), ReadAgent (~14.7k), MemGPT (~4.2k).

## 2. [[wiki/02-experiments-and-results|Experiments and Results]]

**In one sentence:** HiGram achieves the best average F1, BLEU, and LLM-Judge scores on LoCoMo across two backbones (GPT-5.4 and GPT-4o) while using only 7.2% of the tokens of full-context, and it ranks first on all overall and evidence-selection metrics on MemConflict, with both its MicroGraph organization and localized support subgraph contributing complementary, load-bearing roles.

- **Benchmarks.** LoCoMo (five question categories: Single-Hop, Multi-Hop, Open Domain, Temporal, Adversarial) and MemConflict (Dynamic, Static, Conditional conflict subsets).
- **Baselines.** LoCoMo: LoCoMo (full context), MemoryBank, A-MEM, ReadAgent, MemGPT, Mem0. MemConflict: A-MEM, Mem0, LangMem, Letta, MemOS.
- **Headline (LoCoMo).** HiGram wins on average F1, BLEU, and LLM-J under both GPT-5.4 and GPT-4o; its token length of ~2,912 is 7.2% of full-context (4,909) tokens and 15.8% of ReadAgent's (3,873) under GPT-4o.
- **Headline (MemConflict).** HiGram leads on Macro-AA (67.84), SEH@3 (81.06), and SRS (77.31), with best Static AA (68.75) and Cond AA (90.00); it is best on UOCS for Dynamic conflicts.
- **Ablation.** Removing MicroGraph raises token use by 68.6% and drops LLM-J on all categories; removing the support subgraph causes the broadest quality decline, especially on Multi-Hop F1 (~33 to ~19).
- **Update strategy (Table 3).** HiGram's coordinated rewrite outperforms both Append-Only (avg 42.89) and Relation-level (avg 40.76) update strategies, achieving 56.77 average with the strongest Static AA (68.75).
- **Hyperparameters.** Performance is stable across K_g (8–16) and K_p (16–32); gains are gentle and saturating, so careful tuning is unnecessary.

## The argument in five moves

1. Flat, unit-independent graph memories force retrieval over the whole graph and repeated global re-search on every update — expensive and prone to leaving stale dependencies in place.
2. HiGram splits memory into coarse upper-level organization nodes and fine-grained MemoryUnits with explicit dependency edges, so region-level and fact-level structure are handled separately.
3. MicroGraphs (localized views keyed by stable subject/object-category pairs) let the system cheaply narrow to a small relevant region before doing any expensive path scoring.
4. Within that region, a single evidence path is selected and rewriting is confined to it: matched units are updated (intra-unit), then their dependents are re-validated rather than blindly inherited (inter-unit) — outdated conclusions get marked, not left to rot.
5. On LoCoMo and MemConflict this localize-then-rewrite design beats full-context and independent-unit-update baselines on both answer quality and token cost, and ablations confirm both the MicroGraph organization and the support-subgraph localization are independently load-bearing.
