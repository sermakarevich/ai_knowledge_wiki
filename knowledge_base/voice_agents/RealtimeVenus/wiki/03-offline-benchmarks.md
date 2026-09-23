[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Offline benchmarks (chart fragments)
**In one sentence:** This chunk is heavily garbled OCR consisting mostly of Figure 1 and Figure 2 captions plus the numeric full-duplex score tables from Figure 2, with no readable prose argument.
## Key points
- The chunk body is garbled OCR text (e.g., "O ffli n e", "Ben", "ch", "ar", "k", scattered numbers such as 21, 59, 56, 76) with no complete prose sentences.
- The chunk contains the verbatim caption "Figure 1 Understanding performance of Realtime-Venus."
- The chunk contains the verbatim caption "Figure 2 Full-duplex interaction performance of Realtime-Venus."
- Figure 2 in the chunk is organized into four scenarios — User Interruption, User Backchannel, Talking to Other, Background Speech — each split into C_RESPOND and C_RESUME columns.
- Under User Interruption C_RESPOND, the chunk lists Joy-Duplex 0.88, GPT-4o 0.78, Gemini 3.1 Live 0.77, RT-Venus-Audio 0.75, Freeze-Omni 0.72, RT-Venus-Omni 0.60, MiniCPM-o 4.5 0.60, Moshi 0.50.
- Under User Backchannel C_RESUME, the chunk lists RT-Venus-Audio 0.97, Joy-Duplex 0.96, Gemini 3.1 Live 0.95, MiniCPM-o 4.5 0.95, RT-Venus-Omni 0.92, Freeze-Omni 0.80, GPT-4o 0.70, Moshi 0.06.
- Under Talking to Other and Background Speech the chunk lists paired extremes, e.g., Talking-to-Other C_RESPOND GPT-4o 0.91 vs RT-Venus-Omni 0.06, and Background-Speech C_RESPOND GPT-4o 0.93 vs Joy-Duplex 0.10.
- Fragmentary labels mention "Offline Model" vs "Online Model" and model names including Qwen3-Omni, Qwen3.5, FunAudio-Chat, MiniCPM-o 4.5, Daily-Omni, MiniCPM-o 4.5, RT-Venus-Omni, RT-Venus-Audio, VoiceBench, AlpacaEval, WorldSense, MMSU, and Step-Audio2-mini, but the surrounding sentences are unreadable.
---
## Figure 1 fragment
**Covers:** Offline benchmark context and chart fragments

The only readable Figure 1 content is its caption and scattered axis/model tokens:

> Figure 1 Understanding performance of Realtime-Venus.

Readable fragments (verbatim tokens, order garbled): "O ffli n e", "21", "59", "56", "Offline Model", "76", "45", "33", "Ben", "25", "Qwen3-Omni", "ti o", "64", "69", "80", "FunAudio-Chat", "ch", "Qwen3.5", "nA", "m", "50", "29", "44", "69", "MiniCPM-o 4.5", "82", "ns", "84", "ar", "Online Model", "w", "Qwen-3-omni", "k", "e rin", "Daily-Omni", "55", "OmniPro", "JoyAI-VL-Interaction", "Llama g", "55", "MMSU", "MiMo-Audio", "MiniCPM-o 4.5", "Questions", "Step-Audio2-mini", "RT-Venus-Omni", "RT-Venus-Audio", "WorldSense", "VoiceBench AlpacaEval".

## Figure 2 full-duplex tables (verbatim numbers)
**Covers:** Offline benchmark context and chart fragments

Verbatim caption:

> Figure 2 Full-duplex interaction performance of Realtime-Venus.

Tables as they appear in the chunk (verbatim values):

### User Interruption
| | C_RESPOND | | C_RESUME |
|---|---|---|---|
| Joy-Duplex | 0.88 | Joy-Duplex | 0.07 |
| GPT-4o | 0.78 | GPT-4o | 0.10 |
| Gemini 3.1 Live | 0.77 | Freeze-Omni | 0.12 |
| RT-Venus-Audio | 0.75 | Gemini 3.1 Live | 0.20 |
| Freeze-Omni | 0.72 | RT-Venus-Audio | 0.23 |
| RT-Venus-Omni | 0.60 | Moshi | 0.26 |
| MiniCPM-o 4.5 | 0.60 | MiniCPM-o 4.5 | 0.36 |
| Moshi | 0.50 | RT-Venus-Omni | 0.37 |

### User Backchannel
| | C_RESPOND | | C_RESUME |
|---|---|---|---|
| RT-Venus-Audio | 0.00 | RT-Venus-Audio | 0.97 |
| MiniCPM-o 4.5 | 0.00 | Joy-Duplex | 0.96 |
| Joy-Duplex | 0.01 | Gemini 3.1 Live | 0.95 |
| RT-Venus-Omni | 0.02 | MiniCPM-o 4.5 | 0.95 |
| Moshi | 0.02 | RT-Venus-Omni | 0.92 |
| Gemini 3.1 Live | 0.02 | Freeze-Omni | 0.80 |
| GPT-4o | 0.03 | GPT-4o | 0.70 |
| Freeze-Omni | 0.07 | Moshi | 0.06 |

### Talking to Other
| | C_RESPOND | | C_RESUME |
|---|---|---|---|
| RT-Venus-Omni | 0.06 | RT-Venus-Omni | 0.90 |
| RT-Venus-Audio | 0.11 | RT-Venus-Audio | 0.88 |
| Joy-Duplex | 0.17 | MiniCPM-o 4.5 | 0.79 |
| MiniCPM-o 4.5 | 0.18 | Joy-Duplex | 0.72 |
| Moshi | 0.20 | Gemini 3.1 Live | 0.66 |
| Gemini 3.1 Live | 0.27 | Freeze-Omni | 0.25 |
| Freeze-Omni | 0.58 | Moshi | 0.19 |
| GPT-4o | 0.91 | GPT-4o | 0.02 |

### Background Speech
| | C_RESPOND | | C_RESUME |
|---|---|---|---|
| Joy-Duplex | 0.10 | RT-Venus-Audio | 0.86 |
| RT-Venus-Audio | 0.11 | RT-Venus-Omni | 0.85 |
| RT-Venus-Omni | 0.12 | Joy-Duplex | 0.85 |
| MiniCPM-o 4.5 | 0.16 | MiniCPM-o 4.5 | 0.82 |
| Moshi | 0.21 | Gemini 3.1 Live | 0.66 |
| Gemini 3.1 Live | 0.28 | Freeze-Omni | 0.25 |
| Freeze-Omni | 0.62 | Moshi | 0.07 |
| GPT-4o | 0.93 | GPT-4o | 0.04 |

Note: no mechanism, definition of C_RESPOND/C_RESUME, or interpretation is stated anywhere in this chunk; the page above reproduces only what the chunk contains.
