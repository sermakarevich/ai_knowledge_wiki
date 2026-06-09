# Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025

**Paper:** [Professional Software Developers Don't Vibe, They Control: AI Agent Use for Coding in 2025 (Huang et al., 2025)](https://arxiv.org/abs/2512.14012)

## Human Readable TL;DR

You've probably heard that some people let AI just "vibe" -- they describe what they want, the AI builds it, and they never really look under the hood. This paper studies whether experienced professional programmers actually work that way. Spoiler: they don't. Instead, seasoned developers use AI like a powerful but unpredictable junior colleague -- they give it clear, well-scoped tasks, watch what it does, and carefully review everything before it goes anywhere near real software. The study watched 13 developers work and surveyed 99 more, and the consistent finding is: the better you are at coding, the more control you insist on keeping.

## TL;DR

This paper empirically challenges the "vibe coding" narrative through field observations (n=13) and qualitative surveys (n=99) of experienced developers (3+ years). It finds that professionals retain deliberate control over AI agents -- scoping tasks carefully, validating outputs rigorously, and applying software quality standards throughout. Rather than passive automation, expert developers treat agents as productivity amplifiers for well-scoped, straightforward subtasks while reserving design and architectural decisions for themselves.

---

## Problem & Motivation

The AI coding landscape is split between hype ("I run dozens of agents autonomously") and sobering data (experienced developers slowed 19% by AI assistance; agentic systems achieving only 8% merged-PR success rates). Neither extreme explains how experienced professionals are actually integrating agents into real, quality-sensitive codebases. This paper fills that gap with empirical, qualitative data on what skilled developers actually do -- not what they claim or what benchmarks measure.

---

## Main Original Ideas

1. **"Vibe Coding" vs. Controlled Agent Use** -- The paper explicitly distinguishes passive "vibe coding" (trusting AI without review) from the deliberate, quality-driven agent use patterns observed in professionals. This framing rejects the assumption that AI adoption means ceding control.

2. **Agency Retention as a Core Professional Value** -- Experienced developers express a principled preference to retain agency over software design and implementation, viewing quality attributes (correctness, maintainability, security) as non-negotiable regardless of AI involvement.

3. **Task Suitability Taxonomy** -- The study identifies which task categories are well-suited for agent assistance (well-described, straightforward, bounded tasks) versus those where agents fail or slow developers down (complex, interdependent, design-heavy work).

4. **Planning and Validation Strategies** -- Developers employ consistent pre- and post-agent strategies: decomposing problems before delegation, and carefully reviewing/validating agent outputs before integration -- mirroring senior engineering review practices.

5. **Positive Sentiment Through Control** -- Developers express optimism about AI agents specifically because they feel capable of correcting agent failures. Confidence in their own skills enables productive engagement rather than anxiety or blind trust.

---

## Key Findings

| Dimension | Finding |
|-----------|---------|
| Study scope | 13 field observations + 99 survey participants, all 3+ years experience |
| Session format | 45-min observation + 30-min interview; 15-min survey |
| Task types covered | Production software, exploratory R&D, side projects |
| Study period | August 1 -- October 3, 2025 |
| Prior baseline | Agentic systems: ~8% complete success (merged PRs); AI assistance slowed some devs 19% |

- Developers universally describe wanting a "productivity boost" without sacrificing quality standards
- Agent use is constrained to "well-described, straightforward tasks" -- complex work remains human-led
- Positive sentiment correlates with perceived ability to catch and fix agent mistakes
- At least one developer stated they would "never go back to coding by hand" -- reflecting genuine productivity gains when agents are used appropriately
- Professionals apply the same best practices (planning, review, testing) to agent-assisted work as to manual work

---

## Suggestions & Future Directions

1. **Better agentic interfaces** -- Tool designers should build interfaces that support developer control loops: easier inspection of agent reasoning, granular undo, and better scoping primitives.
2. **Practitioner guidelines** -- The authors call for "agentic use guidelines" analogous to code review or testing standards -- structured advice for when and how to delegate to agents effectively.
3. **Recognize software engineering fundamentals** -- Effective agent use appears to depend on developers who already know good software practices; training and tooling should reinforce rather than bypass these fundamentals.
4. **Expand to other experience levels** -- The study focuses on experienced developers; future work should examine how junior developers interact with agents, where quality instincts may not yet be formed.
5. **Quantitative follow-up** -- The qualitative findings here warrant larger-scale quantitative studies measuring actual productivity, defect rates, and code quality under controlled agent use conditions.

---

## Authors & Institutions

Ruanqianqian Huang, Avery Reyna, Sorin Lerner, Haijun Xia, Brian Hempel
