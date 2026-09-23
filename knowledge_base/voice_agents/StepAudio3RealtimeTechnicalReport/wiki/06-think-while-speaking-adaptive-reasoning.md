> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Think While Speaking, Adaptive Reasoning and MTP Acceleration
**In one sentence:** MTP3/MTP5 with Medusa-style typical acceptance accelerate private reasoning (1.49×–2.05× wall-clock) while improving Reasoning and Memory but lowering Instruction Following, and a 3:1:1:1 weighted merge of four specialized teachers balances audio, text, and dialogue capabilities.
## Key points
- All tested MTP configurations improve Reasoning (up to 74.30 vs 70.76 baseline) and Memory (up to 71.36 vs 67.99) over baseline, while Instruction Following declines (61.21–62.73 vs 64.15 baseline).
- Accepted draft tokens per target-model step are 1.231 (MTP3 strict), 1.801 (MTP3 Medusa-typical), 1.353 (MTP5 strict), and 2.153 (MTP5 Medusa-typical), with wall-clock speedups of 1.76×, 2.05×, 1.49×, and 1.72× respectively (baseline 0 and 1.00×).
- MTP3 uses three prediction heads drafting up to three future tokens per target-model step; Medusa-style typical acceptance uses an entropy-adaptive confidence threshold to accept plausible drafts strict verification would reject, plus a 1.05 repetition penalty on private reasoning only, with strict verification retained for spoken responses.
- Marginal acceptance (Table 7) under typical acceptance reaches 82.4%/58.2%/39.4% for MTP3 heads 1–3 and 80.6%/55.7%/37.6%/24.9%/16.4% for MTP5 heads 1–5; strict rates for MTP5 heads 4–5 fall to 10.7% and 5.7%, showing diminishing gains from added depth.
- Acceptance alone does not determine net efficiency since reasoning length and decoding costs also matter, so reported wall-clock ratios "should not be interpreted as a controlled comparison of draft depth," and keeping strict verification for spoken output "does not eliminate errors arising from incomplete private reasoning."
- Four compatible teachers trained from a common base with different data mixtures are merged as θmerge = Σ αi θi (αi ≥ 0, Σαi = 1) with normalized 3:1:1:1 weighting and held-out coefficient selection, adding neither model components nor inference-time routing.
- The merge reaches macro averages of 81.3 on audio understanding (tying best teacher, leading MMAU and WildSpeech), 76.5 on general text (highest, with best HMMT 2026 Feb and GPQA Diamond), and 73.0 on dialogue (above Teachers 2–4, below Teacher 1 at 74.2) — a balanced trade-off, not uniform dominance.
- The full-duplex voice agent routes stable-knowledge requests to direct responses, up-to-date public information to lightweight tools (weather, web search), and private-context/multi-step/beyond-turn work to asynchronous backend execution that continues alongside conversation.
---
## Domain baseline vs MTP3 / MTP5 (Table 6)
| Domain | Baseline | MTP3 | MTP3 (Medusa) | MTP5 | MTP5 (Medusa) |
|---|---|---|---|---|---|
| Instruction Following | 64.15 | 61.21 | 62.71 | 61.25 | 62.73 |
| Faithfulness | 72.35 | 72.29 | 70.46 | 72.49 | 72.03 |
| Reasoning | 70.76 | 74.30 | 73.74 | 73.14 | 72.73 |
| Memory | 67.99 | 69.29 | 68.97 | 70.85 | 71.36 |
| Knowledge | 74.59 | 75.07 | 75.34 | 75.31 | 74.33 |
| Safety & Reliability | 81.41 | 81.07 | 81.59 | 81.23 | 81.17 |
| Conversational Pragmatics | 63.59 | 66.04 | 63.17 | 66.22 | 66.15 |
| Persona & Role | 77.17 | 77.99 | 75.92 | 77.19 | 77.56 |
| Accepted/Step | 0 | 1.231 | 1.801 | 1.353 | 2.153 |
| Wall-clock Speedup | 1.00× | 1.76× | 2.05× | 1.49× | 1.72× |

All configurations use a repetition penalty of 1.05. The chunk notes the tested MTP configurations improve Reasoning and Memory over baseline while Instruction Following declines, and that a "1.72 points from full thinking" gap means "lower thinking frequency alone therefore does not demonstrate that reasoning is allocated to the turns that benefit most."
## Accelerating private reasoning with MTP (§6.3.2)
"Adaptive Thinking reduces how often explicit reasoning is invoked. To reduce the decoding cost of the remaining private thinking, we use MTP3 with three prediction heads, drafting up to three future tokens at each target-model step."
"Strict verification follows the target model's standard speculative-decoding rule. Medusa-style typical acceptance uses an entropy-adaptive confidence threshold to accept plausible draft tokens that strict verification may reject. This increases acceptance while allowing the generated distribution to change."
"A repetition penalty of 1.05 discourages repeated tokens and reduces the risk of repetition loops under permissive acceptance. We apply typical acceptance and the repetition penalty to private reasoning, while retaining strict verification for the spoken response."
## MTP evaluation and marginal acceptance (Table 7)
"Table 6 reports StepAudioChat scores, accepted draft tokens per target-model step, and wall-clock speedup for MTP3 and MTP5."

| Depth | Verification | Head 1 | Head 2 | Head 3 | Head 4 | Head 5 |
|---|---|---|---|---|---|---|
| MTP3 | Strict | 65.0% | 37.2% | 20.8% | N/A | N/A |
| MTP3 | Typical | 82.4% | 58.2% | 39.4% | N/A | N/A |
| MTP5 | Strict | 63.7% | 35.5% | 19.6% | 10.7% | 5.7% |
| MTP5 | Typical | 80.6% | 55.7% | 37.6% | 24.9% | 16.4% |

"Under typical acceptance, MTP5 accepts more drafts per step than MTP3 (2.153 versus 1.801). Table 7 shows similar acceptance rates for the first three heads at both depths. The fourth and fifth heads add accepted drafts, but their strict marginal acceptance rates fall to 10.7% and 5.7%, respectively."
"Acceptance alone does not determine net efficiency, which also depends on reasoning length and decoding costs. The reported wall-clock ratios therefore should not be interpreted as a controlled comparison of draft depth. Keeping strict verification for spoken output does not eliminate errors arising from incomplete private reasoning."
## Model merging for capability integration (§6.4)
"We train multiple compatible teacher checkpoints from a common base model, using a different data composition for each teacher. The mixtures emphasize complementary capabilities, including multi-turn dialogue, audio understanding, general text reasoning and knowledge, and targeted mixed-domain behavior."
"We integrate the specialized teachers by directly averaging their parameters. For teacher parameters θi, the merged model is θmerge = Σ αi θi, where αi ≥ 0 and Σαi = 1." Coefficients are "selected against held-out evaluations spanning dialogue, audio understanding, and general text capabilities" with "four teachers with a normalized 3:1:1:1 weighting." "Because integration occurs in parameter space, it introduces neither additional model components nor inference-time routing."
"Weighted merging is intended to retain complementary strengths rather than make the merged model identical to the best teacher on every metric."
| Domain | Benchmark | Merged | Teacher 1 | Teacher 2 | Teacher 3 | Teacher 4 |
|---|---|---|---|---|---|---|
| Audio Understanding | BigBench Audio | 98.1 | 96.1 | 98.1 | 98.4 | 98.5 |
| Audio Understanding | AudioMultiChallenge | 49.3 | 49.1 | 49.8 | 50.2 | 47.6 |
| Audio Understanding | MMSU | 90.6 | 85.5 | 85.5 | 90.4 | 90.9 |
| Audio Understanding | MMAU | 79.0 | 78.5 | 78.8 | 77.8 | 77.7 |
| Audio Understanding | WildSpeech | 77.1 | 76.5 | 76.4 | 75.9 | 76.1 |
| Audio Understanding | MMAR | 86.5 | 85.4 | 86.4 | 87.3 | 86.5 |
| Audio Understanding | Step-Caption | 78.2 | 75.8 | 78.3 | 79.6 | 79.4 |
| Audio Understanding | MTalk-Bench | 91.7 | 91.8 | 90.3 | 90.9 | 90.7 |
| Audio Understanding | Macro Average | 81.3 | 79.8 | 80.5 | 81.3 | 80.2 |
| General Text | HMMT 2026 Feb | 86.8 | 44.0 | 82.2 | 81.3 | 79.8 |
| General Text | GPQA Diamond | 83.0 | 73.1 | 81.9 | 80.1 | 80.1 |
| General Text | MultiChallenge | 59.7 | 54.6 | 51.3 | 50.6 | 59.7 |
| General Text | Macro Average | 76.5 | 57.2 | 71.8 | 70.7 | 73.2 |
| Dialogue | Instruction Following | 66.3 | 64.2 | 64.5 | 69.3 | 64.2 |
| Dialogue | Faithfulness | 72.4 | 74.0 | 65.6 | 67.1 | 73.6 |
| Dialogue | Reasoning | 73.0 | 75.2 | 67.0 | 67.2 | 67.8 |
| Dialogue | Memory | 72.0 | 73.4 | 70.0 | 68.3 | 71.5 |
| Dialogue | Knowledge | 73.1 | 75.1 | 63.7 | 62.0 | 75.6 |
| Dialogue | Safety & Reliability | 79.0 | 79.2 | 75.7 | 75.6 | 78.0 |
| Dialogue | Conversational Pragmatics | 67.2 | 67.8 | 62.4 | 63.4 | 64.5 |
| Dialogue | Persona & Role | 80.9 | 84.7 | 79.5 | 76.9 | 83.0 |
| Dialogue | Macro Average | 73.0 | 74.2 | 68.6 | 68.7 | 72.3 |

"These measurements evaluate the underlying reasoning model and are separate from the system-level evaluations that additionally use the realtime reasoning mechanisms described above."
## Full-duplex voice agent: request routing (§7–7.1)
"StepAudio 3 Realtime extends its full-duplex interaction capabilities to tool-grounded task execution. The model selects among direct responses, lightweight tool calls, and asynchronous backend execution based on the requirements of each request."
"The model handles routine conversation and questions about stable knowledge directly. Requests for up-to-date public information are routed to lightweight tools such as weather lookup or web search. Requests involving private context, multi-step processing, or work extending beyond the current conversational turn are delegated to the backend."
"Asynchronous execution allows longer-running tasks to proceed alongside the conversation, enabling the user to ask about progress or provide additional requirements while work is underway."
**Covers:** §6 (Table 6 domain baseline) through §7.1 (MTP3/MTP5 with Medusa-typical acceptance, Table 7 marginal acceptance, §6.4 teacher merging with Table 8, voice-agent routing)
