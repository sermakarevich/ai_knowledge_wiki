---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: stimm-ai/stimm
### Q1. What is Optimistic VUI and what four behaviors define it in Stimm?
> [!tip]- Answer
> Optimistic VUI is the voice equivalent of optimistic UI: the system starts behaving usefully as soon as it has enough confidence to move the conversation forward instead of waiting for the full reasoning chain. Its four behaviors are acknowledging the user immediately, starting to speak as early as possible, keeping the response interruptible and steerable, and letting deeper reasoning continue in parallel. See [[wiki/01-overview|Overview]].
### Q2. Which two agents form Stimm's dual-agent runtime and how do they communicate?
> [!tip]- Answer
> The VoiceAgent is optimized for low-latency spoken interaction and owns the live turn, while the Supervisor is optimized for deeper reasoning, planning, and tool orchestration. They exchange typed StimmProtocol messages over LiveKit data channels, so the Supervisor can watch the transcript and steer asynchronously without blocking the first response. See [[wiki/01-overview|Overview]].
### Q3. What are Stimm's three runtime modes and four pre-TTS buffering levels, including defaults?
> [!tip]- Answer
> The modes are autonomous (voice agent acts independently), relay (voice agent only speaks supervisor instructions), and hybrid (default: autonomous first response with supervisor steering). Buffering levels are NONE (send tokens immediately), LOW (buffer until word completion), MEDIUM (default: buffer until 4 words or punctuation), and HIGH (buffer until punctuation), trading raw latency against cleaner spoken delivery. See [[wiki/01-overview|Overview]].
### Q4. What is the wizard-first provider onboarding flow and what must happen after installing extras?
> [!tip]- Answer
> Onboarding UIs use the catalog API (get_provider_catalog()) to display providers and parameters first, then derive an install command from the user selection (e.g. pip install stimm[deepgram,openai]) so only chosen provider plugins are installed and nothing is vendored in the wheel. After installation the Python process must be restarted before instantiating LiveKit plugin classes. See [[wiki/01-overview|Overview]].
### Q5. What hard rules does AGENT.md impose on apps integrating Stimm's provider wizard?
> [!tip]- Answer
> Apps must build wizard discovery UI from get_provider_catalog(), never from list_runtime_providers(), and must derive install commands via required_extras_for_selection(...) or extras_install_command(...) installed in the same environment that runs the app. They must restart the Python process after extras installation, persist only user choices and parameter values, and never store provider module paths or expose secrets in logs, telemetry, or UI snapshots. See [[wiki/02-top-level-files|Top-level-files]].
### Q6. What hooks and versioning back Stimm's repo hygiene at the repo root?
> [!tip]- Answer
> Pre-commit runs ruff format and ruff check --fix for Python, bandit over src/, pip-audit, and npm run check typechecking for packages/protocol-ts changes. Release-please pins the root package at 0.1.13 and packages/protocol-ts at 0.1.3 with linked versions, while .gitignore excludes env/venv dirs, Python and Node build outputs, caches, logs, and the root-owned v1 leftover bin/. See [[wiki/02-top-level-files|Top-level-files]].
### Q7. Would you recommend Stimm's hybrid mode for a customer-support voice agent that needs fast answers plus background retrieval, and why?
> [!tip]- Answer
> Yes, hybrid mode fits that need: the VoiceAgent gives an immediate autonomous first response so callers never wait on the full retrieval chain, while the Supervisor runs tools and retrieval in parallel and steers the turn asynchronously. The main caveats are the extra operational complexity of two cooperating agents over LiveKit data channels and tuning the buffering level for your latency-versus-fluency tradeoff. See [[wiki/01-overview|Overview]].
