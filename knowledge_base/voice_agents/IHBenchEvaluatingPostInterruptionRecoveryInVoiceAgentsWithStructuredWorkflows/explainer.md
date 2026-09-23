> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows — In Plain Language

## What is this about?

Imagine calling customer support and cutting in mid-sentence: "Actually, use my work email, not my home one."

A good voice agent should pause, accept the fix, and pick up exactly where it left off — without repeating everything or losing its place.

IHBench is a test that measures exactly that skill. It is called post-interruption recovery: what the agent says *after* you interrupt it.

The researchers built 45 scripted phone-call-style conversations across 10 business areas, with 428 interruptions planted in the middle of the agent's sentences.

They then tested 27 voice-AI setups from OpenAI, Google, and the open-source community to see which ones recover gracefully and which ones fall apart.

## Why does it matter?

Voice agents are moving into real jobs: scheduling clinic visits, handling insurance claims, managing accounts.

In those calls, interruptions are normal. People correct mistakes, say "mm-hm" while listening, get impatient, push back on requests, or suddenly change the subject.

Older tests only checked the easy part: does the agent stop talking when interrupted? That is like testing whether a driver hits the brakes, but never testing whether they can get back on the road.

IHBench shows the harder part is still broken, even in top models:

- Some models hear a harmless "mm-hm" and start their whole sentence over, or go silent, or say something new instead of simply continuing.
- Some ignore a correction ("use my work address") and keep using the old one.
- Open-source models get noticeably worse the longer the call goes on, losing track of the workflow step by step.

Finding these gaps gives builders a concrete list of behaviors to train and fix.

## How does it work?

Think of each test call as following a recipe card. The agent must work through ordered steps — verify identity, collect details, get consent, book the slot, confirm — and cannot skip ahead or invent facts.

A separate "director" program plants one interruption per test moment, right in the middle of a key sentence, never at a clean pause. There are six kinds:

- **Normal:** a plain question or comment in the flow of the task.
- **Filler:** a backchannel like "mm-hm" or "yeah" that changes nothing — the agent should just finish its sentence.
- **Impatient:** the caller rushes the agent ("just get on with it").
- **Correction:** the caller fixes an earlier detail ("my work email, not home").
- **Pushback:** the caller resists ("I'm not comfortable sharing that by phone").
- **Topic switch:** the caller raises something unrelated ("oh, and check my invoices?"), which must be handled before steering back.

Each interruption comes with its own small scorecard, written before any AI answers. Scoring has two sides:

1. **Task fulfillment:** which answer is better at moving the job forward (judged by comparing against a baseline).
2. **Recovery quality:** pass or fail — did the answer meet every rule on the scorecard for that interruption type?

An AI judge does the scoring, and the authors checked it two ways: a second judge from a different company ranked the models almost identically, and human reviewers agreed with the AI judge about as often as they agreed with each other.

## Where can this be used?

- **Customer-service bots:** handling corrections, impatience, and subject changes without restarting the whole script.
- **Healthcare and appointment scheduling:** keeping track of multi-step intake even when patients interrupt with worries or new questions.
- **Banking, insurance, and government helplines:** de-escalating pushback ("I don't want to share that") while offering alternatives and staying compliant.
- **Voice-assistant training:** using the per-interruption scorecards as training feedback so models learn to continue after "mm-hm," integrate corrections, and return from detours.
- **Buying and benchmarking decisions:** comparing voice models on recovery skill rather than just voice quality or speed of stopping.

## Conclusions & takeaways

- Stopping when interrupted is not enough. Resuming correctly — with the right facts and at the right step — is its own skill, and current tests missed it.
- No single model wins everywhere. One family leads at finishing tasks; another leads at polite, rule-following recovery. Builders must decide which matters more for their use case.
- Tiny backchannels are surprisingly revealing. How a model handles a simple "mm-hm" separates model families more sharply than harder interruptions do.
- Closed commercial models are more stable: they degrade about 3 times more slowly over long calls and work equally well from audio or text. Open models get worse with call length and do better from text than from real audio.
- Recovery skill is genuinely new: it barely overlaps with scores from an existing general voice benchmark, so it needs its own tests and training.
- Limits to keep in mind: the calls are scripted, English-only, and text-scored (tone of voice is not judged). Real-world, multilingual, live-call testing is still to come.

## Jargon decoder

| Term | What it means in plain language |
|------|----------------------------------|
| Post-interruption recovery | What the agent says and does after you cut in — fixing facts, keeping its place, and continuing sensibly. |
| State-machine workflow | A strict step-by-step recipe (step 1, then 2, then 3) the agent must follow without skipping or jumbling. |
| Barge-in | When the caller talks over the agent mid-sentence. |
| Backchannel / filler | A short listener sound ("mm-hm," "yeah," "right") that means "I'm listening," not "stop and do something new." |
| Task fulfillment (TF) | Did the agent move the job forward well? Measured by comparing its answer against a reference answer. |
| Recovery quality (RQ) | Did the agent handle this specific interruption cleanly? Pass only if it meets every rule on the scorecard. |
| Rubric | The small checklist of rules for one interruption (e.g., "accept the correction, use the new value, don't argue"). |
| LLM-as-judge | Using one AI to grade another AI's answers from the checklist. |
| Modality gap | The difference between hearing real audio versus reading a written transcript of the same call. |
| Conversation depth | How far into the call you are — later turns are harder because there is more history to remember. |
