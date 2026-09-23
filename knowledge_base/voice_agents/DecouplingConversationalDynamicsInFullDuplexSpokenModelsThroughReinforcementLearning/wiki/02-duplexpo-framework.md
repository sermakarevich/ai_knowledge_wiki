> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# DuplexPO Framework: Dynamics-Critical Windows, Reward Calculation and Prediction
**In one sentence:** DuplexPO decouples conversational dynamics from semantic content by restricting RL to short dynamics-critical windows around backchanneling, turn-taking, and barge-in events, evaluated by a factorized window-level reward.
## Key points
- Model-level full duplex (Moshi, SALMONN-omni, SALM-Duplex) exposes turn-taking, backchanneling, and barge-in directly to the model, so the challenge is learning a temporally coordinated policy for when an answer should enter, pause, or leave the shared speech stream.
- Whole-dialogue objectives blur credit assignment for local decisions (yielding after barge-in, brief backchannel, delaying turn start), so DuplexPO restricts policy updates to short interaction-critical windows rather than full dialogues.
- Unlike ASPIRin, which projects the action space into active-speech versus inactive-silence states before GRPO-style optimization, DuplexPO keeps the original action space and changes the optimization unit to dynamics-critical windows only.
- DuplexPO consists of three components: Dynamic-critical Window Sampling around annotated agent speaking events, Factorized Conversational Dynamics Reward (FCDR), and group-based policy optimization with multiple rollouts per window.
- The policy is frame-level over a uniform grid of duration Δ: πθ(yt | y<t, x≤t) (Eq. 1), and for window Wi with support [si, ei) it samples only inside the window conditioned on teacher-forced history before si, scored by Ri = R(Wi, y[si,ei)) (Eq. 2).
- Each window is Wi = (si, ei, gi, hi, ci) (Eq. 3) with discretized reference interval gi = ⌊ai/Δ⌋, hi = ⌊bi/Δ⌋ (Eq. 4), lead time L and buffer B via si = max(ei−1, ⌊(ai − L)/Δ⌋), ēi = ⌊(bi + B)/Δ⌋ (Eq. 5), and anti-overlap clipping ei = min(ēi, ⌊(ai+1 − L)/Δ⌋, T) (Eq. 6).
- FCDR replaces coarse rollout-level rewards (e.g. ORISE) with event-level shaped supervision: onset delay τi = Δ(ĝ i − gi) (Eq. 7) with τi < 0 early and τi > 0 late, three masks m_on, m_bc, m_off from metadata ci, and weighted sum RFCD = λon m_on R_on + λbc m_bc R_bc + λoff m_off R_off + λreg R_reg (Eq. 8).
---
## Figure 1: overview and prediction waveform
Figure 1 shows dynamics-critical windows as red shadows covering three behaviors: ① backchanneling, ② turn-taking, and ③ user barge-in. For each window, the policy model generates multiple rollouts (R1 … Rn) for reward calculation and is optimized with RL, with backpropagation and streaming speech synthesis in the loop. The chunk header also carries the labels "Dynamics-critical Window", "Reward Calculation", "Optimization", "Prediction Waveform".
**Covers:** Figure 1 and caption
## System-level vs model-level full duplex
System-level designs use auxiliary control to determine when to speak while the core model focuses on response generation. Model-level full duplex follows a different formulation:
> "Models such as Moshi, SALMONN-omni, SALM-Duplex, and related latent-reasoning variants expose turn-taking, backchanneling, and barge-in behavior directly to the model"
Recent full-duplex benchmarks likewise treat these behaviors as explicit model capabilities rather than peripheral interface features. This paper therefore focuses on model-level full-duplex dialogue, where:
> "the key challenge is not only generating an appropriate answer, but learning a temporally coordinated policy for deciding when that answer should enter, pause, or leave the shared speech stream."
**Covers:** §2.2 opening (system vs model-level framing)
## Reinforcement learning for dialogue agents
RL suits dialogue policy optimization where actions have delayed effects beyond next-token likelihood. Prior work covers task-oriented dialogue, turn-taking, conversational reasoning, retrieval-augmented QA, and AI-feedback response optimization; for end-to-end spoken models, Align-SLM uses AI-feedback preference optimization for semantic coherence in textless SLMs, while user-interaction alignment builds large-scale preference pairs from raw multi-turn speech for full-duplex speech-to-speech models. These studies show reward-based learning helps when desired behavior is sequential, context-dependent, or weakly specified by supervised targets.
Full-duplex dynamics pushes this into a local temporal regime: yielding after user barge-in, producing a brief backchannel, or delaying a turn start depend on narrow acoustic and conversational context, yet whole-dialogue objectives blur credit assignment. Recent spoken-dialogue RL and reward-modeling work optimizes interaction behaviors such as turn-taking and backchanneling via dialogue-level policies or reward models over entire conversations; by contrast, this approach restricts updates to short, interaction-critical windows. ASPIRin shows raw-token RL for full-duplex timing can degrade semantic quality and projects the action space into active-speech versus inactive-silence states before GRPO-style optimization; DuplexPO instead keeps the original action space and updates only dynamic-critical windows rather than the full dialogue.
**Covers:** §2.2 (RL for dialogue agents)
## Methodology overview
> "We propose DuplexPO, a policy optimization method that decouples when and how to engage in conversation (turn-taking, backchanneling, yielding to user barge-ins) from what to say (semantic content)."
DuplexPO improves full-duplex behavior while preserving instruction-following and reasoning capabilities. Three main components:
1. Dynamic-critical Window Sampling — selects local windows around annotated agent speaking events and restricts optimization to these regions.
2. Factorized Conversational Dynamics Reward (FCDR).
3. Group-based policy optimization.
Appendix D provides a token-level example of how DuplexPO reshapes boundary-control decisions.
**Covers:** §3.1 Overview
## Problem formulation
Full-duplex conversational dynamics learning is frame-level policy optimization over streamed dialogue. Let x1:T be the user audio stream and y1:T the agent's real-time interaction decisions on a uniform temporal grid with frame duration Δ. At each frame:
| Item | Exact form |
|---|---|
| Policy (Eq. 1) | πθ(yt \| y<t, x≤t) |
| Causal user context | x≤t |
| Agent state yt | silence, speaking, turn initiation, or yielding |
| Window set | W = {Wi}M i=1 extracted from long human conversations |
| Window support | [si, ei) around an interaction-critical event, with reference speaking interval and event metadata |
| Window reward (Eq. 2) | Ri = R(Wi, y[si,ei)) where y[si,ei) are sampled decisions within the window |
Sampling is only inside the window while conditioning on teacher-forced history before si.
**Covers:** §3.2 Problem Formulation (Eqs. 1–2)
## Dynamics-critical window sampling
Motivation: conversational turn transfer is often determined by local timing and prosodic cues near possible response points, rather than evidence uniformly distributed across the dialogue. DuplexPO therefore selects short windows such as turn transitions, backchannels, and user barge-ins. Let (ai, bi) be start/end times of the i-th annotated human agent segment, and ci its event metadata (whether backchannel; whether window contains user barge-in).
| Item | Exact form |
|---|---|
| Window tuple (Eq. 3) | Wi = (si, ei, gi, hi, ci), with [gi, hi) discretized reference speaking interval and [si, ei) sampled window |
| Reference interval (Eq. 4) | gi = ⌊ai/Δ⌋, hi = ⌊bi/Δ⌋ |
| Lead/buffer (Eq. 5) | si = max(ei−1, ⌊(ai − L)/Δ⌋), ēi = ⌊(bi + B)/Δ⌋, with lead time L before and buffer B after the annotated segment; previous-boundary term omitted for the first window |
| Clipping (Eq. 6) | ei = min(ēi, ⌊(ai+1 − L)/Δ⌋, T); next-segment boundary omitted for the final segment |
Within each window, history before si is teacher-forced and the policy is optimized only on sampled actions in [si, ei).
**Covers:** §3.3 Dynamics-Critical Window Sampling (Eqs. 3–6)
## Factorized conversational dynamics reward (setup)
ORISE shows rollout-level rewards can improve spoken interaction, but sequence-level assignment gives coarse supervision that cannot attribute success or failure to specific real-time decisions. FCDR is a temporally shaped, event-level reward motivated by human turn-taking and backchannel findings. For a sampled continuation in Wi, let Ŝi ⊆ [si, ei] be frames where the agent speaks; if Ŝi ≠ ∅, predicted onset ĝ i = min Ŝi and onset delay (Eq. 7):
| Item | Exact form |
|---|---|
| Onset delay (Eq. 7) | τi = Δ(ĝ i − gi); τi < 0 starts too early, τi > 0 starts late |
| Masks from ci | m_on (onset timing), m_bc (backchannel timing), m_off (barge-in yielding) indicate which components are active |
| Final FCDR (Eq. 8) | RFCD(Wi, Ŝi) = λon m_on R_on + λbc m_bc R_bc + λoff m_off R_off + λreg R_reg |
This factorized design assigns credit to local timing decisions while keeping the reward interpretable across dynamics events. Component definitions are in Table 1 (in this chunk only the table caption/header is present: Bi = [gi, hi] annotated backchannel interval, d(t, Bi) frame distance to Bi, ℓi duration of agent speech after user barge-in, ei,k predefined undesirable interactions); Figure 6 in Appendix gives empirical analysis of reward components, and Appendix I compares FCDR with neural reward-model alternatives (temporal state prediction, window-level dynamics scoring).
**Covers:** §3.4 FCDR through Eq. 8 and Table 1 caption/header
