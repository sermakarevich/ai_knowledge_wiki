> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# MCP Toolbox Background & Tool Patterns

*(MCP = Model Context Protocol, the open standard that lets an AI agent call external tools; NL2SQL = natural language to SQL, turning a plain-English question into a database query; SQL = Structured Query Language, the language used to query databases.)*

**In one sentence:** Google's MCP Toolbox for Databases has grown into a widely-used open-source and hosted database MCP server, and the team has observed three recurring ways agents access databases through it — human-supervised admin tools, flexible-but-risky NL2SQL tools, and locked-down structured SQL tools for production.

## Key points

- The talk is given by Averi Kitsch (Staff Software Engineer, Google Cloud Databases, tech lead for MCP Toolbox for Databases and the Google Cloud MCP server) and Prerna Kakkar (Senior Software Engineer at Google, tech lead for Eval Bench, and an active contributor to MCP Toolbox) [0:33]-[1:07].
- The talk covers three areas: the history of MCP at Google, common tool patterns for database access, and security guardrails against data leaks [1:09]-[1:36].
- MCP Toolbox for Databases is an open-source, self-managed server with about 15.7K GitHub stars, 132+ active contributors, and support across 40+ different databases, and it provides connection pooling, integrated authentication ("O" in the transcript, i.e., OAuth-style auth), and observability out of the box [1:41]-[2:10].
- For teams that don't want to self-manage, Google also offers a fully managed, hosted version called Google-managed MCP, which plugs into agents/IDEs/harnesses such as Gemini CLI, Antigravity CLI, and Claude Code, and adds governed discovery plus "model armor" for secure access management and identity control [2:12]-[2:44].
- Combined, the self-managed toolbox and the Google-managed MCP handled 20 million tool calls last month [2:48]-[2:54].
- Three common tool patterns for database access recur across the team's own work: (1) control-plane/admin tools, (2) NL2SQL tools, and (3) structured SQL tools [2:56]-[3:02].
- Control-plane tools (also called admin or manage tools) handle developer-assistance tasks like creating or managing database instances; they are built on already-provisioned public APIs (so monitoring comes for free), but because they can perform dangerous actions they require a human in the loop [3:04]-[3:33].
- NL2SQL tools rely on a single "execute SQL" tool where the agent generates raw SQL itself, making them well suited to developer assistance and analytical agents doing flexible, unplanned exploration — for example, a query like "find all customers in California who bought a winter coat in July and returned it within 14 days, and group them by the marketing campaign that originally acquired them" [3:44]-[4:33].
- Structured SQL tools use predefined, parameterized queries where the SQL itself is fixed in advance; this prevents SQL injection, restricts the agent to predefined logic for tightly controlled access, and is the pattern favored for production use because it also helps with latency and reduces agent hallucination [4:37]-[5:08].

---

## Speaker introductions

Averi Kitsch introduces herself as a staff software engineer working on Google Cloud databases and the current technical lead for MCP Toolbox for Databases — described as Google's "open-source database MCP server" — as well as a maintainer of the Google Cloud MCP server [0:33]-[0:51].

Prerna Kakkar introduces herself as a senior software engineer at Google and the current tech lead for Eval Bench, described as "the evaluation framework for all your agent[ic], MCP, and skills need." She is also an active contributor to MCP Toolbox [0:51]-[1:09].

The pair frame the talk's agenda in three parts: (1) the history of MCP at Google, (2) common tool patterns observed from their own work, used to build database-access tools, and (3) security guardrails for preventing data leaks via identity-aware controls [1:09]-[1:36].

## History and background of MCP Toolbox for Databases

Kitsch describes MCP Toolbox for Databases as an open-source, self-managed serving layer. As of the talk it has:

- ~15.7K GitHub stars
- 132+ active contributors
- Support across 40+ different databases

It is described as a "highly customizable framework" that provides connection pooling, integrated authentication, and observability "out of the box," so developers don't need to build or configure these themselves [1:39]-[2:11].

For teams that would rather not self-host, Google also provides a hosted, scaled version called **Google-managed MCP**. This fully managed offering can be plugged into a range of agents, IDEs, and harnesses — the talk names Gemini CLI, Antigravity CLI, and Claude Code as examples ("you name any"). It offers governed, simple discovery and includes **model armor**, which provides secure access management and identity control [2:12]-[2:45].

Combining the self-managed toolbox with the Google-managed MCP offering, the team reports **20 million tool calls last month** [2:48]-[2:54].

## The three common tool patterns for database access

Kakkar then walks through tool patterns the team has observed specifically for database access.

### 1. Control-plane / admin tools

Also called "admin tools" or "manage tools," these live in the developer-assistance space: creating an instance, managing an instance, creating databases, managing databases — essentially covering DBA (database administrator) needs. Because these tools can perform dangerous operations, they require a **human in the loop**; they are built on top of already-provisioned public APIs, which means monitoring and related operational capabilities come "out of the box" [3:04]-[3:33].

### 2. NL2SQL (natural language to SQL) tools

These tools rely on a tool the team calls **execute SQL**: the agent itself generates raw SQL queries from a natural-language request. This pattern is useful when the required queries aren't known ahead of time, so it targets developer-assistance and analytical agents doing **flexible exploration**.

The concrete example given: *"find all customers in California who bought a winter coat in July and returned it within 14 days and group them by the marketing campaign that originally acquired them."* This is presented as a case where an NL2SQL tool is used to get an answer without a query having been predefined [3:44]-[4:33].

### 3. Structured SQL tools

Structured SQL tools are described as "getting quite popular" and target mainly **production use cases** — situations where the SQL query needed is already known ahead of time. Key properties:

- The query and its parameters are predefined/preconfigured, which **prevents SQL injection**.
- Access is highly controlled because the agent is restricted to predefined logic rather than free-form query generation.
- This pattern also helps meet latency requirements and reduces hallucination on the agent side [4:37]-[5:08].

---

**Covers:** [0:33]–[5:08]
