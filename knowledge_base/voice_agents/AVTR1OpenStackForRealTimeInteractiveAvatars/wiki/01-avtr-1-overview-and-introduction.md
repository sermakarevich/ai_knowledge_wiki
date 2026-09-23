> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# AVTR-1 overview and introduction
**In one sentence:** AVTR-1 is an open stack for real-time interactive avatar conversations that splits the problem into a 153M-parameter dyadic motion generator (renderer side) and a worklet-based serving backend (streamer side) consuming an external voice agent's speech, because fast inference alone cannot deliver synchronized audio-video, scheduled playback, and interruption handling.
## Key points
- Talking-head and dyadic models now achieve real-time inference, but fast motion generation alone does not produce an interactive conversation: a live system must synchronize model output with external voice-agent speech, schedule video frames, and handle interruptions.
- AVTR-1 spans motion generation, inference, and real-time serving: the motion generator predicts head/facial motion from both participants' audio, the renderer converts motion to video plus session state, and the streamer coordinates the live session driving the renderer in a loop.
- The stack leaves user-speech interpretation and reply-speech generation to an external voice agent and consumes that agent's output; scheduling decisions shape response latency (reply audible) and interruption latency (speech after barge-in).
- Motion synthesis is separated from appearance rendering to keep the generation target compact: a 153M-parameter conditional flow-matching Transformer predicts five-frame motion chunks autoregressively from self audio (speaking) and other audio (listening).
- Training uses an internal 926-hour corpus of curated unscripted dyadic conversations with ground-truth motion history gradually replaced by model estimates; a chunk-based HuBERT encoder is self-distilled to reproduce full-context features from short windows.
- Evaluation claims leading performance among compared dyadic models on visual quality, lip sync, and listening, with real-time inference on data-center and consumer GPUs; listening dependence is measured with the new Reference-Based Directed Granger Gain (R-DGG).
- Artifacts released under component-specific licenses: model weights, renderer, and streamer — the complete path to run a live interactive avatar session locally.
---
## The interactive-avatar problem
Per the introduction: "fast model inference alone is insufficient for live conversation, which requires both speech-conditioned listening and timely delivery of synchronized audio and video." External voice-agent speech arrives in variable-sized fragments while a chunk-based motion generator needs fixed-size audio windows; the surrounding system must adapt one to the other while generating frames, synchronizing them with audio, scheduling playback, and handling interruptions.

## Component map
- Motion generator: predicts head and facial motion from both participants' audio (self = speaking motion, other = listening behavior).
- Renderer (inference-side): converts predicted motion into video and returns updated session state.
- Streamer (serving backend): coordinates the live session and drives the renderer in a continuous loop; converts variable-sized speech fragments to fixed-size audio windows and delivers synchronized audio-video.
- External voice agent: owns the conversation (interprets user speech, generates reply speech); AVTR-1 consumes its output.

## Report roadmap
Per the introduction: Section 2 describes the motion model, Section 3 the training pipeline, Section 4 the streaming inference and serving stack, Section 5 the latency analysis, and Section 6 the evaluation protocol and results.
**Covers:** paper title/abstract framing, contributions, and the interactive-avatar problem statement.
