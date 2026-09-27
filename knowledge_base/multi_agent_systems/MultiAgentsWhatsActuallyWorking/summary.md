# Multi-Agents: What's Actually Working

**Paper:** [Multi-Agents: What's Actually Working (Walden Yan, Cognition, 2026)](https://x.com/walden_yan/status/2047054401341370639)

## Human Readable TL;DR

Think of an AI coding system like a software team. Instead of one person writing AND reviewing their own code, you separate the roles: one person writes, a fresh pair of eyes reviews. The reviewer catches things the writer missed because they aren't carrying all the context baggage. This essay explains that this kind of structured collaboration -- where one AI does the work and others provide intelligence around it -- is what actually works in practice today, while "swarm" approaches where many AIs simultaneously rewrite the same code still lead to chaos.

## TL;DR

Cognition's engineering essay argues that multi-agent systems are only reliable today when writes stay single-threaded and additional agents contribute intelligence rather than parallel writes. Two practical patterns are validated in production: (1) a code-review-loop where a clean-context reviewer catches ~2 bugs/PR at 58% severity rate, and (2) a "smart friend" pattern where a weaker primary model escalates hard problems to a stronger frontier model. Unstructured swarms remain impractical for real software requiring human taste and decision coherence.

---

## Problem & Motivation

Ten months after Cognition published "Don't Build Multi-Agents," model capabilities have improved ~8x in enterprise adoption (Devin usage), creating both demand for multi-agent coordination and cost pressure to avoid expensive frontier models for every token. The essay revisits the original skepticism, documenting what narrower class of patterns actually works in production today.

The core challenge: parallel agents making independent write decisions fragment implicit choices (style, edge cases, code patterns), producing incoherent systems. Real software requires scaling human taste, not just parallelizing computation.

---

## Main Original Ideas

1. **Context Engineering over Prompt Engineering** -- The durable framing is ensuring agents have the right context, not tweaking prompts. Multi-agent setups compound context challenges: agents must share context (todo lists, plans, priors) but parallel writes create conflicting implicit decisions. This constrains most working multi-agent patterns to read-only subagents.

2. **Clean-Context Code Review Loop** -- Separating the coding agent from the review agent, with zero shared context between them, produces meaningfully better review quality. The reviewer reasons backward from implementation, catches things the coder normalized, and benefits from a shorter context window (avoiding "Context Rot" -- the phenomenon where attention quality degrades at long context lengths). Devin's self-review loop catches avg 2 bugs/PR, 58% severe (logic errors, security bugs), iterating until humans open the PR.

3. **Smart Friend Pattern** -- A weaker/faster primary model calls out to a stronger/more expensive frontier model as a tool, letting the primary decide when it's at its limits. Key engineering challenges: (a) the primary model needs to know when and how to escalate (hard for weaker models); (b) the smart model needs to respond beyond the literal question asked, pointing out things the primary missed even when not asked. Works well cross-frontier (Claude + GPT routing by capability), still an open problem with asymmetrically weaker primaries.

4. **Map-Reduce-and-Manage Hierarchy** -- The practical shape of higher-level delegation is: a manager agent breaks work into pieces, spawns child agents to execute, synthesizes and reports back. Not unstructured swarms. Key challenge: managers trained on small-scoped delegation default to over-prescription when they lack codebase context; cross-agent state sharing doesn't happen by default because models haven't been trained in environments requiring it.

5. **Single-Threaded Writes as the Invariant** -- The unifying principle across all working patterns: writes stay single-threaded, additional agents contribute intelligence (review, consultation, coordination) without fragmenting the write path. This preserves decision coherence while unlocking multi-agent benefits.

---

## Key Findings

| Pattern | Status | Key Metric |
|---------|--------|------------|
| Code-Review-Loop (clean context) | Production at Cognition | ~2 bugs/PR avg, 58% severe |
| Smart Friend (cross-frontier) | Production with Claude + GPT | Real gains in tricky scenarios |
| Smart Friend (weak primary) | Open problem | SWE-1.6 closes gap but not there yet |
| Manager-child hierarchy | Live in Devin | Still improving on context engineering |
| Unstructured swarms | Not recommended | Mostly a distraction for real software |

- Enterprise Devin usage grew ~8x over last 6 months.
- Clean-context review outperforms shared-context review because of Context Rot: attention quality degrades at long context lengths.
- Cross-frontier routing (model A vs model B by capability) works better than difficulty escalation (dumb → smart).
- Over-prescriptive managers (a failure mode) traced to training on small-scoped delegation tasks.

---

## Suggestions & Future Directions

1. **Train models for multi-agent communication** -- The current gaps (weaker model knowing when to escalate, child agents surfacing discoveries that change sibling work, context transfer without drowning the receiver) are identified as training problems, not just prompting problems.

2. **Train smart-friend-aware primary models** -- SWE models trained specifically with the back-and-forth smart-friend interaction in mind, so the primary model is calibrated on when/how to escalate.

3. **Build coherent higher-level delegation** -- Making a manager-child system feel as coherent as a single agent on a single task is the stated center of Cognition's 2026 work.

4. **Intelligence injection at every SDLC stage** -- The vision: planning, coding, review, testing, and monitoring all augmented by coordinated agents that scale human taste rather than replacing human decision-making.

---

## Authors & Institutions

Walden Yan (@walden_yan) -- Cognition AI (builders of Devin and Windsurf)
