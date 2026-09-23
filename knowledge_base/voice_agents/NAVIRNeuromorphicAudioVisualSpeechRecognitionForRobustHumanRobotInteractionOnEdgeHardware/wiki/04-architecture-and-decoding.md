> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Architecture Purpose-Designed for the BrainChip Akida
**In one sentence:** NAVIR factorises encoding into Akida-compatible per-frame spatial and temporal stages for video plus a parallel MFCC spectrogram encoder, fuses them through an MLP head, and decodes with grammar-constrained beam search under a hybrid 8/4/4 and 4/4/4 quantization scheme recovered by QAT.
## Key points
- Frames are processed individually rather than as a volumetric sequence because the AKD1000 does not support 3D convolutions, recurrent connections, or attention, so encoding is factorised into a spatial stage (per frame) and a temporal stage (across frames).
- Per-frame embeddings are stacked along the time axis into a 2D time × embedding-features representation, and a second Akida-compatible network applies temporal convolutions across the stack to yield a single video-clip embedding capturing motion and short-range dynamics.
- Audio is converted in parallel into Mel-frequency cepstral coefficients (MFCCs) and processed by a third AkidaNet-based encoder to yield an audio-clip embedding.
- Video-clip and audio-clip embeddings are concatenated into a joint audio-visual representation fed to a lightweight MLP predictor head outputting vocabulary logits, with per-token probabilities via softmax.
- At inference the head produces a T × V token-score matrix (clip windows × vocabulary) decoded by constrained beam search that restricts every per-frame transition to tokens forming a valid prefix of some legal sentence.
- Beam search maintains top-B hypotheses as partial token prefixes with accumulated scores, considering blank/silence emission, last-token repeat, or advance to a new legal-next token, with fallback extension or shortening guaranteeing a grammatically valid output.
- Training uses CTC loss marginalising over alignments via a blank label; WER is the primary metric plus sentence-level command accuracy on the industrial-command corpus.
- Quantization uses a win/w/a triple (first-layer weight bits / later-layer weight bits / activation bits): 8/4/4 for the image and spectrogram encoders on raw inputs, 4/4/4 for the video encoder and predictor head on intermediate embeddings, followed by quantization-aware training with only ℓ2 weight decay.
---
## Architecture constraint: no 3D, recurrent, or attention ops
**Covers:** Section III lead-in, p. 4

> "Processing frames individually rather than as a volumetric sequence is a deliberate architectural choice, since the AKD1000 does not support 3D convolutions, recurrent connections or attention. Factorising encoding into a spatial stage (per frame) and a temporal stage (across frames) keeps the entire pipeline hardware-compatible."

## D. Video-clip temporal encoding
**Covers:** Section III-D

Once each frame has been encoded, embeddings are stacked along the time axis into a 2D representation (time × embedding features). A second Akida-compatible network applies temporal convolutions across this stack, producing a single video-clip embedding that captures motion and short-range temporal dynamics.

## E. Spectrogram-clip audio encoding
**Covers:** Section III-E

In parallel, clip audio is converted into Mel-frequency cepstral coefficients (MFCCs), described as "the standard CNN-friendly audio representation." The spectrogram is processed by a third AkidaNet-based encoder to yield an audio-clip embedding.

## F. Predictor head and audio-visual fusion
**Covers:** Section III-F

The video-clip embedding and audio-clip embedding are concatenated into a joint audio-visual representation, fed to a lightweight MLP predictor head that outputs logits over the vocabulary; per-token probabilities come from softmax.

## G. Constrained beam-search decoding
**Covers:** Section III-G

At inference the head produces a token-score matrix of shape T × V (clip windows × vocabulary). Rather than greedy decoding, a constrained beam search exploits the known grammar: both corpora consist of sentences from a fixed, finite grammar, and the decoder restricts every per-frame transition to tokens forming a valid prefix of some legal sentence.

Mechanism:
- Maintains top-B active hypotheses, each a partial token prefix plus accumulated score.
- At each frame considers three transitions: emitting blank/silence (prefix unchanged), repeating the last token (absorbing duplicates), or advancing to a new token from the legal-next-token set.
- Prunes to top-B after expansion and tracks the best fully terminated hypothesis.
- Fallback: if no beam reaches a valid terminal sentence, extends the best partial prefix into the nearest valid sentence; if no extension exists, progressively shortens the prefix, ultimately defaulting to the globally shortest valid sentence — guaranteeing grammatically valid output.

## H. Training and quantization
**Covers:** Section III-H

- CTC loss marginalises over all frame-to-token alignments via a special blank label, allowing weakly supervised training with only the spoken sentence annotated.
- WER (minimum edit distance normalised by reference length) is the primary metric; sentence-level command accuracy is additionally reported for the industrial-command corpus.
- Hardware requires integer weights/activations, parameterised as win/w/a (first-layer weight bits / subsequent-layer weight bits / activation bits); standard AKD1000 models use 8/4/4 throughout.
- Hybrid scheme: image encoder and spectrogram encoder (raw pixel/spectrogram inputs) use 8/4/4; video encoder and predictor head (intermediate embeddings) use 4/4/4.
- Quantization is followed by quantization-aware training (QAT); both float and QAT phases use only ℓ2 weight decay (same regulariser as AkidaNet recipe [12]), with no magnitude pruning or ℓ1 penalty.

## IV.A GRID corpus and Table 2 hyperparameters (partial, as present in chunk)
**Covers:** Section IV-A lead-in + Table 2

GRID [18] is the canonical sentence-level lip-reading benchmark and the primary public evaluation: audio-visual recordings from 34 speakers × 1,000 sentences from a fixed six-word grammar — command (4) + colour (4) + preposition (4) + letter (25) + digit (10) + adverb (4), e.g. "set blue with H seven again" — yielding up to 64,000 distinct sentences; clips ~3 s at 25 fps, 720×576 pixels, with word-level alignments; overlapped vs. unseen-speaker splits; chosen for availability, size, and published baselines.

| Hyperparameter | GRID | NAVIR |
|---|---|---|
| Batch size | 16 | 3 |
| Epochs, float (unseen/overlap) | 30 / 100 | — / 200 |
| Epochs, QAT (unseen/overlap) | 15 / 100 | — / 200 |
| Video window (frames) | 15 | 18 |
| Video overlap (frames) | 10 | 12 |
| Audio (spectrogram) window | 60 | 60 |
| Sample rate (Hz) | 50,000 | 32,000 |
| FFT points | 2,048 | 1,024 |
| Hop length | 512 | 320 |
| Mel bands | 112 | 112 |
| Noise augmentation ratio | 0.8 | 0.8 |
| SNR sweep (dB) | {−15, −10, −5, 0} | {−15, −10, −5, 0} |
| Image encoder (α) | 0.50 | 0.25 |
| Spec encoder (α) | 0.50 | 0.25 |
| Video encoder dim (α) | 256 (1.0) | 128 (0.5) |
| Predictor head (units) | 512, 256 | 256 |

**Covers:** Sections III (lead-in), III-D–III-H, IV-A lead-in + Table 2, p. 4
