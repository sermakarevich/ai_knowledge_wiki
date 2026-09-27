> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Threats to Validity and Conclusion (Chunk 20/20)

**In one sentence:** The authors qualify their large-scale iterative-refactoring results with internal, external, conclusion, and construct validity threats, then conclude that GPT-5.1 refactoring over five iterations converges toward implicit conventions with prompt-dependent dynamics.

## Key points
- Internal validity: the development-time line-pair dataset could not cover all diff cases, so some lines were mismatched or unmatched, adding noise that does not change big-picture convergence trends.
- Rename handling was not normalized: each occurrence of a repeated variable counted as a separate renaming, which is informative for impact but risks misleading counts and dysfunctional code if renaming is inconsistent — left as open exploration.
- External validity: the main experiment used a single model (GPT-5.1) and not GPT-5.2 (available only after data collection); anecdotal runs with gpt4.1-mini (master's thesis [22]) and gpt5.1-mini showed the same trends, with larger models more "opinionated" (e.g., more renamings across all five iterations).
- Conclusion validity: averaging over many snippets can hide micro-level back-and-forth changes; the similarity score covers only changed segments between successive versions, but insertions/deletions become negligible in later stages so it remains a representative proxy.
- Conclusion validity (replication): temperature was set to 0 per best practice, which reduces but does not eliminate LLM non-determinism; repeated runs could differ slightly.
- Construct validity: readability itself was never directly measured — only anecdotal/sample-based qualitative checks (uniform formatting, context-appropriate renames); whether one snippet is more readable remains inherently subjective.
- Main conclusion: with 230 Java snippets × variants × 5 iterations × 3 prompting strategies, best-practice code was preserved with minor stabilizing edits while convention-violating variants converged to highly similar finals (normalization effect); naming-focused prompts oscillated, comment-focused prompts stabilized faster; follow-ups confirmed semantics preservation and generalization to novel code.

---

## Fig. 27 context

**Covers:** Fig. 27 caption + pp. 37–41 (Sections 6.4–7, Acknowledgments, References [1]–[65])

> "Fig. 27. Sunburst diagram showing the distribution of AST node types affected by code changes, grouped by prompt (center), change type (middle layer), and node category (outer layer)"

No numeric distribution values are present in the chunk body beyond this caption.

## 6.4.1 Internal validity (inferred from body; heading truncated in chunk)

- Line-pair matching: dataset built during iterative development "naturally could not cover all possible cases of code line pairs that may occur in a diff"; errors "may have introduced noise into the analysis, potentially affecting the specific precision of our measurements", but "across many snippets potential line mismatches in a few snippets do not affect the overall results."
- Rename classification: "Rename operations were not normalized in our analysis. This means that if a variable occurred multiple times in the code, each instance was counted as a separate renaming operation."
- Rationale given: "renaming a variable with many occurrences can have greater practical impact than changing a variable used only once."
- Open risk: "whether the model consistently renames all instances of a given variable. Inconsistent renaming would not only produce misleading counts but could also render the code dysfunctional or subtly alter its behavior."

## 6.4.2 External Validity

- "The generalizability of our findings is limited by the fact that we relied on a single model throughout the main experiment."
- "we did not employ the most recent version at the time of writing (gpt5.2), as it became available only after the data collection had been completed."
- Cross-model anecdote: "An early version of this work was a master's thesis using gpt4.1-mini, which showed the same trends [22]"; setup testing used "gpt5.1-mini"; impression: "the larger models are more 'opinionated', such that the absolute change numbers are a bit larger (e.g., more renamings across all five iterations), but across all three models, the main results were the same."
- Pipeline claim: "not bound to any specific model. If an API is available, only minimal adjustments to the request format and conversion of the response are required."

## 6.4.3 Conclusion Validity

- Aggregation: "By averaging results across a large number of snippets and variants, important details may be obscured. For example, back-and-forth changes can occur in individual refactoring sequences, yet their impact may be diluted in the aggregate analysis."
- Similarity measure: "does not account for the change types of insertions and deletions, and therefore does not theoretically capture the overall similarity between entire snippets. Instead, it reflects only the similarity of the changed code segments between two successive versions."
- Mitigation cited: "the proportion of insertions and deletions decreases sharply with higher version numbers and is negligible in later stages."
- Classification gap: "Insertions and deletions were also not explicitly represented as distinct change types"; future work could capture "code growth or reduction explicitly, for example, by reflecting the expansion or contraction of comment sections."
- Non-determinism: "setting the generation parameter of temperature to 0, which is commonly used to minimize randomness. While this increases reproducibility to some extent, it does not fully eliminate the possibility that repeated runs could yield slightly different results."

## 6.4.4 Construct Validity

- "we did not directly measure whether the resulting code was indeed more readable" — impressions "remain anecdotal rather than systematically validated"; what makes code "readable" is "still ongoing research [42]."
- Static-analysis alternative not taken: tools "might have been employed to first evaluate the 'best practice' snippets", but rejected over tool accuracy and "whether they actually improve human readability at all."
- Qualitative observations claimed: "the LLM consistently produced more uniform and well-formatted code outputs and, in cases of variable renaming, was able to correctly infer and assign meaningful names based on context."
- Method note: "given the size of the dataset, we relied on sample-based qualitative checks rather than systematic validation."

## 7 Conclusion

- Setup (exact numbers from chunk): "large-scale main experiment using OpenAI's GPT5.1 with 230 Java snippets, each systematically varied and refactored with respect to readability across five iterations under three different prompting strategies."
- Findings as stated:
  - Best-practice code: "typically preserved structure but introduced minor, sometimes unnecessary, code changes before stabilizing."
  - Convention-violating variants: "still converged toward highly similar final versions, suggesting a normalization effect in which LLMs align diverse inputs with implicit coding conventions."
  - Prompts: "Emphasizing variable naming frequently led to oscillatory changes, whereas prompts stressing comments supported faster stabilization."
  - Follow-ups: "unaffected by the potential of breaking semantic functionality" and "hold even for novel code."
- Future work quoted: "Exploring larger and more diverse code bases or systematically varying prompt strategies and contextual anchoring."

## Acknowledgments and References

- Support: "ERC Advanced Grant 'Brains On Code – A Neuroscientific Foundation of Program Comprehension' 101052182."
- References [1]–[65] listed on pp. 39–41 (Abdelsalam et al. 2026 through Zheng et al.), no additional factual claims extracted.

**Covers:** Fig. 27 caption; Sections 6.4.1–6.4.4, 7, Acknowledgments, References (chunk pp. 37–41). Note: chunk title/slug ("TypeIdentifier Double → → Declaration StringFragment") is a pdftotext/AST-diff artifact and does not describe the body content.
