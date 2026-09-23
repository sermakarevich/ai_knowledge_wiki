> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Conversational Intelligence — Reasoning-Mode Evaluation
**In one sentence:** StepAudio 3 in reasoning mode scores 73.0 macro average on the eight StepAudioChat dimensions — ahead of Doubao 2.0 Lite (70.5) and DeepSeek-V4-Flash (71.4) but behind Kimi K3 (77.1) — while its realtime system adds Think-While-Speaking, Adaptive Thinking routing, and MTP acceleration on top of that reasoning checkpoint.
## Key points
- Reasoning-mode macro average is 73.0 for StepAudio 3, vs 70.5 (Doubao 2.0 Lite), 71.4 (DeepSeek-V4-Flash), and 77.1 (Kimi K3).
- StepAudio 3 ranks second on reasoning (73.0), memory (72.0), knowledge (73.1), conversational pragmatics (67.2), and persona & role consistency (80.9).
- Kimi K3 leads six of eight dimensions, including reasoning at 81.9, memory at 77.6, and safety & reliability at 84.8.
- Doubao 2.0 Lite leads instruction following (72.9) and persona & role consistency (82.6).
- Think-While-Speaking uses two concurrent calls as Formulation Brain (private reasoning trace) and Articulation Brain (short spoken segments), with playback-aware scheduling, Speak-First by default, and Think-First as the prefix-waiting option.
- Adaptive Thinking routes turns to immediate (empty think block) vs deliberate response, with think rates from 51.5% to 82.0% across the eight categories on StepAudioChat (46 benchmark members).
- Full thinking gains most over forced no-think in Reasoning (+11.37), Persona and Role Consistency (+8.37), and Knowledge (+5.94); vs Direct SFT, Adaptive Thinking improves Dialogue Pragmatics 63.59 → 65.87 but reduces Reasoning 71.89 → 66.80, with Reasoning think rate only 59.5% despite benefiting most.
---
## Reasoning-model evaluation on StepAudioChat
The chunk states: "We evaluate StepAudio 3 in reasoning mode on the eight StepAudioChat dimensions. This evaluation isolates the model's conversational and reasoning capability; here we focus only on its dialogue results."
It distinguishes this from Section 8: "the overall comparison in Section 8 evaluates the realtime system, which additionally applies Think-While-Speaking, Adaptive Thinking, and MTP acceleration, as described in Section 6.3."
Scores use a 0–100 scale (higher is better); bold marks best per row, underlining marks second-best.

| Capability | StepAudio 3 Realtime (Reasoning) | Doubao 2.0 Lite | DeepSeek-V4-Flash | Kimi K3 |
|---|---|---|---|---|
| Instruction Following | 66.3 | 72.9 | 71.4 | 68.9 |
| Faithfulness | 72.4 | 67.5 | 75.3 | 78.4 |
| Reasoning | 73.0 | 72.7 | 64.8 | 81.9 |
| Memory | 72.0 | 71.3 | 71.5 | 77.6 |
| Knowledge | 73.1 | 59.9 | 71.6 | 78.6 |
| Safety & Reliability | 79.0 | 75.9 | 79.9 | 84.8 |
| Conversational Pragmatics | 67.2 | 61.5 | 62.9 | 70.3 |
| Persona & Role Consistency | 80.9 | 82.6 | 73.6 | 76.5 |
| Macro Average | 73.0 | 70.5 | 71.4 | 77.1 |

Claim verbatim: "These category-level differences show that strong aggregate reasoning does not imply uniformly stronger instruction following or role consistency."

## Think-While-Speaking
Builds on "the two-process design of Mind-Paced Speaking [17]"; "Two concurrent calls to the same audio model act as a Formulation Brain and an Articulation Brain."
"The Formulation Brain generates a private reasoning trace. The Articulation Brain produces short response segments conditioned on the reasoning available so far and on the response already spoken."
"Playback-aware scheduling releases response segments according to the progress of the streaming output audio while formulation continues in parallel."
"Once formulation finishes, the remaining response can use the complete reasoning state. A final continuation can supplement or correct an answer that began from incomplete reasoning."
"The system uses Speak-First by default, starting the response without waiting for an initial reasoning prefix. Think-First waits for a short reasoning prefix before beginning the response."
"Adaptive Thinking controls whether a turn uses explicit reasoning. For turns that do, MTP acceleration speeds up the private thinking stream, following speculative and multi-token decoding approaches that reduce sequential target-model steps [28–31]."

## Adaptive Thinking — policy
"Motivation. Different conversational turns warrant different deliberation budgets. Explicit reasoning consumes decoding compute and can delay a routine response."
Supervision is built "at the assistant-turn level": "For each turn, we collect the dialogue context, target answer, original reasoning trace, and task-type features."
"A fixed probe model, trained without the adaptive-thinking data transformation, receives an empty think block and regenerates the answer under a no-think condition."
"A blind judge scores the original and no-think trajectories against the target answer, without knowing which is which, and labels the turn by whether reasoning changed the answer's quality."
"This paired judgment provides the primary evidence, with consistency across repeated judgments and the coherence between a reasoning trace and the answer it produces, together with a task-type prior, informing how conservatively to retain reasoning supervision."
Budgeting: "Within each domain, turns labeled reasoning-unnecessary are the candidates for replacement, and a per-domain budget on the no-think rate decides how many are taken while the remaining turns keep their original reasoning." Retention is stratified "by fine-grained topic" with a cap on "the drop rate within each capability, so that reasoning-intensive capabilities are not disproportionately stripped of supervision."

## Adaptive Thinking — evaluation (Table 5)
Setup: "Table 5 compares three configurations on StepAudioChat, covering 46 benchmark members in eight capability categories. Direct SFT and forced no-think share baseline weights, with explicit reasoning enabled or disabled at inference time. Adaptive Thinking is trained separately with reasoning-selection supervision." "Within each category, scores and think rates are unweighted means over benchmark members. Evaluation uses temperature zero and no system prompt."
"Adaptive Thinking invokes explicit reasoning at rates from 51.5% to 82.0% across the eight categories."
"Full thinking provides its largest gain over forced no-think in Reasoning (11.37 points), followed by Persona and Role Consistency (8.37 points) and Knowledge (5.94 points)."
"Relative to Direct SFT, Adaptive Thinking improves Dialogue Pragmatics from 63.59 to 65.87, but reduces Reasoning from 71.89 to 66.80."
Limitation: "The category rates expose a limitation of the selection policy. Reasoning has a think rate of 59.5% despite benefiting most from full thinking. Faithfulness has a higher rate of 79.2%, but gains only" [chunk truncated here].

| Domain | Direct SFT Think Rate | Direct SFT Score | Forced no-think Think Rate | Forced no-think Score | Adaptive Thinking Think Rate | Adaptive Thinking Score |
|---|---|---|---|---|---|---|
| Instruction Following | 100.0 | 64.15 | 0.0 | 61.98 | 60.0 | 62.12 |
| Faithfulness | 100.0 | 72.35 | 0.0 | 70.63 | 79.2 | 72.42 |
| Reasoning | 100.0 | 71.89 | 0.0 | 60.52 | 59.5 | 66.80 |
| Memory | 100.0 | 67.99 | 0.0 | 63.86 | 51.5 | 65.99 |
| Knowledge | 100.0 | 74.59 | 0.0 | 68.65 | 80.4 | 71.55 |
| Safety and Reliability | 100.0 | 78.46 | 0.0 | 74.95 | 56.9 | 77.90 |
| Dialogue Pragmatics | 100.0 | 63.59 | 0.0 | 62.41 | 58.9 | 65.87 |
| Persona and Role Consistency | 100.0 | 77.17 | 0.0 | 68.80 | 82.0 | 74.62 |

Table notes: "Scores are reported in the native percentage-based scale. Higher scores are better. Think rates are percentages. Category values average benchmark members equally. The first two conditions share baseline weights; Adaptive Thinking uses a separately trained model. Bold and underlining mark the best and second-best scores in each row; think rates are not ranked."

**Covers:** StepAudioChat benchmark, multi-turn dialogue data, and reasoning-mode evaluation (chunk 05; Table 4 reasoning-mode results, Section 6.3 Think-While-Speaking, Adaptive Thinking policy and Table 5 ablation).
