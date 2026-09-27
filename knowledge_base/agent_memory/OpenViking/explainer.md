> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# volcengine/OpenViking — In Plain Language

## What is this about?

OpenViking is an open-source "context database" for AI agents.

Think of it this way: today's AI agents keep what they know in a
black box. Text goes in, embeddings come out, and nobody — not even
the developer — can easily see, check, or fix what the agent
remembers.

OpenViking replaces that black box with something familiar: a file
system. Everything an agent knows — project documents, user memories,
and reusable skills — lives in one browsable tree under addresses
that start with `viking://`.

Both agents and humans use the same view. An agent can list, read,
and search folders. A human can open the same folders, read the same
files, and edit them directly when something is wrong.

There are three kinds of content in the tree:

- **Resources** — documents, code, web pages, project files.
- **Memories** — user preferences and past experience, such as writing
  style or coding habits.
- **Skills** — step-by-step procedures the agent can reuse, such as
  "search the code" or "analyze this data."

## Why does it matter?

Agents fail in predictable ways without good memory.

They forget what you told them three weeks ago. They re-read huge
piles of documents for every question, which is slow and expensive.
They mix up one user's private notes with shared project knowledge.
And when they do something strange, you cannot inspect why because
their memory is a pool of vectors you cannot browse.

OpenViking matters because it attacks all four problems at once:

1. **It makes memory inspectable.** If the agent remembers something
   wrong, you can open the memory file and fix it like any document.
2. **It cuts waste.** Agents read short summaries first and open full
   files only when needed, instead of loading everything every time.
3. **It keeps scope tight.** Search runs inside one folder subtree
   rather than across one giant flat pool, so results stay relevant.
4. **It has measured results.** On a long-conversation memory test,
   agents using OpenViking scored around 80–83% accuracy versus about
   24–57% without it, while using fewer tokens and answering faster.
   On multi-step shop-assistant tasks, remembered experience lifted
   success by roughly 7 points in retail and 12 points in airline
   scenarios.

In short: less forgetting, less re-reading, fewer mix-ups, and a
memory you can actually look at.

## How does it work?

Imagine a virtual hard drive called `viking://`.

At the top level there are shared resources (for example, a team's
project docs and source code) and per-user areas holding that user's
memories, private resources, skills, and even records of past
visitors or peers.

You work with it using file-style commands, either through a small
`ov` command-line tool or through SDKs and an HTTP API:

- `ls` and `tree` — browse what exists.
- `read` and `write` — open and update files.
- `grep` — search for exact text.
- `find` — run a semantic query directly in one folder.
- `search` — let the system plan retrieval from the session context.

The clever part is **summaries before sources**.

Every directory can carry two generated helper files: a one-sentence
abstract (called L0) and a longer overview (called L1). The full
content is L2. An agent first scans the short L0 abstracts, then reads
a promising L1 overview, and only then opens the full L2 file. It is
like reading chapter titles, then a chapter summary, then the chapter
itself — instead of reading the whole book every time.

Sessions also become files. When a conversation ends, it can be
archived and distilled into plain Markdown memory files you can read
and edit. A `compile` step can then organize a pile of source
material into a wiki, a knowledge graph, or a report.

Getting started needs Python 3.10 or newer plus an embedding model
and a vision-language model, cloud or local. Setup is a short
sequence: install the package, run an `init` wizard that writes a
config file, run a `doctor` check, then start the server. There is
also a browser-based Studio for browsing context and trying search
without installing anything.

## Where can this be used?

Anywhere an agent needs to remember things over time:

- **Coding assistants** — remember a project's layout, conventions,
  and a developer's habits across sessions.
- **Support and shopping agents** — remember past cases and customer
  preferences so multi-step tasks succeed more often.
- **Research helpers** — organize papers, docs, and web pages into a
  browsable wiki instead of a pile of chat transcripts.
- **Team knowledge bases** — keep shared project docs separate from
  each user's private notes, skills, and history.
- **Long-running personal assistants** — recall writing style,
  decisions, and experience from months of conversations.

It plugs into common agent tools through SDKs for Python, Go, and
TypeScript, a generic plugin interface, and integrations with
popular coding assistants.

## Conclusions & takeaways

- OpenViking treats agent memory as **files, not vectors**: browsable,
  editable, and addressable through `viking://` paths.
- Its core trick is **read less, know more**: tiny abstracts, medium
  overviews, full details only on demand, all scoped to one folder.
- **Sessions become durable knowledge**: conversations turn into
  Markdown memories, and raw material compiles into wikis, graphs,
  or reports.
- Benchmarks suggest the design pays off: much higher memory accuracy
  with fewer tokens, plus double-digit gains on realistic service tasks.
- The trade-off is setup: you must provide models, run a server, and
  organize your context tree — it is infrastructure, not magic.
- If you build agents that should learn and persist, this is a
  practical pattern to copy even if you never install the tool:
  unify knowledge, memory, and skills in one inspectable, summarized,
  scoped store.

## Jargon decoder

| Term | What it really means |
|---|---|
| Context database | A store for everything an agent knows, built for finding the right piece at the right time |
| `viking://` | The address scheme for OpenViking's virtual filesystem, like a path to a file |
| Resources | Documents, code, and web pages the agent can read |
| Memories | Saved preferences and past experience, such as "user likes short answers" |
| Skills | Reusable how-to procedures, such as "search the codebase" |
| Scoped search | Searching inside one folder instead of the whole store, so answers stay relevant |
| L0 abstract | A one-sentence summary used to decide "is this folder worth opening?" |
| L1 overview | A medium-length summary describing structure and key points for planning |
| L2 details | The full original content, opened only when actually needed |
| Session commit | Saving and distilling a conversation into readable memory files |
| Compile | Turning a pile of source files into an organized wiki, graph, or report |
| Embedding model | A model that turns text into numbers so similar meanings can be matched |
