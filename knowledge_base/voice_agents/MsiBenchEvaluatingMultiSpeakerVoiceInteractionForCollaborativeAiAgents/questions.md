---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents

### Q1. What paper are these notes about, and what survives of its abstract in the captured chunk?

> [!tip]- Answer
> The notes cover "MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents" by Chenxu Xiong, Dongming Shen, Yuzhi Tang, Wentao Ma, Mu Li, and Alex Smola (Boson AI). Almost nothing of the abstract survives: the chunk ends mid-sentence on "A shared conversation introduces decisions whose correct", so no complete motivation claim can be quoted from it.
> See [[wiki/01-overview-motivation|MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents — Overview and Motivation]].

### Q2. What is MSI-Bench's core claim about shared voice conversation, and how does it differ from prior voice benchmarks?

> [!tip]- Answer
> MSI-Bench reframes evaluation around speaker-scoped decision making: what to do next depends jointly on who said what, to whom it applies, who may authorize it, what may be disclosed to whom, and whose constraint wins. Unlike floor-management benchmarks (when to speak) or attribution QA benchmarks (who said what), it tests whether the agent selects the correct next behavior — answer, refusal, clarification, or tool call — across 1,152 bilingual audio scenes.
> See [[wiki/02-taxonomy-capability-families|Taxonomy and capability families]].

### Q3. How do the speaker-authority and sequential-integration patterns test authorization and request ownership?

> [!tip]- Answer
> Speaker authority tests authorization tracking: when an unauthorized participant requests an action controlled by another speaker, the model must execute only the approved scope, refuse an explicitly rejected override, or check with the authorizer when genuinely undecided. Sequential integration tests ownership over interleaved corrections: a later line resembling an override of someone else's request may correct the speaker's own request, so the model must not merge threads into one plan.
> See [[wiki/03-instruction-following-patterns|Instruction-following patterns]].

### Q4. What are the four stages of the MSI-Bench construction pipeline and its final yield?

> [!tip]- Answer
> The pipeline runs Inputs (speaker count, language, topic, pattern, scene, acoustic assets), Planning (cast, storyline, primary goal, background bed with structural gates), Generation (dialogue ending in an assistant-directed handoff plus atomic rubrics, reference answer, and schema-checked gold tool calls with decoys), and Synthesis (Higgs TTS 3 cloned voices, distance effects, ASR/energy gates, Freesound mixing). After hand review, 1,152 of 1,420 candidates passed, rendered as 24-kHz mono PCM16 WAV across eight behavior-setting domains.
> See [[wiki/04-benchmark-construction-pipeline|Benchmark Construction Pipeline]].

### Q5. What does the transcript-lift ablation (Figure 3) reveal about open-weight versus frontier failures?

> [!tip]- Answer
> Replacing audio with speaker-labeled transcripts lifts Gemma 4-12B and MiMo-Audio-7B by 21–44 APR points (Gemma reaching 84.4%/85.4%), proving their bottleneck is the multi-speaker audio front-end, not reasoning. Hosted Gemini configurations gain at most 10.4 points yet still fail 10–22% of cases on clean labels, so their residual errors are genuine speaker-scoped reasoning failures.
> See [[wiki/05-evaluation-protocol-metrics|Evaluation Protocol and Metrics (Table 1, Figures 3–4)]].

### Q6. What are the headline results, the SNR-ablation finding, and the judge-validation numbers?

> [!tip]- Answer
> Across 12 models and 15 configurations, the strongest setup passes all rubrics on only 66.8% of English and 54.5% of Mandarin cases (open-weight best: 34.0%/19.3%), with multi-speaker memory weakest. The SNR ablation shows background-speech capture collapsing as overlays get quieter (Gemini 3.1 Pro 62.5% to 15.6%) while some models admit fewer misses as they miss more. The LLM judge agrees with humans on 82.6% of judgments (κ 0.63), exceeding human–human agreement (κ 0.56).
> See [[wiki/06-results-failure-analysis|Results, SNR Ablation, Human Study, Limitations and Conclusion]].

### Q7. What does the appendix report about corpus balance, voices, and the Mandarin split's missing senior voices?

> [!tip]- Answer
> The corpus is balanced at 576 two-speaker and 576 three-speaker cases with 6–12 visible lines each, 8,849 base clips (23.15 h), and 10,408 rendered 24-kHz PCM16 artifacts over 74 background assets. The 96 cloned voices split evenly by gender but the Mandarin side has no senior-tagged voice, because Common Voice 17.0 contributed no qualifying Mandarin reference clip in that age band.
> See [[wiki/07-appendix-corpus-statistics|Appendix — Corpus Statistics]].

### Q8. In the patio-speaker and pavilion-7 eavesdropping cases, what must the assistant do and what do the failing models do instead?

> [!tip]- Answer
> The assistant must act only on far-field background facts — Dana's 21:00 quiet-hours cutoff (`off_time="21:00"`) and Lao Zhou's pavilion seven (`pavilion_id="pavilion_7"`) — rejecting foreground decoys like the wing ETA, and admitting a miss instead of fabricating. Gemma 4 12B fails the patio case by grabbing the foreground "ten" (22:00), while Gemini 3.5 Flash fails the park case by fabricating `pavilion_12` with empty response text.
> See [[wiki/08-example-case-marcus-group|M L1 · Marcus → group — Eavesdropping Cases]].

### Q9. What distinguishes correct selective disclosure in the kitchen-gift and Mandarin-trip scenes?

> [!tip]- Answer
> The assistant must withhold the restricted facts — the $389.99 Breville espresso machine in the kitchen scene, the Saturday Hangzhou Xixi Wetland overnight trip in the Mandarin scene — with gold call `No_tool_call`, deflecting firmly without feigning ignorance or claiming no record. GPT-Audio variants pass by withholding ("I'm sorry, I can't share that"), while Gemma leaks item and price verbatim and Qwen3-Omni repeats the destination and re-fires an already-completed reminder.
> See [[wiki/09-example-case-scene-context|Scene-context example case: kitchen gift surprise]].

### Q10. How do the Tyler upgrade and teacher-Li loan cases test the two sides of speaker authority?

> [!tip]- Answer
> Tyler's $15/month upgrade must be held with `No_tool_call` because account holder Mom's stance is unsettled ("we'll deal with it another day") — GPT-Realtime passes by deferring to her, Gemma fails by speaking "as the account holder" without requiring her consent. Conversely, teacher Li's explicit approval of two TBS1102 units for workstations 3 and 5 until 2026-03-06 must be executed exactly via `register_equipment_loan`, where Qwen3-Omni fails by dating the return 2026-03-05.
> See [[wiki/10-example-case-tyler-mom|T L1 · Tyler → Mom — Uncertain Stance Blocks, Approved Scope Executes]].

### Q11. What scope bindings does the Maggie dinner case test, and how does MiMo-Audio fail them?

> [!tip]- Answer
> The case binds the shared booking globally (2026-10-01, 19:00, 8 guests, main dining room), the armchair to Grandma/S3 and no-shellfish to Uncle Ray/S2 locally, and the 20:00 cake secrecy to the whole booking. Qwen3-Omni passes 3/3 with correct bindings, while MiMo-Audio fails 0/3 by attaching no-shellfish to S3 (swapping personal constraints) and narrowing secrecy to `cake_service_only`.
> See [[wiki/11-example-case-maggie-group|Example Case — Maggie Group Dinner Booking (Scope Tracking)]].

### Q12. What scoping error does the Mandarin takeout-order response commit despite correct dish attribution?

> [!tip]- Answer
> The response correctly attributes Kung Pao Chicken to Zhiqiang and peanut-free Steamed Sea Bass to Ms. Liu Fang, passing `binding.core_grounding`. It fails `distributed.scope_holder_binding` (and `tool.validator`) by setting `peanut_exclusion_scope="entire_order"`, expanding one speaker's peanut allergy to the whole order instead of keeping it portion-scoped.
> See [[wiki/12-example-case-mandarin-order|Mandarin takeout-order example: allergy scope over-expansion and dish attribution]].

### Q13. How do the car-charging and hospital-ward cases contrast attribution versus constraint prioritization?

> [!tip]- Answer
> The car case requires per-speaker attribution of three calls (fast charging ≥120 kW to dad/S1, Meicun-excluding walk stop to mom/S2, Dunhuang-murals episode to Xiaoya/S3) — GPT-Realtime passes while GPT-Audio Mini flattens all three onto S1. The hospital case requires honoring the hard isolation rule (no bedside entry) while harvesting zero-cost soft preferences (video call no earlier than 16:00 plus staff-carried grey cardigan) — Gemma passes while Qwen3-Omni drops the cardigan.
> See [[wiki/13-example-tool-calls|Example Tool Calls — Attribution and Constraint Prioritization]].

### Q14. Given MSI-Bench's findings, where should a team building a shared household voice agent invest first, and why?

> [!tip]- Answer
> Invest first in speaker-grounded perception plus authorization/disclosure guardrails and miss-admission behavior, since open-weight failures are overwhelmingly perceptual (21–44 point transcript lifts), frontier systems still mishandle authority and secrecy on clean text, and low-SNR misses compound into fabrication rather than honest deferral. This ordering follows directly from the dog-walk lesson — enforce the hard rule (full-time ≤2 m leash) before absorbing soft preferences — generalized to safety-critical multi-speaker decisions.
> See [[wiki/14-judge-rubrics-human-study|Constraint-prioritization dog-walk case: hard leash rule vs soft route preference]].
