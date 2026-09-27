> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Ablations and Analysis: Write-Time Distillation, Bank Dynamics, and Task-Adaptivity
**In one sentence:** Replacing raw-trajectory storage with write-time (ReasoningBank-style) distillation hurts JITMEM-base by 1.7–2.9 points on ALFWorld and 6.8–8.2 on WebShop, while controls confirm the RL curator genuinely distills retrieved experience, staged bank refresh helps only modestly, test-bank warm-starting is negligible, and qualitative cases show the same trace curated differently per task with RL-added procedural semantics.
## Key points
- Applying ReasoningBank-style distillation to each trajectory before storage (saving only distilled items instead of raw traces) drops JITMEM-base by 1.7–2.9 on ALFWorld and 6.8–8.2 on WebShop across executors.
- Forcing the retriever to return an empty set degrades JITMEM to or below untrained JITMEM-base, with success rate (SR) dropping by up to 14.8 on ALFWorld and 15.2 on WebShop, confirming RL gains come from distilling retrieved experience rather than parametric hints.
- Staged bank refresh (after 100 GRPO steps, discard the training bank, rebuild it by re-running the executor with the trained curator, hold fixed, train 50 more steps) improves SR by 2.8 for Qwen3-8B and 0.9 for GPT-5.4, with no change for Gemini-2.5-Pro — modest relative to cost.
- Pre-populating the empty test bank with 100 training trajectories ("test bank warm-starting") changes SR by at most 1.3, within standard deviation, across all three executors.
- The same retrieved past experience is curated into different payloads per task (Figure 3): state-change/heat-cool guidance for "put a hot potato in fridge" versus placement/verify-target guidance for "put a newspaper in sofa."
- On identical inputs (Figure 4, "Examine the bowl with the desklamp"), the RL-trained curator recovers the environment-specific workflow (move to the desklamp, then examine the bowl with it) while the untrained curator gives only a generic action sequence.
- The paper concludes JITMEM's read-time curation turns curator learning into an immediate single-step objective and reports the untrained curator is already competitive with strong write-time baselines, with RL further improving effectiveness, efficiency, and cross-executor transfer; limitations are the BM25 retriever, one extra LLM call per task, and fixed hand-designed payload formats.
---
## Write-time distillation discards information the curator needs
The ablation replaces raw trajectory storage with ReasoningBank-style distillation applied to each trajectory before storage, saving only the distilled items in place of the raw traces. This drops JITMEM-base by 1.7–2.9 on ALFWorld and 6.8–8.2 on WebShop across executors. Verbatim rationale from the chunk:
> "Because write-time distillation commits to a query-independent summary, information irreversibly lost at storage time cannot be recovered by the curator at read time (distillation prompt in Appendix A)."
## RL learns to distill retrieved experience, not parametric hints
The test forces the retriever to return an empty set ("w/o retrieved traj." in Figure 2b). Without retrieved context, JITMEM "degrades to or even below the untrained JITMEM-base across all executors, with SR dropping by up to 14.8 on ALFWorld and 15.2 on WebShop." The chunk states: "This confirms that the gains from RL training are grounded in learning how to distill retrieved experience."
## Staged bank refresh yields modest gains at additional training cost
The static training bank creates a mild train/test distribution shift (Section 3). The remedy: after 100 GRPO steps discard the original training bank, rebuild it by re-running the executor with the trained curator, hold the refreshed bank fixed, and continue training for 50 additional steps. Result (Table 5): SR improves by 2.8 for Qwen3-8B and 0.9 for GPT-5.4, while Gemini-2.5-Pro sees no change; the chunk concludes "the gains are modest relative to the additional training cost, suggesting that the static bank already provides a sufficient training signal."
### Table 5: Staged bank refresh and test bank warm-starting on WebShop
| Executor | Variant | Score |  | SR |  |
|---|---|---|---|---|---|
| Qwen3-8B | JITMEM | 61.1 | 0.9 | 32.8 | 1.7 |
| Qwen3-8B | w/ staged bank refresh | 61.7 | 0.9 | 35.6 | 0.3 |
| Qwen3-8B | w/ test bank warm-starting | 60.9 | 1.0 | 32.5 | 1.5 |
| Gemini-2.5-Pro | JITMEM | 61.0 | 0.8 | 50.5 | 0.8 |
| Gemini-2.5-Pro | w/ staged bank refresh | 61.0 | 0.3 | 50.5 | 1.1 |
| Gemini-2.5-Pro | w/ test bank warm-starting | 61.7 | 0.4 | 50.9 | 0.3 |
| GPT-5.4 | JITMEM | 53.8 | 0.3 | 45.4 | 0.0 |
| GPT-5.4 | w/ staged bank refresh | 53.6 | 0.4 | 46.3 | 0.1 |
| GPT-5.4 | w/ test bank warm-starting | 51.9 | 0.3 | 44.1 | 0.4 |
## Warm-starting the test bank provides negligible benefit
By default JITMEM starts with an empty test bank that grows organically as tasks are solved. The variant pre-populates it with 100 trajectories from the training set ("w/ test bank warm-starting" in Table 5). Differences are negligible across all three executors, "with SR changing by at most 1.3 and remaining within standard deviation," so "the curator handles sparse retrieval at the beginning of the test sequence gracefully without warm-starting."
## Qualitative analysis: the curator adapts the same experience differently for different tasks
Figure 3 shows two tasks retrieving the same past task and trajectory ("Put a cool egg in microwave" as retrieved context). For "Put a hot potato in fridge" the curator foregrounds the state-transition aspect, extracts a heat/cool strategy ("Cool/heat the object: Use a fridge or microwave"), and specializes it into task guidance (find the potato; heat it via microwave/stove; move to fridge, open, place inside, close, confirm). For "Put a newspaper in sofa" it emphasizes placement-specific considerations (take the object; move to the target; "Check the target location: Ensure the target location (e.g., sofa) is accessible and clear"), specialized into locate/take newspaper, move to sofa, verify placement. Verbatim: "A write-time artifact would commit to one framing, but the read-time curation produces both from the same stored trace."
## RL training induces environment-specific procedural semantics
Figure 4 compares JITMEM-base and JITMEM payloads on identical inputs for "Examine the bowl with the desklamp": "The untrained curator produces a generic action sequence; the trained curator recovers the environment-specific workflow (move to the desklamp, then examine the bowl with it)." The chunk notes such workflows are "not specified in the curation prompt" and "their emergence under optimization of r_task suggests that immediate task reward encourages task-relevant curation."
## Conclusion and limitations
The chunk's Section 5 states: "We introduced JITMEM, a memory framework that separates storage from curation by preserving raw trajectories at write time and synthesizing task-adaptive payloads only at read time, once the current task is known." It claims this "avoids committing prematurely to a single abstraction" and "turns curator learning from a delayed future-utility problem into an immediate single-step objective"; even the untrained read-time curator "is competitive with or outperforms strong write-time memory baselines" across ALFWorld, WebShop, and τ2-bench, while RL "further improves effectiveness, efficiency, and transfer across executor models." Verbatim closing claim:
> "Together, these results suggest that effective agent memory depends not only on what experience is stored, but on when and for which task that experience is curated."
Limitations given: the retriever (BM25) is simple and may bottleneck as the bank grows large and diverse; the curator adds an extra LLM call per task; the payload format is fixed and hand-designed per benchmark. Future work: jointly optimize the payload format, explore stronger retrievers, and extend curation from once per task to turn- or step-level adaptation as new observations arrive.
**Covers:** chunk 05-write-time-distillation-discards-information-the; ablations through Conclusion (Table 5, Figures 3–4, Sections 4.3–5, pp. 8–10)
