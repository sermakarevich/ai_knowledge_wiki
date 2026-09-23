> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: How to Build a Custom Agent Harness

## Claims vs. evidence
- Claim: a useful agent equals model plus harness (`agent = model + harness`), and task-harness fit decides usefulness.
- The logic is plausible — a customer-service bot and a long-running coding agent clearly need different scaffolding — but the material offers reasoning and examples, not measurements.
- No benchmarks, failure rates, or cost comparisons back the fit claim; treat it as a sound design principle, not a proven performance result.
- Claim: `create_agent(model, tools, system_prompt)` is the easiest way to build a custom harness, shown with a concrete minimal code example.
- Supporting evidence is internal reuse: the GTM agent (go-to-market agent), the async coding agent, and the no-code builder all ship as `create_agent` plus a middleware stack.
- But "easiest" is never tested against alternatives in the material, so the reuse story proves viability, not superiority.
- Claim: middleware (small plug-in pieces hooking into the agent loop) composes freely, one concern per piece, across four levers: deterministic logic, tool lifecycle, custom state, stream handling.
- The levers are clearly described with examples (model swap, prompt adjustment, history updates, tool setup/teardown, counters and flags, event routing).
- Composition risks — hook ordering, conflicting middleware, debugging interacting pieces — are not shown or discussed.
- Claim: eight production capabilities map neatly to prebuilt middleware (overflow prevention, memory, environment actions, delegation, retries, policy, steering, cost control).
- The mapping table is specific and credible as a catalog, but reads as a feature list with no guidance on which combinations were load-tested together.
- Overall: strong conceptual evidence and internal reuse evidence, weak quantitative evidence. Treat the framework as a sound design pattern, not a proven performance claim.

## Genuinely new vs. repackaged
- Genuinely useful framing: "task-harness fit" names something practitioners feel but rarely state — match the scaffolding to the task's context, failure, policy, and environment demands.
- Simple test: fit means giving the model the right context at the right step, and judging every addition against that standard.
- Genuinely practical split: a minimal core loop plus composable middleware, instead of inheriting an opinionated prebuilt stack and fighting its defaults.
- Starting small and adding only what the task needs is a real and defensible alternative, especially for teams running several different agents.
- Repackaged: nearly every capability is a known pattern with a new label — summarization, context editing, retry with backoff (waiting longer between retries), model fallback, approval gates.
- Prompt caching (reusing repeated prompt prefixes to cut cost) and PII redaction (PII means personally identifiable information) are likewise standard practice, newly organized rather than invented.
- Subagent delegation with todo lists, filesystem and shell access, and stream routing to UI, audit log, and monitoring complete the picture: well-organized conventional wisdom.
- The novelty is the packaging — one middleware catalog with uniform hooks — not the underlying techniques.

## Weaknesses and blind spots
- No evaluation story: nothing on regression tests, task success metrics, or guardrail (safety rule) effectiveness measures for a harness.
- No failure analysis: what happens when middleware conflicts, summarization drops a critical fact, or retries amplify a bad tool call?
- Silent on hook ordering, precedence rules, and how to debug a long middleware chain when behavior goes wrong.
- Thin security treatment: PII middleware and approval gates are listed, but sandboxing (running untrusted code in an isolated box) and secret handling get no serious coverage.
- Prompt-injection (malicious text in tools or pages tricking the model) defense is likewise absent despite environment-action middleware widening the attack surface.
- No cost or latency numbers: caching and call limits are recommended without any sense of savings size or middleware overhead.
- Vendor framing throughout: every need resolves to LangChain's `create_agent` plus its catalog, with lock-in risk and migration cost unmentioned.
- Comparison with rival harnesses (Pi, Claude Agent SDK, Deep Agents) stays at slogan level rather than trade-off level.
- Narrow definition: the harness job is reduced to context delivery, while planning quality, tool design, and model choice — arguably equal drivers of success — sit outside the frame.

## Applicability
- Directly applicable when building task-specific agents: start from a minimal loop, add middleware per demonstrated need.
- Compaction for long runs, retries for flaky tools, approval gates for consequential actions — each earns its place instead of arriving by default.
- Works as a production-readiness checklist: walk the eight capabilities and justify each omission explicitly instead of discovering gaps in production.
- Less applicable for one-off prototypes or single-prompt workflows, where a full harness is overkill.
- Does not address planning or reasoning research; it is an engineering-organization article, not a science one.
- **Relevance to my work**
  - AI/ML engineering: adopt the minimal-core plus middleware pattern for experiment agents — deterministic hooks for prompt versioning, history compaction, and model swap (cheap model first, strong model on failure) with logged comparisons.
  - Agentic systems: use the capability table as a design review template — every agent states its choices for memory load/save, delegation, retries and fallbacks, policy enforcement, human steering, and cost caps; add the missing evaluation layer (task success, guardrail tests) the article omits.
  - Elisity data platform: highest value in policy enforcement and human steering — PII redaction, compliance checks, and approve-before-act gates firing on every call regardless of model behavior, plus audit-log stream routing for data access; pair with sandboxing and secret hygiene the article underplays.

## What this changes
- Changes the default starting question from "which framework?" to "what does this task demand?" — then assembles only the matching middleware.
- Changes code organization: tool setup, policy, state, and stream routing live bundled with their governing logic instead of scattered across the agent definition.
- That bundling should make harnesses reusable across an organization: one team writes a redaction or caching piece, every agent reuses it.
- Does not change fundamentals: context management, retries, human oversight, and cost control remain the same hard problems, just better labeled.
- The reuse claim (every LangChain agent ships this way) raises confidence but does not remove the need for our own testing.

## Verdict
- Sound mental model, handy catalog, thin evidence: worth using as design checklist and code structure, not as proof this stack beats alternatives.
- Main risk is silent adoption: taking the catalog without adding evaluation, conflict handling, and security hardening the article skips.
- For our agent work and Elisity needs, the policy, steering, and cost-control pieces map directly to real requirements, so a small pilot is cheap and informative.
- **trial**
