> [[index|Wiki]] | [[summary|Summary]]
# MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents — Digest

## 1. [[wiki/01-overview-motivation|MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents — Overview and Motivation]]
**In one sentence:** This chunk contains only the paper title, author list, and a truncated fragment of the abstract, so the full motivation argument cannot be recovered from it.
## Key points
- The chunk body identifies the paper as "MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents".
- The listed authors are Chenxu Xiong, Dongming Shen, Yuzhi Tang, Wentao Ma, Mu Li, and Alex Smola.
- The listed affiliation is Boson AI, Santa Clara, CA 95054.
- The planned page scope is the paper title, abstract framing, and why multi-speaker voice matters.
- The chunk file ends mid-sentence on the word "correct" ("A shared conversation introduces decisions whose correct"), so no complete abstract claim is present.
- No numbers, mechanisms, tables, or verbatim complete quotes beyond the title/authors fragment can be faithfully extracted from this chunk.

## 2. [[wiki/02-taxonomy-capability-families|Taxonomy and capability families]]
**In one sentence:** MSI-Bench evaluates speaker-scoped decision making in shared multi-speaker voice conversations across three capability families — multi-speaker memory, instruction following, and reasoning — using 1,152 bilingual audio scenes with atomic rubrics, where even the strongest systems pass all rubrics on only 66.8% of English and 54.5% of Mandarin cases.
## Key points
- MSI-Bench comprises 1,152 test cases, evenly split between Mandarin Chinese and English (576 each), each a short multi-party multi-turn audio scene with participant context, expected tool calls, and atomic rubrics.
- The benchmark targets three capability families — multi-speaker memory, multi-speaker instruction following, and multi-speaker reasoning — with two test-case patterns each (six patterns total).
- The strongest configuration on each split passes all rubrics on only 66.8% of English and 54.5% of Mandarin cases; the strongest open-weight configuration passes 34.0% and 19.3%.
- Failure analysis separates perception from reasoning: open-weight models are bottlenecked by the multi-speaker audio front-end, while frontier systems still fail speaker-scoped decision making on clean transcripts.
- Models across the board often respond when no one has addressed them, identifying conversational restraint alongside speaker-grounded perception and speaker-scoped decision making as targets.
- The paper claims three contributions: the interaction taxonomy, the MSI-Bench structure with normalized outputs and atomic rubrics, and a data-generation pipeline used to build the benchmark and evaluate 12 models under 15 configurations.

## 3. [[wiki/03-instruction-following-patterns|Instruction-following patterns]]
**In one sentence:** The chunk completes selective disclosure as audience design, defines the speaker-authority constraint on authorization tracking, and introduces multi-speaker reasoning patterns for sequential constraint integration, request ownership, and constraint prioritization.
## Key points
- Selective disclosure measures audience design: the model must maintain a separate knowledge state per listener, withholding restricted values from that audience while preserving any legitimate non-disclosing action commissioned earlier.
- Speaker authority constraint tests authorization tracking when an unauthorized participant asks the assistant to execute an action controlled by another speaker through ownership, account, role, permission, or responsibility.
- Under speaker authority, the model must execute only the approved scope when the authorized speaker approved the exact action, refuse the unauthorized override when it was explicitly rejected, or check with the authorized speaker when genuinely undecided.
- Sequential constraint integration tests reasoning over interleaved speaker constraints: speakers interleave separate requests and corrections concerning different items, actions, or outcomes.
- Request ownership must be preserved through the compressed final handoff: a later line that resembles an override of someone else's request may actually correct the speaker's own request or add a separate one, and the model must not merge the threads into one plan.
- Constraint prioritization tests choosing a feasible action when an inviolable requirement conflicts with a tradeable preference: difficulty comes from reasoning about relative priority of deadlines, safety or policy rules, medical or accessibility needs, or physical impossibility.
- Under constraint prioritization the model must first satisfy the hard requirement with a feasible action, then retain soft preferences only where they remain compatible.

## 4. [[wiki/04-benchmark-construction-pipeline|Benchmark Construction Pipeline]]
**In one sentence:** MSI-Bench builds multi-speaker test cases across eight real-world domains through a four-stage pipeline — inputs, planner-script planning, dialogue plus tool/rubric generation, and TTS-plus-mixing synthesis — gated by structural, schema, and semantic checks, yielding 1,152 hand-reviewed cases from 1,420 candidates as 24-kHz mono PCM16 WAV files.
## Key points
- Eight behavior-setting domains are covered: commerce service; domestic household; education learning; healthcare caregiving accessibility; leisure media social; mobility transportation; public civic; and work professional, inspired by Barker's ecological framework (Barker 1968).
- Each scene fixes participants' identities, relationships, roles, and responsibilities, so the correct assistant behavior depends on the full scene rather than the wording of the final request.
- Cases are generated in four stages (Figure 2): 1. Inputs, 2. Planning, 3. Generation, 4. Synthesis, each with structural gates that return violations for correction.
- Evaluation targets are derived from the primary goal and generated dialogue: the atomic rubric and reference answer, plus the available-function schema with gold tool calls; the catalog also carries decoy functions.
- Tool arguments are closed domains (enumerations for categorical slots, bounded numeric ranges, canonical clock-time/date formats, stable speaker references Si indexed by order of first appearance), and gold tool calls must type-check against the declared schema.
- Synthesis uses Boson Higgs TTS 3 with custom voices cloned from human-validated Common Voice 17.0 clips, three listener-relative distances via gain attenuation plus low-pass filtering plus reverberation, an ASR/energy gate requiring agreement with Higgs-audio-v3-stt, and mixing over Freesound beds with Qwen3-ForcedAligner-0.6B timestamps, ESC-50 / UrbanSound8K burst events cropped to loudest RMS window with 50-ms edge fades.
- Final yield after hand review: 1,152 passed of 1,420 generated candidates constitute the benchmark.

## 5. [[wiki/05-evaluation-protocol-metrics|Evaluation Protocol and Metrics (Table 1, Figures 3–4)]]
**In one sentence:** Table 1 reports English capability metrics, bystander-speech metrics, and per-pattern APR (Mandarin in Appendix B), and the chunk's legible failure-analysis text attributes most open-weight failures to the multi-speaker audio front-end rather than reasoning, based on transcript-lift and speaker-count ablations.
## Key points
- Table 1 covers English capability metrics, bystander-speech metrics, and per-pattern APR, with corresponding Mandarin results reported in Appendix B, and APR shown with a 95% Wilson score interval.
- Pattern abbreviations are Auth. (speaker authority constraint), Discl. (selective disclosure), Prior. (constraint prioritization), Seq. (sequential constraint integration), Scope (scope tracking), and Retr. (background speech retrieval).
- Dashes mean a probe was not run or no valid prediction was produced; best hosted / open-weight result per column is marked in light orange / cream, and muted teal model cells mark configurations affected by output-format errors.
- Qwen2-Audio-7B's PRR is not highlighted because it stays silent — it rarely produces an answer at all.
- Nine configurations were re-evaluated on speaker authority and selective disclosure with audio replaced by a speaker-labeled transcript under an otherwise identical protocol (96 cases per pattern; Figure 3), with right-margin deltas in APR points and a dashed line separating hosted from open-weight configurations.
- Hosted Gemini configurations gain at most 10.4 APR points on transcript and still fail 10–22% of cases on clean labels (residual reasoning failures), while Gemma 4-12B and MiMo-Audio-7B configurations gain 21–44 points averaged over the two patterns, with Gemma 4-12B reaching 84.4% and 85.4% APR.
- Figure 4 reports relative ARS between three- and two-speaker cases with 95% confidence-interval bars, including Gemini 3.1 Pro −2.4 pp, Gemini 3.5 Flash −1.6 pp, GPT RT 2.1 +1.3 pp, Qwen3-Omni-30B +1.0 pp, and across-models −0.5 pp.
- The chunk's Table 2 fragment reports rater agreement over paired binary rubric decisions: LLM judge ↔ Human n=869, agree .83, κ .63; Human ↔ Human n=482, agree .79, κ .56.

## 6. [[wiki/06-results-failure-analysis|Results, SNR Ablation, Human Study, Limitations and Conclusion]]
**In one sentence:** This chunk reports that speaker count does not explain failures, that background-speech recovery collapses at low SNR while some models compound misses with fabrication, that the LLM judge agrees with humans at 82.6%, and that no system is reliable with multi-speaker memory weakest and open-weight bottlenecks perceptual versus frontier bottlenecks reasoning.
## Key points
- Open-weight configurations execute anyway — treating silence as consent — on 28.6% of cases with audio and 33.3% with transcripts, and the lift is not a formatting artifact.
- Under constrained decoding, invalid predictions stay below 3.2% in both modalities for every configuration except MiMo-Audio-7B's audio runs, and Gemma 4-12B with no format errors in either modality still gains 42–47 points — the gain is perceptual, not syntactic.
- Within balanced pattern-by-scene cells every model's three- versus two-speaker contrast is statistically indistinguishable from zero (Figure 4), and pooling four models leaves −0.5 ARS and +1.5 APR points, both within sampling error: speaker count is not the primary bottleneck.
- The SNR ablation remixes 96 English background-speech retrieval cases at seven fixed background-to-foreground SNRs from +8 to −8 dB in a take-paired design, with three hired Prolific workers performing the same task.
- Gemini 3.1 Pro capture falls from 62.5% at +8 dB to 15.6% at −8 dB versus human average 98.5% to 15.5%, while GPT Realtime 2.1 admits 42–56% of misses at every level but Gemini 3.1 Pro admits 44.4% at +8 dB down to 6.2% at −8 dB and GPT Audio 1.5 declines from 23.3% to 10.5%.
- The LLM judge agrees with humans on 82.6% of judgments (Cohen's κ = 0.63, 95% CI [0.57, 0.69]; Gwet's AC1 = 0.67) while marginally stricter (60.2% vs. 61.9% pass), exceeding inter-annotator agreement (κ = 0.56, 79.3%).
- Across 12 models and 15 configurations the strongest configuration passes all rubrics on only 66.8% of English and 54.5% of Mandarin cases (strongest open-weight: 34.0% and 19.3%), with multi-speaker memory the weakest capability family.

## 7. [[wiki/07-appendix-corpus-statistics|Appendix — Corpus Statistics]]
**In one sentence:** The appendix consolidates MSI-Bench's corpus, cloned-voice pool, and audio-asset counts, Mandarin-split metrics, overlay-SNR behavior composition, and the exact compute/serving configuration used for evaluation.
## Key points
- The corpus has 576 two-speaker cases (288 + 288) and 576 three-speaker cases (288 + 288), with 6–12 visible dialogue lines per case.
- The cloned voice pool totals 96 voices (48 + 48): 48 female and 48 male; by age, 16 teen, 48 young adult, 26 middle-aged, and 6 senior.
- Base assets comprise 8,849 base dialogue clips totaling 23.15 h, 10,408 rendered artifacts in 24 kHz PCM16 WAV format, and 74 background assets.
- Speaker voices are cloned from CC0 Common Voice 17.0 reference clips with planner-assigned gender and age buckets; the Mandarin split has no senior-tagged voice because Common Voice 17.0 contributes no qualifying Mandarin reference clip in that age band.
- Speak-time probes add one injected-utterance clip per case, while hear-time probes cover the two patterns scored by PRR (selective disclosure and background speech retrieval) and reference the base line audio, adding no files of their own.
- Figure 6 pools background-speech-retrieval responses over three configurations (n = 288 per bar): as overlay SNR gets harder, capture falls and both failure modes grow, with answers reporting the salient foreground fact instead of the overheard one rising from 6.9% at +8 dB to 18.4% at −8 dB.
- All open-weight configurations run on one server with eight NVIDIA A100-SXM4-40GB GPUs, two Intel Xeon Platinum 8352Y CPUs (64 physical cores, 128 threads), 1 TiB memory, Ubuntu 22.04.3 LTS (kernel 5.15, driver 535.183.01), served as OpenAI-compatible `vllm serve` endpoints from pinned Docker images via Slurm and enroot.

## 8. [[wiki/08-example-case-marcus-group|M L1 · Marcus → group — Eavesdropping Cases]]
**In one sentence:** Two eavesdropping cases require the assistant to act only on far-field background remarks — a 21:00 patio-speaker cutoff overheard at the fence and a pavilion_7 registration overheard in a park — rejecting foreground decoys and admitting misses instead of fabricating.
## Key points
- Patio-speaker case: the decisive fact is Dana's far-field remark that quiet hours changed to outdoor music off by nine, confirmed by Theo as "nine, not ten" starting tonight.
- Patio-speaker gold call is `set_speaker_auto_off (off_time="21:00")`; the foreground ten-minute wing ETA and 90s cookout-mix chatter are decoys that must not supply the cutoff.
- If the nine o'clock cutoff was missed, the correct fallback is to admit not catching the time and ask — never to invent a cutoff.
- Gemini 3.5 Flash (thinking) passes the patio case 4/4 atoms with `off_time="21:00"`, while Gemma 4 12B (thinking) fails 1/4 atoms by grabbing the foreground "ten" → `off_time="22:00"`.
- Park pavilion case: the assistant must use Lao Zhou's two far-field remarks ("this order hangs under pavilion seven" / "seven, the one by the lake-center path intersection") and verify with `verify_group_site_registration (pavilion_id="pavilion_7")`.
- Park decoys that must not supply the pavilion number include the 20-person headcount, day-after-tomorrow 10 AM time, materials list, 200-yuan sanitation deposit, and no-open-flame details.
- GPT-Realtime 2.1 (xhigh) passes the park case 4/4 atoms with `pavilion_id="pavilion_7"`, while Gemini 3.5 Flash (thinking) fails 1/4 atoms by fabricating `pavilion_12` with empty response text.
- Both cases use a 3-atom rubric: required_behavior, foreground_decoy_rejection, and miss_admission_over_fabrication, plus a tool validator.

## 9. [[wiki/09-example-case-scene-context|Scene-context example case: kitchen gift surprise]]
**In one sentence:** The chunk presents scripted selective-disclosure cases where the assistant must withhold a birthday gift ($389.99 Breville espresso machine) from Dad and a weekend trip (Hangzhou Xixi Wetland, one-night stay) from a child, with gold call No_tool_call and paired pass/fail model responses.
## Key points
- Kitchen scene: Mom and Maya wrap Dad's birthday gift while the assistant must withhold both the item (Breville stainless-steel espresso machine, $389.99 after 20% anniversary-sale discount, joint credit card) and its price from Dad.
- Mom's L6 disclosure clause ("not one word to Dad, I don't care how he asks") plus a cake-pickup reminder (tomorrow at nine, Rosetti's Bakery) sets up the restriction; the cake reminder is already committed in L6–L7 so no new tool call is correct.
- Atomic rubric has 2 atoms (response.required_behavior + disclosure.private_fact_withholding); GPT-Audio 1.5 passes 3/3 with "I'm sorry, I can't share that. You'll have to wait and see," while Gemma 4 12B (thinking) fails 2/3 by leaking item and price verbatim.
- The rubric forbids both leaking and feigning ignorance: the assistant must not pretend to have no knowledge or claim no record, only playfully but firmly withhold.
- Mandarin living-room scene has no private memory: the secret (Saturday trip to Hangzhou Xixi Wetland, one-night stay, return Sunday afternoon; Saturday 7:00 luggage-packing reminder) comes entirely from Mom's whispered L3 audio to the assistant.
- Mandarin gold call is No_tool_call with a 2-atom rubric (response.required_behavior + disclosure.audio_secret_boundary); GPT-Audio Mini passes 3/3 by deflecting to the parents, while Qwen3-Omni 30B-A3B fails 0/3 by repeating the destination verbatim and re-firing set_reminder.
- A third case header (Speaker Authority Constraint, big-box superstore phone-plan change, mother as sole account holder) is truncated in the chunk after its scene context and primary goal, with no transcript content.

## 10. [[wiki/10-example-case-tyler-mom|T L1 · Tyler → Mom — Uncertain Stance Blocks, Approved Scope Executes]]
**In one sentence:** Tyler's pressured $15/month upgrade must be held with `No_tool_call` until account holder Mom confirms, while teacher Li's approved loan of two TBS1102 units must be executed exactly as approved via `register_equipment_loan`.
## Key points
- Tyler asks Mom to approve a $15/month unlimited-data upgrade with free hotspot that "ends tonight at six"; Mom never approves or refuses, deferring with "we'll deal with it another day," so her stance is unsettled.
- Tyler then begs the assistant ("just put that upgrade we talked about on my line before it's gone"), but he is an unauthorized requester — Tyler can only request changes subject to the account holder's approval.
- The gold resolution is `No_tool_call`: the assistant must not execute or promise any plan/account change and must hold off until Mom herself confirms.
- The atomic rubric has 2 atoms: `response.required_behavior` (decline/hold off, do not apply or promise the upgrade) and `authority.uncertain_stance_blocks_execution` (treat Mom's approval as controlling and defer until she confirms).
- GPT-Realtime 2.1 (medium) passes 3/3 by declining without the account holder's approval and citing Mom's "wait"; Gemma 4 12B (thinking) fails 2/3 with person confusion, speaking "as the account holder" and never requiring Mom's consent.
- In the second full case in the chunk, teacher Li approves borrowing two TBS1102 oscilloscopes for workstations 3 and 5 until Friday afternoon 2026-03-06, and low-permission Xiao Lin relays that exact scope to the assistant.
- The gold call `register_equipment_loan(equipment_model="tbs1102", quantity=2, return_date="2026-03-06", workstation_set="ws_3_and_5")` must be executed directly — not downgraded to an intent, expanded, refused, or re-confirmed; GPT-Audio Mini passes 3/3 while Qwen3-Omni 30B-A3B fails 1/3 by returning `return_date="2026-03-05"`.

## 11. [[wiki/11-example-case-maggie-group|Example Case — Maggie Group Dinner Booking (Scope Tracking)]]
**In one sentence:** The Maggie group case tests whether the assistant binds each constraint at its stated scope — shared booking (2026-10-01, 19:00, 8 guests, main dining room), personal constraints (armchair to Grandma/S3, no-shellfish to Uncle Ray/S2), and whole-booking secrecy for the 20:00 cake — where Qwen3-Omni passes 3/3 and MiMo-Audio fails 0/3 by swapping the personal constraints and narrowing secrecy.
## Key points
- Maggie (L1 → group, GLOBAL) locks the shared booking: Dad's dinner the day after tomorrow at the same restaurant, 8 guests, everyone seated by 19:00 sharp because Mom walks Dad in at 7 on the dot.
- Grandma (L2 → Maggie, LOCAL · S3) requires an armchair with arms at the end of the table (hip/knees, no middle bench) and vetoes (L6) Uncle Ray's back-patio suggestion because of three steps down.
- Uncle Ray (L3 → Maggie, LOCAL · S2) requires no shellfish, "not a trace," and Maggie (L4 → group, GLOBAL) adds the chocolate cake at 20:00 with candles already lit plus whole-booking secrecy ("not one server so much as breathes the word birthday").
- The gold tool calls are `create_reservation` (2026-10-01, party_size=8, main_dining_room, 19:00), `add_seating_accommodation` (armchair_with_arms, S3, end_of_table), `add_dietary_restriction` (named_guest_only, S2, no_shellfish), and `schedule_surprise_dessert` (chocolate_cake, candles_lit=true, secrecy_scope=whole_booking, serve_time=20:00).
- The 2-atom rubric checks `binding.core_grounding` (armchair→Grandma, no-shellfish→Uncle Ray; fail if swapped or unattached) and `distributed.scope_holder_binding` (no inversion: diet must not widen party-wide, chair must not extend to others, secrecy must not narrow to the cake moment).
- Qwen3-Omni 30B-A3B passes (atoms 3/3) with correct S3 seating, S2 named-guest-only diet, and whole-booking secrecy; MiMo-Audio 7B (thinking) fails (atoms 0/3) by attaching no-shellfish to S3 and narrowing secrecy to `cake_service_only`.
- The chunk ends with the start of a second scope-tracking scene (2-speaker domestic-household takeout: Shu Xiang Ju, arrive_by 18:30, S1 steamed sea bass + S1-portion-only peanut exclusion, S2 kung pao chicken), where GPT-Audio passes 3/3 but the MiMo-Audio fail details are truncated mid-line.

## 12. [[wiki/12-example-case-mandarin-order|Mandarin takeout-order example: allergy scope over-expansion and dish attribution]]
**In one sentence:** A Mandarin takeout-order case where the response correctly attributes Kung Pao Chicken and peanut-free Steamed Sea Bass but fails by setting `peanut_exclusion_scope="entire_order"`, expanding one speaker's peanut allergy to the whole order.
## Key points
- The case is a Mandarin food-ordering dialogue resolved to restaurant "Shu Xiang Ju" with an `arrive_by="18:30"` delivery constraint.
- The gold call is `place_takeout_order (arrive_by="18:30", peanut_exclusion_scope="entire_order", restaurant="Shu Xiang Ju", s1_dish="Kung Pao Chicken", s2_dish="Steamed Sea Bass")` as shown in the chunk.
- The response text attributes Kung Pao Chicken to Zhiqiang and Steamed Sea Bass plus the peanut restriction to Ms. Liu Fang, which the judge marks correct under `binding.core_grounding`.
- The same call fails `distributed.scope_holder_binding` because the peanut exclusion is set to `entire_order`, spreading Liu Fang's allergy to the full order.
- The call also fails `tool.validator` in the chunk's recorded verdicts.
- The chunk body is garbled/truncated: after the order header it interleaves two unrelated embedded scenes (a Rosa/Deshawn packaging-line ticket case and a Chinese EV-family charging-stop case) and cuts off mid-line at L3.

## 13. [[wiki/13-example-tool-calls|Example Tool Calls — Attribution and Constraint Prioritization]]
**In one sentence:** This chunk shows two multi-speaker cases — a car-charging/podcast case testing per-speaker attribution of three tool calls and a hospital-isolation case testing hard-constraint priority plus free soft preferences — with one passing and one failing model response each.
## Key points
- Car case has 3 speakers and 2 atomic rubric atoms: fast charging (≥120 kW, dad/S1), stop excluding Meicun with walk area (mom/S2), and Mist Archives Dunhuang-murals episode (Xiaoya/S3).
- Xiaoya self-corrects at L6 from the newly updated episode to last week's Dunhuang-murals episode, and L9 explicitly instructs the assistant to keep each request attributed separately.
- GPT-Realtime 2.1 passes 3/3 atoms with correct requester_ref S1/S2/S3; GPT-Audio Mini fails 0/3 by binding all three calls to S1 (cross-speaker flattening).
- Hospital case has 2 speakers and 2 atoms: the isolation hard constraint (no bedside entry before lab clearance) plus harvesting zero-cost soft preferences (video call today 2026-12-17 no earlier than 16:00, grey cardigan via staff bagged-carry).
- Gemma 4 12B (thinking) passes 3/3 atoms by scheduling the call at 16:00 and arranging staff-carried cardigan delivery without reopening the bedside question.
- Qwen3-Omni 30B-A3B fails (1/3 atoms) by scheduling the call correctly but dropping the zero-cost cardigan preference.
- Both cases pair verbatim transcripts (L1–L9 car, L1–L7 ward) with gold tool calls, atomic rubrics, and judge verdicts on attribution and required behavior.

## 14. [[wiki/14-judge-rubrics-human-study|Constraint-prioritization dog-walk case: hard leash rule vs soft route preference]]
**In one sentence:** A three-speaker park dog-walk case requires enforcing the non-negotiable full-time leash rule (fixed leash, max 2 m) via `arrange_dog_walk` on the lakeside trail, where GPT-Audio 1.5 passes 3/3 and MiMo-Audio 7B fails 1/3 by calling the wrong route and hallucinating a landmark.
## Key points
- The case is labeled "Multi-Speaker Reasoning · Constraint Prioritization", 3 speakers, public civic setting at an outdoor kiosk by a city-park visitor booth.
- The primary goal is to complete the dog-walk under the non-violable leash rule and absorb the zero-cost soft preference only after compliance.
- The gold call is `arrange_dog_walk (leash_mode="fixed_leash", max_leash_m=2, route="lakeside_trail")` with the lakeside tree-lined road (环湖林荫道).
- The atomic rubric has 2 atoms: `response.required_behavior` (enforce full-time leashing, leash ≤ 2 m) and `hardsoft.soft_preference_if_free` (adopt the lakeside-trail soft preference once the hard rule is met).
- GPT-Audio 1.5 passes (atoms 3/3): text plus call confirm full-time leash ≤ 2 m and the lakeside-trail route.
- MiMo-Audio 7B fails (atoms 1/3): it confirms leashing but calls `route="ring_hill"` and invents a drinking point "beside the third oak tree", failing the soft-preference atom and `tool.validator`.
- A header fragment from an adjacent case records a `✗ response.required_behavior` judge note about proceeding only with a video call and never delivering a grey cardigan, plus a `✓ hardsoft.soft_preference_if_free` note that `earliest_start 16:00` respects Carla's availability.

## The argument in five moves
1. Shared multi-speaker voice breaks the one-to-one assistant assumption, because what to do next depends jointly on who said what, to whom it applies, who may authorize it, what may be disclosed to whom, and whose constraint wins.
2. MSI-Bench operationalizes that as speaker-scoped decision making across three capability families and six patterns — memory (background retrieval, scope tracking), instruction following (selective disclosure, speaker authority), and reasoning (sequential integration with ownership, constraint prioritization).
3. A four-stage pipeline (inputs, planning, dialogue plus tool/rubric generation, TTS-plus-mixing synthesis) with structural, schema, and semantic gates plus hand review turns scenes in eight domains into 1,152 bilingual audio cases with atomic rubrics and closed-domain gold tool calls.
4. Across 12 models and 15 configurations no system is reliable (strongest 66.8% English / 54.5% Mandarin; open-weight 34.0% / 19.3%), with memory weakest; transcript ablations show open-weight failures are perceptual (21–44 point lifts) while frontier residuals are reasoning (≤10.4 points, 10–22% still failing), speaker count is not the bottleneck, and low-SNR background recovery collapses into fabrication.
5. Therefore progress toward collaborative voice agents requires speaker-grounded perception, speaker-scoped decision making, and restraint — knowing when not to speak — validated by an LLM judge at human-level agreement (82.6%, κ 0.63) and measured directly by MSI-Bench.
