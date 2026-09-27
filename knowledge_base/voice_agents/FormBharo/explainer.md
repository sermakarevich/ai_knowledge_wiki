> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# FormBharo: Designing and Evaluating a Voice Agent for Conversational Form Filling in Rural India — In Plain Language

## What is this about?

FormBharo — Hindi for "fill the form" — is a voice agent that fills in an enrollment form over an ordinary phone call.

The caller just talks. There is nothing to read, type, or install. The agent asks one question at a time in Hindi, listens to the answer, writes it into the right box on the form, and moves on to the next question. The agent always speaks first, reassures the caller that her details stay safe, and closes with a clear ending message.

It was built for a concrete pilot: signing up low-income, Hindi-speaking mothers in rural Maharashtra for free maternal and child health care, together with the nonprofit ARMMAN. The form covers about 12 fields — name, district, clinic name, whether the caller is pregnant, pregnancy duration or the child's name and birth date, phone numbers, and the last four digits of the national ID.

The big claim is not just the agent itself but how it was tested. The team released FormVoiceAgentBench: 380 real human recordings turned into 960 simulated phone calls and 3,760 multi-turn tests, covering transcription, understanding answers, asking the next question, and completing the whole form.

The headline result: clean lab transcripts make every modern AI look near-perfect, but real noisy phone speech cuts form completion by up to about 41 percentage points. Testing single parts in isolation does not predict whether the whole call succeeds — only end-to-end testing does. That gap is the reason the paper pairs every component score with a full-call score.

## Why does it matter?

In India, almost every social benefit starts with a form. Yet more than half of women in the poorest households cannot read at all, so paper forms and apps lock out exactly the people who need help most.

Today the gap is filled by frontline health workers who enroll families one conversation at a time. That work is caring but slow: workers juggle dozens of overlapping registers, apps, and paper records, retyping the same data, which caps enrollment at staff capacity rather than need.

Voice calls are a natural fix. Earlier programs showed the reach: the Kilkari voice-message service passed 10 million subscribers and over a million calls a day, and carefully designed speech interfaces beat touch-tone keypads even for literate users. A spoken call needs no literacy, no data plan, and no new device.

But filling a form by voice is much harder than playing a recorded message. Callers hesitate, correct themselves mid-sentence, mix Hindi and English, say phone numbers and dates in many different ways, and call from noisy rooms over crackly phone lines. One misunderstood answer can send the agent down the wrong branch of questions. FormBharo is an attempt to make that fragile process reliable and cheap enough to run at scale.

## How does it work?

Think of FormBharo as a careful assembly line with six stations per turn:

1. **Listen for silence.** A voice-activity detector notices the caller stopped speaking.
2. **Write down what was heard.** A speech-to-text model transcribes the audio.
3. **Pull out the facts.** An EXTRACT language model reads the transcript plus the conversation so far and pulls out every field the caller just answered — so already-answered questions are never repeated. It also drafts a short "got it" acknowledgement to mask waiting time.
4. **Check with strict rules.** A rule-based layer — no AI guessing here — validates each value: is the phone number 10 digits, is the date in the past, is the name long enough? Bad or missing answers trigger a re-ask, up to a per-field retry limit. Saying "I don't know" on an optional field skips it cleanly.
5. **Pick the next question by rule.** Branching stays deterministic: gestational age is asked only if the caller said she is pregnant, child details only otherwise. The decision is handed to the reply model as an instruction.
6. **Speak naturally.** A REPLY language model phrases the chosen question in friendly Hindi, and a text-to-speech voice reads it aloud. If the caller interrupts, the current turn stops immediately and the agent listens again.

The design motto is: use AI only where it adds value — understanding messy speech and phrasing natural questions — and keep validation, retries, branching, and question order as predictable rules.

Model choice was equally disciplined. No single model won on accuracy, speed, and cost at once, so the team threw out anything too slow or too weak, kept the Pareto-optimal options (the ones where you cannot improve one goal without hurting another), and ranked them with a weighted score reflecting deployment priorities. Winners: Scribe v2 for transcription, Gemini 3.5 Flash for extraction, GPT-5.4-mini for replies.

Testing mirrored real life. Five fictional mothers with tricky names, districts from outside the pilot state, and many ways of saying numbers were recorded by five native Hindi-speaking women under four conditions each: a quiet ideal take, background chatter, random near-or-far microphone distance, and random fast-or-slow pace. Supervisors checked every clip.

Scoring was strict too. Exact answers such as phone numbers needed an exact match, while open-ended names and short acknowledgements were graded by a calibrated AI judge that accepts spelling variants of the same spoken name. Each reply was checked on five points: the right question, Hindi language, one question only, no extra acknowledgement, and no reading the private value back aloud.

## Where can this be used?

The direct use is maternal and child health enrollment: a mother calls a number, answers spoken questions, and gets connected to free checkups and health information without paperwork or a smartphone.

The same pattern fits any benefit that starts with a form and serves low-literacy callers: immunization drives, nutrition programs, clinic registration, farm subsidies, ration cards, or ID-linked services where only basic details are collected by phone.

It also offers a template for builders: the hybrid recipe (AI for understanding and phrasing, rules for validation and flow), the retry-and-skip discipline per field, and the benchmark method (human audio plus unit tests plus chained end-to-end calls) can be reused for other languages, forms, and helplines.

Because only the last four digits of the national ID are collected and the benchmark uses fictional callers, the approach shows how to evaluate with realistic speech without exposing anyone's real personal data.

A failed required answer ends the call as incomplete rather than guessing, while a failed optional answer is simply skipped — so partial progress is preserved instead of forcing a bad entry. Mid-call progress notes ("only 3 questions left") keep the caller oriented.

Small courtesies matter on a long call: the agent's short spoken acknowledgement covers the pause while the next question is prepared.

## Conclusions & takeaways

- Real speech breaks lab-perfect AI: form completion fell up to ~41 points on noisy transcripts versus clean ones, and whole-form scores fell further than single-answer scores because small errors pile up across turns.
- Strict rules rescue small models: normalizing answers (for example, fixing a number returned as text) let cheaper models match or beat flagship models end to end.
- Part scores mislead: the best model at reading one clean answer was not the best at finishing the whole call, so buy decisions need full-call testing, not leaderboard snapshots.
- Measure what matters for speech: classic word-error rate picked the wrong transcription winner; a meaning-aware score plus downstream form accuracy picked Scribe v2.
- Cost and speed decide deployment: with tight phone-call budgets, the winning setup balanced accuracy against per-turn latency and price rather than chasing the top accuracy number alone.
- Share the test, not just the model: the openly released benchmark lets other teams repeat the same noisy-call evaluation for new languages and forms.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Voice agent | A program that holds a spoken phone conversation: it listens, decides what to ask next, and talks back. |
| EXTRACT | The AI step that reads what the caller just said and copies the facts into the right form boxes. |
| REPLY | The AI step that turns "ask question 4 next" into a natural spoken Hindi sentence. |
| Speech-to-text (STT) | Software that converts recorded voice into written words. |
| Text-to-speech (TTS) | Software that converts a written sentence into a spoken voice. |
| Form state | The master copy of the form so far — which boxes are filled and which still need answers. |
| Branching | Follow-up questions that depend on an earlier answer, e.g. pregnancy duration only if pregnant. |
| Retry / skip / end | If an answer is invalid, re-ask a few times; then either skip that box or end the call as incomplete. |
| LLM-as-a-judge | Using one AI with a strict rubric to grade another AI's answer, e.g. whether two name spellings match. |
| Pareto-optimal / weighted-sum | A fair way to pick a winner when no option is best at everything: keep the best trade-offs, then score accuracy, speed, and cost by importance. |
