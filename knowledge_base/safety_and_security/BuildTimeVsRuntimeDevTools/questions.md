---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Build-Time vs. Run-Time: Why Dev Tools Fail in Production

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What three recurring tool patterns did the speakers observe for how agents access databases through MCP (Model Context Protocol) Toolbox, and what distinguishes structured SQL tools from the other two?

> [!tip]- Answer
> The three patterns are control-plane/admin tools (for DBA-style tasks, built on already-provisioned public APIs), NL2SQL tools (a single "execute SQL" tool where the agent writes raw SQL itself for open-ended exploration), and structured SQL tools (predefined, parameterized queries fixed in advance). Unlike the first two, structured SQL tools prevent SQL injection and restrict the agent to predefined logic, which is why they are favored for production — they also help with latency and reduce hallucination. See [[wiki/01-mcp-toolbox-background|MCP Toolbox Background]].

### Q2. Why does handing a "build-time" tool (like an admin tool or NL2SQL's execute-SQL tool) to an autonomous agent in production create danger, even though the same tool is safe during development?

> [!tip]- Answer
> Build-time tools are atomic and flexible by design, so a developer can approve or halt each step as it happens — the human is the safety net. In production there is no human watching each action, so the same flexibility means the agent can be talked into anything, including destructive actions. The talk's failure demo showed exactly this: an unattended build-time tool let an agent delete a table and "start fresh" with no safeguards stopping it. See [[wiki/02-build-time-vs-runtime|Build-Time vs. Runtime]].

### Q3. In Simon Willison's "lethal trifecta," what three conditions must all be present at once for a data breach to occur, and how did the salary-database ticket example map onto them?

> [!tip]- Answer
> The three conditions are: an agent with access to private data, exposure to untrusted content, and a way to exfiltrate that data back out. In the example, a malicious insider hid a request for all employee salaries inside a ticket (untrusted content); the triage agent already held database credentials (private data access) and trusted the ticket enough to post the answer back on it (exfiltration path), producing a full breach. See [[wiki/03-security-guardrails|Security Guardrails]].

### Q4. The talk recommends splitting tools into "read tools" and "write tools." What is the mechanism this enables, and what would break if that separation were removed?

> [!tip]- Answer
> Separating read from write tools lets the system apply different trust levels: read tools (which cannot change data) can be auto-approved, while write tools are routed to a human for confirmation before executing. Without the separation, either every action — including harmless reads — would need human confirmation (slowing the agent down), or destructive writes would run unchecked alongside reads, removing the safety gate exactly where it matters most. See [[wiki/04-tool-quality-best-practices|Tool Quality Best Practices]].

### Q5. Walk through how MCP Toolbox's "source" primitive progressively strips capability away from the agent, from a fully model-controlled tool to a "zero trust" tool. Why does moving connection details into a YAML file matter as the first step?

> [!tip]- Answer
> The evolution runs: (1) fully model-controlled tool, where the agent holds DB credentials, host, port, and writes raw SQL — a superuser; (2) the source primitive moves connection details into a preconfigured YAML file the agent never sees; (3) source-level controls add read-only restrictions, allowed-dataset limits, and output-size caps; (4) custom tools fix the exact SQL with typed prepared statements, preventing injection; (5) custom semantic tools replace raw SQL with business-level parameters like userId and date; (6) bound or authenticated parameters remove PII/identity from the agent; (7) the zero-trust end state leaves only a simple, non-sensitive parameter like a date. Moving connection details out first matters because as long as the agent controls host/port/credentials, tricking the agent hands over the entire database — every later restriction is moot until that first capability is removed. See [[wiki/03-security-guardrails|Security Guardrails]].

### Q6. Suppose you are designing a tool for an agent to process customer support tickets that can query an orders database. Applying the talk's identity-separation principle, how would you scope the user, application, and agent identities differently, and which of the two parameter types (agent-controlled vs. application-controlled) should carry the ticket's authenticated customer ID?

> [!tip]- Answer
> Following the talk's model, the user should only have access to the support application itself; the application's workload identity can be broader since it may need to reach several backend services (orders DB, billing, etc.); but the agent embedded in that application should get only the narrow slice of data relevant to the current ticket's customer, not the whole orders database. The customer ID should be an application-controlled (or bound/authenticated) parameter injected by the application after verifying the ticket's authenticated session, not an agent-controlled value the model derives itself — otherwise the agent could be tricked into supplying a different customer's ID, exactly the confused-deputy failure mode described in the talk. See [[wiki/03-security-guardrails|Security Guardrails]].

### Q7. The talk's two live demos were meant to contrast a failure case (build-time tool used at runtime) against a success case (the "Similar" travel-assistant chatbot resisting identity impersonation). Given that the runtime demo's video failed to load and was only described verbally, what is the weakest point in the talk's evidence for its runtime-tool security claims, and how would you independently verify the claim?

> [!tip]- Answer
> Because the success demo was never actually shown running, the audience has only the presenters' description that authenticated, identity-bound tools would refuse to book a flight under someone else's identity — there is no observed proof it worked as claimed, unlike the failure demo, which was shown happening. To verify independently, one would need to reproduce the "Similar" chatbot's setup (or an equivalent tool using bound/authenticated parameters as described) and actually attempt the impersonation attack against it, checking whether the tool call is rejected or the identity is silently substituted. See [[critical_thinking]].
