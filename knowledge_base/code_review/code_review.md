# Code Review

Research and product analyses on **code review** — both classical software-engineering studies of human Modern Code Review (MCR) and the new wave of LLM-powered PR review systems. Central themes: most review value is evolvability/maintainability not bug-finding; the bottleneck is understanding code and intent; whole-repo context and per-team learning loops are what distinguish frontier AI reviewers from diff-only linters.

## Papers

- [[AutomaticClassificationReviewCommentsPull/summary]] — 4×11 taxonomy for GitHub PR review comments (Correctness/Decision/Management/Interaction); two-stage hybrid SVM classifier with rule + structural-metadata features beats text-only baseline by 5–9% F1.
- [[CodeReviewsDoNotFindBugs/summary]] — Microsoft CODEMINE study: only ~15% of review comments flag defects, ≥50% address maintainability; reviewer familiarity raises usefulness 33%→67%; "everyone reviews everything" wastes effort.
- [[DefectsDiscoveredInCodeReviews/summary]] — 759 defects from 9 industrial + 23 student reviews show ~75% are evolvability defects (readability, structure), not functional bugs; reviews complement rather than duplicate testing.
- [[ExpectationsOutcomesChallengesModernCodeReview/summary]] — Microsoft mixed-methods study: defect comments are only 14% of output despite being the top-stated motivation; the dominant reviewer challenge is understanding code and intent, not finding bugs.
- [[Greptile/summary]] — Commercial PR review bot built on a whole-repo code graph instead of diff-only context; per-team thumbs-up/down feedback loop shapes which findings surface; 18 cross-file and spec-mismatch examples evidence graph value.
- [[ImpactCodeReviewCoverageQuality/summary]] — Mining 1k+ Qt/VTK/ITK Gerrit reviews, post-release defects correlate more with participation depth and reviewer expertise than with raw coverage; binary "reviewed yes/no" misses what matters.
- [[InformationNeedsContemporaryCodeReview/summary]] — Seven-category taxonomy of reviewers' information needs from 900 OSS Gerrit threads; the dominant need is "alternative solution suitability" not bug-checking; median answer in <7 hours.
- [[ModernCodeReviewGoogleCaseStudy/summary]] — Google Critique study (~9M reviews, 2 years): primary motivations are education, gatekeeping, and norm enforcement, not defect finding; median 24-line CL, <4hr latency, ownership + readability dual-gate.
- [[ModernCodeReviewsOpenSourceProblems/summary]] — 1,469 ConQAT/GROMACS changes show 75–81% are evolvability fixes (replicating Mantyla 2009 in lightweight tooling); 10–22% of fixes are author-initiated with no review comment; reviewer identity has no effect.
- [[ReviewsExpensiveRewritesCheap/summary]] — AI inverts review/rewrite economics: AI code is harder to review (over-engineered) but near-free to rewrite; front-load planning and request rewrites over iterative comment cycles.
- [[ai-pr-review-approaches]] — Research synthesis on state-of-the-art AI PR review: multi-agent + verification (`/ultrareview`), nitpick-problem dominance, behavioral embedding filters (Greptile pattern), and per-repo memory as the frontier.
- [[code-review-graph-analysis]] — MCP server persisting a SQLite code knowledge graph (tree-sitter parse, 28 tools) so AI coding agents fetch targeted review context instead of re-reading files.
