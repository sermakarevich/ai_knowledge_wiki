> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Receding-Horizon Prefix Commitment Inference

**In one sentence:** Receding-Horizon Prefix Commitment (RHPC) balances long temporal context with streaming low latency by predicting a 50-frame motion window at each step but committing only the first 15 frames, reusing the latest 10 committed frames as autoregressive prefix.

## Key points

- Each inference step consumes 50 temporally aligned audio tokens and predicts an extended 50-frame rich-motion window, but only the first 15 frames are committed to the robot controller.
- At speaking-turn start the streaming bridge initializes the motion prefix `P0` and audio context `Aprev_0` with zero tensors, since no ground-truth motion history is available at test time; each generated chunk is fed back as the prefix for the next step.
- The next 50-frame prediction uses the latest 10 committed frames as the motion prefix, with commitment advancing 15 frames per step, so the 10-frame overlap smooths transitions across chunk boundaries.
- The 50-frame prediction horizon keeps the sequence length closer to training, reducing the train-test distribution mismatch of applying diffusion denoising to substantially shorter sequences.
- The extended trajectory candidate lets downstream kinematic projection and collision checks assess future motion feasibility before commands are dispatched.
- Only 15 frames (0.50 s) are committed per step, so a CORTEX-triggered interruption ends the session after the current segment without discarding a long pre-generated trajectory, preserving continuity up to the last committed frame.
- At deployment only the denormalized joint qpos of the committed 15 frames are transmitted to the robot controller, while remaining rich-motion predictions are retained internally; incoming TTS audio is resampled from 24 kHz to 16 kHz mono.

---

## Predict-long, commit-short streaming loop

Rather than generating and committing short motion chunks independently, RHPC maintains a longer prediction horizon while committing only a short leading segment at each inference step:

> "At each inference step, the model consumes 50 temporally aligned audio tokens and predicts an extended 50-frame rich-motion window, but only the first 15 frames are committed to the robot controller."

| Quantity | Value |
|---|---|
| Audio tokens consumed per step | 50 |
| Predicted rich-motion window | 50 frames |
| Frames committed per step | 15 (first 15 of the window) |
| Commitment stride | 15 frames per step |
| Prefix for next step | latest 10 committed frames |
| Prefix/commitment overlap | 10 frames |

> "At the next inference step, the model predicts the next 50-frame window using the latest 10 committed frames as the motion prefix, with the commitment progressing by 15 frames at each step. The 10-frame overlap improves continuity between newly generated and previously committed motion, resulting in smoother transitions across chunk boundaries."

**Covers:** Section 4.4 streaming loop (Fig. 4)

## Initialization without ground-truth history

Inference in ROSCO differs from offline clip prediction because no ground-truth motion history exists at test time:

> "at the start of a speaking turn, the streaming bridge initializes the motion prefix P0 ∈ RC×Dm and corresponding audio context Aprev_0 with zero tensors. The generated motion chunk is then fed back as the prefix for the subsequent inference step, enabling autoregressive streaming generation."

**Covers:** Section 4.4 initialization and autoregressive feedback

## Why keep the 50-frame prediction horizon

Maintaining the 50-frame horizon serves two stated purposes:

> "First, it preserves a temporal sequence length closer to that used during training, reducing the train-test distribution mismatch that would arise from applying diffusion denoising to substantially shorter sequences. Second, it provides an extended trajectory candidate that allows downstream kinematic projection and collision checks to assess future motion feasibility before commands are dispatched."

Deployment follows the same strategy: causal inference uses a 50-frame temporal window with a 15-frame commitment, and only the denormalized joint qpos of the committed 15 frames are transmitted while the remaining rich-motion predictions are retained internally for subsequent inference.

**Covers:** Section 4.4 horizon rationale; Section 5.1 deployment window

## Bounded 15-frame commitment for full-duplex interruption

The short commitment bounds how much motion is exposed per step, which keeps barge-in cheap:

> "The 15-frame commitment also bounds the amount of motion exposed to the robot at each inference step, which is beneficial for full-duplex interaction. Since only 15 frames (0.50 s) are committed at a time, an interruption triggered by CORTEX does not require discarding a long pre-generated trajectory. Instead, the active motion session can be terminated after the currently committed segment, while continuity is preserved up to the last committed frame and the system remains responsive to user barge-in."

**Covers:** Section 4.4 bounded commitment and interruption handling
