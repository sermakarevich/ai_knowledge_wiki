> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Documentation Index — Introduction - TypeSafe AI

**In one sentence:** TypeSafe's Jev is a System One model that makes fast, structured decisions software can use directly, exposing three composable primitives (Choice, Score, Noul) evaluated in parallel against the same state instead of generating text to parse.

## Key points

- Large language models (LLMs) produce text for humans to read, so using them for code-consumed judgments means coercing text generation into structured decisions and parsing the results back.
- Jev is TypeSafe's flagship model and the first System One model, built to make fast, structured decisions that software can use directly.
- Jev evaluates typed questions against a state and returns structured results directly with no text generation and no parsing: typed values and probability distributions that code can branch on, sort by, and route with.
- TypeSafe exposes three modular, composable primitives: Choice (choose an option from a list), Score (score the state on a rubric), and Noul (is this statement true?).
- Choice returns choice, probabilities, confidence; Score returns score, probabilities, confidence; Noul returns noul (0–1).
- All three question types can be mixed in a single API call, with every question evaluated in parallel and in isolation against the same state in one go, so adding questions barely changes response time and does not create context-rot.
- System One models work best with atomic, well-scoped questions (a gut-check determination); multi-factor questions should be decomposed into separate questions and combined with logic in code, e.g. market size, technical feasibility, and differentiation instead of "rate this startup pitch".

---

## Documentation index pointer

The chunk's documentation index section points to a single discovery file:

- Fetch the complete documentation index at `/llms.txt`.
- Instruction: "Use this file to discover all available pages before exploring further."

## From text generation to structured decisions

Verbatim core claim from the chunk:

> "Large language models (LLMs) are designed to produce text for humans to read. When you need a model to make a judgment that your code will consume, that creates a mismatch: you are coercing a text-generation system into outputting structured decisions, then parsing the results back into something your code can depend on."

Counter-claim for Jev:

> "Jev is TypeSafe's flagship model and the first System One model. System One models are built to make fast, structured decisions that software can use directly. Jev evaluates typed questions against a state and returns structured results directly. No text generation, no parsing. You get typed values and probability distributions that your code can branch on, sort by, and route with."

## TypeSafe primitives

Chunk states: "TypeSafe exposes three AI primitives. Similar to software primitives, our AI primitives are modular, composable, structured, reliable, and fast. Each asks a different type of question and returns a different type of answer."

| Question type | Goal | Returns |
|---|---|---|
| Choice | Choose an option from a list | choice, probabilities, confidence |
| Score | Score the state on a rubric | score, probabilities, confidence |
| Noul | Is this statement true? | noul (0–1) |

Parallelism rule (verbatim mechanism): "All three question types can be mixed in a single API call. Every question is evaluated in parallel and in isolation against the same state in one go. Adding questions barely changes the response time. Each question is evaluated independently, so adding more questions does not create context-rot."

## Atomic questions, composed in code

Guidance from the chunk:

- "System One models work best when each question asks one specific, well-scoped thing."
- "Think of each question as a gut-check determination: the kind of judgment a highly knowledgeable person could make in a few seconds given the right context."
- "If the question you want to ask would require extended reasoning or weighs multiple independent factors, decompose it. Ask each factor as a separate question, then combine the results with logic in your code."
- "This keeps each individual evaluation reliable and gives you full control over how dimensions are weighted."
- Example: 'instead of "rate this startup pitch," ask separately about market size, technical feasibility, and differentiation. Combine the scores with your own formula. When priorities shift, change a coefficient in your code rather than rewriting a prompt.'

## Next steps

Links listed in the chunk:

- Quick Start — Everything you need to get started immediately.
- AI Primer — Why TypeSafe trains models for calibrated decisions instead of generated text.
- Primitives (Questions) — How to define questions, choose between Choice, Score, and Noul, and ask several at once.
- Confidence — How TypeSafe reports certainty, and how to use it architecturally.
- Patterns — Common patterns for building systems with TypeSafe.

**Covers:** Documentation Index through Next steps (Introduction - TypeSafe AI chunk 01-documentation-index)
