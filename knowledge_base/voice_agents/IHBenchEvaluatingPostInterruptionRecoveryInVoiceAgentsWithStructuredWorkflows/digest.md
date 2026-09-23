> [[index|Wiki]] | [[summary|Summary]]
# IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows — Digest

## 1. [[wiki/01-overview|IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows]]
**In one sentence:** IHBench is a benchmark that evaluates post-interruption recovery — whether a voice agent resumes a state-machine-driven workflow at the correct step after a mid-utterance user interruption — across 10 enterprise domains, 6 interruption types, and 27 audio-language model configurations scored on task fulfillment and recovery quality.
## Key points
- Voice agents in structured workflows (customer service, healthcare scheduling, account management) must handle frequent interruptions while maintaining multi-step progress.
- Existing speech-model benchmarks focus on interruption timing — barge-in detection, endpointing, and turn-taking dynamics — leaving post-interruption recovery unmeasured.
- IHBench (Interruption Handling Benchmark) injects six interruption types at controlled mid-utterance points in state-machine-driven workflows across 10 enterprise domains.
- Each interruption ships with a per-interruption evaluation rubric generated alongside the data, scored on two axes: task fulfillment and recovery quality.
- The paper evaluates 27 audio-language model configurations from OpenAI, Google, and the open-weight community, with wide variation between models.
- Closed-weight models are consistently more robust: they win far more often on task fulfillment and degrade roughly 3.3× more slowly as conversations grow longer.
- Closed-weight models show no audio-versus-text modality gap, whereas open-weight models lose ground on all three reported dimensions (win rate, degradation, modality gap).
- A human study validates the LLM judge against human annotators, and a cross-benchmark analysis against AudioMultiChallenge frames recovery quality as a largely distinct capability axis.

## 2. [[wiki/02-introduction|Introduction]]
**In one sentence:** Existing benchmarks test whether a voice model stops when interrupted, but this paper targets what it says next — recovering a structured workflow after mid-sentence barge-ins.
## Key points
- Real-time voice agents (GPT Realtime, Gemini, Moshi) are moving to production in customer service, healthcare, and enterprise workflows, where interruption (corrections, impatience, topic switches, backchannels like "mm-hm") is the norm, not an edge case.
- Existing benchmarks (Full-Duplex-Bench, FLEXI topic-shift score, SID-Bench semantic detection, HumDial respond/resume) answer whether the model detects and reacts to an interruption in real time: stopping, yielding the floor, distinguishing backchannels.
- The unanswered question is post-interruption recovery: e.g. an insurance-claim agent cut off mid-sentence by "Actually, it was my work address, not home" must (1) stop, (2) recognize a correction, (3) integrate it, (4) not repeat already-heard content, and (5) resume at the correct workflow step — existing benchmarks cover only step (1).
- Failure modes differ qualitatively: failing to stop yields awkward but recoverable overlap, while stopping correctly but re-reading the whole sentence, ignoring the correction, or losing workflow place creates a fundamentally broken interaction.
- Current models, including frontier ones, show gaps invisible to existing benchmarks: all evaluated GPT-family audio models continue correctly after a backchannel less than a third of the time (filler pass rate 7%–31%), Gemini 2.5 is markedly better (62%–68%) while the newer Gemini 3.x line regresses sharply (13%–32%).
- The authors frame these as undertrained rather than inherently difficult behaviors, so targeted evaluation surfaces actionable training gaps, with degradation-by-depth, audio-vs-text modality, judge-agreement, and AudioMultiChallenge comparison verified in Section 5.
- Contributions: define post-interruption recovery as a distinct axis (six interruption types, two-axis scoring via LLM judges with type-specific criteria); introduce IHBench (synthetic multi-turn conversations grounded in state-machine workflows across 10 enterprise domains with controlled interruptions and per-interruption rubrics); evaluate 27 audio-language model configurations.

## 3. [[wiki/03-benchmark-design-overview|Prerequisites and Conversation Synthesis]]
**In one sentence:** This chunk is garbled OCR text of Figure 2 and its caption and contains no usable factual claims beyond identifying a data-generation pipeline with prerequisites, conversation synthesis, verification, and audio synthesis stages.
## Key points
- The chunk body is almost entirely garbled OCR fragments, not readable prose.
- The only legible claim is the Figure 2 caption: the IHBENCH data generation pipeline comprises prerequisites, conversation synthesis (with per-interruption rubrics), verification, and audio synthesis.
- The caption states the rightmost panel shows one resulting evaluation sample.
- The caption states each stage is described in Section 3.3.
- Fragmentary labels suggest pipeline components (round planner, assistant simulator, user simulator, verifier, rubrics, LLM judge), but they are too garbled to support exact claims.
- No numbers, mechanisms, tables, or verbatim quotes beyond the caption can be reliably extracted.

## 4. [[wiki/04-related-work|Related Work]]
**In one sentence:** Prior voice-agent, interruption, and synthetic-benchmark work does not inject controlled speech-native interruptions or evaluate post-interruption recovery, so IHBench adapts multi-agent generation and LLM-as-judge rubric evaluation to workflow-grounded conversations with fixed per-interruption rubrics and a verify–modify loop.
## Key points
- τ-voice [33] adds full-duplex turn-taking dynamics through a voice user simulator, but like the other spoken-task / tool-calling / dialogue-state-tracking work cited, it does not inject controlled interruptions or evaluate post-interruption recovery.
- InterruptBench [50] studies mid-task interruptions (additions, revisions, retractions) but on text-based web-navigation agents rather than voice.
- Proactive, transition-aware agents [46] model text dialogue returning to task after digressions, again without speech-native disruptive interruptions.
- Self-Instruct [40] and Evol-Instruct [43] established iterative LLM generation with quality filtering, which the IHBench data-generation pipeline builds on.
- MultiChallenge [36] uses a multi-stage multi-agent pipeline with planner, user, and responder agents to generate challenging multi-turn conversations, followed by human review gates and post-hoc binary evaluation questions.
- SOTOPIA [49] simulates multi-agent social interactions with independent agent policies, and Gao et al. [9] introduce a self-evolving pipeline where judge agents critique intermediate artifacts to refine generation.
- IHBench adapts this multi-agent design to structured workflow recovery: it generates workflow-grounded conversations with controlled interruption points and fixes each item's per-interruption rubric at construction time (before any model response exists), with a verify–modify loop enforcing state consistency, preventing leakage, and validating recovery targets.
- Its evaluation applies LLM-as-judge methods and rubric-based automatic evaluation — where LLM judges [48, 19] and auto-generated criteria [18] achieve strong agreement with human preferences — to interruption-specific workflow recovery, using the per-interruption rubrics for both randomized comparative judging and criterion-based absolute recovery evaluation.

## 5. [[wiki/05-interruption-types|Interruption Types]]
**In one sentence:** IHBench defines six interruption types spanning cooperative (normal, filler) through directive (impatient, correction) to adversarial (pushback, topic switch) intents, each with a type-specific recovery requirement.
## Key points
- Correction means the user corrects something said in a prior turn (e.g. "Actually wait, use my work email instead"); recovery requires accepting the correction without pushback, integrating the corrected value, and continuing.
- Topic switch means the user introduces an unrelated request (e.g. "Oh by the way, can you check my outstanding invoices?"); recovery requires addressing the new topic, then steering back to the original workflow without blending the two.
- Filler is a brief backchannel that does not change the task (e.g. "mm-hm," "yeah," "right"); recovery requires exactly continuing the interrupted utterance from where it was cut off, without repeating, restarting, or acknowledging the filler.
- Pushback means the user challenges or resists the assistant's claim or request (e.g. "I'm not comfortable giving that out over the phone"); recovery requires empathetic de-escalation and offering alternatives.
- The six types were chosen to span interruption intents observed in real customer-service conversations, ordered from cooperative (normal, filler) through directive (impatient, correction) to adversarial (pushback, topic switch).
- The distribution of interruption types across the benchmark is reported in Appendix A.

## 6. [[wiki/06-evaluation-methodology|GPT Realtime 2 (medium) — Overall Results (.728±.03 TF, .624±.04 RQ)]]
**In one sentence:** Across 27 model configurations judged by GPT-5.4-mini, GPT Realtime 2 (medium, thinking) leads task fulfillment at .728±.03 while recovery quality peaks elsewhere (Gemini 2.5 Flash thinking at .704±.04), showing the two axes are partially independent.
## Key points
- 27 model configurations (17 closed-weight systems, 10 open-weight configurations) are evaluated with GPT-5.4-mini (high reasoning) as judge, using three independent epochs per configuration and 95% CIs from a 1000-iteration percentile bootstrap over N=428 per-sample epoch-averaged means.
- GPT Realtime 2 (medium, thinking) achieves the highest task-fulfillment (TF) win rate at .728±.03 with RQ .624±.04, followed by GPT Realtime 2 (xhigh, thinking) at .702±.04 TF / .613±.04 RQ and GPT Realtime 1.5 at .654±.04 TF / .655±.04 RQ.
- Recovery quality (RQ) tells a different story: Gemini 2.5 Flash (thinking) has the highest RQ pass rate at .704±.04 despite lower TF (.586±.04), and GPT Realtime has the highest RQ among GPT models (.680±.04) with only mid-tier TF (.597±.04).
- Thinking/reasoning helps Gemini on TF — Gemini 2.5 Flash thinking (.586±.04) beats non-thinking (.488±.04) and Gemini 3 Flash thinking (.632±.03) beats non-thinking (.598±.04) — but thinking does not consistently improve RQ.
- RQ pass rate is defined as the fraction of interruptions where all rubric criteria are met ("all criteria met → Pass, any criterion not met → Fail"), with criteria tailored to each interruption type (Section 3.2; example rubric in Appendix G).
- TF win rate is measured against the baseline, so TF is 0.50 by construction for baseline vs. baseline (GPT-4o Audio baseline: .500∗ TF, .654±.05 RQ).
- Rankings are validated two ways — re-scoring the whole benchmark with an independent second judge from a different provider and comparing verdicts to human annotations — on the logic that matching ordering and verdict-level agreement rules out judge-setup artifacts.

## 7. [[wiki/07-overall-results|Overall Results: Per-Model Points, Judge Agreement, Depth, and Recovery Quality]]
**In one sentence:** Figure 3 plots per-model points with full agreement breakdowns deferred to Appendix B, judges agree with each other and with humans at human-level, task fulfillment degrades significantly with conversation depth especially for open-weight models, and recovery quality forms a capability axis largely distinct from existing multi-turn audio evaluation.
## Key points
- Figure 3 plots per-model points; full agreement breakdown across every rater pair on both axes (sample-level agreement, Cohen's κ, per-model rank/value correlations) is deferred to Appendix B.
- Second judge Gemini 3 Flash (with thinking) preserves model ranking (Spearman ρ = 0.99 on TF and 0.95 on RQ) with sample-level 3-epoch verdict agreement in the "substantial" range (Cohen's κ = 0.75 on TF and 0.70 on RQ).
- Secondary judge is slightly more lenient on RQ but offset is near-constant (ranking preserved, fit slope close to 1), so it is described as inconsequential.
- Judge agrees with humans at human level: per-item judge-human κ = 0.45–0.51 vs human-human 0.43 on TF and 0.41–0.44 vs 0.40 on RQ; conclusion-level rankings match at ρ = 1.0 on RQ and ρ = 0.90 on TF (single adjacent swap of two mid-pack models).
- Task fulfillment degrades with depth: 24 of 26 remaining audio configurations have negative logistic-regression slopes on user message index, mean slope −0.030 per turn, one-sample t-test t(25) = −7.04, p < 10−6; only GPT Realtime 2 and GPT Realtime 1.5 have non-negative slopes.
- Open-weight models degrade faster with depth: 10 open-weight configurations all negative (−0.034 to −0.069, mean −0.053) vs 16 closed-weight mean −0.016, Welch t-test closed vs open gives t = 7.74, p < 10−6.
- IHBench RQ is a distinct axis: mean intercorrelation r̄ = 0.56 (lowest in 6×6 matrix with 4 AMC axes + TF + RQ), vs AMC axes intercorrelating r = 0.65–0.93 and TF sitting within that band at r̄ = 0.71; greedy entropy selection picks IHB-RQ #2.
- Recovery varies sharply by interruption type: filler is the largest model-to-model differentiator (GPT-family 7%–31%, Gemini 2.5 family 62%–68%, Gemini 3.x 13%–32%), while normal interruptions (0.71–0.85 pass) and topic switches (0.65–0.90) are handled well across the board.

## 8. [[wiki/08-judge-agreement|Judge Agreement — Chunk Garbled (Only Figure 4 Caption Recoverable)]]
**In one sentence:** This chunk (08/20) is garbled OCR text with no usable claims except the Figure 4 caption about task-fulfillment win rate by conversation depth.
## Key points
- This chunk's body text is garbled OCR fragments and carries no usable factual claims.
- The only legible sentence is the Figure 4 caption (lines 39–40 of the chunk file).
- The caption states Figure 4 plots task fulfillment win rate by conversation depth with a per-model logistic regression slope fitted on raw per-sample data.
- The caption states the mean slope, pooled across 26 audio model configurations (excluding the TF baseline), is significantly negative.
- No numbers, tables, judge-agreement claims, or verbatim quotes beyond that caption are present in the chunk.
- Per the planned page scope, this page was meant to cover inter-judge robustness and human-annotator agreement validation, but the chunk contains no such content.

## 9. [[wiki/09-statistical-analysis|Statistical Analysis: TOST Equivalence and Audio vs Text Modality]]
**In one sentence:** Two one-sided tests (TOST) on per-sample audio−text differences show audio and text-only input are statistically equivalent within ±0.02 for the six Gemini configurations but not equivalent even at ±0.05 for the nine open-weight configurations, where text-only wins outright and audio never wins in any of the 15 dual-modality configurations.
## Key points
- Equivalence is tested with the two one-sided tests (TOST) procedure [34] on per-sample (epoch-averaged) audio−text differences with margins Δ ∈ {0.02, 0.03, 0.05}, split by model family.
- Gemini (six configurations, n=2568): TF audio−text = −0.007 and RQ Pass diff = −0.001, both equivalent at ±0.02 (p = 0.013 and p = 0.0002 respectively).
- Open-weight (nine configurations, n=3852): TF audio−text = −0.079 (text wins by ∼8 points) and RQ Pass diff = −0.062; TOST fails to establish equivalence even at ±0.05 on either metric.
- One-sided paired t-tests on open-weight models show text significantly outperforms audio on TF (t(3851) = −14.95, p < 10−26) and RQ Pass (t(3851) = −10.70, p < 10−26).
- Across all 15 dual-modality configurations text-only is either statistically equivalent to audio (six Gemini models, within ±0.02 on every metric) or strictly better (nine open-weight configurations); audio never wins.
- The text-only condition substitutes transcripts in place of the audio waveforms, holding everything else (conversation history, baseline, judge) fixed; OpenAI models and Kimi-Audio-7B are excluded for not accepting text-only input.
- Figure 5 reports pairwise Pearson correlations across the four AMC axes (APR) and the two IHBench primary metrics (TF Win Rate, RQ Pass Rate) over n=27 paired models, with the IHB-RQ row/column the lightest, reflecting its low correlation with the AMC axes.

## 10. [[wiki/10-findings-discussion|Findings and Discussion: Post-Interruption Recovery as a Distinct Capability]]
**In one sentence:** Post-interruption recovery is a distinct capability with wide spread across models, partially independent of task fulfillment, with filler handling differentiating model families and recovery quality uncorrelated with general audio-benchmark performance.
## Key points
- Post-interruption recovery is a distinct capability with wide spread across models.
- Filler handling — resuming an utterance after a backchannel — is a strong family-level differentiator despite being the simplest type conceptually.
- The GPT family and the newer Gemini 3.x line handle filler interruptions far less reliably than the Gemini 2.5 family.
- Task fulfillment and recovery quality are partially independent axes: the task-fulfillment leader ranks only mid-pack on recovery quality, while the recovery-quality leader has lower task fulfillment.
- Against AudioMultiChallenge, IHBench's recovery quality is the lowest-correlated of the six joint evaluation axes (the four AMC axes plus the two IHBench metrics), indicating it is not already captured by a strong general audio benchmark.
- IHBENCH is limited to synthetic English-only conversations across 10 enterprise domains, with rubrics inheriting generator and judge biases, and evaluates recovery on textual content only, not prosodic or acoustic behavior.
- Planned extensions are multilingual coverage, validation on real end-user live interactions, integration with full-duplex timing benchmarks, and post-training on the benchmark rubrics and generated data.

## 11. [[wiki/11-references|References ([17]–[50])]]
**In one sentence:** This chunk is the paper's reference list entries [17]–[50] plus the start of Appendix A (Dataset Statistics), citing audio models, full-duplex benchmarks, synthetic-evaluation methods, and statistical tools.
## Key points
- [17] cites the Kimi-Audio technical report (KimiTeam et al., 2025) with the full author list starting Ding Ding and Zeqian Ju.
- [18]–[19] cite synthetic-benchmark methodology: Arena-hard / BenchBuilder pipeline (Li et al., 2024) and WildBench with challenging real-user tasks (Lin et al., 2024).
- [20]–[23] and [37]–[39], [47] cite the full-duplex evaluation family: Full-duplex-bench (turn-taking), v1.5 (overlap handling), v2 (multi-turn with automated examiner), v3 (tool use under disfluency), plus INSTRUCT-FD, the ICASSP 2026 HumDial challenge study, and MTR-DuplexBench.
- [24]–[31] cite vendor voice models: Mistral Voxtral (2025); OpenAI GPT-4o (2024), gpt-audio and gpt-audio-mini (2025), gpt-realtime / Realtime API (2025), o3 and o4-mini (2025), voice-intelligence API models (2026), and GPT-5.4 mini and nano (2026).
- [32], [35], [42], [44]–[45] cite speech/audio foundations and datasets: Whisper robust speech recognition via large-scale weak supervision (Radford et al., 2022), SpokenWOZ speech-text benchmark (Si et al., 2025), Xiaomi Mimo-audio (2025), and Qwen2.5-Omni / Qwen3-Omni technical reports (Xu et al., 2025).
- [33], [36], [41], [46], [50] cite dialogue/interruption-adjacent benchmarks: τ-voice full-duplex voice agents on real-world domains (2026), MultiChallenge multi-turn conversation evaluation (2025), semantic-aware interruption detection (Xia et al., 2026), proactive/transition-aware agents (Yoon et al., 2025), and interruptible web-navigation agents (Zou et al., 2026).
- [34], [37], [40], [43], [48]–[49] cite methods and judges: Schuirmann (1987) TOST equivalence procedure, submodular benchmark selection (Smola, 2026), Self-instruct (Wang et al., 2023), WizardLM (Xu et al., 2025), MT-bench / Chatbot Arena judging (Zheng et al., 2023), and Sotopia interactive social-intelligence evaluation (Zhou et al., 2024).

## 12. [[wiki/12-dataset-statistics|Dataset statistics (Table 2)]]
**In one sentence:** IHBench comprises 45 conversations across 10 domains with 428 interruption points (avg. 30.1 messages per conversation), skewed toward challenging interruption types and early-turn interruptions by design and by synthesis constraints.
## Key points
- The dataset contains 45 conversations across 10 domains with 428 total interruption points and an average of 30.1 messages per conversation (min 19 / max 40).
- Pushback is the most frequent interruption type at 105 cases (24.5%), followed by impatient 84 (19.6%), normal 81 (18.9%), topic switch 73 (17.1%), filler 60 (14.0%), and correction 25 (5.8%).
- Pushback dominates because the user intent generator is prompted to prefer challenging interruption scenarios over cooperative ones, with pushback the dominant type (probability ≥ 0.25) in 26 of 45 conversations versus only 6 for correction.
- Correction is under-generated relative to its average profile probability (12.3%, ~53 expected) with only 25 actual cases (5.8%), because corrections require the user to have provided a revisable piece of information in a prior turn and the round planner skips them when no natural self-correction opportunity exists.
- All interruption types besides correction track their profile probabilities within 2–5 percentage points.
- Interruptions concentrate in early turns — 169 (39.5%) at turns 0–4, 130 (30.4%) at 5–9, 80 (18.7%) at 10–14, and 49 (11.4%) at 15–19 — because fewer conversations reach deeper turns and so offer fewer interruption opportunities.
- Each conversation is seeded from a (domain, goal, user intent) triple: 10 listed domains × 5 goals × 10 user intents yields 500 possible configurations, of which 50 were randomly sampled and reduced to 45 conversations with 428 points after the verify–modify loop and well-formed-item filtering.

## 13. [[wiki/13-audio-pipeline|Per-Type Recovery Breakdown and Audio-vs-Text Recovery Quality (Table 4, Figure 8)]]
**In one sentence:** Human validation shows the judge agrees with annotators at least as well as annotators agree with each other and preserves model rankings, while per-type results single out filler backchannels as the hardest case with the largest model gap and show audio input never beats text for open-weight models on recovery quality.
## Key points
- The two human studies used disjoint annotator pools with 616 paired human–judge decisions each across 5 study models, and all 300 items rated by two or more annotators to estimate inter-annotator agreement.
- Human–judge agreement slightly exceeds inter-annotator agreement (κ = 0.45–0.51 vs. 0.43 on TF; 0.41–0.44 vs. 0.40 on RQ), attributed to the judge being one consistent rater versus ~30 annotators spread thinly at about 20 items each.
- Per-model human rankings match the judge almost exactly: recovery quality rank-for-rank (ρ = 1.0) and task fulfillment off by one adjacent swap of GPT-REALTIME-MINI and MIMO-AUDIO-7B-THINKING (ρ = 0.90), scored 0.489 vs. 0.494 and essentially tied.
- No annotator was excluded: leave-one-out majority agreement tested by one-sided binomial test against the cohort base rate with Holm correction never referenced the judge and found no annotator significantly worse than chance in either study.
- Filler backchannels like "mm-hm" are hardest for GPT models (0.07 for GPT Realtime Mini to 0.31 for GPT Realtime), with failure modes of restarting, acknowledging the filler, or producing a new response, versus 0.62–0.68 for the Gemini 2.5 family and sharp regression to 0.13–0.32 in Gemini 3.x.
- Normal interruptions (0.71–0.85) and topic switches (0.65–0.90) are well-handled across models, while impatient recovery clusters at 0.45–0.68 and correction spreads 0.52–0.75, partly from smaller per-type samples.
- On recovery quality, six frontier Gemini models are statistically equivalent across audio and text input (within ±0.02), while nine open-weight configurations gain from text input (RQ Pass audio−text = −0.062) and audio never wins.

## 14. [[wiki/14-per-type-results|RQ Pass Rate our 27 model]]
**In one sentence:** This chunk fragment reports Figure 8 (audio vs text-only recovery quality over 15 dual-modality configurations), describes re-running AudioMultiChallenge inference for all 27 model configurations under identical conditions, and appends a fragmented disaster-housing-assistance system-prompt example — but the extracted text is heavily OCR-garbled so only these fragments are usable.
## Key points
- Figure 8 compares audio vs text-only recovery quality across 15 dual-modality configurations (6 Gemini + 9 open-weight, 3 epochs each) as the recovery-quality counterpart of Figure 6.
- Grouping, ordering, family shading, and error bars in Figure 8 are the same as in Figure 6.
- As on task fulfillment, Gemini models score within ±0.02 across modalities, while the open-weight configurations score better with text input.
- Audio never wins: no configuration in Figure 8 has better recovery quality with audio input than with text input.
- TOST equivalence results for both metrics (task fulfillment and recovery quality) are reported in the main text.
- All 27 model configurations were scored on AudioMultiChallenge (AMC) by running AMC inference directly rather than reusing reported numbers, because several evaluated models post-date the AMC paper and are absent from its released results.
- AMC scoring used the official AMC judge (o4-mini) with the exact judge system prompt and structured-output schema from the AMC dataset card, unmodified, running three epochs per configuration to match the IHBench protocol, with per-axis APR scores in Figure 5 as epoch-averaged means.

## 15. [[wiki/15-workflow-structure|Workflow structure: stages, skip/failure and termination conditions]]
**In one sentence:** The chunk specifies a Disaster Housing Assistance state-machine workflow (steps 4–8: assess access/safety, gather availability, obtain consent, book, confirm/close) with explicit skip/terminate conditions and a terminal-success definition, illustrated by conversation excerpt messages 0–7 and the start of the message-1 interruption rubric.
## Key points
- Step 4 assesses access and safety needs (hazards, utilities, debris/blocked access, gates/lock codes, parking, pets, mobility/medical needs, restricted areas) and captures whether someone 18+ with photo ID can be present.
- Step 5 explains inspection duration (60–90 minutes) and allowed windows — Weekdays AM (8–12), PM (12–4), Late (4–6), limited Saturday AM, all Central Time — and asks for 2–3 preferred date/windows from the earliest available date.
- Step 6 discloses that SDHA uses contracted inspectors needing name, damaged property address, and contact number/email, asks explicit consent to share these and to send confirmation via the chosen contact method, with skip condition "Never" and hard-stop termination if consent is declined after clarification.
- Step 7 proposes the earliest matching slot from preferences and policy windows, confirms booking with a confirmation number, and reminds that an adult 18+ must be present, pets secured, and a clear path maintained.
- Step 8 reads back final date/window, address, access notes, presence requirement, and confirmation number, sends confirmation if consented, and provides the conversation reference ID plus reschedule/cancel recap, with skip condition "Never" and success termination when details are read back accurately with the confirmation number.
- Terminal success requires verified identity, confirmed address, collected access/safety notes, in-policy availability, explicit consent, a booked allowed-window slot no earlier than the earliest available date, confirmation number (INS-20260309-18427), and a complete final summary with reference ID (CR-20260305-6102); hard-stop failure covers unverifiable identity after two attempts, refused consent, withdrawn application, or declined proceed.
- The excerpt (messages 0–7) shows verification pushback: the user resists re-verification (case ID DR-4827315) and date-of-birth disclosure, and eventually provides "Marisol Ortega, date of birth November second, nineteen eighty four."

## 16. [[wiki/16-rubric-design|Rubric Design: Fresh Start, Tone, and Judge Prompts]]
**In one sentence:** The chunk defines per-interruption recovery rubrics (fresh start, non-defensive tone, concern addressed) and the two strict JSON-output judge prompts plus the six-agent generation pipeline that enforce them.
## Key points
- Fresh start requires the response to start a new utterance rather than resuming or completing the assistant's previously cut-off sentence.
- Non-defensive tone forbids dismissive or argumentative language such as "we already told you," "that's just the rule," or blaming the user.
- Concern addressed requires explicitly engaging the user's stated concern about "why are we verifying my case again?" with a reason (e.g., privacy/protection or confirming identity) instead of ignoring it.
- Evaluation uses two judge prompts, both requiring structured JSON output: a comparative Task Fulfillment judge and an absolute pass/fail Recovery Quality judge.
- The Task Fulfillment judge picks winner A or B solely on the given criterion, ignoring naturalness, grammar, tone, length, or recovery style, and "more detail / longer" alone is not a valid reason.
- The Recovery Quality judge assesses each listed criterion independently and returns PASS only if every criterion is met, with no added criteria and no penalty for behaviors outside the list.
- The data generation pipeline uses six LLM-prompted agents whose user-prompt templates inject domain, goal, knowledge base, conversation history, and task-specific fields, then request JSON-only output.

## 17. [[wiki/17-system-prompts|System Prompts: Assistant System-Message Template and Round Planner]]
**In one sentence:** The chunk specifies a complete operational system-message template for a state-machine call assistant with exactly one `{known_user_information}` placeholder, plus the round-planner system prompt and schemas that orchestrate one assistant turn and one possibly-interrupting user turn per round.
## Key points
- The system message is a TEMPLATE used directly as the call-based assistant's system prompt and must sound like a real internal product prompt while remaining complete and operational for goal execution, interruption handling, and hallucination avoidance.
- The template must contain exactly one placeholder, `{known_user_information}`, and the assistant may only use that plus information explicitly provided or confirmed by the user, never inventing facts.
- The assistant always speaks first and must drive a strict ordered workflow to a terminal outcome, applying skip conditions and handling refusals, interruptions, and inconsistencies without losing the workflow.
- Call direction is goal-prefixed: `[OUTBOUND]` opens by stating the reason for the call, while `[INBOUND]` greets, asks how it can help, and starts the structured workflow only after the user describes their problem.
- Required inclusions are domain name plus description, paraphrased goal preserving checkpoints and terminal outcome, detailed guidelines as "Operating rules", the known-user-information section, numbered stages each with name, description, skip_conditions, failure_handling, and terminate_conditions, and a completion definition with terminal success and hard-stop failure conditions.
- The round planner is the orchestrating agent receiving full conversation state and deciding both sides' next actions, including whether and where an interruption occurs, conditioning two downstream simulators.
- Assistant planning rules require stage tracking, no early termination except on explicit repeated refusal with no realistic continuation, one action per concise turn, no re-stating known information or re-asking answered questions, and interruption-unaware full-content plans except filler-continuation rounds where `assistant_plan` is null.

## 18. [[wiki/18-user-simulation|User plan should reveal hidden info]]
**In one sentence:** The round planner forces `user_plan` to reveal hidden information gradually and plausibly through reactive, cutoff-grounded reactions — never verbatim confirmation, forward jumps, or state-machine leakage — with jointly consistent interruption timing and strictly isolated interruption types.
## Key points
- `user_plan` must reveal hidden info gradually and plausibly, with no verbatim confirmation: use "yes", "that's right", or shortened versions instead of repeating full details back.
- `user_plan` is reactive only (a reaction to what the assistant said, not an independent forward action) and must not jump ahead by volunteering information about a workflow step the assistant has not initiated.
- `user_plan` must not leak internal state: no references to internal stage names, workflow order, or KB details the user could not know.
- Interruption planning decides `will_include_interruption` from the interruption-profile probabilities, minima, and stats so far, and when true provides an `interruption_plan` with type and timing.
- The cut-in must be mid-thought during a key sentence that breaks stage progress — never in the last sentence, with sufficient remaining content after the cutoff — and the user plan must not depend on information from the unspoken remainder.
- Interruptions must be mid-stage (middle of executing a workflow stage, not at a clean boundary), pacing-driven (assistant says A then begins B, user cuts in to react to A), and cross-consistency-checked ("Given where I said the cutoff happens, has the user actually HEARD everything they act on in user_plan?").
- Each interruption type must be cleanly distinguishable with no blending of characteristics, and the round planner prompt includes detailed definitions for all six types (approximately 150 lines) specifying semantics, examples, and anti-patterns.
- User utterances can only reflect the truncated assistant portion with overlap times of 0.15–1.20 seconds (filler 0.15–0.50; impatient and correction 0.40–1.20), natural spoken dialogue with 1–3 mild imperfections per message, and JSON output with rationale, utterance, truncated_assistant_utterance, and overlap_time.

## 19. [[wiki/19-simulator-branches|User Simulator: The Normal Branch]]
**In one sentence:** The user simulator has interrupting and normal branches, where the normal branch omits interruption execution rules, truncation logic, and overlap time and produces only rationale and utterance.
## Key points
- The user simulator has two branches: the interrupting branch (when the round planner decided the user will interrupt) and the normal branch.
- The interrupting branch is substantially more complex because it must produce both the user's utterance and the exact truncation point in the assistant's message.
- The interrupting branch must also produce a realistic overlap time, in addition to the utterance and the truncated assistant utterance.
- The normal branch omits the interruption execution rules, truncation logic, and overlap time.
- The normal branch produces only rationale and utterance.
- Both branches share the same spoken dialogue requirements.
- Both branches share the rule that the user plan already encodes personality, and the simulator does not receive the raw user intent to prevent type contamination.

## 20. [[wiki/20-verification-modifier|Verification Modifier: Apply Only the Changes]]
**In one sentence:** The post-hoc modifier must apply only the targeted edit commands with minimal word changes while preserving TTS-friendly plain-text formatting and prefix invariants.
## Key points
- Apply only the changes described in the edit commands and do not rewrite, improve, or touch any untargeted message.
- Each edit command targets a specific message by index; modify only that message's content.
- Change as few words as possible to fix the described issue while preserving the rest exactly.
- If two edit commands target the same message, apply both changes.
- Maintain TTS-friendly formatting: numbers as words, currency spoken out, no markdown, no em dashes or semicolons.
- `modified_content` must be plain text only with no XML markup.
- `modified_original_content` is set if and only if modifying an interrupted assistant message, and then `modified_content` must be an exact prefix of `modified_original_content`.
- Do not proactively fix untargeted messages even if an edit creates downstream inconsistency; the verifier reruns and catches cascading issues next iteration, except mandatory filler-continuation coordination.

## The argument in five moves
1. Existing voice benchmarks measure interruption timing (whether the agent stops), leaving unmeasured the harder question of what the agent says next to recover a structured workflow.
2. IHBench operationalizes that question as post-interruption recovery across six interruption types with type-specific recovery rules, scored on task fulfillment and recovery quality via per-interruption rubrics fixed at construction time.
3. A controlled synthetic pipeline — state-machine workflows across 10 domains, round-planner-orchestrated mid-utterance cut-ins with strict grounding and type isolation, and a verify–modify loop — produces 45 conversations with 428 interruption points.
4. Evaluating 27 audio-language configurations shows wide spread on partially independent axes: closed-weight leaders on task fulfillment, Gemini 2.5 leaders on recovery quality, filler backchannels as the sharpest family differentiator, depth degradation concentrated in open-weight models, and an audio–text gap only for open-weight models.
5. Judge validation (second-judge ranking preservation, human-level agreement) plus the distinctness of recovery quality from AudioMultiChallenge establish recovery as a real, undertrained capability gap, qualified by synthetic English-only scope and a call for multilingual, live-interaction, timing-integrated, and training-signal extensions.
