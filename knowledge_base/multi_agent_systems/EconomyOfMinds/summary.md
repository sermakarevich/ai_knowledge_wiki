# Economy of Minds: Emerging Multi-Agent Intelligence with Economic Interactions

**Paper:** [Economy of Minds: Emerging Multi-Agent Intelligence with Economic Interactions (Qi et al., 2026)](https://arxiv.org/abs/2606.02859)

## Human Readable TL;DR

Imagine a company where no one is in charge -- instead, employees bid for the right to handle each task, the winner gets paid based on how useful their action turns out to be, and anyone who consistently loses money gets fired while good performers spawn slightly varied copies of themselves. This paper shows that running a group of AI agents this way -- with simple economic rules -- makes them collectively smarter than a single expert AI, without anyone ever designing how they should cooperate. The group self-organizes, develops specialists, and improves over time, like a market finding efficient solutions without central planning.

## TL;DR

The paper introduces **Economy of Minds (EoM)**, a framework where LLM-based agents self-organize through economic mechanisms: agents compete via first-price auctions for action rights, exchange wealth via bucket-brigade payments, and evolve through economic selection (exploitation of wealthy agents via mutation; replacement of bankrupt agents via exploration). Starting from weak partial agents, EoM produces emergent multi-step reasoning strategies that outperform complete-agent baselines across five diverse tasks: MATH (15.9% → 57.0% with Llama-3.1-8B), finance research (+15%), scientific research (1.8% → 8.5% mean), accelerator design (2.2× EDP gain over DOSA), and distributed-system optimization (28% cost reduction vs OpenEvolve).

---

## Problem & Motivation

Centralized multi-agent orchestrators bottleneck at a single coordination gate -- all planning flows through the orchestrator, creating a performance bottleneck, a single point of failure, and coordination complexity that grows linearly with system size. The question this paper asks: can a group of individually limited agents form decentralized intelligence that self-organizes and evolves without a central controller or explicit communication protocols?

The motivation draws on Hayek's insight that free markets aggregate dispersed information through prices -- no individual needs global awareness for large-scale coordination to emerge. The paper asks whether the same principle can govern a population of language agents.

---

## Main Original Ideas

1. **Agent Economy (EoM Framework).** A society of LLM agents where global coordination emerges purely from local economic interactions. Each agent is a tuple (φ_a, π_a, b_a, W_a): a triggering predicate, an action policy, a fixed bid, and current wealth. All agents share a frozen LLM backbone; diversity comes entirely from system prompts.

2. **Auction-Based Planning.** At each environment step, agents whose triggering predicates fire become eligible. The highest-bidding eligible agent wins, executes its action, and the environment advances. This decentralizes action selection -- control flows to the agent that values its own relevance most highly, without a coordinator.

3. **Bucket-Brigade Credit Assignment.** The winner pays its bid to the previously active agent and receives any environmental reward. Formally: W_{a*_t} ← W_{a*_t} - b_{a*_t} + r_t ; W_{a*_{t-1}} ← W_{a*_{t-1}} + b_{a*_t}. Value flows backward along successful trajectories: agents whose actions enable productive downstream continuations accumulate wealth without requiring dense process rewards.

4. **Economic Selection (Exploitation + Exploration).** Between episodes, three stages execute: (1) all agents pay periodic rent ρ, (2) agents with negative wealth are removed, (3) the population is replenished. Wealthy agents spawn mutations (exploitation -- preserving successful patterns with small variation); bankrupt agents' slots are filled by novelty injections (exploration -- correcting failure modes or discovering complementary behaviors). A novice bid rule -- b_{a'} = max_{competitors} b_a + ε -- forces each new agent to be tested at least once before market selection decides its fate.

5. **Emergent Specialization Without Templates.** The market naturally produces specialists: agents with narrow, finely tuned wake-up conditions outcompete generalists in their subdomains because their prompts are sharper. Generalists do not monopolize even when granted complete tool access. In accelerator design, output-stationary dataflow patterns emerged from scratch across ResNet-50 bottleneck kernels -- the system recovered a known co-design heuristic without being given it as a template.

---

## Key Findings

| Domain | Baseline | EoM | Metric |
|--------|----------|-----|--------|
| MATH (Llama-3.1-8B) | 15.9% initial / 51.9% complete | **57.0%** | greedy pass@1 |
| MATH (Gemma-2-9B) | 4.2% initial / 44.3% complete | **45.1%** | greedy pass@1 |
| Finance-Agent-Bench | 45.0% (ReAct), 50.0% (GEA) | **60.0%** (best: 65.0%) | accuracy |
| FrontierScience-Research | 1.8% mean / 5.0% best (GEA) | **8.5% mean / 20.0% best** | accuracy |
| Accelerator Design (EDP ↓) | 80.2 (DOSA), 43.1 (ReAct) | **39.3** | avg µJ·Mcyc |
| Distributed Systems (Cloudcast) | 930 (OpenEvolve) | **657** | total cost |

**Ablations reveal economic mechanisms are necessary, not incidental:**
- Removing auctions: Finance mean drops 48.0 (vs 52.5 full)
- Removing exploration: Finance mean drops 26.0 -- sharpest single-component loss
- Removing exploitation: Finance mean drops 33.5
- Perturbing reward scale (0.2× or 4×): MATH best drops to 44–47 (vs 57.0 full)

**Generalization:** Easy-to-hard curriculum on MATH transfers to Level 5 (hardest), raising accuracy from ~10% to ~20%. Hard-to-easy curriculum still improves but plateaus at ~47% vs 57%. Behaviors learned on simpler problems decompose and recombine on harder ones.

**No generalist monopoly:** A complete generalist agent added to Finance-Agent-Bench briefly expands to 1–2 agents in tasks 11–12, then contracts back to a single agent, while specialized populations (Edgar, Tavily) grow to 5–8 agents late in training. Market economics favor local precision over broad capability.

---

## Suggestions & Future Directions

1. **Parameter-space adaptation.** Current adaptation is prompt-only with a frozen backbone. Tasks requiring genuinely new representations or skills cannot be learned within this constraint. Extending EoM to weight-space training -- fine-tuning agent parameters alongside prompt evolution -- is the most direct capability extension.

2. **Hybrid adaptation regimes.** Combining prompt-space exploration (fast, cheap) with periodic parameter updates (slower, more expressive) could balance sample efficiency against representational flexibility.

3. **Multimodal and embodied agents.** The framework is agnostic to modality. Extending to vision-language agents or embodied environments (robotics, simulators) is a natural next step, though partial observability becomes a harder challenge when agents must also perceive physical state.

4. **Richer economic mechanisms.** The current auction is first-price with fixed bids. Exploring second-price auctions, dynamic bid learning, or more complex market structures (futures, insurance) could yield further theoretical guarantees or empirical gains.

---

## Authors & Institutions

Zhenting Qi (Harvard), Huangyuan Su (Harvard, Kempner Institute), Ao Qu (MIT), Chenyu Wang (Harvard), Yu Yao (MIT), Han Zheng (MIT), Kushal Chattopadhyay (Harvard), Guowei Xu (Harvard), Zihan Wang (2077AI), Weirui Ye (MIT), Vijay Janapa Reddi (Harvard), Ju Li (MIT), Paul Pu Liang (MIT), Himabindu Lakkaraju (Harvard, Kempner Institute), Sham Kakade (Harvard, Kempner Institute), Yilun Du (Harvard, MIT)
