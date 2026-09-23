> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Embodiment Cue, Routing, and Execution

**In one sentence:** CORTEX emits a compact `<motion: m>` cue prefix that is stripped before TTS and routed either to pre-validated retrieved motions or to a streaming ROSCO co-speech session, with robot-side safety enforced by a collision-aware projection layer and a 250 Hz control loop.

## Key points
- The embodiment cue `m` is serialized as a compact prefix `<motion: m>; response text` with `m ∈ M` (Eq. 2), where `M` is a finite vocabulary of embodiment cues with representative examples in Tab. 1.
- Cue selection jointly considers user utterance, inferred affect, semantic intent, and recent dialogue history — not a one-to-one affect-to-action mapping (e.g. negative affect raises the likelihood of repair plus an apologize cue only when the utterance indicates dissatisfaction).
- A parser separates the cue prefix from response text before TTS so control metadata never enters spoken audio; missing or malformed cues fall back deterministically to `speak` for non-empty responses and `idle` for empty responses.
- Routing splits by cue: non-speaking cues forward a behavior family to a retrieval service of pre-validated motions (predictable timing, bounded physical envelope); `speak` establishes a co-speech session streaming TTS audio to ROSCO (Sec. 4).
- Robot-side execution runs on an Astribot S1 via an execution bridge that receives discrete cues or streaming co-speech `qpos` frames, opens a realtime co-speech session for `speak`, and sends the first frame through a brief `move_to` transition to avoid discontinuity.
- Every generated `qpos` frame passes through a collision-aware projection layer evaluated in the MuJoCo simulator that solves constrained inverse kinematics under joint-limit and collision constraints, holding the last safe pose or invoking fallback on failure.
- Source-rate motion at typically 30 Hz is consumed by a 250 Hz joint-position control loop on the Orin side with per-tick joint-step limits; on CORTEX interruption the active motion session is terminated and delayed commands rejected while dialogue state stays intact.

---

## 3.3 Embodiment cue format and selection

The embodiment cue `m` is described as "the explicit interface between CORTEX and physical behavior", serialized per Eq. (2) as:

| Item | Value from chunk |
|---|---|
| Format | `< motion: m >; response text, m ∈ M` |
| Vocabulary | Finite vocabulary `M` of embodiment cues; representative examples in Tab. 1 |
| Selection inputs | User utterance, inferred affect, semantic intent, recent dialogue history |
| Mapping rule | Context-appropriate selection, not one-to-one affect→action; negative affect may increase likelihood of conversational repair and an apologize cue when dissatisfaction is indicated, but does not independently determine behavior |
| Parser | Separates cue prefix from response text before TTS, "preventing control metadata from entering spoken audio" |
| Fallback | Missing/malformed cue → deterministically `speak` for non-empty responses, `idle` for empty responses |

## Embodiment-cue routing

> "This routing separates behavioral intent from motion realization: CORTEX determines what kind of embodied response is appropriate, while the corresponding execution module determines how that behavior is physically realized over time."

| Route | Destination | Properties |
|---|---|---|
| Non-speaking cues | Retrieval service with pre-validated robot motions | Predictable execution timing; bounded physical envelope for discrete social behaviors |
| `speak` | Co-speech session streaming TTS audio to ROSCO (Sec. 4) | Speech-synchronized motion generated online |

## 3.4 Robot-side physical execution

Deployed on an Astribot S1 humanoid; the execution bridge connects behavior-generation modules to the robot-side Orin service, translating discrete cues or streaming co-speech motion (sequences of `qpos` frames) into robot commands under final physical constraints.

| Stage | Detail from chunk |
|---|---|
| Discrete cues | Mapped to pre-validated robot actions and dispatched |
| `speak` session | Bridge opens realtime co-speech session receiving ROSCO motion stream (Sec. 4) |
| Handoff | First `qpos` frame sent to brief `move_to` transition from preceding-action pose or current held pose; subsequent frames dispatched in realtime |
| Safety projection | Each `qpos` frame evaluated in MuJoCo simulator, solving constrained inverse kinematics subject to joint-limit and collision constraints; on failure hold last safe pose or invoke fallback policy |
| Control rates | Source-rate frames typically 30 Hz consumed by 250 Hz joint-position loop on Orin side with per-tick joint-step limits before Astribot SDK |
| Interruption | Active motion session terminated and invalidated; delayed commands from that session rejected; controller holds last safe pose or invokes fallback; dialogue state intact |

## 3.4.1 Failure containment and recovery

Recovery is local with bounded per-module scope: language-format errors contained before TTS; interruptions handled at sentence level without invalidating the dialogue session; insufficient audio evidence blocks committing new motion; collision rejection handled independently of speech generation. Physical execution stays subject to robot-side controller constraints. Service components (streaming speech APIs, dialogue models, downstream behavior services) are replaceable behind the session-scoped CORTEX interface without changing the cue-routing protocol.

## 4 / 4.1 ROSCO context and motion representation (as given in chunk)

The `<motion:speak>` route needs motion synchronized to speech rhythm, pauses, and prosodic emphasis; unlike fixed retrieved behaviors, co-speech motion must start before the full utterance is synthesized and stay consistent as audio arrives. ROSCO (Robotic Streaming Co-speech generator) is introduced as a prefix-conditioned model generating temporally coherent motion from streaming speech with continuity across chunks; overview in Fig. 3 (panels: (a) streaming generation, (b) Prefix-DiT block, (c) training objectives).

Training samples retargeted from co-speech dataset BEAT [21] to Astribot S1 joint trajectories at 30 fps using GMR [3]: motion prefix `C = 10` frames plus target chunk `K = 100` frames with aligned audio. Per-frame representation (Eq. 3):

`xt = [qt, Δqt, p_local_t, R^6D_t] ∈ R460`, with `qt ∈ R32` (joint qpos), `Δqt ∈ R32` (joint velocity), `p_local ∈ R132` (Cartesian positions of 44 tracked body segments), `R` 6D local link rotations in `R264` (32+32+132+264 = 460).

**Covers:** Sec. 3.3–3.4.1, Sec. 4–4.1 and Fig. 3 (as present in chunk 04/9)
