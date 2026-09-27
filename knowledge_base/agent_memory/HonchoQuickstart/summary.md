# Honcho Quickstart

**Source:** [Honcho Quickstart](https://honcho.dev/docs/v3/documentation/introduction/quickstart)

## Human Readable TL;DR

Imagine you have a helper that watches all your conversations with an AI assistant and learns your preferences, habits, and goals over time -- without you having to explain yourself every session. Honcho is the plumbing that makes this happen: you feed it your conversation history, and it can answer questions like "what kind of user is this?" so your AI app can adapt to each person automatically.

## TL;DR

Honcho is a context-aware memory layer for AI agents. It ingests multi-session conversation history, models each participant as a "peer", and exposes a natural language query interface (`peer.chat(...)`) that synthesizes implicit user traits across sessions. Billed per reasoning operation, not per token stored or retrieved.

---

## Problem & Motivation

LLM applications lose context between sessions. Developers must either stuff entire conversation histories into prompts (expensive, limited) or build custom memory systems (complex). Honcho provides a managed layer that ingests historical sessions, reasons over them, and surfaces synthesized user signals on demand -- without requiring developers to build their own memory pipelines.

---

## Core Concepts

1. **Workspace** -- top-level isolation boundary. One workspace per app or experiment. Created implicitly on `Honcho(workspace_id=...)`.

2. **Peer** -- a participant identity (user, assistant, or any named agent). Peers are reused across sessions. `honcho.peer("user")` returns or creates the peer.

3. **Session** -- a single conversation unit. Messages are added to sessions; sessions belong to the workspace. `honcho.session(session_id)`.

4. **Message** -- a typed utterance from a peer. Created via `peer.message(content)`, then batch-added to a session.

5. **`peer.chat(query)`** -- the insight interface. Accepts a natural-language question; returns synthesized conclusions drawn by Honcho's reasoning layer across all ingested sessions for that peer.

---

## Setup

```bash
# Get API key from app.honcho.dev (free tier: $100 credit)

# Python
uv add honcho-ai        # or: pip install honcho-ai

# TypeScript
npm install @honcho-ai/sdk
```

---

## Key Findings

| Step | Python | TypeScript |
|------|--------|------------|
| Init client | `Honcho(workspace_id=..., api_key=...)` | `new Honcho({ workspaceId, apiKey })` |
| Create peer | `honcho.peer("user")` | `await honcho.peer("user")` |
| Create session | `honcho.session(id)` | `await honcho.session(id)` |
| Add peers to session | `session.add_peers([user, assistant])` | `await session.addPeers([user, assistant])` |
| Add messages | `session.add_messages([...])` | `await session.addMessages([...])` |
| Query insights | `user.chat("question")` | `await user.chat("question")` |

- Example dataset: 14 messages across 4 sessions
- Execution cost: ~$0.04
- Honcho charges per **reasoning operation** only -- not per token stored or retrieved

---

## Complete Python Example

```python
import json, uuid
from honcho import Honcho
from dotenv import load_dotenv

load_dotenv()

workspace_id = f"docs-example-{uuid.uuid4().hex[:8]}"
honcho = Honcho(environment="production", workspace_id=workspace_id)

user = honcho.peer("user")
assistant = honcho.peer("assistant")

with open("conversation.json", "r") as f:
    conversation_data = json.load(f)

for session_data in conversation_data["sessions"]:
    session = honcho.session(session_data["id"])
    session.add_peers([user, assistant])

    messages = []
    for msg in session_data["messages"]:
        if msg["role"] == "user":
            messages.append(user.message(msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(assistant.message(msg["content"]))

    session.add_messages(messages)

response = user.chat("What should I know about this user? 3 sentences max")
print(response)
```

---

## Complete TypeScript Example

```typescript
import * as fs from 'fs';
import { randomUUID } from 'crypto';
import * as dotenv from 'dotenv';
import { Honcho } from '@honcho-ai/sdk';

dotenv.config();

const workspaceId = `docs-example-${randomUUID().slice(0, 8)}`;
const honcho = new Honcho({ environment: "production", workspaceId });

const user = await honcho.peer("user");
const assistant = await honcho.peer("assistant");

const conversationData = JSON.parse(fs.readFileSync("conversation.json", "utf-8"));

for (const sessionData of conversationData.sessions) {
  const session = await honcho.session(sessionData.id);
  await session.addPeers([user, assistant]);

  const messages = [];
  for (const msg of sessionData.messages) {
    messages.push(
      msg.role === "user" ? user.message(msg.content) : assistant.message(msg.content)
    );
  }
  await session.addMessages(messages);
}

const response = await user.chat("What should I know about this user? 3 sentences max");
console.log(response);
```

---

## Suggestions & Future Directions

1. Explore multi-peer workspaces for group conversation modeling.
2. Use dynamic `workspace_id` per user/tenant for multi-tenant SaaS apps.
3. Query with richer prompts to extract specific traits (communication style, expertise level, goals).
4. Check Honcho docs for streaming responses and async Python client patterns.
