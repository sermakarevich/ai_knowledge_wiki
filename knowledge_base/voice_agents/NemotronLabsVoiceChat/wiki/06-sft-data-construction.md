> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# SFT Data Construction. Like the CPT
**In one sentence:** Like CPT, the SFT stage builds its corpora by rendering text turns into speech with TTS onto a two-channel duplex timeline, retaining a large share of pretraining-style data while adding conversational, instruction-tuning, tool-calling, and text-only knowledge buckets plus online full-duplex augmentations.
## Key points
- SFT renders text turns into speech with TTS and assembles them onto a two-channel duplex timeline with user and agent on separate channels and realistic inter-turn timing.
- CPT trains almost entirely on TTS-rendered pretraining data, while SFT retains a large share of it and adds instruction-tuning, conversational, and tool-calling corpora.
- The extract-knowledge pretraining subset is kept in text form, contributing a text-to-text loss at weight 0.5 in SFT versus 0 in CPT, preserving text-domain competence.
- Tool-calling data is the exception: text tool-calling transcripts contain URLs, markdown, and code with no spoken realization and train poorly on tool relevance, so it is built by a multi-agent pipeline instead of TTS rendering.
- SFT raw sampler weights sum to 1.175 (retention 0.55, conversational 0.28, tool calling 0.305, safety 0.04), normalizing to ~46.8%, ~23.8%, ~26.0%, and ~3.4%.
- SFT adds three online dialogue transformations: early interruption (p = 0.1, truncate mid-utterance + 8 frames / 640 ms overlap), backchannel injection (p = 0.05 per sample, 0.5 per agent turn, loudness-matched), and text-channel delay (agent text targets shifted 2 frames / 160 ms; function channel unshifted).
- Acoustic robustness is raised in the same pass: additive DNS5 and DEMAND noise probability goes from p = 0.1 in CPT to p = 0.5 in SFT at SNR −30 to 60 dB, plus room impulse responses (p = 0.8), microphone impulse responses (p = 0.6), and codec augmentation (p = 0.1), all disabled in CPT.
---
## SFT construction like CPT
SFT draws its corpora from the text-only Nemotron backbone rather than natively recorded conversational speech, rendering text turns into speech with TTS and assembling them onto a two-channel duplex timeline with realistic inter-turn timing. CPT applies only mild additive noise, since its objective is speech-text alignment rather than dialogue behavior.
**Covers:** SFT data construction following the CPT approach.

## Tool-calling data: the exception
Tool-calling data cannot be obtained by rendering an existing text corpus, so it is produced by a multi-agent pipeline that generates scenarios, turn plans, executable tool backends, and simulated conversations, followed by voice adaptation through filtering, normalization, TTS with diverse reference voices, ASR round-trip verification, and dialogue assembly. The tool-calling mixture includes multi-turn conversations interleaving tool use, abstention, and open-domain chat, plus greetings and user interruptions, teaching when to invoke a tool and when to continue without one.
**Covers:** SFT data construction following the CPT approach.

## A.2. Data mixture
Table 5 reports raw sampling weights for weighted randomized round-robin fusion; SFT weights are normalized by the sampler. CPT assigns 0.95 to speech-text pretraining and 0.05 to single-turn QA.

| Data bucket | Scale | CPT | SFT |
|---|---|---|---|
| Retention: Speech-text pretraining | ≈530k | 0.95 | 0.40 |
| Retention: Text-only knowledge (extract-knowledge shards, text) | extract-knowledge shards (text) | – | 0.10 |
| Retention: Spoken MCQ | ≈24k h | – | 0.03 |
| Retention: Single-turn QA | ≈12k h | 0.05 | 0.02 |
| Conversational: Duplex chat | ≈72k h / 4.3M dialogues | – | 0.15 |
| Conversational: Natural voice conversations | ≈4.2k h / 45k conv. | – | 0.08 |
| Conversational: VoiceBench-targeted | ≈3.8k h / 37k conv. | – | 0.04 |
| Conversational: Voice-agent instruction following | instruction-following shards | – | 0.01 |
| Tool calling (all) | ≈7.0k h / 268k conv. | – | 0.305 |
| Safety: Spoken safety alignment | ≈1.1k h / 48k conv. | – | 0.04 |
| Total | | 1.00 | 1.175 |

**Covers:** SFT data construction following the CPT approach.

## A.3. Conversational augmentation
Turn-based data does not by itself supervise full-duplex interaction, so SFT introduces three online transformations:
- Early interruption (p = 0.1): a randomly selected agent turn is truncated mid-utterance and continues for eight further frames (640 ms) before EOS, so the following user turn overlaps agent speech; shards with pre-rendered interruptions opt out via a per-group tag.
- Backchannel injection (p = 0.05 per sample, 0.5 per agent turn): recorded backchannel audio is loudness-matched into the user channel during agent speech, so acknowledgements such as "uh-huh" are not interpreted as interruptions.
- Text-channel delay: during SFT, agent text targets are shifted two frames (160 ms) later, providing additional user audio before the model commits to each token; the function channel is not shifted, preserving the true temporal position of each tool call.
**Covers:** SFT data construction following the CPT approach.
