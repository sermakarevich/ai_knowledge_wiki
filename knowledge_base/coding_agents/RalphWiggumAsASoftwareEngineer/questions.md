---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Ralph Wiggum as a "software engineer"

### Q1. Why will copying the CURSED prompt verbatim not reproduce its outcomes?

> [!tip]- Answer
> There is no perfect copy-pasteable prompt; the CURSED prompt only works because it was continually tuned by watching Ralph's stream for patterns of bad behaviour and adjusting at each opportunity. The operator's job is therefore ongoing observation and tuning, not one-shot prompt engineering. See [[wiki/01-prompt-md-contents|What's in the prompt.md? Can I have it?]].

### Q2. What does "monolithic, one item per loop" mean, and what stack is allocated to context every loop?

> [!tip]- Answer
> Ralph runs as a single process in one repository doing one task per loop, with Ralph itself choosing the most important thing; the restriction is relaxed only later and re-tightened if it goes off the rails. Every loop deterministically loads the same stack — the plan (@fix_plan.md) plus the specifications (@specs/stdlib/*, written one file per spec after a long requirements conversation) — inside a ~170k usable context budget. See [[wiki/01-prompt-md-contents|What's in the prompt.md? Can I have it?]].

### Q3. How does the primary context act as a scheduler, and what is the "don't assume" sign fixing?

> [!tip]- Answer
> The primary context avoids expensive allocations itself and fans out to subagents (e.g. to summarise test results), with many subagents allowed for search and writing but only 1 subagent for Rust build/tests, since hundreds of parallel builders cause bad back pressure. Because ripgrep search is non-deterministic, Ralph wrongly concludes code is missing and duplicates implementations — its Achilles' heel — so an explicit "before making changes search codebase (don't assume not implemented) using subagents" sign is erected. See [[wiki/01-prompt-md-contents|What's in the prompt.md? Can I have it?]].

### Q4. Generation is cheap, so where do you steer quality upstream and how do you enforce correctness downstream?

> [!tip]- Answer
> Wrong patterns mean fixing the technical standard library, while building the wrong thing entirely means fixing the specifications (as when a CURSED lexer spec defined one keyword twice for two opposing scenarios, unnoticed for a month). Correctness comes from a fast back-pressure wheel — type systems, tests/builds, scanners or static analysers — with a per-change rule to run the tests for the unit improved, plus a mandatory static analyser/type checker (Dialyzer, Pyrefly) for dynamically typed languages. See [[wiki/02-phase-one-generate|Phase one: generate]].

### Q5. How are placeholder implementations, the TODO list, and loop-back self-improvement handled?

> [!tip]- Answer
> Claude's bias toward minimal/placeholder implementations is countered with an explicit "DO NOT IMPLEMENT PLACEHOLDER OR SIMPLE IMPLEMENTATIONS" sign plus a duty to implement missing spec functionality and fix even unrelated failing tests, with leftovers harvested by more Ralph loops into a priority-sorted @fix_plan.md built by up to 500 subagents comparing src/ and examples/ against specs/*. Ralph loops back on himself via extra logging or compiling and inspecting LLVM IR output, and self-improves @AGENT.md (how to compile/run) and @fix_plan.md (noticed bugs, even unrelated), while every test and doc must record why it matters so fresh-context future loops can judge relevance. See [[wiki/02-phase-one-generate|Phase one: generate]].

### Q6. What happens when you wake up to a broken codebase, and what commit/tag discipline applies?

> [!tip]- Answer
> Some mornings the codebase will not compile and Ralph cannot fix it himself, so the operator judges between git reset --hard plus restart versus crafting rescue prompts (one past error-volume overflow was handled by throwing the error file into Gemini to make a plan for Ralph). The discipline is: when tests pass update @fix_plan.md, git add -A, git commit with a descriptive message, git push — and when no build/test errors remain, create a git tag starting at 0.0.0 and incrementing patch. See [[wiki/03-broken-codebase-overnight|You will wake up to a broken code base]].

### Q7. A team wants to point Ralph at their large existing codebase with junior-only oversight and treat its output as final. What should you recommend?

> [!tip]- Answer
> Recommend against it: Ralph is Greenfield-only ("no way in heck" for existing codebases), expects only ~90% completion via bootstrapping, and still requires senior expertise guiding it — claims of 100% engineer-free delivery are "peddling horseshit". Accept that AI-created problems are solvable with different prompts plus more loops and post-AI adapt loops rather than human-frame maintainability, and staff and scope the project accordingly. See [[wiki/03-broken-codebase-overnight|You will wake up to a broken code base]].
