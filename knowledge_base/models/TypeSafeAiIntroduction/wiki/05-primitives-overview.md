> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Primitives Overview

**In one sentence:** TypeSafe's three primitives — Choice (which option), Score (which level on a spectrum), Noul (is it true, 0–1) — are question/answer pairs evaluated independently and in parallel against the same state, with answers constrained to the supplied options so code can compose them directly.

## Key points

- Primitives come in pairs: a question defines one judgment for a System One model to make about a state, and its answer is the typed value that comes back, composed in code to make decisions.
- The three types are: Choice (which of these options — returns `choice`, `probabilities`, `confidence`), Score (which level — returns `score`, `legend`, `probabilities`, `confidence`), Noul (is this true — returns `noul`, 0 to 1).
- Every question has an ID (the response key, e.g. `refund_requested`), a `type` (`choice`/`score`/`noul`), `instructions` (the actual question), and `criteria` (options map for Choice, ordered levels for Score, optional yes/no clarification for Noul); question IDs are for code only and are not sent to the model.
- Choice fits unordered known options (ticket routing, document type, language detection, with an `other`/`none of the above` fallback); Score fits a describable spectrum (severity, frustration, skill level); Noul fits clean yes/no where the probability itself is the signal.
- Noul 0.5 means equal yes/no probability, not a medium level — so measure levels with Score (e.g. no experience → deep expertise) and reserve Noul for clearly defined conditions; prefer the type whose answer maps directly onto code (Choice → branches, Score → threshold, Noul → `if`).
- Every question in a request sees the same state and is evaluated independently in parallel, so adding questions barely changes response time and costs only the cheap extra question tokens; answers are constrained to the supplied options/levels, never outside values, and one answer never becomes hidden context for another.
- The shared request token budget is around 32,000 tokens (~150,000 characters of English) for state plus questions; when judgments genuinely depend on each other (fetching more data, building the next state, picking next options) make a second request, otherwise ask everything together and let code ignore unneeded answers (speculative fan-out).

---

## The three question types

| Type | What it answers | Returns |
|---|---|---|
| Choice | Which of these options? | `choice`, `probabilities`, `confidence` |
| Score | Which level? | `score`, `legend`, `probabilities`, `confidence` |
| Noul | Is this true? | `noul` (0 to 1) |

"You can ask one question or send several together. Every question in a request sees the same state, is evaluated independently, and returns a typed answer under the ID you chose."

## Ask for one snap judgment per question

"Ask for a judgment a knowledgeable person makes in a second given the right context. 'Does this message convey urgency?' is a good question. 'Analyze this message and determine the best course of action' is not." Multi-factor judgments split into one question per factor, weighted in code — e.g. instead of "rate this startup pitch", ask market size, technical feasibility, and differentiation, then weight them; when priorities shift, change the weights rather than rewriting a prompt.

## Define a question

- ID: the key you pick (e.g. `refund_requested`) identifying the answer in the response.
- `type`: one of `choice`, `score`, or `noul`.
- `instructions`: the question about the state — where the evaluation logic goes, written as a clear specific question or a statement to judge.
- `criteria`: possible answers — map of options (Choice), ordered levels (Score), optional yes/no description (Noul).

Example — asking whether a customer requested a refund:

```python
from typesafe_sdk import Noul

questions = {
    "refund_requested": Noul(
        instructions="Does the customer request a refund?",
    ),
}
```

Tip (verbatim): "Question IDs are for your code. They are not sent to the model. Write the complete question in `instructions`, even when the ID seems self-explanatory."

## Choose a question type

- **Choice:** one of a known set with no order — routing a ticket, classifying a document, detecting a language; give the full list and add `other`/`none of the above` when coverage is uncertain.
- **Score:** a position on a spectrum with describable points — bug severity, customer frustration, skill level; levels are user-defined and the model returns a position along them (possibly between two levels).
- **Noul:** a clean yes/no where the probability is the signal — bug report, refund request, resume mentioning distributed systems.

Note (verbatim rule): "Use Noul for a yes/no judgment and Score to measure a position on a spectrum... A Noul value of 0.5 means the model gives yes and no equal probability. It does not mean the candidate has a medium skill level." For skill level use a Score (no experience, some familiarity, daily use, deep expertise); for yes/no define the condition clearly. "If two types both seem to fit, prefer the one whose answer your code can act on directly. A Choice between `refund`, `rebook`, and `information` maps straight onto three code paths. A Score of customer frustration maps onto a threshold. A Noul maps onto an `if`."

## What comes back

| Type | Answer fields | How to read it |
|---|---|---|
| Choice | `choice`, `probabilities`, `confidence` | `choice` is the selected option; `probabilities` the distribution across every option; `confidence` summarizes how peaked it is. |
| Score | `score`, `legend`, `probabilities`, `confidence` | `score` is a position along the levels (can fall between two); `legend` repeats levels by number; `probabilities` the distribution across levels. |
| Noul | `noul` | Probability the answer is yes: near 1 strong yes, near 0 strong no, near 0.5 uncertain; no separate `confidence`. |

Composability properties: "Every answer is constrained to the options you supplied... never a value outside them. Your code never has to recover a value from generated prose." And: "Every answer is independent. One question's answer is not hidden context for another. You can add or remove questions without changing the others' results." Answers can be compared, thresholded, sorted, passed into logic, or put into a follow-up request's state.

## Reference specific fields

When the state is a JSON object (conversation, record, policy), name the relevant part in `instructions` with a dot-and-index path in backticks. Example against the State page's support conversation:

```python
questions = {
    "refund_requested": {
        "type": "noul",
        "instructions": "Does `ticket.messages[0].text` request a refund?",
    },
    "policy_supports_refund": {
        "type": "noul",
        "instructions": (
            "Does `refund_policy` support the refund requested "
            "in `ticket.messages[0].text`, given `order.charges`?"
        ),
    },
}
```

## Ask multiple questions together

"Send every question that uses the same state in one request... System One models evaluate every question in a request in parallel. Adding questions barely changes the response time and costs only the tokens for the extra questions, which are cheap. Asking a question you might not need is close to free." The parallel-questions cookbook reports batching 13 questions into one call as 11.5x cheaper and 9.6x faster than 13 separate calls, with no change in answers.

Speculative fan-out: "Ask every question your code might need, including ones whose answer only matters for some inputs, and let the code decide which answers to use." Token budget: "limited only by the request's token budget, which the state and the questions share... around 32,000 tokens, roughly 150,000 characters of English text."

Split complex judgments: one question per factor, combined and weighted in code (e.g. ticket priority from three Scores: bug severity, customer frustration, engineer actionability — the composite-scoring pattern). Dependent questions (second request needs the first answer to fetch data, build the state, or pick options) go in a second request; otherwise ask together and ignore unneeded answers — the exception cases are the skill-suggestion, structure-recovery, and hierarchical-classification cookbooks.

**Covers:** https://docs.typesafe.ai/primitives
