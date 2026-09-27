> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Speculative Fan-Out

**In one sentence:** Because TypeSafe evaluates many questions in a single API call in parallel with typically no added latency, put every question the system might need — including speculative ones — into one request and let code ignore what's irrelevant after the fact.

## Key points

- All questions in one call are evaluated in parallel, so adding more questions to a call typically doesn't add any latency to the response.
- The recommendation is explicit: put all of the questions the system needs in a single request, then use code to decide what is relevant after the fact.
- Speculative questions are ones asked before knowing whether they're relevant — e.g. `bug_severity` and `has_reproducible_steps` only matter if the ticket is a bug report, `refund_requested` only matters for billing — included upfront because there is no speed cost.
- The triage example classifies a ticket's category (Choice: bug_report / billing / feature_request / account) while speculatively scoring bug severity, checking for reproducible steps (Noul), checking refund requests (Noul), and scoring frustration (Score).
- Routing thresholds from the example code: escalate to engineering when `bug_severity.score > 1.5 and has_reproducible_steps.noul > 0.6`; route billing with a refund flag when `refund_requested.noul > 0.7`; flag for priority response when `frustration.score > 1.5`.
- If the ticket turns out to be a feature request, the bug-severity result is simply ignored by the code path — speculative questions save a round trip when relevant and cost nothing when not.
- Everything needed for the full decision tree comes from one call instead of chaining a category call followed by a severity follow-up call.

---

## Example: support ticket triage

A support system must triage tickets: classify the ticket into a category, and if it's a bug report, also determine severity. Instead of asking for the category first and then severity in a follow-up call, both are asked at the same time; if the ticket is not a bug report, the bug-severity result is ignored.

## Step 1: speculative fan-out

Example state: "Hi, I placed an order (#98423) last Thursday and was charged twice. I also can't log in after the site update, and adding Apple Pay would be really helpful. This is getting frustrating."

Questions asked together:

- `category` (choice) — "Determine the broad category of this support ticket": bug_report ("reporting something broken or producing errors"), billing ("Charges, invoices, refunds, subscriptions"), feature_request ("requesting new functionality"), account ("Login, permissions, profile, security").
- `bug_severity` (score) — "How severe is the reported issue": Cosmetic / Broken or degraded feature with workaround / Blocking issue with no workaround.
- `has_reproducible_steps` (noul) — "The user describes specific steps to reproduce the issue".
- `refund_requested` (noul) — "The user is explicitly asking for a refund or credit".
- `frustration` (score) — "How frustrated the user appears": Calm, matter-of-fact / Frustrated but civil / Very angry.

> "Speculative questions: `bug_severity` and `has_reproducible_steps` only matter if the ticket is a bug report. `refund_requested` only matters for billing. We include all upfront because there is no speed cost for additional questions. If the ticket turns out to be a feature request, the bug severity result will be irrelevant, in which case your code path simply ignores it."

## Step 2: route with code

```python
category = response.answers["category"]
bug_severity = response.answers["bug_severity"]
bug_repro = response.answers["has_reproducible_steps"]
refund = response.answers["refund_requested"]
frustration = response.answers["frustration"]

if category.choice == "bug_report":
    if bug_severity.score > 1.5 and bug_repro.noul > 0.6:
        escalate_to_engineering(ticket_id, severity="high")
    else:
        add_to_bug_backlog(ticket_id)

elif category.choice == "billing":
    if refund.noul > 0.7:
        route_to_billing_with_flag(ticket_id, refund_likely=True)
    else:
        route_to_billing(ticket_id)

elif category.choice == "feature_request":
    log_feature_request(ticket_id)

# Frustration is useful regardless of category
if frustration.score > 1.5:
    flag_for_priority_response(ticket_id)
```

**Covers:** https://docs.typesafe.ai/patterns/fan-out
