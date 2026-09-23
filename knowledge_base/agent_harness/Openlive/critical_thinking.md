> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: katipally/openlive

## Claims vs. evidence
- Claim: "the whole voice loop runs on your own machine, no per-minute audio fees" — structurally evidenced: Silero VAD, Whisper STT, Smart-Turn end-of-turn, and Kokoro/Supertonic TTS all execute in-app on WebGPU, with sentence-by-sentence streaming TTS over a warm local WebSocket.
- Claim: "any brain you bring" — evidenced by design: keyed providers (Anthropic, OpenAI, Google, xAI, DeepSeek, Groq), fully local Ollama, plus ACP-driven coding agents (Claude Code, Codex, Cursor, OpenCode, Hermes) over JSON-RPC on local stdio.
- Claim: mid-call flexibility — evidenced: per-conversation agent choice with mid-call model/mode (`ask` / `accept edits` / `bypass`) switching reported over ACP, custom instructions and speaking speed applied across brains.
- Claim: privacy ("nothing spoken leaves the machine except the final transcript") — half-evidenced: audio never uploads and keys sit AES-256-GCM encrypted with only last-four shown, but transcripts and optional camera/screen frames still leave for the brain, so "transcript-private" is the honest label.
- Claim: "it can see" — evidenced as frame-per-turn plus an on-demand `look` tool for hi-res frames, including the fallback where a text-only model borrows a separate vision model's eyes.
- Claim: disciplined shipping — evidenced: strict TS base (`strict` + `noUncheckedIndexedAccess`), one pinned `@huggingface/transformers@4.2.0` to avoid dual-onnxruntime segfaults, one root vitest runner, tag-driven CI installers for macOS/Windows/Linux.
- Claim: barge-in ("interrupt any time; it stops mid-word") — mechanism evidenced (local VAD-driven cutoff feeding streaming TTS), but cutoff latency and false-barge rates are unmeasured, so the experience claim outruns the data.
- Claim: "speak as yourself" via 5–30s local ZipVoice cloning (~208 MB optional install, deletable profiles with export/import) — concretely specified and falsifiable, though clone quality across accents and noise is unevaluated.
- Claim: zero marginal cost with a coding agent as brain — credible given the agent runs under your existing login, but gross cost still depends on that agent's token burn, which voice narration can inflate via chattier turns.
- Missing evidence: no latency figures (time-to-first-audio, barge-in cutoff), no STT WER or turn-taking precision/recall, no TTS MOS or ZipVoice clone eval, and no measured cost/latency comparison against ElevenLabs Agents, Gemini Live, or OpenAI Realtime.

## Genuinely new vs. repackaged
- Repackaged: every voice primitive — Silero VAD, Whisper, Smart-Turn, Kokoro (28 voices, light) vs. Supertonic (10 voices, 44.1 kHz), ZipVoice zero-shot cloning — is assembled, not invented; cascaded STT→model→TTS is the standard open recipe.
- Repackaged: the desktop shape (Electron shell, Next.js UI, Hono + ws agent server, JSON-file store) is competent conventional scaffolding, with the ACP driver and provider adapters as the interesting parts.
- Genuinely new at integration level: voice-driving a pre-existing coding agent with native session placement (`~/.claude/projects/…`, resumable from either side, History shows CLI sessions) — the agent keeps its identity instead of being re-wrapped.
- Genuinely useful glue: spoken permission relay (voice "yes/no" to approve commands and edits), narrated progress ("Step 2 of 4"), live plan checklists with a context/cost chip, CLI install/auth management from Settings, mini-mode pill with tray and notifications.
- Borrowed-but-well-chosen: local ZipVoice cloning keeps voice identity on-device instead of behind a cloning API, and the Kokoro-vs-Supertonic choice (light/28 voices vs. 44.1 kHz/10 voices) gives a real quality-vs-weight knob.
- Borrowed-but-well-chosen: the provider-neutral harness with live model listing and cost/effort tracking turns "any brain" from slogan into a switchable setting with visible spend.
- Net: not a speech-model advance; a control-plane advance — voice as a thin local loop over agents you already run, which is exactly why the "any brain" trade works.

## Weaknesses and blind spots
- Latency ceiling by construction: cascaded turn-taking cannot match full-duplex speech-to-speech models on overlap, backchannels, and interruption naturalness; streaming TTS masks but does not erase the round trip.
- Client weight: Electron + Next.js + on-device models implies ~200 MB+ first-talk downloads (more for Supertonic or larger Whisper), WebGPU dependence, and unanswered questions on low-end or integrated-GPU behavior.
- Thin evaluation story: no benchmarks or accuracy reports in covered material, and the root vitest runner comment ("they existed before this config but had no framework") suggests testing was only recently unified — coverage unknown.
- Storage ceiling: `packages/db` is a JSON-file store with file locking — correct for single-user desktop, a non-starter for multi-user, server, or concurrent-agent deployments.
- Voice-permission hazard: approving file edits and shell commands by voice under noise or mishearing is the riskiest feature; no confirmation-fidelity handling, audit trail, or destructive-action guardrails appear in the digest.
- Native fragility: onnxruntime-node, sherpa-onnx, Electron allow-listed builds plus vendored VAD assets copied by script are classic cross-OS breakage points; lean tag-releases concentrate risk on maintainer CI and signing secrets.
- Robustness unknowns: no data on accents, code-switching, noisy rooms, or domain jargon (code identifiers spoken aloud); Whisper-local is decent but the failure envelope here is undocumented.
- Cross-platform parity risk: macOS universal signed/notarized vs. unsigned Windows/Linux installers plus media-permission handling per OS — expect the non-Mac experience to lag.
- Transcript fidelity: markdown transcripts with code copy buttons are good, but spoken code (brackets, indentation, symbols) is inherently lossy; no repair or confirm-back loop is described.
- Bus factor and velocity: a young single-maintainer-shaped repo with tag-driven releases and maintainer-only release notes concentrates review, signing, and triage on very few hands.
- Scope honesty gap: marketing-adjacent "eyes" framing overstates what is really frame-per-turn plus one hi-res grab — continuous scene understanding this is not.

## Applicability
- Good fit: solo hands-free driving of a coding agent, narrated long-run plans, demos where cloud audio retention or per-minute fees are unacceptable, and prototyping turn-taking UX without building VAD/STT/TTS plumbing.
- Poor fit: telephony, multi-user or server-side realtime products, low-latency duplex research, regulated offline mandates, or teams needing SLAs and eval dashboards.
- Preconditions for use: a decent GPU, tolerance for model downloads, an existing coding-agent login, and willingness to keep voice permissions in a low-risk mode until mishearing behavior is characterized.
- Accessibility angle: hands-free coding-agent operation and spoken plan narration are legitimately useful for RSI, screen-fatigue, or eyes-busy lab work — arguably the strongest single-user case.
- Prototyping angle: the repo layout map (`apps/desktop`, `apps/web` voice engine, `services/agent` ACP driver, `packages/shared` registry) makes it easy to lift one layer — e.g. the ACP driver — without adopting the whole app.
- **Relevance to my work**
  - AI/ML engineering: borrow the cascaded-loop wiring (VAD → streaming STT → end-of-turn → streaming TTS with barge-in) and the one-pinned-transformers plus strict-TS discipline for local-model desktop tooling.
  - Agentic systems: the transferable pattern is ACP-over-stdio with voice permission relay, narrated plans, and a cost chip — a thin voice control plane over a native agent session, no agent re-platforming required.
  - Elisity data platform: no direct reuse (JSON store, no connectors, lineage, or multi-tenancy), but the edge-loop/cloud-brain split is a useful reference shape for future field-ops voice interfaces over platform data.

## What this changes
- It commoditizes the voice pipeline for developers: local ears and mouth become free infrastructure, leaving only the token costs you already pay — or nothing extra under an existing coding-agent login.
- It reframes voice agents as a UX layer over agents already in use rather than a separate hosted product: sessions, permissions, and history stay native to the agent.
- It sets a privacy floor worth copying (audio local, transcript-only egress, encrypted keys) while reminding that "local voice" still leaks intent via transcripts and frames.
- It does not move the frontier on conversational speech quality or duplex interaction; hosted realtime models retain that edge, explicitly conceded by the cascade choice.
- For open-source strategy it demonstrates the viable middle: concede the model frontier, own the loop and the agent relationship, and compete on privacy, cost structure, and workflow embedding.

## Verdict
- Install-grade for individuals: voice-drive one real coding task end to end, then decide — measure turn latency, barge-in cutoff reliability, clone-voice intelligibility, and permission-relay safety before granting broad approvals.
- Reference-grade for builders: copy the ACP control-plane and permission/narration UX; do not adopt the JSON store, desktop-only topology, or unevaluated pipeline for anything serving more than one user.
- The missing piece that would upgrade this judgment is a short honest eval page: WER, turn-taking errors, time-to-first-audio, and a hosted-pipeline cost/latency table.
- Revisit triggers: published evals, a server/multi-user story, or a hardened permission model with audit logs would each merit re-scoring toward broader adoption.
- Call: **trial**
