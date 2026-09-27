> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# ReAct method: reason+act interleaving
**In one sentence:** ReAct augments an LLM agent's action space with free-form language thoughts interleaved with task actions so reasoning guides acting (plan, track, handle exceptions) and acting grounds reasoning (retrieve external facts), fixing CoT hallucination and Act-only myopia across QA and decision-making tasks.
## Key points
- ReAct interleaves verbal reasoning traces (thoughts, no environment effect) with task-specific actions and observations, enabling reason-to-act (create, maintain, adjust plans) and act-to-reason (fetch Wikipedia/environment facts into context).
- Human motivation: cooking-style loop of reasoning between actions to track progress, handle exceptions (no salt → soy sauce + pepper), and seek external info (search dough recipe), mirrored by acting (open cookbook/fridge) to support reasoning.
- Diagnosed failures it fixes: CoT (chain-of-thought, Wei et al. 2022) is a static black box prone to hallucination and error propagation, while Act-only planners (SayCan/Ahn et al. 2022, WebGPT/Nakano et al. 2021) predict actions from language priors without abstract goal reasoning or working memory.
- Formal setup: at step t agent sees o_t, acts a_t ~ pi(a_t|c_t) with c_t = (o_1,a_1,...,o_t); ReAct expands to A_hat = A union L where a_hat_t in L updates context to (c_t, a_hat_t) with no observation, composing and carrying information forward.
- Thought repertoire includes goal decomposition + action-plan creation, commonsense injection (where objects live), extracting salient observation bits, progress tracking + plan transition, and exception handling + plan adjustment.
- Headline results (PaLM-540B, 1-2 in-context examples): HotpotQA/Fever competitive with CoT while more grounded via Wikipedia API; ALFWorld +34% absolute and WebShop +10% absolute over imitation/RL trained on 10^3–10^5 instances; trajectories more interpretable and trustworthy.
- Design claims: intuitive (annotators just write thoughts over actions, no ad-hoc formats), general/flexible (dense thought-action-observation for QA, sparse asynchronous thoughts for long-horizon control), performant from 1–6 examples, and human-aligned/controllable (inspectable traces, editable thoughts).
## Abstract: what the paper claims
- Problem split: LLM reasoning (e.g. chain-of-thought prompting) and LLM acting (e.g. action-plan generation) studied separately; ReAct generates both in one interleaved stream for synergy.
- Mechanism: reasoning traces induce, track, and update action plans and handle exceptions; actions interface with knowledge bases/environments to gather extra information.
- QA/fact results: on HotpotQA and Fever, ReAct overcomes CoT hallucination and error propagation by interacting with a simple Wikipedia API, producing human-like trajectories more interpretable than no-reasoning baselines.
- Decision results: on ALFWorld and WebShop, ReAct beats imitation and reinforcement learning by 34% and 10% absolute success rate with only one or two in-context examples.
- Paper metadata: ReAct: Synergizing Reasoning and Acting in Language Models, Yao et al. (Princeton + Google Research, Brain team), arXiv:2210.03629v3 [cs.CL], 10 Mar 2023, CC BY 4.0.
## 1 Introduction: motivation and gaps
- Human intelligence seamlessly combines task actions with verbal reasoning (inner speech; Alderson-Day & Fernyhough 2015; Vygotsky 1987; Luria 1965; Fernyhough 2010; Baddeley 1992 working memory) for self-regulation, strategization, and memory maintenance.
- Kitchen example: between cuts and heating water, we reason ("now everything is cut, heat the pot"), adapt ("no salt → soy sauce and pepper"), seek info ("how to prepare dough? search Internet"), and act (open cookbook/fridge, check ingredients) to answer "what can I make now?".
- LLM reasoning side: properly prompted LLMs show emergent multi-step reasoning traces on arithmetic/commonsense/symbolic tasks (Wei et al. 2022), but CoT is ungrounded in the outside world — cannot react or update knowledge, causing hallucination and error propagation (Figure 1(1b)).
- LLM acting side: models convert multimodal observations to text, generate domain actions/plans, execute via controller (Ahn et al. 2022; Nakano et al. 2021; Yao et al. 2020; Huang et al. 2022a), but do not abstractly reason about goals or keep working memory — except Huang et al. 2022b's limited reiteration of spatial facts.
- Gap: beyond block-manipulation toys, no study of synergistic reasoning+acting for general task solving or whether the combination systematically beats either alone.
## Figure 1: four paradigms compared
- (1a) Standard prompting: direct answer, no trace.
- (1b) Chain-of-thought / Reason Only: internal reasoning chain, then answer; hallucinates without grounding.
- (1c) Act-only: sequence of Wikipedia or household actions + observations only; fails HotpotQA Act 4 (needs complex reasoning over Q + Acts 1–3 + Obs 1–3) and ALFWorld (misses sinkbasin 1 lacks peppershaker 1, loops hallucinated actions).
- (1d)/(2b) ReAct (Reason+Act): Thought–Act–Obs interleaving for HotpotQA; sparse thoughts + actions for AlfWorld; in-context examples omitted in figure, only generated (Act, Thought) and environment (Obs) shown.
## 1 Contributions and evaluation sketch
- (1) Novel prompt-based paradigm synergizing reasoning and acting for general task solving.
- (2) Few-shot experiments on four benchmarks: HotPotQA (Yang et al. 2018), Fever (Thorne et al. 2018), ALFWorld (Shridhar et al. 2020b), WebShop (Yao et al. 2022).
- (3) Ablations/analysis of acting-in-reasoning and reasoning-in-acting value.
- (4) Analysis of prompting-setup limits plus initial finetuning showing growth with training data; future: scale multi-task training + RL.
- QA finding preview: with Wikipedia API, ReAct beats vanilla action generation, ties CoT; best overall is ReAct+CoT hybrid using internal and external knowledge.
- Decision finding preview: 1–2-shot ReAct beats IL/RL trained on 10^3–10^5 instances (+34% ALFWorld, +10% WebShop); sparse versatile reasoning beats Act-only controls.
- Interpretability claim: humans can separate internal knowledge from external observations and read traces to audit action basis — trustworthiness/diagnosability gain in all domains.
## 2 Method: reasoning + acting formalism
- Agent loop: at time t receive o_t in O, take a_t in A from pi(a_t|c_t), c_t = (o_1,a_1,...,o_{t-1},a_{t-1},o_t); learning c_t → a_t is hard when mapping is implicit and compute-heavy.
- Augmentation: A_hat = A union L; a_hat_t in L is a thought/reasoning trace with no environment effect and no observation; it reasons over c_t and extends context to c_{t+1} = (c_t, a_hat_t) for future steps.
- Thought types (Figure 1 examples): decompose goals + draft plans (2b Act 1; 1d Thought 1), inject task commonsense (2b Act 1), extract observation essentials (1d Thoughts 2, 4), track progress + shift plans (2b Act 8), handle exceptions + revise plans (1d Thought 3).
- Learning difficulty: L is unbounded, needs strong language priors — hence frozen-LLM prompting focus.
## 2 Prompting setup: dense vs sparse thoughts
- Base model: frozen PaLM-540B (Chowdhery et al. 2022); some GPT-3 (Brown et al. 2020) results in Appendix A.1, reported as outperforming PaLM-540B.
- In-context examples: human trajectories of actions + thoughts + observations (Appendix C); 1–6 examples total per task.
- Knowledge-reasoning tasks (Figure 1(1)): alternate thought and action → dense multi-step thought-action-observation chains.
- Long-horizon decision tasks (Figure 1(2)): thoughts appear sparsely only at relevant points; model decides asynchronous placement itself.
## 2 Features A–D claimed
- A) Intuitive/easy to design: annotators type thoughts atop actions; no ad-hoc format, thought design, or example selection; per-task prompt details in Sections 3–4.
- B) General/flexible: one thought space + flexible occurrence covers QA, fact verification, text games, web navigation with distinct action spaces.
- C) Performant/robust: 1–6 examples generalize to new instances, consistently beating reason-only or act-only across domains; finetuning gains (Section 3) and prompt robustness (Section 4) shown later.
- D) Human-aligned/controllable: interpretable sequential traces expose factual correctness; humans can intervene via thought editing (Figure 5, Section 4).
**Covers:** chunk 01: sections 1-2
