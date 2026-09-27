> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Choice

**In one sentence:** A Choice picks one option from a fixed set and returns the selected option plus a full probability distribution and confidence, so code can route, threshold, and fan out on typed values instead of parsing text.

## Key points

- Use a Choice when the answer is one of a fixed set of options (which team handles a ticket, which product category, which programming language); if the answer is a position on a spectrum use a Score, and if it is yes-or-no use a Noul.
- A Choice answer is the selected option in `choice`, a probability for every option in `probabilities` (summing to 1), and a `confidence` value from 0 to 1 computed from how spread the distribution is.
- A Choice accepts up to 255 options at a few tokens each, so pass the full list of teams, categories, or products rather than a shortlist, and add an `other` or `none of the above` option when the list may not cover every input.
- Ask every Choice the code might need in a single request instead of one request per question: questions are evaluated in parallel, adding questions barely changes response time, and the code can ignore answers it does not need (extra questions still cost tokens).
- Speculative questions are cheap and safe: ask follow-ups that only matter conditionally (e.g. `return_reason`, `shipping_issue`), then let ordinary `if` statements use or ignore each answer based on the top-level result.
- Low confidence is a reason to ask rather than act: the reference triage code sends tickets with `department` confidence below 0.3 to manual triage, notifies any second team with probability above 0.25, and asks the customer what they want when `requested_resolution` confidence is below 0.5.
- When two options are confused, describe each with a structured object (`what` it covers, `not_for` what belongs to the neighbor, `examples`) instead of a one-line string; field names are not part of the API and none are reserved.

---

## Definition and when to use it

Verbatim definition from the source:

> "A Choice is a System One question type for selecting one option from a defined set. The answer includes the selected option, a probability for each option, and confidence."

Selection rule from the source: "Use a Choice when the answer is one of a fixed set of options. For example, which team handles a ticket, which category a product belongs to, or which language a code snippet is written in. If the answer is a position on a spectrum, use a [Score](/primitives/score). If it's a yes or no, use a [Noul](/primitives/noul)."

Example questions from the source:

```
"What programming language is this code written in"
  → options: python, javascript, typescript, go, rust, other

"What type of meeting is this based on the title and description"
  → options: standup, planning, retrospective, one on one, brainstorm, none of the above

"Which product category does this item belong to"
  → options: electronics, clothing, home garden, food and beverage
```

## Request structure

The POST request body to the TypeSafe API has three top-level fields: `state` (the content to evaluate), `model`, and `questions` (a map from question ids you choose to question objects). Each Choice question has:

| Field | Value |
|---|---|
| `type` | Always `"choice"` |
| `instructions` | The question the model answers |
| `criteria` | The answer options, as a map: each key is an option name, each value its description |

Reference request: state `'My running shoes arrived in the wrong size. Can I swap them for a size 10?'`, model `jev-latest`, question id `department` with instructions `'Which team should handle this?'` and criteria `returns` ('Exchanges, refunds, wrong or damaged items'), `shipping` ('Delivery status, delays, lost packages'), `billing` ('Charges, invoices, payment problems').

Rules from the source:

- "You choose the question id, `department` in this case. The answer is returned under the same id. The model never sees the question id."
- "The option names and their descriptions are both sent to the model, so write descriptions that separate the options from each other."
- Call via the `system_one` method or the `https://api.typesafe.ai/v1/systemone` endpoint; the `model` field selects the model. Typed questions exist in the client SDKs (Python `Choice`); a coding agent doing the integration should first install the TypeSafe agent skill so it knows the request and response shapes.

## Response structure

Response to the reference request (`usage`: `input_tokens` 330, `output_tokens` 34):

```json
{
  "model": "jev-latest",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "returns",
      "confidence": 1.0,
      "probabilities": { "shipping": 0.0, "returns": 1.0, "billing": 0.0 }
    }
  }
}
```

Besides `type`, each Choice answer has three values:

- `choice`: the option with the highest probability.
- `probabilities`: the full distribution across every option; the values sum to 1.
- `confidence`: a number from 0 to 1 computed from how `probabilities` is spread — "A flat shape, with probability spread across several options, means low confidence. A single peak on one option means high confidence."

"This ticket is an easy one, so all of the probability is on `returns` and confidence is 1.0. A ticket that mentions a wrong size and a missing refund would split probability between `returns` and `billing`, and confidence would drop."

## Good practice: ask more than one question per call

"Ask every Choice your code might need in a single request rather than one request per question. Questions are evaluated in parallel. Adding questions barely changes the response time, and the code can ignore answers it doesn't need. Extra questions still cost tokens."

Option-list guidance: "A Choice accepts up to 255 options, and adding options costs a few tokens each, so give the model the full list of teams, categories, or products rather than a shortlist. Add an `other` or `none of the above` option when the list might not cover every input, so the model can say none of the others fit."

For deep hierarchies or large taxonomies, "chain Choice questions level by level. The [Hierarchical Classification cookbook](/cookbooks/hierarchical_classification) shows how to run a beam search over Choice probabilities, keeping the best `K` candidate paths at each level instead of committing to a single greedy path."

## A more complex example: five Choices in one call

State: `'Shoes arrived two weeks late and in the wrong size. Also I see two charges on my card. What are you going to do about this?'` — five Choice questions: `department`, `return_reason`, `shipping_issue`, `requested_resolution`, `tone` (the last uses `null` descriptions because the option names `calm` / `frustrated` / `angry` are clear on their own). Two questions are speculative: `return_reason` only matters if `department` is `returns`, `shipping_issue` only if it is `shipping`.

Response (`usage`: `input_tokens` 588, `output_tokens` 212):

| Question | `choice` | `confidence` | Key probabilities |
|---|---|---|---|
| `department` | returns | 0.39 | returns 0.6, billing 0.38, shipping 0.02 |
| `return_reason` | wrong_size | 1.0 | wrong_size 1.0, rest 0.0 |
| `shipping_issue` | delayed | 0.53 | delayed 0.63, other 0.37, rest 0.0 |
| `requested_resolution` | exchange | 0.16 | exchange 0.37, refund 0.29, replacement 0.24, information 0.1 |
| `tone` | frustrated | 0.88 | frustrated 0.92, angry 0.08, calm 0.0 |

Per-question reading from the source:

- `department` is `returns` at 0.60 but `billing` holds 0.38 because of the double charge, lowering confidence to 0.39: "The top option is clear enough to act on, but the second option is not noise."
- `return_reason` is `wrong_size` at confidence 1.0 — "expected because it says this clearly in the ticket."
- `shipping_issue` splits `delayed`/`other`; it is speculative and `department` did not come back as shipping, so the code ignores it.
- `requested_resolution` confidence is 0.16 "because of the flat probability distribution of the answers. This is because the customer didn't say what they want."
- `tone` is `frustrated` at 0.92 probability, 0.88 confidence.

The reference triage code then: sends to manual triage if `department` confidence is below 0.3; assigns returns/shipping (with the sub-issue) or billing; notifies any second team with probability above 0.25 (here billing gets a copy); asks the customer what they want when `requested_resolution` confidence is below 0.5; flags senior agents only when tone is `angry`. Result for this ticket: returns team with issue `wrong_size`, billing gets a copy, customer is asked what they want, `shipping_issue` unused.

"One request, five answers, and the routing logic is ordinary `if` statements. If you later need to know the customer's language, or which product the ticket is about, add another Choice to `TRIAGE_QUESTIONS`; the request count stays at one." The smart home assistant demo likewise "evaluates every user request against a long list of Choice questions in one call ... Most of those questions are irrelevant to any one request and the code ignores them."

## Structured instructions and criteria

"Start with a one-line description per option. When two options are similar and the model keeps confusing them, describe each one with an object instead of a string. Give it fields for what the option covers, what belongs to a neighboring option instead, and a few example inputs."

Worked case: options `return_policy` vs `return_status` on state `'I sent the shoes back a week ago. When do I get my money?'`, with instructions object `{question, focus}` and per-option `{what, not_for, examples}` — response is `return_status` at confidence 1.0 (`usage`: `input_tokens` 407, `output_tokens` 32).

"The field names `question`, `focus`, `what`, `not_for`, and `examples` are not part of the API, and none are reserved. You choose them, the same way you choose option names. The model sees the names along with the values, so use short names that label what follows."

**Covers:** https://docs.typesafe.ai/primitives/choice
