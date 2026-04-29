> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Policy & Guardrails

Policies enforce what the agent can and cannot do. Guardrails are the mechanisms that implement policies. This section covers input/output filtering, approval gates, and governance at scale.

### Four Types of Guardrails

**Input guardrails:** Reject obviously bad requests before they reach the model (saves cost, prevents abuse).

**Inline guardrails:** During generation, detect if the model is heading toward a policy violation and steer it away.

**Output guardrails:** Filter final output for policy violations, sensitive data, etc.

**Approval gates:** For high-stakes actions, pause and ask a human before proceeding.

### Policy Engine Pattern

Express rules as code:
```
if action == "refund" and amount > $1000:
  require_approval = true
if user.region == "EU":
  require_gdpr_compliance = true
if cost > user.daily_budget:
  reject = true
```

### Content Filtering

- Regional/regulatory compliance (GDPR, CCPA)
- Brand safety
- Secret detection and redaction
- Prompt injection detection
- PII and sensitive data filtering

### Approval Workflows

- Define approval criteria
- Route to right approvers
- Track approval chain
- Set timeout (auto-escalate if no approval in N hours)
- Immutable audit trail

### Interview Questions

- "Design an approval workflow for 'transfer funds > $10K.' What's the bottleneck?"
- "A user asks for PII about another user. How do you prevent the agent from answering?"
- "How do you detect and block a prompt injection attack?"

### Future Sections (To be expanded)

- Policy language design
- Rule evaluation engines
- Content filtering techniques
- Approval workflow orchestration
- Compliance integration
