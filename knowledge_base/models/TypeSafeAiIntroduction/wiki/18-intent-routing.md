> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Intent Routing

**In one sentence:** TypeSafe sits in front of all handlers as a fast, cheap classifier — one quick call determines intent and complexity, then code routes each request to deterministic logic, a specialist LLM, or a human, so expensive resources run only where needed.

## Key points

- Not every request needs the same handler: some need a database lookup, some an LLM with domain-specific context, some a human — TypeSafe classifies first as the fast, cheap front door.
- The customer-service example classifies two things at once: `intent` (Choice over order_status / product_question / return_exchange / complaint) and `complexity` (Score: simple lookup / needs judgment or multi-step / unusual, edge case, or escalation).
- If `intent.confidence < 0.5`, the ticket routes to a human agent because classification itself is too uncertain.
- `order_status` routes to deterministic code with no LLM involved; `product_question` and `return_exchange` each route to a different specialist LLM loaded with different context.
- `complaint` uses the complexity score as a second axis: `complexity.score > 1` (leaning toward "escalation needed") or `complexity.confidence < 0.5` routes to a human, otherwise a complaint-resolution LLM handles it.
- The page adds an explicit confidence check on the complexity score itself, noting it is always important to consider what a low confidence score means given the system and the stakes.
- TypeSafe handles the classification all in a single quick call; the expensive handlers only get invoked for the requests that actually need them.

---

## Example: customer service routing

Messages arrive and must reach the right handler. Rather than sending every message through an expensive LLM to determine its kind, the system classifies first and routes accordingly.

## Step 1: classify intent and complexity

- `intent` (choice) — "The primary intent of this customer message": order_status ("Asking about an existing order"), product_question ("Asking about a product before buying"), return_exchange ("Wants to return or exchange something"), complaint ("Unhappy with experience, wants resolution").
- `complexity` (score) — "How complex is this request to resolve": Simple lookup or standard procedure / Requires some judgment or multi-step process / Unusual situation, edge case, or escalation needed.

## Step 2: route to the optimal handler

```python
def route_ticket(ticket_id, response):
    intent = response.answers["intent"]
    complexity = response.answers["complexity"]

    if intent.confidence < 0.5:
        # If we don't have enough confidence to classify, route to a human agent
        return route_to_human_agent(ticket_id)

    if intent.choice == "order_status":
        handle_order_status(ticket_id)

    elif intent.choice == "product_question":
        handle_with_llm(ticket_id, PRODUCT_SPECIALIST)

    elif intent.choice == "return_exchange":
        handle_with_llm(ticket_id, RETURNS_SPECIALIST)

    elif intent.choice == "complaint":
        low_confidence = complexity.confidence < 0.5
        # A higher complexity.score leans toward the "escalation needed" end of the scale.
        if complexity.score > 1 or low_confidence:
            # Too complex for safe automation, or we're not sure about the complexity; route to a human.
            route_to_human_agent(ticket_id)
        else:
            handle_with_llm(ticket_id, COMPLAINT_RESOLUTION)
```

> "One intent routes to deterministic code with no LLM involved. Two route to different specialist LLMs, each loaded with different context. One uses the complexity score to decide between an LLM and a human. TypeSafe handles the classification all in a single quick call; the expensive resources only get invoked for the requests that actually need them."

**Covers:** https://docs.typesafe.ai/patterns/intent-routing
