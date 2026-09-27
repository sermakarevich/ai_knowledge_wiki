---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: From Restructuring to Stabilization: A Large-Scale Experiment on Iterative Code Readability Refactoring with Large Langu

### Q1. What was the full experimental design (corpus, variants, prompts, iterations, model) and the three research questions?

> [!tip]- Answer
> The study sampled 230 Java files from TheAlgorithms-Java meeting quality/size criteria, each in three variants (Original, Meaningless identifiers/comments, NoComment), refactored over five iterations under three prompts (PromptGeneral, PromptMeaning, PromptComments) with GPT-5.1 at temperature 0 via stateless calls, totaling 10,350 snippets.
> RQ1 asks how iterative refactoring evolves on already best-practice code, RQ2 whether degraded variants of the same snippet converge when refactored independently, and RQ3 whether prompts explicitly emphasizing a readability aspect make targeted refactoring more effective.
> See [[wiki/01-restructuring-to-stabilization-overview|From Restructuring to Stabilization: Overview]].

### Q2. What "restructuring, then stabilizing" trajectory did already-clean code (Original + PromptGeneral, RQ1) follow?

> [!tip]- Answer
> Unchanged lines rose 45% (v0→v1) → 76% → 86% → 89% → 92% (v4→v5), with early restructuring (9% renames, 11% code insertions in v0→v1) fading until no change type dominated and all types fell below 1%.
> Structurally, code lines grew 58 to over 73 by v5 while empty lines and method counts rose then stabilized from v3 onward, comment lines fell slowly, and inline comments were almost completely removed.
> Adjacent-version changed-line similarity rose 0.86 → 0.90 but never reached 1.00, indicating persistent micro-changes and an over-refactoring tendency.
> See [[wiki/01-restructuring-to-stabilization-overview|From Restructuring to Stabilization: Overview]].

### Q3. How did the degraded Meaningless and NoComment variants compare to Original over the five iterations (RQ2)?

> [!tip]- Answer
> Meaningless started at 31% unchanged (v0→v1, with 24% renames) and NoComment at 44% unchanged (14% renames), then both mirrored the Original trajectory to reach 90% and 89% unchanged by v4→v5, with the bulk of repair in the first two iterations.
> Absolute metrics converged too: code lines rose from ~56 to ~73 and method counts from 3.1 to ~6 across all variants, while inline comments fell to ~0.2.
> Cross-variant similarity converged to ≈0.87 within less than 3% spread (Original–NoComment falling 0.98→0.87, Meaningless–NoComment rising 0.85→0.87), supporting LLM-driven structural normalization, with NoComment converging slightly faster than Meaningless.
> See [[wiki/02-similarity-across-iterations|Similarity Across Iterations]].

### Q4. How did the targeted prompts (PromptMeaning, PromptComments) change the refactoring dynamics without breaking convergence (RQ3)?

> [!tip]- Answer
> PromptMeaning kept structural metrics relatively stable but made renames dominate (Original ≈20% even in later iterations; Meaningless v0→v1 31% renames; NoComment ~30% renames persisting, 30.5% ± 11.0% overall), sometimes inducing oscillatory renaming, and achieved a higher average cross-variant similarity than PromptComments.
> PromptComments front-loaded comment insertions/deletions/changes into v0→v1 (e.g. ~36% comment changes for Meaningless in the first transition) with no further comment inflation later, then stabilized rapidly, though its heatmaps showed more back-and-forth changes.
> A Kruskal-Wallis H test was used for Rename/CommentChange significance since proportional change metrics are not guaranteed normal.
> See [[wiki/02-similarity-across-iterations|Similarity Across Iterations]].

### Q5. What content can be recovered from wiki chunk 03/20 on identifier/expression rename fragments, and how should it be treated?

> [!tip]- Answer
> Nothing substantive can be recovered: the chunk body is garbled pdftotext/AST-diff extraction noise with no complete sentences, numbers, tables, or mechanisms, only scattered tokens such as `Identifier → ExpressionNode` and `DeclarationNode`.
> Per the task contract no content may be invented beyond the chunk, so the page is intentionally a placeholder to be triaged or merged once clean source text is available.
> See [[wiki/03-identifier-expression-rename-fragments|Identifier / Expression Rename Fragments (chunk 03/20)]].

### Q6. What does wiki chunk 04/20 on declaration/privacy fragments contain, and what is its status?

> [!tip]- Answer
> It contains only scattered node-type and modifier tokens — Declaration/DeclarationNode, ExpressionNode, TryWithResourcesStatement, Private, Public, Protected, Static, Final, plus type tokens (ArrayType, IntegralType, Int, VoidType, BooleanType, Byte, Double, Long, GenericType, ScopedTypeIdentifier, TypeIdentifier) and statement tokens (SingleStatement, LabeledStatement, EnhancedForStatement, Block, FormalParameters, MethodReference, RecordDeclaration) — with no sentences, numbers, or claims.
> It is a garbled extraction artifact flagged for triage/merge with sibling chunks 03–20 rather than citation as a finding.
> See [[wiki/04-declaration-privacy-fragments|Declaration / Privacy Fragments]].

### Q7. What can be summarized from wiki chunk 05/20 on assert/boolean-type fragments?

> [!tip]- Answer
> Nothing factual can be summarized: the body holds only whitespace-scattered AST-diff tokens such as `Identifier`, `AssertStatement`, `BooleanType`, `Node`, and `Node → Double`, with no sentences, measurements, tables, or verbatim quotes.
> Although the plan expected assert/boolean/node-type coverage, the body does not confirm it, so the page stands as an intentional placeholder with nothing invented.
> See [[wiki/05-assert-boolean-type-fragments|Assert / Boolean-Type Fragments (chunk 05/20)]].

### Q8. What is recoverable from wiki chunk 06/20 on single-node structural fragments?

> [!tip]- Answer
> Only isolated tokens such as `ControlNode`, `Single`, `lNode`, `ancedF`, `Statement`, `Fragment`, `Program`, and `AccessNode` are recoverable, with no complete sentences, numbers, mechanisms, or comparisons.
> The expected single-node structural coverage from plan.md is unconfirmed by the body, so per the no-invention rule the page records the chunk as empty pending triage/merge.
> See [[wiki/06-single-node-structural-fragments|Single-Node Structural Fragments (chunk 06/20)]].

### Q9. What does wiki chunk 07/20 contain, and why is its title unreliable?

> [!tip]- Answer
> The body carries no prose or argument, only scattered AST node labels such as ProbablyStringFragment, EnhancedForStatement, ControlNode, Program, LiteralNode, ExpressionNode, and DeclarationNode, with no research questions, numbers, tables, or quotes.
> The title itself (`ProbablyStringFragment EnhancedForStatement → ControlNode Program ControlNode`) is a garbled extraction artifact rather than a paper section heading, so the page is left as a stub for later merging instead of citing noise.
> See [[wiki/07-control-statement-fragments|ProbablyStringFragment EnhancedForStatement → ControlNode Program ControlNode]].

### Q10. What is the status of wiki chunk 08/20 on operator/expression fragments?

> [!tip]- Answer
> It is a garbled pdftotext/AST-diff artifact with no extractable claims: only scattered labels (OperatorNode, ExpressionNode, DeclarationNode, TypeIdentifier, ArrayType, EnhancedForStatement, IntegralType) plus bare arrows (`→`) and separators (`;`, `,`), e.g. `; → OperatorNode`, with no surrounding explanation.
> Per the source plan it was expected to cover operator/expression fragments, but the body does not confirm that, so it should be folded into a later merge rather than read as a substantive result.
> See [[wiki/08-operator-expression-fragments|OperatorNo Expres sionNod pKF2 sionN e]].

### Q11. What can be faithfully reported from wiki chunk 09/20 (`ExpressionNode Program → ExpressionNode → →`)?

> [!tip]- Answer
> Only that the body is whitespace-separated AST/fragment labels — ExpressionNode, Program, ArrayType, Declaration/DeclarationNode, SingleStatement, LabeledStatement, EnhancedForStatement, Block, ControlNode, IncompleteSwitchCase, Long/Int/String, TypeIdentifier, TryWithResources, LineComment, ProbablyStringFragment and truncations like `lyS`/`tringFr` — with no sentences, numbers, mechanisms, or quotes.
> No interpretation of what refactored into what is warranted, and per the plan.md note the page is a placeholder pending triage/merge, not a finding.
> See [[wiki/09-expression-node-program-fragments|ExpressionNode Program → ExpressionNode → →]].

### Q12. What does wiki chunk 10/20 on structural/integral-type change fragments yield?

> [!tip]- Answer
> The ~63k-character body is almost entirely whitespace, yielding only ~35 alphabetic tokens of length ≥3 such as `OtherStructuralChange`, `IntegralType`, `atement`, `Singl`, and `Declarati`/`Decla`/`SingleState`.
> No sentence, number, mechanism, measurement, table, figure, or quotable finding is present, so nothing from it may be cited; it awaits triage/merge with sibling extraction-batch fragments once clean source text exists.
> See [[wiki/10-structural-type-fragments|Structural / Integral-Type Change Fragments]].

### Q13. What are the key facts about wiki chunk 11/20 (`cla → TypeIdeonNode lizer ration Enha`)?

> [!tip]- Answer
> The ~127 KB body over 68 lines is nearly all whitespace padding with only ~67 alphabetic tokens (51 distinct) and no complete sentences, tables, numbers, or mechanisms — the most frequent tokens being short fragments (`sio` × 5, `cla` × 4) plus `TypeIdeonNode` × 2 and `SingleSttatemen`.
> Its provisional plan label (type-identifier normalization fragments) fails confirmation against the body, so nothing from it should be cited and downstream merges should skip it or re-extract from the source PDF.
> See [[wiki/11-type-normalization-fragments|Type-identifier normalization fragments (chunk 11/20 — garbled extraction artifact)]].

### Q14. What is recoverable from wiki chunk 12/20 on change-classification fragments?

> [!tip]- Answer
> The ~85k-character body yields only 26 alphabetic tokens of length ≥3 (20 unique) — fragments like `tio` × 3, `sio` × 3, `nge` × 2, `ExpressionNode` × 2 — with the single most complete line being `ExpressionNode → ExpressionNode`.
> With no sentence, number, mechanism, table, or figure present and nothing invented per the task contract, it must be triaged/merged with sibling chunks 03–20 rather than cited.
> See [[wiki/12-change-classification-fragments|Change-Classification Fragments]].

### Q15. What does wiki chunk 13/20 (`sionN tatem t Acc od Strin`) contain?

> [!tip]- Answer
> Only garbled pdftotext/AST-diff fragments across 69 lines (~71 KB of mostly whitespace): generic AST-token shards such as ExpressionNode, Public, Probably, String, Literal, and Control/Continue/ForState-like tokens.
> No complete sentences, quantitative results, tables, quotable claims, mechanisms, or findings are present, so per the plan.md triage note it should be merged or discarded rather than treated as substantive evidence.
> See [[wiki/13-accessor-string-fragments|Accessor / String Fragments (chunk 13/20 — garbled extraction batch)]].

### Q16. What is the content status of wiki chunk 14/20 (`lyStrin clarat De Acce de Exp`)?

> [!tip]- Answer
> The 53-line (~68 KB) body is overwhelmingly whitespace padding with only scattered shards such as String, Declaration-like (`clarat`, `Declarat`), Access (`Acce`, `Acc`), Expression/Express, and Node-like (`Nod`, `nNod`) tokens.
> It offers no sentences, numbers, mechanisms, or comparisons to summarize faithfully, so it belongs to the garbled extraction batch slated for merge or disposal.
> See [[wiki/14-declaration-access-fragments|Declaration / Access Fragments (chunk 14/20 — garbled extraction batch)]].

### Q17. What characterizes wiki chunk 15/20 (`yWith → Priv de Id e→`) on privacy/identifier fragments?

> [!tip]- Answer
> The ~68,626-character body holds only 178 non-whitespace characters across 54 tokens — fragment labels like `yWith`, `Priv`, `de`, `Id`, `OperatorNode`, `ExpressionNode`, `NoralNode`, `Decla`, `Identifie`, plus arrows and semicolons — forming no sentence, number, mechanism, table, or quotable claim.
> Its title is itself a garbled artifact rather than a paper heading, and nothing on the page may be cited as a paper finding; real privacy/identifier content would require re-extraction from the source.
> See [[wiki/15-privacy-identifier-fragments|Privacy / Identifier Fragments (chunk 15/20: yWith → Priv de Id e→)]].

### Q18. What does wiki chunk 16/20 (`Ide nt essio e → Co`) on expression coverage yield, and what do chunks 03–20 share?

> [!tip]- Answer
> Chunk 16 yields no sentences, numbers, or mechanisms — only broken fragments (`Ide`, `nt`, `essio`, `ntif`, `pre`, `ode`, `ion`, plus shards like AccessNode, Program, FormalPara, Enhanc, Sing) — so per the no-invention rule it is recorded as empty.
> All sibling chunks 03–20 share this garbled extraction-batch character and should be triaged or merged rather than read as substantive findings.
> See [[wiki/16-expression-coverage-fragments|Expression Coverage Fragments (Chunk 16/20 — Garbled Extraction Artifact)]].

### Q19. What pair of facts must you recall about wiki chunks 17/20, 18/20, and 19/20?

> [!tip]- Answer
> All three are garbled pdftotext/AST-diff artifacts with no extractable claims: chunk 17 shows only Identifier/Declaration/ExpressionN/SingleStat/Integra-Contr shards with no subsection structure, chunk 18 only SingleStatement/DeclarationNode/ExpressionNode/Continue/Declaration tokens, and chunk 19 only SingleStatement/AssertStatement/ArrayType/ExpressionNode/RecordDeclaration/IntegralType tokens.
> Each page therefore records its garbled status instead of inventing content, belonging to the extraction batch (chunks 03–20) flagged for triage/merge rather than standalone claims.
> See [[wiki/17-identifier-contrast-fragments|Identifier Contrast Fragments (Chunk 17/20 — Garbled Extraction Artifact)]].
> See also [[wiki/18-continue-declaration-fragments|Continue / Declaration Fragments (Chunk 18/20)]] and [[wiki/19-array-assert-statement-fragments|Array / Assert Statement Fragments (Chunk 19/20)]].

### Q20. Your team proposes running unbounded iterative LLM refactoring on already-clean code in CI with a naming-focused prompt and no stopping rule — what should you recommend, and why?

> [!tip]- Answer
> Recommend against it: even best-practice code drifts (code lines 58→73+, inline comments nearly eliminated) with persistent micro-changes that never reach 1.00 similarity, naming-focused prompts induce oscillatory renaming (~20–30% renames persisting), and functionality breaks, though rare, are non-zero per iteration.
> Instead adopt the paper's guardrails — an explicit stopping criterion (convergence stabilizes after ~2–3 iterations), careful prompt phrasing, and mechanisms to preserve valuable comments — while noting the caveats that readability was never directly measured, only GPT-5.1 was tested in the main experiment, temperature-0 runs remain slightly non-deterministic, and aggregation can hide individual back-and-forth changes.
> See [[wiki/20-declaration-string-fragments|Threats to Validity and Conclusion (Chunk 20/20)]].
