> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# MatthewCYM/VoiceBench — In Plain Language

## What is this about?

VoiceBench is a test suite for voice assistants.
That means AI systems you talk to out loud instead of typing to.

Most AI tests hand the model written text.
VoiceBench instead hands it spoken instructions.
These are audio clips made with computer voices (Google text-to-speech)
or recorded by real people.
It then checks how well the assistant answers.

The collection covers 11 mini-tests:

- open chat questions,
- multiple-choice quizzes,
- questions with a known correct answer,
- multi-turn conversations,
- following detailed instructions,
- step-by-step reasoning,
- and safety (refusing harmful requests).

Sizes range from 46 conversations up to about 3,000 quiz questions.
Alongside the datasets there is a public leaderboard, a paper,
and ready-made code that runs the whole evaluation.

## Why does it matter?

Talking is harder than typing.
Speech adds background noise, accents, and misheard words.
It also adds pressure to answer quickly.
A text-only test never sees any of that.

Without a shared spoken test, every team measures its voice assistant differently.
One team uses its own recordings, another uses its own graders.
So results cannot be compared.

VoiceBench gives everyone the same recordings,
the same questions, and the same scoring steps.
That matters because voice assistants are moving into cars, phones, and homes.
A common yardstick helps builders spot real progress,
catch regressions after updates, and compare approaches fairly.

## How does it work?

The process has three steps: get answers, judge the tricky ones,
then compute final scores.

**Step 1 — Get the assistant's answers.**
A script called `main.py` loads one of the 11 datasets from Hugging Face.
It plays each spoken question to your assistant,
or hands it the written version for comparison.
Every answer is saved to a results file.
You pick the model, the mini-test, and whether to test
by ear (`audio`) or by reading (`text`).
There is also a speed-test mode that warms the model up first
and then measures how fast it starts responding.

**Step 2 — Let a judge grade the open-ended answers.**
For four of the mini-tests (casual chat and reference-based questions),
there is no single right answer.
So a second script, `api_judge.py`, asks a helper AI to grade each answer.
Chat answers get a 1-to-5 quality score.
Answers with a known reference get a simple Yes or No.
Each answer is graded three times to smooth out randomness,
and the scores are saved alongside it.
The other seven mini-tests skip this step entirely,
because they have exact answers or rules a computer can check directly.

**Step 3 — Compute the final score.**
A third script, `evaluate.py`, reads the answers
(and judge scores, where used).
It applies the right scoring rule for that mini-test:
averaging judge scores for chat,
checking exact answers for quizzes,
checking rule-following for instructions,
and measuring harmfulness for safety tests.
The final score is printed to the log.
To keep results reproducible, the project pins its setup:
Python 3.10 with fixed versions of PyTorch, audio tools, and AI libraries.

## Where can this be used?

- **Comparing voice assistants:** run rival models on the same recordings
  and see which one handles speech best.
- **Testing speech vs. text:** run the same questions as audio and as text
  to measure how much accuracy is lost when the model must listen.
- **Checking specific skills:** quiz knowledge, multi-turn memory,
  careful instruction-following, math-style reasoning,
  or refusal of dangerous requests.
- **Tracking progress over time:** re-run the suite after each model update
  and watch the leaderboard-style scores move.
- **Speed testing:** a special mode measures how fast the assistant
  starts responding to speech, which matters for natural conversation.
- **Spotting weak spots:** find out whether your model fails at hearing,
  at reasoning, at following instructions, or at staying safe —
  and fix the right part.

## Conclusions & takeaways

VoiceBench turns "does my voice assistant sound good?"
into something measurable.
The recipe is fixed spoken questions plus a fixed three-step scoring pipeline.

Its strength is breadth.
One suite covers chatting, quizzes, instructions, reasoning, and safety,
in both synthetic and human voices.
Its main limitation is cost and subjectivity:
the open-ended parts rely on a paid helper AI as judge,
so those scores depend partly on that judge's taste.

For anyone building or choosing a voice assistant,
it is a practical starting point.
Run the scripts, get comparable numbers,
and know where your model is strong or weak
when people talk instead of type.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Benchmark / test suite | A fixed set of questions plus scoring rules, so different models can be compared fairly. |
| Voice assistant | An AI that listens to speech and answers out loud, like a smart speaker. |
| Modality (audio vs. text) | Whether the model receives the question as a sound clip or as written words. |
| Subset | One mini-test inside the larger collection, e.g. quizzes or safety questions. |
| Text-to-speech (TTS) | Software that turns written sentences into artificial spoken audio. |
| Reference answer | The known-correct answer used to check the assistant's reply. |
| Judge model | A second AI asked to grade answers that have no single right answer. |
| Open-ended QA | Chat-style questions where many different answers can be good. |
| Multiple-choice QA | Quiz questions where the model picks one option from a list. |
| Instruction following | Obeying detailed formatting or content rules, like "answer in three bullet points". |
| Reasoning task | A puzzle or multi-step problem that needs working through, not just recall. |
| Safety test | Checks that the assistant refuses harmful or disallowed requests. |
