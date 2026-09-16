> [[index|Wiki]] | [[summary|Summary]]

# Critical Analysis: Natural-Language Agent Harnesses

## Claims vs. evidence

(1) "IHR-executed NLAHs achieve comparable task outcomes to code harnesses" — **moderate**. The headline numbers cut both ways: IHR beats Code on Live-SWE (73.0 vs 67.0) and MHTBA (53.9 vs 36.0) but loses on OSWorld/SeeAct (46.3 vs 47.1), and Prompted-NLAH (plain instructions, no runtime) beats IHR on all three (77.0, 57.3, 47.9). "Comparable" is true in the sense that none of the three realizations dominates, but the paper's own numbers show a plain-prompted baseline outperforming the more elaborate IHR machinery everywhere tested — the runtime's contribution to task score, as opposed to policy legibility, is not clearly positive.

(2) "Static policy compresses ~20x while preserving mechanisms" — **strong**. The token/file counts (Live-SWE 60.1k/68 → 2.9k/3; MHTBA 10.5k/3 → 0.8k/1; SeeAct 47.5k/5 → 1.4k/1) are a direct, checkable artifact comparison, and the RQ2 mechanism audits (Artifact Contract ~0.96–1.0, Tool Call Success ~0.93, Failed Tool Continuation ~0.99) give converging behavioral evidence that the shrunk document isn't just shorter but still drives the same workflow steps.

(3) "Parent-child handoff is the main bottleneck" — **strong**. This is a clean, load-bearing weakness the authors surface rather than bury: Information Handoff Recall of 0.32 (SWE) and 0.55 (MHTBA) against 1.00 for Prompt, and Orchestration Reliability 0.83–0.85 vs ~0.99–1.00, directly explain why IHR trails Prompt everywhere — the mechanism (splitting execution across parent/child contexts) and the measured symptom (lost information) line up.

(4) "Explicit modules can be analyzed as interventions" (RQ3) — **moderate**. The ablations are real one-at-a-time additions with before/after numbers (file-backed state 73.0→75.6 SWE, 44.4→58.3 OSWorld; multi-candidate search's call-count blowup with a score drop), which is genuine ablation discipline. But the ablation is layered onto one "Basic" condition, one model (gpt-5.4-mini), one runtime version — it demonstrates that modules can be measured this way, not that the direction of each effect (e.g. context compression hurting) generalizes across models or runtimes.

(5) "The MHTBA portability failure shows why code harnesses are brittle" — **strong as a demonstration, narrow as a generalization**. 32/89 resolved with 66/89 timeouts (21 of which already hit verifier reward 1.0) is a concrete, well-diagnosed single case: a two-call `task_complete` protocol mismatched to GPT's text-only "DONE." It is a real, costly failure (up to 16.3M input tokens in the worst disagreement slice) but it is one harness, one model swap, one benchmark — evidence for "code harnesses can be brittle to model swaps," not evidence that NLAH+IHR is immune to the same class of failure in general (the paper does not stress-test IHR itself under a comparable model swap).

## Genuinely new vs. repackaged

The ingredients — natural-language instructions to an agent, parent/child agent delegation, ablation studies of agent scaffolds — are not new; "prompted harness" and "code harness" are both established patterns the paper itself treats as prior baselines. What is new is the explicit three-way framing (code vs. prompted vs. runtime-interpreted document) plus a shared, reusable runtime (IHR) that turns the document into an interpreter target rather than a one-off prompt, and the accompanying instrumentation (mechanism audits, module ablations, static-policy size counts) that make the harness itself a measurable object instead of incidental glue. The real contribution is the audit methodology and the labor-division formalism (Tables 8–10), not the discovery that natural language can drive an agent.

## Weaknesses and blind spots

- Single-model, single-runtime evidence: every RQ1–RQ3 number comes from one IHR instantiation (Codex CLI 0.123.0, gpt-5.4-mini, reasoning effort xhigh). Whether the NLAH pattern's cost/benefit tradeoff (worse handoff recall, comparable-to-worse scores vs. plain prompting) holds under a different base model or runtime is untested within the paper itself — this matters because the one negative control the paper does run (the MHTBA cross-model port) shows exactly this kind of brittleness for the code baseline.
- The comparison that matters least favorably for the paper's thesis (Prompt beating IHR on all three benchmarks) is reported but not foregrounded or explained: if plain, runtime-free prompting already achieves the best raw scores, the paper's case for IHR rests on inspectability, portability, and ablatability, not measured task performance — a claim the abstract's "comparable task outcomes" phrasing partly obscures.
- Cost accounting is asymmetric: RQ3 reports "Agent Calls" as a proxy for overhead (1.1→5.7 for multi-candidate search) but does not give a single harness-choice-normalized cost/latency/token comparison across Code vs. Prompt vs. IHR themselves, so a reader cannot tell whether IHR's readability benefit comes with an offsetting runtime/orchestration tax versus the simpler Prompt baseline.
- Ablations are additive from one Basic condition; interaction effects between modules (e.g. does file-backed state's gain shrink once self-evolution is also on?) are not reported, so "module X helps" claims are conditional on the specific stacking order tested, not necessarily each module's independent effect.
- The appendix's dramatic disagreement-slice numbers (Code-fail/Prompt-success N=26 at 316.5 episodes) are a small, unweighted slice count; no variance or confidence interval is given, so the magnitude of "extreme cost" is illustrative rather than statistically characterized.

## Applicability

Works: teams maintaining multiple hard-to-compare controller codebases who want a single shared runtime and short, diffable, ablatable policy documents for a task family — especially where the goal is legibility, portability across setups, and the ability to switch modules on/off, not squeezing out the last percentage point of benchmark score.
Fails or untested: settings where raw task score is the only metric that matters (the paper's own numbers show plain prompting winning there); any deployment that needs reliable parent-child state transfer without extra file-backed-state scaffolding (handoff recall is the demonstrated weak point); untested model/runtime combinations, since every number is anchored to one instantiation.
**Relevance to my work** —
- When designing a fleet-style orchestrator (parent task spawning child workers), budget explicitly for information loss at the handoff boundary — this paper's own numbers (0.32–0.55 recall) suggest that without file-backed shared state, a parent will systematically under-know what a child actually tried.
- Treat "add a module because it sounds safer" skeptically: multi-candidate search and context compression both hurt in this paper's ablations, which lines up with a general pattern that added branching/summarization steps can drift from what the evaluator actually checks.
- If porting a harness (code or NLAH) to a new model, explicitly re-derive the stopping/completion protocol rather than assuming the old signal transfers — the MHTBA case is a concrete cautionary template for the failure mode (verifier says done, agent doesn't know how to say so).

## What this changes

If the claims hold as stated: teams that currently maintain sprawling controller code for agent harnesses have a credible alternative — write the policy as a short document, run it on a shared interpreter — that keeps most of the mechanism fidelity and makes ablation and portability tractable, at some cost in parent-child information fidelity that can be partly recovered with file-backed state.
If only partially true (plausible given the Prompt-beats-IHR pattern across all three benchmarks): the safe reading is narrower — the NLAH+IHR pattern's main proven value is legibility and ablatability of harness policy, not a task-score improvement over already-good plain prompting, so adopt it where auditability/portability is the actual goal rather than expecting a performance win.

## Verdict

The paper is honest about its own weakest result (Prompt wins on raw score everywhere) and backs its strongest claims (compression, mechanism preservation, handoff bottleneck) with converging quantitative and qualitative evidence (token counts, mechanism audit scores, and a detailed cross-model portability failure case). But every number rests on one model/runtime instantiation, cost is not fully accounted for, and ablations are additive rather than factorial. **Trial** — worth adopting the document+runtime pattern for legibility and ablation on task families you maintain across multiple harness variants, but do not expect it to beat a well-tuned plain-prompted baseline on task score, and add file-backed state from the start given the demonstrated handoff weakness.
