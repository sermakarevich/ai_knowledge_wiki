> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Quickstart and Integration
**In one sentence:** You install a Honcho SDK (Software Development Kit, a ready-made code library), connect with an API (Application Programming Interface, a key that lets your code talk to Honcho) key, save messages into workspaces, peers, and sessions, then ask questions or pull context for your LLM (Large Language Model, the AI model that writes answers).
## Key points
- Install with `uv add honcho-ai` or `pip install honcho-ai` for Python, or `npm install @honcho-ai/sdk` (also `yarn add @honcho-ai/sdk` or `pnpm add @honcho-ai/sdk`) for TypeScript (TypeScript, a typed version of JavaScript).
- Get an API (Application Programming Interface) key at app.honcho.dev under API KEYS; every new account gets $100 in free credits (vendor-reported), and the full quickstart example costs about $0.04 to run (vendor-reported).
- A Workspace is the top-level isolation space, a Peer is any lasting entity such as a user or assistant, and a Session is one interaction thread; the quickstart creates workspace `first-honcho-test`, peers `user` and `assistant`, and ingests a 14-message example across 4 sessions.
- Use `peer.chat()` to ask about one peer and `honcho.chat()` to ask across every peer in a workspace, because peer chat is anchored to one observer-observed pair while workspace chat searches first and reads pair by pair.
- Use `session.context()` to get ready-to-use history with token budgets such as `tokens=1500` or `tokens=2000`, then convert with `to_openai()` or `to_anthropic()` for direct use with OpenAI or Anthropic (two LLM providers) models; storage and retrieval with context() is free and fast at about 200 milliseconds (vendor-reported), you pay only for reasoning.
- API (Application Programming Interface) keys are scoped as admin, workspace, peer, or session, where workspace chat needs a workspace-level or higher key, and the context() `scope` option needs a workspace-level or admin-level key and cannot be combined with `peer_perspective`.
- Self-host locally with `uv tool install honcho-cli` then `honcho start --setup`, which uses Docker (a tool that runs packaged software containers) plus your own LLM (Large Language Model) provider key, instead of the managed cloud at app.honcho.dev.
- Extend through an MCP (Model Context Protocol, a standard way for AI tools to connect) server plus `npx skills add plastic-labs/honcho`, plugins for Claude Code, Codex, Cursor, OpenCode, OpenClaw, DeepSeek Harness, Hermes, Zo, Paperclip, and SillyTavern, frameworks such as LangGraph, CrewAI, Vercel AI SDK, and n8n, plus file uploads as messages, webhooks (automatic notifications) on job completion, and queue-status checks for background reasoning.
---
## 1. Install the SDK (Software Development Kit)
Install the Honcho client library for your language. You need this before any other step.
```bash
uv add honcho-ai
```
```bash
pip install honcho-ai
```
```bash
npm install @honcho-ai/sdk
```
```bash
yarn add @honcho-ai/sdk
```
```bash
pnpm add @honcho-ai/sdk
```
## 2. Initialize the client with API (Application Programming Interface) key
Create an account at app.honcho.dev and copy the key from API KEYS. The client uses a Workspace (top-level isolation space). This example uses a test workspace called `first-honcho-test`.
```python
from honcho import Honcho

# Initialize client
honcho = Honcho(workspace_id="first-honcho-test", api_key=HONCHO_API_KEY)
```
```typescript
import { Honcho } from '@honcho-ai/sdk';

// Initialize client
const honcho = new Honcho({ workspaceId: "first-honcho-test", apiKey: HONCHO_API_KEY });
```
## 3. Create peers
A Peer is any entity that persists and changes, such as a user or an assistant. Here we create two peers.
```python
user = honcho.peer("user")
assistant = honcho.peer("assistant")
```
```typescript
const user = await honcho.peer("user")
const assistant = await honcho.peer("assistant")
```
## 4. Create sessions and ingest messages
A Session is one interaction thread between peers. A Message is one unit of data tied to a peer. Honcho can take up to 100 messages per call. The quickstart loads a JSON (JavaScript Object Notation, a text data format) file with 14 messages across 4 sessions about CI (Continuous Integration, automatic build and test) memory problems and a personal finance side project.
```python
import json

# Load conversation data
with open("conversation.json", "r") as f:
    data = json.load(f)

# Process each session
for session_data in data["sessions"]:
    session = honcho.session(session_data["id"])
    session.add_peers([user, assistant])

    # Add messages with correct roles
    messages = []
    for msg in session_data["messages"]:
        if msg["role"] == "user":
            messages.append(user.message(msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(assistant.message(msg["content"]))

    session.add_messages(messages)
```
```typescript
import * as fs from 'fs';

const data = JSON.parse(fs.readFileSync("conversation.json", "utf-8"));

for (const sessionData of data.sessions) {
    const session = honcho.session(sessionData.id);
    session.addPeers([user, assistant]);

    const messages = sessionData.messages.map((msg: any) =>
        msg.role === "user" ? user.message(msg.content) : assistant.message(msg.content)
    );

    session.addMessages(messages);
}
```
Writes return fast while Neuromancer (Honcho's family of small reasoning models that extract explicit facts and logical conclusions) reasons in the background, so allow a short wait before querying.
## 5. Query with peer.chat and honcho.chat
Peer chat answers about one peer. Workspace chat asks across all peers in the workspace.
```python
response = user.chat("What should I know about this user? 3 sentences max")
print(response)
```
```typescript
user.chat("What should I know about this user? 3 sentences max").then((response) => {
  console.log(response);
})
```
```python
response = honcho.chat("What themes appear across every peer in this workspace?")
```
```typescript
const response = await honcho.chat("What themes appear across every peer in this workspace?");
```
Reasoning levels control cost and depth (vendor-reported prices): minimal $0.001, low $0.01, medium $0.05, high $0.10, max $0.50.
## 6. Get context() with token budgets
The `context()` method returns formatted history for a session. By default it blends summary plus messages. Set `tokens` to cap size. When capped, it uses about 40 percent summary and 60 percent recent messages (vendor-reported).
```python
# Limit context to 1500 tokens
context = session.context(tokens=1500)

# Limit context to 3000 tokens for larger conversations
context = session.context(tokens=3000)
```
```typescript
(async () => {
    // Limit context to 1500 tokens
    const context = await session.context({ tokens: 1500 });

    // Limit context to 3000 tokens for larger conversations
    const context = await session.context({ tokens: 3000 });
})();
```
Summary control:
```python
# Get context with summary enabled -- will contain both summary and messages
context = session.context(summary=True)

# Combine summary=False with token limits to get more messages
context = session.context(summary=False, tokens=2000)
```
```typescript
(async () => {
    // Get context with summary enabled -- will contain both summary and messages
    const context = await session.context({ summary: true });

    // Combine summary=False with token limits to get more messages
    const context = await session.context({
      summary: false,
      tokens: 2000
    });
})();
```
## 7. Add peer representation, search, and session limits
Add `peer_target` to include that peer's representation (learned conclusions) and peer card (biographical facts). Add `search_query` for semantic filtering. Add `limit_to_session` for only the current session.
```python
# Get context with peer representation included
context = session.context(
    tokens=2000,
    peer_target="user-123"  # Include representation of user-123
)

# Access the representation and peer card
print(context.peer_representation)  # String representation
print(context.peer_card)            # List of peer card items

# Get representation from a specific peer's perspective
context = session.context(
    tokens=2000,
    peer_target="user-123",
    peer_perspective="assistant"  # From assistant's viewpoint
)

# Or use a named scope as the perspective source (requires peer_target;
# mutually exclusive with peer_perspective)
context = session.context(
    tokens=2000,
    peer_target="user-123",
    scope="therapy",
)
```
```python
context = session.context(
    tokens=2000,
    peer_target="user-123",
    search_query="What are my coding preferences?",
    search_top_k=10,           # Number of relevant conclusions to fetch
    search_max_distance=0.8,   # Max semantic distance (0.0-1.0)
    include_most_frequent=True, # Include most frequent conclusions
    max_conclusions=25        # Cap total conclusions
)
```
```python
# Get context limited to this session's conclusions only
context = session.context(
    tokens=2000,
    peer_target="user-123",
    limit_to_session=True  # Only conclusions from this session
)
```
## 8. Convert to LLM (Large Language Model) formats
Convert context for OpenAI (an LLM provider) or Anthropic (the maker of Claude, another LLM provider) chat APIs (Application Programming Interfaces). You must name the assistant peer so roles are labeled correctly.
```python
# Create peers
alice = honcho.peer("alice")
assistant = honcho.peer("assistant")

# Add some conversation
session.add_messages([
    alice.message("What's the weather like today?"),
    assistant.message("It's sunny and 75°F outside!")
])

# Get context and convert to OpenAI format
context = session.context()
openai_messages = context.to_openai(assistant=assistant)

# The messages are now ready for OpenAI API
print(openai_messages)
# [
#   {"role": "user", "content": "What's the weather like today?"},
#   {"role": "assistant", "content": "It's sunny and 75°F outside!"}
# ]
```
```python
# Get context and convert to Anthropic format
context = session.context()
anthropic_messages = context.to_anthropic(assistant=assistant)

# Ready for Anthropic API
print(anthropic_messages)
```
Full OpenAI (an LLM provider) loop:
```python
import openai
from honcho import Honcho

# Initialize clients
honcho = Honcho()
openai_client = openai.OpenAI()

# Set up conversation
session = honcho.session("support-chat")
user = honcho.peer("user-123")
assistant = honcho.peer("support-bot")

# Add conversation history
session.add_messages([
    user.message("I'm having trouble with my account login"),
    assistant.message("I can help you with that. What error message are you seeing?"),
    user.message("It says 'Invalid credentials' but I'm sure my password is correct")
])

# Get context for LLM
messages = session.context(tokens=2000).to_openai(assistant=assistant)

# Add new user message and get AI response
messages.append({
    "role": "user",
    "content": "Can you reset my password?"
})

response = openai_client.chat.completions.create(
    model="gpt-4",
    messages=messages
)

# Add AI response back to session
session.add_messages([
    user.message("Can you reset my password?"),
    assistant.message(response.choices[0].message.content)
])
```
## 9. Streaming
Streaming means answers arrive piece by piece instead of all at once. Use it for peer chat and workspace chat when you want low waiting time in a user interface.
```python
# Stream a peer-chat answer in chunks
for chunk in user.chat("What should I know about this user?", stream=True):
    print(chunk, end="", flush=True)
```
```typescript
// Stream a peer-chat answer in chunks
for await (const chunk of user.chat("What should I know about this user?", { stream: true })) {
  process.stdout.write(chunk);
}
```
Check the queue-status helper first if background Neuromancer reasoning is still running, or subscribe to webhooks (automatic notifications sent to your server) for completion before streaming long answers.
## 10. Structured outputs
Structured output means the answer comes back in a fixed shape, such as JSON (JavaScript Object Notation), so your code can read fields safely.
```python
# Ask for a fixed JSON shape
schema = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "goals": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "number"}
    },
    "required": ["summary", "goals"]
}

response = user.chat(
    "Summarize this user in the given schema",
    response_format={"type": "json_schema", "schema": schema}
)
print(response)
```
```typescript
// Ask for a fixed JSON shape
const response = await user.chat("Summarize this user in the given schema", {
  responseFormat: { type: "json_schema", schema }
});
console.log(response);
```
## 11. Key scoping, queue-status, and webhooks
Keys exist at admin, workspace, peer, and session level. Workspace chat needs a workspace-level or higher key. The context() `scope` option needs a workspace-level or admin-level key. Writes are fast because reasoning runs after the call, so poll queue-status or use webhooks (automatic notifications) before trusting fresh chat answers.
```python
# Check background reasoning progress before querying fresh writes
status = honcho.queue_status()
print(status)

# Peer chat with an explicit reasoning level
response = user.chat("What should I know about this user?", reasoning="low")
print(response)
```
## 12. Local self-host, file uploads, and ecosystem
Run your own stack with the CLI (Command Line Interface, a text-command tool):
```bash
uv tool install honcho-cli
honcho start --setup
```
This path uses Docker (a tool that runs packaged software containers) plus your own LLM (Large Language Model) provider key, and the core code is AGPL (Affero General Public License, an open-source license that requires sharing changes) licensed. File uploads such as PDF (Portable Document Format), TXT (plain text), or JSON (JavaScript Object Notation) files become messages tied to a peer. Connect agents through the MCP (Model Context Protocol) server and `npx skills add plastic-labs/honcho`, editor plugins for Claude Code, Codex, Cursor, OpenCode, OpenClaw, DeepSeek Harness, Hermes, Zo, Paperclip, and SillyTavern, frameworks such as LangGraph, CrewAI, Vercel AI SDK, and n8n, and bots or ingestors for Discord, Telegram, Gmail, and Granola.
```python
# File content becomes peer messages
session.add_messages([
    user.message(open("notes.pdf", "rb").read()),
])
```
**Covers:** quickstart.md, get-context.md, chat.md (docs v3, retrieved 2026-09-10)
