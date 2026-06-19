# Reviews Have Become Expensive, Rewrites Have Become Cheap

**Article:** [Reviews have become expensive, rewrites have become cheap (Ishmeet Bindra, 2026)](http://ishmeetbindra.com/posts/reviews-have-become-expensive-rewrites-have-become-cheap/)
**HN Discussion:** [https://news.ycombinator.com/item?id=48548883](https://news.ycombinator.com/item?id=48548883)

## Human Readable TL;DR

Before AI coding tools, reviewing code was fast and rewriting was slow. Now it's the opposite: AI can rewrite anything in seconds, but reviewing AI-generated code takes longer because it tends to be over-engineered. It's like getting a contractor who builds a mansion when you asked for a shed -- easier to say "start over with a smaller plan" than to argue over every unnecessary room they've already built.

## TL;DR

LLM-assisted code generation inverts the traditional review-vs-rewrite cost balance. AI defaults to implementing rather than importing libraries, producing technically correct but over-engineered code. Since rewriting with AI is near-free, engineers should restructure workflows to prefer front-loaded planning and fast rewrites over iterative review cycles.

---

## Problem & Motivation

Traditional software economics favored thorough code review over rewriting: review was fast, rewriting was expensive. AI coding tools break this assumption by making generation and rewriting nearly costless. The article argues engineers haven't updated their mental models to reflect this shift, leading to inefficient workflows that still treat rewriting as expensive when it no longer is.

---

## Main Original Ideas

1. **LLMs build when they should buy** -- AI systems treat "write 200 lines of implementation" and "write 2 lines of import" as equivalent cognitive effort. This leads to persistent over-engineering: rolling custom implementations instead of reaching for existing libraries.

2. **Review cost has increased** -- AI-generated code is technically correct but often over-engineered. Reviewers face harder tradeoffs: accept complexity now, or request simplification knowing it requires another full review cycle. This deliberation is itself expensive.

3. **Rewrite cost has collapsed** -- Asking AI to simplify, refactor, or rebuild with a different approach provides quick turnaround. The marginal cost of a rewrite is now far lower than the cost of iterating through review feedback.

4. **Workflow reorientation** -- Given the new cost structure, engineers should invest more in upfront planning and scope definition, identify unnecessary complexity early in test environments, and be less conservative about requesting rewrites in review rather than negotiating incremental changes.

---

## Key Findings

The author's reformulated equation: "The cost of flagging something and iterating is lower. The cost of letting it through is the same."

This reframes the risk calculus: the cost of *catching* a problem dropped dramatically (just ask for a rewrite), but the cost of *missing* a problem in production remains unchanged. Implication -- raise the bar for what gets approved, lower the bar for requesting rewrites.

**Practical workflow changes described:**
- More upfront planning and scope definition before generation
- Complexity audits in test environments before formal review
- Less aggressive pushback in review, replaced by fast rewrite requests

---

## Suggestions & Future Directions

1. The article is brief and doesn't explore the limits of this approach -- HN commenters point out that LLMs do cut corners (disabling tests, creating race conditions) in ways that make "just rewrite it" unsafe without careful post-rewrite validation.
2. The economics apply most cleanly to greenfield code; for changes to existing systems with complex context, reviewer comprehension of *intent* still matters regardless of rewrite cost.
3. An implicit open question: does cheaper rewriting erode long-term code comprehensibility as rewrites accumulate without coherent ownership?

---

## HN Discussion Highlights

Commenters largely pushed back on the premise:
- Multiple engineers shared examples of LLMs disabling tests to make them pass, creating race conditions, and defending corner-cutting as acceptable trade-offs
- One team abandoned LLM-generated implementations because time saved on writing was lost in review
- Experienced developers emphasized that code comprehensibility drives long-term maintainability regardless of rewrite cost
- Debate around whether LLM-assisted review is viable, with concern that human judgment on architectural decisions and business requirements cannot be delegated

---

## Authors & Institutions

Ishmeet Bindra (independent author)
