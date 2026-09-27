> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# ReAct: Synergizing Reasoning and Acting in Language Models — In Plain Language

## What is this about?

Think of a very keen junior assistant sitting at a computer terminal. You give it a job in plain English, and instead of answering once and stopping, it works in a loop: it thinks, tries a tool, looks at the result, then decides what to do next. That loop — send a request, use tools, read the results, repeat — is the heart of this project.

The project is a small, teachable coding assistant (called a harness) written in Go. It connects a chat-style language model to real tools (like files and outside services), remembers past sessions, and shows everything in a terminal window. Around the code there is also a course: step-by-step lessons, short recipes, and practice exercises, in both English and Spanish.

In short: one conversation manager runs the loop, a swappable connector talks to the language model, tools do the real work, memory keeps context small but persistent, and a terminal interface ties it together.

## Why does it matter?

- Talking to a language model alone is not enough — real work needs tools, repeated steps, and a stop rule so the assistant does not loop forever.
- Swapping models should not mean rewriting everything, so the model connector is kept separate from the loop.
- Conversations get long and models forget, so the project trims old context safely and saves session notes for later.
- Outside capabilities should be easy to plug in, so external tool servers can be bridged in with a standard setup.
- Beginners need a way in, so the same ideas are taught three ways: story-like lessons, copy-paste recipes, and hands-on exercises.

## How does it work?

1. **Start a conversation.** The `Agent` object owns one conversation: the model connector, the tool list, the memory, and the message history.
2. **Send your request.** `Send` adds your message to the history and starts the `loop`.
3. **Run the loop.** Each turn, the agent tidies up history, asks the model for the next step, and saves the reply.
4. **Use tools when asked.** If the model requests a tool, the agent runs it, then feeds the result back in as a new message so the model can react to it.
5. **Know when to stop.** The loop ends when the model stops asking for tools, or fails clearly when the `MaxTurns` cap (50 for the main assistant) is reached.
6. **Route commands.** Lines starting with `/` run as built-in commands; everything else goes into the conversation loop.
7. **Delegate bigger jobs.** Sub-assistants appear as `delegate_<name>` tools that take a single `task` description.
8. **Swap the model freely.** The loop only sees three operations — `Send`, `Model`, `SetModel` — with Anthropic and OpenAI connectors plus a scripted mock for tests.
9. **Track cost.** Both live connectors add up usage and estimate cost in dollars, sharing totals with sub-assistants.
10. **Keep context small.** At the top of each turn, a compaction step trims old messages at safe boundaries, never splitting a tool call from its result; one mode keeps the last N messages, another replaces old chat with a short summary.
11. **Remember across sessions.** A session store saves one markdown file per session plus an index, recalls matches by simple text search, and injects up to the last 5 summaries into the next session.
12. **Plug in outside tools.** External MCP servers are connected, their tools are listed and registered under `<server>_<name>`, failed servers are skipped with a warning, and file writes are previewed as diffs with 3 lines of context.
13. **Show it all.** The terminal interface displays the conversation, an input box, a debug panel, and approval pop-ups for sensitive actions.

## Where can this be used?

- As a learning example for building your own chat assistant with tools in Go.
- As a template where you swap language-model backends without touching the main loop.
- As a test bed for trying context-trimming and session-memory ideas.
- As a starter for connecting outside tool servers through a standard configuration.
- As a classroom path: read the guided lessons, copy a recipe to add a tool, provider, or permission rule, then attempt the graded exercises.

## Conclusions & takeaways

- The whole design is a loop around three things: ask the model, run what it asked for, show it the result.
- Keeping the model connector, the tool list, and the memory as separate pieces makes each one easy to change or test.
- Honest limits, taken only from the digest: the loop is capped by a fixed turn count; trimming and summaries can drop detail; session recall is a simple substring scan, not smart search; only the last few session summaries are reused; unknown models report no cost estimate; a failed tool server is skipped rather than retried; non-text tool output becomes a placeholder; identical file writes show a "no changes" marker.
- If you understand the loop, the safe trim point, and the three learning tracks, you understand most of the project.

## Jargon decoder

| Term | What it means here |
| ---- | ------------------ |
| Agent loop | The repeat cycle: ask the model, run tools, feed results back, until done or capped |
| Provider | The plug-in connector that talks to a specific language model |
| Mock provider | A fake connector with canned answers, used for tests |
| MaxTurns | The maximum number of loop rounds before giving up with an error |
| Tool | An action the model can request, such as writing a file or calling a sub-assistant |
| MCP | A standard way to expose tools from outside servers so the assistant can use them |
| Compaction | Trimming old conversation so it still fits, done at safe message boundaries |
| Session memory | Saved notes from past sessions, recalled later by simple text search |
| Diff preview | A before/after view of a file change shown for approval |
| TUI | The terminal window interface with conversation, input box, and debug panel |
