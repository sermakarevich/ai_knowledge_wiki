> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# System One

**In one sentence:** System One models (starting with TypeSafe's flagship Jev) make fast, structured decisions for software by evaluating a state and returning typed answers plus probabilities instead of generated text.

## Key points

- System One models are a class of AI models built to make fast, structured decisions that software can use directly: a System One model evaluates a state and returns typed answers and probabilities.
- Jev is TypeSafe's flagship model and the first System One model; like an LLM it understands natural-language input, but it returns typed decisions and probabilities rather than generated text.
- System One models are trained for calibrated decisions — probabilities optimized against outcomes to reflect uncertainty — where calibration is measured across groups of predictions and does not guarantee that an individual answer is correct.
- System One models do not write replies, produce code, or generate explanations of their reasoning; instead the user defines the possible answers through primitives (Choice, Score, Noul).
- Answers include confidence, so code can decide when to act and when to escalate to a person or a reasoning model.
- The refund-request workflow pattern is: build a state with the message, transactions, and policy; ask independent questions together (refund requested, duplicate-charge evidence, policy support); combine answers with deterministic checks in code, then route for action or review.
- System One is called through a client SDK or `POST /v1/systemone` in the HTTP API, where the `model` field selects the model; examples use `jev-latest`, which is also the SDK default.

---

## How it differs from an LLM

Verbatim framing: "Like an LLM, a System One model understands natural-language input. It returns typed decisions and probabilities rather than generated text."

Calibration claim (verbatim mechanism): "System One models are trained for calibrated decisions: their probabilities are optimized against outcomes to reflect uncertainty. Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct."

What System One does not do: "System One models do not write replies, produce code, or generate explanations of their reasoning. You define the possible answers through primitives."

| Primitive | Question | Example answer space | Example output |
|---|---|---|---|
| Choice | Which team should handle this ticket? | `billing`, `technical`, or `account` | `choice: "billing"` |
| Score | How frustrated is this customer? | 0 = calm, 1 = frustrated, 2 = very frustrated | `score: 1.4` |
| Noul | Does this message request a refund? | True or false | `noul: 0.95` |

Note from the source: these are illustrative configurations and values; the primitive pages describe the available configuration options and full response fields. The AI primer covers how System One models work and how they are trained.

Name origin (verbatim note): "The System One name comes from the concept Daniel Kahneman popularized in his book *Thinking, Fast and Slow*. System 1 thinking is fast and intuitive. System 2 is slower and more deliberate. Here, the emphasis is on fast, focused judgments."

## Fast judgments inside a larger workflow

For a refund request, the application can:

1. Build a state containing the customer's message, the relevant transactions, and the refund policy.
2. Ask independent questions together: whether a refund was requested, whether the evidence indicates a duplicate charge, and whether the policy supports a refund.
3. Combine the answers with deterministic checks in code, then route the case for action or review.

Mechanism claim: "Because System One models return typed, constrained outputs rather than free-form text, your code can inspect and combine its answers into predictable workflows." Answers also include confidence, "so you can decide when to act and when to escalate to a person or a reasoning model."

## Call a System One model

"Call a System One model through one of our client SDKs or `POST /v1/systemone` in the HTTP API. The `model` field selects which model handles the request. The examples in these docs use `jev-latest`, which is also the SDK default." Next: State (prepare the input) and Primitives / Questions (types of questions to ask).

**Covers:** https://docs.typesafe.ai/concepts/system-one
