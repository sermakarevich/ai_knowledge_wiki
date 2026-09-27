> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Concepts: Workspaces, Peers, Sessions, Messages
**In one sentence:** Honcho stores small interaction records inside threads inside an isolated project area, then reasons over them to maintain a living learned profile for each person or agent.

## Key points
- A Workspace is the top-level isolated project area, used for example for development versus staging versus production or for one customer each, and login keys are issued at this level.
- A Peer is any long-lived entity that changes over time, such as a user, an agent, a group, a project, or an idea, with one unique ID (Identifier, a unique name) per Workspace, and everything Honcho learns is stored as that peer's representation.
- A Session is one interaction thread between peers with a start and an end, such as one support ticket or one meeting, and sessions are the unit of visibility that controls what history can be recalled together.
- A Message is the basic unit of data in a session, always linked to one peer and ordered by time, and each new message triggers background reasoning; bulk import allows up to 100 messages in one API (Application Programming Interface, a way for programs to talk to Honcho) call.
- A Representation is Honcho's learned understanding of a peer, made of logic conclusions plus rolling session summaries plus a short peer card with basic facts, stored in vector collections with one collection per observer-and-observed pair.
- Observation has two modes: observe_me builds Honcho's own view of a peer from all of that peer's messages and is on by default, while observe_others lets one peer build a limited view of another peer using only sessions they shared, which keeps simulated viewpoints from becoming all-knowing.
- Settings cascade from Workspace to Peer to Session, so a default set at the Workspace level can be replaced for one peer or one session, and named scopes group sessions to bound recall to only those sessions.

---
## How the pieces connect
The source docs show the data model as a simple sketch: a Workspace has Peers and has Sessions, a Session has Messages, and Peers and Sessions connect many-to-many, meaning one peer can join many sessions and one session can hold many peers.

```
Workspace
|-- Peers
|-- Sessions
      |-- Messages
Peers <--> Sessions (many-to-many)
```

In plain words: messages live inside sessions, sessions and peers live inside a workspace, and learning attaches to peers so what is learned in one session can help in a different session.

## Workspace
A Workspace is the top container. It keeps different products or environments fully separate. The brief gives development, staging, and production, or one workspace per customer for multi-tenant SaaS (Software as a Service, one product serving many separate customers), as typical uses. Login and access keys are issued at workspace level. A workspace-wide default setting can control behaviour for all peers and sessions inside it.

## Peer
A Peer is the most important idea in Honcho. It is any user, agent, NPC (Non-Player Character, a game character played by the computer), group, project, or idea that lasts over time and needs to be remembered. Each peer has a unique ID inside its workspace. A peer collects reasoning across all of its sessions, so a conclusion learned in one session can inform a later different session. Peers can be set so Honcho does or does not reason about them.

## Session
A Session is one interaction thread or context between peers. It gives time boundaries to a set of interactions. Use sessions for support tickets, meeting transcripts, learning sessions, or conversations. A session can hold many peers. A single-peer session can also be used to import outside data: create a session with only one peer, then store emails, documents, or files as messages to enrich that peer's profile. Session settings control viewpoint behaviour, such as whether a peer forms views of others in that session. Sessions can be grouped into named scopes to bound recall (see Scopes below).

## Message
A Message is the basic unit of interaction inside a session. It is usually a chat turn, but it can carry any useful context: emails, documents, files, user actions, system notes, or rich media. Every message belongs to one peer and is ordered by time within its session. Creating messages triggers automatic background reasoning that updates peer representations. Messages support rich extra data through JSONB (JSON Binary, a flexible structured-data field; JSON means JavaScript Object Notation) metadata fields. File uploads such as PDF, text, or JSON files become messages. Writes are fast because the message is saved to PostgreSQL storage and the reasoning task is queued in the background; the API returns at once, with about 200 milliseconds response for context reads (vendor-reported).

## Representation: conclusions, summaries, peer cards
A Representation is all the reasoning Honcho has done about a peer over time. It changes as new messages arrive. Representations are produced by Neuromancer reasoning, the family of Honcho reasoning models. A representation holds three kinds of artifacts:
- Conclusions are insights built with formal logic. Explicit conclusions repeat what was directly stated. Deductive conclusions follow with certainty from stated premises. Inductive conclusions describe patterns seen across at least two supporting conclusions, with a confidence value. Abductive conclusions guess the simplest explanation for what was seen. Conclusions are stored as structured logic records with premises.
- Summaries compress session history. Short summaries are made about every 20 messages and long summaries about every 60 messages by default (vendor-reported defaults).
- Peer cards cache basic life facts such as name, occupation, and interests, so the model never loses simple grounding.
These artifacts allow steady improvement: each new message refines conclusions, refreshes summaries, and keeps peer cards current.

## Observation modes: observe_me and observe_others
Honcho can build different views based on what each peer actually saw. This allows viewpoints that stay true to shared history. There are two observation modes, controlled by configuration:
- Honcho observing peers (`observe_me`): when on, which is the default, Honcho forms a view of the peer from all messages that peer sent across all sessions. Setting `observe_me: false` stops Honcho from reasoning about that peer at all.
- Peers observing others (`observe_others`): when on at the session level, a peer forms a view of the other peers in that session using only messages it could have seen in shared sessions. For example, if Alice and Bob share sessions 1 and 2, Bob's view of Alice uses sessions 1 and 2, while Charlie, who only met Alice in session 3, gets a different smaller view of Alice. Bob can then refer to shared jokes or past conflicts that Charlie never saw. Without this split, all agents would act all-knowing and the simulation would feel false.
In storage terms, each observer-and-observed pair gets its own vector collection of conclusions.

## Scopes: bounding recall
Sessions are the unit of visibility. When one peer's history covers topics that should not mix, sessions can be grouped into named scopes that bound recall to just those sessions. A query inside one scope does not pull conclusions from sessions outside that scope. Use scopes to separate, for example, work projects from personal chats for the same user.

## Configuration cascade and SDK snippets
Settings cascade in order Workspace, then Peer, then Session. Set a default once at the Workspace level and replace it only where needed for one peer or one session. Feature flags switch reasoning modes and viewpoint tracking on or off. Custom JSON metadata can extend any item. Any LLM (Large Language Model, the AI model that reads and writes text) provider can be used, including OpenAI, Anthropic, or a custom address. Client code uses an SDK (Software Development Kit, a ready-made code library), available as `pip/uv add honcho-ai` for Python and `@honcho-ai/sdk` for TypeScript (both verbatim install strings from the research brief).

The brief names the main operations verbatim as:
- `session.add_messages` for adding messages, up to 100 per call
- `peer.search` and `conclusions.query` for searching
- `messages()` and `conclusions.list` for listing all
- `peer.chat()` for peer-anchored chat over one observer-and-observed pair
- `honcho.chat()` for workspace-wide chat with no anchor peer
- `context()` for session-level ready context, with converters `to_openai()` and `to_anthropic()`
- `schedule_dream` for manual consolidation on demand
- `observe_me` and `observe_others` for the two observation modes

**Covers:** architecture.md, representation.md (docs v3, retrieved 2026-09-10)
