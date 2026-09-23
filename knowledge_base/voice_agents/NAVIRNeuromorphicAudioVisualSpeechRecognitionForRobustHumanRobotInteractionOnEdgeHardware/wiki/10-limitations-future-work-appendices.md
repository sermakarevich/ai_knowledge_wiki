> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Limitations, Future Work and Appendices
**In one sentence:** A small threshold before quantization or ℓ1-penalised fine-tuning is proposed to equalise audio-video and video-only hardware mappings (a generic AKD1000-toolchain property), and Appendix B specifies the AkidaNet image/spectrogram encoders, the NAVIR-specific temporal-video encoder, and the predictor head with exact layers, dimensions, and quantization.
## Key points
- Either a small threshold before quantization or fine-tuning under an additional ℓ1 penalty would directly reduce `incoming_conn` for every convolutional layer and is expected to equalise the audio-video and video-only mappings without further architecture changes.
- The mapping behaviour is described as a generic property of the AKD1000 toolchain, relevant to any work deploying multiple checkpoints of the same architecture on this hardware.
- Image and spectrogram encoders reuse the standard AkidaNet ImageNet model (`akida_models.akidanet_imagenet`, one-channel input) with the dropout + 1000-way dense head removed and replaced by a single dense projection with ReLU bounded at 6.0.
- The AkidaNet backbone has four full convolution blocks (conv_0–conv_3, strided at conv_0 and conv_2) plus ten separable blocks (separable_4–separable_13, strided at 4, 6, 12), with filters doubling from 32 to 1024 scaled by width multiplier α (0.50 on GRID, 0.25 on NAVIR for both encoders).
- The temporal-video encoder stacks per-frame embeddings into a (T, 1, F=128) tensor so the AKD1000 2D convolution acts as an effective 1D temporal convolution, using 3×3 conv blocks with ⌊64α⌋ / ⌊96α⌋ / ⌊128α⌋ filters, global average pooling, dropout 0.03, and a dense projection to D (256 on GRID, 128 on NAVIR).
- On NAVIR the temporal conv blocks are conv → batch normalisation → ReLU while on GRID batch normalisation is omitted (conv → ReLU), with α = 0.5 on NAVIR and 1.0 on GRID, padding `same`, stride 1, and the same ℓ2 weight decay as AkidaNet.
- The predictor head consumes the concatenated fused embedding (768-dim = 256 + 512 on GRID with two hidden layers of 512 and 256 units; 640-dim = 128 + 512 on NAVIR with one hidden layer of 256 units), all hidden activations ReLU bounded at 6.0, outputting V raw logits (including CTC blank) for CTC loss and constrained beam-search decoding, quantized to 4-bit weights/activations and fine-tuned jointly in QAT.
---
## Mapping limitation and proposed fix
> "a small threshold before quantization, or fine-tuning under an additional ℓ1 penalty. Either intervention would directly reduce incoming_conn for every convolutional layer and is expected to equalise the audio-video and video-only mappings without further changes to the architecture."
> "The mapping behaviour identified here is a generic property of the AKD1000 toolchain and therefore relevant to any work that deploys multiple checkpoints of the same architecture on this hardware."

**Covers:** chunk 10 opening fragment on quantization mapping limitation

## Appendix B: image and spectrogram encoders (AkidaNet backbone)
Both encoders are instances of the standard AkidaNet ImageNet model via `akida_models.akidanet_imagenet` with one-channel input; AkidaNet is a MobileNet-style CNN for AKD1000 compatibility. Composition: input rescaling layer, four full convolution blocks (conv_0–conv_3, strided at conv_0 and conv_2), ten separable blocks (separable_4–separable_13, strided at separable_4, separable_6, separable_12), global average pooling at separable_13 output; each block is conv → batch normalisation → ReLU. Filter counts double from 32 at conv_0 to 1024 at separable_12/separable_13, scaled by α. The classification head (dropout + 1000-way dense) is replaced with a single dense projection plus ReLU bounded at 6.0: 128-dim per-frame embeddings (image encoder), 512-dim per-clip embeddings (spectrogram encoder). Width multiplier: α = 0.50 (GRID, both encoders), α = 0.25 (NAVIR). Input shapes: 32 × 64 × 1 (image, GRID), 88 × 176 × 1 (image, NAVIR), 112 × 112 × 1 (spectrogram, both datasets). Full details per the AkidaNet specification in the BrainChip MetaTF SDK [40].

**Covers:** chunk 10, Appendix B section A

## Appendix B: temporal-video encoder
Input is stacked per-frame image embeddings of shape (T, 1, F) with F = 128; the width-1 axis lets the AKD1000 2D convolution primitive operate as an effective 1D temporal convolution.

| Layer | Kernel | Filters | Output |
|---|---|---|---|
| Input | — | — | (T, 1, 128) |
| Rescaling | — | — | (T, 1, 128) |
| video_conv_0 (block) | 3×3 | ⌊64α⌋ | (T, 1, ⌊64α⌋) |
| video_conv_1 (block) | 3×3 | ⌊96α⌋ | (T, 1, ⌊96α⌋) |
| video_conv_2 (block) | 3×3 | ⌊128α⌋ | (T, 1, ⌊128α⌋) |
| Global avg. pool | — | — | (1, 1, ⌊128α⌋) |
| Dropout (0.03) | — | — | (1, 1, ⌊128α⌋) |
| video_dense | — | D | (D) |
| Batch norm. + ReLU | — | — | (D) |

Output dimension D is 256 on GRID and 128 on NAVIR; α is 1.0 on GRID and 0.5 on NAVIR; filter counts use width multiplier α. On NAVIR conv blocks are conv → batch normalisation → ReLU; on GRID batch normalisation is omitted (conv → ReLU). All conv layers use padding = `same`, stride 1, preserving the temporal axis; global average pooling collapses it to one clip embedding projected to D by a dense layer with batch normalisation and bounded ReLU, with the same ℓ2 weight decay as AkidaNet.

**Covers:** chunk 10, Appendix B section B + Table 13

## Appendix B: predictor head
A small MLP on the concatenated (Dv + Ds)-dimensional fused embedding emitting per-clip token logits of dimension V (vocabulary including CTC blank); depth differs by dataset. GRID input Dv + Ds = 256 + 512 = 768: (1) dense 512 + ReLU bounded at 6.0, (2) dense 256 + ReLU bounded at 6.0, (3) dense V, no activation — raw logits for CTC loss (training) and constrained beam-search decoder (inference). NAVIR input Dv + Ds = 128 + 512 = 640: (1) dense 256 + ReLU bounded at 6.0, (2) dense V, no activation. Modality-specific configurations omit the absent stream from the input. The head is quantized to 4-bit weights and activations with the upstream encoders and fine-tuned jointly in the QAT phase.

**Covers:** chunk 10, Appendix B section C
