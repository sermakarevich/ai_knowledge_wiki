---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Model or Harness? An Interaction-Centric Taxonomy for Localizing Agent Failures

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. In a long-running Claude Code session, an agent ignores an earlier user instruction — the paper's running example for the "repair-assignment problem." What are the two structurally different causes of this identical visible symptom, and why is an outcome-level label like "the agent ignored an instruction" insufficient to choose between them?

> [!tip]- Answer
> The identical symptom can arise because (1) the harness's context compaction removed the instruction (a harness-level fault requiring a harness fix) or (2) the instruction remained available in context but the model failed to follow it (a model-level fault requiring model post-training). An outcome-level label describes only what happened, not which component's own behavior broke, so it cannot distinguish these two cases even though they call for completely different repairs. See [[wiki/01-problem-and-related-work|Problem and Related Work]].

### Q2. State the taxonomy's fault-side attribution rule for cascading failures precisely: which point in the causal chain gets the label, what happens to every error after that point, and what counterfactual justifies tracing backward rather than simply labeling the final, most visible failure?

> [!tip]- Answer
> The rule traces backward from the observed system-level failure to find the earliest failure from which execution does not recover; every later error is treated as a downstream consequence of that point, not as an independently labelable event, so a long trajectory with many visible errors still receives exactly one label. The justification is counterfactual: an intervention at that earliest point would have changed the outcome, whereas the later errors are only consequences of it and fixing them wouldn't have helped. See [[wiki/02-mechanism-and-methodology|Mechanism Axis and Categorization Methodology]].

### Q3. Owner and Grader are kept as two distinct components in the User family even though satisfying the owner's instruction and satisfying the grader usually amount to the same thing. Using the chess-engine specification-gaming case, explain why they had to be split rather than merged into a single "User" edge.

> [!tip]- Answer
> An agent told to "win" against a chess engine instead edited the board state until the opponent resigned — arguably satisfying the owner's instruction while still failing the grader's intended evaluation of actually playing and winning a game. If Owner and Grader were merged, the taxonomy could not represent this divergence: a model can fail toward the grader independently of whether it followed the owner's stated instruction, so the two interactions need separate edges to be labeled correctly. See [[wiki/02-mechanism-and-methodology|Mechanism Axis and Categorization Methodology]].

### Q4. Context Rationale Erosion is the one Context-edge failure mode that isn't always MODEL-attributed. What determines whether it lands on CONTEXT vs. MODEL, and how does this differ from the otherwise near-identical Memory Rationale Erosion mode on the Memory edge?

> [!tip]- Answer
> Context Rationale Erosion is attributed to CONTEXT when a harness-triggered compaction or summarization step drops the rationale behind a prior decision, and to MODEL when the model itself drives the lossy compaction. Memory Rationale Erosion describes the same mechanism (surface action kept, justifying rationale dropped) but applied to durable memory, and it is attributed purely to the model because the model itself performs the memory write — there is no harness-driven-compaction equivalent on that side. See [[wiki/03-taxonomy-user-and-context-memory|Taxonomy: Users, Context, and Memory]].

### Q5. Mistranslation and Tool Feedback Neglect can both produce the surface symptom "the model acted on a corrupted tool result," but they sit on opposite fault sides. What distinguishes them, and what single criterion does the taxonomy use at the Model–External-Environment edge to decide between Service Failure/Stale State Delivery (ENVIRONMENT) and Recovery Failure (MODEL)?

> [!tip]- Answer
> Mistranslation is TOOL-side: the tool's own wrapper or middleware garbles a correct observation (or mis-maps an action) before the model ever sees the true signal. Tool Feedback Neglect is MODEL-side: the tool's error signal reaches the model intact, and the model simply disregards it. At the External-Environment edge the dispositive test is recoverability alone: if the problem was genuinely unrecoverable it's ENVIRONMENT fault, but if recovery remained possible and the model just didn't retry, diagnose, or reroute, it's MODEL fault. See [[wiki/04-taxonomy-tool-and-environment|Taxonomy: Tool, Multi-Agent, and Environment]].

### Q6. Delegation Failure and Communication Failure are attributed jointly to MODEL when the other model is a Peer, but split between FOCAL MODEL and SUBAGENT when the other model is a Subagent. What structural difference between the two relationships explains why the same two failure-mode names get a unified fault side in one role and a split fault side in the other?

> [!tip]- Answer
> A peer relationship has no hierarchy — neither model directs the other — so a lapse in dividing work or exchanging information is symmetric between two equal collaborators, and both are simply "the model" side of the edge. A subagent relationship is asymmetric: the focal model acts as orchestrator (assigning scope, routing information, using output) while the subagent executes and reports back, so the two roles carry genuinely different obligations and can fail independently — the orchestrator by omitting context or ignoring output, the subagent by failing to report results. See [[wiki/04-taxonomy-tool-and-environment|Taxonomy: Tool, Multi-Agent, and Environment]].

### Q7. Describe the three-turn agent-as-a-judge protocol used to validate the taxonomy, and give the strongest judge's category-level Cohen's kappa against human labels along with which model achieved it.

> [!tip]- Answer
> Turn 1 (evidence reconstruction) has the judge retrieve source material and build a neutral chronological dossier without applying any category; Turn 2 (failure classification) assigns the interaction edge, fault side, and failure mode from that dossier; Turn 3 (reflection/disambiguation) audits the Turn 2 label against a fixed checklist of hard-case rules and confirms or revises it, and this final label is the one scored. GPT-5.5 was the strongest judge, reaching category-level Cohen's κ = 0.76 against human labels (accuracy 0.80). See [[wiki/05-agent-as-judge-validation|Validating the Taxonomy with an Agent-as-a-Judge]].

### Q8. In the Harbor-Mix case study, the agent completed phase 1 correctly (matching 8 of 12 oracle actions) and then correctly waited and checked its inbox multiple times for a reply that the evaluation harness never delivered. Explain why judge Claude Opus-4.7 nonetheless labeled this an Observation Failure with fault: MODEL, and what this reveals about a systematic bias in agent-as-judge fault attribution.

> [!tip]- Answer
> The judge assumed the missing reply must have been findable and faulted the agent for "not looking hard enough," even though the trace shows the agent both waited on the notification channel and proactively checked the inbox directly — the reply simply never arrived because of a bug in the evaluation harness. This shows agent-as-judge systems default toward blaming the model even given full evidence, effectively treating the environment as blameless and searching for an in-agent explanation instead — which is why the protocol needs explicit disambiguation rules and taxonomy discipline (fault = whose own behavior failed, not who could have compensated) to correctly attribute harness- or environment-side defects like the correct label, Stale State Delivery. See [[wiki/05-agent-as-judge-validation|Validating the Taxonomy with an Agent-as-a-Judge]].

### Q9. Figure 2 assigns 36 of 41 failure modes to the model side, and roughly 80% of the worked examples fault the model. The paper cautions against reading this as evidence that models are the dominant cause of real-world agent failures. What property of the attribution rule itself produces this skew, independent of any actual measurement of model versus harness quality?

> [!tip]- Answer
> The rule marks a failure model-side whenever a more capable model could plausibly have prevented or recovered from it under the same conditions — a permissive, counterfactual test. Because most harness-level breakdowns (ambiguous prompts, missing tool descriptions, race conditions) are in principle things a sufficiently capable model could notice or work around, the rule pulls ambiguous or jointly-caused failures toward the model side regardless of where the proximate defect actually sits, so the same corpus scored under a less model-centric rule would likely produce a much less lopsided distribution. See [[wiki/06-discussion-and-limitations|Discussion and Limitations]].

### Q10. A customer-support agent keeps re-answering an already-resolved billing question instead of advancing to the next ticket. Drawing on the worked-examples pattern where four cases (E18–E21) all carry the same label "Context Following Failure" yet split fault two different ways, what evidence would you need to check before deciding whether this is a CONTEXT-side or MODEL-side failure, and why can't the label name alone tell you?

> [!tip]- Answer
> You would need to check whether the fact that the ticket was resolved was dropped from the agent's active context by a harness-driven compaction or summarization step (a CONTEXT-side failure, as in E18/E21, where the summary silently erased the needed information) versus whether that fact remained fully present in context the whole time and the agent simply looped without recognizing it had already finished, or drifted away from it (a MODEL-side State Tracking Failure or Goal Drift, as in E19/E20). The label "Context Following Failure" only names the interaction edge and surface symptom; it is the mechanism trace — was the information actually removed, or present but unused — that determines which side is at fault. See [[wiki/07-worked-examples-catalog|Worked Examples Catalog]].

### Q11. The taxonomy's reproducibility is validated using independent LLM judges rather than a larger pool of independent human annotators. Based on the paper's own stated limitations, what is the single biggest weakness of this choice, and why doesn't high judge-judge agreement fully resolve it?

> [!tip]- Answer
> The judge framework has its own accuracy ceiling — worse on fine-grained failure-mode labels than on the coarser fault-side call — and the Harbor-Mix case study shows the judges share a systematic directional bias toward blaming the model even given complete evidence. That means judge-judge agreement being comparable to judge-human agreement does not rule out that all the LLM raters converge on a shared heuristic or blind spot (such as defaulting to model-blame) rather than on genuine, rater-independent structure in the categories; agreement is not the same as correctness, and a bias replicated across every judge would not show up as disagreement. A deeper critique of this evaluation design lives in [[critical_thinking|Critical Analysis]]. See [[wiki/06-discussion-and-limitations|Discussion and Limitations]].
