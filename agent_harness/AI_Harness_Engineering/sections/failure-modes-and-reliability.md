> **Guide:** [[../summary]] | **Deep dive:** [[../details]]

## Failure Modes and Reliability Engineering

This is where senior engineers are distinguished from junior ones in interviews. Understanding failure modes—what can break and how to recover—demonstrates operational instinct. This section covers the taxonomy of agent failures and design patterns for resilience.

---

## Failure Mode Taxonomy

### 1. Input Failures

**Problem:** The request itself is malformed or malicious.

| Failure | Cause | Detection | Recovery |
|---------|-------|-----------|----------|
| Malformed JSON | User input is not valid JSON | JSON parser error | Return clear error; ask for clarification |
| Schema violation | Request doesn't match expected schema | Validator rejects | Return schema error with examples |
| Size exceeded | Request is too large | Length check | Reject with size limit |
| Prompt injection | Adversarial input tries to override instructions | Pattern detection or LLM-based check | Filter before passing to model |
| Missing required field | Request is missing a required parameter | Schema validator | Return which field is missing |

**Design for recovery:**
```python
def validate_input(request):
    errors = []
    
    # Type validation
    if not isinstance(request.get("query"), str):
        errors.append("query must be a string")
    
    # Length validation
    if len(request.get("query", "")) > 5000:
        errors.append("query exceeds max length of 5000 chars")
    
    # Prompt injection detection
    if "<SYSTEM>" in request.get("query", "").upper():
        errors.append("query contains suspicious patterns")
    
    if errors:
        return {"status": "invalid", "errors": errors}
    
    return {"status": "valid", "data": request}
```

---

### 2. Model Failures

**Problem:** The model produces invalid, unsafe, or unhelpful output.

| Failure | Cause | Detection | Recovery |
|---------|-------|-----------|----------|
| Hallucination | Model makes up facts | Cross-check against known facts | Return "I don't know"; escalate |
| Invalid JSON | Model's JSON doesn't parse | JSON parser error | Ask model to fix; provide example |
| Schema violation | Model's output doesn't match schema | Schema validator | Reformat or re-prompt |
| Refusal | Model refuses to answer | Check for refusal keywords | Escalate; offer alternative |
| Unsafe content | Model generates PII, secrets, harmful content | Content filter | Block output; log for audit |
| Timeout | Model takes too long to respond | Timeout monitor | Return partial result; suggest escalation |

**Example: Handling hallucination**

```python
def handle_model_output(output):
    # 1. Validate JSON
    try:
        parsed = json.loads(output)
    except JSONDecodeError:
        return {"status": "invalid_json", "recovery": "ask_model_to_fix"}
    
    # 2. Validate schema
    if not validator.is_valid(parsed):
        return {"status": "schema_violation", "recovery": "reformat_or_reprompt"}
    
    # 3. Fact-check critical claims
    if parsed.get("claim"):
        is_factual = check_against_kb(parsed["claim"])
        if not is_factual:
            return {"status": "hallucination", "recovery": "ask_model_to_verify"}
    
    # 4. Filter unsafe content
    if contains_pii(parsed) or contains_secrets(parsed):
        return {"status": "unsafe_content", "action": "block"}
    
    # If all checks pass
    return {"status": "valid", "data": parsed}
```

---

### 3. Tool Failures

**Problem:** The tool call fails, returns invalid data, or times out.

| Failure | Cause | Detection | Recovery |
|---------|-------|-----------|----------|
| Not found | Resource doesn't exist | 404 error | Suggest alternatives; check spelling |
| Permission denied | User not authorized | 403 error | Explain why; offer escalation |
| Rate limited | Too many requests | 429 error | Backoff; retry after delay |
| Timeout | Tool took too long | Timeout monitor | Return cached data or escalate |
| Corrupt data | Tool returned invalid data | Schema validator | Log incident; escalate |
| Transient error | Network glitch, brief outage | 5xx error | Exponential backoff and retry |

**Example: Tool call with retries**

```python
def call_tool_with_retries(tool_name, args, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = tool_invoke(tool_name, args)
            return {"status": "success", "result": result}
        
        except NotFoundError as e:
            # Don't retry; not found is permanent
            return {"status": "not_found", "error": str(e)}
        
        except PermissionError as e:
            # Don't retry; permission doesn't change
            return {"status": "forbidden", "error": str(e)}
        
        except RateLimitError as e:
            # Retry with exponential backoff
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1, 2, 4 seconds
                time.sleep(wait_time)
                continue
            else:
                return {"status": "rate_limited", "recovery": "escalate"}
        
        except TimeoutError as e:
            # Retry, but give up after max_retries
            if attempt < max_retries - 1:
                continue
            else:
                return {"status": "timeout", "recovery": "escalate"}
        
        except Exception as e:
            # Transient error; retry with backoff
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            else:
                return {"status": "error", "error": str(e), "recovery": "escalate"}
    
    return {"status": "failed_after_retries"}
```

---

### 4. Execution Failures

**Problem:** The sandbox, isolation, or resource limits fail.

| Failure | Cause | Detection | Recovery |
|---------|-------|-----------|----------|
| Out of memory | Execution uses too much RAM | OOMKilled signal | Allocate more resources or reject |
| Out of disk | Execution fills disk | ENOSPC error | Clean up; reject if persistent |
| CPU limit exceeded | Execution takes too long | Killed by timeout | Return partial result; log for profiling |
| Network error | Can't reach external service | Connection timeout | Retry with backoff; escalate |
| Credential leak | Secret exposed in logs | Log scanning | Redact immediately; audit |
| Permission denied | Execution lacks necessary access | EACCES error | Verify IAM config; escalate |

**Example: Bounded execution**

```python
def execute_with_bounds(code, timeout=5, memory_limit=512, disk_limit=1024):
    try:
        with isolated_sandbox(
            timeout=timeout,
            memory_limit=memory_limit,
            disk_limit=disk_limit
        ):
            result = execute(code)
            return {"status": "success", "result": result}
    
    except TimeoutError:
        return {"status": "timeout", "recovery": "return_partial_result"}
    except MemoryError:
        return {"status": "out_of_memory", "recovery": "escalate_or_reject"}
    except DiskFullError:
        return {"status": "out_of_disk", "recovery": "cleanup"}
    except PermissionError as e:
        return {"status": "permission_denied", "error": str(e)}
```

---

### 5. Policy Failures

**Problem:** The request violates policy, requires approval, or is outside bounds.

| Failure | Cause | Detection | Recovery |
|---------|-------|-----------|----------|
| Policy violation | Request breaks a rule | Policy engine rejects | Explain rule; offer alternative |
| Requires approval | High-stakes action | Approval gate check | Queue for human review |
| Rate limit (policy) | User making too many requests | Rate limiter | Throttle; suggest escalation |
| Cost limit exceeded | Request would exceed budget | Cost checker | Reject; explain cost |
| Regional restriction | User in disallowed region | Geo-check | Explain; offer escalation |

**Example: Policy enforcement with recovery**

```python
def check_policies(request, user, policies):
    checks = []
    
    # 1. Cost check
    estimated_cost = estimate_cost(request)
    if estimated_cost > user.daily_budget:
        checks.append({
            "policy": "cost_limit",
            "status": "violated",
            "recovery": "suggest_cheaper_alternative"
        })
    
    # 2. Rate limit check
    if user.requests_today() > user.rate_limit:
        checks.append({
            "policy": "rate_limit",
            "status": "violated",
            "recovery": "throttle_or_escalate"
        })
    
    # 3. Approval gate check
    if request.amount > 1000:  # High-value transfer
        checks.append({
            "policy": "approval_gate",
            "status": "required",
            "recovery": "queue_for_approval"
        })
    
    # 4. Regional check
    if user.region not in policies.allowed_regions:
        checks.append({
            "policy": "regional_restriction",
            "status": "violated",
            "recovery": "deny"
        })
    
    return checks
```

---

### 6. Observability Failures

**Problem:** The system can't measure what happened.

| Failure | Cause | Detection | Recovery |
|---------|-------|-----------|----------|
| Missing trace | Decision not logged | Audit gap | Mandatory instrumentation everywhere |
| Lost logs | Logs deleted or expired | Log query returns empty | Immutable log store + long retention |
| Wrong metrics | Metrics don't match reality | Comparison test shows discrepancy | Validation suite for instrumentation |
| Clock skew | Timestamps don't align across services | Correlating events is hard | NTP sync; structured logging with UTC |
| Data poisoning | Malicious actor corrupts metrics | Outlier detection alerts | Immutable metrics + alerting |

**Example: Mandatory instrumentation**

```python
def agent_step(context):
    with span("agent_step", attributes={
        "user_id": context.user_id,
        "request_id": context.request_id,
        "timestamp": datetime.utcnow().isoformat()
    }):
        # Every decision point must be logged
        with span("instruction_selection"):
            instruction = select_instruction(context)
            log_decision("instruction", instruction.version)
        
        with span("model_invocation"):
            output = model.generate(instruction)
            log_tokens("prompt_tokens", output.prompt_tokens)
            log_tokens("completion_tokens", output.completion_tokens)
        
        with span("tool_call_validation"):
            validated = validate_tool_call(output)
            log_decision("tool_call", validated.tool_name)
        
        with span("tool_execution"):
            result = invoke_tool(validated)
            log_decision("tool_result", result.status)
        
        return result
```

---

## Reliability Patterns

### Pattern 1: Graceful Degradation

When a feature breaks, degrade gracefully:

```python
def lookup_customer(customer_id):
    try:
        # Primary path: fresh data
        return db.find(customer_id)
    except DatabaseError:
        try:
            # Fallback: cached data
            return cache.get(customer_id)
        except CacheEmpty:
            # Ultimate fallback: minimal data
            return {
                "id": customer_id,
                "status": "unknown",
                "message": "We're having trouble fetching details; please contact support"
            }
```

### Pattern 2: Circuit Breaker

If a service keeps failing, stop calling it:

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"  # Try again
            else:
                raise CircuitBreakerOpen("Service is unavailable; try again later")
        
        try:
            result = func(*args, **kwargs)
            self.failures = 0
            self.state = "closed"
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "open"
            raise
```

### Pattern 3: Bulkhead Isolation

Separate resource pools so one failure doesn't cascade:

```
┌─────────────────────────────┐
│     Agent                   │
├──────────┬──────────┬───────┤
│ Pool 1   │ Pool 2   │Pool 3 │
│ DB calls │ API      │Email  │
│ Limit:   │ calls    │calls  │
│ 10 threads│ Limit: 5 │Limit: 2│
│          │ threads  │threads│
└──────────┴──────────┴───────┘
```

If email service gets slow and burns all threads, DB and API pools are unaffected.

---

## Interview Questions (Failure Fluency)

1. **Taxonomy:** "List all the ways an agent that sends refund emails can fail. For each, what's your detection and recovery strategy?"

2. **Trade-offs:** "You can retry failed requests up to 3 times or fail fast. Which do you choose? Why? What's the trade-off?"

3. **Irreversibility:** "You're sending a refund email. Once sent, you can't unsend it. Design the flow to minimize failures."

4. **Cascading failures:** "Your agent uses a payment API that starts returning 500 errors. What breaks first? How do you prevent the cascade?"

5. **Observability:** "Your agent claims 95% success, but users report 60% success. Debug it. What would you log?"
