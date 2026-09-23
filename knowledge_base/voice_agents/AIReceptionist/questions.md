---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: AI Receptionist -- Open Source, Self-Hosted, No Compromises

### Q1. What is AIReceptionist's core technical claim, and how does it differ from a typical SaaS AI receptionist?

> [!tip]- Answer
> AIReceptionist uses direct speech-to-speech via OpenAI's Realtime API (gpt-realtime-2.1) instead of a cascaded STT-to-LLM-to-TTS pipeline, giving sub-second responses with model-native turn-taking rather than 1–3 second robotic replies. The comparison table frames it as metered API-key usage with no platform fee, operator-hosted data, full source customization, and built-in multi-business support versus $200–500/month SaaS with dashboard-only control and vendor lock-in. See [[wiki/01-ai-receptionist-open-source-self-hosted-no-compr|AI Receptionist -- Open Source, Self-Hosted, No Compromises]].

### Q2. What broke on 2026-06-03, and what is the required auth fix?

> [!tip]- Answer
> OpenAI sunset the Realtime Beta API on 2026-06-03, so the ChatGPT/Codex OAuth path (`voice.auth.type: oauth_codex`) now connects the call but the caller hears only silence. Deployments must set `voice.auth.type: api_key` with `voice.model: gpt-realtime-2.1` reading a standard `sk-...` key with Realtime access. See [[wiki/01-ai-receptionist-open-source-self-hosted-no-compr|AI Receptionist -- Open Source, Self-Hosted, No Compromises]].

### Q3. What does it take to deploy AIReceptionist for one business?

> [!tip]- Answer
> Prerequisites are Python 3.11+, an OpenAI API key with Realtime access, a LiveKit server, and a SIP trunk (Twilio/Telnyx) with a phone number pointed at the LiveKit SIP URI with REFER enabled. Setup clones the repo, installs with `pip install -e .`, fills `.env` (`LIVEKIT_URL`, keys, `OPENAI_API_KEY`), copies `config/businesses/example-dental.yaml`, and runs `python -m receptionist.agent dev`. See [[wiki/01-ai-receptionist-open-source-self-hosted-no-compr|AI Receptionist -- Open Source, Self-Hosted, No Compromises]].

### Q4. How do message delivery channels and call recording/transcripts work?

> [!tip]- Answer
> Message channels are `file` (synchronous, most reliable), `email`, and `webhook` (POSTs message plus context), with email/webhook retried in the background 3 times with exponential backoff and failures quarantined to `.failures/` for `list-failures` inspection. Recording and transcripts are per-business YAML settings with local or S3 storage via LiveKit Egress, preceded by a spoken consent preamble for two-party consent states. See [[wiki/01-ai-receptionist-open-source-self-hosted-no-compr|AI Receptionist -- Open Source, Self-Hosted, No Compromises]].

### Q5. How do email delivery, multi-language detection, and retention sweeps work?

> [!tip]- Answer
> Email is enabled in a top-level `email` section with an SMTP or Resend sender plus `on_message` / `on_call_end` / `on_booking` triggers, so staff get messages, call summaries, or booking notices automatically. Languages are configured with `primary: "en"` and `allowed: ["en", "es", "fr"]`, where gpt-realtime-2.1 auto-detects the caller's language and continues in it if whitelisted, otherwise redirecting politely in the primary language. Retention defaults (`recordings_days: 90`, `transcripts_days: 90`, `messages_days: 0` forever) are swept with `python -m receptionist.retention sweep` without touching `.failures/`. See [[wiki/02-email-delivery|Email delivery]].

### Q6. How do multi-business routing, Google Calendar booking, and non-standard SIP transfers work?

> [!tip]- Answer
> One agent process serves many businesses by mapping each number's SIP dispatch-rule metadata to its own `config/businesses/<name>.yaml`, billed as metered OpenAI usage at ~$0.20–0.30/min with no platform fee. Calendar booking adds `check_availability` (up to 3 nearby slots) and `book_appointment` tools with spoken confirmation before booking, UNVERIFIED event tagging, and optional `.ics` invites via caller_email. Asterisk chan_sip trunks that reject `tel:` URIs override the default transfer target with `sip.transfer_uri_template`. See [[wiki/02-email-delivery|Email delivery]].

### Q7. A 10-calls/day small office is choosing between AIReceptionist and a $300/month SaaS receptionist — what would you recommend and why?

> [!tip]- Answer
> Recommend self-hosting AIReceptionist if the office can manage a server, SIP trunk, and API key, since ~$5/day (~$150/month) metered usage undercuts the SaaS fee while delivering near-human speech-to-speech quality, full YAML customization, and caller data kept on operator servers under AGPL-3.0. Prefer SaaS only if the office cannot operate Python/LiveKit/SIP infrastructure or needs flat-rate predictability at high call volumes, where per-minute billing can exceed the subscription. See [[wiki/02-email-delivery|Email delivery]].
