> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Patter is the open-source Python/TypeScript SDK that gives an AI agent a phone number by owning the full voice stack between the application and the phone network.
## Key points
- Patter gives an AI agent a phone number and handles everything between the agent and the phone network: agent loop, LLM, STT, TTS, real-time voice, audio processing, and carrier (README.md:38).
- The SDK ships in Python (`pip install getpatter`) and TypeScript (`npm install getpatter`) with the same surface, hooks, and events at full parity (README.md:40).
- Every stack layer is provider-swappable in one line across LLM, STT, TTS, realtime engine, and carrier (README.md:41).
- The stack composes in Realtime, Pipeline, or Hybrid mode and claims 27+ provider integrations, 3 voice modes, and 2 SDKs at parity (README.md:46-48).
- On top of the stack sit an automatic LLM fallback chain, identical cross-carrier tools / call transfer / guardrails, and a vendor-neutral OpenTelemetry call trace (README.md:59).
- Local runs use a built-in tunnel and dashboard or a terminal-simulated call with no phone required, with credentials read from environment variables (README.md:42, README.md:79).
- Anonymous opt-out telemetry collects only SDK version and bucketed provider/model and call facts, never content or secrets (README.md:121).
---
## About
Patter is the open-source SDK that gives your AI agent a phone number; the builder supplies the agent while Patter owns the agent loop, language model, speech-to-text, text-to-speech, real-time voice, audio processing, and telephony carrier (README.md:38).
- **Build** with one API in Python or TypeScript — same surface, same hooks, same events, at full parity (README.md:40).
- **Choose** the provider for every layer and swap any of them with one line (README.md:41).
- **Run** locally with a built-in tunnel and dashboard, or simulate a whole call from the terminal — no phone required (README.md:42).
## How It Works
Patter is the **full voice stack** between the application and the phone network, running the agent loop and owning every layer of the call while the user picks the provider for each one, composed in **Realtime**, **Pipeline**, or **Hybrid** mode (README.md:46).
> **27+ provider integrations across the voice stack · 3 voice modes · 2 SDKs (Python & TypeScript) at parity.** (README.md:48)
| Layer | Choose from (README.md:50-57) |
|---|---|
| **LLM** — text generation | OpenAI · Anthropic · Google Gemini · Groq · Cerebras |
| **STT** — speech-to-text | Deepgram · AssemblyAI · Cartesia · Soniox · Speechmatics · Whisper · Fish Audio |
| **TTS** — text-to-speech | ElevenLabs · OpenAI · Cartesia · LMNT · Rime · Telnyx · Fish Audio |
| **Realtime** — all-in-one voice | OpenAI Realtime · Gemini Live · Ultravox · ElevenLabs ConvAI |
| **Telephony** — phone carriers | Twilio · Telnyx · Plivo |
| **Audio** — VAD & suppression | Silero VAD · Krisp · DeepFilterNet |
Cross-cutting behavior on top of the stack: automatic **LLM fallback chain** (provider failover mid-call), built-in **tools / call transfer / guardrails** identical on every carrier, and vendor-neutral **OpenTelemetry** trace of each call (README.md:59).
## Quickstart
Provider and carrier credentials are read from environment variables (e.g. `TWILIO_ACCOUNT_SID`, `OPENAI_API_KEY`); swapping `Twilio` for `Telnyx` or `Plivo` changes carrier (README.md:79).
### TypeScript (README.md:81-97)
```bash
npm install getpatter
```
```typescript
import { Patter, Twilio, OpenAIRealtime } from "getpatter";

const phone = new Patter({ carrier: new Twilio(), phoneNumber: "+15550001234" });
const agent = phone.agent({
  engine: new OpenAIRealtime(),
  systemPrompt: "You are a friendly receptionist for Acme Corp.",
  firstMessage: "Hello! How can I help?",
});
await phone.serve({ agent, tunnel: true });
```
Exact parameter names: `carrier`, `phoneNumber`, `engine`, `systemPrompt`, `firstMessage`, `agent`, `tunnel` (README.md:90-96).
### Python (README.md:99-115)
```bash
pip install getpatter
```
```python
from getpatter import Patter, Twilio, OpenAIRealtime

phone = Patter(carrier=Twilio(), phone_number="+15550001234")
agent = phone.agent(
    engine=OpenAIRealtime(),
    system_prompt="You are a friendly receptionist for Acme Corp.",
    first_message="Hello! How can I help?",
)
await phone.serve(agent, tunnel=True)
```
Exact parameter names: `carrier`, `phone_number`, `engine`, `system_prompt`, `first_message`, `tunnel` (README.md:108-114).
`tunnel: true` spawns a Cloudflare quick tunnel and points the number at it for local dev; production uses a static `webhook_url` or ngrok (README.md:117).
## Skills for Coding Agents
For Claude Code, Claude Desktop, OpenClaw, Hermes, Cursor, Codex, or other AI coding agents, install via `npx skills add patterai/skills`; the bundle works in ~55 agent harnesses consuming the Anthropic Agent Skills standard, and skills live in `PatterAI/skills` (README.md:67-75).
## Telemetry
Patter collects anonymous, opt-out usage data (SDK version, bucketed provider/model and call facts), never call content, prompts, phone numbers, keys, or free text (README.md:121).
| Opt-out / inspect flag | Form (README.md:123) |
|---|---|
| Constructor (Python) | `Patter(telemetry=False)` |
| Constructor (TypeScript) | `new Patter({ telemetry: false })` |
| CLI | `getpatter telemetry disable` |
| Env disable | `PATTER_TELEMETRY_DISABLED=1` (also honours `DO_NOT_TRACK=1`; auto-off in CI/tests) |
| Inspect without sending | `PATTER_TELEMETRY_DEBUG=1` |
## Templates
Each template is a self-contained repo — clone, add `.env`, and run, with Python and TypeScript both included (README.md:127).
| Template | Description | Repo (README.md:129-138) |
|---|---|---|
| **Inbound Agent** | Answer calls as a restaurant booking assistant | `patter-inbound-agent` |
| **Outbound Calls** | Place calls with AMD and voicemail drop | `patter-outbound-calls` |
| **Tool Calling** | CRM lookup + ticket creation via webhook tools | `patter-tool-calling` |
| **Custom Voice** | Pipeline mode: Deepgram STT + ElevenLabs TTS | `patter-custom-voice` |
| **Dynamic Variables** | Personalize prompts per caller using CRM data | `patter-dynamic-variables` |
| **Custom LLM** | Bring your own model | `patter-custom-llm` |
| **Dashboard** | Real-time monitoring with cost + latency tracking | `patter-dashboard` |
| **Production Setup** | Everything enabled: tools, guardrails, recording, dashboard | `patter-production` |
```bash
git clone https://github.com/PatterAI/patter-inbound-agent
cd patter-inbound-agent
cp .env.example .env    # fill in your keys
cd python && pip install -r requirements.txt && python main.py
```
(README.md:141-145). License is MIT — see `LICENSE` (README.md:167).
**Covers:** README.md (repo overview, provider stack, quickstarts, telemetry, templates); top-level shape note `top-level-files/`
