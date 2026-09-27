> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# itechmeat/open-second-brain — In Plain Language

Imagine your AI assistant keeps forgetting what you told it last week.
Your preferences, your decisions, the evidence behind them — gone every
new session. Open Second Brain fixes that by giving the agent a memory
notebook that lives inside the note-taking app you already use.

## What is this about?

Open Second Brain is a memory layer for Hermes Agent, an AI agent framework.
Instead of hiding memory in a database or a cloud service, it stores
everything as plain Markdown notes inside your Obsidian vault, under a
folder called `Brain/`.

Those notes hold four kinds of things: your preferences (how you like
things done), signals (observations worth remembering), evidence (facts
and sources behind a claim), and audit trails (who wrote what, and when).

The project's own tagline says it best: plain Markdown you own, in the
same vault you already use. There is no background daemon, no mysterious
vector database, and no hidden state outside your vault. You can search
the memory in Obsidian, edit it by hand, find things with grep, and
version it with git like any other notes.

The agent never touches those files directly. It reads and writes only
through a fixed set of command-line and MCP tools (the `o2b` command),
so every memory operation passes through one known, predictable doorway.

## Why does it matter?

Most AI memory is a black box: you cannot see what the agent remembered,
you cannot correct it, and you cannot take it with you. That creates
three everyday problems this project tries to solve.

First, trust. Because every memory is a readable note, you can open it
and check what the agent actually stored about you. If something is
wrong, you fix it the same way you fix any note — by editing text.

Second, accountability. Recent releases made every write attributable
and revertible. Each note change leaves a write record, keeps a
before-image snapshot, seals planned reverts with a digest, and chains
per-shard hashes so tampering shows. A freeze guard can refuse writes
during sensitive fleet operations.

Third, safety and privacy. A `visibility:` marker is not just a label —
it is enforced as a real boundary on every read path, so private notes
stay private. Material extracted from untrusted sources lands in a
quarantine lane first, and writes that name a caller are limited to
allowed folder prefixes.

In short: you get an agent that remembers, but you stay the owner and
the auditor of what it remembers.

## How does it work?

The system works in five plain steps, from notes up to installation.

1. **Start from notes you own.** Preferences, signals, evidence, and
   audit trails are real `.md` files under `Brain/`. Nothing lives
   anywhere else, so backup is just git and your vault folder.

2. **Plug the vault into the agent.** The project acts as a memory
   provider for Hermes Agent. When the agent needs context, lifecycle
   hooks (prompt assembly, prefetch, turn sync, compression, session
   end, memory write, shutdown) pull from or push to the vault through
   the `o2b` tools — never by free-form file access.

3. **Expose a small, stable doorway.** The repository root re-exports
   the provider, health checks, and registration functions so the
   Hermes gateway loads it first. Two MCP servers are declared: a full
   one and an always-loaded writer one. Manifests spell out the plugin
   id, the five contracted tools, and settings such as vault path,
   instance name, agent name, and timezone.

4. **Keep every change traceable.** Writes carry attribution, snapshots,
   digest-sealed reverts, and hash chains. Reads respect `visibility:`.
   Optional settings let you narrow what gets indexed, telemetry notes
   which channel delivered a memory, and unknown tool arguments get
   helpful suggestions instead of being silently ignored.

5. **Install and verify per app.** One router command, `o2b install`,
   wires up each supported editor or runtime, and `o2b init`, `o2b
   doctor`, and `o2b install --check` confirm the setup is healthy.
   Native Windows support keeps files under the local app-data folder
   with `.cmd` launchers beside the bash ones.

Self-description helpers round it out: `o2b version` reports the build,
and wiring views show linked projects and host health plus the exact
instruction block built from granted capabilities.

## Where can this be used?

Anywhere you want a personal AI that remembers you without locking your
data into someone else's service.

- **Personal knowledge work.** Keep lasting preferences, project context,
  and decision logs in Obsidian; let the agent recall them next session.
- **Team and multi-runtime setups.** One install router covers editors
  like Cursor, Kiro, and Gemini CLI, pipeline runtimes like Hermes,
  OpenClaw, Codex, and Claude Code, plus a generic output mode — so the
  same vault-backed memory follows you across tools.
- **Windows desks as well as Mac/Linux.** Native Windows paths and
  launchers mean the same workflow runs on Windows 10 and 11.
- **Audited or cautious environments.** Audit trails, before-images,
  hash chains, quarantine lanes, and enforced visibility make it a fit
  where you must show what the agent knew and when — or keep parts of
  the vault strictly off-limits.

## Conclusions & takeaways

Open Second Brain bets on a simple idea: agent memory should be files
you can read, not rows you cannot see. That choice buys transparency,
portability, and easy backup at the cost of managing a vault — which
Obsidian users already do.

The surrounding machinery — deterministic tools, lifecycle hooks,
attributable writes, visibility enforcement, quarantine — exists to make
that simple idea safe in practice: the agent gets structured access,
and you get proof of everything it did.

If you remember one sentence: it is a notebook your agent may use but
never owns, with every scribble signed, dated, and erasable.

## Jargon decoder

| Term | What it means in plain words |
|---|---|
| Obsidian vault | A folder of Markdown notes that the Obsidian app shows as linked notes. |
| `Brain/` | The subfolder where all agent memories live as plain notes. |
| Memory provider | The plug-in role: supplying the agent with remembered context on demand. |
| CLI / `o2b` | The typed commands (like `o2b install`, `o2b doctor`) that manage memory. |
| MCP server | A standard doorway letting editors and agents call the memory tools. |
| Lifecycle hooks | Automatic moments (session start, turn sync, session end) when memory is read or saved. |
| Write record / before-image | A log entry plus a snapshot of the note before the change, so it can be undone. |
| Hash chain / digest | Tamper-evident seals proving a note's history was not altered. |
| `visibility:` | A marker on a note that the system enforces as a real privacy boundary. |
| Quarantine lane | A holding area for facts pulled from untrusted sources until reviewed. |
