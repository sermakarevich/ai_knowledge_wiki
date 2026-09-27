> [[index|Wiki]] | [[summary|Summary]]
# From Restructuring to Stabilization: A Large-Scale Experiment on Iterative Code Readability Refactoring with Large Langu — Digest

## 1. [[wiki/01-restructuring-to-stabilization-overview|From Restructuring to Stabilization: Overview]]
**In one sentence:** A large-scale experiment iteratively refactoring 230 Java snippets with GPT-5.1 over five iterations under three prompts finds a consistent "restructuring, then stabilizing" dynamic that converges toward an apparently internalized notion of readable code, robust across degraded starting variants and only slightly steered by targeted prompts.
## Key points
- Large-scale design: 230 Java files from TheAlgorithms-Java × 3 variants (Original, Meaningless, NoComment) × 3 prompts × 5 iterations = 10,350 generated snippets, using GPT-5.1 at temperature 0 with stateless API calls.
- Main dynamic (RQ1, Original + PromptGeneral): unchanged lines rise 45% (v0→v1) → 76% → 86% → 89% → 92% (v4→v5), with early restructuring (9% renames, 11% code insertions in v0→v1) fading to no dominant type and all types <1% later.
- Structural drift on already-good code: code lines rise 58 → over 73 (v0→v5), empty lines and method counts rise and stabilize from v3 onward, comment lines fall slowly and inline comments are almost completely removed.
- Convergence without full stability: adjacent-version changed-line similarity rises 0.86 (v0→v1) → 0.90 (v4→v5), early-to-late pairs (v1→v4 = 0.87, v2→v5 = 0.88) show early convergence, but no pair reaches 1.00, indicating persistent micro-changes / over-refactoring tendency.
- Robustness across degraded inputs (RQ2): Meaningless starts at 31% unchanged (v0→v1, 24% renames) and NoComment at 44% unchanged (14% renames), then both follow the Original trajectory to 90% and 89% unchanged by v4→v5, with code lines converging 56 → ~73 and methods 3.1 → ~6 across all variants.
- Prompting and guardrails: targeted prompts steer change types without altering overall convergence, naming-focused prompts may induce oscillatory renaming, and functionality breaks are rare but non-zero per iteration, motivating explicit stopping criteria and care with valuable comments.

## 2. [[wiki/02-similarity-across-iterations|Similarity Across Iterations]]
**In one sentence:** Despite divergent starting similarities (0.98 vs 0.85), all variant pairs converge to ≈0.87 within <3% difference over five refactoring iterations, supporting LLM-driven structural normalization, while targeted prompts (Meaning vs Comments) change the change-type mix without breaking cross-variant convergence.
## Key points
- At v0 under PromptGeneral, Original–NoComment similarity is 0.98 (identical code except removed comments), while Original–Meaningless and Meaningless–NoComment start at 0.85 (renamed identifiers/changed comments).
- Across five iterations all three pairs converge to ≈0.87: Original–NoComment falls 0.98→≈0.87, Meaningless–NoComment rises slightly 0.85→0.87, closing in on Original–Meaningless.
- Final curves sit within a narrow range of less than 3% difference, interpreted as convergence to similar structural representations despite divergent starts (RQ2 hypothesis).
- RQ2 summary: structural metrics (code, comment, empty lines) largely stabilize after the second iteration; most line-level changes occur early; within-variant (v0–v5) and cross-variant scores converge to typically 0.87–0.90 by the final iteration; NoComment converges slightly faster than Meaningless.
- PromptMeaning keeps structural metrics (total lines, methods, code lines) relatively stable versus PromptGeneral's pronounced first-two-iteration growth; for NoComment there is essentially no change in method/comment-line counts, and empty lines are added less.
- PromptComments raises line/inline comment counts (primarily in the first iteration) with code-line/method dynamics similar to PromptGeneral, but inline comments stay very low and comment counts do not keep inflating in later versions.
- Change-type dynamics: under PromptMeaning renames dominate (Original ≈20% even in later iterations; Meaningless v0→v1 31% rename; NoComment v0→v1 31% rename and ~30% rename persisting), while under PromptComments the bulk of comment insertions/deletions/changes concentrates in v0→v1 (e.g. Meaningless ~36% comment changes in first transition) then rapidly stabilizes.
- Figure 22 comparison: both PromptMeaning and PromptComments converge rapidly across variant pairs with the largest change at v0→v1, and PromptMeaning achieves a higher average similarity than PromptComments; Table 4 descriptives (e.g. NoComment Rename 30.5% ± 11.0% under PromptMeaning; Original Rename 20.5% ± 9.3%) with Kruskal-Wallis H test used for Rename/CommentChange significance.

## 3. [[wiki/03-identifier-expression-rename-fragments|Identifier / Expression Rename Fragments (chunk 03/20)]]
**In one sentence:** The chunk body for 03/20 is garbled pdftotext/AST-diff extraction noise (scattered `Identifier → ExpressionNode` tokens with no sentences, numbers, or mechanisms), so no factual claims can be summarised from it.
## Key points
- The chunk body contains no complete sentences, only whitespace-scattered AST-diff tokens such as `Identifier → ExpressionNode` and `DeclarationNode`.
- No exact numbers, tables, measurements, or verbatim quotes are recoverable from the chunk.
- No mechanisms, comparisons, or argumentative claims are present in the chunk body.
- Per plan.md, this chunk was expected to cover identifier/expression-node rename fragments, but the body does not confirm that.
- Per the task contract, no content is invented beyond what the chunk contains; this page is intentionally a placeholder.

## 4. [[wiki/04-declaration-privacy-fragments|Declaration / Privacy Fragments]]
**In one sentence:** This chunk is a garbled pdftotext/AST-diff extraction artifact with no recoverable argument, containing only scattered node-type and modifier tokens such as Declaration, ExpressionNode, TryWithResources, Private, and Public.
## Key points
- The chunk body contains no complete sentences or coherent claims, only whitespace-scattered single tokens and fragments.
- Recurring tokens observable in the body include Declaration/DeclarationNode, ExpressionNode, TryWithResourcesStatement, and modifiers Private, Public, Protected, Static, and Final.
- Recurring type tokens observable in the body include ArrayType, IntegralType, Int, VoidType, BooleanType, Byte, Double, Long, GenericType, ScopedTypeIdentifier, and TypeIdentifier.
- Recurring statement tokens observable in the body include SingleStatement, LabeledStatement, EnhancedForStatement, Block, FormalParameters, MethodReference, and RecordDeclaration.
- No numbers, mechanisms, results, figures, tables, or verbatim quotable claims are present in recoverable form.
- Per the source plan note, chunks 03–20 of this paper are garbled extraction batches that should be triaged/merged rather than treated as substantive findings.

## 5. [[wiki/05-assert-boolean-type-fragments|Assert / Boolean-Type Fragments (chunk 05/20)]]
**In one sentence:** The chunk body for 05/20 is garbled pdftotext/AST-diff extraction noise (scattered `Identifier`, `AssertStatement`, `BooleanType`, `Node → Double` tokens with no sentences, numbers, or mechanisms), so no factual claims can be summarised from it.
## Key points
- The chunk body contains no complete sentences, only whitespace-scattered AST-diff tokens such as `Identifier`, `AssertStatement`, `BooleanType`, `Node`, and `Double`.
- No exact numbers, tables, measurements, or verbatim quotes are recoverable from the chunk.
- No mechanisms, comparisons, or argumentative claims are present in the chunk body.
- Per plan.md, this chunk was expected to cover assert/boolean/node-type fragments, but the body does not confirm that.
- Per the task contract, no content is invented beyond what the chunk contains; this page is intentionally a placeholder.

## 6. [[wiki/06-single-node-structural-fragments|Single-Node Structural Fragments (chunk 06/20)]]
**In one sentence:** The chunk body for 06/20 is garbled pdftotext/AST-diff extraction noise (scattered `ControlNode`, `Single`, `lNode`, `ancedF`, `Statement`, `Fragment` tokens with no sentences, numbers, or mechanisms), so no factual claims can be summarised from it.
## Key points
- The chunk body contains no complete sentences, only whitespace-scattered AST-diff tokens such as `ControlNode`, `Single`, `lNode`, `ancedF`, `Statement`, `Fragment`, `Program`, and `AccessNode`.
- No exact numbers, tables, measurements, or verbatim quotes are recoverable from the chunk.
- No mechanisms, comparisons, or argumentative claims are present in the chunk body.
- Per plan.md, this chunk was expected to cover single-node structural fragments, but the body does not confirm that.
- Per the task contract, no content is invented beyond what the chunk contains; this page is intentionally a placeholder.

## 7. [[wiki/07-control-statement-fragments|ProbablyStringFragment EnhancedForStatement → ControlNode Program ControlNode]]
**In one sentence:** The chunk contains no recoverable prose — it is a garbled pdftotext/AST-diff artifact of node-label fragments (e.g. EnhancedForStatement, ControlNode, LiteralNode) with no extractable claims.
## Key points
- The chunk body carries no complete sentences or argument, only scattered AST node labels.
- No research questions, methods, numbers, tables, or verbatim quotes are recoverable from the chunk.
- Recurring labels include ProbablyStringFragment, EnhancedForStatement, ControlNode, Program, LiteralNode, ExpressionNode, and DeclarationNode.
- No mechanism, comparison, or result can be attributed to the source paper from this chunk alone.
- Per the source plan.md, this chunk was expected to cover enhanced-for/control-node fragments, but the body does not confirm that.
- The page is intentionally left as a stub so later merges can fold any real content in rather than citing noise.

## 8. [[wiki/08-operator-expression-fragments|OperatorNo Expres sionNod pKF2 sionN e]]
**In one sentence:** The chunk contains no recoverable prose — it is a garbled pdftotext/AST-diff artifact of node-label fragments (e.g. OperatorNode, ExpressionNode, DeclarationNode) with no extractable claims.
## Key points
- The chunk body carries no complete sentences or argument, only scattered AST node labels.
- No research questions, methods, numbers, tables, or verbatim quotes are recoverable from the chunk.
- Recurring labels include OperatorNode, ExpressionNode, DeclarationNode, TypeIdentifier, ArrayType, EnhancedForStatement, and IntegralType.
- The only operators present are arrows (`→`) and separators (`;`, `,`), e.g. `; → OperatorNode` and `, → OperatorNode`, with no surrounding explanation.
- No mechanism, comparison, or result can be attributed to the source paper from this chunk alone.
- Per the source plan.md, this chunk was expected to cover operator/expression fragments, but the body does not confirm that.
- The page is intentionally left as a stub so later merges can fold any real content in rather than citing noise.

## 9. [[wiki/09-expression-node-program-fragments|ExpressionNode Program → ExpressionNode → →]]
**In one sentence:** The chunk body for this section is garbled pdftotext/AST-diff artifact text with no extractable claims, so no summary beyond that can be faithfully given.
## Key points
- The chunk contains no complete sentences, numbers, mechanisms, or verbatim quotes to summarize — only isolated AST/fragment labels separated by whitespace.
- The only reliably readable tokens are node/fragment labels such as `ExpressionNode`, `Program`, `ArrayType`, `Declaration`/`DeclarationNode`, `SingleStatement`, `LabeledStatement`, `EnhancedForStatement`, `Block`, `ControlNode`, `IncompleteSwitchCase`, `Long`, `Int`, `String`, `TypeIdentifier`, `TryWithResourcesSt`/`TryWithResources`, `LineComment`, and `ProbablyStringFragment` (plus truncated fragments like `lyS`, `agm`, `bably`, `tringFr`, `ProbablyStrin`).
- The chunk contains no quantitative results, tables, definitions, or causal/mechanistic claims, so none are reported here rather than invented.
- Per the source `plan.md` note, chunks 03–20 of this paper carry garbled extraction-batch titles and this page is intentionally a placeholder pending triage/merge, not a substantive finding.
- No further interpretation of the token sequence (e.g., what refactored into what) is warranted from the body as given.

## 10. [[wiki/10-structural-type-fragments|Structural / Integral-Type Change Fragments]]
**In one sentence:** The chunk for this section contains only garbled pdftotext/AST-diff artifact tokens (e.g. "OtherStructuralChange", "IntegralType") with no recoverable claims, so no substantive summary is possible.
## Key points
- The chunk body (≈63k characters) consists almost entirely of whitespace plus fragmented tokens, yielding only ~35 alphabetic tokens of length ≥3.
- The only recurring tokens are fragment labels such as "OtherStructuralChange", "atement", "IntegralType", "Singl", "Declarati"/"Decla", and "SingleState".
- No complete sentence, number, mechanism, measurement, or verbatim finding is present in the chunk.
- No tables, figures, timestamps, or quotes can be extracted because none exist in the source text.
- Per the task contract, no content has been invented or imported from other chunks, the original paper, or the web.
- The appropriate handling is triage/merge with sibling extraction-batch fragments (chunks 03–20) once clean source text is available.

## 11. [[wiki/11-type-normalization-fragments|Type-identifier normalization fragments (chunk 11/20 — garbled extraction artifact)]]
**In one sentence:** Chunk 11 ("cla → TypeIdeonNode lizer ration Enha") contains no recoverable argument — it is ~127 KB of whitespace-padded pdftotext/AST-diff fragments with only ~67 alphabetic tokens and no complete sentences, tables, or numbers.
## Key points
- The chunk body yields no complete claim about the paper's experiment, methods, or results — only split tokens such as `TypeIdeonNode`, `OtherStructuralChange`, and `SingleSttatemen`.
- The file is ~127,219 characters over 68 lines but nearly all whitespace; only ~67 alphabetic tokens (51 distinct) carry any letters.
- The most frequent tokens are short fragments (`sio` × 5, `cla` × 4, `ration` × 3, `TypeIdeonNode` × 2, `lizer` × 2, `Enha` × 2), none forming a sentence or measurement.
- No exact numbers, effect sizes, iteration counts, similarity scores, tables, or verbatim paper quotes are present in the chunk.
- No mechanism (e.g., renaming, normalization, restructuring rule) is described completely enough to summarize.
- Per the source plan, this slot was provisionally labeled "Type-identifier normalization fragments (extraction batch; worker to confirm against body)" — confirmation against the body fails because the body is garbled.
- Nothing from this chunk should be cited as a paper finding; downstream merges should skip it or re-extract from the source PDF.

## 12. [[wiki/12-change-classification-fragments|Change-Classification Fragments]]
**In one sentence:** The chunk for this section contains only garbled pdftotext/AST-diff artifact tokens (e.g. "ExpressionNode → ExpressionNode") with no recoverable claims, so no substantive summary is possible.
## Key points
- The chunk body (≈85k characters) consists almost entirely of whitespace plus fragmented tokens, yielding only 26 alphabetic tokens of length ≥3 (20 unique).
- The only recurring tokens are fragments such as "tio" (×3), "sio" (×3), "nge" (×2), "ExpressionNode" (×2), plus "Ide", "Nod", "Enhanc", "Cont", and "Expres".
- The single most complete verbatim line is "ExpressionNode → ExpressionNode"; all other lines are 1–2 syllable fragments (e.g. "si", "an", "nge", "Ch", "on").
- No complete sentence, number, mechanism, measurement, or finding is present in the chunk.
- No tables, figures, timestamps, or quotes can be extracted because none exist in the source text.
- Per the task contract, no content has been invented or imported from other chunks, the original paper, or the web.
- The appropriate handling is triage/merge with sibling extraction-batch fragments (chunks 03–20) once clean source text is available.

## 13. [[wiki/13-accessor-string-fragments|Accessor / String Fragments (chunk 13/20 — garbled extraction batch)]]
**In one sentence:** Chunk 13 ("sionN tatem t Acc od Strin") contains only garbled pdftotext/AST-diff fragments with no extractable claims, numbers, or mechanisms.
## Key points
- The chunk body (69 lines, ~71 KB) is almost entirely whitespace padding with scattered single-word fragments.
- Recognizable fragments include generic AST-token shards such as ExpressionNode, Public, Probably, String, Literal, and Control/Continue/ForState-like tokens.
- No complete sentences, quantitative results, tables, or verbatim quotable claims are present in the chunk.
- No mechanisms, comparisons, or findings can be faithfully summarized without inventing content.
- Per the plan.md triage note, this extraction-batch chunk should be merged or discarded rather than treated as substantive evidence.

## 14. [[wiki/14-declaration-access-fragments|Declaration / Access Fragments (chunk 14/20 — garbled extraction batch)]]
**In one sentence:** Chunk 14 ("lyStrin clarat De Acce de Exp") contains only garbled pdftotext/AST-diff fragments with no extractable claims, numbers, or mechanisms.
## Key points
- The chunk body (53 lines, ~68 KB) is almost entirely whitespace padding with scattered single-word fragments.
- Recognizable fragments include generic AST-token shards such as String, Declaration-like ("clarat", "Declarat"), Access ("Acce", "Acc"), Expression/Express, and Node-like ("Nod", "nNod") tokens.
- No complete sentences, quantitative results, tables, or verbatim quotable claims are present in the chunk.
- No mechanisms, comparisons, or findings can be faithfully summarized without inventing content.
- Per the plan.md triage note, this extraction-batch chunk should be merged or discarded rather than treated as substantive evidence.

## 15. [[wiki/15-privacy-identifier-fragments|Privacy / Identifier Fragments (chunk 15/20: yWith → Priv de Id e→)]]
**In one sentence:** This chunk contains no recoverable argument — it is a garbled pdftotext/AST-diff artifact of scattered identifier/privacy-related node fragments, so no paper claim can be summarised from it.
## Key points
- The chunk body holds ~68,626 characters but only 178 non-whitespace characters across 54 whitespace-separated tokens, i.e. it is overwhelmingly blank padding.
- The only legible tokens are fragment labels such as `yWith`, `Priv`, `de`, `Id`, `OperatorNode`, `ExpressionNode`, `NoralNode`, `Decla`, `Identifie`, `Frag`, `Ex`, `No`, `me`, `ment`, `ess`, `Acc`, `lN`, `ier`, and arrows/semicolons — none forms a sentence.
- No complete claim, number, mechanism, table, figure, timestamp, or verbatim quotable sentence is present in the chunk body.
- The chunk title itself (`yWith → Priv de Id e→`) is a garbled artifact title, not a paper section heading, matching the plan.md note that chunks 03–20 carry garbled extraction titles.
- Per plan.md, this chunk maps to privacy/identifier fragments (extraction batch, worker to confirm against body); the body confirms there is nothing substantive to merge beyond that label.
- Nothing in this page should be cited as a finding of the paper; any real privacy/identifier content must come from a re-extraction of the source, not from this chunk.

## 16. [[wiki/16-expression-coverage-fragments|Expression Coverage Fragments (Chunk 16/20 — Garbled Extraction Artifact)]]
**In one sentence:** Chunk 16 ("Ide nt essio e → Co") contains no recoverable argument — it is a garbled pdftotext/AST-diff extraction artifact with only scattered identifier fragments and no complete claims, numbers, or mechanisms.
## Key points
- The chunk body holds no complete sentences or claims, only whitespace with isolated fragments such as "Ide", "nt", "essio", "ntif", "pre", "ode", and "ion".
- No numbers, tables, measurements, or verbatim quotable statements are present in the chunk.
- No refactoring mechanism, experimental result, or conclusion can be extracted from the chunk without inventing content.
- Scattered tokens (e.g., "AccessNode", "Program", "FormalPara", "Enhanc", "Sing") appear only as broken word fragments, not as usable claims.
- Per the no-invention rule, this page records the chunk as empty rather than synthesising a summary.
- Sibling chunks 03–20 share the same garbled extraction-batch character and should be triaged/merged rather than read as substantive findings.

## 17. [[wiki/17-identifier-contrast-fragments|Identifier Contrast Fragments (Chunk 17/20 — Garbled Extraction Artifact)]]
**In one sentence:** Chunk 17 (`17-identifier-e-contr-ier-cont`) contains only garbled pdftotext/AST-diff fragments with no extractable claims, numbers, or mechanisms.
## Key points
- The chunk body has no complete sentences or verifiable claims to summarise.
- Only scattered artifact tokens (e.g. Identifier, Declaration, ExpressionN, SingleStat, Integra/Contr fragments) appear amid whitespace noise.
- No numbers, tables, comparisons, or verbatim quotes can be recovered from the chunk.
- No subsection structure exists in the source to mirror.
- Per the task fallback rule, this page records the garbled status instead of inventing content.

## 18. [[wiki/18-continue-declaration-fragments|Continue / Declaration Fragments (Chunk 18/20)]]
**In one sentence:** This chunk contains no readable prose — only garbled pdftotext/AST-diff fragments (SingleStatement, DeclarationNode, ExpressionNode, Continue tokens) — so no substantive claim can be summarized from it.
## Key points
- The chunk body carries no complete sentences or argumentative claims to summarize.
- Its legible tokens are AST-diff artifacts (e.g. SingleStatement, DeclarationNode, ExpressionNode, Continue, Declaration), not findings.
- No numbers, mechanisms, tables, or verbatim quotes about the refactoring experiment are recoverable from it.
- Per the source plan, this chunk belongs to the garbled extraction batch (chunks 03–20) flagged for triage/merge rather than standalone claims.
- No content is invented here; any real findings for this topic must come from the paper itself, not this chunk.

## 19. [[wiki/19-array-assert-statement-fragments|Array / Assert Statement Fragments (Chunk 19/20)]]
**In one sentence:** This chunk contains no readable prose — only garbled pdftotext/AST-diff fragments (SingleStatement, AssertStatement, ArrayType, ExpressionNode tokens) — so no substantive claim can be summarized from it.
## Key points
- The chunk body carries no complete sentences or argumentative claims to summarize.
- Its legible tokens are AST-diff artifacts (e.g. SingleStatement, AssertStatement, ArrayType, ExpressionNode, RecordDeclaration, IntegralType), not findings.
- No numbers, mechanisms, tables, or verbatim quotes about the refactoring experiment are recoverable from it.
- Per the source plan, this chunk belongs to the garbled extraction batch (chunks 03–20) flagged for triage/merge rather than standalone claims.
- No content is invented here; any real findings for this topic must come from the paper itself, not this chunk.

## 20. [[wiki/20-declaration-string-fragments|Threats to Validity and Conclusion (Chunk 20/20)]]
**In one sentence:** The authors qualify their large-scale iterative-refactoring results with internal, external, conclusion, and construct validity threats, then conclude that GPT-5.1 refactoring over five iterations converges toward implicit conventions with prompt-dependent dynamics.
## Key points
- Internal validity: the development-time line-pair dataset could not cover all diff cases, so some lines were mismatched or unmatched, adding noise that does not change big-picture convergence trends.
- Rename handling was not normalized: each occurrence of a repeated variable counted as a separate renaming, which is informative for impact but risks misleading counts and dysfunctional code if renaming is inconsistent — left as open exploration.
- External validity: the main experiment used a single model (GPT-5.1) and not GPT-5.2 (available only after data collection); anecdotal runs with gpt4.1-mini (master's thesis [22]) and gpt5.1-mini showed the same trends, with larger models more "opinionated" (e.g., more renamings across all five iterations).
- Conclusion validity: averaging over many snippets can hide micro-level back-and-forth changes; the similarity score covers only changed segments between successive versions, but insertions/deletions become negligible in later stages so it remains a representative proxy.
- Conclusion validity (replication): temperature was set to 0 per best practice, which reduces but does not eliminate LLM non-determinism; repeated runs could differ slightly.
- Construct validity: readability itself was never directly measured — only anecdotal/sample-based qualitative checks (uniform formatting, context-appropriate renames); whether one snippet is more readable remains inherently subjective.
- Main conclusion: with 230 Java snippets × variants × 5 iterations × 3 prompting strategies, best-practice code was preserved with minor stabilizing edits while convention-violating variants converged to highly similar finals (normalization effect); naming-focused prompts oscillated, comment-focused prompts stabilized faster; follow-ups confirmed semantics preservation and generalization to novel code.

## The argument in five moves
1. A large-scale setup (230 Java snippets x 3 variants x 3 prompts x 5 GPT-5.1 iterations = 10,350 snippets) asks what happens when an LLM repeatedly refactors its own output: convergence, oscillation, or regression.
2. On already-good code, iteration shows restructuring then stabilization: unchanged lines climb 45% to 92% while early renames, insertions, and comment pruning fade to marginal micro-changes that never fully reach zero.
3. Degraded variants (meaningless names, stripped comments) follow the same trajectory after heavier first-pass repairs, converging with the original on code lines, method counts, and cross-variant similarity near 0.87.
4. Targeted prompts steer the change mix but not the overall convergence: naming-focused prompts keep rename rates high and can oscillate, while comment-focused prompts front-load comment edits then stabilize quickly.
5. The authors conclude LLMs normalize diverse inputs toward an implicit readable style yet need guardrails — explicit stopping criteria, careful prompt phrasing, comment preservation — qualified by single-model, aggregation, non-determinism, and unmeasured-readability validity threats.
