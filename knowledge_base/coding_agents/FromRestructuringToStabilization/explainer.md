> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# From Restructuring to Stabilization: A Large-Scale Experiment on Iterative Code Readability Refactoring with Large Langu — In Plain Language

## What is this about?

This paper asks a simple question: what happens if you ask an AI to tidy up the same piece of code, over and over again?

The researchers took 230 Java programs from a teaching collection called TheAlgorithms-Java. For each one they made three starting versions: the original clean code, a version with meaningless names, and a version with all comments stripped out.

Then they asked GPT-5.1 (temperature 0, fresh request each time) to "refactor for readability" — five rounds in a row, feeding each round's output back in. They repeated this with three different instructions: a general one, one focused on names, and one focused on comments. In total: 230 files x 3 variants x 3 prompts x 5 rounds = 10,350 code snippets.

They then measured what changed each round: how many lines stayed the same, what kind of edits happened (renames, code changes, comment edits), and how similar versions were to each other.

The headline pattern: big tidy-up first, then calm down. On clean code with the general prompt, unchanged lines rose from 45% (round 1) to 76%, 86%, 89%, and finally 92% (round 5). Early edits were renames (9%) and code insertions (11%); later, no single edit type exceeded 1%.

## Why does it matter?

Most earlier work tested one-shot refactoring: ask once, check the result. Nobody had checked what repeated AI refactoring does at scale.

That matters because teams are tempted to put AI refactoring in a loop — auto-tidy on every save, bots that re-polish pull requests, agents that iterate until code "looks good." Without knowing the dynamics, you cannot tell whether looping helps, wastes effort, or quietly breaks things.

Three practical stakes from the paper:

- Over-refactoring is real. Even good code grew from about 58 to over 73 code lines, gained extra blank lines and methods, and lost inline comments almost entirely. The AI does not stop on its own.
- Recovery is possible. Badly named or uncommented code was largely repaired in the first one or two rounds and then followed the same path as clean code, ending at 89–90% unchanged lines.
- Instructions steer but do not rewrite the story. Naming-focused prompts kept rename rates high (around 20–30% even late) and could flip names back and forth; comment-focused prompts front-loaded comment edits and then settled faster. Overall convergence looked similar either way.

Breaking functionality was rare but not zero in any given round, so blind looping is risky.

## How does it work?

Think of it like asking an enthusiastic editor to revise the same essay five times.

Round 1 is the heavy edit. On clean code, the model renames variables, splits code into more methods (average 3.1 rising toward 6), adds spacing, and prunes comments. On the meaningless-names variant, only 31% of lines survived round 1 (24% were renames). On the no-comments variant, 44% survived (14% renames).

Rounds 2–3 are the calming phase. Change volumes shrink fast. Structural counts — code lines, empty lines, method counts — mostly level off after round 2, stabilizing from round 3 onward.

Rounds 4–5 are micro-tweaks. Similarity between consecutive versions climbs from 0.86 to 0.90, and distant versions (round 2 vs. round 5) score 0.88 — the drafts are clearly related. But no pair ever reaches 1.00: the model keeps fiddling with tiny details instead of declaring itself done.

A second lens: compare the three starting variants against each other. The clean and no-comment versions start nearly identical (0.98 similarity, differing only by comments) while renamed versions start at 0.85. After five rounds all pairs land near 0.87, within a 3% band. Different starting points, same neighborhood — the authors call this normalization toward an internal idea of "readable code."

The team also checked back-and-forth behavior (does round 3 undo round 2?), split edits into types with a custom DiffParser tool, and ran follow-ups on meaning preservation and fresh code. Validity caveats are stated openly: one main model, averages can hide individual flip-flops, and readability itself was judged by samples, not measured directly.

Two details worth knowing. First, comment handling is asymmetric: the general prompt slowly trims comments and wipes out inline comments, while the comment-focused prompt adds documentation in round 1 and then holds steady rather than inflating forever. Second, structure drifts upward even on good code — more methods, more code lines, more blank lines — so "more readable" here partly means "more spread out," which is a style choice teams may or may not want.

## Where can this be used?

- AI code-review bots: run one or two passes, then stop. The paper suggests most of the value arrives early; later passes add churn.
- Legacy cleanup: feeding messy, badly named, or uncommented code through a general readability prompt can normalize it toward a consistent style before humans review.
- Prompt design: use a naming-focused instruction only when names are the actual problem (it keeps renaming late into the loop); use a comment-focused instruction when documentation is the gap (it adds comments in round 1 without endless inflation).
- Guardrail design: add explicit stopping rules (e.g., stop when fewer than X% of lines change), preserve valuable explanatory comments before looping, and re-run tests each round since breakage is rare but possible.
- Research tooling: the authors release a model-agnostic pipeline (sequence, token, and syntax-tree similarity plus a line-level diff classifier) so others can repeat the experiment on different models or languages.
- Teaching example: the "restructure then stabilize" curve is a vivid demo of why to bound AI loops — show round-1 vs. round-5 diffs to make the point concrete.
- Style baselines: teams adopting an AI formatter can use the converged outputs as a draft house style, then lock the rules in a linter instead of re-asking the model.

What it is not: a proof that the final code is objectively more readable to humans, or that the same numbers hold for other models, languages, or huge codebases. Those are listed as open follow-ups.

## Conclusions & takeaways

- Big edit, then settle: repeated AI refactoring restructures first and stabilizes after, but never fully stops fidgeting.
- Messy inputs catch up: degraded variants converge with clean code on line counts, method counts, and similarity near 0.87.
- Prompts nudge, they do not redirect: naming prompts prolong renaming (sometimes oscillating); comment prompts act early then calm down.
- Loop with guardrails: cap the number of passes, watch comments, and verify behavior — do not let the loop run open-ended.
- Treat averages with care: aggregate convergence can mask individual snippets that flip-flop, and one model plus sampled quality checks means human review is still required.
- Bottom line for non-specialists: let the AI do the first heavy tidy-up, then take over yourself — the machine is a good first editor, not a finisher.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Iterative refactoring | Asking the AI to tidy the same code several times in a row, feeding each result back in. |
| Readability | How easy code is for a person to read and understand (names, layout, comments, simplicity). |
| Variant (Original / Meaningless / NoComment) | The three starting versions: clean code, code with scrambled names, code with comments removed. |
| Prompt strategy | The instruction given to the AI: general tidy-up vs. "focus on names" vs. "focus on comments." |
| Unchanged-line share | The percentage of lines the AI left alone in a round; higher means calmer editing. |
| Changed-line similarity | A 0-to-1 score for how alike the edited lines are between two versions; 1.00 means identical. |
| Rename operation | Changing a variable, method, or class name without changing what the code does. |
| Convergence / normalization | Different starting versions becoming structurally similar after repeated refactoring. |
| Oscillation (back-and-forth) | The AI changing something in one round and partly undoing it in the next. |
| Temperature 0 | A model setting that makes output as deterministic as possible (less randomness). |
