---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows

### Q1. What is IHBench and what exactly does it measure?
> [!tip]- Answer
> IHBench (Interruption Handling Benchmark) evaluates post-interruption recovery: whether a voice agent resumes a state-machine-driven workflow at the correct step after a mid-utterance user interruption. It spans 10 enterprise domains with six interruption types injected at controlled points, and scores each of 27 audio-language model configurations on two axes, task fulfillment and recovery quality. See [[wiki/01-overview|IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows]].

### Q2. What gap in existing benchmarks motivates IHBench, and what must an agent do after being cut off?
> [!tip]- Answer
> Existing benchmarks (Full-Duplex-Bench, FLEXI, SID-Bench, HumDial) test only interruption timing — whether the model stops and yields — not what it says next. After a barge-in like a corrected address, the agent must stop, recognize the correction type, integrate the new value, avoid repeating already-heard content, and resume at the correct workflow step. See [[wiki/02-introduction|Introduction]].

### Q3. This pipeline page is mostly garbled OCR — what is the one reliable fact recoverable from it?
> [!tip]- Answer
> Only the Figure 2 caption is legible: the IHBench data-generation pipeline comprises prerequisites, conversation synthesis (with per-interruption rubrics), verification, and audio synthesis stages. The caption also states the rightmost panel shows one resulting evaluation sample and each stage is described in Section 3.3. See [[wiki/03-benchmark-design-overview|Prerequisites and Conversation Synthesis]].

### Q4. How does IHBench differ from prior voice, interruption, and synthetic-benchmark work?
> [!tip]- Answer
> Prior work either adds turn-taking without controlled interruptions (τ-voice), studies interruptions in text web-navigation agents (InterruptBench) or post-digression text dialogue, or builds multi-agent generation pipelines (MultiChallenge, SOTOPIA) with post-hoc evaluation questions. IHBench instead generates workflow-grounded conversations with controlled speech-native interruption points, fixes each item's per-interruption rubric at construction time before any model responds, and enforces state consistency with a verify–modify loop. See [[wiki/04-related-work|Related Work]].

### Q5. What are the six interruption types and what does correct recovery require for filler, correction, topic switch, and pushback?
> [!tip]- Answer
> The six types span cooperative (normal, filler) through directive (impatient, correction) to adversarial (pushback, topic switch) intents from real customer-service conversations. Filler backchannels ("mm-hm") require continuing the cut-off utterance exactly without repeating or acknowledging; correction requires accepting and integrating the new value; topic switch requires handling the new request then steering back without blending; pushback requires empathetic de-escalation with alternatives. See [[wiki/05-interruption-types|Interruption Types]].

### Q6. How was the 27-configuration evaluation run, and who leads on each of the two axes?
> [!tip]- Answer
> All 27 configurations (17 closed-weight, 10 open-weight) were judged by GPT-5.4-mini with high reasoning over three epochs each, with 95% CIs from a 1000-iteration bootstrap over N=428 epoch-averaged means. GPT Realtime 2 (medium, thinking) leads task fulfillment at .728±.03, while recovery quality peaks at Gemini 2.5 Flash thinking (.704±.04), showing the axes are partially independent; thinking helps Gemini's TF but not consistently RQ. See [[wiki/06-evaluation-methodology|GPT Realtime 2 (medium) — Overall Results (.728±.03 TF, .624±.04 RQ)]].

### Q7. What do judge agreement, depth degradation, and the AudioMultiChallenge comparison jointly establish?
> [!tip]- Answer
> A second judge (Gemini 3 Flash) preserves rankings (Spearman ρ 0.99 TF, 0.95 RQ; κ 0.75/0.70), and judge–human agreement matches human–human levels with conclusion rankings nearly identical (ρ 1.0 RQ, 0.90 TF). Task fulfillment degrades with conversation depth (mean slope −0.030/turn, p < 10−6), 3.3× faster for open-weight models, while IHBench RQ is the lowest-correlated axis (r̄ = 0.56) in the joint AMC matrix — a distinct capability. See [[wiki/07-overall-results|Overall Results: Per-Model Points, Judge Agreement, Depth, and Recovery Quality]].

### Q8. This judge-agreement page is garbled OCR — what is the only usable claim on it?
> [!tip]- Answer
> The body text carries no usable factual claims; only the Figure 4 caption (lines 39–40) is legible. It states the figure plots task-fulfillment win rate by conversation depth with a per-model logistic-regression slope on raw per-sample data, pooled across 26 audio configurations (excluding the TF baseline), with a significantly negative mean slope. See [[wiki/08-judge-agreement|Judge Agreement — Chunk Garbled (Only Figure 4 Caption Recoverable)]].

### Q9. What does the TOST equivalence analysis show about audio versus text-only input?
> [!tip]- Answer
> With margins Δ ∈ {0.02, 0.03, 0.05}, six Gemini configurations show audio and text statistically equivalent within ±0.02 on both metrics (TF diff −0.007, RQ diff −0.001), while nine open-weight configurations fail equivalence even at ±0.05, with text winning by ~8 TF points and ~6 RQ points (paired t-tests p < 10−26). Across all 15 dual-modality configurations audio never beats text; the text condition swaps transcripts for waveforms holding history, baseline, and judge fixed. See [[wiki/09-statistical-analysis|Statistical Analysis: TOST Equivalence and Audio vs Text Modality]].

### Q10. Evaluation: should a production voice-agent team adopt IHBench recovery quality as a ship gate, and what should it require first?
> [!tip]- Answer
> Adopt it as a diagnostic training signal, not a ship gate yet: RQ is validated (human-level judge agreement, second-judge ranking preservation) and measures a real gap uncaptured by general audio benchmarks, with filler handling and depth degradation as actionable targets. Before gating on it, require multilingual and live-interaction validation plus acoustic/prosodic scoring, since the current evidence is synthetic English-only with text-scored recovery and generator/judge-inherited rubric bias. See [[wiki/10-findings-discussion|Findings and Discussion: Post-Interruption Recovery as a Distinct Capability]].

### Q11. What literature does the reference span [17]–[50] cover?
> [!tip]- Answer
> The references cite audio models and foundations (Kimi-Audio, Whisper, Voxtral, GPT-4o/Realtime/5.4, Qwen-Omni, Mimo-audio, SpokenWOZ), the full-duplex evaluation family (Full-duplex-bench v1.5/v2/v3, INSTRUCT-FD, HumDial, MTR-DuplexBench), and dialogue-adjacent benchmarks (τ-voice, MultiChallenge, interruption detection, proactive agents). They also cover methods and statistics: Self-Instruct, WizardLM, BenchBuilder/Arena-hard, WildBench, LLM judges, SOTOPIA, TOST (Schuirmann 1987), and submodular benchmark selection. See [[wiki/11-references|References ([17]–[50])]].

### Q12. What is the IHBench dataset's scale, type mix, and turn distribution — and why is correction rare?
> [!tip]- Answer
> IHBench has 45 conversations across 10 domains with 428 interruption points (avg. 30.1 messages, range 19–40), seeded from 500 possible (domain, goal, intent) triples and filtered to 45 after the verify–modify loop. Pushback dominates (105, 24.5%) because the intent generator prefers challenging scenarios, while correction is rarest (25, 5.8% vs ~53 expected) since the planner skips corrections when no revisable prior-turn information exists. See [[wiki/12-dataset-statistics|Dataset statistics (Table 2)]].

### Q13. What do the human studies and per-type breakdown show about judge validity and the hardest interruption type?
> [!tip]- Answer
> In two studies with disjoint annotator pools (616 paired decisions each), human–judge agreement slightly exceeds inter-annotator agreement (κ 0.45–0.51 vs 0.43 TF; 0.41–0.44 vs 0.40 RQ), and human model rankings match the judge's (ρ 1.0 RQ, 0.90 TF with one adjacent near-tie swap). Filler backchannels are the hardest and most differentiating case (GPT family 0.07–0.31 vs Gemini 2.5's 0.62–0.68 with sharp Gemini 3.x regression), while normal and topic-switch interruptions are handled well across models. See [[wiki/13-audio-pipeline|Per-Type Recovery Breakdown and Audio-vs-Text Recovery Quality (Table 4, Figure 8)]].

### Q14. What does Figure 8 add on modality, and how was the AudioMultiChallenge comparison kept fair?
> [!tip]- Answer
> Figure 8 is the recovery-quality counterpart of the TF modality plot over the same 15 dual-modality configurations: Gemini stays within ±0.02 across audio and text while open-weight models score better on text, and no configuration has better RQ with audio. For the cross-benchmark analysis, all 27 configurations were re-run on AMC directly (rather than reusing reported numbers) with the official o4-mini judge, prompt, and schema, three epochs each to match IHBench protocol. See [[wiki/14-per-type-results|RQ Pass Rate our 27 model]].

### Q15. How is the Disaster Housing Assistance workflow structured, and what counts as success versus hard-stop failure?
> [!tip]- Answer
> Steps 4–8 assess access/safety needs and adult presence, explain inspection windows and collect 2–3 preferences, disclose contracted-inspector data sharing with mandatory explicit consent, book the earliest matching slot with a confirmation number, and read back the full summary with reference ID. Terminal success requires verified identity, confirmed address, access notes, in-policy availability, explicit consent, a booked slot with confirmation number, and a complete readback; hard-stop failure covers unverifiable identity after two attempts, refused consent, withdrawn application, or declined proceed. See [[wiki/15-workflow-structure|Workflow structure: stages, skip/failure and termination conditions]].

### Q16. What do the recovery rubrics enforce, and how do the two judge prompts differ?
> [!tip]- Answer
> Per-interruption rubrics enforce criteria like fresh start (begin a new utterance, never resume the cut-off sentence), non-defensive tone (no "we already told you" or blaming), and explicitly addressing the user's stated concern with a reason. The comparative Task Fulfillment judge picks winner A or B on the given criterion only, ignoring tone or length, while the absolute Recovery Quality judge returns PASS only if every listed criterion is met, adding none and penalizing nothing outside the list. See [[wiki/16-rubric-design|Rubric Design: Fresh Start, Tone, and Judge Prompts]].

### Q17. What are the key constraints on the assistant system-message template and the round planner?
> [!tip]- Answer
> The system message is a production-style template with exactly one placeholder, `{known_user_information}`, forbidding invented facts, with the assistant speaking first and driving a strict ordered workflow to a terminal outcome; call direction is goal-prefixed ([OUTBOUND] states the reason, [INBOUND] greets and starts the workflow after the user states their problem). The round planner orchestrates each round — one assistant turn plus one possibly-interrupting user turn — tracking stage, acting once per concise turn, and planning full unaware content except filler-continuation rounds where `assistant_plan` is null. See [[wiki/17-system-prompts|System Prompts: Assistant System-Message Template and Round Planner]].

### Q18. What rules keep the simulated user's hidden information, grounding, and interruption timing realistic?
> [!tip]- Answer
> The `user_plan` must reveal hidden information gradually and plausibly — reactive only, no verbatim confirmation, no volunteering unasked-for future-step details, and no leakage of stage names, workflow order, or KB internals. Cut-ins must land mid-stage and mid-thought on a key sentence with remaining content after the cutoff, pacing-driven (reacting to A while B begins), cross-checked so the user only acts on what was actually heard, with one cleanly isolated interruption type per round and overlap times of 0.15–1.20s. See [[wiki/18-user-simulation|User plan should reveal hidden info]].

### Q19. How do the user simulator's interrupting and normal branches differ?
> [!tip]- Answer
> The interrupting branch is substantially more complex: it must produce the user utterance plus the exact truncation point in the assistant's message and a realistic overlap time. The normal branch omits all interruption execution rules, truncation logic, and overlap time, producing only rationale and utterance. See [[wiki/19-simulator-branches|User Simulator: The Normal Branch]].

### Q20. What invariants must the verification modifier preserve when fixing conversations?
> [!tip]- Answer
> The modifier applies only the targeted edit commands with minimal word changes, touching nothing untargeted and leaving downstream inconsistencies for the verifier's next iteration (except mandatory filler-continuation coordination). It must keep TTS-friendly plain-text formatting (numbers as words, no markdown, no em dashes/semicolons, no XML markup), and when modifying an interrupted assistant message, `modified_content` must be an exact prefix of `modified_original_content`. See [[wiki/20-verification-modifier|Verification Modifier: Apply Only the Changes]].
