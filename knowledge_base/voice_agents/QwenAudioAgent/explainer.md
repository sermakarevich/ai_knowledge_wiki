> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# QwenAudio/qwen-audio-agent — In Plain Language

## What is this about?

qwen-audio-agent is a realtime voice runtime for talking to an AI agent.

The normal problem with voice assistants: you ask something, then wait in
silence while it looks things up, calls tools, or runs a task.

This project splits the job in two. A voice frontend keeps the conversation
flowing in the foreground, while a backend coding agent does the heavy work
in the background. When the work finishes, it rejoins the conversation with
something like "It's ready."

You always talk to the same assistant. Simple questions get answered
immediately; only work that needs tools or time is handed off behind the scenes.

## Why does it matter?

Most voice interfaces are half-duplex: you talk, then the system talks, and
nobody can interrupt. Long tasks freeze the whole conversation.

This project matters because it removes that freeze:

- You can interrupt naturally, keep chatting across many turns, and ask
  "how is that task going?" or "cancel it" at any time.
- Conversation and background work run in parallel instead of blocking
  each other.
- You can run several independent tasks at once and get each result back
  in the same conversation for follow-up questions and fixes.
- It reuses agents you already use — Qwen Code, OpenCode, OpenClaw, Claude
  Code, Codex, and others — instead of forcing a new agent on you.
- It remembers you across sessions, with per-user personalization and
  long-term memory.

In short: the assistant stays present whether it is chatting, thinking,
or working.

## How does it work?

Think of three parts: a mouth and ears, a coordinator, and hands.

1. **The voice frontend (mouth and ears).** This handles realtime talking
   and listening, including interruption. The default is Qwen Audio 3.0
   Realtime in the cloud, but you can swap in OpenAI Realtime, Google
   Gemini Live, StepAudio, a self-hosted speech-to-speech service, or
   MiniCPM-o. No core logic changes are needed to add a new voice service.

2. **The Gateway (coordinator).** This sits in the middle. It decides:
   answer now, or delegate to the back? Direct questions are answered on
   the spot. Anything needing tools, files, code, or sustained effort is
   sent to the backend agent as an asynchronous task with progress tracking.

3. **The backend agent (hands).** This is your preferred coding agent,
   connected with one-click setup. It reuses that agent's model settings,
   tools, skills, and login. It can run multiple tasks at once, report
   status, and return results into the live conversation.

4. **Three ways to talk to it.** A browser WebUI, a terminal interface,
   and a desktop floating orb for macOS, Windows, and Linux. The desktop
   orb can idle-sleep, wake on voice, and restyle its appearance.

5. **Setup is small.** Install with npm, run a config command, paste in an
   API key, pick a voice model and a backend agent, then start the Gateway
   plus the WebUI or terminal UI.

Under the hood the repo pins Node 22, locks all dependencies, and uses
lint rules to keep the voice, task, and agent code from tangling together.

## Where can this be used?

- **Desktop productivity:** talk while the agent edits files, writes code,
  searches the web, or runs long jobs — no need to watch a terminal.
- **Hands-busy settings:** workshops, labs, kitchens, or accessibility
  setups where typing is inconvenient but oversight is still wanted.
- **Smart cockpit and embodied devices:** voice in front, task execution
  behind, with the same foreground/background split.
- **Customer help and live assistance:** one conversation stays open while
  lookups and multi-step fixes run in parallel.
- **Personal long-running helper:** timers, notes, recall, and memory
  features support a persistent assistant that learns preferences over time.
- **Local or private deployments:** self-hosted voice services and
  localhost-by-default networking suit privacy-sensitive environments.

## Conclusions & takeaways

- The core idea is presence: never leave the user in dead air while work
  happens. Split talking from doing.
- Swappability is the second idea: voice frontends and backend agents plug
  in independently, so you are not locked to one vendor or model.
- Async-by-default task handling — parallel tasks, progress checks,
  cancellation, automatic return to chat — is what makes voice usable for
  real work rather than just Q&A.
- Trade-offs remain: cloud voice means audio goes to a provider; local
  options exist but some lack backend delegation. Memory and camera
  features are powerful but need careful configuration.
- If you remember one sentence: keep talking in front, keep working
  behind, and bring every result back to the same conversation.

## Jargon decoder

| Term | What it means in plain language |
| --- | --- |
| Full-duplex voice | Both sides can talk and interrupt at once, like a phone call, not walkie-talkie turns. |
| Realtime frontend | The voice service that hears you and speaks back instantly. |
| Backend agent | The worker AI (e.g. Qwen Code, OpenCode) that uses tools and finishes tasks quietly. |
| Gateway | The middleman program that routes speech to answers or background tasks. |
| ACP | A standard plug format letting different coding agents connect to the Gateway. |
| MCP / Skills | Extra tool packs and abilities the backend agent can borrow. |
| Async task | A job that runs in the background while you keep talking. |
| TUI | A text-based control panel inside the terminal. |
| Floating orb | The small always-on-top desktop bubble you talk to. |
| Tailnet / LAN mode | Ways to reach your Gateway over a private network or local Wi-Fi. |
