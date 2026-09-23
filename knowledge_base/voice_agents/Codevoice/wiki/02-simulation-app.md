> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# 1. Simulation App (`src/apps/simulation/`)
**In one sentence:** The Simulation App is the heart of the AI functionality, running `run_ai_bot(room_url, token, room_name)` as a `Audio In → STT → User Aggregator → LLM → TTS → Audio Out` Pipecat pipeline over LiveKit with `on_first_participant_joined` / `on_participant_left` handlers, launched via `python src/manage.py run_bot` and joined via `get_user_token`, alongside the Interviews/Users/Config apps and a Docker + `.env` + migrate setup.
## Key points
- Main pipeline function is `run_ai_bot(room_url, token, room_name)`, which initializes STT/LLM/TTS, creates the LiveKit transport, builds the Pipecat pipeline, sets up event handlers, and manages conversation context.
- Audio flows as `Audio In → STT → User Aggregator → LLM → TTS → Audio Out`, with Transcription and Synthesized Speech as side outputs.
- `on_first_participant_joined` greets the user and starts the interview; `on_participant_left` cleans up when the user disconnects.
- `python src/manage.py run_bot` loads LiveKit credentials from Django settings, generates a bot token, and launches `run_ai_bot()` with asyncio; `python src/manage.py get_user_token` creates a LiveKit access token with identity/permissions and prints it with the `✅ HERE IS YOUR TOKEN` prefix.
- Interview data model is `Question` (`text`, `difficulty` EASY/MEDIUM/HARD, `expected_key_points`), `InterviewSession` (state machine `Started` → `Completed`/`Failed` with `user`, `status`, `total_score`, `started_at`, `completed_at`), and `InterviewTurn` (`session`, `question`, `ai_message`, `user_transcript`, `audio_file`, `score` 0–10).
- Custom `User` inherits from `AbstractUser` and uses UUIDs instead of sequential integers to prevent ID enumeration attacks.
- Setup requires Docker Desktop, Python 3.10+, and Deepgram + Krutrim API keys; `docker-compose up -d` provides `codevoice_db`, `codevoice_redis`, `codevoice_livekit`, and `.env` must define `DEBUG`, `DATABASE_URL`, `REDIS_URL`, `DEEPGRAM_API_KEY`, `KRUTRIM_API_KEY`, `LIVEKIT_API_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`.
---
## `bot.py` — main AI pipeline
The heart of the AI functionality.

**Key Function**: `run_ai_bot(room_url, token, room_name)`

**Responsibilities**:
- Initialize AI services (STT, LLM, TTS)
- Create LiveKit transport
- Build Pipecat pipeline
- Set up event handlers
- Manage conversation context

**Event Handlers**:
- `on_first_participant_joined`: Greet user, start interview
- `on_participant_left`: Clean up when user disconnects

**Pipeline Flow**:
```
Audio In → STT → User Aggregator → LLM → TTS → Audio Out
         ↓                                        ↓
    Transcription                           Synthesized Speech
```

## `management/commands/run_bot.py` — start the bot
**What it does**:
1. Loads LiveKit credentials from Django settings
2. Generates bot token
3. Launches `run_ai_bot()` with asyncio

**Usage**:
```bash
python src/manage.py run_bot
```

**Expected Output** (from Setup Step 5):
```
🚀 LiveKit AI starting
🤖 AI connecting to room: interview-room-1
✅ Connected to interview-room-1
🎧 Deepgram STT initialized
🎙️ Deepgram TTS initialized
⏳ Waiting for participants...
```

## `management/commands/get_user_token.py` — user join token
**What it does**:
1. Creates a LiveKit access token
2. Sets user identity and permissions
3. Prints token to console

**Usage**:
```bash
python src/manage.py get_user_token
```

**Output**:
```
✅ HERE IS YOUR TOKEN (Copy the long string below):
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Interviews App (`src/apps/interviews/`)
Manages interview structure and data persistence.

| Model | Fields / behavior |
|-------|-------------------|
| `Question` | `text`, `difficulty` (EASY/MEDIUM/HARD), `expected_key_points`; used for grading and evaluation |
| `InterviewSession` | Tracks a user's interview attempt; state machine `Started` → `Completed`/`Failed`; fields `user`, `status`, `total_score`, `started_at`, `completed_at` |
| `InterviewTurn` | Granular tracking of each Q&A exchange; fields `session` (FK to InterviewSession), `question` (FK to Question), `ai_message` (what the bot asked), `user_transcript` (what you said), `audio_file` (recording for audit trails), `score` (AI-generated score 0-10) |

## Users App (`src/apps/users/`)
Custom authentication system. Custom `User` model inherits from `AbstractUser` with security feature: uses UUIDs instead of sequential integers for primary keys, preventing ID enumeration attacks.

## Configuration (`src/config/`)
**`settings.py`**: Django settings with environment variable management via `django-environ` reading `.env`; registers apps `daphne`, `users`, `interviews`, `simulation`; CORS configured for frontend connections; Database PostgreSQL via Docker; Cache/Queue Redis for Celery tasks.

Required environment variables:
```ini
DEBUG=on
DATABASE_URL=postgres://user:password@localhost:5432/codevoice
REDIS_URL=redis://localhost:6379/0
DEEPGRAM_API_KEY=your_deepgram_key
KRUTRIM_API_KEY=your_krutrim_key
LIVEKIT_API_URL=ws://localhost:7880
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
```

**`asgi.py`**: ASGI entry point for async server; enables WebSocket support (for future features); currently uses Daphne as ASGI server.

## Setup & Installation
Prerequisites: Docker Desktop (for Redis, Postgres, LiveKit), Python 3.10+, API keys Deepgram and Krutrim.

| Step | Command | Verifies / creates |
|------|---------|--------------------|
| 1. Start Services | `docker-compose up -d` | `codevoice_db` (PostgreSQL), `codevoice_redis` (Redis), `codevoice_livekit` (LiveKit Server) |
| 2. Environment Configuration | Create `.env` in project root (same 8 vars above; example uses `LIVEKIT_API_KEY=devkey`, `LIVEKIT_API_SECRET=secret`) | — |
| 3. Install Dependencies | `pip install -r requirements.txt` | `pipecat-ai`, `livekit`, `django`, `deepgram-sdk`, `openai` (LLM client for Krutrim) |
| 4. Database Setup | `python src/manage.py migrate` | Tables for Users, Questions, Interview Sessions, Interview Turns |
| 5. Run the Bot | `python src/manage.py run_bot` | Output quoted above |
| 6. Get User Token | `python src/manage.py get_user_token` (new terminal) | Copy the token from the output |
| 7. Connect from Browser | Open `src/templates/test_room.html`, paste token, click "Connect", allow microphone access, start talking | — |

## Usage Workflow — complete interview flow
1. **Start Services**: `docker-compose up -d`
2. **Start Bot**: `python src/manage.py run_bot`
3. **Generate Token**: `python src/manage.py get_user_token`
4. **Open Browser**: Navigate to `test_room.html`
5. **Paste Token**: Enter the generated token
6. **Connect**: Click "Connect" button
7. **Interview Begins**: Bot greets you and asks first question
8. **Conversation**: Answer naturally, bot responds with feedback
9. **End Interview**: Close browser or click disconnect

## Troubleshooting
- **Bot Not Responding** — check: 1) bot running (`python src/manage.py run_bot`), 2) LiveKit container up (`docker ps | grep livekit`), 3) browser microphone permission, 4) refresh browser page (verbatim: "important for token updates!").
- **Connection Failed** — verify: 1) LiveKit URL matches in `.env` and `test_room.html`, 2) token not expired (tokens expire after ~6 hours), 3) generate fresh token via `python src/manage.py get_user_token`.
- **No Audio Heard** — debug: 1) check browser console for errors, 2) ensure audio element is created (inspect DOM), 3) manually click play on audio element, 4) verify Deepgram API key is valid.
- **Bot Interrupting Too Early** — the `LocalSmartTurnAnalyzerV3` model controls turn detection; currently uses default sensitivity; can be tuned in `bot.py` if needed.

## Roadmap / Future Enhancements
1. **Orchestrator API**: REST endpoint to start/stop interviews; programmatic control from frontend.
2. **WebSocket Integration**: real-time status updates, live transcription display, score visualization.
3. **Frontend Dashboard**: user login/registration, interview history, performance analytics, question bank management.
4. **Advanced Evaluation**: automatic scoring based on key points, code execution for programming questions, multi-turn follow-up questions.
5. **Recording & Playback**: save interview recordings, review sessions, export transcripts.

## Technology Stack
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Django 5 | Control plane, API, data persistence |
| **Database** | PostgreSQL | User data, questions, sessions |
| **Cache/Queue** | Redis + Celery | Task queue, caching |
| **Real-time** | LiveKit | WebRTC audio routing |
| **AI Pipeline** | Pipecat | Stream processing framework |
| **STT** | Deepgram | Speech-to-text |
| **LLM** | Krutrim (GPT-OSS-120b) | Conversational AI |
| **TTS** | Deepgram | Text-to-speech |
| **ASGI Server** | Daphne | Async/WebSocket support |

Learning resources quoted verbatim: Pipecat Documentation https://docs.pipecat.ai, LiveKit Docs https://docs.livekit.io, Deepgram API https://developers.deepgram.com, Django Async https://docs.djangoproject.com/en/5.0/topics/async/. License and Contributing sections are placeholders (`[Your License Here]`); closing line verbatim: "**Built with ❤️ using Pipecat, LiveKit, and Django**".

**Covers:** codebase deep dive (simulation/interviews/users apps, config), setup Steps 1–7, usage workflow, troubleshooting, roadmap, and tech stack.
