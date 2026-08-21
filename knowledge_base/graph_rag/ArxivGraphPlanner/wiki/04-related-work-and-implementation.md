> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Related Work & Implementation Details

**In one sentence:** GraphPlanner positions itself as an *agentic* router that jointly selects heterogeneous LLM agents (role *and* backbone) and composes per-query workflow graphs, differentiating from single-round/RL backbone-only routers and homogeneous MAS, and is reproduced with a GARNet-parameterized PPO policy trained on a single NVIDIA A6000 across 6 domains, 14 tasks, and 12 LLM backbones.

## Key points

- MAS frameworks (AutoGen, LLM-Debate, AgentVerse) and workflow-generators (ADAS, AFlow, AgentSquare) use manually designed protocols or assume homogeneous agent capabilities; GraphPlanner **automatically selects heterogeneous LLM agents** and composes workflows per query.
- Single-round routers (RouterKNN, RouterMLP, RouterSVM, RouterDC, GraphRouter) are efficient but lack sequential reasoning; multi-round/RL routers (Prompt LLM, Router-KNN-MR, R2-Reasoner, Router-R1) do backbone selection only — GraphPlanner jointly picks agent *and* backbone.
- Policy trained with **PPO** (Schulman et al., 2017), both policy and value functions parameterized by **GARNet** via `torch_scatter` for graph message passing and meta-key aggregation.
- Hyperparameters: γ = 0.99, ϵ = 0.2, k = 4 epochs/update, hidden dim 32, candidate embedding dim 1536, state embedding dim 768, Adam LR 3×10⁻⁴ (doubled for value), gradient clip norm 0.5, BF16, gradient checkpointing, multi-threaded parallel rollouts.
- Training capped at **1000 episodes** with early stopping when **policy entropy drops below a threshold**; evaluation uses **greedy decoding**, best model by running reward.
- All experiments on a **single NVIDIA A6000 GPU**.
- Datasets: 6 domains / 14 tasks (incl. held-out out-of-domain: LogicGrid, MGSM, CommonGen); 12 LLMs across Small (7–12B, $0.20–0.30/M tokens), Medium (49–56B, $0.60–0.90/M tokens), Large (70–176B, $0.90–1.20/M tokens).

---

## Additional Related Work

**LLM-Agents and Agentic Systems.** Multi-agent systems (MAS) enhance reasoning, adaptability, and performance beyond single-agent settings (Wang et al., 2024a; Qian et al., 2024; Guo et al., 2024). Early frameworks — AutoGen (Wu et al., 2024), LLM-Debate (Du et al., 2023), AgentVerse (Chen et al., 2023a) — showed gains in factuality, robustness, and efficiency but relied on manually designed protocols that limited adaptability (Zhuge et al., 2024; De Zarza et al., 2023). Most MAS also assume agents share the same backbone, constraining heterogeneity. Later work explored autonomous cooperation and emergent self-organization with dynamic labor division (Barachini & Stary, 2022; Tran et al., 2025), and reasoning improvements via social behaviors, negotiation, and role specialization (Zhang et al., 2023; Chen et al., 2024b; Chang, 2025). A newer line automates multi-agent workflow design: **ADAS** (Hu et al., 2024b) adaptively schedules agents by task complexity, **AFlow** (Zhang et al., 2024a) searches action graphs to construct multi-step workflows, and **AgentSquare** (Shang et al., 2024) generates task-specific collaboration strategies from a role library — but all assume largely homogeneous agent capabilities. GraphPlanner instead introduces an agentic routing framework that automatically selects heterogeneous LLM agents and composes workflows tailored to each query.

**Tool-Augmented LLMs and Real-World Agent Ecosystems.** Grounded tool agents include **Toolformer** (Schick et al., 2023), **Gorilla** (Patil et al., 2024), and **ReAct**-based tool agents (Yao et al., 2022); production frameworks — LangChain, Semantic Kernel, AutoGPT, OpenAI function-calling agents — demonstrate the importance of reliable tool integration, execution monitoring, and safety in real deployments. These systems rely on static or manually designed workflows, underscoring the need for the learned workflow generation and routing strategies in GraphPlanner.

**LLM routers.** Single-round routers make one-shot assignments via query embeddings or classifiers: **RouterKNN** and **RouterMLP** (Shnitzer et al., 2023), **RouterSVM** (Hu et al., 2024a), **RouterDC** (Chen et al., 2024a), and **GraphRouter** (Feng et al., 2024) — efficient but lacking sequential reasoning. Multi-round routers enable iterative decisions: **Prompt LLM** (Zhang et al., 2025), **Router-KNN-MR** (Zhang et al., 2025), **R2-Reasoner** (Shao et al., 2025), and **Router-R1** (Zhang et al., 2025) — the last combining deliberation and routing with reinforcement learning. All remain restricted to backbone selection without modeling agent roles or heterogeneity. GraphPlanner's agentic routing addresses both limitations by jointly deciding which **agent** and which **backbone** to invoke, combining routing efficiency with the adaptability, specialization, and heterogeneity of MAS.

## Training Details

The heterogeneous graph-based policy network is optimized with **PPO** (Schulman et al., 2017), maximizing the clipped-surrogate objective:

L_PPO(θ) = E[ ẑ_t · min( ρ_t(θ) Â_t, clip(ρ_t(θ), 1−ϵ, 1+ϵ) Â_t ) ]

where ρ_t(θ) = π_θ(a_t | s_t, G_workflow, G_history) / π_θ_old(a_t | s_t, G_workflow, G_history); π_θ and π_θ_old are the current and previous policies; Â_t is the estimated advantage at step t; ϵ is the clipping threshold; s_t the current state; a_t the chosen action; G_workflow the workflow interaction graph; G_history the historical interaction graph.

- Training capped at **1000 episodes**, with **early stopping once policy entropy drops below a threshold** (reduced exploration).
- During evaluation, **greedy decoding** is applied; the **best model is selected by running reward**.
- All experiments run on a **single NVIDIA A6000 GPU**.

## Implementation Details

- **Architecture:** both policy and value functions are parameterized by **GARNet**, integrating local and historical state information. **Local state graphs** encode query embeddings, role–LLM embeddings, and memory updates; **historical graphs** aggregate past interaction representations. Each graph is projected via a **linear–normalization–ReLU** block and fused by **meta-key aggregation**; GARNet is implemented with the **`torch_scatter`** library for graph-based message passing and sparse aggregation.
- **Policy network:** computes action probabilities by matching fused state representations (query, task, and state tower outputs) against role–LLM embeddings, with **action masking**.
- **Value network:** processes state, local, and historical features through multi-layer transformations to output scalar value estimates.
- **PPO hyperparameters:** γ = 0.99, ϵ = 0.2, k = 4 epochs per update.
- **Embedding sizes:** hidden dimension = 32; candidate embedding dimension = 1536; state embedding dimension = 768.
- **Optimizer:** Adam, learning rate 3×10⁻⁴ (policy) and doubled for value; gradient clipping (norm 0.5); BF16 training; gradient checkpointing.
- **Efficiency:** a **multi-threaded rollout design** processes multiple queries in parallel and generates routing interactions simultaneously — increasing sample throughput, reducing wall-clock training time, and stabilizing PPO updates by providing more diverse experience per iteration.

## Dataset and LLM Backbone Details

The benchmarks span **6 domains and 14 tasks**.

| Domain | Tasks |
|---|---|
| Math | GSM8K, MATH |
| Code | MBPP, HumanEval |
| Commonsense Reasoning | CommonsenseQA, ARC, OpenBookQA |
| World Knowledge | NaturalQuestions, TriviaQA |
| Popular | MMLU, GPQA |
| Out-of-domain Testing | LogicGrid, MGSM, CommonGen |

> Tasks marked out-of-domain testing are **held out from training** and reserved solely for evaluating the router's generalization to unseen tasks.

**Sample counts (train / test):**

| Domain | Task | Train Cases | Test Cases |
|---|---|---|---|
| Math | GSM8K (Cobbe et al., 2021) | 500 | 50 |
| Math | MATH (Hendrycks et al., 2021b) | 500 | 50 |
| Code | MBPP (Austin et al., 2021) | 374 | 50 |
| Code | HumanEval (Chen et al., 2021) | 120 | 44 |
| Commonsense Reasoning | CommonsenseQA (Talmor et al., 2019) | 500 | 50 |
| Commonsense Reasoning | ARC (Clark et al., 2018) | 500 | 50 |
| Commonsense Reasoning | OpenBookQA (Mihaylov et al., 2018) | 500 | 50 |
| World Knowledge | NaturalQuestions (Kwiatkowski et al., 2019) | 500 | 50 |
| World Knowledge | TriviaQA (Joshi et al., 2017) | 500 | 50 |
| Popular | MMLU (Hendrycks et al., 2021a) | 500 | 50 |
| Popular | GPQA (Rein et al., 2023) | 400 | 44 |
| Out-of-domain Testing | LogicGrid (Mitra & Baral, 2015) | 0 | 50 |
| Out-of-domain Testing | MGSM (Shi et al., 2022) | 0 | 50 |
| Out-of-domain Testing | CommonGen (Lin et al., 2019) | 0 | 50 |

**Evaluation metrics:**

| Domain | Task | Metric |
|---|---|---|
| Math | GSM8K, MATH | Accuracy |
| Code | MBPP, HumanEval | Pass@1 |
| Commonsense Reasoning | CommonsenseQA, ARC, OpenBookQA | Accuracy |
| World Knowledge | NaturalQuestions, TriviaQA | CEM |
| Popular | MMLU, GPQA | Accuracy |
| Out-of-domain Testing | LogicGrid, MGSM | Accuracy |
| Out-of-domain Testing | CommonGen | Coverage |

**Short task descriptions (Appendix D.1):**

- **GSM8K** — grade-school math word problems probing multi-step arithmetic with natural-language solutions; standard testbed for chain-of-thought and verifier-based selection (Cobbe et al., 2021).
- **MATH** — 12,500 competition-style problems (algebra, geometry, number theory…) with step-by-step solutions; evaluates symbolic reasoning and solution derivation (Hendrycks et al., 2021b).
- **MBPP** — ("Mostly Basic Python Problems") function-level code synthesis from short NL prompts, with unit tests; entry-level Python fluency (Austin et al., 2021).
- **HumanEval** — functional correctness of generated Python on handwritten problems with hidden unit tests; introduced the pass@k metric (Chen et al., 2021).
- **CommonsenseQA** — multiple-choice commonsense reasoning built from ConceptNet relations; plausible distractors require background knowledge (Talmor et al., 2019).
- **ARC** — AI2 Reasoning Challenge; grade-school science MC, split Easy/Challenge, emphasizing multi-hop reasoning (Clark et al., 2018).
- **OpenBookQA** — applying a small "open book" of elementary science facts to novel situations; MC (Mihaylov et al., 2018).
- **NaturalQuestions (NQ)** — real anonymized user queries with Wikipedia pages and annotated spans; document-level comprehension, evaluated via case-insensitive exact match (Kwiatkowski et al., 2019).
- **TriviaQA** — enthusiast-written QA with evidence documents, compositional and diverse, evaluated via CEM (Joshi et al., 2017).
- **MMLU** — Massive Multitask Language Understanding; 57-subject MC exam across humanities, social sciences, STEM, professional domains (Hendrycks et al., 2021a).
- **GPQA** — Graduate-Level Google-Proof Q&A; expert-authored MC in biology/physics/chemistry resistant to web search (Rein et al., 2023).
- **LogicGrid** — classic Zebra-style logic-grid puzzles in NL; deduction over entities, attributes, constraints (Mitra & Baral, 2015).
- **MGSM** — multilingual extension of GSM8K; measures transfer of multi-step arithmetic across languages (Shi et al., 2022).
- **CommonGen** — compose a coherent sentence that must include a given set of concepts; controllable generative commonsense (Lin et al., 2019).
- **AIME** — American Invitational Mathematics Examination; 15 integer-answer problems/year, high-difficulty symbolic reasoning; accuracy is the primary metric.

**LLM backbones (12 LLMs across three scales):**

| Scale | LLMs |
|---|---|
| Small | Qwen2.5 (7B), CodeGemma (7B), Mistral (7B), LLaMA-3.1 (8B), LLaMA-3 ChatQA (8B), Gemma-2 (9B), Mistral-Nemo (12B) |
| Medium | LLaMA-3.3 Nemotron Super (49B), LLaMA-3.1 Nemotron (51B), Mixtral (8×7B) |
| Large | LLaMA-3 ChatQA (70B), Mixtral (8×22B) |

> LLMs not involved in training (used only to evaluate generalization to unseen LLMs) are the ones marked with an underscore in the source (Appendix D); exact membership is not recoverable from this chunk.

**Sizes and pricing (USD per 1M tokens, input / output):**

| Scale | Model | Size | Input Price | Output Price |
|---|---|---|---|---|
| Small | Qwen2.5 (Qwen et al., 2025) | 7B | $0.20 | $0.20 |
| Small | CodeGemma (Team et al., 2024a) | 7B | $0.20 | $0.20 |
| Small | Mistral (Jiang et al., 2023) | 7B | $0.20 | $0.20 |
| Small | LLaMA-3.1 (Grattafiori et al., 2024) | 8B | $0.20 | $0.20 |
| Small | LLaMA-3 ChatQA (Liu et al., 2024) | 8B | $0.20 | $0.20 |
| Small | Gemma-2 (Team et al., 2024b) | 9B | $0.20 | $0.20 |
| Small | Mistral-Nemo (Mistral AI, 2024) | 12B | $0.30 | $0.30 |
| Medium | LLaMA-3.3 Nemotron Super (Wang et al., 2024b) | 49B | $0.90 | $0.90 |
| Medium | LLaMA-3.1 Nemotron (Wang et al., 2024b) | 51B | $0.90 | $0.90 |
| Medium | Mixtral (Jiang et al., 2024) | 56B (8×7B) | $0.60 | $0.60 |
| Large | LLaMA-3 ChatQA (Liu et al., 2024) | 70B | $0.90 | $0.90 |
| Large | Mixtral (Jiang et al., 2024) | 176B (8×22B) | $1.20 | $1.20 |

**Short model descriptions (Appendix D.2):**

- **Qwen2.5 (7B)** — recent-generation Qwen, open-weight, optimized for general-purpose utility, instruction following, strong reasoning/coding; multilingual and long-context (Qwen et al., 2025).
- **CodeGemma (7B)** — code-specialized family derived from Gemma; code completion, generation, conversational coding; fill-in-the-middle prompting; good pass@k on Python (Team et al., 2024a).
- **Mistral (7B)** — open-weight decoder-only transformer; grouped-query and sliding-window attention for fast long-sequence inference; strong for its size (Jiang et al., 2023).
- **LLaMA-3.1 (8B)** — Meta open-weight; improved instruction-following, multilinguality, extended context; lightweight option for on-prem/edge (Grattafiori et al., 2024).
- **LLaMA-3 ChatQA (8B / 70B)** — instruction-tuned QA/chat variants for question answering and retrieval-augmented workflows (Liu et al., 2024).
- **Gemma-2 (9B)** — Google's second-gen open family; architectural refinements, advanced reasoning and multilingual (Team et al., 2024b).
- **Mistral-Nemo (12B)** — collaboratively developed open-weight; efficient inference, high-quality instruction following (Mistral AI, 2024).
- **LLaMA-3.3 Nemotron Super (49B)** — instruction-tuned assistant in NVIDIA's Nemotron lineup; preference-optimization, helpfulness/safety/strong reasoning (Wang et al., 2024b).
- **LLaMA-3.1 Nemotron (51B)** — LLaMA-3.1-based with large-scale instruction tuning and preference modeling for chat/tool-use (Wang et al., 2024b).
- **Mixtral (8×7B)** — sparse Mixture-of-Experts; small subset of experts activated per token; Mistral architecture with dynamic expert routing (Jiang et al., 2024).
- **Mixtral (8×22B)** — scaled MoE with larger experts for higher accuracy at sparse-activation efficiency; multilingual, reasoning, long-input (Jiang et al., 2024).

**Covers:** Appendix A (Additional Related Work), Appendix B (Training Details), Appendix C (Implementation Details), Appendix D (Dataset and LLM Backbone Details)
