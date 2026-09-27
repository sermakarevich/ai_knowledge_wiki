# Brain2Qwerty v2: From Brain Waves to Words

**Article:** [From Brain Waves to Words: Brain2Qwerty Offers a New Path to Communication Without Surgery](https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication/) (Meta AI Research, 2026)

## Human Readable TL;DR

Some people lose ability to speak or type after brain injury. Surgery-based brain implants help but need risky operations. Meta built a cap-like sensor (MEG) that reads brain waves from outside skull, no surgery, and AI decodes those waves into typed words -- like a lip-reader, but for brain instead of lips. New version reads much more accurately than before.

## TL;DR

Brain2Qwerty v2 decodes text from noninvasive MEG brain recordings via end-to-end deep learning, fine-tuning LLMs on neural signals to exploit language's semantic redundancy. Trained on ~22k sentences from 9 volunteers (10h MEG each while typing), it hits 61% word accuracy overall vs 8% for prior noninvasive methods, and 78% for the best participant (half of sentences off by ≤1 word). Meta open-sourced v1/v2 training code plus related models and funding for more brain data.

---

## Problem & Motivation

Millions with brain lesions/paralysis lose ability to communicate. Existing brain-computer interfaces (BCIs) that reach usable accuracy require invasive surgery (stereotactic EEG, ECoG) -- limits scale and accessibility. Noninvasive alternatives (scalp EEG etc.) existed but were far less accurate (~8% word accuracy). Goal: close that gap without surgery.

---

## Main Original Ideas

1. **End-to-end deep learning over hand-crafted pipelines** -- instead of manually engineered feature-detection stages for brain signal decoding, model learns directly from raw MEG signal to text.
2. **LLM fine-tuning on neural data** -- language models pretrained on text are fine-tuned to consume brain signal representations, leveraging semantic/context priors of language to compensate for noisy neural input.
3. **AI-agent-assisted architecture search** -- AI agents explored training/optimization configurations, with human engineers making final selections -- a human-in-the-loop AutoML-style workflow.

---

## Key Findings

| Metric | Value |
|---|---|
| Word accuracy (v2, overall) | 61% |
| Word accuracy (prior noninvasive methods) | 8% |
| Word accuracy (best participant) | 78% |
| Sentences with ≤1 word error (best participant) | >50% |
| Training data | ~22,000 sentences |
| Participants | 9 volunteers |
| Recording time per participant | 10 hours (MEG, while typing) |

- Decoding accuracy scales log-linearly with data volume -- suggests gap to invasive methods narrows further with more data, not just better models.

---

## Suggestions & Future Directions

1. Scale data collection further given the log-linear accuracy/data relationship.
2. Broader community access via open training code (v1 + v2) to accelerate replication and improvement.
3. Basque Center on Cognition, Brain, and Language released v1 dataset publicly.
4. Related released models: Tribev2, NeuralSet, NeuralBench -- foundation for further brain-decoding research.
5. Meta committed $5M (Digital Brain Project) to fund more open brain-data collection.

---

## Authors & Institutions

Meta AI Research (FAIR), in collaboration with Basque Center on Cognition, Brain, and Language (dataset release for v1). Individual author names not listed in the blog post.
