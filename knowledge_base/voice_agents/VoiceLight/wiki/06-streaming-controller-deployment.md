> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# 5 Snapshots Failed for the Multi-Process — End-to-End Latency Case Study

**In one sentence:** A three-session, 36-turn microphone case study against a scale-to-zero Modal service measured 758 ms median final-VAD-to-first-server-audio latency with speculative promotion associated with lower latency, while deployment kept no warm container and observability separated model telemetry from durable conversation.

## Key points

- 5 snapshots failed for the multi-process CUDA layout, and an import-only CPU snapshot added about 30 seconds; keeping a container warm was rejected for expected low visit frequency and cost.
- The case study ran three unscripted microphone sessions by one operator from a browser in Germany against the scale-to-zero service in Modal's European region, measuring from after readiness so cold start is excluded.
- Across 36 measured response turns, median final-VAD-to-first-server-audio latency was 758 ms (mean 932 ms, range 528–1,652 ms), with 21/36 turns below 800 ms.
- In the 13-turn fully exported trace, component medians were endpoint commitment 502 ms, LLM first word 336 ms after generation start, TTS first PCM 444 ms after its first word, and server-to-browser render 95 ms — intervals that overlap and must not be added.
- Nine of 13 fully traced turns promoted speculative work (median 667 ms) versus four without promotion (median 1,513 ms), an observational split confounded with transcript stability and turn difficulty, not a causal 846 ms speedup estimate.
- The original 250–600 ms engineering target was not met consistently; the 800 ms line became a practical development reference, not a population target, with one operator, no scripting or blinding, and no population p50/p95 claims.
- The browser diagnostic stream's rolling 20-second view records user-speech and assistant-audible lanes, raw adapter outputs, Silero state, applicability, causal audio time, age, inference latency, policy decisions, and browser acknowledgments; adapter heads were not independently calibrated and are retained as engineering telemetry, not behavioral results.

---

## Deployment snapshot note

5 snapshots failed for the multi-process CUDA layout, and an import-only CPU snapshot added about 30 seconds. Keeping a container warm was rejected for the expected low visit frequency and cost.

## 8 End-to-end latency case study

The deployment case study comprises three unscripted microphone sessions run by one operator from a browser in Germany against the scale-to-zero service in Modal's European region. Measurements begin after the service reported readiness and therefore exclude cold start. Prompts covered ordinary conversation, longer responses, interruptions, short acknowledgments, calculations, current information, and sequential tool use. The final VAD endpoint is the last speech boundary used for turn commitment; first server audio is the first PCM packet sent for the response.

Across 36 measured response turns, the median final-VAD-to-first-server-audio latency was 758 ms; 21/36 turns were below 800 ms, and the range was 528–1,652 ms. One session exported the complete telemetry trace for 13 turns. In that subset, median endpoint commitment was 502 ms, LLM first word 336 ms after generation start, TTS first PCM 444 ms after its first word, and server-to-browser render 95 ms. These component intervals overlap and must not be added.

Nine of the 13 fully traced turns promoted speculative work. Their median final-VAD-to-first-server-audio latency was 667 ms, compared with 1,513 ms for the four turns without promotion. This observational split is consistent with speculation hiding downstream work, but candidate success is confounded with transcript stability and turn difficulty; it is not a causal estimate of an 846 ms speedup. Kyutai's fixed first-frame computation remained the largest warm downstream cost.

| Measurement | Observed value |
|---|---|
| Sessions / measured turns | 3 / 36 |
| Final VAD to first server audio, median | 758 ms |
| Final VAD to first server audio, mean | 932 ms |
| Final VAD to first server audio, range | 528–1,652 ms |
| Turns below 800 ms | 21 / 36 |
| Fully traced turns | 13 |
| Final VAD to endpoint commitment, median | 502 ms |
| Generation start to LLM first word, median | 336 ms |
| TTS first word to first PCM, median | 444 ms |
| Server audio send to browser render, median | 95 ms |
| Final VAD to browser render, median | 836 ms |

> "The original 250–600 ms engineering target was not met consistently. The 800 ms line became a practical development reference, not a population target."

The sessions were neither scripted nor blinded, involved one operator, and omit users, acoustic conditions, accents, and networks outside the development setting. They do not justify population p50 or p95 claims or independently quantify interruption, duck, or backchannel-resume latency.

## 9 Observability and reproducibility

The browser's diagnostic stream separates model evidence from durable conversation. Its rolling 20-second view records user-speech and assistant-audible lanes, raw adapter outputs, Silero state, applicability, causal audio time, age, inference latency, policy decisions, and browser acknowledgments. The adapter heads were not independently calibrated as probabilities of observable conversational behavior; their values are therefore retained as engineering telemetry rather than presented as behavioral results. Figure 4 limits the paper view to directly observable speech and playback activity.

Concrete reproducibility artifacts accompany each boundary: immutable serialized schemas reject extra fields; manifests retain seeds, input hashes, configuration, metrics, and checkpoint identity; locked evaluation files carry content hashes and detector provenance; and build and test commands are recorded with pinned model revisions. Deployment packages the final adapter and mounts persistent model caches without committing credentials. Table 6 identifies the final runtime snapshot and principal pins.

The public artifacts include the tool-use dataset, LoRA, merged 1.7B checkpoint, and synthetic turn-taking audio. Human conversational audio remains restricted by its source terms. The source repository contains generation, preparation, training, and evaluation code; narrative result summaries; the runtime and browser; and Modal deployment runbooks. Large prediction inventories and restricted source audio are not public artifacts.

Figure 4: Observable activity during a 20-second excerpt from an interactive microphone session. Green spans show detected user speech and gold spans show acknowledged assistant playback. The session exercised short backchannels and a floor-taking interruption, but the lanes intentionally do not assign semantic labels to individual overlaps.

**Covers:** streaming controller, speculation/cancellation, overlap policy and deployment (chunk §§8–9: end-to-end latency case study + observability and reproducibility; Table 5, Figure 4)
