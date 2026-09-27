> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# API Reference

**In one sentence:** POST a `state` plus a caller-named map of typed `questions` to `https://api.typesafe.ai/v1/systemone` with model `jev-latest`, and get back structured `answers` keyed by the same ids plus token `usage`, with standard HTTP error codes and SDK-automatic retries on rate limits.

## Key points

- The evaluation endpoint is `POST https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <API_KEY>` and `Content-Type: application/json`; for a guided introduction the page defers to the primitives docs.
- Every request sends three required top-level fields: `state` (string, object, or array — text, chat logs, records, or app state), `model` (`"jev-latest"`, the flagship model), and `questions` (a map of typed Question objects under caller-chosen keys, with answers returned under the same keys).
- Question keys are not sent to the underlying model and are not used in inference — they are pure caller-side labels.
- The three question types share `type` and `instructions` and differ in `criteria`: Noul takes optional true/false meaning descriptions; Choice requires a map of option to rubric description (null allowed); Score requires an ordered array of at least two level descriptions and returns a probability-weighted value that can land between levels.
- Every answer carries the question's `type`; Choice answers return `choice` plus `probabilities` summing to 1 plus `confidence`; Score answers return `score` plus `legend` plus per-level `probabilities` plus `confidence`; Noul answers return `noul` on a 0–1 scale with no confidence field.
- Choice and Score `confidence` (0 to 1) is derived from the answer's probability distribution; the worked examples show choice confidence 0.82 and score confidence 0.78.
- Errors use standard HTTP codes with a JSON body: 401 for missing/invalid API key, 422 for body validation failures (missing field or malformed question, body names the field), 429 for rate limits, 529 for temporary overload.
- On 429 or 529, retry with exponential backoff rather than immediately; client SDKs handle this automatically under the default retry policy, so SDK users need no extra handling.

---

## Evaluation endpoint

```http
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

## Request body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `state` | string \| object \| array | yes | The content to evaluate — plain string for text, or structured data (object/array) for chat logs, records, or app state |
| `model` | string | yes | The model handling the request — use `"jev-latest"` |
| `questions` | map<string, Question> | yes | Typed questions under caller-chosen keys; answers come back under the same keys |

```json
{
  "state": "Help! My payouts have been failing for 3 days.",
  "model": "jev-latest",
  "questions": {
    "is_urgent": {
      "type": "noul",
      "instructions": "Does this convey urgency?"
    }
  }
}
```

## Question types

### Noul

A yes/no question returning the probability the answer is yes. Optional `criteria` describes what yes (near 1) and no (near 0) mean, e.g. true: "Explicitly time-sensitive", false: "No urgency expressed".

### Choice

Picks one option from a caller-defined set; returns the chosen option and the full probability distribution. `criteria` is a required map of option to rubric description (null when an option needs no detail), e.g. department over billing ("Payments, invoicing, refunds") / technical ("Bugs, outages, integrations") / sales ("Pricing, upgrades, new accounts").

### Score

Rates the state along a caller-defined rubric; returns a probability-weighted value across the levels. `criteria` is a required ordered array of level descriptions with at least two levels, e.g. frustration over ["Calm", "Frustrated", "Very angry"].

## Response body

| Field | Type | Required | Meaning |
|---|---|---|---|
| `model` | string | yes | The model that performed the evaluation |
| `answers` | map<string, Answer> | yes | One Answer per question, keyed by the same ids used in `questions` |
| `usage` | object | yes | Token usage: `input_tokens`, `output_tokens` (integers) |

```json
{
  "model": "jev-latest",
  "answers": {
    "is_urgent": {
      "type": "noul",
      "noul": 0.92
    }
  },
  "usage": { "input_tokens": 312, "output_tokens": 48 }
}
```

## Answer types

### Noul answer

`type: "noul"` plus `noul` (number, required): the yes/no answer on a 0 (no) to 1 (yes) scale.

### Choice answer

`type: "choice"` plus `choice` (highest-probability option), `probabilities` (every option mapped to a probability, summing to 1), and `confidence` (certainty derived from probabilities). Example: choice "technical" with billing 0.08 / technical 0.85 / sales 0.07 and confidence 0.82.

### Score answer

`type: "score"` plus `score` (probability-weighted value, can land between levels), `legend` (each level number mapped to its description), `probabilities` (each level as a string key mapped to a probability, summing to 1), and `confidence`. Example: score 1.6 with legend 0 = Calm / 1 = Frustrated / 2 = Very angry, probabilities 0.05 / 0.3 / 0.65, confidence 0.78.

## Errors

| Status | Meaning |
|---|---|
| `401 Unauthorized` | Missing or invalid API key — check the `Authorization` header |
| `422 Unprocessable Entity` | Body failed validation (e.g. missing required field, malformed question) — the body details the offending field |
| `429 Too Many Requests` | Rate limit exceeded — back off and retry after a short delay |
| `529 Overloaded` | Temporarily overloaded — retry after a short delay |

### Handling rate limits

On `429` or `529`, retry with exponential backoff instead of retrying immediately. Client SDKs handle this automatically, so no extra handling is needed when using an SDK with its default retry policy.

**Covers:** https://docs.typesafe.ai/api
