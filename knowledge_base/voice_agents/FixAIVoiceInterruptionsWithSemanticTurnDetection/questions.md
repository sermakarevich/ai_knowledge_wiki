---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Fix AI Voice Interruptions with Semantic Turn Detection

### Q1. Why does a voice agent that relies only on voice activity detection interrupt constantly?
> [!tip]- Answer
> VAD only spots human-patterned audio, so it hears any pause and assumes the speaker is done talking. Humans pause mid-sentence all the time to think, breathe, or change direction, so the agent starts answering at every single pause even mid-sentence. See [[wiki/01-semantic-turn-detection|The VAD-only interruption problem]].

### Q2. What question does semantic turn detection ask, and how does that differ from what VAD detects?
> [!tip]- Answer
> Semantic detection looks at the meaning of the sentence and asks whether it feels like a complete thought, rather than just detecting audible speech. VAD only decides that human-patterned audio is present, while the turn detector decides when the agent should speak versus stay quiet. See [[wiki/01-semantic-turn-detection|Semantic detection and its benefits]].

### Q3. What are the two headline benefits of waiting for complete thoughts, and what do they cost in latency?
> [!tip]- Answer
> Waiting for complete utterances instead of fragments reduces unwanted interruptions, described as the turn detector's most important job, and gives the speech-to-text engine full utterances that improve accuracy. The cost is minimal at only around 20 milliseconds of added latency. See [[wiki/01-semantic-turn-detection|Semantic detection and its benefits]].

### Q4. What are the three code-level steps for adding semantic turn detection to the agent session?
> [!tip]- Answer
> First add the turn-detector extra via `UV add lifekit agents turn detector`, which pulls in a multilingual model to reference in code. Then import the multilingual model from the turn-detector plugin and pass it into the agent session, after which the session emits turn events when the semantic model decides the speaker is finished. See [[wiki/01-semantic-turn-detection|Adding it to the agent session]].

### Q5. How did the post-fix live test demonstrate a more patient, natural agent?
> [!tip]- Answer
> Run via `uv run agent.py` in console mode, the agent waited through hesitant phrasing instead of jumping in at each pause. It also handled a mid-answer interruption and topic switch by acknowledging the change and answering the new question, such as the octopus and dolphin exchanges. See [[wiki/01-semantic-turn-detection|Live test: patient, natural conversation]].

### Q6. Which three best practices and test scenarios go with semantic turn detection in production?
> [!tip]- Answer
> Combine turn detection with VAD and noise control, use the multilingual semantic model to normalize different pause patterns across languages, and coordinate with preemptive generation so the LLM starts planning while waiting for a clear end of turn. Worth testing are rapid-fire short sentences versus one long sentence with pauses, background noise like a nearby TV, and mid-turn multilingual switching. See [[wiki/01-semantic-turn-detection|Best practices and test scenarios]].

### Q7. Evaluation: a team proposes dropping VAD and noise control and relying on the semantic turn detector alone to cut complexity — would you recommend this?
> [!tip]- Answer
> No, keep the layered setup because semantic detection judges thought completeness while VAD and noise control handle who is speaking and what is background interference. Dropping them risks the agent treating nearby TV chatter as user turns and reacting slower to real speech boundaries, so the small complexity saving is not worth the lost robustness. See [[wiki/01-semantic-turn-detection|Best practices and test scenarios]].
