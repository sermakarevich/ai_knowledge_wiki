---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: SteerDuplex: Steerable Duplex Speech Dialogue Models

### Q1. What is SteerDuplex and what gap does it address?

> [!tip]- Answer
> > SteerDuplex is a Moshi-based full-duplex speech model that adds steerability: reliably shifting tone, persona, speaking rate, and voice style on user instruction. Full-duplex models already handled turn-taking, interruptions, and backchanneling, but steering along those attributes was underexplored. It combines natural/synthetic dialogue fine-tuning, two-stage RL with hybrid rewards, and the SteerBench benchmark. See [[wiki/01-steerduplex-overview|SteerDuplex Overview]].

### Q2. What are the three families of the paper's capability taxonomy, and how do they map to what/how speech dialogue does?

> [!tip]- Answer
> > The three families are natural-language steering (what the model says: requested content), acoustic understanding and adaptation (how it sounds: requested delivery grounded by audio references), and general duplex interaction (how it participates: pauses, interruptions, backchannels, floor management). Fluent turn-taking alone does not guarantee following instructions about tone, persona, or delivery. Steerability is defined as the reliable shift of behavior in response to user instructions. See [[wiki/02-capability-taxonomy|Capability Taxonomy]].

### Q3. What is SteerBench and what baseline gap motivated it?

> [!tip]- Answer
> > SteerBench has 390 spoken prompts combining concrete tasks with steering requests, assessed by 1,067 human-authored binary rubrics across tone, persona, style/accent, and speed/length, with separate text and audio rubrics plus fixed reference clips. Under matched items and the same judge, MOSHI and PERSONAPLEX reach audio-steering average pass rates of only 20.55% and 16.44%, respectively. Supervised SteerDuplex training raises audio-steering APR to 65.10 ± 1.13%. See [[wiki/02-capability-taxonomy|Capability Taxonomy]].

### Q4. How does the SteerDuplex architecture jointly generate audio and text?

> [!tip]- Answer
> > A masked system-prompt prefix conditions joint audio/text streams (user acoustic, user semantic, agent acoustic, agent semantic, agent text) with 300 s context and silent prefix audio, generating at 12.5 Hz. Temporal plus depth transformers predict text and 8 hierarchical RVQ audio codebooks, with waveform-validity checks for silence, clipping, and invalid audio. Policy loss covers text-stream actions only, including sampled padding tokens that encode pause/onset timing, with an adaptive sampled-action KL penalty instead of exact full-distribution KL. See [[wiki/03-architecture-training|Architecture and Training]].

### Q5. How does GDPO normalize rewards, and what do the two RL stages add?

> [!tip]- Answer
> > GDPO normalizes each reward component separately within a rollout group sharing one context before combining with weights, so raw scale cannot dominate and a constant component contributes no signal. Stage 1 (response continuity) starts from the SFT checkpoint as frozen KL reference and adds a continuity term (weight 0.5, 4-second first-response target) to discourage short timing-satisfying but non-sustained answers. Stage 2 re-initializes policy and KL reference from stage 1, retains continuity, and adds a continuation-duration bonus (weight 2.0, 4-second target) on noise and user-backchannel events with dedicated backchannel sampling. See [[wiki/03-architecture-training|Architecture and Training]].

### Q6. What were the headline RL gains on interruption response and pause handling?

> [!tip]- Answer
> > On source-clean FDB-v1.5, correct response after interruption rises from 72.5% to 82.5% with RL, and continuation after a user backchannel rises from 71.4% to 80.6%. On synthetic pause items, barge-in falls from 26.5% to 9% (−17.5 percentage points). On the synthetic interruption task, response rate rises from 96% to 97.7% while semantic score slips 3.94→3.88 and mean takeover latency grows by 40 ms. See [[wiki/04-rl-interruption-results|RL Interruption Results]].

### Q7. Why does the paper conclude that better response timing does not imply uniform improvement?

> [!tip]- Answer
> > Background-speech recovery is effectively flat (60%→59%) and recovery after speech directed elsewhere rises only 42%→48%, while semantic score and latency show mixed changes. The chunk states explicitly: "Thus better response timing does not imply uniform improvement in every interaction measure." Task compliance and floor management therefore need separate checks alongside timing. See [[wiki/04-rl-interruption-results|RL Interruption Results]].

### Q8. What is the silence shortcut in duplex timing rewards, and how does the design counter it?

> [!tip]- Answer
> > A silent model can earn interruption credit without ever yielding, so the design requires assistant speech before the interruption and adds continuity rewards encouraging sustained speech when the user has not taken the floor. In Figure 6 probes, promptness-only optimization attains scalar reward 0.670 but scores zero on the shared duplex diagnostic with 25 of 96 rollouts empty. Single-component text-only, audio-rubric-only, and audio-quality-only probes also collapse to 47, 41, and 41 empty rollouts. See [[wiki/05-reward-hacking|Reward Hacking]].

### Q9. What happens under continued optimization in RL stage 2, and what does it suggest?

> [!tip]- Answer
> > Interruption reward on natural development conversations rises from 0.450 to 0.793, but continuation after a user backchannel falls from 3.20 to 2.00 seconds (below the 2.60 s SFT reference) and noise-robustness reward declines from 1.96 to 0.77. The joint composite probe reaches duplex score 0.371 with 4 empty rollouts versus ≥26% empty for isolated probes, yet the conflict is reduced, not eliminated. Group normalization balances scales, but a component constant within a group supplies no gradient to resist other components, consistent with interference between interaction objectives. See [[wiki/05-reward-hacking|Reward Hacking]].

### Q10. What are the SFT and RL training settings and compute costs?

> [!tip]- Answer
> > SFT uses a Moshi-style 7B backbone on 80 H100 GPUs (batch 8/GPU, global batch 640) for a 3,600-step budget (2.304M draws), with the reported checkpoint at step 2,925 (1.872M draws). Both RL stages use component-normalized GDPO with RL lr 5×10−7, KL 0.05/target 0.01 (adaptive, min 0.02, bounded k3 estimator), clip 0.2/grad-clip 1.0, and continuity weight 0.5/target 4.0 s. Stage 1 ran ~5.08 h on four 8×H100 nodes (~162.7 GPU-h) and stage 2 ~4.01 h on one node (~32.1 GPU-h), excluding queueing, setup, benchmark, and hosted-model compute. See [[wiki/06-references|References and Training Appendix]].

### Q11. How do the Table 4 reward components and Table 5 retention results hang together?

> [!tip]- Answer
> > Pause, backchannel, noise-robustness/speech-mirror, and interruption yield plus recovery each carry weight 1.0, while turn timing (1.0) pairs with a Gemini 3.6 Flash transcript rubric judge (0.75); response continuity (0.5, 4.0 s target) and a stage-2 continuation bonus (2.0, 4 s) apply to specific event groups, with waveform integrity as hard validity and safety/capability held out. Retention deltas are small: AudioMC APR +0.74, STEERBENCH rubric pass +1.47, VoiceBench +0.51, FDB-v2 mean −0.003, interruption semantics −0.069. Controls differ in budget and configuration, so they do not isolate every reward component. See [[wiki/07-reward-components|Reward Components and Evaluation]].

### Q12. How does the text rubric judge (D.4) score a criterion?

> [!tip]- Answer
> > It scores exactly one criterion at a time on a three-level scale: "No Issues," "Minor Issues," or "Major Issues," explaining its decision before rating and outputting JSON with reasoning placed before the rating. It receives criterion metadata (title, category, type, weight, description) plus the latest user request and assistant transcript. Explicit criteria require direct answers while implicit ones may be inferred; objective means factual correctness, subjective means quality; it ignores weights, tolerates minor phrasing differences, and prioritizes content over delivery polish for speech. See [[wiki/08-text-rubric-judge|Text Rubric Judge]].

### Q13. How is SteerBench constructed, voiced, and scored?

> [!tip]- Answer
> > SteerBench has 100 tone, 136 persona, 104 style/accent, and 50 speed/length prompts, each recording identifiers, categories, topics, utterances, and audio/text rubrics pairing an axis with a binary criterion. User utterances are neutral conversational speech via Gemini 3.1 Flash TTS (24 kHz, mono, PCM16) with hash-stable voice assignment; reference scripts come from a text model (Gemini 3 Pro Preview, 3.1 Pro Preview repairs) and Kore/Schedar voices with human review. Text and audio criteria are judged separately with audio conditioned on the fixed reference; judge-error items are excluded from denominators, runs above 5% errors are invalid, and Audio APR, sample APR, and rubric pass rate aggregate differently. See [[wiki/09-audio-profile|Audio Profile]].

### Q14. Should a team deploying a voice assistant adopt SteerDuplex's full SFT-plus-two-stage-RL recipe as is?

> [!tip]- Answer
> > Adopt the SFT steering recipe confidently since it supplies the main steerability and task gains with broadly retained capabilities, but treat stage-2 RL as conditional: it improves interruption response and pause handling yet erodes continuation, shows judge sensitivity, and invites reward hacking. Gate adoption on conversation-event metrics (barge-in, continuation duration, empty-output rate) alongside aggregate scores, and keep continuity/continuation terms with waveform validity. Given CANDOR pause overlap and diagnostic-only source-clean probes, re-validate on held-out interaction data before shipping. See [[wiki/05-reward-hacking|Reward Hacking]].
