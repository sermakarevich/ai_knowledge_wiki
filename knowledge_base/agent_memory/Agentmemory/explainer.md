> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# rohitg00/agentmemory — In Plain Language

## What is this about?
In short: agentmemory gives your AI coding assistant a long-term memory.

Normally, every time you start a new chat with a coding agent, it forgets
everything — your project, your decisions, your preferences. You end up
re-explaining the same things over and over.

agentmemory fixes that. It is a small program that runs on your own computer
and remembers things across sessions. Its motto is simple: "your coding agent
remembers everything, no more re-explaining."

It works with many popular assistants — Claude Code, Cursor, GitHub Copilot
CLI, Gemini CLI, Codex CLI, OpenCode, and others. All of them can share the
same memory instead of each keeping their own separate notes.

Importantly, it needs no external database and no paid service to get started.
Everything runs locally on your machine.

## Why does it matter?
Coding agents are powerful but forgetful. Without memory:

- You repeat context every session ("we use this framework, don't touch that file").
- The agent makes the same mistakes twice.
- Long projects lose continuity — decisions from last week vanish.
- You burn extra time and money feeding the same background text again and again.

A shared memory solves the repetition problem. The project claims big wins:
much less repeated text (92% fewer tokens), strong recall of past facts,
and one memory shared by every tool you use.

It also matters because it is local-first. There is no cloud account to set up,
no database to operate, and it runs without an AI key by default. You can add
smarter features later, but the basic "remember and recall" works out of the box.

For teams and heavy agent users, that means less friction, faster onboarding
of new tools, and agents that get more useful the longer you use them.

## How does it work?
Think of it as three parts: a notebook, a librarian, and a set of messengers.

1. **One install, one memory server.** You install it with a single command
   (`npx -y @agentmemory/agentmemory@latest`). The setup asks which agents
   you use, seeds a configuration file, and starts two things: the memory
   server itself plus a background engine (called the iii engine) that stores
   and serves the data.

2. **It runs quietly in the background.** Once started, it listens on four
   local ports on your computer: one for regular requests, one for live data
   streams, one for a visual viewer in your browser, and one for the internal
   engine. Your notes live in files on your disk, in a standard location for
   your operating system, so they survive restarts.

3. **Agents save and recall through three doors.** Coding agents talk to the
   memory in three ways: automatic hooks (small scripts that save context when
   things happen, like the start of a session or before a tool runs), a plugin
   protocol called MCP (about 54 built-in memory tools), or a plain web API
   (REST). You can connect a new agent any time with `agentmemory connect`.

4. **Smart-enough search by default, smarter if you opt in.** Out of the box
   it uses keyword search (BM25) — fast, private, no keys needed. If you want
   meaning-based search, you flip one setting to use free on-device embeddings,
   or add a provider key for cloud models. Likewise, automatic summarising of
   observations only turns on when you explicitly enable it plus a language-model
   key; otherwise it uses a simple built-in compression that needs no AI.

5. **Configuration is explicit and off by default.** A template file documents
   every knob: which AI provider to use, which embedding method, passwords for
   the web view, search weights, and behaviour flags. Since everything is off
   by default, the first run is safe and keyless. Strict checklists and over
   1,600 automated tests keep the tools, API, and storage format consistent.

## Where can this be used?
Anywhere you use an AI coding assistant that can call out to tools or web
addresses — which is nearly all of them today.

- **Daily coding:** keep project conventions, architecture decisions, gotchas,
  and "don't do this" lessons so every new session starts already briefed.
- **Switching tools:** use Claude Code today and Cursor tomorrow without losing
  context — both read the same memory server.
- **Long projects:** carry decisions across weeks and months instead of a
  single chat window.
- **Teams:** share one memory server so lessons one person teaches the agent
  help everyone else.
- **Private or offline work:** run fully on your laptop with no external
  database and no required cloud key.
- **Power users:** turn on local meaning-based search, the browser viewer,
  and auto-summarising when a project grows large enough to need them.

If you only chat with an AI occasionally, you may not need it. It pays off
most when you code with agents often, across many sessions and tools.

## Conclusions & takeaways
- agentmemory is best understood as "long-term memory as a utility": install
  once, then every compatible coding agent remembers.
- Its biggest idea is sharing — one memory, many agents — instead of each
  assistant starting from zero.
- The design favours starting simple (keyless, local, keyword search) and
  upgrading deliberately (local or cloud embeddings, AI summarising).
- The trade-off is operational: you gain continuity but run one more local
  service with its ports, data files, and settings to look after.
- Treat vendor-style numbers (retrieval scores, token savings, tool counts)
  as marketing claims to verify in your own project, not guarantees.
- If your agents keep forgetting, this is a practical fix; if they don't,
  it is optional complexity.

## Jargon decoder
| Term | What it really means |
|---|---|
| Persistent memory | Notes the agent keeps between chats, so it doesn't forget everything on restart. |
| MCP | A standard plug-in language that lets coding agents call outside tools like this memory. |
| Hooks | Tiny automatic scripts that save or load memory when something happens, e.g. session start. |
| REST API | A plain web-address interface any program can use to save or search memories. |
| BM25 / keyword search | Finding old notes by matching words, no AI needed. Fast and private, but literal-minded. |
| Embeddings / semantic search | Finding old notes by meaning, not just words. Smarter, but needs extra setup. |
| iii engine | The background storage-and-delivery program that agentmemory is built on top of. |
| Noop mode | Running without any AI key: basic saving and keyword search still work. |
| Token | A chunk of text the AI reads; fewer repeated tokens means less cost and waiting. |
| Viewer | A local web page where you can browse what the agent remembers. |
