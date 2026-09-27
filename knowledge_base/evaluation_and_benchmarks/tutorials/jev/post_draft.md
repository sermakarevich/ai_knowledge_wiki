# Notes on Jev (TypeSafe)

Jev is a model from TypeSafe. It does not generate text. It is a judge model, close in spirit to a classification model with a natural-language interface.

Input: a "state", a text or JSON description of the situation. This plays the role of features.
Output: a probability for each of a pre-defined set of outcomes, plus a confidence value.

You have to provide both parts yourself: the description of the state and the list of possible outcomes. Jev does not invent options. It only distributes probability over the options you gave it.

Three question types can be asked against one state:
- Choice: pick one option from a list (up to 255). Returns the chosen option, a probability per option, and a confidence.
- Score: rate the state on an ordered rubric of 2 to 10 described levels. Returns a score that may land between levels, the probabilities, and a confidence.
- Noul: is this statement true. Returns one number from 0 to 1. No confidence field, distance from 0.5 is the rough proxy.

Example workflow for a code bug: an LLM collects the context about the bug, an LLM brainstorms candidate fixes, both go into Jev as state and options, Jev returns a preference for each fix. The LLM proposes, Jev ranks. This shape fits directly into an RL loop, where Jev gives preferences over LLM-generated outputs for a given problem.

TypeSafe trains it with RLCD (reinforcement learning for calibrated decisions). Calibration means that among all answers tagged 0.8, about 80% are correct. This is a group property, any single answer can still be wrong.

Example from the documentation: resume screening. One Score question per skill dimension in a single call. The probability mass per level works as a proxy for expertise. The weights for combining dimensions live in your code, so "senior engineer" and "engineering manager" are two weightings of the same answers rather than two prompts.

Practical notes:
- Probabilities are normalized to sum to 1, so the model always picks something. Check the confidence field, or add an "other" / "none of the above" option so it can say nothing fits.
- Confidence is computed from the shape of the probability distribution. Peaked means sure, flat means guessing. The full distribution is returned, so you can define your own measure.
- Thresholds should depend on stakes. The docs use a 0.5 floor for handing off to a human and above 0.85 for a money transfer. Test thresholds on your own data.
- Extra questions in the same request are almost free. They run in parallel and the state is sent once. Ask every question you might need up front, then let your code pick which answers matter.
- Each question is judged independently against the state. Answers do not leak into each other.
- Request budget is about 32k tokens (roughly 150k characters) shared by state and questions.
- Describe rubric levels as situations, not degrees. "Broken, but a workaround exists" works better than "moderately severe".
- Latency is about 100 to 150 ms per call. Cost is around $0.04 per million input tokens.
- On TypeSafe's own 711-case dashboard Jev scores 67.8% aggregate against 74.1% for the best LLM comparator. The advantage is speed and cost, not accuracy.
- Pin the model version. jev-latest can change under thresholds you tuned.

Fits: triage, routing, ranking, guardrails, checking another model's output, bulk scoring over large datasets.
Does not fit: writing, explaining, planning, coupled multi-factor trade-offs that need shared reasoning.

Own test: a notebook that scanned 199 Python files of the fleet repo against the project's own coding rules, ranked files by refactor need, and built a prioritized backlog. About 30 seconds and about 2 cents.
