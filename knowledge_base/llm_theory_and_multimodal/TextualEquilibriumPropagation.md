# Textual Equilibrium Propagation for Deep Compound AI Systems

**Paper:** [Textual Equilibrium Propagation for Deep Compound AI Systems (Chen, Deng, Zou, Yu, Li, 2025)](https://arxiv.org/abs/2601.21064)

## Human Readable TL;DR

Imagine a big company where feedback from the CEO has to pass through many layers of management before reaching the workers on the ground floor. By the time it arrives, the message is either bloated with every manager's additions (making it impossible to read) or compressed so many times it becomes a vague "do better." This paper tackles exactly that problem -- but for AI systems made of many connected language-model "agents." Instead of passing one long chain of feedback from the end all the way back to the start, each agent gets its own local coach that first helps it do its best work independently, then gives it a small nudge informed by the overall goal. This two-step "local coaching" approach keeps the feedback clear and useful no matter how many agents are chained together, letting teams of AI agents solve harder, longer problems than before.

## TL;DR

This paper introduces Textual Equilibrium Propagation (TEP), a local optimization framework for deep compound AI systems that replaces global textual backpropagation with a two-phase process: a free phase where each node reaches local behavioral equilibrium via structured critic feedback, and a nudged phase where minimal task-guided perturbations align nodes toward the global objective. TEP formally addresses the exploding and vanishing textual gradient problems that degrade optimization in deep LLM pipelines. Empirically, TEP achieves consistent improvements over TextGrad and other baselines across biomedical QA, multi-hop retrieval, and code generation benchmarks, with particularly strong gains as system depth increases.

---

## Problem & Motivation

Modern AI increasingly relies on **compound AI systems** -- pipelines that chain multiple specialized LLM modules (retrievers, reasoners, verifiers, tools) to solve complex, multi-step tasks. Optimizing these systems end-to-end is critical but difficult because the LLM components are black boxes.

Prior work like **TextGrad** introduced "automatic differentiation via text," propagating natural-language feedback backward through the pipeline to refine prompts. While effective for shallow systems, TextGrad suffers from two depth-dependent failure modes analogous to classic neural network training issues:

- **Exploding textual gradient:** Each upstream node preserves and augments all downstream feedback, causing message length to grow exponentially (empirically ~2.2^depth). Messages exceed context limits and bury critical corrections.
- **Vanishing textual gradient:** Compressing feedback via summarization causes actionable detail to decay exponentially, reducing specific corrections to generic platitudes. The effective update rate drops from 36% to 5% across five depth levels.

These failure modes make global textual backpropagation impractical for the deep, long-horizon agentic workflows that compound AI systems are designed to handle.

---

## Main Original Ideas

1. **Formal characterization of textual gradient pathologies.** The paper provides the first rigorous analysis of exploding and vanishing textual gradients in LLM-based computational graphs, proving exponential scaling bounds on message length (explosion) and specificity decay (vanishing).

2. **Textual Equilibrium Propagation (TEP).** Inspired by Equilibrium Propagation from energy-based models (Scellier & Bengio, 2017), TEP replaces global backward feedback chains with a local two-phase optimization:
   - **Free phase:** Each node independently converges to a behavioral equilibrium using a local LLM critic guided by structured rubrics (six task-independent quality dimensions plus task-dependent criteria), with adaptive actor temperature controlling exploration.
   - **Nudged phase:** Minimal, task-objective-informed perturbations are applied via forward signaling (not backward propagation) to steer nodes toward the global optimum.

3. **Local contrast-based update rule.** Feedback from the free and nudged phases is compared locally at each node, yielding O(1)-sized update signals whose quality is depth-invariant. A validation gate ensures only performance-improving edits are accepted.

4. **Annealed nudging strength.** The nudging parameter is gradually reduced over iterations, enabling strong initial global coordination followed by local fine-tuning.

5. **Black-box compatibility.** TEP operates entirely through prompt editing and requires no access to model weights, gradients, or internal states, making it applicable to any LLM API.

---

## Key Findings

**Benchmark performance (compound AI system optimization):**

| Benchmark | Metric | TEP | Best Baseline | Gain |
|---|---|---|---|---|
| PubMedQA | Accuracy | 62.02% | 60.26% (DSPy) | +1.76 |
| STARK-PRIME | MRR | 42.72% | 41.40% (DSPy) | +1.32 |
| HotpotQA | F1 | 48.72% | 44.90% (DSPy) | +8.1% relative |
| BigCodeBench | Pass@1 | 38.97% | 35.71% (TextGrad) | +3.26 |

**Depth-scaling robustness:**
- TextGrad feedback token count grows from ~2K to >32K across 5 depth levels; TEP remains nearly constant.
- TextGrad effective update rate collapses from 36% to 5% at depth 5; TEP degrades only from 37% to 33%.

**Solution optimization (single-node + hierarchical):**
- GPQA: TEP 44.5% vs. TextGrad 41.0% (+3.5 pp); TextGrad w/ summarization drops below CoT baseline.
- Object Counting (5-step hierarchical): TEP 81.6% vs. TextGrad 74.2%.

**Ablation results:**
- Removing the nudged phase causes HotpotQA F1 to collapse by 26.4 points -- local equilibrium alone cannot achieve global coherence.
- Removing the free phase drops F1 by 11.9 points -- the free phase provides strong local initializations that the nudged phase builds upon.

**Computational efficiency:** TEP's token usage grows much more slowly with depth than TextGrad (roughly linear vs. exponential), making it substantially cheaper for deep systems.

---

## Suggestions & Future Directions

- **Dynamic graph structures.** Current TEP assumes a fixed computational graph. Extending TEP to systems where the graph topology changes at runtime (e.g., adaptive retrieval pipelines, dynamic tool selection) is an open challenge.
- **Large-scale multi-agent coordination.** Scaling TEP to systems with many more nodes and richer inter-agent dependencies could enable optimization of large multi-agent organizations.
- **Richer nudging mechanisms.** Exploring alternative nudging strategies beyond proximal prompt edits -- such as architectural nudges or learned nudging policies -- could further improve global alignment.
- **Integration with fine-tuning.** Combining TEP's prompt-level optimization with parameter-efficient fine-tuning of individual modules could yield complementary gains.
- **Theoretical convergence guarantees.** Formalizing convergence properties of TEP under various assumptions about LLM behavior and graph structure remains open.
- **Broader benchmarks.** Evaluating TEP on even deeper, more heterogeneous compound AI systems (e.g., autonomous research agents, multi-modal pipelines) would further validate its scalability claims.

---

## Authors & Institutions

- **Minghui Chen** -- Nanyang Technological University; University of British Columbia
- **Wenlong Deng** -- University of British Columbia; Vector Institute
- **James Zou** -- Stanford University
- **Han Yu** -- Nanyang Technological University
- **Xiaoxiao Li** (corresponding author) -- University of British Columbia; Vector Institute
