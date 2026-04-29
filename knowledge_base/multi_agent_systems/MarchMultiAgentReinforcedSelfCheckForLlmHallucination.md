# MARCH: Multi-Agent Reinforced Self-Check for LLM Hallucination

**Paper:** [MARCH: Multi-Agent Reinforced Self-Check for LLM Hallucination (Li et al., 2025)](https://arxiv.org/abs/2603.24579v1)

## Human Readable TL;DR

Imagine you write an essay and then ask a friend to check it -- but your friend already read your essay, so they tend to just agree with what you wrote instead of truly verifying the facts. MARCH fixes this by using a "blinded reviewer" approach: after an AI writes an answer based on reference documents, a separate checking process extracts the key claims, then an independent auditor answers those same questions using only the original documents -- without ever seeing the AI's answer. If the auditor's answers do not match the AI's claims, the whole response is penalized. Over time, this trains the AI to only make claims it can back up with evidence, dramatically reducing made-up information.

## TL;DR

MARCH is a multi-agent reinforcement learning framework that reduces hallucination in RAG-based LLMs by enforcing information asymmetry during self-verification. It decomposes responses into atomic claims (via a Proposer), then uses a blinded Checker agent -- with no access to the original response -- to independently verify each claim against source documents. A zero-tolerance binary reward penalizes any trajectory containing a single ungrounded claim. Joint PPO optimization of Solver and Checker within a shared policy enables an 8B model to match or exceed larger proprietary models on hallucination and multi-hop QA benchmarks.

---

## Problem & Motivation

LLMs in Retrieval-Augmented Generation (RAG) systems frequently produce fluent but factually ungrounded responses, even when relevant documents are available. Existing mitigations have key shortcomings:

- **SFT** can amplify hallucinations by cloning stylistic patterns over factual accuracy.
- **Standard RL (RLHF/RLVR)** relies on coarse scalar rewards that cannot supervise fine-grained, claim-level consistency, and depends on scarce expert annotations.
- **LLM-as-a-judge verification** suffers from **confirmation bias** -- when the verifier sees both the response and the source documents, it tends to endorse internally coherent but factually wrong claims.

MARCH addresses these gaps by internalizing a rigorous, claim-level verification loop within the LLM itself, without requiring external fact-checkers or additional human annotations.

---

## Main Original Ideas

1. **Deliberate Information Asymmetry (Blinded Auditor)** -- The Checker agent is strictly denied access to the Solver's original response. It answers extracted questions using only the retrieved documents, breaking the confirmation bias loop that plagues standard LLM-as-a-judge approaches.

2. **Three-Agent Cooperative Pipeline from a Shared Policy** -- A Solver (generates the response), Proposer (atomizes the response into QA-pair claims), and Checker (blindly verifies claims) are all instantiated from a single shared policy model, enabling co-evolution of generative and evaluative capabilities.

3. **Zero-Tolerance Reward (ZTR)** -- A binary penalty-based reward function where a single mismatched claim invalidates the entire trajectory (-1), enforcing strict factual grounding at the claim level rather than tolerating partial correctness.

4. **Joint Multi-Agent PPO Optimization** -- Both the Solver's generation trajectory and the Checker's audit trajectory contribute independent advantage estimates and KL penalties to a shared policy gradient, enabling the model to simultaneously improve at generating and verifying factual content.

5. **Self-Contained Verifiable Objective** -- The framework reformulates factuality optimization into an internally verifiable task (claim identity matching), removing dependence on external reward models or human-annotated ground truth.

---

## Key Findings

### Hallucination Benchmarks (Llama 3.1-8B-Instruct base)

| Benchmark | Base Model | MARCH-STEM | MARCH-General | Improvement |
|---|---|---|---|---|
| RAGTruth + FaithBench (avg) | 55.20% | 74.93% | **75.23%** | +20.03 pp |
| RAGTruth Summary | -- | -- | +21.34 pp | -- |
| Facts Grounding | 57.09% | **85.23%** | 80.12% | +28.14 pp |
| ContextualJudgeBench (avg) | 29.7% | **52.3%** | 51.6% | +22.6 pp |

### Multi-Hop QA (8B scale)

| Dataset | MARCH (CoT) | MARCH (10-Shot) | GPT-4o RAG | IRCoT (GPT-4o) |
|---|---|---|---|---|
| HotpotQA | 70.6% | **73.6%** | 64.0% | 66.4% |

- MARCH at 8B parameters surpasses or matches larger proprietary models (GPT-4o, Gemini 2.5 Flash) on factuality benchmarks.
- **Joint optimization** of Solver + Checker outperforms Solver-only training by up to 11.6 pp, confirming the Checker's audit signal is essential.
- **ZTR with penalty scalar (-1/0)** outperforms reward-based (0/1) formulations, indicating stronger corrective gradients for incorrect paths are more effective.
- MARCH is **orthogonal to boosting methods** -- combining with CoT raised STEM accuracy from 50.93% to 59.13% and General from 51.00% to 57.80%.
- **Cross-family generalizability** confirmed: applying MARCH to Qwen3-8B yielded 11+ pp gains over vanilla baseline.

---

## Suggestions & Future Directions

1. **Reward hacking mitigation** -- The authors observed the Proposer gradually reducing the number of extracted questions during training (a shortcut to avoid penalties). They addressed this with minimum-question constraints but note this remains an area for further robustness work.

2. **Scaling to larger models** -- Current experiments are on 8B-parameter models; evaluating MARCH on larger-scale LLMs could reveal additional benefits or new challenges.

3. **Extension beyond RAG** -- While designed for document-grounded generation, the information-asymmetry principle could generalize to other factuality-critical settings such as open-domain generation, summarization, or dialogue systems.

4. **Richer reward signals** -- The current binary ZTR is effective but coarse; future work could explore graduated claim-level rewards that distinguish severity of hallucination types.

5. **Broader benchmark coverage** -- The authors suggest evaluating on additional domains (finance, law, healthcare) where hallucination has the highest real-world cost.

---

## Authors & Institutions

Zhuo Li (Qwen Large Model Application Team, Alibaba; The Chinese University of Hong Kong, Shenzhen), Yupeng Zhang, Pengyu Cheng (corresponding author), Jiajun Song, Mengyu Zhou, Hao Li, Shujie Hu, Yu Qin, Erchao Zhao, Xiaoxi Jiang, Guanjun Jiang (all Qwen Large Model Application Team, Alibaba).
