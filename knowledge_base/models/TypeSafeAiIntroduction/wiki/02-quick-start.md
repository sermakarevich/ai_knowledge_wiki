> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Quick Start

**In one sentence:** You can try TypeSafe in the Playground with pasted text and mixed Noul/Choice/Score questions, call it via POST to `https://api.typesafe.ai/v1/systemone` with model `jev-latest`, use the Python SDK (`typesafe-sdk`, Python >= 3.10), or install the TypeSafe agent skill for coding agents.

## Key points

- The Playground path is: open the Playground and log in, paste any text as the state, add a Noul question such as `"Does this message express urgency?"`, then mix Noul, Choice, and Score in one call and see all results at once.
- The sample state used throughout is: "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP."
- The HTTP API path is: get an API key from the dashboard, then make a POST request to `https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <API_KEY>` and `Content-Type: application/json`; full details are in the API Reference.
- The sample request body sends one state plus the `model` field (`jev-latest`) and a `questions` map with a Choice (department: billing/technical/sales), a Score (frustration over three levels), and a Noul (is_urgent).
- The sample response returns `choice: "technical"` with probabilities billing 0.159 / technical 0.84 / sales 0.001 and confidence 0.596; `score: 1.035` with confidence 0.842; `noul: 0.999`; and usage of 312 input tokens and 48 output tokens.
- The Python SDK path is: install with `pip install typesafe-sdk` (or `uv add typesafe-sdk`, requires Python >= 3.10), then call `client.system_one(state=..., questions={...})` with `Choice`, `Score`, `Noul` objects; the client reads `TYPESAFE_API_KEY` from the environment and calls `jev-latest` by default.
- The agent-skill path is: install via the Claude Code plugin (`claude plugin marketplace add typesafe-ai/skills`, then `claude plugin install typesafe@typesafe-ai`) or via `npx skills add typesafe-ai/skills --skill typesafe-ai` for other agents, then tell the coding agent to use the TypeSafe skill while building.

---

## Try it: the Playground

Steps from the source:

1. **Open the [Playground](https://console.typesafe.ai/playground)** and log in.
2. **Paste any text** as the state, e.g.:

```plaintext
Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP.
```

3. **Add a question** — try a Noul: `"Does this message express urgency?"`:

```json
{
  "urgency": {
    "type": "noul",
    "instructions": "Does this message express urgency?"
  }
}
```

4. **Add more questions** — mix Noul, Choice, and Score in one call and see all results at once.

## Call it: the API

1. **Get your API key** from the dashboard (`https://console.typesafe.ai/settings/keys`).
2. **Make a POST request** to the API endpoint:

```http
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

3. **Review the API Reference** for all the details.

### Sample cURL command

```bash
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
  {
    "state": "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP.",
    "model": "jev-latest",
    "questions": {
      "urgency": {
        "type": "noul",
        "instructions": "Does this message express urgency?"
      }
    }
  }
EOF
```

### Request body

Sends one state, `model: jev-latest`, and three questions (department Choice, frustration Score, is_urgent Noul):

```json
{
  "state": "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP.",
  "model": "jev-latest",
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle this",
      "criteria": {
        "billing": "Payment or subscription issues",
        "technical": "Bugs or integration problems",
        "sales": "Pricing or account questions"
      }
    },
    "frustration": {
      "type": "score",
      "instructions": "How frustrated the customer appears",
      "criteria": [
        "Calm, just stating facts",
        "Frustrated but civil",
        "Very angry, strong language"
      ]
    },
    "is_urgent": {
      "type": "noul",
      "instructions": "The message conveys urgency or time-sensitivity"
    }
  }
}
```

### Response body

| Question | Answer |
|---|---|
| department (choice) | `choice: "technical"`, probabilities billing 0.159 / technical 0.84 / sales 0.001, `confidence: 0.596` |
| frustration (score) | `score: 1.035`, legend 0 = Calm / 1 = Frustrated but civil / 2 = Very angry, `confidence: 0.842` |
| is_urgent (noul) | `noul: 0.999` |

Usage: `input_tokens: 312`, `output_tokens: 48`. Model: `jev-latest`.

## Code it: the Python SDK

1. **Install the SDK** (requires Python >= 3.10): `pip install typesafe-sdk` or `uv add typesafe-sdk`.
2. **Use the SDK** — the client reads `TYPESAFE_API_KEY` from the environment and calls `jev-latest` by default:

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

client = TypeSafeClient()

ticket = "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP."

response = client.system_one(
    state=ticket,
    questions={
        "department": Choice(
            instructions="Which team should handle this",
            criteria={
                "billing": "Payment or subscription issues",
                "technical": "Bugs or integration problems",
                "sales": "Pricing or account questions",
            },
        ),
        "frustration": Score(
            instructions="How frustrated the customer appears",
            criteria=[
                "Calm, just stating facts",
                "Frustrated but civil",
                "Very angry, strong language",
            ],
        ),
        "is_urgent": Noul(
            instructions="The message conveys urgency or time-sensitivity",
        ),
    },
)

print(response.answers["department"].choice)  # "technical"
print(response.answers["frustration"].score)  # 1.035
print(response.answers["is_urgent"].noul)     # 0.999
```

See the client SDKs page for installation options and detailed usage.

## Vibe it: the agent skill

1. **Install the TypeSafe skill** using the Claude Code plugin or `npx skills add typesafe-ai/skills --skill typesafe-ai`; the skill can also be read as SKILL.md on GitHub.
2. **Tell your coding agent** to use the TypeSafe skill as you build, e.g.:

```plaintext
Let's build a simple CLI that uses the TypeSafe API to evaluate a set of supplied documents on multiple dimensions. Use the TypeSafe skill to understand how to use the TypeSafe API and how to structure the system. Ask me questions about what kinds of documents I want to evaluate and on what dimensions.
```

See the Agent Skill page for more details.

**Covers:** https://docs.typesafe.ai/introduction/quickstart
