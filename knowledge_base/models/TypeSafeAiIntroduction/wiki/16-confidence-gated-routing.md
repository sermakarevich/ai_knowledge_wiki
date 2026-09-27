> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Confidence-Gated Routing

**In one sentence:** Use confidence as a second axis alongside the answer — the answer tells you what, confidence tells you whether to act — gating each action at a threshold scaled to its risk.

## Key points

- Confidence is described as one of TypeSafe's most powerful features, and being intentional about gating decisions on it builds systems that are both reliable and safe.
- The core maxim is: "The answer tells you what; confidence tells you whether to act."
- The voice-banking example classifies intent with a Choice over `check_balance` (check an account balance), `approve_transfer` (approve a pending transfer), and `other`.
- A 0.6 confidence floor catches anything genuinely uncertain: below 0.6 on any action, the system routes to a human support agent.
- Low-stakes `check_balance` at or above 0.6 proceeds automatically (`show_balance`), because the worst case is the user hearing a balance read-out.
- High-stakes `approve_transfer` needs confidence above 0.85 to act automatically; at moderate confidence (0.6–0.85) the system asks the user to confirm ("Just to confirm: you would like to approve this transfer, is that correct?").
- The page defers to the Confidence page for more on how to think about confidence in systems.

---

## Example: voice banking commands

A voice banking interface lets users interact with their account verbally. Reasonable confidence in the interpreted intent is always wanted, but some actions are riskier than others and thus demand a higher confidence threshold.

## Step 1: determine the user's intent

A single Choice question: "What action is the user requesting?" over `check_balance` ("Check the balance of an account"), `approve_transfer` ("Approve the pending transfer request"), and `other` ("Something else").

## Step 2: confidence-gated routing

```python
action = response.answers["intent"]

# Below 0.6 confidence on any action, route to a human
if action.confidence < 0.6:
    route_to_support_agent(account_id)

elif action.choice == "check_balance":
    # Low stakes. 0.6 confidence is sufficient.
    show_balance(account_id)

elif action.choice == "approve_transfer":
    if action.confidence > 0.85:
        # High stakes, but high confidence. Safe to act automatically.
        approve_transfer(account_id)
    else:
        # High stakes, moderate confidence. Verify intent first.
        ask_user_to_confirm("Just to confirm: you would like to approve this transfer, is that correct?")

else:
    route_to_support_agent(account_id)
```

> "The 0.6 floor catches anything the model is genuinely uncertain about. Above that floor, each action type has its own threshold based on the consequences of acting on a wrong classification. Checking a balance at 0.6 is fine because the worst case is the user having to listen to the balance read-out. But approving a transfer requires very high confidence (>0.85), otherwise the system should ask the user to confirm."

**Covers:** https://docs.typesafe.ai/patterns/confidence-routing
