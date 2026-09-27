> [[index|Wiki]] | [[summary|Summary]]

# React — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-react-method|ReAct method: reason+act interleaving]]

**In one sentence:** ReAct augments an LLM agent's action space with free-form language thoughts interleaved with task actions so reasoning guides acting (plan, track, handle exceptions) and acting grounds reasoning (retrieve external facts), fixing CoT hallucination and Act-only myopia across QA and decision-making tasks.

- ReAct interleaves verbal reasoning traces (thoughts, no environment effect) with task-specific actions and observations, enabling reason-to-act (create, maintain, adjust plans) and act-to-reason (fetch Wikipedia/environment facts into context).
- Human motivation: cooking-style loop of reasoning between actions to track progress, handle exceptions (no salt → soy sauce + pepper), and seek external info (search dough recipe), mirrored by acting (open cookbook/fridge) to support reasoning.
- Diagnosed failures it fixes: CoT (chain-of-thought, Wei et al. 2022) is a static black box prone to hallucination and error propagation, while Act-only planners (SayCan/Ahn et al. 2022, WebGPT/Nakano et al. 2021) predict actions from language priors without abstract goal reasoning or working memory.
- Formal setup: at step t agent sees o_t, acts a_t ~ pi(a_t|c_t) with c_t = (o_1,a_1,...,o_t); ReAct expands to A_hat = A union L where a_hat_t in L updates context to (c_t, a_hat_t) with no observation, composing and carrying information forward.
- Thought repertoire includes goal decomposition + action-plan creation, commonsense injection (where objects live), extracting salient observation bits, progress tracking + plan transition, and exception handling + plan adjustment.
- Headline results (PaLM-540B, 1-2 in-context examples): HotpotQA/Fever competitive with CoT while more grounded via Wikipedia API; ALFWorld +34% absolute and WebShop +10% absolute over imitation/RL trained on 10^3–10^5 instances; trajectories more interpretable and trustworthy.
- Design claims: intuitive (annotators just write thoughts over actions, no ad-hoc formats), general/flexible (dense thought-action-observation for QA, sparse asynchronous thoughts for long-horizon control), performant from 1–6 examples, and human-aligned/controllable (inspectable traces, editable thoughts).

## 2. [[wiki/02-experiments-results|Knowledge-intensive and decision-making experiments]]

**In one sentence:** ReAct prompting generalizes across models (PaLM-540B and GPT-3), retrieves up-to-date knowledge that static labels and reasoning- or acting-only baselines miss, supports human thought-editing for behavior correction, and is backed by fully specified finetuning configs and verbatim HotpotQA, FEVER, WebShop, and ALFWorld prompts.

- GPT-3 (text-davinci-002, greedy decoding) outperforms PaLM-540B with ReAct prompting: 30.8 vs 29.4 exact match on HotpotQA (500-question validation subset) and 78.4% vs 70.9% success rate on ALFWorld (all 134 unseen validation instances), suggesting instruction tuning helps and ReAct works across different large language models.
- ReAct retrieves up-to-date answers (e.g. a hotel-size question whose answer grew after HotpotQA was built) where Standard and CoT hallucinate and Act fails despite web access, because only ReAct combines reasoning to guide interaction with live retrieval.
- Human-in-the-loop thought editing works: removing one hallucinating sentence (Act 17) and adding hints (Act 23) rescues a failing ALFWorld trajectory, turning tens of manual actions into a two-thought edit that changes beliefs, reasoning style, and subsequent actions.
- Finetuning uses batch size 64 everywhere; on PaLM-8B, ReAct/Act train 4,000 steps vs Standard/CoT 2,000 steps, and on PaLM-62B, ReAct/Act train 4,000 steps vs Standard/CoT 1,000 steps, because ReAct/Act benefit from more steps and data while Standard/CoT degrade soon after finetuning starts.
- The ReAct-IM ablation restricts thoughts to dense external-feedback style: only decomposing the current goal and naming the current subgoal, with no thoughts for subgoal completion, next-subgoal selection, or using pretraining knowledge to locate items.
- Verbatim few-shot prompts are fully specified: 6 HotpotQA examples each for Standard/Act/CoT/ReAct with Search/Lookup/Finish and Thought+Action+Observation traces, 3 FEVER claims (SUPPORTS/REFUTES/NOT ENOUGH INFO), a full WebShop deodorant trajectory (search, think, click scent/size/Buy Now), and ALFWorld clean-lettuce trajectories for Act, ReAct, and ReAct-IM.

## 3. [[wiki/03-appendices-trajectories|Appendices: prompts, trajectories, analysis]]

**In one sentence:** The appendices show full ReAct vs Act vs CoT trajectories on FEVER, ALFWorld, and WebShop plus a success/failure-mode taxonomy, demonstrating that interleaved reasoning keeps search grounded and recoverable while Act repeats dead actions, implicit reasoning skips cleaning steps, and both ReAct and CoT still fail via reasoning slips, search misses, hallucinations, and ambiguous labels.

- On FEVER example 2491 (Bermuda Triangle, ground truth REFUTES), ReAct searches, observes "western part of the North Atlantic Ocean", and finishes REFUTES, while CoT answers REFUTES from parametric memory without any search.
- On FEVER example 1951 (Soyuz, ground truth REFUTES), ReAct searches both "Soyuz" and "American space program", finds no link, and conservatively answers NOT ENOUGH INFO, while CoT hallucinates a collaboration story and wrongly answers SUPPORTS.
- On FEVER example 3208 (Reign Over Me, ground truth REFUTES), ReAct reads the observation "American film made in 2007" and correctly answers REFUTES, while Act skips reading the observation and CoT asserts both parts are true, both wrongly answering SUPPORTS.
- On the same ALFWorld task (put a clean knife in countertop), ReAct succeeds by explicitly decomposing find-take-clean-put and visiting cabinets, drawers, and countertops until knife 1 is found on countertop 2, cleaned at sinkbasin 1, and placed on countertop 1, while Act fails by issuing `clean knife 1 with sinkbasin 1` before navigating to the sink and then loops forever on take/clean commands that return "Nothing happens".
- ReAct-IM (implicit reasoning) finds the knife but its vague thought "find and take a clean knife" tricks it into skipping the cleaning step, so it places a dirty knife and then loops `put knife 1 in/on countertop 1` with "Nothing happens" — showing explicit subgoal tracking matters.
- On WebShop (sixteen-pack apple-cinnamon freeze-dried banana chips under $50), Act clicks the first result B0061IVFZE (strawberry banana, pack of 100, $85.0) and buys it for score 0.125, while ReAct reasons over all three results, selects B092JLLYK6, clicks options `apple cinnamon` + `0.53 ounce (pack of 16)`, and buys for score 1.0.
- Appendix E.1 taxonomizes outcomes into true positives (e.g. David Chanoff → William J. Crowe → Bill Clinton), false positives where the answer is right for the wrong reason (e.g. San Marco via a bad About Time lookup), reasoning errors, search errors (e.g. "goddess frigg" returns no exact hit), hallucinations (CoT invents 1916 vs label 1909), and label ambiguity (Israeli vs Israel-American; Psych vs full description).

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Static chain-of-thought reasoning hallucinates while act-only policies lack goal tracking.
2. Interleaving free-form thoughts with actions lets reasoning guide acting and acting ground reasoning.
3. A small reusable thought repertoire covers planning, tracking, extraction, and exception handling.
4. The same prompting pattern wins on HotpotQA/FEVER via Wikipedia search and on ALFWorld/WebShop control.
5. Explicit traces stay interpretable, human-editable, and general across PaLM and GPT-3 models.
<!-- FIVE_MOVES_END -->
