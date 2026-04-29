> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Tool Calling & Model Context Protocol (MCP)

Tool calling is how agents take actions. The Model Context Protocol (MCP) is the emerging standard for composing tools across different agents and systems. This layer is the control surface that transforms a stateless model into a capable, composable agent.

---

## The Trust Ladder: Validating Tool Calls

Before any model-generated code reaches an action, it must pass through the trust ladder. Each rung filters out a class of failures.

```
Request comes in
    ↓
[Rung 1] Input validation: Is the parsed JSON well-formed?
    ↓
[Rung 2] Schema enforcement: Does it match the declared function schema?
    ↓
[Rung 3] Permission checks: Is this user/org allowed to do this?
    ↓
[Rung 4] Sandboxing: Can we safely execute this in isolation?
    ↓
Action executes
    ↓
Tool returns result
    ↓
[Return to model with result]
```

**Example: Transfer Funds**

```python
# Rung 1: Input validation
request = """{"action": "transfer", "amount": "100", "to_user": "alice"}"""
try:
    parsed = json.loads(request)  # Fails if malformed JSON
except JSONDecodeError:
    return error("Invalid JSON")

# Rung 2: Schema enforcement
schema = {
    "properties": {
        "action": {"enum": ["transfer"]},
        "amount": {"type": "number", "minimum": 0, "maximum": 1000000},
        "to_user": {"type": "string", "pattern": "^[a-z0-9_]+$"}
    },
    "required": ["action", "amount", "to_user"]
}
validator = Draft7Validator(schema)
if not validator.is_valid(parsed):
    return error(f"Schema violation: {validator.iter_errors(parsed)}")

# Rung 3: Permission checks
if not user_can_transfer(current_user, to_user=parsed["to_user"]):
    return error(f"Permission denied: cannot transfer to {parsed['to_user']}")
if parsed["amount"] > current_user.daily_limit:
    return error(f"Amount exceeds daily limit: ${current_user.daily_limit}")

# Rung 4: Sandboxing
with isolated_sandbox(timeout=5s, max_disk=100MB):
    result = execute_transfer(current_user, parsed["to_user"], parsed["amount"])

return result
```

---

## Function Schemas: Explicit Contracts

Never let the model guess. Define explicit schemas for every tool.

**Example: Customer lookup**

```json
{
  "name": "lookup_customer",
  "description": "Look up a customer by email or ID",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Email address or customer ID (e.g., 'cust_12345' or 'alice@acme.com')"
      },
      "fields": {
        "type": "array",
        "items": {"type": "string"},
        "enum": ["name", "email", "plan", "signup_date", "ltv"],
        "description": "Which fields to return (defaults to all)"
      }
    },
    "required": ["query"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string"},
      "name": {"type": "string"},
      "email": {"type": "string"},
      "plan": {"enum": ["free", "pro", "enterprise"]},
      "signup_date": {"type": "string", "format": "date"},
      "ltv": {"type": "number", "description": "Lifetime value in USD"}
    }
  }
}
```

**Why every field matters:**

| Field | Purpose |
|-------|---------|
| `name` | Tool identifier; used in logs and traces |
| `description` | Tells the model what the tool does; models use this to decide when to call it |
| `parameters` | What inputs the tool accepts; model uses to construct valid calls |
| `returns` | What the tool outputs; model uses to parse and reason about the result |

---

## Input Validation Beyond Schema

A valid schema doesn't mean a safe request. Add semantic validation:

```python
def lookup_customer(query: str, fields: List[str] = None) -> dict:
    # Schema validation happens before this function
    # Now add semantic validation
    
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")
    
    if "@" in query:
        # Treat as email
        if not is_valid_email(query):
            raise ValueError(f"Invalid email format: {query}")
        customer = db.find_by_email(query)
    else:
        # Treat as ID
        if not query.startswith("cust_"):
            raise ValueError(f"Invalid customer ID format: {query}")
        customer = db.find_by_id(query)
    
    if not customer:
        raise NotFound(f"Customer not found: {query}")
    
    if fields:
        # Requested fields must be in the schema
        allowed_fields = {"name", "email", "plan", "signup_date", "ltv"}
        invalid = set(fields) - allowed_fields
        if invalid:
            raise ValueError(f"Invalid fields: {invalid}")
        return {k: customer[k] for k in fields}
    
    return customer
```

---

## Read vs. Write Separation

Segregate read-only queries from actions with side effects. They have different properties:

| Property | Reads | Writes |
|----------|-------|--------|
| **Cache-safe?** | Yes; can cache results | No; caching breaks semantics |
| **Retry-safe?** | Yes; retrying is idempotent | Only if idempotent (use idempotency keys) |
| **Batch-safe?** | Yes; can batch requests | Only for certain operations |
| **Cost-critical?** | Sometimes (if high volume) | Always (writes have side effects) |
| **Audit-critical?** | Less | Yes; need immutable audit log |

**Example tool set:**

```json
{
  "read_tools": [
    "lookup_customer",
    "list_transactions",
    "get_account_balance"
  ],
  "write_tools": [
    "transfer_funds",
    "create_support_ticket",
    "send_email"
  ],
  "admin_tools": [
    "refund_transaction",
    "disable_account"
  ]
}
```

Routes to tools:
- Read tools → Fast path, low latency, cache-safe
- Write tools → Slow path, requires idempotency key, audit logging
- Admin tools → Approval gate, double-confirmation, immutable audit log

---

## Idempotency & Retries

Write tools must be idempotent. Use idempotency keys:

```python
@app.post("/transfer")
def transfer_funds(request: TransferRequest, idempotency_key: str):
    # Check if we've seen this key before
    cached_result = idempotency_cache.get(idempotency_key)
    if cached_result:
        return cached_result
    
    # New request; execute
    result = execute_transfer(
        from_account=request.from_account,
        to_account=request.to_account,
        amount=request.amount
    )
    
    # Cache the result
    idempotency_cache.set(idempotency_key, result)
    
    return result
```

**How it works:**
1. Client generates a unique `idempotency_key` (UUID)
2. Sends request with the key
3. Server checks cache; if found, returns cached result
4. If not found, executes transfer and caches result
5. Client retries with same key → server returns cached result (no double-transfer)

---

## Error Messages for LLM Consumption

Return error messages that guide the model to recovery, not just report failure:

**Bad:**
```json
{"error": "404", "message": "User not found"}
```
The model might retry the same query indefinitely.

**Good:**
```json
{
  "error": "not_found",
  "message": "User with ID 'cust_xyz' not found",
  "recovery": "Try searching by email instead with lookup_customer(query='user@acme.com')"
}
```

The model understands what went wrong and what to try next.

**Better:**
```json
{
  "error": "not_found",
  "message": "User with ID 'cust_xyz' not found",
  "suggestion": "Did you mean 'cust_xyza'? Exact matches: ['cust_xyza', 'cust_xyzb']"
}
```

The model can try a suggestion.

---

## Tool Result Formatting

Return structured data, not prose:

**Bad:**
```json
{"result": "Customer Alice has a Pro plan and has spent $500 lifetime."}
```
The model must parse prose.

**Good:**
```json
{
  "customer_id": "cust_alice",
  "name": "Alice",
  "plan": "pro",
  "lifetime_value": 500
}
```
The model can access each field directly.

---

## Model Context Protocol (MCP)

MCP is a standard for composing tools (servers) with agents (clients).

### Architecture

```
┌──────────────┐
│   Agent      │ (Client)
│ (Claude, etc)│
└──────┬───────┘
       │
     [MCP]
       │
┌──────┴───────┐
│ Tool Server 1│ (e.g., customer DB)
│ Tool Server 2│ (e.g., email service)
│ Tool Server 3│ (e.g., payment API)
└──────────────┘
```

### Key Concepts

**Clients (Agents):** Invoke tools. Examples: Claude, a local agent, a multi-step orchestrator.

**Servers (Tools):** Implement actions. Examples: a customer database wrapper, an email service, a payment processor.

**Transports:** How clients and servers communicate:
- **Stdio:** The server runs as a subprocess; communication via stdin/stdout
- **HTTP/WebSocket:** Traditional server; client makes HTTP requests
- **SSE:** Unidirectional server-sent events for streaming

**Capability discovery:** The client queries the server: "What tools do you have?"

```json
{
  "tools": [
    {
      "name": "lookup_customer",
      "description": "...",
      "parameters": {...}
    },
    ...
  ]
}
```

### Composition Example

```
Agent (Claude)
    ↓
MCP Server: Customer DB
    ├─ lookup_customer
    ├─ list_transactions
    └─ create_ticket

MCP Server: Email Service
    ├─ send_email
    └─ schedule_email

MCP Server: Payment API
    ├─ transfer_funds
    └─ get_balance
```

Agent can:
1. Look up a customer (Server 1)
2. Check their balance (Server 3)
3. Send them a confirmation email (Server 2)

All via the standard MCP protocol. No custom integration code.

### Why MCP Matters

1. **Decoupling:** Tool developers build servers independently; agents use them without custom integration
2. **Reusability:** One server can serve multiple agents
3. **Versioning:** Servers can be updated without updating agents
4. **Security:** Explicit capability boundaries (agent can only call advertised tools)
5. **Auditability:** All tool calls flow through MCP; easy to log and audit

---

## Common Patterns

### Pattern 1: Read-only exploration
```
lookup_customer("alice@acme.com")
→ Customer record
→ check_plan() to understand what they have
→ summarize and report
```

### Pattern 2: Approval gate
```
lookup_customer("alice@acme.com")
→ need_refund = true
→ request_approval(reason="Customer is within 30-day window")
→ wait for approval
→ if approved: process_refund()
```

### Pattern 3: Fallback cascade
```
try: transfer_funds(to_account="bob", amount=100)
  on error: {
    try: notify_support(issue="Transfer failed, please investigate")
    return error_to_user("We're experiencing technical issues; a support agent will help shortly")
  }
```

---

## Interview Questions

1. **Design:** "Design a tool schema for 'send email.' What goes in parameters? What validation? What could go wrong?"

2. **Error handling:** "A tool call fails with a 500 error. What does the agent see? How should it recover?"

3. **Idempotency:** "Design idempotent tool calls. Why does idempotency matter for writes?"

4. **Composition:** "You have three tool servers (customer DB, email, payments). An agent needs to send a refund confirmation email. Design the flow."

5. **MCP:** "Why would you use MCP instead of directly embedding tools in your agent code?"
