> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Introduction - TypeSafe AI — In Plain Language

## What is this about?

TypeSafe AI sells fast, structured machine judgments instead of chat text. Its flagship model Jev is called a System One model (a model built for fast, instinct-like decisions, borrowing the "fast vs. slow thinking" idea): you hand it a state (the information to judge — a ticket, message, or app snapshot) and it returns typed answers your code can use directly, with no text to parse.

The full docs cover three composable primitives (small building blocks you combine): Choice picks one option from a list, Score rates against an ordered scale, and Noul answers yes-or-no with a 0-to-1 number. Every question is evaluated in parallel and in isolation against the same state in one API (Application Programming Interface — the way your program calls the service) call. One request handles one state but any mix of questions, and the answers come back under the same names you gave them.

Beyond the primitives, the docs teach confidence-gated control flow, four composition patterns, a use-case map, a smart-home demo, the HTTP API plus Python/JavaScript SDKs (Software Development Kits — ready-made client libraries), and an agent skill that gives coding agents full TypeSafe context. A shared budget of around 32,000 tokens covers the state plus all questions together.

## Why does it matter?

Most teams today force LLMs (Large Language Models — AI trained to write text) into decision jobs: ask a question, get a paragraph, then parse structure back out of prose. That text round-trip is fragile — wording drifts, formats break, and one shared generation mixes all answers together.

TypeSafe bets large-scale automation is ~99% machine-to-machine, so the machine interface matters more than chat. Removing generation gives software-like properties: structured outputs, parallel evaluation with almost no extra latency (~100–150 ms), ~100× cheaper inference for bulk work, and calibrated probabilities (numbers tuned so that, across many calls, a 0.8 really happens ~80% of the time) trained with RLCD (reinforcement learning for calibrated decisions) instead of RLHF (human-preference tuning behind chatbots).

Three properties make the difference for everyday code:

- **No parsing:** answers arrive as JSON with fixed keys, so downstream code never guesses at wording.
- **Comparable:** scores sort, thresholds gate, and probabilities reveal close calls versus clear winners.
- **Observable:** every decision logs a distribution you can plot, test, and audit.

Control moves into reviewable code: weights, thresholds, and routing rules live as numbers and `if` statements, not hidden inside prompts you must rewrite. A refund workflow shows the shape: ask independent questions together (was a refund requested, is there duplicate-charge evidence, does the policy support it), combine the answers with deterministic checks in code, then route to action or human review.

## How does it work?

You POST a state plus a map of named questions to `https://api.typesafe.ai/v1/systemone` with model `jev-latest` (or call `client.system_one(...)` in the SDK, or click through the Playground). Each question has an ID (your label, not sent to the model), a type, instructions, and criteria (the options, levels, or yes/no meanings).

Choice returns the picked option plus a probability for every option and a 0-to-1 confidence (how sure the model is, derived from the spread). A Choice accepts up to 255 options at a few tokens each, so pass the full list of teams or categories rather than a shortlist, and add an `other` fallback for inputs the list may not cover. When two options get confused, describe each with a small structure — what it covers, what belongs to the neighbor instead, and examples — rather than a one-line label.

Score returns a fractional position (a probability-weighted mean that can land between levels), per-level probabilities, a legend mapping numbers to descriptions, and confidence. Scores take 2 to 10 levels: use as many as you can describe distinctly, keep each Score to one dimension, and describe situations rather than degrees ("workaround exists" beats "moderately severe"). Because different distributions can yield the same number, always read the probabilities and confidence alongside the score before rounding or ranking.

Noul returns a single `noul` number with no confidence field of its own; near 1 means yes, near 0 means no. Optional true/false criteria pin down subtle boundaries — for example, what exactly counts as a repeat contact — and are worth testing with and without.

Four rules make it reliable: keep each question atomic (one gut-check each; split "rate this pitch" into market, feasibility, differentiation); send only the relevant state, using JSON structure (objects, arrays, labeled keys) where it sharpens meaning; ask everything possibly relevant in one parallel call and let code ignore the rest (speculative fan-out); and gate every action on confidence with risk-scaled thresholds (e.g. floor 0.5 to act at all, 0.9+ for destructive moves, confirm in between).

Composition patterns do the rest: composite scoring normalizes per-dimension Scores to 0–1 and blends them with explicit weights; intent routing classifies first with the cheap model, then sends each request to deterministic code, a specialist LLM, or a human; confidence-gated routing treats the answer as *what* and confidence as *whether to act*.

Getting started is deliberately easy: try the Playground by pasting text as the state and mixing all three question types in one call, or install the Python SDK (`pip install typesafe-sdk`, Python 3.10+) and call `client.system_one(...)` with `Choice`, `Score`, and `Noul` objects. Coding agents get the same knowledge through the TypeSafe agent skill, installed via the Claude Code plugin or a one-line skills command, then invoked by naming the skill in a prompt.

Errors use standard HTTP codes — 401 for a bad key, 422 for a malformed question, 429/529 for rate limits and overload — and the SDKs retry the transient ones automatically with backoff.

## Where can this be used?

Anywhere code needs a fast typed signal inside a workflow it owns:

- **Background automation:** triage, routing, ranking, and gating steps that must run a million times with no human co-pilot — support tickets, refunds, moderation, recruiting, lead gen, insurance, legal, marketplaces.
- **Real-time decisions:** ~150 ms judgments embedded in games or UIs, faster than human perception.
- **Big-data map-reduce:** ~100× cheaper inference to search, classify, and extract features over giant corpuses, traces, and datasets.
- **Universal verification:** cheap checks over other AIs — jailbreaks, citation errors, hallucinations, bad tool calls, broken reasoning traces.
- **Harness engineering:** model routing, semantic retrieval, guardrails (safety checks), and trace classification at lightspeed.
- **The demo that ties it together:** the Smart Home Assistant evaluates every request against a long speculative question list in one call, splits compound commands with an LLM, and falls back to chat only for open-ended talk.
- **Everyday developer uses:** semantic code linting, model routing (which model should handle this?), support-ticket triage with frustration scoring, resume screening across weighted dimensions, and voice-banking intent checks that confirm before approving transfers.
- **Knowledge work:** search and retrieval ranking, feature extraction, forecasting, and knowledge-graph construction over large document sets.

## Conclusions & takeaways

- Text-writing AI is the wrong shape when code needs a decision; Jev returns typed values plus probabilities directly.
- Three primitives cover most judgments: Choice for options, Score for spectrums, Noul for yes-or-no — mixed freely in one parallel call.
- Reliability comes from atomic questions, minimal relevant state, and code-side composition — not clever mega-prompts.
- Confidence is a second axis: act when sure, confirm or escalate when not, with thresholds scaled to the stakes.
- The same four moves (fan-out, gated routing, composite scoring, intent routing) repeat across every industry in the use-case map.
- Control stays with you: shifting behavior means changing a weight or threshold in versioned code.
- Start in the Playground, graduate to the SDK, and scale through the API — the same question shapes work everywhere.
- Keep questions and thresholds as constants in one reviewable place; agents write poor questions, so edit them collaboratively.
- Measure on your own data: plot confidence against accuracy and set thresholds from evidence, not defaults.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| System One model | A model built for fast, instinct-like typed decisions rather than slow written reasoning. |
| State | The content you ask the model to judge, sent in the `state` field as a string, object, or array. |
| Choice / Score / Noul | The three question types: pick an option, rate on a scale, or answer yes-or-no as a 0–1 number. |
| Confidence | A 0-to-1 number (on Choice/Score) summarizing how concentrated the probabilities are; used to decide act vs. escalate. |
| Calibration | Whether stated probabilities match reality across many calls (0.8 happens ~80% of the time). |
| RLCD | TypeSafe's training method: rewards for calibrated decisions instead of chatty human-preferred text. |
| Speculative fan-out | Asking every possibly-relevant question in one parallel call and letting code ignore what it doesn't need. |
| Composite scoring | Blending several normalized per-dimension Scores with explicit weights set in code. |
| Intent routing | Classifying cheaply first, then sending each request to code, a specialist model, or a human. |
| Noul | A question type that answers "is this statement true?" with a number from 0 (false) to 1 (true); no separate confidence. |
| Probabilities | How likely each option or level is; concentrated means sure, spread out means uncertain — you are never locked into one confidence formula. |
| SDK / API | The client library (Python, JavaScript) and the HTTP endpoint your program uses to call TypeSafe. |
