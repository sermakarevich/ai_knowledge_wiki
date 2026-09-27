> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# State

**In one sentence:** State is the content passed in the `state` field for the model to evaluate — one state per request against one or more independently-evaluated questions — structured as a string, object, or array with the facts kept separate from the judgment questions.

## Key points

- State is the content you ask a System One model to evaluate — a support message, a passage of text, or the current state of an application — passed in the `state` field alongside the questions to answer.
- Each request evaluates one state against one or more questions; all questions see the same state, are evaluated independently, and Choice, Score, and Noul questions can be mixed in one request.
- The simplest state is a plain string such as `"My card was charged twice."`; state can also be a JSON object or array with related context, examples, and other information that helps answer the questions.
- Think of state as the material presented to a panel of experts before asking them to make a judgment; in Python, pass the corresponding string, dictionary, or list directly to `client.system_one(state=...)`.
- Use an object for most requests so each part has a descriptive name and relationships stay clear; a string suits simple single-text use cases.
- The worked object example is one state containing a ticket (duplicate-charge subject plus customer/support messages), an order (id A-104 with two captured $49 charges), and a `refund_policy` string — related information is kept together when the decision requires comparing those parts.
- The state holds the content and supporting facts while questions define the judgments — e.g. keep the refund request and policy in the state, then ask whether the customer requested a refund and whether the policy supports it.

---

## State can be as simple as a string

Simplest form:

```python
state = "My card was charged twice."
```

Formats from the source:

| Format | Useful for | Example |
|---|---|---|
| String | A message, article, or passage | `"My card was charged twice."` |
| Object | Named fields, related records, or application state | `{"message": "My card was charged twice.", "order_id": "A-104"}` |
| Array | A sequence of messages or records | `["Hi", "My customer number is TS1337.", "My card was charged twice."]` |

Guidance (verbatim): "Use an object for most requests so each part of the state has a descriptive name and its relationships remain clear. A string is suitable when the use case is simple and requires only one piece of text."

Worked example — a support conversation as one state:

```json
{
  "ticket": {
    "subject": "Duplicate charge",
    "messages": [
      {"from": "customer", "text": "I was charged twice for order A-104. Please refund the duplicate."},
      {"from": "support", "text": "We are checking the charges."}
    ]
  },
  "order": {
    "id": "A-104",
    "charges": [
      {"amount_usd": 49, "status": "captured"},
      {"amount_usd": 49, "status": "captured"}
    ]
  },
  "refund_policy": "Duplicate charges are eligible for a refund."
}
```

"This object is one state, even though it contains a conversation, an order, and a policy. Put related information together when the decision requires comparing those parts."

## Separate content from questions

"The state contains the content and supporting facts. Questions define the judgments the model should make about that material. For example, keep the refund request and policy in the state, then ask whether the customer requested a refund and whether the policy supports it."

See Primitives (Questions) for instructions, criteria, question types, and asking several questions about one state; see the API reference for the request schema and client SDKs for installation, typed inputs, and response handling.

**Covers:** https://docs.typesafe.ai/concepts/state
