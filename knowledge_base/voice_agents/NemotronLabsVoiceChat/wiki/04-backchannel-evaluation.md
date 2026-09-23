[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Respond Resume Uncertain Unknown Model (↓)
**In one sentence:** Among open full-duplex models V-Model ties Freeze-Omni on VoiceBench (55.1 vs 55.2) with strong knowledge-task gains but weaker open-ended/IFEval scores, and it leads open models on FDB 3.0 tool-selection F1 (82.5%) while trailing on argument accuracy and Pass@1, within a design whose limitations include a ~2-minute audio context window and imperfect multi-tool use.
## Key points
- V-Model obtains a normalized VoiceBench average of 55.1, improving over Moshi by 25.6 points and PersonaPlex by 24.5 points, and effectively tying Freeze-Omni at 55.2.
- Relative to Freeze-Omni, V-Model scores substantially higher on OpenBookQA (61.3 vs 31.0), MMSU (46.1 vs 28.1), and AdvBench safety (100.0 vs 97.3), offset by weaker SD-QA, open-ended response-quality subsets, and IFEval.
- The cascaded DuplexCascade system averages 65.4 while omni-modal MiniCPM-o 4.5 averages 76.1 in the independent Raon-Speech evaluation with a different judge, serving only as a system-level reference across full-duplex design choices.
- On FDB 3.0 spoken tool use with disfluent human speech and chained API calls, the model achieves 82.5% tool-selection F1, outperforming Gemini Live 2.5 (78.6%) and Gemini Live 3.1 (81.7%).
- Argument accuracy (42.2%) and Pass@1 (33.0%) trail both Gemini Live baselines, and because Pass@1 requires exactly the expected tools with perfect arguments, the gap shows routing is stronger than argument extraction and end-to-end execution.
- The model uses parallel specialized streams for agent text, function calls, and user transcription plus a streaming TTS decoder and an RNN-T branch sharing the speech encoder, enabling continuous listen/speak/transcribe/tool-invoke behavior.
- Limitations include at most ~2-minute audio context windows, degraded tool use with many tools (recommendation: no more than five per session), unreliable simultaneous multi-tool invocation, invented arguments, answering from internal knowledge instead of invoking tools, delayed speech after long tool responses, no barge-in during tool execution, and limited robustness in noisy/reverberant conditions with competing speech.
---
## FDB backchannel fragment
**Covers:** backchannel behavior classes (Respond/Resume/Uncertain/Unknown) and model comparison.

Chunk preserves only a garbled fragment of this table (columns rendered as Respond Resume Uncertain Unknown / Model (↓) (↑) (↓) (↓)):

| Model | (↓) | (↑) | (↓) | (↓) |
|---|---|---|---|---|
| Open-weight systems | | | | |
| Moshi | 2.0 | 6.0 | 0.0 | 92.0 |
| Freeze-Omni | 7.0 | 80.0 | 2.0 | 11.0 |
| MoshiRAG† | 5.0 | 61.0 | 0.0 | 34.0 |
| V-Model | 1.0 | 93.0 | 2.0 | 4.0 |
| Closed-API systems | | | | |
| Gemini Live 2.0 | 1.0 | 93.0 | 2.0 | 4.0 |
| GPT-4o Realtime | 3.0 | 70.0 | 1.0 | 25.0 |

> "Moshi, Freeze-Omni, Gemini Live, and GPT-4o Realtime values are reported by the FDB 1.5 benchmark [27]. MoshiRAG† values are reported by its authors [15]; this separate evaluation was not part of the controlled FDB run. Closed-system names refer to the evaluated historical endpoints, not necessarily their current service versions."

## VoiceBench intelligence (Table 3)
CommonEval (CE), AlpacaEval-Full (AE), and WildVoice (WV) are reported on a 1–5 scale; all other task scores and the normalized average are on a 0–100 scale; higher is better; FD = full-duplex speech-to-speech, Cascade-FD = full-duplex cascaded ASR–LLM–TTS, Omni-FD = omni-modal model supporting full-duplex interaction.

| Model | Arch. | OBQA | MMSU | CE | SD-QA | AE | BBH | WV | IFEval | AdvBench | Avg. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Moshi | FD | 25.9 | 24.0 | 1.6 | 15.6 | 2.0 | 47.4 | 1.3 | 10.1 | 44.2 | 29.5 |
| PersonaPlex‡ | FD | 24.4 | 24.9 | 2.3 | 18.8 | 2.7 | 49.4 | 2.0 | 12.0 | 8.1 | 30.6 |
| Freeze-Omni | FD | 31.0 | 28.1 | 3.5 | 53.5 | 4.0 | 50.7 | 3.2 | 23.4 | 97.3 | 55.2 |
| DuplexCascade | Cascade-FD | 56.0 | 52.9 | 3.6 | 45.6 | 4.4 | 59.8 | 3.6 | 43.4 | 99.0 | 65.4 |
| MiniCPM-o 4.5† | Omni-FD | 87.7 | 66.7 | 3.6 | 68.4 | 4.2 | 55.0 | 3.6 | 80.6 | 98.9 | 76.1 |
| V-Model | FD | 61.3 | 46.1 | 3.0 | 32.6 | 3.4 | 51.7 | 2.8 | 19.3 | 100.0 | 55.1 |

> "Moshi and Freeze-Omni values are taken from the public VoiceBench leaderboard. PersonaPlex was evaluated from its released checkpoint by the DuplexCascade authors [10, 30]; these values were not reported in the original PersonaPlex paper. DuplexCascade values are reported by its authors [30]. MiniCPM-o 4.5† values are reported by the independent Raon-Speech evaluation [31], which uses GPT-5.4 to judge the three open-ended subsets; its judge-based scores and aggregate are therefore not directly matched to the official-leaderboard evaluation."

VoiceBench covers nine subsets: elementary science reasoning (OpenBookQA), multidisciplinary knowledge (MMSU), general reasoning (BBH), factual QA (SD-QA), open-ended quality (CommonEval, AlpacaEval-Full, WildVoice), instruction following (IFEval), and safety (AdvBench); OBQA/MMSU/BBH are multiple-choice, SD-QA is free-form scored against references, and the three response-quality subsets are open-ended judged on 1–5.

## Tool calling — FDB 3.0 (Table 4)
| Model | Tool Sel. F1 (↑) | Arg. Acc. (↑) | Pass@1 (↑) |
|---|---|---|---|
| Ours | 82.5 | 42.2 | 33.0 |
| Gemini Live 2.5 | 78.6 | 59.3 | 49.0 |
| Gemini Live 3.1 | 81.7 | 58.8 | 54.0 |

> "To the best of our knowledge, our model is the first fully open full-duplex speech model to support tool calling."
> "Because FDB 3.0 counts a sample as Pass@1 only when the model selects exactly the expected tools and supplies perfect arguments for every call, this gap indicates that tool routing is substantially stronger than argument extraction and end-to-end execution."

## Conclusion (verbatim)
> "We introduced NemotronLabs VoiceChat, an open, unified full-duplex speech-to-speech model with native tool calling capabilities. A central design choice is the use of parallel, specialized streams for agent text, function calls, and user transcription, allowing tool interaction to be integrated without serializing heterogeneous actions into the conversational output stream."

## Limitations (verbatim excerpts)
> "The model is trained with audio context windows of at most approximately two minutes, and conversational information extending beyond this window may therefore not be retained reliably."
> "Tool use also remains imperfect: performance can degrade when many tools are exposed, with a practical recommendation of no more than five tools per session; simultaneous multi-tool invocation is not yet reliable; calls may be skipped, incorrectly selected, or supplied with invented arguments; and the model may answer from internal knowledge when a tool should instead be invoked."
> "Long tool responses can delay subsequent speech, and user barge-in is currently unavailable while a tool is executing."
