> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Similarity Across Iterations
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
---
## Similarity score evolution across variants (Fig. 15, PromptGeneral)
**Covers:** Fig. 13/14 garbled heatmap headers; Fig. 15 caption and body text, v0–v5 trajectories
> "Similarity Score Evolution Across Variants. To complement the pairwise similarity heatmaps, Figure 15 illustrates how the similarity score between each variant pair evolves over the five refactoring iterations."

| Variant pair | v0 score | Later trajectory |
|---|---|---|
| Original – NoComment | 0.98 | decreases significantly to around 0.87 |
| Original – Meaningless | 0.85 | converges to ≈0.87 |
| Meaningless – NoComment | 0.85 | very slight upward trend 0.85→0.87 |

> "Ultimately, all three curves converge within a narrow range of less than 3% difference, indicating that despite their divergent starting points, the iterative refactorings lead all variants to similar structural representations of the code, albeit still with some differences."
> "Notably, the similarity between Original and NoComment decreases significantly from 0.98 to around 0.87, reflecting the increasing structural changes introduced by the LLM that go beyond simple formatting or syntax-only edits."
> "In general, this provides further support for the convergence hypothesis formulated in RQ2: Independently of initial modifications, LLMs tend to normalize and align the structure of code snippets over repeated prompts."

## RQ2 convergence summary box
**Covers:** RQ2 boxed summary, p. 21
> "Our results show a general convergence across all three code variants. Despite structural differences in their initial versions (particularly between Meaningless and NoComment), the iterative refactoring rapidly reduces these differences. Structural metrics (e.g., code, comment, and empty lines) largely stabilize after the second iteration, and line-level analyses reveal that the majority of changes occur early, followed by minimal adjustments in later iterations. Pairwise similarity scores confirm this trajectory: both within-variant comparisons (v0–v5) and cross-variant comparisons converge toward higher similarity values, typically around 0.87–0.90 by the final iteration. Notably, NoComment reaches convergence slightly faster than Meaningless, but in the end all variants align to similar structural representations."

## RQ3 setup and absolute metrics (Figs. 16–17)
**Covers:** §4.3–4.3.1, PromptMeaning vs PromptComments design
> "To address RQ3, we conducted a comparative analysis of three prompt strategies designed to highlight distinct refactoring objectives. Specifically, in addition to our general prompt, we now ran the entire pipeline on all three variants again, but with PromptMeaning explicitly directing LLMs toward meaningful identifiers, while PromptComments emphasizes the improvement of comments."

- PromptMeaning: total lines, methods, code lines "remain relatively stable"; contrasts PromptGeneral where "structural changes (e.g., increases in method count and code lines) are more pronounced, particularly in the first two refactoring iterations"; "empty lines are not added as much"; NoComment shows "essentially no change in the number of methods and comment lines."
- PromptComments: "the number of code lines and methods changes more similar to the general improvement prompt"; "the number of line and inline comments is generally higher than for the PromptMeaning. However, the number of inline comments remain at a very low level"; LLM inserts comments "primarily during the first iteration" with "no further increases ... in later versions," i.e. no artificial documentation inflation.

## Change-type distributions (Figs. 18–20)
**Covers:** §4.3.2, Original / Meaningless / NoComment under PromptMeaning vs PromptComments
- Original + PromptMeaning: "rename operations dominate across all iterations and continue to a larger extent (≈20%) even in later iterations"; besides renaming after v0→v1, other changes only marginal. Original + PromptComments: bulk in first transition (comment changes, insertions, deletions), then "increasingly smaller changes."
- Meaningless + PromptMeaning: renames dominate from the first iteration and persist ("decreases only slowly"); unlike PromptGeneral, "do not converge rapidly." Meaningless + PromptComments: first transition still heavily renames plus "around 36% of all changes" as comment changes; "changing comments remains the top change type until v5."
- NoComment + PromptMeaning: renames dominate all iterations from a large v0→v1 share, persisting while unchanged-line share rises slightly. NoComment + PromptComments: first iteration heavy on comment changes/insertions/deletions, then "rapidly diminishes ... approaching near-stability and almost no further changes by the final iteration."

## Pairwise similarity under targeted prompts (Figs. 21–22)
**Covers:** §4.3.3, heatmaps and convergence curves
- PromptMeaning heatmaps: "clear convergence with each iteration" for Original, "to a large degree" for Meaningless "despite many changes"; NoComment "more chaotic, possibly due to the many alternating rename operations."
- PromptComments heatmaps: "more back-and-forth changes, especially for the manipulated two variants. Starting from v1, alternating similarity scores become apparent, in which pairs of versions separated by two iterations share are very similar score, whereas the direct successor in between shows a lower score."
- Fig. 22: "for both prompt strategies the similarity scores across the three variant pairs converge rapidly, with the most substantial change occurring during the transition from v0 to v1. Overall, PromptMeaning achieves a higher average similarity score across the variant pairs compared to PromptComments."

## Statistical descriptives (Table 4)
**Covers:** §4.3.4 descriptives; Kruskal-Wallis setup
| Code variant | Prompt | Rename | CommentChange |
|---|---|---|---|
| Original | PromptGeneral | 4.9% ± 6.9% | 1.2% ± 2.7% |
| Original | PromptMeaning | 20.5% ± 9.3% | 1.9% ± 3.0% |
| Original | PromptComments | 3.1% ± 5.4% | 3.4% ± 3.7% |
| Meaningless | PromptGeneral | 8.3% ± 10.3% | 0.3% ± 1.3% |
| Meaningless | PromptMeaning | 25.6% ± 10.4% | 0.5% ± 1.6% |
| Meaningless | PromptComments | 6.4% ± 9.5% | 2.8% ± 3.3% |
| NoComment | PromptGeneral | 7.9% ± 9.8% | 0.1% ± 0.5% |
| NoComment | PromptMeaning | 30.5% ± 11.0% | 0.0% ± 0.5% |
| NoComment | PromptComments | 4.1% ± 7.2% | 2.5% ± 3.6% |

> "We applied the Kruskal-Wallis H test [29] as a non-parametric alternative to one-way ANOVA. This test is particularly suited for our data, as the distributions of code change metrics are proportional (i.e., normalized between 0 and 1) and therefore not guaranteed to follow a normal distribution."
