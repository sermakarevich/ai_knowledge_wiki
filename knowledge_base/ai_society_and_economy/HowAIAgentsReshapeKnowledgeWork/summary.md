# How AI Agents Reshape Knowledge Work: Autonomy, Efficiency, and Scope

**Paper:** [How AI Agents Reshape Knowledge Work: Autonomy, Efficiency, and Scope (Yang, Zyskowski, Yonack, Ma, 2026)](https://arxiv.org/abs/2606.07489)

## Human Readable TL;DR

Imagine the difference between asking a librarian to hand you a book versus hiring an assistant who goes off, reads the books, writes a report, builds a spreadsheet, and emails the results -- all while you wait. This paper studies exactly that shift using real usage data from an AI search tool (librarian-style) versus an AI agent (autonomous assistant). The agent does 48 times more work per session, cuts task completion time by 87%, and -- most strikingly -- leads people to tackle work they never would have touched before, like a finance professional suddenly building software dashboards or a marketer running statistical analyses.

## TL;DR

Using production data from Perplexity's Search (conversational assistant) and Computer (autonomous agent) products across 90 days in 2026, this paper provides the first field evidence on how the shift to agentic AI reshapes knowledge work at the task level. Agents reduce task completion time by 87% and cost by 94% on matched tasks, and expand the scope of work users attempt -- horizontally (crossing occupational boundaries) and vertically (higher cognitive complexity, broader domain expertise, more composite tasks). A task-based economic framework with higher fixed delegation cost but lower marginal execution cost explains these patterns theoretically.

---

## Problem & Motivation

Prior productivity studies of AI (GitHub Copilot, ChatGPT, GPT-4) focused on human-AI collaboration where AI augments individual steps interactively. These miss the new paradigm where AI agents asynchronously execute entire multi-step workflows with minimal human intervention. The binding constraint on knowledge work is not information access -- it's execution capacity. The paper asks: when you delegate execution entirely to an agent, how does it change what work gets done, how fast, and at what cost?

---

## Main Original Ideas

1. **Task-based economic framework for agents** -- Models tasks by step count, with agents having higher fixed delegation cost but lower marginal cost per step. This derives a crossover threshold s* above which agents are strictly preferred, and proves that agent access expands the affordable task frontier, weakly increases total value, and improves the value-to-cost ratio when the pre-agent budget binds.

2. **Matched-session natural experiment design** -- Identifies 10,000 session pairs where the same dual-product user issued near-identical initial queries (cosine similarity > 0.99) on both Search and Computer. This controls for user and task heterogeneity, enabling clean comparison of autonomy, efficiency, and quality effects.

3. **Horizontal scope expansion** -- Documents that Computer queries venture outside users' primary occupational domain 9 pp more often than Search queries from the same users (59% vs. 50% cross-occupational). Agents lower barriers to entry for work requiring specialties the user doesn't hold.

4. **Vertical scope expansion via O*NET taxonomy** -- Classifies queries against Bloom's cognitive taxonomy, Autor et al.'s abstract/routine task types, O*NET Knowledge domains, and four levels of O*NET Work Activities to show that Computer queries require deeper cognition, broader expertise, and more composite work bundles.

5. **New task unlocking** -- 23% of Computer queries involve at least one O*NET Task Statement that never appears in the same users' Search queries, concentrated in fine-grained executional work (software development, documentation production, data visualization).

---

## Key Findings

### Efficiency Gains (Matched 10,000 Session Pairs)

| Metric | Search + Human | Computer + Human | Reduction |
|--------|---------------|-----------------|-----------|
| Avg. task completion time | 269 min | 36 min | **87%** |
| Estimated cost per task | baseline | -- | **94%** |
| Marginal cost per step | $2.05 | $0.16 | **92%** |
| Minutes per step | 2.66 min | 0.46 min | **83%** |
| Per-query dissatisfaction (mid+high) | 2.9% | 1.3% | **55% lower** |

### Autonomy
- Computer performs **26 minutes** of autonomous work per session vs. **33 seconds** for Search (48x gap)
- Median runtime: 9 min (Computer) vs. 14 sec (Search) -- 40x gap
- Computer sessions request user input more (13% vs. 0.3%), but user-initiated stops are similar (3.7% vs. 3.4%)

### Scope Expansion (Vertical)

| Dimension | Search | Computer | Gap |
|-----------|--------|----------|-----|
| Higher-order Bloom cognition (Analyze/Evaluate/Create) | 55% | 76% | +21 pp |
| Create-level tasks | 26% | 50% | +24 pp |
| Abstract (non-routine) tasks | 53% | 71% | +18 pp |
| Avg. O*NET Knowledge domains required | 1.74 | 2.40 | +38% |
| Queries requiring 3+ domains | 17% | 51% | 3x |
| Generalized Work Activities per query | 2.24 | 2.95 | +32% |
| Task Statements per query | 2.38 | 3.81 | +60% |

- Computer queries grow to **84x** their first-week total over the 3-month window
- Top use cases: Research & Analysis (25.8%), Document & Asset Creation (18.6%)
- Computer adoption associated with +1.05 daily Search queries (complementarity, not substitution)

---

## Suggestions & Future Directions

1. **Aggregate to organizational level** -- Study how individual-level task recomposition translates to firm-level employment, team structures, and role definitions using firm production and employment data.

2. **Broader and later adopter populations** -- The 90-day window captures power users and paying subscribers in early adoption; replicate with more diverse users as products mature.

3. **Extend matched-query analysis to Computer-unique tasks** -- Many Computer queries have no Search equivalent. Since these tend to be more complex, efficiency gains may be even larger for them.

4. **Link agent usage to downstream workplace outcomes** -- Assess whether agents primarily accelerate existing workers, enable cross-occupational expansion, or create net-new categories of economically viable work.

5. **Labor market equilibrium effects** -- The partial-equilibrium individual framework leaves open how wages, job bundles, and coordination costs shift at macro scale as agents reduce cross-specialty coordination needs.

---

## Authors & Institutions

Jeremy Yang (Harvard University), Kate Zyskowski (Perplexity), Noah Yonack (Perplexity), Jerry Ma (Perplexity)
