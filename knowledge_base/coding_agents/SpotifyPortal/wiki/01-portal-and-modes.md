> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Portal, AiKA Modes, and the Two Worker Modes
**In one sentence:** Portal's AiKA modes let a cheap worker model absorb input/output (I/O)-heavy grunt work so the frontier model only does reasoning.
## Key points
- Portal by Spotify is a platform for running small task-specific agents, so the main coding agent can hand off grunt work instead of spending expensive tokens on it.
- An AiKA mode is a declarative artificial intelligence (AI) agent that runs on an ephemeral runtime like AWS Lambda for agents: you define instructions, pick a model, set temperature, and attach Model Context Protocol (MCP) tools, while Portal handles servers, keys, and infrastructure, and each mode is callable from the Portal command-line interface (CLI) or application programming interface (API) as public (shared company-wide) or private.
- The article creates two worker modes, bulk-reader and code-writer, both using gemini-2.5-flash with temperature 0.2, where bulk-reader answers a question from many large files and code-writer generates tests, configs, stubs, and other predictable output.
- The exact bulk-reader instructions are: You are a precise code analyst. Read the provided files and answer the question concisely. Output structured bullets only. No greetings, no prose, no preambles. Lead every bullet with the exact name, type, or line number. Use nested bullets for details. Skip anything the caller did not ask for.
- The exact code-writer instructions are: You generate code files based on a spec and reference files. Match the existing patterns, conventions, naming, and style exactly. Output only the code — no explanations, no markdown fences unless asked. If the spec is ambiguous, make reasonable choices that match the reference code's patterns.
- The rule Output only the code matters because without it the worker wraps results in markdown fences and explanatory prose that the main model must then read and parse, which wastes tokens and adds cleanup work.
- Cost pressure is the motive: Gartner (June 2026) expects AI coding costs by 2028 to pass the average developer salary, a quarter of engineering leaders already spend $200-500 per developer per month on tokens, and some spend over $2,000.
---
## The cost problem
Most of what a coding agent does is not hard thinking. It is reading files and writing routine output. Reading five files to answer one question, copying test patterns, or updating docs burns thousands of tokens with almost no reasoning. The pain is not the seat license. It is the tokens, spent on a frontier model that is overqualified for simple work.
## What Portal and AiKA modes are
Portal by Spotify runs small declarative agents called AiKA modes. You write what the agent should do, choose the model, set temperature, and attach MCP tools. Portal runs it on a short-lived runtime, like AWS Lambda but for agents, with no servers or keys to manage. You call a mode from the Portal CLI or API. A mode can be public for the whole company or kept private.
## Mode 1 bulk-reader (full config)
Use bulk-reader when the main model would otherwise open many large files just to answer one question.
```
name: bulk-reader
description: Bulk file reader for code analysis - delegates I/O from Claude Code
instructions: You are a precise code analyst. Read the provided files and answer the question concisely. Output structured bullets only. No greetings, no prose, no preambles. Lead every bullet with the exact name, type, or line number. Use nested bullets for details. Skip anything the caller did not ask for.
visibility: public
model: gemini-2.5-flash
resourceLimits:
  temperature: 0.2
tags:
  - coding
  - delegation
```
## Mode 2 code-writer (full config)
Use code-writer for tests, config scaffolding, type stubs, or anything predictable from existing patterns.
```
name: code-writer
description: Boilerplate code generator - delegates output-heavy work from Claude Code
instructions: You generate code files based on a spec and reference files. Match the existing patterns, conventions, naming, and style exactly. Output only the code — no explanations, no markdown fences unless asked. If the spec is ambiguous, make reasonable choices that match the reference code's patterns.
visibility: public
model: gemini-2.5-flash
resourceLimits:
  temperature: 0.2
tags:
  - coding
  - delegation
```
## Prompt details that matter
The prompts are strict on purpose. Bulk-reader must output structured bullets only, start each bullet with the exact name, type, or line number, use nested bullets for details, and skip anything not asked. Code-writer must match naming, style, and conventions exactly and output only code. Without the no-fences rule, the worker adds markdown fences and explanations that the main model must parse through.
**Covers:** article sections "Two modes, zero code" plus intro cost context.
