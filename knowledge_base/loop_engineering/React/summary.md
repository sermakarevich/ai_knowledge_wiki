# ReAct: Synergizing Reasoning and Acting in Language Models

**Paper:** [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)

## Human Readable TL;DR

Imagine cooking without ever pausing to think, or thinking endlessly about a recipe without ever touching a pan. Neither works well: pure thinking can invent facts it never checked, and pure acting forgets the bigger goal. ReAct teaches a language-model agent to alternate short written thoughts with real actions — search a page, open a drawer, read what came back — so each thought is grounded in what just happened and each action is guided by a plan. With only a handful of examples, this simple habit fixes hallucination on question-answering tasks and boosts success on simulated household and shopping tasks well past systems trained on thousands of examples.

## TL;DR

ReAct expands an LLM agent's action space to Â = A ∪ L, where L is free-form thoughts that update context with no environment effect, interleaved with task actions a ∈ A that return observations. Reasoning guides acting (decompose goals, track progress, handle exceptions) while acting grounds reasoning (fetch external facts via a Wikipedia API or environment observations). With 1–6 in-context examples on frozen PaLM-540B, ReAct is competitive with chain-of-thought on HotpotQA/FEVER while far more grounded, and beats imitation/RL baselines trained on 10^3–10^5 instances by +34% absolute on ALFWorld and +10% on WebShop. GPT-3 replicates the pattern, human thought-editing rescues failing trajectories with two edits instead of tens of actions, and an implicit-reasoning ablation (ReAct-IM) shows that vague thoughts skip needed subgoals and loop.

---

## Problem & Motivation

Why: chain-of-thought reasoning (CoT) is a static black box — it reasons entirely from parametric memory, so it hallucinates and propagates errors with no way to check or update itself against the world. Act-only planners (SayCan, WebGPT) can query environments but predict actions from language priors alone, with no abstract goal tracking or working memory, so they behave myopically — repeating dead actions or losing the plan. Need: a way to combine the two so reasoning steers interaction and interaction keeps reasoning honest, tested across both knowledge-intensive QA/fact-checking and interactive decision-making. See [[wiki/01-react-method|method]].

---

## Main Original Ideas

1. **Action space augmented with thoughts (Â = A ∪ L)** — At step t the agent sees o_t and acts a_t ~ π(a_t|c_t) with c_t = (o_1,a_1,...,o_t); a thought â_t ∈ L has no environment effect but extends the context to (c_t, â_t), carrying reasoning forward without spending an action.
2. **A reusable thought repertoire** — Goal decomposition and plan drafting, injecting commonsense (where objects live), extracting the salient bit of an observation, tracking progress and switching subgoals, and handling exceptions by revising the plan.
3. **Dense vs. sparse prompting** — Knowledge tasks (HotpotQA, FEVER) use tight thought-action-observation interleaving; long-horizon control (ALFWorld, WebShop) uses sparse, model-placed thoughts only where useful.
4. **Cross-model generality** — The same prompting pattern works on frozen PaLM-540B and GPT-3 (text-davinci-002), with GPT-3 slightly ahead (30.8 vs 29.4 EM on HotpotQA; 78.4% vs 70.9% on ALFWorld).
5. **Human-in-the-loop thought editing** — Because thoughts are just text, a person can delete a hallucinating sentence or add a hint and change downstream behavior — a lever that acting-only or RL-trained policies do not offer.

---

## Key Findings

| Benchmark | Metric | Best baseline | ReAct | Delta |
|---|---|---|---:|---:|
| ALFWorld | success rate | imitation/RL, 10^3–10^5 instances | — | **+34%** absolute |
| WebShop | task score | imitation/RL, 10^3–10^5 instances | — | **+10%** absolute |
| HotpotQA (PaLM-540B) | exact match | CoT (competitive) | 29.4 | grounded via Wikipedia API |
| HotpotQA (GPT-3) | exact match | PaLM-540B ReAct 29.4 | 30.8 | cross-model gain |
| ALFWorld (GPT-3) | success rate | PaLM-540B ReAct 70.9% | 78.4% | cross-model gain |

- On both FEVER and ALFWorld trajectories, ReAct recovers from dead ends (no exact search hit, out-of-order actions) that trip up Act-only baselines, which loop on "Nothing happens" responses.
- ReAct-IM (thoughts limited to bare goal/subgoal naming) still fails: it skips the explicit "clean the knife" subgoal because its vague thought implies the item is already clean, then loops forever.
- ReAct still fails sometimes: reasoning slips (misreading a comparison), search misses (no exact hit for "goddess frigg"), and label ambiguity (Israeli vs. Israel-American) all appear in the appendix taxonomy. See [[wiki/03-appendices-trajectories|appendices]].

---

## Suggestions & Future Directions

1. Scale beyond 1–6-shot prompting via multi-task finetuning and reinforcement learning on more trajectories (finetuning already shows ReAct/Act keep improving with more steps while Standard/CoT degrade).
2. Study human-in-the-loop thought editing systematically as an alignment and behavior-correction mechanism, not just a rescue anecdote.
3. Pair better reasoning with internet-augmented LMs (WebGPT-style) to fix up-to-date-knowledge failures that Act alone cannot solve despite web access.

---

## Authors & Institutions

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao — Princeton University and Google Research (Brain team). arXiv:2210.03629v3 [cs.CL], 10 Mar 2023, CC BY 4.0.
