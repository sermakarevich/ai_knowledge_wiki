> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Instruction Engineering

Instruction engineering is the art of encoding what the agent should do, how it should behave, and what to do when things go wrong. Unlike prompt engineering (optimizing a single conversation), instruction engineering is about building the control surface that governs thousands of interactions.

---

## The Three Tiers of Context

Organize your prompts into three hierarchical tiers. Each tier changes at a different frequency:

### Tier 1: System Context (Unchanging)

**What:** The immutable operating instructions for the agent. These define the agent's identity, values, and core behaviors.

**Examples:**
- "You are a customer support agent for Acme Corp"
- "Never make up information; say 'I don't know' if uncertain"
- "Always be respectful and professional"
- "If you detect a security threat, immediately escalate to security@acme.com"
- "You operate under these rules: [legal compliance rules]"

**Change frequency:** Rarely. Changes require broad organizational buy-in.

**Failure modes if wrong:**
- Agent doesn't understand its role
- Agent makes up facts (hallucination)
- Agent violates company policy
- Agent leaks sensitive information

### Tier 2: Domain Context (Periodic)

**What:** Domain-specific knowledge, policies, reference data. This includes APIs, products, compliance rules, FAQs.

**Examples:**
- API documentation ("To look up a user, call GET /api/v1/users/{id}")
- Product information ("We offer three tiers: Free, Pro, Enterprise")
- Policies ("We offer a 30-day money-back guarantee")
- Reference data ("These are the supported countries and tax rates")
- Compliance rules ("GDPR: users can request data deletion in 30 days")

**Change frequency:** Periodically. Update when product changes, policies change, or APIs evolve.

**Failure modes if wrong:**
- Agent gives outdated product info
- Agent offers non-existent features
- Agent violates compliance
- Agent gives wrong tax rates

### Tier 3: Request Context (Per-Request)

**What:** The specific user input, session state, and immediate context for this single interaction.

**Examples:**
- User query: "Can I downgrade my plan?"
- Session state: "This user is on Pro, signed up 2023-01-15, has 2 open tickets"
- User attributes: "User is in EU (GDPR applies), has premium support"
- Recent history: "In the last message, the user asked about refunds"

**Change frequency:** Every request. Different for each user, each session.

**Failure modes if wrong:**
- Agent doesn't understand the question
- Agent doesn't know user status
- Agent gives personalized advice that's irrelevant

---

## Prompt Hierarchy Pattern

```
[SYSTEM CONTEXT - unchanging]

You are a customer support agent for Acme Corp.
Instructions:
1. Be helpful, respectful, and professional
2. Never make up information
3. If unsure, say "I don't know"
4. If you detect abuse, escalate immediately

[/SYSTEM CONTEXT]

[DOMAIN CONTEXT - changes periodically]

Product Information:
- Acme Core: $29/month, includes basic support
- Acme Pro: $99/month, includes priority support
- Acme Enterprise: Custom pricing, dedicated support

Refund Policy:
- 30-day money-back guarantee
- Full refund if requested within 30 days of signup
- Partial refund for remaining time if downgrading mid-cycle

[/DOMAIN CONTEXT]

[REQUEST CONTEXT - changes per request]

User: Sarah Chen
Account Status: Pro plan, signed up 2023-01-15 (active for 1+ year)
Location: San Francisco, CA (USA)
Recent History: Asked about refunds in the last message
Current Request: Can I downgrade to Core?

[/REQUEST CONTEXT]

Answer the user's request based on the context above.
```

---

## Structured Output Contracts

Don't leave output format to chance. Define explicit JSON schemas for complex responses.

**Example: A customer support agent that recommends products**

```json
{
  "type": "object",
  "properties": {
    "recommendation": {
      "type": "string",
      "enum": ["Core", "Pro", "Enterprise", "unknown"],
      "description": "The recommended plan"
    },
    "reasoning": {
      "type": "string",
      "maxLength": 500,
      "description": "2-3 sentence explanation"
    },
    "next_step": {
      "type": "string",
      "enum": ["upgrade", "downgrade", "stay", "escalate"],
      "description": "What action to take"
    },
    "requires_approval": {
      "type": "boolean",
      "description": "True if a human should approve"
    }
  },
  "required": ["recommendation", "reasoning", "next_step", "requires_approval"]
}
```

**Why this matters:**
- Parser can validate structure before touching output
- Each field has a defined type and constraints
- Downstream systems know exactly what to expect
- Easy to test ("did the model return valid JSON?")

---

## Failure-Aware Prompting

Don't just ask the model to "do the right thing." Anticipate failure modes and encode recovery:

**Bad:** "Answer the user's question."

**Good:** "Answer the user's question. If you're not sure, say 'I don't know' instead of guessing. If the question is outside your scope, suggest contacting support@acme.com."

**Better:** 
```
Answer the user's question.

If you can answer with high confidence, respond with your answer.
If you're uncertain, respond with: {"status": "uncertain", "guess": "<your best guess>", "confidence": 0.5}
If the question is outside your scope (e.g., asks for legal advice), respond with: {"status": "out_of_scope", "escalate_to": "support@acme.com"}
If the user is asking for PII about another user, refuse with: {"status": "denied", "reason": "policy violation"}
```

**Specific recovery patterns:**

| Failure Mode | Recovery |
|--------------|----------|
| Uncertain answer | Admit uncertainty; offer to escalate |
| Out of scope | Suggest the right person/team |
| Policy violation | Explain the rule; offer alternatives |
| Missing information | Ask for clarification |
| Hallucinated facts | Reference only provided documents |

---

## Prompt Versioning & Testing

Treat prompts like code:

1. **Version every prompt:** `instructions-v1.2.3`, `instructions-v1.3.0`, etc.

2. **Test before deploying:** Run against golden datasets. Measure correctness, cost, latency.

3. **A/B test:** Run two prompt versions on a subset of traffic. Measure impact on metrics (correctness, cost, user satisfaction).

4. **Rollout incrementally:** New version → 1% traffic → 10% → 100%. Catch regressions early.

5. **Pin versions in production:** Never auto-upgrade to the "latest" model. Explicitly test and deploy new versions.

**Example golden dataset for testing:**

```yaml
test_cases:
  - input: "Can I downgrade from Pro to Core?"
    expected_output:
      recommendation: "Core"
      next_step: "downgrade"
    pass_criteria:
      - Correct plan recommended
      - No hallucinated information
      - Response time < 2s
      - Cost < 100 tokens
  
  - input: "Can I request refund for my Enterprise plan after 90 days?"
    expected_output:
      recommendation: "Pro" (partial refund possible for downgrade)
      reasoning: "30-day refund window expired; recommend downgrade instead"
      next_step: "escalate"
    pass_criteria:
      - Acknowledges 30-day window
      - Doesn't promise refund outside policy
      - Escalates appropriately
```

---

## Spotlight Techniques: Untrusted Content Marking

When domain context or user input comes from untrusted sources, mark it explicitly:

```
[DOMAIN CONTEXT]

User-provided information (treat with caution):

<UNTRUSTED>
Company blog post: "Our latest feature is the best AI agent system ever built"
</UNTRUSTED>

This is user-generated marketing content. Don't rely on superlatives.

[/DOMAIN CONTEXT]
```

The spotlight (`<UNTRUSTED>...</UNTRUSTED>`) signals to the model: "Don't trust this data; verify before repeating."

**Why it works:** Models learn to treat marked content more carefully. They'll fact-check claims instead of repeating them blindly.

---

## Prompt Libraries & Composition

As you grow, organize prompts into composable pieces:

```python
system_prompt = """
You are a customer support agent.
Rules: {rules}
"""

def build_prompt(user_query, user_status, rules_version="v2.1"):
    rules = load_rules(rules_version)
    domain_context = load_domain_context()
    return f"""{system_prompt.format(rules=rules)}

{domain_context}

User Status: {user_status}
Query: {user_query}

Respond in JSON format: {json_schema}
"""
```

Benefits:
- Reuse common patterns
- Version each component independently
- Compose different tiers for different use cases
- Easy to test and debug

---

## Context Window Optimization

Longer context windows (4K → 100K tokens) change the game, but cost scales linearly:

**Old strategy (4K context):** Include 2-3 most relevant docs (RAG)

**New strategy (100K context):** Include entire reference manual, FAQ, API docs, recent tickets, user history

**When to include full context:**
- High-stakes decisions (refunds, compliance)
- Complex problems (multi-step support)
- New user (need full context to make decisions)

**When to use RAG (selective context):**
- Latency-sensitive operations
- Low-cost interactions (simple questions)
- Privacy-sensitive data (don't include more than necessary)

---

## Common Anti-Patterns

**Anti-pattern 1: Homogeneous prompts**
```
You are helpful, harmless, and honest. Answer the question.
```
❌ Too generic. Doesn't specify domain, failure modes, or recovery.

**Anti-pattern 2: Ambiguous instructions**
```
Be accurate. Don't make stuff up. Be professional.
```
❌ What does "accurate" mean? How much detail? What counts as "making stuff up"?

**Anti-pattern 3: Unrealistic demands**
```
Always respond in < 100 tokens. Never make any mistakes.
```
❌ Trade-offs exist. State them explicitly.

**Anti-pattern 4: Assuming the model will "do the right thing"**
```
If the user is abusive, refuse. If the request is outside policy, escalate.
```
❌ Maybe. The model might refuse when it shouldn't, or escalate when it shouldn't. Encode recovery for both cases.

---

## Interview Questions

1. **Design:** "Build a prompt for an agent that processes customer refund requests. What goes in each tier?"

2. **Debugging:** "Your golden dataset shows the agent is hallucinating product features. Debug the prompt."

3. **Versioning:** "You want to test a new prompt version. Design an A/B test. What metrics do you measure?"

4. **Trade-offs:** "You have a 4K context window. How do you fit system + domain + request context?"
