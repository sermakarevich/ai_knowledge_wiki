# Retrieval Augmented Generation and Understanding in Vision: A Survey and New Outlook

**Paper:** [Retrieval Augmented Generation and Understanding in Vision: A Survey and New Outlook (Zheng et al., 2025)](https://arxiv.org/abs/2503.18016)

## Human Readable TL;DR

Imagine a brilliant artist who only knows what they learned in school -- they might draw outdated maps or get facts wrong. Now imagine that same artist with access to a library they can look things up in before drawing. This paper surveys how AI systems for understanding and creating images can similarly gain access to external "libraries" of knowledge to become more accurate, current, and reliable. It maps out all the ways researchers have tried this approach for tasks ranging from recognizing objects in photos to generating videos and guiding robots, and points out what still needs to be figured out.

## TL;DR

This survey comprehensively reviews Retrieval-Augmented Generation (RAG) techniques applied to computer vision, covering visual understanding (recognition, detection, VQA, medical imaging), visual generation (image, video, 3D), and embodied AI (robotics, autonomous driving). The authors propose a unified taxonomy, identify core limitations -- retrieval inefficiency, modality misalignment, high compute cost, and domain gap -- and outline future directions including real-time retrieval, cross-modal fusion, and privacy-aware retrieval.

---

## Problem & Motivation

Large vision-language models suffer from hallucinations, stale parametric knowledge, and poor generalization to specialized domains (e.g., rare diseases, niche objects). Vanilla fine-tuning is expensive and fails to keep pace with a constantly changing world. RAG addresses this by retrieving relevant external knowledge at inference time, but its application to computer vision is fragmented across many disconnected sub-fields. No prior survey unified visual understanding, visual generation, and embodied AI under a single RAG framework -- this paper fills that gap.

---

## Main Original Ideas

1. **Unified RAG Taxonomy for Vision** -- Organizes RAG-in-CV literature into three pillars: visual understanding, visual generation, and embodied vision. Each pillar is further broken down by task type (e.g., image vs. video vs. 3D) and retrieval modality (text, image, structured knowledge).

2. **Retrieval-Augmented Visual Understanding** -- Surveys how external retrieval improves image/video recognition, object detection and segmentation, medical report generation, and multimodal question answering. Retrieval sources include image databases, knowledge graphs, and text corpora.

3. **Retrieval-Augmented Visual Generation** -- Covers how retrieved visual exemplars and text descriptions guide diffusion models and autoregressive generators to produce higher-fidelity images, temporally consistent videos, and realistic 3D content.

4. **Retrieval-Augmented Embodied AI** -- Examines RAG for robotic manipulation, navigation, and autonomous driving, where agents must ground decisions in dynamically retrieved scene context and prior experience.

5. **Limitation Analysis and Future Outlook** -- Consolidates cross-cutting challenges: (a) retrieval latency vs. quality trade-offs, (b) aligning heterogeneous retrieval modalities with generation models, (c) computational overhead of re-ranking large corpora, and (d) adapting retrievers to new domains without expensive retraining.

---

## Key Findings

| Dimension | Finding |
|-----------|---------|
| Visual Understanding | RAG consistently improves accuracy on rare/long-tail categories by supplying relevant exemplars at test time |
| Visual Generation | Retrieved image patches and style exemplars increase realism and semantic faithfulness in diffusion-based generation |
| Embodied AI | RAG enables agents to recall past trajectories and domain priors, improving generalization in novel environments |
| Multimodal RAG | Less explored than text-only RAG; multi-task multimodal retrieval remains an open problem |
| Efficiency | Real-time retrieval at inference is a bottleneck; approximate nearest-neighbor and learned sparse retrieval are key mitigations |

- RAG improves robustness in medical imaging by linking visual findings to knowledge-base entries, reducing hallucinated diagnoses.
- Embodied agents using memory-augmented retrieval show stronger zero-shot transfer than agents relying purely on parametric knowledge.
- Cross-modal retrieval (e.g., text query → image retrieval → generation) introduces compounding alignment errors not present in unimodal RAG.

---

## Suggestions & Future Directions

1. **Real-time retrieval optimization** -- Develop lightweight index structures and distilled retrievers that operate within strict latency budgets for robotics and autonomous driving.
2. **Cross-modal retrieval fusion** -- Build unified embedding spaces that allow seamless retrieval across text, image, video, and 3D modalities without modality-specific adapters.
3. **Privacy-aware retrieval** -- Design federated or differentially-private retrieval systems to enable RAG over sensitive medical or personal data without leaking raw records.
4. **Retrieval-based generative modeling** -- Tighter integration of retrieved examples into diffusion/autoregressive model training, not just inference, to learn retrieval-conditioned generation.
5. **Domain adaptation of retrievers** -- Efficient methods (e.g., prompt-tuned retrievers, adapter layers) for adapting pre-trained retrieval models to specialized domains with minimal labeled data.
6. **Evaluation benchmarks** -- Standardized benchmarks that measure both retrieval quality and downstream generation/understanding quality jointly, rather than evaluating them in isolation.

---

## Authors & Institutions

Xu Zheng (HKUST GZ, INSAIT/Sofia University), Ziqiao Weng (HKUST GZ, Sichuan University), Yuanhuiyi Lyu (HKUST GZ), Lutao Jiang (HKUST GZ), Haiwei Xue (HKUST GZ, Tsinghua University), Bin Ren (INSAIT/Sofia University, University of Pisa), Danda Paudel (INSAIT/Sofia University), Nicu Sebe (University of Trento), Luc Van Gool (INSAIT/Sofia University, ETH Zurich), Xuming Hu (HKUST GZ, HKUST -- corresponding author)
