# If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module. | Arpit Bhayani

**Article:** [If you are letting AI agents write large chunks of your codebase, here is something I would recommend - decide your tradeoff per file / module. | Arpit Bhayani](https://www.linkedin.com/posts/arpitbhayani_if-you-are-letting-ai-agents-write-large-activity-7497869801172791296-s0mf) — LinkedIn, n.d.

## Human Readable TL;DR

Think of AI-generated code like cooking: for a quick weeknight snack you just want something fast and edible, but for a wedding cake you check every ingredient and taste at each step, because a mistake there ruins the whole day. Arpit Bhayani's advice is the same for your codebase — let the AI run fast and unsupervised on throwaway scripts and internal tools where mistakes are cheap, like letting a helper chop vegetables for a casual dinner. But for the dishes that really matter, like login systems, payments, and anything guarding your data, treat the AI's work as a rough first draft that a human chef must taste, inspect, and question before it ever reaches the table. The time you save on the quick snacks is exactly what buys you the attention to get the wedding cake right.

## TL;DR

You cannot simultaneously ship faster with AI-generated code and deeply understand everything you ship, so trying to have both everywhere leaves you with neither. The post prescribes sorting every file or module into one of two buckets before handing work to an agent: a speed bucket where the agent fully owns the code and re-deriving understanding is wasted attention, and a high-stakes bucket where failure is expensive or hard to reverse and agent output must be treated as a first draft subject to line-by-line review, system-wide tracing, and an explanation of its reasoning before merge. The time saved by shipping fast in the first bucket is meant to fund deep reading only where it counts, and that deliberate reallocation is presented as the whole tradeoff.

---

## Problem & Motivation

The post responds to a failure mode that appears once AI agents start writing large chunks of a codebase: teams either rubber-stamp everything and accumulate risk they do not understand, or they exhaust themselves trying to review everything and lose the speed advantage that motivated using agents in the first place. Both extremes stem from applying a single uniform level of human attention to all AI-generated code regardless of the blast radius of a mistake. The motivation is therefore to replace that uniform posture with an explicit per-file, per-module decision about where speed is acceptable and where deep human understanding is an engineering requirement, so that limited review attention is spent on the code where misunderstanding is most dangerous.

## Main Original Ideas

1. **Decide the tradeoff per file / module.** The central move is to make the speed-versus-understanding decision explicitly and granularly, module by module, before handing anything to an agent, rather than drifting into an implicit team-wide default of either trusting everything or reviewing everything.

2. **Bucket one: speed over understanding.** For code where being fast matters more than knowing every line — one-off scripts, internal tooling, and throwaway prototypes — the agent should own the code fully and engineers should not waste attention re-deriving understanding they will never need again, since that attention has a real opportunity cost elsewhere.

3. **Bucket two: understanding over speed.** For code where failure is expensive or hard to reverse — auth, payments, and anything touching data integrity — the agent's output is only a first draft, and merging requires reading the diff line by line, tracing how the change touches the rest of the system, and making the agent explain its own reasoning first.

4. **Reinvest saved time where it counts.** The framework closes the loop by directing the time saved through fast shipping in the first bucket into deep reading in the second bucket, so the tradeoff is not merely about accepting risk in low-stakes code but about funding rigor in high-stakes code with the resulting surplus.

## Key Findings

The post itself is a prescriptive framework rather than an empirical study, so its substance lies in the crispness of the rule and the comment thread that refines it around the edges. Commenters reinforce the core ask of not applying the same level of human attention to every line of AI-generated code, with one practical gloss being to use idle time while the agent works to read important code or think through the plan instead of fixing expensive mistakes later, alongside a warning that engineers grow weaker if deep thinking stops. A second refinement is dynamic rather than static: the speed bucket can shrink over time as the codebase matures and as teams learn to write better instructions for agents. The captured discussion also frames the stakes in engineering terms, with auditing every line of throwaway scripts described as diminishing returns on cognitive load versus concentrating review on critical paths such as authentication and data integrity, and with agent-friendly repos, documentation, and automated testing proposed as the guardrails that let the tradeoff scale safely.

## Suggestions & Future Directions

The post's explicit suggestion is procedural: sort modules into the two buckets before delegating to agents, let agents own the low-stakes bucket outright, and enforce first-draft discipline with line-by-line review, impact tracing, and agent self-explanation in the high-stakes bucket. Implicit in the comment discussion are two follow-on directions worth pursuing: building the repo-level guardrails (documentation before and after agent runs, automated tests, CI, and contracts) that make the low-stakes bucket genuinely safe to delegate, and investing in agent instructions and codebase maturity so that the boundary between the buckets can shift deliberately over time rather than by accident. Neither direction is developed into a roadmap in the captured material, but both follow naturally from treating the tradeoff as a living classification rather than a one-time sort.

## Authors & Institutions

The post is authored by Arpit Bhayani, listed on LinkedIn as an Influencer, with the captured page showing approximately 1,258 reactions and 41 comments. No institutional affiliation is stated in the wiki material. Visible comment contributors referenced in the chunks include Kareem Hesham, Arjun Joshi, Trilochanprasad B Hilli, Anurag Upadhyay, and Anshul Sahni.
