> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Tool-Quality Best Practices

**In one sentence:** A tool (a function an AI agent — a program that can act on its own — can call) is only as good as its design: focus each tool on a single outcome, write clear descriptions, separate safe reads from risky writes, return errors the agent can act on, and keep inputs simple, because these choices directly determine whether the agent uses the tool correctly.

## Key points

- Tools should be designed around outcomes (the end result a user wants), not wired up as atomic REST APIs (raw web service calls, one per small operation), because outcome-focused tools cut down the number of round trips the agent needs to make [15:52].
- A tool's description is guidance text the agent reads before deciding how to call the tool; it should not repeat information the agent can already see, such as the input parameter schema (the list and types of arguments the tool accepts) — writing a clear, non-redundant description improves how accurately the agent uses the tool [15:56].
- Read tools (ones that only fetch data) and write tools (ones that change data) should be kept separate, so read tools can be auto-approved while write tools are routed to a human for confirmation before running [16:27].
- Errors returned to the agent should be actionable rather than generic HTTP status codes (web error numbers like 404 "not found"); giving the agent enough detail in the error message lets it retry or correct its own action [16:46].
- Tool inputs should be simple and flat rather than complex nested maps or unusual primitive types, because agents are less reliable at correctly constructing complicated input structures [17:31].
- The speakers point to their own documentation, the MCP Toolbox for Databases GitHub repository, and the Eval Bench repository (their evaluation framework for agents, MCP tools, and skills) as the concrete resources for learning and validating these practices [19:39].

---

## Focus on outcomes, not atomic REST APIs

The speakers recommend that tools be built around what the user actually wants accomplished, rather than exposing many small, atomic REST API operations for the agent to string together itself. Thinking in outcomes rather than fine-grained API calls reduces the number of round trips needed — instead of the agent making several separate tool calls to piece together a result, one outcome-oriented tool call can do the job [15:52]–[15:58].

## Write good tool descriptions, don't duplicate what the agent already knows

Tool descriptions exist to guide the agent's behavior. The speakers stress that descriptions should not restate information the agent already has direct access to, such as the tool's input parameter schema — that is redundant and adds noise. Instead, the effort should go into writing accurate, useful descriptions that help the agent understand when and how to use the tool correctly. They call this "guidance," and note that writing good descriptions is important for accurate tool usage [15:58]–[16:05].

## Separate read tools from write tools

Splitting tools into read-only and write categories lets the system apply different levels of trust. Read tools, which cannot change any data, can be auto-approved so the agent doesn't need to pause and ask permission every time. Write tools, which can modify or delete data, should instead be routed to the user for confirmation before they execute. This separation also makes it clearer to the agent which category a given tool falls into [16:27]–[16:44].

## Return actionable errors instead of generic HTTP codes

One of the most common shortcomings the speakers call out is returning a bare, generic HTTP error code (for example, a 404 "not found") when a tool call fails. Modern agents are capable of reasoning about a failure and retrying with a correction — but only if the error message gives them enough information to do so. The speakers describe this as the "number one thing" that tool builders can do better: return an error that can actually be acted on, not just a status code [16:46]–[17:07].

## Prefer simple, flat inputs over complex nested structures

The speakers observe that developers often try to give tools complex inputs — nested maps or unusual combinations of primitive types — that the agent then has to construct correctly on the fly. This is unreliable in practice. Using a flat structure with simple inputs instead measurably increases how reliably the agent can call the tool [17:31]–[17:49].

## Closing pointers: documentation, MCP Toolbox, and Eval Bench

In their closing remarks, the speakers direct the audience to three resources for going deeper and for validating tool quality in practice: their documentation, the MCP Toolbox for Databases GitHub repository (their open-source database MCP server), and the Eval Bench repository — the evaluation framework the team uses to verify that agent tools, MCP servers, and skills are actually working well. Eval Bench is highlighted specifically as "how we know that our tools are working well" [19:39]–[19:59].

---

**Covers:** [15:52]–[19:59]
