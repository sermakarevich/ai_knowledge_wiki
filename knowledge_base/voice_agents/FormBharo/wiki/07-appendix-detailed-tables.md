> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Appendix: Detailed Tables — Per-Turn Extraction Accuracy and Model Selection
**In one sentence:** The appendix reports per-turn EXTRACT accuracy (Table 10) and end-to-end form-completion accuracy (Table 11) using reference transcripts and three STT-model outputs, plus REPLY selection results (Tables 12–13, Figure 4) and implementation, environment, and determinism details.
## Key points
- Table 10 reports per-turn extraction accuracy for 11 models across Reference, Saaras v3, Scribe v2, and Nova-3 inputs, with confidence intervals reflecting variation across test items (each configuration evaluated once).
- On reference transcripts, Gemini 3 Flash and Gemini 3.5 Flash both reach 100.00 ± 0.00%, followed by GPT-5.5 at 99.95 ± 0.09% and Claude Sonnet 4.6 at 99.66 ± 0.23%.
- On STT outputs, the highest per-column scores in Table 10 are Claude Opus 4.8 / Gemini Pro on Saaras v3 (92.22 ± 0.61 / 92.55 ± 0.52), Gemini Pro on Scribe v2 (93.47 ± 0.45), and Gemini 3.5 Flash on Nova-3 (87.09 ± 0.76).
- GLM-5.1 collapses on Scribe v2 transcripts (58.66 ± 1.46%) despite 99.56 ± 0.27% on reference and 90.92 ± 0.75% / 86.09 ± 0.75% on Saaras v3 / Nova-3.
- Table 11 reports end-to-end form-completion (response) accuracy for 5 models on Reference and Scribe v2, with latency and cost per turn: Claude Sonnet 4.6 reaches 100.00 ± 0.00% / 97.77 ± 0.75% at 5148 ± 392 ms and $0.0146 ± $0.0000, while GPT-5.4-mini reaches 98.09 ± 1.28% / 96.70 ± 0.85% at 3356 ± 523 ms and $0.0008 ± $0.0000.
- For REPLY selection, GPT-5.4-mini "is optimal throughout 0.50 ≤ wa ≤ 0.90 (wℓ = 0.1), among the models on the Pareto frontier (Figure 4), with a consistent composite score of U = 0.9 across the sweep."
- Table 13 gives the optimal EXTRACT model under "weighted-sum scalarization method for 0.50 ≤ wa ≤ 0.90 with wℓ = 0.1" (wc = 1 − wa − wℓ): Gemini 3.5 Flash is optimal at wa = 0.50–0.61 (U = 0.763–0.764), Claude Sonnet 4.6 from wa = 0.62–0.90 (U = 0.767–0.900).
---
## Table 10: Per-turn extraction accuracy
Table 10: "Per-turn extraction accuracy using reference transcripts and the outputs of the three STT models as inputs."

| Model | Reference | Saaras v3 | Scribe v2 | Nova-3 |
|---|---|---|---|---|
| Gemini 3 Flash | 100.00 ± 0.00 | 85.24 ± 0.77 | 89.48 ± 0.60 | 83.92 ± 1.01 |
| Gemini 3.5 Flash | 100.00 ± 0.00 | 90.74 ± 0.61 | 92.50 ± 0.53 | 87.09 ± 0.76 |
| GPT-5.5 | 99.95 ± 0.09 | 89.97 ± 0.73 | 89.37 ± 0.64 | 84.73 ± 0.80 |
| Claude Sonnet 4.6 | 99.66 ± 0.23 | 91.55 ± 0.71 | 93.01 ± 0.50 | 84.54 ± 0.77 |
| GLM-5.1 | 99.56 ± 0.27 | 90.92 ± 0.75 | 58.66 ± 1.46 | 86.09 ± 0.75 |
| Claude Opus 4.8 | 99.41 ± 0.31 | 92.22 ± 0.61 | 92.03 ± 0.56 | 85.83 ± 0.88 |
| Gemini 2.5 Flash | 99.06 ± 0.38 | 91.76 ± 0.70 | 92.39 ± 0.52 | 85.50 ± 0.73 |
| Gemini Pro | 98.90 ± 0.42 | 92.55 ± 0.52 | 93.47 ± 0.45 | 86.53 ± 0.70 |
| GPT-5.4-mini | 98.35 ± 0.48 | 90.68 ± 0.75 | 90.10 ± 0.55 | 84.40 ± 0.79 |
| GPT-4.1 | 95.99 ± 0.70 | 88.82 ± 0.74 | 91.50 ± 0.53 | 86.33 ± 0.74 |
| Mistral Medium 3.5 | 92.83 ± 0.68 | 90.39 ± 0.68 | 91.84 ± 0.49 | 83.37 ± 0.76 |

## Table 11: End-to-end form-completion accuracy
Table 11: "End-to-end form-completion accuracy using reference transcripts and the outputs of the three STT models as inputs." (Columns shown: Response accuracy Reference / Scribe v2, Latency (ms), Cost ($/turn).)

| Model | Reference | Scribe v2 | Latency (ms) | Cost ($/turn) |
|---|---|---|---|---|
| Claude Sonnet 4.6 | 100.00 ± 0.00 | 97.77 ± 0.75 | 5148 ± 392 | 0.0146 ± 0.0000 |
| GPT-4.1 | 100.00 ± 0.00 | 96.60 ± 0.91 | 3647 ± 656 | 0.0025 ± 0.0001 |
| GPT-5.4-mini | 98.09 ± 1.28 | 96.70 ± 0.85 | 3356 ± 523 | 0.0008 ± 0.0000 |
| Gemini 3 Flash | 97.23 ± 1.49 | 96.17 ± 0.96 | 2661 ± 239 | 0.0017 ± 0.0000 |
| Gemini 3.5 Flash | 97.02 ± 1.28 | 94.73 ± 1.11 | 3496 ± 1322 | 0.0052 ± 0.0001 |

## Table 12 and Section D: EXTRACT / REPLY selection
Table 12: "REPLY response accuracy using reference transcripts and transcripts from Scribe v2 as inputs." — the numeric body of Table 12 is not present/garbled in this chunk, so no values are reported here.

- D.1 EXTRACT Selection: "Table 13 gives the optimal EXTRACT model using the weighted-sum scalarization method for 0.50 ≤ wa ≤ 0.90 with wℓ = 0.1."
- D.2 REPLY Selection: "GPT-5.4-mini is optimal throughout 0.50 ≤ wa ≤ 0.90 (wℓ = 0.1), among the models on the Pareto frontier (Figure 4), with a consistent composite score of U = 0.9 across the sweep."

## Table 13: Optimal EXTRACT model under weighted-sum scalarization
Table 13: "Optimal EXTRACT model under weighted-sum scalarization for 0.50 ≤ wa ≤ 0.90, with wℓ = 0.1 and wc = 1 − wa − wℓ, and its composite score U."

| wa | wc | Model | U | wa | wc | Model | U | wa | wc | Model | U |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.50 | 0.40 | Gemini 3.5 Flash | 0.763 | 0.64 | 0.26 | Sonnet 4.6 | 0.776 | 0.78 | 0.12 | Sonnet 4.6 | 0.843 |
| 0.51 | 0.39 | Gemini 3.5 Flash | 0.763 | 0.65 | 0.25 | Sonnet 4.6 | 0.781 | 0.79 | 0.11 | Sonnet 4.6 | 0.848 |
| 0.52 | 0.38 | Gemini 3.5 Flash | 0.763 | 0.66 | 0.24 | Sonnet 4.6 | 0.786 | 0.80 | 0.10 | Sonnet 4.6 | 0.852 |
| 0.53 | 0.37 | Gemini 3.5 Flash | 0.763 | 0.67 | 0.23 | Sonnet 4.6 | 0.791 | 0.81 | 0.09 | Sonnet 4.6 | 0.857 |
| 0.54 | 0.36 | Gemini 3.5 Flash | 0.763 | 0.68 | 0.22 | Sonnet 4.6 | 0.795 | 0.82 | 0.08 | Sonnet 4.6 | 0.862 |
| 0.55 | 0.35 | Gemini 3.5 Flash | 0.763 | 0.69 | 0.21 | Sonnet 4.6 | 0.800 | 0.83 | 0.07 | Sonnet 4.6 | 0.867 |
| 0.56 | 0.34 | Gemini 3.5 Flash | 0.764 | 0.70 | 0.20 | Sonnet 4.6 | 0.805 | 0.84 | 0.06 | Sonnet 4.6 | 0.871 |
| 0.57 | 0.33 | Gemini 3.5 Flash | 0.764 | 0.71 | 0.19 | Sonnet 4.6 | 0.810 | 0.85 | 0.05 | Sonnet 4.6 | 0.876 |
| 0.58 | 0.32 | Gemini 3.5 Flash | 0.764 | 0.72 | 0.18 | Sonnet 4.6 | 0.814 | 0.86 | 0.04 | Sonnet 4.6 | 0.881 |
| 0.59 | 0.31 | Gemini 3.5 Flash | 0.764 | 0.73 | 0.17 | Sonnet 4.6 | 0.819 | 0.87 | 0.03 | Sonnet 4.6 | 0.886 |
| 0.60 | 0.30 | Gemini 3.5 Flash | 0.764 | 0.74 | 0.16 | Sonnet 4.6 | 0.824 | 0.88 | 0.02 | Sonnet 4.6 | 0.890 |
| 0.61 | 0.29 | Gemini 3.5 Flash | 0.764 | 0.75 | 0.15 | Sonnet 4.6 | 0.829 | 0.89 | 0.01 | Sonnet 4.6 | 0.895 |
| 0.62 | 0.28 | Sonnet 4.6 | 0.767 | 0.76 | 0.14 | Sonnet 4.6 | 0.833 | 0.90 | 0.00 | Sonnet 4.6 | 0.900 |
| 0.63 | 0.27 | Sonnet 4.6 | 0.772 | 0.77 | 0.13 | Sonnet 4.6 | 0.838 | | | | |

## Figure 4: Cost–quality–latency trade-off
Figure 4: "Cost–quality–latency trade-off among REPLY models satisfying the deployment constraints. The logarithmic x-axis shows cost per turn, the y-axis shows response accuracy using Scribe v2 transcripts, and marker area encodes p95 latency per turn (bigger is slower). Both models are Pareto-optimal across the three objectives. The model selected for deployment is highlighted." Plotted points in the chunk: GPT-5.4-mini (96.8%–96.4% response-accuracy band) and Gemini 3 Flash (~96.0–96.2%), over cost $0.001–$0.002.

## Implementation details, environment, and determinism
- Orchestration/telephone: "We use Pipecat (Pipecat AI 2026a) for orchestration and Exotel (Exotel 2026) for telephony, which delivers 8 kHz µ-law audio over a WebSocket."
- VAD (Silero at 8 kHz): "It marks the start of speech after 0.1 s, the end after 0.2 s of silence, and ignores any audio that scores below 0.7 confidence or 0.6 loudness. The agent waits a further 0.4 s after that before marking the turn as completed, so a caller pausing mid-answer is not cut off. If the caller has not spoken for more than 3.0 s since the agent stopped speaking, we re-prompt."
- Benchmark audio: "Each audio file in the benchmark is 16 kHz mono 16-bit PCM."
- Models: "All LLM calls are served through OpenRouter (OpenRouter 2026). We set the temperature to 0 for non-reasoning models, and the reasoning effort to "medium" for EXTRACT and "low" for REPLY. For both, we cap the output at 16,000 tokens and pass the most recent 200 turns of the conversation as input."
- TTS: "For TTS, we use Google Cloud Chirp 3 HD (Google Cloud 2026) with the female Hindi voice Achernar, slowed to 0.9× the default speed so the questions are easier to follow."
- Evaluation harness: "All STT and LLM evaluations were run using Calibrate (Dalmia and Doshi 2025)."
- Environment: "Experiments were run from a MacBook Pro (Apple M4 Pro, 24 GB) on macOS 15.7 with Python 3.11, using pipecat-ai 1.2.1, openai 2.15.0, instructor 1.13.0, pydantic 2.12.3, jiwer (Vaessen 2024) 4.0.0, indic-nlp-library (Kunchukuttan 2020) 0.92, pydub 0.25.1 and numpy 2.2.6."
- Determinism: "No random seeds were set: every model is served by a hosted API that offers no determinism guarantee, so identical settings can still produce different outputs. Each configuration was evaluated once over the full test suite, so the confidence intervals in Section C reflect variation across test items rather than across repeated runs."

**Covers:** appendix accuracy tables with confidence intervals and per-model breakdowns.
