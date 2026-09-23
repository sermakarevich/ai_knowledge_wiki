> [[index|Wiki]] | [[summary|Summary]]
# AI Receptionist -- Open Source, Self-Hosted, No Compromises — Digest

## 1. [[wiki/01-ai-receptionist-open-source-self-hosted-no-compr|AI Receptionist -- Open Source, Self-Hosted, No Compromises]]
**In one sentence:** A production-grade, self-hosted, AGPL-3.0 open-source AI receptionist built on OpenAI's Realtime speech-to-speech API via LiveKit and SIP replaces $200-500/month cascaded-pipeline SaaS products with sub-second, near-human phone answering with no platform fee or vendor lock-in.
## Key points
- Direct speech-to-speech via OpenAI Realtime API (the model behind ChatGPT Advanced Voice) eliminates the STT-to-LLM-to-TTS cascade, giving sub-second responses and model-native turn-taking instead of 1-3 second multi-hop delays.
- Self-hosted on the operator's infrastructure with standard SIP (Twilio/Telnyx trunk, LiveKit server) keeps call flows, prompts, and caller data under operator control with no vendor lock-in.
- Costs only metered OpenAI API-key usage per minute with no $200-500/month subscription, platform markup, per-seat pricing, or per-minute SaaS overages.
- One agent process serves multiple businesses, with each phone number routed to its own YAML config covering hours, FAQs, routing, voice, and personality.
- Requires Python 3.11+, a standard `sk-...` OpenAI API key with Realtime access, a LiveKit server, and a SIP trunk provider with a phone number; ChatGPT/Codex OAuth (`oauth_codex`) no longer authenticates Realtime after the 2026-06-03 Beta sunset.
- Customization is a YAML file per business (`business`, `voice`, `greeting`, `personality`, `hours`, `after_hours_message`, `routing`, `faqs`, `messages`) plus recording/transcript and multi-channel message delivery (file, email, webhook) sections — no code changes or dashboard feature requests.
- Active-development status: core voice conversations, FAQ answering, call transfers, and message taking work, but breaking changes and rough edges are expected.

## 2. [[wiki/02-email-delivery|Email delivery]]
**In one sentence:** Email delivery is enabled via a top-level `email` section with SMTP or Resend senders and `on_message` / `on_call_end` / `on_booking` triggers, sitting alongside multi-language support, retention sweeps, multi-business routing, per-minute costing, calendar booking, and SIP transfer overrides.
## Key points
- Email is configured in a top-level `email` section with `from: "receptionist@acmedental.com"` and a `sender` of type `smtp` (host `smtp.gmail.com`, port 587, `use_tls: true`, `${SMTP_USERNAME}` / `${SMTP_PASSWORD}`) or `resend`.
- Two email triggers are shown in the chunk: `triggers.on_message: true` (email when `take_message` fires) and `triggers.on_call_end: false` (email a summary after every call), plus optional `email.triggers.on_booking: true` to email staff whenever a calendar booking lands.
- `gpt-realtime-2.1` auto-detects the caller's language and continues in it when whitelisted (`primary: "en"`, `allowed: ["en", "es", "fr"]`), otherwise politely redirects in `primary`.
- Retention is configured as `recordings_days: 90`, `transcripts_days: 90`, `messages_days: 0` (0 = keep forever), swept on a schedule via `python -m receptionist.retention sweep` (or `--dry-run` preview), and the sweeper never touches `.failures/` directories.
- One agent process serves multiple businesses: each inbound number maps via SIP dispatch-rule metadata `{"agentName": "receptionist", "metadata": "{\"config\": \"my-business\"}"}` to `config/businesses/my-business.yaml`.
- Realtime is authenticated with a standard `sk-...` OpenAI API key and billed per audio minute at an estimated ~$0.20-0.30/minute (e.g. 10 calls/day x 2 min ≈ ~$5/day / ~$150/month; 30 x 2 min ≈ ~$15/day / ~$450/month; 60 x 1.5 min ≈ ~$22/day / ~$660/month), with no AIReceptionist platform fee or markup.
- Google Calendar booking adds `check_availability(preferred_date, preferred_time)` (up to 3 slots near the requested time) and `book_appointment(caller_name, callback_number, proposed_start_iso, notes?, caller_email?)` tools, with the agent reading the proposed time back for a "yes", tagging events UNVERIFIED, and adding `caller_email` as an OPTIONAL Google attendee that does not affect organizer free/busy on decline.

## The argument in five moves
1. SaaS AI receptionists (Bland, Vapi, Retell, Smith.ai, Ruby) fail on latency, robotic cascaded-pipeline voices, poor turn-taking, $200-500/month rent, lock-in, and third-party data custody.
2. Direct speech-to-speech via OpenAI's Realtime API over LiveKit/SIP removes the STT→LLM→TTS cascade, delivering sub-second, near-human answering with model-native turn-taking.
3. Self-hosting plus one-YAML-per-business configuration (hours, FAQs, routing, voice, personality, recording, message channels) keeps data, prompts, and call flows under operator control with no code changes.
4. The economics shift from platform subscription to metered `sk-...` API usage (~$0.20-0.30/min), paired with operational tooling: multi-channel message delivery with retries, SMTP/Resend email triggers, transcripts/recordings with consent preamble, retention sweeps, multi-language handling, and SIP dispatch-rule multi-business routing.
5. In-call Google Calendar booking (availability check, read-back confirmation, UNVERIFIED tagging, optional attendee invites) plus SIP transfer overrides make it a working front desk, licensed AGPL-3.0 so it cannot be re-wrapped as closed SaaS.
