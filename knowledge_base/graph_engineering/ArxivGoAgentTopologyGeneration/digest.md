> [[index|Wiki]] | [[summary|Summary]]

# Digest

## 1. Problem and Motivation

**In one sentence:** Existing LLM-based multi-agent systems build communication topologies agent-by-agent (node-centric), which fails to model divide-and-conquer group structures and causes noise propagation and token overhead, so GoAgent flips the paradigm by treating task-relevant collaborative groups as the atomic construction units and compressing inter-group communication with a conditional information bottleneck.

- LLM-based multi-agent systems (MAS) solve complex tasks (code generation, mathematical reasoning, multi-step decision-making), and the communication topology — a directed graph governing how agents interact and share information — matters more than individual agent capabilities for overall performance.
- Existing topology design has progressed from static hand-crafted structures (chains, trees, fully connected debate graphs) to template-based learning (AgentPrune, AgentDropout, GDesigner, GTD prune/reweight a dense template graph) to autoregressive generation from scratch (ARG-Designer), but all share the node-centric flaw.
- Node-centric generation — predicting each agent and its connections step-by-step as an isolated local decision — has two critical failure modes: (1) higher-order divide-and-conquer structures (e.g., a decomposer–solver–verifier sub-team) must emerge implicitly from ad-hoc edge predictions, yielding disjointed workflows; (2) without explicit group boundaries, graphs become dense and unconstrained, incurring redundant message-passing token overhead and letting task-irrelevant historical noise accumulate.
- GoAgent (Group-of-Agents) treats collaborative groups as the atomic units: an LLM first enumerates a pool of task-relevant candidate groups (each a coherent cluster of expert roles for a subtask), then a learned autoregressive model selects and connects whole groups to build the final graph, preserving intra-group cohesion while explicitly directing inter-group coordination.
- A Conditional Information Bottleneck (CIB) objective, conditioned on the specific task, compresses inter-group communication features to retain only strictly task-relevant signals and filter redundant historical noise.
- GoAgent achieves state-of-the-art results: 93.84% average accuracy across six benchmarks while reducing token consumption by about 17%.
- The problem is formally: given a task query Q, generate a group-level communication graph G = (M, E) over K collaborative groups, each defined as M_i = (S_i, E(S_i)) with S_i ⊆ V and intra-group relations E(S_i), with the final agent-level topology induced jointly by intra-group relations and inter-group dependencies.

## 2. Method: GoAgent

**In one sentence:** GoAgent autoregressively generates a task-specific multi-agent communication topology in which groups of agents — not individual agents — are the atomic generative units, using task-conditioned gated state aggregation plus a Conditional Information Bottleneck (CIB) to filter task-irrelevant signals, trained end-to-end with supervision (Teacher Forcing) instead of online RL.

- **Group-centric generation:** the task topology is factorized as an autoregressive sequence of group selections and inter-group edge predictions, so the generator works over K predefined collaborative groups (e.g., K = 16) rather than individual agent instances, sharply reducing the search space and matching human-like organizational structure.
- **Task encoding and candidate pool:** the task query Q is mapped to a global condition vector z_Q = FFN(SentenceEncoder(Q)) that guides every generation step; an LLM (GPT-4) proposes K groups, each with a schema (Name, Expertise, Roles, Intra-Topology) whose LLM-inducted intra-group edges E(S_i) are rigidly enforced templates (e.g., sequential for refinement), leaving only inter-group edges E to be generated.
- **State fusion with a task gate:** a GRU compresses the sequence of previously chosen group embeddings into h(t)_his, and a learned gate g(t) = σ(h(t)_his · z_Q / √d) blends history with the task vector z_Q plus a learnable step embedding e(t)_pos to form the fused state h(t)_comb.
- **Prediction heads:** the next-group distribution is Softmax(c(t)_group X^⊤) over the candidate embedding matrix X (padded with END tokens to (K+1)×d), and each incoming edge (M_i, M_t) is a binary classifier σ(MLP(c(edge_i,t))) over a compressed edge feature — both features pass through CIB first.
- **Conditional Information Bottleneck:** CIB minimizes −I(c; y | z_Q) + β I(x; c | z_Q), replacing the standard IB's fixed standard-normal prior with a task-conditioned prior p_θ(c | z_Q), so compression is task-aware rather than blind; the compression term is bounded by a KL divergence L_KL, and the decoder exploits the assumption z_Q → x → c → y to predict y from c alone.
- **Training data is auto-curated:** ground-truth trajectories G* are collected by heuristically sampling diverse topologies, executing them with LLMs on the tasks, and keeping the minimal viable graphs that solved the tasks — no manual annotation.
- **Supervised end-to-end learning:** Teacher Forcing on the curated set D = {(Q, G*)} avoids the high variance of online RL; the total loss combines group NLL (L_group), edge BCE (L_edge), and the KL regularizer with per-head coefficients β_g, β_e linearly warmed up over E_warm = 10 epochs.

## 3. Experiments, Related Work, and Conclusion

**In one sentence:** GoAgent achieves state-of-the-art accuracy on all six benchmarks (avg 93.84%) while cutting inference token cost by 17% versus the best baseline, remains the most attack-robust method (89.54% after a prompt-injection attack), and the paper closes with related-work positioning, a conclusion, acknowledged limitations, and an ethics statement.

- GoAgent reaches 91.50 (MMLU), 95.30 (GSM8K), 86.45 (AQuA), 99.11 (MultiArith), 96.46 (SVAMP), 94.21 (HumanEval), average 93.84 — best on all six benchmarks, beating Vanilla (avg 80.80) by 13.04 points and the strongest node-centric baseline ARG-Designer (avg 92.62) by 1.22 points.
- Gains are largest on hard reasoning tasks: MMLU +1.96% over ARG-Designer (91.50 vs 89.54) and HumanEval +2.47% (94.21 vs 91.74); over Vanilla, HumanEval improves by a massive 22.82 points (71.39 → 94.21).
- Ablation on 3 benchmarks: full GoAgent 91.50/95.30/94.21 (avg 93.67); w/o Group 88.89/93.75/91.74 (avg 91.46, −2.61 on MMLU); w/o CIB 88.23/93.96/92.56 (avg 91.58, −3.27 on MMLU); w/o ALL 86.92/91.16/90.56 (avg 89.55) — group-level generation and CIB noise filtering are both necessary and complementary.
- Token cost: GoAgent uses 1.9e+05 tokens on MMLU (vs LLM-Debate 1.6e+06, Complete 6.7e+05) and 3.4e+06 on GSM8K (vs LLM-Debate 2.8e+07, Complete 1.2e+07) — a 17% reduction versus the SOTA baseline ARG-Designer (2.1e+05 / 4.1e+06) while keeping the highest accuracy.
- Robustness to a simulated system-prompt injection attack (one agent compromised): GoAgent drops only from 91.5 to 89.5 (keeping 89.54% accuracy), while node-centric baselines lose more (ARG-Designer 89.5 → 87.3, G-Designer 88.9 → 87.7, Full 82.3 → 70.6).
- Case study on an MMLU item ("An immigrant learning English in the U.S. is an example of …", answer: acculturation): GoAgent's group-centric topology answers correctly; ARG-Designer's denser node-centric graph answers incorrectly.
- Related work positions GoAgent against LLM multi-agent systems (static chains; template-based pruning: G-Designer, AgentPrune, AgentDropout; autoregressive ARG-Designer — all node-centric) and group-aware graph generation (hierarchical networks, diffusion-based generation, higher-order scalable frameworks), showing GoAgent is the first to bring group-centric atomics into LLM MAS.

## 4. Appendix: Algorithms, Complexity, and Implementation Details

**In one sentence:** The appendix pins down GoAgent's full training/inference pseudocode, proves the generator is computationally cheap (O(T²d² + TKd) time, O(d² + Kd) space), itemizes the six benchmarks and thirteen baselines, quantifies the β_g/β_e sensitivity trade-off, and specifies the exact training configuration, architecture dimensions, and LLM prompt design used to curate the task data.

- **Time complexity:** With T generated groups, K candidate-pool size, and hidden dimension d, graph generation costs O(Td² + TKd + T²d²) = O(T²d² + TKd), negligible vs. LLM inference since T is typically < 3 and K (e.g., 16) is tiny.
- **Space complexity:** Generator parameters are bounded by O(d²) (lightweight GRUs, MLPs, CIB projections) plus O(Kd) for candidate embeddings — total O(d² + Kd), highly parameter-efficient.
- **Datasets:** Six benchmarks — MMLU (153 multi-choice), GSM8K (1,319 numeric), MultiArith (600), SVAMP (1,000), AQuA (254), HumanEval (164 code, Pass@1) — following G-Designer's setup.
- **Baselines (13 total):** 3 single-agent (Vanilla, CoT, Self-Consistency with 5 paths + majority vote), 5 fixed topologies (Chain, Tree, Complete, Random, LLM-Debate), 5 learning-based (Agent-Prune, Agent-Dropout, G-Designer, EIB-Learner, ARG-Designer), each learning-based method trained separately per dataset.
- **Inference:** CIB stochastic sampling is bypassed; the deterministic mean c = μ_φ(x) is used for both group and edge predictions, and a Bernoulli edge sample falls back to the argmax edge if none is sampled, guaranteeing connectivity.
- **β sensitivity:** Optimal config is highly asymmetric (β_g ≈ 0.0, β_e ≈ 0.3) — edge prediction benefits far more from compression than group prediction; accuracy stays ~86–90% across the grid while token cost (160–220 K) drops steeply as β_e rises from 0.
- **Training config:** AdamW, lr 1e-4, weight decay 1e-3, grad clipping 1.0, 100 epochs, batch 40, linear β warm-up over first 10 epochs; only B ∈ {40, 60} curated queries per dataset suffice because the generator learns structural collaboration patterns, not task reasoning.

## The argument in five moves

1. **Problem:** node-centric topology generation (predicting one agent-edge at a time) can't represent natural divide-and-conquer group structure and lets graphs grow dense and noisy.
2. **Reframe:** treat whole collaborative groups — not individual agents — as the atomic unit of graph construction; let an LLM propose the candidate group pool up front.
3. **Mechanism:** an autoregressive model, conditioned on the task query, selects groups and predicts only the inter-group edges, fusing history and task via a learned gate.
4. **Filter:** a Conditional Information Bottleneck compresses inter-group features so only task-relevant signal survives, trained with a task-aware prior instead of a blind one.
5. **Evidence:** ablations show both group-centricity and CIB independently matter and stack; GoAgent beats all 13 baselines on average accuracy while using ~17% fewer tokens.
6. **Stress test:** under simulated prompt-injection, GoAgent's structured groups contain the damage better than denser node-centric graphs, showing the benefit isn't just efficiency but also robustness.
7. **Scope:** the group pool is fixed offline (no novel groups at inference) and evaluation stays within static reasoning/coding benchmarks — the paper explicitly flags dynamic, interactive settings as future work.
