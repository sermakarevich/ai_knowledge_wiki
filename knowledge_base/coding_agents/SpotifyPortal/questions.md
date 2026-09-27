---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]]

# Retrieval Practice: Portal by Spotify Cut My Claude Code Token Usage by 90%

Answer from memory before opening any answer. Run sessions with `ai show summary/quiz`.

### Q1. What is an AiKA mode, and what are the two worker modes (including model and temperature)?
> [!tip]- Answer
> An AiKA mode is a declarative agent where you define instructions, pick a model, set temperature, and attach MCP tools, while Portal handles servers, keys, and infrastructure on an ephemeral runtime. The article creates two workers, bulk-reader for answering questions from many large files and code-writer for tests, configs, and stubs, both running gemini-2.5-flash at temperature 0.2. The strict prompts force structured bullets or code-only output so the main model wastes no tokens on prose or fences. See [[wiki/01-portal-and-modes|Portal and modes]].

### Q2. What is the 350-line default, which hooks enforce it, and what still passes through?
> [!tip]- Answer
> The check-file-size hook watches every Read call and blocks files over the line limit, 350 lines by default and changeable with SHUNT_MIN_LINES. The check-bash-read hook catches shell workarounds like cat, head, tail, less, and more on large files. Small targeted reads with offset/limit and piped filter commands like grep still pass through. See [[wiki/02-shunt-routing|Shunt routing]].

### Q3. What was the benchmark setup and what does the 90% number mean?
> [!tip]- Answer
> The test ran on a Java monorepo across four scenarios, comparing tokens Claude would use reading files directly against tokens used via the bulk-reader summary or code-writer path. Mean saving for bulk reads was around 90%, meaning Claude consumed about one tenth of the tokens by receiving only a short summary. The code-write saving was real but unmeasured because both reference reads and output tokens are avoided. See [[wiki/03-benchmarks-savings|Benchmarks and savings]].

### Q4. Why does hook enforcement beat advisory routing rules in CLAUDE.md?
> [!tip]- Answer
> Advisory rules in CLAUDE.md were easy for Claude to ignore when busy, and every project needed its own copy with no central enforcement. The shunt plugin's PreToolUse hooks run before every tool call and block the costly read, with the block message pointing Claude to the /bulk-reader skill with exact syntax. Savings therefore do not depend on Claude remembering advice. See [[wiki/02-shunt-routing|Shunt routing]].

### Q5. Why are small files deliberately excluded from delegation?
> [!tip]- Answer
> Each delegation adds 10 to 30 seconds of network delay plus a 30-second Portal cap per call, so for a small file the wait costs more than the token saving. The line threshold enforces this trade-off: only large reads are blocked and routed to the worker, while small targeted reads pass through. Direct reads stay fast and cheap where delegation would go backwards. See [[wiki/04-limits-and-transfer|Limits and transfer]].

### Q6. How would you apply this delegation pattern to another harness?
> [!tip]- Answer
> Split the router from the worker: a hook or gate decides when to delegate, and a cheap worker mode decides how to respond, so either side can change model, prompt, or tools independently. Any harness that can shell out to the CLI and enforce pre-tool hooks can copy it: block bulk reads over a line threshold, send files plus a question to the worker, and write generated code straight to disk. Reuse shareable declarative modes and fork public ones so your copy takes precedence. See [[wiki/04-limits-and-transfer|Limits and transfer]].

### Q7. What is the weakest link in the evidence behind the 90% saving claim?
> [!tip]- Answer
> The benchmarks were author-run on a single Java monorepo with no per-scenario table, so individual scenario results are unknown and nothing is shown for other languages or repos. They measure only the drop in tokens Claude consumes, not reasoning quality, edit accuracy, or added latency. Treat the 90% as a field report of what is possible in that setup, not an independent guarantee. See [[wiki/targeted|Targeted analysis]].
