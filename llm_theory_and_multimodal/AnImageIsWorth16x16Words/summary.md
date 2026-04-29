# An Image Is Worth 16x16 Words: Transformers for Image Recognition at Scale

**Paper:** [An Image Is Worth 16x16 Words: Transformers for Image Recognition at Scale (Dosovitskiy et al., 2021)](https://arxiv.org/abs/2010.11929)

## Human Readable TL;DR

Imagine you have a jigsaw puzzle -- instead of looking at each tiny pixel of an image, this paper cuts the picture into a grid of small square patches (like puzzle pieces) and reads them one by one, the same way a language model reads words in a sentence. It turns out that this "reading" approach, which was originally designed for understanding text, works remarkably well for understanding images too -- but only if you show it millions of example images first. When trained on enough data, this simpler approach actually beats the specialized image-processing methods that dominated for a decade.

## TL;DR

The Vision Transformer (ViT) applies a standard Transformer encoder directly to sequences of image patches, with minimal vision-specific modifications. When pre-trained on large datasets (ImageNet-21k, JFT-300M), ViT matches or exceeds state-of-the-art CNNs (BiT, Noisy Student) on major benchmarks while requiring 2--4x less compute for pre-training. The key insight: large-scale data can substitute for the inductive biases built into CNNs.

---

## Problem & Motivation

Convolutional Neural Networks had dominated computer vision for years, relying on built-in assumptions about images -- local connectivity, translation equivariance, hierarchical features. Meanwhile, Transformers had revolutionized NLP through self-attention and massive pre-training, but direct application to images was considered impractical due to quadratic attention cost over pixels.

Prior hybrid approaches either bolted attention onto CNNs or used specialized sparse attention patterns, adding complexity. The authors asked: can a pure, unmodified Transformer -- the same architecture used for language -- achieve top-tier image classification if given enough data?

---

## Main Original Ideas

1. **Patch-based tokenization of images.** Split an image into fixed-size patches (e.g., 16x16), flatten each patch, and linearly project it into an embedding vector. This transforms a 2D image into a 1D sequence that a standard Transformer can process directly.

2. **Minimal vision-specific inductive bias.** ViT uses only a linear patch projection and learnable 1D position embeddings -- no convolutions, no pooling, no 2D-aware structure. Spatial relationships are learned entirely from data via self-attention.

3. **[CLS] token for classification.** Borrowing from BERT, a learnable classification token is prepended to the patch sequence. Its output state after the Transformer encoder serves as the global image representation.

4. **Large-scale pre-training as a substitute for architectural bias.** The central thesis: Transformers lack CNN-like inductive biases but compensate when pre-trained on sufficiently large datasets (14M--300M images), ultimately surpassing CNNs.

5. **Resolution-adaptive fine-tuning via position embedding interpolation.** Pre-trained position embeddings are 2D-interpolated to handle higher-resolution images at fine-tuning time, enabling flexible resolution changes without retraining.

---

## Key Findings

| Model | Pre-train Data | ImageNet | CIFAR-100 | VTAB (19 tasks) | Pre-train Cost (TPUv3-core-days) |
|---|---|---|---|---|---|
| **ViT-H/14** | JFT-300M | **88.55%** | **94.55%** | **77.63%** | 2.5k |
| **ViT-L/16** | JFT-300M | 87.76% | 93.44% | 76.28% | 0.68k |
| BiT-L (ResNet152x4) | JFT-300M | 87.54% | 93.51% | 76.29% | 9.9k |
| Noisy Student (EfficientNet-L2) | ImageNet + JFT-300M | 88.4% | -- | -- | 12.3k |

- ViT achieves SOTA or near-SOTA on ImageNet, CIFAR-100, Pets, Flowers, and VTAB with **2--4x less pre-training compute** than leading CNNs.
- On smaller datasets (ImageNet-1k alone), ViT underperforms comparably-sized ResNets -- confirming that data scale is critical.
- Performance scales smoothly with model size and data size, with no saturation observed.
- Learned 1D position embeddings encode 2D spatial structure -- nearby patches have similar embeddings, and the model recovers row/column topology without explicit 2D encoding.
- Early attention heads already integrate information globally (large effective receptive field), while deeper heads focus on semantically relevant regions.
- Hybrid models (CNN feature extractor + Transformer) help at small compute budgets but the advantage vanishes at scale.
- Preliminary masked patch prediction (self-supervised, BERT-style) yields +2% over training from scratch, though still lags supervised pre-training.

---

## Suggestions & Future Directions

1. **Self-supervised pre-training.** Initial masked patch prediction results are promising; the authors suggest scaling this approach could reduce dependence on labeled data.
2. **Extension to dense prediction tasks.** Applying ViT to object detection, segmentation, and video understanding (the paper focuses on classification only).
3. **Further scaling.** No performance saturation was observed -- larger models and datasets may yield additional gains.
4. **Improving data efficiency.** Making ViT competitive on smaller datasets without massive pre-training remains an open challenge.
5. **Contrastive and other self-supervised objectives.** Exploring alternatives to masked prediction for vision Transformers.

---

## Authors & Institutions

Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, Neil Houlsby -- all at **Google Research, Brain Team**.
